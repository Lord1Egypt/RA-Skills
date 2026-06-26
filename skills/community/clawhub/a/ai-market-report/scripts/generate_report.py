#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI陪伴软件调研日报 - HTML/PDF生成器（模板版）"""
import re, os, sys
from weasyprint import HTML as WPHtml

def parse_markdown(md_path):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    dm = re.search(r"\u62a5\u544a\u65e5\u671f[：:]?\s*(\d{4}\u5e74\d{1,2}\u6708\d{1,2}\u65e5)", md)
    rd = dm.group(1) if dm else "\u672a\u77e5"

    def section_text(pat):
        m = re.search(pat, md)
        if not m: return ""
        start = m.start()
        # Stop at next section (## or ### heading)
        nxt = re.search(r'#{2,3}\s+\d+\.', md[start+4:])
        end = start+4+nxt.start() if nxt else len(md)
        return md[start:end]

    def tbl_rows(section_pat):
        text = section_text(section_pat)
        bad = ["\u4ea7\u54c1\u540d","\u6307\u6807","\u7fa4\u4f53","\u5e02\u573a",
               "\u65f6\u95f4","\u6765\u6e90","\u6307\u4ef6","\u5907\u6ce8"]
        rows=[]; in_t=False
        for ln in text.split("\n"):
            if ln.startswith("|"):
                in_t=True
                if "\u2014\u2014" not in ln and "---" not in ln:
                    cells=[c.strip() for c in ln.split("|")[1:-1]]
                    if cells and cells[0] and cells[0] not in bad:
                        rows.append(cells)
            elif in_t: break
        return rows

    def blts(pat):
        items=[]
        for ln in section_text(pat).split("\n"):
            m = re.match(r"\d+\.\s\*\*(.+?)\*\*[：:]\s*(.+)", ln)
            if m: items.append({"title":m.group(1),"desc":m.group(2)})
        return items

    def dash_lines(pat):
        return [ln.lstrip("- *").strip() for ln in section_text(pat).split("\n") if ln.startswith("-")]

    app_r = tbl_rows(r"### 1\.1")
    ops_r = tbl_rows(r"### 1\.2")
    mkt_r = tbl_rows(r"### 1\.3")
    chg_r = tbl_rows(r"### 4\.2")
    ev_r  = tbl_rows(r"### 4\.1")
    mkt2  = tbl_rows(r"### 3\.1")
    per_r = tbl_rows(r"### 5\.3")
    opp   = blts(r"### 4\.3")
    rsk   = blts(r"### 4\.4")
    strs  = dash_lines(r"### 5\.1")
    tacs  = dash_lines(r"### 5\.5")

    market = {r[0]:r[1] for r in mkt_r if len(r)>=2}
    g = lambda k, d="\u672a\u516c\u5f00": market.get(k, d)

    def find_ops(name):
        for r in ops_r:
            if name in r[0]:
                return {"mau":r[1] if len(r)>1 else"\u672a\u516c\u5f00",
                        "rev":r[2] if len(r)>2 else"\u672a\u516c\u5f00",
                        "val":r[3] if len(r)>3 else"\u672a\u516c\u5f00",
                        "dyn":" ".join(r[5:])[:80] if len(r)>5 else""}
        return {"mau":"\u672a\u516c\u5f00","rev":"\u672a\u516c\u5f00","val":"\u672a\u516c\u5f00","dyn":""}

    def find_app(name):
        for r in app_r:
            if name in r[0]:
                return {"rating":r[1],"reviews":r[2],"cat":r[3] if len(r)>3 else""}
        return {"rating":"\u2014","reviews":"\u2014","cat":""}

    product_names=["Character.AI","Replika","PolyBuzz","Chai","Nomi","Talkie"]
    top=[]
    for nm in product_names:
        ops=find_ops(nm); app=find_app(nm)
        top.append({"name":nm,"rating":app["rating"],"reviews":app["reviews"],
                    "category":app["cat"],"mau":ops["mau"],"rev":ops["rev"],
                    "val":ops["val"],"dyn":ops["dyn"]})

    doubao_m=mao_m=xingye_m=hailuo_m="\u672a\u516c\u5f00"
    for r in ops_r:
        if "\u8c46\u5305" in r[0]: doubao_m=r[1]
        if "\u732b\u7bb1" in r[0]: mao_m=r[1]
        if "\u661f\u91ce" in r[0]: xingye_m=r[1]
        if "\u6d77\u87baAI" in r[0]: hailuo_m=r[1]

    return {"report_date":rd,"app_rows":app_r,"ops_rows":ops_r,
            "mkt_2025":g("\u5168\u7403AI\u966a\u4f34\u5e02\u573a\u89c4\u6a21\uff082025\uff09"),
            "mkt_2026":g("\u5168\u7403AI\u966a\u4f34\u5e02\u573a\u89c4\u6a21\uff082026\uff09"),
            "cagr":g("\u590d\u5408\u589e\u957f\u7387\uff082026-2032\uff09"),
            "cai_vis":g("Character.AI \u6708\u8bbf\u95ee\u91cf"),
            "cai_dl":g("Character.AI \u4e0b\u8f7d\u91cf\uff082024\uff09"),
            "minimax_users":g("MiniMax\u5168\u7403\u7528\u6237"),
            "top":top,"chg":chg_r,"ev":ev_r,"mkt2":mkt2,"per":per_r,
            "opp":opp,"rsk":rsk,"strs":strs,"tacs":tacs,
            "doubao_m":doubao_m,"mao_m":mao_m,"xingye_m":xingye_m,"hailuo_m":hailuo_m}


def c(s): return re.sub(r"\*\*(.+?)\*\*", r"\1", s).strip()


def r_app(rows):
    h=""
    for r in rows:
        if len(r)<5: continue
        n,ra,rv,ca,po=r[0],r[1],r[2],r[3],r[4]
        h+="<tr><td><strong>"+n+"</strong></td><td><span class=\"tg tg-b\">&#x2b50; "+ra+"</span></td><td>"+rv+"</td><td>"+ca+"</td><td>"+po+"</td></tr>\n"
    return h


def r_ops(rows):
    h=""
    for r in rows:
        if len(r)<6: continue
        n,mau,rv,vl,dr=r[0],r[1],r[2],r[3],r[4]
        dyn=c(" ".join(r[5:]))[:50]
        cls="wr" if "\u672a\u516c\u5f00" in mau else ""
        h+="<tr><td><strong>"+n+"</strong></td><td class=\""+cls+"\">"+mau+"</td><td>"+rv+"</td><td>"+vl+"</td><td>"+dr+"</td><td style=\"font-size:10px;color:#64748b\">"+dyn+"...</td></tr>\n"
    return h


def r_cards(prods):
    emj={"Character.AI":"&#x1f7e2;","Replika":"&#x1f49a;","PolyBuzz":"&#x1f535;","Chai":"&#x1f7e3;","Nomi":"&#x1f9e1;","Talkie":"&#x1f7e0;"}
    def em(name): return next((v for k,v in emj.items() if k in name),"&#x1f539;")
    def card(p):
        try: hi="hi" if float(p["rating"].replace("\u2b50","").strip() or 0)>=4.6 else ""
        except: hi=""
        rt="rt "+("hi" if hi else "")
        dyn_c=c(p["dyn"])[:80].replace("<","&lt;").replace(">","&gt;")
        return ("<div class=\"pc\">"
                "<div class=\"phd\"><h3>"+em(p["name"])+" "+p["name"]+"</h3>"
                "<span class=\""+rt+"\">&#x2b50; "+p["rating"]+"</span></div>"
                "<div class=\"mr\"><span class=\"mi\"><strong>MAU:</strong> "+p["mau"]+"</span>"
                "<span class=\"mi\"><strong>&#x6536;&#x5165;:</strong> "+p["rev"]+"</span></div>"
                "<div class=\"mr\"><span class=\"mi\"><strong>&#x4f30;&#x503c;:</strong> "+p["val"]+"</span>"
                "<span class=\"mi\"><strong>&#x5206;&#x7c7b;:</strong> "+p["category"]+"</span></div>"
                "<p style=\"font-size:11px;color:#64748b\">"+dyn_c+"</p></div>")
    h=""
    for i in range(0,len(prods),2):
        h+="<div class=\"tc\" style=\"margin-bottom:10px\">"
        for p in prods[i:i+2]: h+=card(p)
        h+="</div>"
    return h


def r_chg(rows):
    if not rows: return '<div class="cg cg2"></div>'
    h='<div class="cg cg2">\n'
    for r in rows:
        if len(r)<3: continue
        ind,diff,st=r[0],r[1],r[2]
        col=("dr" if ("\u4e0b\u964d" in st or "\U0001f534" in st) else ("su" if ("\u63d0\u5347" in st or "\U0001f7e2" in st) else ""))
        h+='<div class="dc"><div class="lbl">'+ind+'</div><div class="val '+col+'">'+c(diff)+'</div><div class="note">'+c(st)+'</div></div>\n'
    return h+'</div>'


def r_mkt(rows):
    eu=cn=None
    for r in rows:
        if len(r)<3: continue
        if "\u6b27\u7f8e" in r[0] and not eu: eu=r
        elif ("\u4e2d\u56fd" in r[0] or "\u4e2d\u56fd" in r[1]) and not cn: cn=r
    h=""  # wrapped in right-column div by caller
    if eu:
        items="".join("<li>"+c(x)+"</li>" for x in eu[2].split("\uff1b") if x.strip())
        h+='<div class="sec">&#x1f30d; \u6b27\u7f8e\u5e02\u573a</div>'
        h+='<div class="cb cb-i" style="margin-bottom:10px;"><p><strong>\u4e3b\u5bfc:</strong>'+c(eu[1])+'</p></div><ul class="fl">'+items+'</ul>\n'
    if cn:
        items="".join("<li>"+c(x)+"</li>" for x in cn[2].split("\uff1b") if x.strip())
        h+='<div class="sec">&#x1f1e8;&#x1f1f3; \u4e2d\u56fd/\u4e1c\u5357\u4e9a</div>'
        h+='<div class="cb cb-w" style="margin-bottom:10px;"><p><strong>\u4e3b\u5bfc:</strong>'+c(cn[1])+'</p></div><ul class="fl">'+items+'</ul>\n'
    return h


def r_ev(rows):
    if not rows: return ""
    h='<div class="sec">&#x1f4c5; \u6700\u8fd1\u91cd\u8981\u52a8\u6001</div>'
    h+='<table class="dt" style="font-size:11px">\n<thead><tr><th>\u65f6\u95f4</th><th>\u4e8b\u4ef6</th><th>\u5907\u6ce8</th></tr></thead>\n<tbody>\n'
    for r in rows[:7]:
        ev=c(r[1] if len(r)>1 else ""); note=c(" ".join(r[2:]) if len(r)>2 else "")
        h+="<tr><td>"+r[0]+"</td><td><strong>"+ev+"</strong></td><td>"+note+"</td></tr>\n"
    return h+"</tbody></table>\n"


def r_or(opp, rsk):
    h='<div class="cg cg3">\n'
    for i,o in enumerate(opp[:5],1):
        h+='<div class="oc"><div class="on">'+str(i)+'</div><div><h4>'+c(o["title"])+'</h4><p>'+c(o["desc"])+'</p></div></div>\n'
    icons=["&#x1f3ed;","&#x1f9e0;","&#x1f4b0;","&#x2694;&#xfe0f;"]
    h+='</div>\n<div class="sec">&#x26a0;&#xfe0f; &#x98ce;&#x9669;&#x63d0;&#x793a;</div>\n<div class="cg cg4">\n'
    for i,r in enumerate(rsk[:4]):
        ico=icons[i] if i<len(icons) else "&#x26a0;&#xfe0f;"
        h+='<div class="rc"><div class="ri">'+ico+'</div><div><h4>'+c(r["title"])+'</h4><p>'+c(r["desc"])+'</p></div></div>\n'
    return h+'</div>'


def r_per(rows):
    if not rows: return ""
    h='<div class="cg cg2">\n'
    for r in rows:
        if len(r)<3: continue
        h+='<div class="dc"><div class="lbl">'+c(r[0])+'</div><div class="note" style="font-size:12px;margin-bottom:5px">'+c(r[1])+'</div><div class="note"><strong>&#x65b9;&#x5411;:</strong> '+c(r[2])+'</div></div>\n'
    return h+'</div>'


def r_str(strs, tacs):
    h=""
    if strs: h+='<ul class="fl">\n'+"\n".join("<li>"+c(s)+"</li>" for s in strs)+'\n</ul>\n'
    if tacs: h+='<div class="sec">&#x1f4e2; \u63a8\u5e7f\u7b56;&#x7565;</div>\n<ul class="fl">\n'+"\n".join("<li>"+c(t)+"</li>" for t in tacs)+'\n</ul>\n'
    return h


def build_html(d, template_path):
    """Read template and fill in all {{variables}}."""
    with open(template_path, encoding="utf-8") as f:
        tpl = f.read()

    # Render sub-components
    app_t  = r_app(d["app_rows"])
    ops_t  = r_ops(d["ops_rows"])
    pcd    = r_cards(d["top"])
    mbl    = r_mkt(d["mkt2"])
    ev_h   = r_ev(d["ev"])
    chg_h  = r_chg(d["chg"])
    or_h   = r_or(d["opp"], d["rsk"])
    per_h  = r_per(d["per"])
    str_h  = r_str(d["strs"], d["tacs"])

    # Build replacements dict
    reps = {
        "{{report_date}}":    d["report_date"],
        "{{product_count}}":  str(len(d["app_rows"])),
        "{{mkt_2025}}":        d["mkt_2025"],
        "{{mkt_2026}}":        d["mkt_2026"],
        "{{cagr}}":            d["cagr"],
        "{{cai_vis}}":         d["cai_vis"],
        "{{cai_dl}}":          d["cai_dl"],
        "{{minimax_users}}":   d["minimax_users"],
        "{{mao_m}}":           d["mao_m"],
        "{{xingye_m}}":        d["xingye_m"],
        "{{hailuo_m}}":        d["hailuo_m"],
        "{{app_table}}":       app_t,
        "{{ops_table}}":       ops_t,
        "{{product_cards}}":   pcd,
        "{{mkt_block}}":       mbl,
        "{{ev_table}}":        ev_h,
        "{{chg_block}}":       chg_h,
        "{{or_block}}":        or_h,
        "{{str_block}}":       str_h,
        "{{per_block}}":       per_h,
    }

    html = tpl
    for k, v in reps.items():
        html = html.replace(k, v)
    return html


def make_report(md_file, out_dir, ts):
    base = os.path.dirname(os.path.abspath(md_file))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)  # skill root (one level above scripts/)

    # Template search order: 1) same dir as markdown, 2) skill assets/, 3) skill root
    for candidate in [
        os.path.join(base, "report_template.html"),
        os.path.join(skill_dir, "assets", "report_template.html"),
        os.path.join(skill_dir, "report_template.html"),
    ]:
        if os.path.exists(candidate):
            template = candidate
            break

    print("  Template:", template)

    print("[1/3] Parse:", md_file)
    d = parse_markdown(md_file)
    n_app = len(d["app_rows"]); n_ops = len(d["ops_rows"])
    print("  AppStore:{} | Ops:{} | Downloads:{}".format(n_app, n_ops, d["cai_dl"]))

    html_file = os.path.join(out_dir, "AI_Report_{}.html".format(ts))
    pdf_file  = os.path.join(out_dir, "AI_Report_{}.pdf".format(ts))

    print("[2/3] HTML:", html_file)
    html = build_html(d, template)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print("  {}KB written".format(len(html)//1024))

    print("[3/3] PDF...")
    WPHtml(string=html, base_url="/").write_pdf(pdf_file)
    sz = os.path.getsize(pdf_file)
    print("  Done: {} ({}KB)".format(pdf_file, sz//1024))
    return html_file, pdf_file


if __name__ == "__main__":
    md  = sys.argv[1] if len(sys.argv) > 1 else "/root/.openclaw/workspace/myfiles/daily_report_data/files/AI_Report_20260331010305.md"
    out = sys.argv[2] if len(sys.argv) > 2 else "/root/.openclaw/workspace/myfiles/daily_report_data/files"
    ts  = sys.argv[3] if len(sys.argv) > 3 else "20260331010305"
    make_report(md, out, ts)
