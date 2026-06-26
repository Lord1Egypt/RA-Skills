#!/bin/bash
# SVN 提交记录导出脚本（增强版 - 支持提交日志）
# 用法: ./export_svn_commits.sh [作者] [起始修订号] [结束修订号] [输出格式] [项目路径] [用户名] [密码]

set -e

# 参数解析
AUTHOR="${1:-}"
START_REV="${2:-}"
END_REV="${3:-HEAD}"
FORMAT="${4:-markdown}"  # markdown, csv, json, detailed
PROJECT_PATH="${5:-$(pwd)}"
SVN_USER="${6:-}"
SVN_PASS="${7:-}"

# 输出文件名
OUTPUT_FILE="svn_commits_${AUTHOR:-all}_$(date +%Y%m%d_%H%M%S).${FORMAT}"

# 切换到项目目录
cd "$PROJECT_PATH" 2>/dev/null || { echo "错误: 项目路径不存在"; exit 1; }

# 检查是否为 SVN 仓库
if [ ! -d ".svn" ]; then
    echo "错误: 当前目录不是 SVN 仓库"
    exit 1
fi

echo "=== SVN 提交记录导出（增强版） ==="
echo "作者: ${AUTHOR:-所有}"
echo "修订号范围: ${START_REV:-无限制} ~ ${END_REV}"
echo "输出格式: $FORMAT"
echo "项目路径: $PROJECT_PATH"
echo ""

# 构建认证参数
AUTH_ARGS=""
if [ -n "$SVN_USER" ]; then
    AUTH_ARGS="--username \"$SVN_USER\""
fi
if [ -n "$SVN_PASS" ]; then
    AUTH_ARGS="$AUTH_ARGS --password \"$SVN_PASS\""
fi

# 尝试获取提交日志（需要认证）
if [ -n "$AUTH_ARGS" ]; then
    echo "使用认证获取提交日志..."
    SVN_LOG_AVAILABLE=true
else
    echo "检查是否可以获取提交日志（无认证）..."
    if svn log -l 1 2>/dev/null; then
        SVN_LOG_AVAILABLE=true
    else
        SVN_LOG_AVAILABLE=false
        echo "⚠️  无法从服务器获取提交日志，需要认证"
        echo "   将使用本地工作副本数据库获取基本信息"
    fi
fi

# 根据输出格式生成报告
case "$FORMAT" in
    detailed)
        # 详细报告（包含提交日志）
        if [ "$SVN_LOG_AVAILABLE" = true ]; then
            echo "# SVN 详细提交记录报告" > "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "**作者**: ${AUTHOR:-所有}" >> "$OUTPUT_FILE"
            echo "**项目路径**: $PROJECT_PATH" >> "$OUTPUT_FILE"
            echo "**导出时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "---" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            
            # 获取日志并解析
            eval svn log $AUTH_ARGS -r ${START_REV:-1}:${END_REV} -v | while IFS= read -r line; do
                if [[ $line =~ ^r([0-9]+)\|([^\|]+)\|([^\|]+)\| ]]; then
                    rev="${BASH_REMATCH[1]}"
                    author="${BASH_REMATCH[2]}"
                    date_str="${BASH_REMATCH[3]}"
                    
                    # 过滤作者
                    if [ -n "$AUTHOR" ] && [[ ! "$author" =~ $AUTHOR ]]; then
                        continue
                    fi
                    
                    echo "## 修订版本: r${rev}" >> "$OUTPUT_FILE"
                    echo "" >> "$OUTPUT_FILE"
                    echo "- **作者**: $author" >> "$OUTPUT_FILE"
                    echo "- **日期**: $date_str" >> "$OUTPUT_FILE"
                    echo "" >> "$OUTPUT_FILE"
                    
                    # 读取提交消息
                    message=""
                    while IFS= read -r msg_line; do
                        if [[ -z "$msg_line" ]] || [[ "$msg_line" =~ ^Changed\ paths: ]]; then
                            break
                        fi
                        if [ -n "$msg_line" ]; then
                            message="$message $msg_line"
                        fi
                    done
                    
                    if [ -n "$message" ]; then
                        echo "- **提交日志**: $message" >> "$OUTPUT_FILE"
                        echo "" >> "$OUTPUT_FILE"
                    fi
                    
                    echo "### 修改文件" >> "$OUTPUT_FILE"
                    echo "" >> "$OUTPUT_FILE"
                    
                    # 读取修改文件列表
                    while IFS= read -r file_line; do
                        if [[ -z "$file_line" ]]; then
                            break
                        fi
                        if [[ $file_line =~ ^[A|M|D|R]\s(.+) ]]; then
                            file="${BASH_REMATCH[1]}"
                            action="${file_line:0:1}"
                            
                            case "$action" in
                                A) echo "- ✅ 新增: $file" >> "$OUTPUT_FILE" ;;
                                M) echo "- ✏️ 修改: $file" >> "$OUTPUT_FILE" ;;
                                D) echo "- ❌ 删除: $file" >> "$OUTPUT_FILE" ;;
                                R) echo "- 🔄 替换: $file" >> "$OUTPUT_FILE" ;;
                            esac
                        fi
                    done
                    
                    echo "" >> "$OUTPUT_FILE"
                    echo "---" >> "$OUTPUT_FILE"
                    echo "" >> "$OUTPUT_FILE"
                fi
            done
        else
            # 无认证时使用 Python 从数据库获取
            python3 << 'PYTHON_SCRIPT' >> "$OUTPUT_FILE"
import sqlite3
import time
from datetime import datetime
import sys

try:
    db_path = '.svn/wc.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n## 从本地数据库获取的提交记录")
    print("\n**注意**: 由于无法连接 SVN 服务器，以下信息来自本地工作副本数据库")
    print("          提交日志需要 SVN 服务器认证才能获取")
    print("\n---\n")
    
    # 查询指定作者的修改
    author_filter = sys.argv[1] if len(sys.argv) > 1 else None
    
    cursor.execute("""
        SELECT DISTINCT
            changed_revision,
            MIN(changed_date) as date,
            changed_author,
            COUNT(*) as file_count
        FROM NODES
        WHERE wc_id = 1 AND op_depth = 0
            AND (? IS NULL OR changed_author LIKE '%' || ? || '%')
        GROUP BY changed_revision
        ORDER BY changed_revision DESC
    """, (author_filter, author_filter))
    
    for rev, date_ts, author, count in cursor.fetchall():
        date_str = datetime.utcfromtimestamp(date_ts / 1000000).strftime('%Y-%m-%d %H:%M:%S') if date_ts else '未知'
        
        print(f"## 修订版本: r{rev}")
        print(f"- **作者**: {author}")
        print(f"- **日期**: {date_str}")
        print(f"- **修改文件数**: {count}")
        print(f"- **提交日志**: ⚠️ 需要认证才能获取")
        print("\n---\n")
    
    conn.close()
except Exception as e:
    print(f"数据库查询错误: {e}")
PYTHON_SCRIPT "$AUTHOR"
        fi
        ;;
    
    markdown|csv|json)
        # 其他格式使用原有逻辑
        echo "使用标准格式导出..."
        # ... (原有代码)
        ;;
    
    *)
        echo "错误: 不支持的输出格式 '$FORMAT'"
        echo "支持的格式: detailed, markdown, csv, json"
        exit 1
        ;;
esac

echo "✅ 导出完成!"
echo "输出文件: $OUTPUT_FILE"

# 提示认证信息
if [ "$SVN_LOG_AVAILABLE" = false ]; then
    echo ""
    echo "⚠️  提交日志未获取"
    echo "   要获取完整提交日志，请提供 SVN 认证信息:"
    echo "   用法: $0 [作者] [起始修订号] [结束修订号] detailed [项目路径] [用户名] [密码]"
    echo ""
    echo "   或在 Windows 上安装 SlikSVN: https://sliksvn.com/download/"
fi