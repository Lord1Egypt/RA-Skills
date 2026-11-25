#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cocktail-bar-cat 数据体检门禁

用法：python3 scripts/audit.py
每次改动数据文件后运行，出现 FAIL 项即为数据回归。
"""
import json, os, re, sys, collections
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
L = lambda f: json.load(open(f, encoding='utf-8'))
results = []

def check(name, ok, detail, level='FAIL'):
    results.append((level if not ok else 'PASS', name, detail))

# 1. 配方数一致性
rec = L('recipes.json')
n_actual = len(rec['recipes'])
check('配方数一致', rec.get('total') == n_actual,
      f"声明 {rec.get('total')} / 实际 {n_actual}")

# 2. 文档宣称数字一致性
docnums = collections.Counter()
for f in ['SKILL.md', 'README.md']:
    if os.path.exists(f):
        for m in re.finditer(r'(\d{2,3})\s*款配方', open(f, encoding='utf-8').read()):
            docnums[(f, m.group(1))] += 1
doc_ok = all(int(v) == n_actual for _, v in docnums)
check('文档配方数一致', doc_ok,
      '、'.join(f'{f}:{v}' for (f, v), _ in docnums.items()) or '未标注')

# 3. 材料价格覆盖率
ing = collections.Counter()
for r in rec['recipes']:
    for i in r['ingredients']:
        ing[i['name']] += 1
pr = L('prices.json')
pnames = set()
for v in pr.values():
    if isinstance(v, dict):
        for kk in v: pnames.add(kk)
missing = [i for i in ing if i not in pnames]
cov = 1 - len(missing) / len(ing)
check('材料价格覆盖 ≥60%', cov >= 0.6,
      f"{len(ing)} 种材料，{len(missing)} 种无价格，覆盖率 {cov:.0%}",
      level='FAIL' if cov < 0.6 else 'WARN')

# 4. 单位可计价率
PRICEABLE = {'ml', 'g', 'dash', 'drop', 'barspoon', '个', '片', '块', '转'}
units = collections.Counter()
for r in rec['recipes']:
    for i in r['ingredients']:
        units[i.get('unit', '?')] += 1
bad = {u: c for u, c in units.items() if u not in PRICEABLE}
rate = 1 - sum(bad.values()) / sum(units.values())
check('单位可计价 ≥95%', rate >= 0.95,
      f"不可计价单位 {bad or '无'}，可计价率 {rate:.1%}")

# 5. 销量酒名命中配方库
names = {r['name'] for r in rec['recipes']}
sales = L('sales.json')
sold = set()
for d in sales['daily']:
    for it in d.get('items', []): sold.add(it.get('name'))
miss_s = sold - names
check('销量酒名全部命中', not miss_s, f"未命中 {sorted(miss_s)[:5]} 共 {len(miss_s)}")

# 6. 酒单命中配方库
for mf, key in [('menu.json', 'menu'), ('menu_real.json', 'menu')]:
    if not os.path.exists(mf): continue
    m = L(mf)[key]
    mn = []
    for cat, items in m.get('categories', {}).items():
        for it in items: mn.append(it.get('name'))
    miss_m = [x for x in mn if x and x not in names]
    check(f'{mf} 命中配方库', not miss_m, f"未命中 {miss_m[:5]} 共 {len(miss_m)}", level='WARN')

# 7. 重复酒名
dup = [k for k, v in collections.Counter(r['name'] for r in rec['recipes']).items() if v > 1]
check('无重复酒名', not dup, f"重复 {dup}")

# 8. 孤立数据文件（未被 SKILL.md 引用）
skill_md = open('SKILL.md', encoding='utf-8').read()
# 渐进加载后的门禁仍验证完整协议；只加载主文件明确引用的参考文档。
reference_paths = sorted(set(re.findall(r'references/[A-Za-z0-9_-]+\.md', skill_md)) |
                         {name for name in ('FEEDBACK.md', 'CONTRIBUTING.md') if name in skill_md})
protocol_md = skill_md
for reference_path in reference_paths:
    if Path(reference_path).is_file():
        protocol_md += '\n' + Path(reference_path).read_text(encoding='utf-8')
    else:
        check('参考文档可加载', False, reference_path)
orphan = [f for f in sorted(os.listdir('.'))
          if f.endswith('.json') and not f.startswith('_') and f not in skill_md]
check('无孤立数据文件', not orphan, f"未被引用的文件 {orphan}", level='WARN')

# 9. 必备字段完整
REQ = ['name', 'name_en', 'category', 'strength', 'ingredients', 'method',
       'glass', 'garnish', 'cost_estimate', 'suggested_price']
lack = collections.Counter()
for r in rec['recipes']:
    for k in REQ:
        if k not in r or r[k] in (None, '', []): lack[k] += 1
check('配方必备字段完整', not lack, f"缺失 {dict(lack) or '无'}")

# 10. 采购库条目命中配方库（防止改配方后 shopping.json 静默失效）
if os.path.exists('shopping.json'):
    sh = L('shopping.json')
    all_ing = set(ing)
    dead = [b['key'] for b in sh.get('bottles', []) if b['key'] not in all_ing]
    check('采购库条目命中配方库', not dead,
          f"{len(sh.get('bottles', []))} 个条目，零命中 {dead or '无'}", level='WARN')

# 11. 有意思的酒单 · 吧台地图 + 酒单时效完整性（v2.6.1）
if os.path.exists('bar_signatures.json'):
    bs = L('bar_signatures.json')
    src = {s['id'] for s in bs.get('sources', [])}
    bars = bs.get('bars', [])
    bar_names = {b['name'] for b in bars}
    sigs = bs.get('signatures', [])
    errs = []

    # 11.1 顶层策略与诚实边界（v2.6.0 的约束，一条都不能少）
    if bs.get('version') != '2.7.4' or bs.get('distribution_profile') != 'clawhub_mit0':
        errs.append('不是 v2.7.4 ClawHub 独立表达版')
    pol = bs.get('selection_policy', {})
    for k in ('criteria', 'not_ranked_by', 'taste_is_subjective', 'honesty', 'materials'):
        if not pol.get(k):
            errs.append(f'selection_policy 缺 {k}')
    cov = bs.get('coverage', {})
    if cov.get('not_exhaustive') is not True:
        errs.append('coverage.not_exhaustive 不是 true（不得宣称全国全量）')
    if not cov.get('known_gaps'):
        errs.append('coverage 未写明 known_gaps')
    if not cov.get('how_to_extend'):
        errs.append('coverage 未写明 how_to_extend')
    if not bs.get('taste_disclaimer'):
        errs.append('缺 taste_disclaimer（口味主观，不评分不排名）')
    if not bs.get('disclaimer'):
        errs.append('缺 disclaimer（非官方原方声明）')

    # 11.2 v2.6.1 时效策略必须存在（防止再拿旧酒单当现在的招牌）
    fp = bs.get('freshness_policy', {})
    for k in ('principle', 'source_priority', 'photo_sources', 'stale_rule',
              'rotating_menu_rule', 'verify_hint', 'update_hint'):
        if not fp.get(k):
            errs.append(f'freshness_policy 缺 {k}')
    ps = fp.get('photo_sources', {})
    for k in ('where', 'how_to_read', 'date_rule', 'known_platform_limits'):
        if not ps.get(k):
            errs.append(f'freshness_policy.photo_sources 缺 {k}')

    # 11.3 stats 必须与实际数量一致
    st = bs.get('stats', {})
    fd = collections.Counter(b.get('freshness') for b in bars)
    fs = collections.Counter(s.get('freshness') for s in sigs)
    real = {
        'bars': len(bars),
        'cities': len({b.get('city') for b in bars}),
        'signatures': len(sigs),
        'menu_concepts': len(bs.get('menu_concepts', [])),
        'twist_levers': len(bs.get('twist_levers', [])),
        'sources': len(bs.get('sources', [])),
        'independent': sum(1 for b in bars if b.get('tier') in ('独立小店', '社区店', '主题概念店')),
        'recent_bars': fd['recent'], 'aging_bars': fd['aging'],
        'historical_bars': fd['historical'], 'unknown_bars': fd['unknown'],
        'rotating_menus': sum(1 for b in bars if b.get('menu_status') in ('rotating', 'no_menu')),
        'past_menu_signatures': fs['historical'],
        'menu_snapshots': sum(len(b.get('menu_snapshots', [])) for b in bars),
    }
    for k, v in real.items():
        if st.get(k) != v:
            errs.append(f'stats.{k} 记录 {st.get(k)} 实际 {v}')

    # 11.4 店家档案字段、来源引用、签名计数、concept_only 一致性
    bar_ids = [b.get('id') for b in bars]
    if len(bar_ids) != len(set(bar_ids)):
        errs.append('店家 id 重复')
    sig_bars = {s.get('bar') for s in sigs}
    FRESH = ('recent', 'aging', 'historical', 'unknown')
    MENU_STATUS = ('rotating', 'no_menu', 'seasonal', 'stable', 'unknown')
    for b in bars:
        nm = b.get('name')
        for k in ('city', 'region', 'tier', 'menu_idea', 'why_interesting',
                  'menu_concept', 'ideas', 'source_ids'):
            if not b.get(k):
                errs.append(f'{nm} 缺 {k}')
        for sid in b.get('source_ids', []):
            if sid not in src:
                errs.append(f'{nm} 引用了不存在的来源 {sid}')
        exp = sum(1 for s in sigs if s.get('bar') == nm)
        if b.get('signature_count') != exp:
            errs.append(f'{nm} 的 signature_count 记 {b.get("signature_count")} 实际 {exp}')
        if b.get('concept_only') is True and nm in sig_bars:
            errs.append(f'{nm} 标 concept_only=true 却编了 replica 招牌')
        if b.get('concept_only') is False and nm not in sig_bars:
            errs.append(f'{nm} 标 concept_only=false 却没有招牌')
        if b.get('freshness') not in FRESH:
            errs.append(f'{nm} 的 freshness 非法：{b.get("freshness")}')
        if b.get('menu_status') not in MENU_STATUS:
            errs.append(f'{nm} 的 menu_status 非法：{b.get("menu_status")}')
        if not b.get('last_verified'):
            errs.append(f'{nm} 缺 last_verified')

    # 11.5 招牌字段、经典锚点、诚实标注、技术类预处理时间、时效字段
    sig_ids = [s.get('id') for s in sigs]
    if len(sig_ids) != len(set(sig_ids)):
        errs.append('招牌 id 重复')
    TECH = ('油洗', '奶洗', '桶陈', '澄清', '解构', '浸渍', '冷浸', '发酵')
    STATUS = ('current_snapshot', 'aging_snapshot', 'past_menu', 'rotating', 'unknown')
    for s in sigs:
        sid_id = s.get('id')
        if s.get('bar') not in bar_names:
            errs.append(f'{sid_id} 的店名未命中 bars')
        anchor = s.get('classic_anchor')
        if anchor and anchor not in names:
            errs.append(f'{sid_id} 的经典锚点「{anchor}」不在配方库')
        for x in s.get('source_ids', []):
            if x not in src:
                errs.append(f'{sid_id} 引用了不存在的来源 {x}')
        if '非官方原方' not in s.get('replica', {}).get('type', ''):
            errs.append(f'{sid_id} 未标注非官方原方')
        if s.get('verified') is not False:
            errs.append(f'{sid_id} 的 verified 不是 false')
        if len(s.get('twists', [])) < 2:
            errs.append(f'{sid_id} 微调方向少于 2 个')
        if not s.get('why'):
            errs.append(f'{sid_id} 缺「为什么值得复刻」')
        rp = s.get('replica', {})
        blob = rp.get('note', '') + rp.get('method', '')
        if any(x in blob for x in TECH) and not re.search(r'\d+\s*[~~\-至]*\s*\d*\s*(小时|天|h)', blob):
            errs.append(f'{sid_id} 技术类未标预处理时间')
        # v2.6.1：每杯必须能回答「这是哪一期的酒」
        for k in ('menu_snapshot', 'freshness', 'status', 'snapshot_source'):
            if not s.get(k):
                errs.append(f'{sid_id} 缺时效字段 {k}')
        if s.get('freshness') not in FRESH:
            errs.append(f'{sid_id} 的 freshness 非法：{s.get("freshness")}')
        if s.get('status') not in STATUS:
            errs.append(f'{sid_id} 的 status 非法：{s.get("status")}')
        if s.get('snapshot_source') and s['snapshot_source'] not in src:
            errs.append(f'{sid_id} 的 snapshot_source 未命中 sources')
        if s.get('freshness') == 'historical' and s.get('status') != 'past_menu':
            errs.append(f'{sid_id} 是历史款却没标 past_menu')
        # 招牌时效不能优于所属店家太多（近期招牌挂在历史店上要能自洽）
        bf = next((b.get('freshness') for b in bars if b['name'] == s.get('bar')), None)
        if bf == 'historical' and s.get('freshness') == 'recent' and not s.get('menu_snapshot', '').startswith('202'):
            errs.append(f'{sid_id} 挂在历史店上却标 recent 且无新快照日期')

    # 11.6 酒单骨架 / 微调手法结构完整
    for c in bs.get('menu_concepts', []):
        if c.get('bar') not in bar_names:
            errs.append(f'酒单骨架 {c.get("name")} 的店名未命中 bars')
        if not c.get('how') or not c.get('why'):
            errs.append(f'酒单骨架 {c.get("name")} 缺 how/why')
    for lv in bs.get('twist_levers', []):
        if not lv.get('name') or not lv.get('how') or not lv.get('effect'):
            errs.append(f'微调手法 {lv.get("id")} 字段不全')

    # 11.7 多期酒单快照（v2.6.1）：日期、来源、酒款、时效都要齐
    for b in bars:
        for sn in b.get('menu_snapshots', []):
            for k in ('as_of', 'label', 'theme', 'drinks', 'freshness', 'source_ids', 'note'):
                if not sn.get(k):
                    errs.append(f"{b['name']} 的快照 {sn.get('as_of')} 缺 {k}")
            if sn.get('freshness') not in FRESH:
                errs.append(f"{b['name']} 的快照 freshness 非法")
            for sid in sn.get('source_ids', []):
                if sid not in src:
                    errs.append(f"{b['name']} 的快照引用了不存在的来源 {sid}")
    # 换季型吧台必须写到店前提醒
    for b in bars:
        if b.get('menu_status') in ('rotating', 'no_menu') and not b.get('current_menu_advice'):
            errs.append(f"{b['name']} 是换季/无酒单吧台却缺 current_menu_advice")

    # 11.8 无锚点必须写说明，别硬凑经典
    null_anchor = [s['id'] for s in sigs if not s.get('classic_anchor') and not s.get('anchor_note')]
    if null_anchor:
        errs.append(f'无锚点却未写 anchor_note 说明：{null_anchor[:3]}')

    # 11.9 v2.6.2：运行时时效可解析、阈值一致、无未来快照
    import datetime as _dt
    today = _dt.date.today()

    def snap_date(text):
        s = str(text or '')
        m = re.search(r'(20\d{2})-(\d{1,2})-(\d{1,2})', s)
        if m:
            try:
                return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                pass
        ys = [int(y) for y in re.findall(r'20\d{2}', s)]
        return _dt.date(max(ys), 1, 1) if ys else None

    def eff(text):
        sd = snap_date(text)
        if sd is None:
            return 'unknown'
        m = max(0, int((today - sd).days / 30.44))
        return 'recent' if m <= 18 else ('aging' if m <= 48 else 'historical')

    bad_date = [s['id'] for s in sigs if snap_date(s.get('menu_snapshot')) is None]
    future = [s['id'] for s in sigs
              if snap_date(s.get('menu_snapshot')) and snap_date(s.get('menu_snapshot')) > today]
    if bad_date:
        errs.append(f'快照日期无法解析：{bad_date[:3]}')
    if future:
        errs.append(f'快照日期在未来：{future[:3]}')
    fc = fp.get('freshness_computation', {})
    th = fc.get('thresholds_months', {})
    if th.get('recent') != 18 or th.get('aging') != 48:
        errs.append('freshness_computation.thresholds_months 不是 18/48')
    bars_src = open('scripts/bars.py', encoding='utf-8').read()
    if 'FRESH_RECENT_MONTHS = 18' not in bars_src or 'FRESH_AGING_MONTHS = 48' not in bars_src:
        errs.append('bars.py 时效阈值与 JSON 不一致')
    for key in ('rule', 'as_of_default', 'as_of_override', 'static_field', 'why'):
        if not fc.get(key):
            errs.append(f'freshness_computation 缺 {key}')
    drift_b = sum(1 for b in bars
                  if b.get('freshness') != eff(b.get('source_date') or b.get('last_verified')))
    drift_s = sum(1 for s in sigs if s.get('freshness') != eff(s.get('menu_snapshot')))
    check('时效基线漂移（预期）', True,
          f'{drift_b} 家店 / {drift_s} 杯与建档标签不同，运行时自动纠偏；--as-of 可复现')

    check('吧台地图+时效完整', not errs,
          f"{real['bars']} 家 / {real['cities']} 城市 / {real['signatures']} 杯 / "
          f"{real['menu_snapshots']} 期快照；问题 {errs[:5] or '无'} 共 {len(errs)}")
else:
    check('吧台地图+时效完整', False, 'bar_signatures.json 缺失')

# 12. v2.6.3：使用反馈通道隐私门禁（不联网、不写盘、不回传）
fb_path = 'scripts/feedback.py'
fb_src = open(fb_path, encoding='utf-8').read() if os.path.exists(fb_path) else ''
fb_md = open('FEEDBACK.md', encoding='utf-8').read() if os.path.exists('FEEDBACK.md') else ''
fb_errs = []
if not fb_src:
    fb_errs.append('scripts/feedback.py 缺失')
if not fb_md:
    fb_errs.append('FEEDBACK.md 缺失')
for t in ('urllib', 'requests', 'socket', 'http.client', 'httpx', 'aiohttp'):
    if t in fb_src:
        fb_errs.append(f'反馈脚本出现网络能力 {t}')
if re.search(r'open\([^)]*[\'\"]w', fb_src) or '.write(' in fb_src or 'json.dump(' in fb_src:
    fb_errs.append('反馈脚本出现写盘调用')
for key in ('不联网', '不回传', '反馈模式', '隐私红线', '回告',
            'FEEDBACK_CHANNEL', '三层', '判定表', '不打扰三原则'):
    if key not in fb_md:
        fb_errs.append(f'FEEDBACK.md 缺 {key}')
if '使用反馈' not in protocol_md or 'FEEDBACK.md' not in skill_md:
    fb_errs.append('SKILL.md 缺使用反馈协议路由')
head = '\n'.join(skill_md.splitlines()[:120])
if '反馈模式 · 前置规则' not in head:
    fb_errs.append('SKILL.md 前置规则不在文档前部（渐进加载会漏读）')
for key in ('L1 触发', 'L2 判定', 'L3 产物', '信号判定表', '任务内纠正',
            '元层评价', '不打扰三原则', '回到原任务'):
    if key not in protocol_md:
        fb_errs.append(f'SKILL.md 缺 {key}')
if '--copy' not in fb_src:
    fb_errs.append('feedback.py 缺 --copy')
check('反馈通道实现门禁', not fb_errs,
      f'前置规则/四类判定/不打扰/隐私；问题 {fb_errs[:4] or "无"} 共 {len(fb_errs)}')

# 13. v2.7.0：历史证据链与创作边界；结构校验不冒充原文核验
try:
    import history as _history
    hd = L('cocktail_history.json')
    history_errs = _history.validate(hd, rec['recipes'])
    history_ids = {r['id'] for r in hd.get('records', [])}
    story_data = L('cocktail_stories.json')
    for story in story_data.get('stories', []):
        for rid in story.get('history_record_ids', []):
            if rid not in history_ids:
                history_errs.append(f"故事 {story.get('name')} 引用未知历史 {rid}")
        if not story.get('history_status'):
            history_errs.append(f"故事 {story.get('name')} 无证据等级")
        if story.get('quote_type') != 'original_bar_copy_not_historical_quote':
            history_errs.append(f"故事 {story.get('name')} 文案冒充史料引语")
    for token in ('7.3 原始文献', '7.5 万变不离其宗', 'scripts/history.py', '历史文献', '单变量'):
        if token not in protocol_md:
            history_errs.append(f'SKILL.md 缺历史路由 {token}')
    check('历史证据+创作门禁', not history_errs,
          f"{len(hd.get('records', []))} 主题 / {len(hd.get('sources', []))} 来源 / "
          f"{len(hd.get('families', []))} 家族；问题 {history_errs[:5] or '无'} 共 {len(history_errs)}")
except (OSError, ValueError, KeyError, ImportError) as exc:
    check('历史证据+创作门禁', False, f'历史模块不可用：{exc}')

# 14. v2.7.1：每次发版必须有可供上传读取的最新中文说明
release_errs = []
version_match = re.search(r'^version:\s*(\S+)', skill_md, re.M)
date_match = re.search(r'^last_updated:\s*"([^"\n]+)"', skill_md, re.M)
release_version = version_match.group(1) if version_match else ''
release_date = date_match.group(1) if date_match else ''
try:
    release_md = open('RELEASE_NOTES.md', encoding='utf-8').read()
    readme_md = open('README.md', encoding='utf-8').read()
    listing_md = open('LISTING.md', encoding='utf-8').read()
    title = re.search(r'^## 最新版本：v(\S+) · (\d{4}-\d{2}-\d{2})$', release_md, re.M)
    if not title or (title.group(1), title.group(2)) != (release_version, release_date):
        release_errs.append('最新说明版本/日期与SKILL元信息不一致')
    latest = release_md.split('\n---\n', 1)[0]
    copy = re.search(r'### 上架可复制文案[^\n]*\n\s*```text\n(.*?)\n```', latest, re.S)
    text = copy.group(1).strip() if copy else ''
    if not text or not text.startswith(f'v{release_version}｜'):
        release_errs.append('最新中文上架文案缺失/版本不一致')
    for filename, body in (('SKILL.md', skill_md), ('README.md', readme_md)):
        snippet = re.search(r'<!-- latest-release:start -->\s*(.*?)\s*<!-- latest-release:end -->', body, re.S)
        if not snippet or snippet.group(1).strip() != text:
            release_errs.append(f'{filename}最新摘要与单一来源不一致')
        if f'本次更新 · v{release_version} · {release_date}' not in '\n'.join(body.splitlines()[:60]):
            release_errs.append(f'{filename}最新版本/日期未放在开头')
    listing_copy = re.search(r'### 上架可复制文案[^\n]*\n\s*```text\n(.*?)\n```', listing_md, re.S)
    if not listing_copy or listing_copy.group(1).strip() != text:
        release_errs.append('LISTING.md上架文案与单一来源不一致')
    if f'| 版本 | {release_version} |' not in listing_md:
        release_errs.append('LISTING.md版本未同步')
    if f'| v{release_version} | {release_date} |' not in protocol_md:
        release_errs.append('SKILL.md技术日志未同步版本/日期')
    for token in ('### 本次新增', '### 本次优化', '### 兼容与边界', '### 验证'):
        if token not in latest:
            release_errs.append(f'最新说明缺{token}')
    if '每次发版必做' not in '\n'.join(skill_md.splitlines()[:120]):
        release_errs.append('固定发版规则未前置')
    if '## 维护者固定发版流程' not in release_md:
        release_errs.append('缺固定发版流程')
except OSError as exc:
    release_errs.append(f'版本说明不可用：{exc}')
check('版本说明一致性门禁', not release_errs,
      f'v{release_version} / {release_date}；问题 {release_errs[:5] or "无"} 共 {len(release_errs)}')

# 15. 公开版门禁：空业务模板、合成价格算术、配方规格与文件范围分层检查。
try:
    import io as _io
    import unittest as _unittest
    import test_public as _public
    _buffer = _io.StringIO()
    _suite = _unittest.defaultTestLoader.loadTestsFromTestCase(_public.PublicTests)
    _result = _unittest.TextTestRunner(stream=_buffer).run(_suite)
    check('公开模板+隐私+金额', _result.wasSuccessful(),
          f'{_result.testsRun}项公开检查；' + ('全部通过' if _result.wasSuccessful() else _buffer.getvalue()))
except (OSError, ValueError, ImportError) as exc:
    check('公开模板+隐私+金额', False, str(exc))

print(f"\n{'='*56}\n cocktail-bar-cat 数据体检  ({n_actual} 款配方)\n{'='*56}")
for st, name, detail in results:
    mark = {'PASS': '  OK  ', 'WARN': ' WARN ', 'FAIL': ' FAIL '}[st]
    print(f"[{mark}] {name:<16} {detail}")
fails = [r for r in results if r[0] == 'FAIL']
warns = [r for r in results if r[0] == 'WARN']
print(f"\n结果：{len(results)-len(fails)-len(warns)} 通过 / {len(warns)} 警告 / {len(fails)} 失败")
print(f"材料总数 {len(ing)} 种，其中无价格 {len(missing)} 种")
sys.exit(1 if fails else 0)
