#!/usr/bin/env python3
"""
天眼查公司查询 - 完整版
支持抓取：基本信息、股东信息、主要人员、对外投资等
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
STORAGE_FILE = CONFIG_DIR / "tianyancha_storage.json"


class TianyanchaQuery:
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

    def _safe_get_text(self, selector: str, default: str = "") -> str:
        """安全获取文本"""
        try:
            elem = self.page.query_selector(selector)
            if elem and elem.is_visible():
                return elem.inner_text().strip()
        except:
            pass
        return default

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
                # 清理
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
            'source': '天眼查'
        }

        try:
            self._init_browser()

            # 直接访问搜索 URL
            search_url = f"https://www.tianyancha.com/search?key={urllib.parse.quote(company_name)}"
            print(f"搜索: {company_name}")
            
            self.page.goto(search_url, wait_until='networkidle', timeout=60000)
            self._delay(2, 4)

            # 获取公司链接
            company_url = None
            
            if '/company/' in self.page.url:
                company_url = self.page.url
            else:
                links = self.page.query_selector_all('a[href*="/company/"]')
                for link in links[:5]:
                    href = link.get_attribute('href') or ''
                    text = link.inner_text().strip()
                    
                    if '/company/' in href and text:
                        if not href.startswith('http'):
                            href = f"https://www.tianyancha.com{href}"
                        
                        if company_name in text or text in company_name or len(text) > 5:
                            company_url = href
                            break

            if not company_url:
                result['error'] = '未找到公司'
                return result

            # 访问公司详情页
            print(f"访问详情页...")
            self.page.goto(company_url, wait_until='networkidle', timeout=60000)
            self._delay(2, 4)

            # 提取所有信息
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
        
        # 获取页面全部文本
        page_text = self.page.inner_text('body')

        # ========== 基本信息 ==========
        print("提取基本信息...")
        
        # 公司名称
        data['name'] = self._safe_get_text('h1') or company_name
        data['name'] = data['name'].replace('存续', '').replace('在业', '').strip()
        
        # 从页面文本提取字段
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
        ]
        
        for field_cn, field_key in fields:
            value = self._extract_field_from_text(page_text, field_cn)
            if value:
                data[field_key] = value

        # ========== 股东信息 ==========
        print("提取股东信息...")
        shareholders = self._extract_shareholders()
        if shareholders:
            data['shareholders'] = shareholders
            data['shareholder_count'] = len(shareholders)

        # ========== 主要人员 ==========
        print("提取主要人员...")
        key_persons = self._extract_key_persons()
        if key_persons:
            data['key_persons'] = key_persons
            data['key_person_count'] = len(key_persons)

        # ========== 对外投资 ==========
        print("提取对外投资...")
        investments = self._extract_investments()
        if investments:
            data['investments'] = investments
            data['investment_count'] = len(investments)

        # ========== 变更记录 ==========
        print("提取变更记录...")
        changes = self._extract_changes()
        if changes:
            data['changes'] = changes
            data['change_count'] = len(changes)

        print(f"共提取 {len(data)} 个字段")
        return data

    def _extract_shareholders(self) -> List[Dict]:
        """提取股东信息"""
        shareholders = []
        
        try:
            # 尝试点击股东信息 tab
            self._click_tab('股东', '股东信息')
            self._delay(1, 2)
            
            # 查找股东列表
            selectors = [
                '[class*=" shareholder"] tr',
                '[class*="holder"] tr',
                'table tr',
            ]
            
            for selector in selectors:
                rows = self.page.query_selector_all(selector)
                if len(rows) > 1:  # 有表头
                    for row in rows[1:11]:  # 取前10个
                        try:
                            cells = row.query_selector_all('td')
                            if len(cells) >= 2:
                                name = cells[0].inner_text().strip()
                                ratio = cells[1].inner_text().strip() if len(cells) > 1 else ''
                                
                                if name and len(name) < 50:
                                    shareholders.append({
                                        'name': name,
                                        'ratio': ratio,
                                    })
                        except:
                            continue
                    
                    if shareholders:
                        break
        
        except Exception as e:
            print(f"  股东信息提取失败: {e}")
        
        return shareholders

    def _extract_key_persons(self) -> List[Dict]:
        """提取主要人员"""
        persons = []
        
        try:
            self._click_tab('主要人员', '人员')
            self._delay(1, 2)
            
            selectors = [
                '[class*="person"] tr',
                '[class*="member"] tr',
                'table tr',
            ]
            
            for selector in selectors:
                rows = self.page.query_selector_all(selector)
                if len(rows) > 1:
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
                    
                    if persons:
                        break
        
        except:
            pass
        
        return persons

    def _extract_investments(self) -> List[Dict]:
        """提取对外投资"""
        investments = []
        
        try:
            self._click_tab('对外投资', '投资')
            self._delay(1, 2)
            
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

    def _extract_changes(self) -> List[Dict]:
        """提取变更记录"""
        changes = []
        
        try:
            self._click_tab('变更', '变更记录')
            self._delay(1, 2)
            
            rows = self.page.query_selector_all('table tr')
            for row in rows[1:11]:
                try:
                    cells = row.query_selector_all('td')
                    if len(cells) >= 2:
                        date = cells[0].inner_text().strip() if len(cells) > 0 else ''
                        item = cells[1].inner_text().strip() if len(cells) > 1 else ''
                        
                        if item:
                            changes.append({
                                'date': date,
                                'item': item[:100],
                            })
                except:
                    continue
        
        except:
            pass
        
        return changes

    def _click_tab(self, *keywords):
        """点击包含关键词的 tab"""
        try:
            tabs = self.page.query_selector_all('[class*="tab"], button, a')
            for tab in tabs:
                try:
                    text = tab.inner_text().strip()
                    for kw in keywords:
                        if kw in text:
                            if tab.is_visible():
                                tab.click()
                                return True
                except:
                    continue
        except:
            pass
        return False


def main():
    parser = argparse.ArgumentParser(description="天眼查公司查询")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器")

    args = parser.parse_args()

    if not STORAGE_FILE.exists():
        print("错误: 未登录天眼查")
        print("请先运行: python scripts/tianyancha_login.py")
        sys.exit(1)

    query = TianyanchaQuery(headless=not args.no_headless)
    result = query.query(args.company)

    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n结果已保存: {args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
