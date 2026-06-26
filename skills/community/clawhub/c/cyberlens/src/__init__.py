"""CyberLens OpenClaw Skill - Security Scanner for websites and repositories."""

__version__ = "1.1.1"
__author__ = "shadoprizm"

from .scanner import SecurityScanner
from .tools import (
    connect_account,
    scan_target,
    scan_website,
    scan_repository,
    get_security_score,
    explain_finding,
    list_scan_rules,
)
from .api_client import CyberLensAPIClient
from .models import (
    ScanResult,
    SecurityScore,
    Finding,
    FindingExplanation,
    ScanRule,
)

__all__ = [
    "SecurityScanner",
    "CyberLensAPIClient",
    "connect_account",
    "scan_target",
    "scan_website",
    "scan_repository",
    "get_security_score",
    "explain_finding",
    "list_scan_rules",
    "ScanResult",
    "SecurityScore",
    "Finding",
    "FindingExplanation",
    "ScanRule",
]
