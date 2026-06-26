"""
Advanced Features Module
Features that make ClawScan worth paying for
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Set

from core.models import Finding, RiskLevel


@dataclass
class DependencyRisk:
    """Risk assessment for a Python dependency"""
    package: str
    version: Optional[str]
    risk_level: RiskLevel
    reasons: List[str] = field(default_factory=list)


@dataclass
class ScanReport:
    """Comprehensive scan report"""
    skill_name: str
    overall_risk: RiskLevel
    summary: str
    findings: List[Finding]
    dependencies: List[DependencyRisk]
    recommendations: List[str]
    scan_timestamp: str


class AdvancedAnalyzer:
    """Advanced analysis features for paid users"""
    
    # Known malicious or risky packages
    RISKY_PACKAGES = {
        "urllib3": RiskLevel.LOW,  # Generally safe but can be misused
        "requests": RiskLevel.LOW,
        "pycryptodome": RiskLevel.MEDIUM,  # Crypto can be legit or malicious
        "cryptography": RiskLevel.MEDIUM,
        "paramiko": RiskLevel.MEDIUM,  # SSH can be risky
        "psutil": RiskLevel.MEDIUM,  # System access
        "pyautogui": RiskLevel.HIGH,  # Can control input/output
        "pynput": RiskLevel.HIGH,  # Keylogger potential
        "mss": RiskLevel.HIGH,  # Screenshot capability
        "pyperclip": RiskLevel.MEDIUM,  # Clipboard access
        "browser-cookie3": RiskLevel.HIGH,  # Steals browser cookies
        "pycryptodomex": RiskLevel.MEDIUM,
        "websockets": RiskLevel.MEDIUM,  # Real-time communication
        "aiohttp": RiskLevel.LOW,
    }
    
    def analyze_dependencies(self, skill_path: Path) -> List[DependencyRisk]:
        """
        Analyze requirements.txt or pyproject.toml for risky dependencies.
        """
        risks = []
        
        # Check requirements.txt
        req_file = skill_path / "requirements.txt"
        if req_file.exists():
            deps = self._parse_requirements(req_file)
            for pkg, version in deps:
                risk = self._assess_package(pkg, version)
                if risk:
                    risks.append(risk)
        
        # Check pyproject.toml
        pyproject = skill_path / "pyproject.toml"
        if pyproject.exists():
            deps = self._parse_pyproject(pyproject)
            for pkg, version in deps:
                risk = self._assess_package(pkg, version)
                if risk:
                    risks.append(risk)
        
        return risks
    
    def _parse_requirements(self, req_file: Path) -> List[tuple]:
        """Parse requirements.txt"""
        deps = []
        try:
            content = req_file.read_text()
            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Handle different formats: pkg==1.0, pkg>=1.0, pkg
                match = re.match(r'^([a-zA-Z0-9_-]+)([<>=!~]+.+)?', line)
                if match:
                    pkg = match.group(1).lower()
                    version = match.group(2)
                    deps.append((pkg, version))
        except:
            pass
        return deps
    
    def _parse_pyproject(self, pyproject: Path) -> List[tuple]:
        """Parse pyproject.toml for dependencies"""
        deps = []
        try:
            import tomllib
            content = pyproject.read_text()
            data = tomllib.loads(content)
            
            project = data.get("project", {})
            dependencies = project.get("dependencies", [])
            
            for dep in dependencies:
                match = re.match(r'^([a-zA-Z0-9_-]+)([<>=!~]+.+)?', dep)
                if match:
                    pkg = match.group(1).lower()
                    version = match.group(2)
                    deps.append((pkg, version))
        except:
            pass
        return deps
    
    def _assess_package(self, package: str, version: Optional[str]) -> Optional[DependencyRisk]:
        """Assess risk of a single package"""
        normalized = package.lower().replace("-", "_").replace(".", "_")
        
        # Check known risky packages
        for risky_pkg, level in self.RISKY_PACKAGES.items():
            if normalized == risky_pkg.lower() or normalized.startswith(risky_pkg.lower() + "["):
                reasons = [f"Known {level.value}-risk package"]
                
                if level == RiskLevel.HIGH:
                    reasons.append("May access sensitive system resources")
                elif level == RiskLevel.MEDIUM:
                    reasons.append("Has elevated system access capabilities")
                
                return DependencyRisk(
                    package=package,
                    version=version,
                    risk_level=level,
                    reasons=reasons
                )
        
        # Check for suspicious patterns in package names
        suspicious_patterns = [
            ("crypto", "Cryptocurrency-related package"),
            ("wallet", "Potential wallet access"),
            ("keylog", "Potential keylogger"),
            ("steal", "Suspicious naming"),
            ("exfil", "Potential data exfiltration"),
        ]
        
        for pattern, reason in suspicious_patterns:
            if pattern in normalized:
                return DependencyRisk(
                    package=package,
                    version=version,
                    risk_level=RiskLevel.HIGH,
                    reasons=[f"Suspicious name pattern: {reason}"]
                )
        
        return None
    
    def generate_report(self, skill_path: Path, findings: List[Finding], 
                       skill_name: str) -> ScanReport:
        """Generate comprehensive scan report"""
        from datetime import datetime
        from core.risk_engine import RiskEngine
        
        # Get overall risk
        engine = RiskEngine()
        overall_risk = engine.calculate(findings, skill_name)
        
        # Analyze dependencies
        deps = self.analyze_dependencies(skill_path)
        
        # Get recommendations
        result = ScanResult(
            skill_name=skill_name,
            skill_path=skill_path,
            overall_risk=overall_risk,
            findings=findings,
            scan_duration_ms=0,
            files_scanned=0
        )
        recommendations = engine.generate_recommendations(result)
        
        # Generate summary
        summary = self._generate_summary(skill_name, overall_risk, findings, deps)
        
        return ScanReport(
            skill_name=skill_name,
            overall_risk=overall_risk,
            summary=summary,
            findings=findings,
            dependencies=deps,
            recommendations=recommendations,
            scan_timestamp=datetime.now().isoformat()
        )
    
    def _generate_summary(self, skill_name: str, risk: RiskLevel, 
                         findings: List[Finding], deps: List[DependencyRisk]) -> str:
        """Generate human-readable summary"""
        high = sum(1 for f in findings if f.level == RiskLevel.HIGH)
        medium = sum(1 for f in findings if f.level == RiskLevel.MEDIUM)
        low = sum(1 for f in findings if f.level == RiskLevel.LOW)
        
        summary = f"Scan of '{skill_name}' found "
        
        if risk == RiskLevel.HIGH:
            summary += f"{high} high-risk issues. "
            summary += "This Skill has dangerous capabilities and should be reviewed carefully."
        elif risk == RiskLevel.MEDIUM:
            summary += f"{medium} medium-risk issues. "
            summary += "Some capabilities may pose security concerns."
        else:
            summary += "no significant security risks. "
            summary += "This Skill appears safe to use."
        
        if deps:
            risky_deps = sum(1 for d in deps if d.risk_level in (RiskLevel.HIGH, RiskLevel.MEDIUM))
            if risky_deps > 0:
                summary += f" Additionally, {risky_deps} dependencies were flagged as potentially risky."
        
        return summary


# Import here to avoid circular dependency
from core.models import ScanResult
