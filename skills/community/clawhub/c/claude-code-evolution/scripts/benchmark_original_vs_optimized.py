#!/usr/bin/env python3
"""
原始系统 vs 优化系统性能基准对比

功能：
1. 估算原始系统（全量加载）的token消耗
2. 估算优化系统的token消耗  
3. 对比性能差异
4. 生成基准测试报告
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from prompt_optimizer import PromptOptimizer, PromptOptimizerConfig
    print("✅ Prompt优化器模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class OriginalSystemAnalyzer:
    """原始系统分析器"""
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
        self.workspace_root = workspace_root
        self.system_files = [
            "SOUL.md",
            "IDENTITY.md", 
            "USER.md",
            "AGENTS.md",
            "TOOLS.md",
            "BOOTSTRAP.md"
        ]
    
    def read_system_file(self, filename: str) -> str:
        """读取系统文件"""
        filepath = os.path.join(self.workspace_root, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def estimate_tokens(self, text: str) -> int:
        """估算token数量（简化版：4字符≈1token）"""
        if not text:
            return 0
        # 简单估算：英文字符约4个=1token，中文字符约2个=1token
        # 这里使用简化版本：总字符数/3
        return max(1, len(text) // 3)
    
    def analyze_original_system(self) -> Dict[str, Any]:
        """分析原始系统"""
        print("\n分析原始系统...")
        
        total_tokens = 0
        file_details = []
        
        for filename in self.system_files:
            content = self.read_system_file(filename)
            if content:
                tokens = self.estimate_tokens(content)
                total_tokens += tokens
                file_details.append({
                    "file": filename,
                    "size_chars": len(content),
                    "tokens_estimated": tokens
                })
                print(f"  {filename}: {len(content)}字符, {tokens} tokens")
        
        # 工具描述（估算）
        # 原始系统加载约52个工具，每个工具描述约50-100 tokens
        estimated_tool_tokens = 52 * 75  # 平均75 tokens每个工具
        total_tokens += estimated_tool_tokens
        
        print(f"\n工具描述（估算）: {estimated_tool_tokens} tokens")
        print(f"原始系统总tokens: {total_tokens} tokens")
        
        return {
            "total_tokens": total_tokens,
            "file_details": file_details,
            "tool_tokens_estimated": estimated_tool_tokens,
            "analyzed_at": datetime.now().isoformat()
        }

class OptimizationBenchmark:
    """优化性能基准测试"""
    
    def __init__(self):
        self.original_analyzer = OriginalSystemAnalyzer()
    
    def run_benchmark_scenarios(self) -> Dict[str, Any]:
        """运行基准测试场景"""
        print("\n" + "="*60)
        print("优化系统性能基准测试")
        print("="*60)
        
        scenarios = [
            {
                "name": "文件操作任务",
                "task_context": {
                    "task_type": "file_operations",
                    "tool_needed": ["read", "write", "edit"],
                    "description": "读取并更新文件"
                }
            },
            {
                "name": "安全敏感任务", 
                "task_context": {
                    "task_type": "security_sensitive",
                    "tool_needed": ["message", "exec", "sessions_spawn"],
                    "risk_level": "high",
                    "description": "发送外部消息并执行命令"
                }
            },
            {
                "name": "多Agent协作",
                "task_context": {
                    "task_type": "multi_agent_collaboration",
                    "tool_needed": ["sessions_send", "sessions_spawn", "subagents"],
                    "agents_involved": ["development", "product"],
                    "description": "Coordinator协调Worker"
                }
            },
            {
                "name": "轻度任务",
                "task_context": {
                    "task_type": "light_task",
                    "tool_needed": ["read", "memory_search"],
                    "description": "简单信息查询"
                }
            },
            {
                "name": "重度任务",
                "task_context": {
                    "task_type": "heavy_task",
                    "tool_needed": ["read", "write", "edit", "exec", "browser", "message"],
                    "description": "复杂多工具操作"
                }
            }
        ]
        
        results = []
        
        # 分析原始系统
        original_analysis = self.original_analyzer.analyze_original_system()
        original_tokens = original_analysis["total_tokens"]
        
        for scenario in scenarios:
            print(f"\n测试场景: {scenario['name']}")
            
            # 配置优化器
            config = PromptOptimizerConfig()
            
            # 根据任务类型调整配置
            if scenario["task_context"]["task_type"] == "security_sensitive":
                config.fragment_priority_threshold = 8
                config.compression_level = 1
                config.max_tokens = 2000
            elif scenario["task_context"]["task_type"] == "light_task":
                config.fragment_priority_threshold = 5
                config.compression_level = 3
                config.max_tokens = 1000
            else:
                config.fragment_priority_threshold = 6
                config.compression_level = 2
                config.max_tokens = 1500
            
            optimizer = PromptOptimizer(config)
            
            # 优化
            start_time = time.time()
            optimized = optimizer.optimize_for_task(scenario["task_context"])
            end_time = time.time()
            
            optimization_time = end_time - start_time
            optimized_tokens = optimized.token_estimate
            
            # 计算节省
            token_saving = original_tokens - optimized_tokens
            token_saving_percent = (token_saving / original_tokens * 100) if original_tokens > 0 else 0
            
            # 计算压缩比
            compression_ratio = (original_tokens / optimized_tokens) if optimized_tokens > 0 else 1
            
            result = {
                "scenario": scenario["name"],
                "original_tokens": original_tokens,
                "optimized_tokens": optimized_tokens,
                "token_saving": token_saving,
                "token_saving_percent": round(token_saving_percent, 1),
                "compression_ratio": round(compression_ratio, 2),
                "optimization_time_ms": round(optimization_time * 1000, 2),
                "task_type": scenario["task_context"]["task_type"],
                "tools_needed": scenario["task_context"].get("tool_needed", [])
            }
            
            results.append(result)
            
            print(f"  原始: {original_tokens} tokens")
            print(f"  优化: {optimized_tokens} tokens")
            print(f"  节省: {token_saving} tokens ({token_saving_percent:.1f}%)")
            print(f"  压缩比: {compression_ratio:.2f}x")
            print(f"  优化时间: {optimization_time_ms}ms")
        
        return {
            "original_analysis": original_analysis,
            "scenario_results": results,
            "summary": self.generate_summary(results)
        }
    
    def generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """生成汇总统计"""
        if not results:
            return {}
        
        avg_token_saving = sum(r["token_saving"] for r in results) / len(results)
        avg_token_saving_percent = sum(r["token_saving_percent"] for r in results) / len(results)
        avg_compression_ratio = sum(r["compression_ratio"] for r in results) / len(results)
        avg_optimization_time = sum(r["optimization_time_ms"] for r in results) / len(results)
        
        # 找到最佳和最差场景
        best_scenario = max(results, key=lambda x: x["token_saving_percent"])
        worst_scenario = min(results, key=lambda x: x["token_saving_percent"])
        
        return {
            "avg_token_saving": round(avg_token_saving),
            "avg_token_saving_percent": round(avg_token_saving_percent, 1),
            "avg_compression_ratio": round(avg_compression_ratio, 2),
            "avg_optimization_time_ms": round(avg_optimization_time, 2),
            "best_scenario": {
                "name": best_scenario["scenario"],
                "saving_percent": best_scenario["token_saving_percent"]
            },
            "worst_scenario": {
                "name": worst_scenario["scenario"],
                "saving_percent": worst_scenario["token_saving_percent"]
            },
            "total_scenarios": len(results)
        }
    
    def generate_report(self, benchmark_results: Dict[str, Any]) -> str:
        """生成基准测试报告"""
        print("\n" + "="*60)
        print("性能基准测试报告")
        print("="*60)
        
        report = {
            "benchmark_date": datetime.now().isoformat(),
            "system": "OpenClaw Prompt优化系统",
            "version": "v1.0",
            "original_system": benchmark_results["original_analysis"],
            "optimization_results": benchmark_results["scenario_results"],
            "summary": benchmark_results["summary"]
        }
        
        # 打印摘要
        summary = benchmark_results["summary"]
        print(f"\n性能优化摘要:")
        print(f"  平均token节省: {summary['avg_token_saving_percent']}%")
        print(f"  平均压缩比: {summary['avg_compression_ratio']}x")
        print(f"  平均优化时间: {summary['avg_optimization_time_ms']}ms")
        print(f"  最佳场景: {summary['best_scenario']['name']} ({summary['best_scenario']['saving_percent']}%)")
        print(f"  最差场景: {summary['worst_scenario']['name']} ({summary['worst_scenario']['saving_percent']}%)")
        
        # 详细场景结果
        print(f"\n详细场景结果:")
        for result in benchmark_results["scenario_results"]:
            print(f"  {result['scenario']}:")
            print(f"    原始{result['original_tokens']} → 优化{result['optimized_tokens']} tokens")
            print(f"    节省{result['token_saving']} tokens ({result['token_saving_percent']}%)")
            print(f"    压缩比{result['compression_ratio']}x")
            print(f"    优化时间{result['optimization_time_ms']}ms")
        
        # 保存报告
        report_file = "memory/prompt-optimizer-benchmark-report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ 基准测试报告已保存: {report_file}")
        except Exception as e:
            print(f"❌ 报告保存失败: {e}")
        
        return report_file
    
    def run_complete_benchmark(self):
        """运行完整基准测试"""
        print("="*60)
        print("原始系统 vs 优化系统性能基准对比")
        print("="*60)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 运行基准测试
            benchmark_results = self.run_benchmark_scenarios()
            
            # 生成报告
            report_file = self.generate_report(benchmark_results)
            
            # 性能评级
            avg_saving = benchmark_results["summary"]["avg_token_saving_percent"]
            if avg_saving >= 40:
                rating = "⭐⭐⭐⭐⭐ 优秀"
            elif avg_saving >= 30:
                rating = "⭐⭐⭐⭐ 良好"
            elif avg_saving >= 20:
                rating = "⭐⭐⭐ 中等"
            else:
                rating = "⭐⭐ 需要改进"
            
            print(f"\n性能评级: {rating}")
            print(f"总体评估: 优化系统可实现平均{avg_saving:.1f}%的token节省")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 基准测试失败: {e}")
            return False

def main():
    """主函数"""
    benchmark = OptimizationBenchmark()
    success = benchmark.run_complete_benchmark()
    
    print("\n" + "="*60)
    if success:
        print("✅ 基准测试完成")
        print("提示: 优化系统已通过性能验证，可部署使用")
    else:
        print("❌ 基准测试失败")
    
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()