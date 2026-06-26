"""ocr_date_extractor.py - 手写日期提取引擎 v4 (实用版)
改进:
1. 动态日期行定位 → 不依赖固定裁剪
2. 单帧高精度OCR → 快 
3. 智能后处理校验 → 修正OCR常见错误
"""
import sys, os, re, json, argparse
from rapidocr_onnxruntime import RapidOCR
from collections import Counter
import fitz

_ENGINE = None
def engine():
    global _ENGINE
    if _ENGINE is None: _ENGINE = RapidOCR()
    return _ENGINE

def _ocr(img):
    e = engine()
    return e(img)

# ─── 1. 动态定位 ──────────────────────────────────────
def find_date_line(page):
    """全页低分OCR找包含'月'的行"""
    pix = page.get_pixmap(dpi=150)
    tmp = os.path.join(os.environ['TEMP'], f'_dl_{id(page)}.png')
    pix.save(tmp)
    res, _ = _ocr(tmp)
    try: os.remove(tmp)
    except: pass
    
    best = None
    for bbox,text,conf in (res or []):
        if '月' in text:
            y1 = bbox[0][1]/pix.height
            y2 = bbox[2][1]/pix.height
            if best is None or conf > best[2]:
                best = (y1, y2, conf, text[:20])
    
    if best: return best[0], best[1]
    return 0.46, 0.60  # fallback

# ─── 2. 日期OCR (单帧高精度) ──────────────────────────
def read_date(page, crop):
    pix = page.get_pixmap(dpi=450, clip=crop)
    tmp = os.path.join(os.environ['TEMP'], f'_rd_{id(page)}.png')
    pix.save(tmp)
    res, _ = _ocr(tmp)
    try: os.remove(tmp)
    except: pass
    
    # 解析日期组件
    year=month=day=''
    for _,text,conf in (res or []):
        m = re.search(r'(\d{4})\s*年', text)
        if m: year = m.group(1)
        m = re.search(r'(\d{1,2})\s*月', text)
        if m: month = m.group(1)
        m = re.search(r'(?:月\s*)?(\d{1,2})\s*日', text)
        if m:
            d = m.group(1)
            # 如果日是1-9但附近有"1"，可能是漏了前导
            if len(d)==1 and '1' in text[max(0,m.start()-3):m.start()]:
                day = '1'+d
            else:
                day = d
    
    parts = []
    if year: parts.append(f"{year}年")
    if month: parts.append(f"{int(month):02d}月")
    if day: parts.append(f"{int(day):02d}日")
    return ''.join(parts) or 'UNKDATE'

# ─── 3. 智能校验 ──────────────────────────────────────
def smart_check(d, cy=2026):
    if not d or d=='UNKDATE': return 'UNKDATE'
    
    y=m=day=''
    mm = re.search(r'(\d{4})年', d)
    if mm: y=mm.group(1)
    mm = re.search(r'(\d{1,2})月', d)
    if mm: m=mm.group(1)
    mm = re.search(r'(\d{1,2})日', d)
    if mm: day=mm.group(1)
    
    # 年
    if y:
        yi = int(y)
        if yi > cy+1: y = str(cy-1)
        elif yi < 2020: y = str(cy-1)
    if not y and m: y = str(cy-1)
    
    # 月
    if m:
        mi = int(m)
        if mi<1 or mi>12: m='06'
    
    # 日
    if day:
        di = int(day)
        if di<1 or di>31: day='15'
    elif m:
        day = '15'  # 有月无日，推断为15
    
    parts=[]
    if y: parts.append(f"{y}年")
    if m: parts.append(f"{int(m):02d}月")
    if day: parts.append(f"{int(day):02d}日")
    return ''.join(parts) or 'UNKDATE'

# ─── Main ──────────────────────────────────────────────
def extract(pdf_path):
    doc = fitz.open(pdf_path)
    results = {}
    
    for pi in range(1, len(doc), 2):
        dn = pi//2 + 1
        page = doc[pi]
        r = page.rect
        
        y1,y2 = find_date_line(page)
        crop = fitz.Rect(r.width*0.1, r.height*max(0,y1-0.02),
                         r.width*0.9, r.height*min(1,y2+0.02))
        date = read_date(page, crop)
        date = smart_check(date)
        results[dn] = date
    
    doc.close()
    
    # 上下文补充UNKDATE
    months = []
    for d in results.values():
        mm = re.search(r'(\d{2})月', d)
        if mm: months.append(mm.group(1))
    cm = Counter(months).most_common(1)[0][0] if months else '06'
    years = []
    for d in results.values():
        mm = re.search(r'(\d{4})年', d)
        if mm: years.append(mm.group(1))
    cy = Counter(years).most_common(1)[0][0] if years else '2022'
    
    for k,v in results.items():
        if v == 'UNKDATE':
            results[k] = f"{cy}年{cm}月"
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(sys.argv[1:])
    
    results = extract(args.input)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for k,v in sorted(results.items()):
            print(f'Doc {k:2d}: {v}')
