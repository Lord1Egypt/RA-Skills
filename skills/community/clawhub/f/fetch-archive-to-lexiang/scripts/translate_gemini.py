#!/usr/bin/env python3
"""用 Gemini API 将英文 Markdown 翻译为中英对照格式"""
import requests, json, re, os, sys, time

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def translate_chunk(text):
    """翻译一段英文为中英对照"""
    prompt = """你是专业翻译。将以下英文 Markdown 翻译为中英对照格式。规则：
1. 每段英文原文后紧跟对应的中文翻译，之间用一个空行分隔
2. 保留所有 Markdown 格式（标题、链接、引用、列表等）
3. 🚨 标题必须单行双语：把中文译文直接接在英文标题后，用 ` / ` 分隔，写成同一行 `## English Title / 中文标题`。禁止把中文标题另起一行成为独立标题（否则目录里一个章节会占两行）
4. 翻译要自然流畅，专业术语保留英文并附中文注释
5. 不加分隔线、不加国旗emoji
6. 保留原文中的图片引用 ![](...)

英文原文：
""" + text

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 16000}
    }
    
    for attempt in range(3):
        try:
            resp = requests.post(URL, json=payload, timeout=120)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            elif resp.status_code == 429:
                print(f"    Rate limited, waiting 30s...")
                time.sleep(30)
            else:
                print(f"    Error {resp.status_code}: {resp.text[:200]}")
                time.sleep(5)
        except Exception as e:
            print(f"    Exception: {e}")
            time.sleep(5)
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 translate_gemini.py <input_md> [output_md]")
        sys.exit(1)
    
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".md", "_translated.md")
    
    with open(src, "r") as f:
        content = f.read()
    
    # 按段落分组，每组 ~4000 字符
    paragraphs = content.split("\n\n")
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 > 4000:
            chunks.append(current)
            current = p
        else:
            current = current + "\n\n" + p if current else p
    if current:
        chunks.append(current)
    
    print(f"Split into {len(chunks)} chunks for translation")
    
    translated_parts = []
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] Translating {len(chunk)} chars...", end=" ", flush=True)
        result = translate_chunk(chunk)
        if result:
            translated_parts.append(result)
            print("OK")
        else:
            print("FAILED - keeping original")
            translated_parts.append(chunk)
        time.sleep(2)  # Rate limit
    
    output = "\n\n".join(translated_parts)
    
    with open(dst, "w") as f:
        f.write(output)
    
    print(f"\nDone! Translated file: {dst}")
    print(f"Original: {len(content)} chars -> Translated: {len(output)} chars")

if __name__ == "__main__":
    main()
