# -*- coding: utf-8 -*-
"""Build progressively richer decks so we can bisect which feature PowerPoint rejects."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
import deck as D

# Run-specific output dir (never reuses or deletes previous runs):
# default ./output/bis_<timestamp>, override with env var QIANTI_OUT.
OUT = os.environ.get(
    "QIANTI_OUT",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "output",
                 "bis_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
os.makedirs(OUT, exist_ok=True)


def new():
    prs = Presentation()
    prs.slide_width = D.E(13.333)
    prs.slide_height = D.E(7.5)
    return prs, prs.slides.add_slide(prs.slide_layouts[6])


steps = []

# v0 plain rounded rectangle
def v0(s):
    D.rrect(s, 1, 1, 3, 2, adj=0.1, fill=D.CARD)
steps.append(("v0_plain", v0))

# v1 + translucent solid fill
def v1(s):
    D.rrect(s, 1, 1, 3, 2, adj=0.1, fill=D.WHITE, alpha=13)
steps.append(("v1_alpha", v1))

# v2 + gradient fill
def v2(s):
    sh = D.rrect(s, 1, 1, 3, 2, adj=0.1)
    D.grad(sh, [(0, D.PINK_DP), (100, D.PINK_LT)], 0)
steps.append(("v2_gradient", v2))

# v3 + custom shadow
def v3(s):
    sh = D.rrect(s, 1, 1, 3, 2, adj=0.1, fill=D.CARD)
    D.shadow(sh, blur=20, dist=6, alpha=40)
steps.append(("v3_shadow", v3))

# v4 + dashed connector
def v4(s):
    D.connector(s, 1, 1, 5, 1, D.LAV, 1.3, alpha=90)
steps.append(("v4_connector", v4))

# v5 + bullet paragraph with custom font
def v5(s):
    tf = D.box(s, 1, 1, 5, 2)
    D.para(tf, "测试条目一", 17, D.MAGENTA, True, first=True, space_after=13,
           line_spacing=1.28, bullet=("●", D.MAGENTA))
steps.append(("v5_bullet", v5))

# v6 + round2SameRect with adj2
def v6(s):
    D.rrect(s, 1, 1, 4, 2, adj=0.075, adj2=0.0, fill=D.CARD_TINT,
            kind=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
steps.append(("v6_round2", v6))

# v7 + picture + star
def v7(s):
    D.pic(s, "gear", 1, 1, 2, 2)
    D.rrect(s, 4, 1, 0.4, 0.4, adj=0, fill=D.YELLOW, alpha=100, kind=MSO_SHAPE.STAR_4_POINT)
steps.append(("v7_pic_star", v7))

# v8 + rotated triangle + text alignment
def v8(s):
    D.rrect(s, 1, 1, 0.42, 0.52, adj=0, fill=D.PINK_DP,
            kind=MSO_SHAPE.ISOSCELES_TRIANGLE, rot=270)
    tf = D.box(s, 3, 1, 4, 0.6, MSO_ANCHOR.MIDDLE)
    D.para(tf, "PT内部培训系列：", 22, D.PLUM_DK, True, PP_ALIGN.CENTER, first=True)
steps.append(("v8_tri_text", v8))

for name, fn in steps:
    prs, s = new()
    fn(s)
    prs.save(os.path.join(OUT, name + ".pptx"))
    print("built", name)
