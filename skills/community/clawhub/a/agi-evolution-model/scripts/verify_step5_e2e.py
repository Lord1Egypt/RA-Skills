#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 5 端到端验收：工具节点三层架构（Rust 能力层 + Python 治理层 + BusyBox 保命层）Q1–Q8 终检。

整合步骤 1–4 的全部质量维度，经真实 Rust 二进制主路径 + BusyBox 兜底路径，产出最终验收报告：
- Q1 真实接线（无生产桩）
- Q2 参数 Schema + 前置校验
- Q3 trace_id 全链路贯穿（含调用方注入）
- Q4 调用后验证（防静默失败：写入回读 + 来源时间戳）
- Q5 重试 / 兜底真实生效（确定性错误不重试 + BusyBox fallback）
- Q6 错误闭环进智慧库
- Q7 可观测性可验证（成功/失败/重试埋点可导出）
- Q8 跨平台一致（双二进制存在 + 活跃平台通过）
- Q+ 危险命令网关全链路拦截

退出码 0 = 全部通过；非 0 = 有失败项。
"""
import os
import sys
import json
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from perception_node import PerceptionNode
import perception_node as pn

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
            return len(json.load(f).get("entries", {}))
    except Exception:
        return -1


def main():
    tmp = tempfile.mkdtemp(prefix="pn_step5_")
    node = PerceptionNode(memory_dir=tmp)
    print(f"PerceptionNode ready (c_ext={node.c_ext_available}, memory_dir={tmp})")
    print("=" * 70)
    print("Step 5 端到端 Q1–Q8 验收（主路径 = Rust 二进制）")
    print("=" * 70)

    # ---------- Q1 真实接线 ----------
    r = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    data = r.get("data") or {}
    check("Q1 真实接线 toolnode(sys.all)",
          r.get("success") is True and {"cpu", "mem", "disk", "platform"}.issubset(set(data.keys())),
          f"data_keys={sorted(data.keys())}")
    r2 = node.call_tool("web_search", {"query": "x"})
    check("Q1 对照: 桩工具被治理层拦截",
          (r2.get("error") or {}).get("code") == "STUB_NOT_IMPLEMENTED",
          f"code={(r2.get('error') or {}).get('code')}")

    # ---------- Q2 参数校验 ----------
    r = node.call_tool("toolnode", {"group": "fs"})  # 缺 op
    c1 = (r.get("error") or {}).get("code")
    r = node.call_tool("toolnode", {"group": "fs", "op": "nope", "path": "."})  # 未知 op
    c2 = (r.get("error") or {}).get("code")
    check("Q2 参数校验 (缺 op / 未知 op)", c1 == "INVALID_PARAMS" and c2 == "INVALID_PARAMS",
          f"missing_op={c1} unknown_op={c2}")

    # ---------- Q3 trace_id 全链路 ----------
    r = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    tid = r.get("trace_id")
    check("Q3a call_tool 链路 trace_id 一致且非空", bool(tid) and tid == (r.get("metadata") or {}).get("trace_id"),
          f"trace_id={tid}")
    # Q3b: 直接调能力层验证注入透传（Rust 二进制）
    bin_path, is_rust = node._toolnode_binary_path()
    injected = "trace_INJECTED_Q3_E2E"
    import subprocess
    if bin_path:
        cmd = ([bin_path, "sys", "all", "--params", "{}", "--trace-id", injected]
               if is_rust else [sys.executable, bin_path, "sys", "all", "--params", "{}", "--trace-id", injected])
        out = subprocess.run(cmd, capture_output=True, timeout=60).stdout.decode("utf-8", errors="replace")
        try:
            echoed = json.loads(out).get("trace_id")
        except Exception:
            echoed = None
        check("Q3b 能力层尊重调用方注入的 trace_id", echoed == injected,
              f"injected={injected} echoed={echoed} backend={'rust' if is_rust else 'python'}")
    else:
        check("Q3b 能力层尊重调用方注入的 trace_id", False, "no capability binary")

    # ---------- Q4 防静默失败 ----------
    wf = os.path.join(tmp, "q4.txt")
    r = node.call_tool("toolnode", {"group": "fs", "op": "write", "path": wf, "content": "Q4中文探针\nline2"})
    d = r.get("data") or {}
    import hashlib
    expect_sha = hashlib.sha256("Q4中文探针\nline2".encode("utf-8")).hexdigest()
    check("Q4a fs.write 回读磁盘验证", r.get("success") and d.get("verified_on_disk") is True
          and d.get("sha256") == expect_sha, f"verified={d.get('verified_on_disk')} sha_match={d.get('sha256')==expect_sha}")
    r = node.call_tool("toolnode", {"group": "fs", "op": "read", "path": wf})
    d = r.get("data") or {}
    check("Q4b fs.read 来源时间戳且内容一致", r.get("success") and d.get("source_timestamp")
          and d.get("content") == "Q4中文探针\nline2", f"src_ts={d.get('source_timestamp')}")

    # ---------- Q5 重试 + 兜底 ----------
    r = node.call_tool("toolnode", {"group": "exec", "op": "run", "command": "ping -n 5 127.0.0.1", "timeout": 1})
    err = r.get("error") or {}
    q5a = err.get("code") == "COMMAND_TIMEOUT" and "retry_count" not in r
    check("Q5a 确定性错误不重试 (COMMAND_TIMEOUT)", q5a, f"code={err.get('code')} retry_present={'retry_count' in r}")
    # Q5b: BusyBox fallback（模拟双二进制缺失）
    orig_bp = node._toolnode_binary_path
    node._toolnode_binary_path = lambda: (None, False)
    orig_schemas = pn.TOOLNODE_SCHEMAS
    try:
        from busybox_fallback import SCHEMAS as BB_SCHEMAS
        pn.TOOLNODE_SCHEMAS = BB_SCHEMAS
    except Exception:
        pass
    rf = os.path.join(tmp, "q5bb.txt")
    r = node.call_tool("toolnode", {"group": "fs", "op": "write", "path": rf, "content": "busybox保命"})
    q5b = r.get("success") and (r.get("metadata") or {}).get("backend") == "busybox"
    check("Q5b BusyBox 兜底真实生效", q5b, f"backend={(r.get('metadata') or {}).get('backend')}")
    node._toolnode_binary_path = orig_bp
    pn.TOOLNODE_SCHEMAS = orig_schemas

    # ---------- Q6 错误闭环进智慧库 ----------
    before = wisdom_count(tmp)
    node.call_tool("toolnode", {"group": "exec", "op": "run", "command": "ping -n 5 127.0.0.1", "timeout": 1})
    after = wisdom_count(tmp)
    check("Q6 真实工具失败自动入错误智慧库", after > before, f"before={before} after={after}")

    # ---------- Q7 可观测性可验证 ----------
    m = node.observability.get_metrics()
    q7 = (m.get("total_calls", 0) > 0 and m.get("successful_calls", 0) > 0
          and m.get("failed_calls", 0) > 0)
    check("Q7 可观测性埋点可导出 (total/success/fail)", q7,
          f"total={m.get('total_calls')} success={m.get('successful_calls')} fail={m.get('failed_calls')} retry={m.get('retry_count')}")

    # ---------- Q8 跨平台一致 ----------
    ext = ".exe" if os.name == "nt" else ""
    exe = os.path.join(HERE, "toolnode" + ext)
    other = os.path.join(HERE, "toolnode" if os.name == "nt" else "toolnode.exe")
    q8 = os.path.isfile(exe) and os.path.isfile(other) and r_getsize_safe(exe) > 0
    check("Q8 双二进制随技能打包 (活跃平台可执行 + 异平台二进制在位)", q8,
          f"active={os.path.basename(exe)}({r_getsize_safe(exe)}B) other={os.path.basename(other)}({'present' if os.path.isfile(other) else 'MISSING'})")

    # ---------- Q+ 危险命令网关 ----------
    r = node.call_tool("toolnode", {"group": "exec", "op": "run", "command": "rm -rf ~"})
    check("Q+ 危险命令全链路拦截", (r.get("error") or {}).get("code") == "DANGEROUS_COMMAND_BLOCKED",
          f"code={(r.get('error') or {}).get('code')}")

    # ---------- 汇总 ----------
    print("=" * 70)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"Step 5 端到端验收结果: {passed}/{total} 通过")
    if passed == total:
        print("全部通过 ✅ 三层架构（Rust 能力 + Python 治理 + BusyBox 保命）Q1–Q8 终检通过")
        print("\nQ1–Q8 终态：")
        print("  Q1 真实接线        ✅   Q5 重试+兜底      ✅")
        print("  Q2 参数校验        ✅   Q6 错误→智慧库    ✅")
        print("  Q3 trace_id 全链路 ✅   Q7 可观测性       ✅")
        print("  Q4 防静默失败      ✅   Q8 跨平台一致     ✅")
        return 0
    print("存在失败项 ❌")
    return 1


def r_getsize_safe(p):
    try:
        return os.path.getsize(p)
    except OSError:
        return 0


if __name__ == "__main__":
    sys.exit(main())
