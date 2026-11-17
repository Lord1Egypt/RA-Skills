#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""content-calibrator统一入口脚本

PRE-01(R7阻断修复): _pipeline_has_skill_steps查找content_calibrator.py,
本脚本作为入口,根据--action参数分发到calibrate_score/predict/review/evolve脚本。

管道JSON格式:
  {"tool": "content-calibrator", "action": "score", "params": {"content": "...", "platform": "douyin"}}

调用方式:
  python content_calibrator.py --action score --content "内容文本" --platform douyin
  python content_calibrator.py --action score --params '{"content":"...","platform":"douyin"}'

统一入口: db_logger日志 + unified_llm.llm_chat Token记录(Phase 19)
"""
import argparse

import json
import sys
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))  # FIX-V58-002: 项目根目录,mcps.shared.db_logger需要
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcps.shared.db_logger import get_logger

logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/content_calibrator.py")

VALID_ACTIONS = {"score", "predict", "review", "evolve", "t3d_orchestrator"}

def _dispatch_score(params: dict) -> dict:
    """分发到calibrate_score.py的score函数"""
    from calibrate_score import score
    content = params.get("content", "")
    platform = params.get("platform", "")
    rubric_version = params.get("rubric_version", params.get("rubric-version", "v1"))
    return score(content, platform, rubric_version)

def _dispatch_predict(params: dict) -> dict:
    """分发到calibrate_predict.py的predict函数"""
    from calibrate_predict import predict
    content = params.get("content", "")
    rubric_notes = params.get("rubric_notes", params.get("rubric-notes", ""))
    return predict(content, rubric_notes)

def _dispatch_review(params: dict) -> dict:
    """分发到calibrate_review.py的review函数

    review函数签名: review(prediction_str: str, actual_str: str, platform: str)
    """
    from calibrate_review import review
    prediction_str = params.get("prediction", params.get("prediction_str", ""))
    if isinstance(prediction_str, dict):
        prediction_str = json.dumps(prediction_str, ensure_ascii=False)
    actual_str = params.get("actual", params.get("actual_str", ""))
    if isinstance(actual_str, dict):
        actual_str = json.dumps(actual_str, ensure_ascii=False)
    platform = params.get("platform", "default")
    return review(prediction_str, actual_str, platform)

def _dispatch_evolve(params: dict) -> dict:
    """分发到calibrate_evolve.py的evolve函数

    evolve函数签名: evolve(tenant_id: str, days: int)
    """
    from calibrate_evolve import evolve
    tenant_id = params.get("tenant_id", params.get("tenant", "default"))
    days = int(params.get("days", 7))
    return evolve(tenant_id, days)

def _dispatch_t3d_orchestrator(params: dict) -> dict:
    """分发到calibrate_t3d_orchestrator.py的run_t3d_review函数"""
    from calibrate_t3d_orchestrator import run_t3d_review
    return run_t3d_review()

DISPATCH_MAP = {
    "score": _dispatch_score,
    "predict": _dispatch_predict,
    "review": _dispatch_review,
    "evolve": _dispatch_evolve,
    "t3d_orchestrator": _dispatch_t3d_orchestrator,
}

def run(action: str, params: dict) -> dict[str, Any]:
    """统一入口: 根据action分发到对应脚本

    Args:
        action: score/predict/review/evolve/t3d_orchestrator
        params: 参数字典

    Returns:
        JSON结果 {success: bool, data: dict, error: str|null, code: str|null}
    """
    if action not in VALID_ACTIONS:
        return {"success": False, "data": {}, "error": f"无效action: {action}, 可选: {VALID_ACTIONS}", "code": "INVALID_ACTION"}

    dispatcher = DISPATCH_MAP.get(action)
    if not dispatcher:
        return {"success": False, "data": {}, "error": f"action {action} 无分发函数", "code": "NO_DISPATCHER"}

    try:
        # Phase 19: score已迁移到unified_llm.llm_chat统一入口,无需SENSENOVA_API_KEY检查
        logger.info(f"content-calibrator action={action} 开始执行")

        result = dispatcher(params)

        if isinstance(result, dict) and "success" in result:
            if result["success"]:
                logger.info(f"content-calibrator action={action} 执行成功")
            else:
                logger.warning(f"content-calibrator action={action} 执行失败: {result.get('error', '')}")
            return result
        else:
            return {"success": True, "data": result if isinstance(result, dict) else {"result": result}, "error": None, "code": None}

    except ModuleNotFoundError as e:
        logger.error(f"content-calibrator action={action} 模块导入失败: {e}")
        return {"success": False, "data": {}, "error": f"模块导入失败: {e}", "code": "MODULE_IMPORT_ERROR"}
    except ValueError as e:
        logger.error(f"content-calibrator action={action} 参数错误: {e}")
        return {"success": False, "data": {}, "error": str(e), "code": "VALUE_ERROR"}
    except Exception as e:
        logger.error(f"content-calibrator action={action} 执行异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "EXEC_ERROR"}

def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="content-calibrator统一入口脚本")
    parser.add_argument("--action", required=True, choices=sorted(VALID_ACTIONS),
                        help="执行动作: score/predict/review/evolve/t3d_orchestrator")
    parser.add_argument("--params", default="{}", help="参数JSON字符串")
    # 也支持直接传参(score/predict常用)
    parser.add_argument("--content", default=None, help="内容文本(score/predict用)")
    parser.add_argument("--platform", default=None, help="平台名(score/predict用)")
    parser.add_argument("--rubric-version", default=None, help="rubric版本(score用)")
    args = parser.parse_args()

    # 解析params JSON
    try:
        params = json.loads(args.params) if args.params else {}
    except json.JSONDecodeError as e:
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": f"params JSON解析失败: {e}", "code": "JSON_PARSE_ERROR"}, ensure_ascii=False))
        return 2

    # 直接传参覆盖params中的值
    if args.content is not None:
        params["content"] = args.content
    if args.platform is not None:
        params["platform"] = args.platform
    if args.rubric_version is not None:
        params["rubric_version"] = args.rubric_version

    result = run(args.action, params)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("success", False) else 1

if __name__ == "__main__":
    sys.exit(main())
