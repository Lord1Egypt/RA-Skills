"""
Dual Retrieval Pipeline - Phase 4
M-Flow（图拓扑检索）+ QMD（BM25+向量检索）双重检索
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# 设置 M-Flow 环境变量（从 .env 加载）
def _setup_mflow_env():
    mflow_dir = Path(__file__).parent.parent.parent / "m_flow"
    env_path = mflow_dir / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            pass  # dotenv not available

_setup_mflow_env()

# 动态加载 M-Flow Memory
def _load_mflow_module():
    skill_path = Path(__file__).parent.parent.parent
    mflow_skill_path = skill_path / "m-flow-memory"
    scripts_path = mflow_skill_path / "scripts"
    spec = importlib.util.spec_from_file_location("mflow_scripts", scripts_path / "__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_mflow_module = _load_mflow_module()
MFlowMemory = _mflow_module.MFlowMemory

# 导入 QMD Searcher
from .qmd_search import QMDSearcher


@dataclass
class RetrievalResult:
    """检索结果"""
    source: str  # "mflow" or "qmd"
    content: str
    score: float
    metadata: Dict[str, Any]


@dataclass
class DualRetrievalResult:
    """双重检索结果"""
    query: str
    mflow_results: List[RetrievalResult]
    qmd_results: List[RetrievalResult]
    merged_results: List[RetrievalResult]
    stats: Dict[str, Any]
    
    def to_markdown(self) -> str:
        lines = [
            f"# Dual Retrieval Results",
            "",
            f"**Query**: {self.query}",
            f"**M-Flow Results**: {len(self.mflow_results)}",
            f"**QMD Results**: {len(self.qmd_results)}",
            f"**Merged Results**: {len(self.merged_results)}",
            "",
            f"**Stats**:",
            f"- M-Flow avg score: {self.stats.get('mflow_avg_score', 0):.3f}",
            f"- QMD avg score: {self.stats.get('qmd_avg_score', 0):.3f}",
            f"- Merge strategy: {self.stats.get('merge_strategy', 'N/A')}",
            "",
        ]
        
        if self.merged_results:
            lines.append("## Merged Results (Top 10)")
            for i, r in enumerate(self.merged_results[:10], 1):
                content_preview = r.content[:200] + "..." if len(r.content) > 200 else r.content
                lines.append(f"\n### {i}. [{r.source.upper()}] Score: {r.score:.3f}")
                lines.append(f"{content_preview}")
                if r.metadata:
                    lines.append(f"```json\n{r.metadata}\n```")
        
        return "\n".join(lines)


class DualRetrievalPipeline:
    """
    双重检索 Pipeline
    
    流程:
    1. 并行执行 M-Flow 和 QMD 检索
    2. 合并结果
    3. 去重
    4. 排序返回
    """
    
    def __init__(
        self,
        mflow_memory: MFlowMemory = None,
        qmd_collections: List[str] = None,
        merge_strategy: str = "score_weighted"  # "score_weighted" | "interleave" | "mflow_first"
    ):
        """
        Args:
            mflow_memory: MFlowMemory 实例
            qmd_collections: QMD collection 列表
            merge_strategy: 合并策略
                - score_weighted: 按分数加权
                - interleave: 交替插入
                - mflow_first: M-Flow 结果优先
        """
        self.mflow_memory = mflow_memory
        self.qmd_searcher = QMDSearcher()
        self.qmd_collections = qmd_collections
        self.merge_strategy = merge_strategy
    
    async def search(
        self,
        query: str,
        mflow_top_k: int = 5,
        qmd_top_k: int = 5,
        final_top_k: int = 10
    ) -> DualRetrievalResult:
        """
        执行双重检索
        
        Args:
            query: 查询文本
            mflow_top_k: M-Flow 返回结果数
            qmd_top_k: QMD 返回结果数
            final_top_k: 最终返回结果数
            
        Returns:
            DualRetrievalResult
        """
        # 并行执行两个检索
        import asyncio
        
        mflow_task = asyncio.create_task(
            self._search_mflow(query, mflow_top_k)
        )
        qmd_task = asyncio.create_task(
            self._search_qmd(query, qmd_top_k)
        )
        
        mflow_results, qmd_results = await asyncio.gather(mflow_task, qmd_task)
        
        # 合并结果
        merged = self._merge_results(mflow_results, qmd_results, final_top_k)
        
        # 统计
        stats = {
            "mflow_count": len(mflow_results),
            "qmd_count": len(qmd_results),
            "merged_count": len(merged),
            "merge_strategy": self.merge_strategy,
            "mflow_avg_score": sum(r.score for r in mflow_results) / len(mflow_results) if mflow_results else 0,
            "qmd_avg_score": sum(r.score for r in qmd_results) / len(qmd_results) if qmd_results else 0,
        }
        
        return DualRetrievalResult(
            query=query,
            mflow_results=mflow_results,
            qmd_results=qmd_results,
            merged_results=merged,
            stats=stats
        )
    
    async def _search_mflow(self, query: str, top_k: int) -> List[RetrievalResult]:
        """M-Flow 检索"""
        results = []
        try:
            # 动态导入 m_flow 并使用正确的 API
            mflow_dir = Path(__file__).parent.parent.parent / "m_flow"
            sys.path.insert(0, str(mflow_dir))
            import m_flow
            
            # 使用正确的 API: query_type= 而不是 mode=
            raw_results = await m_flow.search(
                query,
                query_type=m_flow.RecallMode.EPISODIC,
                top_k=top_k
            )
            
            # 解析 M-Flow 结果格式
            # raw_results = [{'search_result': ['content string', ...], 'dataset_id': ..., ...}, ...]
            for result_group in raw_results:
                search_result_list = result_group.get("search_result", [])
                for content in search_result_list:
                    if content:
                        results.append(RetrievalResult(
                            source="mflow",
                            content=content,
                            score=1.0,  # M-Flow 不提供个别结果的分数
                            metadata={"dataset_name": result_group.get("dataset_name", "")}
                        ))
        except Exception as e:
            print(f"[ERROR] M-Flow search failed: {e}")
            import traceback
            traceback.print_exc()
        
        return results
    
    async def _search_qmd(self, query: str, top_k: int) -> List[RetrievalResult]:
        """QMD 检索"""
        results = []
        try:
            # 直接使用 QMDSearcher（同步调用）
            qmd_results = self.qmd_searcher.search(
                query=query,
                top_k=top_k,
                collection=None  # 搜索所有集合
            )
            
            for r in qmd_results:
                results.append(RetrievalResult(
                    source="qmd",
                    content=r.get("content", ""),
                    score=0.8,  # QMD 默认分数
                    metadata={
                        "filepath": r.get("filepath", ""),
                        "title": r.get("title", ""),
                        "collection": r.get("collection", "")
                    }
                ))
        except Exception as e:
            print(f"[ERROR] QMD search failed: {e}")
            import traceback
            traceback.print_exc()
        
        return results
    
    def _merge_results(
        self,
        mflow_results: List[RetrievalResult],
        qmd_results: List[RetrievalResult],
        top_k: int
    ) -> List[RetrievalResult]:
        """合并两个检索结果"""
        
        if self.merge_strategy == "mflow_first":
            # M-Flow 结果优先，交替插入 QMD 结果
            merged = []
            mflow_idx, qmd_idx = 0, 0
            
            while len(merged) < top_k and (mflow_idx < len(mflow_results) or qmd_idx < len(qmd_results)):
                if mflow_idx < len(mflow_results):
                    merged.append(mflow_results[mflow_idx])
                    mflow_idx += 1
                if len(merged) >= top_k:
                    break
                if qmd_idx < len(qmd_results):
                    merged.append(qmd_results[qmd_idx])
                    qmd_idx += 1
            
            return merged
        
        elif self.merge_strategy == "interleave":
            # 交替插入
            merged = []
            mflow_idx, qmd_idx = 0, 0
            
            while len(merged) < top_k and (mflow_idx < len(mflow_results) or qmd_idx < len(qmd_results)):
                if mflow_idx < len(mflow_results):
                    merged.append(mflow_results[mflow_idx])
                    mflow_idx += 1
                if len(merged) >= top_k:
                    break
                if qmd_idx < len(qmd_results):
                    merged.append(qmd_results[qmd_idx])
                    qmd_idx += 1
            
            return merged
        
        else:  # score_weighted
            # 按分数加权排序
            all_results = []
            
            # M-Flow 分数（稍高权重）
            for r in mflow_results:
                all_results.append((r.score * 1.2, r))  # M-Flow 1.2x 权重
            
            # QMD 分数
            max_qmd_score = max((r.score for r in qmd_results), default=1.0)
            for r in qmd_results:
                normalized_score = r.score / max_qmd_score if max_qmd_score > 0 else 0
                all_results.append((normalized_score, r))
            
            # 按分数排序
            all_results.sort(key=lambda x: x[0], reverse=True)
            
            return [r for _, r in all_results[:top_k]]


async def main():
    """测试双重检索"""
    print("=== Phase 4: Dual Retrieval Test ===")
    
    pipeline = DualRetrievalPipeline(
        merge_strategy="score_weighted"
    )
    
    # 测试 QMD 统计
    qmd_stats = pipeline.qmd_searcher.get_stats()
    print(f"[INFO] QMD Stats: {qmd_stats}")
    
    # 测试查询
    query = "openclaw agent memory"
    print(f"\n[QUERY] {query}")
    
    result = await pipeline.search(query, mflow_top_k=3, qmd_top_k=5, final_top_k=10)
    
    print(f"\n[M-Flow Results] {len(result.mflow_results)}")
    for r in result.mflow_results:
        print(f"  Score: {r.score:.3f} | {r.content[:80]}...")
    
    print(f"\n[QMD Results] {len(result.qmd_results)}")
    for r in result.qmd_results:
        print(f"  Score: {r.score:.3f} | {r.content[:80]}...")
    
    print(f"\n[Merged Results (Top 10)]")
    for i, r in enumerate(result.merged_results[:10], 1):
        print(f"  {i}. [{r.source}] Score: {r.score:.3f} | {r.content[:60]}...")
    
    print(f"\n[Stats]")
    for k, v in result.stats.items():
        print(f"  {k}: {v}")
    
    # 保存报告
    report_path = Path(__file__).parent.parent.parent / "knowledge" / "dual-retrieval-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(result.to_markdown(), encoding="utf-8")
    print(f"\n[INFO] Report saved to {report_path}")
    
    print("\n=== Phase 4 Test Complete ===")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
