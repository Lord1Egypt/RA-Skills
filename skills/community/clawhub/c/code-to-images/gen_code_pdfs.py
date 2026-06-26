#!/usr/bin/env python3
"""Batch convert code files -> A4 images + PDF. One PDF per source file."""
import os, sys, subprocess, json

# ===== CONFIG =====
FILES = ['disp_test.c']
FONT_KEY = 'cascadia'   # cascadia | firacode | jetbrains | consolas | courier | sourcecode
FONT_SIZE = 14
LINE_HEIGHT_RATIO = 1.65
TAB_WIDTH = 4
MIN_FONT_SIZE = 7
WRAP_IDENT = 2

FONT_NAMES = {
    'cascadia':'Cascadia Code','firacode':'Fira Code','jetbrains':'JetBrains Mono',
    'consolas':'Consolas','courier':'Courier New','sourcecode':'Source Code Pro',
}

A4_W, A4_H = 794, 1123
HDR_H = 60; PAD_R = 36; PAD_T = 72; PAD_B = 28
CONTENT_H = A4_H - PAD_T - PAD_B
CHAR_RATIO = 0.60
WRAP_PUNCT = set(';,(){}[]')

KW = {'void','char','int','u8','u16','u32','uchar','unsigned',
      'for','if','else','while','switch','case','break','return',
      'static','bit','sbit','xdata','idata','code','interrupt',
      'do','default','continue','struct','typedef','enum','const',
      '#ifndef','#define','#endif','#ifdef','extern'}
RG = {'P0','P1','P2','P3','P4','P5','P6','P7','RST','SCLK','IO','SCK'}
CO = {'keyword':'#d63384','register':'#e8590c','macro':'#099268',
      'number':'#2b8a3e','string':'#099268','comment':'#868e96',
      'var':'#1971c2','text':'#212529'}
BG='#ffffff'; HDR_BG='#f1f3f5'; HDR_BD='#dee2e6'
GT_BG='#f8f9fa'; GT_BD='#e9ecef'; LN_COLOR='#868e96'


def display_len(text):
    n = 0
    for ch in text:
        if ch == '\t':
            n += TAB_WIDTH - (n % TAB_WIDTH)
        else:
            n += 1
    return n


def compute_indent_levels(lines, all_tokens):
    """Compute indent level based on brace depth ({} nesting).
    0 = top level, 1 = inside one { }, 2 = inside two { }, etc.
    Each level renders at TAB_WIDTH * cw pixels."""
    depths = [0] * len(lines)
    depth = 0
    for idx, (line, toks) in enumerate(zip(lines, all_tokens)):
        depths[idx] = depth
        for val, typ in toks:
            if typ in ('comment', 'string'):
                continue
            for ch in val:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth = max(0, depth - 1)
    return depths


def tokenize_line(line, in_comment=False):
    if in_comment:
        return [(line, 'comment')], False
    t, i, n = [], 0, len(line)
    while i < n:
        if line[i] == '#':
            j = i+1
            while j < n and line[j] not in '\n\r': j += 1
            t.append((line[i:j], 'macro')); break
        if line[i:i+2] == '//':
            t.append((line[i:], 'comment')); break
        if line[i:i+2] == '/*':
            j = i+2
            while j < n and line[j:j+2] != '*/': j += 1
            if j < n: j += 2
            t.append((line[i:j], 'comment'))
            if j >= n or line[j-2:j] != '*/':
                return t, True
            i = j; continue
        if line[i] in '"\'':
            q = line[i]; j = i+1
            while j < n and line[j] != q:
                if line[j] == '\\': j += 1
                j += 1
            if j < n: j += 1
            t.append((line[i:j], 'string')); i = j; continue
        if line[i] in ' \t':
            j = i
            while j < n and line[j] in ' \t': j += 1
            t.append((line[i:j], 'space')); i = j; continue
        if line[i].isdigit() or (line[i]=='0' and i+1<n and line[i+1] in 'xXbB'):
            if line[i]=='0' and i+1<n and line[i+1] in 'xXbB': j = i+2
            else: j = i
            while j < n and (line[j].isalnum() or line[j] in '.xXa-fA-FbBoOdD'): j += 1
            t.append((line[i:j], 'number')); i = j; continue
        if line[i].isalpha() or line[i] == '_':
            j = i
            while j < n and (line[j].isalnum() or line[j] == '_'): j += 1
            w = line[i:j]
            if w in KW: t.append((w,'keyword'))
            elif w in RG: t.append((w,'register'))
            else: t.append((w,'text'))
            i = j; continue
        t.append((line[i],'text')); i += 1
    if not t:
        t.append(('','space'))
    return t, False


def tokenize_full(lines):
    result, in_block = [], False
    for line in lines:
        toks, cont = tokenize_line(line, in_block)
        result.append(toks)
        in_block = cont
    return result


def wrap_line_tokens(tokens, max_px, cw, indent_px):
    """Wrap tokenized line if it exceeds max_px width.
    Returns list of (tokens, is_continuation) tuples.
    Continuation lines do NOT get their own line number."""
    # Reconstruct full text from tokens (including spaces)
    text = ''.join(val for val, typ in tokens)
    if not text.strip():
        return [(tokens, False)]
    raw = text
    dl = display_len(raw.rstrip('\r\n'))
    if dl * cw <= max_px:
        return [(tokens, False)]

    max_chars = int(max_px / cw)
    parts = []
    remaining = raw
    is_first = True
    while remaining:
        avail = max_chars if is_first else int((max_px - indent_px) / cw)
        if avail < 10:
            avail = max_chars
        rem_dl = display_len(remaining.rstrip('\r\n'))
        limit_px = max_px if is_first else max_px - indent_px
        if rem_dl * cw <= limit_px:
            parts.append((tokenize_line(remaining, False)[0], not is_first))
            break
        wrap_pos = -1
        pos = 0
        for i, ch in enumerate(remaining):
            if ch == '\t':
                pos += TAB_WIDTH - (pos % TAB_WIDTH)
            else:
                pos += 1
            if ch in WRAP_PUNCT:
                wrap_pos = i + 1
            elif ch == ' ' and pos > avail * 0.6:
                wrap_pos = i + 1
            if pos > avail and wrap_pos > 0:
                break
        if wrap_pos <= 0:
            pos = 0
            for i, ch in enumerate(remaining):
                if ch == '\t':
                    pos += TAB_WIDTH - (pos % TAB_WIDTH)
                else:
                    pos += 1
                if pos > avail:
                    wrap_pos = i
                    break
            if wrap_pos <= 0 or wrap_pos >= len(remaining):
                wrap_pos = len(remaining)
        if wrap_pos >= len(remaining):
            parts.append((tokenize_line(remaining, False)[0], not is_first))
            break
        seg = remaining[:wrap_pos]
        parts.append((tokenize_line(seg, False)[0], not is_first))
        remaining = remaining[wrap_pos:]
        is_first = False
    return parts


def compute_layout(lines, font_size):
    fs = round(font_size, 1)
    cw = round(fs * CHAR_RATIO, 1)
    lh = round(fs * LINE_HEIGHT_RATIO, 1)
    max_ln = len(str(len(lines)))
    gutter = round(max(44, max_ln * cw + 20), 1)
    code_x = round(gutter + 12, 1)
    code_w = round(A4_W - code_x - PAD_R, 1)
    baseline_ofs = round(fs * 0.85, 1)
    return fs, cw, lh, gutter, code_x, code_w, baseline_ofs


def compute_optimal_font(lines, base_fs, min_fs):
    max_digits = len(str(len(lines)))
    est_g = max(44, max_digits * (base_fs * CHAR_RATIO) + 20)
    est_w = A4_W - est_g - 12 - PAD_R
    max_chars = max((display_len(l.rstrip('\r\n')) for l in lines), default=1)
    if max_chars == 0: max_chars = 1
    fs = max(min_fs, min(base_fs, est_w / (max_chars * CHAR_RATIO)))
    # recalc
    est_g2 = max(44, max_digits * (fs * CHAR_RATIO) + 20)
    est_w2 = A4_W - est_g2 - 12 - PAD_R
    fs = max(min_fs, min(base_fs, est_w2 / (max_chars * CHAR_RATIO)))
    return round(fs, 1)


def gen_svg_page(display_lines, total_lines, page_num, total_pages,
                 fname, font_key, fs, cw, lh, gutter, code_x, code_w, baseline_ofs):
    fn = FONT_NAMES.get(font_key, 'Cascadia Code')
    font_family = '"' + fn + '","Fira Code","Consolas","Courier New",monospace'
    font_name = fn
    ff_sans = 'Arial, Helvetica, sans-serif'
    wrap_px = WRAP_IDENT * cw

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {A4_W} {A4_H}">']
    out.append('<defs>')
    out.append(f'<clipPath id="pageClip"><rect x="0" y="0" width="{A4_W}" height="{A4_H}"/></clipPath>')
    out.append(f'<clipPath id="codeClip"><rect x="{code_x}" y="{PAD_T}" width="{code_w}" height="{CONTENT_H}"/></clipPath>')
    out.append('</defs>')
    out.append(f'<g clip-path="url(#pageClip)">')

    out.append(f'<rect width="{A4_W}" height="{A4_H}" fill="{BG}"/>')
    out.append(f'<rect x="0" y="0" width="{A4_W}" height="{HDR_H}" fill="{HDR_BG}"/>')
    out.append(f'<line x1="0" y1="{HDR_H}" x2="{A4_W}" y2="{HDR_H}" stroke="{HDR_BD}" stroke-width="1.5"/>')

    fl = font_key.capitalize()
    out.append(f'<text x="20" y="24" fill="#343a40" font-size="16" font-family="{ff_sans}" font-weight="700">FILE {fname}</text>')
    out.append(f'<text x="20" y="44" fill="#868e96" font-size="11" font-family="{ff_sans}">Pg {page_num}/{total_pages}  Lns {total_lines}  Font {fl} {fs}px</text>')

    out.append(f'<rect x="0" y="{HDR_H}" width="{gutter+8}" height="{A4_H-HDR_H}" fill="{GT_BG}"/>')
    out.append(f'<line x1="{gutter+8}" y1="{HDR_H}" x2="{gutter+8}" y2="{A4_H}" stroke="{GT_BD}" stroke-width="1"/>')

    # LINE NUMBERS - rendered BEFORE codeClip, always visible
    for idx, (tokens, is_cont, src_ln, depth) in enumerate(display_lines):
        if not src_ln:
            continue
        ly = PAD_T + idx * lh
        tb = ly + baseline_ofs
        out.append(f"<text x=\"{gutter-8}\" y=\"{tb:.1f}\" fill=\"{LN_COLOR}\" text-anchor=\"end\" font-size=\"{fs-1}\" font-family=\'{font_family}\'>{src_ln}</text>")

    # CODE - rendered INSIDE codeClip (clips right-side overflow only)
    out.append(f'<g clip-path="url(#codeClip)">')
    for idx, (tokens, is_cont, src_ln, depth) in enumerate(display_lines):
        ly = PAD_T + idx * lh
        tb = ly + baseline_ofs
        start_x = code_x + depth * TAB_WIDTH * cw if src_ln else code_x + depth * TAB_WIDTH * cw + wrap_px
        tx = start_x
        seen_code = False
        for val, typ in tokens:
            if typ == 'space':
                if not seen_code:
                    continue  # skip leading spaces (indent handled by depth)
                for ch in val:
                    if ch == '\t':
                        col = int(round((tx - start_x) / cw))
                        ns = ((col // TAB_WIDTH) + 1) * TAB_WIDTH
                        tx = start_x + ns * cw
                    else:
                        tx += cw
            else:
                seen_code = True
                c = CO.get(typ, '#212529')
                e = val.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                out.append(f"<text x=\"{tx:.1f}\" y=\"{tb:.1f}\" fill=\"{c}\" font-size=\"{fs}\" font-family=\'{font_family}\'>{e}</text>")
                tx += len(val) * cw
    out.append('</g>')  # end codeClip

    out.append(f'<text x="{A4_W//2}" y="{A4_H-10}" text-anchor="middle" fill="#adb5bd" font-size="10" font-family="{ff_sans}">- {page_num} -</text>')
    out.append('</g></svg>')
    return '\n'.join(out)


# ===== MAIN =====
BASE = os.getcwd()
for fname in FILES:
    src = os.path.join(BASE, fname)
    if not os.path.exists(src):
        print(f'SKIP {fname}')
        continue
    with open(src, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\r\n') for l in f.readlines()]

    all_tokens = tokenize_full(lines)
    fs = compute_optimal_font(lines, FONT_SIZE, MIN_FONT_SIZE)
    fs, cw, lh, gutter, code_x, code_w, baseline_ofs = compute_layout(lines, fs)
    lpp = max(1, int(CONTENT_H / lh))

    depths = compute_indent_levels(lines, all_tokens)
    display_lines = []
    for idx, toks in enumerate(all_tokens):
        dep = depths[idx]
        # Available width accounts for depth-based indent
        avail_w = code_w - dep * TAB_WIDTH * cw
        wrapped = wrap_line_tokens(toks, avail_w, cw, WRAP_IDENT * cw)
        for i, (seg, isc) in enumerate(wrapped):
            display_lines.append((seg, isc, idx+1 if i == 0 else None, dep))

    td = len(display_lines)
    np = (td + lpp - 1) // lpp
    out_dir = os.path.join(BASE, fname + '_images')
    os.makedirs(out_dir, exist_ok=True)

    for p in range(1, np+1):
        s = (p-1) * lpp
        e = min(s + lpp, td)
        svg = gen_svg_page(display_lines[s:e], len(lines), p, np, fname,
                           FONT_KEY, fs, cw, lh, gutter, code_x, code_w, baseline_ofs)
        with open(os.path.join(out_dir, f'code_page_{p}.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)

    wraps = td - len(lines)
    print(f'{fname}: {len(lines)} src -> {td} disp ({wraps} wraps), font={fs}px, {lpp} ln/pg, {np} pgs -> SVG OK')

    js = ('const fs=require("fs");const{Resvg}=require("@resvg/resvg-js");'
          'const dir=' + json.dumps(out_dir.replace('\\','\\\\')) + ';'
          'for(let p=1;p<='+str(np)+';p++){'
          'const s=dir+"\\\\code_page_"+p+".svg";'
          'const pn=dir+"\\\\code_page_"+p+".png";'
          'try{const d=fs.readFileSync(s,"utf8");const r=new Resvg(d,{background:"#ffffff"});'
          'const b=r.render();fs.writeFileSync(pn,b.asPng())}'
          'catch(e){console.log("  ERR:"+p+" "+e.message)}}')
    subprocess.run(['node', '-e', js], check=True)
    print(f'{fname}: PNG OK')

    import img2pdf
    pngs = sorted([os.path.join(out_dir,f) for f in os.listdir(out_dir) if f.endswith('.png')],
                  key=lambda x: int(os.path.basename(x).replace('code_page_','').replace('.png','')))
    pdf_path = os.path.join(BASE, fname+'.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(img2pdf.convert(pngs))
    print(f'{fname}: PDF -> {pdf_path} ({os.path.getsize(pdf_path)//1024}KB)')

print('\n=== All done! ===')
