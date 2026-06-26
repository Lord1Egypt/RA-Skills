#!/usr/bin/env python3
"""
阶段4（简化版）：合成分析报告
"""

import json
import sys
from pathlib import Path
import anthropic

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
OBS_PATH = DATA_DIR / "observations" / "observations.jsonl"

API_KEY = "sk-kimi-Sgsy7YYJPrkwJbUu0EvyGCIOZLbkdvNDcGzN0GrxknUNmXwfLlxlzcyG3Ufs3xAI"
BASE_URL = "https://api.kimi.com/coding/"
MODEL = "k2p5"

def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def main():
    print("阶段4：合成分析报告\n")
    
    client = anthropic.Anthropic(api_key=API_KEY, base_url=BASE_URL)
    
    # 加载观察数据
    observations = load_jsonl(OBS_PATH)
    print(f"加载 {len(observations)} 条观察记录\n")
    
    # 汇总所有观察
    all_obs = []
    all_behaviors = {}
    
    for obs in observations:
        all_obs.extend(obs.get("observations", []))
        for speaker, desc in obs.get("behaviors", {}).items():
            if speaker not in all_behaviors:
                all_behaviors[speaker] = []
            all_behaviors[speaker].append(desc)
    
    # 构建 prompt
    obs_text = "\n".join([f"- {o}" for o in all_obs[:30]])  # 限制数量
    behaviors_text = "\n\n".join([
        f"**{speaker}**:\n" + "\n".join([f"  - {d}" for d in descs[:3]])
        for speaker, descs in all_behaviors.items()
    ])
    
    prompt = f"""基于以下群聊行为观察，生成一份群体分析报告。

## 群体行为观察汇总

{obs_text}

## 成员行为特征

{behaviors_text}

## 要求

生成一份markdown格式的分析报告，包含：
1. 群体概览（群聊风格、氛围、核心价值观）
2. 成员画像（每个发言者的特征总结）
3. 互动模式（谁主导、谁回应、幽默方式等）
4. 话题偏好（常聊什么、怎么聊）

输出纯markdown，不要代码块包裹。"""
    
    print("调用 LLM 生成报告...")
    
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text
        
        # 保存
        OUTPUTS_DIR.mkdir(exist_ok=True)
        output_path = OUTPUTS_DIR / "soul.md"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"\n✓ 报告已保存: {output_path}")
        print(f"  字数: {len(result)} 字符")
        
        # 显示预览
        print("\n--- 预览 ---\n")
        print(result[:1500])
        print("\n...")
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
