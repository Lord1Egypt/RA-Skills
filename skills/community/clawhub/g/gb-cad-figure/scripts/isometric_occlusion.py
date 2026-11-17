#!/usr/bin/env python3
"""
isometric_occlusion.py — 正等轴测【全局遮挡(隐藏线剔除)】通用绘制工具

原理: 把场景里所有实心圆柱(轴//Z)放同一三维空间, 对每条候选轮廓线逐点做
“沿观察方向看, 我前面是否有任意实体的表面挡住我”的全局遮挡判定, 被挡点删除。
连接处(柱顶接台面/柱脚落座/被挡断口)全由同一规则自动算出, 不做分实体各自裁剪。

用法:
    from isometric_occlusion import render_scene
    render_scene(
        entities=[(cx,cy,r,z0,z1), ...],   # 圆柱: 轴心(x,y), 半径r, z范围[z0,z1]
        out_pdf="xxx.pdf", title="...", top_note="...",
        circles=True, side=True,           # 是否画各圆柱顶/底面圆周、侧面母线
    )
每个圆柱自动生成: 顶面圆、底面圆、左右两条侧面母线(可视轮廓)。
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

C30 = math.cos(math.radians(30)); S30 = math.sin(math.radians(30))
_pdfmetrics_registered = False

def _reg_font(path="/usr/share/fonts/HarmonyFont/Harmony-Regular.ttf"):
    global _pdfmetrics_registered
    if not _pdfmetrics_registered:
        pdfmetrics.registerFont(TTFont("HM", path)); _pdfmetrics_registered = True

def iso(x, y, z):
    """正等轴测投影: 观察方向为从斜上方, 深度 d = z - x - y (越大越靠观察者)。"""
    return ((x - y) * C30, (x + y) * S30 + z)

def cyl_fwd_depth(cx, cy, r, z0, z1, up, vp):
    """圆柱在该投影(up,vp)视线线上、最靠近观察者的表面深度; 无交点回None。
    同时考虑侧面柱体与上/下端面圆盘的贡献。"""
    dp = None
    U = up / C30; A = U - (cx - cy); A2 = A / r
    # 侧面柱体
    if A2 * A2 <= 2.0 + 1e-12:
        s2 = 2.0 - A2 * A2
        for sg in (1, -1):
            sig = sg * math.sqrt(max(0.0, s2))
            xs = cx + r * (A2 + sig) / 2.0
            ys = cy + r * (sig - A2) / 2.0
            z = vp - (xs + ys) * S30
            if z0 - 1e-9 <= z <= z1 + 1e-9:
                d = z - (xs + ys)
                if dp is None or d > dp: dp = d
    # 上/下端面圆盘
    for zz in (z0, z1):
        S = (vp - zz) / S30; M = S - (cx + cy)
        if A * A + M * M <= 2.0 * r * r + 1e-9:
            d = zz - S
            if dp is None or d > dp: dp = d
    return dp

def occluded(entities, x, y, z, skip=-1):
    """点(x,y,z)是否被(除skip外的)任意实体遮挡。深度需严格大于+容差(吸收切线处浮点噪声)。"""
    up = (x - y) * C30; vp = (x + y) * S30 + z; dp = z - x - y
    for i, E in enumerate(entities):
        if i == skip: continue
        fwd = cyl_fwd_depth(*E, up, vp)
        if fwd is not None and fwd > dp + 0.05:
            return True
    return False

def _circle(cx, cy, r, z, n=420):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n + 1)]

def _multi(x, y, z0, z1, n=300):
    return [(x, y, z0 + (z1 - z0) * i / n) for i in range(n + 1)]

def build_lines(entities, circles=True, side=True, cn=420, mn=300):
    """为每个圆柱生成候选线: (点列表, skip所属实体, 是否圆)。
    顶面圆/母线: skip自身(母线是可视轮廓,不被自己挡); 底面圆: skip=-1(需被自身顶面挡后半)。"""
    lines = []
    for i, (cx, cy, r, z0, z1) in enumerate(entities):
        if circles:
            lines.append((_circle(cx, cy, r, z1, cn), i, True))    # 顶面圆
            lines.append((_circle(cx, cy, r, z0, cn), -1, True))   # 底面圆
        if side:
            rr = r / math.sqrt(2)
            lines.append((_multi(cx + rr, cy - rr, z0, z1, mn), i, False))
            lines.append((_multi(cx - rr, cy + rr, z0, z1, mn), i, False))
    return lines

def render_scene(entities, out_pdf, title="正等轴测", top_note="",
                 circles=True, side=True, dpi=180, linew=1.4, out_dxf=None):
    """渲染正等轴测去隐藏线图。out_pdf 输出 PDF(并自动出同名 PNG)，out_dxf 可选输出 DXF(单位mm, 2D投影坐标)。"""
    _reg_font()
    lines = build_lines(entities, circles, side)
    W, H = landscape(A4); pad = 50
    allscr = [iso(*p) for ln, _, _ in lines for p in ln]
    xs = [p[0] for p in allscr]; ys = [p[1] for p in allscr]
    minx, maxx = min(xs), max(xs); miny, maxy = min(ys), max(ys)
    ss = min((W - 2 * pad) / max(1.0, maxx - minx), (H - 2 * pad) / max(1.0, maxy - miny)) * 0.95
    ox = (W - (minx + maxx) * ss) / 2; oy = (H - (miny + maxy) * ss) / 2

    c = canvas.Canvas(out_pdf, pagesize=landscape(A4))
    c.setFillColorRGB(1, 1, 1); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColorRGB(0, 0, 0); c.setLineWidth(linew)

    cnt = 0; segments = []
    for ln, skip, _ in lines:
        vis = [False if occluded(entities, x, y, z, skip) else True for (x, y, z) in ln]
        cur_s = []; cur_p = []; segs = []; psegs = []
        for p, ok in zip(ln, vis):
            px = iso(*p)   # 投影mm
            sx = px[0] * ss + ox; sy = px[1] * ss + oy
            if ok:
                cur_s.append((sx, sy)); cur_p.append((px[0], px[1]))
            else:
                if len(cur_s) >= 2: segs.append(cur_s); psegs.append(cur_p)
                cur_s = []; cur_p = []
        if len(cur_s) >= 2: segs.append(cur_s); psegs.append(cur_p)
        segments.extend(psegs)
        for seg in segs:
            pa = c.beginPath(); pa.moveTo(*seg[0])
            for sp in seg[1:]: pa.lineTo(*sp)
            c.drawPath(pa, fill=0, stroke=1); cnt += 1

    c.setFont("HM", 20); c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(W / 2, H - 28, title)
    if top_note:
        c.setFont("HM", 13); c.drawCentredString(W / 2, H - 50, top_note)
    c.save()
    import fitz
    fitz.open(out_pdf)[0].get_pixmap(dpi=dpi).save(out_pdf.replace(".pdf", ".png"))
    if out_dxf:
        import ezdxf
        doc = ezdxf.new("R2010", setup=True); msp = doc.modelspace()
        for seg in segments:
            msp.add_lwpolyline([(round(x,2), round(y,2)) for x,y in seg], close=False)
        doc.saveas(out_dxf)
    return cnt

if __name__ == "__main__":
    # 圆桌示例: 桌面(大圆柱) → 桌柱(中圆柱) → 底盘(扁圆柱)
    DESK_R, DESK_TH = 450, 45
    DESK_Z = 700; LEG_R = 70; BASE_R, BASE_H = 260, 60
    ents = [(0, 0, DESK_R, DESK_Z, DESK_Z + DESK_TH),
            (0, 0, LEG_R, BASE_H, DESK_Z),
            (0, 0, BASE_R, 0, BASE_H)]
    n = render_scene(ents,
                     "/home/sandbox/.openclaw/workspace/cad/圆桌正等轴测-全局遮挡-20260808-0929.pdf",
                     "圆桌 — 正等轴测", "全局遮挡(隐藏线剔除)",
                     out_dxf="/home/sandbox/.openclaw/workspace/cad/圆桌正等轴测-全局遮挡-20260808-0929.dxf")
    print("tool OK, 可见线段:", n)
