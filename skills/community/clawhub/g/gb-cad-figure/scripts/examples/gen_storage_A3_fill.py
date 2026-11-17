#!/usr/bin/env python3
"""酒精储存中间库房 — A3正式工程图纸(GB/T 14689-1993 图框 + GB/T 10609.1-2008 标题栏)。
画面: 库房透视室内(去前/右/顶墙, 室内储罐待定) + 国标轴测尺寸标注, 置于A3图框绘图区。
同时输出 PDF + DXF(单位mm, 图纸坐标, 原点左下角A3=420×297)。
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("HM","/usr/share/fonts/HarmonyFont/Harmony-Regular.ttf"))
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
ENT=[]
def occluded(x,y,z,skip=-1):
    up=(x-y)*C30; vp=(x+y)*S30+z; dp=z-x-y
    for i,E in enumerate(ENT):
        if i==skip: continue
        f=cyl_fwd_depth(*E[1:],up,vp) if E[0]=='cyl' else box_fwd_depth(*E[1:],up,vp)
        if f is not None and f>dp+0.05: return True
    return False
def _seg(x1,y1,z1,x2,y2,z2,n=50):
    return [(x1+(x2-x1)*i/n,y1+(y2-y1)*i/n,z1+(z2-z1)*i/n) for i in range(n+1)]
def _circ(cx,cy,r,z,n=360):
    return [(cx+r*math.cos(2*math.pi*i/n),cy+r*math.sin(2*math.pi*i/n),z) for i in range(n+1)]
def _col(x,y,z0,z1,n=400):
    return [(x,y,z0+(z1-z0)*i/n) for i in range(n+1)]
def box_edges(cx,cy,a,b,z0,z1):
    VEC=(-1,-1,1)
    A=(cx-a,cy-b,z1);B=(cx+a,cy-b,z1);C=(cx+a,cy+b,z1);D=(cx-a,cy+b,z1)
    E=(cx-a,cy-b,z0);F=(cx+a,cy-b,z0);G=(cx+a,cy+b,z0);H=(cx-a,cy+b,z0)
    faces={'top':([A,B,C,D],(0,0,1)),'x-':([A,D,H,E],(-1,0,0)),'x+':([B,C,G,F],(1,0,0)),
           'y-':([A,B,F,E],(0,-1,0)),'y+':([D,C,G,H],(0,1,0)),'bot':([E,F,G,H],(0,0,-1))}
    seg={}
    for (pts,nv) in faces.values():
        if VEC[0]*nv[0]+VEC[1]*nv[1]+VEC[2]*nv[2]<=0: continue
        for k in range(4):
            seg[tuple(sorted((pts[k],pts[(k+1)%4])))]=1
    return [(list(k[0]),list(k[1])) for k in seg]

# ---------- 库房实体(透视室内: 地板+背x墙+背y墙) 储罐待用户定 ----------
AX=2500; BY=1500; HZ=2800
# 地板需延伸到墙体外表面之下(墙厚150: 右墙x→2650, 后墙y→1650), 否则墙脚悬空
EXF=150  # 墙厚(外扩量)
ENT=[('box',0,0,AX+EXF,BY+EXF,0,100),('box',2575,0,75,BY,100,HZ),('box',0,1575,AX,75,100,HZ)]
L=[]
for idx,(tp,cx,cy,*R) in enumerate(ENT):
    a,b,z0,z1=R
    for e1,e2 in box_edges(cx,cy,a,b,z0,z1):
        # 过滤: 从内墙角顶(2500,1500,2800)向两侧墙厚延伸的顶面内端边,
        # 用户确认去掉(与内墙角竖线垂直、从内墙角点向两侧分叉的线); 外墙顶边保留
        if (e1==[2500,1500,2800] and e2==[2650,1500,2800]) or \
           (e2==[2500,1500,2800] and e1==[2650,1500,2800]) or \
           (e1==[2500,1500,2800] and e2==[2500,1650,2800]) or \
           (e2==[2500,1500,2800] and e1==[2500,1650,2800]):
            continue
        L.append((_seg(e1[0],e1[1],e1[2],e2[0],e2[1],e2[2]),idx))
DIMS=[("5000",(2500,-1500,100),(-2500,-1500,100),(0,-500,0),30),
      ("3000",(-2500,-1500,100),(-2500,1500,100),(-500,0,0),-30),
      ("2800",(2500,-1500,0),(2500,-1500,2800),(500,0,0),90)]

seg2d=[]; EXTL=[]; DIMLN=[]; dimtxt=[]
for ln,skip in L:
    vis=[False if occluded(x,y,z,skip) else True for (x,y,z) in ln]
    cur=[];segs=[]
    for p,ok in zip(ln,vis):
        if ok: cur.append(iso(*p))
        else:
            if len(cur)>=2: segs.append(cur)
            cur=[]
    if len(cur)>=2: segs.append(cur)
    seg2d+=segs

# ===== 补充外墙轮廓线(墙体外表面 = 墙厚外侧) =====
# box_edges 已画: 右墙外前竖边(2650,-1500,idx16)、后墙外左竖边(-2500,1650,idx22)、外墙顶边、内墙角线
# 这里补充的外墙线同样做可见性裁剪: 仅保留从视角真实可见的段, 隐藏被墙体背后遮挡的线
ADDSEG3D=[
  ((2650,1500,2800),(2650,1650,2800)),   # 外墙顶边: 右墙外顶(后) 接外墙角顶
  ((2650,1650,2800),(2500,1650,2800)),   # 外墙顶边: 外墙角顶 接后墙外顶(右)
  ((2650,-1500,100),(2650,1500,100)),   # 右墙外表面底边(墙脚)
  ((2650,1500,100),(2650,1650,100)),     # 右墙外底边末端 接外墙脚
  ((2500,1650,100),(-2500,1650,100)),   # 后墙外表面整条底边(墙脚)
  ((2650,1650,100),(2500,1650,100)),     # 后墙外底边 至外墙脚
]
# 注: ①外墙角竖线(2650,1650)不在此绘——其底部被墙遮挡(剪裁仅剩顶段),且该顶段与内墙角竖线 x 投影重合、向上延伸形成"出头"，故隐藏
# ②右/后墙外顶边主体已由 box_edges 自动绘制; ADDSEG 不再额外延伸至外墙角顶, 避免内墙角顶部形成"尖角"
# 注: 后墙内底边(2500,1500,100)-(-2500,1500,100) 已由 box_edges 绘制(idx26), 不在此重复添加, 避免内墙角交点处出头
def _clipvis(a,b,n=60):
    """对3D线段做遮挡裁剪, 返回可见段(3D折线)列表"""
    pts=[tuple(a[i]+(b[i]-a[i])*k/n for i in range(3)) for k in range(n+1)]
    vis=[not occluded(*p) for p in pts]
    segs=[];cur=[]
    for p,v in zip(pts,vis):
        if v: cur.append(p)
        else:
            if len(cur)>=2: segs.append(cur)
            cur=[]
    if len(cur)>=2: segs.append(cur)
    return segs
for a,b in ADDSEG3D:
    for seg in _clipvis(a,b):
        seg2d.append([iso(*p) for p in seg])
for txt,A3,B3,off,rot in DIMS:
    a0=tuple(A3); b0=tuple(B3)
    a1=(A3[0]+off[0],A3[1]+off[1],A3[2]+off[2]); b1=(B3[0]+off[0],B3[1]+off[1],B3[2]+off[2])
    ol=math.sqrt(off[0]**2+off[1]**2+off[2]**2) or 1
    u=(off[0]/ol,off[1]/ol,off[2]/ol)
    a1e=(a1[0]+u[0]*2.5,a1[1]+u[1]*2.5,a1[2]+u[2]*2.5)  # 界线超尺寸线2.5mm
    b1e=(b1[0]+u[0]*2.5,b1[1]+u[1]*2.5,b1[2]+u[2]*2.5)
    EXTL += [(iso(*a0),iso(*a1e)),(iso(*b0),iso(*b1e))]
    DIMLN.append((iso(*a1),iso(*b1)))
    ac,bc=iso(*a1),iso(*b1)
    dimtxt.append((txt,(ac[0]+bc[0])/2,(ac[1]+bc[1])/2,rot))

# ===== 三面整体填充(地板顶面 + x/y两面立墙内面) 真实三维坐标 =====
FACEFILL=[
  [(-2500,-1500,100),(2500,-1500,100),(2500,1500,100),(-2500,1500,100)],  # 地板顶面(z=100)
  [(2500,-1500,100),(2500,-1500,2800),(2500,1500,2800),(2500,1500,100)],   # x内墙(面向-x)
  [(-2500,1500,100),(-2500,1500,2800),(2500,1500,2800),(2500,1500,100)],   # y内墙(面向-y)
]

def gen_hatch(poly, gap=8.0):
    """在Tx后mm坐标的多边形poly内生成45°剖面线线段列表[(x1,y1,x2,y2)]"""
    import math as _m
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    x0,x1=min(xs),max(xs); y0,y1=min(ys),max(ys)
    R=_m.hypot(x1-x0,y1-y0)
    ang=_m.radians(45); u=(_m.cos(ang),_m.sin(ang)); n=(-u[1],u[0])
    c0=( (x0+x1)/2, (y0+y1)/2 )
    t0=(x0-c0[0])*n[0]+(y0-c0[1])*n[1]
    t1=(x1-c0[0])*n[0]+(y1-c0[1])*n[1]
    lo,hi=min(t0,t1)-gap,max(t0,t1)+gap
    segs=[]
    t=lo
    while t<=hi:
        cx=c0[0]+t*n[0]; cy=c0[1]+t*n[1]
        p1=(cx-R*u[0],cy-R*u[1]); p2=(cx+R*u[0],cy+R*u[1])
        segs.append((p1[0],p1[1],p2[0],p2[1]))
        t+=gap
    return segs

def poly_contains(poly,px,py):
    """射线法判断点是否在多边形内(凸多边形专用简便法)"""
    x1,y1=poly[-1]; inside=False
    for x2,y2 in poly:
        if (y1>py)!=(y2>py) and px < (x2-x1)*(py-y1)/(y2-y1)+x1:
            inside=not inside
        x1,y1=x2,y2
    return True

# ---------- 绘图区(图纸mm): A3内框(20,5)-(415,292), 右上避开标题栏 ----------
RECT=(30,64,218,290)
px0,py0,px1,py1=RECT
allp=[p for s in seg2d for p in s]
for a,b in EXTL+DIMLN: allp+=[a,b]
FASEPROJ=[[iso(*p) for p in face] for face in FACEFILL]
for fp in FASEPROJ: allp+=fp
xs=[p[0] for p in allp]; ys=[p[1] for p in allp]
mnx,mxx=min(xs),max(xs); mny,mxy=min(ys),max(ys)
ss=min((px1-px0)/(mxx-mnx or 1e-9),(py1-py0)/(mxy-mny or 1e-9))*0.99
ox=(px0+px1-(mnx+mxx)*ss)/2; oy=(py0+py1-(mny+mxy)*ss)/2
def Tx(pt): return (pt[0]*ss+ox, pt[1]*ss+oy)

# ===== 输出: PDF(mm→pt) =====
W,H=420*MM,297*MM   # A3横向: 420×297mm
out="/home/sandbox/.openclaw/workspace/cad/酒精储存中间库房-工程图纸A3-填充-20260810-0820"
c=canvas.Canvas(out+".pdf",pagesize=(W,H))
c.setFillColorRGB(1,1,1); c.rect(0,0,W,H,fill=1,stroke=0)
# ===== 三面整体填充(淡灰底色) + 45°剖面线(国标图案, clip裁剪) =====
def facePoly2d(fp): return [Tx(p) for p in fp]
def cyrus_beck(poly, p0, p1):
    """Cyrus-Beck: 线段p0p1被凸多边形poly裁剪, 返回内部线段或None"""
    n=len(poly)
    t0,t1=0.0,1.0
    d=(p1[0]-p0[0], p1[1]-p0[1])
    for i in range(n):
        a=poly[i]; b=poly[(i+1)%n]
        e=(b[0]-a[0], b[1]-a[1])
        # 内向法线(边逆时针时左侧为内)
        nx,ny=e[1],-e[0]
        # 多边形顶点序若为顺时, 翻转法线
        # 用多边形面积符号判断绕向
        f=(a[0]-p0[0], a[1]-p0[1])
        dn=nx*d[0]+ny*d[1]
        fn=nx*f[0]+ny*f[1]
        if abs(dn)<1e-9:
            if fn>0: return None
        else:
            t=-fn/dn
            if dn<0:
                if t>t1: return None
                if t>t0: t0=t
            else:
                if t<t0: return None
                if t<t1: t1=t
    if t0<=t1:
        return ((p0[0]+t0*d[0],p0[1]+t0*d[1]),(p0[0]+t1*d[0],p0[1]+t1*d[1]))
    return None

def poly_signed_area(poly):
    s=0
    for i in range(len(poly)):
        x1,y1=poly[i]; x2,y2=poly[(i+1)%len(poly)]
        s+=x1*y2-x2*y1
    return s/2.0

def draw_face_fill(fp):
    """整个凸多边形整体填充 + 剖面线精确裁剪到面内(无需clipPath, 保证所有顶点/共享边被覆盖)"""
    pol=facePoly2d(fp)
    # 若多边形顶点为顺时针, 反转, 使法线指向内侧(统一逆时针)
    if poly_signed_area(pol)<0: pol=list(reversed(pol))
    # 1) 底部整体填充(必覆盖整个凸多边形含所有顶点与共享边)
    path=c.beginPath()
    q0=pol[0]; path.moveTo(q0[0]*MM,q0[1]*MM)
    for p in pol[1:]: path.lineTo(p[0]*MM,p[1]*MM)
    path.close()
    c.setFillColorRGB(0.90,0.90,0.90)
    c.drawPath(path,fill=1,stroke=0)
    # 2) 剖面线: Cyrus-Beck裁剪到多边形内(细线, 不穿出共享边)
    c.setStrokeColorRGB(0.35,0.35,0.35); c.setLineWidth(0.3*MM)
    for (x1,y1,x2,y2) in gen_hatch(pol, gap=8.0):
        seg=cyrus_beck(pol,(x1,y1),(x2,y2))
        if seg:
            (ax,ay),(bx,by)=seg
            c.line(ax*MM,ay*MM,bx*MM,by*MM)
for fp in FASEPROJ: draw_face_fill(fp)
# 库房图(可见轮廓=粗实线 d=1.0)
c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.0*MM)
for s in seg2d:
    q=[Tx(p) for p in s]
    pa=c.beginPath(); pa.moveTo(q[0][0]*MM,q[0][1]*MM)
    for p in q[1:]: pa.lineTo(p[0]*MM,p[1]*MM)
    c.drawPath(pa,fill=0,stroke=1)
# 尺寸界线+尺寸线=细实线 d/2=0.5, 黑色
c.setLineWidth(0.5*MM); c.setStrokeColorRGB(0,0,0)
for a,b in EXTL:
    aT,bT=Tx(a),Tx(b); c.line(aT[0]*MM,aT[1]*MM,bT[0]*MM,bT[1]*MM)
for a,b in DIMLN:
    aT,bT=Tx(a),Tx(b); c.line(aT[0]*MM,aT[1]*MM,bT[0]*MM,bT[1]*MM)
# 实心闭合箭头(长3.2mm, 宽1.1mm)
def ARROW(x1,y1,x2,y2):
    for tip,bk in (((x1,y1),(x2,y2)),((x2,y2),(x1,y1))):
        dx=tip[0]-bk[0]; dy=tip[1]-bk[1]; le=math.hypot(dx,dy) or 1
        un=(dx/le,dy/le); per=(-un[1],un[0])
        base=(tip[0]-un[0]*3.2,tip[1]-un[1]*3.2)
        p1=(base[0]+per[0]*1.1,base[1]+per[1]*1.1); p2=(base[0]-per[0]*1.1,base[1]-per[1]*1.1)
        c.setFillColorRGB(0,0,0)
        pa=c.beginPath(); pa.moveTo(tip[0]*MM,tip[1]*MM)
        pa.lineTo(p1[0]*MM,p1[1]*MM); pa.lineTo(p2[0]*MM,p2[1]*MM); pa.close()
        c.drawPath(pa,fill=1,stroke=0)
for a,b in DIMLN:
    A,T=Tx(a),Tx(b); ARROW(A[0],A[1],T[0],T[1])
# 尺寸数字(黑色, 不被线穿过, 置于尺寸线上方)
c.setFillColorRGB(0,0,0)
for txt,x,y,rot in dimtxt:
    p=Tx((x,y))
    c.saveState(); c.translate(p[0]*MM,p[1]*MM); c.rotate(rot)
    c.setFont("HM",4.2*MM); c.setFillColorRGB(1,1,1)
    c.drawCentredString(0,1.3*MM,txt)          # 白底遮挡底层线
    c.setFillColorRGB(0,0,0); c.drawCentredString(0,1.3*MM,txt)
    c.restoreState()

# ===== 图框(GB/T 14689) =====
c.setStrokeColorRGB(0,0,0)
c.setLineWidth(0.25*MM); c.rect(0,0,W,H)                      # 外框(纸边)细实线
c.setLineWidth(1.0*MM); c.rect(20*MM,5*MM,395*MM,287*MM)      # 内框粗实线(20,5)-(415,292)
# 对中符号(四边中点, 粗实线, 长5mm)——用户要求去除超出框线, 故不画

# ===== 标题栏 180×56: 标签格+填写格分离, 填写格宽度按内容 =====
tbx,tby=235,5
def Pt(x,y): return ((tbx+x)*MM,(tby+y)*MM)
def HL(x1,y1,x2,y2):
    c.line(Pt(x1,y1)[0],Pt(x1,y1)[1],Pt(x2,y2)[0],Pt(x2,y2)[1])
def TX(x,y,s,sz=3.4*MM,anchor='c'):
    c.setFont("HM",sz)
    cx,cy=Pt(x,y)
    if anchor=='c': c.drawCentredString(cx,cy,s)
    elif anchor=='l': c.drawString(cx,cy,s)
    elif anchor=='r': c.drawRightString(cx,cy,s)
def TXc(x,y,s,sz=3.4*MM): TX(x,y,s,sz,'c')
def TXl(x,y,s,sz=3.4*MM): TX(x,y,s,sz,'l')
c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.0*MM)
HL(0,0,180,0); HL(180,0,180,56); HL(0,56,180,56); HL(0,0,0,56)
c.setLineWidth(0.25*MM)
# 行高: 行1(y46-56高10)单位名称 | 行2(y30-46高16)图名 | 行3(y20-30高10)短字段 | 行4(y0-20高20)签字
for yy in (46,30,20): HL(0,yy,180,yy)
# ---- 行1/行2: 标签格16 + 填写格164 ----
HL(16,46,16,56)   # 行1内分格
HL(16,30,16,46)   # 行2内分格
TXl(1.5,48.0,"单位名称",3.0*MM);        # 行1标签, 填写格留空
TXl(1.5,33.5,"图名",3.0*MM);            # 行2标签
TXc(98,34.5,"酒精储存中间库房",6.5*MM)  # 图名大字居中(填格16-180中心)
# ---- 行3 (y20-30高10): 比例/图号/材料/重量/张次 5字段并排, 标签12+填格 ----
# 字段分界 x: 24/70/116/146/180; 标签格各12
for xx in (24,70,116,146): HL(xx,20,xx,30)
for xx in (12,36): HL(xx,20,xx,30)   # 比例(0-24)标签12、图号(24-70)标签12
# 行3内标签竖线: 比例12, 图号36, 材料70+12=82, 重量116+12=128, 张次146+12=158
HL(82,20,82,30); HL(128,20,128,30); HL(158,20,158,30)
def RB(x,y,s): TXl(x+1.5,y+1.0,s,3.0*MM)  # 行3标签
RV3=lambda x,s: TXc(x+ (1 if s=="1:100" else 4),23,s,3.0*MM)  # 行3填写格值
RB(0,22,"比例");    RV3(14,"1:100")
RB(24,22,"图号");   RV3(58,"STG-001")
RB(70,22,"材料");   # 填写格留空
RB(116,22,"重量");  # 填写格留空
RB(146,22,"张次");  RV3(160,"1/1")
# ---- 行4 (y0-20高20): 设计/制图/审核/批准/日期, 标签14+填格 ----
# 字段 x: 设计(0-38,标签14填24) 制图(38-76) 审核(76-114) 批准(114-152) 日期(152-180,标签14填14)
for xx in (38,76,114,152): HL(xx,0,xx,20)
for xx in (14,52,90,128,166): HL(xx,0,xx,20)
def SB(x,y,s): TXl(x+1.5,y+1.2,s,3.0*MM)
SB(0,10,"设计"); SB(38,10,"制图"); SB(76,10,"审核"); SB(114,10,"批准"); SB(152,10,"日期")
# 签字填写格均留空待手写

# ===== 第三部分: 技术说明 + 图例 (标题栏上方右列空白区) =====
def mmL(x1,y1,x2,y2): c.line(x1*MM,y1*MM,x2*MM,y2*MM)
def mmT(x,y,s,sz=3*MM,align='l'):
    c.setFont("HM",sz); c.setFillColorRGB(0,0,0)
    if align=='l': c.drawString(x*MM,y*MM,s)
    elif align=='c': c.drawCentredString(x*MM,y*MM,s)
c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.5*MM)
# --- 技术说明框 (238,180)-(413,290) 无中间横线 ---
for (a,b) in [((238,180),(413,180)),((413,180),(413,290)),((413,290),(238,290)),((238,290),(238,180))]:
    mmL(a[0],a[1],b[0],b[1])
mmT(325.5,284,"技术要求",4*MM,'c')
tech=["1  未注尺寸公差按 GB/T 1804-m 执行。",
     "2  未注形位公差按 GB/T 1184-K 执行。",
     "3  锐角倒钝，去除毛刺、飞边。",
     "4  金属构件除锈后喷涂防腐底漆及面漆。",
     "5  焊缝按 GB/T 985.1 要求，清除焊渣飞溅。"]
for i,t in enumerate(tech):
    mmT(242,269-15*i,t,3*MM,'l')
# --- 图例框 (238,74)-(413,175) ---
for (a,b) in [((238,74),(413,74)),((413,74),(413,175)),((413,175),(238,175)),((238,175),(238,74))]:
    mmL(a[0],a[1],b[0],b[1])
mmT(325.5,163,"图   例",4*MM,'c')
def leglin(y,heavy):
    c.setLineWidth((1.0 if heavy else 0.5)*MM); mmL(243,y,272,y)
c.setLineWidth(0.5*MM)
leglin(149,True);  mmT(276,145,"粗实线 —— 可见轮廓线",3*MM)
leglin(135,False); mmT(276,131,"细实线 —— 尺寸线、尺寸界线",3*MM)
mmL(243,122,272,122)   # 箭头图例线
c.setFillColorRGB(0,0,0)
pa=c.beginPath(); pa.moveTo(272*MM,122*MM)
pa.lineTo((272-3.2)*MM,121.3*MM); pa.lineTo((272-3.2)*MM,122.7*MM); pa.close()
c.drawPath(pa,fill=1,stroke=0)
mmT(276,118,"实心三角 —— 尺寸起止符号",3*MM)
mmT(242,104,"尺寸数字 —— 沿尺寸线方向书写",3*MM)
mmT(242,90,"单位 mm，不加注单位符号",3*MM)

c.save()

import fitz
fitz.open(out+".pdf")[0].get_pixmap(dpi=180).save("/tmp/a3_storage.png")

# ===== 输出: DXF(mm 真实图纸坐标) =====
import ezdxf
doc=ezdxf.new("R2010",setup=True); msp=doc.modelspace()
def dL(a,b,ly="0"):
    msp.add_line((round(a[0],2),round(a[1],2)),(round(b[0],2),round(b[1],2)),dxfattribs={'layer':ly})
# ===== 三面填充: DXF HATCH(ANSI31 45°剖面线 + SOLID淡灰底) =====
doc.layers.add("FACE-FILL",color=8)
doc.layers.add("FACE-SLID",color=252)
for fp in FASEPROJ:
    pol=[Tx(p) for p in fp]
    poly2d=[(round(x,2),round(y,2)) for x,y in pol]
    # 淡灰实底(SOLID)
    hsolid=msp.add_hatch(dxfattribs={'layer':'FACE-SLID','color':252})
    hsolid.paths.add_polyline_path(poly2d, is_closed=True)
    hsolid.set_solid_fill()
    # 45°剖面线(ANSI31)
    hh=msp.add_hatch(dxfattribs={'layer':'FACE-FILL','color':8})
    hh.paths.add_polyline_path(poly2d, is_closed=True)
    hh.set_pattern_fill('ANSI31', scale=70)
# 实体(粗实线)
for s in seg2d:
    pt2=[Tx(p) for p in s]
    for k in range(len(pt2)-1): dL(pt2[k],pt2[k+1])
# 尺寸(界线+尺寸线, DIM层细)
doc.layers.add("DIM",color=1)
for a,b in EXTL:
    dL(Tx(a),Tx(b),"DIM")
for a,b in DIMLN:
    dL(Tx(a),Tx(b),"DIM")
    # 实心闭合箭头(三角)
    def tri(tip,bk):
        dx=tip[0]-bk[0]; dy=tip[1]-bk[1]; le=math.hypot(dx,dy) or 1
        un=(dx/le,dy/le); per=(-un[1],un[0])
        base=(tip[0]-un[0]*3.2,tip[1]-un[1]*3.2)
        p1=(base[0]+per[0]*1.1,base[1]+per[1]*1.1); p2=(base[0]-per[0]*1.1,base[1]-per[1]*1.1)
        msp.add_lwpolyline([(round(x,2),round(y,2)) for x,y in (tip,base,p1,p2)],close=True,dxfattribs={'layer':'DIM'})
    aT,bT=Tx(a),Tx(b); tri(aT,bT); tri(bT,aT)
for txt,x,y,rot in dimtxt:
    p=Tx((x,y)); msp.add_text(txt,dxfattribs={'layer':'DIM','height':200,'rotation':rot,'insert':(round(p[0],2),round(p[1],2))})
# 图框
lyo=doc.layers.add("FRAME",color=7)
for a,b in [((0,0),(420,0)),((420,0),(420,297)),((420,297),(0,297)),((0,297),(0,0))]: dL(a,b,"FRAME")
for a,b in [((20,5),(415,5)),((415,5),(415,292)),((415,292),(20,292)),((20,292),(20,5))]: dL(a,b,"FRAME")
for a,b in []: dL(a,b,"FRAME")
# 对中符号已去除(用户要求超出框线)
# 标题栏(GB层): 180×56 新布局, 与PDF一致 (局部坐标(0,0)-(180,56), 映射到图纸(235,5))
DX=235; DY=5
def tL(x1,y1,x2,y2): dL((DX+x1,DY+y1),(DX+x2,DY+y2),"TITLEBLOCK")
def tT(x,y,s,sz=3.0,anchor='l'):
    kw={'layer':'TITLEBLOCK','height':sz*10,'insert':(round(DX+x,2),round(DY+y,2))}
    msp.add_text(s,dxfattribs=kw)
lbt=doc.layers.add("TITLEBLOCK",color=3)
for a,b in [((0,0),(180,0)),((180,0),(180,56)),((0,56),(180,56)),((0,0),(0,56))]: tL(a[0],a[1],b[0],b[1])
# 行高: 行1(46-56)单位名称 | 行2(30-46)图名 | 行3(20-30)短字段 | 行4(0-20)签字
for yy in (46,30,20): tL(0,yy,180,yy)
# 行1/行2 标签格16
for xx in (16,): tL(xx,46,xx,56)
for xx in (16,): tL(xx,30,xx,46)
# 行3 字段分界+标签格(20-30)
for xx in (24,70,116,146): tL(xx,20,xx,30)
for xx in (12,36): tL(xx,20,xx,30)
for xx in (82,128,158): tL(xx,20,xx,30)
# 行4 字段分界+标签格(0-20)
for xx in (38,76,114,152): tL(xx,0,xx,20)
for xx in (14,52,90,128,166): tL(xx,0,xx,20)
# ---- 文字 ----
tT(1.5,48.0,"单位名称",3.0)
tT(1.5,33.5,"图名",3.0)
tT(98,34.5,"酒精储存中间库房",6.5)
tT(1.5,22.0,"比例",3.0); tT(14,22.0,"1:100",3.0)
tT(25.5,22.0,"图号",3.0); tT(58,22.0,"STG-001",3.0)
tT(71.5,22.0,"材料",3.0); tT(117.5,22.0,"重量",3.0)
tT(147.5,22.0,"张次",3.0); tT(160,22.0,"1/1",3.0)
for i,lb in enumerate(("设计","制图","审核","批准","日期")):
    tT((0,38,76,114,152)[i]+1.5,10.0,lb,3.0)
# 技术说明 + 图例 (NOTE层)
lnt=doc.layers.add("NOTE",color=5)
for a,b in [((238,180),(413,180)),((413,180),(413,290)),((413,290),(238,290)),((238,290),(238,180))]: dL(a,b,"NOTE")
for a,b in [((238,74),(413,74)),((413,74),(413,175)),((413,175),(238,175)),((238,175),(238,74))]: dL(a,b,"NOTE")
for (x,y,s) in [(325.5,284,"技术要求"),(242,269,"1 未注尺寸公差按GB/T 1804-m执行。"),(242,254,"2 未注形位公差按GB/T 1184-K执行。"),(242,239,"3 锐角倒钝，去除毛刺、飞边。"),(242,224,"4 金属构件除锈后喷涂防腐底漆及面漆。"),(242,209,"5 焊缝按GB/T 985.1要求清除焊渣飞溅。"),(325.5,163,"图  例"),(276,145,"粗实线 — 可见轮廓线"),(276,131,"细实线 — 尺寸线、尺寸界线"),(276,118,"实心三角 — 尺寸起止符号"),(242,104,"尺寸数字 — 沿尺寸线方向书写"),(242,90,"单位mm，不加注单位符号")]:
    msp.add_text(s,dxfattribs={'layer':'NOTE','height':120,'insert':(round(x,2),round(y,2))})
# ===== DXF中文字体修复: 新建GB_HZ大字体组合并指定给含中文实体(防方块) =====
st_zh=doc.styles.new('GB_HZ',dxfattribs={'font':'gbenor.shx'})
st_zh.dxf.bigfont='gbcbig.shx'
import itertools as _it
for e in _it.chain(msp.query('TEXT'), msp.query('MTEXT')):
    try:
        txt=e.dxf.text if hasattr(e.dxf,'text') else e.text
        if txt and any('\u4e00'<=ch<='\u9fff' for ch in str(txt)):
            e.dxf.style='GB_HZ'
    except Exception: pass
doc.saveas(out+".dxf")
print("A3 ok; 可见线段",len(seg2d)," 尺寸",len(dimtxt))
