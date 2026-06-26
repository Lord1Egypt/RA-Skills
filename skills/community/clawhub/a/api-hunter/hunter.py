"""
API Hunter - 全自動 API 獵人 (優化版)
"""
import requests
import json
import time
from typing import List, Dict, Optional

# 搜尋引擎
SEARCH_URL = "http://localhost:8888/search"

class APIHunter:
    """全自動 API 獵人"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.found_apis = []
        
    def search(self, feature: str, count: int = 10) -> List[Dict]:
        """搜尋免費 API"""
        print(f"\n🔍 搜尋: {feature}")
        
        # 搜尋免費 API
        queries = [
            f"{feature} free API no credit card required",
            f"{feature} API free tier sign up",
            f"free {feature} API developer"
        ]
        
        all_results = []
        
        for query in queries:
            try:
                resp = requests.get(SEARCH_URL, params={
                    'q': query, 'format': 'json', 'num': 5
                }, timeout=10)
                results = resp.json().get('results', [])
                all_results.extend(results)
            except Exception as e:
                print(f"  ⚠️ 搜尋失敗: {e}")
        
        # 去重
        seen = set()
        unique = []
        for r in all_results:
            url = r.get('url', '')
            if url and url not in seen:
                seen.add(url)
                unique.append(r)
        
        print(f"  找到 {len(unique)} 個結果")
        return unique
    
    def check_api_dashboard(self, url: str) -> Dict:
        """檢查 API 提供者頁面"""
        result = {
            'url': url,
            'has_pricing': False,
            'has_free_tier': False,
            'has_signup': False,
            'api_key_location': None,
            'direct_link': None
        }
        
        try:
            resp = self.session.get(url, timeout=10)
            text = resp.text.lower()
            
            # 檢查關鍵詞
            if 'pricing' in text or 'price' in text:
                result['has_pricing'] = True
            if 'free' in text and ('tier' in text or 'plan' in text):
                result['has_free_tier'] = True
            if 'sign up' in text or 'register' in text or 'get api key' in text:
                result['has_signup'] = True
                
            # 找直接連結
            if 'get started' in text or 'try free' in text:
                result['direct_link'] = url
                
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    def get_free_apis_no_signup(self, feature: str) -> List[Dict]:
        """搜尋免費無需註冊的 API"""
        print(f"\n🎯 搜尋免費無需註冊的 {feature} API...")
        
        # 搜尋 "no key required" APIs
        resp = requests.get(SEARCH_URL, params={
            'q': f'{feature} API no API key required',
            'format': 'json', 'num': 10
        }, timeout=10)
        
        results = resp.json().get('results', [])
        
        apis = []
        for r in results:
            url = r.get('url', '')
            title = r.get('title', '')
            
            # 過濾掉 GitHub
            if 'github.com' in url:
                continue
                
            apis.append({
                'name': title.split('|')[0].split('-')[0].strip()[:40],
                'url': url,
                'description': r.get('body', '')[:100]
            })
        
        return apis
    
    def hunt(self, feature: str) -> str:
        """
        執行獵人任務
        
        使用方式:
            hunter = APIHunter()
            report = hunter.hunt("weather")
            print(report)
        """
        print(f"\n{'='*50}")
        print(f"🎯 API Hunter: {feature}")
        print(f"{'='*50}")
        
        # 1. 搜尋免費 API
        search_results = self.search(feature)
        
        # 2. 檢查每個結果
        print(f"\n📊 檢查 API 提供者...")
        
        report_lines = [
            f"\n## 🎯 {feature} API 獵人報告",
            f"\n### 搜尋結果",
            ""
        ]
        
        for i, r in enumerate(search_results[:8], 1):
            title = r.get('title', '')[:50]
            url = r.get('url', '')
            body = r.get('body', '')[:80]
            
            report_lines.append(f"**{i}. {title}**")
            report_lines.append(f"- URL: {url}")
            report_lines.append(f"- {body}...")
            report_lines.append("")
        
        # 3. 找無需註冊的 API
        print(f"\n🚀 找無需註冊的 API...")
        no_signup_apis = self.get_free_apis_no_signup(feature)
        
        report_lines.append(f"\n### ✅ 無需註冊的 API ({len(no_signup_apis)}個)")
        report_lines.append("")
        report_lines.append("| API 名稱 | 網址 | 說明 |")
        report_lines.append("|----------|------|------|")
        
        for api in no_signup_apis:
            name = api['name'][:20]
            url = api['url'][:40]
            desc = api['description'][:30]
            report_lines.append(f"| {name} | {url} | {desc} |")
        
        report = "\n".join(report_lines)
        print(report)
        
        return report


# ========== 快速函數 ==========

def hunt(feature: str) -> str:
    """一鍵獵取 API"""
    hunter = APIHunter()
    return hunter.hunt(feature)


if __name__ == "__main__":
    import sys
    feature = sys.argv[1] if len(sys.argv) > 1 else "weather"
    hunter = APIHunter()
    print(hunter.hunt(feature))
