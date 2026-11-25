#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debug-pro 本地工具链（零依赖、纯标准库、不联网）。

三件事，且只做这三件事：
  1. triage      从日志/报错文本里抽出「可核验的故障要素」：错误类型、栈首帧、退出码、HTTP 状态、
                 时间戳、路径。输出分诊卡，让「我复现了」变成有据可查。
  2. envsnap     采集一份可粘贴的环境块（OS/解释器/关键依赖），并**强制脱敏**任何含 KEY/TOKEN/SECRET 的项。
                 用来终结「在我机器上能跑」。
  3. reprocheck  检查一份复现步骤是否具备最小五要素（版本环境 / 操作或命令 / 输入 / 期望 vs 实际 / 证据）。
                 缺哪条就指名，不靠感觉。

错误码：D001 文件不存在 · D002 编码不可读 · D003 内容为空 · D004 无错误特征（不是故障日志）

用法：
  python tools/debughunt.py triage --file demo/sample_error.log --out demo_out
  python tools/debughunt.py envsnap --json
  python tools/debughunt.py reprocheck --file demo/repro_steps.md
"""
import argparse
import json
import os
import platform
import re
import subprocess
import sys

ERROR_LINE = re.compile(r"(Traceback \(most recent call last\)|[A-Za-z_][A-Za-z0-9_.]*"
                        r"(?:Error|Exception)|ERROR|FATAL|错误|失败|异常)")
EXC_TYPE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*\.?)+: |([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)): ")
FRAME = re.compile(r'File "([^"]+)", line (\d+)(?:, in (\w+))?')
EXIT_CODE = re.compile(r"(?:exit\s*code|退出码|returned|status)\s*[:=]?\s*(-?\d+)", re.I)
HTTP_STATUS = re.compile(r"\b(?:HTTP/[\d.]+\s+)?(4\d\d|5\d\d)\b")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?")
PATH_HINT = re.compile(r"(?:[A-Za-z]:\\[^\s:]+|/[A-Za-z0-9_./-]+\.(?:py|js|ts|java|go|rs|log))")
PORT = re.compile(r":(\d{2,5})\b")
SECRET_KEY = re.compile(r"(KEY|TOKEN|SECRET|PASS|CRED|AUTH|COOKIE)", re.I)


def log(msg):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(msg)


def die(code, msg):
    log("[%s] %s" % (code, msg))
    sys.exit(1)


def read_text(path):
    if not os.path.isfile(path):
        die("D001", "文件不存在：%s" % path)
    raw = open(path, "rb").read()
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
        try:
            t = raw.decode(enc)
            break
        except UnicodeDecodeError:
            t = None
    if t is None:
        die("D002", "编码无法识别")
    if not t.strip():
        die("D003", "内容为空")
    return t


def triage(text):
    lines = text.splitlines()
    err_lines = [l for l in lines if ERROR_LINE.search(l)]
    frames = FRAME.findall(text)
    exc = []
    for l in lines:
        m = EXC_TYPE.match(l.strip())
        if m:
            exc.append(l.strip().split(":")[0])
    data = {
        "error_lines": len(err_lines),
        "first_error": (err_lines[0].strip()[:160] if err_lines else None),
        "exception_types": sorted(set(e for e in exc if e)),
        "frames": [{"file": f, "line": int(n), "func": fn or None} for f, n, fn in frames],
        "last_frame": ({"file": frames[-1][0], "line": int(frames[-1][1]),
                        "func": frames[-1][2] or None} if frames else None),
        "exit_codes": sorted(set(EXIT_CODE.findall(text))),
        "http_status": sorted(set(HTTP_STATUS.findall(text))),
        "timestamps": sorted(set(TIMESTAMP.findall(text)))[:5],
        "paths": sorted(set(PATH_HINT.findall(text)))[:8],
        "ports": sorted(set(PORT.findall(text)))[:5],
    }
    if not err_lines and not exc and not data["exit_codes"] and not data["http_status"]:
        die("D004", "未发现错误特征：这不像故障日志（无异常类型/错误行/退出码/HTTP 状态）")
    return data


def build_card(d):
    f = d["last_frame"]
    frame_txt = ("%s:%d%s" % (f["file"], f["line"], (" in " + f["func"]) if f["func"] else "")) if f else "原文未提及"
    return """# 分诊卡（自动抽取，判断由人做）

| 字段 | 值 |
|---|---|
| 错误类型 | %s |
| 首条错误行 | %s |
| 栈首帧（最后进入点） | `%s` |
| 退出码 | %s |
| HTTP/业务状态 | %s |
| 时间戳 | %s |
| 涉及路径 | %s |

## 下一步（按 7 步协议，任一步未过不得进下一步）
1. 复现：从上面「栈首帧」反向定位入口，构造最小操作序列。
2. 定位层：看错误类型判断是输入/逻辑/环境/依赖哪一层。
3. 假设：写 1–3 条可证伪假设，第 5 步一次只动一个变量。
""" % (
        "、".join(d["exception_types"]) or "原文未提及",
        d["first_error"] or "原文未提及",
        frame_txt,
        "、".join(d["exit_codes"]) or "原文未提及",
        "、".join(d["http_status"]) or "原文未提及",
        "、".join(d["timestamps"]) or "原文未提及",
        "、".join(d["paths"]) or "原文未提及",
    )


def envsnap():
    item = {
        "os": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "cwd": os.getcwd(),
        "path_entries": len(os.environ.get("PATH", "").split(os.pathsep)),
    }
    # 白名单采集 + 强制脱敏：任何含 KEY/TOKEN/SECRET 的键不入快照
    safe_env = {}
    for k, v in os.environ.items():
        if SECRET_KEY.search(k):
            continue
        if k in ("LANG", "LC_ALL", "SHELL", "TERM", "PYTHONPATH", "VIRTUAL_ENV", "CONDA_DEFAULT_ENV"):
            safe_env[k] = v if len(v) < 120 else v[:117] + "..."
    item["env_whitelist"] = safe_env
    item["redacted_keys_count"] = len([k for k in os.environ if SECRET_KEY.search(k)])
    try:
        item["git_rev"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                         capture_output=True, text=True, timeout=8).stdout.strip() or None
    except Exception:
        item["git_rev"] = None
    return item


CHECK_ITEMS = {
    # 环境必须给到「可对照的具体值」：版本号 / 系统名 / 依赖清单；
    # 只写「python app.py」这类命令不算环境声明（曾把 D08 误判为 PASS）。
    "版本环境": re.compile(r"(版本\s*[:：]?\s*[vV]?\d|version\s*[:：]?\s*[vV]?\d|"
                           r"[vV]\d+\.\d+|Windows|macOS|mac os|Linux|Ubuntu|CentOS|Debian|"
                           r"Python\s*3|Python\s*2|Node\s*[vV]?\d|JDK\s*\d|CUDA|"
                           r"requirements|依赖清单|pip freeze|npm ls)", re.I),
    "操作或命令": re.compile(r"(步骤|命令|运行|执行|点击|输入|run|python|npm|curl|操作)", re.I),
    "输入": re.compile(r"(输入|数据|文件|参数|样本|payload|input|fixture)", re.I),
    "期望与实际": re.compile(r"(期望|应该|预期|实际|结果|expected|actual|报错|返回)", re.I),
    "证据": re.compile(r"(日志|截图|堆栈|traceback|error|报错原文|复现率|链接)", re.I),
}


def reprocheck(text):
    missing = [k for k, pat in CHECK_ITEMS.items() if not pat.search(text)]
    return {"verdict": "PASS" if not missing else "FAIL", "missing": missing,
            "steps_detected": len(re.findall(r"^\s*\d+[.、)]", text, re.M))}


def main():
    ap = argparse.ArgumentParser(description="debug-pro 工具链（零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("triage", help="故障日志分诊")
    t.add_argument("--file", required=True)
    t.add_argument("--out", default=".")
    t.add_argument("--json", action="store_true")

    e = sub.add_parser("envsnap", help="环境快照（自动脱敏）")
    e.add_argument("--json", action="store_true")

    r = sub.add_parser("reprocheck", help="复现步骤五要素检查")
    r.add_argument("--file", required=True)
    r.add_argument("--json", action="store_true")

    a = ap.parse_args()
    as_json = getattr(a, "json", False)

    if a.cmd == "triage":
        text = read_text(a.file)
        d = triage(text)
        card = build_card(d)
        try:
            os.makedirs(a.out, exist_ok=True)
            stem = os.path.splitext(os.path.basename(a.file))[0]
            md = os.path.join(a.out, stem + ".triage.md")
            js = os.path.join(a.out, stem + ".facts.json")
            open(md, "w", encoding="utf-8").write(card)
            open(js, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
        except OSError as ex:
            die("D005", "输出目录不可写：%s" % ex)
        if as_json:
            log(json.dumps({"ok": True, "data": {"out_md": md, "out_json": js,
                                                 "exceptions": d["exception_types"]}},
                           ensure_ascii=False))
        else:
            log(card)
            log("分诊卡已写入：%s" % md)

    elif a.cmd == "envsnap":
        d = envsnap()
        if as_json:
            log(json.dumps({"ok": True, "data": d}, ensure_ascii=False))
        else:
            log("环境块（可直接粘贴进 issue）：")
            for k, v in d.items():
                if k != "env_whitelist":
                    log("  %-18s %s" % (k, v))
            for k, v in d["env_whitelist"].items():
                log("  %-18s %s" % (k, v))
            log("  已排除疑似密钥项：%d 个" % d["redacted_keys_count"])

    else:
        text = read_text(a.file)
        d = reprocheck(text)
        if as_json:
            log(json.dumps({"ok": True, "data": d}, ensure_ascii=False))
        else:
            log("复现步骤检查：%s（识别编号步骤 %d 条）" % (d["verdict"], d["steps_detected"]))
            for m in d["missing"]:
                log("  ✗ 缺要素：%s" % m)
        sys.exit(0 if d["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
