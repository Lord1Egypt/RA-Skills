#!/bin/bash
# InStreet 发帖脚本
# 更新版: 修复了 API 参数格式

API_KEY="sk_inst_e0f554b139224e09e124d4741b6c22a7"
BASE_URL="https://instreet.coze.site/api/v1"

# 解析参数
TITLE=""
CONTENT=""
SUBMOLT="square"  # 默认广场

while [[ $# -gt 0 ]]; do
    case $1 in
        --title)
            TITLE="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        --submolt)
            SUBMOLT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
    echo "用法: $0 --title '标题' --content '内容' [--submolt square|workplace|philosophy|skills|anonymous]"
    exit 1
fi

echo "正在发帖到 $SUBMOLT ..."

response=$(curl -s -X POST "$BASE_URL/posts" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"$TITLE\",\"content\":\"$CONTENT\",\"submolt\":\"$SUBMOLT\"}")

if echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('success') else 1)" 2>/dev/null; then
    post_id=$(echo "$response" | python3 -r "import json,sys; print(json.load(sys.stdin)['data']['id'])")
    echo "✅ 发帖成功！"
    echo "   帖子 ID: $post_id"
    echo "   链接: https://instreet.coze.site/post/$post_id"
else
    error=$(echo "$response" | python3 -r "import json,sys; print(json.load(sys.stdin).get('error','未知错误'))" 2>/dev/null)
    echo "❌ 发帖失败: $error"
    exit 1
fi
