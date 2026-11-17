#!/usr/bin/env python3
"""cue-lead-pieces skill regression — stdlib only, offline (synthetic filings, no network, no model)."""
from __future__ import annotations
import io, json, os, re, shutil, subprocess, sys, tempfile, unittest, contextlib
from pathlib import Path
_HERE = Path(__file__).resolve().parent; _SKILL = _HERE.parent; CUE = _HERE / 'cue.py'
sys.path.insert(0, str(_HERE)); import cue  # noqa: E402
P1 = "Liquidity\nAs a result of the upcoming maturity of the Credit Facility, there is substantial doubt about our ability to continue as a going concern.\nNet loss | 1,234 | 987\n"
P2 = "Other matters\nThe lenders have the right to accelerate the loans for noncompliance with the net leverage ratio covenant.\n"
def make_dir(d):
    os.makedirs(f'{d}/pages'); src = [{'sid': '10-K_FY2025', 'kind': 'annual', 'date': '2026-03-01', 'title': '10-K test', 'n_pages': 2}]
    wj({'company': 'TestCo', 'id': 'TEST', 'market': 'US', 'sources': src}, f'{d}/sources.json')
    with open(f'{d}/pages/10-K_FY2025.jsonl', 'w') as f:
        for i, t in enumerate((P1, P2), 1): f.write(json.dumps({'page': i, 'text': t}) + '\n')
def wj(obj, path, **kw):
    """json.dump 完立刻关句柄（历史上这里是 open() 不关，双跑噪声 148 行的根因之一）。"""
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, **kw)
def rj(path):
    with open(path, encoding='utf-8') as f: return json.load(f)
def rl(path):
    with open(path, encoding='utf-8') as f: return list(f)
def wt(path, text):
    with open(path, 'w', encoding='utf-8') as f: f.write(text)

class CueLeadPiecesRegression(unittest.TestCase):
    def setUp(self): self.d = tempfile.mkdtemp(); make_dir(self.d); self.S = cue.load(self.d)[1]
    def tearDown(self): shutil.rmtree(self.d, ignore_errors=True)
    def test_frontmatter(self):
        md = (_SKILL / 'SKILL.md').read_text(encoding='utf-8'); fm = re.match(r'^---\n(.*?)\n---\n', md, re.S).group(1)
        self.assertRegex(fm, re.compile(r'^name:\s*cue-lead-pieces$', re.M)); self.assertIn('version: "0.4.35"', fm); self.assertEqual(cue.__version__, '0.4.35')
    def test_verify_levels(self):
        c = lambda q, p: cue.check(q, '10-K_FY2025', p, self.S)
        self.assertEqual(c('there is substantial doubt about our ability to continue as a going concern', 1)['status'], 'verbatim')
        self.assertEqual(c('The lenders have the right to accelerate the loans', 9)['status'], 'verbatim_elsewhere')
        r = c('there is substantial doubt about our ability to continue as going concern', 1); self.assertEqual((r['status'], r.get('kind')), ('not_found', 'edited'))
        r = c('The company has ample liquidity and no refinancing needs at all', 1); self.assertEqual(r['status'], 'not_found'); self.assertIn(r['kind'], ('absent', 'numbers_differ'))
    def test_fix_rewrites_answer(self):
        a = os.path.join(self.d, 'answer.json')
        wj({'signals': [{'rank': 1, 'title': 't', 'explanation': 'e', 'evidence': [
            {'source': '10-K_FY2025', 'page': 1, 'quote': 'there is substantial doubt about our ability to continue as going concern'},
            {'source': '10-K_FY2025', 'page': 9, 'quote': 'The lenders have the right to accelerate the loans'},
            {'source': '10-K_FY2025', 'page': 1, 'quote': 'The company has ample liquidity and no refinancing needs at all'}]}]}, a)
        out = subprocess.run([sys.executable, str(CUE), 'verify', self.d, '--json', a, '--fix'], capture_output=True, text=True, check=True).stdout
        self.assertTrue(os.path.exists(os.path.join(self.d, 'answer.before_fix.json')))
        ev = rj(a)['signals'][0]['evidence']; self.assertEqual(len(ev), 2)
        for e in ev: self.assertEqual(cue.check(e['quote'], e['source'], e['page'], cue.load(self.d)[1])['status'], 'verbatim')
        self.assertIn('"after": {"verbatim": 2, "total": 2}', out)
    def test_unknown_code_one_line_error(self):
        """0.3.1: an unknown A-share code / US ticker / CIK exits 2 with one stderr line, not a StopIteration traceback (offline: `get` is faked)"""
        import urllib.error
        def fake_get(url, headers=None, data=None, tries=4):
            if 'cninfo' in url: return json.dumps({'stockList': [{'code': '600606', 'orgId': 'x', 'zwjc': 'X'}]}).encode()
            if 'company_tickers' in url: return json.dumps({'0': {'cik_str': 1, 'ticker': 'LESL', 'title': 'X'}}).encode()
            raise urllib.error.HTTPError(url, 404, 'Not Found', None, None)
        real = cue.get; cue.get = fake_get
        try:
            for args, want in ((['--cn', '999999'], "unknown A-share code '999999'"), (['--us', 'ZZZZQX'], "unknown US ticker 'ZZZZQX'"),
                               (['--us', '9999999999'], "unknown CIK '9999999999'")):
                err = io.StringIO(); d = os.path.join(self.d, 'fetch-' + args[1])
                with contextlib.redirect_stderr(err): rc = cue.main(['fetch', d] + args)
                self.assertEqual(rc, 2); lines = err.getvalue().strip().splitlines()
                self.assertEqual(len(lines), 1, err.getvalue()); self.assertTrue(lines[0].startswith('cue.py: error: ' + want), lines[0])
                self.assertNotIn('Traceback', err.getvalue())
        finally: cue.get = real
    def _bundle(self):
        """synthetic omni.result_bundle.v1 (grounded) in the public shape: Markdown text + segments with UTF-8 byte ranges and source PDF page anchors"""
        parts = [("# 年度报告\n公司存在逾期债务，金额为 1,234 万元。\n", 1), ("| 项目 | 期末 |\n|---|---|\n| 短期借款 | 5,678 |\n", 2), ("会计师对持续经营能力出具了强调事项段。\n", 4)]
        text, segs, pos = '', [], 0
        for i, (t, p) in enumerate(parts, 1):
            b = len(t.encode('utf-8')); text += t
            segs.append({'segment_id': f'segment_{i:06d}', 'content_range_utf8': {'start': pos, 'end': pos + b},
                         'grounding': {'availability': 'available', 'anchors': [{'kind': 'page', 'basis': 'source_pdf_page_1_based', 'reliability': 'reliable', 'value': p}]}}); pos += b
        return {'protocol_version': 'omni.result_bundle.v1', 'detail': 'grounded', 'content': {'media_type': 'text/markdown; charset=utf-8', 'text': text},
                'grounding': {'media_type': 'application/vnd.cue.omni-grounding+json; version=1', 'value': {'schema_version': 'omni.grounding.v1', 'detail': 'grounded',
                              'document': {'format': 'pdf', 'partial': True, 'incomplete': [{'basis': 'source_pdf_page_1_based', 'kind': 'page', 'reason': 'processing_timeout', 'values': [3]}]},
                              'segments': segs}}}
    def test_ingest_omni_grounded_bundle(self):
        """0.4.0: an Omni grounded bundle becomes per-PDF-page text; verify then checks quotes against those pages"""
        d = os.path.join(self.d, 'cn'); od = os.path.join(d, 'omni'); os.makedirs(od)
        wj({'structuredContent': {'result': self._bundle()}}, os.path.join(od, 'AR2025.json'), ensure_ascii=False)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = cue.main(['ingest', d, '--omni', os.path.join(od, 'AR2025.json'), '--sid', 'AR2025', '--kind', 'annual', '--date', '2026-04-20',
                           '--title', '2025年年度报告', '--company', 'TestCN', '--market', 'CN'])
        self.assertEqual(rc, 0); self.assertIn('parser=omni-grounded, page_basis=pdf_page', out.getvalue()); self.assertIn('incomplete page [3]', out.getvalue())
        meta, S = cue.load(d); s = S['AR2025']
        self.assertEqual((s['n_pages'], s['parser'], s['page_basis']), (4, 'omni-grounded', 'pdf_page')); self.assertEqual(s['text'][3], '')
        self.assertEqual(cue.check('公司存在逾期债务，金额为1,234万元', 'AR2025', 1, S)['status'], 'verbatim')
        self.assertEqual(cue.check('会计师对持续经营能力出具了强调事项段', 'AR2025', 4, S)['status'], 'verbatim')
        self.assertEqual(cue.check('会计师对持续经营能力出具了强调事项段', 'AR2025', 1, S)['status'], 'verbatim_elsewhere')
        self.assertIn('短期借款', s['text'][2])
    # ---- real response shapes (sanitized fixture recorded from @cueai/omni-reader-mcp 1.8.3, grounded; synthetic text, fake ids)
    FX = _HERE / 'fixtures' / 'omni_real_shape.json'
    def _fx(self): return rj(self.FX)
    def _ingest(self, d, path, **env):
        e = dict(os.environ, **env)
        return subprocess.run([sys.executable, str(CUE), 'ingest', d, '--omni', path, '--sid', 'ANN-1', '--kind', 'announcement', '--date', '2026-10-01',
                               '--title', 't', '--company', 'TestCN', '--market', 'CN'], capture_output=True, text=True, env=e)
    def _bridge_env(self, fx_path, log):
        import shlex
        return {'CUE_OMNI_BRIDGE': ' '.join(shlex.quote(x) for x in (sys.executable, str(_HERE / 'fixtures' / 'fake_omni_bridge.py'), str(fx_path), log))}
    def test_ingest_real_shape_inline(self):
        """the real parse result: result.kind=bundle, bundle_protocol_version + parts{content,grounding} with inline storage; saved as the full
        tools/call response or as structuredContent -> PDF pages; saved as Markdown only (save_result / content[0].text) -> labeled blocks"""
        fx = self._fx()
        for name, obj in (('full.json', fx['inline_tools_call']), ('sc.json', fx['inline_tools_call']['result']['structuredContent'])):
            d = os.path.join(self.d, name); p = os.path.join(self.d, 'in_' + name); wj(obj, p, ensure_ascii=False)
            r = self._ingest(d, p); self.assertEqual(r.returncode, 0, r.stderr); self.assertIn('ANN-1: 3 pages (parser=omni-grounded, page_basis=pdf_page)', r.stdout)
            S = cue.load(d)[1]; t = S['ANN-1']['text']
            self.assertEqual(cue.check('累计逾期债务 45.60 亿元', 'ANN-1', 1, S)['status'], 'verbatim')
            self.assertEqual(cue.check('公司作为被告的诉讼事项有 12 件，金额 3.40 亿元', 'ANN-1', 2, S)['status'], 'verbatim')
            self.assertNotIn('<td', t[3]); self.assertIn('| 张三 | 5 |', t[3])          # inline HTML table -> pipe rows
        p = os.path.join(self.d, 'view.md'); wt(p, fx['inline_tools_call']['result']['content'][0]['text'])
        r = self._ingest(os.path.join(self.d, 'md'), p); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('page_basis=block', r.stdout); self.assertIn('text-only result', r.stdout)
    def test_ingest_real_shape_artifact_via_bridge(self):
        """large results come back as artifacts (storage.kind=artifact + next_cursor); ingest pages them in through the Bridge's read_result
        (Bridge-local, no parse call, no credits) and checks the content digest"""
        fx = self._fx(); p = os.path.join(self.d, 'final.json'); wj(fx['final_response'], p, ensure_ascii=False)
        log = os.path.join(self.d, 'bridge.log'); d = os.path.join(self.d, 'cn')
        r = self._ingest(d, p, **self._bridge_env(self.FX, log)); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('ANN-1: 3 pages (parser=omni-grounded, page_basis=pdf_page)', r.stdout)
        tools = [json.loads(l)['tool'] for l in rl(log)]; self.assertEqual(set(tools), {'read_result'}); self.assertGreater(len(tools), 4)
        S = cue.load(d)[1]; self.assertEqual(cue.check('累计逾期债务 45.60 亿元', 'ANN-1', 1, S)['status'], 'verbatim')
        bad = dict(fx, parts=dict(fx['parts'], content=fx['parts']['content'].replace('45.60', '46.50'))); bp = os.path.join(self.d, 'bad_fx.json'); wj(bad, bp, ensure_ascii=False)
        r = self._ingest(os.path.join(self.d, 'bad'), p, **self._bridge_env(bp, log)); self.assertEqual(r.returncode, 2); self.assertIn('digest', r.stderr)
        fp = os.path.join(self.d, 'failed.json'); wj(fx['failed_response'], fp)
        r = self._ingest(os.path.join(self.d, 'f'), fp); self.assertEqual(r.returncode, 2); self.assertIn('SOURCE_ACCESS_DENIED', r.stderr); self.assertEqual(len(r.stderr.strip().splitlines()), 1)
    def test_omni_command_asks_first_then_parses(self):
        """`omni` spends credits: without --yes it only states the plan (exit 3, Bridge never started); with --yes it parses, polls, reads, ingests"""
        d = os.path.join(self.d, 'cn'); os.makedirs(d)
        wj({'company': 'TestCN', 'id': '000000', 'market': 'CN', 'sources': [{'sid': 'ANN-1', 'kind': 'announcement', 'date': '2026-10-01', 'title': 't',
                   'source_url': 'https://example.com/a.pdf', 'parser': 'pending', 'n_pages': 0}]}, f'{d}/sources.json')
        log = os.path.join(self.d, 'bridge.log'); env = dict(os.environ, **self._bridge_env(self.FX, log))
        r = subprocess.run([sys.executable, str(CUE), 'omni', d], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 3); self.assertIn('--yes', r.stdout); self.assertFalse(os.path.exists(log))
        r = subprocess.run([sys.executable, str(CUE), 'omni', d, '--yes'], capture_output=True, text=True, env=env); self.assertEqual(r.returncode, 0, r.stderr)
        tools = [json.loads(l) for l in rl(log)]; self.assertEqual([t['tool'] for t in tools[:2]], ['parse', 'get_parse_status'])
        self.assertEqual(tools[0]['args'], {'source': 'https://example.com/a.pdf', 'detail': 'grounded', 'result_delivery': 'artifact'})
        self.assertIn('credits_charged=0.201', r.stdout); self.assertIn('credits charged in total (as reported by Omni): 0.201', r.stdout)
        s = cue.load(d)[1]['ANN-1']; self.assertEqual((s['n_pages'], s['parser'], s['page_basis']), (3, 'omni-grounded', 'pdf_page'))
        self.assertTrue(os.path.exists(f'{d}/omni/ANN-1.json'))
    def test_ingest_text_only_and_markers(self):
        self.assertEqual(cue.text_pages('a\fb')[1], 'form_feed')
        p, basis = cue.text_pages('<!-- page 1 -->\nfirst\n<!-- page 3 -->\nthird\n'); self.assertEqual((basis, len(p), p[2].strip()), ('marker', 3, 'third'))
        p, basis = cue.text_pages(('x' * 100 + '\n') * 80); self.assertEqual(basis, 'block'); self.assertGreater(len(p), 1)
    def test_list_register_and_local_fallback(self):
        """fetch --list registers filings as pending (e.g. from Cue data-MCP); local is the labeled fallback parser (`get` faked, offline)"""
        d = os.path.join(self.d, 'us'); lst = os.path.join(self.d, 'list.json')
        wj([{'sid': '8-K_2026-05-01', 'kind': 'event', 'date': '2026-05-01', 'title': '8-K', 'source_url': 'https://example.com/a.htm'}], lst)
        html = ('<p>' + 'Lenders agreed to a forbearance period under the credit agreement. ' * 3 + '</p><div style="page-break-after: always"></div>') * 3
        real = cue.get; cue.get = lambda url, headers=None, data=None, tries=4: html.encode()
        try:
            with contextlib.redirect_stdout(io.StringIO()) as o1: self.assertEqual(cue.main(['fetch', d, '--list', lst, '--company', 'T', '--market', 'US']), 0)
            self.assertIn('not parsed yet', o1.getvalue()); self.assertEqual(cue.load(d)[1]['8-K_2026-05-01']['parser'], 'pending')
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(cue.main(['local', d]), 0)
        finally: cue.get = real
        s = cue.load(d)[1]['8-K_2026-05-01']; self.assertEqual((s['parser'], s['page_basis'], s['n_pages']), ('local', 'html_page_break', 3))
    def test_cn_fetch_lists_without_download(self):
        """default fetch only lists filings (no download, no parse) so the agent can hand the URLs to Cue Omni Reader"""
        ann = {'announcementId': 1, 'announcementTitle': '2025年年度报告', 'adjunctUrl': 'finalpage/2026-04-20/1.PDF', 'announcementTime': 1776650000000}
        def fake_get(url, headers=None, data=None, tries=4):
            if 'szse_stock' in url: return json.dumps({'stockList': [{'code': '600606', 'orgId': 'x', 'zwjc': 'X'}]}).encode()
            if 'hisAnnouncement' in url: return json.dumps({'announcements': [ann] if b'category_ndbg' in (data or b'') else [], 'hasMore': False}).encode()
            raise AssertionError('download attempted: ' + url)
        real = cue.get; cue.get = fake_get; d = os.path.join(self.d, 'cnlist')
        try:
            with contextlib.redirect_stdout(io.StringIO()) as o: self.assertEqual(cue.main(['fetch', d, '--cn', '600606']), 0)
        finally: cue.get = real
        m = rj(os.path.join(d, 'sources.json')); self.assertEqual([(x['sid'], x['parser']) for x in m['sources']], [('AR2025', 'pending')])
        self.assertTrue(m['sources'][0]['source_url'].endswith('.PDF')); self.assertIn('Cue Omni Reader', o.getvalue())
    def test_page_and_brief_offline(self):
        self.assertEqual(cue.pagespec('1,3-4'), [1, 3, 4])
        out = subprocess.run([sys.executable, str(CUE), 'page', self.d, '10-K_FY2025', '1-2'], capture_output=True, text=True, check=True).stdout
        self.assertIn('[10-K_FY2025 p2]', out)
        env = {k: v for k, v in os.environ.items() if not k.startswith('CUE_LLM_')}
        out = subprocess.run([sys.executable, str(CUE), 'brief', self.d], capture_output=True, text=True, check=True, env=env).stdout
        self.assertIn('10-K_FY2025', out); self.assertEqual(rj(f'{self.d}/leads.json')['aligner'], 'fallback')
class QuietStream:
    """把 unittest 汇总行里的耗时剥掉：双跑逐字节比时「Ran 12 tests in 1.397s」那一秒数是纯噪声，
       与临时路径同族（M255 治的就是这一类）。结论本身照原样出——用例数、OK／FAILED、失败详情一律不改。"""
    def __init__(self, inner): self._inner = inner
    def write(self, s): self._inner.write(re.sub(r'^(Ran \d+ tests?) in [\d.]+s$', r'\1', s, flags=re.M))
    def writeln(self, s=''): self.write(s + '\n')
    def flush(self): self._inner.flush()
    def isatty(self): return False

# 入口自带句柄判别（C1）：漏一枚未关闭的文件句柄就必须翻退码。
# 旧形制把判别挂在外面——普通跑 grep 计数是恒真支（baseline 与注入漏柄后都是 0 枚），
# 而 `-W error::ResourceWarning` 只会把警告打成「Exception ignored」，退码照样 0。
# 现在在进程内以 record 方式收下全部警告、跑完再 gc.collect() 逼出析构期的那一批，
# 有 ResourceWarning 就点名枚数并非 0 退出；判定逻辑与用例数一律不改。
def _live_readers():
    """当场还开着的文件对象（析构期没收到的那一批只能靠这个看见，不能靠 ResourceWarning）。"""
    import gc, io
    gc.collect()
    return [o for o in gc.get_objects()
            if isinstance(o, io.IOBase) and not o.closed
            and o not in (sys.stdin, sys.stdout, sys.stderr)]


def unclosed_handles():
    import gc
    import warnings
    base = _live_readers()
    base_ids = {id(o) for o in base}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(CueLeadPiecesRegression)
        res = unittest.TextTestRunner(stream=QuietStream(sys.stderr), verbosity=2).run(suite)
        gc.collect()
    leaks = [w for w in caught if issubclass(w.category, ResourceWarning)]
    held = [o for o in _live_readers() if id(o) not in base_ids]
    for w in leaks[:6]:
        sys.stderr.write('UNCLOSED-HANDLE: %s\n' % w.message)
    for o in held[:6]:
        sys.stderr.write('LIVE-HANDLE: 仍开着 %r（fd=%s）\n'
                         % (getattr(o, 'name', '?'), getattr(o, 'fileno', lambda: '?')()))
    return res.wasSuccessful(), len(leaks), len(held)


if __name__ == '__main__':
    ok, leaks, held = unclosed_handles()
    if leaks or held:
        sys.stderr.write('REGRESSION FAIL: 检出未关闭句柄 %d 枚（析构期可见）＋ %d 枚（跑完仍被引用，'
                         'gc 逼不出、ResourceWarning 也没有——这一类以前从入口看不见）；规格两路都 0 枚\n'
                         % (leaks, held))
    sys.exit(0 if ok and not leaks and not held else 1)
