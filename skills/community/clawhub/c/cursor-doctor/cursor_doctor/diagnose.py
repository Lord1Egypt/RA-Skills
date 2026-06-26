"""Cursor 诊断器 — 自动检测 Cursor 环境并匹配已知错误模式"""

from .signatures.database import (
    ErrorSignature,
    SIGNATURES,
    find_matching_signatures,
    CATEGORY_NAMES,
)
from dataclasses import dataclass, field
from typing import Optional
import subprocess
import os
import json
import sys


@dataclass
class DiagnosisReport:
    """诊断报告"""
    cursor_version: str = ""
    errors_found: list[dict] = field(default_factory=list)
    system_checks: dict = field(default_factory=dict)
    summary: str = ""
    score: float = 0.0          # 0.0 = 健康, 1.0 = 高危


class CursorDoctor:
    """Cursor 诊断器核心"""
    
    def __init__(self):
        self.cursor_config_dir = self._find_cursor_config()
        self.cursor_binary = self._find_cursor_binary()
    
    def _find_cursor_config(self) -> str:
        """查找 Cursor 配置目录"""
        home = os.path.expanduser("~")
        candidates = [
            os.path.join(home, ".cursor"),
            os.path.join(home, "Library", "Application Support", "Cursor"),
            os.path.join(home, "AppData", "Roaming", "Cursor"),
        ]
        for p in candidates:
            if os.path.isdir(p):
                return p
        return ""
    
    def _find_cursor_binary(self) -> str:
        """查找 Cursor 可执行文件"""
        import shutil
        cmd = shutil.which("cursor")
        if cmd:
            return cmd
        # macOS 常见路径
        for p in [
            "/Applications/Cursor.app/Contents/MacOS/Cursor",
            os.path.expanduser("~/Applications/Cursor.app/Contents/MacOS/Cursor"),
        ]:
            if os.path.isfile(p):
                return p
        return ""
    
    def get_version(self) -> str:
        """获取 Cursor 版本"""
        if not self.cursor_binary:
            return "未找到 Cursor"
        try:
            result = subprocess.run(
                [self.cursor_binary, "--version"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() or result.stderr.strip() or "未知版本"
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return "无法获取版本"
    
    def check_logs(self) -> list[dict]:
        """扫描 Cursor 日志找错误"""
        errors = []
        log_paths = [
            os.path.join(self.cursor_config_dir, "logs"),
            os.path.expanduser("~/.cursor/logs"),
        ]
        for log_dir in log_paths:
            if not os.path.isdir(log_dir):
                continue
            for root, dirs, files in os.walk(log_dir):
                for f in files:
                    if not f.endswith((".log", ".txt")):
                        continue
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", errors="replace") as fh:
                            for line in fh:
                                if any(kw in line.lower() for kw in
                                    ["error", "fail", "crash", "exception", "timeout"]):
                                    matches = find_matching_signatures(line)
                                    for sig, pattern in matches:
                                        errors.append({
                                            "file": os.path.basename(path),
                                            "line": line.strip()[:200],
                                            "signature_id": sig.id,
                                            "signature_name": sig.name,
                                            "severity": sig.severity,
                                        })
                    except (IOError, OSError):
                        continue
        return errors
    
    def check_system(self) -> dict:
        """检查系统环境"""
        checks = {}
        
        # Python
        checks["python"] = sys.version.split()[0] if sys.version else "未知"
        
        # Node.js / npm
        for cmd in ["node", "npm"]:
            try:
                r = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
                checks[cmd] = r.stdout.strip() or "未安装"
            except Exception:
                checks[cmd] = "未安装"
        
        # Git
        try:
            r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5)
            checks["git"] = r.stdout.strip() or "未安装"
        except Exception:
            checks["git"] = "未安装"
        
        # Shell
        checks["shell"] = os.environ.get("SHELL", "未知")
        
        # Proxy
        checks["http_proxy"] = bool(os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy"))
        checks["https_proxy"] = bool(os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))
        
        # Memory
        try:
            import psutil
            mem = psutil.virtual_memory()
            checks["memory_total_gb"] = round(mem.total / (1024**3), 1)
            checks["memory_available_gb"] = round(mem.available / (1024**3), 1)
            checks["memory_percent"] = mem.percent
        except Exception:
            checks["memory"] = "无法获取"
        
        # Disk
        try:
            import shutil
            total, used, free = shutil.disk_usage(os.path.expanduser("~"))
            checks["disk_total_gb"] = round(total / (1024**3), 1)
            checks["disk_free_gb"] = round(free / (1024**3), 1)
        except Exception:
            checks["disk"] = "无法获取"
        
        return checks
    
    def diagnose(self) -> DiagnosisReport:
        """执行全面诊断"""
        report = DiagnosisReport()
        report.cursor_version = self.get_version()
        report.errors_found = self.check_logs()
        report.system_checks = self.check_system()
        
        # 计算健康评分
        severity_weights = {"critical": 1.0, "high": 0.6, "medium": 0.3, "low": 0.1}
        base_score = sum(
            severity_weights.get(e["severity"], 0.2)
            for e in report.errors_found
        )
        report.score = min(1.0, base_score / 3.0)
        
        # 生成摘要
        critical = [e for e in report.errors_found if e["severity"] == "critical"]
        high = [e for e in report.errors_found if e["severity"] == "high"]
        report.summary = (
            f"Cursor 版本: {report.cursor_version}\n"
            f"诊断分数: {report.score:.0%} (阈值: 健康 < 30% | 异常 30-70% | 高危 > 70%)\n"
            f"日志错误: {len(report.errors_found)} 条 (critical={len(critical)}, high={len(high)}, medium/低={len(report.errors_found)-len(critical)-len(high)})\n"
        )
        
        return report
