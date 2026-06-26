"""Output Data Loss Prevention (DLP) - Prevent Sensitive Data Exfiltration

Scans all agent outputs for:
- PII (Personally Identifiable Information)
- API Keys and Credentials
- Financial data
- Exfiltration patterns

Implements multiple modes:
- REDACTION: Replace sensitive data with ***
- BLOCK: Prevent output entirely
- AUDIT: Log only, don't block
"""

import re
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum


class DLPMode(Enum):
    REDACTION = "redaction"  # Replace with ***
    BLOCK = "block"          # Block output entirely
    AUDIT = "audit"          # Log only, don't block


class SensitivityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DLPFinding:
    """Single DLP detection finding"""
    detection_type: str
    sensitivity: SensitivityLevel
    description: str
    matched_text: str
    position_start: int
    position_end: int
    redacted_text: str = ""
    confidence: float = 0.0


@dataclass
class DLPReport:
    """Complete DLP analysis report"""
    original_length: int
    sanitized_length: int
    findings: List[DLPFinding] = field(default_factory=list)
    was_blocked: bool = False
    block_reason: str = ""
    redaction_count: int = 0
    mode: DLPMode = DLPMode.REDACTION
    
    def has_critical(self) -> bool:
        return any(f.sensitivity == SensitivityLevel.CRITICAL for f in self.findings)
    
    def has_high(self) -> bool:
        return any(f.sensitivity == SensitivityLevel.HIGH for f in self.findings)


class PIIPatterns:
    """PII detection patterns"""
    
    # Credit Cards
    CREDIT_CARD = re.compile(
        r'\b(?:4[0-9]{12}(?:[0-9]{3})?'  # Visa
        r'|5[1-5][0-9]{14}'               # MasterCard
        r'|3[47][0-9]{13}'                # Amex
        r'|3(?:0[0-5]|[68][0-9])[0-9]{11}'  # Diners
        r'|(?:2131|1800|35\d{3})\d{11}'  # JCB
        r')\b'
    )
    
    # SSN (US)
    US_SSN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    
    # German Personalausweis
    GERMAN_ID = re.compile(r'\b[0-9]{9}[A-Z]{2}\b')
    
    # IBAN
    IBAN = re.compile(r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b')
    
    # Phone Numbers (general)
    PHONE = re.compile(
        r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    )
    
    # Email addresses
    EMAIL = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # IP Addresses
    IP_ADDRESS = re.compile(
        r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    )


class CredentialPatterns:
    """Credential detection patterns"""
    
    # API Keys (common patterns)
    OPENAI_API_KEY = re.compile(r'sk-[a-zA-Z0-9]{48}')
    ANTHROPIC_API_KEY = re.compile(r'sk-ant-[a-zA-Z0-9]{32,}')
    AWS_ACCESS_KEY = re.compile(r'AKIA[0-9A-Z]{16}')
    AWS_SECRET_KEY = re.compile(r'[0-9a-zA-Z/+]{40}')  # Generic base64-like
    GITHUB_TOKEN = re.compile(r'ghp_[a-zA-Z0-9]{36}')
    SLACK_TOKEN = re.compile(r'xox[baprs]-[0-9a-zA-Z-]+')
    STRIPE_KEY = re.compile(r'sk_live_[0-9a-zA-Z]{24,}')
    
    # Generic patterns
    GENERIC_API_KEY = re.compile(
        r'(api[_-]?key|apikey|api[_-]?secret)\s*[:=]\s*["\']?[a-zA-Z0-9_-]{16,}["\']?',
        re.IGNORECASE
    )
    BEARER_TOKEN = re.compile(
        r'bearer\s+[a-zA-Z0-9_-]{20,}',
        re.IGNORECASE
    )
    PASSWORD = re.compile(
        r'(password|passwd|pwd)\s*[:=]\s*["\']?[^"\'\s]{8,}["\']?',
        re.IGNORECASE
    )


class ExfiltrationPatterns:
    """Data exfiltration detection patterns"""
    
    # Suspicious URLs
    URL_WITH_DATA = re.compile(
        r'https?://[^/\s]+\?(?:data|payload|info|dump|exfil|log)=',
        re.IGNORECASE
    )
    
    # Suspicious base64
    SUSPICIOUS_BASE64 = re.compile(
        r'[A-Za-z0-9+/]{100,}={0,2}'
    )
    
    # Large data blocks
    LARGE_DATA_BLOCK = re.compile(
        r'(\{[^}]{500,}\}|\[[^\]]{500,}\])'  # Large JSON arrays/objects
    )


class OutputDLP:
    """Data Loss Prevention engine for agent outputs"""
    
    def __init__(self, mode: DLPMode = DLPMode.REDACTION, 
                 allow_pii_in_code: bool = True):
        """
        Args:
            mode: How to handle sensitive data
            allow_pii_in_code: Allow PII in code blocks (may be legitimate examples)
        """
        self.mode = mode
        self.allow_pii_in_code = allow_pii_in_code
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile all detection patterns"""
        self.pii_patterns = [
            ("CREDIT_CARD", PIIPatterns.CREDIT_CARD, SensitivityLevel.CRITICAL),
            ("SSN", PIIPatterns.US_SSN, SensitivityLevel.CRITICAL),
            ("GERMAN_ID", PIIPatterns.GERMAN_ID, SensitivityLevel.HIGH),
            ("IBAN", PIIPatterns.IBAN, SensitivityLevel.HIGH),
            ("PHONE", PIIPatterns.PHONE, SensitivityLevel.MEDIUM),
            ("EMAIL", PIIPatterns.EMAIL, SensitivityLevel.MEDIUM),
            ("IP_ADDRESS", PIIPatterns.IP_ADDRESS, SensitivityLevel.LOW),
        ]
        
        self.credential_patterns = [
            ("OPENAI_API_KEY", CredentialPatterns.OPENAI_API_KEY, SensitivityLevel.CRITICAL),
            ("ANTHROPIC_API_KEY", CredentialPatterns.ANTHROPIC_API_KEY, SensitivityLevel.CRITICAL),
            ("AWS_ACCESS_KEY", CredentialPatterns.AWS_ACCESS_KEY, SensitivityLevel.CRITICAL),
            ("GITHUB_TOKEN", CredentialPatterns.GITHUB_TOKEN, SensitivityLevel.CRITICAL),
            ("STRIPE_KEY", CredentialPatterns.STRIPE_KEY, SensitivityLevel.CRITICAL),
            ("SLACK_TOKEN", CredentialPatterns.SLACK_TOKEN, SensitivityLevel.HIGH),
            ("GENERIC_API_KEY", CredentialPatterns.GENERIC_API_KEY, SensitivityLevel.HIGH),
            ("BEARER_TOKEN", CredentialPatterns.BEARER_TOKEN, SensitivityLevel.HIGH),
            ("PASSWORD", CredentialPatterns.PASSWORD, SensitivityLevel.CRITICAL),
        ]
        
        self.exfil_patterns = [
            ("SUSPICIOUS_URL", ExfiltrationPatterns.URL_WITH_DATA, SensitivityLevel.HIGH),
            ("LARGE_DATA_BLOCK", ExfiltrationPatterns.LARGE_DATA_BLOCK, SensitivityLevel.MEDIUM),
        ]
    
    def scan(self, output: str) -> DLPReport:
        """
        Scan output for sensitive data
        
        Returns:
            DLPReport with findings and (optionally) redacted text
        """
        findings = []
        sanitized = output
        offset = 0
        
        # Find all matches
        all_matches = []
        
        # Check PII patterns
        for pii_type, pattern, sensitivity in self.pii_patterns:
            for match in pattern.finditer(output):
                # Skip if in code block and allow_pii_in_code
                if self.allow_pii_in_code and self._is_in_code_block(output, match.start()):
                    continue
                    
                all_matches.append({
                    "type": pii_type,
                    "sensitivity": sensitivity,
                    "match": match,
                    "category": "PII"
                })
        
        # Check credential patterns
        for cred_type, pattern, sensitivity in self.credential_patterns:
            for match in pattern.finditer(output):
                all_matches.append({
                    "type": cred_type,
                    "sensitivity": sensitivity,
                    "match": match,
                    "category": "CREDENTIAL"
                })
        
        # Check exfiltration patterns
        for exfil_type, pattern, sensitivity in self.exfil_patterns:
            for match in pattern.finditer(output):
                all_matches.append({
                    "type": exfil_type,
                    "sensitivity": sensitivity,
                    "match": match,
                    "category": "EXFILTRATION"
                })
        
        # Sort by position
        all_matches.sort(key=lambda x: x["match"].start())
        
        # Process findings and apply redactions
        for m in all_matches:
            match = m["match"]
            
            finding = DLPFinding(
                detection_type=m["type"],
                sensitivity=m["sensitivity"],
                description=f"Detected {m['category']}: {m['type']}",
                matched_text=match.group(),
                position_start=match.start(),
                position_end=match.end(),
                confidence=1.0  # Pattern-based detection
            )
            
            # Generate redaction
            redacted = self._generate_redaction(match.group(), m["type"])
            finding.redacted_text = redacted
            findings.append(finding)
            
            # Apply redaction to sanitized output
            if self.mode == DLPMode.REDACTION:
                # Adjust for previous redactions
                start = match.start() - offset
                end = match.end() - offset
                sanitized = sanitized[:start] + redacted + sanitized[end:]
                offset += (match.end() - match.start()) - len(redacted)
        
        # Check for critical findings that should block
        was_blocked = False
        block_reason = ""
        
        if self.mode == DLPMode.BLOCK:
            critical = any(f.sensitivity == SensitivityLevel.CRITICAL for f in findings)
            high_count = sum(1 for f in findings if f.sensitivity == SensitivityLevel.HIGH)
            
            if critical or high_count >= 3:
                was_blocked = True
                block_reason = f"DLP violation: {len(findings)} sensitive items detected"
        
        return DLPReport(
            original_length=len(output),
            sanitized_length=len(sanitized),
            findings=findings,
            was_blocked=was_blocked,
            block_reason=block_reason,
            redaction_count=len(findings),
            mode=self.mode
        )
    
    def _is_in_code_block(self, text: str, position: int) -> bool:
        """Check if position is inside a markdown code block"""
        # Simple check for code blocks
        before = text[:position]
        code_starts = before.count('```')
        return code_starts % 2 == 1
    
    def _generate_redaction(self, original: str, detection_type: str) -> str:
        """Generate appropriate redaction text"""
        if len(original) <= 4:
            return "****"
        
        # Keep first and last character, redact middle
        if len(original) <= 10:
            return original[0] + "***" + original[-1]
        
        # For longer text, show prefix and suffix
        prefix = original[:2]
        suffix = original[-2:]
        return f"{prefix}****{suffix}"
    
    def scan_and_process(self, output: str) -> Tuple[str, DLPReport]:
        """
        Scan and process output, returning sanitized text and report
        
        Returns:
            (sanitized_text, dlp_report)
        """
        report = self.scan(output)
        
        if report.was_blocked:
            return "[OUTPUT BLOCKED - SENSITIVE DATA DETECTED]", report
        
        if self.mode == DLPMode.REDACTION:
            # Re-scan with redaction
            report = self.scan(output)
            # Apply redactions by position
            sanitized = output
            offset = 0
            for finding in sorted(report.findings, key=lambda f: f.position_start):
                start = finding.position_start - offset
                end = finding.position_end - offset
                sanitized = sanitized[:start] + finding.redacted_text + sanitized[end:]
                offset += (finding.position_end - finding.position_start) - len(finding.redacted_text)
            return sanitized, report
        
        return output, report


class URLValidator:
    """Validate URLs against allowlists/blocklists"""
    
    def __init__(self, allowed_domains: List[str] = None, 
                 blocked_domains: List[str] = None):
        self.allowed = allowed_domains or []
        self.blocked = blocked_domains or []
    
    def is_allowed(self, url: str) -> Tuple[bool, str]:
        """Check if URL is allowed"""
        import fnmatch
        
        # Extract domain
        domain_match = re.search(r'https?://([^/]+)', url, re.IGNORECASE)
        if not domain_match:
            return False, "Invalid URL format"
        
        domain = domain_match.group(1).lower()
        
        # Check blocklist first
        for blocked in self.blocked:
            if fnmatch.fnmatch(domain, blocked.lower()):
                return False, f"Domain blocked: {domain}"
        
        # Check allowlist (if set)
        if self.allowed:
            allowed = False
            for pattern in self.allowed:
                if fnmatch.fnmatch(domain, pattern.lower()):
                    allowed = True
                    break
            if not allowed:
                return False, f"Domain not in allowlist: {domain}"
        
        return True, "Allowed"


# Convenience function
def scan_output(text: str, mode: DLPMode = DLPMode.REDACTION) -> Tuple[str, DLPReport]:
    """Quick scan function"""
    dlp = OutputDLP(mode=mode)
    return dlp.scan_and_process(text)