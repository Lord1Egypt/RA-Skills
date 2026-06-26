#!/usr/bin/env python3
"""
Feishu Notifier Core - Production Ready
飞书通知核心模块

Features:
- Secure config handling (env > skill config > default)
- Robust JSON processing with proper escaping
- Automatic retry with exponential backoff
- Structured output (JSON)
- No secrets in logs
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl
from typing import Optional, Dict, Any, Tuple

# API Endpoints
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
TOKEN_ENDPOINT = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
MESSAGE_ENDPOINT = f"{FEISHU_API_BASE}/im/v1/messages"


class FeishuNotifierError(Exception):
    """Base exception for Feishu Notifier"""
    pass


class ConfigError(FeishuNotifierError):
    """Configuration error"""
    pass


class APIError(FeishuNotifierError):
    """API call error"""
    def __init__(self, message: str, code: Optional[int] = None, response: Optional[Dict] = None):
        super().__init__(message)
        self.code = code
        self.response = response


class FeishuConfig:
    """Configuration manager with secure handling"""
    
    def __init__(self):
        self.app_id: Optional[str] = None
        self.app_secret: Optional[str] = None
        self.receive_id: Optional[str] = None
        self.receive_id_type: str = "open_id"
        self.timeout: int = 30
        self.max_retries: int = 3
        self.retry_delay: int = 2
        
    def load(self) -> "FeishuConfig":
        """Load configuration from multiple sources (env > skill config)"""
        # Priority 1: Environment variables
        self.app_id = os.environ.get("FEISHU_APP_ID") or os.environ.get("FEISHU_appId")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET") or os.environ.get("FEISHU_appSecret")
        self.receive_id = os.environ.get("FEISHU_RECEIVE_ID") or os.environ.get("FEISHU_receiveId")
        self.receive_id_type = os.environ.get("FEISHU_RECEIVE_ID_TYPE", "open_id")
        
        if env_timeout := os.environ.get("FEISHU_TIMEOUT"):
            self.timeout = int(env_timeout)
        if env_retries := os.environ.get("FEISHU_MAX_RETRIES"):
            self.max_retries = int(env_retries)
        if env_delay := os.environ.get("FEISHU_RETRY_DELAY"):
            self.retry_delay = int(env_delay)
        
        # Priority 2: OpenClaw skill config (if available)
        self._load_skill_config()
        
        return self
    
    def _load_skill_config(self):
        """Load from OpenClaw skill config file if exists"""
        # Determine skill directory
        skill_dir = os.environ.get("FEISHU_SKILL_DIR", "")
        
        config_paths = [
            # Environment variable (set by run.sh)
            os.path.join(skill_dir, "config.json") if skill_dir else None,
            # OpenClaw standard locations
            os.path.expanduser("~/.openclaw/skills/feishu-relay/config.json"),
            "/etc/openclaw/skills/feishu-relay/config.json",
            # Fallback: relative to current working directory
            "./config.json",
            # Legacy: .env file in skill directory
            os.path.join(skill_dir, ".env") if skill_dir else None,
        ]
        
        # Filter out None values
        config_paths = [p for p in config_paths if p]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    # Only use skill config if env not set
                    if not self.app_id:
                        self.app_id = config.get("appId")
                    if not self.app_secret:
                        self.app_secret = config.get("appSecret")
                    if not self.receive_id:
                        self.receive_id = config.get("receiveId")
                    if "receiveIdType" in config and self.receive_id_type == "open_id":
                        self.receive_id_type = config.get("receiveIdType", "open_id")
                    if "timeout" in config:
                        self.timeout = config.get("timeout", 30)
                    if "maxRetries" in config:
                        self.max_retries = config.get("maxRetries", 3)
                    if "retryDelay" in config:
                        self.retry_delay = config.get("retryDelay", 2)
                    break
                except (json.JSONDecodeError, IOError):
                    continue
    
    def validate(self) -> None:
        """Validate configuration, raise ConfigError if invalid"""
        errors = []
        
        if not self.app_id:
            errors.append("appId is required (set FEISHU_APP_ID env or skill config)")
        elif not self.app_id.startswith("cli_"):
            errors.append(f"appId should start with 'cli_' (got: {self.app_id[:10]}...)")
            
        if not self.app_secret:
            errors.append("appSecret is required (set FEISHU_APP_SECRET env or skill config)")
        elif len(self.app_secret) < 20:
            errors.append("appSecret seems too short (should be ~32+ chars)")
            
        if not self.receive_id:
            errors.append("receiveId is required (set FEISHU_RECEIVE_ID env or skill config)")
            
        valid_id_types = ["open_id", "user_id", "chat_id", "email"]
        if self.receive_id_type not in valid_id_types:
            errors.append(f"receiveIdType must be one of {valid_id_types}, got: {self.receive_id_type}")
        
        if errors:
            raise ConfigError("; ".join(errors))
    
    def to_safe_dict(self) -> Dict[str, Any]:
        """Return config dict with secrets masked (for logging)"""
        return {
            "app_id": self.app_id[:10] + "..." if self.app_id else None,
            "app_secret": "***REDACTED***" if self.app_secret else None,
            "receive_id": self.receive_id[:10] + "..." if self.receive_id else None,
            "receive_id_type": self.receive_id_type,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        }


class FeishuNotifier:
    """Main notifier class with retry logic"""
    
    def __init__(self, config: FeishuConfig):
        self.config = config
        self._token: Optional[str] = None
        self._token_expires: float = 0
        
        # Create SSL context that verifies certificates
        self._ssl_context = ssl.create_default_context()
    
    def _make_request(
        self, 
        url: str, 
        method: str = "GET", 
        headers: Optional[Dict[str, str]] = None,
        data: Optional[bytes] = None,
        retry_count: int = 0
    ) -> Tuple[int, Dict[str, Any]]:
        """Make HTTP request with retry logic"""
        
        req_headers = headers or {}
        req = urllib.request.Request(
            url, 
            data=data, 
            headers=req_headers, 
            method=method
        )
        
        try:
            with urllib.request.urlopen(
                req, 
                timeout=self.config.timeout,
                context=self._ssl_context
            ) as response:
                body = response.read().decode('utf-8')
                return response.status, json.loads(body) if body else {}
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.read() else "{}"
            try:
                error_data = json.loads(body)
            except json.JSONDecodeError:
                error_data = {"error": body}
            return e.code, error_data
            
        except (urllib.error.URLError, TimeoutError) as e:
            if retry_count < self.config.max_retries:
                time.sleep(self.config.retry_delay * (retry_count + 1))
                return self._make_request(url, method, headers, data, retry_count + 1)
            raise APIError(f"Request failed after {self.config.max_retries} retries: {e}")
    
    def get_access_token(self) -> str:
        """Get tenant access token with caching"""
        # Return cached token if still valid (with 60s buffer)
        if self._token and time.time() < self._token_expires - 60:
            return self._token
        
        payload = json.dumps({
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }).encode('utf-8')
        
        headers = {"Content-Type": "application/json"}
        
        status, response = self._make_request(
            TOKEN_ENDPOINT,
            method="POST",
            headers=headers,
            data=payload
        )
        
        if status != 200 or response.get("code", -1) != 0:
            code = response.get("code", "unknown")
            msg = response.get("msg", "Unknown error")
            raise APIError(f"Failed to get access token: {msg} (code: {code})", code, response)
        
        self._token = response.get("tenant_access_token")
        expire = response.get("expire", 7200)
        self._token_expires = time.time() + expire
        
        return self._token
    
    def send_message(
        self, 
        content: str, 
        title: Optional[str] = None,
        receive_id: Optional[str] = None,
        receive_id_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send text message to Feishu"""
        
        token = self.get_access_token()
        
        target_id = receive_id or self.config.receive_id
        target_type = receive_id_type or self.config.receive_id_type
        
        # Build message using proper JSON serialization (no manual escaping)
        message_card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title or "系统通知"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                },
                {
                    "tag": "note",
                    "elements": [
                        {"tag": "plain_text", "content": f"发送时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"}
                    ]
                }
            ]
        }
        
        payload = json.dumps({
            "receive_id": target_id,
            "msg_type": "interactive",
            "content": json.dumps(message_card)
        }).encode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{MESSAGE_ENDPOINT}?receive_id_type={target_type}"
        status, response = self._make_request(url, method="POST", headers=headers, data=payload)
        
        if status != 200 or response.get("code", -1) != 0:
            code = response.get("code", "unknown")
            msg = response.get("msg", "Unknown error")
            raise APIError(f"Failed to send message: {msg} (code: {code})", code, response)
        
        return {
            "success": True,
            "message_id": response.get("data", {}).get("message_id"),
            "create_time": response.get("data", {}).get("create_time")
        }


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Send notifications via Feishu (Lark)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t "Alert" -m "Server CPU high"
  echo "Backup complete" | %(prog)s -t "Daily Backup"
  %(prog)s --test
        """
    )
    
    parser.add_argument("-t", "--title", default="系统通知", help="Message title")
    parser.add_argument("-m", "--message", help="Message content")
    parser.add_argument("-r", "--receive-id", help="Override receive ID")
    parser.add_argument("--receive-id-type", choices=["open_id", "user_id", "chat_id", "email"],
                       help="Override receive ID type")
    parser.add_argument("--test", action="store_true", help="Send test message")
    parser.add_argument("--config", action="store_true", help="Show current config (masked)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--health", action="store_true", help="Health check (for watchdog)")
    
    args = parser.parse_args()
    
    # Load and validate config
    try:
        config = FeishuConfig().load()
        
        if args.config:
            print(json.dumps(config.to_safe_dict(), indent=2, ensure_ascii=False))
            sys.exit(0)
        
        config.validate()
        
    except ConfigError as e:
        result = {
            "success": False,
            "error": "CONFIG_ERROR",
            "message": str(e),
            "hint": "Set FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_RECEIVE_ID environment variables"
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # Determine message content
    message = args.message
    if not message and not args.test:
        if not sys.stdin.isatty():
            message = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)
    
    # Send message
    try:
        notifier = FeishuNotifier(config)
        
        if args.health:
            # Health check for watchdog
            hostname = os.uname().nodename
            result = {
                "success": True,
                "status": "healthy",
                "hostname": hostname,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(0)
        
        if args.test:
            hostname = os.uname().nodename
            title = "🧪 Feishu Notifier Test"
            content = f"**Server**: {hostname}  \n**Status**: Configuration OK  \n**Time**: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            title = args.title
            content = message
        
        result = notifier.send_message(
            content=content,
            title=title,
            receive_id=args.receive_id,
            receive_id_type=args.receive_id_type
        )
        
        # Output result
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✓ Message sent successfully (ID: {result['message_id']})")
        
        sys.exit(0)
        
    except APIError as e:
        result = {
            "success": False,
            "error": "API_ERROR",
            "message": str(e),
            "code": e.code
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(2)
        
    except Exception as e:
        result = {
            "success": False,
            "error": "UNEXPECTED_ERROR",
            "message": str(e)
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(3)


if __name__ == "__main__":
    main()
