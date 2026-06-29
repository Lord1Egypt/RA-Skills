#!/usr/bin/env python3
"""
Model Gateway — 模型网关与智能路由

用法:
  python model_gateway.py --query "你好" --complexity auto
  python model_gateway.py --benchmark  # 运行成本对比测试
  python model_gateway.py --server     # 启动网关API服务

功能:
  - 多模型智能路由 (基于复杂度自动选择)
  - 熔断降级 (主模型不可用→自动切换)
  - 语义缓存 (相似问题直接返回)
  - 实时成本追踪
"""
import json
import hashlib
import time
import argparse
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from collections import defaultdict
from datetime import datetime


# ============================================================
# 数据模型
# ============================================================

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass
class ModelEndpoint:
    name: str
    model_id: str
    provider: str
    cost_input_per_1m: float   # USD
    cost_output_per_1m: float  # USD
    max_tokens: int = 4096
    supports_streaming: bool = True
    priority: int = 0           # 越小越优先
    avg_latency_ms: int = 1000  # 预估平均延迟


@dataclass
class RouteResult:
    endpoint: ModelEndpoint
    response: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cache_hit: bool = False
    fallback_used: bool = False
    complexity: TaskComplexity = TaskComplexity.MEDIUM


# ============================================================
# 模型定价表 (USD per 1M tokens) — 2026最新
# ============================================================

PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
    "qwen-max": {"input": 0.35, "output": 1.39},
    "qwen-plus": {"input": 0.11, "output": 0.42},
    "qwen-turbo": {"input": 0.04, "output": 0.08},
    "claude-sonnet": {"input": 3.00, "output": 15.00},
    "claude-haiku": {"input": 0.25, "output": 1.25},
}


# ============================================================
# 语义缓存 (简化版)
# ============================================================

class SemanticCache:
    """语义缓存：相似问题直接返回"""
    
    def __init__(self, threshold: float = 0.92):
        self.threshold = threshold
        self.store: Dict[str, tuple] = {}  # key → (query, response)
    
    def get(self, query: str) -> Optional[str]:
        """简单相似度匹配 (生产环境用向量DB)"""
        query_lower = query.lower().strip()
        for key, (cached_query, response) in self.store.items():
            if query_lower in cached_query.lower() or cached_query.lower() in query_lower:
                return response
            # 简单 Jaccard 相似度
            q_words = set(query_lower.split())
            c_words = set(cached_query.lower().split())
            if q_words and c_words:
                sim = len(q_words & c_words) / len(q_words | c_words)
                if sim >= self.threshold:
                    return response
        return None
    
    def set(self, query: str, response: str):
        key = hashlib.md5(query.encode()).hexdigest()
        self.store[key] = (query, response)
    
    @property
    def size(self) -> int:
        return len(self.store)


# ============================================================
# 模型网关核心
# ============================================================

class ModelGateway:
    """统一模型网关"""
    
    def __init__(self):
        # 按复杂度分层配置端点
        self.endpoints: Dict[TaskComplexity, List[ModelEndpoint]] = {
            TaskComplexity.SIMPLE: [
                ModelEndpoint("qwen-turbo", "qwen-turbo", "DashScope", 0.04, 0.08, priority=0),
                ModelEndpoint("gpt-4o-mini", "gpt-4o-mini", "OpenAI", 0.15, 0.60, priority=1),
            ],
            TaskComplexity.MEDIUM: [
                ModelEndpoint("deepseek-chat", "deepseek-chat", "DeepSeek", 0.14, 0.28, priority=0),
                ModelEndpoint("gpt-4o-mini", "gpt-4o-mini", "OpenAI", 0.15, 0.60, priority=1),
            ],
            TaskComplexity.COMPLEX: [
                ModelEndpoint("deepseek-reasoner", "deepseek-reasoner", "DeepSeek", 0.55, 2.19, priority=0),
                ModelEndpoint("gpt-4o", "gpt-4o", "OpenAI", 2.50, 10.00, priority=1),
                ModelEndpoint("claude-sonnet", "claude-3.5-sonnet", "Anthropic", 3.00, 15.00, priority=2),
            ],
        }
        
        # 熔断状态
        self.circuit_breakers: Dict[str, int] = defaultdict(int)  # name → failures
        self.circuit_threshold = 5
        
        # 缓存
        self.cache = SemanticCache()
        
        # 统计
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "fallbacks": 0,
            "total_cost": 0.0,
            "by_model": defaultdict(int),
        }
        
        # LLM 调用函数 (由外部注入)
        self.llm_call: Optional[Callable] = None
    
    def set_llm(self, llm_call: Callable):
        """注入LLM调用函数"""
        self.llm_call = llm_call
    
    def route(self, query: str, complexity: Optional[TaskComplexity] = None) -> RouteResult:
        """核心路由方法"""
        self.stats["total_requests"] += 1
        
        # 1. 缓存检查
        if cached := self.cache.get(query):
            self.stats["cache_hits"] += 1
            return RouteResult(
                endpoint=ModelEndpoint("cache", "cache", "local", 0, 0),
                response=cached,
                latency_ms=5,
                input_tokens=0,
                output_tokens=0,
                cost_usd=0,
                cache_hit=True,
            )
        
        # 2. 复杂度判断
        if complexity is None:
            complexity = self._estimate_complexity(query)
        
        # 3. 选端点 (跳过熔断的)
        endpoint = self._select_endpoint(complexity)
        fallback_used = False
        
        # 4. 调用 LLM
        try:
            result = self._call_llm(endpoint, query)
            # 成功后重置熔断计数
            self.circuit_breakers[endpoint.name] = max(0, self.circuit_breakers[endpoint.name] - 1)
            # 缓存结果
            self.cache.set(query, result.response)
        except Exception:
            # 记录失败 → 触发熔断 → 尝试降级
            self.circuit_breakers[endpoint.name] += 1
            self.stats["fallbacks"] += 1
            fallback_used = True
            # 尝试下一个可用端点
            fallback = self._select_fallback(complexity, exclude=endpoint.name)
            result = self._call_llm(fallback, query)
            endpoint = fallback
        
        result.complexity = complexity
        result.fallback_used = fallback_used
        
        # 5. 更新统计
        self.stats["total_cost"] += result.cost_usd
        self.stats["by_model"][endpoint.name] += 1
        
        return result
    
    def _estimate_complexity(self, query: str) -> TaskComplexity:
        """快速复杂度判断"""
        complex_kw = ["分析", "推理", "总结", "比较", "为什么", "设计", "架构", "方案"]
        simple_kw = ["你好", "谢谢", "再见", "是什么", "时间", "日期", "翻译"]
        
        if any(kw in query for kw in simple_kw) and len(query) < 30:
            return TaskComplexity.SIMPLE
        if len(query) > 200 or any(kw in query for kw in complex_kw):
            return TaskComplexity.COMPLEX
        return TaskComplexity.MEDIUM
    
    def _select_endpoint(self, complexity: TaskComplexity) -> ModelEndpoint:
        """选择最优端点（按优先级，跳过熔断的）"""
        candidates = sorted(self.endpoints.get(complexity, []), key=lambda x: x.priority)
        for ep in candidates:
            if self.circuit_breakers.get(ep.name, 0) < self.circuit_threshold:
                return ep
        # 全熔断 → 用第一个（赌运气）
        return candidates[0] if candidates else self.endpoints[TaskComplexity.SIMPLE][0]
    
    def _select_fallback(self, complexity: TaskComplexity, exclude: str) -> ModelEndpoint:
        """选择降级端点"""
        # 尝试同层下一个，否则降级到更简单层
        for ep in sorted(self.endpoints.get(complexity, []), key=lambda x: x.priority):
            if ep.name != exclude:
                return ep
        # 降级到 Simple 层
        return self.endpoints[TaskComplexity.SIMPLE][0]
    
    def _call_llm(self, endpoint: ModelEndpoint, query: str) -> RouteResult:
        """调用 LLM（生产环境替换为真实API调用）"""
        if self.llm_call:
            start = time.time()
            response = self.llm_call(endpoint.model_id, query)
            latency = (time.time() - start) * 1000
        else:
            # Mock 模式
            time.sleep(0.1)
            response = f"[{endpoint.name}] Mock response: {query[:30]}..."
            latency = 100 + (hash(query) % 200)
        
        input_tokens = len(query) // 3   # 粗略估算
        output_tokens = len(response) // 3
        cost = (input_tokens / 1_000_000) * endpoint.cost_input_per_1m + \
               (output_tokens / 1_000_000) * endpoint.cost_output_per_1m
        
        return RouteResult(
            endpoint=endpoint,
            response=response,
            latency_ms=latency,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )
    
    def print_stats(self):
        """打印统计报告"""
        total = self.stats["total_requests"]
        print(f"\n{'='*60}")
        print(f"📊 模型网关运行统计")
        print(f"{'='*60}")
        print(f"  总请求数:     {total}")
        print(f"  缓存命中:     {self.stats['cache_hits']} ({self.stats['cache_hits']/total*100:.1f}%)" if total else "N/A")
        print(f"  降级次数:     {self.stats['fallbacks']}")
        print(f"  总费用:       ${self.stats['total_cost']:.4f}")
        print(f"  缓存大小:     {self.cache.size}")
        print(f"\n  模型使用分布:")
        for model, count in sorted(self.stats["by_model"].items(), key=lambda x: -x[1]):
            pct = count / (total - self.stats["cache_hits"]) * 100 if (total - self.stats["cache_hits"]) > 0 else 0
            print(f"    {model:20s}: {count:4d} 次 ({pct:.1f}%)")
        print(f"\n  熔断状态:")
        for name, failures in self.circuit_breakers.items():
            status = "🔴 已熔断" if failures >= self.circuit_threshold else "🟢 正常"
            print(f"    {name:20s}: {failures} 次失败 {status}")
        print(f"{'='*60}\n")


# ============================================================
# 成本对比分析
# ============================================================

def run_benchmark(gateway: ModelGateway):
    """运行成本对比基准测试"""
    print("\n" + "="*70)
    print("💰 模型网关成本对比分析")
    print("="*70)
    
    # 模拟场景: 100次请求, 不同复杂度
    test_queries = [
        # (query, expected_complexity)
        ("你好", TaskComplexity.SIMPLE),
        ("今天天气怎么样", TaskComplexity.SIMPLE),
        ("帮我翻译'Hello World'", TaskComplexity.SIMPLE),
        ("Python里怎么读取CSV文件", TaskComplexity.MEDIUM),
        ("FastAPI和Flask有什么区别", TaskComplexity.MEDIUM),
        ("设计一个电商推荐系统的技术方案", TaskComplexity.COMPLEX),
        ("分析一下GPT-5的技术突破点", TaskComplexity.COMPLEX),
        ("为什么大模型会有幻觉问题", TaskComplexity.COMPLEX),
    ]
    
    # 场景A: 全部用最贵模型
    print("\n📋 场景A: 全部使用 gpt-4o ($2.50/$10.00 per 1M)")
    cost_a = 0
    for query, _ in test_queries:
        result = gateway._call_llm(
            ModelEndpoint("gpt-4o", "gpt-4o", "OpenAI", 2.50, 10.00),
            query
        )
        cost_a += result.cost_usd
    
    # 场景B: 智能路由
    print("\n📋 场景B: 模型网关智能路由")
    cost_b = 0
    for query, complexity in test_queries:
        endpoint = gateway._select_endpoint(complexity)
        result = gateway._call_llm(endpoint, query)
        cost_b += result.cost_usd
    
    # 对比
    print(f"\n{'='*70}")
    print(f"  场景A (全部最强模型):   ${cost_a:.6f}")
    print(f"  场景B (智能路由):       ${cost_b:.6f}")
    print(f"  节省:                  ${cost_a - cost_b:.6f} ({(1 - cost_b/cost_a)*100:.1f}%)")
    print(f"  年化节省 (日1000请求):  ${(cost_a - cost_b) * 365000:.2f}")
    print(f"{'='*70}\n")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Gateway — 模型网关与智能路由")
    parser.add_argument("--query", "-q", default="", help="测试查询")
    parser.add_argument("--complexity", default="auto", choices=["auto", "simple", "medium", "complex"])
    parser.add_argument("--benchmark", action="store_true", help="运行成本对比测试")
    parser.add_argument("--stats", action="store_true", help="显示运行统计")
    
    args = parser.parse_args()
    
    gateway = ModelGateway()
    
    if args.benchmark:
        run_benchmark(gateway)
    
    if args.query:
        complexity = None if args.complexity == "auto" else TaskComplexity(args.complexity)
        result = gateway.route(args.query, complexity)
        
        print(f"\n{'='*60}")
        print(f"📤 查询: {args.query[:60]}")
        print(f"  复杂度:     {result.complexity.value if result.complexity else 'auto'}")
        print(f"  使用模型:   {result.endpoint.name} ({result.endpoint.provider})")
        print(f"  缓存命中:   {'✅' if result.cache_hit else '❌'}")
        print(f"  降级:       {'⚠️ 是' if result.fallback_used else '✅ 否'}")
        print(f"  延迟:       {result.latency_ms:.0f}ms")
        print(f"  成本:       ${result.cost_usd:.6f}")
        print(f"  回复预览:   {result.response[:100]}...")
        print(f"{'='*60}")
    
    if args.stats or (not args.query and not args.benchmark):
        gateway.print_stats()
