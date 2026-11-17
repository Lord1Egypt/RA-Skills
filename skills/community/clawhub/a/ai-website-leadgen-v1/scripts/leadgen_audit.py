#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站获客（CRO / 转化漏斗）审计脚本 — 零第三方依赖（仅需 Python 3.8+ 标准库）。

分析单个 URL（或本地 HTML 文件）的公开页面，输出结构化获客信号报告（JSON）：
  - 各阶段分（landing / cta / contact / form / trust，0-100）
  - 整站获客分 leadgen_score（0-100，加权）
  - 原始信号（CTA 列表、表单字段、联系方式、信任信号）
  - 优化建议（stage / risk / issue / recommendation / fix）

不执行 JS、不渲染 SPA；仅分析服务端返回的 HTML。
用法：
  python leadgen_audit.py audit --url https://example.com --out report.json
  python leadgen_audit.py audit --url https://example.com --file page.html --out report.json
  python leadgen_audit.py score --report report.json --out scored.json
"""
import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.error
import urllib.parse
import ssl
from html.parser import HTMLParser
from http.client import IncompleteRead

UA = "Mozilla/5.0 (compatible; YunZhiLeadGen/1.0)"
REQUEST_DELAY = 2.0  # 相邻请求最小间隔（秒），也是脚本内部下限

# CTA 关键词（出现即视为候选 CTA）
CTA_KEYWORDS = ["免费", "获取", "报价", "咨询", "立即", "申请", "下载", "联系", "预约",
                "提交", "试用", "演示", "方案", "购买", "领取", "开通", "注册", "了解更多",
                "马上", "现在", "询价", "订阅", "加入", "开始", "体验"]
# 强动作导向（用于判断文案质量）
ACTION_KEYWORDS = ["免费", "获取", "报价", "咨询", "预约", "申请", "下载", "立即", "试用",
                   "演示", "领取", "开通", "注册", "询价", "订阅", "体验", "开始", "马上", "现在"]

TRUST_KEYWORDS = ["认证", "证书", "资质", "荣誉", "客户", "案例", "iso", "ce", "专利",
                  "合作", "伙伴", "好评", "评价", "口碑", "满意", "权威", "认证", "license", "certified"]

CONTACT_PATTERNS = {
    "phone": re.compile(r'(?:\+?86[-\s]?)?1[3-9]\d{9}|0\d{2,3}[-\s]?\d{7,8}'),
    "email": re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    "whatsapp": re.compile(r'whatsapp', re.I),
    "wechat": re.compile(r'微信|wechat|weixin', re.I),
    "address": re.compile(r'(地址|位于|总部|大厦|园区|路\d|号\d|省|市).{0,40}(号|室|层|栋|区)'),
}


def _norm_url(u):
    p = urllib.parse.urlparse(u)
    return f"{p.scheme}://{p.netloc}"


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        raw = r.read()
        try:
            html = raw.decode("utf-8", errors="replace")
        except Exception:
            html = raw.decode("gbk", errors="replace")
        return html


def crawl(start_url, max_pages=20, depth=3, delay=REQUEST_DELAY):
    """BFS 抓取同域页面，返回 (html_by_url, list_of_urls)。"""
    delay = max(delay, REQUEST_DELAY)
    seen = set()
    q = [(start_url, 0)]
    htmls = {}
    order = []
    while q and len(htmls) < max_pages:
        url, d = q.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html = fetch(url)
        except Exception as e:
            sys.stderr.write(f"[warn] fetch failed {url}: {e}\n")
            continue
        htmls[url] = html
        order.append(url)
        if d >= depth:
            continue
        for link in _extract_links(html, url):
            if link not in seen:
                q.append((link, d + 1))
    return htmls, order


def _extract_links(html, base):
    out = []
    base_net = _norm_url(base)
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']', html, re.I):
        href = m.group(1).strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
            continue
        absurl = urllib.parse.urljoin(base, href)
        if _norm_url(absurl) == base_net:
            out.append(absurl)
    return out


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.metas = {}
        self.h1 = []
        self._in_h1 = False
        self.a_tags = []          # (text, href)
        self.buttons = []         # text
        self.submit_inputs = []   # <input type=submit/image> 的 value
        self.forms = []           # dicts
        self._cur_form = None
        self._form_depth = 0
        self._text = []
        self._in_head = True
        self._head_text = []
        self._body_text_len = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "head":
            self._in_head = True
        elif tag == "body":
            self._in_head = False
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            content = a.get("content", "")
            if name:
                self.metas[name] = content
            if a.get("charset"):
                pass
        elif tag == "a":
            self.a_tags.append(("", a.get("href", "")))
        elif tag == "button":
            self.buttons.append("")
        elif tag == "form":
            self._cur_form = {
                "fields": [], "submit_text": "", "has_file": False,
                "has_validation": False, "action_copy": "",
            }
            self._form_depth += 1
            self.forms.append(self._cur_form)
        elif tag in ("input", "textarea", "select") and self._cur_form is not None:
            ftype = (a.get("type") or "text").lower()
            if tag == "input" and ftype in ("file",):
                self._cur_form["has_file"] = True
            if ftype in ("submit", "image") or (tag == "button"):
                # submit handled in data
                pass
            required = a.get("required") is not None or a.get("isrequire") == "1"
            vt = a.get("validatetype")
            if vt or required:
                self._cur_form["has_validation"] = True
            if ftype in ("hidden", "submit", "image", "button"):
                if ftype in ("submit", "image"):
                    self.submit_inputs.append(a.get("value", ""))
                pass
            else:
                self._cur_form["fields"].append({
                    "type": ftype, "name": a.get("name", ""),
                    "required": required, "validatetype": vt,
                    "placeholder": a.get("placeholder", ""),
                })
        elif tag == "img":
            alt = a.get("alt", "")
            self._text.append(alt)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "head":
            self._in_head = False
        elif tag == "form":
            self._form_depth = max(0, self._form_depth - 1)
            if self._form_depth == 0:
                self._cur_form = None

    def handle_data(self, data):
        txt = data
        if self._in_title:
            self.title += txt
        if self._in_h1:
            self.h1.append(txt)
        # accumulate into last a/button if open (approx: attach to the most recent)
        t = txt.strip()
        if not t:
            return
        self._text.append(t)
        if self._in_head:
            self._head_text.append(t)
        else:
            self._body_text_len += len(t)
        # attach to last a/button text (best-effort)
        if self.a_tags and self.a_tags[-1][0] == "" and not self._in_head:
            self.a_tags[-1] = (t, self.a_tags[-1][1])
        elif self.buttons and self.buttons[-1] == "" and not self._in_head:
            self.buttons[-1] = t


def parse_page(html):
    p = PageParser()
    try:
        p.feed(html)
    except IncompleteRead:
        pass
    all_text = " ".join(p._text)
    body_text = " ".join([x for x in p._text if x])  # simplified
    # CTA detection on links + buttons
    cta_candidates = []
    for txt, href in p.a_tags:
        if txt and len(txt) <= 40 and any(k in txt for k in CTA_KEYWORDS):
            cta_candidates.append(txt)
    for txt in p.buttons:
        if txt and len(txt) <= 40 and any(k in txt for k in CTA_KEYWORDS):
            cta_candidates.append(txt)
    action_cta = [c for c in cta_candidates if any(k in c for k in ACTION_KEYWORDS)]
    # form submit copy + validation
    for f in p.forms:
        # detect submit text inside form (last button/input submit)
        # approximate: scan button texts / submit input values containing 提交/发送/订阅
        btns = p.buttons + p.submit_inputs
        for b in btns:
            if b and any(w in b for w in ("提交", "发送", "订阅", "获取", "预约", "咨询")):
                f["submit_text"] = b
                break
        if f["submit_text"]:
            f["action_copy"] = any(k in f["submit_text"] for k in ACTION_KEYWORDS)
    # contact
    contact = {k: bool(pat.search(all_text)) for k, pat in CONTACT_PATTERNS.items()}
    contact["tel_link"] = ('href="tel:' in html) or ("href='tel:" in html)
    contact["mailto_link"] = ('href="mailto:' in html) or ("href='mailto:" in html)
    # trust
    trust_hits = []
    low = all_text.lower()
    for kw in TRUST_KEYWORDS:
        if kw.lower() in low:
            trust_hits.append(kw)
    trust_count = len(set(trust_hits))
    return {
        "title": p.title.strip(),
        "meta_description": p.metas.get("description", ""),
        "viewport": p.metas.get("viewport", ""),
        "h1": [h.strip() for h in p.h1 if h.strip()],
        "cta_candidates": cta_candidates,
        "action_cta": action_cta,
        "forms": p.forms,
        "contact": contact,
        "trust_count": trust_count,
        "raw_text_sample": all_text[:4000],
    }


def score_landing(home):
    s = 0
    h1 = home.get("h1", [])
    s += 25 if len(h1) == 1 else (10 if len(h1) > 1 else 0)         # H1 唯一
    s += 15 if home.get("viewport") else 0                          # 移动端适配
    t = home.get("title", "")
    s += 15 if (10 <= len(t) <= 70) else 5                          # title 长度
    https = home.get("_https", False)
    s += 10 if https else 0
    cta_n = len(home.get("cta_candidates", []))
    s += 20 if cta_n >= 1 else 0                                    # 首屏 CTA 代理
    s += 15 if home.get("trust_count", 0) >= 2 else 5               # 信任信号
    return min(100, s)


def score_cta(home):
    cta_n = len(home.get("cta_candidates", []))
    act_n = len(home.get("action_cta", []))
    s = 0
    s += 40 if cta_n >= 1 else 0
    s += 30 if act_n >= 1 else 0
    s += 30 if act_n >= 3 else 0
    return min(100, s)


def score_contact(home):
    c = home.get("contact", {})
    s = 0
    s += 25 if c.get("phone") else 0
    s += 25 if c.get("email") else 0
    s += 15 if (c.get("whatsapp") or c.get("wechat")) else 0
    s += 20 if c.get("address") else 0
    s += 15 if (c.get("tel_link") or c.get("mailto_link")) else 0
    return min(100, s)


def score_trust(home):
    n = home.get("trust_count", 0)
    return {0: 0, 1: 30, 2: 55, 3: 75}.get(n, 100)


def score_form(forms):
    """取字段最多的表单为瓶颈表单打分（最差表单 = 漏点）。"""
    if not forms:
        return 0, None
    worst = max(forms, key=lambda f: len(f.get("fields", [])))
    F = len(worst.get("fields", []))
    R = sum(1 for f in worst.get("fields", []) if f.get("required"))
    fields_score = 50 if F <= 5 else (30 if F <= 7 else (15 if F <= 10 else 5))
    req_score = 20 if R <= 3 else (10 if R <= 5 else 0)
    val_score = 10 if worst.get("has_validation") else 0
    sub_score = 10 if worst.get("action_copy") else 0
    mobile_score = 10  # 默认给基线，真实移动适配需人工确认
    total = fields_score + req_score + val_score + sub_score + mobile_score
    return min(100, total), {
        "fields": F, "required": R,
        "submit_text": worst.get("submit_text", ""),
        "has_validation": worst.get("has_validation"),
    }


def build_suggestions(stage_scores, home, form_detail):
    sugs = []
    if stage_scores["cta"] < 60:
        sugs.append({"stage": "cta", "risk": "low", "issue": "缺少动作导向且多处出现的 CTA",
                     "recommendation": "新增/增强主 CTA 按钮（文案动作导向、对比色、首屏+中段+页尾+悬浮）",
                     "fix": "P1 / P6"})
    if stage_scores["trust"] < 60:
        sugs.append({"stage": "trust", "risk": "low", "issue": "页面缺少资质/客户/案例/评价等信任信号",
                     "recommendation": "首页/落地页追加「合作客户 + 资质荣誉 + 客户评价」区块",
                     "fix": "P2"})
    if stage_scores["contact"] < 60:
        sugs.append({"stage": "contact", "risk": "low", "issue": "电话/邮箱/微信等联系方式不显眼",
                     "recommendation": "页头加点击拨打(tel:)、微信入口；Contact 区块前置",
                     "fix": "P3"})
    if stage_scores["form"] < 60 and form_detail:
        fd = form_detail
        sugs.append({"stage": "form", "risk": "low" if fd["fields"] <= 7 else "high",
                     "issue": f"表单字段过多（瓶颈表单 {fd['fields']} 字段，必填 {fd['required']}）",
                     "recommendation": "删减/后置非必要字段、必填最小化、提交按钮改动作导向文案",
                     "fix": "F1 / F2 / F4" + ("（大删需确认）" if fd["fields"] > 7 else "")})
    if stage_scores["landing"] < 60:
        sugs.append({"stage": "landing", "risk": "low", "issue": "首屏未清晰传达价值主张或缺少 FAQ/异议处理",
                     "recommendation": "重写首屏标题价值主张；新增 FAQ 区块",
                     "fix": "P5 / P4"})
    sugs.append({"stage": "lead", "risk": "low",
                 "issue": "历史询盘漏点需结合后台数据确认（高频空字段、产品询盘占比、审核/响应效率）",
                 "recommendation": "有 MCP 时通过 list_enquiry_records（status=-1）拉取历史询盘，统计各字段空置率与高频询盘产品，定位高频空字段再决定删/后置或改选填",
                 "fix": "F10（需 MCP + 确认）"})
    return sugs


def run_audit(url, file_path=None, max_pages=20, depth=3, out=None):
    htmls = {}
    order = [url]
    if file_path:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            htmls[url] = f.read()
    else:
        htmls, order = crawl(url, max_pages=max_pages, depth=depth)
    pages = [parse_page(h) for h in htmls.values()]
    # home = first parsed (url order[0])
    home = pages[0] if pages else {}
    home["_https"] = url.lower().startswith("https")
    # aggregate signals
    all_forms = []
    for pg in pages:
        all_forms.extend(pg.get("forms", []))
    cta_all = []
    for pg in pages:
        cta_all.extend(pg.get("cta_candidates", []))
    action_all = []
    for pg in pages:
        action_all.extend(pg.get("action_cta", []))
    contact_any = {}
    for k in ("phone", "email", "whatsapp", "wechat", "address"):
        contact_any[k] = any(pg.get("contact", {}).get(k) for pg in pages)
    contact_any["tel_link"] = any(pg.get("contact", {}).get("tel_link") for pg in pages)
    contact_any["mailto_link"] = any(pg.get("contact", {}).get("mailto_link") for pg in pages)
    home["contact"] = contact_any
    trust_max = max((pg.get("trust_count", 0) for pg in pages), default=0)
    home["trust_count"] = trust_max
    home["cta_candidates"] = cta_all
    home["action_cta"] = action_all

    stage = {
        "landing": score_landing(home),
        "cta": score_cta(home),
        "contact": score_contact(home),
        "trust": score_trust(home),
    }
    form_score, form_detail = score_form(all_forms)
    stage["form"] = form_score

    leadgen = int(round(0.20 * stage["landing"] + 0.20 * stage["cta"] +
                        0.25 * stage["form"] + 0.15 * stage["contact"] +
                        0.20 * stage["trust"]))

    suggestions = build_suggestions(stage, home, form_detail)

    report = {
        "site": {
            "url": url,
            "domain": _norm_url(url),
            "https": url.lower().startswith("https"),
            "pages_crawled": len(htmls),
        },
        "stage_scores": stage,
        "leadgen_score": leadgen,
        "signals": {
            "cta_count": len(cta_all),
            "cta_samples": cta_all[:15],
            "action_cta_count": len(action_all),
            "forms_count": len(all_forms),
            "form_detail": form_detail,
            "contact": contact_any,
            "trust_count": trust_max,
            "home_title": home.get("title", ""),
            "home_h1": home.get("h1", []),
        },
        "suggestions": suggestions,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"[ok] report -> {out}\n")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def run_score(report_path, out=None):
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    stage = report.get("stage_scores", {})
    leadgen = int(round(0.20 * stage.get("landing", 0) + 0.20 * stage.get("cta", 0) +
                        0.25 * stage.get("form", 0) + 0.15 * stage.get("contact", 0) +
                        0.20 * stage.get("trust", 0)))
    report["leadgen_score"] = leadgen
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"[ok] scored -> {out}\n")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    ap = argparse.ArgumentParser(description="Website Lead-Gen / CRO audit (zero-dep)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    au = sub.add_parser("audit", help="抓取并分析网站")
    au.add_argument("--url", required=True)
    au.add_argument("--file", default=None, help="用本地 HTML 文件分析（CMS 离线源码）")
    au.add_argument("--max-pages", type=int, default=20)
    au.add_argument("--depth", type=int, default=3)
    au.add_argument("--delay", type=float, default=REQUEST_DELAY)
    au.add_argument("--out", default=None)

    sc = sub.add_parser("score", help="基于已有报告重算获客分")
    sc.add_argument("--report", required=True)
    sc.add_argument("--out", default=None)

    args = ap.parse_args()
    if args.cmd == "audit":
        run_audit(args.url, file_path=args.file, max_pages=args.max_pages,
                  depth=args.depth, out=args.out)
    elif args.cmd == "score":
        run_score(args.report, out=args.out)


if __name__ == "__main__":
    main()
