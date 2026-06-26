#!/bin/bash
# AI Daily 抓取脚本
# 从 AI 洞察日报 RSS 获取最新内容

# 读取默认配置
source "$(dirname "$0")/../config.sh"

# 如果传参用参数，否则用默认
if [ -n "$1" ]; then
    COUNT=$1
else
    COUNT=${AI_DAILY_DEFAULT_COUNT:-1}
fi

# RSS 源
RSS_URL=${AI_DAILY_RSS_URL:-"https://justlovemaki.github.io/CloudFlare-AI-Insight-Daily/rss.xml"}

# Python 解析 RSS 并输出
python3 << EOF
import feedparser
import urllib.request
import os
import json
import re

url = "$RSS_URL"
count = int("$COUNT")

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
with urllib.request.urlopen(req, timeout=10) as f:
    content = f.read()

feed = feedparser.parse(content)

articles = []
for entry in list(feed.entries)[:count]:
    title = entry.title
    link = entry.link
    
    # 提取内容，原 RSS 内容是 HTML，重新解析出正确的列表
    content_html = entry.content[0].value
    # 正则提取 <h3> 标题 + <ol> <li> 列表
    sections = re.findall(r'<h3>(.*?)</h3>\\s*<ol>(.*?)</ol>', content_html, re.DOTALL)
    
    processed = []
    for section_name, list_html in sections:
        items = re.findall(r'<li>(.*?)</li>', list_html, re.DOTALL)
        item_list = []
        for item in items:
            item_text = re.sub(r'<[^>]+>', '', item)
            item_text = item_text.strip()
            if item_text:
                item_list.append(item_text)
        if section_name.strip() and item_list:
            processed.append((section_name.strip(), item_list))
    
    articles.append((title, link, processed))

# 生成输出
output = []
if len(articles) == 1:
    title, link, processed = articles[0]
    output.append(f"**AI 洞察日报 - {title}**\\n")
    for section_name, items in processed:
        output.append(f"{section_name}")
        for item in items:
            output.append(f"- {item}")
        output.append("")
else:
    output.append("**AI 洞察日报 最新:**\\n")
    for i, (title, link, _) in enumerate(articles, 1):
        output.append(f"{i}. **{title}**  \\n   {link}")

result = '\\n'.join(output)
print(result)

# 推送至配置的 webhook
webhooks = os.environ.get('AI_DAILY_WEBHOOKS', '')
if webhooks:
    print()
    for wh in webhooks.split():
        try:
            data = None
            headers = {'Content-Type': 'application/json'}
            
            if 'qyapi.weixin.qq.com' in wh:
                # 企业微信 markdown
                data = json.dumps({
                    "msgtype": "markdown",
                    "markdown": {
                        "content": result.replace('**', '*')
                    }
                })
            elif 'open.feishu.cn' in wh:
                # 飞书 text
                data = json.dumps({
                    "msg_type": "text",
                    "content": {
                        "text": result
                    }
                })
            elif 'oapi.dingtalk.com' in wh:
                # 钉钉 markdown
                data = json.dumps({
                    "msgtype": "markdown",
                    "markdown": {
                        "text": result
                    }
                })
            elif 'api.day.app' in wh:
                # Bark
                first_title = "AI 洞察日报" if len(articles) > 1 else articles[0][0]
                data = json.dumps({
                    "title": first_title,
                    "body": result.replace('**', '*'),
                    "autoCopy": 0
                })
            else:
                # 通用 JSON
                data = json.dumps({
                    "title": "AI 洞察日报",
                    "content": result
                })
            
            req = urllib.request.Request(wh, data.encode('utf-8'), headers)
            with urllib.request.urlopen(req, timeout=10) as f:
                resp = f.read().decode('utf-8')
            print(f"✅ 推送成功: {wh[:60]}...")
        except Exception as e:
            print(f"❌ 推送失败: {wh[:60]}...\\n   Error: {e}")
EOF
