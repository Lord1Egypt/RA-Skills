---
name: data-leak-detector
description: 数据泄露检测工具。Use when user wants to scan skills, files, or folders for potential data leaks, privacy risks, or suspicious behavior. Detects network calls, file access, process spawning, and environment variable access. 数据安全、隐私检测、安全审计。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install watchdog"
---

# Data Leak Detector

Scan skills, files, and folders for potential data leaks and privacy risks.

## Features

- 🔍 **Static Analysis**: Scan SKILL.md for suspicious patterns
- 🌐 **Network Detection**: Detect external API calls
- 📁 **File Access**: Detect file read/write operations
- 🔄 **Process Detection**: Detect subprocess spawning
- 🔐 **Env Access**: Detect environment variable access
- 📊 **Risk Scoring**: 0-100 risk score with recommendations

## Risk Levels

| Level | Color | Meaning |
|-------|-------|---------|
| 🟢 Low | Green | Safe, no concerns |
| 🟡 Medium | Yellow | Review recommended |
| 🔴 High | Red | Caution required |

## Detection Patterns

### Network Risks
- curl/wget calls
- requests/httpx usage
- External API endpoints
- WebSocket connections

### File Risks
- File read/write operations
- Directory traversal
- Sensitive file access
- Temporary file creation

### Process Risks
- subprocess calls
- os.system usage
- Shell command execution
- Process spawning

### Environment Risks
- Environment variable access
- Config file reading
- Credential access

## Trigger Conditions

- "检查这个skill安全吗" / "Check if this skill is safe"
- "扫描数据泄露" / "Scan for data leaks"
- "这个skill有没有风险" / "Does this skill have risks"
- "data-leak-detector"

---

## Python Code

```python
import os
import re
import json
from pathlib import Path

class DataLeakDetector:
    def __init__(self):
        self.patterns = {
            'network': {
                'high': [
                    r'curl\s+',
                    r'wget\s+',
                    r'requests\.(get|post|put|delete)',
                    r'http[s]?://',
                    r'urllib\.request',
                    r'httpx\.',
                    r'websocket',
                ],
                'medium': [
                    r'fetch\(',
                    r'axios\.',
                ]
            },
            'file_access': {
                'high': [
                    r'open\s*\(',
                    r'os\.remove',
                    r'os\.rmdir',
                    r'shutil\.rmtree',
                ],
                'medium': [
                    r'readFile',
                    r'writeFile',
                    r'os\.path\.exists',
                    r'glob\.',
                ]
            },
            'process': {
                'high': [
                    r'subprocess\.',
                    r'os\.system',
                    r'os\.popen',
                    r'exec\(',
                    r'eval\(',
                ],
                'medium': [
                    r'Popen',
                    r'call\(',
                ]
            },
            'env_access': {
                'high': [
                    r'os\.environ',
                    r'os\.getenv',
                    r'\$[A-Z_]+',
                ],
                'medium': [
                    r'config\[',
                    r'secrets\[',
                ]
            }
        }
    
    def scan_file(self, filepath):
        """Scan a single file for risks"""
        
        risks = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return risks
        
        for category, levels in self.patterns.items():
            for level, patterns in levels.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        risks.append({
                            'category': category,
                            'level': level,
                            'pattern': pattern,
                            'line': line_num,
                            'match': match.group()[:50]
                        })
        
        return risks
    
    def scan_skill(self, skill_path):
        """Scan entire skill for risks"""
        
        skill_path = Path(skill_path)
        
        all_risks = []
        files_scanned = 0
        
        for ext in ['.md', '.py', '.js', '.ts']:
            for filepath in skill_path.rglob(f'*{ext}'):
                risks = self.scan_file(str(filepath))
                for risk in risks:
                    risk['file'] = str(filepath.relative_to(skill_path))
                all_risks.extend(risks)
                files_scanned += 1
        
        return all_risks, files_scanned
    
    def calculate_risk_score(self, risks):
        """Calculate overall risk score (0-100)"""
        
        if not risks:
            return 0
        
        score = 0
        for risk in risks:
            if risk['level'] == 'high':
                score += 20
            elif risk['level'] == 'medium':
                score += 10
        
        return min(score, 100)
    
    def generate_report(self, skill_path, risks, files_scanned):
        """Generate risk assessment report"""
        
        risk_score = self.calculate_risk_score(risks)
        
        if risk_score <= 20:
            risk_level = "🟢 LOW"
            recommendation = "Safe to use"
        elif risk_score <= 50:
            risk_level = "🟡 MEDIUM"
            recommendation = "Review before installing"
        else:
            risk_level = "🔴 HIGH"
            recommendation = "Caution required"
        
        # Group by category
        by_category = {}
        for risk in risks:
            cat = risk['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(risk)
        
        report = []
        report.append(f"{'='*60}")
        report.append(f"DATA LEAK DETECTOR - SECURITY REPORT")
        report.append(f"{'='*60}")
        report.append(f"")
        report.append(f"Skill: {os.path.basename(skill_path)}")
        report.append(f"Files Scanned: {files_scanned}")
        report.append(f"Total Risks Found: {len(risks)}")
        report.append(f"")
        report.append(f"RISK SCORE: {risk_score}/100 ({risk_level})")
        report.append(f"RECOMMENDATION: {recommendation}")
        report.append(f"")
        
        # Category breakdown
        report.append(f"{'='*60}")
        report.append(f"RISK BREAKDOWN")
        report.append(f"{'='*60}")
        
        for category, category_risks in by_category.items():
            high = len([r for r in category_risks if r['level'] == 'high'])
            medium = len([r for r in category_risks if r['level'] == 'medium'])
            report.append(f"")
            report.append(f"{category.upper()}:")
            report.append(f"  High: {high} | Medium: {medium}")
            
            for risk in category_risks[:3]:  # Show top 3
                report.append(f"  - [{risk['level'].upper()}] {risk['match']} (line {risk['line']})")
        
        # Recommendations
        report.append(f"")
        report.append(f"{'='*60}")
        report.append(f"RECOMMENDATIONS")
        report.append(f"{'='*60}")
        
        if 'network' in by_category:
            report.append(f"- Review network calls: verify destinations")
        if 'file_access' in by_category:
            report.append(f"- Review file access: check for sensitive files")
        if 'process' in by_category:
            report.append(f"- Review subprocess calls: verify commands")
        if 'env_access' in by_category:
            report.append(f"- Review env access: check for credential access")
        
        return '\n'.join(report)

# Example usage
detector = DataLeakDetector()

# Scan skill
risks, files_scanned = detector.scan_skill('/path/to/skill')
report = detector.generate_report('/path/to/skill', risks, files_scanned)
print(report)
```

---

## Usage Examples

```
User: "检查这个skill安全吗"
Agent: Scan SKILL.md and generate risk report

User: "扫描我的skills有没有数据泄露"
Agent: Scan all installed skills

User: "这个skill有没有网络访问"
Agent: Focus on network risks
```

---

## Notes

- Static analysis only (no runtime monitoring)
- Fast scanning (seconds)
- No external API calls
- Cross-platform compatible
