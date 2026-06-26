#!/usr/bin/env python3
"""
parse_chatgpt_share.py - 从 ChatGPT 共享链接提取对话内容

用法:
    python3 parse_chatgpt_share.py --url <shared_url> --output <output.json>
    python3 parse_chatgpt_share.py --html <local.html> --output <output.json>

输出 JSON 格式:
{
    "title": "对话标题",
    "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
        ...
    ]
}

要求: Python 3.6+（仅标准库，零外部依赖）

注意: ChatGPT 的前端使用 React Server Component (RSC/Flight) 序列化格式，
该格式可能随 ChatGPT 更新而变化。如果解析失败（提取到 0 条消息），
可能需要更新解析逻辑以适配新的 RSC 格式。
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error

__version__ = "0.3.0"

# 仅允许解析 ChatGPT 共享链接
ALLOWED_URL_PATTERN = re.compile(
    r'^https?://(chat\.openai\.com|chatgpt\.com)/share/[a-f0-9-]+$'
)


def validate_url(url: str) -> None:
    """校验 URL 是否为合法的 ChatGPT 共享链接"""
    if not ALLOWED_URL_PATTERN.match(url):
        raise ValueError(
            f"不支持的 URL 格式: {url}\n"
            f"仅支持 ChatGPT 共享链接，格式如: https://chatgpt.com/share/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        )


def fetch_html(url: str) -> str:
    """用 Python 标准库下载共享页面 HTML（不依赖 curl）"""
    validate_url(url)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            # 尝试从 Content-Type 获取编码，默认 utf-8
            charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP 请求失败 (状态码 {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e.reason}")
    except TimeoutError:
        raise RuntimeError("下载超时（60 秒），请检查网络连接或链接是否有效")

    if len(html) < 1000:
        raise RuntimeError("下载的页面内容过短，链接可能已失效或需要登录")

    return html


def extract_title(html: str) -> str:
    """提取页面标题"""
    m = re.search(r'<title>ChatGPT\s*-\s*(.*?)</title>', html)
    if m:
        return m.group(1).strip()
    m = re.search(r'<title>(.*?)</title>', html)
    return m.group(1).strip() if m else "未知对话"


def clean_citations(text: str) -> str:
    """清除 ChatGPT 的引用标记"""
    text = re.sub(r'[\ue200\ue202\ue201]', '', text)
    text = re.sub(r'\s*(?:citeturn\d+(?:view|search)\d+)+', '', text)
    return text


def decode_text(text: str) -> str:
    """解码转义字符（包括通用 \\uXXXX Unicode 转义）"""
    text = text.replace('\\n', '\n')
    text = text.replace('\\t', '\t')
    text = text.replace('\\"', '"')
    text = text.replace('\\/', '/')
    # 通用 Unicode 转义: \uXXXX -> 对应字符
    text = re.sub(r'\\u([0-9a-fA-F]{4})',
                  lambda m: chr(int(m.group(1), 16)), text)
    return text


def is_noise(text: str) -> bool:
    """判断文本是否为噪声(非实际对话内容)"""
    if not text or len(text) < 5:
        return True
    # UUID 字符串 (RSC 内部节点 ID)
    if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', text):
        return True
    # Reasoning recap
    if text.startswith('Thought for'):
        return True
    # Redacted tool output
    if text == "The output of this plugin was redacted.":
        return True
    return False


def extract_rsc_data(html: str) -> str:
    """找到并解码 RSC 数据"""
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    data_script = None

    # 优先: 包含 client-created-root 和 parts 的 script
    for script in scripts:
        if 'client-created-root' in script and 'parts' in script:
            data_script = script
            break

    # 备用: 含 parts 的最大 script
    if not data_script:
        for script in sorted(scripts, key=len, reverse=True):
            if 'parts' in script:
                data_script = script
                break

    if not data_script:
        return None

    # RSC 数据可能被双重转义(嵌套在 JSON 字符串中)
    if '\\"' in data_script and '"user"' not in data_script:
        data_script = data_script.replace('\\"', '"').replace('\\\\', '\\')

    return data_script


def extract_messages(data: str) -> list:
    """
    从 RSC 数据中提取对话消息。

    RSC (React Server Component) 序列化格式特点:
    - 字符串被 interned: "user" 和 "assistant" 各只出现一次
    - 后续引用通过 {"_50":KEY,"_52":XX} 的结构指向 interned 的角色
    - 消息内容在 [N],"文本" 格式的数组引用后

    策略: 用 user role key 的引用位置来划分对话轮次,
    每个轮次内取最长的 assistant 内容作为回复。
    """
    messages = []

    # 1. 找到 user 和 assistant 的 interned key
    user_key_match = re.search(r'\{"_50":(\d+),"_52":\d+\},"user"', data)
    asst_key_match = re.search(r'\{"_50":(\d+),"_52":\d+\},"assistant"', data)

    if not user_key_match or not asst_key_match:
        return messages

    user_key = int(user_key_match.group(1))
    asst_key = int(asst_key_match.group(1))

    # 2. 找到所有 user/assistant 角色标记的位置
    user_positions = [m.start() for m in
                      re.finditer(rf'\{{"_50":{user_key},"_52":\d+\}}', data)]
    asst_positions = [m.start() for m in
                      re.finditer(rf'\{{"_50":{asst_key},"_52":\d+\}}', data)]

    # 3. 提取所有内容字符串及其位置
    contents = []  # [(position, decoded_text)]
    for m in re.finditer(r'\[(\d+)\],"((?:[^"\\]|\\.){20,})"', data):
        raw = m.group(2)
        # 过滤 RSC 内部元数据
        if re.match(r'_\d+', raw) or raw.count('"_') > 3:
            continue
        # 过滤 JSON 搜索查询
        if raw.startswith('{\\') or raw.startswith('{"search'):
            continue
        text = decode_text(raw)
        if not is_noise(text):
            contents.append((m.start(), text))

    # 4. 按 user 位置划分对话轮次
    turns = []
    for i, upos in enumerate(user_positions):
        next_upos = user_positions[i + 1] if i + 1 < len(user_positions) else len(data)

        first_asst = next_upos
        for apos in asst_positions:
            if apos > upos:
                first_asst = apos
                break

        user_texts = [(p, t) for p, t in contents if upos < p < first_asst]
        asst_texts = [(p, t) for p, t in contents if first_asst <= p < next_upos]

        turns.append({
            'user_texts': user_texts,
            'asst_texts': asst_texts,
        })

    # 5. 从每个轮次中提取最有价值的消息
    for turn in turns:
        if turn['user_texts']:
            user_content = max(turn['user_texts'], key=lambda x: len(x[1]))[1]
            user_content = clean_citations(user_content).strip()
            if user_content:
                messages.append({'role': 'user', 'content': user_content})

        if turn['asst_texts']:
            substantial = []
            for _, t in turn['asst_texts']:
                cleaned = clean_citations(t).strip()
                if len(cleaned) < 80:
                    skip_phrases = ['查一下', '确认一下', '核对一下', '搜索',
                                    '先确认', '我去查', '先查', '帮你判断',
                                    '我先', '让我']
                    if any(p in cleaned for p in skip_phrases):
                        continue
                if cleaned:
                    substantial.append(cleaned)

            if substantial:
                asst_content = max(substantial, key=len)
                messages.append({'role': 'assistant', 'content': asst_content})

    return messages


def parse_shared_conversation(html: str) -> dict:
    """解析 ChatGPT 共享对话页面"""
    title = extract_title(html)

    data = extract_rsc_data(html)
    if not data:
        print("⚠️  未找到 RSC 数据。ChatGPT 可能已更新前端格式，需要适配解析逻辑。", file=sys.stderr)
        return {'title': title, 'message_count': 0, 'messages': [],
                'warning': 'RSC data not found - ChatGPT frontend format may have changed'}

    msgs = extract_messages(data)

    if len(msgs) == 0:
        print("⚠️  找到 RSC 数据但未提取到消息。可能是 RSC 序列化格式发生了变化。", file=sys.stderr)

    return {
        'title': title,
        'message_count': len(msgs),
        'messages': msgs,
        'parser_version': __version__
    }


def main():
    parser = argparse.ArgumentParser(description='解析 ChatGPT 共享对话链接')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help='ChatGPT 共享链接')
    group.add_argument('--html', help='本地 HTML 文件路径')
    parser.add_argument('--output', required=True, help='输出 JSON 文件路径')

    args = parser.parse_args()

    if args.url:
        print(f"正在下载: {args.url}", file=sys.stderr)
        html = fetch_html(args.url)
    else:
        print(f"正在读取: {args.html}", file=sys.stderr)
        with open(args.html, 'r', encoding='utf-8') as f:
            html = f.read()

    print("正在解析对话内容...", file=sys.stderr)
    result = parse_shared_conversation(html)

    print(f"标题: {result['title']}", file=sys.stderr)
    print(f"提取到 {result['message_count']} 条消息", file=sys.stderr)

    for i, msg in enumerate(result['messages']):
        role = '👤 用户' if msg['role'] == 'user' else '🤖 助手'
        preview = msg['content'][:60].replace('\n', ' ')
        print(f"  [{i+1}] {role}: {preview}...", file=sys.stderr)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n已保存到: {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
