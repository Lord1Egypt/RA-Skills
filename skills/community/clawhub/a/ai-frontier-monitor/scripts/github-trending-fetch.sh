#!/usr/bin/env bash
# github-trending-fetch.sh — 抓取 GitHub Trending AI/ML 项目
# 用法: bash github-trending-fetch.sh [--period daily|weekly] [--json] [--filter AI]
# 默认: daily, AI关键词过滤, 最多10个

set -e

PERIOD="daily"
JSON_OUT=false
FILTER="AI"

while [[ $# -gt 0 ]]; do
  case $1 in
    --period) PERIOD="$2"; shift 2 ;;
    --json) JSON_OUT=true; shift ;;
    --filter) FILTER="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "📡 正在抓取 GitHub Trending (${PERIOD})..." >&2

# 使用更可靠的 Python 解析
curl -s "https://github.com/trending?since=${PERIOD}" | python3 -c "
import sys, json, re
from html.parser import HTMLParser

html = sys.stdin.read()
if not html.strip():
    print(json.dumps({'error': 'empty response', 'repos': []}))
    sys.exit(0)

# AI/ML 关键词
AI_KEYWORDS = [
    'ai', 'llm', 'gpt', 'neural', 'machine-learning', 'transformer',
    'agent', 'deep-learning', 'nlp', 'diffusion', 'langchain',
    'embedding', 'rag', 'mcp', 'claude', 'openai', 'model',
    'inference', 'training', 'fine-tune', 'vector', 'attention',
    'pytorch', 'tensorflow', 'huggingface', 'onnx', 'agentic',
    '人工智能', '大模型', '智能体'
]

def strip_html(text):
    \"\"\"移除 HTML 标签\"\"\"
    return re.sub(r'<[^>]+>', '', text).strip()

def parse_star_count(s):
    \"\"\"解析 star 数字字符串\"\"\"
    if not s:
        return 0
    s = s.strip().replace(',', '').replace(' ', '')
    if s.endswith('k') or s.endswith('K'):
        return int(float(s[:-1]) * 1000)
    if s.endswith('m') or s.endswith('M'):
        return int(float(s[:-1]) * 1000000)
    try:
        return int(s)
    except:
        return 0

# 按 <article> 分割
articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)

repos = []
for article in articles:
    # 项目名：从 h2 > a 提取
    h2_match = re.search(r'<h2[^>]*>.*?<a[^>]*href=\"(/[^\"]+)\"[^>]*>.*?</h2>', article, re.DOTALL)
    if not h2_match:
        continue
    repo_path = h2_match.group(1).strip('/')
    
    # 描述：从 <p> 提取
    desc_match = re.search(r'<p[^>]*class=\"[^\"]*col-9[^\"]*\"[^>]*>(.*?)</p>', article, re.DOTALL)
    if not desc_match:
        desc_match = re.search(r'<p[^>]*>(.*?)</p>', article, re.DOTALL)
    desc = strip_html(desc_match.group(1)) if desc_match else ''
    
    # 语言
    lang_match = re.search(r'itemprop=\"programmingLanguage\">(.*?)<', article)
    if not lang_match:
        lang_match = re.search(r'<span[^>]*class=\"[^\"]*color-fg-default[^\"]*\"[^>]*>\s*([A-Za-z+#]+)\s*<', article)
    lang = lang_match.group(1).strip() if lang_match else ''
    
    # 总 Stars - 从 stargazers 链接提取
    stars_match = re.search(r'href=\"/[^/]+/[^/]+/stargazers\"[^>]*>\s*([\d,\.]+[kKmM]?)\s*<', article)
    if not stars_match:
        stars_match = re.search(r'stargazers[^\>]*>\s*(?:\s*<[^>]*>\s*)*([\d,\.]+[kKmM]?)', article)
    stars_str = stars_match.group(1) if stars_match else '0'
    total_stars = parse_star_count(stars_str)
    
    # 今日 Stars
    today_match = re.search(r'([\d,\.]+[kKmM]?)\s*stars?\s*today', article, re.IGNORECASE)
    today_str = today_match.group(1) if today_match else '0'
    today_stars = parse_star_count(today_str)
    
    # AI 相关性检查
    searchable = f'{repo_path} {desc}'.lower()
    is_ai = any(kw.lower() in searchable for kw in AI_KEYWORDS)
    
    repos.append({
        'name': repo_path,
        'description': desc[:200],
        'language': lang,
        'total_stars': total_stars,
        'today_stars': today_stars,
        'is_ai': is_ai,
        'url': f'https://github.com/{repo_path}'
    })

# 分两批：AI 相关 + 其他
ai_repos = [r for r in repos if r['is_ai']]
other_repos = [r for r in repos if not r['is_ai']]

# 按 today_stars 降序
ai_repos.sort(key=lambda r: r['today_stars'], reverse=True)

result = {
    'ai_repos': ai_repos[:10],
    'other_notable': other_repos[:3] if other_repos else [],
    'total_fetched': len(repos),
    'ai_count': len(ai_repos)
}

print(json.dumps(result, ensure_ascii=False, indent=2))
"