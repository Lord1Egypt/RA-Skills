"""
Scanner - Main orchestration class
"""

import time
from pathlib import Path
from typing import List, Optional

from core.models import Finding, RiskLevel, ScanResult
from core.static_analyzer import StaticAnalyzer
from core.dynamic_tracer import DynamicTracer
from core.risk_engine import RiskEngine


class Scanner:
    """Main scanner that orchestrates static and dynamic analysis"""
    
    def __init__(self, enable_dynamic: bool = True):
        self.static_analyzer = StaticAnalyzer()
        self.dynamic_tracer = DynamicTracer() if enable_dynamic else None
        self.risk_engine = RiskEngine()
        self.enable_dynamic = enable_dynamic
    
    def scan_skill(self, skill_path: Path, skill_name: Optional[str] = None) -> ScanResult:
        """
        Scan a Skill directory or file.
        
        Args:
            skill_path: Path to Skill directory or Python file
            skill_name: Optional name override
        """
        start_time = time.time()
        
        if skill_name is None:
            skill_name = skill_path.name
        
        all_findings: List[Finding] = []
        files_scanned = 0
        
        # Collect all Python files to scan
        if skill_path.is_file() and skill_path.suffix == ".py":
            py_files = [skill_path]
        elif skill_path.is_dir():
            py_files = list(skill_path.rglob("*.py"))
            # Also check for SKILL.md for metadata
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                py_files.append(skill_md)  # Will be ignored by analyzer but counted
        else:
            py_files = []
        
        # Scan each Python file
        for py_file in py_files:
            if py_file.suffix != ".py":
                continue
            
            files_scanned += 1
            
            # Static analysis
            static_findings = self.static_analyzer.analyze_file(py_file)
            all_findings.extend(static_findings)
            
            # Dynamic analysis (if enabled)
            if self.enable_dynamic and self.dynamic_tracer:
                try:
                    code = py_file.read_text(encoding="utf-8", errors="ignore")
                    dynamic_findings = self.dynamic_tracer.analyze(code, py_file)
                    all_findings.extend(dynamic_findings)
                except Exception:
                    # Dynamic analysis failure shouldn't stop the scan
                    pass
        
        # Calculate overall risk
        overall_risk = self.risk_engine.calculate(all_findings, skill_name)
        
        # Deduplicate findings (same file, line, category)
        unique_findings = self._deduplicate(all_findings)
        
        scan_duration = (time.time() - start_time) * 1000
        
        return ScanResult(
            skill_name=skill_name,
            skill_path=skill_path,
            overall_risk=overall_risk,
            findings=unique_findings,
            scan_duration_ms=scan_duration,
            files_scanned=files_scanned,
        )
    
    def _deduplicate(self, findings: List[Finding]) -> List[Finding]:
        """Remove duplicate findings"""
        seen = set()
        unique = []
        
        for f in findings:
            key = (f.file, f.line, f.category, f.description[:50])
            if key not in seen:
                seen.add(key)
                unique.append(f)
        
        return unique
