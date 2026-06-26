#!/bin/bash
# Git 提交记录导出脚本
# 用法: ./export_git_commits.sh [作者] [起始日期] [结束日期] [输出格式] [项目路径]

set -e

# 参数解析
AUTHOR="${1:-}"
START_DATE="${2:-}"
END_DATE="${3:-}"
FORMAT="${4:-markdown}"  # markdown, csv, json
PROJECT_PATH="${5:-$(pwd)}"

# 输出文件名
OUTPUT_FILE="git_commits_${AUTHOR}_$(date +%Y%m%d_%H%M%S).${FORMAT}"

# 切换到项目目录
cd "$PROJECT_PATH" 2>/dev/null || { echo "错误: 项目路径不存在"; exit 1; }

# 检查是否为 Git 仓库
if [ ! -d ".git" ]; then
    echo "错误: 当前目录不是 Git 仓库"
    exit 1
fi

echo "=== Git 提交记录导出 ==="
echo "作者: ${AUTHOR:-所有}"
echo "时间范围: ${START_DATE:-无限制} ~ ${END_DATE:-无限制}"
echo "输出格式: $FORMAT"
echo "项目路径: $PROJECT_PATH"
echo ""

# 构建 git log 命令参数
GIT_LOG_ARGS="--pretty=format:'%H|%an|%ae|%ad|%s' --date=iso"

if [ -n "$AUTHOR" ]; then
    GIT_LOG_ARGS="$GIT_LOG_ARGS --author=\"$AUTHOR\""
fi

if [ -n "$START_DATE" ]; then
    GIT_LOG_ARGS="$GIT_LOG_ARGS --since=\"$START_DATE\""
fi

if [ -n "$END_DATE" ]; then
    GIT_LOG_ARGS="$GIT_LOG_ARGS --until=\"$END_DATE\""
fi

# 根据格式输出
case "$FORMAT" in
    markdown)
        echo "# Git 提交记录报告" > "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "**作者**: ${AUTHOR:-所有}" >> "$OUTPUT_FILE"
        echo "**时间范围**: ${START_DATE:-无限制} ~ ${END_DATE:-无限制}" >> "$OUTPUT_FILE"
        echo "**项目路径**: $PROJECT_PATH" >> "$OUTPUT_FILE"
        echo "**导出时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        # 获取提交记录
        eval git log $GIT_LOG_ARGS | while IFS='|' read -r commit_id author email date message; do
            echo "## 提交: ${commit_id:0:8}" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "- **作者**: $author ($email)" >> "$OUTPUT_FILE"
            echo "- **时间**: $date" >> "$OUTPUT_FILE"
            echo "- **信息**: $message" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "### 修改文件" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            
            # 获取修改文件列表
            git show --name-status --pretty=format:'' "$commit_id" | while read -r status file; do
                if [ -n "$file" ]; then
                    case "$status" in
                        A) echo "- ✅ 新增: $file" >> "$OUTPUT_FILE" ;;
                        M) echo "- ✏️ 修改: $file" >> "$OUTPUT_FILE" ;;
                        D) echo "- ❌ 删除: $file" >> "$OUTPUT_FILE" ;;
                        R) echo "- 🔄 重命名: $file" >> "$OUTPUT_FILE" ;;
                        *) echo "- 📝 $status: $file" >> "$OUTPUT_FILE" ;;
                    esac
                fi
            done
            echo "" >> "$OUTPUT_FILE"
            echo "---" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        done
        ;;
    
    csv)
        echo "commit_id,author,email,date,message,files_changed" > "$OUTPUT_FILE"
        eval git log $GIT_LOG_ARGS | while IFS='|' read -r commit_id author email date message; do
            # 获取修改文件数量
            files_changed=$(git show --name-only --pretty=format:'' "$commit_id" | wc -l)
            echo "\"$commit_id\",\"$author\",\"$email\",\"$date\",\"$message\",\"$files_changed\"" >> "$OUTPUT_FILE"
        done
        ;;
    
    json)
        echo "{" > "$OUTPUT_FILE"
        echo "  \"metadata\": {" >> "$OUTPUT_FILE"
        echo "    \"author\": \"${AUTHOR:-所有}\"," >> "$OUTPUT_FILE"
        echo "    \"start_date\": \"${START_DATE:-null}\"," >> "$OUTPUT_FILE"
        echo "    \"end_date\": \"${END_DATE:-null}\"," >> "$OUTPUT_FILE"
        echo "    \"project_path\": \"$PROJECT_PATH\"," >> "$OUTPUT_FILE"
        echo "    \"export_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\"" >> "$OUTPUT_FILE"
        echo "  }," >> "$OUTPUT_FILE"
        echo "  \"commits\": [" >> "$OUTPUT_FILE"
        
        first=true
        eval git log $GIT_LOG_ARGS | while IFS='|' read -r commit_id author email date message; do
            if [ "$first" = true ]; then
                first=false
            else
                echo "    ," >> "$OUTPUT_FILE"
            fi
            
            echo "    {" >> "$OUTPUT_FILE"
            echo "      \"commit_id\": \"$commit_id\"," >> "$OUTPUT_FILE"
            echo "      \"author\": \"$author\"," >> "$OUTPUT_FILE"
            echo "      \"email\": \"$email\"," >> "$OUTPUT_FILE"
            echo "      \"date\": \"$date\"," >> "$OUTPUT_FILE"
            echo "      \"message\": \"$message\"," >> "$OUTPUT_FILE"
            echo "      \"files\": [" >> "$OUTPUT_FILE"
            
            # 获取修改文件列表
            git show --name-status --pretty=format:'' "$commit_id" | while read -r status file; do
                if [ -n "$file" ]; then
                    echo "        {\"status\": \"$status\", \"file\": \"$file\"}" >> "$OUTPUT_FILE"
                fi
            done
            
            echo "      ]" >> "$OUTPUT_FILE"
            echo "    }" >> "$OUTPUT_FILE"
        done
        
        echo "  ]" >> "$OUTPUT_FILE"
        echo "}" >> "$OUTPUT_FILE"
        ;;
    
    *)
        echo "错误: 不支持的输出格式 '$FORMAT'"
        echo "支持的格式: markdown, csv, json"
        exit 1
        ;;
esac

echo "✅ 导出完成！"
echo "输出文件: $OUTPUT_FILE"
echo ""

# 显示统计信息
total_commits=$(eval git log $GIT_LOG_ARGS --oneline | wc -l)
echo "📊 统计信息:"
echo "   总提交数: $total_commits"