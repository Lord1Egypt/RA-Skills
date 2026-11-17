#!/usr/bin/env python3
"""
selftest.py — bid-opportunity-advisor 一键自测（stdlib only）

从 demo/ 夹具出发，端到端验证：
  1) 解析：fetch_ccgp.parse_listing 正确解析 listing
  2) 合并：fetch_ccgp.parse_detail + apply_detail 正确补全金额/供应商
  3) 去重：opportunity_engine.dedup_records 跨源同项目只计一次
  4) 引擎：opportunity_engine 全链路不崩溃，报告无破损格式化
     （含 discount_stats 为空时的崩溃回归）
  5) ceb 解析：fetch_ceb.parse_ceb_detail 解析「表格 td / 标签值」两种形态，
     字段正确且 schema 与 ccgp 记录一致（可混合喂引擎）

运行：从技能根目录
  python scripts/selftest.py
"""

import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DEMO = SKILL / 'demo'
sys.path.insert(0, str(SKILL / 'scripts'))

import fetch_ccgp as fc
import opportunity_engine as oe

DETAIL_URL = 'https://www.ccgp.gov.cn/cggg/zbgg/2026/08/02/t_2.htm'


def _fail(msg):
    print(f'  ❌ FAIL: {msg}')
    sys.exit(1)


def test_parse_and_merge():
    print('[1] 解析 + 合并 ...')
    html = (DEMO / 'test_listing.html').read_text(encoding='utf-8')
    items = fc.parse_listing(html)
    if len(items) != 3:
        _fail(f'parse_listing 应得 3 条，实际 {len(items)}')
    recs = fc.build_records(items)
    dhtml = (DEMO / 'test_detail_t2.html').read_text(encoding='utf-8')
    dd = fc.parse_detail(dhtml)
    merged = False
    for r in recs:
        if r['source_url'] == DETAIL_URL:
            fc.apply_detail(r, dd)
            merged = True
    if not merged:
        _fail('未找到可合并的详情记录')
    r = next(x for x in recs if x['source_url'] == DETAIL_URL)
    if r['win_company'] != '云南新秦云科技有限公司':
        _fail(f'win_company 错误: {r["win_company"]!r}')
    if r['win_amount'] != 4800000:
        _fail(f'win_amount 错误: {r["win_amount"]!r}')
    if r['budget_amount'] != 5000000:
        _fail(f'budget_amount 错误: {r["budget_amount"]!r}')
    print('  ✅ 解析 3 条 / 合并 win_company+金额 正确')
    return recs


def test_dedup(recs):
    print('[2] 跨源去重 ...')
    dup = dict(recs[0])
    dup['source_platform'] = '中国招标投标公共服务平台'
    dup['source_url'] = 'https://bulletin.cebpubservice.com/xxx'
    merged, removed = oe.dedup_records(recs + [dup])
    if removed != 1:
        _fail(f'应移除 1 条重复，实际 {removed}')
    if len(merged) != len(recs):
        _fail(f'去重后数量应为 {len(recs)}，实际 {len(merged)}')
    print('  ✅ 跨源同名同采购人同日期 → 移除 1 条')
    return merged


def test_multisource_dedup():
    print('[4] 多源真实样本去重 ...')
    raw = json.loads((DEMO / 'multisource_real.json').read_text(encoding='utf-8'))
    # 20 ccgp 真实 + 3 cebpubservice 真实 + 1 受控跨源重复(ccgp 记录[0] 在 ceb 重发)
    deduped, removed = oe.dedup_records(raw)
    if removed != 1:
        _fail(f'多源样本应移除 1 条跨源重复，实际 {removed}')
    if len(deduped) != len(raw) - 1:
        _fail(f'多源去重后数量异常: {len(deduped)}')
    m = next((r for r in deduped if r.get('buyer') == '昆明理工大学'), None)
    if not m or m.get('win_company') is None:
        _fail('跨源合并后中标人丢失（应保留 ccgp 中标侧）')
    ceb_names = {'中国建设银行股份有限公司四川省分行四川大学智慧校园建设项目',
                 '湖北大学知行学院校银合作—智慧校园工程总承包',
                 '2026年都匀二中数字化校园建设项目'}
    kept = [r for r in deduped if r.get('project_name') in ceb_names]
    if len(kept) != 3:
        _fail(f'真实 ceb 项目被误合并：保留 {len(kept)} (应为 3)')
    print('  ✅ 20 ccgp + 3 ceb + 1跨源重复 → 移除1，字段合并保留中标人，无假合并')


def test_ceb_parse():
    print('[5] ceb 详情页解析（两种形态 + schema 一致性）...')
    import fetch_ceb as fe
    a = fe.parse_ceb_detail((DEMO / 'test_ceb_detail_table.html').read_text(encoding='utf-8'))
    if a['type'] != '招标':
        _fail(f'ceb 表格形态 type 错: {a["type"]!r}')
    if a['buyer'] != '中国建设银行股份有限公司四川省分行':
        _fail(f'ceb buyer 错: {a["buyer"]!r}')
    if a['budget_amount'] != 11015000:
        _fail(f'ceb budget 错: {a["budget_amount"]!r}')
    if a['region'] != '四川':
        _fail(f'ceb region 错: {a["region"]!r}')
    if a['publish_date'] != '2026-06-03':
        _fail(f'ceb publish_date 错: {a["publish_date"]!r}')
    if a['source_platform'] != '中国招标投标公共服务平台':
        _fail('ceb source_platform 错')
    b = fe.parse_ceb_detail((DEMO / 'test_ceb_detail_text.html').read_text(encoding='utf-8'))
    if b['type'] != '中标':
        _fail(f'ceb 文本形态 type 错: {b["type"]!r}')
    if b['win_company'] != '武汉智联信息技术有限公司':
        _fail(f'ceb win_company 错: {b["win_company"]!r}')
    if b['win_amount'] != 24800000:
        _fail(f'ceb win_amount 错: {b["win_amount"]!r}')
    # schema 一致性：ceb 记录键集须与 ccgp 记录一致，方可混入同一 records 喂引擎
    ccgp_item = {'title': 't', 'ann_type': '', 'buyer': None, 'agency': None,
                 'province_hint': None, 'publish_date': None, 'url': 'u'}
    ccgp_keys = set(fc.to_record(ccgp_item).keys())
    if set(a.keys()) != ccgp_keys:
        _fail(f'ceb 记录 schema 与 ccgp 不一致: {set(a.keys()) ^ ccgp_keys}')
    print('  ✅ 表格/文本两形态解析正确，schema 与 ccgp 一致（可混合喂引擎）')


def test_ima_real_samples():
    """[6] IMA 知识库真实招标文件解析回归（锁定 7 处真实缺陷修复）。

    两份样本来自 IMA「招标文件、采购文件汇集」知识库真实公告：
      - 贵州大学2026年软件工程学科平台设备采购（两级结构 + 预算带单位括号）
      - 中华人民共和国深圳海关RPA机器人采购项目（仅写城市名 + 落款日期为发布日）
    """
    print('[6] IMA 真实样本解析（两级结构/城市回推/发布日回退）...')
    import fetch_ceb as fe
    gzu = fe.parse_ceb_detail((DEMO / 'ima_real' / 'gzu_software_platform.html').read_text(encoding='utf-8'))
    sz = fe.parse_ceb_detail((DEMO / 'ima_real' / 'szcustoms_rpa.html').read_text(encoding='utf-8'))
    # 贵州大学：两级结构「采购人信息 / 名 称：」+ 预算「（元）：5500000.00」+ 发布日取文件获取起始
    if gzu['buyer'] != '贵州大学':
        _fail(f'gzu buyer 错: {gzu["buyer"]!r}')
    if gzu['agency'] != '贵州新阳光项目管理有限公司':
        _fail(f'gzu agency 错: {gzu["agency"]!r}')
    if gzu['budget_amount'] != 5500000:
        _fail(f'gzu budget_amount 错: {gzu["budget_amount"]!r}')
    if gzu['region'] != '贵州':
        _fail(f'gzu region 错: {gzu["region"]!r}')
    if gzu['publish_date'] != '2026-06-12':
        _fail(f'gzu publish_date 错: {gzu["publish_date"]!r}')
    # 深圳海关：仅城市名 → 回推广东；发布日取文末落款（非投标截止日）
    if sz['buyer'] != '中华人民共和国深圳海关':
        _fail(f'sz buyer 错: {sz["buyer"]!r}')
    if sz['agency'] != '采联国际招标采购集团有限公司':
        _fail(f'sz agency 错: {sz["agency"]!r}')
    if sz['budget_amount'] != 795000:
        _fail(f'sz budget_amount 错: {sz["budget_amount"]!r}')
    if sz['region'] != '广东':
        _fail(f'sz region 错: {sz["region"]!r}')
    if sz['publish_date'] != '2025-06-05':
        _fail(f'sz publish_date 错: {sz["publish_date"]!r}')
    print('  ✅ 两级结构/城市回推/发布日三级回退 全部正确')


def test_engine_pipeline(records):
    print('[3] 引擎全链路（含折扣为空回归）...')
    profile = json.loads((DEMO / 'test_profile.json').read_text(encoding='utf-8'))
    # 正常有中标记录的样本
    _run_report(records, profile, '有中标样本')
    # 全为招标(无中标) → discount_stats 为空，验证不再崩溃
    listings_only = [dict(r, type='招标', win_company=None, win_amount=None) for r in records]
    _run_report(listings_only, profile, '无中标样本(折扣为空)')
    print('  ✅ 引擎无崩溃，报告无破损格式化')


def _run_report(records, profile, label):
    trend = oe.analyze_trends(records)
    winner = oe.analyze_winners(records)
    price = oe.analyze_prices(records)
    fit = oe.compute_fit(records, profile)
    ra = oe.compute_regional_access(records, profile)
    opp = oe.opportunity_score(trend, winner, price, ra)
    conf = oe.confidence(len(records))
    gng = oe.go_no_go(fit[0] if fit[0] is not None else 0, opp['total'], conf, profile is not None)
    html = oe.html_report(records, trend, winner, price, fit, ra, opp, conf, gng, profile)
    if '投标机会分析报告' not in html:
        _fail(f'{label}: 报告标题缺失')
    if 'NaN' in html or 'n/a%' in html:
        _fail(f'{label}: 报告含破损格式化 (NaN / n/a%)')
    print(f'  · {label}: 报告 OK（{len(html)} 字节）')


if __name__ == '__main__':
    recs = test_parse_and_merge()
    recs = test_dedup(recs)
    test_multisource_dedup()
    test_ceb_parse()
    test_ima_real_samples()
    test_engine_pipeline(recs)
    print('\n✅ ALL SELF-TESTS PASSED')
