#!/usr/bin/env python3
"""
Context-Manager 上下文管理师

AI 驱动的系统性问题分析与解决方案生成工具
让知识从"收藏"变成"认知"
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from functools import wraps
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入核心模块
from modules.collector import ContextCollector
from modules.tagger import MeaningTagger
from modules.thought_tree import ThoughtTreeBuilder
from modules.daily_log import DailyLogManager
from modules.recall import DecisionRecaller
from modules.bridge import ContextBridge
from modules.review import CognitiveReviewer
from modules.ai_analyzer import AIAnalyzer
from modules.cognitive_map import CognitiveMapGenerator


class ContextManager:
    """上下文管理师主类"""
    
    # 超时配置（秒）
    TIMEOUT_CONFIG = {
        "collect": 30,
        "tag": 30,
        "build_tree": 60,
        "recall": 60,
        "daily_log": 30,
        "default": 30
    }
    
    def __init__(self, config_path: str = "~/kb/config.yaml"):
        self.config = self._load_config(config_path)
        self.base_path = Path(self.config.get("base_path", "~/context")).expanduser()
        
        # 验证配置
        self._validate_config()
        
        # 初始化核心模块
        self.collector = ContextCollector(self.config)
        self.tagger = MeaningTagger(self.config)
        self.thought_tree = ThoughtTreeBuilder(self.config)
        self.daily_log_mgr = DailyLogManager(self.config)
        self.recall_mgr = DecisionRecaller(self.config)
        self.bridge_mgr = ContextBridge(self.config)
        self.review_mgr = CognitiveReviewer(self.config)
        self.ai_analyzer = AIAnalyzer(self.config)
        self.cognitive_map_gen = CognitiveMapGenerator(self.config)
        
        logger.info("✅ Context-Manager 初始化完成")
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        import yaml
        config_file = Path(config_path).expanduser()
        if config_file.exists():
            return yaml.safe_load(config_file.read_text())
        return {}
    
    def _validate_config(self):
        """验证配置"""
        # 检查 base_path
        if not self.base_path.exists():
            logger.info(f"创建上下文库目录：{self.base_path}")
            self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 检查必需子目录
        required_dirs = ["inbox", "contexts", "trees", "logs", "reviews"]
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                logger.info(f"创建目录：{dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ 配置验证通过")
    
    # ========== 核心功能 ==========
    
    def collect(self, 
                source_type: str,
                content: str,
                metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        收集上下文
        
        Args:
            source_type: 来源类型 (feishu|wechat|xiaohongshu|inner_cognition|manual)
            content: 内容
            metadata: 可选元数据
        
        Returns:
            收集结果
        """
        logger.info(f"收集 {source_type} 内容")
        
        result = self.collector.collect(source_type, content, metadata)
        
        logger.info(f"✓ 收集完成：{result.get('id')}")
        
        return result
    
    def tag(self, context_id: str, content: str) -> Dict[str, Any]:
        """
        打标（意义标签体系）
        
        Args:
            context_id: 上下文 ID
            content: 内容
        
        Returns:
            打标结果
        """
        logger.info(f"打标 {context_id}")
        
        result = self.tagger.tag(context_id, content)
        
        logger.info(f"✓ 打标完成：{result.get('tags')}")
        
        return result
    
    def build_tree(self, 
                   topic: str,
                   time_range: str = "3months") -> Dict[str, Any]:
        """
        构建思维树
        
        Args:
            topic: 主题
            time_range: 时间范围 (3months|6months|1year)
        
        Returns:
            思维树结果
        """
        logger.info(f"构建思维树：{topic} ({time_range})")
        
        result = self.thought_tree.build(topic, time_range)
        
        logger.info(f"✓ 思维树完成：{len(result.get('bridges', []))} 个桥接")
        
        return result
    
    def daily_log(self, items: List[Dict]) -> Dict[str, Any]:
        """
        认知日志（每日 3 件触动事）
        
        Args:
            items: 触动事列表
                [{
                    "content": "触动事内容",
                    "judgment": "你的判断"
                }]
        
        Returns:
            日志结果
        """
        logger.info(f"创建认知日志：{len(items)} 条")
        
        result = self.daily_log_mgr.create(items)
        
        logger.info(f"✓ 认知日志完成：{result.get('date')}")
        
        return result
    
    def recall(self, decision_context: str) -> Dict[str, Any]:
        """
        决策回溯
        
        Args:
            decision_context: 决策上下文
        
        Returns:
            回溯结果
        """
        logger.info(f"决策回溯：{decision_context[:50]}...")
        
        result = self.recall_mgr.recall(decision_context)
        
        logger.info(f"✓ 决策回溯完成：{len(result.get('similar_decisions', []))} 个类似决策")
        
        return result
    
    def bridge(self, 
               inner_thought: str,
               external_info: str) -> Dict[str, Any]:
        """
        上下文桥接
        
        Args:
            inner_thought: 内心想法
            external_info: 外部信息
        
        Returns:
            桥接结果
        """
        logger.info(f"上下文桥接")
        
        result = self.bridge_mgr.build(inner_thought, external_info)
        
        logger.info(f"✓ 桥接完成：{result.get('type')}")
        
        return result
    
    def ai_boundary(self, items: List[Dict]) -> Dict[str, Any]:
        """
        AI 辅助边界
        
        Args:
            items: 事项列表
                [{
                    "task": "事项",
                    "boundary": "must_self|can_ai"
                }]
        
        Returns:
            边界清单
        """
        logger.info(f"设置 AI 辅助边界：{len(items)} 项")
        
        result = {
            "items": items,
            "must_self": [i for i in items if i["boundary"] == "must_self"],
            "can_ai": [i for i in items if i["boundary"] == "can_ai"],
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"✓ AI 边界完成：{len(result['must_self'])} 项必须自己思考")
        
        return result
    
    def review(self, 
               period: str = "weekly",
               operation: str = "generate_map") -> Dict[str, Any]:
        """
        认知更新（季度删除 + 年度重审）
        
        Args:
            period: 周期 (weekly|quarterly|yearly)
            operation: 操作 (generate_map|delete_redundant|review_core)
        
        Returns:
            回顾结果
        """
        logger.info(f"认知更新：{period} - {operation}")
        
        if operation == "generate_map":
            result = self.cognitive_map_gen.generate(period)
        else:
            result = self.review_mgr.run(period, operation)
        
        logger.info(f"✓ 认知更新完成")
        
        return result
    
    # ========== 一键工作流 ==========
    
    def run(self, 
            source_type: str,
            content: str,
            auto_build_tree: bool = False,
            auto_tag: bool = True) -> Dict[str, Any]:
        """
        一键处理工作流
        
        Args:
            source_type: 来源类型
            content: 内容
            auto_build_tree: 是否自动构建思维树
            auto_tag: 是否自动打标
        
        Returns:
            工作流结果
        """
        start_time = time.time()
        
        result = {
            "workflow_id": f"cm-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "status": "running",
            "steps": {}
        }
        
        try:
            # 步骤 1: 收集
            collect_result = self.collect(source_type, content)
            result["steps"]["collect"] = collect_result
            
            # 步骤 2: 打标
            if auto_tag:
                tag_result = self.tag(
                    collect_result["id"],
                    collect_result.get("content", "")
                )
                result["steps"]["tag"] = tag_result
            
            # 步骤 3: 构建思维树（可选）
            if auto_build_tree:
                # 提取主题
                topic = self._extract_topic(content)
                tree_result = self.build_tree(topic, "3months")
                result["steps"]["build_tree"] = tree_result
            
            # 计算总耗时
            total_time = time.time() - start_time
            result["performance"] = {
                "total_time_ms": int(total_time * 1000),
                "status": "success"
            }
            
            result["status"] = "completed"
            logger.info(f"✅ 工作流完成，总耗时：{result['performance']['total_time_ms']}ms")
            
        except Exception as e:
            total_time = time.time() - start_time
            result["status"] = "failed"
            result["error"] = {
                "code": type(e).__name__,
                "message": str(e),
                "suggestion": "请检查输入内容和系统日志"
            }
            result["performance"] = {
                "total_time_ms": int(total_time * 1000),
                "status": "failed"
            }
            logger.error(f"❌ 工作流失败：{str(e)}", exc_info=True)
        
        return result
    
    def _extract_topic(self, content: str) -> str:
        """提取主题（简化版）"""
        # TODO: 用 AI 提取主题
        lines = content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()[:50]
        return "未命名主题"


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python main.py <command> [args]")
        print("\n可用命令:")
        print("  collect <source> <content>  - 收集上下文")
        print("  tag <id> <content>          - 打标")
        print("  build-tree <topic>          - 构建思维树")
        print("  daily-log                   - 认知日志")
        print("  recall <decision>           - 决策回溯")
        print("  run <source> <content>      - 一键工作流")
        return
    
    cm = ContextManager()
    command = sys.argv[1]
    
    if command == "collect":
        if len(sys.argv) < 4:
            print("❌ 需要 source 和 content")
            return
        result = cm.collect(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "tag":
        if len(sys.argv) < 4:
            print("❌ 需要 id 和 content")
            return
        result = cm.tag(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "build-tree":
        if len(sys.argv) < 3:
            print("❌ 需要 topic")
            return
        result = cm.build_tree(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "run":
        if len(sys.argv) < 4:
            print("❌ 需要 source 和 content")
            return
        result = cm.run(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"❌ 未知命令：{command}")


if __name__ == "__main__":
    main()
