"""
AI前沿哨兵 - 主采集脚本
负责协调各信息源采集任务
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from parsers.github_trending import fetch_github_trending
from parsers.arxiv import fetch_arxiv_papers
from parsers.hackernews import fetch_hackernews
from parsers.twitter_x import fetch_twitter
from parsers.blog_rss import fetch_blog_rss
from parsers.web_news import parse_web_news


class DataCollector:
    """数据采集器主类"""
    
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        self.output_dir = Path(__file__).parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self.sources = self._load_config("sources.yaml")
        self.settings = self._load_config("settings.yaml")
        self.schedule = self._load_config("schedule.yaml")
        
        # 采集结果存储
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }
    
    def _load_config(self, filename):
        """加载配置文件"""
        config_path = self.config_dir / filename
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _save_results(self):
        """保存采集结果"""
        output_file = self.output_dir / f"raw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        return output_file
    
    def collect_all(self):
        """采集所有启用的信息源"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始采集...")
        
        for source_name, source_config in self.sources.items():
            # 跳过列表类型的配置（由其他源处理）
            if isinstance(source_config, list):
                continue
            if not source_config.get("enabled", True):
                print(f"  ⏭️  跳过 {source_name} (已禁用)")
                continue
            
            try:
                self._collect_source(source_name, source_config)
            except Exception as e:
                print(f"  ❌ {source_name} 采集失败: {e}")
                self.results["sources"][source_name] = {
                    "status": "error",
                    "error": str(e),
                    "items": []
                }
        
        # 保存结果
        output_file = self._save_results()
        print(f"\n✅ 采集完成，结果已保存到: {output_file}")
        
        return self.results
    
    def collect_source(self, source_name):
        """采集指定信息源"""
        source_config = self.sources.get(source_name)
        if not source_config:
            print(f"❌ 未找到信息源: {source_name}")
            return None
        
        # 跳过列表类型的配置
        if isinstance(source_config, list):
            print(f"❌ {source_name} 是列表类型，无法单独采集")
            return None
        
        if not source_config.get("enabled", True):
            print(f"⏭️  信息源 {source_name} 已禁用")
            return None
        
        try:
            result = self._collect_source(source_name, source_config)
            output_file = self._save_results()
            print(f"✅ {source_name} 采集完成，结果已保存到: {output_file}")
            return result
        except Exception as e:
            print(f"❌ {source_name} 采集失败: {e}")
            return None
    
    def _collect_source(self, source_name, source_config):
        """内部方法：采集单个信息源"""
        print(f"  📡 正在采集 {source_name}...")
        
        start_time = time.time()
        items = []
        
        # 根据源类型调用对应的解析器
        if source_name == "github":
            items = fetch_github_trending(source_config)
        elif source_name == "arxiv":
            items = fetch_arxiv_papers(source_config)
        elif source_name == "hackernews":
            items = fetch_hackernews(source_config)
        elif source_name == "twitter":
            items = fetch_twitter(source_config, self.settings.get("twitter", {}))
        elif source_name == "blogs":
            items = fetch_blog_rss(source_config)
        elif source_name == "chinese_ai_companies":
            items = parse_web_news({"chinese_ai_companies": source_config})
        elif source_name == "custom_feeds":
            # 自定义RSS源，复用blog_rss解析器
            items = fetch_blog_rss({"enabled": True, "limit_per_feed": 10, "feeds": source_config if isinstance(source_config, list) else [source_config]})
        elif source_name == "rsshub":
            # RSSHub实例，暂不处理（需要特殊配置）
            print(f"    ⏭️  RSSHub实例需要单独配置代理")
            return []
        else:
            print(f"    ⚠️  未知的源类型: {source_name}")
            return []
        
        elapsed = time.time() - start_time
        print(f"    ✅ 获取 {len(items)} 条记录，耗时 {elapsed:.2f}s")
        
        self.results["sources"][source_name] = {
            "status": "success",
            "count": len(items),
            "items": items
        }
        
        return items
    
    def get_status(self):
        """获取采集状态"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }
        
        for source_name, source_config in self.sources.items():
            last_result = self.results.get("sources", {}).get(source_name, {})
            status["sources"][source_name] = {
                "enabled": source_config.get("enabled", True),
                "status": last_result.get("status", "unknown"),
                "count": last_result.get("count", 0)
            }
        
        return status


def main():
    parser = argparse.ArgumentParser(description="AI前沿哨兵 - 信息采集工具")
    parser.add_argument("--all", action="store_true", help="采集所有信息源")
    parser.add_argument("--source", type=str, help="指定采集的信息源")
    parser.add_argument("--status", action="store_true", help="显示采集状态")
    
    args = parser.parse_args()
    
    collector = DataCollector()
    
    if args.all:
        collector.collect_all()
    elif args.source:
        collector.collect_source(args.source)
    elif args.status:
        status = collector.get_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
        print("\n示例:")
        print("  python collect.py --all          # 采集所有信息源")
        print("  python collect.py --source github  # 仅采集GitHub")
        print("  python collect.py --status      # 查看采集状态")


if __name__ == "__main__":
    main()
