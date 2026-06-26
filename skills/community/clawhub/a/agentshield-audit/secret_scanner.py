"""
Secret Leakage Detector
Scans for hardcoded secrets, API keys, and sensitive data.
Integrates with open-source tools: detect-secrets, truffleHog patterns
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SecretFinding:
    """Represents a found secret."""
    type: str
    file: str
    line: int
    snippet: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    confidence: float  # 0.0 - 1.0


class SecretScanner:
    """
    Scans agent workspace for leaked secrets.
    Uses open-source patterns + custom rules for AI agents.
    """
    
    # Patterns based on detect-secrets and truffleHog
    PATTERNS = {
        # API Keys
        'openai_api_key': {
            'pattern': r'sk-[a-zA-Z0-9]{48}',
            'severity': 'CRITICAL',
            'description': 'OpenAI API Key'
        },
        'anthropic_api_key': {
            'pattern': r'sk-ant-[a-zA-Z0-9]{32,}',
            'severity': 'CRITICAL',
            'description': 'Anthropic API Key'
        },
        'google_api_key': {
            'pattern': r'AIza[0-9A-Za-z_-]{35}',
            'severity': 'CRITICAL',
            'description': 'Google API Key'
        },
        'aws_access_key': {
            'pattern': r'AKIA[0-9A-Z]{16}',
            'severity': 'CRITICAL',
            'description': 'AWS Access Key ID'
        },
        'aws_secret_key': {
            'pattern': r'[0-9a-zA-Z/+]{40}',
            'severity': 'CRITICAL',
            'description': 'AWS Secret Key'
        },
        'github_token': {
            'pattern': r'ghp_[a-zA-Z0-9]{36}',
            'severity': 'CRITICAL',
            'description': 'GitHub Personal Access Token'
        },
        'slack_token': {
            'pattern': r'xox[baprs]-[0-9a-zA-Z]{10,48}',
            'severity': 'CRITICAL',
            'description': 'Slack Token'
        },
        'discord_token': {
            'pattern': r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}',
            'severity': 'CRITICAL',
            'description': 'Discord Bot Token'
        },
        'telegram_token': {
            'pattern': r'\d{9,10}:[a-zA-Z0-9_-]{35}',
            'severity': 'CRITICAL',
            'description': 'Telegram Bot Token'
        },
        'moltbook_api_key': {
            'pattern': r'moltbook_sk_[a-z]{2}_[A-Za-z0-9_-]{32,}',
            'severity': 'CRITICAL',
            'description': 'Moltbook API Key'
        },
        
        # Generic secrets
        'generic_api_key': {
            'pattern': r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9]{32,}["\']?',
            'severity': 'HIGH',
            'description': 'Generic API Key'
        },
        'generic_secret': {
            'pattern': r'(?i)(secret|password|passwd|pwd)\s*[:=]\s*["\'][^"\']{8,}["\']',
            'severity': 'HIGH',
            'description': 'Generic Secret/Password'
        },
        'private_key': {
            'pattern': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
            'severity': 'CRITICAL',
            'description': 'Private Key'
        },
        'jwt_token': {
            'pattern': r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
            'severity': 'MEDIUM',
            'description': 'JWT Token'
        },
        'database_url': {
            'pattern': r'(?i)(postgres|mysql|mongodb)://[^\s"\']+',
            'severity': 'HIGH',
            'description': 'Database Connection String'
        },
    }
    
    # Files to exclude from scanning
    EXCLUDE_PATTERNS = [
        r'\.git/',
        r'__pycache__/',
        r'\.pyc$',
        r'node_modules/',
        r'\.env\.example',
        r'\.sample$',
        r'CHANGELOG',
        r'README',
        r'\.md$',
        r'certificate\.json$',  # Our own certificates
        r'agent\.key$',  # Our own keys
    ]
    
    def __init__(self, workspace_path: str = None):
        """Initialize scanner with workspace path."""
        if workspace_path:
            self.workspace = Path(workspace_path).expanduser()
        else:
            self.workspace = Path.home() / ".openclaw" / "workspace"
        
        self.findings: List[SecretFinding] = []
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        path_str = str(file_path)
        
        # Skip excluded patterns
        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, path_str):
                return False
        
        # Skip binary files
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:  # Binary file
                    return False
        except:
            return False
        
        return True
    
    def scan_file(self, file_path: Path) -> List[SecretFinding]:
        """Scan a single file for secrets."""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception:
            return findings
        
        # Scan each pattern
        for secret_type, config in self.PATTERNS.items():
            pattern = config['pattern']
            severity = config['severity']
            description = config['description']
            
            for match in re.finditer(pattern, content):
                # Find line number
                start_pos = match.start()
                line_num = content[:start_pos].count('\n') + 1
                
                # Get snippet (context around match)
                line_start = content.rfind('\n', 0, start_pos) + 1
                line_end = content.find('\n', start_pos)
                if line_end == -1:
                    line_end = len(content)
                
                snippet = content[line_start:line_end].strip()
                # Mask the actual secret in snippet
                secret = match.group(0)
                masked_snippet = snippet.replace(secret, '*' * min(len(secret), 20))
                
                # Calculate confidence
                confidence = self._calculate_confidence(secret_type, secret, file_path)
                
                finding = SecretFinding(
                    type=description,
                    file=str(file_path.relative_to(self.workspace)),
                    line=line_num,
                    snippet=masked_snippet,
                    severity=severity,
                    confidence=confidence
                )
                findings.append(finding)
        
        return findings
    
    def _calculate_confidence(self, secret_type: str, secret: str, file_path: Path) -> float:
        """Calculate confidence score for a finding."""
        confidence = 0.8  # Base confidence
        
        # High confidence for well-known patterns
        if secret_type in ['openai_api_key', 'anthropic_api_key', 'github_token', 
                          'slack_token', 'discord_token', 'telegram_token', 'moltbook_api_key']:
            confidence = 0.95
        
        # Adjust based on file type
        if file_path.suffix in ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env']:
            confidence += 0.05
        
        # Reduce confidence for short matches
        if len(secret) < 20:
            confidence -= 0.1
        
        return min(confidence, 1.0)
    
    def scan(self) -> Dict:
        """
        Run full workspace scan.
        Returns scan report.
        """
        self.findings = []
        files_scanned = 0
        
        # Walk workspace
        for file_path in self.workspace.rglob('*'):
            if not file_path.is_file():
                continue
            
            if not self.should_scan_file(file_path):
                continue
            
            files_scanned += 1
            findings = self.scan_file(file_path)
            self.findings.extend(findings)
        
        # Calculate score
        score = self._calculate_score()
        
        return {
            'scan_summary': {
                'files_scanned': files_scanned,
                'findings_count': len(self.findings),
                'critical_count': sum(1 for f in self.findings if f.severity == 'CRITICAL'),
                'high_count': sum(1 for f in self.findings if f.severity == 'HIGH'),
                'medium_count': sum(1 for f in self.findings if f.severity == 'MEDIUM'),
                'low_count': sum(1 for f in self.findings if f.severity == 'LOW'),
            },
            'score': score,
            'passed': score >= 70,
            'findings': [
                {
                    'type': f.type,
                    'file': f.file,
                    'line': f.line,
                    'snippet': f.snippet,
                    'severity': f.severity,
                    'confidence': round(f.confidence, 2)
                }
                for f in self.findings
            ]
        }
    
    def _calculate_score(self) -> int:
        """Calculate security score based on findings."""
        base_score = 100
        
        for finding in self.findings:
            if finding.severity == 'CRITICAL':
                base_score -= 25
            elif finding.severity == 'HIGH':
                base_score -= 15
            elif finding.severity == 'MEDIUM':
                base_score -= 5
            elif finding.severity == 'LOW':
                base_score -= 2
        
        return max(0, base_score)
    
    def export_to_detect_secrets_format(self) -> Dict:
        """Export findings in detect-secrets compatible format."""
        return {
            'version': '1.0.0',
            'plugins_used': list(self.PATTERNS.keys()),
            'filters_used': [],
            'results': {
                f.file: [
                    {
                        'type': f.type,
                        'filename': f.file,
                        'hashed_secret': '<masked>',
                        'is_verified': False,
                        'line_number': f.line
                    }
                    for f in self.findings if f.file == file
                ]
                for file in set(f.file for f in self.findings)
            }
        }


def run_secret_leakage_test(workspace_path: str = None) -> Dict:
    """
    Convenience function to run secret leakage test.
    Returns test results for AgentShield audit.
    """
    scanner = SecretScanner(workspace_path)
    result = scanner.scan()
    
    return {
        'test_name': 'secret_leakage',
        'passed': result['passed'],
        'score': result['score'],
        'details': result['scan_summary'],
        'findings': result['findings'][:5]  # Top 5 only for report
    }


if __name__ == '__main__':
    # Test run
    print("🔍 Running Secret Leakage Test...")
    result = run_secret_leakage_test()
    
    print(f"\nScore: {result['score']}/100")
    print(f"Passed: {result['passed']}")
    print(f"Files scanned: {result['details']['files_scanned']}")
    print(f"Secrets found: {result['details']['findings_count']}")
    
    if result['findings']:
        print("\n⚠️ Top findings:")
        for f in result['findings'][:3]:
            print(f"  - {f['type']} in {f['file']}:{f['line']} ({f['severity']})")
