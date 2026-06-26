#!/usr/bin/env python3
"""
Documentation Consistency Checker
Checks consistency between documentation and code.
"""

import os
import re
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class ConsistencyIssue:
    """Consistency issue"""
    type: str
    severity: str
    location: str
    description: str
    expected: str
    actual: str
    fix_suggestion: str


class ConsistencyChecker:
    """Check documentation consistency"""
    
    def __init__(self, path: str):
        self.root_path = Path(path).resolve()
        self.issues: List[ConsistencyIssue] = []
    
    def check_all(self) -> List[ConsistencyIssue]:
        """Run all consistency checks"""
        print("🔍 Checking documentation consistency...")
        
        self._check_api_docs()
        self._check_code_examples()
        self._check_links()
        
        return self.issues
    
    def _check_api_docs(self):
        """Check API documentation matches code"""
        api_docs = self._find_api_docs()
        if not api_docs:
            return
        
        # Extract documented endpoints
        with open(api_docs, 'r') as f:
            doc_content = f.read()
        
        documented = set(re.findall(r'(?:GET|POST|PUT|DELETE|PATCH)\s+(/\S+)', doc_content, re.IGNORECASE))
        
        # Extract actual endpoints
        actual = set()
        for file_path in self.root_path.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    for match in re.finditer(r'@(?:app|router)\.(?:get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', content, re.IGNORECASE):
                        actual.add(match.group(1))
            except:
                pass
        
        # Find mismatches
        missing = actual - documented
        for endpoint in list(missing)[:5]:
            self.issues.append(ConsistencyIssue(
                type='api_mismatch',
                severity='major',
                location=str(api_docs),
                description=f'Endpoint {endpoint} exists in code but not documented',
                expected='Endpoint should be documented',
                actual='Not in API docs',
                fix_suggestion=f'Add {endpoint} to API documentation'
            ))
    
    def _check_code_examples(self):
        """Check code examples are valid"""
        for md_file in self.root_path.rglob('*.md'):
            try:
                with open(md_file, 'r') as f:
                    content = f.read()
                
                code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
                
                for code in code_blocks[:3]:
                    for match in re.finditer(r'def\s+(\w+)', code):
                        func = match.group(1)
                        if not self._function_exists(func):
                            self.issues.append(ConsistencyIssue(
                                type='code_example_outdated',
                                severity='minor',
                                location=str(md_file),
                                description=f'Function {func} may not exist',
                                expected='Function exists',
                                actual=f'{func} not found',
                                fix_suggestion='Update example'
                            ))
            except:
                pass
    
    def _check_links(self):
        """Check for broken links"""
        for md_file in self.root_path.rglob('*.md'):
            try:
                with open(md_file, 'r') as f:
                    content = f.read()
                
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                for text, link in links:
                    if not link.startswith(('http', '#')):
                        link_path = self.root_path / link.split('#')[0]
                        if not link_path.exists():
                            self.issues.append(ConsistencyIssue(
                                type='broken_link',
                                severity='minor',
                                location=str(md_file),
                                description=f'Link to {link} may be broken',
                                expected='File exists',
                                actual='File not found',
                                fix_suggestion='Fix or remove link'
                            ))
            except:
                pass
    
    def _find_api_docs(self) -> Path:
        """Find API documentation file"""
        for name in ['API.md', 'api.md', 'docs/API.md']:
            path = self.root_path / name
            if path.exists():
                return path
        return None
    
    def _function_exists(self, func_name: str) -> bool:
        """Check if function exists in codebase"""
        for file_path in self.root_path.rglob('*.py'):
            try:
                with open(file_path, 'r') as f:
                    if f'def {func_name}(' in f.read():
                        return True
            except:
                pass
        return False
    
    def export_report(self, output_path: str):
        """Export issues to Markdown"""
        md = []
        md.append("# 🔍 Consistency Check Report\n")
        md.append(f"**Issues Found:** {len(self.issues)}\n")
        
        if self.issues:
            by_severity = {}
            for issue in self.issues:
                by_severity.setdefault(issue.severity, []).append(issue)
            
            for severity in ['critical', 'major', 'minor']:
                if severity in by_severity:
                    md.append(f"\n## {severity.upper()} ({len(by_severity[severity])})\n")
                    for issue in by_severity[severity][:10]:
                        md.append(f"\n### {issue.type}\n")
                        md.append(f"- **Location:** `{issue.location}`")
                        md.append(f"- **Issue:** {issue.description}")
                        md.append(f"- **Fix:** {issue.fix_suggestion}")
        else:
            md.append("\n✅ No consistency issues found!\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        print(f"✅ Report saved to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Check documentation consistency')
    parser.add_argument('--path', '-p', default='.', help='Path to project')
    parser.add_argument('--output', '-o', help='Output file for report')
    
    args = parser.parse_args()
    
    checker = ConsistencyChecker(args.path)
    issues = checker.check_all()
    
    print(f"\n🔍 Found {len(issues)} issues")
    
    if args.output:
        checker.export_report(args.output)


if __name__ == '__main__':
    main()
