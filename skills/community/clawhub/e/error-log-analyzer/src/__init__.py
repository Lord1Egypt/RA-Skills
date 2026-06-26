"""
Error Log Analyzer - Main module
"""
from typing import List, Dict, Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers import LogParser, LogEntry
from src.analyzers import AIAnalyzer, ErrorAnalysis
from src.utils import (
    cluster_errors,
    detect_error_trends,
    filter_noise,
    assess_severity,
    generate_report
)


class LogAnalyzer:
    """Main analyzer class that combines parsing, analysis, and reporting."""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto"):
        self.parser = LogParser()
        self.ai_analyzer = AIAnalyzer(api_key=api_key, provider=provider)
    
    def analyze(self, log_content: str) -> Dict:
        """Analyze log content and return comprehensive results."""
        
        # Parse logs
        entries = self.parser.parse(log_content)
        
        # Filter noise
        entries = filter_noise(entries)
        
        # Cluster similar errors
        clusters = cluster_errors(entries)
        
        # Analyze each unique error
        analyses = []
        for cluster_key, cluster_entries in clusters.items():
            # Analyze first error in cluster
            first_error = cluster_entries[0]
            
            analysis = self.ai_analyzer.analyze(
                first_error.message,
                first_error.stack_trace
            )
            
            analyses.append({
                'error_type': analysis.error_type,
                'severity': analysis.severity,
                'explanation': analysis.explanation,
                'root_cause': analysis.root_cause,
                'suggestions': analysis.suggestions,
                'code_examples': analysis.code_examples or [],
                'occurrence_count': len(cluster_entries),
                'first_occurrence': first_error.timestamp,
                'sample_error': first_error.message,
                'sample_stack_trace': first_error.stack_trace
            })
        
        # Sort by severity and occurrence count
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        analyses.sort(key=lambda x: (severity_order.get(x['severity'], 99), -x['occurrence_count']))
        
        # Detect trends
        trends = detect_error_trends(entries)
        
        return {
            'total_errors': len(entries),
            'unique_errors': len(clusters),
            'analyses': analyses,
            'trends': trends,
            'summary': self._generate_summary(analyses, trends)
        }
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze log file."""
        with open(file_path, 'r') as f:
            content = f.read()
        return self.analyze(content)
    
    def _generate_summary(self, analyses: List[Dict], trends: Dict) -> str:
        """Generate executive summary."""
        if not analyses:
            return "No errors found in the log file."
        
        critical_count = sum(1 for a in analyses if a['severity'] == 'CRITICAL')
        high_count = sum(1 for a in analyses if a['severity'] == 'HIGH')
        
        summary_parts = []
        
        if critical_count > 0:
            summary_parts.append(f"🚨 {critical_count} CRITICAL error(s) requiring immediate attention")
        
        if high_count > 0:
            summary_parts.append(f"⚠️  {high_count} HIGH priority error(s)")
        
        if trends.get('spike_detected'):
            summary_parts.append(f"📈 Error spike detected in the last hour")
        
        summary_parts.append(f"📊 {len(analyses)} unique error types identified")
        
        return '\n'.join(summary_parts)


def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze error logs with AI')
    parser.add_argument('log_file', help='Path to log file or "-" for stdin')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], 
                       default='text', help='Output format')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--no-ai', action='store_true', 
                       help='Disable AI analysis (use pattern matching only)')
    parser.add_argument('--max-errors', type=int, default=100,
                       help='Maximum number of errors to analyze')
    
    args = parser.parse_args()
    
    # Read log content
    if args.log_file == '-':
        log_content = sys.stdin.read()
    else:
        with open(args.log_file, 'r') as f:
            log_content = f.read()
    
    # Analyze
    api_key = None if args.no_ai else None  # Will use env vars
    analyzer = LogAnalyzer(api_key=api_key)
    results = analyzer.analyze(log_content)
    
    # Limit results if needed
    if len(results['analyses']) > args.max_errors:
        results['analyses'] = results['analyses'][:args.max_errors]
        results['truncated'] = True
    
    # Generate output
    if args.format == 'json':
        output = generate_report(results, format='json')
    elif args.format == 'markdown':
        output = generate_report(results['analyses'], format='markdown')
    else:
        output = _format_text_output(results)
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


def _format_text_output(results: Dict) -> str:
    """Format results as human-readable text."""
    lines = []
    
    # Header
    lines.append("=" * 70)
    lines.append(" 🔓 ERROR LOG ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append("")
    
    # Summary
    lines.append("📊 SUMMARY")
    lines.append("-" * 70)
    lines.append(results['summary'])
    lines.append("")
    
    # Trends
    if results['trends']:
        lines.append("📈 TRENDS")
        lines.append("-" * 70)
        lines.append(f"Trend direction: {results['trends']['trend']}")
        if results['trends']['spike_detected']:
            lines.append("⚠️  SPIKE DETECTED in the last hour!")
        lines.append("")
    
    # Top errors
    lines.append("🔍 TOP ERRORS")
    lines.append("-" * 70)
    
    for i, analysis in enumerate(results['analyses'][:10], 1):
        severity_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }.get(analysis['severity'], '⚪')
        
        lines.append(f"\n{i}. {severity_emoji} {analysis['error_type'].upper()}")
        lines.append(f"   Severity: {analysis['severity']}")
        lines.append(f"   Occurrences: {analysis['occurrence_count']}")
        lines.append(f"\n   What happened:")
        lines.append(f"   {analysis['explanation']}")
        lines.append(f"\n   How to fix:")
        for suggestion in analysis['suggestions']:
            lines.append(f"   • {suggestion}")
        
        if analysis.get('code_examples'):
            lines.append(f"\n   Code example:")
            for example in analysis['code_examples']:
                lines.append(f"   {example}")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append(f"Analysis complete. {results['total_errors']} errors analyzed.")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
