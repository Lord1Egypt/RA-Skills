# -*- coding: utf-8 -*-
"""
Color-Filer 文件重命名脚本（安全版）

⚠️ 安全特性：
1. 默认 dry_run=True（仅预览，不修改文件）
2. 目标路径安全验证（拒绝系统目录）
3. 冲突检测与自动处理
4. 可选备份功能
"""

import os
import sys
import shutil
import re
from datetime import datetime

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ==================== 安全配置 ====================

# 禁止处理的危险路径（Windows 和 Linux/Mac）
DANGEROUS_PATHS = [
    # Windows 系统目录
    r'C:\Windows',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\ProgramData',
    r'C:\Users\All Users',
    r'C:\Users\Default',
    r'C:\Users\Public',
    # Linux/Mac 系统目录
    '/root',
    '/bin',
    '/sbin',
    '/usr/bin',
    '/usr/sbin',
    '/usr/local/bin',
    '/System',
    '/etc',
    '/var',
]

# ==================== 表情符号配置 ====================

# 表情符号分类对照表
EMOJI_CATEGORIES = {
    # 🔴 红色系
    'core': '🔴',
    'warning': '🚨',
    'hot': '🔥',
    'favorite': '❤️',
    'emergency': '🧯',

    # 🟠 橙色系
    'tool': '🟠',
    'config': '⚙️',
    'utility': '🛠️',
    'toolbox': '🧰',
    'tweak': '🪛',

    # 🟡 黄色系
    'learning': '🟡',
    'draft': '✏️',
    'note': '📝',
    'idea': '💡',
    'course': '📒',

    # 🟢 绿色系
    'stable': '🟢',
    'ready': '✅',
    'status': '🟩',
    'growing': '🌱',
    'module': '🧩',

    # 🔵 蓝色系
    'tech': '🔵',
    'dev': '💻',
    'doc': '📚',
    'debug': '🔍',
    'algo': '🧠',

    # 🟣 紫色系
    'advanced': '🟣',
    'magic': '✨',
    'test': '🧪',
    'speed': '🚀',
    'innovation': '🧬',

    # ⚫⚪ 黑白系
    'old': '⚫',
    'generic': '⚪',
    'package': '📦',
    'archive': '🗄️',
    'log': '🧾',
}

# 文件类型分类规则
FILE_CATEGORY_RULES = {
    # 脚本类
    '.py': ('dev', '开发'),
    '.bat': ('core', '核心脚本'),
    '.sh': ('core', '核心脚本'),
    '.ps1': ('tool', '工具'),
    '.js': ('dev', '开发'),

    # 文档类
    '.md': ('note', '笔记'),
    '.txt': ('note', '笔记'),
    '.pdf': ('doc', '文档'),
    '.doc': ('doc', '文档'),
    '.docx': ('doc', '文档'),

    # 配置类
    '.ini': ('config', '配置'),
    '.conf': ('config', '配置'),
    '.yaml': ('config', '配置'),
    '.yml': ('config', '配置'),
    '.json': ('config', '配置'),
    '.toml': ('config', '配置'),
    '.xml': ('config', '配置'),

    # 压缩包
    '.zip': ('package', '压缩包'),
    '.rar': ('package', '压缩包'),
    '.tar': ('package', '压缩包'),
    '.gz': ('package', '压缩包'),
    '.7z': ('package', '压缩包'),

    # 图片
    '.jpg': ('generic', '图片'),
    '.jpeg': ('generic', '图片'),
    '.png': ('generic', '图片'),
    '.svg': ('generic', '图片'),
    '.gif': ('generic', '图片'),
    '.webp': ('generic', '图片'),

    # 数据表
    '.xlsx': ('note', '数据表'),
    '.xls': ('note', '数据表'),
    '.csv': ('note', '数据表'),

    # 演示文稿
    '.pptx': ('doc', '演示文稿'),
    '.ppt': ('doc', '演示文稿'),

    # 其他
    '.mmap': ('algo', '思维导图'),
}

# ==================== 安全函数 ====================

def validate_target_path(target_path):
    """
    验证目标路径是否安全

    Returns:
        tuple: (is_safe, reason)
    """
    # 规范化路径
    target_path = os.path.abspath(target_path)

    # 检查是否在危险路径列表中
    for dangerous_path in DANGEROUS_PATHS:
        dangerous_path = os.path.abspath(dangerous_path)
        if target_path == dangerous_path or target_path.startswith(dangerous_path + os.sep):
            return False, f"禁止处理系统目录: {dangerous_path}"

    # 检查路径是否存在
    if not os.path.exists(target_path):
        return False, f"路径不存在: {target_path}"

    # 检查是否为目录
    if not os.path.isdir(target_path):
        return False, f"不是目录: {target_path}"

    return True, "路径安全"


def check_dry_run_warning(dry_run):
    """如果非 dry_run 模式，显示警告"""
    if not dry_run:
        print('\n' + '=' * 60)
        print('⚠️  警告：非预演模式（dry_run=False）')
        print('⚠️  将实际修改文件，建议先使用 --dry-run 测试')
        print('=' * 60 + '\n')
        return True
    return False


# ==================== 核心功能函数 ====================

def analyze_directory(target_path):
    """分析目录结构，生成命名建议"""
    print(f'\n📂 分析目录: {target_path}\n')
    print('=' * 60)

    # 安全验证
    is_safe, reason = validate_target_path(target_path)
    if not is_safe:
        print(f'❌ 安全检查失败: {reason}')
        print('❌ 操作已取消')
        sys.exit(1)

    print(f'✅ 安全检查通过: {reason}\n')

    # 统计信息
    file_list = []
    dir_list = []

    for root, dirs, files in os.walk(target_path):
        for f in files:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path):
                ext = os.path.splitext(f)[1].lower()
                file_list.append({
                    'path': full_path,
                    'name': f,
                    'ext': ext,
                    'size': os.path.getsize(full_path),
                    'dir': os.path.basename(root)
                })

        for d in dirs:
            full_path = os.path.join(root, d)
            dir_list.append({
                'path': full_path,
                'name': d
            })

    # 输出统计
    print(f'📊 文件总数: {len(file_list)}')
    print(f'📁 目录总数: {len(dir_list)}')

    # 按扩展名统计
    ext_stats = {}
    for f in file_list:
        ext = f['ext']
        ext_stats[ext] = ext_stats.get(ext, 0) + 1

    print('\n📋 文件类型分布（Top 10）:')
    sorted_ext = sorted(ext_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    for ext, count in sorted_ext:
        emoji = EMOJI_CATEGORIES.get('generic', '📄')
        print(f'  {emoji} {ext or "无扩展名"}: {count} 个')

    # 检测未使用表情符号的文件
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]"
    )

    untagged_count = sum(1 for f in file_list if not emoji_pattern.search(f['name']))
    print(f'\n⚠️  未使用表情符号的文件: {untagged_count} 个')

    return file_list, dir_list


def generate_naming_suggestions(files):
    """生成命名建议"""
    suggestions = []

    # 按类型分组
    typed_files = {}
    for f in files:
        ext = f['ext']
        if ext not in typed_files:
            typed_files[ext] = []
        typed_files[ext].append(f)

    # 生成建议
    for ext, file_list in typed_files.items():
        if ext in FILE_CATEGORY_RULES:
            category_key, category_name = FILE_CATEGORY_RULES[ext]
            emoji = EMOJI_CATEGORIES.get(category_key, '📄')

            # 确定序号位数
            num_digits = 2 if len(file_list) < 100 else 3

            for i, f in enumerate(file_list, 1):
                old_name = f['name']
                base_name = os.path.splitext(old_name)[0]

                # 生成新文件名
                num_str = f'{i:0{num_digits}d}'
                new_name = f'{emoji}_{num_str}_{base_name}{ext}'

                suggestions.append({
                    'old': old_name,
                    'new': new_name,
                    'category': category_name,
                    'dir': f['dir']
                })

    return suggestions


def rename_files(target_path, mapping, dry_run=True):
    """执行文件重命名"""
    mode_str = "[预演模式]" if dry_run else "[执行模式]"
    print(f'\n🔄 {mode_str}批量重命名\n')
    print('=' * 60)

    success_count = 0
    fail_count = 0
    conflicts = []

    for item in mapping:
        old_path = os.path.join(target_path, item['dir'], item['old'])
        new_name = item['new']
        new_path = os.path.join(target_path, item['dir'], new_name)

        # 检查旧文件是否存在
        if not os.path.exists(old_path):
            print(f'⚠️  跳过（不存在）: {item["old"]}')
            fail_count += 1
            continue

        # 检查新文件是否已存在
        if os.path.exists(new_path):
            # 冲突处理：追加序号
            counter = 1
            while True:
                parts = new_name.rsplit('.', 1)
                conflict_name = f'{parts[0]}_{counter}.{parts[1]}'
                conflict_path = os.path.join(target_path, item['dir'], conflict_name)
                if not os.path.exists(conflict_path):
                    new_name = conflict_name
                    new_path = conflict_path
                    print(f'⚠️  命名冲突，已调整为: {conflict_name}')
                    break
                counter += 1

            conflicts.append({
                'original': item['new'],
                'adjusted': new_name
            })

        if not dry_run:
            try:
                os.rename(old_path, new_path)
                print(f'✅ {item["old"]} → {new_name}')
                success_count += 1
            except Exception as e:
                print(f'❌ 失败: {item["old"]} - {str(e)}')
                fail_count += 1
        else:
            print(f'[DRY] {item["old"]} → {new_name}')
            success_count += 1

    # 输出统计
    print('\n📊 操作统计:')
    print(f'  ✅ 成功: {success_count}')
    print(f'  ❌ 失败: {fail_count}')
    print(f'  ⚠️  冲突: {len(conflicts)}')

    if conflicts:
        print('\n⚠️  命名冲突详情:')
        for c in conflicts:
            print(f'    {c["original"]} → {c["adjusted"]}')

    if dry_run:
        print('\n💡 提示: 当前为预演模式，未实际修改文件')
        print('💡 如需执行实际重命名，请设置 dry_run=False 并重新运行')

    return success_count, fail_count, len(conflicts)


def create_backup(target_path):
    """创建目录备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'{os.path.basename(target_path)}_backup_{timestamp}'
    backup_path = os.path.join(os.path.dirname(target_path), backup_name)

    if os.path.exists(backup_path):
        print(f'⚠️  备份已存在: {backup_path}')
        return backup_path

    print(f'💾 创建备份: {backup_path}')
    try:
        shutil.copytree(target_path, backup_path)
        print(f'✅ 备份成功')
        return backup_path
    except Exception as e:
        print(f'❌ 备份失败: {e}')
        return None


# ==================== 命令行入口 ====================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Color-Filer: 智能文件夹整理与重命名工具（安全版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析目录（只读）
  python rename_files.py "F:\\笔记"

  # 预览重命名（Dry-Run 模式，推荐）
  python rename_files.py "F:\\笔记" --dry-run

  # 执行实际重命名（需先测试）
  python rename_files.py "F:\\笔记" --rename
        """
    )
    parser.add_argument('target', help='目标目录路径')
    parser.add_argument('--dry-run', action='store_true', help='预演模式（默认），不实际重命名')
    parser.add_argument('--rename', action='store_true', help='执行实际重命名（需先测试）')
    parser.add_argument('--no-backup', action='store_true', help='不创建备份')

    args = parser.parse_args()

    # 默认 dry_run=True
    dry_run = not args.rename

    # 分析目录
    files, dirs = analyze_directory(args.target)

    if files is None:
        sys.exit(1)

    # 如果有文件需要重命名
    mapping = generate_naming_suggestions(files)

    if not mapping:
        print('\n✅ 没有需要重命名的文件')
        sys.exit(0)

    # 显示非 dry_run 警告
    check_dry_run_warning(dry_run)

    # 执行重命名
    if args.rename and not dry_run:
        if not args.no_backup:
            backup = create_backup(args.target)
            if backup is None:
                print('❌ 备份失败，取消操作')
                sys.exit(1)

    rename_files(args.target, mapping, dry_run=dry_run)
