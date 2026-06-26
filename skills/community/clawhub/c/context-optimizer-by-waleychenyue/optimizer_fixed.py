#!/usr/bin/env python3
"""
Fixed context optimizer - ASCII only
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class ContextOptimizer:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.results = {
            "analysis_time": datetime.now().isoformat(),
            "files_analyzed": 0,
            "total_chars": 0,
            "total_tokens": 0,
            "results": {}
        }
    
    def analyze_file(self, filepath):
        """Analyze a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            char_count = len(content)
            line_count = content.count('\n') + 1
            
            # Simple duplicate detection
            lines = content.split('\n')
            unique_lines = set(lines)
            duplicate_rate = 100 * (1 - len(unique_lines) / max(1, len(lines)))
            
            # Token estimation (rough)
            estimated_tokens = char_count // 4
            
            # Optimization score (lower is better)
            optimization_score = min(100, int(duplicate_rate * 1.5))
            
            return {
                "filename": filepath.name,
                "analysis": {
                    "char_count": char_count,
                    "line_count": line_count,
                    "duplicate_rate": round(duplicate_rate, 1),
                    "estimated_tokens": estimated_tokens,
                    "optimization_score": optimization_score
                },
                "status": "success"
            }
        except Exception as e:
            return {
                "filename": filepath.name,
                "error": str(e),
                "status": "error"
            }
    
    def analyze_workspace(self):
        """Analyze all markdown files in workspace"""
        print(f"Analyzing workspace context...")
        print(f"Workspace path: {self.workspace_path}")
        
        # Find markdown files
        md_files = list(self.workspace_path.glob("*.md"))
        
        for filepath in md_files:
            result = self.analyze_file(filepath)
            self.results["results"][filepath.name] = result
            
            if result["status"] == "success":
                self.results["files_analyzed"] += 1
                self.results["total_chars"] += result["analysis"]["char_count"]
                self.results["total_tokens"] += result["analysis"]["estimated_tokens"]
        
        return self.results
    
    def generate_report(self):
        """Generate optimization report"""
        report = []
        report.append("=" * 60)
        report.append("CONTEXT OPTIMIZATION ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {self.results['analysis_time']}")
        report.append(f"Workspace: {self.workspace_path}")
        report.append("")
        
        # Summary
        report.append("## SUMMARY")
        report.append(f"- Files analyzed: {self.results['files_analyzed']}")
        report.append(f"- Total characters: {self.results['total_chars']:,}")
        report.append(f"- Estimated tokens: {self.results['total_tokens']:,}")
        report.append("")
        
        # File analysis
        report.append("## FILE ANALYSIS")
        for filename, result in self.results["results"].items():
            if result["status"] == "success":
                analysis = result["analysis"]
                report.append(f"- {filename}: {analysis['char_count']} chars, {analysis['estimated_tokens']} tokens, score: {analysis['optimization_score']}/100")
        
        report.append("")
        
        # Recommendations
        report.append("## RECOMMENDATIONS")
        
        # Check if optimization needed
        high_score_files = []
        for filename, result in self.results["results"].items():
            if result["status"] == "success" and result["analysis"]["optimization_score"] > 40:
                high_score_files.append((filename, result["analysis"]["optimization_score"]))
        
        if high_score_files:
            report.append("Files needing optimization:")
            for filename, score in high_score_files:
                report.append(f"  - {filename} (score: {score})")
            report.append("")
            report.append("Suggested actions:")
            report.append("1. Remove duplicate content")
            report.append("2. Extract reusable patterns to skills")
            report.append("3. Archive old context to memory files")
        else:
            report.append("Context is in good state, no urgent optimization needed")
        
        report.append("")
        
        # Next steps
        report.append("## NEXT STEPS")
        report.append("1. Review detailed analysis in JSON file")
        report.append("2. Run optimization on high-score files")
        report.append("3. Configure scheduled optimization")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_results(self):
        """Save analysis results"""
        # Save JSON data
        json_path = self.workspace_path / "context_analysis_data.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save report
        report_path = self.workspace_path / "context_analysis_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        return str(json_path), str(report_path)

def main():
    """Main function"""
    workspace_path = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
    
    optimizer = ContextOptimizer(workspace_path)
    results = optimizer.analyze_workspace()
    
    json_path, report_path = optimizer.save_results()
    
    print(optimizer.generate_report())
    print(f"\n[OK] Report saved: {report_path}")
    print(f"[OK] Data saved: {json_path}")

if __name__ == "__main__":
    main()