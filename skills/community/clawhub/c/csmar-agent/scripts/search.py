import sys
import json
import requests
from typing import Generator, Dict, Any


def baidu_search(query:str) -> Generator[str, None, None]:
    url = "http://10.222.21.157:6600/api/Agent/queryanswerstream"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json"
    }
    data = {
        "Query": query,
        "IsReasoner": False
    }
    try:
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()
        yield  from simple_sse_reader(response)
    except Exception as e:
        print(f"其他错误: {e}")


def simple_sse_reader(response) -> Generator[str, None, None]:
    """处理SSE流式响应"""
    for line in response.iter_lines(decode_unicode=False):
        if not line:
            continue
        try:
            line_str = line.decode('utf-8')
            # print(line_str)
            if line_str.startswith('data: '):
                json_str = line_str[6:]
                data = json.loads(json_str)
                content = data.get('Reasoning_content', '')
                if not content:
                    content = data.get('Content', '')
                if content:
                    #print(content)
                    yield content
        except Exception as e:
            yield f"\n[解析错误] {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python baidu_search.py <Json>")
        sys.exit(1)
    parse_data=sys.argv[1]
    # 验证必需字段
    if not parse_data:
        print(f"错误: 缺少必需字段 'Query'", file=sys.stderr)
        sys.exit(1)
    try:
        # results = list(baidu_search(parse_data["Query"]))
        # full_text = ''.join(results)
        # print(full_text)
        # # 直接输出流式内容
        for content in baidu_search(parse_data):
            print(content, end='', flush=True)
    except Exception as e:
        print(f"\n错误: {str(e)}", file=sys.stderr)
        sys.exit(1)