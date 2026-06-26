#!/usr/bin/env python3
"""
阶段3（简化版）：使用 Kimi API 快速提取行为模式
"""

import json
import sys
import os
from pathlib import Path
import anthropic

DATA_DIR = Path(__file__).parent.parent / "data"
OBS_DIR = DATA_DIR / "observations"
OBS_PATH = OBS_DIR / "observations.jsonl"

API_KEY = "sk-kimi-Sgsy7YYJPrkwJbUu0EvyGCIOZLbkdvNDcGzN0GrxknUNmXwfLlxlzcyG3Ufs3xAI"
BASE_URL = "https://api.kimi.com/coding/"
MODEL = "k2p5"

SIMPLE_PROMPT = """分析这段群聊记录，提取关键行为模式。

{chat_text}

要求：
1. 识别每个发言者的语言特征和表达习惯
2. 提取群体互动模式（谁主导话题、谁回应、幽默方式等）
3. 发现共同的价值观或兴趣点

输出纯JSON格式（不要markdown代码块）：
{{
  "chunk_id": {chunk_id},
  "observations": ["观察1", "观察2", ...],
  "behaviors": {{
    "发言者1": "特征描述",
    "发言者2": "特征描述"
  }}
}}"""

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
    print("阶段3：LLM 提取行为模式（简化版）\n")
    
    client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)
    
    # 测试连接
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(f"✓ API 连接成功\n")
    except Exception as e:
        print(f"✗ API 连接失败: {e}")
        sys.exit(1)
    
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
    
    observations = existing.copy()
    
    for i, chunk in enumerate(to_process, 1):
        chunk_id = chunk["chunk_id"]
        text = chunk["text"][:3000]  # 限制长度
        
        prompt = SIMPLE_PROMPT.format(chat_text=text, chunk_id=chunk_id)
        
        print(f"[{i}/{len(to_process)}] chunk {chunk_id}...", end=" ", flush=True)
        
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
                timeout=60
            )
            result_text = response.content[0].text
            
            # 解析 JSON
            try:
                # 清理可能的 markdown
                cleaned = result_text
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0]
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0]
                
                result = json.loads(cleaned.strip())
                observations.append({
                    "chunk_id": chunk_id,
                    "observations": result.get("observations", []),
                    "behaviors": result.get("behaviors", {})
                })
                print("✓")
            except json.JSONDecodeError:
                print(f"⚠ JSON解析失败，保存原文")
                observations.append({
                    "chunk_id": chunk_id,
                    "raw": result_text
                })
            
            # 每3个保存一次
            if i % 3 == 0:
                save_jsonl(OBS_PATH, observations)
                print(f"  已保存 {i}/{len(to_process)}")
                
        except Exception as e:
            print(f"✗ 错误: {str(e)[:50]}")
            continue
    
    # 最终保存
    save_jsonl(OBS_PATH, observations)
    print(f"\n✓ 完成！共处理 {len(observations)} 个观察")

if __name__ == "__main__":
    main()
