#!/usr/bin/env python3
"""
Contradiction Checker - Detect conflicting facts
"""

import json
from pathlib import Path
from typing import List, Dict, Set
import re

class ContradictionChecker:
    def __init__(self):
        # Patterns that might indicate contradictions
        self.contradiction_patterns = [
            # Same entity, different values
            (r'模型[:：]\s*(\w+)', 'model'),
            (r'API\s*Key[:：]\s*([a-zA-Z0-9-]+)', 'api_key'),
            (r'Provider[:：]\s*(\w+)', 'provider'),
            # Status changes
            (r'(✅|成功|完成)', 'success'),
            (r'(❌|失败|错误)', 'failure'),
        ]
    
    def extract_key_values(self, content: str) -> Dict[str, str]:
        """Extract key-value pairs that might conflict"""
        values = {}
        
        for pattern, key_type in self.contradiction_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                key = f"{key_type}:{match}"
                if key in values:
                    # Potential contradiction found
                    pass
                else:
                    values[key] = match
        
        return values
    
    def check_contradictions(self, old_facts: List[Dict], new_facts: List[Dict]) -> List[Dict]:
        """Check for contradictions between old and new facts"""
        contradictions = []
        
        old_values = {}
        for fact in old_facts:
            if fact.get('text'):
                vals = self.extract_key_values(fact['text'])
                old_values.update(vals)
        
        for fact in new_facts:
            if fact.get('text'):
                new_vals = self.extract_key_values(fact['text'])
                for key, value in new_vals.items():
                    if key in old_values and old_values[key] != value:
                        contradictions.append({
                            'type': 'value_changed',
                            'key': key,
                            'old_value': old_values[key],
                            'new_value': value,
                            'old_source': f"memory/{fact.get('source', 'unknown')}",
                            'new_source': fact.get('source', 'unknown')
                        })
        
        return contradictions
    
    def check_status_conflicts(self, content: str) -> List[Dict]:
        """Check for conflicting statuses in the same content"""
        conflicts = []
        
        success_pattern = r'(?:✅|成功|完成|已修复)'
        failure_pattern = r'(?:❌|失败|错误|未完成)'
        
        has_success = bool(re.search(success_pattern, content))
        has_failure = bool(re.search(failure_pattern, content))
        
        if has_success and has_failure:
            conflicts.append({
                'type': 'mixed_status',
                'description': 'Both success and failure indicators found'
            })
        
        return conflicts

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: checker.py <file1> [file2]")
        sys.exit(1)
    
    checker = ContradictionChecker()
    
    file1 = sys.argv[1]
    with open(file1, 'r') as f:
        content1 = f.read()
    
    conflicts = checker.check_status_conflicts(content1)
    
    if conflicts:
        print(f"Found {len(conflicts)} potential issues:")
        for c in conflicts:
            print(f"  - {c['type']}: {c.get('description', '')}")
    else:
        print("No conflicts found")
    
    if len(sys.argv) > 2:
        file2 = sys.argv[2]
        with open(file2, 'r') as f:
            content2 = f.read()
        
        # Simple check - just compare content
        if content1 != content2:
            print(f"\nFiles differ (not a contradiction, just different versions)")

if __name__ == '__main__':
    main()
