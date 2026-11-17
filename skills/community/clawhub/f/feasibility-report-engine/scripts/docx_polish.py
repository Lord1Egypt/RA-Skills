#!/usr/bin/env python3
"""可研报告 docx 排版引擎 —— AI 初稿 → 专业交付版 一键流水线

用前必装: pip install python-docx
用法:
  python3 docx_polish.py 输入.docx 输出.docx "项目全称" [--title 报告标题] [--no-cover-src]

阶段（顺序执行，全部幂等可重跑）:
  S1 符号清理   ：「」→“” 、全角＋→+ 、全角空格→半角（AI味清除）
  S2 首行缩进    ：正文段落 firstLine=2字符（标题/封面/空段/表格除外）
  S3 标题体系    ：Heading1-4 字号字体统一（16黑/14黑/13楷/12仿宋）——样式驱动，导航窗格可见
  S4 列表悬挂    ："- " 开头段落设悬挂缩进（换行文字对齐条目）
  S5 正文字号    ：14pt→12pt（小四）；表格字号统一 10.5pt
  S6 封面留空    ：编制单位/日期/文件编号/资料密级 处理（单位与日期由客户自填）
  S7 表格美化    ：细灰边框+表头浅蓝底纹+行高自动+单元格边距+禁止跨页断行
  S8 元数据      ：author/company 清空（去 python-docx 痕迹）

适用: AI 生成的 / 客户给的 raw docx → 对外交付版。
说明: 封面/签署页/目录域 重建请配合 scripts/face_docx.py 使用（本引擎处理内容层，
      face_docx 处理门面层，先 face 后 polish 或先 polish 后 face 均可）。
"""
import re, sys, shutil
import docx
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def log(*a): print(*a, flush=True)

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    pname = sys.argv[3] if len(sys.argv) > 3 else "××××项目"
    argv = sys.argv[4:]
    TITLE = None
    for i,a in enumerate(argv):
        if a == '--title': TITLE = argv[i+1]
    shutil.copy(src, dst)
    doc = docx.Document(dst)
    if TITLE: doc.core_properties.title = TITLE

    # ---------- S1 符号清理 ----------
    def clean(paras):
        n1=n2=n3=0
        for p in paras:
            for r in p.runs:
                if not r.text: continue
                t = r.text
                if '「' in t or '」' in t: t = t.replace('「','“').replace('」','”'); n1+=1
                if '＋' in t: t = t.replace('＋','+'); n2+=1
                if '\u3000' in t: t = t.replace('\u3000',' '); n3+=1
                r.text = t
        return n1,n2,n3
    body_paras = list(doc.paragraphs)
    tbl_paras  = [p for tb in doc.tables for row in tb.rows for c in row.cells for p in c.paragraphs]
    a = clean(body_paras); b = clean(tbl_paras)
    log(f"S1 符号清理: 正文「」{a[0]} ＋{a[1]} 全角空格{a[2]} | 表格「」{b[0]} ＋{b[1]} 全角空格{b[2]}")

    def is_cover(p):
        t = p.text.strip()
        if not t: return False
        sizes = [r.font.size.pt for r in p.runs if r.font.size]
        if sizes and max(sizes) > 18: return True
        return t in ('目  录','目录') or t.startswith('编制单位') or (t.startswith('年') and len(t)<10) or t.startswith('文件编号')

    # ---------- S2 首行缩进 ----------
    n_ind = 0
    for i,p in enumerate(body_paras):
        t = p.text.strip()
        if not t: continue
        st = p.style.name if p.style else ''
        if st.startswith('Heading'): continue
        if i < 30 and (is_cover(p) or not t): continue
        pPr = p._p.get_or_add_pPr()
        ind = pPr.find(qn('w:ind'))
        if ind is None: ind = OxmlElement('w:ind'); pPr.append(ind)
        # 表格/列表已有悬挂缩进的不重复加首行
        if ind.get(qn('w:hangingChars')): continue
        ind.set(qn('w:firstLineChars'),'200'); ind.set(qn('w:firstLine'),'480')
        n_ind += 1
    log(f"S2 首行缩进: {n_ind} 段")

    # ---------- S3 标题体系 ----------
    sizes = {'Heading 1':(16,'黑体'),'Heading 2':(14,'黑体'),'Heading 3':(13,'楷体_GB2312'),'Heading 4':(12,'仿宋_GB2312'),
             'Heading1':(16,'黑体'),'Heading2':(14,'黑体'),'Heading3':(13,'楷体_GB2312'),'Heading4':(12,'仿宋_GB2312')}
    n_h = 0
    for p in body_paras:
        st = p.style.name if p.style else ''
        if st in sizes:
            sz, cn = sizes[st]
            for r in p.runs:
                if not r.text: continue
                r.font.size = Pt(sz); r.font.name = 'Times New Roman'; r.font.bold = True
                rPr = r._element.get_or_add_rPr()
                rf = rPr.find(qn('w:rFonts'))
                if rf is None: rf = OxmlElement('w:rFonts'); rPr.append(rf)
                rf.set(qn('w:eastAsia'), cn)
            n_h += 1
    log(f"S3 标题统一: {n_h} 段")

    # ---------- S4 列表悬挂缩进 ----------
    n_lst = 0
    for i,p in enumerate(body_paras):
        t = p.text
        if not t.strip(): continue
        st = p.style.name if p.style else ''
        if st.startswith('Heading'): continue
        if i < 30 and is_cover(p): continue
        if re.match(r'^\s*[-•·]\s+', t):
            pPr = p._p.get_or_add_pPr()
            ind = pPr.find(qn('w:ind'))
            if ind is None: ind = OxmlElement('w:ind'); pPr.append(ind)
            ind.set(qn('w:leftChars'),'200'); ind.set(qn('w:left'),'480')
            ind.set(qn('w:hangingChars'),'200'); ind.set(qn('w:hanging'),'480')
            n_lst += 1
    log(f"S4 列表悬挂缩进: {n_lst} 段")

    # ---------- S5 正文字号 14→12 ----------
    n_sz = 0
    for i,p in enumerate(body_paras):
        t = p.text.strip()
        if not t: continue
        st = p.style.name if p.style else ''
        if st.startswith('Heading'): continue
        if i < 30 and any(r.font.size and r.font.size.pt >= 16 for r in p.runs): continue
        for r in p.runs:
            if r.text and r.font.size and r.font.size.pt == 14:
                r.font.size = Pt(12); n_sz += 1
    # 表格统一 10.5pt
    n_tbl = 0
    for tb in doc.tables:
        for row in tb.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        if r.text and r.font.size and r.font.size.pt != 10.5:
                            r.font.size = Pt(10.5); n_tbl += 1
    log(f"S5 字号: 正文14→12 {n_sz} runs, 表格→10.5 {n_tbl} runs")

    # ---------- S6 封面留空 ----------
    def re_match_year(t): return bool(re.match(r'^二〇\d+年', t))
    for p in doc.paragraphs[:30]:
        t = p.text.strip()
        if not t: continue
        if t.startswith('编制单位：'):
            for r in p.runs: r.text=''
            r = p.add_run('编制单位：'); r.font.size=Pt(16); r.font.name='Times New Roman'
            rPr = r._element.get_or_add_rPr()
            rf = rPr.find(qn('w:rFonts'))
            if rf is None: rf = OxmlElement('w:rFonts'); rPr.append(rf)
            rf.set(qn('w:eastAsia'),'仿宋_GB2312')
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            log("S6 封面编制单位留空")
        elif t.startswith('二〇') or re_match_year(t):
            for r in p.runs: r.text=''
            r = p.add_run('年    月'); r.font.size=Pt(16); r.font.name='Times New Roman'
            rPr = r._element.get_or_add_rPr()
            rf = rPr.find(qn('w:rFonts'))
            if rf is None: rf = OxmlElement('w:rFonts'); rPr.append(rf)
            rf.set(qn('w:eastAsia'),'仿宋_GB2312')
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            log("S6 封面日期留空")
        elif t.startswith('文件编号'):
            for r in p.runs: r.text=''
            p.add_run('文件编号：')
            log("S6 封面文件编号留空")
        elif t.startswith('资料密级'):
            p._p.getparent().remove(p._p)
            log("S6 删除封面资料密级行")

    # ---------- S7 表格美化 ----------
    def set_borders(table, color="808080", sz="4"):
        tblPr = table._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for edge in ('top','left','bottom','right','insideH','insideV'):
            el = OxmlElement(f'w:{edge}')
            el.set(qn('w:val'),'single'); el.set(qn('w:sz'),sz); el.set(qn('w:color'),color)
            borders.append(el)
        old = tblPr.find(qn('w:tblBorders'))
        if old is not None: tblPr.remove(old)
        tblPr.append(borders)
    def set_margins(table, top=40, bottom=40, left=80, right=80):
        tblPr = table._tbl.tblPr
        m = OxmlElement('w:tblCellMar')
        for name,val in (('top',top),('start',left),('bottom',bottom),('end',right)):
            el = OxmlElement(f'w:{name}'); el.set(qn('w:w'),str(val)); el.set(qn('w:type'),'dxa'); m.append(el)
        old = tblPr.find(qn('w:tblCellMar'))
        if old is not None: tblPr.remove(old)
        tblPr.append(m)
    n_t = 0
    for table in doc.tables:
        try:
            set_borders(table); set_margins(table)
            for row in table.rows:  # 禁止跨页断行
                trPr = row._tr.get_or_add_trPr()
                cs = OxmlElement('w:cantSplit'); trPr.append(cs)
            # 表头底纹加粗
            if table.rows:
                for c in table.rows[0].cells:
                    tcPr = c._tc.get_or_add_tcPr()
                    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:fill'),'D9E2F3')
                    tcPr.append(shd)
                    for p in c.paragraphs:
                        for r in p.runs:
                            if r.text: r.font.bold = True
            # 表格段落去首行缩进
            for row in table.rows:
                for c in row.cells:
                    for p in c.paragraphs:
                        pPr = p._p.get_or_add_pPr()
                        ind = pPr.find(qn('w:ind'))
                        if ind is not None:
                            if ind.get(qn('w:firstLineChars')): ind.set(qn('w:firstLineChars'),'0')
                            if ind.get(qn('w:firstLine')): ind.set(qn('w:firstLine'),'0')
            n_t += 1
        except Exception as e:
            log(f"  表{n_t+1} 失败: {str(e)[:60]}")
    log(f"S7 表格美化: {n_t}/{len(doc.tables)}")

    # ---------- S8 元数据 ----------
    cp = doc.core_properties
    cp.author=''; cp.last_modified_by=''; cp.comments=''; cp.company=''
    if not cp.title: cp.title = pname
    doc.save(dst)
    log(f"✓ 完成 → {dst}")

if __name__ == '__main__':
    main()
