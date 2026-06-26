#!/usr/bin/env python3
"""Render a WHO weight-for-age chart as a PNG using only Python stdlib."""
from __future__ import annotations

import argparse, csv, json, math, os, statistics, struct, zlib
from pathlib import Path
from datetime import datetime, date

DEFAULT_DATA_DIR = Path(os.environ.get("BABY_TRACKER_DIR", Path.home() / ".openclaw" / "workspace" / "data" / "baby-tracker"))
W,H = 1400,900
ND = statistics.NormalDist()

FONT = {
' ': ['000','000','000','000','000','000','000'],'.': ['000','000','000','000','000','110','110'],
'-': ['000','000','000','111','000','000','000'],':': ['000','110','110','000','110','110','000'],
'0': ['111','101','101','101','101','101','111'],'1': ['010','110','010','010','010','010','111'],
'2': ['111','001','001','111','100','100','111'],'3': ['111','001','001','111','001','001','111'],
'4': ['101','101','101','111','001','001','001'],'5': ['111','100','100','111','001','001','111'],
'6': ['111','100','100','111','101','101','111'],'7': ['111','001','001','010','010','100','100'],
'8': ['111','101','101','111','101','101','111'],'9': ['111','101','101','111','001','001','111'],
'A': ['010','101','101','111','101','101','101'],'B': ['110','101','101','110','101','101','110'],
'C': ['111','100','100','100','100','100','111'],'D': ['110','101','101','101','101','101','110'],
'E': ['111','100','100','110','100','100','111'],'F': ['111','100','100','110','100','100','100'],
'G': ['111','100','100','101','101','101','111'],'H': ['101','101','101','111','101','101','101'],
'I': ['111','010','010','010','010','010','111'],'J': ['111','001','001','001','001','101','111'],
'K': ['101','101','110','100','110','101','101'],'L': ['100','100','100','100','100','100','111'],
'M': ['101','111','111','101','101','101','101'],'N': ['101','111','111','111','101','101','101'],
'O': ['111','101','101','101','101','101','111'],'P': ['111','101','101','111','100','100','100'],
'Q': ['111','101','101','101','111','001','001'],'R': ['110','101','101','110','101','101','101'],
'S': ['111','100','100','111','001','001','111'],'T': ['111','010','010','010','010','010','010'],
'U': ['101','101','101','101','101','101','111'],'V': ['101','101','101','101','101','101','010'],
'W': ['101','101','101','101','111','111','101'],'X': ['101','101','101','010','101','101','101'],
'Y': ['101','101','101','010','010','010','010'],'Z': ['111','001','001','010','100','100','111'],
'/': ['001','001','010','010','010','100','100'],'%': ['101','001','010','010','010','100','101'],
'(': ['001','010','100','100','100','010','001'],')': ['100','010','001','001','001','010','100'],
}
for k,v in list(FONT.items()): FONT[k.lower()] = v

img = bytearray([248,250,252]) * (W*H)
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def px(x,y,c):
    if 0 <= x < W and 0 <= y < H:
        i=(y*W+x)*3; img[i:i+3]=bytes(c)
def rect(x0,y0,x1,y1,c):
    for y in range(max(0,int(y0)), min(H,int(y1))):
        for x in range(max(0,int(x0)), min(W,int(x1))): px(x,y,c)
def line(x0,y0,x1,y1,c,width=1):
    x0=int(round(x0)); y0=int(round(y0)); x1=int(round(x1)); y1=int(round(y1))
    dx=abs(x1-x0); dy=-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; err=dx+dy
    while True:
        r=width//2
        for yy in range(y0-r,y0+r+1):
            for xx in range(x0-r,x0+r+1): px(xx,yy,c)
        if x0==x1 and y0==y1: break
        e2=2*err
        if e2>=dy: err+=dy; x0+=sx
        if e2<=dx: err+=dx; y0+=sy
def circle(cx,cy,r,c,outline=None):
    cx=int(round(cx)); cy=int(round(cy))
    for y in range(cy-r-2,cy+r+3):
        for x in range(cx-r-2,cx+r+3):
            d=(x-cx)**2+(y-cy)**2
            if d <= r*r: px(x,y,c)
            if outline and r*r < d <= (r+3)*(r+3): px(x,y,outline)
def text(x,y,s,c,scale=3):
    x0=x
    for ch in s:
        pat=FONT.get(ch, FONT.get(ch.upper(), FONT[' ']))
        for row,bits in enumerate(pat):
            for col,b in enumerate(bits):
                if b=='1':
                    for yy in range(scale):
                        for xx in range(scale): px(x+col*scale+xx,y+row*scale+yy,c)
        x += 4*scale
    return x-x0
def poly(points,c,width=2):
    for (x0,y0),(x1,y1) in zip(points, points[1:]): line(x0,y0,x1,y1,c,width)


def load_lms(sex, who_lms):
    by_unit={'week': [], 'month': []}
    with who_lms.open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['sex'] == sex:
                by_unit[r['age_unit']].append({k: float(r[k]) if k in {'age_days','L','M','S'} else r[k] for k in r})
    for rows in by_unit.values(): rows.sort(key=lambda r:r['age_days'])
    if not by_unit['week'] or not by_unit['month']:
        raise SystemExit(f'No WHO LMS rows found for sex={sex!r} in {who_lms}')
    return by_unit

def interp(age_days, rows):
    if age_days <= rows[0]['age_days']: return rows[0]
    if age_days >= rows[-1]['age_days']: return rows[-1]
    for a,b in zip(rows, rows[1:]):
        if a['age_days'] <= age_days <= b['age_days']:
            t=(age_days-a['age_days'])/(b['age_days']-a['age_days'])
            return {k: (a[k]+t*(b[k]-a[k]) if k in {'age_days','L','M','S'} else a[k]) for k in a}
    return rows[-1]

def lms_for_age(age_days, lms):
    # WHO offers a more granular 0-13 weeks table; use it while in range, then monthly 0-5y.
    if age_days <= lms['week'][-1]['age_days']:
        return interp(age_days, lms['week'])
    return interp(age_days, lms['month'])

def weight_for_z(age_days, z, lms):
    r=lms_for_age(age_days,lms); L,M,S=r['L'],r['M'],r['S']
    if abs(L) < 1e-9: return M * math.exp(S*z)
    return M * ((1 + L*S*z) ** (1/L))

def z_for_weight(age_days, weight, lms):
    r=lms_for_age(age_days,lms); L,M,S=r['L'],r['M'],r['S']
    if abs(L) < 1e-9: return math.log(weight/M)/S
    return ((weight/M)**L - 1)/(L*S)

def percentile_for_weight(age_days, weight, lms):
    return ND.cdf(z_for_weight(age_days, weight, lms))*100

def main():
    ap = argparse.ArgumentParser(description='Render a WHO weight-for-age PNG chart from baby-tracker CSV data')
    ap.add_argument('--data-dir', type=Path, default=DEFAULT_DATA_DIR)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--who-lms', type=Path, help='Path to who_weight_lms.csv; defaults to <data-dir>/who/who_weight_lms.csv')
    ap.add_argument('--title')
    args = ap.parse_args()

    data = args.data_dir
    who_lms = args.who_lms or data / 'who' / 'who_weight_lms.csv'
    out = args.output or data / 'charts' / 'weight-latest.png'

    meta=json.loads((data/'metadata.json').read_text())
    if not meta.get('date_of_birth'):
        raise SystemExit('metadata.json must contain date_of_birth')
    dob=date.fromisoformat(meta['date_of_birth'])
    sex=meta.get('sex') or 'female'
    baby_name = meta.get('name') or 'Baby'
    lms=load_lms(sex, who_lms)
    weights=[]
    with (data/'events.csv').open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r.get('metric')=='weight' and r.get('value') and (r.get('unit') in ('kg','')):
                ts=datetime.fromisoformat(r['timestamp_local'])
                age=(ts.date()-dob).days + ts.hour/24 + ts.minute/1440
                weights.append((age,float(r['value']),ts.strftime('%d %b')))
    weights=sorted(weights)
    if not weights:
        raise SystemExit('No weight events found in events.csv')
    latest_age, latest_value, latest_label = weights[-1]
    latest_pct = percentile_for_weight(latest_age, latest_value, lms)
    latest_z = z_for_weight(latest_age, latest_value, lms)

    xmin=max(0, latest_age-45); xmax=latest_age+8
    visible=[w for w in weights if xmin <= w[0] <= xmax]
    curve_ps=[3,15,50,85,97]
    plot_vals=[v for _,v,_ in visible]
    for day in range(int(xmin), int(xmax)+1):
        for p in curve_ps:
            plot_vals.append(weight_for_z(day, ND.inv_cdf(p/100), lms))
    ymin=max(0,min(plot_vals)-0.18); ymax=max(plot_vals)+0.28

    ml,mr,mt,mb=135,125,145,155; pw=W-ml-mr; ph=H-mt-mb
    xmap=lambda x: ml+(x-xmin)/(xmax-xmin)*pw
    ymap=lambda y: mt+ph-(y-ymin)/(ymax-ymin)*ph

    rect(28,28,W-28,H-28,rgb('#ffffff'))
    title = args.title or f'{baby_name} weight recent view'
    text(ml,48,title,rgb('#0f172a'),5)
    text(ml,88,f'Current {latest_value:.2f}kg at {latest_age:.0f}d WHO {latest_pct:.1f}%',rgb('#0f766e'),4)
    text(ml,121,'Official WHO weight-for-age LMS/z-score reference',rgb('#475569'),3)

    for i in range(6):
        yv=ymin+(ymax-ymin)*i/5; yy=ymap(yv)
        line(ml,yy,W-mr,yy,rgb('#e2e8f0'),1)
        text(42,int(yy)-11,f'{yv:.1f}',rgb('#64748b'),3)
    for i in range(6):
        xv=xmin+(xmax-xmin)*i/5; xx=xmap(xv)
        line(xx,mt,xx,H-mb,rgb('#e2e8f0'),1)
        text(int(xx)-30,H-mb+30,f'{int(round(xv))}d',rgb('#64748b'),3)
    line(ml,H-mb,W-mr,H-mb,rgb('#334155'),2); line(ml,mt,ml,H-mb,rgb('#334155'),2)
    text(W//2-110,H-54,'Age in days',rgb('#334155'),4)
    text(44,mt+8,'kg',rgb('#334155'),4)

    colors={3:'#c7d2fe',15:'#93c5fd',50:'#64748b',85:'#f9a8d4',97:'#f0abfc'}
    for p in curve_ps:
        z=ND.inv_cdf(p/100)
        pts=[]
        for step in range(0, 240):
            age=xmin+(xmax-xmin)*step/239
            pts.append((xmap(age), ymap(weight_for_z(age,z,lms))))
        poly(pts,rgb(colors[p]),2)
        text(int(pts[-1][0])+10,int(pts[-1][1])-10,f'P{p}',rgb(colors[p]),3)

    wpts=[(xmap(a),ymap(v)) for a,v,_ in visible]
    poly(wpts,rgb('#0f766e'),5)
    for a,v,label in visible:
        circle(xmap(a),ymap(v),8,rgb('#14b8a6'),rgb('#0f766e'))

    offsets=[-58,-86,-44,-72]
    for idx,(a,v,label) in enumerate(visible):
        xx=int(xmap(a)); yy=int(ymap(v)); dy=offsets[idx % len(offsets)]
        text(xx-34,yy+dy,f'{v:.2f}',rgb('#0f766e'),3)
        line(xx,yy-13,xx,yy+dy+24,rgb('#99f6e4'),1)

    lx,ly=xmap(latest_age),ymap(latest_value)
    line(lx,ly,lx-210,ly-112,rgb('#0f766e'),2)
    text(int(lx)-390,int(ly)-154,f'Latest {latest_value:.2f}kg',rgb('#0f766e'),4)
    text(int(lx)-390,int(ly)-116,f'WHO percentile {latest_pct:.1f}',rgb('#0f766e'),4)
    text(int(lx)-390,int(ly)-82,f'z {latest_z:.2f}',rgb('#0f766e'),3)

    text(ml,H-26,'WHO reference for monitoring growth; not a diagnosis',rgb('#64748b'),3)

    out.parent.mkdir(parents=True,exist_ok=True)
    raw=b''.join(b'\x00'+bytes(img[y*W*3:(y+1)*W*3]) for y in range(H))
    def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    out.write_bytes(png)
    print(out)
    print(f'who_percentile={latest_pct:.2f}')
    print(f'z_score={latest_z:.3f}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
