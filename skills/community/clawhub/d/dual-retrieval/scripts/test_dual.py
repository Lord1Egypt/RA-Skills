"""
Test Phase 4 Dual Retrieval Pipeline - with Real QMD Integration
"""
import asyncio
import sys
import importlib.util
from pathlib import Path

# 设置 UTF-8 输出
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 动态加载 dual-retrieval
scripts_path = Path(__file__).parent / "__init__.py"
spec = importlib.util.spec_from_file_location("dual_scripts", scripts_path)
module = importlib.util.module_from_spec(spec)
sys.modules["dual_scripts"] = module
spec.loader.exec_module(module)

DualRetrievalPipeline = module.DualRetrievalPipeline
RetrievalResult = module.RetrievalResult


async def test_dual_with_real_qmd():
    """使用真实 QMD 测试双重检索"""
    print("=== Phase 4: Dual Retrieval with Real QMD Test ===")
    
    pipeline = DualRetrievalPipeline(merge_strategy="score_weighted")
    
    # QMD 统计
    qmd_stats = pipeline.qmd_searcher.get_stats()
    print(f"[INFO] QMD Stats: {qmd_stats}")
    
    # 测试查询
    queries = [
        "openclaw agent memory",
        "python programming",
        "knowledge base system"
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"[QUERY] {query}")
        
        result = await pipeline.search(
            query, 
            mflow_top_k=3, 
            qmd_top_k=5, 
            final_top_k=10
        )
        
        print(f"\n[M-Flow] {len(result.mflow_results)} results")
        for r in result.mflow_results[:3]:
            content_preview = r.content[:60].replace('\n', ' ')
            print(f"  [{r.source}] {content_preview}...")
        
        print(f"\n[QMD] {len(result.qmd_results)} results")
        for r in result.qmd_results[:3]:
            content_preview = r.content[:60].replace('\n', ' ')
            print(f"  [{r.source}] {content_preview}...")
        
        print(f"\n[Merged Top 5]")
        for i, r in enumerate(result.merged_results[:5], 1):
            content_preview = r.content[:50].replace('\n', ' ')
            print(f"  {i}. [{r.source}] Score:{r.score:.2f} | {content_preview}...")
        
        all_results.append(result)
    
    # 保存报告
    report_lines = ["# Phase 4: Dual Retrieval Test Report\n"]
    report_lines.append("## QMD Statistics\n")
    report_lines.append(f"- Documents: {qmd_stats['document_count']}")
    report_lines.append(f"- Collections: {qmd_stats['collection_count']}\n")
    
    report_lines.append("\n## Test Results\n")
    for i, result in enumerate(all_results, 1):
        report_lines.append(f"\n### Query {i}: {result.query}")
        report_lines.append(f"- M-Flow results: {len(result.mflow_results)}")
        report_lines.append(f"- QMD results: {len(result.qmd_results)}")
        report_lines.append(f"- Merged results: {len(result.merged_results)}")
        report_lines.append(f"- M-Flow avg score: {result.stats['mflow_avg_score']:.3f}")
        report_lines.append(f"- QMD avg score: {result.stats['qmd_avg_score']:.3f}")
    
    report_path = Path(__file__).parent.parent.parent / "knowledge" / "dual-retrieval-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\n[INFO] Report saved to {report_path}")
    
    return all_results


async def main():
    print("=== Phase 4: Dual Retrieval Pipeline Test ===\n")
    
    await test_dual_with_real_qmd()
    
    print("\n\n=== Phase 4 Test Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
