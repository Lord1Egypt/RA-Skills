#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工作台结构闸门 C1–C7 共享机检引擎（零第三方依赖 · 零浏览器）。

规范真源：`ct-base/references/workbench_ui.md`
  - §18.1 三轮事故（版本漂移 / 内嵌配置陈旧 / 窄屏溢出）
  - §18.2 结构红线 1–10（配置单源 / 外链 CSS / 无 sibling / 字号令牌 / 顶栏按钮簇 / 窄屏）
  - §18.3 交付闸门（本脚本即该节的家族单点实现）
  - §4.5 / §4.5.1 字号梯度令牌

检查项（P1 阻止发布 / WARN 建议）：

  C1  版本一圈锚点一致      SKILL.md frontmatter / AGENTS.md 标题 / CHANGELOG 顶部 /
                            workbench.config.json / 各页内嵌配置 / 页面「<skill> vX.Y.Z」展示位
  C1b coze.skill_version    存在即须等于基准版本（缺失按 N/A，不判）
  C2  内嵌配置同源          内嵌副本须与 workbench.config.json 深度相等（陈旧=P1；无内嵌=WARN）
  C3  窄屏守卫规则          §5.6.2 五条（吸顶 / 横向 / 折叠保标签 / 网格塌陷 / 长词断行）；
                            启发式判据，首期 WARN
  C4  生产页外链共享 CSS    tokens.css 必外链；用到 wb-list 组件须外链 wb-list.css；
                            检出内联共享组件副本（§18.2-3）判 P1
  C5  无兄弟技能依赖        页面/样式/脚本零 `../ct-*` sibling 回退
  C6a 字号令牌齐备          tokens.css 含 --wb-fs-{2xl,xl,lg,base,sm,xs,2xs} 七档
  C6b 无裸 px 字号          页面（含内联 style）与本地 CSS 零 `font-size:<数字>px`
  C6c body 基准令牌化       tokens.css 的 body 使用 var(--wb-fs-base)（缺失 WARN）
  C7  返回 CT 首页钮        #wb-cthome + wbGoCtHome() + 带协议/相对路径的 CT_HOME
  C8  诊断信息收纳          §32.1：业务视图不得出现自检/探活矩阵；禁 appendChild 挂 .wb-content；
                          自检路由须在 about 折叠链内；标准后端状态 pill 探活属 §5.2 合法例外

设计口径（2026-11-14 收进 ct-base，替换各叶子手工副本）：
  - **自动定位**：不假设文件名。主页面 = `workbench/` 下不以 `_` 开头、且外链了
    tokens.css 的所有 `*.html`（多页技能逐页检查，如 ct-datacheck 的 index + workbench）。
  - **JS 全域收集**：C7 与 C5 在 html + 全部本地 `*.js` 上联合判定，故内联/外置两种
    架构同等适用（原 ct-adam 版只扫 html，外置 app.js 的技能会被误判）。
  - **零叶子硬编码**：不含任何技能名、类名、文件名常量；技能名取自目录名。
  - **WARN 优先**：启发式项（C3）与「无内嵌副本」类结构性缺失首期只 WARN，
    待全家族基线清零后再改 `_LEVEL_*` 升 P1——同 §32.4 纪律。

用法：
  python wb_ui_check.py --root <技能根>          # 单技能
  python wb_ui_check.py --root <技能根> --json
  python wb_ui_check.py --all                    # ct-base 同级全部 ct-* 技能汇总
  python wb_ui_check.py --root <根> --sync       # 按 config.json 重写内嵌配置副本
  python wb_ui_check.py --root <根> --set-version X.Y.Z
退出码：有 P1 = 1，仅 WARN/全绿 = 0。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

P1, WARN, OK = "P1", "WARN", "OK"
_ORDER = {P1: 2, WARN: 1, OK: 0}

# 启发式项等级（基线清零后改 "P1" 即升级，判据不动）
_LEVEL_C3 = WARN
_LEVEL_EMBED_MISSING = WARN
_LEVEL_C6C = WARN
_LEVEL_C8_PROBE = WARN          # §32.1 机检口径②：探活 fetch 需人工确认

FS_TOKENS = ["--wb-fs-2xl", "--wb-fs-xl", "--wb-fs-lg",
             "--wb-fs-base", "--wb-fs-sm", "--wb-fs-xs", "--wb-fs-2xs"]

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FS_DECL_RE = re.compile(r"font-size\s*:\s*([^;{}\n]*)")
BARE_PX_RE = re.compile(r"\d+(?:\.\d+)?px")


def bare_px_font_size(text, orig=None):
    """返回 [{idx, decl}]：font-size 取值里出现裸 px。

    ⚠ 不能只做「冒号后不是 var(」的负向断言——`var(--wb-fs-xs, 13px)` 的**回退值**
    里也有 px，`\\s*` 回溯后会被误判成硬编码（实测假阳性来源）。改为先取整个取值，
    含 `var(` 即视为令牌驱动（回退值问题归 §32.4 的 THEME-TOKEN-UNDEFINED 管），
    否则再判是否出现 `数字px`。

    行内豁免：命中行或其上一行写 `/* wb-fs-ok: <理由> */`，或家族既有的
    `/* ctqa-allow:bare-px <理由> */`（如 iOS 聚焦防缩放的 `input{font-size:16px}`，
    属 §4.5-2 允许的令牌外特殊情况，须标理由）。
    `text` 通常是已消隐注释的副本，故豁免标记要从 `orig`（原文）读——否则注释放进
    消隐副本后连标记本身一起被抹掉，豁免永远失效。
    """
    out = []
    lines = (orig if orig is not None else text).split("\n")
    starts, acc = [], 0
    for ln in text.split("\n"):
        starts.append(acc)
        acc += len(ln) + 1

    def _line_idx(idx):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= idx:
                lo = mid
            else:
                hi = mid - 1
        return lo

    for m in FS_DECL_RE.finditer(text):
        decl = m.group(1)
        if "var(" in decl:
            continue
        if not BARE_PX_RE.search(decl):
            continue
        ln = _line_idx(m.start())
        ctx_txt = lines[ln] + (lines[ln - 1] if ln else "")
        if "wb-fs-ok:" in ctx_txt or "ctqa-allow:bare-px" in ctx_txt:
            continue
        out.append({"idx": m.start(), "decl": decl.strip()})
    return out

# C3：每条 = (正则, 事故编号, 缺了会怎样)。正则按「家族已有写法」取并集，避免锁死实现。
RESPONSIVE_RULES = [
    (r"position\s*:\s*sticky",
     "INC-2026-10-20-B",
     "侧栏不吸顶，页面滚动时菜单滚出视口（§5.6.5：≤768px 转吸顶横条）"),
    (r"@media[^{]*max-width[^{]*\{(?:(?!\}\s*$).)*?flex-direction\s*:\s*(?:row|column)",
     "INC-2026-10-20-A",
     "窄屏断点内缺方向切换：侧栏竖向 flex 不变，菜单项竖排撑破横向"),
    (r"collapsed[^{}]*\{[^{}]*display\s*:\s*inline",
     "INC-2026-10-20-C",
     "窄屏误触侧栏空白触发折叠，整条菜单退化为纯图标行（.lbl 须保持 inline）"),
    (r"grid-template-columns\s*:\s*(?:1fr|repeat\(\s*1\s*,|minmax\(\s*0\s*,\s*1fr)",
     "INC-2026-10-22-A",
     "多列 grid 轨道在 ≤360px 视口不塌陷，撑破页面横向溢出"),
    (r"(?:overflow-wrap\s*:\s*(?:anywhere|break-word)|word-break\s*:\s*break-word|word-wrap\s*:\s*break-word)",
     "INC-2026-10-22-B",
     "长斜杠令牌（PARAMCD/AVAL/…）min-content 沿祖先链撑到视口"),
]

_EMBED_MARKERS = [
    "const WB_CONFIG_EMBED = ",
    "const CFG_EMBED = ",
    "var WB_CONFIG_EMBED = ",
    "window.WB_CONFIG_EMBED = ",
]
_SIBLING_RE = re.compile(r"""['"(][^'"()\s]*\.\.[/\\]ct-[a-z][^'"()\s]*""")
_INLINE_SHARED_RE = re.compile(
    r"<style[^>]*id=[\"'][^\"']*(?:inline|wblist|shared)[^\"']*[\"'][^>]*>", re.I)


# ── 基础工具 ────────────────────────────────────────────────────────────────
def read(p):
    try:
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return None


def blank_comments(text):
    """注释替换为等长空白：保行号、防注释示例误判（同 wb_theme_check 手法）。"""
    def _c(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"/\*[\s\S]*?\*/", _c, text or "")
    return re.sub(r"(?m)^(\s*)//.*$", lambda m: " " * len(m.group(0)), text)


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def media_blocks(css):
    """切出 @media (max-width:…) 块 → [(条件, 块内文本)]，用于窄屏规则的位置判定。"""
    out = []
    for m in re.finditer(r"@media[^{]*max-width[^{]*\{", css or ""):
        i = m.end()
        depth, j = 1, i
        while j < len(css) and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        out.append((css[m.start():i], css[i:j]))
    return out


class Report:
    def __init__(self, skill, exempt=None):
        self.skill = skill
        self.exempt = exempt or {}          # {"C4": "理由"} —— 见 wb_ui_check.exempt.json
        self.items = []

    def add(self, check, level, msg, hint="", loc=""):
        key = check.split()[0]
        if level != OK and key in self.exempt:
            self.items.append({"skill": self.skill, "check": check, "level": OK,
                               "msg": "豁免：%s（原始判定 %s）" % (self.exempt[key], msg),
                               "hint": "", "loc": loc})
            return
        self.items.append({"skill": self.skill, "check": check, "level": level,
                           "msg": msg, "hint": hint, "loc": loc})

    @property
    def worst(self):
        w = OK
        for it in self.items:
            if _ORDER[it["level"]] > _ORDER[w]:
                w = it["level"]
        return w

    @property
    def failed(self):
        return [i for i in self.items if i["level"] == P1]


# ── 上下文：自动定位 ────────────────────────────────────────────────────────
class Ctx:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.skill = os.path.basename(self.root.rstrip(os.sep))
        self.wb = os.path.join(self.root, "workbench")
        self.cfg_path = os.path.join(self.wb, "workbench.config.json")
        self.cfg = self._json(self.cfg_path)
        self.pages = self._pages()          # [(文件名, 文本)]
        self.css = self._files(".css")      # [(文件名, 文本)]
        self.js = self._files(".js")        # [(文件名, 文本)]

    @staticmethod
    def _json(p):
        t = read(p)
        try:
            return json.loads(t) if t else None
        except Exception:
            return None

    def _files(self, ext):
        out = []
        if not os.path.isdir(self.wb):
            return out
        for fn in sorted(os.listdir(self.wb)):
            if fn.startswith("_") or not fn.lower().endswith(ext):
                continue
            t = read(os.path.join(self.wb, fn))
            if t is not None:
                out.append((fn, t))
        return out

    def _pages(self):
        """主页面 = 外链了 tokens.css 的 html（不以 _ 开头的全部，多页逐个查）。"""
        cands = []
        if not os.path.isdir(self.wb):
            return cands
        for fn in sorted(os.listdir(self.wb)):
            if fn.startswith("_") or not fn.lower().endswith((".html", ".htm")):
                continue
            t = read(os.path.join(self.wb, fn))
            if t is None or not re.search(r'href=["\'][^"\']*tokens\.css', t):
                continue
            cands.append((fn, t))
        # 无外链页（历史形态）退化为「最大的 html」，保证仍有检查对象
        if not cands:
            bulk = [(fn, read(os.path.join(self.wb, fn)))
                    for fn in sorted(os.listdir(self.wb))
                    if fn.lower().endswith((".html", ".htm")) and not fn.startswith("_")]
            bulk = [(f, t) for f, t in bulk if t]
            if bulk:
                cands = [max(bulk, key=lambda x: len(x[1]))]
        return cands

    @property
    def html(self):
        return self.pages[0][1] if self.pages else ""

    def all_text(self):
        """html + css + js 联合文本（C5 跨资产判定用）。"""
        return "\n".join([t for _, t in self.pages] + [t for _, t in self.css] + [t for _, t in self.js])

    def exempt(self):
        """逐项豁免表：workbench/wb_ui_check.exempt.json（缺省空；理由必填，可审计）。

        形如 {"C4": "存量页内联共享组件，无法外链（§14 存量豁免）"}。键为检查编号
        （C1/C2/C3/C4/C5/C6a/C6b/C6c/C7），命中后该项记 OK 并保留原始判定文本。
        """
        p = os.path.join(self.wb, "wb_ui_check.exempt.json")
        obj = self._json(p)
        if not isinstance(obj, dict):
            return {}
        return {k: str(v) for k, v in obj.items()
                if not k.startswith("_") and str(v).strip()}


# ── C1 / C1b 版本锚点 ───────────────────────────────────────────────────────
def extract_embed(text):
    for mk in _EMBED_MARKERS:
        i = text.find(mk)
        if i < 0:
            continue
        try:
            obj, _ = json.JSONDecoder().raw_decode(text, i + len(mk))
            return obj, None
        except ValueError as e:
            return None, "%s 声明处 JSON 解析失败: %s" % (mk.strip(), str(e)[:100])
    m = re.search(r'<script[^>]*id=["\']wb-config["\'][^>]*>([\s\S]*?)</script>', text)
    if m:
        try:
            return json.loads(m.group(1)), None
        except Exception as e:
            return None, "内嵌 #wb-config JSON 解析失败: %s" % str(e)[:100]
    return None, None


def check_version(ctx, rep):
    skill = ctx.skill
    anchors = {}

    t = read(os.path.join(ctx.root, "SKILL.md")) or ""
    m = re.search(r"^\s*version:\s*(\S+)", t, re.M)
    anchors["SKILL.md"] = m.group(1).strip() if m else None

    t = read(os.path.join(ctx.root, "AGENTS.md")) or ""
    m = re.search(re.escape(skill) + r"\s+v(\d+\.\d+\.\d+)", t)
    anchors["AGENTS.md"] = m.group(1) if m else None

    t = read(os.path.join(ctx.root, "CHANGELOG.md")) or ""
    # 只认三段式：日期 `2026-10-30` 不含点号，天然不会误命中（§18.1 事故 A 复现）。
    # ⚠ 取标题里**全部** X.Y.Z，并在全文前若干标题里收集候选：标题常夹带引用他处版本
    # （实测 `## 2026-11-14 · 补装「CT 首页」（ct-base §5.2 / v1.4.5 · C7）` 会先吃到
    #  ct-base 的 1.4.5，若只取首个候选会把基准判成别人家版本）。
    cl_cands = []
    for h in re.findall(r"(?m)^##\s+([^\n]+)$", t)[:12]:
        for v in re.findall(r"\bv?(\d+\.\d+\.\d+)\b", h):
            if v not in cl_cands:
                cl_cands.append(v)          # 保持标题自上而下的顺序
    anchors["CHANGELOG.md"] = None
    anchors["_cl_cands"] = cl_cands or None

    anchors["workbench.config.json"] = (ctx.cfg or {}).get("version")

    emb_versions, page_shown = set(), set()
    for fn, text in ctx.pages:
        emb, _err = extract_embed(text)
        if isinstance(emb, dict) and emb.get("version"):
            emb_versions.add(str(emb["version"]))
        # 只取「<skill> vX.Y.Z」展示位；正文历史沿革标注不参与比对
        for v in re.findall(re.escape(skill) + r"\s+v(\d+\.\d+\.\d+)", text):
            page_shown.add(v)
    if emb_versions:
        anchors["html 内嵌版本"] = ",".join(sorted(emb_versions))
    if page_shown:
        anchors["html 版本展示"] = ",".join(sorted(page_shown))

    # CHANGELOG 锚点解歧：与自身其它锚点取交集；交集空 → 不可采信（多半是标题引用了
    # 他技能版本，或标题已不写版本号），记 WARN 后让基准退化为多数票。
    cl = anchors.pop("_cl_cands", None) or []
    others = {v for k, v in anchors.items() if v}
    if cl:
        inter = [v for v in cl if v in others]
        if inter:
            anchors["CHANGELOG.md"] = inter[0]   # 自上而下第一个与自身锚点相符的版本
        elif len(cl) == 1 and not others:
            anchors["CHANGELOG.md"] = cl[0]
        else:
            rep.add("C1 版本锚点一致", WARN,
                    "CHANGELOG 标题版本 %s 与自身其它锚点 %s 不符，未采信" % (cl, sorted(others)),
                    "标题统一写成 `## X.Y.Z · 摘要`，勿在标题内引用他技能版本（§18.1 事故 A）")
    else:
        rep.add("C1 版本锚点一致", WARN, "CHANGELOG 顶部标题未携带版本号",
                "建议 `## X.Y.Z · 摘要`；基准退化为多数票")

    for k, v in list(anchors.items()):
        if v is not None and not VER_RE.match(str(v).strip()):
            anchors[k] = None

    # 基准：CHANGELOG 可用则以它为事实（发布时最后写入的一环）；否则多数票。
    # 多数票避免「单一陈旧锚点把正确值判成不一致」——漂移仍由多数方暴露为 P1。
    truth = anchors.get("CHANGELOG.md")
    if not truth:
        votes = {}
        for k in ("SKILL.md", "workbench.config.json", "AGENTS.md", "html 版本展示", "html 内嵌版本"):
            v = anchors.get(k)
            if v:
                votes[v] = votes.get(v, 0) + 1
        if votes:
            truth = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    if not truth:
        rep.add("C1 版本锚点一致", P1, "无法解析基准版本（CHANGELOG / SKILL.md / config 均无 X.Y.Z）",
                "补 CHANGELOG 顶部 `## X.Y.Z` 或 SKILL.md frontmatter version:")
        return None

    bad = {k: v for k, v in anchors.items() if v is not None and v != truth}
    na = [k for k, v in anchors.items() if v is None]
    if bad:
        rep.add("C1 版本锚点一致", P1,
                "基准=%s 不一致=%s" % (truth, json.dumps(bad, ensure_ascii=False)),
                "python wb_ui_check.py --root %s --set-version %s" % (ctx.root, truth))
    else:
        rep.add("C1 版本锚点一致", OK, "携带版本锚点全部 = %s%s" % (
            truth, ("（N/A: %s）" % ", ".join(na)) if na else ""))

    sv = (ctx.cfg or {}).get("coze") or {}
    if isinstance(sv, dict) and "skill_version" in sv:
        if sv.get("skill_version") != truth:
            rep.add("C1b coze.skill_version", P1, "%s != %s" % (sv.get("skill_version"), truth),
                    "随 --set-version 一并修正")
        else:
            rep.add("C1b coze.skill_version", OK, truth)
    else:
        rep.add("C1b coze.skill_version", OK, "N/A（配置未设 coze.skill_version）")
    return truth


# ── C2 内嵌配置同源 ─────────────────────────────────────────────────────────
def check_embed(ctx, rep):
    if ctx.cfg is None:
        rep.add("C2 内嵌配置同源", P1, "workbench.config.json 缺失或非法 JSON", "配置是唯一真源（§18.2-1）")
        return
    for fn, text in ctx.pages:
        emb, err = extract_embed(text)
        if err:
            rep.add("C2 内嵌配置同源", P1, err, "", fn)
            continue
        if emb is None:
            rep.add("C2 内嵌配置同源", _LEVEL_EMBED_MISSING, "无内嵌配置副本（运行期经 /api/config 读取）",
                    "file:// 直开将无配置兜底；若有意如此，本条保持 WARN", fn)
            continue
        if emb == ctx.cfg:
            rep.add("C2 内嵌配置同源", OK, "内嵌 == workbench.config.json", "", fn)
            continue
        diff = []
        if isinstance(emb, dict):
            for k in sorted(set(emb) | set(ctx.cfg)):
                if emb.get(k) != ctx.cfg.get(k):
                    diff.append("%s: embed=%s / cfg=%s" % (
                        k,
                        json.dumps(emb.get(k), ensure_ascii=False)[:50],
                        json.dumps(ctx.cfg.get(k), ensure_ascii=False)[:50]))
        rep.add("C2 内嵌配置同源", P1, "不同步（file:// 打开会看到陈旧内容）",
                "python wb_ui_check.py --root %s --sync ; %s" % (ctx.root, "; ".join(diff[:3])), fn)


# ── C3 窄屏守卫 ─────────────────────────────────────────────────────────────
def _narrow_bottom_tab_hits(css):
    """窄屏（≤768px）媒体块内，侧栏导航被改为底部固定 Tab 的反模式命中。

    统一规范 §5.6.2（2026-11-15 收敛，范本 ct-safety）：窄屏侧栏须为**顶部横排菜单条**，
    禁止 `position:fixed;bottom:0`（或 `top:auto` 后 `bottom:0`）的「底部 Tab」旧形态。
    """
    hits = []
    for cond, body in media_blocks(css):
        mw = re.search(r"max-width\s*:\s*(\d+)", cond)
        if not mw or int(mw.group(1)) > 768:
            continue
        for rm in re.finditer(
                r"(?:\.wb-side|\.wb-nav)(?:\.[A-Za-z0-9_-]+|\[[^\]]*\])*[^{]*\{[^{}]*\}", body):
            b = rm.group(0)
            if re.search(r"position\s*:\s*fixed", b) and re.search(r"bottom\s*:\s*0", b) \
                    and not re.search(r"top\s*:\s*0(?:\s*px)?", b):
                hits.append(b[:72])
    return hits


def check_responsive(ctx, rep):
    """规则 2 要求「媒体查询内」有方向切换，其余在全文命中即可（家族写法不一）。

    **适用性**：无侧栏的单列页（过渡页 / 只读展示页）不存在「侧栏转横条」「折叠保
    标签」这两条约束，强行套用只会产出无法整改的噪音——故按页面是否有侧栏导航
    （`#wb-side` / `.wb-side` / `.wb-navitem`）决定这两条是否参与判定。
    """
    css = "\n".join(t for _, t in ctx.css) + "\n" + "\n".join(
        m.group(1) for t in [p for _, p in ctx.pages]
        for m in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", t))
    css = blank_comments(css)
    pages_html = "\n".join(t for _, t in ctx.pages)
    has_side = bool(re.search(r'id=["\']wb-side["\']|class=["\'][^"\']*\bwb-side\b|wb-navitem', pages_html))

    side_only = {"INC-2026-10-20-A", "INC-2026-10-20-C"}
    rules = [r for r in RESPONSIVE_RULES if has_side or r[1] not in side_only]

    missing = []
    for pat, rid, why in rules:
        m = re.search(pat, css, re.S if rid == "INC-2026-10-20-A" else 0)
        if m:
            continue
        missing.append((rid, why))
    if missing:
        rep.add("C3 窄屏守卫规则", _LEVEL_C3, "缺 %d 条" % len(missing),
                " | ".join("%s → %s" % (r, w) for r, w in missing))
    else:
        rep.add("C3 窄屏守卫规则", OK,
                "%d 条全部在位%s" % (len(rules), "" if has_side else "（无侧栏页：侧栏两条不适用）"))

    if has_side:
        bt = _narrow_bottom_tab_hits(css)
        if bt:
            rep.add("C3 窄屏守卫规则", _LEVEL_C3, "侧栏窄屏被改为底部 Tab（反模式）",
                    "§5.6.2：窄屏统一为顶部横排菜单条，删除 768px 块内对 .wb-side/.wb-nav 的 "
                    "position:fixed;bottom:0 / top:auto 写法（例如：%s）" % bt[0])


# ── C9 顶栏窄屏触控重声明（§5.2）───────────────────────────────────────────
_TOPBAR_34_RE = re.compile(
    r'\.wb-topbar[^{}]*\{[^{}]*min-height\s*:\s*34px'
    r'|\.wb-lang\{[^{}]*min-height\s*:\s*40px')
_TOPBAR_44_RE = re.compile(
    r'(?:\.wb-btn|\.wb-lang|\.wb-topbar|\.top-actions|\.navitem)[^{}]*\{'
    r'[^{}]*min-(?:height|width)\s*:\s*44px')


def check_topbar_narrow_touch(ctx, rep):
    """桌面顶栏 34px 专属选择器优先级高，窄屏块内必须显式重声明 ≥44px。

    §5.2 的「移动端点击区 ≥44px」是纪律，但 `.wb-topbar .wb-btn{min-height:34px}`
    会压住全局 `.wb-btn` 的窄屏 44px；只在全局写等于没写（ct-registry 实测 390px
    仍是 34px）。仅对确实写了 34px 基线的页面判定，避免无基线技能产生噪音。
    """
    css = "\n".join(t for _, t in ctx.css) + "\n" + "\n".join(
        m.group(1) for t in [p for _, p in ctx.pages]
        for m in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", t))
    css = blank_comments(css)
    if not _TOPBAR_34_RE.search(css):
        rep.add("C9 顶栏窄屏触控", OK, "N/A（无 34px 顶栏专属基线）")
        return
    covered = any(_TOPBAR_44_RE.search(body) for _, body in media_blocks(css))
    if covered:
        rep.add("C9 顶栏窄屏触控", OK, "窄屏块内已重声明 ≥44px（§5.2）")
    else:
        rep.add("C9 顶栏窄屏触控", WARN,
                "桌面 34px 顶栏专属选择器未在窄屏块内重声明 44px",
                "§5.2：在 @media (max-width:768px) 内对 .wb-topbar .wb-btn / .wb-lang 补 min-height:44px")


# ── C4 外链共享 CSS ─────────────────────────────────────────────────────────
def check_css_links(ctx, rep):
    for fn, text in ctx.pages:
        miss = [] if re.search(r'href=["\'][^"\']*tokens\.css', text) else ["tokens.css"]
        # 用到列表组件才要求 wb-list.css（避免对不使用该组件的页面误判）
        if re.search(r"class=[\"'][^\"']*\bwb-list", text) and \
                not re.search(r'href=["\'][^"\']*wb-list\.css', text):
            miss.append("wb-list.css")
        if miss:
            rep.add("C4 生产页外链 CSS", P1, "缺外链: %s" % ", ".join(miss),
                    "预览用内联副本禁止上线——令牌须全家族共享单源（§18.2-3）", fn)
        else:
            rep.add("C4 生产页外链 CSS", OK, "共享 CSS 均为外链", "", fn)

        inline = _INLINE_SHARED_RE.findall(blank_comments(text))
        if inline:
            rep.add("C4 生产页外链 CSS", P1,
                    "内联共享组件副本 %d 处：%s" % (len(inline), inline[:2]),
                    "§18.2-3：改为外链（内联块不随真源升级，已实测落后数个版本）", fn)


# ── C5 无 sibling 依赖 ──────────────────────────────────────────────────────
def check_sibling(ctx, rep):
    hits = []
    for fn, t in ctx.pages + ctx.css + ctx.js:
        for m in _SIBLING_RE.finditer(blank_comments(t)):
            hits.append("%s:%d" % (fn, line_of(t, m.start())))
    if hits:
        rep.add("C5 无兄弟技能依赖", P1, "%d 处 ../ct-* 回退" % len(hits),
                "§5 / §13.16：发布包须自包含，共享件走 publish_inject；%s" % ", ".join(hits[:4]))
    else:
        rep.add("C5 无兄弟技能依赖", OK, "无 ../ct-* 回退")


# ── C6 字号令牌化 ───────────────────────────────────────────────────────────
def check_fs_tokens(ctx, rep):
    tokens = dict(ctx.css).get("tokens.css")
    if tokens is None:
        rep.add("C6a 字号令牌齐备", P1, "tokens.css 缺失",
                "从 ct-base/workbench/tokens.css 取最新版（走 inject_workbench_shared.py）")
        return
    miss = [t for t in FS_TOKENS if (t + ":") not in tokens]
    rep.add("C6a 字号令牌齐备", P1 if miss else OK,
            ("缺 %d 档: %s" % (len(miss), ", ".join(miss))) if miss else "七档 --wb-fs-* 齐备",
            "从 ct-base/workbench/tokens.css 覆盖本技能 tokens.css（共享单源）")

    hits = []
    for fn, t in ctx.pages + ctx.css:
        b = blank_comments(t)
        for h in bare_px_font_size(b, t):
            hits.append("%s:%d" % (fn, line_of(b, h["idx"])))
    rep.add("C6b 无裸 px 字号", P1 if hits else OK,
            ("%d 处 font-size 硬编码像素" % len(hits)) if hits else "全部走 var(--wb-fs-*)",
            "§4.5 梯度映射：24→2xl / 21·20·18→xl / 16·17→lg / 15→base / 14.5·14·13.5→sm / "
            "13·12.5·12→xs / 11.5·11·10.5·10→2xs；%s" % ", ".join(hits[:5]))

    if "font-size:var(--wb-fs-base)" in blank_comments(tokens).replace(" ", ""):
        rep.add("C6c body 基准令牌化", OK, "body 已引用 --wb-fs-base")
    else:
        rep.add("C6c body 基准令牌化", _LEVEL_C6C, "body 未显式引用 --wb-fs-base",
                "tokens.css 的 body{...font-size:var(--wb-fs-base)...}（§4.5 纪律 3）")


# ── C7 返回 CT 首页钮 ──────────────────────────────────────────────────────
def check_cthome(ctx, rep):
    src = "\n".join([t for _, t in ctx.pages] + [t for _, t in ctx.js])
    need = [
        (r'id=["\']wb-cthome["\']', "按钮节点 #wb-cthome"),
        (r"wbGoCtHome\s*[=(]", "跳转函数 wbGoCtHome()"),
        (r"\bCT_HOME\s*=", "目标常量 CT_HOME"),
    ]
    miss = [name for pat, name in need if not re.search(pat, src)]
    if miss:
        rep.add("C7 返回 CT 首页钮", P1, "缺: %s" % ", ".join(miss),
                "§5.2-7 顶栏按钮簇最右端「离开」位：house SVG + <span data-i18n=\"ctHome\">；"
                "I18N 键 ctHome = CT 首页 / CT Home")
        return
    m = re.search(r"CT_HOME\s*=\s*[\"']([^\"']*)[\"']", src)
    if not m:      # 形如 CT_HOME = "" + BASE 的动态赋值 → 无法静态判定，按通过并注明
        rep.add("C7 返回 CT 首页钮", OK, "节点/函数/常量齐备（CT_HOME 动态赋值，未静态校验取值）")
        return
    url = m.group(1)
    if url and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://|^/", url):
        rep.add("C7 返回 CT 首页钮", P1, "CT_HOME 为裸域名: %s" % url,
                "必须带协议（https://…）或写成相对路径；裸域名会被当相对路径解析")
    else:
        rep.add("C7 返回 CT 首页钮", OK, "节点/函数/常量齐备，CT_HOME=%s" % (url or "(空·仅告警不跳转)"))


# §32.1 诊断类可见文案（业务视图内出现即违规）
_DIAG_VISIBLE_RE = re.compile(
    r"能力自检|Capability\s*Health|脚本自检|自检结果|自检状态|接口连通矩阵|构建期断言|"
    r"连通状态矩阵|能力探活", re.I)
# §32.1 反例：JS 建卡后 appendChild 到全局内容容器（对所有视图生效）
_DIAG_APPEND_RE = re.compile(
    r"querySelector\(\s*[\"']\.(?:wb-content|wb-main|content)[\"']\s*\)[\s\S]{0,200}?appendChild|"
    r"appendChild\([\s\S]{0,80}?\)\s*;[^\n]{0,80}wb-card", re.I)
_VIEW_OPEN_RE = re.compile(r"<section[^>]*\bid=[\"']((?:view-|v-)?[^\"']+)[\"'][^>]*>", re.I)


# ── C8 诊断信息收纳（§32.1）─────────────────────────────────────────────────
def check_diagnostics(ctx, rep):
    """把 §32.1 的两条机检口径落地，并对标准后端状态探活做合法例外。

    人工目检仍不可替代：业务结论与技术状态是否混排、数据源清单是否夹带环境回显，
    须逐页判断（本轮人工复核结论见 ct-base/references/workbench_ui.md §32.6）。
    """
    hits = []
    for fn, html in ctx.pages:
        starts = [m.start() for m in _VIEW_OPEN_RE.finditer(html)]
        starts.append(len(html))
        for i in range(len(starts) - 1):
            blk = html[starts[i]:starts[i + 1]]
            m = re.match(r"<section[^>]*\bid=[\"']([^\"']+)", blk)
            vid = m.group(1) if m else "?"
            if re.search(r"(?:^|[-_])about$", vid, re.I):
                continue
            m = _DIAG_VISIBLE_RE.search(blk)
            if m:
                hits.append("%s:%d %s(%s)" % (fn, line_of(html, starts[i] + m.start()), vid, m.group(0)))
    if hits:
        rep.add("C8a 诊断信息不占正文", P1, "%d 处业务视图含诊断类可见文案" % len(hits),
                "§32.1：移入「关于」页并用 <details class=\"wb-disclose\"> 默认折叠；%s" % ", ".join(hits[:4]))
    else:
        rep.add("C8a 诊断信息不占正文", OK, "业务视图无诊断类可见标题")

    append_hits = []
    for fn, text in ctx.pages + ctx.js:
        if _DIAG_APPEND_RE.search(text):
            append_hits.append(fn)
    if append_hits:
        rep.add("C8b 禁全局追加卡片", P1, "检出 appendChild 到全局内容容器: %s" % ", ".join(append_hits),
                "§32.1 反例：该写法对**所有**视图生效，等于每页页尾挂技术噪音")
    else:
        rep.add("C8b 禁全局追加卡片", OK, "无 .wb-content/.wb-main 全局追加")

    # 纯自检路由（/api/capabilities/*）须落在折叠/关于链内；/api/health 属 §5.2
    # 标准后端状态探活（有 #wb-backend pill 或 wbProbeHealth/setConnState），不视为违规。
    probe = [(fn, t) for fn, t in ctx.pages + ctx.js if "/api/capabilities/" in t]
    if not probe:
        rep.add("C8c 自检探活懒加载", OK, "N/A（无 /api/capabilities/* 探活）")
        return
    all_src = "\n".join(t for _, t in ctx.pages + ctx.js)
    lazy = ("addEventListener(\"toggle\"" in all_src or "addEventListener('toggle'" in all_src
            or ".onopen" in all_src or "dataset.loaded" in all_src)
    folded = bool(re.search(r"<details[^>]*class=[\"'][^\"']*wb-disclose", all_src))
    if lazy and folded:
        rep.add("C8c 自检探活懒加载", OK, "折叠块 + 首次展开才探活（§32.3）")
    else:
        rep.add("C8c 自检探活懒加载", _LEVEL_C8_PROBE,
                "有自检路由但未见折叠链%s" % ("" if folded else " / 无 .wb-disclose"),
                "§32.2/32.3：移入「关于」页折叠，用 toggle + dataset.loaded 幂等，首次展开才请求")


# ── C10 / C11 配置形态同源 + 内嵌副本运行期消费（§5.4 / §18.2 / §30.5）──────
def check_config_shape(ctx, rep):
    """config.views / modules[].mount 须与页面真实形态同源。

    实测：7 视图页面因 config 缺 views[] 被 FRAME-REGION 误判为单页，
    档位迁移后该 WARN 升级为 P1 阻断（档位技能强制）。
    """
    if ctx.cfg is None:
        rep.add("C10 配置形态同源", "OK", "N/A（无 workbench.config.json）")
        return
    html = "\n".join(t for _, t in ctx.pages)
    views = ctx.cfg.get("views") or []
    navish = bool(re.search(r'class="[^"]*(?:wb-navitem|wb-side)|id="wb-side"', html))
    viewish = bool(re.search(r'class="[^"]*wb-view|id="view-', html))
    multi = navish or viewish
    if views and not multi:
        rep.add("C10 配置形态同源", "WARN",
                "config.views 声明 %d 项，页面却无视图/导航容器" % len(views),
                "§5.4：views[] 须与页面形态同源，否则 FRAME-REGION 按错误形态判定。")
    elif not views and multi:
        rep.add("C10 配置形态同源", "WARN",
                "页面为多视图形态，但 config 缺 views[]",
                "FRAME-REGION 会误判为单页四区；档位迁移后该 WARN 升级为 P1。")
    else:
        rep.add("C10 配置形态同源", "OK",
                "views=%d / 页面形态=%s" % (len(views), "多视图" if multi else "单页"))
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    bad = sorted({m.get("mount") for m in (ctx.cfg.get("modules") or [])
                  if isinstance(m, dict) and m.get("mount") and m["mount"] not in ids})
    rep.add("C10b 模块挂载点存在", "WARN" if bad else "OK",
            "指向不存在 id 的 mount: %s" % ", ".join(bad) if bad else "全部 mount 均有对应节点",
            "§30.5 配置同源：modules[].mount 应指向页面真实挂载点。" if bad else "")


def check_embed_consumed(ctx, rep):
    """§18.2-1 的深度相等只保证副本存在；本项校验加载链是否真的读取它。"""
    html = "\n".join(t for _, t in ctx.pages)
    js = "\n".join(t for _, t in ctx.js)
    has_script = bool(re.search(r'<script[^>]*id=["\']wb-config["\']', html))
    if not has_script:
        rep.add("C11 内嵌配置运行期消费", "OK", "N/A（非 #wb-config 形态，由 C2 管辖）")
        return
    consumed = bool(re.search(
        r"(?:getElementById|querySelector)\(\s*['\"]#?wb-config['\"]|#wb-config",
        html + "\n" + js))
    rep.add("C11 内嵌配置运行期消费", "OK" if consumed else "WARN",
            "配置加载链已读取 #wb-config" if consumed else "有内嵌副本但加载链未读取",
            "" if consumed else "§18.2-1：副本若不被 wbLoadConfig() 消费只是过机检的死数据；"
            "/api/config 404 或 file:// 直开仍会掉回硬编码兜底。")


# ── 修复动作（--sync / --set-version）──────────────────────────────────────
def _write(path, s):
    try:
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    except PermissionError:
        raise SystemExit("[write] 目标只读：%s\n[write] 请用 --root <可写副本> 生成修正副本再覆盖。" % path)


def do_sync(ctx):
    if ctx.cfg is None:
        print("[sync] workbench.config.json 缺失/非法，放弃")
        return False
    payload = json.dumps(ctx.cfg, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    done = 0
    for fn, text in ctx.pages:
        replaced = None
        for mk in _EMBED_MARKERS:
            i = text.find(mk)
            if i < 0:
                continue
            try:
                _, end = json.JSONDecoder().raw_decode(text, i + len(mk))
            except ValueError:
                continue
            replaced = text[: i + len(mk)] + payload + text[end:]
            break
        if replaced is None:
            # 第四代写法：<script id="wb-config" type="application/json">{…}</script>
            m = re.search(r'(<script[^>]*id=["\']wb-config["\'][^>]*>)([\s\S]*?)(</script>)', text)
            if m:
                replaced = text[:m.start(2)] + "\n" + payload + "\n" + text[m.end(2):]
        if replaced is None:
            continue
        _write(os.path.join(ctx.wb, fn), replaced)
        print("[sync] %s 内嵌配置已按 workbench.config.json 重写" % fn)
        done += 1
    if not done:
        print("[sync] 未找到内嵌配置声明（WB_CONFIG_EMBED / CFG_EMBED / #wb-config），无需同步")
    return True


def do_set_version(ctx, ver):
    if not VER_RE.match(ver):
        print("[version] 非法版本号（须 X.Y.Z）: %s" % ver)
        return False
    cur = (ctx.cfg or {}).get("version") or ""
    if VER_RE.match(str(cur)):
        a = [int(x) for x in str(cur).split(".")]
        b = [int(x) for x in ver.split(".")]
        if b < a:
            print("[version] ⚠ 目标 %s 低于当前 config.version %s —— 确认不是把新版本回退成旧值"
                  "（锚点冲突时先判断哪一侧才是最新，再决定改哪一侧）" % (ver, cur))
    changed = []
    cfg = dict(ctx.cfg or {})
    if cfg.get("version") != ver:
        cfg["version"] = ver
        changed.append("workbench.config.json.version")
    if isinstance(cfg.get("coze"), dict) and cfg["coze"].get("skill_version") != ver:
        cfg["coze"]["skill_version"] = ver
        changed.append("workbench.config.json.coze.skill_version")
    _write(ctx.cfg_path, json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")

    safe = re.escape(ctx.skill)
    for fn, text in ctx.pages:
        new, n = re.subn(safe + r"(\s+v)\d+\.\d+\.\d+", r"%s\g<1>%s" % (ctx.skill, ver), text)
        if n:
            _write(os.path.join(ctx.wb, fn), new)
            changed.append("%s 版本展示 ×%d" % (fn, n))

    for name in ("AGENTS.md", "SKILL.md"):
        p = os.path.join(ctx.root, name)
        t = read(p)
        if t is None:
            continue
        if name == "SKILL.md":
            t2 = re.sub(r"(^\s*version:\s*)\S+", r"\g<1>" + ver, t, count=1, flags=re.M)
        else:
            t2 = re.sub(safe + r" v[\d.]+", "%s v%s" % (ctx.skill, ver), t, count=1)
        if t2 != t:
            _write(p, t2)
            changed.append(name)

    print("[version] 已设为 %s；机械改动: %s" % (ver, ", ".join(changed) or "无"))
    print("[version] ⚠ CHANGELOG.md 正文需人工补 `## %s` 章节（本脚本不改发布说明）" % ver)
    ctx.cfg = cfg
    return True


# ── 汇总 ────────────────────────────────────────────────────────────────────
def run_one(root):
    ctx = Ctx(root)
    rep = Report(ctx.skill, ctx.exempt())
    if not ctx.pages:
        rep.add("FRAME-PAGE", P1, "workbench/ 下未找到可检查的 html 页面", "确认 --root 指向技能根")
        return rep
    check_version(ctx, rep)
    check_embed(ctx, rep)
    check_responsive(ctx, rep)
    check_topbar_narrow_touch(ctx, rep)
    check_css_links(ctx, rep)
    check_sibling(ctx, rep)
    check_fs_tokens(ctx, rep)
    check_cthome(ctx, rep)
    check_diagnostics(ctx, rep)
    check_config_shape(ctx, rep)
    check_embed_consumed(ctx, rep)
    return rep


def print_report(rep):
    print("=" * 78)
    print("%s 工作台结构闸门 C1–C9（ct-base §18.3）" % rep.skill)
    print("=" * 78)
    for it in rep.items:
        loc = (" [%s]" % it["loc"]) if it.get("loc") else ""
        print("  [%-4s] %-22s %s%s" % (it["level"], it["check"], it["msg"], loc))
        if it["level"] in (P1, WARN) and it["hint"]:
            print("         ↳ %s" % it["hint"])
    nfail = len(rep.failed)
    nwarn = len([i for i in rep.items if i["level"] == WARN])
    print("-" * 78)
    print("P1: %d ｜ WARN: %d ｜ 结论：%s" % (
        nfail, nwarn, "阻断发布" if nfail else ("可发布（有建议项）" if nwarn else "全绿 ✅")))


def main(argv=None):
    ap = argparse.ArgumentParser(description="ct- 工作台结构闸门 C1–C9 共享机检")
    ap.add_argument("--root", help="技能根目录（默认=ct-base 自身）")
    ap.add_argument("--all", action="store_true", help="扫描 ct-base 同级全部 ct-* 技能")
    ap.add_argument("--sync", action="store_true", help="按 config.json 重写内嵌配置副本")
    ap.add_argument("--set-version", metavar="X.Y.Z", help="机械对齐全部版本锚点")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args(argv)

    ctbase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roots = []
    if args.all:
        parent = os.path.dirname(ctbase)
        for fn in sorted(os.listdir(parent)):
            p = os.path.join(parent, fn)
            # ct-base 自身是共享件真源（workbench/ 下只有 template + schema，无 config），
            # 不适用叶技能闸门；仅显式 --root 时才检查它。
            if fn == "ct-base":
                continue
            if fn.startswith("ct-") and os.path.isdir(os.path.join(p, "workbench")):
                roots.append(p)
    else:
        roots = [args.root or ctbase]

    reports = []
    for r in roots:
        ctx = Ctx(r)
        if args.set_version:
            do_set_version(ctx, args.set_version)
        if args.sync:
            do_sync(ctx)
        reports.append(run_one(r))

    if args.json:
        items = [i for rep in reports for i in rep.items]
        print(json.dumps({"reports": [{"skill": r.skill, "worst": r.worst,
                                       "items": r.items} for r in reports],
                          "p1": len([i for i in items if i["level"] == P1])},
                         ensure_ascii=False, indent=2))
        return 1 if any(r.failed for r in reports) else 0

    if args.all:
        print("%-16s %-6s %-6s %s" % ("技能", "P1", "WARN", "主要问题"))
        for rep in reports:
            p1 = [i for i in rep.items if i["level"] == P1]
            wn = [i for i in rep.items if i["level"] == WARN]
            brief = "; ".join("%s(%s)" % (i["check"].split()[0], i["msg"][:34]) for i in (p1 or wn)[:2])
            print("%-16s %-6d %-6d %s" % (rep.skill, len(p1), len(wn), brief))
        print("-" * 78)
        tot = sum(len(r.failed) for r in reports)
        print("合计 P1: %d ｜ 技能: %d" % (tot, len(reports)))
        return 1 if tot else 0

    print_report(reports[0])
    return 1 if reports[0].failed else 0


if __name__ == "__main__":
    sys.exit(main())
