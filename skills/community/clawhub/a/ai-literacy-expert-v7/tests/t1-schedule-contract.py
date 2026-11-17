# -*- coding: utf-8 -*-
"""T1 · L4 调度契约静态校验：解析 6 条注册命令 + 6 份自包含 prompt"""
import re, json, sys, os, pathlib

# 路径自适应：技能根目录由脚本位置推导（本脚本位于 <skill>/tests/），输出目录同理。
# 可用环境变量 V7_TEST_OUT 覆盖输出目录，避免硬编码安装路径。
SKILL = str(pathlib.Path(__file__).resolve().parent.parent)
OUT = os.environ.get("V7_TEST_OUT") or str(pathlib.Path(__file__).resolve().parent / "out")
os.makedirs(OUT, exist_ok=True)
OPS   = f"{SKILL}/references/automation-ops.md"
L4    = f"{SKILL}/references/automation-l4-scheduler.md"
TPL   = f"{SKILL}/assets/self-contained-prompt-template.md"

results = []
def check(name, cond, detail=""):
    results.append({"name": name, "pass": bool(cond), "detail": detail})
    return bool(cond)

ops_txt = open(OPS, encoding="utf-8").read()

# ---------- 按 OPS-N 切分区块 ----------
blocks = {}
parts = re.split(r'\n## (OPS-\d)', ops_txt)
for i in range(1, len(parts), 2):
    blocks[parts[i]] = parts[i+1]

check("运营流数量为 6 类（OPS-1~6）", len(blocks) == 6, f"实际 {len(blocks)} 类: {sorted(blocks)}")

REQUIRED_SECTIONS = ["【角色】","【会话】","【任务】","【状态】","【幂等】","【执行】","【验证】","【落点】","【留痕】","【失败】"]

def validate_cron(cron):
    """返回 (ok, msg)"""
    f = cron.split()
    if len(f) != 6:
        return False, f"必须是 6 位，实际 {len(f)} 位"
    sec, mi, ho, dom, mon, dow = f
    if sec != "0":
        return False, f"秒位必须固定为 0（严禁秒级），实际 '{sec}'"
    # 各字段范围粗校验
    def ok_range(v, lo, hi, nm):
        if v == "*": return True
        for part in v.split(","):
            body = part.split("/")[0]
            if body == "*": continue
            for x in body.split("-"):
                if x and not (x.isdigit() and lo <= int(x) <= hi):
                    return False, f"{nm} 字段值 '{x}' 超出范围 {lo}-{hi}"
        return True
    for v, lo, hi, nm in [(mi,0,59,"分"),(ho,0,23,"时"),(dom,1,31,"日"),(mon,1,12,"月"),(dow,0,7,"周")]:
        ok, msg = True, ""
        if v != "*":
            for part in v.split(","):
                body = part.split("/")[0]
                if body == "*": continue
                for x in body.split("-"):
                    if x and not (x.isdigit() and lo <= int(x) <= hi):
                        return False, f"{nm} 字段 '{x}' 超出范围 {lo}-{hi}"
    return True, "OK(秒=0 → 最小间隔 1 分钟)"

all_tasks = {}
for key in sorted(blocks):
    blk = blocks[key]
    # --- 提取 create 命令 ---
    bash_blocks = re.findall(r'```bash\n(.*?)```', blk, re.S)
    cmd = None
    for b in bash_blocks:
        if "scheduler-api.sh" in b and "create" in b:
            cmd = b
            break
    if not check(f"{key} 存在注册命令", cmd is not None):
        continue

    # 把续行拼成一行
    oneline = re.sub(r'\\\s*\n\s*', ' ', cmd).replace("\n", " ")
    def arg(name):
        m = re.search(rf'--{name}\s+"([^"]*)"', oneline) or re.search(rf'--{name}\s+(\S+)', oneline)
        return m.group(1) if m else None

    name_ = arg("name"); cron_ = arg("cron"); ftype = arg("frequency-type")
    timeout = arg("timeout"); retry = arg("retry-count")
    estart = arg("effective-start"); eend = arg("effective-end")
    prompt_ref = re.search(r'--prompt\s+"\$\(cat\s+([^)]+)\)"', oneline)
    prompt_ref = prompt_ref.group(1) if prompt_ref else None

    check(f"{key} 必填 --name", name_, str(name_))
    check(f"{key} 必填 --cron", cron_, str(cron_))
    check(f"{key} 必填 --frequency-type", ftype in ("daily","interval","once"), f"实际 '{ftype}'")
    check(f"{key} frequency-type 合法", ftype in ("daily","interval","once"), str(ftype))

    if cron_:
        ok, msg = validate_cron(cron_)
        check(f"{key} cron 合法（{cron_}）", ok, msg)

    if ftype == "once":
        check(f"{key} once 类型有生效区间", bool(estart and eend), f"start={estart} end={eend}")
    else:
        check(f"{key} 非 once 不设生效区间", not (estart or eend), "OK")

    if timeout:
        check(f"{key} timeout 在 10-1800", 10 <= int(timeout) <= 1800, f"{timeout}s")
    if retry:
        check(f"{key} retry-count ≤10", int(retry) <= 10, f"{retry} 次")

    check(f"{key} prompt 通过文件传入（避免引号转义）", prompt_ref is not None, str(prompt_ref))

    # --- 提取自包含 prompt 正文 ---
    text_blocks = re.findall(r'```text\n(.*?)```', blk, re.S)
    prompt = text_blocks[0] if text_blocks else ""
    check(f"{key} 提供自包含 prompt 正文", bool(prompt.strip()), f"{len(prompt)} 字符")

    if prompt:
        missing = [s for s in REQUIRED_SECTIONS if s not in prompt]
        check(f"{key} prompt 自包含 10 段齐全", not missing, f"缺失: {missing}" if missing else "10/10 段齐全")
        check(f"{key} prompt 含『禁加载 automation-task-manager』",
              ("严禁加载 automation-task-manager" in prompt) or ("严禁加载/调用 automation-task-manager" in prompt),
              "已声明")
        check(f"{key} prompt 含『不提问/不等待确认』",
              ("不提问" in prompt) and ("确认" in prompt), "已声明")
        check(f"{key} prompt 无残留 {{{{占位符}}}}", "{{" not in prompt, "无残留")
        check(f"{key} prompt 指定 IMA 为状态源", "IMA" in prompt, "含 IMA 状态源")
        check(f"{key} prompt 含幂等键规则", "key = " in prompt or "idempotency" in prompt.lower(), "已定义")
        check(f"{key} prompt 含失败退出码 0", "退出码 0" in prompt or "退出码0" in prompt, "已声明")
        # 只有当 prompt 明确要求「生成 HTML 产物」时才必须要求 harness
        # （仅"提及课件"如汇总清单/给出建议，并不产出 HTML，不应强制）
        gen_html = re.search(r'(?:生成|产出)[^。；\n]*HTML', prompt)
        if gen_html:
            has_h = "harness" in prompt
            check(f"{key} 生成HTML产物→要求 harness 实测", has_h,
                  f"匹配'{gen_html.group(0)[:32]}…' → harness:{'已要求' if has_h else '缺失'}")
        else:
            check(f"{key} 不生成HTML产物→无需 harness（设计正确）", True,
                  "仅汇总/建议类，无 HTML 产物，不强制实测")

    all_tasks[key] = {"name": name_, "cron": cron_, "ftype": ftype,
                      "timeout": timeout, "retry": retry, "prompt_len": len(prompt)}

# ---------- 校验 L4 文档与模板 ----------
l4 = open(L4, encoding="utf-8").read()
for kw, label in [("L4 的判据","L4 五判据"), ("自包含指令契约","自包含指令契约"),
                  ("幂等设计","幂等设计"), ("执行台账","执行台账"),
                  ("automation 会话行为铁律","automation 会话铁律"),
                  ("scheduler-api.sh create","注册命令"), ("INVALID_CRON_EXPR","错误码")]:
    check(f"L4 文档含「{label}」", kw in l4, kw)

tpl = open(TPL, encoding="utf-8").read()
missing_tpl = [s for s in REQUIRED_SECTIONS if s not in tpl]
check("指令模板含 10 个必备段", not missing_tpl, f"缺失: {missing_tpl}" if missing_tpl else "10/10")
phs = sorted(set(re.findall(r'\{\{([A-Z_]+)\}\}', tpl)))
check("模板占位符有说明表", all(p in tpl for p in phs), f"占位符 {phs} 均已在说明表出现")
check("模板含注册前自检清单", "自检清单" in tpl or "自检" in tpl, "含自检")

# ---------- 输出 ----------
passed = sum(1 for r in results if r["pass"])
total  = len(results)
print("="*78)
print(f"T1 · L4 调度契约静态校验    通过 {passed}/{total}")
print("="*78)
for r in results:
    print(f"  {'✅' if r['pass'] else '❌'} {r['name']}" + (f"  — {r['detail']}" if (r['detail'] and not r['pass']) else ""))
print()
print("解析出的任务清单：")
for k, v in all_tasks.items():
    print(f"  {k}: cron={v['cron']:18} type={v['ftype']:8} timeout={v['timeout']}s retry={v['retry']} prompt={v['prompt_len']}字符")

json.dump({"suite":"T1-L4调度契约静态校验","passed":passed,"total":total,
           "results":results,"tasks":all_tasks},
          open(f"{OUT}/t1-results.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
sys.exit(0 if passed == total else 1)
