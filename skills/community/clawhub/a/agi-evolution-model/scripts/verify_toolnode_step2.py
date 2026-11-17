#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2 验收脚本：toolnode 接入 PerceptionNode 治理层后的 Q1-Q6 质量门禁实测。

不依赖人工读码，直接跑真实调用并断言：
- Q1 真实接线：toolnode 走真实能力层（非桩），返回真实系统数据
- Q2 参数 schema + 校验：缺参/未知操作被拦截为 INVALID_PARAMS
- Q3 trace_id 全链路：call_tool 链路 trace_id 一致；toolnode 尊重注入的 trace_id
- Q4 防静默失败：fs.write 回读磁盘验证；fs.read 返回来源时间戳
- Q5 重试 + 兜底：确定性错误（COMMAND_TIMEOUT）不重试、立即返回
- Q6 错误→智慧库：真实工具失败自动写入 error_wisdom

退出码 0 = 全部通过；非 0 = 有失败项。
"""
import os
import sys
import json
import subprocess
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from perception_node import PerceptionNode

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f"  -- {detail}" if detail else ""))


def wisdom_count(memory_dir):
    p = os.path.join(memory_dir, "error_wisdom", "error_wisdom_entries.json")
    if not os.path.isfile(p):
        return 0
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data.get("entries", {}))
    except Exception:
        return -1


def main():
    tmp = tempfile.mkdtemp(prefix="pn_step2_")
    node = PerceptionNode(memory_dir=tmp)
    print(f"PerceptionNode ready (c_ext={node.c_ext_available}, memory_dir={tmp})")
    print("-" * 64)

    # ---------- Q1 真实接线 ----------
    r = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    data = r.get("data") or {}
    q1_ok = (
        r.get("success") is True
        and isinstance(data, dict)
        and "mem" in data and "cpu" in data and "disk" in data
    )
    check("Q1 真实接线 toolnode(sys.all)", q1_ok,
          f"success={r.get('success')} data_keys={sorted(data.keys())}")

    rs = node.call_tool("web_search", {"query": "x"})
    q1c = rs.get("error", {}).get("code") == "STUB_NOT_IMPLEMENTED"
    check("Q1 对照: 桩工具 web_search 被治理层拦截", q1c,
          f"code={rs.get('error', {}).get('code')}")

    # ---------- Q2 参数 schema + 校验 ----------
    r2a = node.call_tool("toolnode", {"group": "sys"})  # 缺 op
    r2b = node.call_tool("toolnode", {"group": "sys", "op": "nope"})  # 未知 op
    q2_ok = (
        r2a.get("error", {}).get("code") == "INVALID_PARAMS"
        and r2b.get("error", {}).get("code") == "INVALID_PARAMS"
    )
    check("Q2 参数校验 (缺 op / 未知 op)", q2_ok,
          f"missing_op={r2a.get('error', {}).get('code')} unknown_op={r2b.get('error', {}).get('code')}")

    # ---------- Q3 trace_id 全链路 ----------
    r3 = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    tid_top = r3.get("trace_id")
    tid_meta = (r3.get("metadata") or {}).get("trace_id")
    q3a = bool(tid_top) and tid_top == tid_meta and str(tid_top).startswith("trace_")
    check("Q3a call_tool 链路 trace_id 一致且非空", q3a, f"trace_id={tid_top}")

    # toolnode 尊重注入的 trace_id（直接 subprocess 验证能力层；优先二进制，回退 Python）
    inj = "trace_INJECTED_Q3_TEST"
    ext = ".exe" if os.name == "nt" else ""
    bin_path = os.path.join(HERE, "toolnode" + ext)
    if not os.path.exists(bin_path):
        bin_path = os.path.join(HERE, "toolnode.py")
    if bin_path.endswith(".py"):
        inj_cmd = [sys.executable, bin_path, "sys", "all", "--params", "{}", "--trace-id", inj]
    else:
        inj_cmd = [bin_path, "sys", "all", "--params", "{}", "--trace-id", inj]
    out = subprocess.run(inj_cmd, capture_output=True, timeout=60)
    try:
        inj_res = json.loads(out.stdout.decode("utf-8", errors="replace"))
        q3b = inj_res.get("trace_id") == inj
    except Exception:
        q3b = False
    check("Q3b toolnode 尊重调用方注入的 trace_id", q3b, f"injected={inj} echoed={inj_res.get('trace_id') if q3b else 'PARSE_FAIL'}")

    # ---------- Q4 防静默失败 ----------
    tf = os.path.join(tmp, "q4.txt")
    w = node.call_tool("toolnode", {"group": "fs", "op": "write", "path": tf, "content": "hello 中文OK\n"})
    wd = w.get("data") or {}
    q4a = (
        w.get("success") is True
        and wd.get("verified_on_disk") is True
        and bool(wd.get("sha256"))
        and (wd.get("bytes_written") or 0) > 0
    )
    check("Q4a fs.write 回读磁盘验证(防静默失败)", q4a,
          f"verified={wd.get('verified_on_disk')} sha256?={bool(wd.get('sha256'))} bytes={wd.get('bytes_written')}")

    EXPECTED = "hello 中文OK\n"
    rd = node.call_tool("toolnode", {"group": "fs", "op": "read", "path": tf})
    rdd = rd.get("data") or {}
    q4b = (
        rd.get("success") is True
        and bool(rdd.get("source_timestamp"))
        and rdd.get("content") == EXPECTED
    )
    check("Q4b fs.read 返回来源时间戳且内容一致", q4b,
          f"source_timestamp={rdd.get('source_timestamp')} content_match={rdd.get('content') == EXPECTED}")

    # ---------- Q5 确定性错误不重试 ----------
    t0 = time.time()
    r5 = node.call_tool(
        "toolnode",
        {"group": "exec", "op": "run", "command": "ping -n 3 127.0.0.1", "timeout": 1})
    dt = time.time() - t0
    q5_ok = (
        r5.get("success") is False
        and r5.get("error", {}).get("code") == "COMMAND_TIMEOUT"
        and "retry_count" not in r5
    )
    check("Q5 确定性错误不重试(COMMAND_TIMEOUT)", q5_ok,
          f"code={r5.get('error', {}).get('code')} retry_count_present={'retry_count' in r5} elapsed={dt:.2f}s")

    # ---------- Q6 错误→智慧库 ----------
    before = wisdom_count(tmp)
    # 触发一次真实工具失败（COMMAND_TIMEOUT 非客户端错误，应入智慧库）
    node.call_tool(
        "toolnode",
        {"group": "exec", "op": "run", "command": "ping -n 3 127.0.0.1", "timeout": 1})
    after = wisdom_count(tmp)
    q6_ok = after > before
    check("Q6 真实工具失败自动入错误智慧库", q6_ok, f"before={before} after={after}")

    # ---------- 附加：危险命令网关贯穿全链路 ----------
    rd2 = node.call_tool(
        "toolnode",
        {"group": "exec", "op": "run", "command": "sudo rm -rf /important"})
    code = rd2.get("error", {}).get("code")
    qx = code in ("DANGEROUS_COMMAND_BLOCKED", "PREVENTION_CHECK_FAILED")
    check("Q+ 危险命令在全链路被拦截(未执行)", qx, f"code={code}")

    # ---------- 汇总 ----------
    print("-" * 64)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"Step 2 门禁结果: {passed}/{total} 通过")
    failed = [n for n, ok, _ in results if not ok]
    if failed:
        print("未通过: " + ", ".join(failed))
    else:
        print("全部通过 ✅ 可进入 Step 3 (Rust 化)")

    # 清理临时目录
    try:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
