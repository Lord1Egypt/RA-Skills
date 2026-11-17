"""封号应急处理器 - DEF-37封号应急预案执行脚本

用法:
  python ban_handler.py --action detect --account-id ID --reason REASON
  python ban_handler.py --action pause --account-id ID
  python ban_handler.py --action switch --account-id ID --backup-account BACKUP_ID
  python ban_handler.py --action republish --backup-account BACKUP_ID
  python ban_handler.py --action appeal --account-id ID [--reason REASON]
  python ban_handler.py --action analyze --account-id ID
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from pathlib import Path as _Path
from typing import Any
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-ban-emergency", source="skills/account-ban-emergency/scripts/ban_handler.py")
from mcps.shared.atomic_write import safe_read_json, atomic_write_json

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BAN_EVENTS_DIR = PROJECT_ROOT / "data" / "ban_events"
ACCOUNT_POOL_FILE = PROJECT_ROOT / "data" / "account_pool.json"
TENANT_COOKIE_MAP_FILE = PROJECT_ROOT / "data" / "tenant_cookie_map.json"


def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> dict:
    if path.exists():
        result = safe_read_json(path)
        if result is None or not result.get("success"):
            logger.warning(f"JSON文件读取失败(path={path})")
            return {}
        return result.get("data", {})
    return {}


def _save_json(path: Path, data: dict):
    _ensure_dir(path.parent)
    atomic_write_json(path, data, indent=2, ensure_ascii=False)


def action_detect(account_id: str, reason: str) -> dict[str, Any]:
    """action detect

    Args:
        account_id (str): 参数说明
        reason (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    _ensure_dir(BAN_EVENTS_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    event_file = BAN_EVENTS_DIR / f"{account_id}_{timestamp}.json"
    event_data = {
        "account_id": account_id,
        "platform": "xianyu",
        "banned_reason": reason,
        "detected_at": datetime.now().isoformat(),
        "detection_source": "ban_handler",
        "status": "detected",
    }
    _save_json(event_file, event_data)
    return {"success": True, "data": {"event_file": str(event_file), "event": event_data}, "error": None, "code": None}


def action_pause(account_id: str) -> dict[str, Any]:
    """action pause

    Args:
        account_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    _ensure_dir(BAN_EVENTS_DIR)
    pause_file = BAN_EVENTS_DIR / f"{account_id}_paused.json"
    pause_data = {
        "account_id": account_id,
        "paused_at": datetime.now().isoformat(),
        "paused_services": ["cron-publish", "auto-reply", "auto-delivery"],
        "status": "paused",
    }
    _save_json(pause_file, pause_data)
    return {"success": True, "data": pause_data, "error": None, "code": None}


def action_switch(account_id: str, backup_account: str) -> dict[str, Any]:
    """action switch

    Args:
        account_id (str): 参数说明
        backup_account (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    cookie_map = _load_json(TENANT_COOKIE_MAP_FILE)
    old_cookie_id = cookie_map.get(account_id, "")
    cookie_map[account_id] = f"banned_{old_cookie_id}"
    if backup_account not in cookie_map:
        pool = _load_json(ACCOUNT_POOL_FILE)
        backup_cookie = pool.get("accounts", {}).get(backup_account, {}).get("cookie_id", "")
        if backup_cookie:
            cookie_map[backup_account] = backup_cookie
    _save_json(TENANT_COOKIE_MAP_FILE, cookie_map)
    switch_data = {
        "account_id": account_id,
        "backup_account": backup_account,
        "switched_at": datetime.now().isoformat(),
        "cookie_map_updated": True,
    }
    return {"success": True, "data": switch_data, "error": None, "code": None}


def action_republish(backup_account: str) -> dict[str, Any]:
    # P0-12修复(复核批次2): 返回success:False+next_action,禁止虚假成功
    # 来源: 文档3 §11.4 批次2-A + R56层间依赖方向(LLM编排而非MCP直接调用)
    # SKILL.md声明调用fishclaw-mcp,但exec脚本不应直接调用MCP(违反R56)
    # 返回success:False告知LLM需要编排调用fishclaw-mcp publish_item
    # R6-014修复确认: 已消除虚假实现,exec返回指引而非直接执行,SKILL.md应标注"action_republish需LLM编排"
    return {
        "success": False,
        "data": {
            "backup_account": backup_account,
            "next_action": "call_fishclaw_publish",
        },
        "error": "重新发布需LLM编排调用fishclaw-mcp publish_item,exec脚本不直接调用MCP(遵循R56层间依赖方向)",
        "code": "REQUIRES_LLM_ORCHESTRATION",
    }


def action_appeal(account_id: str, reason: str = "") -> dict[str, Any]:
    """自动申诉流程接入(HL-009修复)

    记录申诉事件+生成申诉建议+返回LLM编排指引(遵循R56层间依赖方向)
    来源: HL-009 + 修复提示词R56(exec不直接调用MCP) + R34(虚假实现检测)

    流程:
    1. 若reason为空,从最近封号事件读取
    2. 根据封号原因生成申诉建议
    3. 记录申诉事件到data/ban_events/{account_id}_appeal_{timestamp}.json
    4. 返回REQUIRES_LLM_ORCHESTRATION让LLM编排调用闲鱼申诉渠道

    Args:
        account_id (str): 参数说明
        reason (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    _ensure_dir(BAN_EVENTS_DIR)

    # 1. 若reason为空,从最近封号事件读取
    if not reason:
        events = []
        if BAN_EVENTS_DIR.exists():
            for f in BAN_EVENTS_DIR.glob(f"{account_id}_*.json"):
                if "paused" not in f.name and "appeal" not in f.name:
                    events.append((f, _load_json(f)))
        if events:
            # 按文件名时间戳排序取最新
            events.sort(key=lambda x: x[0].name, reverse=True)
            reason = events[0][1].get("banned_reason", "unknown")
            logger.info(f"action_appeal: 从历史事件读取封号原因 account_id={account_id}, reason={reason}")
        else:
            reason = "unknown"
            logger.warning(f"action_appeal: 无历史封号事件,使用默认reason=unknown account_id={account_id}")

    # 2. 生成申诉建议(根据封号原因)
    appeal_advice = _generate_appeal_advice(reason)

    # 3. 记录申诉事件到data/ban_events/{account_id}_appeal_{timestamp}.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    appeal_file = BAN_EVENTS_DIR / f"{account_id}_appeal_{timestamp}.json"
    appeal_data = {
        "account_id": account_id,
        "platform": "xianyu",
        "banned_reason": reason,
        "appeal_advice": appeal_advice,
        "appeal_initiated_at": datetime.now().isoformat(),
        "appeal_status": "initiated",
        "appeal_source": "ban_handler",
        "next_action": "call_xianyu_appeal_channel",
    }
    _save_json(appeal_file, appeal_data)

    # 4. 返回LLM编排指引(遵循R56,不直接调用MCP)
    return {
        "success": False,
        "data": {
            "account_id": account_id,
            "banned_reason": reason,
            "appeal_advice": appeal_advice,
            "appeal_file": str(appeal_file),
            "next_action": "call_xianyu_appeal_channel",
        },
        "error": "申诉需LLM编排调用闲鱼申诉渠道(人工/API),exec脚本不直接调用MCP(遵循R56层间依赖方向)",
        "code": "REQUIRES_LLM_ORCHESTRATION",
    }


def _generate_appeal_advice(reason: str) -> dict:
    """根据封号原因生成申诉建议

    来源: 01手册§十风控规则 + DEF-37封号应急预案
    策略: 按封号原因分类生成差异化申诉文本+证据清单+成功率预估
    """
    reason_lower = (reason or "").lower()

    if any(kw in reason_lower for kw in ["导流", "引流", "微信号", "qq", "外部联系方式"]):
        return {
            "appeal_strategy": "承认+整改承诺",
            "appeal_text": "尊敬的闲鱼客服,我已认识到在商品描述中包含外部联系方式违反平台规则,现已全面整改。承诺今后严格遵守平台规范,请求解封。",
            "evidence_required": ["整改后的商品截图", "学习平台规则的记录"],
            "estimated_success_rate": "中",
        }
    elif any(kw in reason_lower for kw in ["刷单", "虚假交易", "boosting"]):
        return {
            "appeal_strategy": "举证+否认",
            "appeal_text": "尊敬的闲鱼客服,我从未参与刷单或虚假交易,所有订单均为真实交易。请求提供违规证据,如有误判请求解封。",
            "evidence_required": ["真实订单物流单号", "买家沟通记录", "商品发货凭证"],
            "estimated_success_rate": "低",
        }
    elif any(kw in reason_lower for kw in ["侵权", "仿冒", "假货", "counterfeit"]):
        return {
            "appeal_strategy": "举证+授权证明",
            "appeal_text": "尊敬的闲鱼客服,所售商品均为正品,有正规采购渠道。请求提供侵权判定依据,如有误判请求解封。",
            "evidence_required": ["采购发票", "品牌授权书", "商品溯源码"],
            "estimated_success_rate": "中",
        }
    elif any(kw in reason_lower for kw in ["骚扰", "abuse", "辱骂"]):
        return {
            "appeal_strategy": "道歉+整改承诺",
            "appeal_text": "尊敬的闲鱼客服,为沟通中的不当言行深表歉意,已反思并承诺今后文明沟通。请求给予改过机会,申请解封。",
            "evidence_required": ["整改承诺书"],
            "estimated_success_rate": "中",
        }
    elif any(kw in reason_lower for kw in ["发布频率", "spam", "频繁"]):
        return {
            "appeal_strategy": "承认+整改承诺",
            "appeal_text": "尊敬的闲鱼客服,已认识到发布频率过高触发风控,承诺今后遵守频率限制(每账号≤3次/天)。请求解封。",
            "evidence_required": ["发布频率调整记录"],
            "estimated_success_rate": "高",
        }
    else:
        return {
            "appeal_strategy": "通用申诉",
            "appeal_text": f"尊敬的闲鱼客服,我的账号因'{reason}'被封,经自查未发现明显违规行为。请求提供具体违规证据,如有误判请求解封。",
            "evidence_required": ["账号使用记录"],
            "estimated_success_rate": "中",
        }


def action_analyze(account_id: str) -> dict[str, Any]:
    """action analyze

    Args:
        account_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    events = []
    if BAN_EVENTS_DIR.exists():
        for f in BAN_EVENTS_DIR.glob(f"{account_id}_*.json"):
            if "paused" not in f.name:
                events.append(_load_json(f))
    analysis = {
        "account_id": account_id,
        "ban_count": len(events),
        "latest_ban": events[-1] if events else None,
        "analyzed_at": datetime.now().isoformat(),
    }

    # DEF-37闭环修复: 调用自生长引擎记录封号经验(吃一堑长一智)
    # 来源: 36设计文档§2.1 P0-2 + 修复提示词R31.2(自生长引擎不可因bug禁用)
    learn_result = _learn_from_ban_events(account_id, events)
    analysis["learn_result"] = learn_result

    # 根据封号次数动态生成建议(替代原硬编码)
    if len(events) == 0:
        analysis["recommendation"] = "无封号记录,保持当前运营策略"
    elif len(events) == 1:
        analysis["recommendation"] = "首次封号,建议降低发布频率30%+增加消息间隔+检查导流词过滤"
    elif len(events) <= 3:
        analysis["recommendation"] = f"累计{len(events)}次封号,建议切换备用账号+全面检查风控策略+暂停高风险操作24小时"
    else:
        analysis["recommendation"] = f"累计{len(events)}次封号(高风险),建议永久弃用该账号+全面复盘运营策略+人工介入"

    return {"success": True, "data": analysis, "error": None, "code": None}


def _learn_from_ban_events(account_id: str, events: list) -> dict:
    """调用自生长引擎记录封号经验(DEF-37闭环核心)

    Token优化: 自生长引擎消除"封号不学习"盲区，禁止删除(见36设计文档+修复提示词R33)
    生产价值: 真实经验记录,非硬编码(R32)
    """
    import subprocess

    result = {"learned": False, "error_recorded": False, "errors": []}

    if not events:
        return result

    growth_script = PROJECT_ROOT / "skills" / "_lazy" / "self-growth" / "scripts" / "self_growth_engine.py"
    latest_ban = events[-1] if events else {}
    ban_reason = latest_ban.get("reason", "unknown")
    ban_count = len(events)

    # 1. 调用 self_growth_engine.py do_learn
    if growth_script.exists():
        lesson = f"账号{account_id}第{ban_count}次封号,原因:{ban_reason},建议:降低发布频率+增加间隔+检查导流词"
        importance = min(5 + ban_count * 2, 10)  # 封号次数越多,重要性越高
        try:
            r = subprocess.run(
                ["python", str(growth_script), "learn",
                 "--scenario", "account_ban",
                 "--lesson", lesson,
                 "--category", "error",
                 "--importance", str(importance),
                 "--tags", "ban", account_id],
                capture_output=True, text=True, timeout=30, encoding='utf-8'
            )
            if r.returncode == 0:
                result["learned"] = True
            else:
                result["errors"].append(f"self_growth_engine failed: {r.stderr[:200] if r.stderr else 'unknown'}")
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            result["errors"].append(f"self_growth_engine timeout: {str(e)}")
    else:
        result["errors"].append("self_growth_engine.py not found")

    # 2. 写入 error_history.jsonl
    error_history_file = PROJECT_ROOT / "skills" / "_lazy" / "self-growth" / "experience" / "error_history.jsonl"
    try:
        error_history_file.parent.mkdir(parents=True, exist_ok=True)
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "skill_name": "account-ban-emergency",
            "error_type": "account_ban",
            "account_id": account_id,
            "ban_count": ban_count,
            "ban_reason": ban_reason,
            "severity": "critical",
            "lesson": f"账号{account_id}封号,需调整运营策略",
        }
        with open(error_history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry, ensure_ascii=False) + "\n")
        result["error_recorded"] = True
    except OSError as e:
        logger.error(f"ban handler异常: {e}", exc_info=True)
        result["errors"].append(f"error_history write failed: {str(e)}")

    return result


def main():
    # 修复编码: Windows默认GBK无法输出Unicode,强制UTF-8(R6根因修复)
    """main"""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="封号应急处理器")
    parser.add_argument("--action", required=True, choices=["detect", "pause", "switch", "republish", "appeal", "analyze"])
    parser.add_argument("--account-id", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--backup-account", default="")
    args = parser.parse_args()

    actions = {
        "detect": lambda: action_detect(args.account_id, args.reason),
        "pause": lambda: action_pause(args.account_id),
        "switch": lambda: action_switch(args.account_id, args.backup_account),
        "republish": lambda: action_republish(args.backup_account),
        "appeal": lambda: action_appeal(args.account_id, args.reason),
        "analyze": lambda: action_analyze(args.account_id),
    }

    result = actions[args.action]()
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
