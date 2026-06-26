"""WebSocket listener config: webhook endpoints + routing rules + routing modes + E2EE transparent handling.

[INPUT]: Environment variables, JSON config file, settings.json (unified config)
[OUTPUT]: ListenerConfig, RoutingRules, ROUTING_MODES using current-protocol
          E2EE ignore types
[POS]: Configuration module for ws_listener.py, defines routing rules, webhook targets, and E2EE handling parameters

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from utils.config import SDKConfig

logger = logging.getLogger(__name__)

# Routing mode constants
ROUTING_MODES = ("agent-all", "smart", "wake-all")


@dataclass(frozen=True)
class RoutingRules:
    """Message routing rules.

    Controls how messages are classified into agent (high priority) or wake (low priority) mode.
    Only effective when mode="smart".
    """

    # Agent mode trigger conditions
    whitelist_dids: frozenset[str] = frozenset()
    private_always_agent: bool = True
    command_prefix: str = "/"
    keywords: tuple[str, ...] = ("urgent", "approval", "payment", "alert")
    bot_names: tuple[str, ...] = ()

    # Blacklist (drop directly, do not forward)
    blacklist_dids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ListenerConfig:
    """WebSocket listener configuration."""

    # Routing mode: agent-all / smart / wake-all
    mode: str = "smart"

    # Dual webhook endpoints (OpenClaw Gateway default port 18789)
    agent_webhook_url: str = "http://127.0.0.1:18789/hooks/agent"
    wake_webhook_url: str = "http://127.0.0.1:18789/hooks/wake"
    webhook_token: str = ""  # Must match OpenClaw hooks.token

    # Agent webhook additional parameters
    agent_hook_name: str = "IM"  # name field for OpenClaw hooks/agent

    # Routing rules (only effective when mode="smart")
    routing: RoutingRules = field(default_factory=RoutingRules)

    # Current E2EE protocol message types (intercepted by the E2EE handler
    # before classify_message; legacy types are dropped by ws_listener guards).
    ignore_types: frozenset[str] = frozenset({
        "e2ee_init", "e2ee_ack", "e2ee_msg", "e2ee_rekey", "e2ee_error",
    })

    # E2EE transparent handling (always enabled)
    e2ee_save_interval: float = 30.0        # E2EE state save interval (seconds)
    e2ee_decrypt_fail_action: str = "drop"  # Decryption failure action: "drop" / "forward_raw"

    # Reconnect backoff
    reconnect_base_delay: float = 1.0
    reconnect_max_delay: float = 60.0

    # Heartbeat interval (must be < ws_idle_timeout=300s)
    heartbeat_interval: float = 120.0

    def __post_init__(self) -> None:
        if self.mode not in ROUTING_MODES:
            raise ValueError(
                f"mode must be one of {ROUTING_MODES}, got: {self.mode!r}"
            )
        for url in (self.agent_webhook_url, self.wake_webhook_url):
            if not (url.startswith("http://127.0.0.1")
                    or url.startswith("http://localhost")):
                raise ValueError(f"webhook_url must be localhost: {url}")
        if self.e2ee_decrypt_fail_action not in ("drop", "forward_raw"):
            raise ValueError(
                f"e2ee_decrypt_fail_action must be 'drop' or 'forward_raw', "
                f"got: {self.e2ee_decrypt_fail_action!r}"
            )

    @classmethod
    def load(
        cls,
        config_path: str | None = None,
        mode_override: str | None = None,
    ) -> ListenerConfig:
        """Load configuration from JSON file + settings.json + environment variables.

        Priority: CLI --mode > environment variables > config file > settings.json > defaults.

        When config_path is None, automatically reads <DATA_DIR>/settings.json
        and extracts the "listener" sub-object. Supports both unified format
        (with "listener" key) and legacy flat format.

        Args:
            config_path: JSON config file path. Falls back to settings.json when None.
            mode_override: Mode override value passed from CLI.

        Returns:
            ListenerConfig instance.
        """
        logger.info(
            "Loading listener config config_path=%s mode_override=%s",
            config_path,
            mode_override,
        )
        data: dict = {}

        # 1. Read from config file or settings.json
        if config_path:
            path = Path(config_path)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                # Support unified format: extract "listener" sub-object
                if "listener" in data:
                    data = data["listener"]
        else:
            # Auto-read from <DATA_DIR>/config/settings.json
            settings_path = SDKConfig().data_dir / "config" / "settings.json"
            if settings_path.exists():
                settings = json.loads(settings_path.read_text(encoding="utf-8"))
                if "listener" in settings:
                    data = settings["listener"]

        # 2. Environment variable overrides
        env_agent = os.environ.get("LISTENER_AGENT_WEBHOOK_URL")
        env_wake = os.environ.get("LISTENER_WAKE_WEBHOOK_URL")
        env_token = os.environ.get("LISTENER_WEBHOOK_TOKEN")
        env_mode = os.environ.get("LISTENER_MODE")
        if env_agent:
            data["agent_webhook_url"] = env_agent
        if env_wake:
            data["wake_webhook_url"] = env_wake
        if env_token:
            data["webhook_token"] = env_token
        if env_mode:
            data["mode"] = env_mode

        # 3. CLI arguments take highest priority
        if mode_override:
            data["mode"] = mode_override

        # 4. Build RoutingRules
        routing_data = data.pop("routing", {})
        routing = RoutingRules(
            whitelist_dids=frozenset(routing_data.get("whitelist_dids", [])),
            private_always_agent=routing_data.get("private_always_agent", True),
            command_prefix=routing_data.get("command_prefix", "/"),
            keywords=tuple(routing_data.get("keywords", ("urgent", "approval", "payment", "alert"))),
            bot_names=tuple(routing_data.get("bot_names", ())),
            blacklist_dids=frozenset(routing_data.get("blacklist_dids", [])),
        )

        # 5. Build ListenerConfig
        result = cls(
            mode=data.get("mode", "smart"),
            agent_webhook_url=data.get("agent_webhook_url", "http://127.0.0.1:18789/hooks/agent"),
            wake_webhook_url=data.get("wake_webhook_url", "http://127.0.0.1:18789/hooks/wake"),
            webhook_token=data.get("webhook_token", ""),
            agent_hook_name=data.get("agent_hook_name", "IM"),
            routing=routing,
            e2ee_save_interval=float(data.get("e2ee_save_interval", 30.0)),
            e2ee_decrypt_fail_action=data.get("e2ee_decrypt_fail_action", "drop"),
        )
        logger.info(
            "Loaded listener config mode=%s agent_webhook=%s wake_webhook=%s",
            result.mode,
            result.agent_webhook_url,
            result.wake_webhook_url,
        )
        return result


__all__ = ["ListenerConfig", "ROUTING_MODES", "RoutingRules"]
