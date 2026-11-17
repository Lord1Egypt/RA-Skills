#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""内容合规检查(U19管道步骤) — v25.0合并自content-compliance-checker

R规则: R1(运行时证据) / R34(虚假实现检测) / R38(测试闭环) / R75.5(Skill去重)
来源: BUG-V4A-008 (E2E-DAILY缺少必需Skill content_compliance_checker)
v25.0: 合并到content-qa-guard,作为管道U19步骤的执行入口

功能: 委托risk-detector执行合规检查,返回管道步骤契约格式的结果
使用: python check_compliance.py --content "<text>" --platform "<platform>"
"""
import os
import sys
import json
import argparse
from typing import Any

# db_logger统一日志 (R14统一入口铁律)
# 路径: skills/_lazy/content-qa-guard/scripts/ → parents[4]=项目根
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[4] / "scripts"))
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[4]))  # 项目根(R45修复: parents[5]→parents[4])
from mcps.shared.db_logger import get_logger
logger = get_logger("content-qa-guard", source="check_compliance.py(v25.0合并)")

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# risk-detector脚本路径
RISK_DETECTOR_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'risk-detector', 'scripts'
)


def check_compliance(content: str, platform: str = "", content_type: str = "") -> dict[str, Any]:
    """执行内容合规检查(U19管道步骤)

    Args:
        content: 待检查内容文本
        platform: 目标平台
        content_type: 内容类型

    Returns:
        {success, data: {risk_level, score, passed, block, details}, error, code}
    """
    # 空内容直接通过(R38边界场景)
    if not content or not content.strip():
        return {
            "success": True,
            "data": {
                "risk_level": "SAFE",
                "score": 100,
                "passed": True,
                "block": False,
                "details": {"reason": "empty_content_skip"}
            },
            "error": None,
            "code": "EMPTY_CONTENT"
        }

    # 委托risk-detector执行全量15维风险检测(R01-R15)
    try:
        # risk-detector入口脚本(risk_detector.py,支持--action+--params)
        risk_script = os.path.join(RISK_DETECTOR_SCRIPT, "risk_detector.py")
        if not os.path.exists(risk_script):
            logger.warning("risk_detector.py未找到,降级为基础合规检查")
            return _basic_compliance_check(content, platform)

        # 调用risk-detector: --action full_check --params JSON
        import subprocess
        params_json = json.dumps({"content": content, "platform": platform or "general"}, ensure_ascii=False)
        result = subprocess.run(
            [sys.executable, risk_script, "--action", "full_check", "--params", params_json],
            capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace',
            stdin=subprocess.DEVNULL
        )

        if result.returncode == 0 and result.stdout:
            risk_result = json.loads(result.stdout)
            # risk_detector.py返回 data.level(非risk_level), 需映射
            risk_level = risk_result.get("data", {}).get("level", "SAFE")
            score = risk_result.get("data", {}).get("score", 0)
            passed = risk_level in ("SAFE", "LOW")
            block = risk_level in ("HIGH", "CRITICAL")

            return {
                "success": True,
                "data": {
                    "risk_level": risk_level,
                    "score": score,
                    "passed": passed,
                    "block": block,
                    "details": risk_result.get("data", {}).get("checks", {})
                },
                "error": None,
                "code": "RISK_DETECTOR_OK"
            }
        else:
            logger.warning(f"risk-detector返回非0: {result.returncode}, stderr: {result.stderr[:200]}")
            return _basic_compliance_check(content, platform)

    except subprocess.TimeoutExpired:
        logger.warning("risk-detector调用超时(30s),降级为基础合规检查")
        return _basic_compliance_check(content, platform)
    except Exception as e:
        logger.error(f"risk-detector调用失败,降级为基础合规检查: {e}")
        return _basic_compliance_check(content, platform)


def _basic_compliance_check(content: str, platform: str) -> dict:
    """基础合规检查(降级模式) — 仅检查明显违规模式

    R18(自动化不可降级): 降级不是跳过,仍执行基础检查
    R74.4(允许降级模式): 标注downgraded=True+日志+downgraded字段
    """
    violations = []

    # 基础违规模式检测
    basic_patterns = {
        "private_traffic": ["加微信", "加V信", "加v信", "微信号", "VX:", "vx:", "扫码加"],
        "false_advertising": ["100%", "绝对", "包治", "根治", "无风险", "零风险"],
        "contact_info": ["QQ群", "qq群", "电话:", "手机:", "tel:"],
    }

    content_lower = content.lower()
    for category, patterns in basic_patterns.items():
        for pattern in patterns:
            if pattern.lower() in content_lower:
                violations.append(category)
                break

    # 平台特定规则
    platform_rules = {
        "douyin": {"patterns": ["淘宝", "天猫", "京东", "拼多多"], "category": "external_link"},
        "xiaohongshu": {"patterns": ["微商", "代购", "一手货源"], "category": "business_violation"},
    }

    if platform in platform_rules:
        rule = platform_rules[platform]
        for pattern in rule["patterns"]:
            if pattern in content:
                violations.append(rule["category"])
                break

    if violations:
        risk_level = "MEDIUM"
        score = 60
        passed = False
        block = False
    else:
        risk_level = "SAFE"
        score = 90
        passed = True
        block = False

    return {
        "success": True,
        "data": {
            "risk_level": risk_level,
            "score": score,
            "passed": passed,
            "block": block,
            "downgraded": True,
            "downgrade_reason": "risk-detector unavailable, using basic pattern check",
            "details": {"violations": violations, "check_method": "basic_pattern"}
        },
        "error": None,
        "code": "BASIC_CHECK_OK"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="内容合规检查U19 (v25.0合并到content-qa-guard)")
    parser.add_argument("--content", required=True, help="待检查内容")
    parser.add_argument("--platform", default="", help="目标平台")
    parser.add_argument("--content-type", default="", help="内容类型")
    args = parser.parse_args()

    result = check_compliance(args.content, args.platform, args.content_type)
    print(json.dumps(result, ensure_ascii=False, indent=2))
