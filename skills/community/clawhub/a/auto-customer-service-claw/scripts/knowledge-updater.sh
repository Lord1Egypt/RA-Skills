#!/bin/bash
# 自动客服应答虾 - 知识库更新脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
FAQ_FILE="$SKILL_DIR/references/faq-database.md"

import_faq() {
    local file="$1"
    
    if [ -z "$file" ]; then
        echo "用法: $0 import --file <文件路径>"
        echo "支持格式: .xlsx, .csv, .md"
        return 1
    fi
    
    if [ ! -f "$file" ]; then
        echo "❌ 文件不存在: $file"
        return 1
    fi
    
    ext="${file##*.}"
    
    case "$ext" in
        xlsx)
            echo "从 Excel 导入 FAQ..."
            python3 -c "
import sys
try:
    import openpyxl
except ImportError:
    print('❌ 需要安装 openpyxl: pip install openpyxl')
    sys.exit(1)

wb = openpyxl.load_workbook('$file')
ws = wb.active
output = []

for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] and row[1]:  # 问题, 答案
        output.append(f'**Q: {row[0]}**')
        output.append(f'A: {row[1]}')
        output.append('')

with open('$FAQ_FILE', 'a', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f'✅ 已导入 {len(output)//3} 条 FAQ')
"
            ;;
        csv)
            echo "从 CSV 导入 FAQ..."
            python3 -c "
import csv, sys

output = []
with open('$file', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        q = row.get('问题') or row.get('question') or ''
        a = row.get('答案') or row.get('answer') or ''
        if q and a:
            output.append(f'**Q: {q}**')
            output.append(f'A: {a}')
            output.append('')
            count += 1

with open('$FAQ_FILE', 'a', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f'✅ 已导入 {count} 条 FAQ')
"
            ;;
        md)
            echo "从 Markdown 导入 FAQ..."
            cat "$file" >> "$FAQ_FILE"
            echo "✅ 已追加到知识库"
            ;;
        *)
            echo "❌ 不支持的文件格式: .$ext"
            echo "支持格式: .xlsx, .csv, .md"
            return 1
            ;;
    esac
}

export_faq() {
    local output="$1"
    
    if [ -z "$output" ]; then
        output="faq_export_$(date +%Y%m%d_%H%M%S).md"
    fi
    
    echo "导出知识库到: $output"
    cp "$FAQ_FILE" "$output"
    echo "✅ 导出完成"
}

backup_faq() {
    local backup_dir="$SKILL_DIR/references/backups"
    mkdir -p "$backup_dir"
    
    local backup_file="$backup_dir/faq-database_$(date +%Y%m%d_%H%M%S).md"
    cp "$FAQ_FILE" "$backup_file"
    echo "✅ 已备份到: $backup_file"
}

case "$1" in
    import)
        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --file)
                    import_faq "$2"
                    shift 2
                    ;;
                *)
                    echo "未知参数: $1"
                    exit 1
                    ;;
            esac
        done
        ;;
    export)
        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --output)
                    export_faq "$2"
                    shift 2
                    ;;
                *)
                    echo "未知参数: $1"
                    exit 1
                    ;;
            esac
        done
        ;;
    backup)
        backup_faq
        ;;
    *)
        echo "用法: $0 {import|export|backup}"
        echo ""
        echo "命令说明:"
        echo "  import --file <文件>    从文件导入 FAQ（支持 .xlsx, .csv, .md）"
        echo "  export --output <文件>  导出知识库到文件"
        echo "  backup                  备份当前知识库"
        echo ""
        echo "示例:"
        echo "  $0 import --file faq.xlsx"
        echo "  $0 export --output current_faq.md"
        echo "  $0 backup"
        exit 1
        ;;
esac
