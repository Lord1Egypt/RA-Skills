"""Supply Chain Security Scanner - Protection against Data Poisoning
Defense against:
- Training data poisoning attacks (DeepMind $60 attack)
- Model file tampering
- Malicious fine-tuning data
- Backdoor injections
"""

import hashlib
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from pathlib import Path
import zipfile
import tarfile


class RiskLevel(Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CheckType(Enum):
    INTEGRITY = "integrity"
    PROVENANCE = "provenance"
    ANOMALY = "anomaly"
    MALWARE = "malware"
    BACKDOOR = "backdoor"


@dataclass
class SupplyChainFinding:
    """Single supply chain security finding"""
    check_type: CheckType
    risk_level: RiskLevel
    component: str
    description: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    remediation: str = ""


@dataclass
class SupplyChainReport:
    """Complete supply chain security report"""
    overall_risk: RiskLevel
    component_count: int
    findings: List[SupplyChainFinding] = field(default_factory=list)
    integrity_hash: str = ""
    check_timestamp: str = ""
    
    def get_high_severity(self) -> List[SupplyChainFinding]:
        return [f for f in self.findings if f.risk_level in 
                [RiskLevel.HIGH, RiskLevel.CRITICAL]]


class SupplyChainScanner:
    """Main supply chain security scanner"""
    
    def __init__(self, trusted_hashes: Optional[Dict[str, str]] = None):
        self.integrity_checker = ModelIntegrityChecker(trusted_hashes)
        self.provenance_checker = TrainingDataProvenance()
    
    def scan_skill_code(self, code: str) -> Dict[str, Any]:
        """Scan skill code for malicious patterns"""
        indicators = []
        
        # Check for suspicious imports
        suspicious_patterns = [
            (r'import\s+os\s*\n', "OS module import - check for file system access", RiskLevel.MEDIUM),
            (r'import\s+subprocess', "Subprocess import - potential command execution", RiskLevel.HIGH),
            (r'import\s+socket', "Socket import - potential network access", RiskLevel.MEDIUM),
            (r'requests\.post\s*\(', "HTTP POST request - potential data exfiltration", RiskLevel.HIGH),
            (r'urllib\.request', "URL request - potential network access", RiskLevel.MEDIUM),
            (r'os\.environ|os\.getenv|environ\[', "Environment variable access - potential secret theft", RiskLevel.CRITICAL),
            (r'exec\s*\(|eval\s*\(', "Dynamic code execution - dangerous", RiskLevel.CRITICAL),
        ]
        
        for pattern, description, level in suspicious_patterns:
            if re.search(pattern, code):
                indicators.append(SupplyChainFinding(
                    check_type=CheckType.MALWARE,
                    risk_level=level,
                    component="skill_code",
                    description=description,
                    evidence={"pattern": pattern}
                ))
        
        # Determine overall risk
        critical_count = sum(1 for i in indicators if i.risk_level == RiskLevel.CRITICAL)
        high_count = sum(1 for i in indicators if i.risk_level == RiskLevel.HIGH)
        
        if critical_count > 0:
            overall_risk = RiskLevel.CRITICAL
        elif high_count > 0:
            overall_risk = RiskLevel.HIGH
        elif indicators:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.SAFE
        
        return {
            "is_malicious": overall_risk in [RiskLevel.CRITICAL, RiskLevel.HIGH],
            "threats": indicators,
            "risk_level": overall_risk,
            "scan_timestamp": time.time()
        }
    
    def scan_model_file(self, filepath: str, expected_hash: Optional[str] = None) -> SupplyChainReport:
        """Scan a model file for integrity issues"""
        integrity_result = self.integrity_checker.verify_integrity(filepath, expected_hash)
        
        findings = [
            SupplyChainFinding(
                check_type=f["check_type"],
                risk_level=f["risk_level"],
                component=f["component"],
                description=f["description"],
                evidence=f.get("evidence", {})
            )
            for f in integrity_result.get("findings", [])
        ]
        
        overall_risk = RiskLevel.CRITICAL if findings else RiskLevel.SAFE
        
        return SupplyChainReport(
            overall_risk=overall_risk,
            component_count=1,
            findings=findings,
            integrity_hash=integrity_result.get("hash", ""),
            check_timestamp=str(time.time())
        )


class ModelIntegrityChecker:
    """Verify model file integrity and signatures"""
    
    def __init__(self, trusted_hashes: Optional[Dict[str, str]] = None):
        self.trusted_hashes = trusted_hashes or {}
        self.known_vulnerable_versions = self._load_vulnerable_versions()
    
    def _load_vulnerable_versions(self) -> Set[str]:
        """Load known vulnerable model versions"""
        return {
            "transformers-4.20.0-cve-2022-xxxxx",
            # Add known vulnerabilities here
        }
    
    def compute_hash(self, filepath: str, algorithm: str = "sha256") -> str:
        """Compute file hash"""
        hasher = hashlib.sha256() if algorithm == "sha256" else hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def verify_integrity(self, filepath: str, expected_hash: Optional[str] = None) -> Dict[str, Any]:
        """Verify model file integrity"""
        findings = []
        
        # Check file exists
        if not os.path.exists(filepath):
            return {"verified": False, "findings": [{
                "check_type": CheckType.INTEGRITY,
                "risk_level": RiskLevel.CRITICAL,
                "component": filepath,
                "description": "Model file not found"
            }]}
        
        # Compute actual hash
        actual_hash = self.compute_hash(filepath)
        
        # Compare with expected
        if expected_hash:
            if actual_hash != expected_hash:
                findings.append({
                    "check_type": CheckType.INTEGRITY,
                    "risk_level": RiskLevel.CRITICAL,
                    "component": filepath,
                    "description": f"Hash mismatch! Expected: {expected_hash[:16]}..., Got: {actual_hash[:16]}..."
                })
        
        # Check against known trusted hashes
        if filepath in self.trusted_hashes:
            if actual_hash != self.trusted_hashes[filepath]:
                findings.append({
                    "check_type": CheckType.INTEGRITY,
                    "risk_level": RiskLevel.CRITICAL,
                    "component": filepath,
                    "description": "File hash does not match trusted version"
                })
        
        return {
            "verified": len(findings) == 0,
            "hash": actual_hash,
            "findings": findings
        }


class TrainingDataProvenance:
    """Track and validate training data provenance"""
    
    SUSPICIOUS_DATA_SOURCES = [
        "unknown", 
        "unverified",
        "crowdsourced-unvetted",
        "scraped-public",
    ]
    
    def __init__(self):
        self.dataset_metadata = {}
    
    def validate_dataset(self, dataset_path: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Validate training dataset security"""
        findings = []
        
        # Check dataset metadata
        meta = metadata or self._extract_metadata(dataset_path)
        
        # Verify source
        source = meta.get("source", "unknown")
        if source in self.SUSPICIOUS_DATA_SOURCES:
            findings.append({
                "check_type": CheckType.PROVENANCE,
                "risk_level": RiskLevel.HIGH,
                "component": dataset_path,
                "description": f"Dataset from suspicious source: {source}"
            })
        
        # Check for data poisoning indicators
        poison_indicators = self._check_poisoning_indicators(dataset_path)
        for indicator in poison_indicators:
            findings.append({
                "check_type": CheckType.ANOMALY,
                "risk_level": indicator["level"],
                "component": dataset_path,
                "description": indicator["description"],
                "evidence": indicator["evidence"]
            })
        
        return {
            "valid": len(findings) == 0,
            "findings": findings,
            "metadata": meta
        }
    
    def _extract_metadata(self, dataset_path: str) -> Dict[str, Any]:
        """Extract metadata from dataset"""
        meta = {
            "path": dataset_path,
            "size": os.path.getsize(dataset_path) if os.path.exists(dataset_path) else 0,
            "source": "unknown"
        }
        
        # Try to read accompanying metadata file
        meta_path = dataset_path + ".json"
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    meta.update(json.load(f))
            except:
                pass
        
        return meta
    
    def _check_poisoning_indicators(self, dataset_path: str) -> List[Dict]:
        """Check for data poisoning indicators"""
        indicators = []
        
        # If it's a text file, scan for suspicious patterns
        if dataset_path.endswith(('.txt', '.json', '.jsonl', '.csv')):
            try:
                with open(dataset_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Check for known poison patterns
                poison_patterns = [
                    (r'(?i)ignore\s+previous\s+instruction', "Potential prompt injection training data"),
                    (r'(?i)jailbreak\s+success', "Jailbreak training attempt"),
                    (r'(?i)system:\s*override', "System override training data"),
                ]
                
                for pattern, description in poison_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        indicators.append({
                            "level": RiskLevel.CRITICAL,
                            "description": description,
                            "evidence": {"matches": len(matches), "sample": matches[0][:50]}
                        })
                        
            except Exception as e:
                indicators.append({
                    "level": RiskLevel.MEDIUM,
                    "description": f"Could not analyze dataset: {str(e)}",
                    "evidence": {"error": str(e)}
                })
        
        return indicators
    
    def scan_skill_code(self, code: str) -> "ScanResult":
        """Scan skill code for malicious patterns"""
        indicators = []
        
        # Check for suspicious imports
        suspicious_imports = [
            (r'import\s+os\s*\n', "OS module import - check for file system access"),
            (r'import\s+subprocess', "Subprocess import - potential command execution"),
            (r'import\s+socket', "Socket import - potential network access"),
            (r'requests\.post\s*\(', "HTTP POST request - potential data exfiltration"),
            (r'urllib\.request', "URL request - potential network access"),
        ]
        
        for pattern, description in suspicious_imports:
            if re.search(pattern, code):
                indicators.append({
                    "level": RiskLevel.HIGH,
                    "description": description,
                    "evidence": {"pattern": pattern}
                })
        
        # Check for env var access
        if re.search(r'os\.environ|os\.getenv|environ\[', code):
            indicators.append({
                "level": RiskLevel.CRITICAL,
                "description": "Environment variable access - potential secret theft",
                "evidence": {"pattern": "os.environ"}
            })
        
        # Determine overall risk
        critical_count = sum(1 for i in indicators if i["level"] == RiskLevel.CRITICAL)
        high_count = sum(1 for i in indicators if i["level"] == RiskLevel.HIGH)
        
        if critical_count > 0:
            overall_risk = RiskLevel.CRITICAL
        elif high_count > 0:
            overall_risk = RiskLevel.HIGH
        elif indicators:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW
        
        return ScanResult(
            is_malicious=overall_risk in [RiskLevel.CRITICAL, RiskLevel.HIGH],
            threats=indicators,
            risk_level=overall_risk,
            scan_timestamp=time.time()
        )


@dataclass
class ScanResult:
    """Supply chain scan result"""
    is_malicious: bool
    threats: list
    risk_level: RiskLevel
    scan_timestamp: float