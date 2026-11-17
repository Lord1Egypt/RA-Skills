#!/usr/bin/env python3
"""
fetch_ccgp.py — ccgp.gov.cn 数据管线（stdlib only）

架构定位（重要）
================
本脚本**只做解析与落 JSON**，不做"主动取数"的主路径。

  ✅ 主路径（推荐）：由 agent 用 WebFetch / Bash(python|curl) 等工具把原始
     HTML 落盘后，本脚本用 `--html-file` / `--html-dir` / `--detail` 解析。
     —— 这样取数行为由 agent 在对话中受控发生，脚本不擅自联网。

  ⚠️ 离线补充（兜底）：`--kw` 直连 bxsearch 仍可抓，但可能因"频繁访问"
     被限流，仅用于无 agent 取数能力时的批量回填，不作为主推。

解析函数（parse_listing / parse_detail / normalize_amount）都是纯函数，
输入 HTML 字符串、输出 dict，可直接被 agent 在内存里复用，无需落盘。

用法：
  # 主路径：解析 agent 已落盘的 listing HTML
  python fetch_ccgp.py --html-file listing.html --out records.json
  python fetch_ccgp.py --html-dir ./ccgp_html/ --out records.json

  # 详情补全（agent 已落盘 detail HTML，需带原 source_url 以便合并）
  python fetch_ccgp.py --html-file listing.html \
      --detail detail_1.html::https://www.ccgp.gov.cn/cggg/.../t1.htm \
      --detail detail_2.html::https://www.ccgp.gov.cn/cggg/.../t2.htm \
      --out records.json

  # 落 JSON 后直接跑机会引擎
  python fetch_ccgp.py --html-file listing.html --profile profile.json --run

  # 离线补充（直连，可能限流）：
  python fetch_ccgp.py --kw 智慧校园 --pages 1 --details 3 \
      --profile profile.json --out records.json --run
"""

import argparse
import http.cookiejar
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = 'https://search.ccgp.gov.cn/bxsearch'
HOME = 'https://www.ccgp.gov.cn/'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
HEADERS = {'User-Agent': UA, 'Accept': 'text/html,*/*', 'Accept-Language': 'zh-CN,zh;q=0.9'}


# ---------- network helpers (离线补充用) ----------

def make_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)), cj


def warm(opener):
    try:
        opener.open(urllib.request.Request(HOME, headers=HEADERS), timeout=15)
    except Exception:
        pass


def get(opener, url):
    req = urllib.request.Request(url, headers={**HEADERS, 'Referer': HOME})
    with opener.open(req, timeout=25) as r:
        return r.read().decode('utf-8', 'ignore')


# ---------- text helpers ----------

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s or '')


def clean(s):
    return re.sub(r'\s+', ' ', strip_tags(s)).strip()


def read_text(path):
    return Path(path).read_text(encoding='utf-8', errors='ignore')


# ---------- amount normalization ----------

def normalize_amount(text):
    """'94.800000 万元' → 948000 ; '950000.00元' → 950000 ; '￥1,200万元' → 12000000"""
    if not text:
        return None
    m = re.search(r'[\d,]+\.?\d*', text)
    if not m:
        return None
    val = float(m.group().replace(',', ''))
    if '万' in text:
        val *= 10000
    return int(round(val))


# ---------- listing parser ----------

def parse_listing(html):
    items = []
    for m in re.finditer(r'<li>(.*?)</li>', html, re.S):
        blk = m.group(1)
        if 'cggg' not in blk or '采购人' not in blk:
            continue
        href = re.search(r'href="(https?://www\.ccgp\.gov\.cn/cggg/[^"]+\.htm)"', blk)
        if not href:
            continue
        url = href.group(1)
        ta = re.search(r'<a[^>]*>(.*?)</a>', blk, re.S)
        title = clean(ta.group(1)) if ta else ''
        span = re.search(r'<span>(.*?)</span>', blk, re.S)
        meta = clean(span.group(1)) if span else blk
        date = re.search(r'(\d{4}\.\d{2}\.\d{2})', meta)
        buyer = re.search(r'采购人[:：]\s*([^|]+)', meta)
        agency = re.search(r'代理机构[:：]\s*([^|<]+)', meta)
        typ = re.search(r'<strong[^>]*>\s*([^<]+?)\s*</strong>', blk)
        ann_type = clean(typ.group(1)) if typ else ''
        prov = re.search(r'</strong>\s*\|([^|]+)\|', blk)
        province = clean(prov.group(1)) if prov else ''
        items.append({
            'url': url, 'title': title,
            'publish_date': date.group(1).replace('.', '-') if date else None,
            'buyer': clean(buyer.group(1)) if buyer else None,
            'agency': clean(agency.group(1)) if agency else None,
            'ann_type': ann_type, 'province_hint': province,
        })
    return items


def map_type(ann_type):
    if '中标' in ann_type or '成交' in ann_type:
        return '中标'
    if '废标' in ann_type or '终止' in ann_type:
        return '废标'
    if '更正' in ann_type or '变更' in ann_type:
        return '变更'
    if '招标' in ann_type or '谈判' in ann_type or '磋商' in ann_type or '询价' in ann_type:
        return '招标'
    return '其他'


# ---------- detail parser ----------

def _value_after(html, keyword):
    """定位含 keyword 的 <td>，返回紧随其后的取值单元格（表头则再跳一个）。"""
    heads = {'供应商名称', '供应商地址', '中标（成交）金额', '中标金额', '成交金额',
             '评审得分', '总得分', '项目编号', '项目名称', '预算金额', '预算'}
    tds = re.findall(r'<td[^>]*>(.*?)</td>', html, re.S)
    for i, t in enumerate(tds):
        if keyword in clean(t) and i + 1 < len(tds):
            nxt = clean(tds[i + 1])
            if nxt in heads and i + 2 < len(tds):   # 紧邻仍是表头，跳过取真实值
                return clean(tds[i + 2])
            return nxt
    return None


def parse_detail(html):
    out = {'budget_amount': None, 'win_amount': None, 'win_company': None,
           'project_name': None, 'project_type': None}
    # 预算：先试正文「预算：X 元」，再试表格 label→value 单元格
    for kw in ['预算金额', '预算']:
        m = re.search(kw + r'[:：]\s*([\d,\.]+)\s*万?元', html)
        if m:
            out['budget_amount'] = normalize_amount(m.group(1) + ('万元' if '万' in m.group(0) else '元'))
            break
        val = _value_after(html, kw)
        if val:
            na = normalize_amount(val)
            if na:
                out['budget_amount'] = na
                break
    # 中标/成交金额：同上，兼容「中标（成交）金额」「总中标金额」等表头
    for kw in ['中标（成交）金额', '总中标金额', '中标金额', '总成交金额', '成交金额']:
        m = re.search(kw + r'[:：]\s*([^<]+)', html)
        if m:
            na = normalize_amount(m.group(1))
            if na:
                out['win_amount'] = na
                break
        val = _value_after(html, kw)
        if val:
            na = normalize_amount(val)
            if na:
                out['win_amount'] = na
                break
    mi = html.find('供应商名称')
    if mi > 0:
        seg = html[mi:mi + 2500]
        tds = re.findall(r'<td[^>]*>(.*?)</td>', seg, re.S)
        headers = {'供应商名称', '供应商地址', '中标（成交）金额', '中标金额',
                   '成交金额', '评审得分', '总得分', '项目编号', '项目名称'}
        suff = ('公司', '有限公司', '中心', '大学', '学院', '局', '所', '集团',
                '医院', '银行', '厂', '研究院', '事务所')
        for t in tds:
            n = clean(t)
            if len(n) < 2 or n in headers:
                continue
            if any(s in n for s in suff):
                out['win_company'] = n
                break
        if not out['win_company']:
            seg2 = re.sub(r'[^一-龥A-Za-z（）()·\.\d]', ' ',
                          strip_tags(html[mi:mi + 800]))
            for tok in re.findall(r'[一-龥A-Za-z（）()·\.\d]{4,}', seg2):
                if tok in headers:
                    continue
                if any(s in tok for s in suff):
                    out['win_company'] = tok
                    break
    mp = re.search(r'项目名称[:：]\s*([^<\n]{4,80})', html)
    if mp:
        out['project_name'] = clean(mp.group(1))
    mpt = re.search(r'采购方式[:：]\s*([^<\n]{2,20})', html)
    if mpt:
        out['project_type'] = clean(mpt.group(1))
    return out


# ---------- schema assembly ----------

DETAIL_KEYS = ('budget_amount', 'win_amount', 'win_company', 'project_name', 'project_type')


def to_record(it):
    return {
        'title': it['title'],
        'type': map_type(it['ann_type']),
        'project_name': it['title'],
        'budget_amount': None,
        'win_amount': None,
        'win_company': None,
        'buyer': it['buyer'],
        'agency': it['agency'],
        'region': it['province_hint'] or None,
        'publish_date': it['publish_date'],
        'source_url': it['url'],
        'source_platform': '中国政府采购网',
        'project_type': None,
        'content_summary': it['ann_type'],
    }


def build_records(items):
    return [to_record(it) for it in items]


def apply_detail(rec, d):
    rec.update({k: d[k] for k in DETAIL_KEYS if d[k] is not None})
    if d['project_name']:
        rec['content_summary'] = d['project_name']


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    # 主路径：解析 agent 已落盘的 HTML
    ap.add_argument('--html-file', action='append', default=[],
                    help='已用 WebFetch/工具落盘的 listing HTML（可重复）。主取数路径。')
    ap.add_argument('--html-dir', default=None,
                    help='解析该目录下所有 *.html 作为 listing（批量补充）。')
    ap.add_argument('--detail', action='append', default=[],
                    help='详情页 path::source_url（可重复），补全预算/中标/供应商。')
    # 离线补充：直连 bxsearch（可能限流，不作主推）
    ap.add_argument('--kw', default=None,
                    help='(离线补充) 直连 bxsearch 关键词；主路径请改用 --html-file')
    ap.add_argument('--pages', type=int, default=1)
    ap.add_argument('--details', type=int, default=0,
                    help='(仅离线模式) 直连抓前 N 条详情补金额/供应商')
    # 通用
    ap.add_argument('--profile', default=None)
    ap.add_argument('--out', default='records.json')
    ap.add_argument('--run', action='store_true', help='落 JSON 后直接跑机会引擎')
    args = ap.parse_args()

    items = []

    # ---- 主路径：解析落盘 HTML ----
    listing_files = list(args.html_file)
    if args.html_dir:
        listing_files += sorted(Path(args.html_dir).glob('*.html'))
    for fp in listing_files:
        try:
            got = parse_listing(read_text(fp))
        except Exception as e:
            print(f'  {fp} 解析失败: {e}', file=sys.stderr)
            continue
        print(f'{fp}: 解析到 {len(got)} 条 listing')
        items.extend(got)

    # ---- 离线补充：直连 bxsearch ----
    if args.kw:
        print('[离线模式] 直连 bxsearch（可能触发限流，主路径建议用 --html-file）', file=sys.stderr)
        opener = make_opener()[0]
        warm(opener)
        for p in range(1, args.pages + 1):
            url = (f'{BASE}?searchtype=1&page_index={p}&start_time=&end_time='
                   f'&timeType=2&searchparam=&searchchannel=0&dbselect=bidx'
                   f'&kw={urllib.parse.quote(args.kw)}&bidSort=0&pinMu=0&bidType=0'
                   f'&buyerName=&projectId=&displayZone=&zoneId=&agentName=')
            try:
                html = get(opener, url)
            except Exception as e:
                print(f'listing 抓取失败({e}); 可能触发限流，改用 --html-file', file=sys.stderr)
                break
            if '频繁访问' in html:
                print('命中 ccgp 限流页，停止。建议用 agent 的 WebFetch 取数。', file=sys.stderr)
                break
            got = parse_listing(html)
            print(f'page {p}: 解析到 {len(got)} 条')
            items.extend(got)
            time.sleep(1)

    out = build_records(items)

    # ---- 详情补全：来自落盘 HTML（--detail）----
    for d in args.detail:
        if '::' not in d:
            print(f'  --detail 格式应为 path::url: {d}', file=sys.stderr)
            continue
        fpath, src = d.split('::', 1)
        try:
            dd = parse_detail(read_text(fpath))
        except Exception as e:
            print(f'  detail 解析失败 {fpath}: {e}', file=sys.stderr)
            continue
        merged = False
        for rec in out:
            if rec['source_url'] == src:
                apply_detail(rec, dd)
                print(f'  merged {src} -> {rec["win_company"]} | 预算 {rec["budget_amount"]} | 中标 {rec["win_amount"]}')
                merged = True
                break
        if not merged:
            print(f'  no record matched {src}', file=sys.stderr)

    # ---- 详情补全：离线直连（--details，仅离线模式）----
    if args.details and args.details > 0 and args.kw:
        opener2 = make_opener()[0]
        warm(opener2)
        for i, rec in enumerate(out[:args.details]):
            try:
                dh = get(opener2, rec['source_url'])
                apply_detail(rec, parse_detail(dh))
                print(f'  detail[{i}] {rec["win_company"]} | 预算 {rec["budget_amount"]} | 中标 {rec["win_amount"]}')
            except Exception as e:
                print(f'  detail[{i}] 失败: {e}', file=sys.stderr)
            time.sleep(1.5)

    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n写入 {args.out}（{len(out)} 条）')

    if args.run:
        import subprocess
        cmd = [sys.executable, str(Path(__file__).parent / 'opportunity_engine.py'), args.out]
        if args.profile:
            cmd += ['--profile', args.profile]
        cmd += ['--output', 'opportunity_report.html']
        print('\n--- 运行机会引擎 ---')
        subprocess.run(cmd)


if __name__ == '__main__':
    main()
