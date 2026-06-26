#!/usr/bin/env python3
"""
collectors/cookie_db.py - SQLite Cookie持久化模块

功能：
1. SQLite存储，支持加密、分域隔离
2. 自动清理过期Cookie
3. 多域名Cookie管理
4. 与Playwright/BrowserContext无缝集成

与 base.py 的 StructuredItem 完全兼容（Cookie记录 → 可序列化为dict）

Usage:
    db = CookieDatabase()
    db.save_cookies([...], 'github.com')
    cookies = db.get_cookies('github.com')
    context.add_cookies(cookies)

    # 多域名管理
    manager = MultiDomainCookieManager()
    cookies = manager.get_all_cookies_for_request('https://api.github.com/repos/...')
"""

import sqlite3
import json
import time
import hashlib
import os
import uuid
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


# ==================== 数据结构 ====================

@dataclass
class CookieRecord:
    """单个Cookie记录（兼容StructuredItem的dataclass风格）"""
    domain: str
    name: str
    value: str
    path: str
    expires: float
    http_only: bool
    secure: bool
    same_site: Optional[str]
    created_at: float
    last_used: float
    use_count: int

    @property
    def is_expired(self) -> bool:
        return self.expires > 0 and self.expires < time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'domain': self.domain,
            'name': self.name,
            'value': self.value,
            'path': self.path,
            'expires': self.expires,
            'httpOnly': self.http_only,
            'secure': self.secure,
            'sameSite': self.same_site,
        }


# ==================== 加密支持 ====================

try:
    from cryptography.fernet import Fernet
    HAS_FERNET = True
except ImportError:
    HAS_FERNET = False


# ==================== CookieDatabase ====================

class CookieDatabase:
    """
    SQLite Cookie持久化存储

    特性：
    1. 加密存储（Fernet，对称加密；无cryptography时fallback到XOR）
    2. 按域名索引，高效查询
    3. 自动清理过期Cookie
    4. 记录使用次数和最后使用时间

    Usage:
        db = CookieDatabase('./data/cookies.db')
        db.save_cookies(playwright_cookies, 'github.com')
        cookies = db.get_cookies('github.com')
        context.add_cookies(cookies)
    """

    def __init__(self, db_path: str = None, encryption_key: str = None):
        if db_path is None:
            base = Path.home() / ".openclaw" / "data"
            base.mkdir(parents=True, exist_ok=True)
            db_path = str(base / "cookies.db")

        self.db_path = db_path
        self.encryption_key = encryption_key or self._generate_key()
        self._init_cipher()
        self._init_db()

    def _init_cipher(self):
        """初始化加密器（Fernet或XOR fallback）"""
        if HAS_FERNET:
            if self.encryption_key:
                try:
                    # 尝试作为原生Fernet key（44字符，URL-safe base64）
                    self._fernet = Fernet(self.encryption_key.encode())
                except Exception:
                    # 不合法，当作旧XOR密码，派生Fernet key
                    self._fernet = Fernet(self._derive_key(self.encryption_key))
            else:
                fkey = Fernet.generate_key()
                self._fernet = Fernet(fkey)
        else:
            self._fernet = None

    def _derive_key(self, password: str) -> bytes:
        """从密码派生Fernet key"""
        import hashlib as _hm
        import base64 as _b64
        raw = _hm.sha256(password.encode()).digest()
        return _b64.urlsafe_b64encode(raw)

    def _generate_key(self) -> str:
        """生成机器相关的密钥"""
        machine_id = uuid.getnode()
        return hashlib.sha256(str(machine_id).encode()).hexdigest()[:32]

    def _init_db(self):
        """初始化数据库表"""
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cookies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT NOT NULL,
                    name TEXT NOT NULL,
                    value_encrypted TEXT NOT NULL,
                    path TEXT DEFAULT '/',
                    expires REAL DEFAULT 0,
                    http_only INTEGER DEFAULT 0,
                    secure INTEGER DEFAULT 0,
                    same_site TEXT,
                    created_at REAL NOT NULL,
                    last_used REAL NOT NULL,
                    use_count INTEGER DEFAULT 0,
                    UNIQUE(domain, name)
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_domain ON cookies(domain)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_expires ON cookies(expires)')
            conn.commit()

    @contextmanager
    def _get_conn(self):
        """获取数据库连接（自动提交/回滚）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}") from e
        finally:
            conn.close()

    # ---- 加密 ----

    def _encrypt(self, value: str) -> str:
        """加密值（Fernet或XOR fallback）"""
        if not value:
            return ''
        if HAS_FERNET:
            return self._fernet.encrypt(value.encode()).decode()
        else:
            import logging
            logging.warning("Using XOR encryption (insecure). Install cryptography for better security.")
            key_bytes = self.encryption_key.encode()
            value_bytes = value.encode()
            result = bytearray()
            for i, b in enumerate(value_bytes):
                result.append(b ^ key_bytes[i % len(key_bytes)])
            return result.hex()

    def _decrypt(self, encrypted: str) -> str:
        """解密值（Fernet或XOR fallback）"""
        if not encrypted:
            return ''
        if HAS_FERNET:
            return self._fernet.decrypt(encrypted.encode()).decode()
        else:
            import logging
            logging.warning("Using XOR decryption (insecure). Install cryptography for better security.")
            key_bytes = self.encryption_key.encode()
            encrypted_bytes = bytes.fromhex(encrypted)
            result = bytearray()
            for i, b in enumerate(encrypted_bytes):
                result.append(b ^ key_bytes[i % len(key_bytes)])
            return result.decode()

    # ---- CRUD 操作 ----

    def save_cookie(self,
                    domain: str,
                    name: str,
                    value: str,
                    path: str = '/',
                    expires: float = -1,
                    http_only: bool = False,
                    secure: bool = False,
                    same_site: str = None):
        """保存单个Cookie（UPSERT）"""
        with self._get_conn() as conn:
            # 已有则更新use_count
            existing = conn.execute(
                'SELECT use_count FROM cookies WHERE domain=? AND name=?',
                (domain, name)
            ).fetchone()

            use_count = (existing['use_count'] + 1) if existing else 1

            conn.execute('''
                INSERT OR REPLACE INTO cookies
                (domain, name, value_encrypted, path, expires, http_only, secure, same_site,
                 created_at, last_used, use_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                domain, name, self._encrypt(value), path, expires,
                int(http_only), int(secure), same_site,
                time.time(), time.time(), use_count
            ))

    def save_cookies(self, cookies: List[Dict], domain: str):
        """
        批量保存Cookie

        Args:
            cookies: Playwright格式的Cookie列表
                    [{name, value, domain, path, expires, httpOnly, secure, sameSite}, ...]
            domain: 目标域名
        """
        for c in cookies:
            self.save_cookie(
                domain=domain,
                name=c.get('name', ''),
                value=c.get('value', ''),
                path=c.get('path', '/'),
                expires=c.get('expires', -1),
                http_only=c.get('httpOnly', False),
                secure=c.get('secure', False),
                same_site=c.get('sameSite'),
            )

    def get_cookies(self,
                    domain: str,
                    include_expired: bool = False) -> List[Dict]:
        """
        获取域名的Cookie

        Returns:
            Playwright格式的Cookie列表（可直接用于 context.add_cookies）
        """
        with self._get_conn() as conn:
            if include_expired:
                rows = conn.execute('''
                    SELECT * FROM cookies WHERE domain=? ORDER BY last_used DESC
                ''', (domain,)).fetchall()
            else:
                rows = conn.execute('''
                    SELECT * FROM cookies
                    WHERE domain=? AND (expires < 0 OR expires > ?)
                    ORDER BY last_used DESC
                ''', (domain, time.time())).fetchall()

            result = []
            for row in rows:
                record = CookieRecord(
                    domain=row['domain'],
                    name=row['name'],
                    value=self._decrypt(row['value_encrypted']),
                    path=row['path'],
                    expires=row['expires'],
                    http_only=bool(row['http_only']),
                    secure=bool(row['secure']),
                    same_site=row['same_site'],
                    created_at=row['created_at'],
                    last_used=row['last_used'],
                    use_count=row['use_count'],
                )
                result.append(record.to_dict())
            return result

    def delete_cookie(self, domain: str, name: str):
        """删除单个Cookie"""
        with self._get_conn() as conn:
            conn.execute('DELETE FROM cookies WHERE domain=? AND name=?',
                        (domain, name))

    def delete_expired(self) -> int:
        """清理过期Cookie，返回删除数量"""
        with self._get_conn() as conn:
            cursor = conn.execute(
                'DELETE FROM cookies WHERE expires > 0 AND expires < ?',
                (time.time(),)
            )
            return cursor.rowcount

    def delete_domain(self, domain: str) -> int:
        """删除某域名的所有Cookie"""
        with self._get_conn() as conn:
            cursor = conn.execute('DELETE FROM cookies WHERE domain=?', (domain,))
            return cursor.rowcount

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._get_conn() as conn:
            total = conn.execute('SELECT COUNT(*) FROM cookies').fetchone()[0]
            expired = conn.execute(
                'SELECT COUNT(*) FROM cookies WHERE expires > 0 AND expires < ?',
                (time.time(),)
            ).fetchone()[0]
            domains = conn.execute(
                'SELECT COUNT(DISTINCT domain) FROM cookies'
            ).fetchone()[0]
            return {
                'total': total,
                'expired': expired,
                'domains': domains,
                'db_path': self.db_path,
            }


# ==================== MultiDomainCookieManager ====================

class MultiDomainCookieManager:
    """
    多域名Cookie管理器

    功能：
    1. 域名组管理（如 github.com/api.github.com 共用Cookie）
    2. 获取请求对应的所有相关Cookie

    Usage:
        manager = MultiDomainCookieManager()
        cookies = manager.get_all_cookies_for_request('https://api.github.com/repos/...')
        context.add_cookies(cookies)
    """

    DOMAIN_GROUPS = {
        'github': ['github.com', 'www.github.com', 'api.github.com', 'gist.github.com'],
        'zhihu': ['zhihu.com', 'www.zhihu.com', 'api.zhihu.com'],
        'baidu': ['baidu.com', 'www.baidu.com', 'tieba.baidu.com'],
        'aliyun': ['aliyun.com', 'www.aliyun.com', 'help.aliyun.com'],
        'douban': ['douban.com', 'www.douban.com', 'accounts.douban.com'],
    }

    def __init__(self, db_path: str = None):
        self.db = CookieDatabase(db_path)
        self._reverse_map: Dict[str, str] = {}
        for group, domains in self.DOMAIN_GROUPS.items():
            for d in domains:
                self._reverse_map[d] = group

    def get_group(self, domain: str) -> str:
        """获取域名所属的组名"""
        return self._reverse_map.get(domain, domain)

    def get_all_cookies_for_request(self, url: str) -> List[Dict]:
        """
        获取请求URL对应的所有相关Cookie

        包括：主域名 + 同组所有子域名的Cookie
        """
        parsed = urlparse(url)
        base_domain = parsed.netloc
        group = self.get_group(base_domain)

        relevant_domains = self.DOMAIN_GROUPS.get(group, [base_domain])
        if base_domain not in relevant_domains:
            relevant_domains.append(base_domain)

        all_cookies = []
        seen = set()
        for domain in relevant_domains:
            cookies = self.db.get_cookies(domain)
            for c in cookies:
                key = f"{c['domain']}:{c['name']}"
                if key not in seen:
                    seen.add(key)
                    all_cookies.append(c)

        return all_cookies

    def sync_to_context(self, url: str, context):
        """
        将相关Cookie同步到Playwright BrowserContext

        Args:
            url: 目标URL
            context: playwright BrowserContext
        """
        cookies = self.get_all_cookies_for_request(url)
        if cookies:
            playwright_cookies = [
                {
                    'name': c['name'],
                    'value': c['value'],
                    'domain': c['domain'],
                    'path': c['path'],
                    'expires': c['expires'] if c['expires'] > 0 else -1,
                    'httpOnly': c.get('httpOnly', False),
                    'secure': c.get('secure', False),
                }
                for c in cookies
            ]
            context.add_cookies(playwright_cookies)

    def save_from_context(self, url: str, context):
        """从BrowserContext保存Cookie到数据库"""
        parsed = urlparse(url)
        domain = parsed.netloc
        cookies = context.cookies()
        self.db.save_cookies(cookies, domain)


# ---- CLI ----

def main():
    import argparse
    from urllib.parse import urlparse

    parser = argparse.ArgumentParser(description='Cookie DB CLI')
    parser.add_argument('command', choices=['status', 'export', 'delete-expired'])
    parser.add_argument('--domain', help='指定域名')
    args = parser.parse_args()

    db = CookieDatabase()

    if args.command == 'status':
        stats = db.get_statistics()
        print(f"Total cookies: {stats['total']}")
        print(f"Expired: {stats['expired']}")
        print(f"Domains: {stats['domains']}")
        print(f"DB path: {stats['db_path']}")

        # 按域名分组统计
        with db._get_conn() as conn:
            rows = conn.execute('''
                SELECT domain, COUNT(*) as cnt
                FROM cookies
                GROUP BY domain
                ORDER BY cnt DESC
                LIMIT 10
            ''').fetchall()
            print("\nTop domains:")
            for row in rows:
                print(f"  {row['domain']}: {row['cnt']}")

    elif args.command == 'export':
        domain = args.domain or 'github.com'
        cookies = db.get_cookies(domain)
        print(json.dumps(cookies, indent=2, ensure_ascii=False))

    elif args.command == 'delete-expired':
        deleted = db.delete_expired()
        print(f"Deleted {deleted} expired cookies")


if __name__ == '__main__':
    import sys
    sys.exit(main())
