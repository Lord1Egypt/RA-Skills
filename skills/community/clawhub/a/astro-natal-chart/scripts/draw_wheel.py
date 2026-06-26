#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Natal chart — wheel (left) + info panel (1/3) + interpretation panel (2/3)."""
import json, math, os, subprocess, sys, argparse, shutil
from collections import Counter
from interp_data import (HOUSE_TEXTS_RU, HOUSE_TEXTS_EN, PLANET_MEANING_RU,
    PLANET_MEANING_EN, SIGN_KEYWORDS_RU, SIGN_KEYWORDS_EN,
    ASPECT_MEANING_RU, ASPECT_MEANING_EN)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    subprocess.check_call([sys.executable,"-m","pip","install","pillow","-q"])
    from PIL import Image, ImageDraw, ImageFont

_ttf_dir = os.path.dirname(os.path.abspath(__file__))
for _f in os.listdir(_ttf_dir):
    if _f.endswith('.ttf.dat'):
        _s = os.path.join(_ttf_dir, _f)
        _d = _s[:-4]
        if not os.path.exists(_d):
            shutil.copy2(_s, _d)

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=["en","ru"], default="en")
parser.add_argument("--name", default="")
parser.add_argument("--conclusion", default="", help="Path to text file with AI conclusion")
parser.add_argument("--frame", default=None, help="Path to frame image .png.dat (QR code) to embed. Default: bundled frame_small.png.dat")
parser.add_argument("date", nargs="?", default="14.12.1991")
parser.add_argument("time", nargs="?", default="18:30")
parser.add_argument("city", nargs="?", default="\u0418\u0436\u0435\u0432\u0441\u043a")
args = parser.parse_args()
RU = (args.lang == "ru")

_SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))

# Load frame image (QR code). Default: bundled frame_small.png.dat
frame_img = None
frame_path = args.frame
if frame_path is None:
    frame_path = os.path.join(_SCRIPTDIR, "frame_small.png.dat")
else:
    if not os.path.isabs(frame_path):
        frame_path = os.path.join(_SCRIPTDIR, frame_path)
frame_path = os.path.normpath(frame_path)
if os.path.exists(frame_path):
    try:
        frame_img = Image.open(frame_path)
        print(f"Frame loaded: {frame_img.size} from {frame_path}")
    except Exception as e:
        print(f"Warning: could not load frame image: {e}")
else:
    print(f"Warning: frame not found at {frame_path}")

res = subprocess.run([sys.executable, os.path.join(_SCRIPTDIR,"natal_chart_swe.py"),
    args.date, args.time, args.city, "--json"],
    capture_output=True, text=True, timeout=30, cwd=_SCRIPTDIR, encoding="utf-8")
if res.returncode != 0: print("Error:", res.stderr or res.stdout); sys.exit(1)
chart = json.loads(res.stdout)
if "error" in chart: print("Error:", chart["error"]); sys.exit(1)

ZSYM = ['\u2648','\u2649','\u264a','\u264b','\u264c','\u264d',
        '\u264e','\u264f','\u2650','\u2651','\u2652','\u2653']
ZAB  = ['AR','TA','GE','CN','LE','VI','LI','SC','SG','CP','AQ','PI']
ZEL  = [0,1,2,3,0,1,2,3,0,1,2,3]
EL_COL = [(80,30,30),(30,70,30),(70,70,30),(30,50,80)]
SIG_COL = [(200,60,60),(80,180,70),(220,190,50),(70,130,220),
           (240,170,40),(100,160,80),(180,90,180),(160,40,70),
           (90,110,210),(100,100,100),(70,170,210),(60,140,140)]
EL_RU = ['\u041e\u0433\u043e\u043d\u044c','\u0417\u0435\u043c\u043b\u044f','\u0412\u043e\u0437\u0434\u0443\u0445','\u0412\u043e\u0434\u0430']
EL_EN = ['Fire','Earth','Air','Water']
SN_RU = ['\u041e\u0432\u0435\u043d','\u0422\u0435\u043b\u0435\u0446','\u0411\u043b\u0438\u0437\u043d\u0435\u0446\u044b','\u0420\u0430\u043a',
         '\u041b\u0435\u0432','\u0414\u0435\u0432\u0430','\u0412\u0435\u0441\u044b','\u0421\u043a\u043e\u0440\u043f\u0438\u043e\u043d',
         '\u0421\u0442\u0440\u0435\u043b\u0435\u0446','\u041a\u043e\u0437\u0435\u0440\u043e\u0433','\u0412\u043e\u0434\u043e\u043b\u0435\u0439','\u0420\u044b\u0431\u044b']
SN_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
PM = {
    "Sun":("SU",(255,220,50),"\u0421\u043e\u043b\u043d\u0446\u0435","Sun"),
    "Moon":("MO",(210,210,220),"\u041b\u0443\u043d\u0430","Moon"),
    "Mercury":("ME",(100,210,100),"\u041c\u0435\u0440\u043a\u0443\u0440\u0438\u0439","Mercury"),
    "Venus":("VE",(80,230,170),"\u0412\u0435\u043d\u0435\u0440\u0430","Venus"),
    "Mars":("MA",(230,70,50),"\u041c\u0430\u0440\u0441","Mars"),
    "Jupiter":("JU",(210,150,60),"\u042e\u043f\u0438\u0442\u0435\u0440","Jupiter"),
    "Saturn":("SA",(150,150,170),"\u0421\u0430\u0442\u0443\u0440\u043d","Saturn"),
    "Uranus":("UR",(100,210,230),"\u0423\u0440\u0430\u043d","Uranus"),
    "Neptune":("NE",(90,140,230),"\u041d\u0435\u043f\u0442\u0443\u043d","Neptune"),
    "Pluto":("PL",(170,80,80),"\u041f\u043b\u0443\u0442\u043e\u043d","Pluto"),
}
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']

def zod(d):
    d=float(d)%360; i=int(d//30); s=d-i*30
    return i,ZAB[i],int(s),int((s-int(s))*60)
def aof(d): return math.radians(90.0-float(d))
def ppos(cx,cy,r,d):
    a=aof(d); return cx+r*math.cos(a),cy-r*math.sin(a)

_SYM = os.path.join(_SCRIPTDIR,"seguisym.ttf")
_TXT = os.path.join(_SCRIPTDIR,"segoeuisl.ttf")
_FC = {}
def fnt(size, sym=False):
    k=(size,sym)
    if k in _FC: return _FC[k]
    fp = _SYM if sym else _TXT
    if os.path.exists(fp):
        try: _FC[k]=ImageFont.truetype(fp,size); return _FC[k]
        except: pass
    _FC[k]=ImageFont.load_default(); return _FC[k]

_ASP_CHARS = frozenset(('\u260c','\u260d','\u25a1','\u25b3','\u2736','\u26b9','\u26ba','\u2220'))

def is_z(ch):
    return ('\u2648'<=ch<='\u2653') or ch in _ASP_CHARS


def ch_w(ch, f):

    bb = f.getbbox(ch); return (bb[2]-bb[0]) if bb else 10

def rtext(draw, x, y, text, size, fill, cy=False):
    sf=fnt(size,sym=True); tf=fnt(size,sym=False)
    if cy:
        bb=tf.getbbox(text); y-=(bb[3]-bb[1])//2
    cx=x
    for ch in text:
        f=sf if is_z(ch) else tf
        draw.text((cx,y),ch,fill=fill,font=f)
        cx+=ch_w(ch,f)

def rcent(draw, cx, y, text, size, fill, ox=0):
    """Center text at cx (+ optional ox offset), starting at y."""
    sf=fnt(size,sym=True); tf=fnt(size,sym=False)
    tw=sum(ch_w(ch,sf if is_z(ch) else tf) for ch in text)
    x=cx-tw//2+ox
    for ch in text:
        f=sf if is_z(ch) else tf
        draw.text((x,y),ch,fill=fill,font=f)
        x+=ch_w(ch,f)

planets_raw=[]
for pn,pd in chart["planets"].items():
    if pn not in PM: continue
    ab,cl,nr,ne=PM[pn]; ln=pd["lon"]; rt=pd["retro"]
    si=int(ln//30); sd=ln-si*30
    planets_raw.append({'key':pn,'abbr':ab,'nr':nr,'ne':ne,
        'lon':ln,'si':si,'sab':ZAB[si],'sym':ZSYM[si],
        'deg':int(sd),'min':int((sd-int(sd))*60),
        'retro':rt,'col':cl,'house':chart["planet_houses"].get(pn,1)})
PO=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]
planets_raw.sort(key=lambda p:PO.index(p['key']) if p['key'] in PO else 99)

houses=chart["houses"]; asc_deg=chart["asc"]; mc_deg=chart["mc"]
house_data=[]
for i in range(12):
    cd=float(houses[i]); ci=int(cd//30); sd=cd-ci*30
    house_data.append({'num':i+1,'rom':ROMAN[i],'cusp_deg':cd,'si':ci,
        'sab':ZAB[ci],'sym':ZSYM[ci],'deg':int(sd),'min':int((sd-int(sd))*60),
        'pls':[p for p in planets_raw if p['house']==i+1]})

asp_data=[]
for a in chart["aspects"]:
    p1=PM.get(a["p1"],('??',))[0]; p2=PM.get(a["p2"],('??',))[0]
    at=a["type"]
    cm={'conjunction':(200,200,200),'sextile':(100,180,240),'square':(220,80,80),
        'trine':(80,220,80),'quincunx':(180,160,60),'opposition':(240,140,40),
        'semisextile':(150,150,100),'semisquare':(150,100,100)}
    asp_data.append({'p1':p1,'p2':p2,'type':at,'col':cm.get(at,(150,150,150))})

asc_z=zod(asc_deg); mc_z=zod(mc_deg)
SN = SN_RU if RU else SN_EN

T = {
    "asc":"\u0410\u0421\u0426" if RU else "ASC",
    "mc":"\u041c\u0421" if RU else "MC",
    "pl":"\u041f\u041b\u0410\u041d\u0415\u0422\u042b" if RU else "PLANETS",
    "asp":"\u0410\u0421\u041f\u0415\u041a\u0422\u042b" if RU else "ASPECTS",
    "el":"\u0421\u0442\u0438\u0445\u0438\u0438" if RU else "Elements",
    "info":"\u041d\u0410\u0422\u0410\u041b\u042c\u041d\u0410\u042f \u041a\u0410\u0420\u0422\u0410" if RU else "NATAL CHART",
    "interp":"\u0418\u041d\u0422\u0415\u0420\u041f\u0420\u0415\u0422\u0410\u0426\u0418\u042f" if RU else "INTERPRETATION",
    "houses":"\u0414\u041e\u041c\u0410" if RU else "HOUSES",
    "aspects_blk":"\u0410\u0421\u041f\u0415\u041a\u0422\u042b \u0418 \u041a\u041e\u041d\u0424\u0418\u0413\u0423\u0420\u0410\u0426\u0418\u0418" if RU else "ASPECTS & CONFIGURATIONS",
    "cj":"\u0421\u043e\u0435\u0434" if RU else "Conj",
    "sx":"\u0421\u0435\u043a\u0441\u0442" if RU else "Sext",
    "sq":"\u041a\u0432\u0430\u0434\u0440" if RU else "Sqr",
    "tr":"\u0422\u0440\u0438\u043d" if RU else "Trine",
    "qn":"\u041a\u0432\u0438\u043d\u043a" if RU else "Quinc",
    "op":"\u041e\u043f\u043f\u043e\u0437" if RU else "Opp",
    "no_planets":"\u043d\u0435\u0442 \u043f\u043b\u0430\u043d\u0435\u0442" if RU else "no planets",
    "stellium":"\u0421\u0422\u0415\u041b\u041b\u0418\u0423\u041c" if RU else "STELLIUM",
    "dominant_el":"\u0414\u043e\u043c\u0438\u043d\u0438\u0440\u0443\u044e\u0449\u0430\u044f \u0441\u0442\u0438\u0445\u0438\u044f" if RU else "Dominant element",
    "retro_mark":" \u211e" if RU else " R",
    "data_title":"\u041e\u0421\u041d\u041e\u0412\u041d\u042b\u0415 \u0414\u0410\u041d\u041d\u042b\u0415" if RU else "ESSENTIAL DATA",
    "planet_table":"\u041f\u041b\u0410\u041d\u0415\u0422\u042b" if RU else "PLANETS",
    "house_table":"\u0414\u041e\u041c\u0410" if RU else "HOUSES",
}

# ═══ LAYOUT ═══
WHEEL = 2160
PANEL_W = 3600
# Info panel = 1/3 of right side, Interp panel = 2/3
INFO_W = PANEL_W // 3       # 1200
INTERP_W = PANEL_W - INFO_W # 2400
TOT_W = WHEEL + PANEL_W     # 5760
TOT_H = TOT_W // 2          # 2880

# Info panel x-origin
IX = WHEEL
# Interp panel x-origin
IPX = WHEEL + INFO_W

img = Image.new('RGB',(TOT_W,TOT_H),(8,8,20))
dw = ImageDraw.Draw(img)
FS=19; FM=22; FL=26; FH=20; FZL=38
LH = 22  # line height for body text

HM = HOUSE_TEXTS_RU if RU else HOUSE_TEXTS_EN
PMean = PLANET_MEANING_RU if RU else PLANET_MEANING_EN
SK = SIGN_KEYWORDS_RU if RU else SIGN_KEYWORDS_EN
AM = ASPECT_MEANING_RU if RU else ASPECT_MEANING_EN

# ═══════════════════════════════════════════════════════════
# LEFT WHEEL
# ═══════════════════════════════════════════════════════════
cx=WHEEL//2; cy=TOT_H//2
RO=960; RS=888; RH=816; RP=648; RI=432

dw.ellipse((cx-RO,cy-RO,cx+RO,cy+RO),fill=(16,16,36),outline=(80,80,130),width=4)
asc_sign_idx = int(asc_deg // 30) % 12
sector_start = asc_sign_idx * 30
for i in range(12):
    sd = sector_start + i * 30
    ed = sector_start + (i + 1) * 30
    sign_idx = (asc_sign_idx + i) % 12
    col = EL_COL[ZEL[sign_idx]]
    pts = [(cx, cy)]
    for j in range(41):
        d = sd + (ed - sd) * j / 40
        a = math.radians(90.0 - d)
        pts.append((cx + RO * math.cos(a), cy - RO * math.sin(a)))
    dw.polygon(pts, fill=col)
dw.ellipse((cx-RO,cy-RO,cx+RO,cy+RO),outline=(180,180,210),width=4)

for i in range(12):
    dc = sector_start + i * 30
    ax,ay=ppos(cx,cy,RO-6,dc); bx,by=ppos(cx,cy,RS-18,dc)
    dw.line([(int(ax),int(ay)),(int(bx),int(by))],fill=(160,160,190),width=2)
    mid_dc = sector_start + i * 30 + 15
    si = (asc_sign_idx + i) % 12
    lx,ly=ppos(cx,cy,RS,mid_dc)
    rcent(dw,int(lx),int(ly),ZSYM[si],FZL,SIG_COL[si])

for i in range(12):
    dc=float(houses[i])
    ax,ay=ppos(cx,cy,RI+12,dc); bx,by=ppos(cx,cy,RH,dc)
    dw.line([(int(ax),int(ay)),(int(bx),int(by))],fill=(90,130,190),width=2)
    nc=float(houses[(i+1)%12])
    mid=dc+(nc-dc)/2 if nc>dc else (dc+(nc+360-dc)/2)%360
    hnx,hny=ppos(cx,cy,RH+48,mid)
    rcent(dw,int(hnx),int(hny),ROMAN[i],FH,(140,170,210))

for lbl,dg,col in [(T["asc"],asc_deg,(255,255,120)),(T["mc"],mc_deg,(255,200,100))]:
    ax,ay=ppos(cx,cy,RI,dg); bx,by=ppos(cx,cy,RO-4,dg)
    dw.line([(int(ax),int(ay)),(int(bx),int(by))],fill=col,width=6)
    lx,ly=ppos(cx,cy,RO+36,dg)
    rcent(dw,int(lx),int(ly),lbl,FM,col)

dw.ellipse((cx-RI,cy-RI,cx+RI,cy+RI),outline=(90,90,140),width=2)

pp_main=[]
for p in planets_raw:
    px,py=ppos(cx,cy,RP,p['lon']); pp_main.append((p,int(px),int(py)))
    r=18
    dw.ellipse((int(px)-r,int(py)-r,int(px)+r,int(py)+r),fill=p['col'],outline=(255,255,255),width=3)
    rcent(dw,int(px),int(py)-42,p['abbr']+('(R)' if p['retro'] else ''),FS-2,p['col'])

for a in asp_data:
    d1=next(((pl,px,py) for pl,px,py in pp_main if pl['abbr']==a['p1']),None)
    d2=next(((pl,px,py) for pl,px,py in pp_main if pl['abbr']==a['p2']),None)
    if d1 and d2: dw.line([(d1[1],d1[2]),(d2[1],d2[2])],fill=a['col'],width=2)

# Legends below wheel
LEG=cy+RO+20
plx=30; ply=LEG; prh=30; pw=310
lb=ply+(len(planets_raw)+1)*prh+14
dw.rectangle((plx-10,ply-10,plx+pw,lb),fill=(12,12,28),outline=(60,60,100),width=2)
rtext(dw,plx,ply,T["pl"],FM-2,(200,200,220))
for idx,p in enumerate(planets_raw):
    ry=ply+prh+idx*prh
    nm=p['nr'] if RU else p['ne']
    lbl="%s  %-3s  %s"%(p['sym'],p['abbr'],nm)
    if p['retro']: lbl+=' R'
    rtext(dw,plx,ry,lbl,FS-2,p['col'])

elx=plx+pw+30; ely=LEG; eeh=30; ew=230
elb=ely+5*eeh+14
dw.rectangle((elx-10,ely-10,elx+ew,elb),fill=(12,12,28),outline=(60,60,100),width=2)
rtext(dw,elx,ely,T["el"],FM-2,(200,200,220))
for ei in range(4):
    ry=ely+eeh+ei*eeh
    enm=EL_RU[ei] if RU else EL_EN[ei]
    dw.rectangle((elx,ry+4,elx+22,ry+24),fill=EL_COL[ei])
    rtext(dw,elx+30,ry,enm,FS-2,(200,200,200))

asx=elx+ew+30; asy=LEG; ash=30; asw=190
asb=asy+7*ash+14
dw.rectangle((asx-10,asy-10,asx+asw,asb),fill=(12,12,28),outline=(60,60,100),width=2)
rtext(dw,asx,asy,T["asp"],FM-2,(200,200,220))
ail=[
    ((200,200,200),"\u260c","Conj"),((100,180,240),"\u2736","Sext"),
    ((220,80,80),"\u25a1","Sqr"),((80,220,80),"\u25b3","Trine"),
    ((180,160,60),"\u26b9","Qnc"),((240,140,40),"\u260d","Opp")
]
for ai,(ac,al,albl) in enumerate(ail):
    ry=asy+ash+ai*ash
    dw.rectangle((asx,ry+4,asx+22,ry+24),fill=ac)
    rtext(dw,asx+30,ry,al+" "+albl,FS-2,ac)

# Panel dividers
dw.line([(IX,0),(IX,TOT_H)],fill=(80,80,120),width=3)
dw.line([(IPX,0),(IPX,TOT_H)],fill=(80,80,120),width=3)

# ═══════════════════════════════════════════════════════════
# HELPER: word-wrap with per-panel max width
# ═══════════════════════════════════════════════════════════
def wrap_text(text, font, max_w):
    words = text.split(' ')
    lines = []
    cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        bb = font.getbbox(test)
        tw = (bb[2]-bb[0]) if bb else 0
        if tw <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# ═══════════════════════════════════════════════════════════
# INFO PANEL (1/3) — Essential data, planet table, house table
# ═══════════════════════════════════════════════════════════
# Padding inside info panel
IP = 18  # inner padding
IXL = IX + IP        # left x for text
IY = 20              # current y
IPW = INFO_W - IP*2  # usable width

def info_text(x, y, text, size, fill, center=False):
    """Draw text in info panel with wrapping."""
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    if center:
        tw = sum(ch_w(ch, sf if is_z(ch) else tf) for ch in text)
        x = x + (IPW - tw) // 2
    for ch in text:
        f = sf if is_z(ch) else tf
        dw.text((x, y), ch, fill=fill, font=f)
        x += ch_w(ch, f)

def info_cent(cx_y, y, text, size, fill):
    """Center text in info panel."""
    info_text(IXL, y, text, size, fill, center=True)

def info_wrap(line, size, max_w, fill, indent=0):
    """Draw a wrapped line in info panel, return height used."""
    global IY
    _tf = fnt(size, sym=False)
    wrapped = wrap_text(line, _tf, max_w)
    for wl in wrapped:
        info_text(IXL + indent, IY, wl, size, fill)
        IY += LH
    return len(wrapped) * LH

def info_divider():
    global IY
    dw.line([(IX+8,IY),(IX+INFO_W-8,IY)],fill=(60,60,100),width=1)
    IY += 10

# ── Chart Title + Name ──
info_cent(IXL, IY, T["info"], FL, (255,255,200))
IY += FL + 14
if args.name:
    info_cent(IXL, IY, args.name, FM, (200,200,240))
    IY += FM + 10

info_divider()

# ── Essential Data ──
info_text(IXL, IY, T["data_title"], FM, (255,220,100))
IY += FM + 6

info_text(IXL, IY, chart["date"]+"  "+chart["time"], FS, (200,200,220)); IY += 22
info_text(IXL, IY, chart["city_full"], FS, (200,200,220)); IY += 22
info_text(IXL, IY, "%.4fN  %.4fE"%(chart["lat"],chart["lon"]), FS-1, (170,170,190)); IY += 22
info_text(IXL, IY, chart["tz"], FS-1, (170,170,190)); IY += 24

asc_s = "%s: %s%s %d\u00b0%d'"%(T["asc"],ZSYM[asc_z[0]],asc_z[1],asc_z[2],asc_z[3])
mc_s = "%s: %s%s %d\u00b0%d'"%(T["mc"],ZSYM[mc_z[0]],mc_z[1],mc_z[2],mc_z[3])
info_text(IXL, IY, asc_s, FS, (255,255,120)); IY += 22
info_text(IXL, IY, mc_s, FS, (255,200,100)); IY += 24

info_divider()

# ── Planet table ──
info_text(IXL, IY, T["planet_table"], FM, (255,220,100))
IY += FM + 4

for p in planets_raw:
    nm = p['nr'] if RU else p['ne']
    retro_s = '\u211e' if p['retro'] else ''
    sign_nm = SN[p['si']]
    line = "%s %s%s %s %d\u00b0%d'" % (p['sym'], nm, retro_s, sign_nm, p['deg'], p['min'])
    # Planet name + sign on one line, wrapped
    info_text(IXL, IY, line, FS-2, p['col'])
    IY += 20
    # House + speed on second line
    h_line = "    %s %d" % (("дом" if RU else "House"), p['house'])
    info_text(IXL, IY, h_line, FS-3, (140,140,160))
    IY += 18
    if IY > TOT_H - 40: break

info_divider()

# ── House cusps table ──
info_text(IXL, IY, T["house_table"], FM, (255,220,100))
IY += FM + 4

for hd in house_data:
    cusp_str = "%s %s %d\u00b0%d'" % (hd['sym'], hd['sab'], hd['deg'], hd['min'])
    line = "%s  %s" % (hd['rom'], cusp_str)
    info_text(IXL, IY, line, FS-2, (180,200,255))
    IY += 20
    # Planets in this house
    if hd['pls']:
        pl_names = ', '.join(("%s%s" % (p['nr'] if RU else p['ne'], '\u211e' if p['retro'] else '')) for p in hd['pls'])
        pl_line = "   %s" % pl_names
        info_wrap(pl_line, FS-3, IPW - 10, (160,180,200))
    else:
        info_text(IXL + 10, IY, T["no_planets"], FS-3, (100,100,120))
        IY += LH
    if IY > TOT_H - 40: break

info_divider()

# ═══ ASPECTS & CONFIGURATIONS (info panel) ══=
info_text(IXL, IY, T["aspects_blk"], FM, (255,220,100))
IY += FM + 4

aspect_symbols = {
    "conjunction":"\u260c","opposition":"\u260d","square":"\u25a1","trine":"\u25b3",
    "sextile":"\u2736","quincunx":"\u26b9","semisextile":"\u26ba","semisquare":"\u2220"
}
for a in asp_data:
    p1n = next((p['nr'] if RU else p['ne'] for p in planets_raw if p['abbr']==a['p1']), a['p1'])
    p2n = next((p['nr'] if RU else p['ne'] for p in planets_raw if p['abbr']==a['p2']), a['p2'])
    asp_sym = aspect_symbols.get(a['type'], '')
    orb_s = ""
    for ca in chart.get("aspects",[]):
        if PM.get(ca.get("p1",""),("",))[0]==a['p1'] and PM.get(ca.get("p2",""),("",))[0]==a['p2']:
            orb_s = " (orb: %.1f\u00b0)"%ca.get("orb",0)
            break
    a_type = a['type']
    a_mean = AM.get(a_type, "")
    line = "%s %s %s%s \u2014 %s" % (p1n, asp_sym, p2n, orb_s, a_mean)
    info_wrap(line, FS-2, IPW - 10, a['col'], indent=0)
    IY += 2
    if IY > TOT_H - 40: break

# Stelliums
sign_counts = Counter(p['si'] for p in planets_raw)
house_counts = Counter(p['house'] for p in planets_raw)
stellium_lines = []
for si, cnt in sign_counts.items():
    if cnt >= 3:
        pls = [p for p in planets_raw if p['si']==si]
        names = ['%s%s'%(p['abbr'],'\u211e' if p['retro'] else '') for p in pls]
        stellium_lines.append("%s \u0432 %s (%d \u043f\u043b\u0430\u043d\u0435\u0442): %s"%(T["stellium"],SN[si],cnt,', '.join(names)) if RU else "%s in %s (%d planets): %s"%(T["stellium"],SN[si],cnt,', '.join(names)))
for hi, cnt in house_counts.items():
    if cnt >= 3:
        pls = [p for p in planets_raw if p['house']==hi]
        names = ['%s%s'%(p['abbr'],'\u211e' if p['retro'] else '') for p in pls]
        stellium_lines.append("%s \u0432 %s \u0434\u043e\u043c\u0435 (%d \u043f\u043b\u0430\u043d\u0435\u0442): %s"%(T["stellium"],ROMAN[hi-1],cnt,', '.join(names)) if RU else "%s in House %s (%d planets): %s"%(T["stellium"],ROMAN[hi-1],cnt,', '.join(names)))
if stellium_lines and IY < TOT_H - 40:
    IY += 4
    for sl in stellium_lines:
        if IY > TOT_H - 40: break
        info_wrap(sl, FS-2, IPW - 10, (255,180,255), indent=0)
        IY += 4

info_divider()

# ── ClawHub link (info panel) ──
if frame_img is not None and IY < TOT_H - 40:
    IY += 10
    _tf = fnt(FS - 2, sym=False)
    _url = "https://clawhub.ai/dynamicsalex/astro-natal-chart"
    _bb = _tf.getbbox(_url)
    _tw = (_bb[2] - _bb[0]) if _bb else 0
    _ux = IXL + (IPW - _tw) // 2
    dw.text((_ux, IY), _url, fill=(80, 80, 120), font=_tf)
    IY += FS + 10

# ── QR code (info panel) ──
if frame_img is not None and IY < TOT_H - 40:
    IY += 14
    frame_w = frame_img.size[0]
    frame_h = frame_img.size[1]
    frame_x = IXL + IPW - frame_w
    frame_y = IY
    if frame_img.mode == 'RGBA':
        img.paste(frame_img, (frame_x, frame_y), frame_img)
    else:
        img.paste(frame_img, (frame_x, frame_y))
    IY += frame_h + 10

# ═══════════════════════════════════════════════════════════
# INTERPRETATION PANEL (2/3) — Full interpretation text
# ═══════════════════════════════════════════════════════════
IPP = 20  # inner padding
IPXL = IPX + IPP   # left x for text in interp panel
YP = 20             # current y in interp panel
IPWW = INTERP_W - IPP*2  # usable width for text

def interp_text(x, y, text, size, fill, center=False):
    """Draw text in interp panel."""
    sf = fnt(size, sym=True); tf = fnt(size, sym=False)
    if center:
        tw = sum(ch_w(ch, sf if is_z(ch) else tf) for ch in text)
        x = x + (IPWW - tw) // 2
    for ch in text:
        f = sf if is_z(ch) else tf
        dw.text((x, y), ch, fill=fill, font=f)
        x += ch_w(ch, f)

def interp_cent(y, text, size, fill):
    """Center text in interp panel."""
    interp_text(IPXL, y, text, size, fill, center=True)

def interp_wrap(line, size, max_w, fill, indent=0):
    """Draw a wrapped line in interp panel, advance YP."""
    global YP
    _tf = fnt(size, sym=False)
    wrapped = wrap_text(line, _tf, max_w)
    for wl in wrapped:
        interp_text(IPXL + indent, YP, wl, size, fill)
        YP += LH
    return len(wrapped) * LH

def interp_divider():
    global YP
    dw.line([(IPX+8,YP),(IPX+INTERP_W-8,YP)],fill=(60,60,100),width=1)
    YP += 10

def draw_interp_section(title, lines, title_clr, body_clr, is_header=False, indent=5):
    """Draw a section with title + body lines in the interp panel."""
    global YP
    _fs = FM if is_header else FS
    if title:
        interp_text(IPXL, YP, title, _fs, title_clr)
        YP += _fs + 6
    _tf = fnt(FS-1, sym=False)
    for line in lines:
        wrapped = wrap_text(line, _tf, IPWW - indent)
        for wl in wrapped:
            interp_text(IPXL + indent, YP, wl, FS-1, body_clr)
            YP += LH
    if is_header:
        YP += 14
    else:
        YP += 8

# ── Title ──
interp_cent(YP, T["interp"], FL+6, (255,220,100))
YP += FL + 18
if args.name:
    interp_cent(YP, args.name, FM+2, (200,200,240))
    YP += FM + 14

interp_divider()

# ═══ CORE INTERPRETATION ═══

# Sun
sun = next((p for p in planets_raw if p['key']=='Sun'), None)
if sun:
    _sn = SN[sun['si']]
    sm = PMean.get('Sun','')
    _sk = SK.get(sun['sab'],'')
    if RU:
        lines = [
            "\u0421\u043e\u043b\u043d\u0446\u0435 \u0432 %s (%d\u00b0%d')  \u2014  %s"%(_sn,sun['deg'],sun['min'],_sk),
            sm,
            "\u0421\u043e\u043b\u043d\u0446\u0435 \u0432 %s \u0434\u0430\u0451\u0442 \u0444\u043e\u043a\u0443\u0441 \u043d\u0430 %s \u0438 \u0441\u043e\u0437\u043d\u0430\u0442\u0435\u043b\u044c\u043d\u0443\u044e \u0441\u0430\u043c\u043e\u043e\u0446\u0435\u043d\u043a\u0443."%(_sn, _sk[:40].lower()),
        ]
    else:
        lines = [
            "Sun in %s (%d\u00b0%d')  \u2014  %s"%(_sn,sun['deg'],sun['min'],_sk),
            sm,
            "The Sun in %s gives focus on %s and conscious self-evaluation."%(_sn, _sk[:40].lower()),
        ]
    draw_interp_section("", lines, (255,220,100), (220,210,180))

# Moon
moon = next((p for p in planets_raw if p['key']=='Moon'), None)
if moon:
    sn = SN[moon['si']]
    mm = PMean.get('Moon','')
    sk = SK.get(moon['sab'],'')
    if RU:
        lines = [
            "\u041b\u0443\u043d\u0430 \u0432 %s (%d\u00b0%d')  \u2014  %s"%(sn,moon['deg'],moon['min'],sk),
            mm,
            "\u041b\u0443\u043d\u0430 \u0432 %s \u0433\u043e\u0432\u043e\u0440\u0438\u0442 \u043e \u0433\u043b\u0443\u0431\u0438\u043d\u043d\u044b\u0445 \u043f\u043e\u0442\u0440\u0435\u0431\u043d\u043e\u0441\u0442\u044f\u0445 \u0432 %s."%(sn, sk[:40].lower()),
        ]
    else:
        lines = [
            "Moon in %s (%d\u00b0%d')  \u2014  %s"%(sn,moon['deg'],moon['min'],sk),
            mm,
            "The Moon in %s speaks of deep needs in %s."%(sn, sk[:40].lower()),
        ]
    draw_interp_section("", lines, (200,200,255), (200,210,220))

# ASC
asc_sn = SN[asc_z[0]]
asc_sk = SK.get(ZAB[asc_z[0]],'')
if RU:
    lines = [
        "\u0410\u0441\u0446\u0435\u043d\u0434\u0435\u043d\u0442: %s (%d\u00b0%d')  \u2014  %s"%(asc_sn,asc_z[2],asc_z[3],asc_sk),
        "\u041c\u0430\u0441\u043a\u0430, \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u0447\u0435\u043b\u043e\u0432\u0435\u043a \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442 \u043c\u0438\u0440\u0443. \u041f\u0435\u0440\u0432\u043e\u0435 \u0432\u043f\u0435\u0447\u0430\u0442\u043b\u0435\u043d\u0438\u0435 \u0438 \u0441\u043f\u043e\u0441\u043e\u0431\u044b \u0430\u0434\u0430\u043f\u0442\u0430\u0446\u0438\u0438.",
    ]
else:
    lines = [
        "Ascendant: %s (%d\u00b0%d')  \u2014  %s"%(asc_sn,asc_z[2],asc_z[3],asc_sk),
        "The mask the person shows to the world. First impression and adaptation strategies.",
    ]
draw_interp_section("", lines, (255,255,120), (220,220,200))

# Dominant element
el_count = [0,0,0,0]
for p in planets_raw:
    el_count[ZEL[p['si']]] += 1
dom_el = max(range(4), key=lambda i: el_count[i])
el_names = EL_RU if RU else EL_EN
el_desc_ru = ["\u043d\u0430\u043f\u043e\u0440\u0438\u0441\u0442\u043e\u0441\u044c \u0438 \u0438\u043d\u0438\u0446\u0438\u0430\u0442\u0438\u0432\u0430","\u043f\u0440\u0430\u043a\u0442\u0438\u0447\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c","\u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442 \u0438 \u043a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u044f","\u044d\u043c\u043e\u0446\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0438 \u0438\u043d\u0442\u0443\u0438\u0446\u0438\u044f"]
el_desc_en = ["assertiveness and initiative","practicality and stability","intellect and communication","emotionality and intuition"]
dom_line = "%s: %s (%d \u043f\u043b\u0430\u043d\u0435\u0442) \u2014 %s"%(T["dominant_el"],el_names[dom_el],el_count[dom_el],el_desc_ru[dom_el] if RU else el_desc_en[dom_el])
draw_interp_section(dom_line, [], (180,255,180), (200,220,200))

# Stelliums
sign_counts = Counter(p['si'] for p in planets_raw)
house_counts = Counter(p['house'] for p in planets_raw)
stellium_lines = []
for si, cnt in sign_counts.items():
    if cnt >= 3:
        pls = [p for p in planets_raw if p['si']==si]
        names = ['%s%s'%(p['abbr'],'\u211e' if p['retro'] else '') for p in pls]
        stellium_lines.append("%s \u0432 %s (%d \u043f\u043b\u0430\u043d\u0435\u0442): %s"%(T["stellium"],SN[si],cnt,', '.join(names)))
for hi, cnt in house_counts.items():
    if cnt >= 3:
        pls = [p for p in planets_raw if p['house']==hi]
        names = ['%s%s'%(p['abbr'],'\u211e' if p['retro'] else '') for p in pls]
        stellium_lines.append("%s \u0432 %s \u0434\u043e\u043c\u0435 (%d \u043f\u043b\u0430\u043d\u0435\u0442): %s"%(T["stellium"],ROMAN[hi-1],cnt,', '.join(names)))
if stellium_lines:
    draw_interp_section("", stellium_lines, (255,180,255), (220,200,220))

# Retrograde planets
retro = [p for p in planets_raw if p['retro']]
if retro:
    rlines = []
    for p in retro:
        if RU:
            rlines.append("%s %s%s %d\u00b0%d' \u0432 %s \u0434\u043e\u043c\u0435 (%s) \u2014 \u044d\u043d\u0435\u0440\u0433\u0438\u044f \u043f\u043e\u0432\u0435\u0440\u043d\u0443\u0442\u0430 \u0432\u043d\u0443\u0442\u044c, \u043a\u0430\u0440\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0443\u0440\u043e\u043a\u0438" % (
                p['sym'], p['nr'],'\u211e',p['deg'],p['min'],ROMAN[p['house']-1], p['key']))
        else:
            rlines.append("%s %s%s %d\u00b0%d' in House %s (%s) \u2014 internalized energy, karmic lessons" % (
                p['sym'], p['ne'],' R',p['deg'],p['min'],ROMAN[p['house']-1], p['key']))
    draw_interp_section("", rlines, (180,180,255), (200,200,220))

interp_divider()

# ═══ HOUSES WITH INTERPRETATION ═══
interp_text(IPXL, YP, T["houses"], FL, (255,220,100))
YP += FL + 6

for i, ht in enumerate(HM):
    if YP > TOT_H - 80: break
    hd = house_data[i]
    pls_in_house = hd['pls']

    cusp_str = "%s %s %d\u00b0%d'"%(hd['sym'], hd['sab'], hd['deg'], hd['min'])
    title_str = "%s  [%s]"%(ht['title'], cusp_str)
    interp_text(IPXL, YP, title_str, FS, (180,200,255))
    YP += 22

    tf = fnt(FS-1, sym=False)
    for body_line in ht['body']:
        wrapped = wrap_text(body_line, tf, IPWW - 20)
        for wl in wrapped:
            interp_text(IPXL + 8, YP, wl, FS-1, (180,180,200))
            YP += LH
        if YP > TOT_H - 60: break

    if pls_in_house and YP < TOT_H - 60:
        for p in pls_in_house:
            if YP > TOT_H - 60: break
            pnm = p['nr'] if RU else p['ne']
            pmean = PMean.get(p['key'],'')
            ppos_str = "%s %s %d\u00b0%d'"%(p['sym'],p['sab'],p['deg'],p['min'])
            retro_s = '\u211e' if p['retro'] else ''
            if RU:
                planet_line = "  \u25e6 %s (%s%s %s) \u0432 %s \u0434\u043e\u043c\u0435" % (pnm, p['abbr'], retro_s, ppos_str, ROMAN[p['house']-1])
                meaning_line = "    \u25e6 \u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435: %s. %s \u0432 \u044d\u0442\u043e\u043c \u0434\u043e\u043c\u0435 \u043f\u0440\u043e\u044f\u0432\u043b\u044f\u0435\u0442 %s" % (pmean, pnm, ht['title'].split('\u2014')[1].strip()[:30] if '\u2014' in ht['title'] else ht['title'][:30])
            else:
                planet_line = "  \u25e6 %s (%s%s %s) in House %s" % (pnm, p['abbr'], ' R' if p['retro'] else '', ppos_str, ROMAN[p['house']-1])
                meaning_line = "    \u25e6 Meaning: %s. %s expresses %s in this house" % (pmean, pnm, ht['title'].split('\u2014')[1].strip()[:30] if '\u2014' in ht['title'] else ht['title'][:30])
            interp_wrap(planet_line, FS-1, IPWW - 15, p['col'], indent=8)
            if YP < TOT_H - 40:
                interp_wrap(meaning_line, FS-2, IPWW - 20, (160,160,180), indent=12)
    elif YP < TOT_H - 40:
        interp_text(IPXL + 8, YP, "  \u25e6 "+T["no_planets"], FS-1, (130,130,150))
        YP += LH

    YP += 6
    # Divider every 3 houses
    if (i+1) % 3 == 0 and i < 11 and YP < TOT_H - 100:
        dw.line([(IPX+10,YP),(IPX+INTERP_W-10,YP)],fill=(40,40,70),width=1)
        YP += 8

# ═══ CONCLUSION (AI-generated) ══=
conclusion_text = ""
if args.conclusion:
    try:
        with open(args.conclusion, "r", encoding="utf-8") as cf:
            conclusion_text = cf.read().strip()
    except Exception as e:
        print("Warning: cannot read conclusion file:", e)

if conclusion_text:
    # Visual separator
    YP += 8
    dw.line([(IPX+30,YP),(IPX+INTERP_W-30,YP)],fill=(120,100,60),width=2)
    YP += 18
    # Title
    _conc_title = "\u0417\u0410\u041a\u041b\u042e\u0427\u0415\u041d\u0418\u0415" if RU else "CONCLUSION"
    interp_text(IPXL, YP, _conc_title, FL, (255,215,0))
    YP += FL + 10
    # Body text — wrap to full interp panel width
    _tf = fnt(FS-1, sym=False)
    for para in conclusion_text.split("\n"):
        if not para.strip():
            YP += 6
            continue
        wrapped = wrap_text(para.strip(), _tf, IPWW - 16)
        for wl in wrapped:
            if YP > TOT_H - 60: break
            interp_text(IPXL + 8, YP, wl, FS-1, (240,230,200))
            YP += LH  
        YP += 4
    # Decorative bottom line
    if YP < TOT_H - 80:
        YP += 6
        dw.line([(IPX+60,YP),(IPX+INTERP_W-60,YP)],fill=(120,100,60),width=1)
        YP += 14



# ═══ Save ═══
_name_clean = args.name.replace(" ", "_") if args.name else "chart"
_out = os.path.join(r"C:\Users\alter\.openclaw\workspace", "%s_full_natal_%s.png" % (_name_clean, "ru" if RU else "en"))
img.save(_out, "PNG")
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass
print("Saved:", _out, img.size)
