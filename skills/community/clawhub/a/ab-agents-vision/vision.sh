#!/bin/bash
# AB Agents Vision — MiniMax VL API wrapper

export MINIMAX_API_KEY="${MINIMAX_API_KEY:-$(grep MINIMAX_API_KEY ~/.minimax-env 2>/dev/null | cut -d'"' -f2)}"
export MINIMAX_API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"
export PATH="/root/.local/bin:$HOME/.local/bin:$PATH"

IMAGE_PATH="$1"
PROMPT="${2:-Describe this image in detail}"

if [ -z "$IMAGE_PATH" ]; then
    echo "Usage: vision.sh <image_path> [prompt]"
    exit 1
fi

if [ -z "$MINIMAX_API_KEY" ]; then
    echo "Error: MINIMAX_API_KEY not set"
    exit 1
fi

# MCP call via uvx
{
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"vision","version":"1.0"}}}'
    sleep 1
    echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"understand_image\",\"arguments\":{\"prompt\":\"$PROMPT\",\"image_source\":\"$IMAGE_PATH\"}}}"
} | uvx minimax-coding-plan-mcp 2>/dev/null | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        resp = json.loads(line)
        if resp.get('id') == 2 and 'result' in resp:
            for item in resp['result'].get('content', []):
                if item.get('type') == 'text' and not item.get('isError'):
                    print(item['text'])
                    exit(0)
    except: continue
print('Error: No response from vision API')
"
