#!/usr/bin/env python3
"""像素级文本重叠验证器 v3.1: 三级验证闭环。

一级: 全页渲染 -> 连通分量 -> 过滤大分量(网格线/矢量图形)
二级: 分量质心归属 (质心须在某 char bbox 内才归属该 span)
三级: 候选对 600dpi 局部重渲染 -> 两 span 墨迹像素集最小欧氏距离
      (min_dist > 0.05pt 即判定为分离, 消除行高模型误报)

根因背景: PyMuPDF span/char bbox 采用字体行高模型 (Noto CJK 2.856em,
DejaVu 1.695em), 对旋转文本/堆叠标签系统性高估 (45° 时 fs=9 报 32.3pt,
真实墨迹仅 16.8pt), 导致 bbox 相交误报为重叠。
"""
import sys, fitz, numpy as np
from scipy import ndimage

MAX_COMP_AREA = 5000
INK_THRESH = 200
MIN_DIST_PT = 0.05  # 低于此即认为真实接触


def page_components(page, dpi, ink_thresh):
    """返回 (labels, comp_centers: {c: (x_pt, y_pt)}, big: set)"""
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    gray = img.mean(axis=2)
    ink = gray < ink_thresh
    labels, n = ndimage.label(ink, structure=np.ones((3,3)))
    centers = {}
    big = set()
    if n == 0:
        return labels, centers, big
    sizes = np.bincount(labels.ravel())
    # 只对尺寸合理的分量算质心 (质心坐标换算为 pt)
    sc = 72.0 / dpi
    for c in range(1, n+1):
        if sizes[c] > MAX_COMP_AREA:
            big.add(c)
            continue
        ys, xs = np.where(labels == c)
        if len(ys) < 3:
            continue
        centers[c] = (xs.mean()*sc, ys.mean()*sc)
    return labels, centers, big


def span_texts(page):
    """从 rawdict 提取 (文本, span_bbox, [char_bbox], origin) 列表"""
    spans = []
    d = page.get_text('rawdict')
    for block in d['blocks']:
        if block['type'] != 0:
            continue
        for line in block.get('lines', []):
            for s in line['spans']:
                chars = s.get('chars', [])
                txt = ''.join(ch['c'] for ch in chars).strip()
                if not txt:
                    continue
                spans.append((txt, s['bbox'], [ch['bbox'] for ch in chars],
                              tuple(chars[0]['origin'])))
    return spans


def confirm_min_dist(page, origin_a, cbboxes_a, origin_b, cbboxes_b, dpi=600):
    """第三级: 局部 600dpi 重渲染, 计算两 span 墨迹像素集最小欧氏距离 (pt)。

    归属采用"唯一归属": 分量若同时落入两 span 的候选区 (行高模型 bbox 膨胀),
    则归属给质心距 origin 最近的一方, 避免旋转 ylabel 等场景的交叉误归。
    真实重叠时跨文本分量两端连接两方专属墨迹, min_dist 仍趋近 0。
    """
    x0 = min(min(b[0] for b in cbboxes_a), min(b[0] for b in cbboxes_b)) - 4
    y0 = min(min(b[1] for b in cbboxes_a), min(b[1] for b in cbboxes_b)) - 4
    x1 = max(max(b[2] for b in cbboxes_a), max(b[2] for b in cbboxes_b)) + 4
    y1 = max(max(b[3] for b in cbboxes_a), max(b[3] for b in cbboxes_b)) + 4
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(x0, y0, x1, y1))
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    ink = img.mean(axis=2) < INK_THRESH
    labels, n = ndimage.label(ink, structure=np.ones((3,3)))
    sizes = np.bincount(labels.ravel())
    sc = 72.0 / dpi

    def candidates(origin, cbboxes, win=(-10, 2)):
        cx0 = min(b[0] for b in cbboxes) - 1
        cx1 = max(b[2] for b in cbboxes) + 1
        out = []
        for c in range(1, n+1):
            if sizes[c] > MAX_COMP_AREA:
                continue
            ys, xs = np.where(labels == c)
            if len(ys) < 3:
                continue
            cy = y0 + ys.mean()*sc
            cx = x0 + xs.mean()*sc
            if origin[1]+win[0] <= cy <= origin[1]+win[1] and cx0 <= cx <= cx1:
                out.append((c, cx, cy, ys, xs))
        return out

    ca = candidates(origin_a, cbboxes_a)
    cb = candidates(origin_b, cbboxes_b)
    if not ca or not cb:
        return None
    # 唯一归属: 冲突分量给质心距 origin 更近的一方
    def pick(cands, other):
        keep = []
        for c, cx, cy, ys, xs in cands:
            da2 = (cx-origin_a[0])**2 + (cy-origin_a[1])**2
            db2 = (cx-origin_b[0])**2 + (cy-origin_b[1])**2
            mine = da2 if origin_a is other else db2
            theirs = db2 if origin_a is other else da2
            if mine <= theirs:
                keep.append((c, ys, xs))
        return keep
    ma_comp = pick(ca, origin_b)
    mb_comp = pick(cb, origin_a)
    ma = np.zeros_like(ink, dtype=bool)
    mb = np.zeros_like(ink, dtype=bool)
    for c, ys, xs in ma_comp:
        ma[ys, xs] = True
    for c, ys, xs in mb_comp:
        mb[ys, xs] = True
    if (ma & mb).any():
        return 0.0
    if not ma.any() or not mb.any():
        return None
    da = ndimage.distance_transform_edt(~ma)[mb]
    db = ndimage.distance_transform_edt(~mb)[ma]
    return min(da.min()*sc, db.min()*sc)


def verify(pdf_path, dpi=200, ink_thresh=INK_THRESH, verbose=True, confirm=True):
    doc = fitz.open(pdf_path)
    total_pairs = candidate_pairs = real_overlaps = 0
    details = []
    for pno, page in enumerate(doc):
        labels, centers, big = page_components(page, dpi, ink_thresh)
        spans = span_texts(page)
        # 二级: 质心归属 (质心在 char bbox 膨胀1pt 内)
        comp_sets = []
        for txt, sbbox, cbboxes, origin in spans:
            owned = set()
            for c, (cx, cy) in centers.items():
                if c in big:
                    continue
                for cb in cbboxes:
                    if cb[0]-1 <= cx <= cb[2]+1 and cb[1]-1 <= cy <= cb[3]+1:
                        owned.add(c)
                        break
            comp_sets.append(owned)
        n = len(spans)
        for i in range(n):
            for j in range(i+1, n):
                total_pairs += 1
                bi, bj = spans[i][1], spans[j][1]
                inter = (min(bi[2], bj[2])-max(bi[0], bj[0])) * (min(bi[3], bj[3])-max(bi[1], bj[1]))
                if inter <= 0:
                    gap_x = max(bi[0], bj[0])-min(bi[2], bj[2]) if (bi[0] > bj[2] or bj[0] > bi[2]) else 0
                    gap_y = max(bi[1], bj[1])-min(bi[3], bj[3]) if (bi[1] > bj[3] or bj[1] > bi[3]) else 0
                    if gap_x > 2 and gap_y > 2:
                        continue
                shared = comp_sets[i] & comp_sets[j]
                if shared:
                    candidate_pairs += 1
                    if confirm:
                        dmin = confirm_min_dist(page, spans[i][3], spans[i][2],
                                                spans[j][3], spans[j][2])
                        if dmin is None or dmin > MIN_DIST_PT:
                            continue  # 三级确认分离
                    real_overlaps += 1
                    details.append((pno+1, spans[i][0][:30], spans[j][0][:30],
                                    tuple(round(v, 1) for v in bi),
                                    tuple(round(v, 1) for v in bj)))
    print(f"{pdf_path.split('/')[-1]}: 文本对={total_pairs} 候选={candidate_pairs} "
          f"真实重叠={real_overlaps}")
    for x in details[:12]:
        print(f"  p{x[0]} '{x[1]}' × '{x[2]}' bboxA={x[3]} bboxB={x[4]}")
    if len(details) > 12:
        print(f"  ... 共 {len(details)} 处")
    return real_overlaps, details


if __name__ == '__main__':
    for p in sys.argv[1:]:
        verify(p)
