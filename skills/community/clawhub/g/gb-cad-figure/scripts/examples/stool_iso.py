#!/usr/bin/env python3
"""方凳 — 正等轴测【全局遮挡(隐藏线剔除)】· 混合实体版(box座面 + 圆柱四腿)。
复用同一套全局深度判定逻辑, 新增长方体(box)实体支持。
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("HM","/usr/share/fonts/HarmonyFont/Harmony-Regular.ttf"))
C30=math.cos(math.radians(30)); S30=math.sin(math.radians(30))
def iso(x,y,z): return ((x-y)*C30,(x+y)*S30+z)

# ---------- 实体遮挡判定 ----------
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
    Wlo=max(2*(cx-a)-U, 2*(cy-b)+U, (vp-z1)/S30)
    Whi=min(2*(cx+a)-U, 2*(cy+b)+U, (vp-z0)/S30)
    if Wlo<=Whi+1e-9:
        return vp - Wlo*(1+S30)   # 顶面(最靠观察者)的深度
    return None

def fwd_of(ent, up,vp):
    if ent[0]=='cyl': return cyl_fwd_depth(*ent[1:],up,vp)
    return box_fwd_depth(*ent[1:],up,vp)

def occluded(entities,x,y,z,skip=-1):
    up=(x-y)*C30; vp=(x+y)*S30+z; dp=z-x-y
    for i,E in enumerate(entities):
        if i==skip: continue
        f=fwd_of(E,up,vp)
        if f is not None and f>dp+0.05: return True
    return False

# ---------- 候选线 ----------
def _seg(x1,y1,z1,x2,y2,z2,n=40):
    return [(x1+(x2-x1)*i/n, y1+(y2-y1)*i/n, z1+(z2-z1)*i/n) for i in range(n+1)]
def _circ(cx,cy,r,z,n=360):
    return [(cx+r*math.cos(2*math.pi*i/n), cy+r*math.sin(2*math.pi*i/n), z) for i in range(n+1)]
def _col(x,y,z0,z1,n=320):
    return [(x,y,z0+(z1-z0)*i/n) for i in range(n+1)]

def build_lines(entities):
    lines=[]
    for i,(tp,cx,cy,*R) in enumerate(entities):
        if tp=='cyl':
            r,z0,z1=R
            lines.append((_circ(cx,cy,r,z1),i))     # 顶面圆(skip自身)
            lines.append((_circ(cx,cy,r,z0),-1))    # 底面圆(不跳,留前缘)
            rr=r/math.sqrt(2)
            lines.append((_col(cx+rr,cy-rr,z0,z1),i))
            lines.append((_col(cx-rr,cy+rr,z0,z1),i))
        else:
            a,b,z0,z1=R
            # 可见轮廓: 对box找出"可见面"(法向与观察方向(-1,-1,1)内积>0),
            # 提取可见面的全部边界棱(去重)作为候选线。可见面=顶面 + 朝观察者的两侧壁。
            VEC=(-1,-1,1)
            A=(cx-a,cy-b,z1);B=(cx+a,cy-b,z1);C=(cx+a,cy+b,z1);D=(cx-a,cy+b,z1)
            E=(cx-a,cy-b,z0);F=(cx+a,cy-b,z0);G=(cx+a,cy+b,z0);H=(cx-a,cy+b,z0)
            faces={'top':([A,B,C,D],(0,0,1)),'x-':([A,D,H,E],(-1,0,0)),
                   'x+':([B,C,G,F],(1,0,0)),'y-':([A,B,F,E],(0,-1,0)),
                   'y+':([D,C,G,H],(0,1,0)),'bot':([E,F,G,H],(0,0,-1))}
            seg={}
            for nm,(pts,nv) in faces.items():
                if VEC[0]*nv[0]+VEC[1]*nv[1]+VEC[2]*nv[2]<=0: continue
                for k in range(4):
                    key=tuple(sorted((pts[k],pts[(k+1)%4])))
                    seg[key]=1
            for (p1,p2) in seg:
                lines.append((_seg(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],50),i))
    return lines

# ---------- 渲染 ----------
def render(entities,out_pdf,title,top_note,dpi=180):
    lines=build_lines(entities)
    W,H=landscape(A4); pad=50
    alls=[iso(*p) for ln,_ in lines for p in ln]
    xs=[p[0] for p in alls]; ys=[p[1] for p in alls]
    minx,maxx=min(xs),max(xs); miny,maxy=min(ys),max(ys)
    ss=min((W-2*pad)/max(1.0,maxx-minx),(H-2*pad)/max(1.0,maxy-miny))*0.95
    ox=(W-(minx+maxx)*ss)/2; oy=(H-(miny+maxy)*ss)/2
    c=canvas.Canvas(out_pdf,pagesize=landscape(A4))
    c.setFillColorRGB(1,1,1); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColorRGB(0,0,0); c.setLineWidth(1.4)
    cnt=0
    for ln,skip in lines:
        vis=[False if occluded(entities,x,y,z,skip) else True for (x,y,z) in ln]
        cur=[]; segs=[]
        for p,ok in zip(ln,vis):
            sx,sy=iso(*p)
            if ok: cur.append((sx*ss+ox,sy*ss+oy))
            else:
                if len(cur)>=2: segs.append(cur)
                cur=[]
        if len(cur)>=2: segs.append(cur)
        for seg in segs:
            pa=c.beginPath(); pa.moveTo(*seg[0])
            for sp in seg[1:]: pa.lineTo(*sp)
            c.drawPath(pa,fill=0,stroke=1); cnt+=1
    c.setFont("HM",20); c.setFillColorRGB(0,0,0)
    c.drawCentredString(W/2,H-28,title)
    c.setFont("HM",13); c.drawCentredString(W/2,H-50,top_note)
    c.save()
    import fitz
    fitz.open(out_pdf)[0].get_pixmap(dpi=dpi).save("/tmp/stool_iso.png")
    return cnt

if __name__=="__main__":
    # 方凳: box座面(半宽330 半深180 高420-460) + 4条圆柱腿(r45, 地面0-座底420)
    ents=[('box',0,0,330,180,420,460),
          ('cyl',250,120,45,0,420),('cyl',250,-120,45,0,420),
          ('cyl',-250,120,45,0,420),('cyl',-250,-120,45,0,420)]
    n=render(ents,"/home/sandbox/.openclaw/workspace/cad/方凳正等轴测-去隐藏线-20260808-0955.pdf",
             "方凳 — 正等轴测","全局遮挡(隐藏线剔除) · box座面+圆柱四腿")
    print("stool OK, 可见线段:",n)
