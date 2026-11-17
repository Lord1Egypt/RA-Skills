#!/usr/bin/env python3
"""
pipeline_graph — 任务图编排器（通用，不绑定具体管线）

对标 Anthropic Managed Agent 架构：
  - Coordinator：管编排（走哪步、重试、降级）
  - Worker Node：管执行（每个节点做一件事，无状态）
  - 牛马模式：节点崩了只重跑该节点，不影响其他节点

用法：
  g = Graph()
  g.add_node("collect", collect_func, ...)
  g.add_node("transcribe", transcribe_func, depends=["collect"])
  g.add_node("enhance", enhance_func, depends=["transcribe"])
  g.add_node("save", save_func, depends=["enhance"])
  
  results = g.run(context={"url": "..."})
  # → 自动拓扑排序 → 逐层执行（同层并行）
  # → 返回 {"collect": {...}, "transcribe": {...}, ...}
"""

import time, traceback
from typing import Callable, Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class Node:
    """任务图中的一个节点"""
    id: str
    func: Callable                     # 执行函数
    depends: List[str] = field(default_factory=list)  # 依赖的节点ID
    kwargs: Dict = field(default_factory=dict)         # 传给 func 的固定参数
    
    # 运行时状态
    status: str = "pending"            # pending | running | success | error | skipped
    error: Optional[str] = None
    result: Any = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 1               # 失败自动重试次数
    
    # 牛马模式配置
    continue_on_error: bool = False    # 失败是否跳过继续（true=跳过）
    timeout: int = 300                 # 单次执行超时


@dataclass
class GraphResult:
    """整个图执行完的结果"""
    node_results: Dict[str, Node]      # node_id → Node（含运行时结果）
    total_nodes: int
    success_nodes: int
    error_nodes: int
    skipped_nodes: int
    duration_s: float
    graph_summary: str


class Graph:
    """任务图 — 对标视频的20个Agent并发+任务图编排"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
    
    def add_node(self, id: str, func: Callable,
                 depends: Optional[List[str]] = None,
                 kwargs: Optional[Dict] = None,
                 max_retries: int = 1,
                 continue_on_error: bool = False,
                 timeout: int = 300) -> 'Graph':
        """添加一个任务节点"""
        self.nodes[id] = Node(
            id=id,
            func=func,
            depends=depends or [],
            kwargs=kwargs or {},
            max_retries=max_retries,
            continue_on_error=continue_on_error,
            timeout=timeout,
        )
        return self  # 链式调用
    
    def get_graph_summary(self) -> str:
        """生成人类可读的图摘要"""
        lines = [f"任务图: {len(self.nodes)} 个节点"]
        layers = self._topological_sort()
        for i, layer in enumerate(layers):
            dep_info = []
            for node_id in layer:
                node = self.nodes[node_id]
                deps = node.depends
                dep_str = f"(等{','.join(deps)})" if deps else "(并行)"
                dep_info.append(f"{node_id}{dep_str}")
            lines.append(f"  第{i+1}层 ({'并行' if len(layer)>1 else '单任务'}): {', '.join(dep_info)}")
        return "\n".join(lines)
    
    def _topological_sort(self) -> List[List[str]]:
        """拓扑排序：按依赖分层"""
        in_degree = {nid: len(n.depends) for nid, n in self.nodes.items()}
        remaining = set(self.nodes.keys())
        layers = []
        
        while remaining:
            current = [nid for nid in remaining if in_degree.get(nid, 0) == 0]
            if not current:
                # 有环路或孤立节点——全并行
                current = list(remaining)
            layers.append(current)
            for nid in current:
                remaining.remove(nid)
                for other in remaining:
                    if nid in self.nodes[other].depends:
                        in_degree[other] -= 1
        return layers
    
    def _get_ready_nodes(self, finished: set) -> List[str]:
        """获取当前就绪（所有依赖已成功完成）的节点"""
        ready = []
        for nid, node in self.nodes.items():
            if nid in finished:
                continue
            if node.status == "running":
                continue
            # 检查依赖：要么依赖全部成功，要么全部跳过（error且continue_on_error）
            all_deps_ok = True
            for dep in node.depends:
                dep_node = self.nodes.get(dep)
                if dep_node is None:
                    continue
                if dep_node.status == "success":
                    continue
                if dep_node.status == "error" and dep_node.continue_on_error:
                    continue  # 依赖出错但配置了跳过
                all_deps_ok = False
                break
            if all_deps_ok:
                ready.append(nid)
        return ready
    
    def run(self, context: Dict = None) -> GraphResult:
        """
        执行整个任务图
        
        流程：
        1. 拓扑排序 → 分层
        2. 逐层执行（同层就绪的一起跑，对标20个Agent并发）
        3. 每个节点：执行 → 成功/失败 → 按策略重试/跳过
        4. 节点执行时 context 自动注入
        """
        start = time.time()
        context = context or {}
        finished = set()
        layers = self._topological_sort()
        
        print("\n" + self.get_graph_summary())
        
        for layer_idx, layer_ids in enumerate(layers):
            # 只执行未完成的节点
            pending = [nid for nid in layer_ids if nid not in finished]
            if not pending:
                continue
            
            print(f"\n[层{layer_idx+1}] {len(pending)} 个就绪节点: {', '.join(pending)}")
            
            for nid in pending:
                node = self.nodes[nid]
                self._run_node(node, context)
                if node.status == "success" and node.result is not None:
                    context[nid] = node.result  # 结果入池，后续节点可见
                finished.add(nid)
        
        # 统计
        duration = time.time() - start
        success = sum(1 for n in self.nodes.values() if n.status == "success")
        errors = sum(1 for n in self.nodes.values() if n.status == "error")
        skipped = sum(1 for n in self.nodes.values() if n.status == "skipped")
        
        # 生成摘要
        summary_parts = []
        for nid in sorted(self.nodes.keys()):
            n = self.nodes[nid]
            icon = {"success": "✅", "error": "❌", "skipped": "⏭️", "pending": "⏳"}.get(n.status, "❓")
            dur = f"{n.finished_at - n.started_at:.1f}s" if n.finished_at and n.started_at else "?"
            retry = f" (重试{n.retry_count}次)" if n.retry_count > 0 else ""
            summary_parts.append(f"  {icon} {nid} — {dur}{retry}")
        
        return GraphResult(
            node_results=self.nodes,
            total_nodes=len(self.nodes),
            success_nodes=success,
            error_nodes=errors,
            skipped_nodes=skipped,
            duration_s=duration,
            graph_summary="\n".join(summary_parts),
        )
    
    def _run_node(self, node: Node, live_context: Dict):
        """执行单个节点（含重试）"""
        node.status = "running"
        node.started_at = time.time()
        
        # 自动注入所有已完成节点的结果
        dep_results = {}
        for nid, other in self.nodes.items():
            if other.status == "success" and other.result is not None:
                dep_results[nid] = other.result
                if isinstance(other.result, dict):
                    dep_results.update(other.result)
        
        for attempt in range(node.max_retries + 1):
            if attempt > 0:
                node.retry_count += 1
                print(f"  ↺ 重试 {node.id} (第{attempt}次)...")
            
            try:
                # 拼装参数：初始上下文 + 已完成的节点结果 + 节点固定参数
                call_kwargs = {**live_context, **dep_results, **node.kwargs}
                result = node.func(**call_kwargs)
                
                node.result = result
                node.status = "success"
                node.finished_at = time.time()
                dur = node.finished_at - node.started_at
                print(f"  ✅ {node.id} — {dur:.1f}s")
                return
                
            except Exception as e:
                error_msg = f"{type(e).__name__}: {e}"
                print(f"  ❌ {node.id} 失败: {error_msg[:80]}")
                
                if attempt < node.max_retries:
                    print(f"  ↺ 等待重试 ({attempt+1}/{node.max_retries})...")
                    continue
                
                # 重试用尽
                node.error = error_msg
                node.finished_at = time.time()
                
                if node.continue_on_error:
                    node.status = "skipped"
                    print(f"  ⏭️ {node.id} 跳过（继续执行）")
                else:
                    node.status = "error"
                    print(f"  🛑 {node.id} 失败阻断管线")
    
    def get_node_result(self, node_id: str, default=None):
        """获取节点执行结果"""
        node = self.nodes.get(node_id)
        if node and node.status == "success":
            return node.result
        return default
    
    def get_node_error(self, node_id: str) -> Optional[str]:
        """获取节点错误信息"""
        node = self.nodes.get(node_id)
        return node.error if node else None


# ═══════════════════════════════════════════════════════════════
# 管道函数（将 dict 节点结果转为特定函数需要的参数）
# ═══════════════════════════════════════════════════════════════

def pipe(context: Dict, *keys: str) -> Tuple:
    """从 context 中提取指定 key 的值，用于前一个节点的结果传递"""
    return tuple(context.get(k) for k in keys)
