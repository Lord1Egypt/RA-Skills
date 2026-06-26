#!/usr/bin/env python3
"""
heartvoice ECG Analysis Skill
通过心之声 API 分析心电信号（单导联/十二导联），返回诊断 summary 及详细参数。
适用于 OpenClaw Agent 调用。

Usage:
    python3 scripts/call_api.py 1-lead  --json_path  ./data/ecg.json
    python3 scripts/call_api.py 12-lead --json_path  ./data/12lead.json

Environment:
    HEARTVOICE_API_KEY  — required API key
"""

import json
import os
import sys
import argparse
import requests


# ── API Endpoints ─────────────────────────────────────────────────────────────

API_1LEAD  = "https://api.heartvoice.com.cn/api/v1/basic/ecg/1-lead/analyze"
API_12LEAD = "https://api.heartvoice.com.cn/api/v1/basic/ecg/12-lead/analyze"

REQUIRED_1LEAD = {"ecgData", "ecgSampleRate", "adcGain", "adcZero"}

REQUIRED_12LEAD = {
    "dataI", "dataII", "dataIII",
    "dataAVR", "dataAVL", "dataAVF",
    "dataV1", "dataV2", "dataV3", "dataV4", "dataV5", "dataV6",
    "ecgSampleRate", "adcGain", "adcZero",
}


# ── Data loaders ──────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在 / File not found: {path}")
    if os.path.getsize(path) > 5 * 1024 * 1024:
        raise ValueError("JSON 文件过大，限制 5 MB / File too large (max 5 MB)")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_1lead_payload(data: dict) -> dict:
    missing = REQUIRED_1LEAD - set(data.keys())
    if missing:
        raise ValueError(f"JSON 缺少字段 / Missing fields: {sorted(missing)}")
    return {k: data[k] for k in REQUIRED_1LEAD}


def build_12lead_payload(data: dict) -> dict:
    missing = REQUIRED_12LEAD - set(data.keys())
    if missing:
        raise ValueError(f"JSON 缺少字段 / Missing fields: {sorted(missing)}")
    return {k: data[k] for k in REQUIRED_12LEAD}


# ── API caller ────────────────────────────────────────────────────────────────

def call_api(endpoint: str, payload: dict, api_key: str) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    error_code = str(result.get("errorCode", result.get("code", "0")))
    if error_code != "0":
        raise RuntimeError(f"API 错误 / API error: {result.get('msg', result.get('message', '未知错误'))}")
    return result.get("data", result)


# ── Result formatters ─────────────────────────────────────────────────────────

def _na(value) -> str:
    return str(value) if value is not None else "N/A"


def _build_1lead_summary_zh(data: dict, diagnosis: list, possible: list) -> str:
    diag_text = ("检测到：" + "，".join(diagnosis)) if diagnosis else "未检测到主要异常"
    if possible:
        diag_text += "；可能存在：" + "，".join(possible)
    return (
        f"{diag_text}。"
        f"平均心率 {_na(data.get('avgHr'))} 次/分钟，"
        f"QRS 宽度 {_na(data.get('avgQrs'))} 毫秒，"
        f"PR 间期 {_na(data.get('prInterval'))} 毫秒，"
        f"QT 间期 {_na(data.get('avgQt'))} 毫秒，"
        f"QTc {_na(data.get('avgQtc'))} 毫秒，"
        f"P 波宽度 {_na(data.get('avgP'))} 毫秒。"
        f"信号质量 {_na(data.get('sqGrade'))}。"
        f"房性早搏 {data.get('pacCount', 0)} 次，室性早搏 {data.get('pvcCount', 0)} 次。"
    )


def _build_1lead_summary_en(data: dict, diagnosis: list, possible: list) -> str:
    diag_text = ("Detected: " + ", ".join(diagnosis)) if diagnosis else "No major abnormalities detected"
    if possible:
        diag_text += "; Possible: " + ", ".join(possible)
    return (
        f"{diag_text}. "
        f"Avg heart rate {_na(data.get('avgHr'))} bpm, "
        f"QRS duration {_na(data.get('avgQrs'))} ms, "
        f"PR interval {_na(data.get('prInterval'))} ms, "
        f"QT interval {_na(data.get('avgQt'))} ms, "
        f"QTc {_na(data.get('avgQtc'))} ms, "
        f"P wave duration {_na(data.get('avgP'))} ms. "
        f"Signal quality {_na(data.get('sqGrade'))}. "
        f"PACs {data.get('pacCount', 0)}, PVCs {data.get('pvcCount', 0)}."
    )


def format_1lead_result(data: dict, lang: str = "zh") -> dict:
    diagnosis = data.get("diagnosis", [])
    possible = data.get("possibleDiags", [])

    if lang == "en":
        summary = _build_1lead_summary_en(data, diagnosis, possible)
    else:
        summary = _build_1lead_summary_zh(data, diagnosis, possible)

    return {
        "status": "success",
        "summary": summary,
        "diagnosis": diagnosis,
        "possible_diagnosis": possible,
        "is_abnormal": data.get("isAbnormal"),
        "is_reverse": data.get("isReverse"),
        "sq_grade": data.get("sqGrade"),
        "avg_hr": data.get("avgHr"),
        "pac_count": data.get("pacCount"),
        "pvc_count": data.get("pvcCount"),
        "avg_qrs": data.get("avgQrs"),
        "pr_interval": data.get("prInterval"),
        "avg_qt": data.get("avgQt"),
        "avg_p": data.get("avgP"),
        "avg_qtc": data.get("avgQtc"),
    }


def _build_12lead_summary_zh(data: dict, results: list, descriptions: list) -> str:
    diag_text = ("检测到：" + "，".join(results)) if results else "未检测到主要异常"
    parts = [
        f"{diag_text}。",
        f"心率 {_na(data.get('HR'))} 次/分钟，",
        f"QRS 宽度 {_na(data.get('QRS'))} 毫秒，",
        f"PR 间期 {_na(data.get('PR'))} 毫秒，",
        f"QT 间期 {_na(data.get('QT'))} 毫秒，",
        f"QTc {_na(data.get('QTc'))} 毫秒，",
        f"P 波宽度 {_na(data.get('P'))} 毫秒，",
        f"T 波宽度 {_na(data.get('T'))} 毫秒。",
    ]
    if data.get("riskLevel") is not None:
        risk = data["riskLevel"]
        parts.append(f"风险评估：{'正常' if risk == 0 else f'风险等级 {risk}'}。")
    if descriptions:
        parts.append("描述：" + "；".join(descriptions) + "。")
    return "".join(parts)


def _build_12lead_summary_en(data: dict, results: list, descriptions: list) -> str:
    diag_text = ("Detected: " + ", ".join(results)) if results else "No major abnormalities detected"
    parts = [
        f"{diag_text}. ",
        f"Heart rate {_na(data.get('HR'))} bpm, ",
        f"QRS duration {_na(data.get('QRS'))} ms, ",
        f"PR interval {_na(data.get('PR'))} ms, ",
        f"QT interval {_na(data.get('QT'))} ms, ",
        f"QTc {_na(data.get('QTc'))} ms, ",
        f"P wave {_na(data.get('P'))} ms, ",
        f"T wave {_na(data.get('T'))} ms. ",
    ]
    if data.get("riskLevel") is not None:
        risk = data["riskLevel"]
        parts.append(f"Risk assessment: {'normal' if risk == 0 else f'level {risk}'}. ")
    if descriptions:
        parts.append("Description: " + "; ".join(descriptions) + ".")
    return "".join(parts)


def format_12lead_result(data: dict, lang: str = "zh") -> dict:
    diagnoses = data.get("diagnoses", [])
    results = [d.get("result", d.get("label", "")) for d in diagnoses if d]
    descriptions = [d["description"] for d in diagnoses if d.get("description")]

    if lang == "en":
        summary = _build_12lead_summary_en(data, results, descriptions)
    else:
        summary = _build_12lead_summary_zh(data, results, descriptions)

    return {
        "status": "success",
        "analysis_state": data.get("analysisState", True),
        "summary": summary,
        "diagnoses": diagnoses,
        "diagnosis_results": results,
        "risk_level": data.get("riskLevel"),
        "HR": data.get("HR"),
        "atrial_rate": data.get("AtrialRate"),
        "ventricular_rate": data.get("VentricularRate"),
        "P": data.get("P"),
        "PR": data.get("PR"),
        "QRS": data.get("QRS"),
        "QT": data.get("QT"),
        "QTc": data.get("QTc"),
        "T": data.get("T"),
        "QRS_axis": data.get("QRSaxis"),
        "P_axis": data.get("Paxis"),
        "T_axis": data.get("Taxis"),
        "SV1": data.get("SV1"),
        "SV2": data.get("SV2"),
        "SV5": data.get("SV5"),
        "RV1": data.get("RV1"),
        "RV2": data.get("RV2"),
        "RV5": data.get("RV5"),
        "RV6": data.get("RV6"),
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="心之声 ECG 分析工具 / heartvoice ECG Analyzer"
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # 1-lead
    p1 = subparsers.add_parser("1-lead", help="单导联信号分析 / Single-lead signal analysis")
    p1.add_argument("--json_path", "-j", required=True, help="ECG JSON file path")
    p1.add_argument("--lang", "-l", choices=["zh", "en"], default="zh",
                    help="Output language: zh (Chinese, default) or en (English)")

    # 12-lead
    p12 = subparsers.add_parser("12-lead", help="十二导联信号分析 / 12-lead signal analysis")
    p12.add_argument("--json_path", "-j", required=True, help="ECG JSON file path")
    p12.add_argument("--lang", "-l", choices=["zh", "en"], default="zh",
                    help="Output language: zh (Chinese, default) or en (English)")

    args = parser.parse_args()

    api_key = os.environ.get("HEARTVOICE_API_KEY", "")
    if not api_key:
        msg = (
            "未检测到 HEARTVOICE_API_KEY。\n"
            "请前往 https://www.heartvoice.com.cn/aiCloud 注册并获取您的 API Key，\n"
            "然后将其配置到环境变量 HEARTVOICE_API_KEY 中。\n"
            "\n"
            "HEARTVOICE_API_KEY not found.\n"
            "Please visit https://www.heartvoice.com.cn/aiCloud to register and obtain your API Key,\n"
            "then set it as the environment variable HEARTVOICE_API_KEY."
        )
        print(json.dumps({"status": "error", "message": msg}, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        if args.mode == "1-lead":
            raw = load_json(args.json_path)
            payload = build_1lead_payload(raw)
            result_data = call_api(API_1LEAD, payload, api_key)
            output = format_1lead_result(result_data, lang=args.lang)

        elif args.mode == "12-lead":
            raw = load_json(args.json_path)
            payload = build_12lead_payload(raw)
            result_data = call_api(API_12LEAD, payload, api_key)
            output = format_12lead_result(result_data, lang=args.lang)

        else:
            parser.error(f"未知模式 / Unknown mode: {args.mode}")

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except requests.HTTPError as e:
        msg = f"HTTP {e.response.status_code}: {e.response.text}"
        print(json.dumps({"status": "error", "message": msg}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
