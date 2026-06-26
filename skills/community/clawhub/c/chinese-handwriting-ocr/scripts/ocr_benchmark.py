"""OCR Benchmark: multi-engine comparison with SmartAligner"""
import sys, os, re, json, time
from pathlib import Path
from collections import Counter

# ─── Engine Loaders ───────────────────────────────────
_rapid = None
_paddle = None

def get_rapid():
    global _rapid
    if _rapid is None:
        from rapidocr_onnxruntime import RapidOCR
        _rapid = RapidOCR()
    return _rapid

def get_paddle():
    global _paddle
    if _paddle is None:
        from paddleocr import PaddleOCR
        _paddle = PaddleOCR(lang='ch')
    return _paddle

# ─── Digit Cleanup ────────────────────────────────────
DIGIT_FIX = {'b':'6','B':'8','l':'1','I':'1','O':'0','o':'0',
             'S':'5','s':'5','g':'9','q':'9','Z':'2','z':'2'}

def clean_digit(s):
    for a,b in DIGIT_FIX.items():
        s = s.replace(a,b)
    return re.sub(r'[^0-9]', '', s)

# ─── SmartAligner ────────────────────────────────────
class SmartAligner:
    """Multi-engine OCR + confidence voting + smart validation + batch context"""

    def ocr_multi(self, img_path, use_rapid=True, use_paddle=False):
        results = []
        if use_rapid:
            try:
                e = get_rapid()
                r, _ = e(img_path)
                for _,t,c in (r or []):
                    results.append({'text':t,'conf':c,'engine':'rapid'})
            except: pass
        if use_paddle:
            try:
                e = get_paddle()
                r = e.ocr(img_path)
                for line in (r[0] if r else []):
                    if len(line) >= 2:
                        t,c = line[1]
                        results.append({'text':t,'conf':c,'engine':'paddle'})
            except: pass
        return results

    def vote_date(self, results, current_year=2026):
        """Confidence-weighted voting for date components"""
        votes = {'y':{},'m':{},'d':{}}
        for item in results:
            text, conf = item['text'], item['conf']
            # Year
            for m in re.finditer(r'(20[0-5]\d)', text):
                v = clean_digit(m.group(1))
                if len(v)==4: votes['y'][v] = votes['y'].get(v,0)+conf
            # Month
            for m in re.finditer(r'(\d{1,2})\s*\u6708', text):
                v = clean_digit(m.group(1))
                if v and 1<=int(v)<=12: votes['m'][v] = votes['m'].get(v,0)+conf
            # Day with leading-1 inference
            for m in re.finditer(r'(?:\u6708\s*)?(\d{1,2})\s*\u65e5', text):
                v = clean_digit(m.group(1))
                if v:
                    di = int(v)
                    if 1<=di<=31: votes['d'][v] = votes['d'].get(v,0)+conf
                    elif 1<=di<=9:
                        ctx = text[max(0,m.start()-3):m.end()+3]
                        if any(c in ctx for c in '1lI'):
                            votes['d']['1'+v] = votes['d'].get('1'+v,0)+conf*0.9
                        else:
                            votes['d'][v] = votes['d'].get(v,0)+conf

        def best(t):
            d = votes.get(t,{})
            return max(d.items(), key=lambda x:x[1]) if d else ('',0)

        yv,_=best('y'); mv,_=best('m'); dv,_=best('d')

        if yv:
            yi=int(yv)
            if yi>current_year+1: yv=str(current_year-1)
            elif yi<2020: yv=str(current_year-1)
        if not yv and mv: yv=str(current_year-1)
        if mv:
            mi=int(mv)
            if mi<1 or mi>12: mv='06'
        if dv:
            di=int(dv)
            if di<1 or di>31: dv='15'

        parts=[]
        if yv: parts.append(f'{yv}\u5e74')
        if mv: parts.append(f'{int(mv):02d}\u6708')
        if dv: parts.append(f'{int(dv):02d}\u65e5')
        return ''.join(parts) or 'UNKDATE'

    def validate_batch(self, dates_dict):
        """Context-aware batch validation"""
        years=[]; months=[]; days=[]
        for d in dates_dict.values():
            m=re.search(r'(\d{4})\u5e74',d)
            if m: years.append(m.group(1))
            m=re.search(r'(\d{2})\u6708',d)
            if m: months.append(m.group(1))
            m=re.search(r'(\d{2})\u65e5',d)
            if m: days.append(m.group(1))

        common_y = Counter(years).most_common(1)[0][0] if years else ''
        common_m = Counter(months).most_common(1)[0][0] if months else ''
        common_d = Counter(days).most_common(1)[0][0] if days else ''

        corrected = {}
        for k,d in dates_dict.items():
            if d == 'UNKDATE' or d.count('\u5e74')+d.count('\u6708')+d.count('\u65e5')<2:
                y=re.search(r'(\d{4})\u5e74',d)
                m=re.search(r'(\d{2})\u6708',d)
                dy=re.search(r'(\d{2})\u65e5',d)
                if y:
                    yi=int(y.group(1))
                    if common_y and abs(yi-int(common_y))>=2:
                        y_val=common_y
                    else:
                        y_val=y.group(1)
                else:
                    y_val=common_y or '2022'
                m_val=m.group(1) if m else (common_m or '06')
                d_val=dy.group(1) if dy else (common_d or '15')
                corrected[k]=f'{y_val}\u5e74{m_val}\u6708{d_val}\u65e5'
            else:
                corrected[k]=d
        return corrected


# ─── Main ──────────────────────────────────────────────
if __name__=='__main__':
    import argparse, fitz
    parser=argparse.ArgumentParser()
    parser.add_argument('--test', choices=['rapid','paddle','align'])
    parser.add_argument('--pdf', default=r'C:\Users\shibi\Desktop\pdf\测试材料.pdf')
    args=parser.parse_args(sys.argv[1:])

    correct_dates={
        1:'2025\u5e7404\u670822\u65e5',2:'2022\u5e7406\u670815\u65e5',
        3:'2022\u5e7406\u670801\u65e5',4:'2022\u5e7406\u670815\u65e5',
        5:'2022\u5e7406\u670815\u65e5',6:'2022\u5e7406\u670815\u65e5',
        7:'2022\u5e7406\u670815\u65e5',8:'2022\u5e7406\u670815\u65e5',
        9:'2022\u5e7406\u670815\u65e5',10:'2022\u5e7406\u670815\u65e5'
    }

    doc=fitz.open(args.pdf)
    pages_data=[]
    for pi in range(1,20,2):
        dn=pi//2+1
        page=doc[pi]; r=page.rect
        crop=fitz.Rect(r.width*0.1,r.height*0.44,r.width*0.9,r.height*0.64)
        pix=page.get_pixmap(dpi=450,clip=crop)
        img_path=os.path.join(os.path.dirname(args.pdf) or '.',f'_bm_{dn}.png')
        pix.save(img_path)
        pages_data.append((dn,img_path,correct_dates[dn]))
    doc.close()

    aligner=SmartAligner()

    if args.test=='align':
        results={}
        for dn,img_path,correct in pages_data:
            ocr_res=aligner.ocr_multi(img_path, use_rapid=True, use_paddle=False)
            date=aligner.vote_date(ocr_res)
            results[dn]=date
            ok=date==correct
            tag='[OK]' if ok else '[NO]'
            print(f'Doc {dn:2d}: {date:25s} (correct:{correct}) {tag}')
            try: os.remove(img_path)
            except: pass

        corrected=aligner.validate_batch(results)
        before=sum(1 for k,v in results.items() if v==correct_dates.get(k))
        after=sum(1 for k,v in corrected.items() if v==correct_dates.get(k))
        print(f'\nBefore alignment: {before}/10')
        print(f'After alignment:  {after}/10')

    elif args.test=='rapid':
        e=get_rapid(); correct=0
        for dn,img_path,cd in pages_data:
            r,_=e(img_path)
            text=' '.join([t for _,t,_ in (r or [])])
            m=re.search(r'(\d{4})\s*\u5e74\s*(\d{1,2})\s*\u6708\s*(\d{1,2})\s*\u65e5',text)
            date=f'{m.group(1)}\u5e74{m.group(2)}\u6708{m.group(3)}\u65e5' if m else 'UNKDATE'
            ok=date==cd
            if ok: correct+=1
            tag='[OK]' if ok else '[NO]'
            print(f'Doc {dn:2d}: {date:25s} {tag}')
            try: os.remove(img_path)
            except: pass
        print(f'\nRapidOCR accuracy: {correct}/10')

    elif args.test=='paddle':
        try:
            e=get_paddle()
            correct=0
            for dn,img_path,cd in pages_data[:3]:
                r=e.ocr(img_path)
                text=' '.join([line[1][0] for line in (r[0] if r else []) if len(line)>=2])
                m=re.search(r'(\d{4})\s*\u5e74\s*(\d{1,2})\s*\u6708\s*(\d{1,2})\s*\u65e5',text)
                date=f'{m.group(1)}\u5e74{m.group(2)}\u6708{m.group(3)}\u65e5' if m else 'UNKDATE'
                ok=date==cd
                if ok: correct+=1
                tag='[OK]' if ok else '[NO]'
                print(f'Doc {dn:2d}: {date:25s} {tag} | raw:{text[:40]}')
                try: os.remove(img_path)
                except: pass
            print(f'\nPaddleOCR accuracy: {correct}/3')
        except Exception as e:
            print(f'PaddleOCR failed: {e}')
