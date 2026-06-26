#!/bin/bash
#
# 🛡️ agent-defender 备份管理脚本
# =================================
#
# 功能:
# - 创建规则备份
# - 压缩归档
# - 生成索引清单
# - 恢复备份
# - 清理旧备份
#
# 使用:
#   ./backup_manager.sh backup    # 创建备份
#   ./backup_manager.sh list      # 列出备份
#   ./backup_manager.sh restore   # 恢复备份
#   ./backup_manager.sh clean     # 清理旧备份
#

set -e

# 配置
BACKUP_BASE_DIR="$(dirname "$0")/backups"
RULES_DIR="$(dirname "$0")/rules"
INTEGRATED_RULES_DIR="$(dirname "$0")/integrated_rules"
INDEX_FILE="$BACKUP_DIR/backup_index.json"
MAX_BACKUPS=10  # 保留最近 10 个备份

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印信息
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

error() {
    echo -e "${RED}[❌]${NC} $1"
}

# 创建备份
create_backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$BACKUP_BASE_DIR/$timestamp"
    local notes="${1:-自动备份}"
    
    info "创建备份..."
    info "时间戳：$timestamp"
    info "备份目录：$backup_dir"
    
    # 创建备份目录
    mkdir -p "$backup_dir"
    
    # 备份规则文件
    if [ -d "$RULES_DIR" ]; then
        cp -r "$RULES_DIR" "$backup_dir/"
        success "已备份 rules/ 目录"
    else
        warning "rules/ 目录不存在"
    fi
    
    if [ -d "$INTEGRATED_RULES_DIR" ]; then
        cp -r "$INTEGRATED_RULES_DIR" "$backup_dir/"
        success "已备份 integrated_rules/ 目录"
    else
        warning "integrated_rules/ 目录不存在"
    fi
    
    # 备份 Python 脚本
    for file in *.py; do
        if [ -f "$file" ]; then
            cp "$file" "$backup_dir/"
        fi
    done
    success "已备份 Python 脚本"
    
    # 备份配置文件
    if [ -d "config" ]; then
        cp -r "config" "$backup_dir/"
        success "已备份 config/ 目录"
    fi
    
    # 统计规则数量
    local rules_count=0
    if [ -d "$backup_dir/rules" ]; then
        rules_count=$(ls -1 "$backup_dir/rules"/*.json 2>/dev/null | wc -l)
    fi
    
    # 生成清单
    cat > "$backup_dir/manifest.json" <<EOF
{
  "backup_time": "$(date -Iseconds)",
  "timestamp": "$timestamp",
  "rules_count": $rules_count,
  "notes": "$notes",
  "files": [
$(ls -1 "$backup_dir"/*.* 2>/dev/null | xargs -I {} basename {} | sed 's/^/    "/' | sed 's/$/",/' | sed '$ s/,$//')
  ]
}
EOF
    success "已生成 manifest.json"
    
    # 压缩备份
    cd "$BACKUP_BASE_DIR"
    tar -czf "$timestamp.tar.gz" "$timestamp"
    cd - > /dev/null
    success "已压缩备份：$timestamp.tar.gz"
    
    # 移除未压缩的备份目录
    rm -rf "$backup_dir"
    
    # 更新索引
    update_index "$timestamp" "$rules_count" "$notes"
    
    # 显示备份信息
    echo ""
    info "备份信息:"
    echo "  文件：$BACKUP_BASE_DIR/$timestamp.tar.gz"
    echo "  大小：$(du -h "$BACKUP_BASE_DIR/$timestamp.tar.gz" | cut -f1)"
    echo "  规则数：$rules_count"
    echo "  备注：$notes"
    
    success "备份完成!"
}

# 更新索引
update_index() {
    local timestamp="$1"
    local rules_count="$2"
    local notes="$3"
    
    # 创建索引文件 (如果不存在)
    if [ ! -f "$INDEX_FILE" ]; then
        cat > "$INDEX_FILE" <<EOF
{
  "backups": []
}
EOF
    fi
    
    # 添加新备份到索引
    local new_entry=$(cat <<EOF
  {
    "timestamp": "$(date -Iseconds)",
    "archive": "$timestamp.tar.gz",
    "rules_count": $rules_count,
    "notes": "$notes"
  }
EOF
)
    
    # 使用 Python 更新 JSON (更可靠)
    python3 <<EOF
import json

with open('$INDEX_FILE', 'r') as f:
    data = json.load(f)

new_entry = {
    "timestamp": "$(date -Iseconds)",
    "archive": "$timestamp.tar.gz",
    "rules_count": $rules_count,
    "notes": "$notes"
}

data['backups'].append(new_entry)

# 保留最近 MAX_BACKUPS 个备份
if len(data['backups']) > $MAX_BACKUPS:
    data['backups'] = data['backups'][-$MAX_BACKUPS:]

with open('$INDEX_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"已更新索引，当前 {len(data['backups'])} 个备份")
EOF
}

# 列出备份
list_backups() {
    info "可用备份:"
    echo ""
    
    if [ ! -f "$INDEX_FILE" ]; then
        warning "暂无备份记录"
        return
    fi
    
    python3 <<EOF
import json
from datetime import datetime

with open('$INDEX_FILE', 'r') as f:
    data = json.load(f)

backups = data.get('backups', [])

if not backups:
    print("暂无备份")
else:
    print(f"{'序号':<6} {'时间':<22} {'规则数':<8} {'大小':<10} {'备注'}")
    print("-" * 70)
    
    for i, backup in enumerate(backups, 1):
        timestamp = backup.get('timestamp', 'N/A')[:19].replace('T', ' ')
        rules = backup.get('rules_count', 0)
        notes = backup.get('notes', '')[:30]
        archive = backup.get('archive', '')
        
        # 获取文件大小
        size = 'N/A'
        try:
            import os
            size_bytes = os.path.getsize(f'$BACKUP_BASE_DIR/{archive}')
            if size_bytes < 1024:
                size = f'{size_bytes}B'
            elif size_bytes < 1024*1024:
                size = f'{size_bytes/1024:.1f}K'
            else:
                size = f'{size_bytes/(1024*1024):.1f}M'
        except:
            pass
        
        print(f"{i:<6} {timestamp:<22} {rules:<8} {size:<10} {notes}")

print(f"\n总计：{len(backups)} 个备份")
EOF
}

# 恢复备份
restore_backup() {
    local backup_num="$1"
    
    if [ -z "$backup_num" ]; then
        error "请指定备份序号"
        echo "使用 ./backup_manager.sh list 查看可用备份"
        exit 1
    fi
    
    info "恢复备份 #$backup_num..."
    
    python3 <<EOF
import json
import os
import tarfile
import sys

with open('$INDEX_FILE', 'r') as f:
    data = json.load(f)

backups = data.get('backups', [])

if not backups or int('$backup_num') > len(backups):
    print(f"❌ 无效的备份序号：$backup_num")
    print(f"可用备份数：{len(backups)}")
    sys.exit(1)

backup = backups[int('$backup_num') - 1]
archive = backup.get('archive')
backup_dir = archive.replace('.tar.gz', '')

print(f"准备恢复:")
print(f"  文件：$BACKUP_BASE_DIR/$archive")
print(f"  时间：{backup.get('timestamp', 'N/A')}")
print(f"  规则数：{backup.get('rules_count', 0)}")
print(f"  备注：{backup.get('notes', '')}")
print()

confirm = input("确认恢复？(y/n): ")
if confirm.lower() != 'y':
    print("取消恢复")
    sys.exit(0)

# 解压备份
try:
    with tarfile.open(f'$BACKUP_BASE_DIR/$archive', 'r:gz') as tar:
        tar.extractall(path='$BACKUP_BASE_DIR/')
    
    # 恢复规则文件
    extracted_dir = f'$BACKUP_BASE_DIR/{backup_dir}'
    
    if os.path.exists(f'{extracted_dir}/rules'):
        import shutil
        if os.path.exists('rules'):
            # 备份当前规则
            shutil.move('rules', 'rules.backup')
            print("✅ 已备份当前 rules/ 为 rules.backup/")
        
        shutil.copytree(f'{extracted_dir}/rules', 'rules')
        print("✅ 已恢复 rules/ 目录")
    
    if os.path.exists(f'{extracted_dir}/integrated_rules'):
        import shutil
        if os.path.exists('integrated_rules'):
            shutil.move('integrated_rules', 'integrated_rules.backup')
        
        shutil.copytree(f'{extracted_dir}/integrated_rules', 'integrated_rules')
        print("✅ 已恢复 integrated_rules/ 目录")
    
    print("\n✅ 恢复完成!")
    print("⚠️  建议运行测试验证:")
    print("   python3 scanner_v2.py")
    
except Exception as e:
    print(f"❌ 恢复失败：{e}")
    sys.exit(1)
EOF
}

# 清理旧备份
clean_backups() {
    info "清理旧备份..."
    
    python3 <<EOF
import json
import os

with open('$INDEX_FILE', 'r') as f:
    data = json.load(f)

backups = data.get('backups', [])

if len(backups) <= $MAX_BACKUPS:
    print(f"当前备份数 ({len(backups)}) 未超过限制 ($MAX_BACKUPS)，无需清理")
else:
    old_backups = backups[:-$MAX_BACKUPS]
    
    print(f"将删除 {len(old_backups)} 个旧备份:")
    for backup in old_backups:
        print(f"  - {backup.get('archive')}")
    
    confirm = input("\n确认删除？(y/n): ")
    if confirm.lower() != 'y':
        print("取消删除")
        exit(0)
    
    # 删除旧备份文件
    for backup in old_backups:
        archive = backup.get('archive')
        archive_path = f'$BACKUP_BASE_DIR/{archive}'
        if os.path.exists(archive_path):
            os.remove(archive_path)
            print(f"✅ 已删除：{archive}")
    
    # 更新索引
    data['backups'] = backups[-$MAX_BACKUPS:]
    with open('$INDEX_FILE', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 清理完成，保留 {len(data['backups'])} 个备份")
EOF
}

# 显示帮助
show_help() {
    cat <<EOF
🛡️ agent-defender 备份管理脚本

使用:
  $0 backup [备注]    创建备份
  $0 list             列出所有备份
  $0 restore <序号>   恢复指定备份
  $0 clean            清理旧备份
  $0 help             显示帮助

示例:
  $0 backup "集成 Scanner v4.1.0"  # 创建带备注的备份
  $0 list                          # 查看所有备份
  $0 restore 3                     # 恢复第 3 个备份
  $0 clean                         # 清理旧备份 (保留最近 10 个)

配置:
  备份目录：$BACKUP_BASE_DIR
  索引文件：$INDEX_FILE
  最大保留：$MAX_BACKUPS 个备份

EOF
}

# 主程序
case "${1:-help}" in
    backup)
        create_backup "${2:-自动备份}"
        ;;
    list)
        list_backups
        ;;
    restore)
        restore_backup "$2"
        ;;
    clean)
        clean_backups
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        error "未知命令：$1"
        show_help
        exit 1
        ;;
esac
