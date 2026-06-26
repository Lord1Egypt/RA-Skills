import requests
import os
import re
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='抓取 ClawFeed 简报')
parser.add_argument('--type', '-t', default='daily', choices=['4h', 'daily', 'weekly'], help='简报类型')
parser.add_argument('--limit', '-l', type=int, default=1, help='获取数量')
parser.add_argument('--offset', '-o', type=int, default=0, help='偏移量')
parser.add_argument('--output', '-out', type=str, default=None, help='输出目录 (默认: ~/OneDrive/文档/Obsidian Vault/AI新闻)')
args = parser.parse_args()

# 获取 ClawFeed 简报
api_url = f"https://clawfeed.kevinhe.io/api/digests?type={args.type}&limit={args.limit}&offset={args.offset}"
r = requests.get(api_url)

if r.status_code != 200:
    print(f"Error: {r.status_code}")
    exit(1)

data = r.json()

# 确定输出目录
if args.output:
    ai_news_dir = args.output
else:
    vault_path = os.path.expanduser("~/OneDrive/文档/Obsidian Vault")
    ai_news_dir = os.path.join(vault_path, "AI新闻")

os.makedirs(ai_news_dir, exist_ok=True)

# 处理每个简报
for digest in data:
    content = digest["content"]
    
    # 从内容中提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        date_str = date_match.group(1)
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 文件名加类型前缀
    if args.type == '4h':
        filename = f"{date_str}-4h.md"
    elif args.type == 'weekly':
        filename = f"周报-{date_str}.md"
    else:
        filename = f"{date_str}.md"
    
    file_path = os.path.join(ai_news_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已写入: {file_path}")

print(f"共处理 {len(data)} 条简报")
