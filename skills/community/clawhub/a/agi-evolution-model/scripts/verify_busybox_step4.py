#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 4 验收脚本：BusyBox 兜底层（保命层）实测。

验证 Q5 的 fallback 分支：当能力层（Rust 二进制 + Python 原型）全缺/崩溃时，
治理层自动回退到 BusyBox 保命层，仍返回统一契约并维持核心能力。

测试项：
- F1 双二进制缺失 → fs.write 经 BusyBox 成功，backend=busybox，回读 verified
- F2 fs.read 经 BusyBox 返回来源时间戳 + 内容一致
- F3 fs.list 经 BusyBox 返回条目
- F4 sys.all 经 BusyBox 返回基础系统摘要，backend=busybox
- F5 危险命令在 BusyBox 路径仍被拦截（DANGEROUS_COMMAND_BLOCKED）
- F6 不支持的 op 返回 BUSYBOX_UNSUPPORTED（明确边界，不静默假装成功）
- F7 trace_id 在 BusyBox 路径仍贯穿（Q3 兜底一致）
- F8 正常路径（二进制在）不误触发 BusyBox（backend=rust）

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

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    tmp = tempfile.mkdtemp(prefix="pn_step4_")
    node = PerceptionNode(memory_dir=tmp)
    print(f"PerceptionNode ready (memory_dir={tmp})")
    print("-" * 64)

    # ---------- F8 正常路径不误触发 BusyBox ----------
    r = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    backend_normal = (r.get("metadata") or {}).get("backend")
    # 正常路径 backend 可能为 None（Rust 契约不带 backend 键）或 "rust"；绝不应是 "busybox"
    check("F8 正常路径不误触发 BusyBox", backend_normal != "busybox" and r.get("success") is True,
          f"backend={backend_normal}")

    # ---------- 模拟能力层全缺：monkeypatch _toolnode_binary_path ----------
    orig = node._toolnode_binary_path
    node._toolnode_binary_path = lambda: (None, False)
    # 同时让 SCHEMAS 走 busybox（模拟 toolnode.py 也缺）：直接 patch 模块级 TOOLNODE_SCHEMAS
    import perception_node as pn
    orig_schemas = pn.TOOLNODE_SCHEMAS
    if not orig_schemas:
        # 正常情况 schemas 来自 toolnode.py；保命测试强制切到 busybox schemas 以模拟 toolnode.py 缺失
        try:
            from busybox_fallback import SCHEMAS as BB_SCHEMAS
            pn.TOOLNODE_SCHEMAS = BB_SCHEMAS
        except Exception:
            pass

    test_file = os.path.join(tmp, "bb_probe.txt")

    # F1 fs.write 经 BusyBox
    r = node.call_tool("toolnode", {"group": "fs", "op": "write",
                                    "path": test_file, "content": "BusyBox保命探针\n中文"})
    d = r.get("data") or {}
    check("F1 BusyBox fs.write 回读 verified", r.get("success") is True and d.get("verified_on_disk") is True
          and d.get("bytes_written", 0) > 0, f"backend={(r.get('metadata') or {}).get('backend')} bytes={d.get('bytes_written')}")

    # F2 fs.read 经 BusyBox
    r = node.call_tool("toolnode", {"group": "fs", "op": "read", "path": test_file})
    d = r.get("data") or {}
    check("F2 BusyBox fs.read 来源时间戳+内容一致", r.get("success") is True and d.get("source_timestamp")
          and d.get("content") == "BusyBox保命探针\n中文", f"src_ts={d.get('source_timestamp')}")

    # F3 fs.list 经 BusyBox
    r = node.call_tool("toolnode", {"group": "fs", "op": "list", "path": tmp})
    d = r.get("data") or {}
    check("F3 BusyBox fs.list 返回条目", r.get("success") is True and d.get("count", 0) >= 1
          and (r.get("metadata") or {}).get("backend") == "busybox", f"count={d.get('count')}")

    # F4 sys.all 经 BusyBox
    r = node.call_tool("toolnode", {"group": "sys", "op": "all"})
    d = r.get("data") or {}
    check("F4 BusyBox sys.all 基础摘要", r.get("success") is True and d.get("platform") in ("windows", "linux")
          and "disk" in d and (r.get("metadata") or {}).get("backend") == "busybox",
          f"platform={d.get('platform')} backend={(r.get('metadata') or {}).get('backend')}")

    # F5 危险命令在 BusyBox 路径仍被拦截
    r = node.call_tool("toolnode", {"group": "exec", "op": "run", "command": "rm -rf ~"})
    err = r.get("error") or {}
    check("F5 BusyBox 危险命令拦截", r.get("success") is False and err.get("code") == "DANGEROUS_COMMAND_BLOCKED",
          f"code={err.get('code')}")

    # F6 不支持的 op 返回 BUSYBOX_UNSUPPORTED
    r = node.call_tool("toolnode", {"group": "fs", "op": "search", "path": tmp, "pattern": "x"})
    err = r.get("error") or {}
    check("F6 BusyBox 不支持 op 明确报错", r.get("success") is False and err.get("code") == "BUSYBOX_UNSUPPORTED",
          f"code={err.get('code')}")

    # F7 trace_id 在 BusyBox 路径贯穿
    r = node.call_tool("toolnode", {"group": "fs", "op": "stat", "path": test_file})
    tid = r.get("trace_id")
    meta_tid = (r.get("metadata") or {}).get("trace_id")
    check("F7 BusyBox 路径 trace_id 一致", bool(tid) and tid == meta_tid, f"trace_id={tid}")

    # ---------- 还原 ----------
    node._toolnode_binary_path = orig
    pn.TOOLNODE_SCHEMAS = orig_schemas

    print("-" * 64)
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"Step 4 (BusyBox 兜底) 门禁结果: {passed}/{total} 通过")
    if passed == total:
        print("全部通过 ✅ Q5 fallback 分支就位，可进入 Step 5 (端到端)")
        return 0
    print("存在失败项 ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())
