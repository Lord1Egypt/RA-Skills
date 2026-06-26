"""
ClawScan - OpenClaw Skill Security Scanner
Static + Dynamic analysis for OpenClaw Skills
"""

import ast
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class RiskLevel(Enum):
    HIGH = "high"      # 🔴 Network, filesystem write, env vars
    MEDIUM = "medium"  # 🟡 Subprocess, imports
    LOW = "low"        # 🟢 Pure computation
    UNKNOWN = "unknown"


@dataclass
class Finding:
    """Single security finding"""
    level: RiskLevel
    category: str       # network, filesystem, crypto, etc.
    description: str
    file: str
    line: int
    code_snippet: str = ""
    confidence: float = 1.0  # 0.0-1.0


@dataclass  
class ScanResult:
    """Complete scan result for a Skill"""
    skill_name: str
    skill_path: Path
    overall_risk: RiskLevel
    findings: List[Finding] = field(default_factory=list)
    scan_duration_ms: float = 0.0
    files_scanned: int = 0
    
    def summary(self) -> Dict:
        """Generate summary dict"""
        high = sum(1 for f in self.findings if f.level == RiskLevel.HIGH)
        medium = sum(1 for f in self.findings if f.level == RiskLevel.MEDIUM)
        low = sum(1 for f in self.findings if f.level == RiskLevel.LOW)
        
        return {
            "skill": self.skill_name,
            "risk_level": self.overall_risk.value,
            "total_findings": len(self.findings),
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low,
            "files_scanned": self.files_scanned,
        }
