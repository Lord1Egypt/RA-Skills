#!/usr/bin/env python3
"""
企查查公司查询脚本

使用方法:
    python scripts/query_qichacha.py "公司名称"
    python scripts/query_qichacha.py "公司名称" --output result.json
"""

import os
import sys
import json
import time
import random
import argparse
import urllib.parse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("错误: Playwright 未安装")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".due_diligence"
STORAGE_FILE = CONFIG_DIR / "qichacha_storage.json"

QICHACHA_URL = "https://www.qcc.com/"


class QichachaQuery:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def _load_storage_state(self) -> Optional[Dict]:
        if STORAGE_FILE.exists():
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        return None

    def _init_browser(self):
        storage_state = self._load_storage_state()
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        
        if storage_state:
            self.context = self.browser.new_context(
                storage_state=storage_state,
                viewport={'width': 1400, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
        else:
            self.context = self.browser.new_context(
                viewport={'width': 1400, 'height': 900},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
        
        self.page = self.context.new_page()

    def _close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _delay(self, min_s=1, max_s=3):
        time.sleep(random.uniform(min_s, max_s))

    def _extract_field_from_text(self, page_text: str, field_name: str) -> str:
        """从页面文本中提取字段"""
        patterns = [
            rf'{field_name}[：:\s]*([^\n\r]+)',
            rf'{field_name}\s*[:：]\s*([^\n\r]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, page_text)
            if match:
                value = match.group(1).strip()
                value = value.split('\n')[0].strip()
                value = re.sub(r'\s+', ' ', value)
                if len(value) > 2 and len(value) < 500:
                    return value
        return ""

    def query(self, company_name: str) -> Dict:
        """查询公司信息"""
        result = {
            'company_name': company_name,
            'query_time': datetime.now().isoformat(),
            'source': '企查查'
        }

        try:
            self._init_browser()

            # 访问企查查搜索页
            search_url = f"https://www.qcc.com/web/search?key={urllib.parse.quote(company_name)}"
            print(f"搜索: {company_name}")
            
            self.page.goto(search_url, wait_until='networkidle', timeout=60000)
            self._delay(2, 4)

            # 截图
            self.page.screenshot(path="/tmp/qichacha_search.png")

            # 获取公司链接
            company_url = None
            
            # 查找搜索结果
            selectors = [
                'a[href*="/firm/"]',
                'a[href*="/company/"]',
                '.search-result a',
                'tbody tr a',
            ]
            
            for selector in selectors:
                try:
                    links = self.page.query_selector_all(selector)
                    for link in links[:5]:
                        href = link.get_attribute('href') or ''
                        text = link.inner_text().strip()
                        
                        if ('/firm/' in href or '/company/' in href) and text:
                            if not href.startswith('http'):
                                href = f"https://www.qcc.com{href}"
                            
                            # 优先匹配公司名
                            if company_name in text or text in company_name or len(text) > 5:
                                company_url = href
                                print(f"找到公司: {text[:30]}")
                                break
                    
                    if company_url:
                        break
                except:
                    continue

            if not company_url:
                result['error'] = '未找到公司'
                return result

            # 访问公司详情页
            print("访问详情页...")
            self.page.goto(company_url, wait_until='networkidle', timeout=60000)
            self._delay(2, 4)
            
            self.page.screenshot(path="/tmp/qichacha_detail.png")

            # 提取信息
            data = self._extract_all_info(company_name)
            data['url'] = company_url
            
            result.update(data)
            result['success'] = True
            
            print(f"✓ 查询完成")

        except Exception as e:
            result['error'] = str(e)
            print(f"✗ 查询失败: {e}")

        finally:
            self._close()

        return result

    def _extract_all_info(self, company_name: str) -> Dict:
        """提取所有信息"""
        data = {}
        
        page_text = self.page.inner_text('body')

        # 基本信息
        print("提取基本信息...")
        
        # 公司名称
        title_elem = self.page.query_selector('h1, .title, [class*="company"]')
        if title_elem:
            data['name'] = title_elem.inner_text().strip()
        else:
            data['name'] = company_name
        
        # 提取字段
        fields = [
            ('法定代表人', '法定代表人'),
            ('注册资本', '注册资本'),
            ('实缴资本', '实缴资本'),
            ('成立日期', '成立日期'),
            ('经营状态', '经营状态'),
            ('统一社会信用代码', '统一社会信用代码'),
            ('纳税人识别号', '纳税人识别号'),
            ('注册号', '注册号'),
            ('组织机构代码', '组织机构代码'),
            ('企业类型', '企业类型'),
            ('行业', '行业'),
            ('核准日期', '核准日期'),
            ('登记机关', '登记机关'),
            ('注册地址', '注册地址'),
            ('经营范围', '经营范围'),
            ('营业期限', '营业期限'),
            ('英文名称', '英文名称'),
            ('曾用名', '曾用名'),
            ('参保人数', '参保人数'),
        ]
        
        for field_cn, field_key in fields:
            value = self._extract_field_from_text(page_text, field_cn)
            if value:
                data[field_key] = value

        # 股东信息
        print("提取股东信息...")
        shareholders = self._extract_shareholders()
        if shareholders:
            data['shareholders'] = shareholders
            data['shareholder_count'] = len(shareholders)

        # 主要人员
        print("提取主要人员...")
        key_persons = self._extract_key_persons()
        if key_persons:
            data['key_persons'] = key_persons
            data['key_person_count'] = len(key_persons)

        # 对外投资
        print("提取对外投资...")
        investments = self._extract_investments()
        if investments:
            data['investments'] = investments
            data['investment_count'] = len(investments)

        # 风险信息（企查查特色）
        print("提取风险信息...")
        risks = self._extract_risks()
        if risks:
            data['risks'] = risks

        print(f"共提取 {len(data)} 个字段")
        return data

    def _extract_shareholders(self) -> List[Dict]:
        """提取股东信息"""
        shareholders = []
        
        try:
            # 企查查的股东信息通常在表格中
            rows = self.page.query_selector_all('table tr, [class*="holder"] tr')
            
            for row in rows[1:11]:
                try:
                    cells = row.query_selector_all('td')
                    if len(cells) >= 2:
                        name = cells[0].inner_text().strip()
                        ratio = cells[1].inner_text().strip() if len(cells) > 1 else ''
                        
                        if name and len(name) < 50 and name not in ['股东名称', '持股比例']:
                            shareholders.append({
                                'name': name,
                                'ratio': ratio,
                            })
                except:
                    continue
        
        except:
            pass
        
        return shareholders

    def _extract_key_persons(self) -> List[Dict]:
        """提取主要人员"""
        persons = []
        
        try:
            rows = self.page.query_selector_all('table tr')
            
            for row in rows[1:11]:
                try:
                    cells = row.query_selector_all('td')
                    if len(cells) >= 2:
                        name = cells[0].inner_text().strip()
                        position = cells[1].inner_text().strip() if len(cells) > 1 else ''
                        
                        if name and len(name) < 20:
                            persons.append({
                                'name': name,
                                'position': position,
                            })
                except:
                    continue
        
        except:
            pass
        
        return persons

    def _extract_investments(self) -> List[Dict]:
        """提取对外投资"""
        investments = []
        
        try:
            rows = self.page.query_selector_all('table tr')
            
            for row in rows[1:11]:
                try:
                    cells = row.query_selector_all('td')
                    if len(cells) >= 2:
                        name = cells[0].inner_text().strip()
                        ratio = cells[1].inner_text().strip() if len(cells) > 1 else ''
                        
                        if name and len(name) < 50:
                            investments.append({
                                'name': name,
                                'ratio': ratio,
                            })
                except:
                    continue
        
        except:
            pass
        
        return investments

    def _extract_risks(self) -> Dict:
        """提取风险信息（企查查特色）"""
        risks = {}
        
        try:
            page_text = self.page.inner_text('body')
            
            # 风险指标
            risk_fields = [
                ('自身风险', 'self_risk'),
                ('关联风险', 'related_risk'),
                ('提示信息', 'hints'),
                ('司法案件', 'judicial_cases'),
                ('失信信息', 'dishonesty'),
                ('被执行人', 'executor'),
                ('行政处罚', 'penalty'),
            ]
            
            for cn_name, en_name in risk_fields:
                match = re.search(rf'{cn_name}[：:\s]*(\d+)', page_text)
                if match:
                    risks[en_name] = int(match.group(1))
        
        except:
            pass
        
        return risks


def main():
    parser = argparse.ArgumentParser(description="企查查公司查询")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器")

    args = parser.parse_args()

    if not STORAGE_FILE.exists():
        print("错误: 未登录企查查")
        print("请先运行: python scripts/qichacha_login.py")
        sys.exit(1)

    query = QichachaQuery(headless=not args.no_headless)
    result = query.query(args.company)

    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n结果已保存: {args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
