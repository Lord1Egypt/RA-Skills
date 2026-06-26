#!/usr/bin/env python3
"""
Docs Improver - Main Entry Point
Analyze, Generate, Check, and Improve Documentation
"""

import argparse
import sys
from pathlib import Path

# Import modules
from analyze import DocsAnalyzer
from generate import DocsGenerator
from consistency_check import ConsistencyChecker
from improve import DocsImprover


def main():
    parser = argparse.ArgumentParser(
        description='Docs Improver - Complete Documentation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --path . --mode all                    # Full analysis + generation + checking
  %(prog)s --path . --mode analyze                # Quality assessment only
  %(prog)s --path . --mode generate               # Generate missing docs
  %(prog)s --path . --mode check                  # Consistency check
  %(prog)s --path . --mode improve                # Improvement suggestions
  %(prog)s --path . --mode all --report report.md # Save report
        """
    )
    
    parser.add_argument('--path', '-p', default='.', help='Path to project')
    parser.add_argument('--mode', '-m', default='all',
                       choices=['analyze', 'generate', 'check', 'improve', 'all'],
                       help='Operation mode')
    parser.add_argument('--output', '-o', help='Output directory for generated docs')
    parser.add_argument('--report', '-r', help='Output file for reports')
    
    args = parser.parse_args()
    
    print(f"📚 Docs Improver - {args.mode.title()} Mode")
    print(f"Path: {args.path}\n")
    
    if args.mode in ['analyze', 'all']:
        print("=" * 60)
        print("📊 DOCUMENTATION QUALITY ANALYSIS")
        print("=" * 60)
        analyzer = DocsAnalyzer(args.path)
        analyzer.scan()
        report = analyzer.analyze()
        
        print(f"\n📊 Overall Score: {report.overall_score}/100")
        print(f"\nDimension Scores:")
        print(f"  - Completeness: {report.completeness_score}/100")
        print(f"  - Clarity: {report.clarity_score}/100")
        print(f"  - Structure: {report.structure_score}/100")
        print(f"  - Maintainability: {report.maintainability_score}/100")
        
        if args.report:
            analyzer.export_report(args.report.replace('.md', '_quality.md'))
    
    if args.mode in ['generate', 'all']:
        print("\n" + "=" * 60)
        print("📝 DOCUMENTATION GENERATION")
        print("=" * 60)
        generator = DocsGenerator(args.path)
        generator.generate_all(args.output)
    
    if args.mode in ['check', 'all']:
        print("\n" + "=" * 60)
        print("🔍 CONSISTENCY CHECK")
        print("=" * 60)
        checker = ConsistencyChecker(args.path)
        issues = checker.check_all()
        
        print(f"\n🔍 Found {len(issues)} issues")
        
        if issues:
            print("\nTop Issues:")
            for issue in issues[:5]:
                print(f"  [{issue.severity.upper()}] {issue.description}")
        
        if args.report:
            checker.export_report(args.report.replace('.md', '_consistency.md'))
    
    if args.mode in ['improve', 'all']:
        print("\n" + "=" * 60)
        print("💡 IMPROVEMENT RECOMMENDATIONS")
        print("=" * 60)
        improver = DocsImprover(args.path)
        recommendations = improver.analyze_and_suggest()
        
        print("\n💡 Recommendations:")
        print("\nQuick Wins (Hours):")
        for rec in recommendations['quick_wins']:
            print(f"  - {rec}")
        
        print("\nShort Term (Days):")
        for rec in recommendations['short_term']:
            print(f"  - {rec}")
        
        print("\nLong Term (Weeks):")
        for rec in recommendations['long_term']:
            print(f"  - {rec}")
        
        if args.report:
            improver.export_plan(args.report.replace('.md', '_improvements.md'))
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
