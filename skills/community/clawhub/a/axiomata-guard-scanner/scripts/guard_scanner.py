#!/usr/bin/env python3
"""
Axiomata Guard Scanner v1.0
Universal OpenClaw skill security scanner.

Impersonal, universal security tool for any OpenClaw agent.

Usage:
    python3 guard_scanner.py --file <skill-path>
    python3 guard_scanner.py --code "<skill code>"
    python3 guard_scanner.py --file <skill-path> --json
"""

import sys
import os
import re
import json
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any


# ============================================================
# VAX-001: ClawHub Known Malicious Patterns
# ============================================================
class VAX001Scanner:
    """VAX-001: ClawHub known malicious patterns"""
    
    MALICIOUS_PATTERNS = [
        (r"openclawcli\.zip", "MALICIOUS_BINARY", "GitHub ZIP download — malware"),
        (r"glot\.io/snippets/", "RCE_VIA_GLOT", "Remote code execution via glot.io"),
        (r"github\.com.*releases.*download", "GITHUB_MALWARE", "Malware via GitHub releases"),
        (r"download.*\.zip.*password", "PASSWORD_PROTECTED_ZIP", "Encrypted malware archive"),
    ]
    
    RISK_WEIGHTS = {
        "MALICIOUS_BINARY": 90,
        "RCE_VIA_GLOT": 95,
        "GITHUB_MALWARE": 80,
        "PASSWORD_PROTECTED_ZIP": 70,
    }
    
    @classmethod
    def scan(cls, code: str, skill_name: str = "unknown") -> Dict:
        findings = []
        total_score = 0
        
        for pattern, vuln_type, description in cls.MALICIOUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append({
                    "pattern": pattern,
                    "type": vuln_type,
                    "description": description,
                })
                total_score += cls.RISK_WEIGHTS.get(vuln_type, 50)
        
        threat_level = "CLEAN"
        if total_score >= 80:
            threat_level = "CRITICAL"
        elif total_score >= 50:
            threat_level = "HIGH"
        elif total_score >= 20:
            threat_level = "MEDIUM"
        
        return {
            "vaccine": "VAX-001",
            "vaccine_name": "ClawHub Malicious Patterns",
            "skill_name": skill_name,
            "threat_level": threat_level,
            "score": min(total_score, 100),
            "findings": findings,
            "verdict": "BLOCK" if threat_level in ["HIGH", "CRITICAL"] else "APPROVE" if threat_level == "CLEAN" else "WARN",
        }


# ============================================================
# VAX-027: Data Exfiltration & C2 Infrastructure
# ============================================================
class VAX027Scanner:
    """VAX-027: C2 and data exfiltration detection"""
    
    C2_PATTERNS = [
        (r"dns\.lookup\s*\(\s*['\"]evil", "C2_DNS", "Malicious DNS lookup"),
        (r"duckdns\.org|noip\.com|dyndns\.com", "C2_DYNAMIC_DNS", "Dynamic DNS — C2"),
        (r"discord\.com/api/webhooks", "EXFIL_DISCORD", "Discord webhook exfiltration"),
        (r"telegram\.org/api/webhooks", "EXFIL_TELEGRAM", "Telegram webhook exfiltration"),
        (r"bit\.ly|tinyurl\.com|goo\.gl", "EXFIL_SHORT_URL", "Short URL exfiltration"),
        (r"curl.*\|.*bash", "RCE_PIPE", "Remote code execution via pipe"),
        (r"eval\s*\(|base64_decode\s*\(", "RCE_EVAL", "Code injection via eval"),
        (r"subprocess.*shell\s*=\s*True", "RCE_SHELL", "Shell injection risk"),
    ]
    
    @classmethod
    def scan(cls, code: str, skill_name: str = "unknown") -> Dict:
        findings = []
        total_score = 0
        
        for pattern, vuln_type, description in cls.C2_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append({
                    "pattern": pattern,
                    "type": vuln_type,
                    "description": description,
                })
                if "C2" in vuln_type:
                    total_score += 40
                elif "EXFIL" in vuln_type:
                    total_score += 30
                elif "RCE" in vuln_type:
                    total_score += 50
        
        threat_level = "CLEAN"
        if total_score >= 80:
            threat_level = "CRITICAL"
        elif total_score >= 50:
            threat_level = "HIGH"
        elif total_score >= 20:
            threat_level = "MEDIUM"
        
        return {
            "vaccine": "VAX-027",
            "vaccine_name": "C2 & Data Exfiltration",
            "skill_name": skill_name,
            "threat_level": threat_level,
            "score": min(total_score, 100),
            "findings": findings,
            "verdict": "BLOCK" if threat_level in ["HIGH", "CRITICAL"] else "APPROVE" if threat_level == "CLEAN" else "WARN",
        }


# ============================================================
# VAX-029: Rootkit & Bootkit Detection
# ============================================================
class VAX029Scanner:
    """VAX-029: Rootkit and bootkit detection"""
    
    ROOTKIT_PATTERNS = [
        (r"PsActiveProcessHead", "ROOTKIT_WIN32", "Windows kernel manipulation"),
        (r"KeServiceDescriptorTable", "ROOTKIT_SYSENTER", "System call table hook"),
        (r"UEFI|EFI.*inject|\.efi", "BOOTKIT_UEFI", "UEFI bootkit injection"),
        (r"AmsiScanBuffer.*=\s*0", "ROOTKIT_ANTIVIRUS", "AMSI bypass — malicious"),
        (r"NtLoadDriver", "ROOTKIT_DRIVER", "Driver loading vulnerability"),
        (r"Unlink.*Process", "ROOTKIT_DLLCONCEPT", "DLL unlinking technique"),
    ]
    
    @classmethod
    def scan(cls, code: str, skill_name: str = "unknown") -> Dict:
        findings = []
        total_score = 0
        
        for pattern, vuln_type, description in cls.ROOTKIT_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append({
                    "pattern": pattern,
                    "type": vuln_type,
                    "description": description,
                })
                total_score += 45
        
        threat_level = "CLEAN"
        if total_score >= 80:
            threat_level = "CRITICAL"
        elif total_score >= 50:
            threat_level = "HIGH"
        elif total_score >= 20:
            threat_level = "MEDIUM"
        
        return {
            "vaccine": "VAX-029",
            "vaccine_name": "Rootkit & Bootkit Detection",
            "skill_name": skill_name,
            "threat_level": threat_level,
            "score": min(total_score, 100),
            "findings": findings,
            "verdict": "BLOCK" if threat_level in ["HIGH", "CRITICAL"] else "APPROVE" if threat_level == "CLEAN" else "WARN",
        }


# ============================================================
# VAX-030: Package Ecosystem Attack Detection
# ============================================================
class VAX030Scanner:
    """VAX-030: Package ecosystem attack detection"""
    
    PKG_PATTERNS = [
        (r"pip install\s+--index-url.*trusted-host", "PKG_CONFUSION", "Package confusion attack"),
        (r"pip install\s+--extra-index-url", "PKG_CONFUSION", "Package confusion attack"),
        (r"requirements\.txt.*http://", "PKG_HTTP_REQS", "HTTP requirements — MITM risk"),
        (r"setup\.py.*http://|install_requires.*http://", "PKG_HTTP_SETUP", "HTTP setup — MITM risk"),
        (r"import\s+requests.*verify\s*=\s*False", "PKG_SSL_BYPASS", "SSL bypass — MITM risk"),
        (r"typosquat|typo squat|spell check", "PKG_TYPOSQUAT", "Typosquatting pattern"),
    ]
    
    @classmethod
    def scan(cls, code: str, skill_name: str = "unknown") -> Dict:
        findings = []
        total_score = 0
        
        for pattern, vuln_type, description in cls.PKG_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append({
                    "pattern": pattern,
                    "type": vuln_type,
                    "description": description,
                })
                total_score += 25
        
        threat_level = "CLEAN"
        if total_score >= 50:
            threat_level = "HIGH"
        elif total_score >= 20:
            threat_level = "MEDIUM"
        
        return {
            "vaccine": "VAX-030",
            "vaccine_name": "Package Ecosystem Attacks",
            "skill_name": skill_name,
            "threat_level": threat_level,
            "score": min(total_score, 100),
            "findings": findings,
            "verdict": "BLOCK" if threat_level == "HIGH" else "APPROVE" if threat_level == "CLEAN" else "WARN",
        }


# ============================================================
# UNIFIED SCANNER
# ============================================================
class GuardScanner:
    """Unified security scanner for OpenClaw skills"""
    
    def __init__(self, skill_code: str, skill_name: str = "unknown"):
        self.code = skill_code
        self.skill_name = skill_name
        self.results: Dict[str, Dict] = {}
        self.start_time = time.time()
    
    def scan_all(self) -> Dict:
        """Run all vaccines and aggregate results"""
        
        # VAX-001: ClawHub malicious patterns
        self.results["VAX-001"] = VAX001Scanner.scan(self.code, self.skill_name)
        
        # VAX-027: C2 & exfiltration
        self.results["VAX-027"] = VAX027Scanner.scan(self.code, self.skill_name)
        
        # VAX-029: Rootkit & bootkit
        self.results["VAX-029"] = VAX029Scanner.scan(self.code, self.skill_name)
        
        # VAX-030: Package ecosystem
        self.results["VAX-030"] = VAX030Scanner.scan(self.code, self.skill_name)
        
        # VAX-028: Cross-vector correlation (simplified)
        self.results["VAX-028"] = self._cross_vector_scan()
        
        return self._build_report()
    
    def _cross_vector_scan(self) -> Dict:
        """VAX-028: Correlate findings from other vaccines"""
        triggered = []
        for vid, result in self.results.items():
            if vid == "VAX-028":
                continue
            if result.get("threat_level") in ["HIGH", "CRITICAL"]:
                triggered.append(vid)
        
        # Multiple triggers = higher risk
        score = len(triggered) * 20
        threat_level = "CLEAN"
        if len(triggered) >= 3:
            threat_level = "CRITICAL"
            score = 100
        elif len(triggered) == 2:
            threat_level = "HIGH"
            score = 70
        elif len(triggered) == 1:
            threat_level = "MEDIUM"
            score = 40
        
        return {
            "vaccine": "VAX-028",
            "vaccine_name": "Cross-Vector Attack Chain",
            "threat_level": threat_level,
            "score": score,
            "triggered": triggered,
            "verdict": "BLOCK" if threat_level in ["HIGH", "CRITICAL"] else "APPROVE"
        }
    
    def _build_report(self) -> Dict:
        """Aggregate all vaccine results into unified report"""
        elapsed = round((time.time() - self.start_time) * 1000, 1)
        
        all_scores = []
        triggered = []
        critical_count = 0
        high_count = 0
        
        for vid, result in self.results.items():
            score = result.get("score", 0)
            level = result.get("threat_level", "CLEAN")
            all_scores.append(score)
            
            if level in ["HIGH", "CRITICAL"]:
                triggered.append({
                    "vaccine": vid,
                    "level": level,
                    "score": score,
                    "findings": result.get("findings", [])
                })
            
            if level == "CRITICAL":
                critical_count += 1
            if level == "HIGH":
                high_count += 1
        
        # Global score
        base_score = max(all_scores) if all_scores else 0
        multi_bonus = len([s for s in all_scores if s >= 20]) * 10
        total_score = min(base_score + multi_bonus, 300)
        
        # Global threat level
        if critical_count >= 2:
            global_level = "CRITICAL"
        elif critical_count >= 1 or high_count >= 2:
            global_level = "HIGH"
        elif high_count >= 1:
            global_level = "MEDIUM"
        elif any(s >= 20 for s in all_scores):
            global_level = "LOW"
        else:
            global_level = "CLEAN"
        
        # Decision
        if global_level == "CRITICAL":
            decision = f"ISOLATE — {critical_count} CRITICAL, {high_count} HIGH"
            action = "ISOLATE"
        elif global_level == "HIGH":
            decision = f"BLOCK — {high_count} HIGH triggers"
            action = "BLOCK"
        elif global_level == "MEDIUM":
            decision = f"WARN — manual review required"
            action = "WARN"
        elif global_level == "LOW":
            decision = "APPROVE with monitoring"
            action = "MONITOR"
        else:
            decision = "APPROVE — no threats detected"
            action = "APPROVE"
        
        return {
            "scanner": "Axiomata Guard Scanner",
            "version": "1.0.0",
            "skill_name": self.skill_name,
            "scan_time_ms": elapsed,
            "global_threat_level": global_level,
            "global_score": total_score,
            "decision": decision,
            "action": action,
            "triggered_vaccines": triggered,
            "all_results": self.results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def main():
    parser = argparse.ArgumentParser(description="Axiomata Guard Scanner v1.0")
    parser.add_argument("--file", "-f", help="Path to skill file or directory")
    parser.add_argument("--code", "-c", help="Skill code directly")
    parser.add_argument("--name", "-n", default="unknown", help="Skill name")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output only")
    
    args = parser.parse_args()
    
    if args.file:
        skill_path = Path(args.file)
        if skill_path.is_dir():
            skill_path = skill_path / "SKILL.md"
        try:
            with open(skill_path) as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {skill_path}", file=sys.stderr)
            return 1
        skill_name = skill_path.parent.name
    elif args.code:
        code = args.code
        skill_name = args.name
    else:
        parser.print_help()
        return 1
    
    scanner = GuardScanner(code, skill_name)
    report = scanner.scan_all()
    
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print_report(report)
    
    # Exit code based on threat level
    if report["global_threat_level"] == "CRITICAL":
        return 2
    elif report["global_threat_level"] == "HIGH":
        return 1
    return 0


def print_report(report: Dict):
    """Print human-readable report"""
    level_colors = {
        "CRITICAL": "\033[91m",
        "HIGH": "\033[95m",
        "MEDIUM": "\033[93m",
        "LOW": "\033[94m",
        "CLEAN": "\033[92m",
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    level = report["global_threat_level"]
    color = level_colors.get(level, "")
    
    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}{color}Axiomata Guard Scanner v1.0 — Security Report{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"Skill: {BOLD}{report['skill_name']}{RESET}")
    print(f"Scan time: {report['scan_time_ms']}ms")
    print()
    print(f"{BOLD}┌{'─' * 50}┐{RESET}")
    print(f"{BOLD}│{RESET} Global Threat: {color}{level.center(22)}{BOLD}│{RESET}")
    print(f"{BOLD}│{RESET} Score: {color}{str(report['global_score']).rjust(38)}{RESET}│{RESET}")
    print(f"{BOLD}└{'─' * 50}┘{RESET}")
    print()
    print(f"{BOLD}Decision:{RESET} {report['decision']}")
    print(f"{BOLD}Action:{RESET} {report['action']}")
    print()
    print(f"{BOLD}VACCINE RESULTS:{RESET}")
    
    for vid, result in report.get("all_results", {}).items():
        status = result.get("threat_level", "UNKNOWN")
        status_color = level_colors.get(status, "")
        score = result.get("score", 0)
        print(f"  {BOLD}{vid}{RESET}: {status_color}{status}{RESET} ({score})")
    
    if report.get("triggered_vaccines"):
        print()
        print(f"{BOLD}{'\033[91m'}TRIGGERED VACCINES:{RESET}")
        for t in report["triggered_vaccines"]:
            lvl_color = level_colors.get(t["level"], "")
            print(f"  {BOLD}{t['vaccine']}{RESET}: {lvl_color}{t['level']}{RESET} (score: {t['score']})")
            for finding in t.get("findings", [])[:3]:
                print(f"    - {finding.get('description', 'N/A')}")
    
    print()
    print(f"{BOLD}Scanned: {report['timestamp']}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")


if __name__ == "__main__":
    sys.exit(main())