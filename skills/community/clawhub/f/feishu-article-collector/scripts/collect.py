#!/usr/bin/env python3
"""飞书文章收集器 - 一站式处理脚本

Usage: python3 collect.py '<message_text>'

环境变量:
  FEISHU_APP_ID      飞书应用 App ID
  FEISHU_APP_SECRET  飞书应用 App Secret
  DEEPSEEK_API_KEY   DeepSeek API 密钥

从消息中提取链接 → 抓取文章正文 → AI生成摘要和分类 → 写入飞书多维表格
多维表格自动发现或创建，状态缓存在 .state.json 中
"""

import json
import os
import re
import sys
import time
import requests
from urllib.parse import unquote

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(SCRIPT_DIR, ".state.json")
BASE_URL = "https://open.feishu.cn/open-apis"
BITABLE_NAME = "今日头条文章收藏"

# 支持的域名
TOUTIAO_DOMAINS = [
    "toutiao.com",
    "toutiaocdn.com",
    "toutiao.io",
    "snssdk.com",
]

WECHAT_DOMAINS = [
    "mp.weixin.qq.com",
    "weixin.qq.com",
]

SUPPORTED_DOMAINS = TOUTIAO_DOMAINS + WECHAT_DOMAINS

CATEGORIES = ["科技", "财经", "娱乐", "健康", "教育", "体育", "其他"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def get_env(name):
    """获取必需的环境变量"""
    val = os.environ.get(name, "")
    if not val:
        raise Exception(f"缺少环境变量: {name}")
    return val


def load_state():
    """加载本地缓存的多维表格状态"""
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    """保存多维表格状态到本地缓存"""
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def extract_url(text):
    """从消息文本中提取支持的文章链接（今日头条、微信公众号）"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    for url in urls:
        if any(domain in url for domain in SUPPORTED_DOMAINS):
            return url
    return None


def detect_source(url):
    """检测链接来源：toutiao 或 wechat"""
    if any(domain in url for domain in WECHAT_DOMAINS):
        return "wechat"
    return "toutiao"


def extract_title_from_message(text, url):
    """从分享文本中提取标题"""
    text_without_url = text.replace(url, "").strip()

    match = re.search(r'[《「](.+?)[》」]', text_without_url)
    if match:
        return match.group(1)

    match = re.search(r'看到了?\s*(.+)', text_without_url)
    if match:
        return match.group(1).strip()

    cleaned = re.sub(r'^(我在今日头条|分享一篇|推荐一篇|转发|分享)', '', text_without_url).strip()
    if cleaned:
        return cleaned

    return None


def fetch_wechat_article(url):
    """抓取微信公众号文章"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.encoding = "utf-8"
        html = resp.text

        title = None
        m = re.search(r'property="og:title"\s+content="([^"]+)"', html)
        if m:
            title = m.group(1).strip()

        content = ""
        m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*(?:<div|<script)', html, re.DOTALL)
        if m:
            content = re.sub(r'<[^>]+>', '', m.group(1)).strip()

        content = re.sub(r'\s+', ' ', content).strip()
        if len(content) > 5000:
            content = content[:5000]

        return title, content

    except Exception as e:
        return None, f"抓取失败: {str(e)}"


def fetch_toutiao_article(url):
    """抓取今日头条文章正文"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        resp.encoding = "utf-8"
        html = resp.text

        title = None
        m = re.search(r'<title[^>]*>([^<]+)</title>', html)
        if m:
            title = m.group(1).strip()
            title = re.sub(r'\s*[-_|]\s*(今日头条|头条号|手机搜狐网).*$', '', title)

        if not title or title in ("今日头条", ""):
            m = re.search(r'property=["\']og:title["\']\s+content=["\']([^"\']+)', html)
            if m:
                title = m.group(1).strip()

        content = ""

        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        for script in scripts:
            if 'articleInfo' not in script and '%22articleInfo%22' not in script:
                continue
            decoded_script = unquote(script)
            content_key = '"content":"'
            idx = decoded_script.find(content_key)
            if idx >= 0:
                start = idx + len(content_key)
                pos = start
                while pos < len(decoded_script):
                    if decoded_script[pos] == '"' and decoded_script[pos - 1] != '\\':
                        break
                    pos += 1
                raw = decoded_script[start:pos]
                raw = raw.replace('\\u003C', '<').replace('\\u003E', '>')
                raw = raw.replace('\\u0026', '&').replace('\\u003D', '=')
                content = re.sub(r'<[^>]+>', '', raw).strip()
            break

        if not content:
            paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
            good_p = [p.strip() for p in paragraphs if len(p.strip()) > 10]
            if good_p:
                content = "\n".join(good_p)

        content = re.sub(r'\s+', ' ', content).strip()
        if len(content) > 3000:
            content = content[:3000]

        return title, content

    except Exception as e:
        return None, f"抓取失败: {str(e)}"


def fetch_article(url):
    """根据链接来源分发到对应的抓取函数"""
    source = detect_source(url)
    if source == "wechat":
        return fetch_wechat_article(url)
    return fetch_toutiao_article(url)


def ai_analyze(title, content, deepseek_api_key):
    """使用 DeepSeek API 生成总结和分类"""
    if not content or content.startswith("抓取失败"):
        return "无法获取正文", "其他"

    prompt = f"""请分析以下文章，完成两个任务：

1. 生成总结：提炼文章的核心观点、关键信息和主要结论，200-300字
2. 自动分类：从以下类别中选择最合适的一个：科技、财经、娱乐、健康、教育、体育、其他

文章标题：{title or '未知'}
文章内容：{content}

请严格按以下 JSON 格式返回，不要包含其他内容：
{{"summary": "总结内容", "category": "分类标签"}}"""

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {deepseek_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 600,
            },
            timeout=30,
        )
        data = resp.json()
        reply = data["choices"][0]["message"]["content"].strip()

        m = re.search(r'\{[^}]+\}', reply, re.DOTALL)
        if m:
            result = json.loads(m.group())
            summary = result.get("summary", "")[:500]
            category = result.get("category", "其他")
            if category not in CATEGORIES:
                category = "其他"
            return summary, category

        return reply[:150], "其他"

    except Exception as e:
        return f"AI分析失败: {str(e)}", "其他"


def get_tenant_access_token(app_id, app_secret):
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": app_id,
        "app_secret": app_secret,
    })
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def find_or_create_bitable(token):
    """查找已有的多维表格，不存在则自动创建并配置字段"""
    headers = {"Authorization": f"Bearer {token}"}

    # 搜索已有的多维表格
    resp = requests.get(
        f"{BASE_URL}/drive/v1/files",
        headers=headers,
        params={"folder_token": "", "page_size": 50},
    )
    data = resp.json()
    if data.get("code") == 0:
        for f in data.get("data", {}).get("files", []):
            if f.get("name") == BITABLE_NAME and f.get("type") == "bitable":
                app_token = f["token"]
                # 获取 table_id
                resp2 = requests.get(
                    f"{BASE_URL}/bitable/v1/apps/{app_token}/tables",
                    headers=headers,
                )
                tables = resp2.json()
                if tables.get("code") == 0 and tables["data"]["items"]:
                    table_id = tables["data"]["items"][0]["table_id"]
                    return app_token, table_id

    # 未找到，创建新的多维表格
    resp = requests.post(
        f"{BASE_URL}/bitable/v1/apps",
        headers=headers,
        json={"name": BITABLE_NAME},
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"创建多维表格失败: {data}")

    app_token = data["data"]["app"]["app_token"]
    table_id = data["data"]["app"]["default_table_id"]

    # 重命名默认字段为"文章标题"
    resp = requests.get(
        f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
        headers=headers,
    )
    fields_data = resp.json()
    if fields_data.get("code") == 0 and fields_data["data"]["items"]:
        first_field = fields_data["data"]["items"][0]
        requests.put(
            f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{first_field['field_id']}",
            headers=headers,
            json={"field_name": "文章标题", "type": first_field["type"]},
        )

    # 添加其余字段
    fields = [
        {"field_name": "文章链接", "type": 15},
        {"field_name": "文章ID", "type": 1},
        {"field_name": "分享人", "type": 1},
        {
            "field_name": "分享时间",
            "type": 5,
            "property": {"date_formatter": "yyyy/MM/dd", "auto_fill": True},
        },
        {
            "field_name": "分类标签",
            "type": 3,
            "property": {
                "options": [
                    {"name": c} for c in CATEGORIES
                ]
            },
        },
        {"field_name": "备注", "type": 1},
        {"field_name": "已读", "type": 7},
    ]
    for field in fields:
        requests.post(
            f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
            headers=headers,
            json=field,
        )

    return app_token, table_id


def get_bitable(token):
    """获取多维表格的 app_token 和 table_id（优先读缓存）"""
    state = load_state()
    app_token = state.get("bitable_app_token")
    table_id = state.get("bitable_table_id")

    if app_token and table_id:
        # 验证缓存是否仍然有效
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
            headers=headers,
        )
        if resp.json().get("code") == 0:
            return app_token, table_id

    # 缓存无效或不存在，重新查找/创建
    app_token, table_id = find_or_create_bitable(token)
    save_state({"bitable_app_token": app_token, "bitable_table_id": table_id})
    return app_token, table_id


def extract_article_id(url):
    """从 URL 中提取文章唯一标识"""
    m = re.search(r'/(?:article|w|i)/(\d+)', url)
    if m:
        return m.group(1)
    m = re.search(r'/s/([A-Za-z0-9_-]+)', url)
    if m:
        return m.group(1)
    return None


def check_duplicate(token, app_token, table_id, article_id):
    """通过文章ID字段精确搜索，检查是否已收录"""
    api = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    headers = {"Authorization": f"Bearer {token}"}
    body = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "文章ID",
                    "operator": "is",
                    "value": [article_id],
                }
            ],
        },
        "page_size": 1,
    }
    resp = requests.post(api, headers=headers, json=body)
    data = resp.json()
    if data.get("code") != 0:
        return False
    return data.get("data", {}).get("total", 0) > 0


def write_record(token, app_token, table_id, record):
    url = f"{BASE_URL}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, json={"fields": record})
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"写入失败: {data}")
    return data


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: python3 collect.py '<message_text>'"}))
        sys.exit(1)

    message_text = sys.argv[1]

    # 1. 提取 URL
    url = extract_url(message_text)
    if not url:
        print(json.dumps({"success": False, "error": "未找到支持的文章链接"}))
        sys.exit(1)

    # 2. 获取飞书凭证并认证
    app_id = get_env("FEISHU_APP_ID")
    app_secret = get_env("FEISHU_APP_SECRET")
    token = get_tenant_access_token(app_id, app_secret)

    # 3. 获取多维表格（自动发现或创建）
    app_token, table_id = get_bitable(token)

    # 4. 去重检查
    clean_url = url.split("?")[0]
    article_id = extract_article_id(url)
    if article_id and check_duplicate(token, app_token, table_id, article_id):
        print(json.dumps({"success": False, "error": "该文章已收录，跳过重复链接", "url": clean_url}, ensure_ascii=False))
        sys.exit(0)

    # 5. 检测来源
    source = detect_source(url)
    source_name = "微信公众号" if source == "wechat" else "今日头条"

    # 6. 提取标题 + 抓取文章
    msg_title = extract_title_from_message(message_text, url)
    page_title, content = fetch_article(url)
    title = msg_title or page_title or "未知标题"

    # 7. AI 分析
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    analyze_content = content if content and not content.startswith("抓取失败") else title
    summary, category = ai_analyze(title, analyze_content, deepseek_key)

    # 8. 写入多维表格
    record = {
        "文章标题": title,
        "文章链接": {"link": clean_url, "text": title},
        "文章ID": article_id or "",
        "分享人": source_name,
        "分享时间": int(time.time()) * 1000,
        "分类标签": category,
        "备注": summary,
    }
    result = write_record(token, app_token, table_id, record)
    record_id = result["data"]["record"]["record_id"]

    output = {
        "success": True,
        "title": title,
        "category": category,
        "summary": summary,
        "record_id": record_id,
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
