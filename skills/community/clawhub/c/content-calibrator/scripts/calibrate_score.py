#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容7维评分脚本 - content-calibrator Skill的exec脚本
来源: 02手册§十一 W9 / FIX-06降频+免费模型
统一入口: unified_llm.llm_chat() (Phase 19已消除直调SenseNova, R75.2连接统一化)
Token记录: llm_chat内部自动写入llm_call_logs表
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
from mcps.shared.db_logger import get_logger
logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/calibrate_score.py")
VALID_PLATFORMS = {"douyin", "xiaohongshu", "bilibili", "zhihu", "juejin", "csdn",
                   "baijiahao", "sohu", "jianshu", "wechat", "weibo", "kuaishou",
                   "xianyu", "tiktok", "douyin_image", "toutiao", "headlines",
                   "xiaohongshu_image", "kuaishou_image"}
THRESHOLD = 6.0  # 综合分及格线
DIMENSIONS = ["ER", "HP", "SR", "QL", "NA", "AB", "PV"]
WEIGHTS = {"ER": 1.5, "HP": 1.5, "SR": 1.5, "QL": 1.0, "NA": 1.0, "AB": 1.0, "PV": 1.0}
WEIGHT_SUM = sum(WEIGHTS.values())  # 8.5

# P2-07修复: rubric进化后的权重文件目录
RUBRICS_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "rubrics"


def _load_rubric_weights(platform: str) -> tuple:
    """加载平台对应的rubric权重(P2-07修复: evolve脚本写入的权重)

    Returns: (weights_dict, weight_sum, rubric_version)
    """
    rubric_file = RUBRICS_DIR / f"{platform}.json"
    if rubric_file.exists():
        try:
            rubric = json.loads(rubric_file.read_text(encoding="utf-8"))
            weights = rubric.get("weights", WEIGHTS)
            # 确保所有维度都存在
            for d in DIMENSIONS:
                weights.setdefault(d, WEIGHTS[d])
            return weights, sum(weights.values()), rubric.get("updated_at", "evolved")
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"读取rubric权重失败{platform}: {e}, 使用默认权重")
    return dict(WEIGHTS), WEIGHT_SUM, "v1"

SCORE_PROMPT = """你是内容质量评估专家。对以下内容按7个维度各打0-10分(整数)。

7维度说明:
- ER(情感共鸣): 内容引发读者情感反应的能力
- HP(钩子强度): 前3秒/首段抓注意力的能力
- SR(社会议题): 与社会热点/普遍议题的关联度
- QL(金句密度): 可传播金句/核心观点的密度
- NA(叙事性): 故事性/叙事流畅度
- AB(受众广度): 内容覆盖的受众范围
- PV(实用价值): 读者可获得的实用信息/技巧

平台: {platform}

返回严格JSON格式:
{{"ER": 8, "HP": 7, "SR": 6, "QL": 7, "NA": 8, "AB": 7, "PV": 9, "suggestions": ["建议1", "建议2"]}}

仅返回JSON,不要其他文字。内容:
"""


def _call_llm(prompt: str, system: str) -> str:
    """V58.0修复(BUG-WAVE23-004): 使用unified_llm统一入口替代直接调用SenseNova API

    根因: sensenova-6.7-flash-lite是reasoning模型,思考过程占满max_tokens(1024),
          content字段为空,JSON输出无法生成,导致"LLM返回解析失败: char 0"
    修复: 通过unified_llm.llm_chat()统一入口,使用sensenova默认模型glm-5.2(非reasoning)
          +fallback chain(sensenova→zhipu→dashscope)确保可用性
    (R75.2连接统一化: 禁止独立API调用,使用unified_llm统一入口)
    Token记录: llm_chat内部自动写入llm_call_logs表,无需手动record_direct_usage
    """
    from mcps.shared.unified_llm import llm_chat

    result = llm_chat(
        prompt=prompt,
        system_prompt=system,
        caller="content-calibrator",
        max_tokens=1024,
        temperature=0.3,
        fallback_chain=["sensenova", "zhipu", "dashscope"],
    )

    if not result.get("success"):
        raise ValueError(f"LLM调用失败: {result.get('error', 'unknown error')}")

    text = result.get("raw_text", "")
    return text.strip()


def score(content: str, platform: str, rubric_version: str) -> Dict:
    """7维评分主函数

    Args:
        content (str): 参数说明
        platform (str): 参数说明
        rubric_version (str): 参数说明

    Returns:
        Dict: 返回值说明
    """
    if not content or not content.strip():
        return {"success": False, "data": {}, "error": "内容不能为空", "code": "EMPTY_CONTENT"}
    if platform not in VALID_PLATFORMS:
        return {"success": False, "data": {}, "error": f"无效平台: {platform}", "code": "INVALID_PLATFORM"}
    try:
        prompt = SCORE_PROMPT.format(platform=platform) + content[:8000]
        text = _call_llm(prompt, "你是内容质量评估专家,擅长多维度内容分析。")
        # SenseNova reasoning模型可能将JSON嵌在reasoning文本中,需提取
        import re as _re
        json_match = _re.search(r'\{[^{}]*"ER"[^{}]*\}', text)
        if json_match:
            text = json_match.group(0)
        elif text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        scores_data = json.loads(text)
        scores = {d: int(scores_data.get(d, 0)) for d in DIMENSIONS}
        for d in DIMENSIONS:
            scores[d] = max(0, min(10, scores[d]))
        # P2-07修复: 读取evolve脚本写入的rubric权重(如果存在)
        weights, weight_sum, rubric_ver = _load_rubric_weights(platform)
        composite = round(sum(scores[d] * weights[d] for d in DIMENSIONS) / weight_sum * 2.0, 2)
        suggestions = scores_data.get("suggestions", [])
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]
        return {"success": True, "data": {"scores": scores, "composite": composite,
                "threshold_pass": composite >= THRESHOLD, "suggestions": suggestions[:5],
                "rubric_version": rubric_ver, "weights": weights,
                "content": content},  # V58.0修复: 传递content给下游步骤(配图生成需要prompt)
                "error": None, "code": None}
    except json.JSONDecodeError as e:
        logger.error(f"score LLM返回非JSON: {e}")
        return {"success": False, "data": {}, "error": f"LLM返回解析失败: {e}", "code": "LLM_PARSE_FAILED"}
    except (TimeoutError, OSError) as e:
        logger.error(f"score LLM超时: {e}")
        return {"success": False, "data": {}, "error": f"LLM调用超时: {e}", "code": "LLM_TIMEOUT"}
    except Exception as e:
        logger.error(f"score失败: {e}")
        return {"success": False, "data": {}, "error": str(e), "code": "SCORE_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="内容7维评分")
    parser.add_argument("--content", required=True, help="内容文本")
    parser.add_argument("--platform", required=True, help="平台名")
    parser.add_argument("--rubric-version", default="v1", help="rubric版本")
    args = parser.parse_args()
    result = score(args.content, args.platform, args.rubric_version)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
