"""
OpenClaw Skill: 外呼运营小助手 (Outbound Call Operations Assistant)

This skill provides tools for managing AI outbound call tasks, tenant lines,
supply lines, scripts, and task templates. Query operations read from local
JSON data files; action operations call the Baize outbound platform API.
"""

import json
import os
import re
import uuid
import httpx
from datetime import datetime
from pathlib import Path
from typing import Optional

from openclaw.skills import skill, SkillContext

# ---------------------------------------------------------------------------
# Local data helpers
# ---------------------------------------------------------------------------

_DATA_DIR = Path(__file__).parent / "data"

_BAIZE_BASE_URL = os.getenv("BAIZE_BASE_URL", "http://localhost:8860/market")
_BAIZE_TOKEN = os.getenv("BAIZE_TOKEN", "")


def _load(filename: str) -> list:
    """Load a JSON array from a local data file."""
    path = _DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _fmt_task(t: dict) -> str:
    status_map = {
        "RUNNING": "运行中",
        "STOP": "已暂停",
        "FINISH": "已完成",
        "INIT": "待启动",
    }
    status = status_map.get(t.get("callStatus", ""), t.get("callStatus", "未知"))
    phone_num = t.get("phoneNum", 0)
    called = t.get("calledPhoneNum", 0)
    put_through = t.get("putThroughPhoneNum", 0)
    rate = f"{t.get('putThroughPhoneRate', 0) * 100:.1f}%" if t.get("putThroughPhoneRate") else "0.0%"
    return (
        f"【{t.get('taskName', 'N/A')}】(ID: {t.get('id')})\n"
        f"  账号: {t.get('account', 'N/A')}  商户: {t.get('tenantName', 'N/A')}  状态: {status}\n"
        f"  话术: {t.get('speechCraftName', 'N/A')}  线路: {t.get('lineName', 'N/A')}  并发: {t.get('concurrency', 0)}\n"
        f"  名单总量: {phone_num}  已呼: {called}  接通: {put_through}  接通率: {rate}\n"
        f"  创建时间: {t.get('createTime', 'N/A')}"
    )


def _fmt_line(line: dict) -> str:
    status = "启用" if line.get("enableStatus") == "ENABLE" else "停用"
    return (
        f"【{line.get('lineName', 'N/A')}】(编号: {line.get('lineNumber')}  ID: {line.get('id')})\n"
        f"  类型: {line.get('lineType', 'N/A')}  状态: {status}\n"
        f"  最大并发: {line.get('concurrentLimit', 0)}  剩余并发: {line.get('lineRemainConcurrent', 0)}\n"
        f"  行业: {', '.join(line.get('secondIndustries', []))}\n"
        f"  备注: {line.get('notes', '')}"
    )


def _fmt_supply_line(sl: dict) -> str:
    status = "启用" if sl.get("enableStatus") == "ENABLE" else "停用"
    return (
        f"【{sl.get('lineName', 'N/A')}】(编号: {sl.get('lineNumber')}  ID: {sl.get('id')})\n"
        f"  供应商: {sl.get('callLineSupplierName', 'N/A')}  状态: {status}\n"
        f"  最大并发: {sl.get('concurrentLimit', 0)}  单价: {sl.get('unitPrice', 0)}元/分钟\n"
        f"  主叫号码: {sl.get('masterCallNumber', 'N/A')}  号码类型: {', '.join(sl.get('phoneTypeList', []))}\n"
        f"  加密号码: {'是' if sl.get('isForEncryptionPhones') else '否'}  接入方式: {sl.get('lineAccessType', 'N/A')}\n"
        f"  行业: {', '.join(sl.get('secondIndustries', []))}"
    )


def _fmt_script(s: dict) -> str:
    status = "启用" if s.get("status") == "ENABLE" else "停用"
    return (
        f"【{s.get('scriptName', 'N/A')}】(ID: {s.get('id')}  版本: v{s.get('version', 1)})\n"
        f"  状态: {status}  行业: {s.get('primaryIndustry', 'N/A')}/{s.get('secondaryIndustry', 'N/A')}\n"
        f"  归属账号: {s.get('ownerAccount', 'N/A')}  最近使用: {s.get('lastUsingDate', 'N/A')}\n"
        f"  备注: {s.get('remark', '')}"
    )


def _fmt_template(tmpl: dict) -> str:
    status_map = {"0": "启用", "1": "停用"}
    status = status_map.get(str(tmpl.get("templateStatus", "0")), "未知")
    return (
        f"【{tmpl.get('templateName', 'N/A')}】(ID: {tmpl.get('id')})\n"
        f"  账号: {tmpl.get('account', 'N/A')}  状态: {status}\n"
        f"  话术: {tmpl.get('speechCraftName', 'N/A')}  任务名: {tmpl.get('taskName', 'N/A')}\n"
        f"  拨打时段: {tmpl.get('startWorkTimes', 'N/A')} - {tmpl.get('endWorkTimes', 'N/A')}\n"
        f"  自动补呼: {'是' if tmpl.get('autoReCall') == 1 else '否'}  隔日续呼: {'是' if tmpl.get('nextDayCall') == 1 else '否'}\n"
        f"  说明: {tmpl.get('comment', '')}"
    )


def _baize_post(path: str, body: dict) -> dict:
    """Send a POST request to the Baize API and return the parsed response."""
    url = _BAIZE_BASE_URL + path
    headers = {"token": _BAIZE_TOKEN, "Content-Type": "application/json"}
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Query skills — read from local JSON files
# ---------------------------------------------------------------------------


@skill(
    name="query_tasks",
    description=(
        "查询AI外呼任务列表。支持按账号、任务名称关键词、任务状态进行筛选。"
        "任务状态可选值：RUNNING（运行中）、STOP（已暂停）、FINISH（已完成）、INIT（待启动）。"
        "返回符合条件的任务列表，包含任务ID、名称、话术、线路、并发、名单及接通情况。"
    ),
    parameters={
        "account": {
            "type": "string",
            "description": "账号名称，不填则查询所有账号下的任务",
            "required": False,
        },
        "task_name_contain": {
            "type": "string",
            "description": "任务名称包含的关键词，不填则不过滤",
            "required": False,
        },
        "task_status": {
            "type": "string",
            "description": "任务状态（RUNNING / STOP / FINISH / INIT），不填则返回所有状态",
            "required": False,
        },
    },
)
async def query_tasks(
    ctx: SkillContext,
    account: Optional[str] = None,
    task_name_contain: Optional[str] = None,
    task_status: Optional[str] = None,
) -> str:
    tasks = _load("tasks.json")

    if account:
        tasks = [t for t in tasks if t.get("account", "").lower() == account.lower()]
    if task_name_contain:
        tasks = [t for t in tasks if task_name_contain in t.get("taskName", "")]
    if task_status:
        tasks = [t for t in tasks if t.get("callStatus", "").upper() == task_status.upper()]

    if not tasks:
        return "未找到符合条件的任务。"

    return f"共找到 {len(tasks)} 个任务：\n\n" + "\n\n".join(_fmt_task(t) for t in tasks)


@skill(
    name="get_tenant_lines",
    description=(
        "查询商户线路列表。可按启停状态筛选，返回线路ID、名称、类型、最大并发、剩余并发及适用行业等信息。"
    ),
    parameters={
        "enable_status": {
            "type": "string",
            "description": "线路状态：ENABLE（启用）或 DISABLE（停用），不填返回所有",
            "required": False,
        },
        "line_name_contain": {
            "type": "string",
            "description": "线路名称包含的关键词，不填则不过滤",
            "required": False,
        },
    },
)
async def get_tenant_lines(
    ctx: SkillContext,
    enable_status: Optional[str] = None,
    line_name_contain: Optional[str] = None,
) -> str:
    lines = _load("tenant_lines.json")

    if enable_status:
        lines = [ln for ln in lines if ln.get("enableStatus", "").upper() == enable_status.upper()]
    if line_name_contain:
        lines = [ln for ln in lines if line_name_contain in ln.get("lineName", "")]

    if not lines:
        return "未找到符合条件的商户线路。"

    return f"共找到 {len(lines)} 条商户线路：\n\n" + "\n\n".join(_fmt_line(ln) for ln in lines)


@skill(
    name="get_supply_lines",
    description=(
        "查询供应线路列表。可按线路名称关键词或启停状态筛选，"
        "返回线路编号、供应商、并发上限、单价、号码类型及适用行业等详细信息。"
    ),
    parameters={
        "enable_status": {
            "type": "string",
            "description": "线路状态：ENABLE（启用）或 DISABLE（停用），不填返回所有",
            "required": False,
        },
        "line_name_contain": {
            "type": "string",
            "description": "线路名称包含的关键词，不填则不过滤",
            "required": False,
        },
        "is_for_encryption": {
            "type": "boolean",
            "description": "是否只查加密号码线路，不填返回所有",
            "required": False,
        },
    },
)
async def get_supply_lines(
    ctx: SkillContext,
    enable_status: Optional[str] = None,
    line_name_contain: Optional[str] = None,
    is_for_encryption: Optional[bool] = None,
) -> str:
    lines = _load("supply_lines.json")

    if enable_status:
        lines = [sl for sl in lines if sl.get("enableStatus", "").upper() == enable_status.upper()]
    if line_name_contain:
        lines = [sl for sl in lines if line_name_contain in sl.get("lineName", "")]
    if is_for_encryption is not None:
        lines = [sl for sl in lines if sl.get("isForEncryptionPhones") == is_for_encryption]

    if not lines:
        return "未找到符合条件的供应线路。"

    return f"共找到 {len(lines)} 条供应线路：\n\n" + "\n\n".join(_fmt_supply_line(sl) for sl in lines)


@skill(
    name="get_scripts",
    description=(
        "查询话术（AI外呼脚本）列表。可按话术名称关键词或启停状态筛选，"
        "返回话术ID、名称、版本、所属行业、归属账号及使用情况等信息。"
    ),
    parameters={
        "script_status": {
            "type": "string",
            "description": "话术状态：ENABLE（启用）或 DISABLE（停用），不填返回所有",
            "required": False,
        },
        "script_name_contain": {
            "type": "string",
            "description": "话术名称包含的关键词，不填则不过滤",
            "required": False,
        },
        "account": {
            "type": "string",
            "description": "归属账号，不填则返回所有账号的话术",
            "required": False,
        },
    },
)
async def get_scripts(
    ctx: SkillContext,
    script_status: Optional[str] = None,
    script_name_contain: Optional[str] = None,
    account: Optional[str] = None,
) -> str:
    scripts = _load("scripts.json")

    if script_status:
        scripts = [s for s in scripts if s.get("status", "").upper() == script_status.upper()]
    if script_name_contain:
        scripts = [s for s in scripts if script_name_contain in s.get("scriptName", "")]
    if account:
        scripts = [s for s in scripts if s.get("ownerAccount", "").lower() == account.lower()]

    if not scripts:
        return "未找到符合条件的话术。"

    return f"共找到 {len(scripts)} 个话术：\n\n" + "\n\n".join(_fmt_script(s) for s in scripts)


@skill(
    name="get_task_templates",
    description=(
        "查询任务模板列表。可按模板名称关键词或账号筛选，"
        "返回模板ID、名称、关联话术、拨打时段及补呼设置等信息。"
    ),
    parameters={
        "template_name_contain": {
            "type": "string",
            "description": "模板名称包含的关键词，不填则不过滤",
            "required": False,
        },
        "account": {
            "type": "string",
            "description": "归属账号，不填则返回所有账号的模板",
            "required": False,
        },
    },
)
async def get_task_templates(
    ctx: SkillContext,
    template_name_contain: Optional[str] = None,
    account: Optional[str] = None,
) -> str:
    templates = _load("task_templates.json")

    if template_name_contain:
        templates = [t for t in templates if template_name_contain in t.get("templateName", "")]
    if account:
        templates = [t for t in templates if t.get("account", "").lower() == account.lower()]

    if not templates:
        return "未找到符合条件的任务模板。"

    return f"共找到 {len(templates)} 个任务模板：\n\n" + "\n\n".join(_fmt_template(t) for t in templates)


@skill(
    name="get_system_concurrency",
    description=(
        "查询当前系统外呼并发使用情况，统计各账号正在运行的任务并发总量及名单执行进度。"
        "数据来源于本地任务数据文件。"
    ),
    parameters={},
)
async def get_system_concurrency(ctx: SkillContext) -> str:
    tasks = _load("tasks.json")
    running = [t for t in tasks if t.get("callStatus") == "RUNNING"]

    if not running:
        return "当前没有正在运行的外呼任务。"

    total_concurrency = sum(t.get("concurrency", 0) for t in running)
    account_stats: dict = {}
    for t in running:
        acc = t.get("account", "unknown")
        if acc not in account_stats:
            account_stats[acc] = {"tasks": 0, "concurrency": 0}
        account_stats[acc]["tasks"] += 1
        account_stats[acc]["concurrency"] += t.get("concurrency", 0)

    lines = [f"系统当前运行任务数：{len(running)}  总并发：{total_concurrency}\n"]
    lines.append("各账号并发详情：")
    for acc, stats in account_stats.items():
        lines.append(f"  {acc}：{stats['tasks']} 个任务  并发 {stats['concurrency']}")

    return "\n".join(lines)


@skill(
    name="get_task_statistics",
    description=(
        "汇报外呼任务数据统计，包含任务名称、名单总量、已呼数量、接通数量及接通率。"
        "可按账号、任务名称关键词或任务状态进行筛选。"
    ),
    parameters={
        "account": {
            "type": "string",
            "description": "账号名称，不填则汇报所有账号",
            "required": False,
        },
        "task_name_contain": {
            "type": "string",
            "description": "任务名称包含的关键词，不填则不过滤",
            "required": False,
        },
        "task_status": {
            "type": "string",
            "description": "任务状态（RUNNING / STOP / FINISH），不填则返回所有",
            "required": False,
        },
    },
)
async def get_task_statistics(
    ctx: SkillContext,
    account: Optional[str] = None,
    task_name_contain: Optional[str] = None,
    task_status: Optional[str] = None,
) -> str:
    tasks = _load("tasks.json")

    if account:
        tasks = [t for t in tasks if t.get("account", "").lower() == account.lower()]
    if task_name_contain:
        tasks = [t for t in tasks if task_name_contain in t.get("taskName", "")]
    if task_status:
        tasks = [t for t in tasks if t.get("callStatus", "").upper() == task_status.upper()]

    if not tasks:
        return "未找到符合条件的任务。"

    total_phone = sum(t.get("phoneNum", 0) for t in tasks)
    total_called = sum(t.get("calledPhoneNum", 0) for t in tasks)
    total_put_through = sum(t.get("putThroughPhoneNum", 0) for t in tasks)
    overall_rate = (total_put_through / total_called * 100) if total_called > 0 else 0.0

    rows = [
        f"{'任务名称':<30} {'总量':>8} {'已呼':>8} {'接通':>8} {'接通率':>8}",
        "-" * 68,
    ]
    for t in tasks:
        called = t.get("calledPhoneNum", 0)
        put_through = t.get("putThroughPhoneNum", 0)
        rate = (put_through / called * 100) if called > 0 else 0.0
        rows.append(
            f"{t.get('taskName', 'N/A'):<30} {t.get('phoneNum', 0):>8} "
            f"{called:>8} {put_through:>8} {rate:>7.1f}%"
        )
    rows.append("-" * 68)
    rows.append(
        f"{'合计':<30} {total_phone:>8} {total_called:>8} "
        f"{total_put_through:>8} {overall_rate:>7.1f}%"
    )

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Action skills — call Baize outbound platform API
# ---------------------------------------------------------------------------


@skill(
    name="start_task",
    description=(
        "启动指定的AI外呼任务。需要提供任务ID列表和商户线路ID，可选择设置并发数或预计完成时间。"
        "启动前请先通过 query_tasks 确认任务ID，通过 get_tenant_lines 确认线路ID。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要启动的任务ID列表（数字数组）",
        },
        "tenant_line_id": {
            "type": "integer",
            "description": "用于外呼的商户线路ID",
        },
        "concurrency": {
            "type": "integer",
            "description": "并发数（手动模式时使用），不填则由系统自动分配",
            "required": False,
        },
        "expected_end_time": {
            "type": "string",
            "description": "预计完成时间（格式：yyyy-MM-dd HH:mm:ss），自动模式时使用",
            "required": False,
        },
        "include_auto_stop": {
            "type": "boolean",
            "description": "是否包含止损任务，默认 false",
            "required": False,
        },
    },
)
async def start_task(
    ctx: SkillContext,
    task_ids: list,
    tenant_line_id: int,
    concurrency: Optional[int] = None,
    expected_end_time: Optional[str] = None,
    include_auto_stop: bool = False,
) -> str:
    body: dict = {
        "taskIds": task_ids,
        "tenantLineId": tenant_line_id,
        "isIncludeAutoStop": include_auto_stop,
    }
    if concurrency is not None:
        body["concurrency"] = concurrency
    if expected_end_time:
        body["expectedEndTime"] = expected_end_time

    endpoint = "/AiSpeech/aiOutboundTask/startAiTask"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 已成功启动，线路ID：{tenant_line_id}。"
        return f"启动任务失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"启动任务时发生错误：{exc}"


@skill(
    name="stop_task",
    description=(
        "暂停指定的AI外呼任务。需要提供任务类型和任务ID列表。"
        "暂停后任务保留进度，可通过 resume_task 恢复。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要暂停的任务ID列表（数字数组）",
        },
        "task_type": {
            "type": "string",
            "description": "任务类型：OUTBOUND_AI（AI外呼）或 OUTBOUND_MANUAL（人工外呼），默认 OUTBOUND_AI",
            "required": False,
        },
    },
)
async def stop_task(
    ctx: SkillContext,
    task_ids: list,
    task_type: str = "OUTBOUND_AI",
) -> str:
    body = {"taskIds": task_ids, "taskType": task_type}
    endpoint = "/AiSpeech/aiOutboundTask/stopAiTask"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 已成功暂停。"
        return f"暂停任务失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"暂停任务时发生错误：{exc}"


@skill(
    name="resume_task",
    description=(
        "恢复已暂停的AI外呼任务，继续之前的外呼进度。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要恢复的任务ID列表（数字数组）",
        },
        "task_type": {
            "type": "string",
            "description": "任务类型：OUTBOUND_AI（AI外呼）或 OUTBOUND_MANUAL（人工外呼），默认 OUTBOUND_AI",
            "required": False,
        },
        "include_auto_stop": {
            "type": "boolean",
            "description": "是否包含止损任务，默认 false",
            "required": False,
        },
    },
)
async def resume_task(
    ctx: SkillContext,
    task_ids: list,
    task_type: str = "OUTBOUND_AI",
    include_auto_stop: bool = False,
) -> str:
    body = {
        "taskIds": task_ids,
        "taskType": task_type,
        "isIncludeAutoStop": include_auto_stop,
    }
    endpoint = "/AiSpeech/aiOutboundTask/resumeAiTask"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 已成功恢复运行。"
        return f"恢复任务失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"恢复任务时发生错误：{exc}"


@skill(
    name="change_concurrency",
    description=(
        "调整正在运行的外呼任务的并发数。可同时启动多个任务并设置统一并发。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要调整并发的任务ID列表",
        },
        "tenant_line_id": {
            "type": "integer",
            "description": "使用的商户线路ID",
        },
        "concurrency": {
            "type": "integer",
            "description": "新的并发数",
        },
        "include_auto_stop": {
            "type": "boolean",
            "description": "是否包含止损任务，默认 false",
            "required": False,
        },
    },
)
async def change_concurrency(
    ctx: SkillContext,
    task_ids: list,
    tenant_line_id: int,
    concurrency: int,
    include_auto_stop: bool = False,
) -> str:
    body = {
        "taskIds": task_ids,
        "tenantLineId": tenant_line_id,
        "concurrency": concurrency,
        "isIncludeAutoStop": include_auto_stop,
    }
    endpoint = "/AiSpeech/aiOutboundTask/editConcurrencyAndStartTask"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 并发已调整为 {concurrency}，线路ID：{tenant_line_id}。"
        return f"调整并发失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"调整并发时发生错误：{exc}"


@skill(
    name="change_tenant_line",
    description=(
        "切换外呼任务使用的商户线路，同时可调整并发数。"
        "切换前请通过 get_tenant_lines 确认目标线路ID。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要切换线路的任务ID列表",
        },
        "tenant_line_id": {
            "type": "integer",
            "description": "目标商户线路ID",
        },
        "concurrency": {
            "type": "integer",
            "description": "切换后的并发数",
            "required": False,
        },
        "include_auto_stop": {
            "type": "boolean",
            "description": "是否包含止损任务，默认 false",
            "required": False,
        },
    },
)
async def change_tenant_line(
    ctx: SkillContext,
    task_ids: list,
    tenant_line_id: int,
    concurrency: Optional[int] = None,
    include_auto_stop: bool = False,
) -> str:
    body: dict = {
        "taskIds": task_ids,
        "tenantLineId": tenant_line_id,
        "isIncludeAutoStop": include_auto_stop,
    }
    if concurrency is not None:
        body["concurrency"] = concurrency

    endpoint = "/AiSpeech/aiOutboundTask/editConcurrencyAndStartTask"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 已成功切换至线路ID：{tenant_line_id}。"
        return f"切换线路失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"切换线路时发生错误：{exc}"


@skill(
    name="forbid_district",
    description=(
        "为指定外呼任务设置地区屏蔽。支持屏蔽指定省份或城市，"
        "可选择屏蔽范围（全网 / 移动 / 联通 / 电信 / 虚拟运营商 / 未知运营商）。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要设置屏蔽的任务ID列表",
        },
        "provinces": {
            "type": "array",
            "items": {"type": "string"},
            "description": "要屏蔽的省份名称列表，如 [\"广东\", \"浙江\"]",
            "required": False,
        },
        "cities": {
            "type": "array",
            "items": {"type": "string"},
            "description": "要屏蔽的城市名称列表，如 [\"深圳\", \"广州\"]",
            "required": False,
        },
        "operator": {
            "type": "string",
            "description": (
                "运营商范围：ALL（全网）、YD（移动）、LT（联通）、DX（电信）、"
                "VIRTUAL（虚拟运营商）、UNKNOWN（未知），默认 ALL"
            ),
            "required": False,
        },
    },
)
async def forbid_district(
    ctx: SkillContext,
    task_ids: list,
    provinces: Optional[list] = None,
    cities: Optional[list] = None,
    operator: str = "ALL",
) -> str:
    body: dict = {
        "taskIds": task_ids,
        "changeType": "ADD",
        "operator": operator,
    }
    if provinces:
        body["restrictProvinces"] = provinces
    if cities:
        body["restrictCities"] = cities

    endpoint = "/AiSpeech/aiOutboundTask/changeRestrictArea"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            desc = []
            if provinces:
                desc.append(f"省份：{provinces}")
            if cities:
                desc.append(f"城市：{cities}")
            return f"已为任务 {task_ids} 设置屏蔽（{operator}）：{', '.join(desc)}。"
        return f"设置屏蔽失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"设置屏蔽时发生错误：{exc}"


@skill(
    name="allow_district",
    description=(
        "放开指定外呼任务的地区屏蔽，恢复对指定省份或城市的拨打。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要放开屏蔽的任务ID列表",
        },
        "provinces": {
            "type": "array",
            "items": {"type": "string"},
            "description": "要放开的省份名称列表",
            "required": False,
        },
        "cities": {
            "type": "array",
            "items": {"type": "string"},
            "description": "要放开的城市名称列表",
            "required": False,
        },
        "operator": {
            "type": "string",
            "description": "运营商范围：ALL / YD / LT / DX / VIRTUAL / UNKNOWN，默认 ALL",
            "required": False,
        },
    },
)
async def allow_district(
    ctx: SkillContext,
    task_ids: list,
    provinces: Optional[list] = None,
    cities: Optional[list] = None,
    operator: str = "ALL",
) -> str:
    body: dict = {
        "taskIds": task_ids,
        "changeType": "REMOVE",
        "operator": operator,
    }
    if provinces:
        body["restrictProvinces"] = provinces
    if cities:
        body["restrictCities"] = cities

    endpoint = "/AiSpeech/aiOutboundTask/changeRestrictArea"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            desc = []
            if provinces:
                desc.append(f"省份：{provinces}")
            if cities:
                desc.append(f"城市：{cities}")
            return f"已为任务 {task_ids} 放开屏蔽（{operator}）：{', '.join(desc)}。"
        return f"放开屏蔽失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"放开屏蔽时发生错误：{exc}"


@skill(
    name="create_main_account",
    description=(
        "新建主账号（运营账号）。需提供账号名、密码、显示名称及所属商户ID。"
        "仅限管理员操作。"
    ),
    parameters={
        "account": {
            "type": "string",
            "description": "新账号的登录名（英文字母和数字）",
        },
        "password": {
            "type": "string",
            "description": "账号初始密码",
        },
        "name": {
            "type": "string",
            "description": "账号显示名称（中文姓名或昵称）",
        },
        "tenant_id": {
            "type": "integer",
            "description": "所属商户ID",
        },
        "is_for_encryption": {
            "type": "boolean",
            "description": "是否为加密号码账号，默认 false",
            "required": False,
        },
    },
)
async def create_main_account(
    ctx: SkillContext,
    account: str,
    password: str,
    name: str,
    tenant_id: int,
    is_for_encryption: bool = False,
) -> str:
    body = {
        "account": account,
        "password": password,
        "name": name,
        "tenantId": tenant_id,
        "isForEncryptionPhones": is_for_encryption,
    }
    endpoint = "/AiSpeech/admin/addMainUser"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"主账号 [{account}]（{name}）已成功创建，所属商户ID：{tenant_id}。"
        return f"创建主账号失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"创建主账号时发生错误：{exc}"


@skill(
    name="create_sub_account",
    description=(
        "为当前主账号下新建子账号（操作员账号）。需提供登录名、密码、显示名称及角色ID。"
        "角色ID可通过查询角色列表获取。"
    ),
    parameters={
        "account": {
            "type": "string",
            "description": "子账号登录名",
        },
        "password": {
            "type": "string",
            "description": "子账号密码",
        },
        "name": {
            "type": "string",
            "description": "子账号显示名称",
        },
        "role_id": {
            "type": "integer",
            "description": "分配给该子账号的角色ID",
        },
    },
)
async def create_sub_account(
    ctx: SkillContext,
    account: str,
    password: str,
    name: str,
    role_id: int,
) -> str:
    body = {
        "account": account,
        "password": password,
        "password2": password,
        "name": name,
        "roleId": role_id,
    }
    endpoint = "/AiSpeech/admin/addSubUser"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"子账号 [{account}]（{name}）已成功创建，角色ID：{role_id}。"
        return f"创建子账号失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"创建子账号时发生错误：{exc}"


@skill(
    name="set_line_ratio",
    description=(
        "设置外呼任务的集线比（线路占用比例）。集线比越大，任务占用的线路资源越多。"
    ),
    parameters={
        "task_ids": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "要设置集线比的任务ID列表",
        },
        "line_ratio": {
            "type": "number",
            "description": "集线比，如 1.0、1.2、1.5，通常范围 0.5 ~ 3.0",
        },
    },
)
async def set_line_ratio(
    ctx: SkillContext,
    task_ids: list,
    line_ratio: float,
) -> str:
    body = {"taskIds": task_ids, "lineRatio": line_ratio}
    endpoint = "/AiSpeech/aiOutboundTask/setLineRatio"
    try:
        result = _baize_post(endpoint, body)
        if str(result.get("code")) == "2000":
            return f"任务 {task_ids} 的集线比已设置为 {line_ratio}。"
        return f"设置集线比失败：{result.get('msg', '未知错误')}"
    except Exception as exc:
        return f"设置集线比时发生错误：{exc}"


# ---------------------------------------------------------------------------
# InstructionEngine skill — parse natural language query to instructionBeanList
# (replaces HTTP data lookups with local JSON file reads)
# ---------------------------------------------------------------------------

# ---- Intent detection rules (mirrors Java intent_rules.json patterns) ----

_INTENT_RULES: list = [
    # (intent_name, score, regex_pattern_list)
    # Higher score takes priority in ambiguous matches.
    # NOTE: Python re does NOT support variable-length lookbehinds;
    # only fixed-length lookbehinds (e.g. (?<!X) where X is exactly 1 char)
    # are used here.  Lookaheads may be variable-length.
    ("START_TASK", 100, [r"操作(类型)?[：:]开[始起启]任务"]),
    ("START_TASK", 100, [r"用.{1,5}[0-9一二两三四五六七八九十百千万]?(并发|线路|仙人|得心|白泽|限时)下发"]),
    ("START_TASK", 1, [
        r"开[测冲]", r"首轮呼", r"呼掉", r"全开", r"开始赚钱吧",
        r"数据已推", r"已上传.{0,10}(?:线路|并发|下发)",
        r"呼叫(?!成功|失败)",
        r"开始(?:测试|启动|外呼|呼叫|任务)(?!了?[吗么])",
        r"(?<!放)开启?任务|启动任务",
        r"开始?呼(?!了?[吗么])",
        r"[小大]并发呼",
        r"(?:已推|已传|已上传).{0,20}(?:线路|并发|下发)",
        r"(?:并发|开始)下发(?!的)",
        r"[开走用呼跑](?:白泽|baize|仙人|xianren|得心|德心|dexin|限时|xianshi)",
    ]),
    ("STOP_TASK", 100, [r"操作(类型)?[：:](暂停|停止)任务"]),
    ("STOP_TASK", 1, [
        r"暂停(?!了?的)", r"停止(?!了?的)", r"停一?下", r"停呼",
    ]),
    ("RESUME_TASK", 100, [r"操作(类型)?[：:]恢复任务"]),
    ("RESUME_TASK", 1, [r"恢复(?:运行|外呼)?", r"继续(?:外呼|下发|呼)"]),
    ("CHANGE_CONCURRENCY", 100, [r"操作(类型)?[：:]调整并发"]),
    ("CHANGE_CONCURRENCY", 1, [
        r"(?:调整|加到|降到|开到)并发|并发(?:调整|[加降升提减]到)",
    ]),
    ("CHANGE_LINE", 100, [r"操作(类型)?[：:]切换线路"]),
    ("CHANGE_LINE", 2, [
        r"[切换](?:[至到为成]|一?下).{2,5}线路",
        r"改[至到为成用呼].{2,5}线路",
        r"[切换改](?:[至到为成]|一?下)(?:白泽|baize|仙人|xianren|得心|德心|dexin|限时|xianshi)",
    ]),
    ("FORBID_DISTRICT", 100, [r"操作(类型)?[：:](设置|地区)屏蔽"]),
    ("FORBID_DISTRICT", 1, [
        r"盲区",
        # Lookaheads (not lookbehinds) are variable-length safe in Python re
        r"屏蔽(?!.{0,10}(?:放|重)开)",
    ]),
    ("ALLOW_DISTRICT", 100, [r"操作(类型)?[：:]放开屏蔽"]),
    ("ALLOW_DISTRICT", 2, [
        r"(?:放开|重开|取消|解除).{0,10}屏蔽",
        r"(?:盲区|屏蔽).{0,3}(?:帮忙|麻烦|再|重新)?.{0,5}(?:[放重]开|重新再?开)",
    ]),
]


def _ie_detect_intents(text: str) -> list:
    """Return list of detected intent names, sorted by score (highest first)."""
    matched: dict = {}
    for intent, score, patterns in _INTENT_RULES:
        for pat in patterns:
            try:
                if re.search(pat, text):
                    if matched.get(intent, 0) < score:
                        matched[intent] = score
                    break
            except re.error:
                pass  # skip malformed patterns defensively
    return sorted(matched.keys(), key=lambda k: -matched[k])


# ---- Slot extraction helpers ----

def _ie_extract_account(text: str) -> Optional[str]:
    """Extract explicitly stated account name from text."""
    m = re.search(r'(?:主?账号|账户)[：:\s]*([A-Za-z0-9][A-Za-z0-9_]*)', text)
    return m.group(1) if m else None


def _ie_normalize_concurrency(val_str: str, unit_str: str) -> Optional[str]:
    """Normalize a concurrency value + unit to an integer string."""
    try:
        val = float(val_str)
        if unit_str in ('k', 'K', '千'):
            val = val * 1000
        elif unit_str == '万':
            val = val * 10000
        return str(int(val))
    except (ValueError, TypeError):
        return None


def _ie_extract_concurrency(text: str) -> Optional[str]:
    """Extract concurrency number from text. Avoids matching '呼通X' contexts."""
    patterns = [
        # "1k并发", "1000k并发"
        (r'(\d+(?:\.\d+)?)\s*([kK千])\s*并发', 1, 2),
        # "1万并发"
        (r'(\d+(?:\.\d+)?)\s*(万)\s*并发', 1, 2),
        # "并发开500", "并发加到1000"
        (r'并发[开到加降升调改设]\s*(\d+(?:\.\d+)?)\s*([kK千万]?)', 1, 2),
        # "500并发" — exclude '呼通' / '接通' prefixes (fixed-length lookbehinds)
        (r'(?<!呼通)(?<!接通)(?<!\d)(\d{2,5})\s*([kK千]?)\s*并发(?!率)', 1, 2),
        # "并发500"
        (r'并发\s*(\d+)\s*([kK千万]?)', 1, 2),
    ]
    for pat, val_grp, unit_grp in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val_str = m.group(val_grp)
            unit_str = m.group(unit_grp) if unit_grp else ''
            result = _ie_normalize_concurrency(val_str, unit_str or '')
            if result:
                return result
    return None


def _ie_extract_expected_end_time(text: str) -> Optional[str]:
    """Extract expected-end-time from '11:00前呼完' style expressions."""
    m = re.search(
        r'(\d{1,2})[:.：](\d{2})(?:之?前)(?:呼完|结束|完成|停|搞定|弄完|跑完|完)?',
        text,
    )
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{today} {h:02d}:{mi:02d}:00"
    return None


def _ie_extract_expected_start_time(text: str) -> Optional[str]:
    """Extract expected-start-time from '10:00开始' style expressions."""
    m = re.search(r'(\d{1,2})[:.：](\d{2})(?:开始|之?后|起|再?呼)', text)
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{today} {h:02d}:{mi:02d}:00"
    return None


def _ie_extract_connected_count(text: str) -> Optional[str]:
    """Extract expected connected-call count from '呼通5000暂停' style expressions."""
    m = re.search(r'呼通\s*(\d+(?:\.\d+)?)\s*([kK千万])?.{0,5}暂停', text)
    if m:
        return _ie_normalize_concurrency(m.group(1), m.group(2) or '')
    return None


def _ie_extract_task_name_filters(text: str) -> dict:
    """Extract task-name filter conditions (contain / not-contain / equal / suffix)."""
    result: dict = {"contain": [], "not_contain": [], "equal": [], "suffix": []}
    # Use non-greedy match and lookahead to stop at natural terminators
    for m in re.finditer(r'不[含包括].{0,2}?(.{1,15}?)(?=的任务|任务|，|,|。|全开|\s|$)', text):
        val = m.group(1).strip('，,。、 ')
        if val:
            result["not_contain"].append(val)
    for m in re.finditer(r'任务名称?[：:]\s*([^\s，,。\n]+)', text):
        result["equal"].append(m.group(1))
    for m in re.finditer(r'(?:任务)?名称?包含[：:\s]*([^\s，,。\n]+)', text):
        result["contain"].append(m.group(1))
    return result


def _ie_match_tasks(filters: dict, account: Optional[str], tasks: list) -> list:
    """Filter local task records by name filters and account."""
    result = tasks
    if account:
        result = [t for t in result if t.get("account", "").lower() == account.lower()]
    for s in filters.get("contain", []):
        result = [t for t in result if s in t.get("taskName", "")]
    for s in filters.get("not_contain", []):
        result = [t for t in result if s not in t.get("taskName", "")]
    for s in filters.get("equal", []):
        result = [t for t in result if t.get("taskName", "") == s]
    return result


def _ie_extract_operator(text: str) -> str:
    """Extract carrier operator type from text."""
    op_map = {"全网": "ALL", "移动": "YD", "联通": "LT", "电信": "DX",
              "虚拟": "VIRTUAL", "未知": "UNKNOWN"}
    for cn, code in op_map.items():
        if cn in text:
            return code
    m = re.search(r'\b(ALL|YD|LT|DX|VIRTUAL|UNKNOWN)\b', text, re.IGNORECASE)
    return m.group(1).upper() if m else "ALL"


_IE_PROVINCES = [
    "北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江",
    "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南",
    "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "内蒙古",
    "广西", "西藏", "宁夏", "新疆",
]

_IE_CITIES = list(dict.fromkeys([  # dict.fromkeys preserves insertion order while deduplicating
    "广州", "深圳", "北京", "上海", "天津", "重庆", "成都", "杭州", "武汉",
    "苏州", "南京", "西安", "长沙", "济南", "郑州", "东莞", "沈阳", "青岛",
    "合肥", "佛山", "宁波", "昆明", "南宁", "哈尔滨", "福州", "厦门", "大连",
    "太原", "长春", "南昌", "石家庄", "贵阳", "兰州", "银川", "西宁", "拉萨",
    "乌鲁木齐", "呼和浩特", "海口", "南通", "无锡", "常州", "泉州", "温州",
    "烟台", "唐山", "保定", "洛阳", "南阳", "泰州", "盐城", "连云港", "淮安",
    "宿迁", "芜湖", "蚌埠", "淮南", "铜陵", "安庆", "黄山", "绍兴", "台州",
    "金华", "嘉兴", "徐州", "扬州", "镇江", "湖州", "赣州", "吉安", "上饶",
    "宜春", "九江", "景德镇", "济宁", "菏泽", "临沂", "潍坊", "威海", "淄博",
    "枣庄", "泰安", "日照", "平顶山", "安阳", "新乡", "焦作", "许昌", "漯河",
    "三门峡", "商丘", "周口", "驻马店", "信阳", "开封", "荆州", "宜昌", "十堰",
    "孝感", "黄冈", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "益阳",
    "郴州", "永州", "珠海", "汕头", "韶关", "惠州", "中山", "江门", "湛江",
    "茂名", "肇庆", "清远", "潮州", "揭阳", "梅州", "绵阳", "德阳", "宜宾",
    "自贡", "泸州", "南充", "达州", "遂宁", "内江", "乐山", "广安", "资阳",
    "广元", "遵义", "安顺", "曲靖", "玉溪", "保山", "昭通", "大理", "丽江",
    "延安", "宝鸡", "咸阳", "铜川", "渭南", "汉中", "安康", "商洛", "榆林",
    "天水", "武威", "张掖", "酒泉", "庆阳",
]))


def _ie_extract_locations(text: str) -> tuple:
    """Return (provinces, cities) lists of location names found in text."""
    provinces = [p for p in _IE_PROVINCES if p in text]
    cities = [c for c in _IE_CITIES if c in text]
    return provinces, cities


def _ie_build_task_info_bean(
    tenant_line_name: Optional[str] = None,
    tenant_line_id: Optional[int] = None,
    concurrency: Optional[str] = None,
    expected_start_time: Optional[str] = None,
    expected_end_time: Optional[str] = None,
    expected_connected_count: Optional[str] = None,
    task_name_filters: Optional[dict] = None,
) -> dict:
    """Build a TaskInfoBean dict."""
    bean: dict = {}
    if tenant_line_name:
        bean["tenantLine"] = tenant_line_name
    if tenant_line_id is not None:
        bean["tenantLineId"] = tenant_line_id
    if concurrency:
        bean["concurrency"] = concurrency
    if expected_start_time:
        bean["expectedStartTime"] = expected_start_time
    if expected_end_time:
        bean["expectedEndTime"] = expected_end_time
    if expected_connected_count:
        bean["expectedConnectedCallCount"] = expected_connected_count
    if task_name_filters:
        if task_name_filters.get("contain"):
            bean["taskNameContainList"] = task_name_filters["contain"]
        if task_name_filters.get("not_contain"):
            bean["taskNameNotContainList"] = task_name_filters["not_contain"]
        if task_name_filters.get("equal"):
            bean["taskNameEqualList"] = task_name_filters["equal"]
        if task_name_filters.get("suffix"):
            bean["taskNameSuffixList"] = task_name_filters["suffix"]
    return bean


def _ie_build_instruction_bean(
    instruction_type: str,
    account: Optional[str] = None,
    task_info_bean_list: Optional[list] = None,
    extra: Optional[dict] = None,
) -> dict:
    """Build an InstructionBean dict mirroring the Java AbstractInstructionBean.

    The instructionId uses UUID hex (no dashes) to match the Java
    ``UUID.randomUUID().toString().replace("-", "")`` format.
    """
    bean: dict = {
        "instructionId": uuid.uuid4().hex,
        "instructionType": instruction_type,
        "account": account or "",
        "taskInfoBeanList": task_info_bean_list or [],
    }
    if extra:
        bean.update(extra)
    return bean


def _ie_split_segments(text: str) -> list:
    """
    Split a multi-operation query into individual segments for line-by-line parsing.

    Handles queries like "白泽加到1000，仙人500，得心6k" where each segment
    refers to a different line or concurrency setting.
    """
    parts = re.split(
        r'(?<=[0-9])[，,]\s*'  # comma after a digit
        r'|(?<=[kK千万])[，,]\s*'  # comma after a concurrency unit character
        r'|(?<=并发)[，,]\s*'   # comma after 并发
        r'|[；;]\s*'            # semicolons
        r'|\n+',                # newlines
        text,
    )
    return [p.strip() for p in parts if p.strip()]


def _ie_parse_line_segments(text: str, all_lines: list, account: Optional[str]) -> list:
    """
    Parse a query that may reference multiple lines/concurrencies into a list
    of TaskInfoBean dicts, one per distinct segment.

    Data for tenant line matching is read from the local tenant_lines.json file
    (replacing the original HTTP call to the Baize API).
    """
    segments = _ie_split_segments(text)
    task_name_filters = _ie_extract_task_name_filters(text)
    task_info_beans: list = []

    for seg in segments:
        # Match a tenant line referenced in this segment (local file lookup)
        matched_line = None
        for ln in all_lines:
            line_name = ln.get("lineName", "")
            line_number = ln.get("lineNumber", "")
            if line_name and (line_name in seg or (line_number and line_number in seg)):
                matched_line = ln
                break

        concurrency = _ie_extract_concurrency(seg)
        expected_end = _ie_extract_expected_end_time(seg)
        expected_start = _ie_extract_expected_start_time(seg)
        connected_count = _ie_extract_connected_count(seg)

        if matched_line or concurrency or expected_end or expected_start or connected_count:
            task_info_beans.append(_ie_build_task_info_bean(
                tenant_line_name=matched_line.get("lineName") if matched_line else None,
                tenant_line_id=matched_line.get("id") if matched_line else None,
                concurrency=concurrency,
                expected_start_time=expected_start,
                expected_end_time=expected_end,
                expected_connected_count=connected_count,
                task_name_filters=task_name_filters,
            ))

    # Fallback: try the full text when no individual segments yielded results
    if not task_info_beans:
        matched_line = next(
            (ln for ln in all_lines
             if ln.get("lineName", "") and ln.get("lineName", "") in text),
            None,
        )
        concurrency = _ie_extract_concurrency(text)
        expected_end = _ie_extract_expected_end_time(text)
        expected_start = _ie_extract_expected_start_time(text)
        connected_count = _ie_extract_connected_count(text)

        task_info_beans.append(_ie_build_task_info_bean(
            tenant_line_name=matched_line.get("lineName") if matched_line else None,
            tenant_line_id=matched_line.get("id") if matched_line else None,
            concurrency=concurrency,
            expected_start_time=expected_start,
            expected_end_time=expected_end,
            expected_connected_count=connected_count,
            task_name_filters=task_name_filters,
        ))

    return task_info_beans


# ---- Main skill ----

@skill(
    name="parse_query_to_instructions",
    description=(
        "解析自然语言外呼操作指令，返回结构化指令列表（instructionBeanList）。"
        "通过关键词和正则规则识别操作意图（开始/暂停/恢复任务、调整并发、切换线路、"
        "屏蔽/放开地区等），并从本地数据文件中匹配线路 ID、任务 ID 等实体，"
        "输出 JSON 格式的指令列表，供后续执行技能使用。"
        "注意：查询所需的线路和任务数据从本地文件读取，无需发起 HTTP 请求。"
    ),
    parameters={
        "query": {
            "type": "string",
            "description": "用户输入的自然语言外呼操作指令文本",
        },
        "account": {
            "type": "string",
            "description": "当前操作的主账号名称，用于筛选相关任务数据；不填则不限账号",
            "required": False,
        },
    },
)
async def parse_query_to_instructions(
    ctx: SkillContext,
    query: str,
    account: Optional[str] = None,
) -> str:
    # Load local data files — replaces HTTP API calls to the Baize platform
    all_lines: list = _load("tenant_lines.json")
    all_tasks: list = _load("tasks.json")

    # Detect intent(s) using rule-based matching
    intents = _ie_detect_intents(query)
    if not intents:
        return json.dumps([], ensure_ascii=False)

    # Use account from query text if not explicitly supplied
    account = account or _ie_extract_account(query)

    instruction_beans: list = []
    primary_intent = intents[0]

    if primary_intent in ("START_TASK", "RESUME_TASK", "STOP_TASK"):
        task_info_bean_list = _ie_parse_line_segments(query, all_lines, account)
        # Resolve task IDs from local tasks.json for each sub-operation
        for tib in task_info_bean_list:
            filters = {
                "contain": tib.get("taskNameContainList", []),
                "not_contain": tib.get("taskNameNotContainList", []),
                "equal": tib.get("taskNameEqualList", []),
                "suffix": tib.get("taskNameSuffixList", []),
            }
            matched = _ie_match_tasks(filters, account, all_tasks)
            if matched:
                tib["resolvedTaskIds"] = [t["id"] for t in matched]
        instruction_beans.append(_ie_build_instruction_bean(
            instruction_type=primary_intent,
            account=account,
            task_info_bean_list=task_info_bean_list,
        ))

    elif primary_intent == "CHANGE_CONCURRENCY":
        task_info_bean_list = _ie_parse_line_segments(query, all_lines, account)
        instruction_beans.append(_ie_build_instruction_bean(
            instruction_type="CHANGE_CONCURRENCY",
            account=account,
            task_info_bean_list=task_info_bean_list,
        ))

    elif primary_intent == "CHANGE_LINE":
        task_info_bean_list = _ie_parse_line_segments(query, all_lines, account)
        instruction_beans.append(_ie_build_instruction_bean(
            instruction_type="CHANGE_LINE",
            account=account,
            task_info_bean_list=task_info_bean_list,
        ))

    elif primary_intent == "FORBID_DISTRICT":
        provinces, cities = _ie_extract_locations(query)
        operator = _ie_extract_operator(query)
        task_name_filters = _ie_extract_task_name_filters(query)
        matched_tasks = _ie_match_tasks(task_name_filters, account, all_tasks)
        instruction_beans.append(_ie_build_instruction_bean(
            instruction_type="FORBID_DISTRICT",
            account=account,
            extra={
                "provinces": provinces,
                "cities": cities,
                "operator": operator,
                "resolvedTaskIds": [t["id"] for t in matched_tasks],
            },
        ))

    elif primary_intent == "ALLOW_DISTRICT":
        provinces, cities = _ie_extract_locations(query)
        operator = _ie_extract_operator(query)
        task_name_filters = _ie_extract_task_name_filters(query)
        matched_tasks = _ie_match_tasks(task_name_filters, account, all_tasks)
        instruction_beans.append(_ie_build_instruction_bean(
            instruction_type="ALLOW_DISTRICT",
            account=account,
            extra={
                "provinces": provinces,
                "cities": cities,
                "operator": operator,
                "resolvedTaskIds": [t["id"] for t in matched_tasks],
            },
        ))

    return json.dumps(instruction_beans, ensure_ascii=False, indent=2)
