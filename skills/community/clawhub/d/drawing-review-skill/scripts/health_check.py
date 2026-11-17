# -*- coding: utf-8 -*-
"""图纸转换体检单（P1~P10 一次性跑完，出报告）

用法:
    python health_check.py <待检目录> [--baseline <原DWG直转目录>] [--out 报告.md]

检查项:
    P1/P2/P3  参照可达性（所有参照逐个解析，不挑类型）
    P4        超大块（污染检测：内容是否被塞进主图）
    P5        文件可读性
    P6        内容对照（需 --baseline：实体数/图层/块/文字）
    P7        AUDIT 坏图层
    P8        实体类型分布对照（需 --baseline）
    P9        视口丢失
    P10       字体缺失
"""
import os, sys, argparse, collections, json, time
import ezdxf

GBK_FRAME = '图框'.encode('gbk')


def _has_surrogate(s):
    return any('\ud800' <= ch <= '\udfff' for ch in s)


def _repair_path(xp):
    """还原参照路径的编码。

    DXF 里中文参照路径常是 GBK（ANSI_936）字节，被按 UTF-8 解码后会变成代理字符
    （如 '\\A2图框.dxf' → '.\\A2\\u037c\\udcbf\\udcf2.dxf'）。
    这时 os.path.exists 必然返回 False，会把**大量正常参照误判成断链**。
    这里按 gb18030 → gbk → big5 依次尝试还原，还原不了就原样返回。
    返回 (路径, 是否做过编码还原)。
    """
    if not xp or not _has_surrogate(xp):
        return xp, False
    try:
        raw = xp.encode('utf-8', 'surrogateescape')
    except Exception:
        return xp, False
    for enc in ('gb18030', 'gbk', 'big5'):
        try:
            cand = raw.decode(enc)
        except Exception:
            continue
        if not _has_surrogate(cand):
            return cand, True
    return xp, False


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('--baseline', default=None)
    ap.add_argument('--out', default=None)
    return ap.parse_args()

def all_text_count(doc):
    n = 0
    for b in doc.blocks:
        for e in b:
            if e.dxftype() in ('TEXT', 'MTEXT', 'ATTRIB'): n += 1
    return n

def analyze(path, root):
    """单文件分析，返回 dict"""
    r = {'file': os.path.relpath(path, root), 'err': None}
    try:
        doc = ezdxf.readfile(path)
    except Exception as e:
        r['err'] = f'{type(e).__name__}: {str(e)[:70]}'
        return r
    d = os.path.dirname(path)

    # P1/P2/P3 参照可达性
    refs = []
    for b in doc.blocks:
        xp = b.block.dxf.get('xref_path', None)
        if not xp: continue
        if not xp.lower().endswith(('.dwg', '.dxf')): continue      # 块名不算参照
        fixed, enc_fixed = _repair_path(xp)
        real = os.path.normpath(os.path.join(d, fixed))
        ok_ = os.path.exists(real)
        note = '编码还原' if enc_fixed else ''
        how = ''
        if not ok_:
            # 同名兜底：同目录 / 上一级找同名文件（CAD 的搜索路径行为）
            base = os.path.basename(fixed.replace('\\', '/'))
            for up in (d, os.path.dirname(d)):
                cand = os.path.join(up, base)
                if os.path.exists(cand):
                    real, ok_, how = cand, True, '同名兜底'
                    break
        refs.append({'block': b.name, 'path': fixed,
                     'ok': ok_, 'inblock': len(list(b)),
                     'note': note, 'how': how})
    r['refs'] = refs
    r['ref_total'] = len(refs)
    r['ref_ok'] = sum(1 for x in refs if x['ok'])

    # P4 超大块
    big = [(b.name, len(list(b))) for b in doc.blocks
           if not b.name.startswith('*') and len(list(b)) > 5000]
    r['huge_blocks'] = big

    # P7 AUDIT 坏图层
    audit = [l.dxf.name for l in doc.layers if 'AUDIT_BAD_LAYER' in l.dxf.name.upper()]
    audit_ents = 0
    if audit:
        aset = set(audit)
        for e in doc.modelspace():
            try:
                if e.dxf.layer in aset: audit_ents += 1
            except Exception: pass
    r['audit_layers'] = audit
    r['audit_ents'] = audit_ents

    # P9 视口
    lays = []
    for l in doc.layouts:
        ents = list(l)
        vp = sum(1 for e in ents if e.dxftype() == 'VIEWPORT')
        lays.append({'name': l.name, 'ents': len(ents), 'vp': vp})
    r['layouts'] = lays

    # P10 字体
    fonts = set()
    for st in doc.styles:
        try:
            f = st.dxf.font
            if f: fonts.add(str(f))
            bf = st.dxf.get('bigfont', '')
            if bf: fonts.add(str(bf))
        except Exception: pass
    r['fonts'] = sorted(fonts)

    # P6/P8 统计
    ms = doc.modelspace()
    tc = collections.Counter(e.dxftype() for e in ms)
    r['ms_count'] = len(ms)
    r['ms_types'] = dict(tc)
    r['text_count'] = all_text_count(doc)
    r['layers'] = len(doc.layers)
    r['blocks'] = len(list(doc.blocks))
    return r

def main():
    a = get_args()
    t0 = time.time()
    files = []
    for root, _, fs in os.walk(a.target):
        for fn in fs:
            if fn.lower().endswith('.dxf'): files.append(os.path.join(root, fn))
    files.sort()
    print(f'体检对象: {a.target} ｜ {len(files)} 个 DXF', flush=True)

    results = []
    for i, p in enumerate(files, 1):
        results.append(analyze(p, a.target))
        if i % 50 == 0: print(f'  {i}/{len(files)} {time.time()-t0:.0f}s', flush=True)

    # 汇总
    S = collections.Counter()
    unreadable, ref_bad, huge, audit_hit, font_missing, vp_lost = [], [], [], [], [], []
    all_fonts = set()
    for r in results:
        if r['err']: S['不可读'] += 1; unreadable.append((r['file'], r['err'])); continue
        S['可读'] += 1
        S['参照总数'] += r['ref_total']; S['参照可达'] += r['ref_ok']
        for x in r.get('refs', []):
            if x.get('note'): S['编码还原'] += 1
            if x.get('how') == '同名兜底': S['同名兜底'] += 1
        if r['ref_total'] - r['ref_ok'] > 0:
            ref_bad.append((r['file'], r['ref_total'] - r['ref_ok'], r['ref_total']))
        if r['huge_blocks']: huge.append((r['file'], r['huge_blocks'][:2]))
        if r['audit_layers'] and r['audit_ents'] > 0:
            audit_hit.append((r['file'], r['audit_layers'][:2], r['audit_ents']))
        all_fonts.update(r['fonts'])
        for l in r['layouts']:
            if l['ents'] > 0 and l['vp'] == 0 and l['name'] != 'Model':
                vp_lost.append((r['file'], l['name'], l['ents']))

    # P10 字体检查（通用：系统字体目录 + 自动探测 CAD 字形目录；探不到就降级不判）
    import glob
    local_ttf = set()
    sys_font_dirs = []
    if os.name == 'nt':
        sys_font_dirs = [os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')]
    else:
        sys_font_dirs = ['/usr/share/fonts', os.path.expanduser('~/.fonts')]
    for d2 in sys_font_dirs:
        if os.path.isdir(d2):
            for f2 in glob.glob(os.path.join(d2, '**', '*'), recursive=True):
                if f2.lower().endswith(('.ttf', '.ttc', '.otf')):
                    local_ttf.add(os.path.splitext(os.path.basename(f2))[0].lower())

    local_shx, shx_pool = set(), 0
    roots = [os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)'),
             os.environ.get('ProgramW6432'), os.environ.get('LOCALAPPDATA')]
    keys = ('cad', 'autodesk', 'autocad', 'bricscad', 'gstar', '浩辰', '中望', 'zw')
    for r0 in filter(None, roots):
        try:
            for name in os.listdir(r0):
                if not any(k in name.lower() for k in keys): continue
                for root2, _, fs2 in os.walk(os.path.join(r0, name)):
                    for f2 in fs2:
                        if f2.lower().endswith('.shx'):
                            local_shx.add(os.path.splitext(f2)[0].lower()); shx_pool += 1
        except Exception:
            pass

    for f in sorted(all_fonts):
        base, ext = os.path.splitext(f)
        bl, el = base.lower(), ext.lower()
        if el == '.shx':
            if shx_pool and bl and bl not in local_shx:
                font_missing.append(f)              # 探到字形库，才判缺失
            # 探不到字形库 → 降级：不判定（避免误报）
        elif el in ('.ttf', '.ttc', '.otf'):
            if bl and bl not in local_ttf:
                font_missing.append(f)
    font_scan_note = ('已在本机探到 CAD 字形库（%d 个 SHX）' % shx_pool) if shx_pool \
                     else '本机未探到 CAD 字形库 → SHX 字形**未做缺失判定**（降级）'

    # P6/P8 对照
    diff_rows = []
    if a.baseline and os.path.isdir(a.baseline):
        print('对照 baseline ...', flush=True)
        base_map = {}
        for root, _, fs in os.walk(a.baseline):
            for fn in fs:
                if fn.lower().endswith('.dxf'):
                    p = os.path.join(root, fn)
                    base_map[os.path.relpath(p, a.baseline)] = p
        for r in results:
            if r['err']: continue
            bp = base_map.get(r['file'])
            if not bp: diff_rows.append((r['file'], '基线缺失', '', '')); continue
            try: bd = analyze(bp, a.baseline)
            except Exception: continue
            if bd.get('err'): diff_rows.append((r['file'], '基线不可读', '', '')); continue
            for key, label in [('ms_count', '模型实体'), ('text_count', '文字'),
                               ('layers', '图层'), ('blocks', '块')]:
                if r[key] != bd[key]:
                    diff_rows.append((r['file'], label, bd[key], r[key]))

    # 出报告
    L = []
    L.append('# 图纸转换体检报告\n')
    L.append(f'> 体检对象：`{a.target}` ｜ 共 **{len(files)}** 个 DXF ｜ 耗时 {time.time()-t0:.0f}s\n')
    L.append('## 一、结论\n')
    ok = (S['不可读'] == 0)
    L.append(f'| 项 | 结果 |\n|---|---|')
    L.append(f'| **P5 可读性** | {"✅ 全部可读" if ok else f"❌ {S[chr(19981)+chr(21487)+chr(35835)]} 个不可读"} |')
    L.append(f'| **P1~P3 参照可达** | {S["参照可达"]}/{S["参照总数"]} ｜ 有不可达的文件 **{len(ref_bad)}** 个 |')
    if S['编码还原'] or S['同名兜底']:
        L.append(f'| ↳ 其中「不是真丢，只是路径对不上」 | 中文路径编码还原 **{S["编码还原"]}** 个 ｜ 同目录同名兜底 **{S["同名兜底"]}** 个 |')
    L.append(f'| **P4 超大块(污染)** | {len(huge)} 个文件 |')
    L.append(f'| **P7 AUDIT坏图层** | {len(audit_hit)} 个文件 |')
    L.append(f'| **P9 视口异常** | {len(vp_lost)} 处 |')
    L.append(f'| **P10 字体缺失** | {len(font_missing)} 个字体 |')
    if a.baseline:
        L.append(f'| **P6 与基线差异** | {len(diff_rows)} 处（基线=修复前版本，验证「修复没改坏」） |')
    L.append('| **P8 转换丢内容** | ⚠️ **无法自动查** —— 需人眼看原 DWG（见下） |')
    L.append('')
    if unreadable:
        L.append('## P5 不可读文件\n')
        for f, e in unreadable[:30]: L.append(f'- `{f}` — {e}')
        L.append('')
    if ref_bad:
        L.append('## P1~P3 参照不可达（前 30）\n')
        L.append('| 文件 | 不可达/总数 |\n|---|---|')
        for f, b, t in ref_bad[:30]: L.append(f'| `{f[:70]}` | {b}/{t} |')
        L.append('')
    if huge:
        L.append('## P4 超大块（疑似内容被塞进主图）\n')
        for f, bs in huge[:20]:
            L.append(f'- `{f[:70]}`')
            for n, c in bs: L.append(f'    - `{n}` ({c} 实体)')
        L.append('')
    if audit_hit:
        L.append('## P7 AUDIT 坏图层（其上有实体）\n')
        for f, ls, c in audit_hit[:20]: L.append(f'- `{f[:70]}` — {ls} 共 {c} 实体')
        L.append('')
    if vp_lost:
        L.append('## P9 布局有内容但无视口\n')
        for f, l, c in vp_lost[:20]: L.append(f'- `{f[:70]}` 布局 `{l}`（{c} 实体，0 视口）')
        L.append('')
    if font_missing:
        L.append(f'## P10 本机未找到的字体\n')
        L.append(f'> 扫描说明：{font_scan_note}\n')
        for f in font_missing[:30]: L.append(f'- `{f}`')
        L.append('')
    elif all_fonts:
        L.append('## P10 字体\n')
        L.append(f'> {font_scan_note} —— 未发现缺失 ✅\n')
    if diff_rows:
        L.append('## P6/P8 与基线（原 DWG 直转）的差异（前 40）\n')
        L.append('| 文件 | 项 | 基线 | 当前 |\n|---|---|:-:|:-:|')
        for f, k, b, c in diff_rows[:40]: L.append(f'| `{f[:60]}` | {k} | {b} | {c} |')
        L.append('')

    L.append('## 说明：本体检单能查什么、不能查什么\n')
    L.append('### ✅ 能自动查（P1~P7 / P9 / P10）\n')
    L.append('| 项 | 说明 |')
    L.append('|---|---|')
    L.append('| P1~P3 参照可达性 | **所有**参照逐个解析，图框 / 总平面 / 剖面详图全查 |')
    L.append('| P4 污染检测 | 超大块 = 疑似内容被塞进主图 |')
    L.append('| P5 文件可读性 | 读不了 = 改坏了 |')
    L.append('| P6 修复无副作用 | 与「**修复前版本**」逐项对照（实体 / 文字 / 图层 / 块） |')
    L.append('| P7 AUDIT 坏图层 | 审计产生的坏图层上还有实体 |')
    L.append('| P9 视口 | 布局有内容却没有视口 |')
    L.append('| P10 字体 | 缺 TTF 字体 / 缺 SHX 字形 |')
    L.append('')
    L.append('### ⚠️ 不能自动查 —— **必须人眼看图**\n')
    L.append('| 查不了的 | 为什么 |')
    L.append('|---|---|')
    L.append('| **P8 转换本身丢内容**（代理对象 / 天正自定义对象） | 转换前后两边一样都少 → 数据比不出来。**唯一的基准是原 DWG 本身，只能人眼** |')
    L.append('| **图面看着对不对**（位置 / 比例 / 显示状态） | 数据全对也可能显示异常 |')
    L.append('| **参照文件内容对不对** | 只能验"路径指向的文件存在"，不能验"是不是原来那份" |')
    L.append('')
    L.append('> ## **⇒ 数据比对防"已知的坑"，人眼看图防"未知的坑"。两道都过，才算检查通过。**')
    L.append('>')
    L.append('> **用法（两阶段）**：测试期人手看为主、边看边给本表打补丁；交付期以本表为主、人眼抽验为辅。')

    rep = '\n'.join(L)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), '体检报告.md')
    open(out, 'w', encoding='utf-8').write(rep)
    print(f'\n=== 汇总 ===')
    for k, v in S.items(): print(f'  {k}: {v}')
    print(f'  超大块文件 {len(huge)} | AUDIT坏图层 {len(audit_hit)} | 视口异常 {len(vp_lost)} | 字体缺失 {len(font_missing)}')
    print(f'  字体扫描：{font_scan_note}')
    print(f'  报告: {out}')

if __name__ == '__main__':
    main()
