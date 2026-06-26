#!/usr/bin/env python3
"""
Documentation Improver
Provides actionable improvement suggestions.
"""

import os
from pathlib import Path
from typing import Dict, List


class DocsImprover:
    """Improve documentation quality"""
    
    def __init__(self, path: str):
        self.root_path = Path(path).resolve()
        self.recommendations: Dict[str, List[str]] = {
            'quick_wins': [],
            'short_term': [],
            'long_term': []
        }
    
    def analyze_and_suggest(self) -> Dict[str, List[str]]:
        """Analyze and provide recommendations"""
        print("💡 Analyzing documentation for improvements...")
        
        self._check_readme()
        self._check_examples()
        self._check_structure()
        
        return self.recommendations
    
    def _check_readme(self):
        """Check README quality"""
        readme = self.root_path / 'README.md'
        
        if not readme.exists():
            self.recommendations['quick_wins'].append('Create README.md with project overview')
            return
        
        with open(readme, 'r') as f:
            content = f.read().lower()
        
        if 'install' not in content:
            self.recommendations['quick_wins'].append('Add installation instructions')
        
        if 'usage' not in content and 'example' not in content:
            self.recommendations['quick_wins'].append('Add usage examples')
        
        if '```' not in content:
            self.recommendations['quick_wins'].append('Add code examples')
        
        if 'contribut' not in content:
            self.recommendations['short_term'].append('Add contributing guidelines')
    
    def _check_examples(self):
        """Check example quality"""
        examples_dir = self.root_path / 'examples'
        
        if not examples_dir.exists() or not any(examples_dir.iterdir()):
            self.recommendations['short_term'].append('Add examples directory with working examples')
    
    def _check_structure(self):
        """Check documentation structure"""
        docs_dir = self.root_path / 'docs'
        
        if not docs_dir.exists():
            self.recommendations['short_term'].append('Create docs/ directory for detailed documentation')
        
        required_docs = {
            'API.md': 'API documentation',
            'ARCHITECTURE.md': 'Architecture documentation',
            'CONTRIBUTING.md': 'Contributing guidelines'
        }
        
        for doc, desc in required_docs.items():
            if not (docs_dir / doc).exists() and not (self.root_path / doc).exists():
                self.recommendations['long_term'].append(f'Create {desc}')
    
    def export_plan(self, output_path: str):
        """Export improvement plan"""
        md = []
        md.append("# 💡 Documentation Improvement Plan\n")
        
        md.append("\n## Quick Wins (Hours)\n")
        for rec in self.recommendations['quick_wins']:
            md.append(f"- [ ] {rec}")
        
        md.append("\n## Short Term (Days)\n")
        for rec in self.recommendations['short_term']:
            md.append(f"- [ ] {rec}")
        
        md.append("\n## Long Term (Weeks)\n")
        for rec in self.recommendations['long_term']:
            md.append(f"- [ ] {rec}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        print(f"✅ Plan saved to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Improve documentation')
    parser.add_argument('--path', '-p', default='.', help='Path to project')
    parser.add_argument('--output', '-o', help='Output file for improvement plan')
    
    args = parser.parse_args()
    
    improver = DocsImprover(args.path)
    recommendations = improver.analyze_and_suggest()
    
    print("\n💡 Recommendations:")
    print("\nQuick Wins:")
    for rec in recommendations['quick_wins']:
        print(f"  - {rec}")
    
    print("\nShort Term:")
    for rec in recommendations['short_term']:
        print(f"  - {rec}")
    
    print("\nLong Term:")
    for rec in recommendations['long_term']:
        print(f"  - {rec}")
    
    if args.output:
        improver.export_plan(args.output)


if __name__ == '__main__':
    main()
