#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""盲预测脚本 - content-calibrator Skill的exec脚本
来源: 02手册§十一 W9 / FIX-07 exec直调LLM(不读对话历史)
模型: sensenova-6.7-flash-lite (免费, 通过SENSENOVA API直调)
硬约束: 脚本内部构造独立prompt,不传入任何对话上下文/历史消息
统一入口: record_direct_usage记录Token + db_logger日志
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
from mcps.shared.db_logger import get_logger
logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/calibrate_predict.py")
from mcps.shared.atomic_write import atomic_write_json
from mcps.shared.unified_llm import llm_chat

PREDICT_MODEL = os.environ.get("CALIBRATOR_PREDICT_MODEL", "sensenova-6.7-flash-lite")
DATA_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "predictions"

# FIX-07硬约束: 盲预测prompt只包含稿件+rubric_notes,不包含任何对话历史
PREDICT_PROMPT = """你是内容表现预测专家。基于以下稿件和评分标准备注,预测该内容发布后的互动表现。

评分标准备注: {rubric_notes}

请预测以下指标:
1. expected_views: 预计阅读/播放量范围(如"500-800")
2. expected_engagement: 预计互动率范围(如"3-5%",互动率=(点赞+评论+转发)/阅读量)
3. expected_viral: 是否有爆款潜力(布尔值true/false)

返回严格JSON格式:
{{"expected_views": "500-800", "expected_engagement": "3-5%", "expected_viral": false}}

仅返回JSON,不要其他文字。稿件内容:
"""


def _call_llm(prompt: str, system: str) -> str:
    """通过llm_chat统一入口调用LLM - 盲预测专用,无对话历史
    SenseNova reasoning模型可能返回reasoning而非content,需兼容处理"""
    result = llm_chat(
        prompt=prompt,
        system_prompt=system,
        caller="content-calibrator",
        model=PREDICT_MODEL,
        provider="sensenova",
        temperature=0.4,
        max_tokens=1024,
    )
    if not result.get("success"):
        raise ValueError(f"LLM调用失败: {result.get('error', '未知错误')}")
    # Token由llm_chat内部自动记录,无需手动调用record_direct_usage
    return result.get("raw_text", "").strip()


def _save_prediction(prediction: Dict, content_preview: str) -> str:
    """保存预测记录到文件,返回prediction_id"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    pred_id = f"pred_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    record = {"prediction_id": pred_id, "prediction": prediction,
              "content_preview": content_preview[:200], "created_at": datetime.now().isoformat()}
    pred_file = DATA_DIR / f"{pred_id}.json"
    atomic_write_json(pred_file, record, indent=2, ensure_ascii=False)
    return pred_id


def predict(content: str, rubric_notes: str) -> Dict:
    """盲预测主函数 - FIX-07: 不读对话历史,只喂稿件+rubric_notes

    Args:
        content (str): 参数说明
        rubric_notes (str): 参数说明

    Returns:
        Dict: 返回值说明
    """
    if not content or not content.strip():
        return {"success": False, "data": {}, "error": "内容不能为空", "code": "EMPTY_CONTENT"}
    if not rubric_notes:
        rubric_notes = "默认评分标准: ER情感共鸣/HP钩子强度/SR社会议题/QL金句密度/NA叙事性/AB受众广度/PV实用价值"
    try:
        # FIX-07硬约束: prompt只包含稿件+rubric_notes,无任何对话上下文
        prompt = PREDICT_PROMPT.format(rubric_notes=rubric_notes) + content[:8000]
        text = _call_llm(prompt, "你是内容表现预测专家,基于稿件内容预测互动数据。")
        # SenseNova reasoning模型可能将JSON嵌在reasoning文本中,需提取
        import re as _re
        json_match = _re.search(r'\{[^{}]*"expected_views"[^{}]*\}', text)
        if json_match:
            text = json_match.group(0)
        elif text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        prediction = json.loads(text)
        pred_id = _save_prediction(prediction, content)
        confidence = 0.6  # 默认置信度,后续复盘校准
        reasoning = f"基于稿件内容分析,钩子和情感维度评估互动潜力。预测ID: {pred_id}"
        return {"success": True, "data": {"prediction": prediction, "prediction_id": pred_id,
                "confidence": confidence, "reasoning": reasoning}, "error": None, "code": None}
    except json.JSONDecodeError as e:
        logger.error(f"predict LLM返回非JSON: {e}")
        return {"success": False, "data": {}, "error": f"LLM返回解析失败: {e}", "code": "LLM_PARSE_FAILED"}
    except (TimeoutError, OSError) as e:
        logger.error(f"predict LLM超时: {e}")
        return {"success": False, "data": {}, "error": f"LLM调用超时: {e}", "code": "LLM_TIMEOUT"}
    except Exception as e:
        logger.error(f"predict失败: {e}")
        return {"success": False, "data": {}, "error": str(e), "code": "PREDICT_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="内容盲预测(FIX-07: exec直调LLM)")
    parser.add_argument("--content", required=True, help="内容文本")
    parser.add_argument("--rubric-notes", default="", help="评分标准备注")
    args = parser.parse_args()
    result = predict(args.content, args.rubric_notes)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
