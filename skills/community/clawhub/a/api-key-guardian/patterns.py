"""敏感信息检测规则"""

PATTERNS = [
    {"name": "OpenAI API Key",    "regex": r"sk-[A-Za-z0-9]{32,}",                                           "severity": "high"},
    {"name": "Anthropic API Key", "regex": r"sk-ant-[A-Za-z0-9\-_]{32,}",                                    "severity": "high"},
    {"name": "AWS Access Key",    "regex": r"AKIA[0-9A-Z]{16}",                                               "severity": "high"},
    {"name": "Google API Key",    "regex": r"AIza[0-9A-Za-z\-_]{35}",                                        "severity": "high"},
    {"name": "GitHub Token",      "regex": r"gh[pousr]_[A-Za-z0-9]{36,}",                                    "severity": "high"},
    {"name": "Stripe Live Key",   "regex": r"sk_live_[A-Za-z0-9]{24,}",                                      "severity": "high"},
    {"name": "ClawHub Token",     "regex": r"clh_[A-Za-z0-9\-_]{30,}",                                       "severity": "high"},
    {"name": "RSA Private Key",   "regex": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",                         "severity": "critical"},
    {"name": "Database URL",      "regex": r"(mysql|postgresql|mongodb|redis)://[^:]+:[^@]+@",                "severity": "high"},
    {"name": "Generic Secret",    "regex": r'(?i)(secret|password|passwd|pwd|token|api_key|apikey|access_key)\s*[=:]\s*["\']?([A-Za-z0-9\-_\.]{16,})', "severity": "medium"},
]

SKIP_DIRS  = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next"}
SKIP_EXTS  = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".pyc", ".exe", ".bin", ".woff", ".ttf"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "poetry.lock", "Pipfile.lock"}

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
