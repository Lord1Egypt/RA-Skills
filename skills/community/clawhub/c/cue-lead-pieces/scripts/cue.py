#!/usr/bin/env python3
"""cue-lead-pieces: turn a company's own filings into traceable lead pieces. The agent thinks; Cue perceives.

  Parsing — primary channel is Cue Omni Reader (MCP, run by the agent); this script ingests its results:
  cue.py fetch   <dir> --cn 600606 | --us LESL [--months 12]      list filings (cninfo / SEC EDGAR public index, no download, zero credit)
  cue.py fetch   <dir> --list filings.json --company X --market CN  register filings found elsewhere (e.g. Cue data-MCP disclosure_cn)
  cue.py ingest  <dir> --omni-dir <dir>/omni                      ingest Omni results saved as <sid>.json (grounded bundle) or <sid>.md
  cue.py ingest  <dir> --omni r.json --sid SID [--kind --date --title --url]   one result; registers SID if new
  cue.py local   <dir> [SID ...]                                  FALLBACK without Cue: download + local parse (PyMuPDF / pdftotext / HTML)
  cue.py fetch   <dir> --cn 600606 --local                        list + local fallback in one step (the 0.3.x behaviour)

  Reading and checking:
  cue.py brief   <dir> [--top 10]                                 ONE call: source catalog + lead pieces + paste-ready verbatim evidence (JSON lines)
  cue.py find    <dir> <term> [<term> ...] [--max 30]             sentences containing the terms, as paste-ready evidence JSON lines
  cue.py page    <dir> <source> <pages> [<source> <pages> ...]    print pages (e.g. AR2025 54,196-198 ANN-2026-05-14-1 2), compacted
  cue.py changes <dir>  /  cue.py leads <dir> [--no-llm]           risk-sentence changes / lead pieces (brief already includes both)
  cue.py verify  <dir> (--json answer.json [--fix] | --quote Q --source S --page N)   check quotes verbatim against the source text;
                 --fix repairs answer.json in place (wrong page -> real page, edited -> the real sentence, absent/fabricated -> dropped)

Every quote Cue emits is copied by the program from the page text, never written by a model. Page = source PDF page from the Omni
grounding sidecar (or PDF page / EDGAR page break with the local fallback); text-only results fall back to ~3500-char blocks and are
labeled page_basis=block. Pure stdlib; the local fallback needs PyMuPDF or the pdftotext CLI for PDFs."""
import sys, os, re, json, time, argparse, difflib, datetime, urllib.request, urllib.parse, urllib.error, html, collections
# SEC EDGAR asks every client to identify itself ("Company Name contact@domain"); set CUE_SEC_UA to your own name and email.
UA_SEC = os.environ.get('CUE_SEC_UA', 'cue-lead-pieces research contact@example.com')
# ---------------------------------------------------------------- text utils
import unicodedata
__version__ = '0.4.35'
class CueError(Exception):
    """a user-facing error: printed as one line on stderr, exit code 2 (no traceback)"""
def nrm_map(s):
    """normalised string for matching + map to original indices: NFKC, lower-case, and NO whitespace / punctuation / table marks
    (so a quote that differs from the page only in spacing, line breaks or punctuation still counts as verbatim)"""
    out, idx = [], []
    for i, ch in enumerate(s or ''):
        for x in unicodedata.normalize('NFKC', ch).lower():
            if x.isspace() or x in '|#*' or unicodedata.category(x)[0] in 'PZS' and x not in '%': continue
            out.append(x); idx.append(i)
    return ''.join(out), idx
def nrm(s): return nrm_map(s)[0]
def jload(p, d=None):
    if not os.path.exists(p): return d
    with open(p, encoding='utf-8') as f: return json.load(f)
def jload_lenient(p):
    """answers written by agents sometimes contain unescaped double quotes inside strings; escape a quote that is not followed by , : } ]"""
    with open(p, encoding='utf-8') as f: t = f.read()
    try: return json.loads(t)
    except json.JSONDecodeError: pass
    o, ins, i = [], False, 0
    while i < len(t):
        ch = t[i]
        if ch == '\\' and ins: o.append(t[i:i + 2]); i += 2; continue
        if ch == '"':
            if not ins: ins = True
            else:
                nxt = t[i + 1:].lstrip()[:1]
                if nxt in (',', ':', '}', ']', ''): ins = False
                else: o.append('\\"'); i += 1; continue
        o.append(ch); i += 1
    return json.loads(''.join(o))
def jdump(o, p):
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f: json.dump(o, f, ensure_ascii=False, indent=1)
def get(url, headers=None, data=None, tries=4):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers or {'User-Agent': 'Mozilla/5.0'}), timeout=90) as r: return r.read()
        except urllib.error.HTTPError as e:
            if a == tries - 1 or (400 <= e.code < 500 and e.code != 429): raise   # 4xx (except rate limit) will not fix itself on retry
            time.sleep(2 * (a + 1))
        except Exception:
            if a == tries - 1: raise
            time.sleep(2 * (a + 1))
# ---------------------------------------------------------------- page extraction
def pdf_pages(path, max_pages=1000):
    try:
        import fitz
        doc = fitz.open(path)
        try: return [doc[i].get_text() for i in range(min(doc.page_count, max_pages))]
        finally: doc.close()
    except ImportError:
        import subprocess
        t = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout.split('\f')
        if len(t) > 1 and not t[-1].strip(): t = t[:-1]            # pdftotext ends with a form feed: no extra empty page
        return t[:max_pages]
class _Txt(__import__('html.parser').parser.HTMLParser):
    BLOCK = {'p', 'div', 'br', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'table', 'hr'}
    def __init__(s): super().__init__(); s.o = []; s.skip = 0
    def handle_starttag(s, t, a):
        if t in ('script', 'style'): s.skip += 1
        if t in s.BLOCK: s.o.append('\n')
        if t in ('td', 'th'): s.o.append(' | ')
    def handle_endtag(s, t):
        if t in ('script', 'style'): s.skip -= 1
        if t in s.BLOCK: s.o.append('\n')
    def handle_data(s, d):
        if not s.skip: s.o.append(d)
def html_text(h):
    p = _Txt(); p.feed(h); t = ''.join(p.o).replace('\xa0', ' ')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\s*\n(\s*\|\s*\n)+\s*', ' | ', t)          # table cells split over lines -> one row
    return re.sub(r'\n\s*\n+', '\n', t).strip()
def html_pages(h):
    h = re.sub(r'(?is)<ix:header>.*?</ix:header>', '', h)
    parts = re.split(r'(?i)<[^>]+page-break-(?:before|after)\s*:\s*always[^>]*>', h)
    pages = [html_text(x) for x in parts]
    pages = [x for x in pages if len(x) > 40]
    if len(pages) < 3 and sum(map(len, pages)) > 8000:      # no usable page breaks: fixed blocks at paragraph boundaries
        t = '\n'.join(pages); pages, cur = [], ''
        for para in t.split('\n'):
            if len(cur) + len(para) > 3500 and cur: pages.append(cur); cur = ''
            cur += para + '\n'
        if cur: pages.append(cur)
    return pages
# ---------------------------------------------------------------- fetch: cninfo (A-share)
CN_KEEP = ['诉讼', '仲裁', '冻结', '查封', '拍卖', '执行', '立案', '处罚', '警示', '监管', '关注函', '问询函', '逾期', '违约', '资金占用', '退市', '风险提示',
           '更正', '差错', '减值', '质押', '担保', '辞职', '会计师事务所', '破产', '重整', '失信', '债务', '保留意见', '无法表示', '强调事项', '业绩预告',
           '业绩快报', '亏损', '控制权', '减持', '停牌', '出售', '借款', '贷款', '展期', '终止', '持续经营', '回复']
CN_DROP = re.compile(r'已取消|英文|English|法律意见书|股东大会的通知|召开.{0,12}股东大会|股东大会决议|章程|议事规则|管理制度|工作细则|摘要')
def cn_fetch(d, code, months, download=True):
    stocks = json.loads(get('http://www.cninfo.com.cn/new/data/szse_stock.json'))['stockList']
    org = next((x for x in stocks if x['code'] == code), None)
    if org is None: raise CueError(f"unknown A-share code '{code}': not in the cninfo stock list (use the 6-digit code, e.g. 600606)")
    end = datetime.date.today(); start = end - datetime.timedelta(days=int(months * 30.5)); ar_start = end - datetime.timedelta(days=800)
    def query(s, e, category=''):
        out, page = [], 1
        while True:
            body = urllib.parse.urlencode({'pageNum': page, 'pageSize': 30, 'column': 'sse' if code.startswith('6') else 'szse', 'tabName': 'fulltext',
                                           'stock': f"{code},{org['orgId']}", 'category': category, 'seDate': f'{s}~{e}', 'isHLtitle': 'true'}).encode()
            r = json.loads(get('http://www.cninfo.com.cn/new/hisAnnouncement/query', data=body, headers={'User-Agent': 'Mozilla/5.0', 'X-Requested-With': 'XMLHttpRequest',
                                                                                                          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}))
            for a in r.get('announcements') or []:
                out.append({'id': str(a['announcementId']), 'title': re.sub('</?em>', '', a['announcementTitle'] or ''), 'url': a['adjunctUrl'],
                            'date': datetime.datetime.fromtimestamp(a['announcementTime'] / 1000, datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()})
            if not r.get('hasMore'): return out
            page += 1; time.sleep(0.4)
    srcs = []
    per = query(ar_start, end, 'category_ndbg_szsh;category_bndbg_szsh')
    ars = sorted([a for a in per if re.search(r'年度报告$|年度报告（更新后）$|年度报告\(修订版\)$', a['title']) and '半年度' not in a['title'] and '摘要' not in a['title']], key=lambda a: a['date'], reverse=True)
    hs = sorted([a for a in per if '半年度报告' in a['title'] and '摘要' not in a['title']], key=lambda a: a['date'], reverse=True)
    seen = set()
    for a in ars:
        y = re.search(r'(20\d\d)年', a['title']); y = y.group(1) if y else a['date'][:4]
        if y in seen or len(seen) >= 2: continue
        seen.add(y); srcs.append(dict(a, sid=f'AR{y}', kind='annual'))
    for a in hs[:1]:
        y = re.search(r'(20\d\d)年', a['title']); srcs.append(dict(a, sid=f"H{y.group(1) if y else a['date'][:4]}", kind='interim'))
    anns = [a for a in query(start, end) if not CN_DROP.search(a['title']) and any(k in a['title'] for k in CN_KEEP)
            and not re.search(r'年度报告|季度报告', a['title']) or re.search(r'年度报告.*(问询|更正|延期|专项说明)', a['title'])]
    anns = sorted(anns, key=lambda a: a['date'], reverse=True)[:30]
    cnt = collections.Counter()
    for a in sorted(anns, key=lambda a: (a['date'], a['id'])):
        cnt[a['date']] += 1; srcs.append(dict(a, sid=f"ANN-{a['date']}-{cnt[a['date']]}", kind='announcement'))
    for s in srcs:
        s['source_url'] = 'http://static.cninfo.com.cn/' + s.pop('url'); s['ann_id'] = s.pop('id')
        if download: s['pages'] = local_pages(d, s)
    return {'company': org['zwjc'], 'id': code, 'market': 'CN'}, srcs
# ---------------------------------------------------------------- fetch: SEC EDGAR (US)
def us_fetch(d, ticker, months, download=True):
    H = {'User-Agent': UA_SEC}
    if ticker.isdigit(): cik = int(ticker); name = ticker
    else:
        m = next((v for v in json.loads(get('https://www.sec.gov/files/company_tickers.json', H)).values() if v['ticker'].upper() == ticker.upper()), None)
        if m is None: raise CueError(f"unknown US ticker '{ticker}': not in the SEC EDGAR ticker list (use the ticker, e.g. LESL, or the numeric CIK)")
        cik, name = m['cik_str'], m['title']
    try: sub = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json', H))
    except urllib.error.HTTPError as e:
        if e.code == 404: raise CueError(f"unknown CIK '{ticker}': SEC EDGAR has no filings index for it (use the ticker, e.g. LESL, or a valid CIK)")
        raise
    r = sub['filings']['recent']
    F = [dict(form=r['form'][i], date=r['filingDate'][i], acc=r['accessionNumber'][i], doc=r['primaryDocument'][i], period=r['reportDate'][i]) for i in range(len(r['form']))]
    start = (datetime.date.today() - datetime.timedelta(days=int(months * 30.5))).isoformat()
    pick = [f for f in F if f['form'] == '10-K'][:2] + [f for f in F if f['form'] == '10-Q'][:2] + [f for f in F if f['form'] == '8-K' and f['date'] >= start][:15]
    srcs, cnt = [], collections.Counter()
    for f in pick:
        base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{f['acc'].replace('-', '')}"
        sid = {'10-K': f"10-K_FY{f['period'][:4]}", '10-Q': f"10-Q_{f['period']}"}.get(f['form'])
        if not sid: cnt[f['date']] += 1; sid = f"8-K_{f['date']}" + (f"_{cnt[f['date']]}" if cnt[f['date']] > 1 else '')
        docs = [(sid, f['doc'])]
        if f['form'] == '8-K':
            try:
                idx = json.loads(get(base + '/index.json', H))['directory']['item']
                docs += [(f'{sid}_EX99' + (str(j) if j else ''), it['name']) for j, it in enumerate([x for x in idx if re.search(r'ex-?99', x['name'], re.I) and x['name'].endswith('.htm')][:2])]
            except Exception: pass
        for s2, doc in docs:
            x = {'sid': s2, 'kind': {'10-K': 'annual', '10-Q': 'interim'}.get(f['form'], 'event'), 'date': f['date'], 'title': f"{f['form']} {doc}", 'source_url': f'{base}/{doc}'}
            if download: x['pages'] = local_pages(d, x)
            srcs.append(x)
    return {'company': name, 'id': ticker, 'cik': cik, 'market': 'US'}, srcs
def local_pages(d, s):
    """local fallback parser (no Cue channel): download the filing and extract per-page text with PyMuPDF / pdftotext (PDF) or HTML page breaks"""
    url = s['source_url']; ext = '.pdf' if url.lower().endswith('.pdf') else '.htm'; p = f"{d}/raw/{s['sid']}{ext}"
    if not os.path.exists(p):
        os.makedirs(f'{d}/raw', exist_ok=True)
        with open(p, 'wb') as f: f.write(get(url, {'User-Agent': UA_SEC} if 'sec.gov' in url else None))
        time.sleep(0.3)
    if ext == '.pdf': return pdf_pages(p)
    with open(p, encoding='utf-8', errors='ignore') as f: return html_pages(f.read())
def write_source(d, meta, s, pages, parser, basis, warnings=()):
    """write pages/<sid>.jsonl + docs/<sid>.txt for one source and update its entry in sources.json"""
    os.makedirs(f'{d}/pages', exist_ok=True); os.makedirs(f'{d}/docs', exist_ok=True)
    mark = '第{}页' if meta.get('market') == 'CN' else 'page {}'
    with open(f"{d}/pages/{s['sid']}.jsonl", 'w', encoding='utf-8') as f:
        for i, t in enumerate(pages, 1): f.write(json.dumps({'page': i, 'text': t}, ensure_ascii=False) + '\n')
    with open(f"{d}/docs/{s['sid']}.txt", 'w', encoding='utf-8') as f:
        f.write(f"# {s['sid']} | {s.get('date', '')} | {s.get('title', '')} | parser={parser} page_basis={basis}\n")
        for i, t in enumerate(pages, 1): f.write(f"\n[{mark.format(i)}]\n{t}\n")
    s.update(n_pages=len(pages), parser=parser, page_basis=basis, parsed=datetime.date.today().isoformat())
    if warnings: s['parse_warnings'] = list(warnings)
    else: s.pop('parse_warnings', None)
def save_meta(d, meta):
    jdump(meta, f'{d}/sources.json'); os.makedirs(f'{d}/docs', exist_ok=True); jdump(meta, f'{d}/docs/sources.json')
    for c in ('changes.json', 'leads.json'):                    # sources changed: cached changes / lead pieces are stale
        if os.path.exists(f'{d}/{c}'): os.remove(f'{d}/{c}')
def print_pending(d, meta):
    P = [s for s in meta['sources'] if s.get('parser', 'pending') == 'pending']
    if not P: return
    print(f"\n{len(P)} source(s) not parsed yet. Primary path — Cue Omni Reader (ask the user before spending credits):")
    print(f"  cue.py omni {d}            (prints the plan; after the user agrees: cue.py omni {d} --yes)")
    print(f"  or parse(source=<url>, detail=\"grounded\") yourself, save the completed JSON (structuredContent) to {d}/omni/<sid>.json, then: cue.py ingest {d} --omni-dir {d}/omni")
    print(f"  fallback without Cue (local parser, labeled parser=local): cue.py local {d}")
    for s in P: print(f"  {s['sid']}\t{s.get('kind', '')}\t{s.get('date', '')}\t{s.get('source_url', '')}")
def cmd_fetch(a):
    if a.list:
        if not (a.company and a.market): raise CueError('--list needs --company and --market (CN or US)')
        L = jload(a.list); L = L.get('sources', L) if isinstance(L, dict) else L
        meta = jload(f'{a.dir}/sources.json') if os.path.exists(f'{a.dir}/sources.json') else {'company': a.company, 'id': a.id or a.company, 'market': a.market.upper(), 'sources': []}
        have = {s['sid'] for s in meta['sources']}
        for x in L:
            miss = [k for k in ('sid', 'kind', 'date', 'title', 'source_url') if not x.get(k)]
            if miss: raise CueError(f"list entry {x.get('sid', '?')}: missing {', '.join(miss)} (each entry needs sid, kind, date, title, source_url)")
            if x['sid'] not in have: meta['sources'].append(dict(x, n_pages=0, parser='pending')); have.add(x['sid'])
        meta['fetched'] = datetime.date.today().isoformat(); os.makedirs(a.dir, exist_ok=True); save_meta(a.dir, meta)
        print(f"{meta['company']}: {len(meta['sources'])} sources registered -> {a.dir}/sources.json"); print_pending(a.dir, meta); return
    if not (a.cn or a.us): raise CueError('fetch needs --cn CODE, --us TICKER or --list FILE')
    meta, srcs = cn_fetch(a.dir, a.cn, a.months, download=a.local) if a.cn else us_fetch(a.dir, a.us, a.months, download=a.local)
    meta['fetched'] = datetime.date.today().isoformat(); meta['sources'] = srcs; os.makedirs(a.dir, exist_ok=True)
    for s in srcs:
        if a.local: write_source(a.dir, meta, s, s.pop('pages'), 'local', 'pdf_page' if s['source_url'].lower().endswith('.pdf') else 'html_page_break')
        else: s.update(n_pages=0, parser='pending')
    save_meta(a.dir, meta)
    print(f"{meta['company']}: {len(srcs)} sources, {sum(s['n_pages'] for s in srcs)} pages parsed -> {a.dir}/sources.json"); print_pending(a.dir, meta)
def cmd_local(a):
    meta = jload(f'{a.dir}/sources.json'); n = 0
    for s in meta['sources']:
        if (a.sids and s['sid'] not in a.sids) or (not a.sids and s.get('parser', 'pending') != 'pending'): continue
        write_source(a.dir, meta, s, local_pages(a.dir, s), 'local', 'pdf_page' if s['source_url'].lower().endswith('.pdf') else 'html_page_break'); n += 1
        print(f"{s['sid']}: {s['n_pages']} pages (parser=local)")
    save_meta(a.dir, meta); print(f'{n} source(s) parsed locally'); print_pending(a.dir, meta)
# ---------------------------------------------------------------- ingest: Cue Omni Reader results
PAGE_MARK = re.compile(r'(?im)^[ \t]*(?:<!--\s*page[:\s]*(\d+)\s*-->|\[(?:第\s*(\d+)\s*页|page\s+(\d+))\])[ \t]*$')
def text_pages(t):
    """Markdown/text without grounding: split on form feeds or explicit page markers; else ~3500-char blocks (page_basis=block)"""
    if '\f' in t: return t.split('\f'), 'form_feed'
    ms = list(PAGE_MARK.finditer(t))
    if ms:
        pages = {}
        for i, m in enumerate(ms):
            p = int(next(g for g in m.groups() if g)); end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
            pages[p] = pages.get(p, '') + t[m.end():end].strip('\n')
        return [pages.get(i, '') for i in range(1, max(pages) + 1)], 'marker'
    out, cur = [], ''
    for para in t.split('\n'):
        if len(cur) + len(para) > 3500 and cur: out.append(cur); cur = ''
        cur += para + '\n'
    if cur: out.append(cur)
    return out, 'block'
def _find(o, pred):
    if pred(o): return o
    if isinstance(o, dict): it = o.values()
    elif isinstance(o, list): it = o
    else: return None
    for v in it:
        x = _find(v, pred)
        if x is not None: return x
    return None
def bundle_pages(b):
    """omni.result_bundle.v1 (detail=grounded|layout): map each segment's UTF-8 byte range to its source PDF page anchor"""
    text = b['content']['text']; tb = text.encode('utf-8'); g = b.get('grounding', {}).get('value', {}) or {}
    warn, pages, last, cond = [], {}, None, False
    segs = sorted(g.get('segments') or [], key=lambda x: x.get('content_range_utf8', {}).get('start', 0))
    def anchor_page(sg):
        nonlocal cond
        A = (sg.get('grounding') or {}).get('anchors') or []
        P = [x['value'] for x in A if x.get('kind') == 'page' and x.get('basis') == 'source_pdf_page_1_based']
        if not P:
            P = [x['value'] for x in A if x.get('kind') == 'page' and x.get('basis') == 'rendered_pdf_page_1_based']; cond = cond or bool(P)
        return min(P) if P else None
    if not any(anchor_page(sg) for sg in segs):
        p, basis = text_pages(text); return p, basis, ['no page anchors in the grounding sidecar; split as ' + basis]
    pos = 0
    for sg in segs:
        rg = sg.get('content_range_utf8') or {}; st, en = rg.get('start', pos), rg.get('end', pos)
        p = anchor_page(sg) or last or 1
        if st > pos: pages[last or p] = pages.get(last or p, '') + tb[pos:st].decode('utf-8', 'ignore')   # uncovered gap -> previous page
        pages[p] = pages.get(p, '') + tb[st:en].decode('utf-8', 'ignore'); last, pos = p, max(pos, en)
    if pos < len(tb): pages[last] = pages.get(last, '') + tb[pos:].decode('utf-8', 'ignore')
    doc = g.get('document') or {}
    for x in doc.get('incomplete') or []: warn.append(f"incomplete {x.get('kind', '')} {x.get('values', '')} ({x.get('reason', '')})")
    for x in doc.get('truncated') or []: warn.append(f"truncated {x.get('count', '')} {x.get('kind', '')}(s) ({x.get('reason', '')})")
    if cond: warn.append('some pages use rendered_pdf_page anchors (conditional reliability)')
    return [pages.get(i, '') for i in range(1, max(pages) + 1)], 'pdf_page', warn
# Bridge = the official Cue Omni Reader MCP server (stdio). Used for (a) Bridge-local reads of artifact results (read_result:
# no credits, no key) and (b) the `omni` command's parse calls. The Bridge reads CUE_API_KEY from its own environment or launcher;
# this script never reads, prints or passes the key itself.
BRIDGE_DEFAULT = 'npx -y @cueai/omni-reader-mcp@1.8.6'
class Bridge:
    def __init__(self, cmd=None):
        import subprocess, shlex, threading, queue
        cmd = cmd or os.environ.get('CUE_OMNI_BRIDGE') or BRIDGE_DEFAULT
        try: self.p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
        except OSError as e: raise CueError(f'cannot start the Omni Bridge ({cmd.split()[0]}): {e.strerror}; set CUE_OMNI_BRIDGE to your omni-reader MCP command')
        self.q, self.i = queue.Queue(), 0
        threading.Thread(target=lambda: [self.q.put(l) for l in self.p.stdout], daemon=True).start()
        self.rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'cue-lead-pieces', 'version': __version__}}, 240)
        self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n'); self.p.stdin.flush()
    def rpc(self, method, params, timeout=300):
        import queue
        self.i += 1; self.p.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': self.i, 'method': method, 'params': params}) + '\n'); self.p.stdin.flush()
        end = time.time() + timeout
        while time.time() < end:
            try: line = self.q.get(timeout=2)
            except queue.Empty:
                if self.p.poll() is not None: raise CueError('the Omni Bridge exited (check CUE_OMNI_BRIDGE and run its `doctor --json`)')
                continue
            try: m = json.loads(line)
            except ValueError: continue
            if m.get('id') == self.i:
                if 'error' in m: raise CueError(f"Omni Bridge {method}: {m['error'].get('message', m['error'])}")
                return m.get('result') or {}
        raise CueError(f'Omni Bridge {method}: no answer within {timeout}s')
    def tool(self, name, args, timeout=300):
        r = self.rpc('tools/call', {'name': name, 'arguments': args}, timeout)
        if isinstance(r.get('structuredContent'), dict): return r['structuredContent']
        for c in r.get('content') or []:
            try: return json.loads(c.get('text', ''))
            except ValueError: return {'status': 'completed', 'result': {'kind': 'inline', 'text': c.get('text', '')}}
        return r
    def close(self):
        try: self.p.stdin.close(); self.p.terminate(); self.p.wait(10)
        except Exception: pass
def omni_response(o):
    """the parse / get_parse_status body inside whatever was saved: a full tools/call response, its structuredContent, or the compact
    JSON from content[0].text (what the agent sees when the result is an artifact)"""
    if isinstance(o, dict) and isinstance(o.get('result'), dict) and ('structuredContent' in o['result'] or 'content' in o['result']) and 'jsonrpc' in o: o = o['result']
    if isinstance(o, dict) and isinstance(o.get('structuredContent'), dict): return o['structuredContent']
    if isinstance(o, dict) and isinstance(o.get('content'), list) and 'status' not in o:
        for c in o['content']:
            try: return json.loads(c.get('text', ''))
            except (ValueError, AttributeError): return {'status': 'completed', 'result': {'kind': 'inline', 'text': c.get('text', '')}}
    return o
def bundle_from_response(b, bridge=None):
    """real Bridge shape (1.8.x): result = {kind: bundle, bundle_protocol_version: omni.result_bundle.v1, parts: {content, grounding}};
    each part's storage is inline (text / value) or artifact (next_cursor -> Bridge-local read_result, no credits)"""
    res = b.get('result') or {}; parts = res.get('parts') or {}; out = {}
    for name in ('content', 'grounding'):
        st = (parts.get(name) or {}).get('storage') or {}
        if st.get('kind') == 'inline': out[name] = st.get('text') if 'text' in st else st.get('value')
        elif st.get('kind') == 'artifact':
            own = bridge is None; br = bridge or Bridge(); buf, cur = [], st.get('next_cursor')
            try:
                while cur:
                    r = br.tool('read_result', {'result_id': res['result_id'], 'cursor': cur, 'max_bytes': 65536}, 120)
                    if r.get('status') != 'completed': raise CueError(f"read_result({name}) {r.get('status')}: {(r.get('error') or {}).get('code', '')} — the local result may have expired (see expires_at); re-parsing may be billed, ask first")
                    rr = r.get('result') or {}; buf.append(rr.get('text') or ''); cur = rr.get('next_cursor')
            finally:
                if own: br.close()
            out[name] = ''.join(buf) if name == 'content' else json.loads(''.join(buf))
    if not isinstance(out.get('content'), str): raise CueError('Omni result has no content part')
    dg = (parts.get('content') or {}).get('digest', '')
    if dg.startswith('sha256:'):
        import hashlib
        if hashlib.sha256(out['content'].encode('utf-8')).hexdigest() != dg[7:]: raise CueError('Omni content does not match its sha256 digest (incomplete read?); not ingested')
    return {'protocol_version': res.get('bundle_protocol_version', 'omni.result_bundle.v1'), 'detail': res.get('detail', 'grounded'),
            'content': {'text': out['content']}, 'grounding': {'value': out.get('grounding') or {}}}
def html_tables_to_rows(t):
    """Omni emits complex tables (rowspan/colspan) as inline HTML: keep cell text as pipe rows so quotes and verify see the cells, not tags"""
    if '<t' not in t: return t
    t = re.sub(r'(?i)</t[dh]>\s*<t[dh][^>]*>', ' | ', t); t = re.sub(r'(?i)<tr[^>]*>', '\n| ', t); t = re.sub(r'(?i)</tr>', ' |', t)
    return html.unescape(re.sub(r'(?i)</?(?:table|tbody|thead|tfoot|td|th|caption|colgroup|col)[^>]*>', '', t))
def omni_pages(path, bridge=None):
    p, parser, basis, w = _omni_pages(path, bridge); return [html_tables_to_rows(x) for x in p], parser, basis, w
def _omni_pages(path, bridge=None):
    with open(path, 'rb') as f: raw = f.read().decode('utf-8', 'ignore')
    if not path.lower().endswith('.json'):
        p, basis = text_pages(raw); return p, 'omni-text', basis, ['text-only result (no grounding sidecar); page numbers are ' + basis] if basis == 'block' else []
    try: o = json.loads(raw)
    except ValueError: raise CueError(f'{path}: not valid JSON (save the Omni result as .json, or as .md for plain Markdown)')
    b = omni_response(o)
    if isinstance(b, dict) and b.get('status') not in (None, 'completed'):
        raise CueError(f"{path}: Omni status is {b.get('status')} ({(b.get('error') or {}).get('code', '')}); nothing to ingest — use `cue.py local` for this source")
    if isinstance(b, dict) and (b.get('result') or {}).get('kind') == 'bundle':
        bb = bundle_from_response(b, bridge); p, basis, w = bundle_pages(bb); return p, 'omni-' + bb['detail'], basis, w
    full = _find(o, lambda x: isinstance(x, dict) and x.get('protocol_version') == 'omni.result_bundle.v1')   # canonical bundle bytes
    if full: p, basis, w = bundle_pages(full); return p, 'omni-' + full.get('detail', 'grounded'), basis, w
    t = _find(b, lambda x: isinstance(x, dict) and isinstance(x.get('text'), str) and len(x['text']) > 0)
    if t is None: raise CueError(f'{path}: no Omni result text found (expected a completed parse result or an omni.result_bundle.v1 bundle)')
    p, basis = text_pages(t['text']); return p, 'omni-text', basis, ['text-only result (no grounding sidecar); page numbers are ' + basis] if basis == 'block' else []
def cmd_omni(a):
    """parse pending sources through the user's Omni Bridge (grounded), save each response to DIR/omni/<sid>.json, then ingest"""
    meta = jload(f'{a.dir}/sources.json'); by = {s['sid']: s for s in meta['sources']}
    todo = [by[k] for k in a.sids if k in by] if a.sids else [s for s in meta['sources'] if s.get('parser', 'pending') == 'pending']
    bad = [k for k in a.sids if k not in by]
    if bad: raise CueError(f"not in sources.json: {', '.join(bad)}")
    todo = [s for s in todo if re.match(r'https?://', s.get('source_url') or '')]
    if not a.sids:          # measured 2026-10-07: Omni answered SOURCE_ACCESS_DENIED (not billed) for an SEC EDGAR URL -> EDGAR stays on `local`
        sec = [s for s in todo if 'sec.gov' in s['source_url']]; todo = [s for s in todo if s not in sec]
        if sec: print(f"{len(sec)} SEC EDGAR source(s) skipped (Omni cannot fetch EDGAR URLs today): cue.py local {a.dir}")
    kinds = collections.Counter(s.get('kind', '') for s in todo)
    print(f"{len(todo)} source(s) to parse with Cue Omni Reader (detail={a.detail}): " + ', '.join(f'{v} {k}' for k, v in kinds.items()))
    if not a.yes:
        print('Omni parsing is billed per source. Ask the user, then re-run with --yes (or pass only some SIDs).'); return 3
    os.makedirs(f'{a.dir}/omni', exist_ok=True); br = Bridge(); total = 0.0; ok = []
    try:
        for s in todo:
            b = br.tool('parse', {'source': s['source_url'], 'detail': a.detail, 'result_delivery': 'artifact'}, 900)
            while b.get('status') == 'processing':
                b = br.tool('get_parse_status', {'operation_id': b['operation_id'], 'wait_ms': 20000}, 120)
            bill = b.get('billing') or {}; total += float(bill.get('credits_charged') or 0)
            jdump(b, f"{a.dir}/omni/{s['sid']}.json")
            if b.get('status') == 'completed':
                ok.append(s['sid']); print(f"{s['sid']}: completed, credits_charged={bill.get('credits_charged')}")
            else:
                e = b.get('error') or {}; print(f"{s['sid']}: {b.get('status')} {e.get('code', '')} billed={e.get('billed')} — left pending; use `cue.py local {a.dir} {s['sid']}`")
                os.remove(f"{a.dir}/omni/{s['sid']}.json")
        for sid in ok:
            pages, parser, basis, warn = omni_pages(f'{a.dir}/omni/{sid}.json', br)
            write_source(a.dir, meta, by[sid], pages, parser, basis, warn)
            print(f"{sid}: {len(pages)} pages (parser={parser}, page_basis={basis})" + ''.join(f"\n  warning: {w}" for w in warn))
    finally: br.close()
    save_meta(a.dir, meta); print(f'credits charged in total (as reported by Omni): {round(total, 4)}'); print_pending(a.dir, meta)
def cmd_ingest(a):
    if os.path.exists(f'{a.dir}/sources.json'): meta = jload(f'{a.dir}/sources.json')
    elif a.company and a.market: meta = {'company': a.company, 'id': a.id or a.company, 'market': a.market.upper(), 'sources': []}
    else: raise CueError(f'{a.dir}/sources.json not found: run fetch first, or pass --company and --market to start a new directory')
    by = {s['sid']: s for s in meta['sources']}; jobs = []
    if a.omni_dir:
        for fn in sorted(os.listdir(a.omni_dir)):
            sid, ext = os.path.splitext(fn)
            if ext.lower() in ('.json', '.md', '.txt') and sid in by: jobs.append((sid, os.path.join(a.omni_dir, fn)))
        if not jobs: raise CueError(f'{a.omni_dir}: no files named <sid>.json / <sid>.md matching a source in sources.json')
    elif a.omni and a.sid:
        if a.sid not in by:
            miss = [k for k in ('kind', 'date', 'title') if not getattr(a, k)]
            if miss: raise CueError(f"source '{a.sid}' is not in sources.json: pass --{' --'.join(miss)} (and --url) to register it")
            by[a.sid] = {'sid': a.sid, 'kind': a.kind, 'date': a.date, 'title': a.title, 'source_url': a.url or ''}; meta['sources'].append(by[a.sid])
        jobs.append((a.sid, a.omni))
    else: raise CueError('ingest needs --omni FILE --sid SID, or --omni-dir DIR')
    os.makedirs(a.dir, exist_ok=True)
    for sid, path in jobs:
        pages, parser, basis, warn = omni_pages(path)
        write_source(a.dir, meta, by[sid], pages, parser, basis, warn)
        print(f"{sid}: {len(pages)} pages (parser={parser}, page_basis={basis})" + ''.join(f"\n  warning: {w}" for w in warn))
    save_meta(a.dir, meta); print_pending(a.dir, meta)
def load(d):
    meta = jload(f'{d}/sources.json'); S = collections.OrderedDict()
    for s in meta['sources']:
        p = f"{d}/pages/{s['sid']}.jsonl"
        pages = {}
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for l in f: pages[json.loads(l)['page']] = json.loads(l)['text']
        S[s['sid']] = dict(s, text=pages)
    return meta, S
_NC = {}
def normpage(k, p, t):
    if (k, p) not in _NC: _NC[(k, p)] = nrm_map(t)
    return _NC[(k, p)]
# ---------------------------------------------------------------- changes
RISK_CN = ['逾期', '违约', '冻结', '查封', '诉讼', '仲裁', '担保', '持续经营', '重大不确定性', '减值', '亏损', '立案', '处罚', '警示', '问询', '退市', '质押',
           '资金占用', '无法表示', '保留意见', '强调事项', '流动负债', '债务', '重整', '破产', '失信', '被执行', '展期', '停产', '贷款', '借款', '偿还', '净资产为负', '受限']
RISK_EN = ['going concern', 'substantial doubt', 'default', 'forbearance', 'waiver', 'covenant', 'accelerat', 'impairment', 'material weakness', 'restat',
           'delist', 'minimum bid', 'nasdaq', 'liquidity', 'matur', 'refinanc', 'bankruptcy', 'chapter 11', 'restructur', 'workforce', 'net loss',
           'cash runway', 'deficit', 'insufficient', 'unable to', 'termination', 'lender', 'interest payment']
def sentences(text, cn):
    t = text.replace('\r', '')
    if cn:
        t = re.sub(r'(?<=[\u4e00-\u9fff，、；：（）0-9%])\n(?=[\u4e00-\u9fff（0-9])', '', t)
        parts = re.split(r'(?<=[。；！？])|\n', t)
    else:
        t = re.sub(r'(?<![.:;])\n(?=[a-z0-9(])', ' ', t)
        parts = re.split(r'(?<=[.;])\s+(?=[A-Z(“"])|\n', t)
    return [p.strip() for p in parts if 25 <= len(p.strip()) <= 600]
def risk_hits(s, cn):
    sl = s.lower(); return [k for k in (RISK_CN if cn else RISK_EN) if k in sl]
def cmd_changes(a):
    meta, S = load(a.dir); cn = meta['market'] == 'CN'; ch = []
    def sents(sid): return [(p, s) for p, t in S[sid]['text'].items() for s in sentences(t, cn) if risk_hits(s, cn)]
    for kind in ('annual', 'interim'):
        ids = sorted([sid for sid, s in S.items() if s['kind'] == kind], key=lambda x: S[x]['date'], reverse=True)
        if not ids: continue
        new = sents(ids[0])
        if len(ids) >= 2:     # cross-period: wording present in the latest but not in the previous report of the same kind (and vice versa)
            old = sents(ids[1]); oldn = {nrm(s) for _, s in old}; newn = {nrm(s) for _, s in new}
            oldtxt = nrm(''.join(S[ids[1]]['text'].values())); newtxt = nrm(''.join(S[ids[0]]['text'].values()))
            for p, s in new:
                if nrm(s) not in oldn and nrm(s) not in oldtxt:
                    best = max(old, key=lambda x: difflib.SequenceMatcher(None, nrm(s)[:200], nrm(x[1])[:200]).quick_ratio(), default=None)
                    prior = None
                    if best:
                        r = difflib.SequenceMatcher(None, nrm(s)[:300], nrm(best[1])[:300]).ratio()
                        if r >= 0.55: prior = {'source': ids[1], 'date': S[ids[1]]['date'], 'page': best[0], 'quote': best[1], 'similarity': round(r, 2)}
                    ch.append({'status': 'new_wording', 'source': ids[0], 'date': S[ids[0]]['date'], 'page': p, 'quote': s, 'prior': prior, 'compared_with': ids[1]})
            for p, s in old:
                if nrm(s) not in newn and nrm(s) not in newtxt and len(risk_hits(s, cn)) >= 2:
                    ch.append({'status': 'dropped_wording', 'source': ids[1], 'date': S[ids[1]]['date'], 'page': p, 'quote': s, 'compared_with': ids[0]})
        else:
            ch += [{'status': 'in_report', 'source': ids[0], 'date': S[ids[0]]['date'], 'page': p, 'quote': s} for p, s in new]
    for sid, s in S.items():
        if s['kind'] in ('announcement', 'event'):
            ss = sorted(sents(sid), key=lambda x: -len(risk_hits(x[1], cn)))[:8]
            ch += [{'status': 'event', 'source': sid, 'date': s['date'], 'page': p, 'quote': q, 'title': s['title']} for p, q in ss]
    for c in ch: c['keywords'] = risk_hits(c['quote'], cn); c['score'] = len(c['keywords']) + (2 if c['status'] in ('new_wording', 'event') else 0)
    ch.sort(key=lambda c: (c['date'], c['source'], c['page']))
    for i, c in enumerate(ch, 1): c['id'] = f'C{i}'
    jdump({'company': meta['company'], 'n': len(ch), 'changes': ch}, f'{a.dir}/changes.json')
    print(f"{len(ch)} changes ({collections.Counter(c['status'] for c in ch)}) -> {a.dir}/changes.json")
# ---------------------------------------------------------------- leads
ALIGN = ("下面是一家公司（{company}）在多个来源、多个时点留下的“变化条目”：年报/中报（或 10-K/10-Q）之间新增或删除的风险表述，以及之后的临时公告（或 8-K）里的风险事项。"
         "每条有编号、日期、来源、状态和原文。请把指向同一对象或同一问题的条目跨时间、跨来源对齐，合成不超过 10 个“线索件”，按信贷员现在最该跟进的程度排序。每个线索件给出："
         "object（对象，不超过 25 字）、why_now（为何现在：哪些条目在什么时间发生了什么变化、前后如何衔接，不超过 150 字）、action（建议动作：信贷员下一步具体核查、索要或跟进什么，不超过 60 字）、"
         "change_ids（所依据的条目编号，按时间先后）。只能依据这些条目，不得使用外部知识。只输出 JSON：{{\"leads\":[{{\"object\":\"...\",\"why_now\":\"...\",\"action\":\"...\",\"change_ids\":[\"C3\",\"C12\"]}}]}}\n\n条目：\n{items}")
def llm(prompt, max_tokens=5000):
    """optional: any OpenAI-compatible chat-completions endpoint. Set CUE_LLM_BASE_URL (e.g. https://api.example.com/v1), CUE_LLM_API_KEY and
    CUE_LLM_MODEL; without them `leads` uses the deterministic grouping (no network call, no key needed)."""
    base = os.environ.get('CUE_LLM_BASE_URL', '').rstrip('/'); tok = os.environ.get('CUE_LLM_API_KEY'); model = os.environ.get('CUE_LLM_MODEL')
    if not (base and tok and model): return None
    body = {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': max_tokens, 'temperature': 0}
    for a in range(4):
        try:
            r = json.loads(get(base + '/chat/completions', data=json.dumps(body).encode(), headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'}))
            return r['choices'][0]['message'].get('content') or ''
        except Exception: time.sleep(5 * (a + 1))
    return None
def parse_json(t):
    t = t or ''; i, j = t.find('{'), t.rfind('}')
    try: return json.loads(t[i:j + 1])
    except Exception: return None
def cmd_leads(a):
    out = f'{a.dir}/leads.json'
    if os.path.exists(out) and not a.rebuild: print(render(jload(out))); return
    if not os.path.exists(f'{a.dir}/changes.json'): cmd_changes(a)
    C = jload(f'{a.dir}/changes.json'); ch = sorted(C['changes'], key=lambda c: -c['score'])[:260]; by = {c['id']: c for c in C['changes']}
    ch.sort(key=lambda c: (c['date'], int(c['id'][1:])))
    st = {'new_wording': '新增表述', 'dropped_wording': '删除表述', 'event': '事项', 'in_report': '报告内'}
    items = '\n'.join(f"{c['id']}｜{c['date']}｜{c['source']}｜{st[c['status']]}｜{c['quote'][:220]}" for c in ch)
    d = None if a.no_llm else parse_json(llm(ALIGN.format(company=C['company'], items=items)))
    if not d or not d.get('leads'):     # deterministic fallback: one lead per dominant keyword, most recent first
        groups = collections.defaultdict(list)
        for c in ch: groups[c['keywords'][0] if c['keywords'] else '其他'].append(c['id'])
        d = {'leads': [{'object': k, 'why_now': f'{len(v)} 条相关变化，最近一条 {by[v[-1]]["date"]}', 'action': '核对原文并向公司索要说明', 'change_ids': v[-6:]}
                       for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))[:10]], 'fallback': True}
    L = []
    for x in d['leads'][:10]:
        ids = [i for i in (x.get('change_ids') or []) if i in by]
        if not ids: continue
        ev = []
        for i in ids[:5]:
            c = by[i]; e = {'source': c['source'], 'date': c['date'], 'page': c['page'], 'quote': c['quote'], 'status': st[c['status']]}
            if c.get('prior'): e['prior'] = c['prior']
            ev.append(e)
        why = re.sub(r'\bC(\d+)\b', lambda m: f"[{by['C' + m.group(1)]['source']} p{by['C' + m.group(1)]['page']}]" if 'C' + m.group(1) in by else '', str(x.get('why_now', '')))
        L.append({'object': x.get('object', ''), 'why_now': why, 'action': x.get('action', ''), 'evidence': ev})
    res = {'company': C['company'], 'built': datetime.datetime.now().isoformat(timespec='seconds'), 'aligner': 'fallback' if d.get('fallback') else os.environ.get('CUE_LLM_MODEL', 'llm'), 'leads': L}
    jdump(res, out); print(render(res))
def render(r):
    o = [f"# Cue 线索件：{r['company']}（{len(r['leads'])} 个；每条引文均由程序从原文逐字截取，可用 verify 复核）"]
    for i, x in enumerate(r['leads'], 1):
        o.append(f"\n## L{i} {x['object']}\n为何现在：{x['why_now']}\n建议动作：{x['action']}\n证据：")
        for e in x['evidence']:
            o.append(f"- [{e['source']} {e['date']} p{e['page']}]（{e['status']}）{e['quote']}")
            if e.get('prior'): o.append(f"    上期对应 [{e['prior']['source']} p{e['prior']['page']}] {e['prior']['quote']}")
    return '\n'.join(o)
def pagespec(x):
    out = []
    for part in str(x).replace('，', ',').split(','):
        part = part.strip().lower().lstrip('p')
        if re.fullmatch(r'\d+\s*-\s*\d+', part):
            lo, hi = map(int, re.split(r'\s*-\s*', part)); out += list(range(lo, min(hi, lo + 9) + 1))
        elif part.isdigit(): out.append(int(part))
    return out
def compact(t):
    """same text, fewer tokens: trailing spaces and empty lines removed (verify ignores whitespace, so quotes copied from here still match)"""
    return '\n'.join(l.strip() for l in (t or '').split('\n') if l.strip())
def cmd_page(a):
    meta, S = load(a.dir); sp = a.specs
    if len(sp) % 2: print('usage: page DIR SOURCE PAGES [SOURCE PAGES ...]  e.g. page DIR AR2025 54,196-198 ANN-2026-05-14-1 2'); return
    shown = 0
    for src, pg in zip(sp[0::2], sp[1::2]):
        sid = resolve(src, S)
        if not sid: print(f'[{src}] (unknown source; see `brief` for the catalog)'); continue
        for n in pagespec(pg):
            if shown >= 12: print('(more than 12 pages requested; stopped -- ask for fewer pages or use `find`)'); return
            print(f'[{sid} p{n}]\n' + compact(S[sid]['text'].get(n, '(no such page)'))); shown += 1
# ---------------------------------------------------------------- verify
def resolve(src, S):
    s = str(src or '').strip()
    if s in S: return s
    s2 = re.sub(r'\.(txt|pdf|htm|jsonl)$', '', os.path.basename(s))
    if s2 in S: return s2
    cand = [k for k in S if k.lower() in s.lower() or s2.lower() in k.lower() or (s and s in S[k]['title'])]
    return max(cand, key=len) if cand else None
def find(qn, S, sid, page):
    """locations where the normalised quote occurs; fragments split by ellipses must all occur in order on one page"""
    frags = [nrm(f) for f in re.split(r'\.{3,}|…+|\[\.\.\.\]', qn_raw_holder[0]) if len(nrm(f)) >= 6] or [qn]
    hits = []
    for k, s in S.items():
        for p, t in s['text'].items():
            nx = s['text'].get(p + 1); tn = normpage(k, p, t)[0] + (normpage(k, p + 1, nx)[0] if nx else ''); pos = 0; ok = True   # may run onto next page
            for f in frags:
                j = tn.find(f, pos)
                if j < 0: ok = False; break
                pos = j + len(f)
            if ok: hits.append((k, p))
    return hits
qn_raw_holder = ['']
def nearest(q, S, sid):
    qn = nrm(q)[:400]; grams = {qn[i:i + 4] for i in range(0, max(1, len(qn) - 3), 2)}; best = (0, None, None, '')
    pool = sorted(((sum(1 for g in grams if g in normpage(k, p, t)[0]), k, p, t) for k, s in S.items() for p, t in s['text'].items()), key=lambda x: -x[0])
    for _, k, p, t in pool[:4]:
        tn, idx = normpage(k, p, t); sm = difflib.SequenceMatcher(None, qn, tn, autojunk=False); m = sm.find_longest_match(0, len(qn), 0, len(tn))
        lo = max(0, m.b - m.a); hi = min(len(tn), lo + int(len(qn) * 1.2) + 5)
        if hi <= lo: continue
        r = difflib.SequenceMatcher(None, qn, tn[lo:hi], autojunk=False).ratio()
        if r > best[0]: best = (r, k, p, t[idx[lo]:idx[hi - 1] + 1])
    return best
def _check(q, src, page, S):
    qn_raw_holder[0] = q; qn = nrm(q)
    if len(qn) < 8: return {'status': 'too_short'}
    sid = resolve(src, S)
    try: page = int(re.search(r'\d+', str(page)).group())
    except Exception: page = None
    hits = find(qn, S, sid, page)
    if sid and page is not None and any(k == sid and abs(p - page) <= 1 for k, p in hits): return {'status': 'verbatim', 'source': sid, 'page': page}
    if hits: return {'status': 'verbatim_elsewhere', 'found_at': [f'{k} p{p}' for k, p in hits[:3]], 'cited': f'{src} p{page}'}
    r, k, p, real = nearest(q, S, sid)
    # not verbatim: classify honestly. numbers (commas/points dropped, bare years ignored) - are they really in the filings?
    nums = {re.sub(r'[,，.]', '', n) for n in re.findall(r'\d[\d,，]*(?:\.\d+)?', q)}
    nums = {n for n in nums if len(n) >= 2 and not re.fullmatch(r'(19|20)\d\d', n)}
    def pg(ck, cp):
        t = S[ck]['text'].get(cp) if ck in S else None; nx = S[ck]['text'].get(cp + 1) if t else None
        return (normpage(ck, cp, t)[0] + (normpage(ck, cp + 1, nx)[0] if nx else '')) if t else ''
    near = [(sid, pp) for pp in ((page - 1, page, page + 1) if page is not None else ()) if sid] + ([(k, p), (k, p - 1)] if k else [])
    base = {'status': 'not_found', 'cited': f'{src} p{page}', 'nearest': {'similarity': round(r, 2), 'source': k, 'page': p, 'text': real[:400]}}
    # edited: >=85% of the quote's characters occur, in order, in the real text (deleted words, joined clauses, ellipsis gaps)
    cov = max([sum(b.size for b in difflib.SequenceMatcher(None, qn, pg(ck, cp), autojunk=False).get_matching_blocks() if b.size >= 4) / max(1, len(qn)) for ck, cp in near] or [0])
    base['coverage'] = round(cov, 2)
    if cov >= 0.85 and all(n in ''.join(pg(ck, cp) for ck, cp in near) for n in nums): return dict(base, kind='edited')
    # table restated: every number of the quote sits on one real page (labels re-worded, cells joined into a sentence)
    if nums and r >= 0.4:
        for ck, cp in near + [(sid or k, pp) for pp in sorted(S[sid or k]['text']) if (sid or k)]:
            if all(n in pg(ck, cp) for n in nums): return dict(base, kind='table_restated', numbers_at=f'{ck} p{cp}')
    miss = sorted(n for n in nums if len(n) >= 3 and n not in _alldoc(S))
    return dict(base, kind='numbers_differ' if miss else 'absent', missing_numbers=miss[:5])
_AD = {}
def _alldoc(S):
    if id(S) not in _AD: _AD[id(S)] = '\n'.join(normpage(k, p, t)[0] for k in S for p, t in S[k]['text'].items())
    return _AD[id(S)]
def check(q, src, page, S):
    """_check + fabricated numbers: numbers (>=3 digits once commas/points are dropped, bare years ignored) in the quote that occur neither on
    the cited page (+-1) nor anywhere in the documents"""
    r = _check(q, src, page, S)
    if r['status'] in ('verbatim', 'too_short'): r['fab_numbers'] = []; return r
    nums = {re.sub(r'[,，.]', '', n) for n in re.findall(r'\d[\d,，]*(?:\.\d+)?', q)}
    nums = {n for n in nums if len(n) >= 3 and not re.fullmatch(r'(19|20)\d\d', n)}
    sid = resolve(src, S)
    try: pg = int(re.search(r'\d+', str(page)).group())
    except Exception: pg = None
    near = ''.join(normpage(sid, p, S[sid]['text'][p])[0] for p in ((pg - 1, pg, pg + 1) if pg is not None else ()) if sid and p in S[sid]['text'])
    r['fab_numbers'] = sorted(n for n in nums if n not in near and n not in _alldoc(S))
    return r
def snap(t, real, cn):
    """widen a matched span of page text t to whole sentence(s), so the replacement quote reads naturally (still a verbatim substring of t)"""
    i = t.find(real)
    if i < 0: return real
    j = i + len(real); stops = '。；！？\n' if cn else '\n'
    lo = max([t.rfind(c, max(0, i - 200), i) for c in stops] + [-1]) + 1
    if not cn:
        m = [x.end() for x in re.finditer(r'[.;]\s+(?=[A-Z(“"])', t[max(0, i - 200):i])]
        if m: lo = max(lo, max(0, i - 200) + m[-1])
    his = [k for k in (t.find(c, j) for c in stops) if 0 <= k <= j + 200]
    if not cn:
        m = re.search(r'[.;](\s|$)', t[j:j + 200]); his += [j + m.start()] if m else []
    hi = min(his) + 1 if his else j
    q = t[lo:hi].strip()
    return q if 8 <= len(q) <= 700 else real
def table_snippet(t, q):
    """for a quote that restates table cells: the smallest span of the real page holding every number of the quote, widened to whole lines
    (plus the row label line above), copied verbatim. None if the span would be too long."""
    raw = [n for n in re.findall(r'\d[\d,，]*(?:\.\d+)?', q) if len(re.sub(r'[,，.]', '', n)) >= 2 and not re.fullmatch(r'(19|20)\d\d', n)]
    pats = {re.sub(r'[,，]', '', n): '(?<![\\d.])' + '[,，]?'.join(re.escape(c) for c in re.sub(r'[,，]', '', n)) + '(?![\\d])' for n in raw}
    occ = [[m.start() for m in re.finditer(pt, t)] for pt in pats.values()]
    if not pats or not all(occ): return None
    best = None
    for start in sorted({x for o in occ for x in o}):
        ends = [min([x for x in o if x >= start], default=None) for o in occ]
        if None in ends: continue
        w = (start, max(ends))
        if best is None or w[1] - w[0] < best[1] - best[0]: best = w
    if not best: return None
    lo = best[0]
    for _ in range(2):                     # the row label sits on the line(s) above in A-share PDFs (one cell per line)
        k = t.rfind('\n', 0, max(0, lo - 1)); lo = k + 1 if k >= 0 else 0
    hi = t.find('\n', best[1]); hi = len(t) if hi < 0 else hi
    sn = t[lo:hi].strip()
    return sn if 8 <= len(sn) <= 600 else None
def fix_answer(path, d, sig, res, S):
    """repair an answer in place; every kept quote is verbatim text of the cited page afterwards. The verify levels themselves are unchanged."""
    bak = re.sub(r'\.json$', '', path) + '.before_fix.json'
    if not os.path.exists(bak):
        with open(path, encoding='utf-8') as src: body = src.read()
        with open(bak, 'w', encoding='utf-8') as dst: dst.write(body)
    cn = any(re.search(r'[\u4e00-\u9fff]', S[k]['title'] or '') for k in S) or any(k.startswith(('AR', 'ANN-')) for k in S)
    it = iter(res); log = collections.Counter(); lines = []
    for i, x in enumerate(sig, 1):
        keep = []
        for e in x.get('evidence') or []:
            r = next(it); q = e.get('quote', '')
            if r['status'] == 'verbatim': keep.append(e); continue
            if r['status'] == 'verbatim_elsewhere':
                k, p = r['found_at'][0].rsplit(' p', 1); e = dict(e, source=k, page=int(p)); keep.append(e); log['page_fixed'] += 1
                lines.append(f"[S{i} 页码改正] {r['cited']} -> {k} p{p}: {q[:60]}"); continue
            nb = r.get('nearest') or {}; kind = r.get('kind')
            if kind == 'table_restated' and r.get('numbers_at') and not r.get('fab_numbers'):
                k, p0 = r['numbers_at'].rsplit(' p', 1); p0 = int(p0); tx = S[k]['text']; nq = None
                for p, t in ((p0, tx.get(p0, '')), (p0 + 1, tx.get(p0 + 1, '')), (p0, tx.get(p0, '') + '\n' + tx.get(p0 + 1, ''))):   # numbers may sit on the next page
                    nq = table_snippet(t, q)
                    if nq and check(nq, k, p, S)['status'] == 'verbatim': break
                    nq = None
                if nq:
                    keep.append(dict(e, source=k, page=p, quote=nq)); log['replaced_with_original'] += 1
                    lines.append(f"[S{i} 换成原表] {q[:50]} -> [{k} p{p}] {' '.join(nq.split())[:80]}"); continue
            if r['status'] == 'not_found' and kind in ('edited', 'table_restated') and nb.get('source') and nb.get('similarity', 0) >= (0.5 if kind == 'edited' else 0.6) and not r.get('fab_numbers'):
                k, p = nb['source'], nb['page']; t = S[k]['text'].get(p, ''); r0 = nearest(q, S, k)
                nq = snap(t, r0[3], cn) if r0[1] == k and r0[2] == p else nb['text']
                if check(nq, k, p, S)['status'] == 'verbatim':
                    keep.append(dict(e, source=k, page=p, quote=nq)); log['replaced_with_original'] += 1
                    lines.append(f"[S{i} 换成原文] {q[:50]} -> [{k} p{p}] {nq[:80]}"); continue
            log['dropped'] += 1; lines.append(f"[S{i} 删除] ({r['status']}{'/' + kind if kind else ''}) {q[:80]}")
        x['evidence'] = keep
        if not keep: lines.append(f"[S{i} 警告] 这条信号已没有可核对的原文证据：用 find 或 page 找一句原文补上，或删掉这条。")
    jdump(d, path)
    after = [check(e.get('quote', ''), e.get('source'), e.get('page'), S)['status'] for x in sig for e in x.get('evidence') or []]
    print(json.dumps({'before': dict(collections.Counter(r['status'] for r in res), total=len(res)), 'fixes': dict(log),
                      'after': {'verbatim': after.count('verbatim'), 'total': len(after)}, 'saved_original': os.path.basename(bak)}, ensure_ascii=False))
    for l in lines: print(l)
    print('answer.json 已写回；引文现在都能在所注页 ±1 内逐字命中。直接用中文复述答案即可，不需要再逐句复核。' if all(x.get('evidence') for x in sig) else '有信号缺证据，见上面的警告。')
def cmd_brief(a):
    meta, S = load(a.dir); cn = meta.get('market') == 'CN'
    if not os.path.exists(f'{a.dir}/leads.json'):
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): cmd_leads(argparse.Namespace(dir=a.dir, no_llm=False, rebuild=False))
    L = jload(f'{a.dir}/leads.json')
    o = [f"# Cue 简报：{meta['company']}（{meta.get('id', '')}，{meta.get('market', '')}）",
         "一次给全：材料目录、线索件、可直接粘贴的逐字证据。不需要再 ls / cat sources.json / Read 原文件。",
         "\n## 材料（来源编号｜类型｜日期｜页数｜解析通道｜标题）"]
    BAS = {'pdf_page': 'PDF页', 'html_page_break': '原文分页', 'marker': '页标记', 'form_feed': '分页符', 'block': '文本块(页码=块号)'}
    for k, x in S.items(): o.append(f"{k}｜{x['kind']}｜{x['date']}｜{len(x['text'])}｜{x.get('parser', 'local')}/{BAS.get(x.get('page_basis'), x.get('page_basis') or '-')}｜{(x.get('title') or '')[:40]}")
    pend = [k for k, x in S.items() if x.get('parser') == 'pending']
    if pend: o.append(f"未解析 {len(pend)} 个（{', '.join(pend[:8])}{' …' if len(pend) > 8 else ''}）：先用 Cue Omni Reader 解析后 ingest，或 cue.py local 本地兜底。")
    o.append("\n## 线索件（每行 JSON 证据都由程序从原文截取并已逐字核对，可原样粘贴进 answer.json 的 evidence）")
    for i, x in enumerate(L['leads'][:a.top], 1):
        o.append(f"\n### L{i} {x['object']}\n为何现在：{x['why_now']}\n建议动作：{x['action']}")
        for e in x['evidence']:
            if check(e['quote'], e['source'], e['page'], S)['status'] != 'verbatim': continue
            o.append(json.dumps({'source': e['source'], 'page': e['page'], 'quote': e['quote']}, ensure_ascii=False) + f"  # {e['date']} {e['status']}")
            pr = e.get('prior')
            if pr: o.append('  上期对应 ' + json.dumps({'source': pr['source'], 'page': pr['page'], 'quote': pr['quote']}, ensure_ascii=False))
    o.append("\n## 下一步\n1. 线索件证据不够时，在同一条命令里一次补查：find DIR 关键词1 关键词2 --max 30，或 page DIR 来源 页码,页码-页码 来源2 页码。"
             "\n2. 一次写好 answer.json，然后运行一次 verify DIR --json answer.json --fix，修正后直接复述，不要逐句复核。")
    print('\n'.join(o))
def cmd_find(a):
    meta, S = load(a.dir); cn = meta.get('market') == 'CN'; terms = [t.lower() for t in a.terms]; seen = set(); hits = []
    for k, x in S.items():
        if a.source and k != resolve(a.source, S): continue
        for p, t in x['text'].items():
            for q in sentences(t, cn):
                ql = q.lower(); m = [t2 for t2 in terms if t2 in ql]
                if not m or nrm(q) in seen: continue
                seen.add(nrm(q)); hits.append((len(m), len(risk_hits(q, cn)), x['date'], k, p, q))
    hits.sort(key=lambda h: (-h[0], -h[1], h[2]), reverse=False)
    for h in hits[:a.max]: print(json.dumps({'source': h[3], 'page': h[4], 'quote': h[5]}, ensure_ascii=False))
    if len(hits) > a.max: print(f'(共 {len(hits)} 句，只列前 {a.max} 句；可加 --source 或换更具体的词)')
    if not hits: print('(没有找到；换个词，或用 page 读原页)')
def cmd_verify(a):
    meta, S = load(a.dir)
    if a.json:
        d = jload_lenient(a.json); sig = d.get('signals') or d.get('leads') or []; res = []
        for i, x in enumerate(sig, 1):
            for e in x.get('evidence') or []:
                r = check(e.get('quote', ''), e.get('source') or e.get('report'), e.get('page'), S); r.update(signal=i, quote=e.get('quote', '')); res.append(r)
        n = collections.Counter(r['status'] + ('/' + r['kind'] if r.get('kind') else '') for r in res)
        out = {'summary': dict(n, total=len(res), fab_numbers=sum(len(r.get('fab_numbers') or []) for r in res)), 'results': res}
        if a.out: jdump(out, a.out)
        if a.fix: return fix_answer(a.json, d, sig, res, S)
        print(json.dumps(out['summary'], ensure_ascii=False)); [print(f"[{r['status']}] {r['quote'][:80]}") for r in res if r['status'] != 'verbatim']
    else:
        print(json.dumps(check(a.quote, a.source, a.page, S), ensure_ascii=False, indent=1))
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('fetch'); p.add_argument('dir'); g = p.add_mutually_exclusive_group(required=True); g.add_argument('--cn'); g.add_argument('--us'); g.add_argument('--list')
    p.add_argument('--months', type=float, default=12); p.add_argument('--local', action='store_true'); p.add_argument('--company'); p.add_argument('--market'); p.add_argument('--id')
    p = sp.add_parser('local'); p.add_argument('dir'); p.add_argument('sids', nargs='*')
    p = sp.add_parser('omni'); p.add_argument('dir'); p.add_argument('sids', nargs='*'); p.add_argument('--yes', action='store_true'); p.add_argument('--detail', default='grounded', choices=['grounded', 'text'])
    p = sp.add_parser('ingest'); p.add_argument('dir'); p.add_argument('--omni'); p.add_argument('--sid'); p.add_argument('--omni-dir')
    for k in ('kind', 'date', 'title', 'url', 'company', 'market', 'id'): p.add_argument('--' + k)
    p = sp.add_parser('changes'); p.add_argument('dir')
    p = sp.add_parser('leads'); p.add_argument('dir'); p.add_argument('--no-llm', action='store_true'); p.add_argument('--rebuild', action='store_true')
    p = sp.add_parser('page'); p.add_argument('dir'); p.add_argument('specs', nargs='+')
    p = sp.add_parser('brief'); p.add_argument('dir'); p.add_argument('--top', type=int, default=10)
    p = sp.add_parser('find'); p.add_argument('dir'); p.add_argument('terms', nargs='+'); p.add_argument('--max', type=int, default=30); p.add_argument('--source')
    p = sp.add_parser('verify'); p.add_argument('dir'); p.add_argument('--json'); p.add_argument('--out'); p.add_argument('--fix', action='store_true'); p.add_argument('--quote'); p.add_argument('--source'); p.add_argument('--page')
    ap.add_argument('--version', action='version', version=__version__)
    a = ap.parse_args(argv)
    try: return {'fetch': cmd_fetch, 'local': cmd_local, 'omni': cmd_omni, 'ingest': cmd_ingest, 'changes': cmd_changes, 'leads': cmd_leads, 'brief': cmd_brief, 'find': cmd_find, 'page': cmd_page, 'verify': cmd_verify}[a.cmd](a) or 0
    except CueError as e:
        print(f'cue.py: error: {e}', file=sys.stderr); return 2
    return 0
if __name__ == '__main__':
    sys.exit(main())
