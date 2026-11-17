# 详细参考 - feedstream-monitor-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import json
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

STORE_DIR = Path.home() / "workspace" / "feedstream" / "monitor"
STORE_DIR.mkdir(parents=True, exist_ok=True)

class FeedStreamMonitor:
    """安全公告流监控（免费版核心）"""

    SEVERITY_KEYWORDS = {
        "critical": ["critical", "紧急", "rce", "remote code execution", "zero-day", "0day"],
        "high": ["high", "严重", "privilege escalation", "sql injection", "xss"],
        "medium": ["medium", "中等", "dos", "denial of service", "bypass"],
        "low": ["low", "低", "information disclosure", "minor"]
    }

    def __init__(self):
        self.store = STORE_DIR
        self.feeds_file = self.store / "feeds.json"
        self.advisories_file = self.store / "advisories.json"
        for f in [self.feeds_file, self.advisories_file]:
            if not f.exists():
                f.write_text("[]", encoding="utf-8")

    def add_feed(self, name, url, feed_type="rss", category="general"):
        """添加订阅源"""
        feeds = json.loads(self.feeds_file.read_text(encoding="utf-8"))
        feed = {
            "id": f"feed_{len(feeds)+1:03d}",
            "name": name, "url": url,
            "type": feed_type, "category": category,
            "status": "active",
            "added_at": datetime.now().isoformat(),
            "last_fetched": None, "fetch_count": 0
        }
        feeds.append(feed)
        self.feeds_file.write_text(json.dumps(feeds, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ 订阅源已添加：{feed['id']} - {name}")
        return feed

    def list_feeds(self):
        """列出所有订阅源"""
        feeds = json.loads(self.feeds_file.read_text(encoding="utf-8"))
        print(f"\n{'ID':<12} {'名称':<20} {'类别':<10} {'状态':<10} {'抓取次数':<10}")
        print("-" * 65)
        for f in feeds:
            print(f"{f['id']:<12} {f['name']:<20} {f['category']:<10} "
                  f"{f['status']:<10} {f['fetch_count']}")
        return feeds

    def fetch_feed(self, feed_id):
        """抓取单个订阅源"""
        feeds = json.loads(self.feeds_file.read_text(encoding="utf-8"))
        feed = next((f for f in feeds if f["id"] == feed_id), None)
        if not feed:
            print(f"✗ 未找到订阅源：{feed_id}")
            return []

        try:
            req = urllib.request.Request(feed["url"], headers={"User-Agent": "FeedStreamMonitor/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read().decode("utf-8", errors="ignore")

            items = self._parse_feed(content, feed["type"])
            new_items = self._deduplicate(items)

            for item in new_items:
                item["severity"] = self._classify_severity(item["title"] + " " + item.get("description", ""))
                item["source_feed"] = feed["name"]
                item["category"] = feed["category"]

            advisories = json.loads(self.advisories_file.read_text(encoding="utf-8"))
            advisories.extend(new_items)
            self.advisories_file.write_text(
                json.dumps(advisories, ensure_ascii=False, indent=2), encoding="utf-8")

            feed["last_fetched"] = datetime.now().isoformat()
            feed["fetch_count"] += 1
            self.feeds_file.write_text(json.dumps(feeds, ensure_ascii=False, indent=2), encoding="utf-8")

            print(f"✓ 抓取成功：{feed['name']}（新增{len(new_items)}条，总计{len(advisories)}条）")
            return new_items

        except Exception as e:
            print(f"✗ 抓取失败：{feed['name']} - {e}")
            return []

    def _parse_feed(self, content, feed_type):
        """解析RSS/Atom"""
        items = []
        try:
            root = ET.fromstring(content)

            if feed_type == "atom":
                entries = root.findall("{http://www.w3.org/2005/Atom}entry")
                for entry in entries:
                    title = entry.find("{http://www.w3.org/2005/Atom}title")
                    link = entry.find("{http://www.w3.org/2005/Atom}link")
                    summary = entry.find("{http://www.w3.org/2005/Atom}summary")
                    updated = entry.find("{http://www.w3.org/2005/Atom}updated")
                    items.append({
                        "title": title.text if title is not None else "",
                        "link": link.get("href") if link is not None else "",
                        "description": (summary.text[:200] if summary is not None and summary.text else ""),
                        "published": updated.text if updated is not None else "",
                        "fetched_at": datetime.now().isoformat()
                    })
            else:  # rss
                for item in root.iter("item"):
                    title = item.find("title")
                    link = item.find("link")
                    desc = item.find("description")
                    pub = item.find("pubDate")
                    items.append({
                        "title": title.text if title is not None else "",
                        "link": link.text if link is not None else "",
                        "description": (desc.text[:200] if desc is not None and desc.text else ""),
                        "published": pub.text if pub is not None else "",
                        "fetched_at": datetime.now().isoformat()
                    })
        except ET.ParseError as e:
            print(f"解析失败：{e}")
        return items

    def _deduplicate(self, items):
        """去重（基于标题+链接哈希）"""
        existing = json.loads(self.advisories_file.read_text(encoding="utf-8"))
        seen_hashes = {self._hash(a["title"], a.get("link", "")) for a in existing}

        new_items = []
        for item in items:
            h = self._hash(item["title"], item.get("link", ""))
            if h not in seen_hashes:
                item["id"] = h[:16]
                new_items.append(item)
                seen_hashes.add(h)
        return new_items

    def _hash(self, title, link):
        """生成唯一哈希"""
        return hashlib.md5(f"{title}|{link}".encode()).hexdigest()

    def _classify_severity(self, text):
        """严重性分级"""
        text_lower = text.lower()
        for severity, keywords in self.SEVERITY_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return severity
        return "info"

    def search(self, keyword=None, severity=None, limit=20):
        """搜索公告"""
        advisories = json.loads(self.advisories_file.read_text(encoding="utf-8"))

        if keyword:
            keyword_lower = keyword.lower()
            advisories = [a for a in advisories
                         if keyword_lower in a["title"].lower()
                         or keyword_lower in a.get("description", "").lower()]

        if severity:
            advisories = [a for a in advisories if a.get("severity") == severity]

        advisories = advisories[-limit:]
        print(f"\n找到 {len(advisories)} 条公告：")
        print(f"{'严重性':<10} {'标题':<50} {'来源':<15}")
        print("-" * 80)
        for a in advisories:
            print(f"{a.get('severity','info'):<10} {a['title'][:50]:<50} {a.get('source_feed','')[:15]}")
        return advisories

    def stats(self):
        """统计信息"""
        advisories = json.loads(self.advisories_file.read_text(encoding="utf-8"))
        feeds = json.loads(self.feeds_file.read_text(encoding="utf-8"))

        severity_count = {}
        for a in advisories:
            sev = a.get("severity", "info")
            severity_count[sev] = severity_count.get(sev, 0) + 1

        print(f"\n=== 安全公告统计 ===")
        print(f"订阅源数量：{len(feeds)}")
        print(f"公告总数：{len(advisories)}")
        print(f"\n按严重性分布：")
        for sev in ["critical", "high", "medium", "low", "info"]:
            count = severity_count.get(sev, 0)
            print(f"  {sev:<10}: {count}")

monitor = FeedStreamMonitor()

monitor.add_feed("NVD漏洞公告", "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml", "rss", "cve")
monitor.add_feed("安全客", "https://api.anquanke.com/data/v1/rss", "rss", "blog")

monitor.list_feeds()

monitor.fetch_feed("feed_001")

monitor.search(keyword="Apache")
monitor.search(severity="critical")

monitor.stats()
```

