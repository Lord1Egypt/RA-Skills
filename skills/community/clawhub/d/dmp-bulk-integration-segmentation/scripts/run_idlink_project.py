#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量打通人群项目统一执行入口（对齐批量圈包的“分批+定时监控”思路）

模式说明：
- init：读取输入、校验、生成计划；确认后仅创建“第一批”（最多5个）并输出“定时监控任务模板”。
- monitor：定时任务触发时执行：检查当前批状态；若本批全部成功则创建下一批；全部批次完成则汇总输出并触发第八步任务记录检查提示。

注意：本脚本不直接创建定时任务，仅输出模板；具体创建需使用你们平台提供的“定时任务工具”。

依赖：
- 鉴权能力（mingdata-dmp-auth）的 minri_dmp_api.py，用于签名与调用 OPEN API。
"""

import argparse
import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path
import subprocess

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except Exception:
    PANDAS_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from cron_helper import check_cron_setup, mark_cron_setup as _mark_cron, cleanup as _cron_cleanup  # noqa: E402

DATA_DIR = SKILL_DIR / "data" / "plans"

ENDPOINT_CREATE = "/audience/idlink/create"
ENDPOINT_TASKLIST = "/audience/manage/taskList"
ENDPOINT_AUDIENCE_LIST = "/audience/manage/list"

DEFAULT_BATCH_SIZE = 1
DEFAULT_POLL_INTERVAL_SEC = 60
DEFAULT_POLL_TIMEOUT_SEC = 1800

REQUIRED_FIELDS = [
    "name",
    "inputAudienceId",
    "linkType",
    "inputTrackType",
    "inputIdTypes",
    "outputTrackType",
    "outputIdTypes",
]

TRACK_TYPES = {"MOBILE", "OTT"}
# 按用户提供的截图口径：仅对外展示/校验以下可选范围
MOBILE_ID_TYPES = {"MD5_IDFA", "MD5_IMEI", "MD5_OAID"}
OTT_ID_TYPES = {"MD5_MAC"}


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_project_id():
    return f"idlink_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def ensure_project_dirs(project_id: str):
    project_dir = DATA_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def safe_json_dump(obj, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_auth_skill_path():
    try:
        from find_auth_skill import find_auth_skill_path as _finder
        return _finder()
    except Exception:
        return None


def call_api_via_auth(auth_script: Path, method: str, endpoint: str, body: dict, timeout=60):
    try:
        result = subprocess.run(
            ["python3", str(auth_script), method.upper(), endpoint, json.dumps(body, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"_call_error": "TIMEOUT", "_raw": ""}

    stdout = (result.stdout or "").strip()
    if not stdout:
        return {"_call_error": "EMPTY_OUTPUT", "_raw": "", "_stderr": result.stderr}

    try:
        return json.loads(stdout)
    except Exception:
        return {"_call_error": "NON_JSON_OUTPUT", "_raw": stdout, "_stderr": result.stderr}


def normalize_idtypes(val):
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]

    s = str(val).strip()
    if not s:
        return []

    if s.startswith("[") and s.endswith("]"):
        try:
            arr = json.loads(s)
            if isinstance(arr, list):
                return [str(x).strip() for x in arr if str(x).strip()]
        except Exception:
            pass

    return [x.strip() for x in s.split(",") if x.strip()]


def fetch_audience_name(auth_script: Path, audience_id: int):
    """通过人群列表查询接口按ID获取人群名称。找不到则返回None。"""
    resp = call_api_via_auth(auth_script, "POST", ENDPOINT_AUDIENCE_LIST, {"audienceIds": [audience_id], "pageSize": 20, "pageNum": 1}, timeout=60)
    try:
        if isinstance(resp, dict) and resp.get("code") == "0":
            data = resp.get("data")
            if isinstance(data, dict):
                lst = data.get("list")
                if isinstance(lst, list) and lst:
                    # 优先匹配指定ID
                    for it in lst:
                        if isinstance(it, dict) and it.get("audienceId") == audience_id:
                            return it.get("audienceName")
                    # 否则取第一条
                    return lst[0].get("audienceName") if isinstance(lst[0], dict) else None
    except Exception:
        pass
    return None


def resolve_names_for_tasks(auth_script: Path, tasks: list):
    """为每条任务补齐 _audienceName 与 name（若未提供新名称则按规则自动生成）。"""
    for t in tasks:
        aud_id = t.get("inputAudienceId")
        if aud_id is None:
            continue
        aud_name = fetch_audience_name(auth_script, int(aud_id))
        if not aud_name:
            raise RuntimeError(f"无法通过人群ID查询到人群名称，请检查被打通的人群ID是否存在：{aud_id}")
        t["_audienceName"] = str(aud_name).strip()
        if not t.get("name"):
            suffix = "_ott" if t.get("outputTrackType") == "OTT" else "_mobile"
            t["name"] = f"{t['_audienceName']}{suffix}"
    return tasks


def parse_tasks_from_json(json_str: str):
    """支持用户一次性输入：
    - 单条：JSON对象
    - 多条：JSON数组

    同时兼容“中文字段”和“接口字段名”两种写法。
    """
    try:
        obj = json.loads(json_str)
    except Exception as e:
        raise ValueError(f"JSON解析失败: {e}")

    if isinstance(obj, dict):
        return [obj]
    if isinstance(obj, list):
        return obj
    raise ValueError("JSON必须是对象或数组")


def parse_tasks_from_file(file_path: str):
    if not PANDAS_AVAILABLE:
        raise RuntimeError("缺少pandas，无法读取Excel/CSV文件")

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = p.suffix.lower()
    if suffix not in {".xlsx", ".xls", ".csv"}:
        raise ValueError("仅支持 .xlsx/.xls/.csv")

    if suffix == ".csv":
        df = pd.read_csv(p, dtype="object")
    else:
        df = pd.read_excel(p, dtype="object")

    df_cols = {str(c).strip(): c for c in df.columns}
    lower_map = {str(c).strip().lower(): c for c in df.columns}

    def pick(*candidates):
        """按候选列名依次匹配，支持中文表头与英文表头。"""
        for col_name in candidates:
            if not col_name:
                continue
            if col_name in df_cols:
                return df_cols[col_name]
            if col_name.lower() in lower_map:
                return lower_map[col_name.lower()]
        return None

    # 中文字段优先（面向业务人员）
    # 人群名称无需用户提供；如用户表格里仍有该列可忽略（脚本会以API查询结果为准）
    col_audience_name = pick("被打通的人群名称", "人群名称", "audienceName")
    col_input_aud = pick("被打通的人群ID", "人群ID", "inputAudienceId")
    col_direction = pick("打通方向", "direction")
    col_in_ids = pick("输入终端ID类型", "inputIdTypes")
    col_out_ids = pick("输出终端ID类型", "outputIdTypes")
    col_custom_name = pick("新名称", "name")
    col_link_type = pick("打通类型", "linkType")
    col_brands = pick("品牌", "brandId", "brand")
    col_ieee = pick("MAC格式过滤", "ieeeFlag", "ieee")

    tasks = []
    for _, row in df.iterrows():
        task = {
            # 中文字段（用户侧）
            "被打通的人群名称": None if col_audience_name is None else row.get(col_audience_name),
            "被打通的人群ID": None if col_input_aud is None else row.get(col_input_aud),
            "打通方向": None if col_direction is None else row.get(col_direction),
            "输入终端ID类型": None if col_in_ids is None else row.get(col_in_ids),
            "输出终端ID类型": None if col_out_ids is None else row.get(col_out_ids),
            "新名称": None if col_custom_name is None else row.get(col_custom_name),
            "打通类型": None if col_link_type is None else row.get(col_link_type),
            # v1.4新增字段
            "品牌": None if col_brands is None else row.get(col_brands),
            "MAC格式过滤": None if col_ieee is None else row.get(col_ieee),
        }

        # 跳过空行：只要核心中文字段全空则跳过
        core_keys = ["被打通的人群ID", "打通方向", "输入终端ID类型", "输出终端ID类型"]
        if all((task.get(k) is None or str(task.get(k)).strip() == "") for k in core_keys):
            continue

        tasks.append(task)

    return tasks


def _get(task: dict, *keys, default=None):
    for k in keys:
        if k in task and task[k] is not None and str(task[k]).strip() != "":
            return task[k]
    return default


def _normalize_direction(val: str):
    s = (val or "").strip()
    s = s.replace(" ", "")
    # 兼容多种写法
    if s in {"移动端→OTT端", "移动端->OTT端", "MOBILE->OTT", "MOBILE→OTT", "MOBILE-OTT"}:
        return "MOBILE_TO_OTT"
    if s in {"OTT端→移动端", "OTT端->移动端", "OTT->MOBILE", "OTT→MOBILE", "OTT-MOBILE"}:
        return "OTT_TO_MOBILE"
    return None


def validate_task(task: dict, index: int):
    """校验并把“中文字段”转换为接口所需字段（不在用户侧暴露英文参数名）。"""

    # 1) 读取中文字段（优先）或兼容接口字段
    # 人群名称不要求用户输入；将通过 inputAudienceId 调用人群列表查询接口自动获取
    audience_name = _get(task, "被打通的人群名称", "audienceName")
    input_audience_id = _get(task, "被打通的人群ID", "inputAudienceId")
    direction = _get(task, "打通方向", "direction")
    in_id_types_raw = _get(task, "输入终端ID类型", "inputIdTypes")
    out_id_types_raw = _get(task, "输出终端ID类型", "outputIdTypes")
    custom_name = _get(task, "新名称", "name")
    link_type_raw = _get(task, "打通类型", "linkType")
    # v1.4新增字段
    brand_id_raw = _get(task, "品牌", "brandId", "brand")
    ieee_flag_raw = _get(task, "MAC格式过滤", "ieeeFlag", "ieee")

    missing_cn = []
    # 人群名称不再要求用户提供：后续会用人群ID自动查询
    if input_audience_id is None:
        missing_cn.append("被打通的人群ID")
    if direction is None:
        missing_cn.append("打通方向")
    if in_id_types_raw is None:
        missing_cn.append("输入终端ID类型")
    if out_id_types_raw is None:
        missing_cn.append("输出终端ID类型")

    if missing_cn:
        return False, {"index": index, "missing_fields": missing_cn}

    # 2) 标准化方向 -> 输入/输出终端
    dir_norm = _normalize_direction(str(direction))
    if not dir_norm:
        return False, {"index": index, "error": "打通方向不合法，请使用：移动端→OTT端 或 OTT端→移动端"}

    if dir_norm == "MOBILE_TO_OTT":
        in_track, out_track = "MOBILE", "OTT"
    else:
        in_track, out_track = "OTT", "MOBILE"

    # 3) ID types
    in_ids = normalize_idtypes(in_id_types_raw)
    out_ids = normalize_idtypes(out_id_types_raw)
    if not in_ids:
        return False, {"index": index, "error": "输入终端ID类型不能为空"}
    if not out_ids:
        return False, {"index": index, "error": "输出终端ID类型不能为空"}

    # 4) inputAudienceId
    try:
        input_aud = int(str(input_audience_id).strip())
    except Exception:
        return False, {"index": index, "error": "被打通的人群ID必须为数字"}

    # 5) linkType：支持中文默认
    # 约定：不填则默认TV-移动端跨屏打通=1；如果用户给了数字则用数字
    link_type = 1
    if link_type_raw is not None:
        s = str(link_type_raw).strip()
        if s.isdigit():
            link_type = int(s)
        else:
            # 用户侧只展示中文选项，这里做最小兼容（若未来有更多类型可扩展映射）
            if "跨屏" in s:
                link_type = 1

    # 6) 最小匹配校验
    if in_track == "MOBILE":
        if not all(x in MOBILE_ID_TYPES for x in in_ids):
            return False, {"index": index, "error": "输入终端ID类型与打通方向（输入=移动端）不匹配"}
    else:
        if not all(x in OTT_ID_TYPES for x in in_ids):
            return False, {"index": index, "error": "输入终端ID类型与打通方向（输入=OTT端）不匹配"}

    if out_track == "MOBILE":
        if not all(x in MOBILE_ID_TYPES for x in out_ids):
            return False, {"index": index, "error": "输出终端ID类型与打通方向（输出=移动端）不匹配"}
    else:
        if not all(x in OTT_ID_TYPES for x in out_ids):
            return False, {"index": index, "error": "输出终端ID类型与打通方向（输出=OTT端）不匹配"}

    # 7) 新名称：若用户提供则使用；否则稍后将通过 inputAudienceId 查询到的人群名称自动生成
    # v1.4: 解析品牌字段
    brand_id_list = []
    if brand_id_raw is not None:
        if isinstance(brand_id_raw, list):
            brand_id_list = [str(b).strip() for b in brand_id_raw if b]
        elif isinstance(brand_id_raw, str):
            brand_id_list = [b.strip() for b in brand_id_raw.split(',') if b.strip()]
    # v1.4: 解析ieeeFlag（MAC格式过滤）
    ieee_flag = None
    if ieee_flag_raw is not None:
        try:
            ieee_flag = int(ieee_flag_raw) if str(ieee_flag_raw).strip() else None
        except (ValueError, TypeError):
            ieee_flag = None
    normalized = {
        "name": None if (custom_name is None or str(custom_name).strip()=="") else str(custom_name).strip(),
        "inputAudienceId": input_aud,
        "linkType": link_type,
        "inputTrackType": in_track,
        "inputIdTypes": in_ids,
        "outputTrackType": out_track,
        "outputIdTypes": out_ids,
        "brandId": brand_id_list,
        "ieeeFlag": ieee_flag,  # v1.4: 1=输出标准MAC格式, 0/None=正常输出
        # 仅用于日志/汇总
        "_audienceName": None,
        "_direction": "移动端→OTT端" if dir_norm == "MOBILE_TO_OTT" else "OTT端→移动端",
    }

    return True, normalized


def build_monitor_job_template(project_id: str, audience_ids: list, interval_ms: int = 60000):
    aid_str = ','.join(str(a) for a in audience_ids) if audience_ids else ''
    return {
        "_IMPORTANT_": "🔴 必须使用 cron(action='add', job=<此对象>) 工具创建此监控任务，严格禁止：(1) exec(background=true)+sleep轮询（session断连后无法唤醒AI导致不通知，已发生故障）；(2) openclaw cron add命令行（无法设置sessionTarget=current）。必须设置 sessionTarget='current', delivery={'mode':'none'}。完成后所有任务结束时调用cron(action='remove')删除本任务。",
        "name": f"DMP打通监控-{project_id}",
        "schedule": {"kind": "every", "everyMs": interval_ms},
        "payload": {
            "kind": "agentTurn",
            "message": f"检查DMP批量打通项目{project_id}状态：运行 cd ~/.openclaw/skills/明日dmp批量打通圈包 && python3 scripts/run_idlink_project.py --mode monitor --project-id {project_id} 推进批次；若本批完成则自动创建下一批；全部完成则执行第八步任务记录检查、汇报汇总结果、然后调用cron(action='remove', jobId=<本任务ID>)删除此监控任务。本批audienceIds=[{aid_str}]。"
        },
        "sessionTarget": "current",
        "delivery": {"mode": "none"}
    }


def summarize_and_write_result(project_id: str, project_dir: Path, success_rows, failed_rows):
    result = {
        "projectId": project_id,
        "completedAt": now_ts(),
        "success": success_rows,
        "failed": failed_rows,
    }
    safe_json_dump(result, project_dir / "result.json")

    print("\n==================== 汇总输出（强制） ====================")
    if success_rows:
        print("\n✅ 成功清单（人群名称 + audienceId）")
        for r in success_rows:
            print(f"- {r.get('name')}\t{r.get('audienceId')}")
    else:
        print("\n✅ 成功清单：无")

    if failed_rows:
        print("\n⚠️ 失败清单（人群名称 + 原因）")
        for r in failed_rows:
            name = r.get("name") if isinstance(r, dict) else None
            err = r.get("error") if isinstance(r, dict) else str(r)
            if name:
                print(f"- {name}\t{err}")
            else:
                print(f"- {err}")
    else:
        print("\n⚠️ 失败清单：无")

    print(f"\n结果文件：{project_dir / 'result.json'}")
    print("==========================================================\n")

    # 第八步：任务记录检查（强制提示）
    print("【第八步】请执行任务记录检查：")
    print(f"python3 scripts/check_task_logger.py {project_id}")


def monitor_turn(auth_script: Path, project_id: str, poll_interval: int, poll_timeout: int):
    # 🔴 硬拦截：monitor模式必须检查cron锁文件
    cron_check = check_cron_setup(project_id, str(DATA_DIR))
    if not cron_check["setup"]:
        print(json.dumps({
            "status": "blocked",
            "blocker": "CRON_NOT_SETUP",
            "message": "🔴 monitor模式拒绝执行：cron监控未设置。可能是有人用exec background而不是cron工具触发的。",
            "instruction": "你必须使用 cron(action='add', job=...) 工具创建监控任务，然后运行 cron_helper.py mark-cron-set 标记。禁止用exec后台轮询。",
            "cron_check": cron_check
        }, ensure_ascii=False, indent=2))
        sys.exit(2)

    project_dir = ensure_project_dirs(project_id)
    plan_path = project_dir / "plan.json"
    status_path = project_dir / "status.json"
    if not plan_path.exists() or not status_path.exists():
        print(json.dumps({"status": "error", "message": f"项目不存在或缺少状态文件: {project_id}"}, ensure_ascii=False, indent=2))
        sys.exit(2)

    plan = load_json(plan_path)
    status = load_json(status_path)

    total = int(plan.get("totalTasks", 0))
    batch_size = int(plan.get("batchSize", DEFAULT_BATCH_SIZE))
    batch_count = int(plan.get("totalBatches", math.ceil(total / batch_size)))

    on_create_fail = (plan.get("failureStrategy") or {}).get("onCreateFail", "pause")
    on_exec_fail = (plan.get("failureStrategy") or {}).get("onExecuteFail", "pause")

    current_batch = int(status.get("currentBatch", 0))
    created_tasks = status.get("tasks", [])

    # 找到当前批的 audienceIds（从 status.tasks 里取 batch_no）
    batch_audience_ids = []
    for t in created_tasks:
        if t.get("batch") == current_batch and t.get("audience_id"):
            batch_audience_ids.append(t.get("audience_id"))

    if current_batch == 0:
        print(json.dumps({"status": "error", "message": "当前批次为0，说明未初始化创建第一批，请先运行 init 模式"}, ensure_ascii=False, indent=2))
        sys.exit(2)

    # 轮询本批状态
    start = time.time()
    while True:
        resp = call_api_via_auth(auth_script, "POST", ENDPOINT_TASKLIST, {"audienceIds": batch_audience_ids}, timeout=60)
        data = resp.get("data") if isinstance(resp, dict) else None

        if isinstance(resp, dict) and resp.get("code") == "0" and isinstance(data, list):
            failed = [d for d in data if d.get("audienceStatus") == 0]
            all_success = all(d.get("audienceStatus") == 1 for d in data)
            if failed:
                # 计算失败
                status["lastPollAt"] = now_ts()
                safe_json_dump(status, status_path)
                print(json.dumps({"status": "failed", "message": "本批计算失败", "failed": failed[0]}, ensure_ascii=False, indent=2))
                if on_exec_fail == "pause":
                    sys.exit(5)
                break
            if all_success:
                break

        if time.time() - start > poll_timeout:
            print(json.dumps({"status": "timeout", "message": "本批轮询超时"}, ensure_ascii=False, indent=2))
            if on_exec_fail == "pause":
                sys.exit(5)
            break

        time.sleep(poll_interval)

    # 若当前批已成功，创建下一批或结束
    if current_batch >= batch_count:
        # 全部批次已创建并计算完成，输出汇总
        success_rows = []
        failed_rows = []
        for t in created_tasks:
            if t.get("status") == "success" and t.get("audience_id"):
                success_rows.append({"name": t.get("name"), "audienceId": t.get("audience_id"), "batch": t.get("batch")})
            if t.get("status") == "failed":
                failed_rows.append({"name": t.get("name"), "error": t.get("error")})

        summarize_and_write_result(project_id, project_dir, success_rows, failed_rows)
        status["status"] = "completed"
        status["completedAt"] = now_ts()
        safe_json_dump(status, status_path)
        sys.exit(0)

    # 创建下一批
    next_batch = current_batch + 1
    batch_start = (next_batch - 1) * batch_size
    batch_end = min(next_batch * batch_size, total)
    tasks = plan.get("tasks", [])
    next_tasks = tasks[batch_start:batch_end]

    print(f"\n【监控触发】当前批={current_batch} 已完成，准备创建下一批={next_batch}（{batch_start+1}-{batch_end}）")

    for idx, task in enumerate(next_tasks, start=batch_start + 1):
        payload = {
            "name": task["name"],
            "inputAudienceId": task["inputAudienceId"],
            "linkType": task["linkType"],
            "inputTrackType": task["inputTrackType"],
            "inputIdTypes": task["inputIdTypes"],
            "outputTrackType": task["outputTrackType"],
            "outputIdTypes": task["outputIdTypes"],
        }
        # v1.4: 品牌字段
        if task.get("brandId"):
            payload["brandId"] = task["brandId"]
        # v1.4: MAC标准格式过滤（仅TV-Mobile跨屏打通时有效）
        if task.get("ieeeFlag") is not None:
            payload["ieeeFlag"] = task["ieeeFlag"]
        resp = call_api_via_auth(auth_script, "POST", ENDPOINT_CREATE, payload, timeout=60)
        if isinstance(resp, dict) and resp.get("code") == "0" and isinstance(resp.get("data"), dict) and resp["data"].get("audienceId"):
            aud_id = resp["data"]["audienceId"]
            status.setdefault("tasks", []).append({
                "task_id": idx,
                "name": task["name"],
                "audience_id": aud_id,
                "status": "success",
                "createdAt": now_ts(),
                "batch": next_batch,
            })
            print(f"  ✅ 创建成功：{task['name']} -> audienceId={aud_id}")
        else:
            err = resp.get("msg") if isinstance(resp, dict) else "创建失败"
            status.setdefault("tasks", []).append({
                "task_id": idx,
                "name": task["name"],
                "audience_id": None,
                "status": "failed",
                "createdAt": now_ts(),
                "error": err,
                "batch": next_batch,
            })
            print(f"  ❌ 创建失败：{task['name']} | {err}")
            if on_create_fail == "pause":
                safe_json_dump(status, status_path)
                sys.exit(4)

    status["currentBatch"] = next_batch
    status["lastPollAt"] = now_ts()
    safe_json_dump(status, status_path)

    print("\n【下一步】请继续由定时任务触发 monitor 模式检查本批状态。")


def init_mode(args, auth_script: Path):
    if bool(args.file) == bool(args.json):
        print(json.dumps({"status": "error", "message": "必须且只能提供 --file 或 --json"}, ensure_ascii=False, indent=2))
        sys.exit(2)

    project_id = args.project_id or generate_project_id()
    project_dir = ensure_project_dirs(project_id)

    try:
        raw_tasks = parse_tasks_from_file(args.file) if args.file else parse_tasks_from_json(args.json)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    if not raw_tasks:
        print(json.dumps({"status": "error", "message": "未解析到任何任务"}, ensure_ascii=False, indent=2))
        sys.exit(2)

    normalized_tasks = []
    errors = []
    for i, t in enumerate(raw_tasks, start=1):
        ok, info = validate_task(t, i)
        if ok:
            normalized_tasks.append(info)
        else:
            errors.append(info)

    if errors:
        print(json.dumps({
            "status": "error",
            "message": "参数校验失败，请补全或修正后重试（不支持逐条追问模式）",
            "errors": errors,
            "required_fields": REQUIRED_FIELDS
        }, ensure_ascii=False, indent=2))
        sys.exit(2)

    # 自动查询人群名称并生成默认新名称（若未提供）
    try:
        normalized_tasks = resolve_names_for_tasks(auth_script, normalized_tasks)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    total = len(normalized_tasks)
    batch_size = max(1, int(args.batch_size))
    batch_count = math.ceil(total / batch_size)

    plan = {
        "projectId": project_id,
        "createdAt": now_ts(),
        "input": {"mode": "file" if args.file else "json", "file": args.file, "jsonProvided": bool(args.json)},
        "totalTasks": total,
        "batchSize": batch_size,
        "totalBatches": batch_count,
        "failureStrategy": {"onCreateFail": args.on_create_fail, "onExecuteFail": args.on_exec_fail},
        "tasks": normalized_tasks,
    }

    status = {
        "projectId": project_id,
        "status": "running",
        "createdAt": plan["createdAt"],
        "currentBatch": 0,
        "tasks": [],
        "lastPollAt": None,
        "failureStrategy": plan["failureStrategy"],
    }

    safe_json_dump(plan, project_dir / "plan.json")
    safe_json_dump(status, project_dir / "status.json")

    print(f"\n【执行计划预览】projectId={project_id} 任务数={total} 批次数={batch_count} 批大小={batch_size}")
    print(f"失败策略：创建失败={args.on_create_fail} | 计算失败={args.on_exec_fail}")
    print("\n任务预览（前3条）：")
    for t in normalized_tasks[:3]:
        print(f"- {t.get('name')} | inputAudienceId={t.get('inputAudienceId')} | {t.get('inputTrackType')}->{t.get('outputTrackType')}")
    if total > 3:
        print(f"- ... 其余 {total-3} 条略")

    if not args.yes:
        print("\n【需要确认】请确认以上执行计划无误后再执行创建：")
        print("- 若要开始执行，请重新运行命令并追加参数：--yes")
        sys.exit(0)

    # 仅创建第一批
    first_batch = 1
    batch_start = 0
    batch_end = min(batch_size, total)
    batch_tasks = normalized_tasks[batch_start:batch_end]

    print(f"\n【开始执行】创建第1批（{batch_start+1}-{batch_end}），共 {len(batch_tasks)} 条")

    batch_audience_ids = []
    for idx, task in enumerate(batch_tasks, start=1):
        payload = {
            "name": task["name"],
            "inputAudienceId": task["inputAudienceId"],
            "linkType": task["linkType"],
            "inputTrackType": task["inputTrackType"],
            "inputIdTypes": task["inputIdTypes"],
            "outputTrackType": task["outputTrackType"],
            "outputIdTypes": task["outputIdTypes"],
        }
        # v1.4: 品牌字段
        if task.get("brandId"):
            payload["brandId"] = task["brandId"]
        # v1.4: MAC标准格式过滤（仅TV-Mobile跨屏打通时有效）
        if task.get("ieeeFlag") is not None:
            payload["ieeeFlag"] = task["ieeeFlag"]
        resp = call_api_via_auth(auth_script, "POST", ENDPOINT_CREATE, payload, timeout=60)
        if isinstance(resp, dict) and resp.get("code") == "0" and isinstance(resp.get("data"), dict) and resp["data"].get("audienceId"):
            aud_id = resp["data"]["audienceId"]
            batch_audience_ids.append(aud_id)
            status.setdefault("tasks", []).append({
                "task_id": idx,
                "name": task["name"],
                "audience_id": aud_id,
                "status": "success",
                "createdAt": now_ts(),
                "batch": first_batch,
            })
            print(f"  ✅ 创建成功：{task['name']} -> audienceId={aud_id}")
        else:
            err = resp.get("msg") if isinstance(resp, dict) else "创建失败"
            status.setdefault("tasks", []).append({
                "task_id": idx,
                "name": task["name"],
                "audience_id": None,
                "status": "failed",
                "createdAt": now_ts(),
                "error": err,
                "batch": first_batch,
            })
            print(f"  ❌ 创建失败：{task['name']} | {err}")
            if args.on_create_fail == "pause":
                safe_json_dump(status, project_dir / "status.json")
                sys.exit(4)

    status["currentBatch"] = first_batch
    status["lastPollAt"] = now_ts()
    safe_json_dump(status, project_dir / "status.json")

    # 输出定时任务模板
    job = build_monitor_job_template(project_id, batch_audience_ids, interval_ms=int(args.poll_interval) * 1000)
    print("\n【🔴 强制：创建cron监控任务】")
    print("必须立即使用 cron(action='add', job=<下面的JSON对象>) 工具创建监控任务。")
    print("严格禁止：(1) exec background+sleep轮询；(2) openclaw cron add命令行。")
    print("\n🔴 创建完cron任务后，必须立即运行以下命令写入锁标记（否则monitor模式会拒绝推进）：")
    print(f"  python3 scripts/cron_helper.py --project-id {project_id} --base-dir {DATA_DIR} mark-cron-set --cron-name {job['name']}")
    print("\ncron job 参数（将此对象作为job参数传入cron工具）：")
    print(json.dumps(job, ensure_ascii=False, indent=2))
    print("\n创建完成后，cron每60秒自动触发monitor模式推进后续批次，全部完成后需主动删除cron任务。")
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="明日DMP 批量打通人群项目执行入口")
    parser.add_argument("--mode", choices=["init", "monitor"], default="init", help="init=初始化并创建第一批；monitor=定时任务触发检查并推进")
    parser.add_argument("--file", help="Excel/CSV 文件路径（init模式）")
    parser.add_argument("--json", help="一次性JSON（对象或数组）（init模式）")
    parser.add_argument("--project-id", help="项目ID（init可选，monitor必填）")
    parser.add_argument("--on-create-fail", choices=["pause", "skip"], default="pause")
    parser.add_argument("--on-exec-fail", choices=["pause", "skip"], default="pause")
    parser.add_argument("--yes", action="store_true", help="确认执行：init模式下跳过仅预览直接创建第一批")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL_SEC)
    parser.add_argument("--poll-timeout", type=int, default=DEFAULT_POLL_TIMEOUT_SEC)
    args = parser.parse_args()

    auth_script = find_auth_skill_path()
    if not auth_script:
        print(json.dumps({
            "status": "error",
            "message": "未找到鉴权能力脚本（mingdata-dmp-auth），请先完成安装",
            "hint": "阅读 references/技能安装与环境检查.md"
        }, ensure_ascii=False, indent=2))
        sys.exit(3)

    if args.mode == "init":
        init_mode(args, auth_script)
    else:
        if not args.project_id:
            print(json.dumps({"status": "error", "message": "monitor 模式必须提供 --project-id"}, ensure_ascii=False, indent=2))
            sys.exit(2)
        monitor_turn(auth_script, args.project_id, int(args.poll_interval), int(args.poll_timeout))


if __name__ == "__main__":
    main()