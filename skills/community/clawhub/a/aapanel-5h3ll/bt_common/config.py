# /// script
# dependencies = [
#   "pyyaml>=6.0",
# ]
# ///
"""
Configuration Management Module
Loads configuration from environment variables or YAML files, supports global and local configs
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import yaml


# aaPanel minimum version requirement
MIN_PANEL_VERSION = "9.0.0"

# Global config file path
GLOBAL_CONFIG_DIR = Path.home() / ".openclaw"
GLOBAL_CONFIG_FILE = GLOBAL_CONFIG_DIR / "bt-skills.yaml"


@dataclass
class ThresholdConfig:
    """Alert threshold config"""

    cpu: int = 80
    memory: int = 85
    disk: int = 90


@dataclass
class GlobalConfig:
    """Global config"""

    retry_count: int = 3
    retry_delay: int = 1000
    concurrency: int = 3
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)


@dataclass
class ServerConfig:
    """Server config"""

    name: str
    host: str
    token: str
    timeout: int = 10000
    enabled: bool = True
    verify_ssl: bool = True  # SSL certificate verification enabled by default


@dataclass
class Config:
    """Full config"""

    servers: list[ServerConfig] = field(default_factory=list)
    global_config: GlobalConfig = field(default_factory=GlobalConfig)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create config from dict"""
        servers = []
        for s in data.get("servers", []):
            servers.append(
                ServerConfig(
                    name=s["name"],
                    host=s["host"],
                    token=s["token"],
                    timeout=s.get("timeout", 10000),
                    enabled=s.get("enabled", True),
                    verify_ssl=s.get("verify_ssl", True),  # Load SSL verification config
                )
            )

        global_data = data.get("global", {})
        thresholds_data = global_data.get("thresholds", {})
        thresholds = ThresholdConfig(
            cpu=thresholds_data.get("cpu", 80),
            memory=thresholds_data.get("memory", 85),
            disk=thresholds_data.get("disk", 90),
        )
        global_config = GlobalConfig(
            retry_count=global_data.get("retryCount", 3),
            retry_delay=global_data.get("retryDelay", 1000),
            concurrency=global_data.get("concurrency", 3),
            thresholds=thresholds,
        )

        return cls(servers=servers, global_config=global_config)


def get_global_config_path() -> Path:
    """
    Get global config file path

    Returns:
        Global config file path
    """
    return GLOBAL_CONFIG_FILE


def ensure_global_config_dir() -> Path:
    """
    Ensure global config directory exists

    Returns:
        Global config directory path
    """
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return GLOBAL_CONFIG_DIR


def create_default_global_config() -> Path:
    """
    Create default global config file

    Returns:
        Created config file path
    """
    ensure_global_config_dir()

    default_config = f"""# aaPanel Log Inspection Skill Package Config
# Config file path: {GLOBAL_CONFIG_FILE}
#
# This config file can be read and modified by AI tools
# aaPanel version requirement: >= {MIN_PANEL_VERSION}

servers:
  # Server config example
  # - name: "prod-01"
  #   host: "https://your-panel.com:8888"
  #   token: "YOUR_API_TOKEN"
  #   timeout: 10000
  #   enabled: true
  #   verify_ssl: true  # Whether to verify SSL certificate, default is true
  #                     # Set to false if panel uses self-signed certificate

global:
  # Request retry count
  retryCount: 3
  # Retry delay (milliseconds)
  retryDelay: 1000
  # Concurrent request limit
  concurrency: 3
  # Alert threshold config
  thresholds:
    cpu: 80        # CPU usage rate alert threshold (%)
    memory: 85     # Memory usage rate alert threshold (%)
    disk: 90       # Disk usage rate alert threshold (%)
"""

    if not GLOBAL_CONFIG_FILE.exists():
        GLOBAL_CONFIG_FILE.write_text(default_config, encoding="utf-8")

    return GLOBAL_CONFIG_FILE


def find_config_file() -> Optional[str]:
    """
    Find config file

    Search order:
    1. BT_CONFIG_PATH environment variable
    2. Global config file ~/.openclaw/bt-skills.yaml
    3. config/servers.local.yaml in current directory
    4. config/servers.yaml in current directory
    """
    # 1. Environment variable
    env_path = os.environ.get("BT_CONFIG_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    # 2. Global config file
    if GLOBAL_CONFIG_FILE.exists():
        return str(GLOBAL_CONFIG_FILE)

    # 3. Local config
    local_path = Path("config/servers.local.yaml")
    if local_path.exists():
        return str(local_path)

    # 4. Default config
    default_path = Path("config/servers.yaml")
    if default_path.exists():
        return str(default_path)

    return None


def load_config(config_path: Optional[str] = None) -> dict[str, Any]:
    """
    Load config file

    Args:
        config_path: Config file path, auto-search when None

    Returns:
        Config dictionary

    Raises:
        FileNotFoundError: Config file does not exist
        yaml.YAMLError: YAML parse error
    """
    if config_path is None:
        config_path = find_config_file()

    if config_path is None:
        # Try to create default global config
        try:
            config_path = str(create_default_global_config())
        except Exception:
            pass

    if config_path is None:
        raise FileNotFoundError(
            f"Config file not found.\n"
            f"Solutions:\n"
            f"1. Set BT_CONFIG_PATH environment variable\n"
            f"2. Create global config file: {GLOBAL_CONFIG_FILE}\n"
            f"3. Create local config file: config/servers.local.yaml"
        )

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config or {}


def load_config_object(config_path: Optional[str] = None) -> Config:
    """
    Load config and return Config object

    Args:
        config_path: Config file path

    Returns:
        Config object
    """
    data = load_config(config_path)
    return Config.from_dict(data)


def get_servers(config_path: Optional[str] = None) -> list[ServerConfig]:
    """
    Get server list

    Args:
        config_path: Config file path

    Returns:
        Server configuration list
    """
    config = load_config_object(config_path)
    return [s for s in config.servers if s.enabled]


def get_thresholds(config_path: Optional[str] = None) -> ThresholdConfig:
    """
    Get alert threshold config

    Args:
        config_path: Config file path

    Returns:
        Threshold config
    """
    config = load_config_object(config_path)
    return config.global_config.thresholds


def normalize_host(host: str) -> str:
    """
    Normalize panel address

    Handle various input formats:
    - 192.168.69.154:8888 -> https://192.168.69.154:8888
    - 192.168.69.154:8888/soft/plugin -> https://192.168.69.154:8888
    - panel.example.com:8888 -> https://panel.example.com:8888
    - https://panel.example.com:8888/ -> https://panel.example.com:8888
    - http://panel.example.com:8888 -> http://panel.example.com:8888

    Args:
        host: User input panel address

    Returns:
        Normalized URL
    """
    host = host.strip()

    # If no scheme, add https://
    if not host.startswith(("http://", "https://")):
        # Check if starts with IP or domain (may contain port or path)
        host = "https://" + host

    # Parse URL
    parsed = urlparse(host)

    # Remove path part, keep only scheme://netloc
    # netloc contains host:port
    normalized = f"{parsed.scheme}://{parsed.netloc}"

    return normalized


def validate_host(host: str) -> tuple[bool, str]:
    """
    Validate panel address

    Args:
        host: Panel address

    Returns:
        (is_valid, error message or normalized address)
    """
    try:
        normalized = normalize_host(host)
        parsed = urlparse(normalized)

        # Check for valid netloc
        if not parsed.netloc:
            return False, "Invalid panel address: missing hostname"

        # Check port
        if ":" in parsed.netloc:
            _, port_str = parsed.netloc.rsplit(":", 1)
            try:
                port = int(port_str)
                if port < 1 or port > 65535:
                    return False, f"Invalid port number: {port}"
            except ValueError:
                return False, f"Invalid port number: {port_str}"

        return True, normalized

    except Exception as e:
        return False, f"Invalid panel address: {str(e)}"


def add_server(name: str, host: str, token: str, timeout: int = 10000, enabled: bool = True, verify_ssl: bool = True, config_path: Optional[str] = None) -> bool:
    """
    Add server configuration

    Args:
        name: Server name
        host: Panel address (auto-normalized)
        token: API Token
        timeout: Timeout
        enabled: Whether enabled
        verify_ssl: Whether to verify SSL certificate
        config_path: Config file path

    Returns:
        Whether addition succeeded

    Raises:
        ValueError: Invalid address format
    """
    # Normalize address
    is_valid, result = validate_host(host)
    if not is_valid:
        raise ValueError(result)
    host = result

    if config_path is None:
        config_path = str(GLOBAL_CONFIG_FILE)

    # Ensure directory exists
    ensure_global_config_dir()

    # Load existing config
    try:
        config = load_config(config_path)
    except FileNotFoundError:
        config = {"servers": [], "global": {}}

    # Check if already exists
    servers = config.get("servers", [])
    for s in servers:
        if s.get("name") == name:
            # Update existing config
            s["host"] = host
            s["token"] = token
            s["timeout"] = timeout
            s["enabled"] = enabled
            s["verify_ssl"] = verify_ssl
            break
    else:
        # Add new config
        servers.append({
            "name": name,
            "host": host,
            "token": token,
            "timeout": timeout,
            "enabled": enabled,
            "verify_ssl": verify_ssl,
        })

    config["servers"] = servers

    # Ensure global config exists
    if "global" not in config:
        config["global"] = {
            "retryCount": 3,
            "retryDelay": 1000,
            "concurrency": 3,
            "thresholds": {"cpu": 80, "memory": 85, "disk": 90},
        }

    # Save config
    path = Path(config_path)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def remove_server(name: str, config_path: Optional[str] = None) -> bool:
    """
    Remove server configuration

    Args:
        name: Server name
        config_path: Config file path

    Returns:
        Whether removal succeeded
    """
    if config_path is None:
        config_path = str(GLOBAL_CONFIG_FILE)

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        return False

    servers = config.get("servers", [])
    original_count = len(servers)
    config["servers"] = [s for s in servers if s.get("name") != name]

    if len(config["servers"]) == original_count:
        return False  # Not found

    # Save config
    path = Path(config_path)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def update_thresholds(cpu: Optional[int] = None, memory: Optional[int] = None, disk: Optional[int] = None, config_path: Optional[str] = None) -> bool:
    """
    Update alert threshold config

    Args:
        cpu: CPU threshold
        memory: Memory threshold
        disk: Disk threshold
        config_path: Config file path

    Returns:
        Whether update succeeded
    """
    if config_path is None:
        config_path = str(GLOBAL_CONFIG_FILE)

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        config = {"servers": [], "global": {}}

    if "global" not in config:
        config["global"] = {}

    if "thresholds" not in config["global"]:
        config["global"]["thresholds"] = {"cpu": 80, "memory": 85, "disk": 90}

    if cpu is not None:
        config["global"]["thresholds"]["cpu"] = cpu
    if memory is not None:
        config["global"]["thresholds"]["memory"] = memory
    if disk is not None:
        config["global"]["thresholds"]["disk"] = disk

    # Save config
    path = Path(config_path)
    ensure_global_config_dir()
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return True


def get_config_info() -> dict:
    """
    Get config info (for AI reading)

    Returns:
        Config info dictionary
    """
    config_path = find_config_file()

    info = {
        "min_panel_version": MIN_PANEL_VERSION,
        "global_config_path": str(GLOBAL_CONFIG_FILE),
        "current_config_path": config_path,
        "config_exists": config_path is not None and Path(config_path).exists(),
        "env_var": "BT_CONFIG_PATH",
        "env_var_value": os.environ.get("BT_CONFIG_PATH"),
    }

    if config_path and Path(config_path).exists():
        try:
            config = load_config(config_path)
            info["server_count"] = len(config.get("servers", []))
            info["servers"] = [
                {"name": s.get("name"), "host": s.get("host"), "enabled": s.get("enabled", True), "verify_ssl": s.get("verify_ssl", True)}
                for s in config.get("servers", [])
            ]
            info["thresholds"] = config.get("global", {}).get("thresholds", {})
        except Exception as e:
            info["error"] = str(e)

    return info
