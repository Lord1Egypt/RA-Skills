#!/bin/bash
# parse-tokens.sh — Parse token usage from agent output log
# Usage: parse-tokens.sh <log_file>
# Output: JSON {"input": N, "output": N, "cache_read": N, "cache_write": N}
#
# Supports Claude Code (--print) and Codex output formats.

LOG_FILE="${1:?Usage: parse-tokens.sh <log_file>}"

if [[ ! -f "$LOG_FILE" ]]; then
  echo '{"input":0,"output":0,"cache_read":0,"cache_write":0}'
  exit 0
fi

python3 -c "
import re, json, sys

text = open('$LOG_FILE', 'r', errors='replace').read()

result = {'input': 0, 'output': 0, 'cache_read': 0, 'cache_write': 0}

# ---- Claude Code (--output-format json) — direct JSON sidecar file ----
# dispatch.sh passes CC_JSON_FILE (not LOG_FILE) when --output-format json is used.
# The file is the raw JSON object from claude --print --output-format json.
# Require Claude-specific signature fields ('type' in result/success/error AND 'usage'
# with 'input_tokens') to avoid false-positive on Codex logs that happen to be valid JSON.
try:
    obj = json.loads(text)
    obj_type = obj.get('type', '')
    usage = obj.get('usage', {})
    is_claude_output = (
        obj_type in ('result', 'success', 'error') and
        'input_tokens' in usage and
        'output_tokens' in usage
    )
    if is_claude_output:
        result['input']       = usage.get('input_tokens', 0)
        result['output']      = usage.get('output_tokens', 0)
        result['cache_read']  = usage.get('cache_read_input_tokens', 0)
        result['cache_write'] = usage.get('cache_creation_input_tokens', 0)
        print(json.dumps(result))
        sys.exit(0)
except Exception:
    pass

# ---- Claude Code (--print) ----
# Format 1: 'Tokens: 1234 input, 567 output'
m = re.search(r'Tokens:\s*([\d,]+)\s*input,\s*([\d,]+)\s*output', text)
if m:
    result['input'] = int(m.group(1).replace(',', ''))
    result['output'] = int(m.group(2).replace(',', ''))

# Format 2: full cost line with cache
# 'Tokens: 12345 input (1234 cache read, 567 cache write), 890 output'
m2 = re.search(
    r'Tokens:\s*([\d,]+)\s*input\s*\(?\s*([\d,]*)\s*cache\s*read[,\s]*([\d,]*)\s*cache\s*write\s*\)?,\s*([\d,]+)\s*output',
    text, re.IGNORECASE
)
if m2:
    result['input']       = int(m2.group(1).replace(',', ''))
    result['cache_read']  = int(m2.group(2).replace(',', '')) if m2.group(2) else 0
    result['cache_write'] = int(m2.group(3).replace(',', '')) if m2.group(3) else 0
    result['output']      = int(m2.group(4).replace(',', ''))

# ---- Codex ----
# Format: 'prompt_tokens: 1234' / 'completion_tokens: 567'
m_in  = re.search(r'prompt_tokens[:\s]+([\d,]+)',     text)
m_out = re.search(r'completion_tokens[:\s]+([\d,]+)', text)
if m_in and not result['input']:
    result['input'] = int(m_in.group(1).replace(',', ''))
if m_out and not result['output']:
    result['output'] = int(m_out.group(1).replace(',', ''))

# Format: 'tokens used\n<number>' (Codex actual output — total token count)
# Use the LAST occurrence (most recent / largest cumulative count)
m_codex = list(re.finditer(r'tokens used\s*\n\s*([\d,]+)', text, re.IGNORECASE))
if m_codex and not result['input']:
    total = int(m_codex[-1].group(1).replace(',', ''))
    # Codex doesn't split input/output; store as input (output stays 0)
    result['input'] = total

print(json.dumps(result))
"
