#!/bin/bash
# Bailian Search - Real-time web search via Alibaba Cloud DashScope MCP
# Usage: export DASHSCOPE_API_KEY="your-key" && ./search.sh "search query" [count]
# Version: 1.1.0 - Fixed MCP protocol implementation

set -e

DASHSCOPE_API_KEY="${DASHSCOPE_API_KEY}"
QUERY="$1"
COUNT="${2:-5}"

# Validate API key
if [ -z "$DASHSCOPE_API_KEY" ]; then
  echo "Error: DASHSCOPE_API_KEY environment variable is not set." >&2
  echo "" >&2
  echo "Please set your DashScope API key:" >&2
  echo "  export DASHSCOPE_API_KEY='your-api-key'" >&2
  echo "" >&2
  echo "Get your API key from: https://bailian.console.aliyun.com" >&2
  exit 1
fi

# Validate query
if [ -z "$QUERY" ]; then
  echo "Usage: DASHSCOPE_API_KEY='your-key' ./search.sh <search query> [count]" >&2
  echo "Example 1: DASHSCOPE_API_KEY='sk-xxx' ./search.sh 'latest AI news'" >&2
  echo "Example 2: DASHSCOPE_API_KEY='sk-xxx' ./search.sh 'OpenAI updates' 10" >&2
  exit 1
fi

# Execute Python script with arguments
python3 -c "
import sys, json, requests, threading, time, os

api_key = os.environ['DASHSCOPE_API_KEY']
query = sys.argv[1]
count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

# SSE监听
sse_raw = []
session_ready = threading.Event()
session_id_holder = [None]

def listen_sse():
    headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'text/event-stream'}
    try:
        resp = requests.get('https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse', headers=headers, stream=True, timeout=60)
        buffer = b''
        for chunk in resp.iter_content(chunk_size=None):
            buffer += chunk
            while b'\\n' in buffer:
                line, buffer = buffer.split(b'\\n', 1)
                line = line.rstrip(b'\\r').decode('utf-8', errors='replace')
                if line.startswith('data:'):
                    data = line[5:].strip()
                    if 'sessionId=' in data:
                        session_id_holder[0] = data.split('sessionId=')[-1]
                        session_ready.set()
                    else:
                        sse_raw.append(data)
    except Exception as e:
        print(f'SSE连接错误: {e}', file=sys.stderr)
        sys.exit(1)

threading.Thread(target=listen_sse, daemon=True).start()
if not session_ready.wait(timeout=15):
    print('错误: 无法建立MCP会话连接', file=sys.stderr)
    sys.exit(1)

sid = session_id_holder[0]
msg_url = f'https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/message?sessionId={sid}'
h2 = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

# MCP握手
requests.post(msg_url, headers=h2, json={
    'jsonrpc':'2.0','id':0,'method':'initialize',
    'params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'bailian-search','version':'1.1.0'}}
}, timeout=10)
time.sleep(0.5)

requests.post(msg_url, headers=h2, json={'jsonrpc':'2.0','method':'notifications/initialized','params':{}}, timeout=10)
time.sleep(0.5)

# 搜索
requests.post(msg_url, headers=h2, json={
    'jsonrpc':'2.0','id':100,'method':'tools/call',
    'params':{'name':'bailian_web_search','arguments':{'query':query,'count':count}}
}, timeout=10)

# 等待结果
time.sleep(15)

# 解析结果
result_found = False
for item in sse_raw:
    try:
        d = json.loads(item)
        if d.get('id') == 100:
            result = d.get('result', {})
            content_list = result.get('content', [])
            for c in content_list:
                if c.get('type') == 'text':
                    sr = json.loads(c['text'])
                    pages = sr.get('pages', [])
                    if pages:
                        result_found = True
                        print(f'✅ Bailian Search 成功！共返回 {len(pages)} 条结果')
                        print('=' * 60)
                        for i, p in enumerate(pages, 1):
                            title = p.get('title', '无标题')
                            url = p.get('url', '')
                            snippet = p.get('snippet', '无摘要')
                            print(f'\\n【{i}】{title}')
                            print(f'   链接: {url}')
                            print(f'   摘要: {snippet[:200]}' + ('...' if len(snippet) > 200 else ''))
                        print('=' * 60)
                        sys.exit(0)
    except:
        continue

if not result_found:
    print(f'错误: 未找到搜索结果 (收到 {len(sse_raw)} 条SSE事件)', file=sys.stderr)
    if len(sse_raw) > 0:
        print('前3条事件:', file=sys.stderr)
        for i, evt in enumerate(sse_raw[:3]):
            print(f'  [{i}] {evt[:300]}', file=sys.stderr)
    sys.exit(1)
" "$QUERY" "$COUNT"