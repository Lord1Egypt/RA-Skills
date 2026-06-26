#!/usr/bin/env python3
"""
GeeLark Cloud Phone - Error Code Definitions

Structured error codes for better diagnostics and troubleshooting.
Used by doctor.py, boot_and_connect(), and other scripts.

Usage:
    from scripts.error_codes import ErrorCode, classify_error
    
    # Raise structured error
    raise ErrorCode.ENV_DEPENDENCY_MISSING("requests not installed")
    
    # Classify exception
    error = classify_error(exception)
    print(error.code, error.message, error.recommendation)
"""


# ============================================
# Error Code Definitions
# ============================================
class ErrorCode:
    """Structured error codes with recommendations"""
    
    # Environment & Dependencies
    ENV_DEPENDENCY_MISSING = "ENV_DEPENDENCY_MISSING"
    
    # Network & DNS
    NETWORK_DNS_FAILED = "NETWORK_DNS_FAILED"
    
    # GeeLark API
    GEELARK_API_FAILED = "GEELARK_API_FAILED"
    
    # Phone Lifecycle
    PHONE_START_TIMEOUT = "PHONE_START_TIMEOUT"
    PHONE_STOP_TIMEOUT = "PHONE_STOP_TIMEOUT"
    PHONE_STATUS_UNKNOWN = "PHONE_STATUS_UNKNOWN"
    
    # ADB
    ADB_NOT_FOUND = "ADB_NOT_FOUND"
    ADB_CONNECT_FAILED = "ADB_CONNECT_FAILED"
    ADB_AUTH_FAILED = "ADB_AUTH_FAILED"
    
    # GLogin
    GLOGIN_REQUIRED = "GLOGIN_REQUIRED"
    GLOGIN_FAILED = "GLOGIN_FAILED"
    
    # uiautomator2
    UIAUTOMATOR_TIMEOUT = "UIAUTOMATOR_TIMEOUT"
    UIAUTOMATOR_CONNECT_FAILED = "UIAUTOMATOR_CONNECT_FAILED"
    UIAUTOMATOR_DUMP_FAILED = "UIAUTOMATOR_DUMP_FAILED"
    
    # App Installation
    APP_INSTALL_CANDIDATE_AMBIGUOUS = "APP_INSTALL_CANDIDATE_AMBIGUOUS"
    APP_INSTALL_FAILED = "APP_INSTALL_FAILED"
    
    # Balance & Billing
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    
    # Generic
    CONFIG_LOAD_FAILED = "CONFIG_LOAD_FAILED"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


# ============================================
# Error Code Metadata
# ============================================
ERROR_METADATA = {
    ErrorCode.ENV_DEPENDENCY_MISSING: {
        "description": "Required dependency (Python package, adb, etc.) is not installed",
        "recommendation": "Install missing dependencies:\n"
                         "  python3 -m venv .venv\n"
                         "  source .venv/bin/activate\n"
                         "  pip install requests uiautomator2\n"
                         "  brew install android-platform-tools  # macOS",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.NETWORK_DNS_FAILED: {
        "description": "Cannot resolve DNS or connect to GeeLark API",
        "recommendation": "Check network connectivity and DNS settings:\n"
                         "  1. Verify internet connection\n"
                         "  2. Check DNS resolution: nslookup api.geelark.com\n"
                         "  3. Verify baseUrl in assets/config.json\n"
                         "  4. Check firewall/proxy settings",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.GEELARK_API_FAILED: {
        "description": "GeeLark API call failed or returned error",
        "recommendation": "Check API configuration and authentication:\n"
                         "  1. Verify token in assets/config.json\n"
                         "  2. Run: python scripts/init_config.py\n"
                         "  3. Check API rate limits\n"
                         "  4. Review error message from API response",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.PHONE_START_TIMEOUT: {
        "description": "Cloud phone did not start within timeout period",
        "recommendation": "Phone startup timed out:\n"
                         "  1. Check account balance (wallet())\n"
                         "  2. Verify phone ID is correct\n"
                         "  3. Check GeeLark service status\n"
                         "  4. Try again after a few minutes",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.PHONE_STOP_TIMEOUT: {
        "description": "Cloud phone did not stop within timeout period",
        "recommendation": "Phone stop timed out:\n"
                         "  1. Wait a few minutes and retry\n"
                         "  2. Check phone status via API\n"
                         "  3. Contact GeeLark support if persistent",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.PHONE_STATUS_UNKNOWN: {
        "description": "Cannot determine phone status",
        "recommendation": "Check phone status:\n"
                         "  1. Verify phone ID is correct\n"
                         "  2. Check API connectivity\n"
                         "  3. List phones: python scripts/geelark_boot_helper.py",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.ADB_NOT_FOUND: {
        "description": "ADB (Android Debug Bridge) not found in PATH",
        "recommendation": "Install ADB:\n"
                         "  macOS:   brew install android-platform-tools\n"
                         "  Ubuntu:  sudo apt install adb\n"
                         "  Windows: winget install Google.AndroidSDK",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.ADB_CONNECT_FAILED: {
        "description": "Cannot connect to ADB device",
        "recommendation": "Check ADB connection:\n"
                         "  1. Ensure cloud phone is started (boot_and_connect())\n"
                         "  2. Verify ADB is enabled for the phone\n"
                         "  3. Check ADB version: adb version\n"
                         "  4. List devices: adb devices",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.ADB_AUTH_FAILED: {
        "description": "ADB authentication failed (glogin)",
        "recommendation": "Re-authenticate with ADB:\n"
                         "  1. Get ADB credentials from boot_and_connect()\n"
                         "  2. Run: adb -s <ip:port> shell glogin <password>\n"
                         "  3. Verify credentials are correct",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.GLOGIN_REQUIRED: {
        "description": "GLogin authentication required before using ADB",
        "recommendation": "Run glogin after connecting:\n"
                         "  adb -s <ip:port> shell glogin <password>\n"
                         "  Password is returned by boot_and_connect()",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.GLOGIN_FAILED: {
        "description": "GLogin authentication failed",
        "recommendation": "Check glogin credentials:\n"
                         "  1. Verify password from boot_and_connect()\n"
                         "  2. Ensure phone is running\n"
                         "  3. Try rebooting the phone",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.UIAUTOMATOR_TIMEOUT: {
        "description": "uiautomator2 operation timed out",
        "recommendation": "Check device responsiveness:\n"
                         "  1. Verify device is connected: adb devices\n"
                         "  2. Run smoke test: python scripts/ui_smoke_test.py <serial>\n"
                         "  3. Check if UIAutomation agent is running on device\n"
                         "  4. Try reconnecting: uiautomator2.connect()",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.UIAUTOMATOR_CONNECT_FAILED: {
        "description": "Cannot connect to uiautomator2 device",
        "recommendation": "Check uiautomator2 connection:\n"
                         "  1. Ensure ADB is connected first\n"
                         "  2. Verify serial format: ip:port\n"
                         "  3. Check firewall allows connection\n"
                         "  4. Run: python scripts/ui_smoke_test.py <serial>",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.UIAUTOMATOR_DUMP_FAILED: {
        "description": "UI hierarchy dump failed",
        "recommendation": "Check UI automation:\n"
                         "  1. Verify device is responsive\n"
                         "  2. Check if app is in foreground\n"
                         "  3. Try: d.info to get basic device info\n"
                         "  4. Run smoke test for detailed diagnostics",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.APP_INSTALL_CANDIDATE_AMBIGUOUS: {
        "description": "Multiple app candidates found, cannot auto-select",
        "recommendation": "Specify app more precisely:\n"
                         "  1. Use --exclude flag: --exclude Lite\n"
                         "  2. Provide direct --version-id\n"
                         "  3. Search with more specific --name",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.APP_INSTALL_FAILED: {
        "description": "App installation failed",
        "recommendation": "Check installation:\n"
                         "  1. Verify appVersionId is correct\n"
                         "  2. Check phone has sufficient storage\n"
                         "  3. Check account balance\n"
                         "  4. Review API error message",
        "severity": "warning",
        "actionable": True
    },
    
    ErrorCode.INSUFFICIENT_BALANCE: {
        "description": "Account balance insufficient for operation",
        "recommendation": "Recharge account:\n"
                         "  1. Check balance: wallet()\n"
                         "  2. Add funds via GeeLark dashboard\n"
                         "  3. Check for gift money or time credits",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.CONFIG_LOAD_FAILED: {
        "description": "Failed to load configuration from assets/config.json",
        "recommendation": "Initialize configuration:\n"
                         "  1. Run: python scripts/init_config.py\n"
                         "  2. Verify assets/config.json exists\n"
                         "  3. Check file permissions: chmod 600 assets/config.json",
        "severity": "critical",
        "actionable": True
    },
    
    ErrorCode.UNEXPECTED_ERROR: {
        "description": "Unexpected error occurred",
        "recommendation": "Check error details and logs:\n"
                         "  1. Review error message and stack trace\n"
                         "  2. Check logs in logs/cloudphone/\n"
                         "  3. Run doctor: python scripts/doctor.py\n"
                         "  4. Report issue if persistent",
        "severity": "error",
        "actionable": True
    }
}


# ============================================
# Error Classification Helper
# ============================================
class StructuredError:
    """Structured error with code, message, and recommendation"""
    
    def __init__(self, code: str, message: str = None, recommendation: str = None):
        self.code = code
        self.message = message or ERROR_METADATA.get(code, {}).get("description", "")
        self.recommendation = recommendation or ERROR_METADATA.get(code, {}).get("recommendation", "")
        self.severity = ERROR_METADATA.get(code, {}).get("severity", "error")
        self.actionable = ERROR_METADATA.get(code, {}).get("actionable", False)
    
    def __str__(self):
        return f"[{self.code}] {self.message}\n\n💡 Recommendation:\n{self.recommendation}"
    
    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "recommendation": self.recommendation,
            "severity": self.severity,
            "actionable": self.actionable
        }


def classify_error(exception: Exception) -> StructuredError:
    """
    Classify an exception into a structured error code.
    
    Args:
        exception: Exception to classify
    
    Returns:
        StructuredError with code and recommendation
    """
    error_msg = str(exception).lower()
    error_type = type(exception).__name__
    
    # ImportError / ModuleNotFoundError
    if error_type in ("ImportError", "ModuleNotFoundError"):
        return StructuredError(ErrorCode.ENV_DEPENDENCY_MISSING, str(exception))
    
    # FileNotFoundError for config
    if error_type == "FileNotFoundError" and "config" in error_msg:
        return StructuredError(ErrorCode.CONFIG_LOAD_FAILED, str(exception))
    
    # Connection errors
    if "connection" in error_msg or "connect" in error_msg:
        if "adb" in error_msg:
            return StructuredError(ErrorCode.ADB_CONNECT_FAILED, str(exception))
        elif "uiautomator" in error_msg or "u2" in error_msg:
            return StructuredError(ErrorCode.UIAUTOMATOR_CONNECT_FAILED, str(exception))
        else:
            return StructuredError(ErrorCode.NETWORK_DNS_FAILED, str(exception))
    
    # Timeout errors
    if "timeout" in error_msg or error_type == "TimeoutError":
        if "uiautomator" in error_msg or "dump" in error_msg:
            return StructuredError(ErrorCode.UIAUTOMATOR_TIMEOUT, str(exception))
        elif "phone" in error_msg or "start" in error_msg:
            return StructuredError(ErrorCode.PHONE_START_TIMEOUT, str(exception))
        else:
            return StructuredError(ErrorCode.UNEXPECTED_ERROR, str(exception))
    
    # Authentication errors
    if "auth" in error_msg or "login" in error_msg or "glogin" in error_msg:
        return StructuredError(ErrorCode.GLOGIN_FAILED, str(exception))
    
    # Balance errors
    if "balance" in error_msg or "insufficient" in error_msg:
        return StructuredError(ErrorCode.INSUFFICIENT_BALANCE, str(exception))
    
    # Default: unexpected error
    return StructuredError(ErrorCode.UNEXPECTED_ERROR, str(exception))


# ============================================
# Convenience Functions
# ============================================
def raise_error(code: str, message: str = None):
    """Raise a structured error as RuntimeError"""
    error = StructuredError(code, message)
    raise RuntimeError(str(error))


def log_error(error: StructuredError, logger=None):
    """Log structured error"""
    if logger:
        logger.error(error.code, error.message)
    print(f"❌ [{error.code}] {error.message}", flush=True)
    if error.actionable:
        print(f"💡 {error.recommendation}", flush=True)


if __name__ == "__main__":
    # Test error classification
    print("=" * 70)
    print("🧪 Testing Error Classification")
    print("=" * 70)
    
    test_exceptions = [
        ImportError("No module named 'requests'"),
        FileNotFoundError("Config file not found: config.json"),
        ConnectionError("Failed to connect to adb"),
        TimeoutError("uiautomator2 dump timed out"),
        Exception("Unknown error occurred")
    ]
    
    for exc in test_exceptions:
        print(f"\n📝 Exception: {type(exc).__name__}: {exc}")
        error = classify_error(exc)
        print(f"  → Code: {error.code}")
        print(f"  → Severity: {error.severity}")
        print(f"  → Actionable: {error.actionable}")
    
    print("\n" + "=" * 70)
    print("✅ Error classification tests completed")
    print("=" * 70)
