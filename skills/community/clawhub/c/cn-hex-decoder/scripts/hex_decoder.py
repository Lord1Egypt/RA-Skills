#!/usr/bin/env python3
import sys, json

def encode(text):
    return text.encode().hex()

def decode(hex_str):
    try:
        return bytes.fromhex(hex_str).decode()
    except:
        return None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({'error': '用法: hex_decoder.py encode/decode <text>'}))
    else:
        op, text = sys.argv[1], ' '.join(sys.argv[2:])
        print(json.dumps({'result': encode(text) if op=='encode' else decode(text)}, ensure_ascii=False))
