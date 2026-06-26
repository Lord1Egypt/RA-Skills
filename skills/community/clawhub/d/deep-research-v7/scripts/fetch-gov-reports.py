#!/usr/bin/env python3
"""
政府/行业报告自动抓取
功能：搜索并抓取政府官网、行业协会、券商研报
"""

import requests
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

class GovReportFetcher:
    """政府报告抓取器"""
    
    def __init__(self, output_dir="/tmp/gov_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 政府/行业数据源
        self.sources = {
            'gov_cn': {
                'base': 'https://www.gov.cn',
                'search': 'https://sousuo.www.gov.cn/search-gov/data',
                'type': '政府文件'
            },
            'nhc': {
                'base': 'http://www.nhc.gov.cn',
                'search': None,  # 需人工搜索
                'type': '卫健委文件'
            },
            'miit': {
                'base': 'https://www.miit.gov.cn',
                'search': None,
                'type': '工信部文件'
            }
        }
        
        # User-Agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def search_gov_cn(self, keyword, page=1):
        """搜索gov.cn政府文件"""
        print(f"搜索 gov.cn: {keyword}")
        
        try:
            url = self.sources['gov_cn']['search']
            params = {
                't': 'govall',
                'q': keyword,
                'page': page,
                'searchfield': 'title'
            }
            
            r = requests.get(url, params=params, headers=self.headers, timeout=15)
            data = r.json()
            
            results = []
            search_data = data.get('searchVO', {}).get('catMap', {}).get('govall', {})
            docs = search_data.get('docs', [])
            
            for doc in docs[:5]:  # 取前5条
                result = {
                    'title': doc.get('title', '').replace('<em>', '').replace('</em>', ''),
                    'url': doc.get('url', ''),
                    'publish_time': doc.get('pubtimeStr', ''),
                    'source': 'gov.cn',
                    'type': '政府文件'
                }
                results.append(result)
                print(f"  ✓ {result['title'][:40]}...")
            
            return results
            
        except Exception as e:
            print(f"  ✗ 搜索失败: {e}")
            return []
    
    def fetch_with_jina(self, url):
        """使用Jina Reader抓取网页"""
        jina_url = f"https://r.jina.ai/{url}"
        
        try:
            print(f"  抓取: {url}")
            r = requests.get(jina_url, headers=self.headers, timeout=20)
            if r.status_code == 200:
                content = r.text
                print(f"  ✅ 成功 ({len(content)} 字符)")
                return content
            else:
                print(f"  ❌ 失败: HTTP {r.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return None
    
    def fetch_pdf_report(self, url, filename=None):
        """下载PDF报告"""
        if not filename:
            filename = Path(urlparse(url).path).name or "report.pdf"
        
        pdf_path = self.output_dir / filename
        
        try:
            print(f"  下载PDF: {url}")
            r = requests.get(url, headers=self.headers, timeout=30, stream=True)
            if r.status_code == 200:
                with open(pdf_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  ✅ 下载成功: {pdf_path}")
                return str(pdf_path)
            else:
                print(f"  ❌ 下载失败: HTTP {r.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return None
    
    def extract_gov_data(self, content, source_url):
        """从政府文件提取数据"""
        data = {
            'source_url': source_url,
            'extracted': {}
        }
        
        # 提取发布日期
        date_patterns = [
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{4}-\d{2}-\d{2})',
            r'发布时间[：:]\s*(\d{4}-\d{2}-\d{2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                data['extracted']['publish_date'] = match.group(1)
                break
        
        # 提取文号
        doc_num = re.search(r'([国发国办发国卫健发国医保发国中医药发]\s*[\〔\[\(]\d{4}[\〕\]\)]\s*\d+号)', content)
        if doc_num:
            data['extracted']['document_number'] = doc_num.group(1)
        
        # 提取目标/指标
        target_patterns = [
            r'目标[:：]\s*([^。\n]+)',
            r'到(\d{4}年)[，,]?\s*([^。\n]+)',
            r'(覆盖率|普及率|达标率)\s*(达到|提高至|实现)?\s*(\d+%)',
        ]
        targets = []
        for pattern in target_patterns:
            matches = re.findall(pattern, content)
            targets.extend(matches[:3])
        if targets:
            data['extracted']['targets'] = targets[:5]
        
        # 提取金额
        money_patterns = [
            r'(\d+(?:\.\d+)?)\s*(亿|万亿|千万|百万)?\s*元',
            r'投资\s*(\d+(?:\.\d+)?)\s*(亿|万亿)?',
        ]
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, content)
            amounts.extend(matches[:3])
        if amounts:
            data['extracted']['amounts'] = amounts[:5]
        
        return data
    
    def create_report_card(self, report_info, content):
        """生成报告卡片"""
        card_id = f"gov-{int(time.time())}"
        
        extracted = self.extract_gov_data(content, report_info['url'])
        
        card = {
            'card_id': card_id,
            'title': report_info['title'],
            'source': report_info.get('source', '政府官网'),
            'type': report_info.get('type', '政策文件'),
            'url': report_info['url'],
            'publish_time': report_info.get('publish_time', ''),
            'content_preview': content[:1000],
            'extracted_data': extracted['extracted'],
            'full_content': content[:5000]  # 保存前5000字符
        }
        
        # 保存卡片
        card_file = self.output_dir / f"{card_id}.json"
        with open(card_file, 'w', encoding='utf-8') as f:
            json.dump(card, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 卡片生成: {card_file}")
        
        return card
    
    def search_and_fetch(self, keyword, max_results=3):
        """搜索并抓取政府报告"""
        print(f"\n=== 搜索政府报告: {keyword} ===\n")
        
        # 搜索gov.cn
        results = self.search_gov_cn(keyword)
        
        cards = []
        for result in results[:max_results]:
            # 限速
            time.sleep(1)
            
            # 抓取内容
            content = self.fetch_with_jina(result['url'])
            if content:
                # 生成卡片
                card = self.create_report_card(result, content)
                cards.append(card)
                
                # 显示提取的数据
                if card['extracted_data']:
                    print(f"  📊 提取数据:")
                    for key, value in card['extracted_data'].items():
                        print(f"    - {key}: {value}")
        
        print(f"\n完成: 生成 {len(cards)} 个政府报告卡片")
        return cards


class IndustryReportFetcher:
    """行业报告抓取器"""
    
    def __init__(self, output_dir="/tmp/industry_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def search_industry_keywords(self, keyword):
        """生成行业搜索关键词"""
        keywords = [
            f"{keyword} 市场规模",
            f"{keyword} 行业报告",
            f"{keyword} 发展现状",
            f"{keyword} 政策分析"
        ]
        return keywords


def test_fetcher():
    """测试政府报告抓取"""
    fetcher = GovReportFetcher()
    
    # 测试搜索
    keyword = "医疗信息化"
    cards = fetcher.search_and_fetch(keyword, max_results=2)
    
    return cards


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        
        fetcher = GovReportFetcher()
        fetcher.search_and_fetch(keyword, max_results)
    else:
        print("用法: python fetch-gov-reports.py <关键词> [数量]")
        print("示例: python fetch-gov-reports.py '医疗信息化' 3")
        print("\n测试运行...")
        test_fetcher()