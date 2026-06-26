#!/usr/bin/env python3
"""
简化版上下文优化器 - 用于测试
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
        word_count = len(content.split())
        
        # 检查重复内容
        lines = content.split('\n')
        unique_lines = set(lines)
        duplicate_rate = 1 - len(unique_lines) / max(len(lines), 1)
        
        # 评估优化潜力
        optimization_potential = {
            "char_count": char_count,
            "line_count": line_count,
            "word_count": word_count,
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
    
    # 生成报告
    report = generate_report(results, total_chars, total_tokens)
    
    return {
        "analysis_time": datetime.now().isoformat(),
        "files_analyzed": len(results),
        "total_chars": total_chars,
        "total_tokens": total_tokens,
        "results": results,
        "report": report
    }

def generate_report(results, total_chars, total_tokens):
    """生成报告"""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("📊 上下文优化分析报告 (简化版)")
    report_lines.append("=" * 60)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"工作空间: {os.path.expanduser('~/.openclaw/workspace')}")
    report_lines.append("")
    
    report_lines.append("## 总体统计")
    report_lines.append(f"- 分析文件数: {len(results)}")
    report_lines.append(f"- 总字符数: {total_chars:,}")
    report_lines.append(f"- 估算Token数: {total_tokens:,}")
    report_lines.append("")
    
    report_lines.append("## 文件分析详情")
    
    for filename, result in results.items():
        if result.get("status") == "success":
            analysis = result.get("analysis", {})
            score = analysis.get("optimization_score", 0)
            
            report_lines.append(f"### {filename}")
            report_lines.append(f"  - 字符数: {analysis.get('char_count', 0):,}")
            report_lines.append(f"  - 行数: {analysis.get('line_count', 0)}")
            report_lines.append(f"  - 重复率: {analysis.get('duplicate_rate', 0)}%")
            report_lines.append(f"  - 优化分数: {score}/100")
            
            if score >= 60:
                report_lines.append(f"  - 建议: 🔥 优先优化 (潜力大)")
            elif score >= 30:
                report_lines.append(f"  - 建议: ⚡ 考虑优化")
            else:
                report_lines.append(f"  - 建议: ✅ 状态良好")
    
    report_lines.append("")
    report_lines.append("## 优化建议")
    
    high_score_files = []
    for filename, result in results.items():
        if result.get("status") == "success":
            score = result.get("analysis", {}).get("optimization_score", 0)
            if score >= 60:
                high_score_files.append((filename, score))
    
    if high_score_files:
        report_lines.append("建议优先优化以下文件:")
        for filename, score in sorted(high_score_files, key=lambda x: x[1], reverse=True):
            report_lines.append(f"- {filename} (优化分数: {score})")
    else:
        report_lines.append("当前上下文状态良好，无需紧急优化")
    
    report_lines.append("")
    report_lines.append("## 后续步骤")
    report_lines.append("1. 查看详细优化报告")
    report_lines.append("2. 执行优化: python context_optimizer.py optimize")
    report_lines.append("3. 配置定期优化任务")
    
    report_lines.append("=" * 60)
    
    return "\n".join(report_lines)

def main():
    """主函数"""
    workspace_path = os.path.expanduser("~/.openclaw/workspace")
    
    print("正在分析工作空间上下文...")
    print(f"工作空间路径: {workspace_path}")
    print()
    
    results = analyze_workspace(workspace_path)
    
    # 打印报告
    print(results["report"])
    
    # 保存报告
    report_file = os.path.join(workspace_path, "context_analysis_report.md")
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(results["report"])
        print(f"\n✅ 报告已保存: {report_file}")
    except Exception as e:
        print(f"\n⚠️  报告保存失败: {e}")
    
    # 保存JSON数据
    json_file = os.path.join(workspace_path, "context_analysis_data.json")
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ 数据已保存: {json_file}")
    except Exception as e:
        print(f"⚠️  数据保存失败: {e}")

if __name__ == "__main__":
    main()