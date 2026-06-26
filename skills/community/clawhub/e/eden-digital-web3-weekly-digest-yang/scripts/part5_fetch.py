#!/usr/bin/env python3
"""
Part.5 上市公司 BTC 持仓动态抓取脚本
数据源：https://www.coinglass.com/zh/BitcoinTreasuries

页面结构（已通过浏览器实测验证）：
  主页可公开抓取：
    · 全市场汇总：单周净流入 BTC/USD、总持仓、持币公司数
    · 持仓排行榜：61 家公司当前持仓快照（排名/代码/国家/持仓/市值）
    · Strategy 周度购买历史（日期/买入BTC/均价/金额/累计持仓）
  各公司详情页 /zh/BitcoinTreasuries/{TICKER}：
    · "比特币持仓变动历史"表格 → 需登录，No data（已实测确认）

抓取方式：Playwright（页面 JS 渲染，curl 无法直接获取表格数据）

运行：
  python3 scripts/part5_fetch.py
  python3 scripts/part5_fetch.py --top 10      # 展示前 N 家（默认 10）
  python3 scripts/part5_fetch.py --headful     # 显示浏览器（调试用）
"""

import sys, re, json, argparse
from datetime import datetime, timezone

SOURCE_URL = 'https://www.coinglass.com/zh/BitcoinTreasuries'
DETAIL_URL = 'https://www.coinglass.com/zh/BitcoinTreasuries/{ticker}'

COUNTRY_ZH = {
    'US': '美国', 'JP': '日本', 'HK': '香港', 'CN': '中国内地',
    'SG': '新加坡', 'AU': '澳大利亚', 'CA': '加拿大', 'GB': '英国',
    'DE': '德国', 'KR': '韩国', 'TW': '台湾', 'CH': '瑞士',
}

def now_zh():
    dt = datetime.now(tz=timezone.utc)
    return f'{dt.year}年{dt.month}月{dt.day}日'

def is_within_days(date_str: str, days: int = 7) -> bool:
    try:
        dt = datetime.strptime(date_str.strip(), '%Y-%m-%d').replace(tzinfo=timezone.utc)
        return 0 <= (datetime.now(tz=timezone.utc) - dt).days <= days
    except ValueError:
        return False

def fetch_data(top: int = 10, headful: bool = False) -> dict:
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print('[ERROR] 请先安装：pip install playwright && playwright install chromium', file=sys.stderr)
        sys.exit(1)

    result = {'companies': [], 'strategy_history': [], 'summary': {}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headful)
        context = browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            ),
            viewport={'width': 1440, 'height': 900},
            locale='zh-CN',
        )
        page = context.new_page()

        print(f'[INFO] 加载 {SOURCE_URL} ...', file=sys.stderr)
        try:
            page.goto(SOURCE_URL, wait_until='networkidle', timeout=30000)
        except PWTimeout:
            print('[WARN] 页面加载超时，继续处理已加载内容', file=sys.stderr)

        try:
            page.wait_for_selector('table', timeout=15000)
        except PWTimeout:
            print('[ERROR] 表格未出现，请用 --headful 排查', file=sys.stderr)
            browser.close()
            return result

        # 滚动触发懒加载，再滚回顶部
        for i in range(1, 6):
            page.evaluate(f'window.scrollTo(0, document.body.scrollHeight * {i} / 5)')
            page.wait_for_timeout(500)
        page.wait_for_timeout(1500)
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_timeout(500)

        # ── 1. 全局汇总（单周净流入、总持仓、持币公司数）─────────────────
        summary_js = r"""
        (() => {
            const lines = document.body.innerText.split('\n')
                .map(l => l.trim()).filter(Boolean);
            const r = {};
            for (let i = 0; i < lines.length; i++) {
                const l = lines[i];
                if (l.includes('单周') && l.includes('净流入')) {
                    r.weekly_usd  = lines[i+1] || '';
                    r.weekly_date = (lines[i+2] || '').replace('截止', '').trim();
                    r.weekly_btc  = lines[i+4] || '';
                    break;
                }
            }
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].includes('持有比特币总量'))   r.total_btc    = lines[i+1] || '';
                if (lines[i].includes('持有比特币总价值')) r.total_value  = lines[i+1] || '';
                if (lines[i].includes('持币公司数'))       r.company_count= lines[i+1] || '';
            }
            return JSON.stringify(r);
        })()
        """
        try:
            result['summary'] = json.loads(page.evaluate(summary_js))
        except Exception as e:
            print(f'[WARN] 汇总解析失败: {e}', file=sys.stderr)

        # ── 2. 持仓排行榜（前 top 家）───────────────────────────────────
        # 实测：表格列顺序 排名/公司名/上市地/交易代码/比特币持仓/持仓价值/占比/市值
        companies_js = f"""
        (() => {{
            const tables = document.querySelectorAll('table');
            let target = null;
            for (const t of tables) {{
                const ths = [...t.querySelectorAll('th')].map(h => h.innerText.trim());
                if (ths.some(h => h.includes('交易代码') || h.includes('上市地'))) {{
                    target = t; break;
                }}
            }}
            if (!target) {{
                target = [...tables].reduce((a, b) =>
                    b.querySelectorAll('tbody tr').length >
                    a.querySelectorAll('tbody tr').length ? b : a
                );
            }}
            const rows = [...target.querySelectorAll('tbody tr')]
                .filter(r => r.querySelectorAll('td').length >= 5)
                .slice(0, {top});
            return JSON.stringify(rows.map(row => {{
                const cells = [...row.querySelectorAll('td')]
                    .map(c => c.innerText.trim().replace(/\\s+/g, ' '));
                const a = row.querySelector('a[href*="BitcoinTreasuries"]');
                return {{
                    rank:     cells[0] || '',
                    name:     cells[1] || '',
                    country:  cells[2] || '',
                    ticker:   cells[3] || '',
                    holdings: cells[4] || '',
                    value:    cells[5] || '',
                    pct:      cells[6] || '',
                    mktcap:   cells[7] || '',
                    href:     a ? a.href : '',
                }};
            }}));
        }})()
        """
        try:
            raw = json.loads(page.evaluate(companies_js))
            result['companies'] = [c for c in raw if c.get('name')]
            print(f'[INFO] 读取 {len(result["companies"])} 家公司', file=sys.stderr)
        except Exception as e:
            print(f'[WARN] 排行榜解析失败: {e}', file=sys.stderr)

        # ── 3. Strategy 周度购买历史 ─────────────────────────────────────
        # 实测：表头 日期/买入BTC数量/平均买入成本/购买金额/比特币持仓
        # 第一行是"总计"汇总行，之后每行是一个周期
        strategy_js = """
        (() => {
            for (const t of document.querySelectorAll('table')) {
                const ths = [...t.querySelectorAll('th')].map(h => h.innerText.trim());
                if (ths.some(h => h.includes('买入BTC') || h.includes('购买金额'))) {
                    const rows = [...t.querySelectorAll('tbody tr')]
                        .filter(r => r.querySelectorAll('td').length >= 4);
                    return JSON.stringify(rows.slice(0, 9).map(row => {
                        const cells = [...row.querySelectorAll('td')]
                            .map(c => c.innerText.trim().replace(/\\s+/g, ' '));
                        return {
                            date:           cells[0] || '',
                            btc_bought:     cells[1] || '',
                            avg_cost:       cells[2] || '',
                            amount_usd:     cells[3] || '',
                            total_holdings: cells[4] || '',
                        };
                    }));
                }
            }
            return JSON.stringify([]);
        })()
        """
        try:
            result['strategy_history'] = json.loads(page.evaluate(strategy_js))
            print(f'[INFO] Strategy 历史: {len(result["strategy_history"])} 条', file=sys.stderr)
        except Exception as e:
            print(f'[WARN] Strategy 历史解析失败: {e}', file=sys.stderr)

        browser.close()

    return result

def print_report(data: dict, top: int) -> None:
    summary   = data.get('summary', {})
    companies = data.get('companies', [])
    history   = data.get('strategy_history', [])

    # 预处理 Strategy 本周变动，供排行榜内嵌
    weekly = [r for r in history
              if re.match(r'\d{4}-\d{2}-\d{2}', r.get('date', ''))]
    this_week = [r for r in weekly if is_within_days(r['date'], 7)]
    strategy_this_week = this_week[0] if this_week else None

    print('=' * 62)
    print('  Part.5  上市公司 BTC 持仓动态')
    print(f'  数据来源：{SOURCE_URL}')
    print(f'  抓取时间：{now_zh()}')
    print('=' * 62)

    # 全市场汇总
    if summary:
        print('\n【全市场本周汇总】')
        btc  = summary.get('weekly_btc', '').strip()
        usd  = summary.get('weekly_usd', '').strip()
        date = summary.get('weekly_date', '').strip()
        if btc or usd:
            print(f'  单周净流入：{btc} BTC  /  {usd}')
            if date:
                print(f'  统计截止：{date}')
        if summary.get('total_btc'):
            print(f'  全市场总持仓：{summary["total_btc"]}')
        if summary.get('total_value'):
            print(f'  总持仓价值：{summary["total_value"]}')
        if summary.get('company_count'):
            print(f'  持币上市公司数：{summary["company_count"]}')

    # 持仓排行榜（只展示 BTC，无 ETH 板块）
    print(f'\n{"─"*62}')
    print(f'  BTC 持仓 TOP {top}')
    print(f'{"─"*62}')

    for c in companies:
        country_zh = COUNTRY_ZH.get(c['country'], c['country']) if c['country'] else ''
        detail_url = c.get('href') or DETAIL_URL.format(ticker=c['ticker'])
        is_strategy = c['ticker'].upper() == 'MSTR'

        print(f'\n【{c["rank"]}】{c["name"]}（{country_zh}）  {c["ticker"]}')
        print(f'  当前持仓：{c["holdings"]} BTC   持仓市值：{c["value"]}   占总供应：{c["pct"]}')
        print(f'  公司市值：{c["mktcap"]}')

        # 仓位变动：Strategy 展示真实数据，其余展示链接
        if is_strategy and strategy_this_week:
            r = strategy_this_week
            print(f'  本周变动：✅ {r["date"]} 买入 +{r["btc_bought"]} BTC'
                  f'  均价 {r["avg_cost"]}  金额 {r["amount_usd"]}')
            print(f'            累计持仓 {r["total_holdings"]} BTC')
        elif is_strategy:
            print(f'  本周变动：ℹ️  本周暂无新购入记录（截至抓取时间）')
        else:
            print(f'  本周变动：⚠️  需登录查看 → {detail_url}')

        print(f'  点评：⚠️（AI 根据公司特征与持仓变动自动生成）')

    # Strategy 近4周趋势（附在最后，供参考）
    if weekly:
        print(f'\n{"─"*62}')
        print('  Strategy（MSTR）近4周购买趋势')
        print(f'{"─"*62}')
        print(f'  {"日期":<13}{"买入BTC":>10}  {"均价":>10}  {"金额":>12}  {"累计持仓":>10}')
        print(f'  {"─"*60}')
        for r in weekly[:4]:
            tag = '  ◀ 本周' if is_within_days(r['date'], 7) else ''
            print(f'  {r["date"]:<13}{r["btc_bought"]:>10}  {r["avg_cost"]:>10}'
                  f'  {r["amount_usd"]:>12}  {r["total_holdings"]:>10}{tag}')

    print(f'\n{"─"*62}')
    print('  ⚠️  数据说明')
    print(f'{"─"*62}')
    print("""
  · 持仓排行榜和 Strategy 购买历史无需登录，Playwright 直接读取
  · 其余公司"持仓变动历史"表格需登录 Coinglass 账号（已实测确认）
  · 如需完整自动化所有公司变动，可考虑 Coinglass Pro API（付费）
""")

def main():
    parser = argparse.ArgumentParser(description='抓取 Coinglass BTC 持仓排行榜')
    parser.add_argument('--top',    type=int, default=10, help='展示前 N 家（默认 10）')
    parser.add_argument('--headful', action='store_true',  help='显示浏览器（调试用）')
    args = parser.parse_args()
    print(f'[INFO] 抓取前 {args.top} 家 + Strategy 周度数据', file=sys.stderr)
    data = fetch_data(top=args.top, headful=args.headful)
    print_report(data, args.top)

if __name__ == '__main__':
    main()
