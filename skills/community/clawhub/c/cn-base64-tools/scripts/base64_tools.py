#!/usr/bin/env python3
import sys, json, base64

def encode(text):
    return base64.b64encode(text.encode()).decode()

def decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except:
        return None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({'error': '用法: base64_tools.py encode/decode <text>'}))
    else:
        op, text = sys.argv[1], ' '.join(sys.argv[2:])
        result = encode(text) if op == 'encode' else decode(text)
        print(json.dumps({'result': result}, ensure_ascii=False))
