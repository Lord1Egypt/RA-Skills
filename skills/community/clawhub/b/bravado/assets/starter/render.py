"""Brand film renderer: brief-driven 31-second motion template with original sound."""
from pathlib import Path
import argparse, json, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
from brief import load_brief

ROOT=Path(__file__).resolve().parent
W,H=1920,1080
S=W/1280
FPS=30
DURATION=31
FOREST='#1F2D24'; DARK='#162119'; CLAY='#D65A3A'; CREAM='#F6F1E6'
SUN='#EAD79A'; STONE='#DCCDB2'; LINE='#E4D8C1'; MUTED='#77766B'
CUTS=[0,3,7.5,12,17.5,23,27,31]
BRIEF=None
OUT=None

def cfg(path):
    return load_brief(path)

def load(path,out):
    global BRIEF, OUT, FOREST,DARK,CLAY,CREAM,SUN,STONE,LINE,MUTED
    BRIEF=cfg(path);OUT=Path(out).resolve();OUT.mkdir(parents=True,exist_ok=True)
    FOREST,DARK,CLAY,CREAM,SUN,STONE,LINE,MUTED=[BRIEF['palette'][k] for k in ('forest','dark','clay','cream','sun','stone','line','muted')]

def b(*keys):
    v=BRIEF
    for k in keys:v=v[k]
    return v

def clamp(x):return max(0,min(1,x))
def ease(x):x=clamp(x);return 1-(1-x)**3
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def rgb(c):return tuple(bytes.fromhex(c.lstrip('#')))
def mix(a,b,t):return tuple(round(x*(1-t)+y*t) for x,y in zip(rgb(a) if isinstance(a,str) else a,rgb(b) if isinstance(b,str) else b))
@lru_cache(None)
def font(sz,kind='bold'):
    name={'bold':'Inter-700','heavy':'Inter-800','body':'Inter-400','mono':'IBMPlexMono-400','serif':'PlayfairDisplay-700'}[kind]
    return ImageFont.truetype(str(ROOT/'fonts'/f'{name}.ttf'),round(sz*S))
def xy(box):return tuple(round(v*S) for v in box)

class Canvas:
    def __init__(self,bg=None):self.im=Image.new('RGB',(W,H),CREAM if bg is None else bg);self.d=ImageDraw.Draw(self.im)
    def text(self,x,y,s,size=24,color=None,kind='bold',anchor=None):
        color=FOREST if color is None else color
        self.d.text((round(x*S),round(y*S)),s,font=font(size,kind),fill=color,anchor=anchor,stroke_width=0)
    def line(self,pts,color=None,width=1):self.d.line([xy(p) for p in pts],fill=FOREST if color is None else color,width=max(1,round(width*S)),joint='curve')
    def rect(self,box,fill=None,outline=None,r=0,width=1):
        self.d.rounded_rectangle(xy(box),radius=round(r*S),fill=fill,outline=outline,width=max(1,round(width*S)))
    def circle(self,x,y,r,fill=None,outline=None,width=1):self.d.ellipse(xy((x-r,y-r,x+r,y+r)),fill=fill,outline=outline,width=max(1,round(width*S)))
    def label(self,x,y,s,color=None,size=11):self.text(x,y,s,size,MUTED if color is None else color,'mono')
    def reveal(self,x,y,s,local,delay=0,size=52,color=None,kind='bold'):
        color=FOREST if color is None else color
        p=ease((local-delay)/.65)
        if p<=0:return
        available=(1280-x-64)*S
        while self.d.textlength(s,font=font(size,kind))>available and size>14:size-=1
        height=int((size*1.4)*S); layer=Image.new('RGBA',(W,height),(0,0,0,0));d=ImageDraw.Draw(layer)
        d.text((0,int((1-p)*(size*1.4)*S)),s,font=font(size,kind),fill=color)
        self.im.paste(layer,(round(x*S),round(y*S)),layer)
    def reveal_center(self,y,s,local,delay=0,size=52,color=None,kind='bold'):
        color=CREAM if color is None else color
        while self.d.textlength(s,font=font(size,kind))>1050*S and size>15:size-=1
        x=(1280-self.d.textlength(s,font=font(size,kind))/S)/2
        self.reveal(x,y,s,local,delay,size,color,kind)
    def logo(self,x,y,size=36,color=None):
        color=FOREST if color is None else color
        if b('brand').get('mark_style')!='triple_arc':
            self.circle(x,y,size*.46,outline=color,width=2)
            self.text(x,y-size*.29,b('brand').get('monogram',b('brand','name')[0])[:1],size*.56,color,'heavy',anchor='mt')
            return
        # Three concentric arcs used in the Cadence example.
        for rr,ww in [(size*.45,size*.055),(size*.33,size*.075),(size*.18,size*.07)]:
            box=xy((x-rr,y-rr,x+rr,y+rr))
            self.d.arc(box,48,312,fill=color,width=max(1,round(ww*S)))
            for ang in [48,312]:
                a=math.radians(ang); self.circle(x+rr*math.cos(a),y+rr*math.sin(a),ww*.47,color)
    def header(self,n,section,t):
        self.logo(73,49,32);self.text(97,32,b('brand','name'),25,FOREST,'serif')
        self.text(1205,45,f'{n:02d}   {section}',10,MUTED,'mono',anchor='ra')
        self.line([(64,665),(1216,665)],LINE)
        self.line([(64,665),(64+1152*t/31,665)],CLAY,2)
        self.label(64,682,b('brand','eyebrow').upper(),size=10)
        self.text(1216,682,b('brand','footer').upper(),10,MUTED,'mono',anchor='ra')
    def pill(self,x,y,s,bg=None,fg=None):
        bg=FOREST if bg is None else bg;fg=CREAM if fg is None else fg
        length=self.d.textlength(s,font=font(11,'mono'))/S
        self.rect((x,y,x+length+24,y+29),bg,r=4);self.label(x+12,y+7,s,fg)
    def check(self,x,y,color=None):self.line([(x-6,y),(x-1,y+5),(x+8,y-6)],CLAY if color is None else color,2)

def pulse_points(x,y,width,height,phase=0):
    pts=[]
    for i in range(301):
        z=i/300; q=(z*3-phase)%1
        amp=(math.exp(-((q-.45)/.04)**2)-.35*math.exp(-((q-.52)/.025)**2))
        pts.append((x+z*width,y-height*amp))
    return pts

def scene0(t):
    c=Canvas(DARK)
    for k in range(3):
        c.line(pulse_points(-120,405+k*8,1520,62-k*12,t*.12),mix(DARK,SUN,.14+k*.05),1)
    pts=pulse_points(0,390,1280,60,0)
    p=ease(t/1.7);c.line(pts[:max(2,int(len(pts)*p))],CLAY,2)
    if t>.85:
        c.reveal(64,145,b('story','opening','headline'),t,.85,64,CREAM)
        c.reveal(67,228,b('story','opening','subline'),t,1.12,27,SUN,'body')
    c.logo(75,53,39,CREAM);c.text(105,33,b('brand','name'),29,CREAM,'serif')
    c.label(66,618,b('brand','eyebrow').upper(),SUN)
    return c

def scene1(t,u):
    c=Canvas();c.header(1,'THE WAIT',t)
    c.reveal(64,118,b('story','wait','line1'),u,size=56)
    c.reveal(64,183,b('story','wait','line2'),u,.16,size=56)
    period=int(b('example','period_days'))
    p=ease((u-.5)/2.9);days=min(period,int(p*period))
    c.text(1168,109,str(days).zfill(2),92,CLAY,'heavy',anchor='ra')
    c.text(1164,214,b('story','wait','count_label').upper(),10,MUTED,'mono',anchor='ra')
    c.label(66,304,b('story','wait','timeline_label').upper(),FOREST)
    tile_w=min(65,1100/period-17); step=1135/period
    for i in range(period):
        x=65+i*step; active=i<days
        c.rect((x,350,x+tile_w,433),FOREST if active else None,FOREST if active else LINE,r=5)
        c.text(x+tile_w/2,378,str(i+1).zfill(2),18,CREAM if active else STONE,'mono',anchor='ma')
        c.line([(x+tile_w*.23,367),(x+tile_w*.77,367)],CLAY if active else LINE,2)
    c.line([(66,499),(1180,499)],LINE,2)
    c.line([(66,499),(66+1114*p,499)],CLAY,3)
    c.circle(66+1114*p,499,6,CLAY)
    c.label(66,530,'DAY 01');c.text(1180,530,f'DAY {period:02} / {b("story","wait","end_label").upper()}',11,MUTED,'mono',anchor='ra')
    c.reveal(66,583,b('story','wait','payoff'),u,2.7,25,FOREST,'body')
    return c

def scene2(t,u):
    c=Canvas();c.header(2,'THE SHIFT',t)
    c.reveal(64,115,b('story','shift','line1'),u,size=58)
    c.reveal(64,183,b('story','shift','line2'),u,.14,size=58,color=CLAY)
    p=ease((u-.5)/1.5)
    c.rect((66,341,244,522),FOREST,r=12)
    c.label(87,365,b('story','shift','source_label').upper(),SUN)
    c.text(88,401,b('example','unit'),30,CREAM)
    c.label(88,480,b('story','shift','source_note').upper(),STONE)
    c.rect((952,341,1208,522),DARK,r=12)
    c.label(978,364,b('story','shift','destination_label').upper(),SUN)
    c.text(978,410,b('story','shift','destination_state'),29,CREAM)
    c.circle(983,488,4,CLAY);c.label(995,480,b('story','shift','status').upper(),SUN)
    for j in range(3):
        pts=[]
        for k in range(160):
            z=k/159
            pts.append((244+708*z,420+(j-1)*34*math.sin(math.pi*z)))
        c.line(pts[:max(2,int(160*p))],mix(CREAM,FOREST,.22),1)
        for k in range(7):
            z=((u-.8)*.25+k/7+j*.035)%1
            if u>.8+k*.065:
                x=244+708*z;y=420+(j-1)*34*math.sin(math.pi*z)
                c.rect((x-6,y-6,x+6,y+6),CLAY if j==1 else FOREST,r=2)
    c.reveal(367,538,b('story','shift','payoff'),u,1.2,23,FOREST,'body')
    c.label(473,596,b('brand','rail_label').upper(),size=11)
    return c

def scene3(t,u):
    c=Canvas();c.header(3,'THE CADENCE',t)
    c.reveal(64,114,b('story','cadence','line1'),u,size=54)
    c.reveal(64,177,b('story','cadence','line2'),u,.14,size=54)
    c.label(70,301,b('story','cadence','metric_label').upper(),CLAY)
    c.text(64,322,str(b('example','interval_seconds')),150,FOREST,'heavy');c.text(264,411,b('example','interval_unit'),31,FOREST,'body')
    for i in range(15):
        a=-math.pi/2+i*2*math.pi/15
        x=477+58*math.cos(a);y=408+58*math.sin(a)
        c.circle(x,y,4,CLAY if i<=int(u*5)%15 else STONE)
    c.label(71,520,b('story','cadence','caption1').upper(),FOREST)
    c.label(71,547,b('story','cadence','caption2').upper(),MUTED)
    slide=(1-ease((u-.35)/.8))*220
    x=659+slide
    c.rect((x,285,x+548,603),DARK,r=14)
    c.label(x+29,310,b('story','cadence','card_label').upper(),STONE)
    c.circle(x+457,318,4,CLAY);c.label(x+472,310,'LIVE',SUN)
    packets=max(0,int((u-.6)*3))
    e=b('example');interval=int(e['interval_seconds']);weekly=float(e['weekly_total'])
    per=weekly*interval/(7*24*3600)
    amount=float(e['starting_amount'])+packets*per
    c.text(x+29,351,f'{e["currency_symbol"]}{amount:,.4f}',48,CREAM,'mono')
    c.label(x+31,421,f'{e["currency_symbol"]}{per:.4f} / {interval} SEC  ·  {e["currency_symbol"]}{weekly:,.0f} / WEEK',SUN,size=12)
    c.line(pulse_points(x+30,496,486,29,u*.25),CLAY,2)
    c.line([(x+29,542),(x+518,542)],'#35463A')
    c.label(x+30,560,b('example','unit').upper(),STONE);c.label(x+207,560,b('example','network').upper(),STONE);c.label(x+363,560,b('story','cadence','card_footer').upper(),STONE)
    c.label(661,621,'ILLUSTRATIVE ANIMATION · NOT LIVE PRODUCT DATA',size=9)
    return c

def scene4(t,u):
    c=Canvas();c.header(4,'THE FLOW',t)
    c.reveal(64,113,b('story','flow','line1'),u,size=57)
    c.reveal(64,180,b('story','flow','line2'),u,.14,size=57)
    c.reveal(66,270,b('story','flow','subline'),u,.45,23,MUTED,'body')
    cx,cy=204,465
    c.circle(cx,cy,67,FOREST);c.text(cx,cy-18,b('story','flow','source').upper(),16,CREAM,'mono',anchor='ma')
    for j,(title,sub) in enumerate(b('story','flow','audiences')):
        y=345+j*105;p=ease((u-.45-j*.18)/.9)
        ex=790;ey=y+38
        pts=[]
        for k in range(100):
            z=k/99;pts.append((272+(ex-272)*z,cy+(ey-cy)*smooth(z)))
        c.line(pts[:max(2,int(p*100))],STONE,2)
        if p>.95:
            for k in range(3):
                z=(u*.36+k/3+j*.15)%1;x=272+(ex-272)*z;yy=cy+(ey-cy)*smooth(z)
                c.circle(x,yy,5,CLAY)
        xx=ex+(1-p)*120
        c.rect((xx,y,xx+406,y+79),'#FFF9EC',LINE,r=9)
        c.circle(xx+38,y+39,21,FOREST);c.text(xx+38,y+25,title[0],21,CREAM,anchor='ma')
        c.text(xx+76,y+15,title,20);c.label(xx+76,y+44,sub,size=10)
        if p>.97:c.check(xx+375,y+40)
    c.pill(399,587,b('brand','rail_label').upper())
    return c

def scene5(t,u):
    c=Canvas();c.header(5,'THE PROOF',t)
    c.reveal(64,120,b('story','proof','line1'),u,size=57)
    c.reveal(64,188,b('story','proof','line2'),u,.15,size=57)
    c.reveal(66,310,b('story','proof','subline1'),u,.6,27,MUTED,'body')
    c.reveal(66,347,b('story','proof','subline2'),u,.72,27,MUTED,'body')
    for j,word in enumerate(b('story','proof','verbs')):c.pill(66+j*110,462,word.upper())
    x=682;y=302
    for j in range(3,0,-1):c.rect((x+j*10,y-j*13,x+504+j*10,y+287-j*13),mix(CREAM,STONE,.12*j),LINE,r=10)
    c.rect((x,y,x+504,y+287),'#FFF9EC',LINE,r=10)
    c.label(x+25,y+24,b('story','proof','record_label').upper(),CLAY)
    c.label(x+25,y+59,f'{b("example","unit").upper()}   /   {b("example","network").upper()}',FOREST)
    for j in range(3):
        pp=ease((u-.65-j*.32)/.6);yy=y+108+j*48
        if pp>0:
            col=mix(CREAM,FOREST,pp)
            c.line([(x+25,yy-10),(x+477,yy-10)],LINE)
            c.label(x+27,yy,f'{b("story","proof","record_item").upper()}  {j+1:03}',col)
            per=float(b('example','weekly_total'))*float(b('example','interval_seconds'))/(7*24*3600)
            c.label(x+227,yy,f'+{per:.4f} {b("example","unit")}',col)
            if pp>.95:c.check(x+456,yy+8)
    c.label(x+26,y+259,'ILLUSTRATIVE RECORD',MUTED,size=9)
    c.reveal(67,572,b('story','proof','payoff'),u,1.75,24,FOREST,'body')
    return c

def scene6(t,u):
    c=Canvas(DARK)
    for j in range(3):c.line(pulse_points(-30,560+j*12,1340,44-j*8,u*.05),mix(DARK,SUN,.11+j*.03),1)
    c.logo(640,150,96,CREAM)
    c.reveal_center(214,b('brand','name'),u,.1,76,CREAM,'serif')
    c.reveal_center(325,b('brand','tagline'),u,.3,58,CREAM,'serif')
    c.reveal_center(422,b('brand','closing_subline'),u,.55,23,SUN,'body')
    p=ease((u-.9)/.6)
    if p>0:
        c.rect((507,492,773,545),mix(DARK,CLAY,p),r=7)
        c.text(640,508,b('brand','cta'),18,CREAM,anchor='ma')
    c.text(640,616,b('brand','url'),17,STONE,'mono',anchor='ma')
    c.text(640,666,b('brand','footer').upper(),10,STONE,'mono',anchor='ma')
    return c

SCENES=[lambda t,u:scene0(u),scene1,scene2,scene3,scene4,scene5,scene6]
def frame(t):
    idx=next((i for i in range(7) if t<CUTS[i+1]),6);u=t-CUTS[idx]
    c=SCENES[idx](t,u)
    # A quick upward masked page replacement, with a narrow clay leading edge.
    if idx>0 and u<.36:
        prev=SCENES[idx-1](CUTS[idx]-.001,CUTS[idx]-CUTS[idx-1]-.001).im
        p=ease(u/.36);edge=round(H*(1-p))
        prev.paste(c.im.crop((0,edge,W,H)),(0,edge))
        ImageDraw.Draw(prev).rectangle((0,max(0,edge-3),W,edge),fill=CLAY)
        return prev
    return c.im

def make_audio():
    sr=48000;n=int(DURATION*sr);a=np.zeros((n,2),dtype=np.float64);rng=np.random.default_rng(19)
    def add(start,sig,level=1,pan=0):
        k=int(start*sr);m=min(len(sig),n-k)
        if k<0 or m<=0:return
        a[k:k+m,0]+=sig[:m]*level*math.sqrt((1-pan)/2)
        a[k:k+m,1]+=sig[:m]*level*math.sqrt((1+pan)/2)
    def tone(start,f=660,d=.18,v=.06,pan=0):
        z=np.arange(int(d*sr))/sr;env=(1-np.exp(-z*160))*np.exp(-z*20)
        sig=(np.sin(2*np.pi*f*z)+.24*np.sin(2*np.pi*f*2*z))*env
        add(start,sig,v,pan)
    def whoosh(start,d=.42,v=.12):
        z=np.arange(int(d*sr))/sr;noise=rng.normal(0,1,len(z));noise=np.convolve(noise,np.ones(9)/9,'same')
        env=np.sin(np.pi*z/d)**2
        add(start,noise*env,v,-.15);add(start+.025,noise*env,v,.5)
    def thump(start,v=.13):
        z=np.arange(int(.24*sr))/sr
        add(start,np.sin(2*np.pi*(65*z-65*z*z))*np.exp(-z*22),v)
    # Warm, quiet harmonic bed in A minor; original synthesis, no samples.
    z=np.arange(n)/sr
    env=np.minimum(z/2,1)*np.minimum((31-z)/1.1,1)
    for f in [110,164.8138,220,261.6256,329.6276]:
        pad=np.sin(2*np.pi*f*z+.22*np.sin(2*np.pi*.11*z))*.009*env
        a[:,0]+=pad;a[:,1]+=np.sin(2*np.pi*f*z+.15)*.008*env
    for sec in np.arange(.25,29.8,.625):
        thump(sec,.038);tone(sec+.3125,880,.09,.019,.25)
    for sec in CUTS[1:-1]:whoosh(sec-.14);thump(sec+.12,.19)
    for i in range(14):tone(3.55+i*.15,520+i*24,.075,.06,(i/13-.5)*.9)
    for sec in np.arange(8.35,11.8,.32):tone(sec,760,.1,.04,(sec%1)-.5)
    for sec in np.arange(12.7,17.3,.34):tone(sec,740,.09,.045,.2)
    for sec in [18.1,18.45,18.8,23.85,24.17,24.49]:tone(sec,990,.2,.085)
    for f in [440,554.365,659.255]:tone(27.55,f,1,.15)
    a*=np.minimum(np.arange(n)/(sr*.02),1)[:,None]
    a*=np.minimum((n-np.arange(n))/(sr*.35),1)[:,None]
    peak=np.max(abs(a));a=a*(.83/peak) if peak>.83 else a
    with wave.open(str(OUT/'sound-design.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
    normalized=OUT/'sound-normalized.wav'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(OUT/'sound-design.wav'),'-af','loudnorm=I=-18:TP=-1.5:LRA=9','-ar','48000',str(normalized)],check=True)
    normalized.replace(OUT/'sound-design.wav')

def main():
    parser=argparse.ArgumentParser(description='Bravado 31-second motion film')
    parser.add_argument('--brief',default='projects/cadence.json')
    parser.add_argument('--out',default='output')
    parser.add_argument('--stills',action='store_true')
    parser.add_argument('--validate-only',action='store_true',help='Check brief without loading fonts or rendering')
    args=parser.parse_args()
    try:cfg(args.brief)
    except (ValueError, OSError) as exc:parser.error(str(exc))
    if args.validate_only:
        print('Brief valid');return
    load(args.brief,args.out)
    (OUT/'review').mkdir(exist_ok=True)
    times=[1.8,6.2,10,15.8,20.6,25.5,29.5]
    for sec in times:frame(sec).save(OUT/'review'/f'frame-{sec}.jpg',quality=90)
    from PIL import ImageOps
    contact=Image.new('RGB',(1280,4*384),CREAM);dc=ImageDraw.Draw(contact)
    for i,sec in enumerate(times):
        im=Image.open(OUT/'review'/f'frame-{sec}.jpg').resize((640,360))
        x=i%2*640;y=i//2*384;contact.paste(im,(x,y));dc.text((x+10,y+365),f'{sec:.1f} s',font=font(10,'mono'),fill=FOREST)
    contact.save(OUT/'review'/'storyboard.jpg',quality=90)
    # Check both sides and the middle of every wipe, plus the final frame.
    boundary_frames=sorted({round(cut*FPS)+offset for cut in CUTS[1:-1] for offset in (-1,0,5,11)} | {FPS*DURATION-1})
    for index in boundary_frames:
        frame(index/FPS).save(OUT/'review'/f'boundary-{index:04d}.jpg',quality=90)
    if args.stills:return
    make_audio()
    name=''.join(ch.lower() if ch.isalnum() else '-' for ch in b('brand','name')).strip('-')
    output=OUT/f'{name}-bravado.mp4'
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-', '-i',str(OUT/'sound-design.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(DURATION),str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):
        p.stdin.write(frame(i/FPS).tobytes())
        if i%150==0:print(f'Rendered {i}/{FPS*DURATION} frames',flush=True)
    p.stdin.close()
    if p.wait()!=0:raise RuntimeError('ffmpeg render failed')
    print(f'Complete: {output}',flush=True)
if __name__=='__main__':main()
