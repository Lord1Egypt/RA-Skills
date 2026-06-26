#!/usr/bin/env python3
"""
裁判文书网查询脚本

使用方法:
    python scripts/query_wenshu.py "公司名称"
    python scripts/query_wenshu.py "公司名称" --output result.json
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
STORAGE_FILE = CONFIG_DIR / "wenshu_storage.json"

WENSHU_URL = "http://wenshu.court.gov.cn/"


class WenshuQuery:
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

    def query(self, company_name: str) -> Dict:
        """查询公司诉讼信息"""
        result = {
            'company_name': company_name,
            'query_time': datetime.now().isoformat(),
            'source': '裁判文书网'
        }

        try:
            self._init_browser()

            # 访问裁判文书网
            print(f"访问裁判文书网...")
            self.page.goto(WENSHU_URL, wait_until='networkidle', timeout=60000)
            self._delay(2, 4)

            # 截图
            self.page.screenshot(path="/tmp/wenshu_home.png")

            # 查找搜索框
            print("查找搜索框...")
            search_input = None
            
            selectors = [
                'input[placeholder*="搜索"]',
                'input[placeholder*="当事人"]',
                'input[name*="search"]',
                '#_search_key',
                '.search-input input',
            ]
            
            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    for elem in elements:
                        if elem.is_visible():
                            search_input = elem
                            print(f"找到搜索框: {selector}")
                            break
                    if search_input:
                        break
                except:
                    continue

            if not search_input:
                print("⚠ 未找到搜索框，可能需要手动登录")
                result['error'] = '未找到搜索框'
                result['message'] = '请先运行: python scripts/wenshu_login.py'
                
                # 保存截图供调试
                self.page.screenshot(path="/tmp/wenshu_error.png")
                return result

            # 输入公司名称
            print(f"输入搜索词: {company_name}")
            search_input.fill(company_name)
            self._delay(0.5, 1)

            # 点击搜索按钮
            print("提交搜索...")
            search_btn_selectors = [
                'button:has-text("搜索")',
                '.search-btn',
                'input[type="submit"]',
                'button[type="submit"]',
            ]
            
            for selector in search_btn_selectors:
                try:
                    btn = self.page.query_selector(selector)
                    if btn and btn.is_visible():
                        btn.click()
                        break
                except:
                    continue
            else:
                # 尝试按回车
                search_input.press('Enter')

            # 等待搜索结果
            self._delay(3, 5)
            
            # 截图
            self.page.screenshot(path="/tmp/wenshu_search.png")
            print("截图: /tmp/wenshu_search.png")

            # 获取当前 URL
            print(f"当前 URL: {self.page.url}")

            # 提取搜索结果
            print("提取搜索结果...")
            cases = self._extract_cases()
            
            result['cases'] = cases
            result['case_count'] = len(cases)
            result['search_url'] = self.page.url
            result['success'] = True
            
            # 统计信息
            if cases:
                # 统计作为原告/被告的数量
                as_plaintiff = sum(1 for c in cases if '原告' in c.get('parties', '') and company_name in c.get('parties', ''))
                as_defendant = sum(1 for c in cases if '被告' in c.get('parties', '') and company_name in c.get('parties', ''))
                
                result['statistics'] = {
                    'total': len(cases),
                    'as_plaintiff': as_plaintiff,
                    'as_defendant': as_defendant,
                }
            
            print(f"✓ 查询完成，找到 {len(cases)} 条记录")

        except Exception as e:
            result['error'] = str(e)
            print(f"✗ 查询失败: {e}")
            
            # 保存错误截图
            try:
                self.page.screenshot(path="/tmp/wenshu_error.png")
            except:
                pass

        finally:
            self._close()

        return result

    def _extract_cases(self) -> List[Dict]:
        """提取案件列表"""
        cases = []
        
        try:
            # 等待结果加载
            self.page.wait_for_load_state('networkidle', timeout=10000)
            
            # 尝试多种选择器
            result_selectors = [
                '.case-item',
                '.result-item',
                'table tr',
                '[class*="case"]',
                '[class*="result"]',
                '.LM_list tr',
            ]
            
            items = []
            for selector in result_selectors:
                try:
                    items = self.page.query_selector_all(selector)
                    if items and len(items) > 1:
                        print(f"找到 {len(items)} 个结果项 ({selector})")
                        break
                except:
                    continue
            
            # 如果没找到结构化的结果，尝试从页面文本提取
            if not items or len(items) <= 1:
                print("尝试从页面文本提取...")
                page_text = self.page.inner_text('body')
                
                # 提取案号
                case_numbers = re.findall(r'（\d{4}）[^）]+号', page_text)
                case_numbers += re.findall(r'\(\d{4}\)[^）]+号', page_text)
                
                for i, case_num in enumerate(set(case_numbers)[:20]):
                    cases.append({
                        'index': i + 1,
                        'case_number': case_num,
                        'title': case_num,
                    })
                
                return cases
            
            # 从结构化元素提取
            for i, item in enumerate(items[:20]):  # 取前20条
                try:
                    text = item.inner_text().strip()
                    if not text or len(text) < 10:
                        continue
                    
                    case = {
                        'index': i + 1,
                        'raw_text': text[:500],
                    }
                    
                    # 提取案号
                    case_num_match = re.search(r'[（(]\d{4}[）)][^）)〕]+号', text)
                    if case_num_match:
                        case['case_number'] = case_num_match.group()
                        case['title'] = case['case_number']
                    
                    # 提取案件类型
                    type_match = re.search(r'(民事|刑事|行政|执行|赔偿)', text)
                    if type_match:
                        case['case_type'] = type_match.group()
                    
                    # 提取日期
                    date_match = re.search(r'(\d{4}[-年]\d{1,2}[-月]\d{1,2})', text)
                    if date_match:
                        case['date'] = date_match.group(1)
                    
                    # 当事人信息
                    case['parties'] = text
                    
                    cases.append(case)
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"提取案件失败: {e}")
        
        return cases


def main():
    parser = argparse.ArgumentParser(description="裁判文书网查询")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器")

    args = parser.parse_args()

    # 检查登录状态
    if not STORAGE_FILE.exists():
        print("提示: 未登录裁判文书网")
        print("建议先运行: python scripts/wenshu_login.py")
        print("继续尝试查询...\n")

    query = WenshuQuery(headless=not args.no_headless)
    result = query.query(args.company)

    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\n结果已保存: {args.output}")
    else:
        print("\n" + output)


if __name__ == "__main__":
    main()
