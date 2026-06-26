"""Input Sanitizer - Defense against Prompt Injection attacks
OWASP LLM01:2025 Protection Layer

Blocks:
- Direct prompt injection patterns
- Hidden unicode attacks (zero-width spaces)
- Encoded payloads (base64, URL encoding)
- Instruction override attempts
"""

import re
import base64
import binascii
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import unicodedata


class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SanitizationFinding:
    """Single sanitization finding"""
    threat_type: str
    threat_level: ThreatLevel
    description: str
    original_snippet: str
    position: int
    sanitized_snippet: Optional[str] = None


@dataclass
class SanitizationReport:
    """Complete sanitization report"""
    original_length: int
    sanitized_length: int
    threat_level: ThreatLevel
    findings: List[SanitizationFinding] = field(default_factory=list)
    processing_time_ms: float = 0.0
    
    def has_critical(self) -> bool:
        return any(f.threat_level == ThreatLevel.CRITICAL for f in self.findings)
    
    def has_high(self) -> bool:
        return any(f.threat_level == ThreatLevel.HIGH for f in self.findings)


class InputSanitizer:
    """Input sanitization engine for AgentShield"""
    
    # Instruction override patterns (CRITICAL)
    OVERRIDE_PATTERNS = [
        (r'ignore\s+(all\s+)?previous\s+instructions?', ThreatLevel.CRITICAL),
        (r'disregard\s+(all\s+)?prior\s+instructions?', ThreatLevel.CRITICAL),
        (r'forget\s+(everything|all)\s+(you|your)', ThreatLevel.CRITICAL),
        (r'system\s*:\s*', ThreatLevel.CRITICAL),
        (r'you\s+are\s+now\s+a', ThreatLevel.HIGH),
        (r'new\s+role\s*:\s*', ThreatLevel.HIGH),
        (r'override\s+(safety|security|restrictions)', ThreatLevel.CRITICAL),
        (r'\[\[SYSTEM\]\]', ThreatLevel.CRITICAL),
        (r'<system>', ThreatLevel.CRITICAL),
        (r'<!--\s*system\s*-->', ThreatLevel.CRITICAL),
    ]
    
    # Markdown/HTML injection patterns
    MARKDOWN_PATTERNS = [
        (r'<!\[CDATA\[', ThreatLevel.HIGH),
        (r'<script[^>]*>', ThreatLevel.CRITICAL),
        (r'javascript:', ThreatLevel.HIGH),
        (r'on\w+\s*=', ThreatLevel.HIGH),
        (r'data:text/html', ThreatLevel.HIGH),
    ]
    
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for performance"""
        self._override_patterns = [
            (re.compile(pattern, re.IGNORECASE), level) 
            for pattern, level in self.OVERRIDE_PATTERNS
        ]
        self._markdown_patterns = [
            (re.compile(pattern, re.IGNORECASE), level)
            for pattern, level in self.MARKDOWN_PATTERNS
        ]
    
    def sanitize(self, text: str) -> Tuple[str, SanitizationReport]:
        """
        Main sanitization entry point
        
        Returns:
            (sanitized_text, report)
        """
        import time
        start = time.time()
        
        findings = []
        original = text
        
        # Step 1: Check for instruction overrides
        text, override_findings = self._sanitize_overrides(text)
        findings.extend(override_findings)
        
        # Step 2: Strip invisible unicode
        text, unicode_findings = self._sanitize_unicode(text)
        findings.extend(unicode_findings)
        
        # Step 3: Detect and flag encoded payloads
        text, encoding_findings = self._sanitize_encoding(text)
        findings.extend(encoding_findings)
        
        # Step 4: Clean markdown/HTML
        text, markdown_findings = self._sanitize_markdown(text)
        findings.extend(markdown_findings)
        
        # Determine overall threat level
        threat_level = self._calculate_threat_level(findings)
        
        elapsed = (time.time() - start) * 1000
        
        report = SanitizationReport(
            original_length=len(original),
            sanitized_length=len(text),
            threat_level=threat_level,
            findings=findings,
            processing_time_ms=elapsed
        )
        
        return text, report
    
    def _sanitize_overrides(self, text: str) -> Tuple[str, List[SanitizationFinding]]:
        """Detect and block instruction override attempts"""
        findings = []
        
        for pattern, level in self._override_patterns:
            for match in pattern.finditer(text):
                finding = SanitizationFinding(
                    threat_type="INSTRUCTION_OVERRIDE",
                    threat_level=level,
                    description=f"Potential instruction override detected: '{match.group()}'",
                    original_snippet=match.group(),
                    position=match.start(),
                    sanitized_snippet="[BLOCKED]"
                )
                findings.append(finding)
                
                # Block critical patterns by replacement
                if level == ThreatLevel.CRITICAL:
                    text = text[:match.start()] + "[BLOCKED_INSTRUCTION]" + text[match.end():]
        
        return text, findings
    
    def _sanitize_unicode(self, text: str) -> Tuple[str, List[SanitizationFinding]]:
        """Remove dangerous/invisible unicode characters"""
        findings = []
        
        # Characters to strip
        dangerous_chars = {
            '\u200b': "ZERO_WIDTH_SPACE",
            '\u200c': "ZERO_WIDTH_NON_JOINER", 
            '\u200d': "ZERO_WIDTH_JOINER",
            '\ufeff': "ZERO_WIDTH_NO_BREAK_SPACE",
            '\u202a': "LEFT_TO_RIGHT_EMBEDDING",
            '\u202b': "RIGHT_TO_LEFT_EMBEDDING",
            '\u202c': "POP_DIRECTIONAL_FORMATTING",
            '\u202d': "LEFT_TO_RIGHT_OVERRIDE",
            '\u202e': "RIGHT_TO_LEFT_OVERRIDE",
            '\u2060': "WORD_JOINER",
            '\u2061': "FUNCTION_APPLICATION",
            '\u2062': "INVISIBLE_TIMES",
            '\u2063': "INVISIBLE_SEPARATOR",
            '\u2064': "INVISIBLE_PLUS",
        }
        
        for char, name in dangerous_chars.items():
            if char in text:
                count = text.count(char)
                finding = SanitizationFinding(
                    threat_type="HIDDEN_UNICODE",
                    threat_level=ThreatLevel.HIGH,
                    description=f"Detected {count} instance(s) of {name}",
                    original_snippet=char,
                    position=text.find(char),
                    sanitized_snippet=""
                )
                findings.append(finding)
                text = text.replace(char, "")
        
        return text, findings
    
    def _sanitize_encoding(self, text: str) -> Tuple[str, List[SanitizationFinding]]:
        """Detect and handle encoded payloads"""
        findings = []
        
        # Base64 detection
        b64_pattern = re.compile(r'[A-Za-z0-9+/]{40,}={0,2}')
        
        for match in b64_pattern.finditer(text):
            snippet = match.group()
            try:
                decoded = base64.b64decode(snippet).decode('utf-8', errors='ignore')
                # Check if decoded content contains suspicious patterns
                if self._contains_suspicious_content(decoded):
                    finding = SanitizationFinding(
                        threat_type="ENCODED_PAYLOAD",
                        threat_level=ThreatLevel.HIGH,
                        description=f"Suspicious base64 encoded content detected",
                        original_snippet=snippet[:50],
                        position=match.start(),
                        sanitized_snippet="[ENCODED_CONTENT_BLOCKED]"
                    )
                    findings.append(finding)
                    if self.strict_mode:
                        text = text.replace(snippet, "[ENCODED_CONTENT_BLOCKED]")
            except:
                pass
        
        # URL-encoded detection
        url_pattern = re.compile(r'%[0-9A-Fa-f]{2}')
        url_matches = list(url_pattern.finditer(text))
        
        if len(url_matches) > 10:  # Threshold for URL encoding
            try:
                import urllib.parse
                decoded = urllib.parse.unquote(text)
                if self._contains_suspicious_content(decoded):
                    finding = SanitizationFinding(
                        threat_type="URL_ENCODED_PAYLOAD",
                        threat_level=ThreatLevel.MEDIUM,
                        description=f"Potential URL-encoded payload detected",
                        original_snippet=text[max(0, url_matches[0].start()-20):url_matches[0].start()+50],
                        position=url_matches[0].start()
                    )
                    findings.append(finding)
            except:
                pass
        
        return text, findings
    
    def _sanitize_markdown(self, text: str) -> Tuple[str, List[SanitizationFinding]]:
        """Clean potentially dangerous markdown/HTML constructs"""
        findings = []
        
        for pattern, level in self._markdown_patterns:
            for match in pattern.finditer(text):
                finding = SanitizationFinding(
                    threat_type="MARKDOWN_INJECTION",
                    threat_level=level,
                    description=f"Potentially dangerous markdown/HTML pattern detected",
                    original_snippet=match.group()[:50],
                    position=match.start(),
                    sanitized_snippet="[MARKDOWN_BLOCKED]"
                )
                findings.append(finding)
                
                if level == ThreatLevel.CRITICAL:
                    text = text.replace(match.group(), "[MARKDOWN_BLOCKED]")
        
        return text, findings
    
    def _contains_suspicious_content(self, text: str) -> bool:
        """Check if text contains suspicious patterns"""
        suspicious = [
            'ignore', 'system', 'instruction', 'override',
            '<script', 'javascript:', 'prompt', 'jailbreak'
        ]
        text_lower = text.lower()
        return any(s in text_lower for s in suspicious)
    
    def _calculate_threat_level(self, findings: List[SanitizationFinding]) -> ThreatLevel:
        """Determine overall threat level from findings"""
        if not findings:
            return ThreatLevel.LOW
        
        levels = [f.threat_level for f in findings]
        
        if ThreatLevel.CRITICAL in levels:
            return ThreatLevel.CRITICAL
        if ThreatLevel.HIGH in levels:
            return ThreatLevel.HIGH
        if ThreatLevel.MEDIUM in levels:
            return ThreatLevel.MEDIUM
        return ThreatLevel.LOW


# Convenience function
def sanitize_input(text: str, strict: bool = False) -> Tuple[str, SanitizationReport]:
    """Quick sanitize function"""
    sanitizer = InputSanitizer(strict_mode=strict)
    return sanitizer.sanitize(text)