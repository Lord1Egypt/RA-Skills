#!/usr/bin/env python3
"""
阶段3（OpenClaw Kimi版）：使用 OpenClaw 配置的 Kimi API
"""

import json
import sys
import os
from pathlib import Path

# 使用 OpenAI 兼容的 API
from openai import OpenAI

DATA_DIR = Path(__file__).parent.parent / "data"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
OBS_DIR = DATA_DIR / "observations"
OBS_PATH = OBS_DIR / "observations.jsonl"

# OpenClaw Kimi Coding API 配置
API_KEY = os.environ.get("KIMI_API_KEY") or "sk-kimi-Sgsy7YYJPrkwJbUu0EvyGCIOZLbkdvNDcGzN0GrxknUNmXwfLlxlzcyG3Ufs3xAI"
BASE_URL = "https://api.kimi.com/coding/"
MODEL = "kimi-k2-5"

def load_jsonl(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def save_jsonl(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def main():
    print("阶段3：LLM 提取行为模式（OpenClaw Kimi API 模式）\n")
    
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    # 测试连接
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print(f"✓ API 连接成功，使用模型: {MODEL}\n")
    except Exception as e:
        print(f"✗ API 连接失败: {e}")
        print(f"Key: {API_KEY[:20]}...")
        print(f"Base URL: {BASE_URL}")
        sys.exit(1)
    
    # 加载 prompt
    prompt_template = (PROMPTS_DIR / "extract_patterns.md").read_text(encoding="utf-8")
    
    # 加载 chunks
    chunks = load_jsonl(DATA_DIR / "denoised" / "chunks.jsonl")
    print(f"读入 {len(chunks)} 个对话块\n")
    
    # 加载已有结果
    existing = load_jsonl(OBS_PATH) if OBS_PATH.exists() else []
    done_ids = {o["chunk_id"] for o in existing}
    print(f"已有结果：{len(done_ids)} 个")
    
    # 需要处理的 chunks
    to_process = [c for c in chunks if c["chunk_id"] not in done_ids]
    print(f"需要处理：{len(to_process)} 个\n")
    
    if not to_process:
        print("✓ 所有块已处理完成")
        return
    
    # 逐个处理
    observations = existing.copy()
    
    for i, chunk in enumerate(to_process, 1):
        chunk_id = chunk["chunk_id"]
        text = chunk["text"]
        time_range = f"{chunk['start_time']} ~ {chunk['end_time']}"
        
        prompt = (
            prompt_template
            .replace("{{CHAT_TEXT}}", text)
            .replace("{{CHUNK_ID}}", str(chunk_id))
            .replace("{{TIME_RANGE}}", time_range)
        )
        
        print(f"[{i}/{len(to_process)}] 处理 chunk {chunk_id}...", end=" ")
        
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.3
            )
            result_text = response.choices[0].message.content
            
            # 解析结果
            try:
                result = json.loads(result_text)
                observation = {
                    "chunk_id": chunk_id,
                    "time_range": time_range,
                    "observations": result.get("observations", []),
                    "behaviors": result.get("behaviors", {}),
                    "raw": result_text[:500]
                }
                observations.append(observation)
                print("✓")
                
                # 每5个保存一次
                if i % 5 == 0:
                    save_jsonl(OBS_PATH, observations)
                    print(f"  已保存进度 ({i}/{len(to_process)})\n")
                    
            except json.JSONDecodeError:
                print(f"⚠ 非JSON格式，保存原文")
                observations.append({
                    "chunk_id": chunk_id,
                    "time_range": time_range,
                    "raw": result_text,
                    "parse_error": True
                })
                
        except Exception as e:
            print(f"✗ API 错误: {e}")
            continue
    
    # 最终保存
    save_jsonl(OBS_PATH, observations)
    print(f"\n✓ 完成！共处理 {len(observations)} 个观察")

if __name__ == "__main__":
    main()
