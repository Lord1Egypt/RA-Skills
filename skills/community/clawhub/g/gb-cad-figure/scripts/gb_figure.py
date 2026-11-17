#!/usr/bin/env python3
"""国标正式工程图纸通用引擎 V3 —— 横/竖布局自动选择 + 按主体自动选图幅(标准尺寸)。
方向自动选择: 高型主体(高>宽)→竖版; 宽型主体(宽>高)→横版。
竖版: 标题栏底部横贯(高30, 宽=图框宽), 自下而上 标题栏→图例→说明→绘图区; 装订边左25/其余三边10。
横版: 标题栏右下角(180×56, 标签|内容分格), 右侧栏 技术说明(上)/图例(下), 主体在左绘图区; 装订边左20/其余三边5。
选图幅: 按主体量级(名义尺寸≤图幅短边)选相称标准图幅, 比例取能容纳的最小标准比。
交付 PDF + DXF(mm, 汉字 gbenor.shx+gbcbig.shx 大字体防方块)。
"""
import math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("HM","/usr/share/fonts/HarmonyFont/Harmony-Regular.ttf"))
LATHE_ARCH=None   # 瓶底拱高(mm); None=自动(默认外凸), 0=平底, >0指定外凸
LATHE_RIBS=None   # 回转体可见素线(经线)角度(度)列表; None=不画素线, 如 [-9,27,63,99]
LATHE_BOT=None    # 瓶底可见前缘半圆; None=默认(θ180→360), 'front'=面向观察者(θ135→315,cos+sin<0,令素线下端落在瓶底弧上)
LATHE_RIB_SIDE=None # 素线可见侧; None=cos+sin>0(旧), 'front'=cos+sin<0(正确正等轴测前表面)
C30=math.cos(math.radians(30)); S30=math.sin(math.radians(30))
def iso(x,y,z): return ((x-y)*C30,(x+y)*S30+z)
MM=2.834645669

# ---------- 实体遮挡(cyl+box) ----------
def cyl_fwd_depth(cx,cy,r,z0,z1,up,vp):
    dp=None; U=up/C30; A=U-(cx-cy); A2=A/r
    if A2*A2<=2.0+1e-12:
        s2=2.0-A2*A2
        for sg in (1,-1):
            sig=sg*math.sqrt(max(0.0,s2))
            xs=cx+r*(A2+sig)/2.0; ys=cy+r*(sig-A2)/2.0; z=vp-(xs+ys)*S30
            if z0-1e-9<=z<=z1+1e-9:
                d=z-(xs+ys)
                if dp is None or d>dp: dp=d
    for zz in (z0,z1):
        S=(vp-zz)/S30; M=S-(cx+cy)
        if A*A+M*M<=2.0*r*r+1e-9:
            d=zz-S
            if dp is None or d>dp: dp=d
    return dp
def box_fwd_depth(cx,cy,a,b,z0,z1,up,vp):
    U=up/C30
    Wlo=max(2*(cx-a)-U,2*(cy-b)+U,(vp-z1)/S30)
    Whi=min(2*(cx+a)-U,2*(cy+b)+U,(vp-z0)/S30)
    if Wlo<=Whi+1e-9: return vp-Wlo*(1+S30)
    return None
def lathe_fwd_depth(cx,cy,contour,up,vp):
    """平滑回转体(lathe)的近似前向遮挡深度: 用最大半径圆柱近似, 偏保守(优先删隐藏线)."""
    rm=max(r for z,r in contour); zs=[z for z,r in contour]
    return cyl_fwd_depth(cx,cy,rm,min(zs),max(zs),up,vp)
def occluded(x,y,z,ENT,skip=-1):
    up=(x-y)*C30; vp=(x+y)*S30+z; dp=z-x-y
    for i,E in enumerate(ENT):
        if i==skip: continue
        if E[0]=='lathe': f=lathe_fwd_depth(*E[1:],up,vp)
        elif E[0]=='cyl': f=cyl_fwd_depth(*E[1:],up,vp)
        else:            f=box_fwd_depth(*E[1:],up,vp)
        if f is not None and f>dp+0.05: return True
    return False
def _seg(x1,y1,z1,x2,y2,z2,n=50):
    return [(x1+(x2-x1)*i/n,y1+(y2-y1)*i/n,z1+(z2-z1)*i/n) for i in range(n+1)]
def _circ(cx,cy,r,z,n=360):
    return [(cx+r*math.cos(2*math.pi*i/n),cy+r*math.sin(2*math.pi*i/n),z) for i in range(n+1)]
def _col(x,y,z0,z1,n=400):
    return [(x,y,z0+(z1-z0)*i/n) for i in range(n+1)]
def lathe_profile(cx,cy,contour,n=48):
    """平滑回转体(lathe): contour=list of (z,r) 折点. 返回 左母线/右母线/顶口圆/底前缘圆 的3D点列.
    r(z) 用 Catmull-Rom 样条插值(通过所有折点,C1连续), 等轴测下左右母线即平滑弧线轮廓."""
    pts=sorted(contour); czs=[z for z,r in pts]; crs=[r for z,r in pts]
    def r_at(z):
        if z<=czs[0]: return crs[0]
        if z>=czs[-1]: return crs[-1]
        i=0
        while i<len(czs)-2 and z>czs[i+1]: i+=1
        p0=crs[max(0,i-1)]; p1=crs[i]; p2=crs[i+1]; p3=crs[min(len(crs)-1,i+2)]
        t=(z-czs[i])/(czs[i+1]-czs[i])
        r=0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
        return r if r>0.4 else 0.4
    zmin,zmax=czs[0],czs[-1]
    zs=[zmin+(zmax-zmin)*i/n for i in range(n+1)]
    if LATHE_BOT=='front':
        # 用户选方案: 保留底面椭圆长轴水平露出, 并把左右粗实线(轮廓母线)底端移到底面椭圆弧端头(θ135/315, 投影±24.5, y=0), 与底面弧两端完全衔接
        _c=0.7071067811865476
        left=[(cx-_c*r_at(z), cy+_c*r_at(z), z) for z in zs]   # θ135, 底端(-24.5,0)
        right=[(cx+_c*r_at(z), cy-_c*r_at(z), z) for z in zs]  # θ315, 底端(+24.5,0)
    else:
        left=[(cx-r_at(z),cy,z) for z in zs]; right=[(cx+r_at(z),cy,z) for z in zs]
    top=_circ(cx,cy,crs[-1],zmax)
    # 瓶底拱形前缘轮廓: 默认(θ180→360连接左右母线底); 'front'=面向观察者(θ-45→135, cos+sin>0), 令可见素线下端落在瓶底弧上
    arch = (max(4.0,min(10.0,0.05*(czs[-1]-czs[0]))) if LATHE_ARCH is None else LATHE_ARCH)
    if LATHE_BOT=='front':
        # 正等轴测正确画法: 底面圆投影为长轴水平的标准椭圆, 可见前弧=θ135°~315°(长轴端点, 比半圆大), 两端露在轮廓外侧(轮廓在椭圆内侧)
        _b=[(cx+crs[0]*math.cos(th), cy+crs[0]*math.sin(th), zmin-arch*(math.sin(th))) for th in (3*math.pi/4+math.pi*(k/n) for k in range(n+1))]
    else:
        _b=[(cx+crs[0]*math.cos(th), cy+crs[0]*math.sin(th), zmin-arch*(-math.sin(th))) for th in (math.pi+math.pi*(k/n) for k in range(n+1))]
    bot=_b
    # 可见素线(经线): 仅画朝向前方(观察者)的表面竖线, 增强圆柱/曲面立体感
    ribs=[]
    if LATHE_RIBS:
        # 素线作为完整曲面经线: 从瓶底半圆(zmin)贯穿到瓶口(zmax), 两端落在瓶底圆/瓶口圆上(用户明确要求半圆到瓶口连起)
        zr=[zmin+(zmax-zmin)*i/n for i in range(n+1)]
        for deg in LATHE_RIBS:
            a=math.radians(deg)
            if LATHE_RIB_SIDE=='front':
                if math.cos(a)+math.sin(a) >= -1e-6: continue   # 只画cos+sin<0(正确正等轴测前表面)
            else:
                if math.cos(a)+math.sin(a) <= 1e-6: continue      # 旧:只画cos+sin>0
            ribs.append([(cx+r_at(z)*math.cos(a), cy+r_at(z)*math.sin(a), z) for z in zr])
    return left,right,top,bot,ribs

def box_edges(cx,cy,a,b,z0,z1):
    VEC=(-1,-1,1)
    A=(cx-a,cy-b,z1);B=(cx+a,cy-b,z1);C=(cx+a,cy+b,z1);D=(cx-a,cy+b,z1)
    E=(cx-a,cy-b,z0);F=(cx+a,cy-b,z0);G=(cx+a,cy+b,z0);H=(cx-a,cy+b,z0)
    faces={'top':([A,B,C,D],(0,0,1)),'x-':([A,D,H,E],(-1,0,0)),'x+':([B,C,G,F],(1,0,0)),
           'y-':([A,B,F,E],(0,-1,0)),'y+':([D,C,G,H],(0,1,0)),'bot':([E,F,G,H],(0,0,-1))}
    seg={}
    for (pts,nv) in faces.values():
        if VEC[0]*nv[0]+VEC[1]*nv[1]+VEC[2]*nv[2]<=0: continue
        for k in range(4): seg[tuple(sorted((pts[k],pts[(k+1)%4])))]=1
    return [(list(k[0]),list(k[1])) for k in seg]

# ---------- 图幅 ----------
# 横版(宽≥高) / 竖版(高≥宽); 尺寸按主体量级匹配(名义尺寸≤图幅短边)
FRAMES_HB=[dict(na="A4",W=297,H=210),dict(na="A3",W=420,H=297),dict(na="A2",W=594,H=420),
           dict(na="A1",W=841,H=594),dict(na="A0",W=1189,H=841)]
FRAMES_VS=[dict(na="A4",W=210,H=297),dict(na="A3",W=297,H=420),dict(na="A2",W=420,H=594),
           dict(na="A1",W=594,H=841),dict(na="A0",W=841,H=1189)]
STD=[0.5,1,2,5,10,20,50,100,200,500,1000]
def ratio_label(N):
    if abs(N-1)<1e-6: return "1:1"
    if N>1: return "1:%d"%round(N)
    return "%d:1"%round(1/N)
def body_size(ENT):
    xs=[]; zs=[]
    for E in ENT:
        if E[0]=='cyl': cx,cy,r,z0,z1=E[1:]; xs+=[cx-r,cx+r]; zs+=[z0,z1]
        elif E[0]=='lathe': cx,cy,ct=E[1:]; rm=max(r for z,r in ct); xs+=[cx-rm,cx+rm]; zs+=[min(z for z,r in ct),max(z for z,r in ct)]
        else:          cx,cy,a,b,z0,z1=E[1:]; xs+=[cx-a,cx+a]; zs+=[z0,z1]
    return (max(xs)-min(xs)), (max(zs)-min(zs))
def body_plot(ENT):
    """返回主体所有已遮蔽成2D后的包围盒(minx,maxx,miny,maxy), 用于fit."""
    xs=[];ys=[];L=[]
    for idx,(tp,cx,cy,*R) in enumerate(ENT):
        if tp=='box':
            a,b,z0,z1=R
            for e1,e2 in box_edges(cx,cy,a,b,z0,z1): L.append((_seg(*e1,*e2),idx))
        elif tp=='lathe':
            ct=R[0]; left,right,top,bot,ribs=lathe_profile(cx,cy,ct)
            L.append((left,idx)); L.append((right,idx)); L.append((top,idx)); L.append((bot,'VISSEG') if LATHE_BOT=='front' else (bot,idx))
            for rb in ribs: L.append((rb,'VIS'))
        else:
            r,z0,z1=R
            L.append((_circ(cx,cy,r,z1),idx)); L.append((_circ(cx,cy,r,z0),-1))
            rr=r/math.sqrt(2)
            L.append((_col(cx+rr,cy-rr,z0,z1),idx)); L.append((_col(cx-rr,cy+rr,z0,z1),idx))
    for ln,skip in L:
        vis=[True]*len(ln) if skip=='VIS' else [False if occluded(x,y,z,ENT,skip) else True for (x,y,z) in ln]
        cur=[]
        for p,ok in zip(ln,vis):
            if ok: cur.append(iso(*p))
            else:
                if len(cur)>=2: xs+=[q[0] for q in cur]; ys+=[q[1] for q in cur]
                cur=[]
        if len(cur)>=2: xs+=[q[0] for q in cur]; ys+=[q[1] for q in cur]
    return min(xs),max(xs),min(ys),max(ys)

# ---------- 布局 ----------
def pick_frame(dr,S,bbw,bbh,legh,exph):
    """按主体量级选相称标准图幅, 比例按含尺寸bbox能容纳的最小标准比; 若某图幅需把主体缩到>1:2, 自动升下一档图幅保比例."""
    FM=FRAMES_VS if dr=='vs' else FRAMES_HB
    BIND=25; RIM=10 if dr=='vs' else 5
    TBW=0 if dr=='vs' else 180; TBH=45 if dr=='vs' else 56; GAP=10
    last=FM[-1]
    for f in FM:
        W,H=f["W"],f["H"]
        if dr=='vs':
            OCC=TBH+legh+exph+3*GAP
            AW=W-BIND-RIM; AH=(H-RIM)-(RIM+OCC)
        else:
            AW=W-BIND-RIM-2*GAP-TBW
            AH=H-RIM-(RIM+TBH+GAP)
        AW-=10; AH-=10
        Nmin=max(bbw/max(AW,1), bbh/max(AH,1))
        N=min(n for n in STD if n>=Nmin) if Nmin>1 else 1.0
        if N<=2 or f is last:
            return dict(na=f["na"],W=W,H=H,N=N)

def vs_layout(W,H,N,名称,图号,日期,rl,tech,leg):
    return dict(dr='vs',BIND=25,RIM=10,TBW=W-25-10,TBH=45,GAP=10,thk=1.15,   # A4 竖版标题栏高45mm, 文字 3.5~5mm
                tbc=[0,16,66,80,104,116,140,152,W-25-10],tbz=[0,15,30,45],
                legh=max(30,min(90,26+len(leg)*13)),exph=max(24,min(80,17+len(tech)*9)),
                title=(名称,图号,日期,rl))
def hb_layout(W,H,N,名称,图号,日期,rl,tech,leg):
    BIND=25;RIM=5;TBW=min(180,W-BIND-RIM);TBH=56;GAP=10
    return dict(dr='hb',BIND=BIND,RIM=RIM,TBW=TBW,TBH=TBH,GAP=GAP,thk=1.6,   # A0~A3 标题栏文字 5~7mm
                tbc=[0,26,52,78,110,TBW],tbz=[0,19,38,56],   # 紧凑: 签字区(左)+信息区(中)+图名大格(右占全高), 无冗余空格
                legh=max(30,min(90,26+len(leg)*13)),exph=max(24,min(80,17+len(tech)*9)),
                title=(名称,图号,日期,rl))

def layout_boxes2(L):
    dr=L["dr"]; W=L["W"]; H=L["H"]; B,Ld=L["BIND"],L["RIM"]; TBW=L["TBW"];TBH=L["TBH"];GAP=L["GAP"]
    legh,exph=L["legh"],L["exph"]
    drx0=B+6; dry1=H-Ld
    if dr=='vs':
        tb=(B,Ld,B+TBW,Ld+TBH)
        drx1=W-Ld-6; dry0=Ld+TBH+GAP+legh+GAP+exph+GAP
        lg=(B,tb[3]+GAP,B+TBW,tb[3]+GAP+legh)
        ex=(B,lg[3]+GAP,B+TBW,lg[3]+GAP+exph)
        dry0=ex[3]+GAP
    else:
        tb=(W-Ld-TBW,Ld,W-Ld,Ld+TBH)
        drx1=W-Ld-TBW-GAP-4; dry0=Ld+TBH+GAP+6
        rc_x0=W-Ld-TBW+3; rc_x1=W-Ld-2
        ex_y1=H-Ld-GAP; ex=(rc_x0,ex_y1-exph,rc_x1,ex_y1)      # 说明(上), 顶边与内框上边线留 GAP(10) 不贴合
        lg=(rc_x0,tb[3]+GAP,rc_x1,tb[3]+GAP+legh)               # 图例(下)紧邻标题栏
    return dict(tb=tb,lg=lg,ex=ex,dr=(drx0,dry0,drx1,dry1))

def _build_poly(c,pts):
    pa=c.beginPath(); pa.moveTo(pts[0][0],pts[0][1])
    for p in pts[1:]: pa.lineTo(p[0],p[1]); 
    return pa

def generate(名称,图号,ENT,DIMS,日期,out,tech,leg,direction='auto',LDIMS=None,bottom_arch=None,lathe_ribs=None,bot_visible=None,rib_side=None):
    global LATHE_ARCH, LATHE_RIBS, LATHE_BOT, LATHE_RIB_SIDE; LATHE_ARCH=bottom_arch; LATHE_RIBS=lathe_ribs; LATHE_BOT=bot_visible; LATHE_RIB_SIDE=rib_side
    # ---- 主体遮蔽2D + 尺寸 ----
    mnx,mxx,mny,mxy=body_plot(ENT)
    EXTL=[]; DIMLN=[]; dimtxt=[]
    for txt,A3,B3,off,rot in DIMS:
        a0=tuple(A3); b0=tuple(B3)
        a1=(A3[0]+off[0],A3[1]+off[1],A3[2]+off[2]); b1=(B3[0]+off[0],B3[1]+off[1],B3[2]+off[2])
        ol=math.sqrt(off[0]**2+off[1]**2+off[2]**2) or 1; u=(off[0]/ol,off[1]/ol,off[2]/ol)
        EXTL+=[(iso(*a0),iso(*a1)),(iso(*b0),iso(*b1))]
        DIMLN.append((iso(*a1),iso(*b1)))
        at,bt=iso(*a1),iso(*b1); dimtxt.append((txt,(at[0]+bt[0])/2,(at[1]+bt[1])/2,rot))
    LD_LEAD=[]; LD_TXT=[]
    if LDIMS:
        for it in LDIMS:
            txt=it[0]; a=(it[1],it[2],it[3]); d=(it[4],it[5],it[6]); e=(a[0]+d[0],a[1]+d[1],a[2]+d[2])
            LD_LEAD.append((iso(*a),iso(*e))); LD_TXT.append((txt,*iso(*e),0))
    # ---- 尺寸bbox + 图例/说明高(提前算, 供 auto 与选幅) ----
    _ps=[(mnx,mny),(mxx,mxy)]
    for _a,_b in EXTL+DIMLN: _ps.append(_a); _ps.append(_b)
    for _t,_x,_y,_r in dimtxt: _ps.append((_x,_y))
    for _a,_b in LD_LEAD: _ps.append(_a); _ps.append(_b)
    for _t,_x,_y,_r in LD_TXT: _ps.append((_x,_y))
    mnx=min(p[0] for p in _ps); mxx=max(p[0] for p in _ps)
    mny=min(p[1] for p in _ps); mxy=max(p[1] for p in _ps)
    bbw=mxx-mnx; bbh=mxy-mny
    legh=max(30,min(90,26+len(leg)*13)); exph=max(24,min(80,17+len(tech)*9))
    # ---- 方向自动选择(A4 竖版仅当 主体+标注 能以≥1:2 放入; 否则用横版 A0~A3) ----
    Lx,Lz=body_size(ENT); S=max(Lx,Lz)
    if direction=='auto':
        _AW=210-25-10-10
        _AH=(297-10)-(10+ (45+legh+exph+3*10) )-10
        dr='vs' if (S<=210 and bbw/2<=_AW and bbh/2<=_AH) else 'hb'
    else: dr=direction
    # ---- 选图幅(量级选幅, 比例按 主体+尺寸bbox 能容纳的最小标准比) ----
    fr=pick_frame(dr,S,bbw,bbh,legh,exph); W=fr["W"];H=fr["H"];N=fr["N"];rl=ratio_label(N)
    # ---- 布局 ----
    L = (vs_layout if dr=='vs' else hb_layout)(W,H,N,名称,图号,日期,rl,tech,leg)
    L["W"],L["H"]=W,H; L["rl"]=rl
    bx=layout_boxes2(L)
    tb,bxlg,bxex,drb=bx["tb"],bx["lg"],bx["ex"],bx["dr"]
    B,Ld=L["BIND"],L["RIM"]; TBW=L["TBW"];TBH=L["TBH"];GAP=L["GAP"]
    # ---- fit 主体到绘图区 ----
    dx0,dy0,dx1,dy1=drb
    ss=min((dx1-dx0)/(mxx-mnx or 1e-9),(dy1-dy0)/(mxy-mny or 1e-9))*0.97
    ox=(dx0+dx1-(mnx+mxx)*ss)/2; oy=(dy0+dy1-(mny+mxy)*ss)/2
    def Tx(pt): return (pt[0]*ss+ox, pt[1]*ss+oy)
    # ---- 重建主体线段用于绘制 ----
    LINES=[]
    for idx,(tp,cx,cy,*R) in enumerate(ENT):
        if tp=='box':
            a,b,z0,z1=R
            for e1,e2 in box_edges(cx,cy,a,b,z0,z1): LINES.append((_seg(*e1,*e2),idx))
        elif tp=='lathe':
            ct=R[0]; left,right,top,bot,ribs=lathe_profile(cx,cy,ct)
            LINES.append((left,idx)); LINES.append((right,idx)); LINES.append((top,idx)); LINES.append((bot,'VISSEG') if LATHE_BOT=='front' else (bot,idx))
            for rb in ribs: LINES.append((rb,'VIS'))
        else:
            r,z0,z1=R
            LINES.append((_circ(cx,cy,r,z1),idx)); LINES.append((_circ(cx,cy,r,z0),-1))
            rr=r/math.sqrt(2)
            LINES.append((_col(cx+rr,cy-rr,z0,z1),idx)); LINES.append((_col(cx-rr,cy+rr,z0,z1),idx))
    seg2d=[]; ribs2d=[]
    for ln,skip in LINES:
        vis=[True]*len(ln) if skip in ('VIS','VISSEG') else [False if occluded(x,y,z,ENT,skip) else True for (x,y,z) in ln]
        cur=[]
        for p,ok in zip(ln,vis):
            if ok: cur.append(iso(*p))
            else:
                if len(cur)>=2: (ribs2d if skip=='VIS' else seg2d).append(cur)
                cur=[]
        if len(cur)>=2: (ribs2d if skip=='VIS' else seg2d).append(cur)
    # ---- PDF ----
    c=canvas.Canvas(out+".pdf",pagesize=(W*MM,H*MM))
    c.setFillColorRGB(1,1,1); c.rect(0,0,W*MM,H*MM,fill=1,stroke=0)
    c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.7*MM)      # 粗实线 b: 可见轮廓/底面(seg2d)
    for s in seg2d:
        q=_build_poly(c,[(x*MM,y*MM) for x,y in (Tx(p) for p in s)])
        c.drawPath(q,fill=0,stroke=1)
    c.setLineWidth(0.35*MM)                                  # 细实线 b/2: 素线(曲面经线)(ribs2d)
    for s in ribs2d:
        q=_build_poly(c,[(x*MM,y*MM) for x,y in (Tx(p) for p in s)])
        c.drawPath(q,fill=0,stroke=1)
    # ---- 中心线(点画线, 回转体轴线, 贯穿并上下延伸) ----
    _CL=None
    try:
        _cx=sum(E[1] for E in ENT)/len(ENT); _cy=sum(E[2] for E in ENT)/len(ENT)
        _zz=[]
        for E in ENT:
            if E[0]=='lathe': _zz += [z for z,r in E[3]]
            elif E[0]=='cyl': _zz += [E[4],E[5]]
            else: _zz += [E[5],E[6]]
        _mz=min(_zz); _Mz=max(_zz); _ext=max(10,0.05*(_Mz-_mz))
        _p0=Tx(iso(_cx,_cy,_mz-_ext)); _p1=Tx(iso(_cx,_cy,_Mz+_ext))
        c.saveState(); c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.25*MM)
        c.setDash([3.0,1.0,0.5,1.0],0)  # 点画线: 长划-空-点-空
        c.line(_p0[0]*MM,_p0[1]*MM,_p1[0]*MM,_p1[1]*MM); c.restoreState()
        _CL=(_p0,_p1)
    except: _CL=None
    c.setLineWidth(0.5*MM)
    for a,b in EXTL:
        aT,bT=Tx(a),Tx(b); c.line(aT[0]*MM,aT[1]*MM,bT[0]*MM,bT[1]*MM)
    for a,b in DIMLN:
        aT,bT=Tx(a),Tx(b); c.line(aT[0]*MM,aT[1]*MM,bT[0]*MM,bT[1]*MM)
    def ARROW(x1,y1,x2,y2):
        for tip,bk in (((x1,y1),(x2,y2)),((x2,y2),(x1,y1))):
            dx=tip[0]-bk[0]; dy=tip[1]-bk[1]; le=math.hypot(dx,dy) or 1
            un=(dx/le,dy/le); per=(-un[1],un[0]); base=(tip[0]-un[0]*3.2,tip[1]-un[1]*3.2)
            p1=(base[0]+per[0]*1.1,base[1]+per[1]*1.1); p2=(base[0]-per[0]*1.1,base[1]-per[1]*1.1)
            c.setFillColorRGB(0,0,0)
            c.drawPath(_build_poly(c,[(p[0]*MM,p[1]*MM) for p in (tip,p1,p2)]),fill=1,stroke=0)
    for a,b in DIMLN:
        A,T=Tx(a),Tx(b); ARROW(A[0],A[1],T[0],T[1])
    for txt,x,y,rot in dimtxt:
        p=Tx((x,y)); c.saveState(); c.translate(p[0]*MM,p[1]*MM); c.rotate(rot)
        c.setFont("HM",4.2*MM); c.setFillColorRGB(1,1,1); c.drawCentredString(0,1.3*MM,txt)
        c.setFillColorRGB(0,0,0); c.drawCentredString(0,1.3*MM,txt); c.restoreState()
    # 引线标注(不穿实体)
    c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.3*MM)
    for a,b in LD_LEAD:
        AT,T=Tx(a),Tx(b); c.line(AT[0]*MM,AT[1]*MM,T[0]*MM,T[1]*MM)
    for txt,x,y,rot in LD_TXT:
        p=Tx((x,y)); c.saveState(); c.translate(p[0]*MM,p[1]*MM); c.rotate(rot)
        c.setFont("HM",4.2*MM); c.setFillColorRGB(1,1,1); c.drawCentredString(0,1.3*MM,txt)
        c.setFillColorRGB(0,0,0); c.drawCentredString(0,1.3*MM,txt); c.restoreState()
    # 图框(外细内粗)+对中
    c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.25*MM); c.rect(0,0,W*MM,H*MM)
    c.setLineWidth(1.0*MM); c.rect(B*MM,Ld*MM,(W-B-Ld)*MM,(H-2*Ld)*MM)
    c.setLineWidth(1.0*MM)
    c.line((B+((W-B-Ld)/2))*MM,Ld*MM,(B+((W-B-Ld)/2))*MM,0)
    c.line((B+((W-B-Ld)/2))*MM,(H-Ld)*MM,(B+((W-B-Ld)/2))*MM,H*MM)
    c.line(B*MM,(H/2)*MM,0,(H/2)*MM); c.line((W-Ld)*MM,(H/2)*MM,W*MM,(H/2)*MM)
    # 标题栏
    tbc,tbz=L["tbc"],L["tbz"]; tblx,tbly=tb[0],tb[1]
    名称,图号,日期,rl=L["title"]
    c.setStrokeColorRGB(0,0,0)
    # 外框四边(中粗, 完整)
    c.setLineWidth(1.0*MM)
    c.line((tblx)*MM,tbly*MM,(tblx+TBW)*MM,tbly*MM); c.line((tblx)*MM,(tbly+TBH)*MM,(tblx+TBW)*MM,(tbly+TBH)*MM)
    c.line((tblx)*MM,tbly*MM,(tblx)*MM,(tbly+TBH)*MM); c.line((tblx+TBW)*MM,tbly*MM,(tblx+TBW)*MM,(tbly+TBH)*MM)  # 左右外框边(修复左侧缺失)
    def TBC(col,row,text,sz=3.0*MM,label=False):
        x0,x1=tbc[col],tbc[col+1]; y0,y1=tbz[row],tbz[row+1]
        cx,cy=tblx+(x0+x1)/2, tbly+(y0+y1)/2
        c.setFillColorRGB(0,0,0); c.setFont("HM",sz*MM)
        if label: c.drawString((tblx+x0+1.2)*MM,cy*MM,text)
        elif text: c.drawCentredString(cx*MM,cy*MM,text)
    TFILL={(2,0):("制图",3,1),(1,0):("审核",3,1),(0,0):("日期",3,1),(0,1):(日期,2.8,0),
           (2,2):("比例",3,1),(2,3):(rl,3.4,0),(1,2):("图号",3,1),(1,3):(图号,3.2,0),
           (0,2):("张次",3,1),(0,3):("共1 第1",2.8,0)}
    if L["dr"]=='hb':
        # ==== 三行标题栏(规范 2026-08-09): 行1设计单位 | 行2图名·图号·页数 | 行3设计·制图·审核·日期 ====
        c.setLineWidth(0.25*MM)
        def hline(y): c.line(tblx*MM,(tbly+y)*MM,(tblx+TBW)*MM,(tbly+y)*MM)
        def vline(x,y0,y1): c.line((tblx+x)*MM,(tbly+y0)*MM,(tblx+x)*MM,(tbly+y1)*MM)
        hline(19); hline(38)                                   # 内横线
        for x in (20,45,65,90,110,135,155): vline(x,0,19)      # 行3(底): 设计/制图/审核/日期
        for x in (20,60,80,120,140):        vline(x,19,38)     # 行2(中): 图名/图号/页数
        vline(35,38,56)                                        # 行1(顶): 设计单位
        def cell(x0,x1,y0,y1,text,sz,align):
            cx,cy=tblx+(x0+x1)/2, tbly+(y0+y1)/2
            c.setFillColorRGB(0,0,0); c.setFont("HM",sz*MM)
            if align=='l': c.drawString((tblx+x0+1.2)*MM,cy*MM,text)
            elif text: c.drawCentredString(cx*MM,cy*MM,text)
        for lab,x0,x1 in (("设计",0,20),("制图",45,65),("审核",90,110),("日期",135,155)): cell(x0,x1,0,19,lab,3*L["thk"],'l')
        cell(155,180,0,19,日期,2.8*L["thk"],'c')                                                   # 日期值
        for lab,x0,x1 in (("图名",0,20),("图号",60,80),("页数",120,140)): cell(x0,x1,19,38,lab,3*L["thk"],'l')
        cell(20,60,19,38,名称,4*L["thk"],'c'); cell(80,120,19,38,图号,3.2*L["thk"],'c')          # 图名/图号值
        cell(0,35,38,56,"设计单位",3*L["thk"],'l')
    else:
        # 竖版: 原网格
        c.setLineWidth(0.25*MM)
        for x in tbc[1:-1]: c.line((tblx+x)*MM,tbly*MM,(tblx+x)*MM,(tbly+TBH)*MM)
        for y in tbz[1:-1]: c.line(tblx*MM,(tbly+y)*MM,(tblx+TBW)*MM,(tbly+y)*MM)
        for (row,col),(txt,sz,lb) in TFILL.items(): TBC(col,row,txt,sz*L["thk"],lb)
    # 图例 / 说明 框
    def box(x0,y0,x1,y1,lw=0.5*MM):
        c.setStrokeColorRGB(0,0,0); c.setLineWidth(lw); c.rect(x0*MM,y0*MM,(x1-x0)*MM,(y1-y0)*MM)
    def mmT(x,y,s,sz=3*MM,align='l'):
        c.setFont("HM",sz*MM); c.setFillColorRGB(0,0,0)
        if align=='l': c.drawString(x*MM,y*MM,s)
        elif align=='c': c.drawCentredString(x*MM,y*MM,s)
    box(*bxex); mmT((bxex[0]+bxex[2])/2,bxex[3]-8,"技术要求",4,'c')
    for i,t in enumerate(tech):
        yy=bxex[3]-14-8.5*i
        if yy>bxex[1]+3: mmT(bxex[0]+5,yy,t,3,'l')
    box(*bxlg); mmT((bxlg[0]+bxlg[2])/2,bxlg[3]-8,"图   例",4,'c')
    ycur=bxlg[3]-14
    for txt,heavy in leg:
        if ycur<bxlg[1]+14: break
        c.setLineWidth((1.0 if heavy else 0.5)*MM); c.line((bxlg[0]+5)*MM,ycur*MM,(bxlg[0]+34)*MM,ycur*MM)
        mmT(bxlg[0]+38,ycur-4,txt,3,'l'); ycur-=12
    c.save()
    import fitz
    fitz.open(out+".pdf")[0].get_pixmap(dpi=150).save("/tmp/gb_figure_view.png")
    # ---- DXF ----
    import ezdxf
    doc=ezdxf.new("R2010",setup=True); msp=doc.modelspace()
    def dL(a,b,ly="0",lw=None):
        _l=msp.add_line((round(a[0],2),round(a[1],2)),(round(b[0],2),round(b[1],2)),dxfattribs={'layer':ly})
        if lw is not None: _l.dxf.lineweight=lw
        return _l
    for s in seg2d:
        p2=[Tx(p) for p in s]
        for k in range(len(p2)-1): dL(p2[k],p2[k+1],"0",70)   # 粗实线 0.7
    doc.layers.add("RIB",color=4)
    for s in ribs2d:
        p2=[Tx(p) for p in s]
        for k in range(len(p2)-1): dL(p2[k],p2[k+1],"RIB",35) # 细实线 0.35(素线)
    doc.layers.add("DIM",color=1)
    for a,b in EXTL: dL(Tx(a),Tx(b),"DIM")
    for a,b in DIMLN:
        dL(Tx(a),Tx(b),"DIM")
        def tri(tip,bk):
            dx=tip[0]-bk[0]; dy=tip[1]-bk[1]; le=math.hypot(dx,dy) or 1
            un=(dx/le,dy/le); per=(-un[1],un[0]); base=(tip[0]-un[0]*3.2,tip[1]-un[1]*3.2)
            p1=(base[0]+per[0]*1.1,base[1]+per[1]*1.1); p2=(base[0]-per[0]*1.1,base[1]-per[1]*1.1)
            msp.add_lwpolyline([(round(a,2),round(b,2)) for a,b in (tip,base,p1,p2)],close=True,dxfattribs={'layer':'DIM'})
        aT,bT=Tx(a),Tx(b); tri(aT,bT); tri(bT,aT)
    for txt,x,y,rot in dimtxt:
        p=Tx((x,y)); msp.add_text(txt,dxfattribs={'layer':'DIM','style':'GB_HZ','height':6*ss,'rotation':rot,'insert':(round(p[0],2),round(p[1],2))})
    for a,b in LD_LEAD:
        dL(Tx(a),Tx(b),"DIM")
    for txt,x,y,rot in LD_TXT:
        p=Tx((x,y)); msp.add_text(txt,dxfattribs={'layer':'DIM','style':'GB_HZ','height':6*ss,'rotation':0,'insert':(round(p[0],2),round(p[1],2))})
    if _CL is not None:
        doc.layers.add("CENTER",color=8,linetype="CENTER")
        dL(_CL[0],_CL[1],"CENTER")
    doc.layers.add("FRAME",color=7)
    for a,b in [((0,0),(W,0)),((W,0),(W,H)),((W,H),(0,H)),((0,H),(0,0))]: dL(a,b,"FRAME")
    for a,b in [((B,Ld),(W-Ld,Ld)),((W-Ld,Ld),(W-Ld,H-Ld)),((W-Ld,H-Ld),(B,H-Ld)),((B,H-Ld),(B,Ld))]: dL(a,b,"FRAME")
    for a,b in [((B+((W-B-Ld)/2),Ld),(B+((W-B-Ld)/2),0)),((B+((W-B-Ld)/2),H-Ld),(B+((W-B-Ld)/2),H)),((0,H/2),(B,H/2)),((W-Ld,H/2),(W,H/2))]: dL(a,b,"FRAME")
    if 'GB_HZ' not in [s.dxf.name for s in doc.styles]:
        _st=doc.styles.add('GB_HZ',font='gbenor.shx'); _st.dxf.bigfont='gbcbig.shx'
    lbt=doc.layers.add("TITLEBLOCK",color=3)
    for a,b in [((tblx,tbly),(tblx+TBW,tbly)),((tblx+TBW,tbly),(tblx+TBW,tbly+TBH)),((tblx+TBW,tbly+TBH),(tblx,tbly+TBH)),((tblx,tbly+TBH),(tblx,tbly))]: dL(a,b,"TITLEBLOCK")
    if L["dr"]=='hb':
        # 三行标题栏(横版): 独立分格 + 填充
        def hL(y): dL((tblx,tbly+y),(tblx+TBW,tbly+y))
        def vL(x,y0,y1): dL((tblx+x,tbly+y0),(tblx+x,tbly+y1))
        hL(19); hL(38)
        for x in (20,45,65,90,110,135,155): vL(x,0,19)
        for x in (20,60,80,120,140):        vL(x,19,38)
        vL(35,38,56)
        def cl(x0,x1,y0,y1,text,sz,align):
            cx=tblx+(x0+x1)/2; cy=tbly+(y0+y1)/2; szh=round(sz*L["thk"],2)
            if align=='l': msp.add_text(text,dxfattribs={'layer':'TITLEBLOCK','style':'GB_HZ','height':szh,'insert':(round(tblx+x0+1.2,2),round(cy,2))})
            elif text: msp.add_text(text,dxfattribs={'layer':'TITLEBLOCK','style':'GB_HZ','height':szh,'halign':1,'insert':(round(cx,2),round(cy,2))})
        for lab,x0,x1 in (("设计",0,20),("制图",45,65),("审核",90,110),("日期",135,155)): cl(x0,x1,0,19,lab,3,'l')
        cl(155,180,0,19,日期,2.8,'c')                                                      # 日期值
        for lab,x0,x1 in (("图名",0,20),("图号",60,80),("页数",120,140)): cl(x0,x1,19,38,lab,3,'l')
        cl(20,60,19,38,名称,4,'c'); cl(80,120,19,38,图号,3.2,'c')                          # 图名/图号值
        cl(0,35,38,56,"设计单位",3,'l')
    else:
        for x in tbc[1:-1]: dL((tblx+x,tbly),(tblx+x,tbly+TBH))
        for y in tbz[1:-1]: dL((tblx,tbly+y),(tblx+TBW,tbly+y))
        for (row,col),(txt,sz,lb) in TFILL.items():
            xa,xc=tbc[col],tbc[col+1]; ya,yc=tbz[row],tbz[row+1]
            cx=tblx+(xa+xc)/2; cy=tbly+(ya+yc)/2
            szh=round(sz*L["thk"],2)
            if lb: msp.add_text(txt,dxfattribs={'layer':'TITLEBLOCK','style':'GB_HZ','height':szh,'insert':(round(tblx+xa+1.2,2),round(cy,2))})
            elif txt: msp.add_text(txt,dxfattribs={'layer':'TITLEBLOCK','style':'GB_HZ','height':szh,'halign':1,'insert':(round(cx,2),round(cy,2))})
    lnt=doc.layers.add("NOTE",color=5)
    for x0,y0,x1,y1 in (bxex,bxlg):
        for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]: dL(a,b,"NOTE")
    _nt=[("技术要求",(bxex[0]+bxex[2])/2,bxex[3]-6)]
    for i,t in enumerate(tech):
        yy=bxex[3]-14-8.5*i
        if yy>bxex[1]+3: _nt.append((t,bxex[0]+5,yy))
    _nt.append(("图   例",(bxlg[0]+bxlg[2])/2,bxlg[3]-6))
    for i,(txt,_h) in enumerate(leg):
        yy=bxlg[3]-14-12*i
        if yy>=bxlg[1]+14: _nt.append((txt,bxlg[0]+38,yy-4))
    for s,x,y in _nt:
        msp.add_text(s,dxfattribs={'layer':'NOTE','style':'GB_HZ','height':4,'halign':(1 if s in("技术要求","图   例") else 0),'insert':(round(x,2),round(y,2))})
    doc.saveas(out+".dxf")
    print("%s | 方向=%s 图幅=%s(%dx%d) 比例=%s 可见线=%d 尺寸=%d"%(名称,"竖版" if dr=='vs' else "横版",fr["na"],W,H,rl,len(seg2d),len(dimtxt)))

if __name__=="__main__":
    tech=["1  未注尺寸公差按 GB/T 1804-m 执行。","2  未注形位公差按 GB/T 1184-K 执行。","3  锐角倒钝, 去除毛刺飞边。","4  构件除锈后喷涂防腐底漆面漆。"]
    leg=[("粗实线 — 可见轮廓线",True),("细实线 — 尺寸线界限",False)]
    base="/home/sandbox/.openclaw/workspace/cad/"
    # 高型(高>宽)→竖版
    ENTb=[('cyl',0,0,52,0,6),('cyl',0,0,52,6,128),('cyl',0,0,48,128,148),('cyl',0,0,42,148,166),('cyl',0,0,36,166,182),('cyl',0,0,30,182,196),('cyl',0,0,26,196,230),('cyl',0,0,30,230,258)]
    DIMSb=[("Ø104",(-52,0,120),(52,0,120),(0,-70,0),-30),("Ø52",(-26,0,200),(26,0,200),(-55,0,0),90),("258",(52,0,0),(52,0,258),(60,0,0),90)]
    # 宽型(宽>高)→横版
    ENTt=[('cyl',0,0,280,0,120),('box',0,0,1600,140,0,160)]
    DIMSt=[("Ø560",(-280,0,100),(280,0,100),(0,-340,0),-30),("160",(1600,0,0),(1600,0,160),(300,0,0),90)]
    # 高型→竖版
    ENTp=[('cyl',0,0,40,0,15),('cyl',0,0,40,15,90),('cyl',0,0,30,90,110)]
    DIMSp=[("Ø80",(-40,0,60),(40,0,60),(0,-50,0),-30),("110",(40,0,0),(40,0,110),(50,0,0),90)]
    generate("饮料瓶（正等轴测）","BOTTLE-01",ENTb,DIMSb,"2026.08.08",base+"V3-饮料瓶",tech,leg)
    generate("机架底座（等轴测）","BASE-01",ENTt,DIMSt,"2026.08.08",base+"V3-机架横版",tech,leg)
    generate("小型阀体","VALVE-01",ENTp,DIMSp,"2026.08.08",base+"V3-阀体",tech,leg)
