"""business-correctness-validator 业务规则校验exec脚本

功能: 校验内容合规性(28平台规则+内容合规)
依赖MCP: business-correctness-validator
业务规则来源: 02手册§二28平台矩阵 + §八8.2平台严格度

用法:
  python validate_business_rules.py --content "文本" --platform xianyu --tenant_id default
  python validate_business_rules.py --price 99.9 --category virtual --platform xianyu
  python validate_business_rules.py --metrics '{"refund_rate":0.08}' --tenant_id default
"""
import argparse

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger

import logging
logger = get_logger("system", source="skills/business-correctness-validator/scripts/validate_business_rules.py")

logger = get_logger("skills", source="skills/business-correctness-validator/scripts/validate_business_rules.py")

# 内置平台规则(与MCP Server同步,来源:02手册§二+§八8.2)
PLATFORM_RULES = {
    "weixin_gzh": {"strictness": 5, "min_length": 20, "max_length": 20000, "forbidden": ["导流", "虚假宣传", "医疗违规"]},
    "xiaohongshu": {"strictness": 5, "min_length": 20, "max_length": 1000, "forbidden": ["医疗美容", "减肥药", "处方药"]},
    "douyin": {"strictness": 4, "min_length": 10, "max_length": 5000, "forbidden": ["金融诈骗", "色情擦边"]},
    "kuaishou": {"strictness": 4, "min_length": 10, "max_length": 5000, "forbidden": ["金融诈骗", "色情擦边"]},
    "zhihu": {"strictness": 4, "min_length": 50, "max_length": 100000, "forbidden": ["导流", "虚假宣传"]},
    "shipinhao": {"strictness": 4, "min_length": 10, "max_length": 5000, "forbidden": ["导流", "金融诈骗"]},
    "xianyu": {"strictness": 4, "min_length": 10, "max_length": 2000, "forbidden": ["代写论文", "代考", "盗版", "破解版"]},
    "bilibili": {"strictness": 3, "min_length": 20, "max_length": 50000, "forbidden": ["低俗内容", "虚假宣传"]},
    "weibo": {"strictness": 3, "min_length": 10, "max_length": 2000, "forbidden": ["政治敏感", "热搜操控"]},
    "baijiahao": {"strictness": 3, "min_length": 50, "max_length": 20000, "forbidden": ["虚假宣传", "标题党"]},
    "toutiao": {"strictness": 3, "min_length": 50, "max_length": 20000, "forbidden": ["虚假宣传", "标题党"]},
    "csdn": {"strictness": 2, "min_length": 100, "max_length": 100000, "forbidden": ["纯广告"]},
    "juejin": {"strictness": 2, "min_length": 100, "max_length": 100000, "forbidden": ["纯广告"]},
    "default": {"strictness": 3, "min_length": 10, "max_length": 10000, "forbidden": ["违法内容"]},
}

ABSOLUTE_WORDS = ["最好", "第一", "国家级", "顶级", "绝对", "100%", "包治", "根治", "零风险"]

def validate_content_local(content: str, platform: str, tenant_id: str) -> dict[str, Any]:
    """本地内容校验(不依赖MCP,用于快速校验)

    Args:
        content (str): 参数说明
        platform (str): 参数说明
        tenant_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        if not content or not content.strip():
            return {"success": False, "data": {}, "error": "content不能为空", "code": "INVALID_INPUT"}
        rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["default"])
        strictness = rules.get("strictness", 3)
        violations = []

        # 长度校验
        content_len = len(content)
        if content_len < rules["min_length"]:
            violations.append({"type": "content_too_short", "severity": "medium", "message": f"长度{content_len}<{rules['min_length']}"})
        if content_len > rules["max_length"]:
            violations.append({"type": "content_too_long", "severity": "high", "message": f"长度{content_len}>{rules['max_length']}"})

        # 品类禁令(严格度>=4)
        if strictness >= 4:
            for cat in rules.get("forbidden", []):
                if cat in content:
                    violations.append({"type": "forbidden_category", "severity": "critical", "message": f"禁售品类: {cat}", "keyword": cat})

        # 绝对化用语(严格度>=5,来源:02手册§八8.1)
        if strictness >= 5:
            for word in ABSOLUTE_WORDS:
                if word in content:
                    violations.append({"type": "absolute_word_violation", "severity": "high", "message": f"广告法违禁词: {word}", "keyword": word})

        result = "pass" if not violations else ("blocked" if any(v["severity"] in ["critical", "high"] for v in violations) else "warning")
        risk_level = "SAFE" if result == "pass" else ("CRITICAL" if any(v["severity"] == "critical" for v in violations) else "HIGH" if any(v["severity"] == "high" for v in violations) else "MEDIUM")

        return {
            "success": True,
            "data": {
                "result": result, "risk_level": risk_level, "platform": platform,
                "tenant_id": tenant_id, "platform_strictness": strictness,
                "content_length": content_len, "violation_count": len(violations),
                "violations": violations, "rule_source": "02手册§二+§八8.1+§八8.2",
            },
            "error": None, "code": None,
        }
    except ValueError as ve:
        logger.error(f"validate_business_rules ValueError: {ve}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(ve), "code": "VALUE_ERROR"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"validate_business_rules异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "VALIDATE_ERROR"}, ensure_ascii=False))
        sys.exit(2)

def main() -> None:
    """CLI入口: 解析参数并执行校验"""
    parser = argparse.ArgumentParser(description="业务规则校验exec脚本")
    parser.add_argument("--content", type=str, default="", help="待校验内容文本")
    parser.add_argument("--platform", type=str, default="default", help="目标平台")
    parser.add_argument("--tenant_id", type=str, default="default", help="租户ID")
    args = parser.parse_args()

    if not args.content:
        print(json.dumps({"success": False, "data": {}, "error": "缺少--content参数", "code": "MISSING_CONTENT"}, ensure_ascii=False))
        sys.exit(1)

    result = validate_content_local(args.content, args.platform, args.tenant_id)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] and result["data"].get("result") != "blocked" else 1)

if __name__ == "__main__":
    main()
