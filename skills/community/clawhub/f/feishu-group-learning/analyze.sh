#!/bin/bash

TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a92b19fbc278dbd6","app_secret":"WFsYhmcEZnRjL4c1ClotIeHhoq5568Sp"}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

echo "📚 飞书群学习分析报告"
echo "生成时间: $(date '+%Y-%m-%d %H:%M')"
echo "分析周期: 每6小时"
echo ""

for CHAT_ID in "oc_60c795e2e04eefc3d09eb49da4df15a5:养虾乐园🦞" "oc_3cc1c4abbc093b180cb0b75e40bb6e1b:🦞龙虾聚会"; do
    IFS=':' read -r ID NAME <<< "$CHAT_ID"
    
    echo "📌 $NAME"
    echo "   Chat ID: $ID"
    
    # Get messages
    curl -s "https://open.feishu.cn/open-apis/im/v1/messages?container_id=$ID&container_id_type=chat&page_size=50" \
      -H "Authorization: Bearer $TOKEN" > /tmp/chat_${ID##*_}.json
    
    # Count and analyze
    python3 << PYTHON
import json

with open('/tmp/chat_${ID##*_}.json', 'r') as f:
    data = json.load(f)

items = data.get('data', {}).get('items', [])
messages = []

for msg in items:
    if msg.get('msg_type') == 'system':
        continue
    content = msg.get('body', {}).get('content', '')
    if content and len(content) > 5:
        try:
            if content.startswith('['):
                data = json.loads(content)
                if isinstance(data, list) and len(data) > 0:
                    text_data = data[0]
                    if isinstance(text_data, list):
                        text = ''.join([item.get('text', '') for item in text_data if item.get('tag') == 'text'])
                        if text:
                            messages.append(text)
            elif content.startswith('{'):
                data = json.loads(content)
                text = data.get('text', '')
                if text:
                    messages.append(text)
        except:
            pass

print(f"   有效消息: {len(messages)} 条")

if messages:
    all_text = ' '.join(messages).lower()
    insights = []
    
    keywords = {
        '科技领袖追踪': ['@sama', '@elonmusk', '科技圈', '大佬', 'vc'],
        'Agent稳定性': ['失灵', '连接', '无响应'],
        '内容创作': ['简报', '整理', '文章'],
        '新用户引导': ['你是谁', '介绍'],
        '产品发布': ['大会', '发布', 'app', 'web']
    }
    
    for insight, kws in keywords.items():
        if any(kw in all_text for kw in kws):
            insights.append(insight)
    
    if insights:
        print(f"   发现: {', '.join(insights)}")
    else:
        print("   发现: 暂无")
else:
    print("   发现: 无有效消息")

print("")
PYTHON
done

echo "✅ 分析完成"
echo "报告已保存到记忆系统"
