#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_package.py —— 实现「导入」动词的底层机械步骤（一步式）

用法（由 SKILL.md 的「导入」动词调用，推荐一行跑完）:
    python import_package.py --package D:/exports/projA-R0-A2-20260915.zip \
        [--namespace B-R0-A2] [--workspace E:/projB]

    # 同设备便捷：扫描默认目录列出可导入包
    python import_package.py --scan [--workspace E:/projB]

行为（单命令完成 scan → 校验 → 落盘 → 登记 → 对账）:
    1. 读包内 PROVENANCE.json
    2. 哈希校验：优先用 PROVENANCE.files 逐文件比对（无需知晓复合哈希算法）；
       逐文件全通过即「内容完整」，否则逐条报出差异文件。
    3. 落盘（命名空间隔离子树，杜绝污染）：
       - 包内 handoffs/X      → CT_DIR/handoffs/<prefix>_X
       - 包内 artifacts/Y     → <workspace>/<prefix>/artifacts/Y
       - 包内 INDEX.excerpt.md→ <workspace>/<prefix>/INDEX.excerpt.md
       - PROVENANCE 合并导入事件 → CT_DIR/imports/PROVENANCE_import_<prefix>_<ts>.json
    4. 在 INDEX 追加「导入子树」区块 + B- 前缀会话地图 / 依赖边（type=imported）
    5. 局部对账（reconcile）：回读落盘文件字节数，写审计。

防污染核心：导入端产物副本落在命名空间子目录，与 A 原文件零关联。
"""

import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)


def _guard_not_skill_pkg(path: str, label: str):
    """安全硬闸（§〇 安全铁律）：禁止任何写盘路径落在技能包目录（~/.workbuddy/skills/）下。
    动词脚本绝不修改技能包自身；命中立即 abort。"""
    p = os.path.abspath(os.path.expanduser(path)).replace("\\", "/").lower()
    skills = os.path.abspath(os.path.expanduser("~/.workbuddy/skills")).replace("\\", "/").lower()
    if p == skills or p.startswith(skills + "/"):
        print(f"[安全闸·拒绝] {label} 目标路径落在技能包目录内：{p}\n"
              f"        本技能的动词脚本禁止写入/修改技能包自身（~/.workbuddy/skills/）。\n"
              f"        若你确需改包，请直接编辑文件，不要通过动词脚本代劳。", file=sys.stderr)
        sys.exit(2)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def list_default_dir():
    cfg = os.path.join(SKILL_ROOT, "config.yaml")
    if os.path.isfile(cfg):
        for line in open(cfg, encoding="utf-8"):
            if line.strip().startswith("export_dir:"):
                v = line.split(":", 1)[1].strip().strip('"').strip("'")
                if v and os.path.isdir(v):
                    return v
    d = os.path.join(os.path.expanduser("~"), ".edo-tensei", "exports")
    return d if os.path.isdir(d) else None


def ensure_index(ct: str):
    os.makedirs(ct, exist_ok=True)
    idx = os.path.join(ct, "INDEX.md")
    if not os.path.isfile(idx):
        with open(idx, "w", encoding="utf-8") as f:
            f.write("# 项目会话地图 INDEX\n根代号：R0　|　最后更新：" +
                    datetime.date.today().isoformat() + "\n\n## 1. 会话清单\n")
        return False
    return True


def _col_index(header, *names):
    if not header:
        return -1
    for name in names:
        for i, c in enumerate(header):
            if name in c:
                return i
    return -1


def parse_excerpt(index_text: str):
    """解析包内 INDEX.excerpt.md 的会话地图表与依赖表，用于 B- 前缀回填。"""
    lines = index_text.splitlines()
    map_rows = []          # list of dict(code, type, task, status)
    dep_rows = []          # list of (consumer, provider)
    in_map = False
    in_dep = False
    header = None
    for ln in lines:
        s = ln.strip()
        if not s.startswith("|"):
            if in_map:
                in_map = False
            if in_dep:
                in_dep = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not in_map and not in_dep:
            if cells and cells[0] == "代号":
                in_map = True
                header = cells
                continue
            if cells and cells[0] == "消费方" and len(cells) > 1 and "提供方" in cells[1]:
                in_dep = True
                continue
        if in_map:
            if len(cells) < 2 or cells[0] in ("", "代号"):
                continue
            if set(cells[0].strip()) <= set("-: "):  # 跳过 |------| 分隔行
                continue
            code = cells[0]
            if code == "总览":
                continue  # 导航节点不 fork
            hi_t = _col_index(header, "类型")
            hi_task = _col_index(header, "负责子任务", "子任务")
            hi_st = _col_index(header, "状态")
            map_rows.append({
                "code": code,
                "type": cells[hi_t] if hi_t >= 0 and hi_t < len(cells) else "",
                "task": cells[hi_task] if hi_task >= 0 and hi_task < len(cells) else "",
                "status": cells[hi_st] if hi_st >= 0 and hi_st < len(cells) else "",
            })
        elif in_dep:
            if len(cells) < 2 or cells[0] in ("", "消费方"):
                continue
            if set(cells[0].strip()) <= set("-: "):  # 跳过 |------| 分隔行
                continue
            dep_rows.append((cells[0], cells[1]))
    return map_rows, dep_rows


def prefix_exists(idx_text: str, prefix: str) -> bool:
    """判断控制塔 INDEX 是否已登记该命名空间前缀（避免重复落盘/重复地图行）。"""
    if not idx_text:
        return False
    if "`%s`" % prefix in idx_text:            # 导入区块标题：命名空间 `B-R0`
        return True
    if re.search(r"\|\s*%s\s*\|" % re.escape(prefix), idx_text):  # 地图行 | B-R0 |
        return True
    return False


def next_free_prefix(idx_text: str, base: str):
    """base 如 'B-R0'；若已占用，依次尝试 B2-R0 / B3-R0 … 直到空闲。"""
    if not prefix_exists(idx_text, base):
        return base
    i = 2
    while prefix_exists(idx_text, "B%d-%s" % (i, base[2:])):
        i += 1
    return "B%d-%s" % (i, base[2:])


def find_existing_import_json(im_dir: str, prefix: str):
    """读取该前缀此前写过的 PROVENANCE_import，用于幂等判定。"""
    if not os.path.isdir(im_dir):
        return None
    cands = sorted(glob.glob(os.path.join(im_dir, "PROVENANCE_import_%s_*.json" % prefix)))
    if not cands:
        return None
    try:
        return json.load(open(cands[-1], encoding="utf-8"))
    except Exception:
        return None


def same_import(prev, prov) -> bool:
    """两次导入是否为同一导出包（内容一致 → 可幂等跳过）。"""
    if not prev:
        return False
    if prev.get("source_node") != prov.get("source_node"):
        return False
    if prov.get("files") and prev.get("files"):
        return prov["files"] == prev["files"]
    return prev.get("package_content_hash") == prov.get("package_content_hash")


def main():
    # H3 加载验签（密钥门禁）：技能包 SEAL 被篡改或缺失签名则拒绝执行
    try:
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        import maintenance_lock
        if not maintenance_lock.verify_seal(SKILL_ROOT):
            print("[门禁·拒绝] 技能包 SEAL 验签失败（缺签名/被篡改），拒绝执行。", file=sys.stderr)
            sys.exit(1)
    except Exception as _e:
        print("[门禁·警告] 验签跳过（%s）；若这是已发布包请检查 assets/pubkey.pem 与 provenance/SEAL.json。" % _e, file=sys.stderr)
    ap = argparse.ArgumentParser(description="秽土转生 · 导入包（一步式）")
    ap.add_argument("--package", help="包文件路径")
    ap.add_argument("--scan", action="store_true", help="列出默认目录可导入包")
    ap.add_argument("--namespace", help="命名空间前缀（默认 B-<源首节点>）")
    ap.add_argument("--workspace", default=os.getcwd(), help="目标工作空间根目录")
    args = ap.parse_args()

    if args.scan and not args.package:
        d = list_default_dir()
        if not d:
            print("[提示] 默认导出目录为空或不存在，请直接 --package <路径>")
            sys.exit(0)
        print(f"默认目录: {d}")
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".zip"):
                print(f"  - {fn}")
        return

    if not args.package or not os.path.isfile(args.package):
        print("[错误] 需提供存在的 --package 路径")
        sys_exit(1)

    ws = os.path.abspath(args.workspace)
    _guard_not_skill_pkg(ws, "目标工作空间")
    ct = os.path.join(ws, ".workbuddy", "control-tower")
    had_index = ensure_index(ct)
    idx = os.path.join(ct, "INDEX.md")
    idx_text_existing = ""
    if had_index and os.path.isfile(idx):
        idx_text_existing = open(idx, encoding="utf-8", errors="ignore").read()
    ho_dir = os.path.join(ct, "handoffs")
    im_dir = os.path.join(ct, "imports")
    os.makedirs(ho_dir, exist_ok=True)
    os.makedirs(im_dir, exist_ok=True)

    # 读 PROVENANCE（先进内存，再决定落盘布局）
    with zipfile.ZipFile(args.package, "r") as z:
        raw = z.read("PROVENANCE.json").decode("utf-8", "ignore")
    prov = json.loads(raw)
    source_node = prov.get("source_node", "")
    first_code = source_node.split(",")[0].strip() or "R0"

    # 幂等处理：自动推导前缀时，若已登记则判定「同包跳过 / 异包 bump」
    prefix = args.namespace or ("B-" + first_code)
    skip_registration = False
    if not args.namespace:
        if prefix_exists(idx_text_existing, prefix):
            prev = find_existing_import_json(im_dir, prefix)
            if prev and same_import(prev, prov):
                skip_registration = True
                print(f"[幂等] 命名空间 {prefix} 已存在且为同一导出包，跳过重复落盘与登记。")
            else:
                new_prefix = next_free_prefix(idx_text_existing, "B-" + first_code)
                print(f"[提示] 命名空间 {prefix} 已存在（内容不同/旧版），自动 bump 到 {new_prefix}（视为新 fork）。")
                prefix = new_prefix

    # 幂等跳过（须在解压/落盘前判定，确保真正不写盘）
    if skip_registration:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        note = {
            "imported_at": datetime.datetime.now().astimezone().isoformat(),
            "target_workspace": ws,
            "namespace_prefix": prefix,
            "skipped": True,
            "reason": "已存在同一导出包（source_node + 文件清单一致），幂等跳过落盘与登记",
        }
        prov_path = os.path.join(im_dir, f"PROVENANCE_import_{prefix}_{ts}.json")
        with open(prov_path, "w", encoding="utf-8") as f:
            json.dump(note, f, ensure_ascii=False, indent=2)
        print(f"[OK] 幂等跳过：{args.package}")
        print(f"     命名空间前缀: {prefix}（已存在，内容一致）")
        print(f"     审计: {prov_path}")
        print(f"     A 原文件零触碰；本次未解压、未落盘、未改动任何文件。")
        return

    # 落盘目录
    ns_dir = os.path.join(ws, prefix)                       # <ws>/<prefix>/
    os.makedirs(ns_dir, exist_ok=True)

    # 包内相对路径 → 落盘绝对路径（命名空间隔离，绝不指原路径）
    def landed_of(rel: str):
        rel = rel.replace("\\", "/")
        if rel == "INDEX.excerpt.md":
            return os.path.join(ns_dir, "INDEX.excerpt.md")
        if rel.startswith("handoffs/"):
            base = rel[len("handoffs/"):]
            return os.path.join(ho_dir, f"{prefix}_{base}")
        if rel.startswith("artifacts/"):
            rest = rel[len("artifacts/"):]
            return os.path.join(ns_dir, "artifacts", rest)
        # 其余文件（如 full 深度的顶层 CONTEXT_DIGEST.md）按原名落命名空间根
        # 安全护栏：拒绝绝对路径与 .. 逃逸
        if os.path.isabs(rel) or ".." in rel.split("/"):
            return None
        return os.path.join(ns_dir, rel)

    # 提取并落盘
    landed_files = []  # (rel_in_package, landed_abs)
    landed_sha = {}    # rel_in_package -> sha256_hex（抽取时算出，校验免重读）
    with zipfile.ZipFile(args.package, "r") as z:
        for name in z.namelist():
            if name.endswith("/") or name == "PROVENANCE.json":
                continue
            dest = landed_of(name)
            if not dest:
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(name) as src, open(dest, "wb") as out:
                h = hashlib.sha256()
                for _chunk in iter(lambda: src.read(65536), b""):
                    out.write(_chunk)
                    h.update(_chunk)
                landed_sha[name] = h.hexdigest()
            landed_files.append((name, dest))

    # 注：幂等跳过已在「解压/落盘前」处理并提前返回，本分支 skip_registration 恒为 False。

    # 哈希校验：优先逐文件比对 PROVENANCE.files
    verify_lines = []
    verify_ok = True
    files_manifest = prov.get("files", {})
    if files_manifest:
        for rel, expected in files_manifest.items():
            dest = landed_of(rel)
            if not dest or not os.path.isfile(dest):
                verify_lines.append(f"[缺失] {rel} 未落盘")
                verify_ok = False
                continue
            actual = landed_sha.get(rel) or sha256_file(dest)
            if actual.lower() == expected.lower():
                verify_lines.append(f"[OK] {rel}")
            else:
                verify_lines.append(f"[不符] {rel}\n   期望 {expected}\n   实得 {actual}")
                verify_ok = False
        verify_summary = "逐文件校验全部通过 ✓" if verify_ok else "逐文件校验存在差异（见上）✗"
    else:
        # 旧包无清单：退回复合哈希（尽力而为）
        recompute = dict(landed_sha)
        recomputed = hashlib.sha256(
            "".join(recompute[k] for k in sorted(recompute)).encode("utf-8")).hexdigest()
        if prov.get("package_content_hash") == recomputed:
            verify_summary = "（旧包·无逐文件清单）复合哈希校验通过 ✓"
            verify_ok = True
        else:
            verify_summary = "（旧包·无逐文件清单）复合哈希不匹配 ✗"
            verify_ok = False

    # 写导入溯源（合并导出 PROVENANCE + 本次导入事件）
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    import_event = {
        "imported_at": datetime.datetime.now().astimezone().isoformat(),
        "target_workspace": ws,
        "namespace_prefix": prefix,
        "landed_handoff": next((d for r, d in landed_files
                                if r.startswith("handoffs/")), ""),
        "hash_verification": verify_summary,
    }
    merged = dict(prov)
    merged["import_event"] = import_event
    prov_path = os.path.join(im_dir, f"PROVENANCE_import_{prefix}_{ts}.json")
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    # 登记 INDEX：解析 excerpt 回填 B- 前缀子树
    excerpt_text = ""
    for r, d in landed_files:
        if r == "INDEX.excerpt.md":
            excerpt_text = open(d, encoding="utf-8", errors="ignore").read()
            break
    map_rows, dep_rows = parse_excerpt(excerpt_text) if excerpt_text else ([], [])

    handoff_dest = next((d for r, d in landed_files if r.startswith("handoffs/")), "(无)")
    art_dir = os.path.join(ns_dir, "artifacts")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(f"\n## 导入子树（命名空间 {prefix}）\n")
        f.write(f"- 来源工作空间: {prov.get('source_workspace','?')}　源节点: {source_node}\n")
        f.write(f"- 导入时间: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n")
        f.write(f"- 命名空间前缀: `{prefix}`（与源代号隔离，杜绝撞码）\n")
        f.write(f"- 落盘：交接文档 `{os.path.relpath(handoff_dest, ws)}`；"
                f"产物副本 `{os.path.relpath(art_dir, ws)}/`（与源空间零关联）\n")
        f.write(f"- 溯源：`{os.path.relpath(prov_path, ws)}`\n")
        f.write(f"- 防污染：命名空间隔离子树，绝不指向原路径；A 与 B 各自独立演进\n")
        f.write(f"- 哈希校验：{verify_summary}\n")
        def bcode(code):
            # "R0" -> prefix；"R0-1" -> prefix + "-1"（支持 bump 后的前缀）
            return prefix if code == first_code else prefix + code[len(first_code):]
        if map_rows:
            f.write("\n### 会话地图（fork 副本，代号加命名空间前缀）\n")
            f.write("| 代号 | 类型 | 负责子任务 | 状态 | 来源节点 |\n")
            f.write("|------|------|-----------|------|----------|\n")
            for r in map_rows:
                f.write(f"| {bcode(r['code'])} | {r['type']} | {r['task']} | {r['status']} | {r['code']} |\n")
        if dep_rows:
            f.write("\n### 依赖边（命名空间前缀）\n")
            f.write("| 消费方 | ← 提供方 | 说明 |\n")
            f.write("|--------|---------|------|\n")
            for cons, prov_c in dep_rows:
                f.write(f"| {bcode(cons)} | {bcode(prov_c)} | 随源子树导入的历史边 |\n")
        f.write("\n")

    # 回读对账
    audit = []
    for r, d in landed_files:
        sz = os.path.getsize(d) if os.path.isfile(d) else -1
        audit.append(f"  - {os.path.relpath(d, ws)} : {sz} B")
    print(f"[OK] 已导入: {args.package}")
    print(f"     命名空间前缀: {prefix}")
    print(f"     落盘根: {ns_dir}")
    print(f"     原 INDEX 是否存在: {had_index}（已增量追加，未覆盖）")
    print(f"     哈希校验: {verify_summary}")
    for ln in verify_lines:
        print("     " + ln)
    print(f"     落盘回读对账:")
    for a in audit:
        print("       " + a)
        print(f"     A 原文件零触碰，B 新子树独立演进。")


if __name__ == "__main__":
    main()
