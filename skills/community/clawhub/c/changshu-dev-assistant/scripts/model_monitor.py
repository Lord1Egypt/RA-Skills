#!/usr/bin/env python3
"""
模型性能监控器
为昌叔量身定制的模型性能监控工具, 支持JSON持久化存储
"""

import json
import time
import sys
import os
from typing import Dict, Optional
from pathlib import Path


class ModelPerformanceMonitor:
    """模型性能监控器, 支持持久化到JSON文件"""

    DEFAULT_STATS_PATH = os.path.expanduser("~/.hermes/changshu_model_stats.json")

    def __init__(self, stats_path: str = None):
        """初始化模型性能监控器

        Args:
            stats_path: 统计数据持久化文件路径, 默认 ~/.hermes/changshu_model_stats.json
        """
        self.stats_path = stats_path or self.DEFAULT_STATS_PATH
        self.records: list = []
        self.model_stats: Dict = {}
        self._load()

    def _load(self):
        """从JSON文件加载历史数据"""
        try:
            with open(self.stats_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.records = data.get("records", [])
            self.model_stats = data.get("model_stats", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = []
            self.model_stats = {}

    def _save(self):
        """将数据持久化到JSON文件"""
        os.makedirs(os.path.dirname(self.stats_path), exist_ok=True)
        with open(self.stats_path, "w", encoding="utf-8") as f:
            json.dump({"records": self.records, "model_stats": self.model_stats}, f, ensure_ascii=False, indent=2)

    def record_performance(self, model_name: str, prompt_tokens: int = 0,
                           completion_tokens: int = 0, total_tokens: int = 0,
                           response_time_ms: float = 0.0, success: bool = True,
                           timestamp: float = None):
        """记录模型性能数据

        Args:
            model_name: 模型名称
            prompt_tokens: prompt token数
            completion_tokens: completion token数
            total_tokens: 总token数
            response_time_ms: 响应时间(毫秒)
            success: 是否成功
            timestamp: 时间戳, 默认为当前时间
        """
        if timestamp is None:
            timestamp = time.time()

        record = {
            "model_name": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "response_time_ms": response_time_ms,
            "success": success,
            "timestamp": timestamp,
        }
        self.records.append(record)

        # 更新累计统计
        if model_name not in self.model_stats:
            self.model_stats[model_name] = {
                "total_calls": 0,
                "total_prompt_tokens": 0,
                "total_completion_tokens": 0,
                "total_tokens": 0,
                "total_response_time_ms": 0.0,
                "total_success": 0,
                "avg_total_tokens": 0.0,
                "avg_response_time_ms": 0.0,
                "success_rate": 0.0,
            }

        stats = self.model_stats[model_name]
        stats["total_calls"] += 1
        stats["total_prompt_tokens"] += prompt_tokens
        stats["total_completion_tokens"] += completion_tokens
        stats["total_tokens"] += total_tokens
        stats["total_response_time_ms"] += response_time_ms
        if success:
            stats["total_success"] += 1

        calls = stats["total_calls"]
        stats["avg_total_tokens"] = round(stats["total_tokens"] / calls, 2)
        stats["avg_response_time_ms"] = round(stats["total_response_time_ms"] / calls, 2)
        stats["success_rate"] = round(stats["total_success"] / calls * 100, 2)

        self._save()

    def get_stats(self, model_name: str = None) -> Dict:
        """获取累计统计信息

        Args:
            model_name: 指定模型名, 为None时返回所有模型统计

        Returns:
            单个模型的统计dict, 或所有模型的统计dict
        """
        if model_name is not None:
            return self.model_stats.get(model_name, {})
        return self.model_stats

    def recommend_model(self) -> Optional[str]:
        """综合响应时间和成功率推荐最佳模型

        评分公式: score = success_rate / (avg_response_time_ms + 1)
        分数越高越推荐

        Returns:
            推荐的模型名称, 无数据时返回None
        """
        if not self.model_stats:
            return None

        best_model = None
        best_score = -1.0

        for model_name, stats in self.model_stats.items():
            avg_rt = stats.get("avg_response_time_ms", 0.0)
            sr = stats.get("success_rate", 0.0)
            # 成功率权重高, 响应时间越低越好
            score = sr / (avg_rt + 1.0)
            if score > best_score:
                best_score = score
                best_model = model_name

        return best_model


def main():
    """CLI入口"""
    if len(sys.argv) < 2:
        print("用法: python3 model_monitor.py [stats|recommend]")
        sys.exit(1)

    command = sys.argv[1]
    monitor = ModelPerformanceMonitor()

    if command == "stats":
        stats = monitor.get_stats()
        if not stats:
            print("暂无模型统计数据")
        else:
            print(json.dumps(stats, indent=2, ensure_ascii=False))
    elif command == "recommend":
        model = monitor.recommend_model()
        if model:
            print(f"推荐模型: {model}")
        else:
            print("暂无足够数据推荐模型")
    else:
        print(f"未知命令: {command}")
        print("用法: python3 model_monitor.py [stats|recommend]")
        sys.exit(1)


if __name__ == "__main__":
    main()
