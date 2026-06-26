#!/usr/bin/env python3
"""
Documentation Quality Analyzer
Analyzes documentation completeness, accuracy, clarity, structure, and maintainability.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QualityReport:
    """Documentation quality report"""
    overall_score: int = 0
    completeness_score: int = 0
    accuracy_score: int = 0
    clarity_score: int = 0
    structure_score: int = 0
    maintainability_score: int = 0
    
    files_analyzed: List[Dict] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    recommendations: Dict[str, List[str]] = field(default_factory=lambda: {
        'quick_wins': [],
        'short_term': [],
        'long_term': []
    })


class DocsAnalyzer:
    """Analyze documentation quality"""
    
    ESSENTIAL_DOCS = ['README.md', 'README.rst', 'README.txt']
    IMPORTANT_DOCS = ['CHANGELOG.md', 'CONTRIBUTING.md', 'LICENSE', 'API.md', 'ARCHITECTURE.md']
    
    def __init__(self, path: str):
        self.root_path = Path(path).resolve()
        self.report = QualityReport()
        self.doc_files: List[Path] = []
        
    def scan(self) -> List[Path]:
        """Scan for documentation files"""
        print(f"📚 Scanning documentation in: {self.root_path}")
        
        # Find all markdown and text files
        for pattern in ['*.md', '*.rst', '*.txt', '*.adoc']:
            self.doc_files.extend(self.root_path.rglob(pattern))
        
        # Filter out node_modules, vendor, etc.
        exclude_dirs = {'node_modules', 'vendor', '.git', 'dist', 'build'}
        self.doc_files = [
            f for f in self.doc_files 
            if not any(exclude in str(f) for exclude in exclude_dirs)
        ]
        
        print(f"  Found {len(self.doc_files)} documentation files")
        return self.doc_files
    
    def analyze(self) -> QualityReport:
        """Analyze all documentation files"""
        print("📊 Analyzing documentation quality...")
        
        if not self.doc_files:
            self.report.overall_score = 0
            self.report.issues.append({
                'severity': 'critical',
                'type': 'no_docs',
                'description': 'No documentation files found',
                'fix': 'Create README.md with project overview'
            })
            return self.report
        
        # Analyze each file
        scores = []
        for file_path in self.doc_files:
            score = self._analyze_file(file_path)
            scores.append(score)
            self.report.files_analyzed.append({
                'path': str(file_path.relative_to(self.root_path)),
                'size': file_path.stat().st_size,
                'score': score['overall']
            })
        
        # Calculate overall scores
        if scores:
            self.report.overall_score = sum(s['overall'] for s in scores) // len(scores)
            self.report.completeness_score = sum(s['completeness'] for s in scores) // len(scores)
            self.report.accuracy_score = sum(s['accuracy'] for s in scores) // len(scores)
            self.report.clarity_score = sum(s['clarity'] for s in scores) // len(scores)
            self.report.structure_score = sum(s['structure'] for s in scores) // len(scores)
            self.report.maintainability_score = sum(s['maintainability'] for s in scores) // len(scores)
        
        # Generate recommendations
        self._generate_recommendations()
        
        return self.report
    
    def _analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single documentation file"""
        scores = {
            'overall': 0,
            'completeness': 0,
            'accuracy': 0,
            'clarity': 0,
            'structure': 0,
            'maintainability': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return scores
        
        # Completeness (30%)
        scores['completeness'] = self._check_completeness(content, file_path.name)
        
        # Clarity (25%)
        scores['clarity'] = self._check_clarity(content)
        
        # Structure (20%)
        scores['structure'] = self._check_structure(content)
        
        # Maintainability (15%)
        scores['maintainability'] = self._check_maintainability(content)
        
        # Accuracy (10%) - Hard to assess automatically
        scores['accuracy'] = 70  # Default
        
        # Weighted overall
        scores['overall'] = int(
            scores['completeness'] * 0.30 +
            scores['accuracy'] * 0.10 +
            scores['clarity'] * 0.25 +
            scores['structure'] * 0.20 +
            scores['maintainability'] * 0.15
        )
        
        return scores
    
    def _check_completeness(self, content: str, filename: str) -> int:
        """Check documentation completeness"""
        checks = [
            ('has_title', '#' in content),
            ('has_description', len(content) > 200),
            ('has_sections', content.count('## ') >= 2),
            ('has_code_examples', '```' in content),
            ('has_links', '](' in content or 'http' in content),
        ]
        
        if filename.startswith('README'):
            checks.extend([
                ('has_installation', 'install' in content.lower()),
                ('has_usage', 'usage' in content.lower() or 'example' in content.lower()),
            ])
        
        passed = sum(1 for _, check in checks if check)
        return min(100, passed * 100 // len(checks))
    
    def _check_clarity(self, content: str) -> int:
        """Check documentation clarity"""
        score = 100
        
        # Penalize very long paragraphs
        paragraphs = content.split('\n\n')
        long_paragraphs = sum(1 for p in paragraphs if len(p) > 500)
        score -= min(30, long_paragraphs * 5)
        
        # Reward use of lists
        if '-' in content or '*' in content or '1.' in content:
            score += 10
        
        # Reward use of headings
        heading_count = content.count('#')
        if heading_count >= 5:
            score += 10
        elif heading_count >= 3:
            score += 5
        
        return max(0, min(100, score))
    
    def _check_structure(self, content: str) -> int:
        """Check documentation structure"""
        score = 0
        
        # Check heading hierarchy
        if '# ' in content:
            score += 20  # Has H1
        if '## ' in content:
            score += 30  # Has H2
        if '### ' in content:
            score += 20  # Has H3
        
        # Check for table of contents
        if 'toc' in content.lower() or 'contents' in content.lower():
            score += 15
        
        # Check for consistent formatting
        if content.count('```') % 2 == 0:  # Balanced code blocks
            score += 15
        
        return min(100, score)
    
    def _check_maintainability(self, content: str) -> int:
        """Check documentation maintainability"""
        score = 100
        
        # Penalize very long files
        if len(content) > 50000:
            score -= 20
        
        # Penalize outdated content indicators
        if 'TODO' in content or 'FIXME' in content:
            score -= 15
        
        # Reward internal linking
        internal_links = len([l for l in content.split() if l.startswith('[') and '](' in l])
        if internal_links >= 5:
            score += 15
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self):
        """Generate improvement recommendations"""
        report = self.report
        
        if report.completeness_score < 60:
            report.recommendations['quick_wins'].append('Add project description and badges')
            report.recommendations['quick_wins'].append('Add code examples')
        
        if report.structure_score < 60:
            report.recommendations['short_term'].append('Improve document structure with clear sections')
            report.recommendations['short_term'].append('Add table of contents')
        
        if report.maintainability_score < 60:
            report.recommendations['long_term'].append('Break down large documents')
            report.recommendations['long_term'].append('Remove TODOs and FIXMEs')
        
        report.recommendations['long_term'].append('Set up automated documentation generation')
        report.recommendations['long_term'].append('Establish documentation review process')
    
    def export_report(self, output_path: str):
        """Export quality report to Markdown"""
        report = self.report
        
        md = []
        md.append("# 📊 Documentation Quality Report\n")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append(f"**Path:** {self.root_path}\n")
        
        md.append("\n## Overall Score\n")
        md.append(f"**{report.overall_score}/100** {self._score_emoji(report.overall_score)}\n")
        
        md.append("\n## Dimension Scores\n")
        md.append("| Dimension | Score | Status |")
        md.append("|-----------|-------|--------|")
        md.append(f"| Completeness | {report.completeness_score}/100 | {self._score_status(report.completeness_score)} |")
        md.append(f"| Accuracy | {report.accuracy_score}/100 | {self._score_status(report.accuracy_score)} |")
        md.append(f"| Clarity | {report.clarity_score}/100 | {self._score_status(report.clarity_score)} |")
        md.append(f"| Structure | {report.structure_score}/100 | {self._score_status(report.structure_score)} |")
        md.append(f"| Maintainability | {report.maintainability_score}/100 | {self._score_status(report.maintainability_score)} |")
        
        if report.issues:
            md.append("\n## Issues\n")
            for issue in report.issues:
                md.append(f"- **[{issue['severity'].upper()}]** {issue['description']}")
                md.append(f"  - Fix: {issue['fix']}\n")
        
        md.append("\n## Recommendations\n")
        md.append("\n### Quick Wins\n")
        for rec in report.recommendations['quick_wins']:
            md.append(f"- [ ] {rec}")
        
        md.append("\n### Short Term\n")
        for rec in report.recommendations['short_term']:
            md.append(f"- [ ] {rec}")
        
        md.append("\n### Long Term\n")
        for rec in report.recommendations['long_term']:
            md.append(f"- [ ] {rec}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        print(f"✅ Report saved to: {output_path}")
    
    def _score_emoji(self, score: int) -> str:
        """Get emoji for score"""
        if score >= 90:
            return "🏆"
        elif score >= 80:
            return "✅"
        elif score >= 70:
            return "👍"
        elif score >= 60:
            return "⚠️"
        else:
            return "❌"
    
    def _score_status(self, score: int) -> str:
        """Get status text for score"""
        if score >= 80:
            return "✅ Good"
        elif score >= 60:
            return "⚠️ Needs Work"
        else:
            return "❌ Poor"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze documentation quality')
    parser.add_argument('--path', '-p', default='.', help='Path to project')
    parser.add_argument('--output', '-o', help='Output file for report')
    
    args = parser.parse_args()
    
    analyzer = DocsAnalyzer(args.path)
    analyzer.scan()
    report = analyzer.analyze()
    
    print(f"\n📊 Overall Score: {report.overall_score}/100")
    print(f"\nDimension Scores:")
    print(f"  - Completeness: {report.completeness_score}/100")
    print(f"  - Clarity: {report.clarity_score}/100")
    print(f"  - Structure: {report.structure_score}/100")
    print(f"  - Maintainability: {report.maintainability_score}/100")
    
    if args.output:
        analyzer.export_report(args.output)


if __name__ == '__main__':
    main()
