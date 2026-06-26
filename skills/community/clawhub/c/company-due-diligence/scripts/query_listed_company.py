#!/usr/bin/env python3
"""
查询上市公司信息
数据源：巨潮资讯网(cninfo)、上交所、深交所
"""

import requests
import json
import re
import time
from typing import Dict, List, Optional
from datetime import datetime

class ListedCompanyQuery:
    """上市公司信息查询"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        # 数据源URL
        self.cninfo_search_url = "http://www.cninfo.com.cn/new/fulltextSearch"
        self.cninfo_company_url = "http://www.cninfo.com.cn/new/data/company"
        
    def search_company(self, company_name: str) -> List[Dict]:
        """
        在巨潮资讯网搜索公司
        
        Args:
            company_name: 公司名称或股票代码
            
        Returns:
            匹配的公司列表
        """
        print(f"🔍 正在搜索: {company_name}")
        
        params = {
            'keyword': company_name,
            'type': 'company'
        }
        
        try:
            # 巨潮资讯的搜索接口
            search_url = f"http://www.cninfo.com.cn/new/data/search"
            resp = self.session.get(search_url, params=params, timeout=10)
            
            if resp.status_code == 200:
                # 解析返回的JSON数据
                data = resp.json()
                companies = []
                
                if 'companyList' in data:
                    for item in data['companyList']:
                        companies.append({
                            'name': item.get('companyName', ''),
                            'code': item.get('code', ''),
                            'stock_code': item.get('stockcode', ''),
                            'exchange': '上交所' if item.get('code', '').startswith('6') else '深交所',
                            'org_id': item.get('orgId', '')
                        })
                
                print(f"✅ 找到 {len(companies)} 家公司")
                return companies
            else:
                print(f"❌ 搜索失败: HTTP {resp.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索出错: {str(e)}")
            return []
    
    def get_company_announcements(self, stock_code: str, org_id: str = None) -> List[Dict]:
        """
        获取公司公告列表
        
        Args:
            stock_code: 股票代码
            org_id: 公司组织ID
            
        Returns:
            公告列表
        """
        print(f"📄 正在获取 {stock_code} 的公告...")
        
        announcements = []
        
        # 巨潮资讯公告查询接口
        announcement_url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
        
        params = {
            'stock': stock_code,
            'tabName': 'fulltext',
            'pageSize': 30,
            'pageNum': 1,
            'column': 'szse',  # 深交所，上交所用'sse'
            'category': 'category_ndbg_szsh',  # 年度报告
            'isHLtitle': 'true'
        }
        
        try:
            resp = self.session.post(announcement_url, data=params, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                if 'announcements' in data:
                    for item in data['announcements']:
                        announcements.append({
                            'title': item.get('announcementTitle', ''),
                            'date': item.get('announcementTime', ''),
                            'type': item.get('adjunctType', ''),
                            'url': f"http://www.cninfo.com.cn/new/disclosure/{item.get('announcementId', '')}"
                        })
                
                print(f"✅ 找到 {len(announcements)} 条公告")
                
        except Exception as e:
            print(f"❌ 获取公告失败: {str(e)}")
        
        return announcements
    
    def get_latest_annual_report(self, stock_code: str) -> Optional[str]:
        """
        获取最新年报PDF链接
        
        Args:
            stock_code: 股票代码
            
        Returns:
            年报PDF URL
        """
        print(f"📊 正在查找 {stock_code} 的最新年报...")
        
        # 尝试获取年度报告公告
        announcements = self.get_company_announcements(stock_code)
        
        for ann in announcements:
            if '年度报告' in ann['title'] and '摘要' not in ann['title']:
                print(f"✅ 找到年报: {ann['title']} ({ann['date']})")
                return ann
        
        print("⚠️ 未找到年报")
        return None
    
    def query_sse_company(self, stock_code: str) -> Dict:
        """
        查询上交所公司信息
        
        Args:
            stock_code: 6位股票代码
            
        Returns:
            公司基本信息
        """
        if not stock_code.startswith('6'):
            return {}
            
        print(f"🏛️ 查询上交所: {stock_code}")
        
        info = {}
        
        try:
            # 上交所公司概况接口
            profile_url = f"http://query.sse.com.cn/commonSoQuery.do?jsonCallBack=&productid={stock_code}&type=1"
            
            headers = {
                'Referer': 'http://www.sse.com.cn/',
            }
            
            resp = self.session.get(profile_url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                # 上交所返回的是JSONP格式
                data = resp.json()
                
                if isinstance(data, dict) and 'result' in data:
                    result = data['result'][0] if data['result'] else {}
                    
                    info = {
                        'name': result.get('COMPANY_ABBR', ''),
                        'full_name': result.get('COMPANY_FULL_NAME', ''),
                        'english_name': result.get('COMPANY_ENGLISH_NAME', ''),
                        'listing_date': result.get('LISTING_DATE', ''),
                        'share_code': result.get('SHARE_CODE', ''),
                        'industry': result.get('INDUSTRY', ''),
                        'province': result.get('PROVINCE', ''),
                        'city': result.get('CITY', ''),
                        'website': result.get('WEBSITE', ''),
                    }
                    
                    print(f"✅ 获取到公司信息: {info['name']}")
                    
        except Exception as e:
            print(f"❌ 上交所查询失败: {str(e)}")
        
        # 延迟，避免请求过快
        time.sleep(2)
        
        return info
    
    def query_company_info(self, company_name_or_code: str) -> Dict:
        """
        综合查询公司信息
        
        Args:
            company_name_or_code: 公司名称或股票代码
            
        Returns:
            完整的公司信息
        """
        print(f"\n{'='*60}")
        print(f"开始查询: {company_name_or_code}")
        print(f"{'='*60}\n")
        
        result = {
            'query_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'query_target': company_name_or_code,
            'company': {},
            'announcements': [],
            'latest_annual_report': None,
            'data_source': []
        }
        
        # 1. 搜索公司
        companies = self.search_company(company_name_or_code)
        
        if not companies:
            print("\n⚠️ 未找到匹配的上市公司")
            print("💡 提示: 该公司可能不是上市公司，或请使用准确的股票代码")
            return result
        
        # 如果有多个结果，选择最匹配的
        target_company = companies[0]
        
        # 如果输入的是名称，尝试精确匹配
        if not company_name_or_code.isdigit():
            for comp in companies:
                if company_name_or_code in comp['name']:
                    target_company = comp
                    break
        
        result['company'] = target_company
        result['data_source'].append('巨潮资讯网(cninfo)')
        
        print(f"\n✅ 匹配公司: {target_company['name']} ({target_company['stock_code']})")
        
        # 2. 如果是上交所公司，查询详细信息
        if target_company['stock_code'].startswith('6'):
            sse_info = self.query_sse_company(target_company['stock_code'])
            if sse_info:
                result['company'].update(sse_info)
                result['data_source'].append('上海证券交易所')
        
        # 3. 获取最新公告
        announcements = self.get_company_announcements(
            target_company['stock_code'],
            target_company.get('org_id')
        )
        result['announcements'] = announcements[:10]  # 只保留最近10条
        
        # 4. 查找最新年报
        latest_report = self.get_latest_annual_report(target_company['stock_code'])
        if latest_report:
            result['latest_annual_report'] = latest_report
        
        print(f"\n{'='*60}")
        print("✅ 查询完成")
        print(f"{'='*60}\n")
        
        return result


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python query_listed_company.py <公司名称或股票代码>")
        print("示例: python query_listed_company.py 建元信托")
        print("示例: python query_listed_company.py 600816")
        sys.exit(1)
    
    query = ListedCompanyQuery()
    result = query.query_company_info(sys.argv[1])
    
    # 输出JSON格式结果
    print("\n📊 查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
