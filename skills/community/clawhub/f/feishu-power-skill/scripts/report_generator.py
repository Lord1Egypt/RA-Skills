#!/usr/bin/env python3
"""
report_generator.py — 定时报告生成器
支持多种报告类型（审计/数据摘要/自定义模板），可通过 YAML 配置调度。
设计为 cron job 或 CLI 直接调用。

用法:
  # 从调度配置运行所有到期任务
  python3 report_generator.py run --schedule schedule.yaml

  # 运行指定任务
  python3 report_generator.py run --schedule schedule.yaml --job daily_audit

  # 列出所有任务
  python3 report_generator.py list --schedule schedule.yaml

  # 单次审计报告（不需要调度配置）
  python3 report_generator.py audit --demo --output report.md

  # 单次模板报告
  python3 report_generator.py template --app <token> --table <id> --template <path> --publish
"""

import argparse
import json
import os
import sys
import time
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# 添加脚本目录到 path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# 默认路径
CONFIGS_DIR = os.path.join(SCRIPT_DIR, "..", "configs")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "..", "templates")
STATE_FILE = os.path.join(SCRIPT_DIR, "..", ".report_state.json")

# 延迟导入缓存
_modules = {}


def _import(name: str):
    """按需导入模块，自动处理飞书凭证缺失的情况"""
    if name in _modules:
        return _modules[name]
    patched = False
    if not os.environ.get("FEISHU_APP_ID"):
        os.environ["FEISHU_APP_ID"] = "_placeholder_"
        os.environ["FEISHU_APP_SECRET"] = "_placeholder_"
        patched = True
    mod = __import__(name)
    _modules[name] = mod
    if patched:
        os.environ.pop("FEISHU_APP_ID", None)
        os.environ.pop("FEISHU_APP_SECRET", None)
    return mod


# ============================================================
# 调度状态管理
# ============================================================

def load_state() -> Dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: Dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def is_job_due(job: Dict, state: Dict) -> bool:
    """检查任务是否到期

    schedule 格式:
      frequency: daily | weekly | monthly | hourly
      time: "09:00"
      day_of_week: 1        # weekly: 周一=1 ... 周日=7
      day_of_month: 1       # monthly: 每月几号
      interval_hours: 4     # hourly: 间隔小时数
    """
    job_id = job["id"]
    schedule = job.get("schedule", {})
    freq = schedule.get("frequency", "daily")
    now = datetime.now()

    last_run_str = state.get(job_id, {}).get("last_run")
    last_run = datetime.fromisoformat(last_run_str) if last_run_str else None

    if freq == "hourly":
        interval = schedule.get("interval_hours", 1)
        if not last_run:
            return True
        return (now - last_run).total_seconds() >= interval * 3600

    if freq == "daily":
        h, m = map(int, schedule.get("time", "09:00").split(":"))
        if now < now.replace(hour=h, minute=m, second=0, microsecond=0):
            return False
        return not (last_run and last_run.date() == now.date())

    if freq == "weekly":
        dow = schedule.get("day_of_week", 1)
        if now.isoweekday() != dow:
            return False
        h, m = map(int, schedule.get("time", "09:00").split(":"))
        if now < now.replace(hour=h, minute=m, second=0, microsecond=0):
            return False
        return not (last_run and last_run.date() == now.date())

    if freq == "monthly":
        dom = schedule.get("day_of_month", 1)
        if now.day != dom:
            return False
        h, m = map(int, schedule.get("time", "09:00").split(":"))
        if now < now.replace(hour=h, minute=m, second=0, microsecond=0):
            return False
        return not (last_run and last_run.date() == now.date())

    return False


# ============================================================
# 报告执行器
# ============================================================

def run_audit_report(job: Dict) -> Dict:
    """执行审计报告

    params: app_token, sales_table, config, folder_token,
            publish(bool), output_local, use_demo(bool)
    """
    ra = _import("retail_audit")
    params = job.get("params", {})
    use_demo = params.get("use_demo", False)

    config_path = params.get("config")
    if config_path and not os.path.isabs(config_path):
        config_path = os.path.join(CONFIGS_DIR, config_path)
    cfg = ra.load_config(config_path)

    if use_demo:
        stores = ra.generate_demo_data(50)
        data_source = "Demo 模拟数据（50家门店）"
    else:
        api = _import("feishu_api")
        app_token = params["app_token"]
        sales_table = params["sales_table"]
        records = api.bitable_list_all_records(app_token, sales_table)
        stores = [r.get("fields", {}) for r in records]
        data_source = f"Bitable {app_token}/{sales_table}（{len(stores)} 家门店）"

    result = ra.run_audit(stores, config=cfg)
    md = ra.generate_report_markdown(result)

    output = {
        "type": "audit",
        "data_source": data_source,
        "summary": result["summary"],
        "store_count": result["total_stores"],
    }

    local_path = params.get("output_local")
    if local_path:
        os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(md)
        output["local_path"] = local_path

    if params.get("publish", False):
        doc_token = ra.publish_report_to_feishu(md, folder_token=params.get("folder_token"))
        output["doc_token"] = doc_token
        output["url"] = f"https://my.feishu.cn/docx/{doc_token}"

    return output


def run_template_report(job: Dict) -> Dict:
    """执行模板报告

    params: app_token, table_id, template, title, group_by,
            filter, folder_token, publish(bool), output_local, extra_context
    """
    dw = _import("doc_workflow")
    params = job.get("params", {})

    template_path = params["template"]
    if not os.path.isabs(template_path):
        template_path = os.path.join(TEMPLATES_DIR, template_path)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")

    app_token = params["app_token"]
    table_id = params["table_id"]
    output = {"type": "template", "template": template_path}

    if params.get("publish", False):
        result = dw.bitable_to_doc(
            app_token, table_id, template_path,
            title=params.get("title"),
            group_by=params.get("group_by"),
            filter_str=params.get("filter"),
            folder_token=params.get("folder_token"),
            output_local=params.get("output_local"),
            extra_context=params.get("extra_context"),
        )
        output.update(result)
    else:
        ctx = dw.build_context_from_bitable(
            app_token, table_id,
            group_by=params.get("group_by"),
            filter_str=params.get("filter"),
            extra=params.get("extra_context"),
        )
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        rendered = dw.render_template(template, ctx)

        local_path = params.get("output_local")
        if local_path:
            os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(rendered)
            output["local_path"] = local_path
        else:
            output["content"] = rendered

    return output


def run_custom_report(job: Dict) -> Dict:
    """执行自定义脚本报告

    params: script, args(list)
    """
    import subprocess
    params = job.get("params", {})
    script = params["script"]
    if not os.path.isabs(script):
        script = os.path.join(SCRIPT_DIR, script)

    cmd = [sys.executable, script] + params.get("args", [])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {
        "type": "custom",
        "script": script,
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:] if result.stdout else "",
        "stderr": result.stderr[-1000:] if result.stderr else "",
    }


REPORT_RUNNERS = {
    "audit": run_audit_report,
    "template": run_template_report,
    "custom": run_custom_report,
}


# ============================================================
# 调度引擎
# ============================================================

def load_schedule(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    jobs = data.get("jobs", [])
    for job in jobs:
        if "id" not in job:
            job["id"] = job.get("name", "unnamed").replace(" ", "_").lower()
    return jobs


def run_due_jobs(schedule_path: str, force_job: Optional[str] = None) -> List[Dict]:
    """运行所有到期任务（或 force_job 指定的单个任务）"""
    jobs = load_schedule(schedule_path)
    state = load_state()
    results = []

    for job in jobs:
        if not job.get("enabled", True):
            continue
        job_id = job["id"]
        if force_job and job_id != force_job:
            continue
        if not force_job and not is_job_due(job, state):
            continue

        runner = REPORT_RUNNERS.get(job.get("type", "audit"))
        if not runner:
            print(f"❌ 未知报告类型: {job.get('type')} (job: {job_id})", file=sys.stderr)
            continue

        print(f"▶ 执行任务: {job.get('name', job_id)} ({job.get('type', 'audit')})", flush=True)
        start = time.time()

        try:
            output = runner(job)
            elapsed = time.time() - start
            output.update({"job_id": job_id, "elapsed_seconds": round(elapsed, 1), "status": "success"})
            results.append(output)
            state[job_id] = {"last_run": datetime.now().isoformat(), "last_status": "success", "last_elapsed": round(elapsed, 1)}
            url = output.get("url", "")
            print(f"  ✅ 完成 ({elapsed:.1f}s){' → ' + url if url else ''}", flush=True)
        except Exception as e:
            elapsed = time.time() - start
            err = str(e)
            results.append({"job_id": job_id, "status": "error", "error": err, "elapsed_seconds": round(elapsed, 1)})
            state[job_id] = {"last_run": datetime.now().isoformat(), "last_status": "error", "last_error": err[:500]}
            print(f"  ❌ 失败: {err[:200]}", file=sys.stderr, flush=True)

    save_state(state)
    return results


def list_jobs(schedule_path: str):
    jobs = load_schedule(schedule_path)
    state = load_state()
    print(f"配置: {schedule_path}")
    print(f"任务数量: {len(jobs)}\n")
    for job in jobs:
        job_id = job["id"]
        enabled = "✅" if job.get("enabled", True) else "⏸️"
        schedule = job.get("schedule", {})
        job_state = state.get(job_id, {})
        due = " 📌 到期" if is_job_due(job, state) else ""
        print(f"  {enabled} {job.get('name', job_id)}")
        print(f"     ID: {job_id} | 类型: {job.get('type', 'audit')} | 频率: {schedule.get('frequency', 'daily')} {schedule.get('time', '')}")
        print(f"     上次: {job_state.get('last_run', '从未运行')} ({job_state.get('last_status', '-')}){due}\n")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="定时报告生成器")
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="运行调度任务")
    p_run.add_argument("--schedule", required=True, help="调度配置文件 (YAML)")
    p_run.add_argument("--job", help="只运行指定任务 ID")
    p_run.add_argument("--json", action="store_true", help="JSON 格式输出")

    p_list = sub.add_parser("list", help="列出所有任务")
    p_list.add_argument("--schedule", required=True, help="调度配置文件 (YAML)")

    p_audit = sub.add_parser("audit", help="单次审计报告")
    p_audit.add_argument("--app", help="Bitable app token")
    p_audit.add_argument("--table", help="销售数据表 ID")
    p_audit.add_argument("--config", help="审计规则配置文件")
    p_audit.add_argument("--publish", action="store_true", help="发布到飞书")
    p_audit.add_argument("--folder", help="飞书文件夹 token")
    p_audit.add_argument("--output", help="本地保存路径")
    p_audit.add_argument("--demo", action="store_true", help="使用模拟数据")

    p_tpl = sub.add_parser("template", help="单次模板报告")
    p_tpl.add_argument("--app", required=True, help="Bitable app token")
    p_tpl.add_argument("--table", required=True, help="数据表 ID")
    p_tpl.add_argument("--template", required=True, help="模板文件路径")
    p_tpl.add_argument("--title", help="文档标题")
    p_tpl.add_argument("--group-by", help="分组字段")
    p_tpl.add_argument("--filter", help="过滤条件")
    p_tpl.add_argument("--publish", action="store_true", help="发布到飞书")
    p_tpl.add_argument("--folder", help="飞书文件夹 token")
    p_tpl.add_argument("--output", help="本地保存路径")

    sub.add_parser("status", help="查看运行状态")

    args = parser.parse_args()

    if args.command == "run":
        results = run_due_jobs(args.schedule, force_job=args.job)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        elif not results:
            print("没有到期任务需要执行。")

    elif args.command == "list":
        list_jobs(args.schedule)

    elif args.command == "audit":
        job = {"id": "cli_audit", "type": "audit", "params": {
            "use_demo": args.demo, "publish": args.publish,
            "output_local": args.output, "folder_token": args.folder, "config": args.config,
        }}
        if args.app:
            job["params"]["app_token"] = args.app
        if args.table:
            job["params"]["sales_table"] = args.table
        print(json.dumps(run_audit_report(job), ensure_ascii=False, indent=2))

    elif args.command == "template":
        job = {"id": "cli_template", "type": "template", "params": {
            "app_token": args.app, "table_id": args.table, "template": args.template,
            "title": args.title, "group_by": args.group_by, "filter": args.filter,
            "publish": args.publish, "folder_token": args.folder, "output_local": args.output,
        }}
        print(json.dumps(run_template_report(job), ensure_ascii=False, indent=2))

    elif args.command == "status":
        state = load_state()
        if not state:
            print("暂无运行记录。")
        else:
            print("运行状态:")
            for job_id, info in sorted(state.items()):
                emoji = "✅" if info.get("last_status") == "success" else "❌"
                print(f"  {emoji} {job_id}")
                print(f"     上次运行: {info.get('last_run', '-')}")
                if info.get("last_error"):
                    print(f"     错误: {info['last_error'][:100]}")
                print()


if __name__ == "__main__":
    main()
