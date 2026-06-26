#!/usr/bin/env python3
"""
企业关联关系数据源 - 中期方案
整合维基百科、上市公司公告等公开数据源
"""

import requests
import json
import re
from typing import Optional, List


class CorporateDataSources:
    """企业数据源查询类"""
    
    def __init__(self):
        self.wikidata_url = "https://www.wikidata.org/w/api.php"
        self.wikipedia_url = "https://zh.wikipedia.org/w/api.php"
    
    def query_wikidata(self, company_name: str) -> List[str]:
        """
        查询 Wikidata 获取企业关联关系
        返回：子公司、母公司、品牌等
        """
        subsidiaries = []
        
        try:
            # 1. 搜索企业实体
            search_params = {
                "action": "wbsearchentities",
                "search": company_name,
                "language": "zh",
                "format": "json"
            }
            response = requests.get(self.wikidata_url, params=search_params, timeout=10)
            if response.status_code != 200:
                return []
            
            search_data = response.json()
            if not search_data.get("search"):
                return []
            
            # 取第一个匹配结果
            entity_id = search_data["search"][0].get("id")
            if not entity_id:
                return []
            
            # 2. 获取实体详情
            entity_params = {
                "action": "wbgetentities",
                "ids": entity_id,
                "props": "claims",
                "format": "json"
            }
            response = requests.get(self.wikidata_url, params=entity_params, timeout=10)
            if response.status_code != 200:
                return []
            
            entity_data = response.json()
            if not entity_data.get("entities"):
                return []
            
            entity = entity_data["entities"][entity_id]
            claims = entity.get("claims", {})
            
            # 3. 提取子公司（P355 - 子公司）
            if "P355" in claims:
                for claim in claims["P355"]:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"]:
                        sub_name = claim["mainsnak"]["datavalue"]["value"]
                        if isinstance(sub_name, str):
                            subsidiaries.append(sub_name)
            
            # 4. 提取母公司（P749 - 母公司）
            if "P749" in claims:
                for claim in claims["P749"]:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"]:
                        parent_name = claim["mainsnak"]["datavalue"]["value"]
                        if isinstance(parent_name, str):
                            subsidiaries.append(parent_name)
            
            # 5. 提取品牌（P3798 - 品牌）
            if "P3798" in claims:
                for claim in claims["P3798"]:
                    if "mainsnak" in claim and "datavalue" in claim["mainsnak"]:
                        brand_name = claim["mainsnak"]["datavalue"]["value"]
                        if isinstance(brand_name, str):
                            subsidiaries.append(brand_name)
            
        except Exception as e:
            print(f"⚠️ Wikidata 查询失败：{e}")
        
        return list(set(subsidiaries))
    
    def query_wikipedia(self, company_name: str) -> List[str]:
        """
        查询维基百科获取企业简介中的关联信息
        """
        subsidiaries = []
        
        try:
            # 搜索维基百科条目
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": company_name,
                "format": "json",
                "utf8": ""
            }
            response = requests.get(self.wikipedia_url, params=search_params, timeout=10)
            if response.status_code != 200:
                return []
            
            search_data = response.json()
            if not search_data.get("query", {}).get("search"):
                return []
            
            # 取第一个搜索结果
            title = search_data["query"]["search"][0]["title"]
            
            # 获取条目内容
            content_params = {
                "action": "query",
                "titles": title,
                "prop": "extracts",
                "exintro": "",  # 只获取简介部分
                "format": "json",
                "utf8": ""
            }
            response = requests.get(self.wikipedia_url, params=content_params, timeout=10)
            if response.status_code != 200:
                return []
            
            content_data = response.json()
            pages = content_data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id == "-1":
                    continue
                extract = page_data.get("extract", "")
                
                # 从简介中提取关键词
                # 匹配"旗下"、"子公司"、"品牌"等关键词
                patterns = [
                    r'旗下 (?:品牌 | 公司 | 企业)[:：]?\s*([^，。,.\n]+)',
                    r'子公司 (?:包括 | 有)[:：]?\s*([^，。,.\n]+)',
                    r'品牌 (?:包括 | 有)[:：]?\s*([^，。,.\n]+)',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, extract)
                    for match in matches:
                        # 分割多个结果
                        items = re.split(r'[、，,]', match)
                        subsidiaries.extend([item.strip() for item in items if len(item.strip()) >= 2])
        
        except Exception as e:
            print(f"⚠️ 维基百科查询失败：{e}")
        
        return list(set(subsidiaries))
    
    def query_all(self, company_name: str) -> List[str]:
        """
        查询所有数据源，合并结果
        """
        all_subsidiaries = []
        
        print(f"🔍 查询公开数据源：{company_name}")
        
        # 1. Wikidata
        print(f"   → Wikidata...")
        wikidata_result = self.query_wikidata(company_name)
        all_subsidiaries.extend(wikidata_result)
        if wikidata_result:
            print(f"      找到：{', '.join(wikidata_result[:5])}")
        
        # 2. 维基百科
        print(f"   → 维基百科...")
        wikipedia_result = self.query_wikipedia(company_name)
        all_subsidiaries.extend(wikipedia_result)
        if wikipedia_result:
            print(f"      找到：{', '.join(wikipedia_result[:5])}")
        
        return list(set(all_subsidiaries))


# 命令行测试
if __name__ == '__main__':
    import sys
    
    datasource = CorporateDataSources()
    
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
        result = datasource.query_all(company_name)
        print(f"\n✅ 查询结果：{result}")
    else:
        # 测试示例
        test_companies = [
            '滴滴出行',
            '阿里巴巴',
            '腾讯',
            '小米',
        ]
        
        print("=" * 60)
        print("企业数据源查询测试")
        print("=" * 60)
        
        for company in test_companies:
            print(f"\n查询：{company}")
            result = datasource.query_all(company)
            print(f"结果：{result}")
            print("-" * 60)
