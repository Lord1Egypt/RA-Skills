#!/usr/bin/env python3
"""
端到端测试：验证主入口 CLI 全流程（review / interview / all）与 4 个输出文件。
运行：python3 tests/test_e2e.py
"""

import json
import os
import shutil
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DIR = os.path.join(BASE_DIR, "..", "sample")
MAIN = os.path.join(BASE_DIR, "main.py")
RESUME_TXT = os.path.join(SAMPLE_DIR, "resume.txt")
JD_TXT = os.path.join(SAMPLE_DIR, "jd.txt")
TMP_OUT = os.path.join(BASE_DIR, "tests", "_tmp_out")


def run(name, cond, extra=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {extra}")
    return cond


def cli(*args):
    cmd = [sys.executable, MAIN] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    return proc.returncode, proc.stdout + proc.stderr


all_ok = True
shutil.rmtree(TMP_OUT, ignore_errors=True)
os.makedirs(TMP_OUT, exist_ok=True)

# 1. stage=all（文本免费模式）
code, out = cli(
    "--resume-text", open(RESUME_TXT, encoding="utf-8").read(),
    "--jd", JD_TXT,
    "--stage", "all",
    "-o", TMP_OUT,
)
ok = run("e2e all: 退出码 0", code == 0)
all_ok = all_ok and ok
for f in ["01_评分报告.md", "02_优化后简历.md", "03_评分结果.json", "04_模拟面试题.md"]:
    p = os.path.join(TMP_OUT, f)
    ok = run(f"e2e all: 生成 {f}", os.path.isfile(p))
    all_ok = all_ok and ok

if os.path.isfile(os.path.join(TMP_OUT, "01_评分报告.md")):
    report = open(os.path.join(TMP_OUT, "01_评分报告.md"), encoding="utf-8").read()
    all_ok = run("e2e all: 报告含综合评分", "综合评分" in report) and all_ok
    all_ok = run("e2e all: 报告含评分依据章节", "评分依据" in report) and all_ok
    all_ok = run("e2e all: 报告含 JD 拆解", ("JD" in report and "技能" in report)) and all_ok
if os.path.isfile(os.path.join(TMP_OUT, "04_模拟面试题.md")):
    qs = open(os.path.join(TMP_OUT, "04_模拟面试题.md"), encoding="utf-8").read()
    all_ok = run("e2e all: 面试题 ≥20 题", qs.count("**问题**") >= 20) and all_ok

# 2. stage=review + 优化指令
shutil.rmtree(TMP_OUT, ignore_errors=True)
os.makedirs(TMP_OUT, exist_ok=True)
code, out = cli(
    "--resume-text", open(RESUME_TXT, encoding="utf-8").read(),
    "--jd", JD_TXT,
    "--stage", "review",
    "--optimize-instruction", "突出实习经历，补充量化表达",
    "-o", TMP_OUT,
)
all_ok = run("e2e review: 退出码 0", code == 0) and all_ok
opt_p = os.path.join(TMP_OUT, "02_优化后简历.md")
if os.path.isfile(opt_p):
    opt = open(opt_p, encoding="utf-8").read()
    all_ok = run("e2e review: 优化稿含量化标注", "待补充量化数据" in opt) and all_ok
    all_ok = run("e2e review: 无 04 面试题文件", not os.path.isfile(os.path.join(TMP_OUT, "04_模拟面试题.md"))) and all_ok

# 3. 自定义维度配置
my_dims = os.path.join(TMP_OUT, "my_dimensions.json")
with open(my_dims, "w", encoding="utf-8") as f:
    json.dump({"dimensions": [
        {"id": "custom_1", "name": "自定义维度A", "weight": 100,
         "standard": "测试自定义维度",
         "rules": [{"type": "keyword_density", "keywords": ["PRD", "原型"], "target_hits": 2}]}
    ]}, f, ensure_ascii=False)
code, out = cli(
    "--resume-text", open(RESUME_TXT, encoding="utf-8").read(),
    "--jd", JD_TXT,
    "--dimensions", my_dims,
    "--stage", "review",
    "-o", TMP_OUT,
)
all_ok = run("e2e 自定义维度: 退出码 0", code == 0) and all_ok
if os.path.isfile(os.path.join(TMP_OUT, "01_评分报告.md")):
    rep = open(os.path.join(TMP_OUT, "01_评分报告.md"), encoding="utf-8").read()
    all_ok = run("e2e 自定义维度: 报告使用自定义维度", "自定义维度A" in rep) and all_ok

# 4. 非法输入（无简历）
code, out = cli("--jd", JD_TXT, "--stage", "all", "-o", TMP_OUT)
all_ok = run("e2e 缺简历参数: 非零退出", code != 0) and all_ok

shutil.rmtree(TMP_OUT, ignore_errors=True)
print()
print("ALL PASS" if all_ok else "SOME FAILED")
sys.exit(0 if all_ok else 1)
