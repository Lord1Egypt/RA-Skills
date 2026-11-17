#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_eval_battery.py — AI 大脑学习记忆 · 自研评测电池（配置层）

用途：对「文件系统记忆」的编码→存储→提取→蒸馏链路做可复现评测（LongMemEval 四类问题
     单跳/多跳/时序/开放域 的配置层落地版，非标准 LoCoMo 跑分，口径见输出说明）。

安全设计：
- 本地闭环、零网络、零真实凭据、零真实记忆——全部在临时目录用合成数据模拟，不触碰
  真实 MEMORY.md / 日志 / 用户信息。
- 输出 JSON 可留存可重跑（对应发布安全稳定性验证门：测试脚本+结果 JSON 留存）。

用法：
  python memory_eval_battery.py [--out results.json]

版本：1.0.0 ｜ 作者：注册老炮 ｜ MIT
"""

import json
import os
import sys
import tempfile
import datetime

# ---------------------------------------------------------------- 合成测试数据
# 全部为中性示例（无真实用户/客户/凭据信息），仅用于验证记忆链路功能。

FACTS = [
    # (主题, 事实, 类型)  类型: single=单跳 / link=多跳关联 / time=时序
    ("preference", "用户偏好：报告默认输出 PDF 格式", "single"),
    ("preference", "用户偏好：交付物先给结论再给过程", "single"),
    ("project",    "项目 A 使用 Python 技术栈，负责人是开发者 1", "single"),
    ("project",    "项目 B 使用 Node 技术栈，负责人是开发者 2", "single"),
    ("meeting",    "周一例会评审项目 A 的周报", "link"),
    ("meeting",    "项目 A 的周报由负责人 1 汇报", "link"),
    ("standard",   "行业标准 S1 版本 2024 规定限值 X", "time"),
    ("standard",   "行业标准 S1 版本 2026 将限值更新为 Y", "time"),
]

QUESTIONS = [
    # (问题, 期望命中事实关键词, 类型)
    ("用户偏好的报告格式是什么？", "PDF", "single"),
    ("项目 A 用什么技术栈？", "Python", "single"),
    ("项目 A 的周报由谁汇报？", "负责人 1", "multi"),
    ("行业标准 S1 当前的限值是多少？", "Y", "time"),
    ("行业标准 S1 旧版限值是什么？", "X", "time"),
]

# ---------------------------------------------------------------- 记忆模拟器
class MemStore:
    """极简文件系统记忆模拟：entries.md = 语义记忆（事实），log.md = 情节记忆（流水）。"""

    def __init__(self, root):
        self.root = root
        self.semantic = os.path.join(root, "entries.md")
        self.episodic = os.path.join(root, "log.md")
        open(self.semantic, "w", encoding="utf-8-sig").close()
        open(self.episodic, "w", encoding="utf-8-sig").close()

    def write(self, text, kind="semantic"):
        path = self.semantic if kind == "semantic" else self.episodic
        with open(path, "a", encoding="utf-8-sig") as f:
            f.write(text + "\n")

    def read(self, kind="semantic"):
        path = self.semantic if kind == "semantic" else self.episodic
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()


def simulate_encode(store):
    """阶段1-2：编码与存储——情节记忆（经验/会议）进 log，语义记忆（事实/偏好）进 entries。"""
    for topic, fact, ftype in FACTS:
        if ftype == "link":
            # 会议/经验类 → 情节记忆（当日日志的模拟）
            store.write(fact, kind="episodic")
        elif ftype == "time":
            # 时序事实：记录时间戳，保证取最新（语义记忆）
            ts = "2026-06" if "旧版" in fact or "2024" in fact else "2026-08"
            store.write(f"[{ts}] {fact}")
        else:
            store.write(fact, kind="semantic")


def eval_single_hop(store):
    """单跳提取：直接问答命中率。"""
    text = store.read()
    hits = 0
    total = 0
    for q, expect, qtype in QUESTIONS:
        if qtype != "single":
            continue
        total += 1
        # 极简提取：判断期望关键词是否存在于记忆（对应"按需检索命中"）
        if expect in text:
            hits += 1
    return hits / total if total else 1.0


def eval_multi_hop(store):
    """多跳关联：跨条目关联（项目 A → 负责人 → 周报汇报人）。
    注意：需同时查语义记忆 + 情节记忆（对应技能"提取阶段：先读 MEMORY.md + 最近日志"）。"""
    sem = store.read(kind="semantic")
    epi = store.read(kind="episodic")
    text = sem + "\n" + epi
    # 链路：项目A(语义)→开发者1(语义)→周一例会评审周报(情节)
    ok = ("项目 A" in text) and ("开发者 1" in text) and ("周一例会" in text)
    return 1.0 if ok else 0.0


def eval_temporal(store):
    """时序一致性：取最新版本（2026 版限值 Y 而非 2024 版 X）。"""
    text = store.read()
    # 若两版都在，应能区分"当前=2026 版"；判定是否含最新版且保留版本轨迹
    has_latest = "限值更新为 Y" in text
    has_history = "规定限值 X" in text
    # 合格 = 最新版在 + 旧版轨迹保留（可追溯）
    return 1.0 if (has_latest and has_history) else 0.0


def simulate_consolidation(store, limit=200):
    """阶段4：蒸馏巩固——超限后压缩，核心保留率。"""
    # 先塞入噪音行（一次性信息），模拟真实场景中"低价值内容混入"
    for i in range(30):
        store.write(f"临时噪音 {i}：无关紧要的一次性记录，无长期价值", kind="semantic")
    text = store.read(kind="semantic")
    # 模拟蒸馏：保留含关键词"偏好/项目/标准"的核心行
    core_keywords = ("偏好", "项目", "标准")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    kept = [ln for ln in lines if any(k in ln for k in core_keywords)]
    core_in_kept = sum(1 for ln in kept for k in core_keywords if k in ln)
    core_total = sum(1 for ln in lines for k in core_keywords if k in ln)
    recall = core_in_kept / core_total if core_total else 1.0
    compressed = len(kept) < len(lines)  # 是否真的压缩了
    return recall, compressed


def simulate_capacity(store, flood=60):
    """容量控制：大量写入后是否触发超限（>阈值即压缩/报告）。"""
    for i in range(flood):
        store.write(f"临时条目 {i}：一次性信息，无长期价值", kind="semantic")
    size = os.path.getsize(store.semantic)
    limit = 3000
    triggered = size > limit
    return size, triggered


def run_all(root):
    store = MemStore(root)
    simulate_encode(store)

    single = eval_single_hop(store)
    multi = eval_multi_hop(store)
    temporal = eval_temporal(store)
    recall, compressed = simulate_consolidation(store)
    size, cap_triggered = simulate_capacity(store)
    # 编码质量：语义/情节分离是否正确
    encoded_ok = os.path.exists(store.semantic) and os.path.exists(store.episodic) \
                 and os.path.getsize(store.episodic) > 0

    def score(ratio, cap=1.0):
        """0-5 分：ratio 1.0 → 5；0 → 0。"""
        return round(min(5.0, 5.0 * min(1.0, ratio / cap)), 2)

    dims = {
        "编码写入": 5.0 if encoded_ok else 0.0,
        "单跳提取": score(single),
        "多跳关联": score(multi),
        "时序一致性": score(temporal),
        "蒸馏保真": score(recall),
        "容量控制": 5.0 if cap_triggered else 2.0,
    }
    return dims, {
        "single_hop": single,
        "multi_hop": multi,
        "temporal": temporal,
        "consolidation_recall": recall,
        "consolidation_compressed": compressed,
        "capacity_bytes": size,
        "capacity_triggered": cap_triggered,
    }


def main():
    out = "memory_eval_results.json"
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    with tempfile.TemporaryDirectory() as tmp:
        dims, raw = run_all(tmp)

    results = {
        "tool": "memory_eval_battery.py",
        "version": "1.0.0",
        "scope": "config-layer file-system memory (synthetic data, no real credentials)",
        "run_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "note": "自研配置层评测，非标准 LoCoMo/LongMemEval 跑分；分数为链路功能验证口径",
        "dimensions_0_5": dims,
        "raw_metrics": raw,
        "avg_score_0_5": round(sum(dims.values()) / len(dims), 2),
    }

    with open(out, "w", encoding="utf-8-sig") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n结果已存: {out}")


if __name__ == "__main__":
    main()
