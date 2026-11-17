#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 环境变量审计器（零依赖 / 静态启发式 / JSON IR / 修复回执）
# HIGH：已知密钥前缀或疑似密钥字段被赋长字面量；MEDIUM：代码使用但 example 未声明。
import argparse, json, os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea", ".vscode"}
SRC_EXT = (".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs", ".sh")
EXAMPLES = (".env.example", ".env.sample", ".env.template")
PY_RE = re.compile(r"os\.environ\.get\(\s*[\'\"]([A-Za-z_]\w*)[\'\"]|os\.environ\[[\'\"]([A-Za-z_]\w*)[\'\"]\s*\]|os\.getenv\(\s*[\'\"]([A-Za-z_]\w*)[\'\"]")
JS_RE = re.compile(r"process\.env\.([A-Za-z_]\w*)|process\.env\[[\'\"]([A-Za-z_]\w*)[\'\"]\s*\]")
SH_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=", re.M)
SECRET_RE = re.compile(r"(?i)(api[_-]?key|apikey|token|secret|password|passwd|pwd|access[_-]?key|secret[_-]?key)\b\s*[:=]\s*[\'\"]([^\'\"]+)[\'\"]")
KEY_PREFIX = ("ghp_", "gho_", "github_pat_", "sk-", "AKIA", "xoxb-", "xoxp-", "AIza", "-----BEGIN")
PLACEHOLDER = ("your_", "xxx", "placeholder", "example", "changeme", "dummy", "<", "${", "test", "insert_")


def used_keys(text, fname, used):
    for m in PY_RE.finditer(text):
        k = m.group(1) or m.group(2) or m.group(3)
        if k:
            used.setdefault(k, fname)
    for m in JS_RE.finditer(text):
        used.setdefault(m.group(1) or m.group(2), fname)
    if fname.endswith(".sh"):
        for m in SH_RE.finditer(text):
            used.setdefault(m.group(1), fname)


def secret_scan(text, rel, findings):
    for i, line in enumerate(text.splitlines(), 1):
        for m in SECRET_RE.finditer(line):
            name, val = m.group(1), m.group(2)
            low = val.lower()
            is_prefix = any(val.startswith(p) for p in KEY_PREFIX)
            is_long = len(val) >= 12
            is_ph = any(p in low for p in PLACEHOLDER)
            if (is_prefix and not is_ph) or (is_long and not is_ph):
                findings.append({"severity": "HIGH", "code": "EVA_F_HARDCODED_SECRET",
                                 "subject": name, "evidence": "%s:%d 值长度 %d" % (rel, i, len(val)),
                                 "fixes": ["改为 os.environ / process.env 读取，值移入环境或密钥管理",
                                           "轮换该凭据（已入源码即视为泄露）"]})
                break


def main():
    ap = argparse.ArgumentParser(prog="env_var_audit", description="环境变量审计：使用清单 vs .env.example + 硬编码密钥扫描")
    ap.add_argument("root", nargs="?", default=".", help="项目根目录")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.root):
        print(json.dumps({"errors": [{"code": "EVA_E_NO_DIR", "subject": a.root,
                                      "evidence": "目录不存在", "fixes": ["传入正确的项目根目录"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    used, secrets = {}, []
    ex_keys = set()
    n_files = 0
    for dirpath, dirnames, filenames in os.walk(a.root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, a.root)
            if fn in EXAMPLES:
                try:
                    txt = open(fp, encoding="utf-8-sig", errors="replace").read()
                except Exception:
                    continue
                for line in txt.splitlines():
                    m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
                    if m:
                        ex_keys.add(m.group(1))
                continue
            if fn.endswith(SRC_EXT):
                n_files += 1
                try:
                    txt = open(fp, encoding="utf-8-sig", errors="replace").read()
                except Exception:
                    continue
                used_keys(txt, rel, used)
                secret_scan(txt, rel, secrets)
    if n_files == 0:
        print(json.dumps({"errors": [{"code": "EVA_E_NO_FILES", "subject": a.root,
                                      "evidence": "未发现可扫描的源码文件", "fixes": ["确认目录含 .py/.js/.ts/.sh 文件"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    undocumented = [{"severity": "MEDIUM", "code": "EVA_F_UNDOCUMENTED", "subject": k,
                     "evidence": "使用于 %s，example 未声明" % used[k],
                     "fixes": ["在 .env.example 补充 %s=<占位符> 及说明" % k]} for k in sorted(used) if k not in ex_keys]
    unused = sorted(ex_keys - set(used))
    high = [f for f in secrets if f["severity"] == "HIGH"]
    summary = {"src_files": n_files, "used": len(used), "example_keys": len(ex_keys),
               "high": len(high), "undocumented": len(undocumented), "unused_example": unused}
    if a.json:
        print(json.dumps({"summary": summary, "findings": high + undocumented}, ensure_ascii=False, indent=2))
    else:
        print("源码文件 %d · 代码读取环境变量 %d · .env.example 声明 %d" % (n_files, len(used), len(ex_keys)))
        for f in high:
            print("  硬编码疑密 HIGH：%s = ...（%s）" % (f["subject"], f["evidence"]))
        for u in undocumented:
            print("  未文档化 MEDIUM：%s（%s）" % (u["subject"], u["evidence"]))
        for k in unused:
            print("  example 冗余 LOW：%s（代码未读取）" % k)
        print("%s，rc=%d" % ("发现高危项" if high else "审计完成", 1 if high else 0))
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main()
