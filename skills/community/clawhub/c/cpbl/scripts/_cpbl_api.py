#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "scrapling[ai]",
# ]
# ///
"""
CPBL API 共用模組
負責 CSRF token 取得、快取與 API 呼叫
提供共用常數（KIND_NAMES、TEAM_ALIASES）與工具函式（resolve_team）
"""

import json
import re
import sys
import tempfile
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 快取檔案路徑（使用系統暫存目錄，跨平台相容）
TOKEN_CACHE_FILE = Path(tempfile.gettempdir()) / 'cpbl_csrf_token.txt'


# ─── 輕量 In-Memory TTL 快取 ───

class _TTLCache:
    """簡易 TTL 快取，用於避免短時間內重複 API 呼叫"""

    def __init__(self, ttl_seconds: int = 300):
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, object]] = {}

    def get(self, key: str):
        entry = self._store.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: object):
        self._store[key] = (time.monotonic(), value)

    def clear(self):
        self._store.clear()


# 全域 API 回應快取（TTL 5 分鐘）
_response_cache = _TTLCache(ttl_seconds=300)


class CPBLAPI:
    """CPBL 官方隱藏 API 封裝"""
    
    BASE_URL = 'https://cpbl.com.tw'
    
    def __init__(self):
        self.csrf_token: Optional[str] = None
        self.token_expire: Optional[datetime] = None
        self._load_token_cache()
    
    def _load_token_cache(self):
        """載入快取的 CSRF token"""
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, 'r') as f:
                    data = json.load(f)
                    self.csrf_token = data.get('token')
                    expire_str = data.get('expire')
                    if expire_str:
                        self.token_expire = datetime.fromisoformat(expire_str)
            except (json.JSONDecodeError, KeyError, OSError, ValueError) as e:
                print(f'⚠️ CSRF token 快取讀取失敗: {e}', file=sys.stderr)
    
    def _save_token_cache(self):
        """儲存 CSRF token 到快取"""
        data = {
            'token': self.csrf_token,
            'expire': self.token_expire.isoformat() if self.token_expire else None
        }
        with open(TOKEN_CACHE_FILE, 'w') as f:
            json.dump(data, f)
    
    def _is_token_valid(self) -> bool:
        """檢查 token 是否有效"""
        if not self.csrf_token or not self.token_expire:
            return False
        return datetime.now() < self.token_expire
    
    def fetch_csrf_token(self, force_refresh: bool = False) -> str:
        """
        取得 CSRF token
        
        先嘗試用純 HTTP GET 取得（快速），失敗時才 fallback 到 headless browser。
        
        Args:
            force_refresh: 強制重新取得（忽略快取）
        
        Returns:
            CSRF token 字串
        """
        # 檢查快取
        if not force_refresh and self._is_token_valid():
            return self.csrf_token
        
        token = self._try_fetch_token_http()
        if not token:
            token = self._try_fetch_token_dynamic()
        
        if not token:
            raise ValueError('無法從頁面取得 CSRF token')
        
        self.csrf_token = token
        # Token 有效期設為 1 小時
        self.token_expire = datetime.now() + timedelta(hours=1)
        self._save_token_cache()
        
        return self.csrf_token
    
    def _try_fetch_token_http(self) -> Optional[str]:
        """嘗試用純 HTTP GET 取得 CSRF token（無需 headless browser，約 1 秒）"""
        try:
            url = f'{self.BASE_URL}/schedule?KindCode=A'
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(
                r"RequestVerificationToken['\"]?\s*[:=]\s*['\"]([^'\"]{20,})", html
            )
            return matches[0] if matches else None
        except Exception:
            return None
    
    def _try_fetch_token_dynamic(self) -> Optional[str]:
        """Fallback：用 scrapling DynamicFetcher 取得 token"""
        try:
            from scrapling.fetchers import DynamicFetcher
            url = f'{self.BASE_URL}/schedule?KindCode=A'
            page = DynamicFetcher.fetch(url, wait=5, headless=True)
            html = page.body if hasattr(page, 'body') else str(page)
            if isinstance(html, bytes):
                html = html.decode('utf-8', errors='ignore')
            matches = re.findall(
                r"RequestVerificationToken['\"]?\s*[:=]\s*['\"]([^'\"]{20,})", html
            )
            return matches[0] if matches else None
        except Exception as e:
            print(f'⚠️ DynamicFetcher fallback 失敗: {e}', file=sys.stderr)
            return None
    
    def _build_request(self, endpoint: str, data: dict) -> urllib.request.Request:
        """
        建立 POST 請求物件
        
        Args:
            endpoint: API 路徑
            data: POST 資料
        
        Returns:
            Request 物件
        """
        if not self._is_token_valid():
            self.fetch_csrf_token()
        
        url = f'{self.BASE_URL}{endpoint}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'RequestVerificationToken': self.csrf_token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=post_data, headers=headers, method='POST')
        return req
    
    def _send_request(self, endpoint: str, data: dict, parse_json: bool = True,
                      use_cache: bool = False) -> dict | str:
        """
        發送 POST 請求，支援 JSON 和 HTML 回應
        
        Args:
            endpoint: API 路徑
            data: POST 資料
            parse_json: True 回傳 JSON dict，False 回傳 HTML 字串
            use_cache: True 啟用 TTL 快取（適用於短時間內不會變化的資料）
        
        Returns:
            JSON dict 或 HTML 字串
        """
        # 快取查找
        cache_key = None
        if use_cache:
            cache_key = f'{endpoint}|{json.dumps(data, sort_keys=True)}|{parse_json}'
            cached = _response_cache.get(cache_key)
            if cached is not None:
                return cached

        req = self._build_request(endpoint, data)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                body = response.read().decode('utf-8')
                result = json.loads(body) if parse_json else body
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                self.fetch_csrf_token(force_refresh=True)
                req = self._build_request(endpoint, data)
                with urllib.request.urlopen(req, timeout=30) as response:
                    body = response.read().decode('utf-8')
                    result = json.loads(body) if parse_json else body
            else:
                raise

        if cache_key is not None:
            _response_cache.set(cache_key, result)
        return result
    
    def post_api(self, endpoint: str, data: dict) -> dict:
        """
        發送 POST 請求到 CPBL API（JSON 回應）
        
        Args:
            endpoint: API 路徑（如 /schedule/getgamedatas）
            data: POST 資料
        
        Returns:
            JSON 回應
        """
        return self._send_request(endpoint, data, parse_json=True)
    
    def post_api_html(self, endpoint: str, data: dict) -> str:
        """
        發送 POST 請求到 CPBL API（HTML 回應）
        
        Args:
            endpoint: API 路徑（如 /stats/recordall）
            data: POST 資料
        
        Returns:
            HTML 字串
        """
        return self._send_request(endpoint, data, parse_json=False)


# 提供全域實例
_api_instance: Optional[CPBLAPI] = None

def get_api() -> CPBLAPI:
    """取得 CPBL API 實例（singleton）"""
    global _api_instance
    if _api_instance is None:
        _api_instance = CPBLAPI()
    return _api_instance


def get_csrf_token(force_refresh: bool = False) -> str:
    """取得 CSRF token（便捷函式）"""
    return get_api().fetch_csrf_token(force_refresh)


def post_api(endpoint: str, data: dict) -> dict:
    """發送 POST 請求，回傳 JSON（便捷函式）"""
    return get_api().post_api(endpoint, data)


def post_api_html(endpoint: str, data: dict) -> str:
    """發送 POST 請求，回傳 HTML（便捷函式）"""
    return get_api().post_api_html(endpoint, data)


def fetch_game_datas(year: int, kind: str = 'A') -> list[dict]:
    """
    取得整年比賽資料（含 TTL 快取）
    
    統一處理 API 呼叫 + JSON 雙重解析，各 script 不需重複寫。
    
    Args:
        year: 年份
        kind: 賽事類型代碼
    
    Returns:
        解析後的比賽 dict 列表
    """
    api = get_api()
    result = api._send_request('/schedule/getgamedatas', {
        'calendar': f'{year}/01/01',
        'location': '',
        'kindCode': kind
    }, parse_json=True, use_cache=True)

    if not result.get('Success'):
        raise ValueError(f'API 回應失敗: {result}')

    return json.loads(result.get('GameDatas', '[]'))


# ─── 共用常數與工具函式 ───

# 賽事類型對照表
KIND_NAMES = {
    'A': '一軍例行賽', 'B': '一軍明星賽', 'C': '一軍總冠軍賽',
    'D': '二軍例行賽', 'E': '一軍季後挑戰賽', 'F': '二軍總冠軍賽',
    'G': '一軍熱身賽', 'H': '未來之星邀請賽', 'X': '國際交流賽',
}

# 球隊名稱模糊匹配對照表
TEAM_ALIASES = {
    '兄弟': '中信兄弟', '中信': '中信兄弟', '中信兄弟': '中信兄弟',
    '統一': '統一7-ELEVEn獅', '獅': '統一7-ELEVEn獅', '統一7-ELEVEn獅': '統一7-ELEVEn獅',
    '統一獅': '統一7-ELEVEn獅', '統一7-11獅': '統一7-ELEVEn獅',
    '樂天': '樂天桃猿', '桃猿': '樂天桃猿', '樂天桃猿': '樂天桃猿', 'Lamigo': '樂天桃猿',
    '富邦': '富邦悍將', '悍將': '富邦悍將', '富邦悍將': '富邦悍將',
    '味全': '味全龍', '龍': '味全龍', '味全龍': '味全龍',
    '台鋼': '台鋼雄鷹', '雄鷹': '台鋼雄鷹', '台鋼雄鷹': '台鋼雄鷹',
}


def resolve_team(team_input: str) -> Optional[str]:
    """模糊匹配球隊名稱，回傳正式名稱或 None"""
    if team_input in TEAM_ALIASES.values():
        return team_input
    for alias, full_name in TEAM_ALIASES.items():
        if team_input in alias or alias in team_input:
            return full_name
    return None


def resolve_team_cli(team_input: Optional[str]) -> Optional[str]:
    """CLI 用球隊名稱模糊匹配，自動輸出提示訊息到 stderr"""
    if not team_input:
        return None
    team = resolve_team(team_input)
    if team:
        if team != team_input:
            print(f'✅ 「{team_input}」→「{team}」', file=sys.stderr)
    else:
        print(f'⚠️ 找不到球隊「{team_input}」', file=sys.stderr)
    return team


def validate_date(value: str) -> str:
    """驗證日期格式 YYYY-MM-DD（嚴格零補齊），無效則印出錯誤並 exit"""
    if len(value) == 10 and value[4] == '-' and value[7] == '-':
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            pass
    print(f'⚠️ --date 格式應為 YYYY-MM-DD，例如 2025-03-29', file=sys.stderr)
    sys.exit(1)


def validate_month(value: str) -> str:
    """驗證月份格式 YYYY-MM，無效則印出錯誤並 exit"""
    if len(value) == 7 and value[4] == '-':
        try:
            datetime.strptime(value + '-01', '%Y-%m-%d')
            return value
        except ValueError:
            pass
    print(f'⚠️ --month 格式應為 YYYY-MM，例如 2025-03', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    # 測試
    api = CPBLAPI()
    
    print('測試 CSRF token 取得...')
    token = api.fetch_csrf_token()
    print(f'Token: {token[:20]}...')
    print(f'快取位置: {TOKEN_CACHE_FILE}')
    
    print('\n測試 post_api()...')
    result = api.post_api('/schedule/getgamedatas', {
        'calendar': '2025/01/01',
        'location': '',
        'kindCode': 'A'
    })
    
    if result.get('Success'):
        games = json.loads(result.get('GameDatas', '[]'))
        print(f'✅ 取得 {len(games)} 場 2025 年比賽')
    else:
        print('❌ API 呼叫失敗')
