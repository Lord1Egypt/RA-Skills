"""HTML and DOCX writer primitives for report generation."""

import io
import zipfile
from xml.sax.saxutils import escape as _esc

from .common import _DOCX_RISK_COLOR

def esc(s):
    return _esc(str(s if s is not None else ""))


def esc_ml(s):
    return esc(s).replace("\n", "<br>")


def _toc_label(t):
    """目录文案：去掉章节标题里的「一、二、…」前缀（目录另有序号）。"""
    t = str(t)
    if len(t) > 1 and t[0] in "一二三四五六七八九十" and "、" in t[:4]:
        return t.split("、", 1)[1]
    return t

# block = (kind, text, opts)
_HEAD_SZ = {"title": 44, "subtitle": 21, "h2": 30, "h3": 25, "issue": 24}


def _run(text, *, bold=False, italic=False, color=None, sz=21):
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if color:
        rpr.append(f'<w:color w:val="{color}"/>')
    rpr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    runs = []
    for i, seg in enumerate(_esc(str(text)).split("\n")):
        if i:
            runs.append("<w:br/>")
        runs.append(f'<w:t xml:space="preserve">{seg}</w:t>')
    return f"<w:r><w:rPr>{''.join(rpr)}</w:rPr>{''.join(runs)}</w:r>"


def _ppr(*, before=0, after=80, ind=0, shade=None, border=None):
    p = []
    if shade:
        p.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    if border:
        p.append(f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="{border}"/></w:pBdr>')
    if ind:
        p.append(f'<w:ind w:left="{ind}"/>')
    p.append(f'<w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>')
    return f"<w:pPr>{''.join(p)}</w:pPr>"


def _para(block):
    kind, text, opts = block
    risk = opts.get("risk", "")
    if kind == "title":
        return f'<w:p>{_ppr(before=0, after=60)}{_run(text, bold=True, sz=44, color="1F3A8A")}</w:p>'
    if kind == "subtitle":
        return f'<w:p>{_ppr(after=200)}{_run(text, sz=20, color="647084")}</w:p>'
    if kind == "h2":
        return (f'<w:p>{_ppr(before=240, after=100, border="2563EB")}'
                f'{_run(text, bold=True, sz=30, color="1F3A8A")}</w:p>')
    if kind == "h3":
        return f'<w:p>{_ppr(before=140, after=60)}{_run(text, bold=True, sz=25, color="1F2933")}</w:p>'
    if kind == "issue":
        c = _DOCX_RISK_COLOR.get(risk, "475569")
        return (f'<w:p>{_ppr(before=140, after=40, border=c)}'
                f'{_run(text, bold=True, sz=24, color=c)}</w:p>')
    if kind == "callout":
        return (f'<w:p>{_ppr(before=80, after=120, ind=120, shade="EEF4FF")}'
                f'{_run(text, bold=True, sz=22, color="1E3A8A")}</w:p>')
    if kind == "muted":
        return f'<w:p>{_ppr(after=40, ind=120)}{_run(text, sz=18, color="647084")}</w:p>'
    if kind == "bullet":
        return f'<w:p>{_ppr(after=40, ind=300)}{_run("▪  " + str(text), sz=21)}</w:p>'
    if kind == "tender":
        return f'<w:p>{_ppr(after=30, ind=300, shade="F3F6FB")}{_run(text, sz=20, color="475569")}</w:p>'
    if kind == "bid":
        return f'<w:p>{_ppr(after=30, ind=300, shade="FFF7ED")}{_run(text, sz=20, color="9A3412")}</w:p>'
    if kind == "sug":
        return f'<w:p>{_ppr(after=80, ind=300, shade="ECFDF5")}{_run(text, sz=20, color="047857")}</w:p>'
    return f'<w:p>{_ppr()}{_run(text, sz=21)}</w:p>'


def build_docx(blocks) -> bytes:
    body = "".join(_para(b) for b in blocks)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}<w:sectPr><w:pgMar w:top=\"1200\" w:right=\"1200\" w:bottom=\"1200\" "
        'w:left="1200" w:header="720" w:footer="720"/></w:sectPr></w:body></w:document>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>'
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
    return buf.getvalue()

_HTML_CSS = """
:root{
--paper:#dce8e3;--card:#ffffff;--ink:#1b2430;--ink2:#66707c;
--line:#c9d4ce;--cyan:#1f5f6b;--lime:#1f5f6b;--blue:#2c3a4a;
--h2bg:#243040;--gtbg:#d4e4db;--h3bg:#e4d6b0;--toc:#e4eee9;
--high:#b42318;--review:#b45309;--tip:#1f5f6b;--ok:#0f6b4c;
--hud:"Avenir Next Condensed","Bahnschrift","DIN Alternate","PingFang SC",sans-serif;
--display:"Iowan Old Style","Palatino Linotype","Songti SC","STSong",serif;
--sans:"PingFang SC","Hiragino Sans GB","Noto Sans SC","Microsoft YaHei",sans-serif}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;scroll-behavior:smooth}
body{margin:0;color:var(--ink);font-size:15px;line-height:1.75;font-family:var(--sans);min-height:100vh;
background:
radial-gradient(ellipse 85% 55% at -5% -8%,rgba(31,95,107,.28),transparent 58%),
radial-gradient(ellipse 70% 50% at 108% 108%,rgba(196,165,116,.22),transparent 54%),
radial-gradient(ellipse 55% 40% at 92% 8%,rgba(36,48,64,.12),transparent 52%),
linear-gradient(165deg,#e7efe9 0%,var(--paper) 46%,#e6e3d6 100%)}
.fx{position:fixed;inset:0;pointer-events:none;z-index:0}
.fx .orb{position:absolute;border-radius:50%;filter:blur(72px);opacity:.5;display:block}
.fx .orb.a{width:58vw;height:58vw;left:-20vw;top:-24vw;background:radial-gradient(circle,#5f8f8a 0%,transparent 68%)}
.fx .orb.b{width:46vw;height:46vw;right:-14vw;top:12vh;background:radial-gradient(circle,#c4a574 0%,transparent 70%);opacity:.32}
.fx .orb.c{width:50vw;height:50vw;right:6vw;bottom:-20vw;background:radial-gradient(circle,#243040 0%,transparent 72%);opacity:.18}
.fx .grid{position:absolute;inset:0;opacity:.7;
background-image:linear-gradient(rgba(31,95,107,.09) 1px,transparent 1px),
linear-gradient(90deg,rgba(31,95,107,.06) 1px,transparent 1px);background-size:56px 56px;
mask-image:radial-gradient(ellipse at 50% 20%,#000 30%,transparent 78%)}
.fx .noise{position:absolute;inset:0;opacity:.16;mix-blend-mode:multiply;
background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='.55'/></svg>")}
.shell{position:relative;z-index:1;display:flex;min-height:100vh}
/* ---- 左侧目录 ---- */
.toc{width:248px;flex:none;color:var(--ink);
background:linear-gradient(180deg,#eef4f1 0%,var(--toc) 42%,#d5e3dd 100%);
position:sticky;top:0;height:100vh;overflow:auto;padding:32px 20px 24px;
box-shadow:inset -1px 0 0 rgba(31,95,107,.1);border-top:3px solid #c4a574;border-right:1px solid var(--line)}
.toc .brand{font-family:var(--hud);font-size:11px;letter-spacing:3.6px;color:#1f5f6b;font-weight:700;display:flex;align-items:center;gap:8px}
.toc .brand:before{content:"";width:7px;height:7px;background:#c4a574;flex:none}
.toc .bt{font-family:var(--display);font-size:19px;color:var(--ink);line-height:1.38;margin:14px 0 22px;
padding-bottom:16px;border-bottom:1px solid var(--line);font-weight:600}
.toc nav{background:transparent;border:0;border-radius:0;padding:0}
.toc nav a{display:flex;gap:10px;align-items:flex-start;color:#4a5854;text-decoration:none;font-size:15px;line-height:1.45;
padding:10px 8px 10px 10px;border-radius:0;margin:0;border-left:2px solid transparent;transition:.16s;background:transparent}
.toc nav a:hover{background:rgba(31,95,107,.07);color:var(--ink)}
.toc nav a.on{background:linear-gradient(90deg,rgba(31,95,107,.14),transparent);color:#1f5f6b;border-left-color:#c4a574;font-weight:600}
.toc nav a .i{font-family:var(--hud);font-size:12px;color:#8a9691;font-variant-numeric:tabular-nums;font-weight:600;min-width:1.8em;padding-top:1px}
.toc nav a.on .i{color:#c4a574}
.toc .sfoot{margin-top:22px;padding-top:14px;border-top:1px solid var(--line);font-size:11px;color:var(--ink2);letter-spacing:.4px}
/* ---- 内容区 ---- */
.content{flex:1;min-width:0;background:transparent}
.accent{display:flex;height:3px}.accent i{flex:1}
.accent .a{background:#243040}.accent .b{background:var(--cyan)}.accent .c{background:#c4a574}
.inner{position:relative;max-width:860px;margin:28px 40px 56px;padding:44px 52px 72px;
background:
linear-gradient(var(--cyan),var(--cyan)) 14px 14px/22px 1px no-repeat,
linear-gradient(var(--cyan),var(--cyan)) 14px 14px/1px 22px no-repeat,
linear-gradient(#c4a574,#c4a574) calc(100% - 14px) 14px/22px 1px no-repeat,
linear-gradient(#c4a574,#c4a574) calc(100% - 14px) 14px/1px 22px no-repeat,
linear-gradient(var(--cyan),var(--cyan)) 14px calc(100% - 14px)/22px 1px no-repeat,
linear-gradient(var(--cyan),var(--cyan)) 14px calc(100% - 14px)/1px 22px no-repeat,
linear-gradient(#c4a574,#c4a574) calc(100% - 14px) calc(100% - 14px)/22px 1px no-repeat,
linear-gradient(#c4a574,#c4a574) calc(100% - 14px) calc(100% - 14px)/1px 22px no-repeat,
linear-gradient(180deg,rgba(255,252,247,.96),rgba(255,255,255,.92));
box-shadow:0 28px 70px rgba(36,48,64,.14),0 0 0 1px rgba(31,95,107,.1);
outline:1px solid rgba(196,165,116,.4);outline-offset:8px}
.inner:after{content:"百炼标书";position:absolute;right:18px;top:56px;font-family:var(--display);
font-size:64px;line-height:1;color:rgba(31,95,107,.055);pointer-events:none;letter-spacing:.18em}
/* ---- 封面 ---- */
.cover{position:relative;padding:4px 88px 28px 42px;margin:0 0 12px;border:0;border-radius:0;
background:transparent;box-shadow:none}
.cover:before{content:"BAILIAN";position:absolute;left:0;top:10px;bottom:28px;
writing-mode:vertical-rl;font-family:var(--hud);font-size:10px;letter-spacing:7px;
color:#c4a574;font-weight:700}
.cover:after{content:"";position:absolute;left:42px;right:72px;bottom:0;height:1px;
background:linear-gradient(90deg,var(--cyan),#c4a574 42%,transparent);border-radius:0}
.kicker{font-family:var(--hud);font-size:11px;letter-spacing:4px;color:var(--cyan);font-weight:700;
text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:12px}
.kicker:after{content:"";flex:1;height:1px;background:rgba(31,95,107,.22)}
.cover h1{font-family:var(--display);font-weight:600;font-size:34px;line-height:1.24;letter-spacing:.15px;
margin:0 0 18px;color:var(--ink);text-shadow:none}
.meta{display:flex;flex-wrap:wrap;gap:8px}
.meta .pill{font-size:12.5px;color:var(--ink2);background:rgba(255,255,255,.7);border:1px solid var(--line);
border-radius:0;padding:5px 11px}
.meta .pill b{color:var(--cyan);font-family:var(--hud);font-weight:700;margin-right:5px;letter-spacing:.5px}
.cover .seal{position:absolute;right:2px;top:2px;width:72px;height:72px;border:2px solid #8e2a24;
color:#8e2a24;font-family:var(--display);font-size:15px;font-weight:700;font-style:normal;
display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;place-items:center;
letter-spacing:0;line-height:1;padding:6px;box-sizing:border-box;
transform:rotate(-13deg);background:rgba(142,42,36,.05);pointer-events:none}
.cover .seal span{display:block}
/* ---- 章节：一级墨底 / 二级矿绿 / 三级铜纸 ---- */
h2{font-family:var(--display);font-weight:600;font-size:22px;color:#f7f4ee;scroll-margin-top:14px;
margin:36px 0 18px;padding:12px 18px 12px 20px;border:0;border-left:4px solid #c4a574;
display:flex;align-items:baseline;gap:11px;position:relative;letter-spacing:.2px;
background:linear-gradient(90deg,#243040,var(--h2bg) 56%,#2c3a4a)}
h2:before{content:none;display:none}
h3{font-size:15px;margin:16px 0 8px;color:#3d3424;font-weight:700;
background:var(--h3bg);padding:8px 12px;border-left:4px solid #c4a574}
p{margin:6px 0;color:#2a3340}
/* ---- 风险条 ---- */
.riskbar{display:flex;height:6px;border-radius:0;overflow:hidden;margin:6px 0 12px;
border:0;background:#eceef1}
.riskbar span{display:block}.riskbar .high{background:var(--high)}.riskbar .review{background:var(--review)}
.riskbar .tip{background:var(--tip)}.riskbar .none{background:#eceef1;flex:1}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2);margin-bottom:4px}
.legend i{display:inline-block;width:8px;height:8px;border-radius:0;margin-right:5px;vertical-align:-1px}
/* ---- 指标 ---- */
.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:16px 0 10px;background:transparent;border:0}
.metric{position:relative;background:var(--card);border:1px solid var(--line);border-radius:0;
padding:18px 10px 14px;text-align:center;overflow:hidden;box-shadow:0 8px 20px rgba(36,48,64,.05)}
.metric:before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:var(--cyan)}
.metric.high:before{background:var(--high)}.metric.review:before{background:var(--review)}
.metric.tip:before{background:var(--tip)}.metric.ok:before{background:var(--ok)}
.metric .n{font-family:var(--hud);font-size:32px;font-weight:700;line-height:1;color:var(--ink);letter-spacing:.5px}
.metric.high .n{color:var(--high);text-shadow:none}
.metric.review .n{color:var(--review)}.metric.tip .n{color:var(--cyan);text-shadow:none}
.metric .l{font-size:11.5px;color:var(--ink2);margin-top:8px;letter-spacing:.6px}
/* ---- 摘要 ---- */
.callout{position:relative;background:#f4f7f4;border:1px solid var(--line);border-left:3px solid var(--cyan);border-radius:0;
padding:18px 20px;margin:20px 0;font-size:16px;color:var(--ink);font-weight:500;font-family:var(--display);line-height:1.7}
.callout:before{content:"摘要";position:absolute;top:-9px;left:14px;background:#fffaf4;font-family:var(--hud);
font-size:10px;letter-spacing:2.2px;color:var(--cyan);padding:0 6px;font-weight:700}
/* ---- 问题卡 ---- */
.issue{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--cyan);
border-radius:0;padding:16px 18px;margin:12px 0;break-inside:avoid;box-shadow:0 10px 24px rgba(36,48,64,.05)}
.issue.high{border-left-color:var(--high);box-shadow:none}
.issue.review{border-left-color:var(--review)}.issue.tip{border-left-color:var(--tip)}
.ihead{display:flex;align-items:center;gap:10px;margin-bottom:2px}
.tag{font-family:var(--hud);font-size:10.5px;letter-spacing:1.4px;font-weight:700;padding:2px 7px;
border-radius:0;border:1px solid currentColor;white-space:nowrap}
.tag.high{color:var(--high)}.tag.review{color:var(--review)}.tag.tip{color:var(--tip)}.tag.other{color:var(--ink2)}
.issue h3{margin:0;font-size:15.5px;font-weight:700;color:var(--ink);
background:transparent;padding:0;border:0}
.fname{font-size:12px;color:var(--ink2);margin:1px 0 8px}
.issue p{margin:5px 0;color:#2a3340;font-size:14.5px}
.evi{display:grid;gap:6px;margin:9px 0 3px}
.evi .row{padding:8px 12px;border-radius:0;font-size:13.5px;line-height:1.6}
.evi .tender{background:#f0f5f4;border-left:3px solid var(--cyan)}
.evi .bid{background:#f1f7f4;border-left:3px solid var(--ok)}
.evi .lbl{display:block;font-family:var(--hud);font-size:10px;letter-spacing:1.4px;color:var(--ink2);font-weight:700;margin-bottom:2px}
.sug{margin-top:8px;padding:8px 12px;background:#f1f7f4;border-left:2px solid var(--ok);
border-radius:0;font-size:13.5px;color:#0f6b4c}
.sug b{color:var(--ok)}
/* ---- 项目信息表 ---- */
.facts{display:grid;grid-template-columns:minmax(112px,26%) 1fr;border:1px solid var(--line);
background:var(--card);margin:12px 0 8px;border-radius:0;overflow:hidden}
.facts dt{padding:10px 14px;font-family:var(--hud);font-size:12px;color:var(--cyan);border-bottom:1px solid var(--line);
background:#f3f6f3;letter-spacing:.8px;display:flex;align-items:center}
.facts dd{padding:10px 16px;margin:0;border-bottom:1px solid var(--line);color:var(--ink);line-height:1.55}
.facts dt:nth-last-child(2),.facts dd:last-child{border-bottom:0}
/* ---- 分类条目 ---- */
.group{margin:18px 0 22px;counter-reset:ent}
.gt{display:flex;align-items:baseline;justify-content:space-between;gap:12px;font-family:var(--display);
font-size:17px;font-weight:600;padding:10px 14px;border-left:4px solid var(--cyan);margin:0 0 10px;color:var(--ink);
background:var(--gtbg)}
.gt .n{font-family:var(--hud);font-size:12px;color:var(--ink2);font-weight:500;letter-spacing:.8px;white-space:nowrap}
.entry{position:relative;background:var(--card);border:1px solid var(--line);border-radius:0;
padding:12px 16px 12px 44px;margin:0 0 8px;break-inside:avoid}
.entry:before{content:counter(ent,decimal-leading-zero);counter-increment:ent;position:absolute;left:12px;top:13px;
font-family:var(--hud);font-size:12px;color:var(--cyan);font-weight:700;letter-spacing:.4px}
.entry .body{margin:0;color:#2a3340;line-height:1.72}
.quote{margin:8px 0 0;padding:8px 12px 8px 14px;background:#f7f7f4;border-left:3px solid var(--cyan);
font-size:13.5px;color:#5a6470;line-height:1.7;font-family:var(--display);font-style:italic}
.quote .pg{display:inline-block;font-family:var(--hud);font-size:10px;letter-spacing:1px;
color:var(--cyan);font-weight:700;margin-right:8px;font-style:normal}
/* ---- 具名卡片 ---- */
.named{display:grid;gap:8px;margin:8px 0 12px}
.named .card{background:var(--card);border:1px solid var(--line);border-radius:0;padding:12px 16px;
break-inside:avoid}
.named .card .nm{font-weight:700;font-size:15px;margin:0 0 4px;color:var(--ink)}
.named .card .dt{margin:0;color:#2a3340;font-size:14.5px;line-height:1.65}
/* ---- 评分表 ---- */
.board{width:100%;border-collapse:collapse;margin:8px 0 16px;font-size:14px;
background:var(--card);border-radius:0;overflow:hidden;border:1px solid var(--line)}
.board th{text-align:left;font-family:var(--hud);font-size:11.5px;letter-spacing:1px;color:var(--cyan);font-weight:700;
padding:10px 12px;border-bottom:1px solid var(--cyan);background:#f7f7f4}
.board td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.board td.comp{font-family:var(--display);font-weight:600;background:#f7f7f4;letter-spacing:.2px;width:92px}
.board td.item{width:132px;font-weight:600;color:var(--ink)}
.board td.detail{line-height:1.65;color:#2a3340}
.board .pg{display:block;margin-top:4px;font-size:12px;color:var(--ink2);letter-spacing:.3px}
.board .sc{font-family:var(--hud);font-weight:700;white-space:nowrap;color:var(--cyan);text-align:right;width:72px}
.board .quote{margin-top:6px}
/* ---- 优先级 ---- */
.prio{display:inline-block;font-family:var(--hud);font-size:10px;letter-spacing:1px;font-weight:700;padding:0 6px;
border-radius:0;margin-right:8px;vertical-align:2px;border:1px solid currentColor}
.prio.high{color:var(--high)}.prio.medium{color:var(--review)}.prio.low{color:var(--tip)}
/* ---- 文件清单 ---- */
.files{list-style:none;margin:10px 0 14px;padding:0;border:1px solid var(--line);background:var(--card);
border-radius:0;overflow:hidden}
.files li{display:grid;grid-template-columns:88px 1fr auto;gap:12px;padding:10px 14px;
border-bottom:1px solid var(--line);align-items:baseline}
.files li:last-child{border-bottom:0}
.files .role{font-family:var(--hud);font-size:11.5px;letter-spacing:.6px;color:var(--cyan);font-weight:700}
.files .fn{color:var(--ink);font-weight:600}
.files .ex{font-size:12.5px;color:var(--ink2)}
/* ---- 查重仪表 ---- */
.meters{display:grid;gap:12px;margin:10px 0 6px}
.meter{display:grid;grid-template-columns:108px 1fr 52px;gap:10px;align-items:center}
.meter .ml{font-size:12.5px;color:var(--ink2)}
.meter .track{height:4px;background:#eceef1;border-radius:0;overflow:hidden;border:0}
.meter .track i{display:block;height:100%;background:var(--cyan);border-radius:0}
.meter .mv{font-family:var(--hud);font-weight:700;font-size:13px;color:var(--ink);text-align:right}
/* ---- 对照栏 ---- */
.compare{background:var(--card);border:1px solid var(--line);border-radius:0;padding:12px 14px;margin:8px 0;
break-inside:avoid}
.compare .cmeta{font-family:var(--hud);font-size:12.5px;color:var(--ink2);margin-bottom:8px;letter-spacing:.3px}
.compare .cols{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.compare .col{padding:10px 12px;border-radius:0;font-size:13.5px;line-height:1.62}
.compare .col.a{background:#f0f5f4;border-left:3px solid var(--cyan)}
.compare .col.b{background:#f7f7f4;border-left:3px solid #c4a574}
.compare .col .lbl{display:block;font-family:var(--hud);font-size:10px;letter-spacing:1.3px;color:var(--ink2);
font-weight:700;margin-bottom:4px}
.compare .col p{margin:0;color:#2a3340}
/* ---- 提示行 / 清单 ---- */
.tiprow{display:grid;grid-template-columns:minmax(120px,28%) 1fr;gap:10px;padding:9px 0;
border-bottom:1px solid var(--line)}
.tiprow:last-child{border-bottom:0}
.tiprow b{font-size:14px;color:var(--ink)}
.tiprow span{color:#2a3340;font-size:14px;line-height:1.6}
.chk{display:grid;grid-template-columns:22px 1fr;gap:8px;padding:8px 0;border-bottom:1px solid var(--line)}
.chk:last-child{border-bottom:0}
.chk .box{font-size:15px;color:var(--cyan);line-height:1.4}
.chk .ttl{font-weight:700;font-size:14.5px;color:var(--ink)}
.chk .note{font-size:12.5px;color:var(--ink2);margin-top:2px}
.okline{margin:10px 0;padding:10px 14px;background:#f1f7f4;border-left:3px solid var(--ok);
color:#0f6b4c;border-radius:0}
/* ---- 通用 ---- */
.bullet{position:relative;margin:5px 0;padding-left:16px;color:#2a3340}
.bullet:before{content:"";position:absolute;left:0;top:10px;width:5px;height:1px;background:var(--cyan);transform:none}
.muted{color:var(--ink2);font-size:12.5px;margin:2px 0}
.foot{position:relative;margin-top:52px;padding-top:18px;border-top:1px solid var(--line);
display:flex;justify-content:space-between;font-size:11.5px;color:var(--ink2);letter-spacing:.3px}
.foot:before{content:"";position:absolute;left:50%;top:-3px;width:6px;height:6px;background:#c4a574;
transform:translateX(-50%) rotate(45deg)}
.foot .mark{font-family:var(--display);color:var(--ink);font-weight:600}
@media print{
.fx,.toc{display:none}.content{flex:none;background:#fff}
.inner:after,.cover:before{display:none}.inner{margin:0;padding:0;background:#fff;box-shadow:none;outline:none}
body{background:#fff;color:#122}
.cover h1,.issue h3,.files .fn,.named .card .nm,.tiprow b,.chk .ttl{color:#1b2430;text-shadow:none}
h2{color:#f7f4ee;background:#243040}
.gt{color:#1b2430;background:#d4e4db}
h3{background:#e4d6b0}
.issue h3{background:transparent;padding:0;border:0}
.cover,.metric,.issue,.callout,.entry,.named .card,.compare,.facts,.files,.board{background:#fff;box-shadow:none;backdrop-filter:none}
*{animation:none!important}
.issue,.metric,.callout,.entry,.named .card,.compare{break-inside:avoid}}
@media(max-width:820px){.shell{flex-direction:column}.toc{width:auto;height:auto;position:static}
.toc nav{display:flex;flex-wrap:wrap;gap:0}.toc nav a{margin:0;font-size:14.5px;padding:8px 10px}.metrics{grid-template-columns:repeat(3,1fr)}
.inner{padding:28px 20px 48px;margin:16px 12px 32px;max-width:none;outline-offset:5px}
.cover{padding:8px 80px 20px 0}.cover:before{display:none}.cover .seal{width:60px;height:60px;font-size:12px;padding:4px}
.facts{grid-template-columns:1fr}.facts dt{border-bottom:0;padding-bottom:0}.entry{padding-left:16px}.entry:before{content:none}
.compare .cols{grid-template-columns:1fr}.files li,.meter,.tiprow{grid-template-columns:1fr}.files .ex{display:none}}

"""


class Report:
    """同时累积 HTML 片段与 docx blocks。"""

    def __init__(self, title):
        self.title = title
        self.html = []
        self.blocks = []
        self.sections = []
        self._sec = 0

    def _d(self, kind, text, **opts):
        self.blocks.append((kind, text, opts))

    def cover(self, kicker, title, meta):
        """meta: [(label, value)]"""
        pills = "".join(f"<span class='pill'><b>{esc(l)}</b> {esc(v)}</span>" for l, v in meta if v)
        self.html.append(
            f"<header class='cover'><div class='kicker'>{esc(kicker)}</div>"
            f"<h1>{esc(title)}</h1><div class='meta'>{pills}</div>"
            f"<i class='seal' aria-hidden='true'><span>百</span><span>炼</span><span>标</span><span>书</span></i></header>")
        self._d("title", title)
        self._d("subtitle", "　·　".join(f"{l}：{v}" for l, v in meta if v))

    def h2(self, t):
        self._sec += 1
        sid = f"s{self._sec}"
        self.sections.append((sid, t))
        self.html.append(f"<h2 id='{sid}'>{esc(t)}</h2>")
        self._d("h2", t)

    def h3(self, t):
        self.html.append(f"<h3>{esc(t)}</h3>")
        self._d("h3", t)

    def p(self, t):
        self.html.append(f"<p>{esc_ml(t)}</p>")
        self._d("p", t)

    def bullet(self, t):
        self.html.append(f"<div class='bullet'>{esc_ml(t)}</div>")
        self._d("bullet", t)

    def callout(self, t):
        self.html.append(f"<div class='callout'>{esc_ml(t)}</div>")
        self._d("callout", t)

    def metrics(self, items):
        """items: [(label, value, cls)]"""
        cells = "".join(
            f"<div class='metric {c}'><div class='n'>{esc(v)}</div><div class='l'>{esc(l)}</div></div>"
            for l, v, c in items)
        self.html.append(f"<div class='metrics'>{cells}</div>")
        self._d("p", "　".join(f"{l} {v}" for l, v, _ in items))

    def risk_bar(self, high, review, tip):
        total = max(high + review + tip, 1)
        segs = ""
        for cls, n in (("high", high), ("review", review), ("tip", tip)):
            if n:
                segs += f"<span class='{cls}' style='flex:{n}'></span>"
        if not segs:
            segs = "<span class='none'></span>"
        legend = (f"<span><i style='background:var(--high)'></i>高风险 {high}</span>"
                  f"<span><i style='background:var(--review)'></i>待复核 {review}</span>"
                  f"<span><i style='background:var(--tip)'></i>提示 {tip}</span>")
        self.html.append(f"<div class='riskbar'>{segs}</div><div class='legend'>{legend}</div>")

    def signal_card(self, risk_cls, badge, title, body, note=""):
        h = [f"<div class='issue {risk_cls}'>",
             f"<div class='ihead'><span class='tag {risk_cls}'>{esc(badge)}</span>"
             f"<h3>{esc(title)}</h3></div>"]
        if body:
            h.append(f"<p>{esc_ml(body)}</p>")
        if note:
            h.append(f"<div class='muted'>{esc_ml(note)}</div>")
        h.append("</div>")
        self.html.append("".join(h))
        self._d("issue", f"[{badge}] {title}", risk=risk_cls)
        if body:
            self._d("p", body)
        if note:
            self._d("muted", note)

    def issue_card(self, risk_cls, badge, title, meta, desc, tender, bid, suggestion):
        h = [f"<div class='issue {risk_cls}'>",
             f"<div class='ihead'><span class='tag {risk_cls}'>{esc(badge)}</span>"
             f"<h3>{esc(title)}</h3></div>"]
        if meta:
            h.append(f"<div class='fname'>📄 {esc(meta)}</div>")
        if desc:
            h.append(f"<p>{esc_ml(desc)}</p>")
        if tender or bid:
            h.append("<div class='evi'>")
            if tender:
                h.append(f"<div class='row tender'><span class='lbl'>招标要求</span>{esc_ml(tender)}</div>")
            if bid:
                h.append(f"<div class='row bid'><span class='lbl'>标书现状</span>{esc_ml(bid)}</div>")
            h.append("</div>")
        if suggestion:
            h.append(f"<div class='sug'><b>建议 ▸</b> {esc_ml(suggestion)}</div>")
        h.append("</div>")
        self.html.append("".join(h))
        self._d("issue", f"[{badge}] {title}", risk=risk_cls)
        if meta:
            self._d("muted", meta)
        if desc:
            self._d("p", desc)
        if tender:
            self._d("tender", "招标要求：" + tender)
        if bid:
            self._d("bid", "标书现状：" + bid)
        if suggestion:
            self._d("sug", "建议：" + suggestion)

    def facts(self, pairs):
        rows = [(l, v) for l, v in pairs if v not in (None, "")]
        if not rows:
            return
        cells = "".join(f"<dt>{esc(l)}</dt><dd>{esc_ml(v)}</dd>" for l, v in rows)
        self.html.append(f"<dl class='facts'>{cells}</dl>")
        for l, v in rows:
            self._d("bullet", f"{l}：{v}")

    def _quote_html(self, page, source):
        if not source:
            return "", ""
        pg = f"第{page}页" if page not in (None, "", "?") else "原文"
        html = f"<blockquote class='quote'><span class='pg'>{esc(pg)}</span>{esc_ml(source)}</blockquote>"
        return html, f"原文（{pg}）：{source}"

    def req_group(self, title, items):
        n = len(items)
        self.html.append(
            f"<section class='group'><h3 class='gt'>{esc(title)}<span class='n'>{n} 项</span></h3>")
        self._d("h3", f"{title}（{n} 项）")
        for it in items:
            body = it.get("body", "") if isinstance(it, dict) else str(it)
            page = it.get("page", "") if isinstance(it, dict) else ""
            source = it.get("source", "") if isinstance(it, dict) else ""
            qh, qt = self._quote_html(page, source)
            self.html.append(f"<article class='entry'><p class='body'>{esc_ml(body)}</p>{qh}</article>")
            self._d("p", body)
            if qt:
                self._d("tender", qt)
        self.html.append("</section>")

    def named_cards(self, items):
        self.html.append("<div class='named'>")
        for it in items:
            name, detail = it[0], it[1]
            page = it[2] if len(it) > 2 else ""
            source = it[3] if len(it) > 3 else ""
            self.html.append("<article class='card'>")
            if name:
                self.html.append(f"<div class='nm'>{esc(name)}</div>")
                self._d("h3", name)
            if detail:
                self.html.append(f"<p class='dt'>{esc_ml(detail)}</p>")
                self._d("p", detail)
            qh, qt = self._quote_html(page, source)
            if qh:
                self.html.append(qh)
                self._d("tender", qt)
            self.html.append("</article>")
        self.html.append("</div>")

    def eval_table(self, rows):
        show_weight = any(rec.get("weight") not in (None, "") for rec in rows)
        heads = ["组成部分", "评审项", "评分细则", "分值"]
        if show_weight:
            heads.append("权重")
        th = "".join(f"<th>{esc(h)}</th>" for h in heads)
        self.html.append(f"<table class='board'><thead><tr>{th}</tr></thead><tbody>")
        i = 0
        while i < len(rows):
            comp = rows[i].get("component", "")
            j = i + 1
            while j < len(rows) and rows[j].get("component") == comp:
                j += 1
            span = j - i
            self._d("h3", comp)
            for k in range(i, j):
                rec = rows[k]
                item = rec.get("item") or "—"
                detail = rec.get("detail") or "—"
                score = rec.get("score")
                sc = f"{score} 分" if score not in (None, "") else "—"
                page = rec.get("page", "")
                pg = f"<span class='pg'>第{esc(page)}页</span>" if page not in (None, "", "?") else ""
                cells = []
                if k == i:
                    cells.append(f"<td class='comp' rowspan='{span}'>{esc(comp)}</td>")
                cells.append(f"<td class='item'>{esc(item)}</td>")
                cells.append(f"<td class='detail'>{esc_ml(detail)}{pg}</td>")
                cells.append(f"<td class='sc'>{esc(sc)}</td>")
                if show_weight:
                    w = rec.get("weight")
                    cells.append(f"<td class='sc'>{esc(w) if w not in (None, '') else '—'}</td>")
                self.html.append(f"<tr>{''.join(cells)}</tr>")
                line = f"{comp}　{item}　{detail}　（{sc}）"
                self._d("bullet", line)
            i = j
        self.html.append("</tbody></table>")

    def prio_bullet(self, level, text):
        cls = {"高": "high", "中": "medium", "低": "low"}.get(str(level), "low")
        self.html.append(
            f"<div class='bullet'><span class='prio {cls}'>{esc(level)}</span>{esc_ml(text)}</div>")
        self._d("bullet", f"[{level}] {text}")

    def file_rows(self, rows):
        if not rows:
            return
        items = "".join(
            f"<li><span class='role'>{esc(role)}</span><span class='fn'>{esc(name)}</span>"
            f"<span class='ex'>{esc(extra)}</span></li>"
            for role, name, extra in rows)
        self.html.append(f"<ul class='files'>{items}</ul>")
        for role, name, extra in rows:
            self._d("bullet", f"{role}：{name}" + (f"（{extra}）" if extra else ""))

    def meters(self, items):
        cells = []
        for label, rate in items:
            try:
                width = max(0.0, min(100.0, float(rate) * 100.0))
                shown = f"{width:.1f}%"
            except (TypeError, ValueError):
                width, shown = 0.0, "-"
            cells.append(
                f"<div class='meter'><div class='ml'>{esc(label)}</div>"
                f"<div class='track'><i style='width:{width:.1f}%'></i></div>"
                f"<div class='mv'>{esc(shown)}</div></div>")
        self.html.append(f"<div class='meters'>{''.join(cells)}</div>")
        lines = []
        for label, rate in items:
            try:
                lines.append(f"{label} {float(rate) * 100:.1f}%")
            except (TypeError, ValueError):
                lines.append(f"{label} -")
        self._d("p", "　".join(lines))

    def compare(self, meta, text_a, text_b, label_a="文件A", label_b="文件B"):
        self.html.append(
            f"<article class='compare'><div class='cmeta'>{esc(meta)}</div><div class='cols'>"
            f"<div class='col a'><span class='lbl'>{esc(label_a)}</span><p>{esc_ml(text_a)}</p></div>"
            f"<div class='col b'><span class='lbl'>{esc(label_b)}</span><p>{esc_ml(text_b)}</p></div>"
            f"</div></article>")
        self._d("h3", meta)
        self._d("tender", f"{label_a}：{text_a}")
        self._d("bid", f"{label_b}：{text_b}")

    def tip_row(self, title, desc):
        self.html.append(f"<div class='tiprow'><b>{esc(title)}</b><span>{esc_ml(desc)}</span></div>")
        self._d("bullet", f"{title}：{desc}" if desc else title)

    def check_item(self, checked, title, note="", desc=""):
        mark = "☑" if checked else "☐"
        extra = "".join(
            f"<div class='note'>{esc_ml(x)}</div>" for x in (note, desc) if x)
        self.html.append(
            f"<div class='chk'><div class='box'>{mark}</div>"
            f"<div><div class='ttl'>{esc(title)}</div>{extra}</div></div>")
        line = f"{mark} {title}"
        if note:
            line += f"（备注：{note}）"
        self._d("bullet", line)
        if desc:
            self._d("p", desc)

    def ok_line(self, text):
        self.html.append(f"<p class='okline'>{esc(text)}</p>")
        self._d("p", text)

    def render_html(self):
        nav = "".join(
            f"<a href='#{sid}'><span class='i'>{i:02d}</span><span>{esc(_toc_label(t))}</span></a>"
            for i, (sid, t) in enumerate(self.sections, 1))
        foot = (f"<div class='foot'><span>本报告由「百炼®标书」skill 自动生成</span>"
                f"<span class='mark'>百炼®标书 · {esc(self.title)}</span></div>")
        js = ("<script>(function(){var L=[].slice.call(document.querySelectorAll('.toc nav a'));"
              "var S=L.map(function(a){return document.querySelector(a.getAttribute('href'));});"
              "function spy(){var idx=0;for(var j=0;j<S.length;j++){"
              "if(S[j]&&S[j].getBoundingClientRect().top<=130)idx=j;}"
              "L.forEach(function(a,j){a.classList.toggle('on',j===idx);});}"
              "document.addEventListener('scroll',spy,{passive:true});"
              "window.addEventListener('resize',spy);spy();})();</script>")
        return (f"<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
                f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
                f"<title>{esc(self.title)}</title><style>{_HTML_CSS}</style></head>"
                f"<body><div class='fx' aria-hidden='true'><i class='orb a'></i><i class='orb b'></i>"
                f"<i class='orb c'></i><i class='grid'></i><i class='noise'></i></div><div class='shell'>"
                f"<aside class='toc'><div class='brand'>百炼®标书</div>"
                f"<div class='bt'>{esc(self.title)}</div><nav>{nav}</nav>"
                f"<div class='sfoot'>「百炼®标书」skill</div></aside>"
                f"<main class='content'><div class='accent'>"
                f"<i class='a'></i><i class='b'></i><i class='c'></i></div>"
                f"<div class='inner'>{''.join(self.html)}{foot}</div></main>"
                f"</div>{js}</body></html>")
