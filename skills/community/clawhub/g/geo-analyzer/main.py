import os
import json
import logging
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field
from typing import List, Optional

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pydantic Schema 定义，用于校验大模型返回的数据结构
class GEOAnalysisResult(BaseModel):
    mentioned: bool = Field(description="是否提及了目标品牌")
    sentiment: str = Field(description="情感倾向：positive/negative/neutral/none")
    context: Optional[str] = Field(description="提及目标品牌的具体上下文句子，未提及则为 null", default=None)
    competitors_mentioned: List[str] = Field(description="作为推荐被提及的其他竞品品牌列表", default_factory=list)

def analyze_geo_performance(brand_name: str, category_keyword: str) -> str:
    """
    测试和验证特定品牌/产品的 GEO 表现。
    第一阶段：咨询模型获取行业解决方案。
    第二阶段：让模型担任裁判，提取并验证提及情况。
    第三阶段：基于结构化数据生成约 500 字的专业分析报告。
    """
    # 安全要求：从环境变量读取 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        error_msg = "未找到 DEEPSEEK_API_KEY 环境变量。请确保在运行前已正确配置。"
        logger.error(error_msg)
        return json.dumps({"error": error_msg}, ensure_ascii=False)

    # 初始化 OpenAI 客户端，Base URL 指向 DeepSeek API
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

    try:
        # ==========================================
        # 阶段 1: 探针阶段 (Probing)
        # ==========================================
        logger.info(f"阶段 1: 开始探测行业关键词 '{category_keyword}'")
        probing_prompt = f"作为一个客观的行业专家，请为我推荐几个优秀的【{category_keyword}】解决方案，并详细说明推荐理由。"
        
        probing_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": probing_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        probing_text = probing_response.choices[0].message.content
        logger.info("阶段 1: 探测完成，成功获取大模型推荐文本。")

        # ==========================================
        # 阶段 2: 裁判阶段 (LLM-as-a-Judge)
        # ==========================================
        logger.info(f"阶段 2: 启动裁判模型，分析目标品牌 '{brand_name}' 的提及情况...")
        
        judge_system_prompt = (
            "你是一个专业的数据提取专家和文本审核员。请仔细阅读用户提供的文本，提取出结构化的评估结果。\n"
            "严格遵循 JSON 格式输出，不要包含任何多余的解释、对话前缀或 Markdown 标记。"
        )
        
        judge_user_prompt = (
            f"目标品牌/产品：{brand_name}\n\n"
            f"待分析文本：\n{probing_text}\n\n"
            f"请提取信息并以如下 JSON 格式返回结果（必须完全符合此结构）：\n"
            f"{{\n"
            f'  "mentioned": true 或 false,\n'
            f'  "sentiment": "positive" 或 "negative" 或 "neutral" 或 "none",\n'
            f'  "context": "提及目标品牌的具体上下文句子，如果未提及则填 null",\n'
            f'  "competitors_mentioned": ["竞品1", "竞品2"]\n'
            f"}}"
        )
        
        # 裁判模型需要极低的温度以保证结果稳定可复现，并启用强制 JSON 返回模式
        judge_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": judge_system_prompt},
                {"role": "user", "content": judge_user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        judge_result_str = judge_response.choices[0].message.content
        
        try:
            # 使用 JSON 解析和 Pydantic Schema 进行二次强校验
            raw_data = json.loads(judge_result_str)
            validated_result = GEOAnalysisResult(**raw_data)
            logger.info("阶段 2: 裁判分析完成并成功通过结构化校验。")

            # ==========================================
            # 阶段 3: 报告生成阶段 (Report Generation)
            # ==========================================
            logger.info("阶段 3: 正在生成 GEO 分析报告...")

            sentiment_cn = {
                "positive": "正面（Positive）",
                "negative": "负面（Negative）",
                "neutral": "中性（Neutral）",
                "none": "无（未被提及）"
            }.get(validated_result.sentiment, validated_result.sentiment)

            competitors_str = "、".join(validated_result.competitors_mentioned) if validated_result.competitors_mentioned else "无"

            report_system_prompt = (
                "你是一位专业的 GEO（生成式引擎优化）分析师，擅长撰写品牌在大模型中的曝光分析报告。"
                "请用专业、客观、有洞察力的语言撰写报告，报告字数约 500 字，使用中文，结构清晰。"
            )

            report_user_prompt = (
                f"请基于以下数据，为品牌「{brand_name}」撰写一份完整的 GEO 表现分析报告。\n\n"
                f"【测试行业关键词】{category_keyword}\n"
                f"【品牌是否被提及】{'是' if validated_result.mentioned else '否'}\n"
                f"【情感倾向】{sentiment_cn}\n"
                f"【提及上下文】{validated_result.context or '无'}\n"
                f"【同场景被提及的竞品】{competitors_str}\n\n"
                f"【大模型原始推荐文本（供参考）】\n{probing_text}\n\n"
                f"报告须包含以下四个部分：\n"
                f"1. 测试概述（说明测试方法与目标）\n"
                f"2. 核心发现（品牌曝光情况与情感倾向分析）\n"
                f"3. 竞品格局（分析同场景中被点名的竞争对手）\n"
                f"4. 优化建议（给出 2~3 条具体可执行的 GEO 优化建议）"
            )

            report_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": report_system_prompt},
                    {"role": "user", "content": report_user_prompt}
                ],
                temperature=0.6,
                max_tokens=1500
            )

            report_text = report_response.choices[0].message.content
            logger.info("阶段 3: 分析报告生成完成。")

            # 组合最终输出：结构化 JSON + 分析报告
            final_output = {
                "structured_result": validated_result.model_dump(),
                "report": report_text
            }
            return json.dumps(final_output, ensure_ascii=False, indent=2)

        except json.JSONDecodeError:
            logger.error(f"JSON 解析异常，大模型未按规范输出。原始返回：{judge_result_str}")
            return json.dumps({
                "error": "裁判模型未能返回规范的 JSON 格式数据",
                "raw_response": judge_result_str
            }, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Pydantic 结构校验失败: {str(e)}")
            return json.dumps({
                "error": f"结果验证失败: {str(e)}",
                "raw_response": judge_result_str
            }, ensure_ascii=False)

    except OpenAIError as e:
        logger.error(f"DeepSeek API 调用失败: {str(e)}")
        return json.dumps({"error": f"DeepSeek API 错误: {str(e)}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"未预期的异常: {str(e)}")
        return json.dumps({"error": f"系统运行错误: {str(e)}"}, ensure_ascii=False)

if __name__ == "__main__":
    # 提供给开发者的本地测试入口
    import argparse
    parser = argparse.ArgumentParser(description="测试 GEO Performance 分析插件")
    parser.add_argument("--brand", type=str, required=True, help="需要验证的目标品牌名称")
    parser.add_argument("--category", type=str, required=True, help="目标行业或痛点关键词")
    args = parser.parse_args()
    
    print(f"\n[测试启动] 正在验证行业 [{args.category}] 中的品牌 [{args.brand}]...")
    raw = analyze_geo_performance(args.brand, args.category)

    try:
        output = json.loads(raw)
        if "report" in output:
            print("\n========== 结构化评估数据 ==========")
            print(json.dumps(output["structured_result"], ensure_ascii=False, indent=2))
            print("\n========== GEO 分析报告（约 500 字）==========")
            print(output["report"])
        else:
            print(raw)
    except Exception:
        print(raw)
