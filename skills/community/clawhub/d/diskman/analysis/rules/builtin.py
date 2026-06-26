"""Built-in rules for directory analysis."""

from ...models import DirectoryType, RecommendedAction, RiskLevel
from .engine import Rule

# Cache directories - safe to delete
CACHE_RULES = [
    Rule(
        name="npm_cache",
        patterns=["npm-cache", ".npm"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="npm cache - safe to delete, will be regenerated",
        confidence=0.95,
    ),
    Rule(
        name="pip_cache",
        patterns=["pip-cache", ".pip", "pip"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="pip cache - safe to delete",
        confidence=0.95,
    ),
    Rule(
        name="yarn_cache",
        patterns=[".yarn", "yarn-cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Yarn cache - safe to delete",
        confidence=0.95,
    ),
    Rule(
        name="pnpm_cache",
        patterns=[".pnpm-store", "pnpm-cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="pnpm cache - safe to delete",
        confidence=0.95,
    ),
    Rule(
        name="uv_cache",
        patterns=[".uv", "uv-cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="uv (Python) cache - safe to delete",
        confidence=0.95,
    ),
    Rule(
        name="gradle_cache",
        patterns=[".gradle", "gradle-cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Gradle cache - safe to delete",
        confidence=0.90,
    ),
    Rule(
        name="maven_cache",
        patterns=[".m2"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Maven cache - safe to delete",
        confidence=0.90,
    ),
    Rule(
        name="cargo_cache",
        patterns=[".cargo"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Cargo (Rust) cache - safe to delete",
        confidence=0.90,
    ),
    Rule(
        name="go_cache",
        patterns=["go-build", "go-cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Go build cache - safe to delete",
        confidence=0.90,
    ),
    Rule(
        name="browser_cache",
        patterns=["Cache", "cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Browser or application cache - generally safe to delete",
        confidence=0.70,
    ),
]

# Dependency directories - can delete or move
DEPENDENCY_RULES = [
    Rule(
        name="node_modules",
        patterns=["node_modules"],
        directory_type=DirectoryType.DEPENDENCY,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Node.js dependencies - can be reinstalled with npm install",
        confidence=0.95,
    ),
    Rule(
        name="python_pycache",
        patterns=["__pycache__"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.SAFE,
        action=RecommendedAction.CAN_DELETE,
        reason="Python bytecode cache - safe to delete",
        confidence=0.98,
    ),
    Rule(
        name="pytest_cache",
        patterns=[".pytest_cache", ".pytest"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.SAFE,
        action=RecommendedAction.CAN_DELETE,
        reason="pytest cache - safe to delete",
        confidence=0.98,
    ),
    Rule(
        name="mypy_cache",
        patterns=[".mypy_cache"],
        directory_type=DirectoryType.CACHE,
        risk_level=RiskLevel.SAFE,
        action=RecommendedAction.CAN_DELETE,
        reason="mypy cache - safe to delete",
        confidence=0.98,
    ),
    Rule(
        name="venv",
        patterns=["venv", ".venv", "env", ".env"],
        directory_type=DirectoryType.DEPENDENCY,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.CAN_MOVE,
        reason="Python virtual environment - consider moving to another drive",
        confidence=0.85,
    ),
    Rule(
        name="conda_env",
        patterns=[".conda", "conda", "miniconda", "anaconda"],
        directory_type=DirectoryType.DEPENDENCY,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.CAN_MOVE,
        reason="Conda environment - consider moving to another drive",
        confidence=0.85,
    ),
]

# Build outputs - usually safe to delete
BUILD_RULES = [
    Rule(
        name="build_output",
        patterns=["build", "dist", "out", "target"],
        directory_type=DirectoryType.BUILD,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Build output - can be regenerated",
        confidence=0.80,
    ),
    Rule(
        name="nextjs_build",
        patterns=[".next"],
        directory_type=DirectoryType.BUILD,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Next.js build output - can be regenerated",
        confidence=0.95,
    ),
    Rule(
        name="pyinstaller_cache",
        patterns=["pyinstaller"],
        directory_type=DirectoryType.BUILD,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="PyInstaller build cache - safe to delete",
        confidence=0.90,
    ),
]

# Temporary files - safe to delete
TEMP_RULES = [
    Rule(
        name="temp_files",
        patterns=["Temp", "temp", "tmp", ".tmp"],
        directory_type=DirectoryType.TEMP,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Temporary files - safe to delete",
        confidence=0.85,
    ),
]

# Log files - usually safe to delete
LOG_RULES = [
    Rule(
        name="log_files",
        patterns=["logs", "log", ".log"],
        directory_type=DirectoryType.LOG,
        risk_level=RiskLevel.LOW,
        action=RecommendedAction.CAN_DELETE,
        reason="Log files - usually safe to delete",
        confidence=0.80,
    ),
]

# System/application data - caution required
SYSTEM_RULES = [
    Rule(
        name="git_directory",
        patterns=[".git"],
        directory_type=DirectoryType.SYSTEM,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="Git repository data - DO NOT DELETE (will lose history)",
        confidence=0.99,
    ),
    Rule(
        name="vscode_data",
        patterns=[".vscode"],
        directory_type=DirectoryType.CONFIG,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.KEEP,
        reason="VS Code settings - recommend keeping",
        confidence=0.90,
    ),
    Rule(
        name="docker_data",
        patterns=["docker", "Docker"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.REVIEW,
        reason="Docker data - review before deleting (may contain images/containers)",
        confidence=0.70,
    ),
    Rule(
        name="microsoft_data",
        patterns=["Microsoft"],
        directory_type=DirectoryType.SYSTEM,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="Microsoft/Windows system data - do not delete",
        confidence=0.95,
    ),
    Rule(
        name="onedrive",
        patterns=["OneDrive"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="OneDrive sync data - do not delete",
        confidence=0.95,
    ),
]

# User data - keep
USER_DATA_RULES = [
    Rule(
        name="documents",
        patterns=["Documents", "documents"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="User documents - keep",
        confidence=0.95,
    ),
    Rule(
        name="desktop",
        patterns=["Desktop", "desktop"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="Desktop files - keep",
        confidence=0.95,
    ),
    Rule(
        name="downloads",
        patterns=["Downloads", "downloads"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="Downloads - review contents before cleaning",
        confidence=0.85,
    ),
    Rule(
        name="projects",
        patterns=["projects", "Projects", "code", "Code", "programming", "Programming"],
        directory_type=DirectoryType.PROJECT,
        risk_level=RiskLevel.HIGH,
        action=RecommendedAction.KEEP,
        reason="User projects - keep",
        confidence=0.85,
    ),
]

# Cloud/IM data - review needed
CLOUD_RULES = [
    Rule(
        name="wechat",
        patterns=["WeChat", "wechat", "微信"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="WeChat data - may contain chat history and files",
        confidence=0.80,
    ),
    Rule(
        name="qq",
        patterns=["QQ", "Tencent", "腾讯"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="QQ/Tencent data - may contain chat history",
        confidence=0.80,
    ),
    Rule(
        name="feishu",
        patterns=["Feishu", "Lark", "飞书", "LarkShell"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="Feishu data - may contain documents and chat history",
        confidence=0.80,
    ),
    Rule(
        name="dingtalk",
        patterns=["DingTalk", "钉钉"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="DingTalk data - may contain work files",
        confidence=0.80,
    ),
    Rule(
        name="baidu_pan",
        patterns=["BaiduNetdisk", "baidu"],
        directory_type=DirectoryType.DATA,
        risk_level=RiskLevel.MEDIUM,
        action=RecommendedAction.REVIEW,
        reason="Baidu Pan data - review before cleaning",
        confidence=0.75,
    ),
]

# All built-in rules in priority order
BUILTIN_RULES: list[Rule] = (
    SYSTEM_RULES  # Check system first (highest risk)
    + USER_DATA_RULES  # Then user data
    + CLOUD_RULES  # Cloud/IM data
    + DEPENDENCY_RULES  # Dependencies (can delete/move)
    + BUILD_RULES  # Build outputs
    + CACHE_RULES  # Caches
    + TEMP_RULES  # Temp files
    + LOG_RULES  # Logs
)
