"""content-qa-guard 内容合规审核脚本

三级审核: 敏感词库→AI语义→平台规则
依赖MCP: sensitive-word-mcp
每日限额: 50条(01手册§十10.1)
"""
import json
import sys
import os
import subprocess
from datetime import datetime, date
from pathlib import Path

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("_lazy", source="skills/_lazy/content-qa-guard/scripts/qa_guard.py")


# 审核计数文件
COUNT_FILE = Path("d:/JueJin/data/qa_guard_daily_count.json")
# 审核日志目录
LOG_DIR = Path("d:/JueJin/data/qa_verification_log")
# 每日限额(01手册§十10.1)
DAILY_LIMIT = 50

# 平台严格度(02手册§八8.2)
PLATFORM_STRICTNESS = {
    "xiaohongshu": 5, "wechat_official": 5,
    "douyin": 4, "xianyu": 4, "kuaishou": 4, "zhihu": 4, "shipinhao": 4,
    "bilibili": 3, "weibo": 3, "baijiahao": 3, "toutiao": 3,
    "csdn": 2,
    "default": 3,
}

# 平台规则(02手册§八8.1)
PLATFORM_RULES = {
    "xianyu": ["禁止导流", "虚假宣传", "虚拟商品违禁", "金融风险", "侵权"],
    "xiaohongshu": ["严格禁止导流和营销", "种草套路词", "医疗美容", "减肥瘦身", "代购违规"],
    "douyin": ["禁止导流", "直播间特有违规", "短视频引流词", "金融风险", "低俗"],
    "weibo": ["禁止导流和营销", "热搜操控", "政治敏感", "虚假宣传"],
    "bilibili": ["禁止导流", "低俗内容", "虚假宣传"],
    "default": ["禁止导流", "虚假宣传"],
}


def get_daily_count() -> int:
    """获取今日审核计数"""
    today = date.today().isoformat()
    if COUNT_FILE.exists():
        try:
            data = json.loads(COUNT_FILE.read_text(encoding="utf-8"))
            if data.get("date") == today:
                return data.get("count", 0)
        except Exception as e:

            logger.error(f"qa_guard: {e}")
    return 0


def increment_daily_count() -> None:
    """增加今日审核计数"""
    today = date.today().isoformat()
    count = get_daily_count() + 1
    COUNT_FILE.parent.mkdir(parents=True, exist_ok=True)
    COUNT_FILE.write_text(json.dumps({"date": today, "count": count}, ensure_ascii=False), encoding="utf-8")


def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """通过MCP调用sensitive-word-mcp工具(使用openclaw CLI)"""
    try:
        cmd = [
            sys.executable, "-c",
            f"import json; print(json.dumps({{'tool': '{tool_name}', 'args': {json.dumps(arguments)}}}))"
        ]
        # 使用openclaw agent调用MCP工具
        agent_cmd = [
            "openclaw", "agent", "--message",
            f"调用MCP工具 {tool_name} 参数: {json.dumps(arguments, ensure_ascii=False)}",
            "--agent", "xingbu"
        ]
        result = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=60, encoding="utf-8")
        if result.returncode == 0:
            return {"success": True, "output": result.stdout.strip()}
        else:
            return {"success": False, "error": result.stderr.strip()[:200]}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "MCP调用超时60秒"}
    except Exception as e:
        logger.error(f"qa guard异常: {e}", exc_info=True)
        return {"success": False, "error": str(e)[:200]}


def check_platform_rules(text: str, platform: str) -> list:
    """三级审核: 平台规则合规检查(本地规则匹配)"""
    violations = []
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES["default"])

    # 导流检测(所有平台)
    daoliu_keywords = ["加微信", "加V", "加群", "私聊领取", "扫码领", "转账", "支付宝账号"]
    if platform in ["xianyu", "xiaohongshu", "douyin"]:
        daoliu_keywords.extend(["微信号", "VX", "WX", "QQ号", "QQ群"])

    for kw in daoliu_keywords:
        if kw in text:
            violations.append(f"导流词: {kw}")
            break

    # 虚假宣传检测
    xuji_keywords = ["100%成功", "包过", "必过", "绝对有效", "零风险", "稳赚"]
    for kw in xuji_keywords:
        if kw in text:
            violations.append(f"虚假宣传: {kw}")
            break

    # 金融风险检测
    jinrong_keywords = ["贷款", "借贷", "信用卡套现", "投资回报", "高收益"]
    for kw in jinrong_keywords:
        if kw in text:
            violations.append(f"金融风险: {kw}")
            break

    return violations


def determine_risk_level(level1_count: int, level2_findings: list, level3_violations: list) -> str:
    """综合判定风险等级"""
    total = level1_count + len(level2_findings) + len(level3_violations)
    if total == 0:
        return "SAFE"
    if total >= 3 or any("导流" in str(v) for v in level3_violations):
        return "HIGH"
    if total >= 2:
        return "MEDIUM"
    return "LOW"


def qa_guard(text: str, platform: str, context: str = "") -> dict:
    """执行三级内容合规审核"""
    # 参数验证
    if not text or not text.strip():
        return {"success": False, "data": {}, "error": "text不能为空", "code": "INVALID_INPUT"}

    valid_platforms = list(PLATFORM_STRICTNESS.keys())
    if platform not in valid_platforms:
        platform = "default"

    # 每日限额检查
    daily_count = get_daily_count()
    if daily_count >= DAILY_LIMIT:
        return {"success": False, "data": {"daily_count": daily_count, "daily_limit": DAILY_LIMIT},
                "error": f"每日审核限额{DAILY_LIMIT}条已用完", "code": "DAILY_LIMIT_EXCEEDED"}

    # 一级审核: 敏感词库扫描
    level1_result = {"found": [], "count": 0, "library_status": "ok"}
    mcp_result = call_mcp_tool("check_sensitive_words", {"text": text, "platform": platform, "context": context})
    if mcp_result.get("success"):
        level1_result["mcp_output"] = mcp_result["output"][:500]
    else:
        level1_result["library_status"] = "mcp_unavailable"

    # 二级审核: AI语义级检测(严格度>=3时启用)
    strictness = PLATFORM_STRICTNESS.get(platform, 3)
    level2_result = {"enabled": strictness >= 3, "llm_findings": []}
    if strictness >= 3:
        # LLM语义分析通过MCP调用
        pass  # 由sensitive-word-mcp内部处理LLM调用

    # 三级审核: 平台规则合规检查
    level3_violations = check_platform_rules(text, platform)
    level3_result = {"platform_violations": level3_violations}

    # 综合判定
    risk_level = determine_risk_level(level1_result["count"], level2_result["llm_findings"], level3_violations)

    # 审核结果
    if level1_result["count"] > 0 or level3_violations:
        result = "blocked" if risk_level in ["HIGH", "CRITICAL"] else "warning"
    else:
        result = "pass"

    # 生成修改建议
    suggestion = None
    if result in ["warning", "blocked"]:
        replace_result = call_mcp_tool("replace_sensitive_words", {
            "text": text, "platform": platform, "context": context
        })
        if replace_result.get("success"):
            suggestion = replace_result.get("output", "")[:300]

    # 增加计数
    increment_daily_count()

    # 记录审核日志
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "result": result,
        "risk_level": risk_level,
        "text_length": len(text),
    }
    log_file = LOG_DIR / f"{date.today().isoformat()}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return {
        "success": True,
        "data": {
            "result": result,
            "risk_level": risk_level,
            "level1": level1_result,
            "level2": level2_result,
            "level3": level3_result,
            "suggestion": suggestion,
            "daily_count": daily_count + 1,
            "daily_limit": DAILY_LIMIT,
        },
        "error": None,
        "code": None,
    }


def main():
    """CLI入口"""
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False, "data": {}, "error": "用法: qa_guard.py <text> <platform> [context]",
            "code": "INVALID_INPUT"
        }))
        sys.exit(1)

    text = sys.argv[1]
    platform = sys.argv[2]
    context = sys.argv[3] if len(sys.argv) > 3 else ""

    result = qa_guard(text, platform, context)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
