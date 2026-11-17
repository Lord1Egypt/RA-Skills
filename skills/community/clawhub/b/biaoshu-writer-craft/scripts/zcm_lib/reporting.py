"""Result presentation and report rendering helpers."""
import importlib.util
import json
import os
import sys
from pathlib import Path


_RISK_ZH = {"high": "高风险", "review": "待复核", "tip": "提示"}
_PRIORITY_ZH = {"high": "高", "medium": "中", "low": "低"}
_ENUM_ZH = {"risk_level": _RISK_ZH, "priority": _PRIORITY_ZH}


def zh_risk(obj):
    """Recursively translate common result enum values for display."""
    if isinstance(obj, dict):
        out = {}
        for key, value in obj.items():
            mapping = _ENUM_ZH.get(key)
            if mapping and isinstance(value, str) and value in mapping:
                out[key] = mapping[value]
            else:
                out[key] = zh_risk(value)
        return out
    if isinstance(obj, list):
        return [zh_risk(item) for item in obj]
    return obj


def platform_reminder(log_fn):
    log_fn("📎 结果同步在百炼®标书平台查看：https://biaoshu.zhiliaobiaoxun.com/")


def report_balance(request_json_fn, log_fn):
    """Report remaining words after a completed task; never fail the task."""
    try:
        data = request_json_fn("GET", "/me")
        balance = data.get("available_words", data.get("wallet_balance"))
    except BaseException:
        return
    if balance is not None:
        log_fn(f"💰 当前可用字数：{balance}")


def _import_report_module():
    try:
        import report as _report
        return _report
    except ModuleNotFoundError as exc:
        if exc.name != "report":
            raise
    scripts_dir = Path(__file__).resolve().parents[1]
    report_path = scripts_dir / "report.py"
    spec = importlib.util.spec_from_file_location("report", report_path)
    module = importlib.util.module_from_spec(spec)
    old_path = list(sys.path)
    sys.path.insert(0, str(scripts_dir))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = old_path
    return module


def maybe_report(result_response, fmt, label, *, tender_name=None,
                 output_dir_fn, log_fn, platform_reminder_fn):
    """Render optional HTML/Word reports for interpretation, compliance, duplicate."""
    if not fmt:
        return
    _report = _import_report_module()

    out_dir = output_dir_fn()
    try:
        outputs = _report.generate(result_response, fmt=fmt, out_dir=out_dir, tender_name=tender_name)
    except Exception as exc:
        log_fn(f"⚠️ 报告生成失败：{exc}")
        return
    for path in outputs:
        log_fn(f"已生成{label}报告：{os.path.abspath(path)}")
    log_fn(f"报告所在目录：{os.path.abspath(out_dir)}")
    platform_reminder_fn()


def cmd_report(args, *, request_json_fn, recall_tender_fn, output_dir_fn,
               log_fn, platform_reminder_fn, print_fn=print):
    _report = _import_report_module()

    if args.in_file:
        with open(args.in_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    else:
        data = request_json_fn("GET", f"/jobs/{args.job}/result")

    tender = args.name
    if not tender:
        result = data.get("result") if isinstance(data, dict) else {}
        result = result if isinstance(result, dict) else {}
        project_id = result.get("project_id") or (result.get("compliance") or {}).get("document_id") or result.get("document_id")
        tender = recall_tender_fn(job_id=args.job, project_id=project_id)

    out_dir = args.out_dir or output_dir_fn()
    outputs = _report.generate(
        data,
        service=args.service,
        fmt=args.format,
        out_dir=out_dir,
        basename=args.basename,
        tender_name=tender,
    )
    for path in outputs:
        log_fn(f"已生成报告：{os.path.abspath(path)}")
        print_fn(os.path.abspath(path))
    log_fn(f"报告所在目录：{os.path.abspath(out_dir)}")
    platform_reminder_fn()
