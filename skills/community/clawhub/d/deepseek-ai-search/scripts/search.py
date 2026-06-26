import sys
import json
import requests
import os
from typing import Dict, Optional

# Ensure stdout uses UTF-8 encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def ai_search(query: str, model: str = "deepseek-expert-chat-search", stream: bool = False) -> dict:
    """Execute search using AI model with built-in search capability."""
    base_url = os.environ.get("AI_SEARCH_BASE_URL", "https://ai.ch66.top")
    api_key = os.environ.get("AI_SEARCH_API_KEY")

    if not api_key:
        raise ValueError("AI_SEARCH_API_KEY environment variable is not set")

    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个具有联网搜索能力的AI助手，每次回答前请先搜索互联网获取最新信息。"},
            {"role": "user", "content": query}
        ],
        "stream": stream,
        "tools": [{"type": "web_search", "web_search": {"enabled": True}}],
        "search_enabled": True
    }

    response = requests.post(url, json=payload, headers=headers, timeout=90)
    response.raise_for_status()
    return response.json()


def format_result(result: dict, verbose: bool = True) -> str:
    """Format the search result for display."""
    if "choices" not in result or len(result["choices"]) == 0:
        return json.dumps(result, indent=2, ensure_ascii=False)

    output_parts = []

    # Extract the main response
    message = result["choices"][0].get("message", {})

    # Include reasoning content if available and verbose mode
    if verbose and "reasoning_content" in message:
        output_parts.append("=== 推理过程 ===")
        output_parts.append(message["reasoning_content"])
        output_parts.append("")

    # Include main content
    if "content" in message:
        output_parts.append("=== 搜索结果 ===")
        output_parts.append(message["content"])

    # Include usage info if verbose mode
    if verbose and "usage" in result:
        output_parts.append("")
        output_parts.append("=== 使用统计 ===")
        usage = result["usage"]
        output_parts.append(f"提示词: {usage.get('prompt_tokens', 0)} tokens")
        output_parts.append(f"完成: {usage.get('completion_tokens', 0)} tokens")
        output_parts.append(f"总计: {usage.get('total_tokens', 0)} tokens")

    return "\n".join(output_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py '<JSON>'")
        print("\nParameters:")
        print("  query   - (required) Search query")
        print("  model   - (optional) Model name, default: deepseek-reasoner-search")
        print("  verbose - (optional) Show reasoning and stats, default: true")
        print("\nAvailable models:")
        print("  - deepseek-reasoner-search (recommended)")
        print("  - deepseek-chat-search")
        print("  - deepseek-expert-chat-search")
        print("  - deepseek-expert-reasoner-search")
        print("  - deepseek-vision-chat-search")
        print("  - deepseek-vision-reasoner-search")
        print("\nExample:")
        print('  python search.py \'{"query":"最新科技新闻"}\'')
        print('  python search.py \'{"query":"天气","model":"deepseek-chat-search","verbose":false}\'')
        sys.exit(1)

    query_str = sys.argv[1]
    parse_data = {}

    try:
        parse_data = json.loads(query_str)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    if "query" not in parse_data:
        print("Error: 'query' field is required in request body.")
        sys.exit(1)

    query = parse_data["query"]
    model = parse_data.get("model", "deepseek-expert-chat-search")
    stream = parse_data.get("stream", False)
    verbose = parse_data.get("verbose", True)

    try:
        result = ai_search(query, model, stream)
        print(format_result(result, verbose))
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"Value error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
