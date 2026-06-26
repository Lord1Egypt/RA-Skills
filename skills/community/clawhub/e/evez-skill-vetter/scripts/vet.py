"""
Skill Vetter — Security review for OpenClaw skills
"""
import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Finding:
    severity: str  # "info", "warn", "danger"
    category: str
    message: str
    file: str
    line: int = 0
    score_impact: int = 0


DANGEROUS_PATTERNS = [
    (r'\beval\s*\(', "code_injection", "eval() can execute arbitrary code", 25),
    (r'\bexec\s*\(', "code_injection", "exec() can execute arbitrary code", 20),
    (r'\bsubprocess\.\w+\(', "command_exec", "subprocess can run system commands", 15),
    (r'\bos\.system\s*\(', "command_exec", "os.system() runs shell commands", 20),
    (r'\bos\.popen\s*\(', "command_exec", "os.popen() runs shell commands", 18),
    (r'\b__import__\s*\(', "dynamic_import", "Dynamic imports can load untrusted code", 12),
    (r'base64\.b64decode', "obfuscation", "Base64 decode may hide malicious payloads", 8),
    (r'pickle\.loads', "deserialization", "pickle.loads is unsafe deserialization", 20),
    (r'marshal\.loads', "deserialization", "marshal.loads is unsafe", 15),
    (r'\bopen\s*\([^)]*[\'"]w', "file_write", "File write access", 5),
    (r'requests\.(post|put|patch)\s*\(', "network_write", "HTTP POST/PUT sends data externally", 10),
    (r'urllib\.request\.urlopen', "network_access", "Network access via urllib", 8),
    (r'fetch\s*\(', "network_access", "fetch() makes network requests", 6),
    (r'XMLHttpRequest', "network_access", "XHR makes network requests", 6),
    (r'localStorage\.', "browser_storage", "Access to browser localStorage", 3),
    (r'document\.cookie', "cookie_access", "Access to cookies", 8),
    (r'process\.env', "env_access", "Reads environment variables", 4),
    (r'child_process', "command_exec", "Node.js child_process can run commands", 18),
    (r'require\s*\([\'"]child_process', "command_exec", "Requires child_process module", 18),
    (r'\.exec\s*\(', "command_exec", ".exec() can run commands", 15),
    (r'\.spawn\s*\(', "command_exec", ".spawn() can run commands", 15),
]

SECRET_PATTERNS = [
    (r'(?:api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9]{20,}', "api_key", "Hardcoded API key", 30),
    (r'(?:secret|token|password)\s*[=:]\s*["\'][a-zA-Z0-9]{16,}', "secret", "Hardcoded secret/token/password", 30),
    (r'sk-[a-zA-Z0-9]{20,}', "openai_key", "Hardcoded OpenAI API key", 35),
    (r'ghp_[a-zA-Z0-9]{36}', "github_token", "Hardcoded GitHub token", 35),
    (r'AKIA[0-9A-Z]{16}', "aws_key", "Hardcoded AWS access key", 35),
]

OBFUSCATION_PATTERNS = [
    (r'\\x[0-9a-f]{2}', "hex_encoding", "Hex-encoded strings may hide content", 5),
    (r'\\u[0-9a-f]{4}', "unicode_escape", "Unicode escapes may hide content", 3),
    (r'atob\s*\(', "base64_browser", "atob() decodes base64 in browser", 6),
    (r'String\.fromCharCode', "char_code", "String.fromCharCode obfuscation", 8),
]


class SkillVetter:
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.findings: list[Finding] = []
        self.total_risk = 0

    def vet(self) -> dict:
        self._check_structure()
        self._scan_files()
        self._check_size()
        self.total_risk = min(100, sum(f.score_impact for f in self.findings))
        return self.report()

    def _check_structure(self):
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.findings.append(Finding("danger", "structure", "No SKILL.md found", "", 0, 20))
        else:
            content = skill_md.read_text()
            if len(content) < 50:
                self.findings.append(Finding("warn", "structure", "SKILL.md is suspiciously short", "SKILL.md", 0, 5))
            if "---" not in content[:100]:
                self.findings.append(Finding("warn", "structure", "SKILL.md missing YAML frontmatter", "SKILL.md", 0, 5))

    def _scan_files(self):
        for filepath in self.skill_path.rglob("*"):
            if filepath.is_dir():
                continue
            if filepath.suffix in ('.pyc', '.pyo', '.so', '.dll', '.exe'):
                self.findings.append(Finding("danger", "binary", f"Binary file found: {filepath.name}", str(filepath), 0, 25))
                continue
            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            rel_path = str(filepath.relative_to(self.skill_path))

            for line_num, line in enumerate(content.splitlines(), 1):
                for pattern, category, message, impact in DANGEROUS_PATTERNS:
                    if re.search(pattern, line):
                        self.findings.append(Finding(
                            "warn" if impact < 15 else "danger", category, message, rel_path, line_num, impact
                        ))
                for pattern, category, message, impact in SECRET_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.findings.append(Finding("danger", category, message, rel_path, line_num, impact))
                for pattern, category, message, impact in OBFUSCATION_PATTERNS:
                    if re.search(pattern, line):
                        self.findings.append(Finding("warn", category, message, rel_path, line_num, impact))

    def _check_size(self):
        total = sum(f.stat().st_size for f in self.skill_path.rglob("*") if f.is_file())
        if total > 5_000_000:
            self.findings.append(Finding("warn", "size", f"Skill is {total//1024}KB — suspiciously large", "", 0, 10))

    def report(self) -> dict:
        if self.total_risk <= 20:
            level = "safe"
        elif self.total_risk <= 50:
            level = "caution"
        elif self.total_risk <= 75:
            level = "risky"
        else:
            level = "dangerous"

        return {
            "skill": self.skill_path.name,
            "risk_score": self.total_risk,
            "risk_level": level,
            "findings_count": len(self.findings),
            "findings": [
                {"severity": f.severity, "category": f.category, "message": f.message, "file": f.file, "line": f.line}
                for f in sorted(self.findings, key=lambda x: -x.score_impact)
            ],
        }


if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--skill", type=click.Path(exists=True), help="Path to skill directory")
    @click.option("--slug", help="ClawHub skill slug to vet")
    def vet(skill, slug):
        if skill:
            vetter = SkillVetter(Path(skill))
            report = vetter.vet()
            level = report["risk_level"].upper()
            icons = {"safe": "✅", "caution": "⚠️", "risky": "🚨", "dangerous": "❌"}
            click.echo(f"\n{icons.get(level, '?')} RISK: {report['risk_score']}/100 ({level})")
            click.echo(f"Findings: {report['findings_count']}\n")
            for f in report["findings"]:
                icon = {"info": "ℹ️", "warn": "⚠️", "danger": "🚨"}.get(f["severity"], "?")
                click.echo(f"  {icon} {f['category']}: {f['message']} ({f['file']}:{f['line']})")

    vet()
