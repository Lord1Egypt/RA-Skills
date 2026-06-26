"""
Claw-News Main Entry Point
主入口脚本
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config, Settings
from interest_manager import InterestManager
from search_engine import SearchEngine, SearchResult
from result_aggregator import ResultAggregator
from digest_generator import DigestGenerator


class NewsmanAgent:
    """Newsman 主代理"""
    
    def __init__(self):
        self.config = Config()
        self.interest_manager = InterestManager(self.config)
        self.search_engine = SearchEngine(self.config)
        self.aggregator = ResultAggregator()
        self.generator = DigestGenerator()
    
    def run_daily_digest(self, dry_run: bool = False) -> str:
        """执行每日简报生成"""
        print("🚀 启动 Claw-News 每日简报生成\n")
        
        # 1. 加载关注列表
        interests_data = self.config.load_interests()
        interests = self.interest_manager.interests
        
        if not interests:
            print("⚠️ 关注列表为空，请先添加关注项")
            return "关注列表为空"
        
        print(f"📋 加载了 {len(interests)} 个关注项\n")
        
        # 2. 执行搜索
        search_results = []
        queries = self.interest_manager.get_search_queries()
        
        for query_info in queries:
            print(f"🔍 搜索: {query_info['value']} (查询: {query_info['query']})")
            
            result = self.search_engine.search(query_info['query'])
            
            # 标记 interest_id
            if result['success']:
                for r in result['results']:
                    r.interest_id = query_info['id']
            
            search_results.append(result)
            
            # 简单延时避免请求过快
            import time
            time.sleep(0.5)
        
        # 3. 聚合结果
        print(f"\n📊 聚合搜索结果...")
        categorized = self.aggregator.aggregate(search_results)
        
        if not categorized:
            print("⚠️ 未找到任何新闻")
            return "未找到新闻"
        
        total_count = sum(len(v) for v in categorized.values())
        print(f"✅ 聚合完成: {total_count} 条新闻，{len(categorized)} 个分类\n")
        
        # 4. 生成简报
        print("📝 生成简报...")
        digest = self.generator.generate(
            categorized, 
            interests_data,
            self.config.settings.to_dict()
        )
        
        # 5. 输出或推送
        if dry_run:
            print("\n" + "="*60)
            print("📄 简报预览 (Dry Run)")
            print("="*60)
            print(digest)
            return digest
        else:
            # 保存到文件
            self._save_digest(digest)
            
            # 推送
            self._push_digest(digest, interests_data)
            
            print(f"\n✅ 简报已生成并推送")
            return digest
    
    def _save_digest(self, digest: str):
        """保存简报到文件"""
        from pathlib import Path
        
        # 创建输出目录
        output_dir = self.config.BASE_DIR / "output"
        output_dir.mkdir(exist_ok=True)
        
        # 生成文件名
        filename = f"digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(digest)
        
        print(f"💾 简报已保存: {filepath}")
    
    def _push_digest(self, digest: str, interests_data: Dict):
        """推送简报到 Channel"""
        channel = self.config.settings.delivery_channel
        
        if channel == "slack":
            self._push_to_slack(digest)
        elif channel == "terminal":
            print("\n" + "="*60)
            print(digest)
            print("="*60)
        else:
            print(f"⚠️ 未知的推送渠道: {channel}")
    
    def _push_to_slack(self, digest: str):
        """推送到 Slack"""
        # 这里可以调用 OpenClaw 的 message 工具
        # 简化实现：写入文件并提示
        print(f"📤 推送到 Slack 频道: {self.config.settings.slack_channel}")
        
        # 如果运行在 OpenClaw 环境中，可以使用 message 工具
        # 否则提示用户手动发送
        if os.getenv("OPENCLAW_ENV"):
            try:
                # 调用 OpenClaw message 工具
                import subprocess
                result = subprocess.run(
                    ["openclaw", "message", "send", "--channel", "slack", digest],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("✅ Slack 推送成功")
                else:
                    print(f"⚠️ Slack 推送失败: {result.stderr}")
            except Exception as e:
                print(f"⚠️ Slack 推送失败: {e}")
    
    def search_and_show(self, query: str):
        """搜索并直接显示结果"""
        print(f"🔍 搜索: {query}\n")
        
        result = self.search_engine.search(query)
        
        if result['success']:
            print(f"✅ 使用 {result['source']} 搜索成功\n")
            print(f"找到 {len(result['results'])} 条结果:\n")
            
            for i, r in enumerate(result['results'][:5], 1):
                print(f"{i}. {r.title}")
                print(f"   📰 {r.source} | 🕐 {r.published_at[:16] if r.published_at else '未知'}")
                print(f"   🔗 {r.url}")
                if r.summary:
                    summary = r.summary[:150] + "..." if len(r.summary) > 150 else r.summary
                    print(f"   📝 {summary}")
                print()
        else:
            print(f"❌ 搜索失败: {result.get('error', '未知错误')}")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="Claw-News - 智能每日新闻简报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python newsman.py --mode digest              # 生成每日简报
  python newsman.py --mode digest --dry-run    # 预览模式
  python newsman.py --mode search -q "AI"      # 搜索关键词
  python newsman.py --mode list                # 查看关注列表
        """
    )
    
    parser.add_argument("--mode", "-m", 
                       choices=["digest", "search", "list"],
                       default="digest",
                       help="运行模式 (默认: digest)")
    parser.add_argument("--query", "-q", type=str,
                       help="搜索关键词 (search 模式)")
    parser.add_argument("--dry-run", "-d", action="store_true",
                       help="预览模式，不实际推送")
    
    args = parser.parse_args()
    
    # 创建 agent
    agent = NewsmanAgent()
    
    if args.mode == "digest":
        agent.run_daily_digest(dry_run=args.dry_run)
    
    elif args.mode == "search":
        if not args.query:
            print("❌ 请提供搜索关键词: --query <关键词>")
            sys.exit(1)
        agent.search_and_show(args.query)
    
    elif args.mode == "list":
        agent.interest_manager.print_list()


if __name__ == "__main__":
    main()
