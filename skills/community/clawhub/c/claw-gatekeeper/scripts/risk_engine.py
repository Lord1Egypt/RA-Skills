#!/usr/bin/env python3
"""
Claw-Gatekeeper Risk Assessment Engine
Analyzes operations and assigns risk scores for OpenClaw safety control

Merged from: SafeClaw (risk_analyzer.py) + Claw-Guardian (risk_engine.py)
Features:
- Comprehensive risk analysis for file, shell, network, and skill operations
- Configurable sensitivity via policy configuration
- Detailed risk reasoning and recommendations
"""

import re
import os
import json
import sys
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path


class RiskLevel(Enum):
    """Risk level classification"""
    CRITICAL = "CRITICAL"  # Score 80-100 - System-level danger
    HIGH = "HIGH"          # Score 60-79 - Sensitive operations
    MEDIUM = "MEDIUM"      # Score 30-59 - General risk
    LOW = "LOW"            # Score 0-29 - Safe operations
    
    def get_emoji(self) -> str:
        """Get emoji representation"""
        return {
            RiskLevel.CRITICAL: "🔴",
            RiskLevel.HIGH: "🟠",
            RiskLevel.MEDIUM: "🟡",
            RiskLevel.LOW: "🟢"
        }.get(self, "⚪")


@dataclass
class RiskAssessment:
    """Risk assessment result"""
    level: RiskLevel
    score: int
    reasons: List[str]
    recommendation: str
    requires_approval: bool
    operation_type: str
    operation_detail: str


class RiskEngine:
    """Core risk assessment engine with comprehensive detection capabilities"""
    
    # Sensitive paths that indicate high risk
    SENSITIVE_PATHS = [
        (r"^/etc/(passwd|shadow|hosts|ssh|sudoers)$", "System authentication file"),
        (r"^/etc/(fstab|crypttab)$", "System mount configuration"),
        (r"^~/.ssh/", "SSH keys and configuration"),
        (r"^~/.gnupg/", "GPG keys and configuration"),
        (r"^~/.aws/", "AWS credentials"),
        (r"^~/.azure/", "Azure credentials"),
        (r"^~/.kube/", "Kubernetes configuration"),
        (r"^~/.docker/", "Docker configuration"),
        (r".*\.env$", "Environment file with secrets"),
        (r".*\.env\.", "Environment file variant"),
        (r".*secret", "Secret file"),
        (r".*password", "Password file"),
        (r".*credential", "Credential file"),
        (r".*token", "Token file"),
        (r".*key\.json$", "JSON key file"),
        (r".*key\.pem$", "PEM key file"),
        (r".*id_rsa", "RSA private key"),
        (r".*id_ed25519", "Ed25519 private key"),
        (r"^/var/log/", "System log directory"),
        (r"^/root/", "Root home directory"),
        (r"^/sys/", "System kernel interface"),
        (r"^/proc/", "Process information"),
        (r"^/boot/", "Boot directory"),
        (r"^/dev/(sd|hd|nvme|md)", "Block device"),
    ]
    
    # Dangerous command patterns with descriptions and penalties
    DANGEROUS_PATTERNS: List[Tuple[str, str, int]] = [
        (r"\brm\s+-rf\s+/\b", "Recursive deletion of root directory", 100),
        (r"\brm\s+-rf\s+/\*", "Wildcard deletion in root", 100),
        (r"\bdd\s+if=.*of=/dev/[sh]d", "Direct disk write operation", 100),
        (r"\bdd\s+if=.*of=/dev/null", "Data destruction to null", 80),
        (r"\bmv\s+/\S+\s+/dev/null", "Moving files to null device", 80),
        (r"\bmkfs\.[a-z]+", "Filesystem formatting", 100),
        (r"\bfdisk\s", "Partition manipulation", 90),
        (r"\bparted\s", "Partition editing", 90),
        (r"\bformat\s+", "Drive formatting", 90),
        (r">\s*/etc/passwd", "Overwriting system password file", 100),
        (r">\s*/etc/shadow", "Overwriting system shadow file", 100),
        (r">\s*/etc/sudoers", "Overwriting sudoers file", 100),
        (r"\bwipefs\s", "Filesystem signature wiping", 85),
        (r"\bshred\s", "Secure file deletion", 70),
    ]
    
    # System-level commands
    SYSTEM_COMMANDS: List[Tuple[str, str, int]] = [
        (r"\bsudo\s+", "Elevated privilege execution", 50),
        (r"\bsu\s+-", "User switch to root", 60),
        (r"\bchown\s+-R\s+root", "Changing ownership to root", 50),
        (r"\bchmod\s+777", "World-writable permissions", 60),
        (r"\bchmod\s+[0-7]777", "World-writable permissions", 60),
        (r"\busermod\s+", "User modification", 50),
        (r"\buserdel\s+", "User deletion", 60),
        (r"\bgroupmod\s+", "Group modification", 50),
        (r"\bgroupdel\s+", "Group deletion", 50),
        (r"\bsystemctl\s+(stop|restart|disable|mask)", "Service control", 45),
        (r"\bservice\s+\S+\s+(stop|restart)", "Service control", 45),
        (r"\bkill\s+-9\s+1\b", "Killing init process", 100),
        (r"\binit\s+0\b", "System shutdown", 100),
        (r"\breboot\b", "System reboot", 80),
        (r"\bshutdown\b", "System shutdown", 80),
        (r"\bhalt\b", "System halt", 80),
        (r"\bpoweroff\b", "System poweroff", 80),
    ]
    
    # Network-related commands
    NETWORK_COMMANDS: List[Tuple[str, str, int]] = [
        (r"\bcurl\s+.*\|\s*sh", "Remote script execution", 90),
        (r"\bwget\s+.*\|\s*sh", "Remote script execution", 90),
        (r"\bcurl\s+.*\|\s*bash", "Remote script execution", 90),
        (r"\bwget\s+.*\|\s*bash", "Remote script execution", 90),
        (r"\bcurl\b", "Data transfer via curl", 25),
        (r"\bwget\b", "Data transfer via wget", 25),
        (r"\bnc\b|\bnetcat\b", "Network connection tool", 35),
        (r"\bnmap\b", "Network scanning", 50),
        (r"\bscp\b", "Secure copy", 30),
        (r"\bsftp\b", "Secure FTP", 30),
        (r"\bssh\s+.*\s+rm", "Remote deletion", 60),
        (r"\bssh\s+.*\s+mkfs", "Remote formatting", 90),
        (r"\btelnet\b", "Insecure remote access", 50),
        (r"\bftp\b", "Insecure file transfer", 40),
    ]
    
    # Suspicious patterns for skill names
    SUSPICIOUS_SKILL_PATTERNS = [
        r"hack", r"crack", r"exploit", r"backdoor", r"rootkit",
        r"bypass", r"inject", r"trojan", r"malware", r"virus",
        r"keylog", r"sniff", r"spoof", r"brute",
        r"test.*admin", r"temp.*root", r"debug.*system"
    ]
    
    # System-level skill indicators
    SYSTEM_SKILL_KEYWORDS = [
        "system", "shell", "exec", "admin", "root", "kernel",
        "privilege", "escalation", "sudo", "superuser"
    ]
    
    # High-risk permissions for skills
    HIGH_RISK_PERMISSIONS = [
        "filesystem", "network", "shell", "system", "process",
        "clipboard", "input", "screen", "camera", "microphone"
    ]
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        defaults = {
            "whitelist_paths": [],
            "whitelist_commands": [],
            "whitelist_domains": [],
            "whitelist_skills": [],
            "sensitive_extensions": [
                ".env", ".key", ".secret", ".password", ".token",
                ".pem", ".p12", ".pfx", ".crt", ".cer"
            ],
            "batch_threshold": 5,
            "strict_mode": False,
            "check_hidden_files": True,
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    defaults.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}", file=sys.stderr)
        
        return defaults
    
    def assess_file_operation(self, operation: str, paths: List[str], 
                             recursive: bool = False) -> RiskAssessment:
        """
        Assess risk of file operations
        
        Args:
            operation: Type of operation (read/write/delete/move/copy)
            paths: List of target paths
            recursive: Whether operation is recursive
        """
        reasons = []
        score = 0
        
        # Check for batch operations
        if len(paths) > self.config.get("batch_threshold", 5):
            score += 20
            reasons.append(f"Batch operation ({len(paths)} files)")
        
        if len(paths) > 20:
            score += 10
            reasons.append(f"Large batch operation ({len(paths)} files)")
        
        # Check for recursive operations
        if recursive:
            score += 25
            reasons.append("Recursive operation")
        
        for path in paths:
            expanded_path = os.path.expanduser(path)
            
            # Check sensitive paths
            sensitive_match = self._is_sensitive_path(expanded_path)
            if sensitive_match:
                score += 40
                reasons.append(f"Access to {sensitive_match}: {path}")
            
            # Check sensitive file extensions
            if self._has_sensitive_extension(expanded_path):
                score += 30
                reasons.append(f"Sensitive file type: {os.path.basename(path)}")
            
            # Check hidden files (if enabled)
            if self.config.get("check_hidden_files", True):
                basename = os.path.basename(expanded_path)
                if basename.startswith('.') and len(basename) > 1:
                    score += 5
                    # Don't add reason for every hidden file to avoid noise
            
            # Check write/delete operations
            if operation in ["write", "delete", "move"]:
                base_scores = {"write": 20, "delete": 30, "move": 25}
                score += base_scores.get(operation, 20)
                
                if operation == "delete":
                    if os.path.isdir(expanded_path) if os.path.exists(expanded_path) else recursive:
                        score += 15
                        reasons.append(f"Directory deletion: {path}")
                    else:
                        reasons.append(f"File deletion: {path}")
                        
                elif operation == "write":
                    if os.path.exists(expanded_path):
                        score += 15
                        reasons.append(f"Overwriting existing file: {path}")
                    else:
                        reasons.append(f"Creating new file: {path}")
                
                elif operation == "move":
                    reasons.append(f"Moving file: {path}")
        
        # Calculate final level
        level = self._calculate_level(score)
        requires_approval = level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        
        operation_detail = f"{operation} {', '.join(paths[:3])}"
        if len(paths) > 3:
            operation_detail += f" and {len(paths) - 3} more"
        
        recommendation = self._generate_recommendation(operation, paths, reasons)
        
        return RiskAssessment(
            level=level,
            score=min(score, 100),
            reasons=reasons,
            recommendation=recommendation,
            requires_approval=requires_approval,
            operation_type="file",
            operation_detail=operation_detail
        )
    
    def assess_shell_command(self, command: str) -> RiskAssessment:
        """Assess risk of shell command execution"""
        reasons = []
        score = 0
        
        # Check whitelist
        if self._is_whitelisted_command(command):
            return RiskAssessment(
                level=RiskLevel.LOW,
                score=0,
                reasons=["Command in whitelist"],
                recommendation="Safe to execute",
                requires_approval=False,
                operation_type="shell",
                operation_detail=command[:100]
            )
        
        # Check dangerous patterns
        for pattern, description, penalty in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                score += penalty
                reasons.append(f"Dangerous pattern: {description}")
        
        # Check system commands
        for pattern, description, penalty in self.SYSTEM_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                score += penalty
                reasons.append(f"System operation: {description}")
        
        # Check network commands
        for pattern, description, penalty in self.NETWORK_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                score += penalty
                reasons.append(f"Network operation: {description}")
                break  # Only count once
        
        # Complex commands (pipes, redirects)
        pipe_count = command.count('|')
        if pipe_count > 0:
            score += min(pipe_count * 5, 15)
            reasons.append(f"Command pipeline ({pipe_count + 1} stages)")
        
        redirect_count = command.count('>')
        if redirect_count > 0:
            score += min(redirect_count * 5, 10)
            if redirect_count == 1:
                reasons.append("Output redirection")
            else:
                reasons.append("Multiple redirections")
        
        # Background execution
        if command.rstrip().endswith('&'):
            score += 10
            reasons.append("Background execution")
        
        level = self._calculate_level(score)
        requires_approval = level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        recommendation = self._generate_command_recommendation(command, reasons)
        
        return RiskAssessment(
            level=level,
            score=min(score, 100),
            reasons=reasons,
            recommendation=recommendation,
            requires_approval=requires_approval,
            operation_type="shell",
            operation_detail=command[:200]
        )
    
    def assess_network_request(self, url: str, method: str = "GET", 
                                data: Optional[str] = None,
                                headers: Optional[Dict] = None) -> RiskAssessment:
        """Assess risk of network requests"""
        reasons = []
        score = 0
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            
            # Check whitelist
            if self._is_whitelisted_domain(hostname):
                return RiskAssessment(
                    level=RiskLevel.LOW,
                    score=0,
                    reasons=["Domain in whitelist"],
                    recommendation="Safe to proceed",
                    requires_approval=False,
                    operation_type="network",
                    operation_detail=f"{method} {url[:100]}"
                )
            
            # External domain check
            if self._is_external_domain(hostname):
                score += 40
                reasons.append(f"External domain: {hostname}")
            
            # Check for IP addresses (potentially suspicious)
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname):
                score += 20
                reasons.append("Direct IP address access")
            
            # Insecure protocols
            if parsed.scheme == "http":
                score += 10
                reasons.append("Unencrypted HTTP protocol")
            elif parsed.scheme in ["ftp", "telnet"]:
                score += 50
                reasons.append(f"Insecure protocol: {parsed.scheme}")
            elif parsed.scheme == "file":
                score += 40
                reasons.append("File protocol access")
            
            # Data modification methods
            if method in ["POST", "PUT", "DELETE", "PATCH"]:
                score += 20
                reasons.append(f"Data modification: {method}")
            
            # Data payload present
            if data:
                score += 15
                data_size = len(data)
                if data_size > 10000:
                    score += 10
                    reasons.append(f"Large data payload ({data_size} bytes)")
                else:
                    reasons.append("Request includes data payload")
            
            # Sensitive headers
            if headers:
                sensitive_headers = ['authorization', 'x-api-key', 'cookie']
                for header in sensitive_headers:
                    if any(h.lower() == header for h in headers.keys()):
                        score += 10
                        reasons.append(f"Contains sensitive header: {header}")
                        break
            
            # Sensitive ports
            sensitive_ports = {
                22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                110: "POP3", 143: "IMAP", 3389: "RDP", 
                5900: "VNC", 6379: "Redis", 3306: "MySQL",
                5432: "PostgreSQL", 27017: "MongoDB", 9200: "Elasticsearch"
            }
            port = parsed.port
            if port in sensitive_ports:
                score += 25
                reasons.append(f"Sensitive service port: {port} ({sensitive_ports[port]})")
            
            # URL path analysis
            path = parsed.path.lower()
            if any(keyword in path for keyword in ['admin', 'config', 'api/v1', 'internal']):
                score += 15
                reasons.append("Potentially sensitive API endpoint")
        
        except Exception as e:
            score += 20
            reasons.append(f"Could not parse URL: {e}")
        
        level = self._calculate_level(score)
        requires_approval = level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        recommendation = f"Network request to {hostname or 'unknown'} - verify data destination is trusted"
        
        return RiskAssessment(
            level=level,
            score=min(score, 100),
            reasons=reasons,
            recommendation=recommendation,
            requires_approval=requires_approval,
            operation_type="network",
            operation_detail=f"{method} {url[:150]}"
        )
    
    def assess_skill_install(self, skill_name: str, source: str,
                              permissions: Optional[List[str]] = None,
                              version: Optional[str] = None) -> RiskAssessment:
        """Assess risk of skill installation"""
        reasons = []
        score = 0
        
        # Check whitelist
        if self._is_whitelisted_skill(skill_name):
            return RiskAssessment(
                level=RiskLevel.LOW,
                score=0,
                reasons=["Skill in whitelist"],
                recommendation="Trusted skill - safe to install",
                requires_approval=False,
                operation_type="skill",
                operation_detail=f"{skill_name}@{version or 'latest'} from {source}"
            )
        
        # Source risk assessment
        source_risk = {
            "clawhub": (10, "Official registry"),
            "npm": (15, "NPM registry"),
            "github": (25, "GitHub repository"),
            "git": (30, "Git repository"),
            "local": (40, "Local file"),
            "url": (45, "Direct URL"),
            "unknown": (50, "Unknown source")
        }
        src_score, src_desc = source_risk.get(source.lower(), (50, "Unknown source"))
        score += src_score
        reasons.append(f"Installation source: {src_desc}")
        
        # Version check
        if version:
            if 'alpha' in version.lower() or 'beta' in version.lower() or 'rc' in version.lower():
                score += 15
                reasons.append(f"Pre-release version: {version}")
        
        # Suspicious naming patterns
        for pattern in self.SUSPICIOUS_SKILL_PATTERNS:
            if pattern in skill_name.lower():
                score += 25
                reasons.append(f"Suspicious naming pattern: '{pattern}'")
                break  # Only count once
        
        # System-level indicators
        for keyword in self.SYSTEM_SKILL_KEYWORDS:
            if keyword in skill_name.lower():
                score += 15
                reasons.append(f"System-level skill indicator: '{keyword}'")
                break
        
        # Permissions analysis
        if permissions:
            for perm in permissions:
                perm_lower = perm.lower()
                for high_risk in self.HIGH_RISK_PERMISSIONS:
                    if high_risk in perm_lower:
                        score += 20
                        reasons.append(f"High-risk permission: {perm}")
                        break
        else:
            # No permissions specified is suspicious
            score += 10
            reasons.append("No permissions declared")
        
        level = self._calculate_level(score)
        requires_approval = level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        recommendation = f"Installing skill '{skill_name}' grants system access - verify source and reviews before installation"
        
        return RiskAssessment(
            level=level,
            score=min(score, 100),
            reasons=reasons,
            recommendation=recommendation,
            requires_approval=requires_approval,
            operation_type="skill",
            operation_detail=f"{skill_name}@{version or 'latest'} from {source}"
        )
    
    def assess_system_config(self, config_path: str, changes: Dict[str, Any]) -> RiskAssessment:
        """Assess risk of system configuration changes"""
        reasons = []
        score = 50  # Base score for system config
        
        # Check if path is sensitive
        sensitive_match = self._is_sensitive_path(config_path)
        if sensitive_match:
            score += 30
            reasons.append(f"System configuration file: {sensitive_match}")
        
        # Analyze changes
        for key, value in changes.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in ['password', 'secret', 'key', 'token']):
                score += 20
                reasons.append(f"Sensitive configuration key: {key}")
            
            if isinstance(value, bool) and value == True:
                if any(enable in key_lower for enable in ['enable', 'disable', 'debug', 'trace']):
                    score += 10
                    reasons.append(f"Enabling feature: {key}")
        
        level = self._calculate_level(score)
        requires_approval = level in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        recommendation = "System configuration changes can affect stability - verify changes before applying"
        
        return RiskAssessment(
            level=level,
            score=min(score, 100),
            reasons=reasons,
            recommendation=recommendation,
            requires_approval=requires_approval,
            operation_type="system",
            operation_detail=f"Config: {config_path}"
        )
    
    def _is_sensitive_path(self, path: str) -> Optional[str]:
        """Check if path is sensitive and return description"""
        for pattern, description in self.SENSITIVE_PATHS:
            if re.search(pattern, path, re.IGNORECASE):
                return description
        return None
    
    def _has_sensitive_extension(self, path: str) -> bool:
        """Check if file has sensitive extension"""
        path_lower = path.lower()
        for ext in self.config.get("sensitive_extensions", []):
            if path_lower.endswith(ext.lower()):
                return True
        return False
    
    def _is_whitelisted_command(self, command: str) -> bool:
        """Check if command is whitelisted"""
        whitelist = self.config.get("whitelist_commands", [])
        for pattern in whitelist:
            if command.strip().startswith(pattern):
                return True
        return False
    
    def _is_whitelisted_domain(self, hostname: str) -> bool:
        """Check if domain is whitelisted"""
        whitelist = self.config.get("whitelist_domains", [])
        return hostname in whitelist
    
    def _is_whitelisted_skill(self, skill_name: str) -> bool:
        """Check if skill is whitelisted"""
        whitelist = self.config.get("whitelist_skills", [])
        return skill_name in whitelist
    
    def _is_external_domain(self, hostname: str) -> bool:
        """Check if domain is external (not internal/private)"""
        if not hostname:
            return False
        
        internal_patterns = [
            r"\.local$",
            r"\.internal$",
            r"\.lan$",
            r"\.home$",
            r"localhost$",
            r"^127\.",
            r"^10\.",
            r"^192\.168\.",
            r"^172\.(1[6-9]|2[0-9]|3[01])\.",
            r"^169\.254\."
        ]
        
        for pattern in internal_patterns:
            if re.search(pattern, hostname, re.IGNORECASE):
                return False
        return True
    
    def _calculate_level(self, score: int) -> RiskLevel:
        """Calculate risk level from score"""
        if score >= 80:
            return RiskLevel.CRITICAL
        elif score >= 60:
            return RiskLevel.HIGH
        elif score >= 30:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_recommendation(self, operation: str, paths: List[str], 
                                  reasons: List[str]) -> str:
        """Generate recommendation message for file operations"""
        if not reasons:
            return "Operation appears safe"
        
        if operation == "delete":
            return f"About to delete {len(paths)} item(s). Ensure important data is backed up before proceeding."
        elif operation == "write":
            return "File write operation - verify this won't overwrite important configuration or data"
        elif operation == "move":
            return "File move operation - verify source and destination are correct"
        else:
            return f"Detected risks: {', '.join(reasons[:3])}"
    
    def _generate_command_recommendation(self, command: str, 
                                          reasons: List[str]) -> str:
        """Generate command-specific recommendation"""
        cmd_lower = command.lower()
        
        if any(x in cmd_lower for x in ["rm -rf", "rmdir /s"]):
            return "⚠️  DESTRUCTIVE DELETION detected - double-check target path before proceeding"
        elif "sudo" in cmd_lower or "su -" in cmd_lower:
            return "⚠️  PRIVILEGE ESCALATION detected - verify command source and intent"
        elif any(x in cmd_lower for x in ["curl", "wget"]) and ("|" in command or ";" in command):
            return "⚠️  REMOTE CODE EXECUTION risk - verify script source before execution"
        elif "mkfs" in cmd_lower or "format" in cmd_lower:
            return "🛑 FORMATTING OPERATION - This will ERASE ALL DATA on target device"
        elif any(x in cmd_lower for x in ["dd if", "dcfldd"]):
            return "🛑 DISK WRITE OPERATION - This can destroy data or entire filesystems"
        elif "reboot" in cmd_lower or "shutdown" in cmd_lower:
            return "⚠️  SYSTEM RESTART - Save all work before proceeding"
        else:
            return f"Review carefully: {', '.join(reasons[:2])}"


def main():
    """Command-line interface for risk assessment"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Claw-Guardian Risk Assessment Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file delete ~/test.txt
  %(prog)s shell "rm -rf /tmp/*"
  %(prog)s network https://api.example.com POST
  %(prog)s skill unknown-skill github
  %(prog)s system /etc/config --changes '{"debug": true}'
        """
    )
    
    parser.add_argument("command", choices=["file", "shell", "network", "skill", "system"],
                       help="Type of operation to assess")
    parser.add_argument("target", help="Target of the operation")
    parser.add_argument("args", nargs="*", help="Additional arguments")
    parser.add_argument("--config", "-c", help="Path to configuration file")
    parser.add_argument("--method", "-m", default="GET", help="HTTP method (for network)")
    parser.add_argument("--data", "-d", help="Request data (for network)")
    parser.add_argument("--source", "-s", default="unknown", help="Skill source")
    parser.add_argument("--permissions", "-p", help="Skill permissions (comma-separated)")
    parser.add_argument("--version", "-v", help="Skill version")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursive operation")
    parser.add_argument("--changes", help="Configuration changes (JSON)")
    
    args = parser.parse_args()
    
    engine = RiskEngine(config_path=args.config)
    
    if args.command == "file":
        operation = args.args[0] if args.args else "read"
        paths = [args.target] + args.args[1:] if len(args.args) > 1 else [args.target]
        result = engine.assess_file_operation(operation, paths, args.recursive)
    
    elif args.command == "shell":
        result = engine.assess_shell_command(args.target)
    
    elif args.command == "network":
        result = engine.assess_network_request(
            args.target, 
            method=args.method,
            data=args.data
        )
    
    elif args.command == "skill":
        perms = args.permissions.split(",") if args.permissions else None
        result = engine.assess_skill_install(
            args.target,
            source=args.source,
            permissions=perms,
            version=args.version
        )
    
    elif args.command == "system":
        changes = json.loads(args.changes) if args.changes else {}
        result = engine.assess_system_config(args.target, changes)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    # Output as JSON
    output = {
        "level": result.level.value,
        "score": result.score,
        "reasons": result.reasons,
        "recommendation": result.recommendation,
        "requires_approval": result.requires_approval,
        "operation_type": result.operation_type,
        "operation_detail": result.operation_detail
    }
    print(json.dumps(output, indent=2))
    
    # Exit code based on risk level
    sys.exit(0 if result.level in [RiskLevel.LOW, RiskLevel.MEDIUM] else 1)


if __name__ == "__main__":
    main()
