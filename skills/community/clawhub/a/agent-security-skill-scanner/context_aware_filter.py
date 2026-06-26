"""
Context-Aware Filter for Security Scanner v6.2.0

Analyzes file context to reduce false positives by understanding
the legitimate purpose of security tools, dev scripts, and templates.
"""

import re
from typing import Dict, Tuple, Any


class ContextAwareFilter:
    """Context-aware risk adjustment for security scanning results."""
    
    # Patterns indicating legitimate security tooling
    SECURITY_TOOL_PATTERNS = [
        r'def\s+(scan|detect|analyze|check|audit|assess|test)',
        r'(security|vulnerability|threat|malware|intrusion)\s+(tool|scanner|detector|framework)',
        r'(sigma|yara|snort|suricata|zeek|nmap|masscan)',
        r'(penetration\s*test|pentest|red\s*team|blue\s*team)',
        r'(ethical\s*hacking|security\s*research|bug\s*bounty)',
        r'(mitre\s*att&ck|attack\s*framework|tactic|technique)',
        r'(cve|cwe|capec|keV)\s*database',
        r'(ioc|indicator\s*of\s*compromise|threat\s*intel)',
        r'(siem|soar|xdr|edr|mdr)',
        r'(compliance|pci|hipaa|gdpr|iso\s*27001)',
    ]
    
    # Patterns indicating development/devops tooling
    DEV_TOOL_PATTERNS = [
        r'def\s+(setup|install|deploy|build|compile|test|lint|format)',
        r'(ci|cd|pipeline|workflow|action)\s*(config|setup|file)',
        r'(docker|kubernetes|k8s|helm|terraform|ansible)',
        r'(github\s*actions|gitlab\s*ci|jenkins|circleci)',
        r'(pytest|unittest|nose|mocha|jest|cypress)',
        r'(black|flake8|pylint|mypy|ruff|isort)',
        r'(webpack|babel|eslint|prettier|tsconfig)',
    ]
    
    def analyze_context(self, content: str) -> Dict[str, Any]:
        """Analyze file content for contextual signals."""
        context_score = 0.0
        signals = []
        
        content_lower = content.lower()
        all_patterns = self.SECURITY_TOOL_PATTERNS + self.DEV_TOOL_PATTERNS
        
        for pattern in all_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                context_score += 0.1
                signals.append(f"Matched pattern: {pattern}")
        
        # Cap at 1.0
        context_score = min(context_score, 1.0)
        
        return {
            'context_score': context_score,
            'signals': signals,
            'is_security_tool': context_score >= 0.3,
            'is_dev_tool': any(re.search(p, content_lower, re.IGNORECASE) 
                             for p in self.DEV_TOOL_PATTERNS),
        }
    
    def should_downgrade_risk(self, context: Dict[str, Any], 
                             original_risk: str) -> Tuple[str, str]:
        """Determine if risk should be downgraded based on context."""
        context_score = context.get('context_score', 0.0)
        
        if context_score < 0.3:
            return original_risk, "Insufficient context for downgrade"
        
        if original_risk == 'CRITICAL':
            return 'MEDIUM', "Context suggests legitimate security tooling"
        elif original_risk == 'HIGH':
            return 'LOW', "Context suggests legitimate development tooling"
        elif original_risk == 'MEDIUM':
            return 'LOW', "Context suggests legitimate purpose"
        elif original_risk == 'LOW':
            return 'SAFE', "Context strongly suggests benign purpose"
        
        return original_risk, "No downgrade needed"
