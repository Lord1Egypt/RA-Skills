#!/usr/bin/env python3
"""
花园感知引擎 — 动态厂商清单 + bloom 评分

核心思想：蜂巢不维护静态厂商清单，而是通过多信号感知"花园中哪些花开了"。
每天先做一轮轻量扫描，再决定去哪采蜜。
"""

import json
import os
import re
import time
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = PROJECT_ROOT / "output" / "vendor_registry.json"


class VendorRegistry:
    """动态厂商注册表 — 花园的地图"""
    
    def __init__(self, path: Optional[Path] = None):
        self.path = path or REGISTRY_PATH
        self.vendors: dict = {}
        self.load()
    
    def load(self):
        if self.path.exists():
            with open(self.path) as f:
                data = json.load(f)
                self.vendors = data.get("vendors", {})
    
    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "last_updated": datetime.now().isoformat(),
            "vendor_count": len(self.vendors),
            "vendors": self.vendors,
        }
        with open(self.path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_or_create(self, name: str, **kwargs) -> dict:
        if name not in self.vendors:
            self.vendors[name] = {
                "name": name,
                "aliases": kwargs.get("aliases", []),
                "category": kwargs.get("category", "discovered"),
                "bloom_score": kwargs.get("bloom_score", 0.3),
                "bloom_history": [],
                "urls": kwargs.get("urls", {}),
                "signals": {},
                "status": "new",
                "first_seen": date.today().isoformat(),
                "last_foraged": None,
                "forage_count": 0,
            }
        return self.vendors[name]
    
    def update_bloom(self, name: str, delta: float, reason: str = ""):
        v = self.vendors.get(name)
        if not v:
            return
        old = v["bloom_score"]
        new = min(1.0, max(0.0, old + delta))
        v["bloom_score"] = round(new, 3)
        v["bloom_history"].append({
            "date": date.today().isoformat(),
            "old": old,
            "new": new,
            "delta": round(delta, 3),
            "reason": reason,
        })
        # 只保留最近30条
        v["bloom_history"] = v["bloom_history"][-30:]
    
    def decay_all(self, rate: float = 0.05):
        """每日自然衰减——没有新信号的厂商逐渐凋谢"""
        for name, v in self.vendors.items():
            if v["status"] != "dormant":
                v["bloom_score"] = round(max(0.0, v["bloom_score"] - rate), 3)
    
    def get_bloom_status(self, name: str) -> str:
        """返回厂商花期状态"""
        score = self.vendors[name]["bloom_score"]
        if score >= 0.7:
            return "盛开"   # 全量采蜜
        elif score >= 0.4:
            return "开花"   # 标准采蜜
        elif score >= 0.2:
            return "含苞"   # 轻量检查
        else:
            return "凋谢"   # 最低限度
    
    def get_forage_targets(self) -> list[dict]:
        """返回今日采蜜目标，按 bloom_score 排序"""
        targets = []
        for name, v in self.vendors.items():
            if v["bloom_score"] >= 0.2:
                targets.append(v)
        targets.sort(key=lambda x: x["bloom_score"], reverse=True)
        return targets
    
    def get_all_sorted(self) -> list[dict]:
        return sorted(self.vendors.values(), key=lambda x: x["bloom_score"], reverse=True)


class GardenScanner:
    """花园感知引擎 — 通过 web search 感知哪些花开了"""
    
    def __init__(self, registry: VendorRegistry, config: dict):
        self.registry = registry
        self.config = config
        self.garden_config = config.get("garden", {})
        self.bloom_config = self.garden_config.get("bloom", {})
    
    def scan(self) -> dict:
        """
        执行一轮花园扫描。
        返回扫描结果摘要。
        """
        results = {
            "date": date.today().isoformat(),
            "scan_time": datetime.now().isoformat(),
            "signals_detected": {},
            "vendors_updated": [],
            "new_vendors": [],
            "status_changes": [],
        }
        
        # Step 1: 自然衰减
        decay_rate = self.bloom_config.get("decay_rate", 0.05)
        self.registry.decay_all(decay_rate)
        
        # Step 2: 采集新闻热度信号
        news_signals = self._scan_news_heat()
        results["signals_detected"]["news_heat"] = news_signals
        
        # Step 3: 采集社区讨论信号
        community_signals = self._scan_community()
        results["signals_detected"]["community"] = community_signals
        
        # Step 4: 合并信号，更新 bloom
        all_signals = self._merge_signals(news_signals, community_signals)
        for vendor_name, signal_score in all_signals.items():
            before = self.registry.vendors.get(vendor_name, {}).get("bloom_score", 0)
            
            v = self.registry.get_or_create(
                vendor_name,
                bloom_score=self.bloom_config.get("new_vendor_boost", 0.15),
            )
            
            # 信号越强，bloom 增幅越大
            delta = signal_score * 0.3  # 归一化
            self.registry.update_bloom(vendor_name, delta, f"信号得分 {signal_score:.2f}")
            
            after = self.registry.vendors[vendor_name]["bloom_score"]
            
            if v["status"] == "new":
                results["new_vendors"].append(vendor_name)
                v["status"] = "discovered"
            
            results["vendors_updated"].append({
                "name": vendor_name,
                "bloom_before": round(before, 3),
                "bloom_after": round(after, 3),
            })
            
            # 检测状态变化
            old_status = self._score_to_status(before)
            new_status = self._score_to_status(after)
            if old_status != new_status:
                results["status_changes"].append({
                    "name": vendor_name,
                    "from": old_status,
                    "to": new_status,
                })
        
        # Step 5: 保存
        self.registry.save()
        
        return results
    
    def _scan_news_heat(self) -> dict:
        """通过 mmx search 采集新闻热度信号"""
        signals = {}
        news_config = self.garden_config.get("signals", {}).get("news_heat", {})
        queries = news_config.get("search_queries", [])
        
        for query in queries:
            try:
                import subprocess
                result = subprocess.run(
                    ["mmx", "search", "query", "--query", query, "--output", "json"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    # mmx search 返回格式：{"organic": [{"title", "link", "snippet", "date"}]}
                    hits = []
                    if isinstance(data, list):
                        hits = data
                    elif isinstance(data, dict):
                        hits = data.get("organic", data.get("results", []))
                    
                    for hit in hits[:15]:
                        title = hit.get("title", "")
                        snippet = hit.get("snippet", "") or hit.get("body", "")
                        # 从搜索结果中识别厂商名
                        vendor_name = self._extract_vendor(title + " " + snippet)
                        if vendor_name:
                            # 近期新闻权重更高
                            date_str = hit.get("date", "")
                            recency = 1.0
                            if date_str:
                                try:
                                    from datetime import datetime as dt
                                    news_date = dt.strptime(date_str[:10], "%Y-%m-%d")
                                    days_ago = (dt.now() - news_date).days
                                    recency = max(0.3, 1.0 - days_ago * 0.1)  # 10天衰减到0.3
                                except:
                                    pass
                            signals[vendor_name] = signals.get(vendor_name, 0) + recency
            except Exception as e:
                signals["_scan_error"] = str(e)
        
        return signals
    
    def _scan_community(self) -> dict:
        """通过 mmx search 采集社区讨论信号"""
        signals = {}
        comm_config = self.garden_config.get("signals", {}).get("community", {})
        queries = comm_config.get("search_queries", [])
        
        for query in queries:
            try:
                import subprocess
                result = subprocess.run(
                    ["mmx", "search", "query", "--query", query, "--output", "json"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    hits = []
                    if isinstance(data, list):
                        hits = data
                    elif isinstance(data, dict):
                        hits = data.get("organic", data.get("results", []))
                    
                    for hit in hits[:15]:
                        title = hit.get("title", "")
                        snippet = hit.get("snippet", "") or hit.get("body", "")
                        vendor_name = self._extract_vendor(title + " " + snippet)
                        if vendor_name:
                            signals[vendor_name] = signals.get(vendor_name, 0) + 0.7
            except Exception as e:
                signals["_scan_error"] = str(e)
        
        return signals
    
    def _merge_signals(self, news: dict, community: dict) -> dict:
        """合并多信号源"""
        merged = {}
        news_weight = self.garden_config.get("signals", {}).get("news_heat", {}).get("weight", 0.35)
        comm_weight = self.garden_config.get("signals", {}).get("community", {}).get("weight", 0.25)
        
        for name, score in news.items():
            if name.startswith("_"):
                continue
            merged[name] = merged.get(name, 0) + score * news_weight
        
        for name, score in community.items():
            if name.startswith("_"):
                continue
            merged[name] = merged.get(name, 0) + score * comm_weight
        
        # 归一化到 0-1
        max_val = max(merged.values()) if merged else 1
        if max_val > 0:
            merged = {k: round(v / max_val, 3) for k, v in merged.items()}
        
        return merged
    
    def _extract_vendor(self, text: str) -> Optional[str]:
        """从文本中识别厂商名"""
        # 已知厂商别名映射
        alias_map = {}
        for name, v in self.registry.vendors.items():
            alias_map[name] = name
            for alias in v.get("aliases", []):
                alias_map[alias] = name
        
        # 也从 config seed_vendors 读取
        seed_vendors = self.config.get("seed_vendors", [])
        for sv in seed_vendors:
            name = sv["name"]
            alias_map[name] = name
            for alias in sv.get("aliases", []):
                alias_map[alias] = name
        
        # 在文本中搜索
        text_lower = text.lower()
        for alias, canonical in alias_map.items():
            if alias.lower() in text_lower:
                return canonical
        
        # 检测新厂商：常见模式
        new_vendor_patterns = [
            r'([\u4e00-\u9fa5]{2,6})(?:大模型|AI|智能|智脑)',
            r'([\w]+)-(?:AI|LM|GPT|LLM)',
        ]
        # 暂不自动添加新厂商，仅记录已知厂商
        
        return None
    
    @staticmethod
    def _score_to_status(score: float) -> str:
        if score >= 0.7:
            return "盛开"
        elif score >= 0.4:
            return "开花"
        elif score >= 0.2:
            return "含苞"
        else:
            return "凋谢"


def init_registry_from_config(config: dict) -> VendorRegistry:
    """从 config.yaml 初始化厂商注册表"""
    registry = VendorRegistry()
    
    for sv in config.get("seed_vendors", []):
        existing = registry.vendors.get(sv["name"])
        if not existing:
            registry.get_or_create(
                sv["name"],
                aliases=sv.get("aliases", []),
                category=sv.get("category", "seed"),
                bloom_score=0.5,  # 种子厂商初始分 0.5
                urls=sv.get("urls", {}),
            )
            registry.vendors[sv["name"]]["status"] = "seed"
        else:
            # 更新已知厂商的 URLs
            if "urls" in sv:
                existing["urls"] = sv["urls"]
            if "aliases" in sv:
                existing["aliases"] = sv.get("aliases", [])
    
    registry.save()
    return registry


if __name__ == "__main__":
    import yaml
    
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # 初始化
    registry = init_registry_from_config(config)
    print(f"✅ 注册表初始化完成：{len(registry.vendors)} 个厂商")
    
    # 扫描
    scanner = GardenScanner(registry, config)
    results = scanner.scan()
    
    print(f"\n📡 花园扫描结果 ({results['date']}):")
    print(f"  信号检测: {len(results['signals_detected'])} 类")
    print(f"  厂商更新: {len(results['vendors_updated'])} 家")
    print(f"  新发现: {len(results['new_vendors'])} 家")
    print(f"  状态变化: {len(results['status_changes'])} 家")
    
    print(f"\n🌸 今日花期:")
    for v in registry.get_all_sorted():
        status = registry.get_bloom_status(v["name"])
        print(f"  {v['name']:8s}  bloom={v['bloom_score']:.3f}  [{status}]")
