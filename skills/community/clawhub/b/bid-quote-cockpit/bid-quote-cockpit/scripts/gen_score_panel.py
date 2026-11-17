#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_score_panel.py —— 看板「评委打分」区块生成器（配置驱动，通用无项目信息）

用途
    把评委打分**永久固化**进看板 HTML，使线下 / 云端 / 任何设备打开结果完全一致，
    并驱动「综合评分表 + 首屏推荐卡」的分数与名次。

    解决的老问题
        · 打分写在 localStorage → 浏览器按 origin 隔离，`file://` 与 `https://` 互不相通，
          别人电脑打开是空表，页面回退到静态基线，**显示出来的分数和评委实际打分不一致**。
        · 固化后彻底绕开该问题：分数随 HTML 字节走，任何设备一致；页面不提供修改入口。

用法
    python gen_score_panel.py --config ./score_config.json --out ./score_panel.html --report

    产物为两段（由 --split 控制）：
        score_panel.html        : 可直接 <details> 包住插入看板的完整区块（CSS + 表格 + JS）
        score_panel.meta.json   : 供主看板生成器读取的元数据（各维度满分 / 有效平均 / 校验结果）

    若要直接主看板可用，推荐 `--mode fragment`（默认）：输出不含 <html>/<body>，
    由调用方注入到既有看板的 `<style>` 与 `<script>` 段中。

数据契约见 ../references/score-panel-contract.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]

C_STEEL = "#3E6E9E"
C_INK = "#1F2A36"
C_SUB = "#5A6B7C"
C_LINE = "#E3EAF1"

_ROLE_ORDER_DEFAULT = ["采购", "设计", "零售", "零售", "销售"]


# --------------------------------------------------------------------------
# 配置装载与校验
# --------------------------------------------------------------------------
class CfgError(Exception):
    pass


def load_config(path):
    p = Path(path)
    if not p.is_file():
        raise CfgError("配置文件不存在: %s" % p)
    try:
        cfg = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise CfgError("配置不是合法 JSON: %s" % e)

    # —— 供应商 ——
    vendors = cfg.get("vendors")
    if not isinstance(vendors, list) or not vendors:
        raise CfgError("config.vendors 必须是非空数组")
    for i, v in enumerate(vendors):
        if not isinstance(v, dict):
            raise CfgError("vendors[%d] 必须是对象" % i)
        for k in ("name", "code"):
            if not str(v.get(k) or "").strip():
                raise CfgError("vendors[%d] 缺少 %s" % (i, k))
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", str(v["code"])):
            raise CfgError("vendors[%d].code 只能是「字母开头 + 字母数字下划线」：%s" % (i, v["code"]))
        v.setdefault("short", v["name"])
    codes = [v["code"] for v in vendors]
    if len(set(codes)) != len(codes):
        raise CfgError("vendors[].code 有重复：%s" % codes)

    # —— 维度 ——
    dims = cfg.get("dims")
    if not isinstance(dims, list) or not dims:
        raise CfgError("config.dims 必须是非空数组")
    for i, d in enumerate(dims):
        if not isinstance(d, dict):
            raise CfgError("dims[%d] 必须是对象" % i)
        for k in ("key", "code", "max"):
            if k not in d:
                raise CfgError("dims[%d] 缺少 %s" % (i, k))
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", str(d["code"])):
            raise CfgError("dims[%d].code 只能是「字母开头 + 字母数字下划线」：%s" % (i, d["code"]))
        if not isinstance(d["max"], (int, float)) or d["max"] <= 0:
            raise CfgError("dims[%d].max 必须是正数" % i)
        d.setdefault("weight", d["max"])
    dkeys = [d["key"] for d in dims]
    if len(set(dkeys)) != len(dkeys):
        raise CfgError("dims[].key 有重复")

    # —— 评委 ——
    judges = cfg.get("judges")
    if not isinstance(judges, list) or not judges:
        raise CfgError("config.judges 必须是非空数组（每位评委一行）")
    if len(judges) % 2 == 0:
        # 仅提示，不阻断：某些项目允许偶数评委（此时不取中位，只取算术平均）
        cfg["_even_judges_warning"] = (
            "评委人数为偶数（%d），有效平均仍按算术平均计算；若项目评审规则要求奇数评委，请补充或调整。"
            % len(judges)
        )
    cfg.setdefault("max_judges", len(judges))

    # —— 权重与固定分（用于算综合分）——
    wsum = sum(float(d["weight"]) for d in dims)
    cfg["_team_weight_sum"] = wsum

    return cfg


def build_seed(cfg):
    """把 judges 转成页面 seed 结构 {scores:[{name,role,<vendorCode>_<dimCode>:int}], savedAt}"""
    vendors = cfg["vendors"]
    dims = cfg["dims"]
    roles = cfg.get("roles") or _ROLE_ORDER_DEFAULT
    rows, problems = [], []

    for ji, j in enumerate(cfg["judges"]):
        if not isinstance(j, dict):
            raise CfgError("judges[%d] 必须是对象" % ji)
        name = str(j.get("name") or "").strip()
        role = str(j.get("role") or (roles[ji] if ji < len(roles) else "")).strip()
        row = {"name": name, "role": role}
        for v in vendors:
            for d in dims:
                k = "%s_%s" % (v["code"], d["code"])
                val = j.get(k)
                if val is None:
                    row[k] = None
                    problems.append("第 %d 位评委「%s」缺少 %s.%s（%s）→ 置空，该格不计入有效平均"
                                    % (ji + 1, name or role, v["name"], d["key"], k))
                    continue
                if isinstance(val, bool) or not isinstance(val, (int, float)):
                    problems.append("第 %d 位评委「%s」的 %s 非数值（%r）→ 置空" % (ji + 1, name, k, val))
                    row[k] = None
                    continue
                if float(val) != int(val):
                    problems.append("第 %d 位评委「%s」的 %s 不是整数（%r）→ 置空" % (ji + 1, name, k, val))
                    row[k] = None
                    continue
                ival = int(val)
                if ival < 0 or ival > d["max"]:
                    problems.append("第 %d 位评委「%s」的 %s = %d 超出 0~%s → 置空"
                                    % (ji + 1, name, k, ival, d["max"]))
                    row[k] = None
                    continue
                row[k] = ival
        rows.append(row)

    return {"scores": rows, "savedAt": str(cfg.get("scored_at") or "").strip() or None}, problems


def effective_avg(seed, cfg):
    """(vendorName, dimKey) -> 有效平均 或 None；有效 = 姓名非空 + 该格为 0~max 整数"""
    out = {}
    dims = cfg["dims"]
    for v in cfg["vendors"]:
        for d in dims:
            k = "%s_%s" % (v["code"], d["code"])
            vals = [r[k] for r in seed["scores"]
                    if str(r.get("name") or "").strip() and isinstance(r.get(k), int)]
            out[(v["name"], d["key"])] = (sum(vals) / len(vals)) if vals else None
    return out


def composite(cfg, seed, avg):
    """
    综合分 = 价格分(业务侧另给) + 其他分
    其他分 = 固定分项（经验/及时性/完整性… 由 cfg.other_fixed 给）
             + 各「打分维度」的有效平均（维度不在 other_fixed 里的）
    本函数只算「由打分驱动的部分」，价格分与固定分缺省时返回 None（由调用方补齐）。
    """
    res = {}
    for v in cfg["vendors"]:
        name = v["name"]
        fixed = (cfg.get("other_fixed") or {}).get(name)
        team = 0.0
        missing = []
        for d in cfg["dims"]:
            a = avg.get((name, d["key"]))
            if a is None:
                missing.append(d["key"])
                continue
            team += a
        res[name] = {
            "team_avg_sum": round(team, 2),
            "missing_dims": missing,
            "fixed_other": fixed,
            "other_total": (None if fixed is None else round(float(fixed) + team, 2)),
            "price_score": (cfg.get("price_score") or {}).get(name),
        }
        ps = res[name]["price_score"]
        res[name]["composite"] = (None if (ps is None or res[name]["other_total"] is None)
                                  else round(float(ps) + res[name]["other_total"], 2))
    order = sorted([v for v in res if res[v]["composite"] is not None],
                   key=lambda x: -res[x]["composite"])
    for i, v in enumerate(order):
        res[v]["rank"] = i + 1
    for v in res:
        res[v].setdefault("rank", None)
    return res, order


# --------------------------------------------------------------------------
# HTML / JS 渲染
# --------------------------------------------------------------------------
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


CSS = """/* ── 评委打分区块（固化只读）─────────────────────────────────────
   设计要点：面板在「已固化」模式下**不得包含任何 input/select/button/textarea**，
   否则校验器会把「可修改」判为真。表格用 table-layout:fixed + colgroup 控宽，
   避免「岗位/姓名」被全局 td{white-space:nowrap} 撑破卡片。 */
.sp-panel{margin-top:6px}
.sp-rulesbox{border:1px dashed #C3D2DF;border-radius:10px;background:#F8FBFD;padding:13px 16px;font-size:12.5px;line-height:1.9;color:var(--sub,#5A6B7C)}
.sp-rulesbox b{color:var(--ink,#1F2A36)}
.sp-tablewrap{margin-top:12px;overflow-x:auto}
.sp-table{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;background:#fff;
  border:1px solid #E3EAF1;border-radius:10px;overflow:hidden;font-size:12px}
.sp-table th,.sp-table td{padding:7px 8px;border-bottom:1px solid #EDF2F7;text-align:left;
  white-space:normal;word-break:break-word;overflow-wrap:anywhere}
.sp-table thead th{background:#F4F8FB;color:#1F2A36;font-weight:800;text-align:center;white-space:nowrap}
.sp-table thead tr.sp-h1 th{font-size:12.5px;letter-spacing:.2px}
.sp-table thead tr.sp-h2 th{font-size:11px;color:#5A6B7C;font-weight:700}
.sp-table td.sp-num{text-align:center;font-variant-numeric:tabular-nums}
.sp-table tbody tr:hover td{background:#FAFCFE}
.sp-table tr.sp-avgrow td{background:#F4F8FB;font-weight:800;color:#1F2A36;border-top:2px solid #D7E2EB;border-bottom:none}
.sp-table tr.sp-avgrow td.sp-num{color:#2E6B4F}
.sp-note{margin-top:11px;font-size:12px;line-height:1.9;color:#5A6B7C}
.sp-note b{color:#1F2A36}
.sp-badge{display:inline-block;font-size:11.5px;font-weight:800;border-radius:12px;padding:2px 11px;white-space:nowrap}
.sp-badge.ok{background:#EAF5EF;color:#2E6B4F;border:1px solid #CBE4D6}
.sp-badge.warn{background:#FBEEE4;color:#B05A2A;border:1px solid #EFD3BE}
.sp-foldmeta{display:inline-block;font-size:10.5px;font-weight:700;color:#5A6B7C;background:#F1F5F9;
  border-radius:10px;padding:2px 9px;margin-left:9px;vertical-align:2px;white-space:nowrap}
"""


def render_html(cfg, seed, problems):
    vendors = cfg["vendors"]
    dims = cfg["dims"]
    rows = seed["scores"]
    njudge = len([r for r in rows if str(r.get("name") or "").strip()])
    label = cfg.get("score_label") or "评委最终打分"
    vn = len(vendors)
    nd = len(dims)

    cg = ['<colgroup><col style="width:44px"><col style="width:88px"><col style="width:150px">']
    for _ in dims:
        for _v in vendors:
            cg.append('<col style="width:64px">')
    cg.append("</colgroup>")
    cg = "".join(cg)

    h = []
    h.append('<div class="sp-panel" id="scorePanel">')
    h.append('<div class="sp-rulesbox" id="scoreRulesBox">')
    h.append('<b>%s：</b>共 <b>%d</b> 位评委，对 <b>%d</b> 家单位 × <b>%d</b> 个维度'
             '（%s）逐格打分，共 <b>%d</b> 个整数分。'
             % (esc(label), njudge, vn, nd,
                "、".join("%s 0~%s" % (d["key"], d["max"]) for d in dims), njudge * vn * nd))
    h.append('打分随看板构建内置，<b>线下 / 云端 / 任何设备打开均为同一结果</b>；'
             '本页不提供修改、保存、清空入口。如需改分，由采购更新构建种子后重新生成并发布。</div>')

    h.append('<div class="sp-tablewrap"><table class="sp-table">%s<thead>' % cg)
    h.append('<tr class="sp-h1"><th rowspan="2">序号</th><th rowspan="2">岗位</th><th rowspan="2">姓名</th>')
    for d in dims:
        h.append('<th colspan="%d">%s（0~%s 分）</th>' % (vn, esc(d["key"]), d["max"]))
    h.append('</tr><tr class="sp-h2">')
    for _d in dims:
        for v in vendors:
            h.append('<th>%s</th>' % esc(v["short"]))
    h.append("</tr></thead><tbody>")

    for si, r in enumerate(rows):
        h.append("<tr><td class=\"sp-num\">%d</td><td>%s</td><td style=\"font-weight:700\">%s</td>"
                 % (si + 1, esc(r.get("role") or ""), esc(r.get("name") or "")))
        for d in dims:
            for v in vendors:
                val = r.get("%s_%s" % (v["code"], d["code"]))
                h.append('<td class="sp-num">%s</td>' % ("—" if val is None else val))
        h.append("</tr>")

    avg = effective_avg(seed, cfg)
    h.append('<tr class="sp-avgrow"><td colspan="3">有效平均（共 %d 人有效 · 已计入综合评分表）</td>' % njudge)
    for d in dims:
        for v in vendors:
            a = avg.get((v["name"], d["key"]))
            h.append('<td class="sp-num">%s</td>' % ("—" if a is None else "%.2f" % a))
    h.append("</tr></tbody></table></div>")

    comp, order = composite(cfg, seed, avg)
    if order:
        h.append('<div class="sp-note"><b>按上述有效平均算出的综合分（价格分 + 固定分项 + 打分维度）：</b>')
        for v in order:
            c = comp[v]
            h.append('<br>· 第 %d 名 <b>%s</b>：%s（价格分 %s + 其他 %s）'
                     % (c["rank"], esc(v), c["composite"],
                        c["price_score"], c["other_total"]))
        h.append("</div>")

    if problems:
        h.append('<div class="sp-note"><span class="sp-badge warn">配置告警 %d 条</span> ' % len(problems))
        h.append("；".join(esc(p) for p in problems[:12]))
        if len(problems) > 12:
            h.append(" 等 %d 条" % len(problems))
        h.append("</div>")

    h.append("</div>")
    return "\n".join(h), avg, comp, order


def render_js(cfg, seed, label):
    """生成内联 JS：把 seed 注入页面并让 9.3 主表 / 首屏卡走「有效平均」口径。"""
    payload = json.dumps(seed, ensure_ascii=False)
    dims_js = json.dumps([{"key": d["key"], "code": d["code"], "max": d["max"]} for d in dims_flat(cfg)],
                         ensure_ascii=False)
    code_map = json.dumps({v["name"]: v["code"] for v in cfg["vendors"]}, ensure_ascii=False)
    return f"""<script>
/* ── 评委打分固化注入（由 gen_score_panel.py 生成，勿手改）──────────────
   机制：window.__SCORE_SEED__ 随 HTML 字节走 → 任何设备打开都是同一批分数。
   页面**只读**：不探测、不写入 localStorage，也不提供打分码入口。 */
window.__SCORE_SEED__={payload};
window.__SCORE_META__={{"dims":{dims_js},"vendorCode":{code_map},"label":{json.dumps(label, ensure_ascii=False)}}};
(function(){{
  var M=window.__SCORE_META__, S=window.__SCORE_SEED__;
  function fieldKey(vendor,dimCode){{ return M.vendorCode[vendor]+'_'+dimCode; }}
  /* 有效平均：(单位 × 维度) —— 姓名非空 且 该格为 0~max 整数 */
  window.scoreAvg=function(dimKey,vendor){{
    var dim=null;
    for(var i=0;i<M.dims.length;i++) if(M.dims[i].key===dimKey) dim=M.dims[i];
    if(!dim) return null;
    var k=fieldKey(vendor,dim.code), vals=[];
    S.scores.forEach(function(s){{
      var v=s[k];
      if((s.name||'').trim()!=='' && typeof v==='number' && !isNaN(v) && v>=0 && v<=dim.max && Math.floor(v)===v) vals.push(v);
    }});
    if(!vals.length) return null;
    var sum=0; vals.forEach(function(v){{sum+=v;}});
    return sum/vals.length;
  }};
  window.scoreFrozen=true;
  window.scoreJudges=S.scores.filter(function(s){{return (s.name||'').trim()!=='';}}).length;
  /* 若主看板定义了刷新入口，则在 DOM 就绪后触发一次（分数已在 seed 里，无需用户操作） */
  function kick(){{
    try{{ if(typeof refreshAllViews==='function') refreshAllViews(); }}catch(e){{}}
    try{{ if(typeof renderTeamPanel==='function') renderTeamPanel(); }}catch(e){{}}
  }}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',kick); else kick();
}})();
</script>"""


def dims_flat(cfg):
    return cfg["dims"]


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="看板评委打分区块生成器（固化只读）")
    ap.add_argument("--config", required=True, help="score_config.json 路径")
    ap.add_argument("--out", default="./score_panel.html", help="HTML 片段输出路径")
    ap.add_argument("--meta", default=None, help="元数据 JSON 输出路径（默认与 --out 同名 .meta.json）")
    ap.add_argument("--report", action="store_true", help="打印核查报表")
    args = ap.parse_args()

    cfg = load_config(args.config)
    seed, problems = build_seed(cfg)
    html, avg, comp, order = render_html(cfg, seed, problems)
    js = render_js(cfg, seed, cfg.get("score_label") or "评委最终打分")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html + "\n\n" + js + "\n", encoding="utf-8")

    meta_path = Path(args.meta) if args.meta else out.with_suffix(".meta.json")
    meta = {
        "score_label": cfg.get("score_label") or "评委最终打分",
        "judges": len([r for r in seed["scores"] if str(r.get("name") or "").strip()]),
        "vendors": [v["name"] for v in cfg["vendors"]],
        "dims": [{"key": d["key"], "max": d["max"], "weight": d["weight"]} for d in cfg["dims"]],
        "max_judges": cfg.get("max_judges"),
        "team_weight_sum": cfg.get("_team_weight_sum"),
        "effective_avg": {"%s|%s" % (k[0], k[1]): (None if v is None else round(v, 4))
                          for k, v in avg.items()},
        "composite": comp,
        "rank_order": order,
        "problems": problems,
        "warnings": [w for w in [cfg.get("_even_judges_warning")] if w],
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.report:
        print("=" * 68)
        print("评委打分固化 —— 核查报表")
        print("=" * 68)
        print("评委：%d 位 / 上限 %s" % (meta["judges"], meta["max_judges"]))
        print("单位：%d 家  %s" % (len(meta["vendors"]), "、".join(meta["vendors"])))
        print("维度：%d 个  %s" % (len(cfg["dims"]),
                                  "、".join("%s(0~%s,权重%s)" % (d["key"], d["max"], d["weight"])
                                            for d in cfg["dims"])))
        print("打分维度权重合计：%s" % cfg.get("_team_weight_sum"))
        print("-" * 68)
        for v in meta["vendors"]:
            c = comp.get(v, {})
            print("%-14s 维度均值和 %-6s 固定分项 %-6s 其他合计 %-6s 价格分 %-6s 综合 %-7s 名次 %s"
                  % (v, c.get("team_avg_sum"), c.get("fixed_other"), c.get("other_total"),
                     c.get("price_score"), c.get("composite"), c.get("rank")))
            if c.get("missing_dims"):
                print("               ⚠ 缺有效打的维度：%s" % "、".join(c["missing_dims"]))
        print("-" * 68)
        if meta["warnings"]:
            for w in meta["warnings"]:
                print("警告: %s" % w)
        if problems:
            print("配置告警 %d 条：" % len(problems))
            for p in problems:
                print("  · %s" % p)
        else:
            print("配置告警: 无")
        print("-" * 68)
        print("HTML 片段 → %s" % out)
        print("元数据     → %s" % meta_path)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CfgError as e:
        print("配置错误: %s" % e, file=sys.stderr)
        raise SystemExit(2)
