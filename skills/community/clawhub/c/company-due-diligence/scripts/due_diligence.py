#!/usr/bin/env python3
"""
尽职调查主脚本

使用方法:
    # 完整尽调
    python scripts/due_diligence.py "公司名称" --full

    # 仅基本信息
    python scripts/due_diligence.py "公司名称" --basic

    # 仅诉讼记录
    python scripts/due_diligence.py "公司名称" --litigation

    # 仅失信信息
    python scripts/due_diligence.py "公司名称" --dishonest
"""

import os
import sys
import json
import time
import random
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("⚠ Playwright 未安装，部分功能不可用")
    print("  安装: pip install playwright && playwright install chromium")

import requests
from bs4 import BeautifulSoup


class DueDiligence:
    """尽职调查类"""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.credentials = self._load_credentials()
        self.results = {
            "company_name": "",
            "query_time": datetime.now().isoformat(),
            "basic_info": {},
            "financial_info": {},
            "legal_info": {},
            "news_info": {}
        }

    def _load_credentials(self) -> Optional[Dict]:
        """加载登录凭证"""
        try:
            from setup_credentials import load_credentials
            return load_credentials()
        except:
            return None

    def _init_browser(self):
        """初始化浏览器"""
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright 未安装")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = self.context.new_page()

    def _close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()

    def _random_delay(self, min_sec: float = 2, max_sec: float = 5):
        """随机延迟"""
        time.sleep(random.uniform(min_sec, max_sec))

    # ==================== 基本信息查询 ====================

    def query_basic_info_tianyancha(self, company_name: str) -> Dict:
        """通过天眼查查询基本信息"""
        if not HAS_PLAYWRIGHT:
            return {"error": "Playwright 未安装"}

        if not self.credentials or "tianyancha" not in self.credentials:
            return {"error": "天眼查凭证未配置，请运行 setup_credentials.py"}

        if not self.browser:
            self._init_browser()

        print(f"正在通过天眼查查询: {company_name}")

        try:
            # 登录
            creds = self.credentials["tianyancha"]
            self.page.goto("https://www.tianyancha.com/login")
            self._random_delay()

            # 切换到密码登录
            self.page.click("text=密码登录", timeout=5000)
            self._random_delay(1, 2)

            # 输入账号密码
            self.page.fill('input[placeholder*="手机号"]', creds["username"])
            self.page.fill('input[placeholder*="密码"]', creds["password"])
            self._random_delay(1, 2)

            # 点击登录
            self.page.click("button:has-text('登录')")
            self._random_delay(3, 5)

            # 搜索公司
            self.page.goto("https://www.tianyancha.com/")
            self._random_delay()

            self.page.fill('input[placeholder*="公司名"]', company_name)
            self.page.press('input[placeholder*="公司名"]', 'Enter')
            self._random_delay(2, 4)

            # 点击第一个结果
            self.page.click('.search-result-item:first-child a', timeout=10000)
            self._random_delay(2, 4)

            # 提取数据
            data = {
                "name": self.page.text_content('.company-name', timeout=5000) or "",
                "legal_person": self.page.text_content('.legal-person', timeout=5000) or "",
                "capital": self.page.text_content('.capital', timeout=5000) or "",
                "establish_date": self.page.text_content('.establish-date', timeout=5000) or "",
                "status": self.page.text_content('.company-status', timeout=5000) or "",
                "source": "天眼查",
                "query_url": self.page.url
            }

            print(f"✓ 天眼查查询完成")
            return data

        except Exception as e:
            print(f"✗ 天眼查查询失败: {e}")
            return {"error": str(e)}

    def query_basic_info_qichacha(self, company_name: str) -> Dict:
        """通过企查查查询基本信息"""
        if not HAS_PLAYWRIGHT:
            return {"error": "Playwright 未安装"}

        if not self.credentials or "qichacha" not in self.credentials:
            return {"error": "企查查凭证未配置"}

        if not self.browser:
            self._init_browser()

        print(f"正在通过企查查查询: {company_name}")

        try:
            creds = self.credentials["qichacha"]
            self.page.goto("https://www.qcc.com/")
            self._random_delay()

            # 登录流程（简化版，实际可能需要调整）
            self.page.click("text=登录", timeout=5000)
            self._random_delay(1, 2)

            self.page.click("text=密码登录", timeout=5000)
            self._random_delay(1, 2)

            self.page.fill('input[placeholder*="手机号"]', creds["username"])
            self.page.fill('input[placeholder*="密码"]', creds["password"])
            self._random_delay(1, 2)

            self.page.click("button:has-text('登录')")
            self._random_delay(3, 5)

            # 搜索
            self.page.fill('input[placeholder*="搜索"]', company_name)
            self.page.press('input[placeholder*="搜索"]', 'Enter')
            self._random_delay(2, 4)

            # 提取数据（简化版）
            data = {
                "name": company_name,
                "source": "企查查",
                "query_url": self.page.url
            }

            print(f"✓ 企查查查询完成")
            return data

        except Exception as e:
            print(f"✗ 企查查查询失败: {e}")
            return {"error": str(e)}

    # ==================== 上市公司查询 ====================

    def query_listed_company(self, company_name: str) -> Dict:
        """查询上市公司信息（巨潮资讯）"""
        print(f"正在查询上市公司信息: {company_name}")

        try:
            # 搜索公司
            search_url = "http://www.cninfo.com.cn/new/fulltextSearch"
            params = {
                'searchtype': 'company',
                'keyword': company_name
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            companies = []
            for item in soup.select('.company-item')[:5]:
                name_elem = item.select_one('.company-name')
                code_elem = item.select_one('.stock-code')

                if name_elem and code_elem:
                    companies.append({
                        'name': name_elem.text.strip(),
                        'code': code_elem.text.strip()
                    })

            if not companies:
                return {"is_listed": False, "message": "未找到上市公司信息"}

            # 获取第一个匹配的公司详情
            company = companies[0]
            print(f"✓ 找到上市公司: {company['name']} ({company['code']})")

            return {
                "is_listed": True,
                "name": company['name'],
                "code": company['code'],
                "source": "巨潮资讯网",
                "query_url": f"http://www.cninfo.com.cn/new/disclosure/stock?stockCode={company['code']}"
            }

        except Exception as e:
            print(f"✗ 上市公司查询失败: {e}")
            return {"error": str(e)}

    # ==================== 诉讼查询 ====================

    def query_litigation(self, company_name: str) -> Dict:
        """查询诉讼记录（获取查询指引）"""
        print(f"正在获取诉讼查询指引: {company_name}")

        return {
            "company_name": company_name,
            "source": "中国裁判文书网",
            "query_url": "http://wenshu.court.gov.cn/",
            "search_keywords": [
                company_name,
                f'"{company_name}"',
                f'被告:{company_name}',
                f'原告:{company_name}',
            ],
            "tips": [
                "1. 访问裁判文书网: http://wenshu.court.gov.cn/",
                "2. 输入验证码",
                "3. 在当事人栏输入公司名称",
                "4. 按时间倒序排列查看最新案件",
                "5. 重点关注作为被告的案件"
            ],
            "manual_query_required": True,
            "note": "裁判文书网有验证码，需手动查询"
        }

    # ==================== 失信查询 ====================

    def query_dishonest(self, company_name: str) -> Dict:
        """查询失信信息（获取查询指引）"""
        print(f"正在获取失信查询指引: {company_name}")

        return {
            "company_name": company_name,
            "source": "中国执行信息公开网",
            "query_urls": {
                "失信被执行人": "http://zxgk.court.gov.cn/shixin/",
                "被执行人": "http://zxgk.court.gov.cn/zhixing/",
                "限制消费": "http://zxgk.court.gov.cn/xiaofei/"
            },
            "tips": [
                "1. 访问执行信息公开网: http://zxgk.court.gov.cn/",
                "2. 选择查询类型（失信/被执行/限制消费）",
                "3. 输入验证码",
                "4. 在名称栏输入公司名称",
                "5. 查看是否有相关记录"
            ],
            "manual_query_required": True,
            "note": "执行信息公开网有验证码，需手动查询"
        }

    # ==================== 舆情查询 ====================

    def query_news(self, company_name: str, keywords: List[str] = None) -> Dict:
        """查询舆情信息"""
        print(f"正在查询舆情信息: {company_name}")

        query = company_name
        if keywords:
            query += " " + " ".join(keywords)

        try:
            url = "https://www.baidu.com/s"
            params = {
                'wd': query,
                'tn': 'news',
                'rtt': '1',  # 按时间排序
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, params=params, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            news = []
            for item in soup.select('.result')[:10]:
                title_elem = item.select_one('h3 a')
                source_elem = item.select_one('.c-showurl')
                date_elem = item.select_one('.c-color-gray')

                if title_elem:
                    news.append({
                        'title': title_elem.text.strip(),
                        'url': title_elem.get('href', ''),
                        'source': source_elem.text.strip() if source_elem else '',
                        'date': date_elem.text.strip() if date_elem else ''
                    })

            print(f"✓ 找到 {len(news)} 条相关新闻")
            return {
                "company_name": company_name,
                "news_count": len(news),
                "news": news,
                "source": "百度新闻"
            }

        except Exception as e:
            print(f"✗ 舆情查询失败: {e}")
            return {"error": str(e)}

    # ==================== 主流程 ====================

    def run(self, company_name: str, mode: str = "full") -> Dict:
        """执行尽职调查"""
        self.results["company_name"] = company_name

        print("=" * 60)
        print(f"尽职调查: {company_name}")
        print(f"模式: {mode}")
        print("=" * 60)
        print()

        try:
            if mode in ["full", "basic"]:
                # 查询基本信息
                print("\n【1/5】查询基本信息...")

                # 先查上市公司（免费且可靠）
                listed_info = self.query_listed_company(company_name)
                self.results["basic_info"]["listed"] = listed_info

                # 再查天眼查/企查查
                if self.credentials:
                    if "tianyancha" in self.credentials:
                        self.results["basic_info"]["tianyancha"] = \
                            self.query_basic_info_tianyancha(company_name)
                    elif "qichacha" in self.credentials:
                        self.results["basic_info"]["qichacha"] = \
                            self.query_basic_info_qichacha(company_name)
                else:
                    print("⚠ 未配置天眼查/企查查凭证，跳过工商信息查询")
                    print("  运行 python scripts/setup_credentials.py 配置")

            if mode in ["full", "litigation"]:
                print("\n【2/5】查询诉讼记录...")
                self.results["legal_info"]["litigation"] = self.query_litigation(company_name)

            if mode in ["full", "dishonest"]:
                print("\n【3/5】查询失信信息...")
                self.results["legal_info"]["dishonest"] = self.query_dishonest(company_name)

            if mode in ["full", "news"]:
                print("\n【4/5】查询舆情信息...")
                self.results["news_info"] = self.query_news(
                    company_name,
                    keywords=["风险", "诉讼", "处罚"]
                )

            print("\n【5/5】整理结果...")
            self.results["query_time"] = datetime.now().isoformat()

            print("\n" + "=" * 60)
            print("✓ 尽职调查完成")
            print("=" * 60)

            return self.results

        finally:
            self._close_browser()


def main():
    parser = argparse.ArgumentParser(description="企业尽职调查")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--full", action="store_true", help="完整尽调")
    parser.add_argument("--basic", action="store_true", help="仅基本信息")
    parser.add_argument("--litigation", action="store_true", help="仅诉讼记录")
    parser.add_argument("--dishonest", action="store_true", help="仅失信信息")
    parser.add_argument("--news", action="store_true", help="仅舆情信息")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")

    args = parser.parse_args()

    # 确定模式
    mode = "basic"
    if args.full:
        mode = "full"
    elif args.litigation:
        mode = "litigation"
    elif args.dishonest:
        mode = "dishonest"
    elif args.news:
        mode = "news"

    # 执行查询
    dd = DueDiligence(headless=not args.no_headless)
    results = dd.run(args.company, mode=mode)

    # 输出结果
    if args.format == "json":
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output = format_text(results)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n结果已保存到: {args.output}")
    else:
        print("\n" + output)


def format_text(results: Dict) -> str:
    """格式化为文本"""
    lines = []
    lines.append(f"尽职调查报告")
    lines.append("=" * 50)
    lines.append(f"公司名称: {results['company_name']}")
    lines.append(f"查询时间: {results['query_time']}")
    lines.append("")

    # 基本信息
    if results.get("basic_info"):
        lines.append("【基本信息】")
        basic = results["basic_info"]

        if basic.get("listed"):
            listed = basic["listed"]
            if listed.get("is_listed"):
                lines.append(f"  上市公司: {listed.get('name')} ({listed.get('code')})")
            else:
                lines.append("  非上市公司")

        lines.append("")

    # 法律信息
    if results.get("legal_info"):
        lines.append("【法律风险】")
        legal = results["legal_info"]

        if legal.get("litigation"):
            lit = legal["litigation"]
            lines.append(f"  诉讼查询: {lit.get('query_url')}")
            lines.append(f"  提示: 需手动查询")

        if legal.get("dishonest"):
            dis = legal["dishonest"]
            lines.append(f"  失信查询: {dis.get('query_urls', {}).get('失信被执行人')}")

        lines.append("")

    # 舆情信息
    if results.get("news_info"):
        lines.append("【舆情信息】")
        news = results["news_info"]
        lines.append(f"  相关新闻: {news.get('news_count', 0)} 条")

        for item in news.get("news", [])[:5]:
            lines.append(f"  - {item.get('title')}")

        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
