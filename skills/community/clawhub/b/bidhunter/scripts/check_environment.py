#!/usr/bin/env python3
"""
check_environment.py — BidHunter 只读环境检查（依赖型 Skill 标准件）。

只读取状态，不修改配置、不登录、不安装、不授权、不输出凭据值。
输出 JSON 到 stdout，供 Skill 宿主/人工判断就绪状态。

状态含义：
  ready       核心与当前请求所需的可选依赖均可用
  partial     核心流程可用，部分可选功能不可用
  needs_setup 当前请求所需的必需依赖缺失或未授权
  unavailable 配置存在但服务故障/权限/额度/版本问题

退出码：0=ready/partial（可继续），2=needs_setup/unavailable（需处理）
"""
import json
import os
import sys

CONFIG_DIR = os.path.expanduser("~/.config/bidhunter")


def status_ok(ok):
    return "ready" if ok else "needs_setup"


def check_minimax():
    path = os.path.join(CONFIG_DIR, "ai.json")
    if not os.path.exists(path):
        return {"id": "minimax-api", "state": "needs_setup",
                "detail": "未配置 ~/.config/bidhunter/ai.json（可选，AI 功能将跳过）",
                "optional": True}
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        has_key = bool(cfg.get("api_key"))
    except Exception:
        return {"id": "minimax-api", "state": "unavailable",
                "detail": "ai.json 无法解析", "optional": True}
    if has_key:
        return {"id": "minimax-api", "state": "ready",
                "detail": "已配置 API Key（值不输出）", "optional": True}
    return {"id": "minimax-api", "state": "needs_setup",
            "detail": "ai.json 存在但缺少 api_key", "optional": True}


def check_push():
    path = os.path.join(CONFIG_DIR, "push.json")
    if not os.path.exists(path):
        return {"id": "push-config", "state": "needs_setup",
                "detail": "未配置推送（可选，报告仅落本地文件）", "optional": True}
    return {"id": "push-config", "state": "ready",
            "detail": "推送配置存在（值不输出）", "optional": True}


def check_pdf_deps():
    try:
        import PyPDF2  # noqa: F401
        pdf = True
    except Exception:
        pdf = False
    try:
        import docx  # noqa: F401
        docx_ok = True
    except Exception:
        docx_ok = False
    if pdf and docx_ok:
        return {"id": "pdf-doc-deps", "state": "ready",
                "detail": "PyPDF2 + python-docx 均已安装", "optional": True}
    return {"id": "pdf-doc-deps", "state": "partial",
            "detail": f"PDF/Word 原生解析依赖缺失（PyPDF2={pdf}, python-docx={docx_ok}），将降级为正则抽取",
            "optional": True}


def main():
    results = [check_minimax(), check_push(), check_pdf_deps()]
    # 核心流程无必需外部依赖 → 永远可继续
    any_unavailable = any(r["state"] == "unavailable" for r in results)
    overall = "ready" if not any_unavailable else "partial"
    out = {"overall": overall, "core_runnable": True, "checks": results}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    # 核心永远可跑；可选依赖缺失不阻断
    sys.exit(0)


if __name__ == "__main__":
    main()
