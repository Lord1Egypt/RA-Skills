#!/usr/bin/env python3
"""
缓存管理模块
用于存储和检索搜索结果，避免重复搜索
"""

import json
import os
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta


class CacheManager:
    def __init__(self, cache_dir=None, expire_days=7):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / 'cache'
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.expire_days = expire_days
        
        self.companies_db = self.cache_dir / 'companies.json'
        self.searches_db = self.cache_dir / 'searches.json'
        self.emails_db = self.cache_dir / 'emails.json'
        
        self._init_db(self.companies_db, {})
        self._init_db(self.searches_db, {})
        self._init_db(self.emails_db, {})
    
    def _init_db(self, path, default):
        if not path.exists():
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(default, f, ensure_ascii=False)
    
    def _load_db(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_db(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _get_cache_key(self, keyword, region=None):
        key = f"{keyword}_{region or ''}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get_search_cache(self, keyword, region=None):
        cache_key = self._get_cache_key(keyword, region)
        searches = self._load_db(self.searches_db)
        
        if cache_key in searches:
            cache_entry = searches[cache_key]
            cache_time = datetime.fromisoformat(cache_entry['timestamp'])
            
            if datetime.now() - cache_time < timedelta(days=self.expire_days):
                return cache_entry['results']
        
        return None
    
    def save_search_cache(self, keyword, region, results):
        cache_key = self._get_cache_key(keyword, region)
        searches = self._load_db(self.searches_db)
        
        searches[cache_key] = {
            'keyword': keyword,
            'region': region,
            'timestamp': datetime.now().isoformat(),
            'count': len(results),
            'results': results
        }
        
        self._save_db(self.searches_db, searches)
    
    def is_company_exists(self, domain):
        companies = self._load_db(self.companies_db)
        return domain in companies
    
    def add_company(self, company_info):
        companies = self._load_db(self.companies_db)
        domain = company_info.get('domain')
        
        if domain:
            companies[domain] = {
                **company_info,
                'first_found': datetime.now().isoformat(),
                'search_count': companies.get(domain, {}).get('search_count', 0) + 1
            }
            self._save_db(self.companies_db, companies)
    
    def add_companies_batch(self, companies_list):
        for company in companies_list:
            self.add_company(company)
    
    def get_company_emails(self, domain):
        emails = self._load_db(self.emails_db)
        return emails.get(domain, {}).get('emails', [])
    
    def save_company_emails(self, domain, emails):
        emails_db = self._load_db(self.emails_db)
        
        emails_db[domain] = {
            'emails': emails,
            'timestamp': datetime.now().isoformat(),
            'count': len(emails)
        }
        
        self._save_db(self.emails_db, emails_db)
    
    def filter_new_companies(self, companies_list):
        return [c for c in companies_list if not self.is_company_exists(c.get('domain'))]
    
    def get_all_companies(self):
        return self._load_db(self.companies_db)
    
    def get_all_emails(self):
        return self._load_db(self.emails_db)
    
    def get_stats(self):
        companies = self._load_db(self.companies_db)
        emails = self._load_db(self.emails_db)
        searches = self._load_db(self.searches_db)
        
        total_emails = sum(len(e.get('emails', [])) for e in emails.values())
        
        return {
            'total_companies': len(companies),
            'total_emails': total_emails,
            'total_searches': len(searches),
            'companies_with_emails': len(emails)
        }
    
    def clear_expired(self):
        searches = self._load_db(self.searches_db)
        expired_keys = []
        
        for key, entry in searches.items():
            cache_time = datetime.fromisoformat(entry['timestamp'])
            if datetime.now() - cache_time >= timedelta(days=self.expire_days):
                expired_keys.append(key)
        
        for key in expired_keys:
            del searches[key]
        
        if expired_keys:
            self._save_db(self.searches_db, searches)
        
        return len(expired_keys)


if __name__ == '__main__':
    import sys
    
    cache = CacheManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'stats':
            stats = cache.get_stats()
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        
        elif cmd == 'clear':
            cleared = cache.clear_expired()
            print(f"Cleared {cleared} expired entries")
        
        elif cmd == 'list':
            companies = cache.get_all_companies()
            print(f"Total companies: {len(companies)}")
            for domain, info in list(companies.items())[:10]:
                print(f"  - {info.get('name', domain)}: {domain}")
        
        elif cmd == 'export':
            output = {
                'companies': cache.get_all_companies(),
                'emails': cache.get_all_emails(),
                'stats': cache.get_stats()
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
    
    else:
        print("Usage: cache_manager.py [stats|clear|list|export]")
