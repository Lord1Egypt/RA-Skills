#!/usr/bin/env python3
"""DXF 中文字体自检工具: 排查"文字变方块/问号"。
真正会方块的是"含中文字符的实体所用样式未配 bigfont/TrueType"。本脚本:
 1) 打印文字样式(font + bigfont)
 2) 检查引用样式是否已定义
 3) 检查含中文的实体样式是否配 bigfont 或 TrueType 字体(否则 CAD 中文变方块)
用法: python3 check_dxf_fonts.py <file.dxf>
"""
import sys, ezdxf

def zh(s): return any('\u4e00' <= c <= '\u9fff' for c in s)

def ok_style(st):
    big = getattr(st.dxf, 'bigfont', '')
    font = getattr(st.dxf, 'font', '')
    return bool(big) or font.lower().endswith(('.ttf', '.ttc'))

def check(dxfpath):
    doc = ezdxf.readfile(dxfpath)
    print(f"== 字体自检: {dxfpath} ==")
    print("-- 文字样式 --")
    for st in doc.styles:
        print(f"   {st.dxf.name:12} font={getattr(st.dxf,'font','')!r} "
              f"bigfont={getattr(st.dxf,'bigfont','')!r}")
    stmap = {st.dxf.name: st for st in doc.styles}
    containers = [doc.modelspace()] + [
        doc.blocks.get(n) for n in doc.blocks.block_names() if not n.startswith('*')]
    ref_used = set(); zh_used = set(); cnt = 0
    for c in containers:
        for e in c.query('TEXT MTEXT ATTDEF'):
            ref_used.add(e.dxf.get('style', 'Standard')); cnt += 1
            if zh(e.dxf.get('text', '')): zh_used.add(e.dxf.get('style', 'Standard'))
        for ins in c.query('INSERT'):
            for a in ins.attribs:
                ref_used.add(a.dxf.get('style', 'Standard')); cnt += 1
                if zh(a.dxf.get('text', '')): zh_used.add(a.dxf.get('style', 'Standard'))
    missing = [s for s in ref_used if s not in stmap]
    bad = [(s, stmap[s]) for s in zh_used if s in stmap and not ok_style(stmap[s])]
    bad += [('(样式未定义)', None) for s in zh_used if s not in stmap]
    print(f"-- 文字实体核查(共{cnt}) --")
    if missing:
        print(f"   [!] 引用未定义样式: {sorted(missing)}")
    if bad:
        for s, st in bad:
            print(f"   [!] 含中文的样式 {s!r} 未配bigfont/非TrueType -> CAD中中文会变方块")
        print("        => 修复: 把中文实体样式改为 配 GB_HZ 大字体组合 或 TrueType")
    else:
        print(f"   含中文的样式 {sorted(zh_used)} 均已配 bigfont/TrueType, 中文可正常显示")
    print("== " + ("结论: 字体配置完整" if not (missing or bad) else "结论: 存在需修复的中文字体问题") + " ==")
    return not (missing or bad)

if __name__ == "__main__":
    ok = check(sys.argv[1] if len(sys.argv) > 1 else "国标A3图纸模板-字体修复-20260808-1424.dxf")
    sys.exit(0 if ok else 1)
