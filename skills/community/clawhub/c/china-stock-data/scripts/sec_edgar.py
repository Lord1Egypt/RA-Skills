#!/usr/bin/env python3
"""
SEC EDGAR 数据抓取工具
用途：获取美股 13F 持仓、年报(10-K)、季报(10-Q) 等公开数据
合规要点：实名 User-Agent + 限频 ≤8次/秒
"""
import json, sys, os, time

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

try:
    from edgar import set_identity, Company, Filing
    from edgar import CompanySearch
    EDGAR_OK = True
except ImportError:
    EDGAR_OK = False

# === 设置身份（实名！SEC 要求）===
IDENTITY_NAME = "HermesAgent"
IDENTITY_EMAIL = "hermes@nousresearch.com"

if EDGAR_OK:
    set_identity(f"{IDENTITY_NAME} ({IDENTITY_EMAIL})")

def get_13f(cik, year=None):
    """获取某机构 13F 持仓（需要网络通海外）"""
    if not EDGAR_OK:
        return {'error': 'edgartools 未安装', 'fix': 'pip install edgartools'}
    try:
        company = Company(cik)
        # 获取所有 13F  filings
        filings = company.get_filings(form="13F-HR")
        if year:
            filings = filings.filter(year=year)
        results = []
        for f in filings[:5]:
            results.append({
                'cik': cik,
                'form': f.form,
                'date': f.filing_date,
                'accession': f.accession_number,
            })
            time.sleep(0.15)  # 限频
        return {'source': 'SEC EDGAR', 'cik': cik, 'filings': results}
    except Exception as e:
        return {'error': str(e)}

def get_10k(cik, count=3):
    """获取公司年报"""
    if not EDGAR_OK:
        return {'error': 'edgartools 未安装'}
    try:
        company = Company(cik)
        filings = company.get_filings(form="10-K")
        results = []
        for f in filings[:count]:
            results.append({
                'cik': cik,
                'form': f.form,
                'date': f.filing_date,
                'description': f.description[:100] if f.description else '',
            })
            time.sleep(0.15)
        return {'source': 'SEC EDGAR', 'cik': cik, 'filings': results}
    except Exception as e:
        return {'error': str(e)}

def search_company(name):
    """搜索公司"""
    if not EDGAR_OK:
        return {'error': 'edgartools 未安装'}
    try:
        from edgar import CompanySearch
        results = CompanySearch.get_results(name)
        data = []
        for r in results[:10]:
            data.append({'cik': r.cik, 'name': r.company_name})
        return {'source': 'SEC EDGAR', 'query': name, 'results': data}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"usage": """
SEC EDGAR 工具（需海外网络代理）:
  sec search <公司名>         搜索公司CIK
  sec 13f <CIK> [year]       获取13F持仓
  sec 10k <CIK> [count]      获取年报
  sec status                  工具状态

合规提醒:
  - 必须设置实名 User-Agent（已自动配置）
  - 限频 ≤8次/秒（内置 sleep 0.15s）
  - 违规后果: HTTP 429 → IP 限制约10分钟
""", "example": "sec search 伯克希尔  →  查找BRK的CIK"}, ensure_ascii=False))
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'status':
        print(json.dumps({
            'edgartools': '✅已安装' if EDGAR_OK else '❌未安装',
            'identity': f'{IDENTITY_NAME} ({IDENTITY_EMAIL})',
            'rate_limit': '≤8 req/s (sleep 0.15s)',
            'network': '⚠️需要海外代理(等待配Vultr)',
        }, ensure_ascii=False, indent=2))

    elif cmd == 'search':
        name = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        r = search_company(name)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == '13f':
        cik = sys.argv[2] if len(sys.argv) > 2 else ''
        year = sys.argv[3] if len(sys.argv) > 3 else None
        r = get_13f(cik, year)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == '10k':
        cik = sys.argv[2] if len(sys.argv) > 2 else ''
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        r = get_10k(cik, count)
        print(json.dumps(r, ensure_ascii=False, default=str))

    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
