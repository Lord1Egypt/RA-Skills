"""
多模型交叉验证脚本（可选功能，需配置 API Key）

本脚本调用多个 LLM API 对同一内容进行验证，实现真正的多模型交叉验证。
需自行配置各模型 API Key。

支持的模型：
- GLM（智谱 AI）
- DeepSeek
- 混元（腾讯）
- Kimi（Moonshot）
- MiniMax

使用方法：
  python multi_model_verify.py --question "魏建军是谁？" --answer "魏建军是长城汽车创始人，1964年出生"

  # 或者验证文章/论点
  python multi_model_verify.py --text "比亚迪2024年销量400万辆，已经超过特斯拉成为全球第一"

依赖安装：
  pip install openai zhipuai dashscope moonshot-sdk
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional

# ============================================================
# 配置说明：
# 请在环境变量中设置各模型的 API Key：
# - ZHIPUAI_API_KEY（GLM）
# - DEEPSEEK_API_KEY
# - HUNYUAN_API_KEY
# - MOONSHOT_API_KEY（Kimi）
# - MINIMAX_API_KEY
# ============================================================


def verify_with_glm(question: str, answer: str, api_key: str) -> Dict:
    """使用 GLM 验证（智谱 AI）"""
    try:
        from zhipuai import ZhipuAI
        
        client = ZhipuAI(api_key=api_key)
        prompt = f"""请作为事实核查员，验证以下回答是否正确。

问题：{question}
回答：{answer}

请逐条验证回答中的事实，给出：
1. 事实列表
2. 每个事实的判定（正确/错误/无法验证）
3. 置信度（0-100%）
4. 依据

用中文回答。"""

        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "model": "GLM-4-Plus",
            "result": response.choices[0].message.content,
            "error": None
        }
    except Exception as e:
        return {"model": "GLM-4-Plus", "result": None, "error": str(e)}


def verify_with_deepseek(question: str, answer: str, api_key: str) -> Dict:
    """使用 DeepSeek 验证"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        prompt = f"""请作为质疑者，仔细核查以下回答中的事实，主动寻找反例或错误。

问题：{question}
回答：{answer}

请：
1. 列出回答中的每个事实
2. 主动寻找反例或错误信息
3. 给出你的判定（正确/错误/无法验证）和理由
4. 给出置信度（0-100%）

用中文回答。"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "model": "DeepSeek-V3",
            "result": response.choices[0].message.content,
            "error": None
        }
    except Exception as e:
        return {"model": "DeepSeek-V3", "result": None, "error": str(e)}


def verify_with_hunyuan(question: str, answer: str, api_key: str) -> Dict:
    """使用混元验证（腾讯）"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key, base_url="https://api.hunyuan.cloud.tencent.com/v1")
        prompt = f"""请综合各方信息，对以下回答进行事实核查，给出平衡、公正的判断。

问题：{question}
回答：{answer}

请：
1. 分解回答中的原子事实
2. 给出每个事实的判定（正确/错误/无法验证）
3. 给出置信度（0-100%）
4. 给出综合评分（0-100分）

用中文回答。"""

        response = client.chat.completions.create(
            model="hunyuan-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "model": "Hunyuan-Turbo",
            "result": response.choices[0].message.content,
            "error": None
        }
    except Exception as e:
        return {"model": "Hunyuan-Turbo", "result": None, "error": str(e)}


def verify_with_kimi(question: str, answer: str, api_key: str) -> Dict:
    """使用 Kimi 验证（Moonshot）"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        prompt = f"""请作为事实核查员，验证以下回答。

问题：{question}
回答：{answer}

请分解事实、逐一验证、给出判定和置信度。

用中文回答。"""

        response = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "model": "Kimi-K2",
            "result": response.choices[0].message.content,
            "error": None
        }
    except Exception as e:
        return {"model": "Kimi-K2", "result": None, "error": str(e)}


def verify_with_minimax(question: str, answer: str, api_key: str) -> Dict:
    """使用 MiniMax 验证"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key, base_url="https://api.minimax.chat/v1")
        prompt = f"""请作为事实核查员，验证以下回答中的事实。

问题：{question}
回答：{answer}

请给出每个事实的判定、置信度和依据。

用中文回答。"""

        response = client.chat.completions.create(
            model="MiniMax-Text-01",
            messages=[{"role": "user", "content": prompt}],
        )
        return {
            "model": "MiniMax-M2.7",
            "result": response.choices[0].message.content,
            "error": None
        }
    except Exception as e:
        return {"model": "MiniMax-M2.7", "result": None, "error": str(e)}


def multi_model_verify(question: str, answer: str, text: Optional[str] = None) -> Dict:
    """
    真正的多模型交叉验证。
    
    Args:
        question: 问题（模式A）
        answer: 回答（模式A）
        text: 文章/论点文本（模式B）
    
    Returns:
        各模型的验证结果
    """
    results = {
        "question": question,
        "answer": answer,
        "text": text,
        "results": []
    }
    
    # GLM
    glm_key = os.getenv("ZHIPUAI_API_KEY")
    if glm_key:
        print("🔍 正在调用 GLM-4-Plus 验证...")
        results["results"].append(verify_with_glm(question, answer or text or "", glm_key))
    
    # DeepSeek
    ds_key = os.getenv("DEEPSEEK_API_KEY")
    if ds_key:
        print("🔍 正在调用 DeepSeek-V3 验证...")
        results["results"].append(verify_with_deepseek(question, answer or text or "", ds_key))
    
    # 混元
    hy_key = os.getenv("HUNYUAN_API_KEY")
    if hy_key:
        print("🔍 正在调用 Hunyuan-Turbo 验证...")
        results["results"].append(verify_with_hunyuan(question, answer or text or "", hy_key))
    
    # Kimi
    kimi_key = os.getenv("MOONSHOT_API_KEY")
    if kimi_key:
        print("🔍 正在调用 Kimi-K2 验证...")
        results["results"].append(verify_with_kimi(question, answer or text or "", kimi_key))
    
    # MiniMax
    mm_key = os.getenv("MINIMAX_API_KEY")
    if mm_key:
        print("🔍 正在调用 MiniMax-M2.7 验证...")
        results["results"].append(verify_with_minimax(question, answer or text or "", mm_key))
    
    return results


def print_results(results: Dict):
    """打印验证结果"""
    print("\n" + "="*60)
    print("🔍 多模型交叉验证结果")
    print("="*60)
    
    for r in results["results"]:
        print(f"\n【{r['model']}】")
        if r["error"]:
            print(f"  ❌ 错误：{r['error']}")
        else:
            print(r["result"])
    
    print("\n" + "="*60)
    print(f"总计：{len([r for r in results['results'] if not r['error']])} 个模型验证成功，{len([r for r in results['results'] if r['error']])} 个失败")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="多模型交叉验证（需配置 API Key）")
    parser.add_argument("--question", type=str, default="", help="问题（模式A）")
    parser.add_argument("--answer", type=str, default="", help="回答（模式A）")
    parser.add_argument("--text", type=str, default="", help="文章/论点文本（模式B）")
    parser.add_argument("--config", type=str, default="", help="配置文件路径（YAML）")
    
    args = parser.parse_args()
    
    if not args.question and not args.text:
        print("❌ 请提供 --question 和 --answer（模式A），或 --text（模式B）")
        sys.exit(1)
    
    results = multi_model_verify(args.question, args.answer, args.text)
    
    if not results["results"]:
        print("❌ 没有配置任何 API Key，无法进行验证。")
        print("\n请设置以下环境变量中的至少一个：")
        print("  - ZHIPUAI_API_KEY（GLM）")
        print("  - DEEPSEEK_API_KEY")
        print("  - HUNYUAN_API_KEY（混元）")
        print("  - MOONSHOT_API_KEY（Kimi）")
        print("  - MINIMAX_API_KEY")
        sys.exit(1)
    
    print_results(results)
    
    # 保存结果到 JSON
    output_file = "verification_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ 结果已保存到 {output_file}")


if __name__ == "__main__":
    main()
