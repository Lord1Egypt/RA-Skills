import sys
import json
import requests
import os


def baidu_search(api_key, requestBody: dict):
    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"

    headers = {
        "Authorization": "Bearer %s" % api_key,
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=requestBody, headers=headers, timeout=25)
    response.raise_for_status()
    results = response.json()
    if "code" in results:
        raise Exception(results["message"])
    datas = results["references"]
    keys_to_remove = {"snippet"}
    for item in datas:
        for key in keys_to_remove:
            if key in item:
                del item[key]
    return datas


def load_json_input(query):
    """Load and parse JSON from various input methods, handling BOM and encoding issues."""
    # Try to load as direct JSON string first
    query = query.strip()
    
    # Handle UTF-8 BOM
    if query.startswith('\ufeff'):
        query = query[1:]
    
    # Try parsing as JSON
    try:
        return json.loads(query)
    except json.JSONDecodeError:
        pass
    
    # If it looks like a file path, try reading from file
    if os.path.exists(query):
        with open(query, 'r', encoding='utf-8-sig') as f:
            content = f.read().strip()
            if content.startswith('\ufeff'):
                content = content[1:]
            return json.loads(content)
    
    # If stdin has data, try reading from it
    if not os.isatty(0):
        stdin_data = sys.stdin.read().strip()
        if stdin_data:
            if stdin_data.startswith('\ufeff'):
                stdin_data = stdin_data[1:]
            return json.loads(stdin_data)
    
    return None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if len(sys.argv) < 2:
        print("Usage: python baidu_search.py <json_string_or_file_path>")
        sys.exit(1)
    
    query = sys.argv[1]
    parse_data = load_json_input(query)
    
    if parse_data is None:
        print(f"JSON parse error: could not parse input: {repr(query[:100])}")
        sys.exit(1)
    
    if "query" not in parse_data:
        print("Error: query must be present in request body.")
        sys.exit(1)

    api_key = os.getenv("BAIDU_API_KEY")

    if not api_key:
        print("Error: BAIDU_API_KEY must be set in environment.")
        sys.exit(1)

    request_body = {
        "messages": [
            {
                "content": parse_data["query"],
                "role": "user"
            }
        ],
        "edition": parse_data.get("edition", "standard"),
        "search_source": "baidu_search_v2",
        "resource_type_filter": parse_data.get("resource_type_filter", [{"type": "web", "top_k": 20}]),
        "search_filter": parse_data.get("search_filter", {}),
        "block_websites": parse_data.get("block_websites", None),
        "search_recency_filter": parse_data.get("search_recency_filter", "year"),
        "safe_search": parse_data.get("safe_search", False),
    }
    try:
        results = baidu_search(api_key, request_body)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
