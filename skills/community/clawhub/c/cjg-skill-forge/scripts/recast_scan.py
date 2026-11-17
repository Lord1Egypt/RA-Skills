#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recast_scan.py — 技能锻造炉 Mode C 只读扫描器（v2.7.0）

功能：
  - 锁死 ~/.workbuddy/skills/，只读扫描本机技能
  - 轻量元数据聚类（关键词同义 + recommends 引用图 + 目录名相似度）
  - 三维打分（使用率 / 完整度 / 牛逼度代理）
  - 输出《重铸计划报告》Markdown，不改写任何技能（零副作用）

安全：
  - 范围锁死：扫描目录默认 ~/.workbuddy/skills/，不接收命令行任意外部路径
  - 零网络默认：除非显式 --semantic 且本地有向量 key，否则不发起任何网络请求
  - 向量 key 外部化：仅读 env SILICONFLOW_API_KEY 或 ~/.workbuddy/secrets/cjg-evo/siliconflow.json，包内零密钥

用法：
  python recast_scan.py [--out report.md] [--semantic] [--top-n 20]
  （无 --out 时打印到标准输出）
"""

import os
import re
import sys
import json
import math
import glob
import datetime
from collections import defaultdict

# ---- 范围锁死 ----
DEFAULT_SKILLS_DIR = os.path.expanduser("~/.workbuddy/skills")
SKILLS_DIR = os.environ.get("SKILLS_DIR", DEFAULT_SKILLS_DIR)  # 仅本地测试可用 env 覆盖，命令行不暴露
USAGE_LOG = os.path.expanduser("~/.workbuddy/usage-log.json")
SECRETS_KEY_FILE = os.path.expanduser("~/.workbuddy/secrets/cjg-evo/siliconflow.json")

# ---- 中英文同义组（用于关键词聚类的可解释扩展）----
_SYN_GROUPS = [
    {"文献", "literature", "检索", "search", "searching", "reference", "参考", "biblio", "bib", "论文", "paper"},
    {"设计", "design", "ui", "ux", "视觉", "visual", "作图", "draw"},
    {"电商", "ecommerce", "e-commerce", "shop", "商城", "commerce", "商品"},
    {"文案", "copy", "copywriting", "营销", "marketing", "内容", "content", "写作", "writing"},
    {"部署", "deploy", "deployment", "发布", "publish", "release", "ci", "上线"},
    {"测试", "test", "testing", "qa", "eval", "评测"},
    {"邮件", "mail", "email", "邮箱", "qqmail"},
    {"知识库", "wiki", "knowledge", "kb", "笔记", "note", "obsidian"},
    {"语音", "voice", "tts", "speech", "克隆", "clone", "配音"},
    {"安全", "security", "sec", "审计", "audit", "review", "审查"},
    {"技能", "skill", "forge", "锻造", "元技能"},
    {"代理", "agent", "助手", "assistant", "智能体"},
    {"图表", "chart", "diagram", "可视化", "visualize", "plot", "图"},
    {"文件", "file", "文档", "doc", "office", "excel", "pdf"},
    {"翻译", "translate", "translation", "i18n", "双语", "bilingual"},
    {"学术", "academic", "科研", "research", "scholar", "学者"},
]
GROUP_OF = {}
for _gid, _grp in enumerate(_SYN_GROUPS):
    for _t in _grp:
        GROUP_OF[_t] = _gid


# ----------------------------------------------------------------------------
# Frontmatter 解析（轻量 YAML，纯标准库）
# ----------------------------------------------------------------------------
def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    data = {}
    lines = block.split("\n")
    cur_key = None
    cur_list = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if re.match(r"^\s*-\s+", line):
            if cur_list is not None:
                cur_list.append(line.strip()[2:].strip())
            i += 1
            continue
        mm = re.match(r"^([\w-]+):\s*(.*)$", line)
        if mm:
            key = mm.group(1)
            val = mm.group(2).strip().strip('"').strip("'")
            if val in ("|", ">"):
                # 块标量：读后续缩进行
                buf = []
                j = i + 1
                while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\t")):
                    buf.append(lines[j].strip())
                    j += 1
                data[key] = " ".join(buf)
                i = j
                cur_key, cur_list = None, None
                continue
            if val == "":
                cur_key = key
                cur_list = []
                data[key] = cur_list
                i += 1
                continue
            data[key] = val
            cur_key, cur_list = key, None
            i += 1
            continue
        i += 1
    return data


def load_skill(skill_dir):
    sk_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(sk_path):
        return None
    with open(sk_path, encoding="utf-8") as f:
        text = f.read()
    fm = parse_frontmatter(text)
    # 用于工作流影响扫描：recommends / allowed-tools
    return {
        "dir": skill_dir,
        "slug": fm.get("slug") or os.path.basename(skill_dir),
        "name": fm.get("name") or fm.get("slug") or os.path.basename(skill_dir),
        "displayName": fm.get("displayName") or "",
        "description": fm.get("description") or "",
        "version": fm.get("version") or "",
        "recommends": fm.get("recommends") or [],
        "allowed_tools": fm.get("allowed-tools") or [],
        "deprecated": fm.get("deprecated", "") in ("true", "True", True),
        "raw": text,
    }


# ----------------------------------------------------------------------------
# 三维打分
# ----------------------------------------------------------------------------
def completeness_score(skill_dir):
    score = 0
    if os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        score += 1
    if os.path.isdir(os.path.join(skill_dir, "references")):
        score += 1
    if os.path.isdir(os.path.join(skill_dir, "scripts")):
        score += 1
    if os.path.isdir(os.path.join(skill_dir, "tests")):
        score += 1
    try:
        n = sum(1 for _ in open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8"))
        if 100 <= n <= 600:
            score += 1
    except Exception:
        pass
    return min(score, 5)


def brilliance_proxy(skill):
    score = 0
    desc = (skill.get("description") or "").lower()
    if "use when" in desc or "当你" in (skill.get("description") or ""):
        score += 1
    if skill.get("recommends"):
        score += 1
    if skill.get("version"):
        score += 1
    if "技能锻造炉" in skill.get("raw", "") or "⚙️" in skill.get("raw", ""):
        score += 1
    refs = os.path.join(skill["dir"], "references")
    if os.path.isdir(refs) and len(os.listdir(refs)) >= 2:
        score += 1
    return min(score, 5)


def load_usage():
    if not os.path.isfile(USAGE_LOG):
        return {}
    try:
        with open(USAGE_LOG, encoding="utf-8") as f:
            return json.load(f).get("skills", {})
    except Exception:
        return {}


def usage_score(skill, usage_map):
    # 按 slug / name / displayName 多键匹配
    for key in (skill.get("slug"), skill.get("name"), skill.get("displayName")):
        if key and key in usage_map:
            entry = usage_map[key]
            dates = entry.get("recentDates", []) or []
            if not dates:
                return 0.0
            today = datetime.date.today()
            recent30 = 0
            for d in dates:
                try:
                    dd = datetime.datetime.strptime(d, "%Y-%m-%d").date()
                    if (today - dd).days <= 30:
                        recent30 += 1
                except Exception:
                    pass
            raw = recent30 * 1.0 + (len(dates) - recent30) * 0.3
            return min(1.0, raw / 12.0)
    return 0.0


# ----------------------------------------------------------------------------
# 轻量聚类
# ----------------------------------------------------------------------------
def _tokens(text):
    text = (text or "").lower()
    toks = set()
    for w in re.findall(r"[a-z0-9]+", text):
        toks.add(w)
    for c in re.findall(r"[\u4e00-\u9fff]+", text):
        toks.add(c)
        for ch in c:
            toks.add(ch)
    return toks


def _normalize(ts):
    out = set()
    for t in ts:
        gid = GROUP_OF.get(t)
        out.add(gid if gid is not None else t)
    return out


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def levenshtein(a, b):
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def _lev_sim(a, b):
    if not a or not b:
        return 0.0
    return 1.0 - levenshtein(a, b) / max(len(a), len(b))


def cluster(skills):
    n = len(skills)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    # 预计算 token 集合
    toks = []
    for s in skills:
        t = _normalize(_tokens(s["name"] + " " + s["displayName"] + " " + s["description"]))
        toks.append(t)

    for i in range(n):
        for j in range(i + 1, n):
            hit = False
            reason = []
            # 关键词 jaccard
            jac = _jaccard(toks[i], toks[j])
            if jac >= 0.2 and len(toks[i] & toks[j]) >= 1:
                hit = True
                reason.append("keyword")
            # 目录名相似度
            if _lev_sim(skills[i]["slug"], skills[j]["slug"]) >= 0.6:
                hit = True
                reason.append("name-sim")
            # recommends 引用图邻居
            ri = set(skills[i].get("recommends", []))
            rj = set(skills[j].get("recommends", []))
            if skills[i]["slug"] in rj or skills[j]["slug"] in ri or (ri & rj):
                hit = True
                reason.append("recommends")
            if hit:
                union(i, j)
                skills[i].setdefault("_links", []).append((skills[j]["slug"], reason))
                skills[j].setdefault("_links", []).append((skills[i]["slug"], reason))

    # 收集聚类
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)
    clusters = []
    for idxs in groups.values():
        members = [skills[i] for i in idxs]
        clusters.append(members)
    # 单成员聚类不叫"重叠"，但保留用于完整报告；多成员优先
    clusters.sort(key=lambda c: -len(c))
    return clusters


# ----------------------------------------------------------------------------
# 可选语义精校（需本地 key，否则跳过）
# ----------------------------------------------------------------------------
def _load_embed_key():
    key = os.environ.get("SILICONFLOW_API_KEY")
    base = os.environ.get("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1/embeddings")
    model = os.environ.get("SILICONFLOW_MODEL", "BAAI/bge-m3")
    if not key and os.path.isfile(SECRETS_KEY_FILE):
        try:
            with open(SECRETS_KEY_FILE, encoding="utf-8") as f:
                d = json.load(f)
            key = d.get("api_key")
            base = d.get("base_url", base)
            model = d.get("model", model)
        except Exception:
            pass
    return key, base, model


def semantic_similarity(texts, key, base, model):
    """返回两两平均余弦相似度（0-1）；失败返回 None。"""
    import urllib.request
    try:
        vecs = []
        for t in texts:
            payload = json.dumps({"model": model, "input": t[:2000]}).encode("utf-8")
            req = urllib.request.Request(base, data=payload, headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            })
            with urllib.request.urlopen(req, timeout=20) as resp:
                obj = json.loads(resp.read().decode("utf-8"))
            vecs.append(obj["data"][0]["embedding"])
        # 平均余弦
        import math
        total, cnt = 0.0, 0
        for a in range(len(vecs)):
            for b in range(a + 1, len(vecs)):
                va, vb = vecs[a], vecs[b]
                dot = sum(x * y for x, y in zip(va, vb))
                na = math.sqrt(sum(x * x for x in va))
                nb = math.sqrt(sum(x * x for x in vb))
                if na and nb:
                    total += dot / (na * nb)
                    cnt += 1
        return (total / cnt) if cnt else None
    except Exception:
        return None


# ----------------------------------------------------------------------------
# 报告渲染
# ----------------------------------------------------------------------------
def render_report(clusters, usage_map, semantic=False):
    lines = []
    lines.append("# 重铸计划报告（Mode C · 技能锻造炉）")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append("> 扫描范围：仅 `~/.workbuddy/skills/`（锁死）  ")
    lines.append("> **默认仅分析，不合并。** 合并为可选、逐技能确认的高权限操作。")
    lines.append("")
    multi = [c for c in clusters if len(c) > 1]
    lines.append(f"## 概览")
    lines.append(f"- 本机技能总数：{sum(len(c) for c in clusters)}")
    lines.append(f"- 检测到的重叠聚类（≥2 成员）：**{len(multi)}** 个")
    lines.append(f"- 单技能（无重叠）：{len(clusters) - len(multi)} 个")
    lines.append("")
    if not multi:
        lines.append("✅ 未检测到明显的同类/重叠技能。若仍想精校，可加 `--semantic` 做语义相似性复核（需本地向量 key）。")
        lines.append("")
        return "\n".join(lines)

    lines.append("## 重叠聚类详情")
    lines.append("")
    for ci, members in enumerate(multi, 1):
        # 三维分
        scored = []
        for s in members:
            u = usage_score(s, usage_map)
            c = completeness_score(s["dir"])
            b = brilliance_proxy(s)
            base_score = 0.4 * u + 0.25 * (c / 5.0) + 0.35 * (b / 5.0)
            scored.append((s, u, c, b, base_score))
        scored.sort(key=lambda x: -x[4])
        base = scored[0][0]
        lines.append(f"### 聚类 {ci}（{len(members)} 个成员）")
        lines.append("")
        lines.append("| 成员 slug | 使用率 | 完整度 | 牛逼度(代理) | 综合分 | 基座候选 |")
        lines.append("|---|---|---|---|---|---|")
        for s, u, c, b, bs in scored:
            cand = "⭐ 推荐" if s is base else ""
            lines.append(
                f"| `{s['slug']}`{' (deprecated)' if s['deprecated'] else ''} "
                f"| {u:.2f} | {c}/5 | {b}/5 | {bs:.2f} | {cand} |"
            )
        lines.append("")
        # 推荐理由
        bu, bc, bb, bbs = scored[0][1], scored[0][2], scored[0][3], scored[0][4]
        reasons = []
        if bu >= 0.5:
            reasons.append(f"使用率最高（{bu:.2f}）")
        if bc >= 4:
            reasons.append(f"完整度满（{bc}/5，含 references/scripts）")
        if bb >= 4:
            reasons.append(f"牛逼度代理达标（{bb}/5）")
        if not reasons:
            reasons.append("综合分相对最高（其他成员更弱）")
        lines.append(f"**推荐基座**：`{base['slug']}` —— 理由：{'；'.join(reasons)}。")
        lines.append("")
        # 关联依据（可解释）
        link_seen = set()
        link_uniq = []
        member_slugs = {m["slug"] for m in members}
        for s in members:
            for (other, rsn) in s.get("_links", []):
                if other in member_slugs:
                    ln = f"- `{s['slug']}` ↔ `{other}`：{'/'.join(rsn)}"
                    if ln not in link_seen:
                        link_seen.add(ln)
                        link_uniq.append(ln)
        if link_uniq:
            lines.append("**关联依据**（可解释，便于人工复核；注意 `recommends` 表示\"推荐使用\"而非\"同类\"，请人工判断）：")
            lines.extend(link_uniq)
            lines.append("")
        # 预测影响
        lines.append("**预测影响**：")
        lines.append("- 正面：合并后单一技能覆盖该类别全部场景，减少选择成本；继承基座使用动量，迭代环立即有信号。")
        lines.append("- 负面：被并技能若含独特引用/参数，需人工核对是否并入；合并技能首次发布需重新走质检（quick_validate + 真机测试）。")
        lines.append("")
        # 工作流影响（静态引用图，仅供参考）
        deps = []
        for other in [sk for cl in clusters for sk in cl]:
            if other["slug"] == base["slug"]:
                continue
            rec = set(other.get("recommends", []))
            if base["slug"] in rec:
                deps.append((other["slug"], "recommends"))
        if deps:
            lines.append("**工作流影响（仅供参考，基于静态引用图推断，不保证完整）**：")
            for dslug, via in deps:
                lines.append(f"- `{dslug}` 通过 `{via}: {base['slug']}` 引用本基座；若 deprecated 被并成员，需同步更新其引用。")
            lines.append("")
        else:
            lines.append("**工作流影响**：未检测到其他技能静态引用本聚类成员（仅供参考）。")
            lines.append("")
        # 可选语义确认度
        if semantic:
            key, base_url, model = _load_embed_key()
            if key:
                sim = semantic_similarity(
                    [f"{s['name']} {s['description'][:300]}" for s in members], key, base_url, model
                )
                if sim is not None:
                    verdict = "语义强关联" if sim >= 0.7 else ("语义中等关联" if sim >= 0.5 else "语义弱关联，建议人工复核")
                    lines.append(f"**语义精校**（{model}）：簇内平均余弦相似度 {sim:.2f} → {verdict}。")
                else:
                    lines.append("**语义精校**：向量调用失败，已回退轻量判定（不影响主流程）。")
                lines.append("")
        lines.append("---")
        lines.append("")
    lines.append("## 下一步")
    lines.append("确认以上计划后，在对话中告知基座 + 逐技能确认合并；合并 SOP 见 `references/skill-consolidation.md` §5。")
    lines.append("")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# 主入口
# ----------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    out_path = None
    semantic = False
    top_n = 0
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out":
            i += 1
            out_path = args[i] if i < len(args) else None
        elif a == "--semantic":
            semantic = True
        elif a == "--top-n":
            i += 1
            top_n = int(args[i]) if i < len(args) else 0
        i += 1

    if not os.path.isdir(SKILLS_DIR):
        print(f"[错误] 技能目录不存在：{SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    usage_map = load_usage()
    skills = []
    for d in sorted(glob.glob(os.path.join(SKILLS_DIR, "*"))):
        if os.path.isdir(d):
            s = load_skill(d)
            if s:
                skills.append(s)

    if not skills:
        print("[警告] 未扫描到任何技能。", file=sys.stderr)
        sys.exit(1)

    clusters = cluster(skills)
    if top_n:
        clusters = clusters[:top_n]

    report = render_report(clusters, usage_map, semantic=semantic)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[OK] 报告已写入：{out_path}（共 {len(clusters)} 个聚类，{sum(len(c) for c in clusters)} 个技能；零副作用）")
    else:
        print(report)


if __name__ == "__main__":
    main()
