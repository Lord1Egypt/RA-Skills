#!/usr/bin/env python3
import subprocess, re, sys
from html.parser import HTMLParser
from datetime import datetime, timedelta

def fetch_html(url):
    r = subprocess.run(['curl','-s','-L','--max-time','20',
        '-H','User-Agent: Mozilla/5.0','-H','Accept: text/html', url],
        capture_output=True, text=True)
    if r.returncode != 0: print(f"[ERROR] {r.stderr}",file=sys.stderr); sys.exit(1)
    return r.stdout

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td=False; self.cells,self.rows,self.cur=[],[],[]
    def handle_starttag(self,tag,attrs):
        if tag=='td': self.in_td=True; self.cur=[]
        elif tag=='tr': self.cells=[]
    def handle_endtag(self,tag):
        if tag=='td': self.cells.append(' '.join(''.join(self.cur).split()).strip()); self.in_td=False
        elif tag=='tr' and len(self.cells)==7: self.rows.append(self.cells[:]); self.cells=[]
    def handle_data(self,data):
        if self.in_td: self.cur.append(data)

def get_week_dates():
    today=datetime.today(); monday=today-timedelta(days=today.weekday()+7)
    return {(monday+timedelta(days=i)).strftime('%b %-d') for i in range(7)}

def parse_m(s):
    s=s.replace('$','').replace('€','').replace(',','').strip()
    try:
        if 'B' in s: return float(s.replace('B',''))*1000
        if 'M' in s: return float(s.replace('M',''))
        if 'K' in s: return float(s.replace('K',''))/1000
    except: pass
    return 0

def parse_investors(inv):
    inv=re.sub(r'\+\d+','',inv).strip()
    if not inv or inv=='--': return [],[]
    leads=[m.group(1).strip() for m in re.finditer(r'([\w][\w\s&.]*?)\s*\*',inv)]
    rest=re.sub(r'[\w][\w\s&.]*?\s*\*','',inv).strip()
    follows=[t.strip() for t in re.split(r'\s{2,}',rest) if len(t.strip())>1]
    if not leads and inv!='--':
        parts=re.split(r'\s{2,}',inv)
        leads=[parts[0]] if parts else []
        follows=[p.strip() for p in parts[1:] if p.strip()]
    return leads,follows

TOP={'a16z','Andreessen Horowitz','Paradigm','Coinbase Ventures','Sequoia','Polychain',
     'Dragonfly','YZi Labs','Binance Labs','Animoca Brands','Bain Capital Crypto',
     'Coatue Management','OKX Ventures','Kucoin Ventures','Alibaba','阿里巴巴','Tencent','腾讯'}

if __name__=='__main__':
    WEEK=get_week_dates()
    html=fetch_html('https://www.rootdata.com/Fundraising')
    p=TableParser(); p.feed(html)
    entries=[]
    for row in p.rows:
        name=row[0].split('\n')[0].strip()
        rnd,amt,val,date,_,inv=[row[i] for i in range(1,7)]
        if date not in WEEK: continue
        leads,follows=parse_investors(inv)
        entries.append({'name':name,'round':rnd,'amount':amt,'valuation':val,'date':date,
            'leads':leads,'follows':follows,'is_mna':rnd=='M&A','amount_m':parse_m(amt),
            'has_top':any(t in inv for t in TOP)})
    fund=sorted([e for e in entries if not e['is_mna']],key=lambda e:(e['amount_m'],int(e['has_top'])),reverse=True)
    mna=[e for e in entries if e['is_mna']]
    total_m=sum(e['amount_m'] for e in fund)
    print("=== Part.2 关键数据 ===")
    print(f"融资项目数：{len(fund)} 件")
    print(f"总融资额：约 {total_m/100:.2f} 亿美元" if total_m>=100 else f"总融资额：约 {total_m:.1f}M 美元")
    print(f"并购交易：{len(mna)} 起\n")
    n=5 if len(fund)<=15 else 10
    top_n=fund[:n]+[e for e in fund[n:] if e['has_top']][:2]
    print(f"=== Part.4 主要融资事件（Top {len(top_n)}）===")
    for e in top_n:
        ls='、'.join(e['leads'])+' 领投' if e['leads'] else ''
        fs='、'.join(e['follows'][:5])+' 参投' if e['follows'] else ''
        inv_s='；'.join(filter(None,[ls,fs])) or '未披露'
        amt_s=e['amount'] if e['amount']!='--' else '金额未披露'
        val_s=f"，估值 {e['valuation']}" if e['valuation'] not in ('--','') else ''
        print(f"\n【{e['name']}】\n定位：（AI 搜索补充）\n轮次与金额：{amt_s} {e['round']}{val_s}\n投资方：{inv_s}\n点评：（AI 生成）")
    if mna:
        print(f"\n=== Part.6 并购交易 ===")
        for e in mna:
            acq=e['leads'][0] if e['leads'] else (e['follows'][0] if e['follows'] else '未披露')
            amt_s=f"，金额 {e['amount']}" if e['amount']!='--' else ''
            print(f"\n{acq} 收购 {e['name']}{amt_s}\n分析：（AI 生成）")
