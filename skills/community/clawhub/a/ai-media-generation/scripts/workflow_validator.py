#!/usr/bin/env python3
"""ComfyUI 工作流 JSON 校验器 — 节点图完整性门禁。

校验 Web 界面导出的 workflow JSON 的节点图结构：
  - JSON 可解析
  - nodes[] 每个节点有唯一 int id 与非空 type
  - links[] 格式正确（6 元组），源/目标节点 id 存在，目标 slot 非负，类型非空
  - 节点 inputs 里带 "link" 的引用必须指向真实存在的 link id
  - 重复 id / 悬空 link / 悬空节点引用都会被报出

用途：提交 ComfyUI 工作流到仓库/脚本自动化前先过一遍，防止"加载后节点全红"。

用法:
  python3 workflow_validator.py path/to/workflow.json [more.json ...]
  python3 workflow_validator.py --dir ./workflows --strict --json

退出码: 0=全部通过; 1=存在错误(配合 --strict 用作 CI 门禁)
"""
import argparse
import json
import sys
from pathlib import Path


def validate(path):
    """校验单个工作流 JSON，返回 (errors, warnings)。"""
    errors, warnings = [], []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON 解析失败: {e}"], []
    except OSError as e:
        return [f"读取失败: {e}"], []

    if not isinstance(data, dict):
        return ["顶层必须是 JSON 对象"], []

    nodes = data.get("nodes")
    links = data.get("links")

    if not isinstance(nodes, list):
        errors.append("缺少 nodes 数组（Web 导出格式必须含 nodes）")
    if not isinstance(links, list):
        errors.append("缺少 links 数组（Web 导出格式必须含 links）")
    if errors:
        return errors, warnings

    # ---- 节点表 ----
    node_ids = {}
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"nodes[{i}] 不是对象")
            continue
        nid = n.get("id")
        if not isinstance(nid, int) or isinstance(nid, bool):
            errors.append(f"nodes[{i}] 缺 id 或 id 非 int: {nid!r}")
            continue
        if nid in node_ids:
            errors.append(f"nodes[{i}] 重复 id: {nid}（首次出现在 nodes[{node_ids[nid]}]）")
        node_ids[nid] = i
        ntype = n.get("type")
        if not isinstance(ntype, str) or not ntype.strip():
            errors.append(f"nodes[{i}] (id={nid}) 缺 type 或 type 为空")

    # ---- link 表 ----
    link_ids = set()
    for i, l in enumerate(links):
        if not isinstance(l, list) or len(l) != 6:
            errors.append(f"links[{i}] 不是 6 元组: {l!r}")
            continue
        lid, src, _sslot, dst, dslot, ltype = l
        if not isinstance(lid, int) or isinstance(lid, bool):
            errors.append(f"links[{i}] link id 非 int: {lid!r}")
        elif lid in link_ids:
            errors.append(f"links[{i}] 重复 link id: {lid}")
        link_ids.add(lid if isinstance(lid, int) else i)
        if src not in node_ids:
            errors.append(f"links[{i}] 源节点 id {src!r} 不存在")
        if dst not in node_ids:
            errors.append(f"links[{i}] 目标节点 id {dst!r} 不存在")
        # 独立判断：节点存在性与 slot 合法性互不遮蔽（避免 elif 静默失配）
        if isinstance(dslot, int) and not isinstance(dslot, bool) and dslot < 0:
            errors.append(f"links[{i}] 目标 slot {dslot} 为负")
        if not isinstance(ltype, str) or not ltype.strip():
            errors.append(f"links[{i}] 缺连接类型（MODEL/CLIP/LATENT/VAE/IMAGE 等）")

    # ---- 节点内 link 引用 ----
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            continue
        inputs = n.get("inputs")
        if not isinstance(inputs, list):
            continue
        for j, inp in enumerate(inputs):
            if not isinstance(inp, dict):
                continue
            ref = inp.get("link")
            if ref is None:
                continue  # -1 / 手动值
            if not isinstance(ref, int) or ref == -1:
                continue
            if ref not in link_ids:
                errors.append(f"nodes[{i}] (id={n.get('id')}) inputs[{j}] 引用不存在的 link id: {ref}")

    # ---- 冗余检查（非阻断） ----
    if nodes and links:
        used_links = set()
        for n in nodes:
            if not isinstance(n, dict):
                continue
            for inp in n.get("inputs", []) or []:
                ref = inp.get("link") if isinstance(inp, dict) else None
                if isinstance(ref, int) and ref != -1:
                    used_links.add(ref)
        orphan = [lid for lid in link_ids if lid not in used_links and isinstance(lid, int) and lid >= 0]
        if orphan:
            warnings.append(f"{len(orphan)} 条 link 未被任何节点输入引用（悬空连接）: {sorted(orphan)[:10]}")

    return errors, warnings


def main():
    p = argparse.ArgumentParser(
        description="ComfyUI 工作流 JSON 节点图校验器（--strict 可作 CI 门禁）",
    )
    p.add_argument("paths", nargs="*", help="工作流 JSON 文件路径")
    p.add_argument("--dir", default=None, help="批量校验目录（*.json）")
    p.add_argument("--strict", action="store_true", help="存在错误时退出码 1（CI 门禁）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = p.parse_args()

    targets = list(args.paths)
    if args.dir:
        d = Path(args.dir)
        if not d.is_dir():
            print(f"目录不存在: {d}", file=sys.stderr)
            return 2
        targets += sorted(str(x) for x in d.glob("*.json"))

    if not targets:
        p.error("至少给一个 JSON 文件或 --dir 目录")

    results = {}
    total_err = 0
    for t in targets:
        errors, warnings = validate(t)
        results[t] = {"errors": errors, "warnings": warnings}
        total_err += len(errors)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for t, r in results.items():
            status = "PASS" if not r["errors"] else f"FAIL({len(r['errors'])})"
            print(f"[{status}] {t}")
            for e in r["errors"]:
                print(f"  ERROR: {e}")
            for w in r["warnings"]:
                print(f"  WARN : {w}")

    if total_err:
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
