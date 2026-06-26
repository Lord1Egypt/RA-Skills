#!/usr/bin/env python3
"""
ASCII版上下文优化器 - 兼容Windows GBK编码
"""

import os
import json
from datetime import datetime

def analyze_file(filepath):
    """分析文件"""
    if not os.path.exists(filepath):
        return {"error": f"文件不存在: {filepath}"}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        
        # 简单分析
        char_count = len(content)
        line_count = content.count('\n') + 1
        
        # 检查重复内容
        lines = content.split('\n')
        unique_lines = set(lines)
        duplicate_rate = 1 - len(unique_lines) / max(len(lines), 1)
        
        # 评估优化潜力
        optimization_potential = {
            "char_count": char_count,
            "line_count": line_count,
            "duplicate_rate": round(duplicate_rate * 100, 1),
            "estimated_tokens": char_count // 4,
            "optimization_score": min(int(duplicate_rate * 100 + (char_count > 1000) * 20), 100)
        }
        
        return {
            "filename": filename,
            "analysis": optimization_potential,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e), "status": "failed"}

def analyze_workspace(workspace_path):
    """分析工作空间"""
    files_to_analyze = [
        "AGENTS.md",
        "SOUL.md",
        "MEMORY.md",
        "HEARTBEAT.md",
        "TOOLS.md",
        "IDENTITY.md",
        "USER.md"
    ]
    
    results = {}
    total_chars = 0
    total_tokens = 0
    
    for filename in files_to_analyze:
        filepath = os.path.join(workspace_path, filename)
        if os.path.exists(filepath):
            result = analyze_file(filepath)
            results[filename] = result
            
            if result.get("status") == "success":
                analysis = result.get("analysis", {})
                total_chars += analysis.get("char_count", 0)
                total_tokens += analysis.get("estimated_tokens", 0)
    
    return {
        "analysis_time": datetime.now().isoformat(),
        "files_analyzed": len(results),
        "total_chars": total_chars,
        "total_tokens": total_tokens,
        "results": results
    }

def generate_ascii_report(results, total_chars, total_tokens):
    """生成ASCII报告"""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("CONTEXT OPTIMIZATION ANALYSIS REPORT")
    report_lines.append("=" * 60)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Workspace: {os.path.expanduser('~/.openclaw/workspace')}")
    report_lines.append("")
    
    report_lines.append("## SUMMARY")
    report_lines.append(f"- Files analyzed: {len(results)}")
    report_lines.append(f"- Total characters: {total_chars:,}")
    report_lines.append(f"- Estimated tokens: {total_tokens:,}")
    report_lines.append("")
    
    report_lines.append("## FILE ANALYSIS")
    
    for filename, result in results.items():
        if isinstance(result, dict) and result.get("status") == "success":
            analysis = result.get("analysis", {})
            score = analysis.get("optimization_score", 0)
            
            report_lines.append(f"### {filename}")
            report_lines.append(f"  - Characters: {analysis.get('char_count', 0):,}")
            report_lines.append(f"  - Lines: {analysis.get('line_count', 0)}")
            report_lines.append(f"  - Duplication: {analysis.get('duplicate_rate', 0)}%")
            report_lines.append(f"  - Optimization score: {score}/100")
            
            if score >= 60:
                report_lines.append(f"  - Recommendation: HIGH priority (high potential)")
            elif score >= 30:
                report_lines.append(f"  - Recommendation: MEDIUM priority")
            else:
                report_lines.append(f"  - Recommendation: LOW priority (good state)")
    
    report_lines.append("")
    report_lines.append("## RECOMMENDATIONS")
    
    high_score_files = []
    for filename, result in results.items():
        if isinstance(result, dict) and result.get("status") == "success":
            score = result.get("analysis", {}).get("optimization_score", 0)
            if score >= 60:
                high_score_files.append((filename, score))
    
    if high_score_files:
        report_lines.append("Prioritize optimization for:")
        for filename, score in sorted(high_score_files, key=lambda x: x[1], reverse=True):
            report_lines.append(f"- {filename} (score: {score})")
    else:
        report_lines.append("Context is in good state, no urgent optimization needed")
    
    report_lines.append("")
    report_lines.append("## NEXT STEPS")
    report_lines.append("1. Review detailed analysis")
    report_lines.append("2. Run optimization: Use context optimizer skill")
    report_lines.append("3. Configure scheduled optimization")
    
    report_lines.append("=" * 60)
    
    return "\n".join(report_lines)

def main():
    """主函数"""
    workspace_path = os.path.expanduser("~/.openclaw/workspace")
    
    print("Analyzing workspace context...")
    print(f"Workspace path: {workspace_path}")
    print()
    
    results = analyze_workspace(workspace_path)
    
    # 生成并打印报告
    report = generate_ascii_report(results, results["total_chars"], results["total_tokens"])
    print(report)
    
    # 保存报告
    report_file = os.path.join(workspace_path, "context_analysis_report.txt")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n[OK] Report saved: {report_file}")
    except Exception as e:
        print(f"\n[WARN] Report save failed: {e}")
    
    # 保存JSON数据
    json_file = os.path.join(workspace_path, "context_analysis_data.json")
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"[OK] Data saved: {json_file}")
    except Exception as e:
        print(f"[WARN] Data save failed: {e}")

if __name__ == "__main__":
    main()