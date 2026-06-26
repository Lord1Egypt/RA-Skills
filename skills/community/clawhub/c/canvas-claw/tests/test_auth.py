import os

from canvas_claw.config import RuntimeConfig, load_runtime_config


def test_runtime_config_requires_base_url_and_site_id() -> None:
    config = RuntimeConfig(
        base_url="http://localhost:8000",
        token="token-123",
        site_id=10000,
    )
    assert config.base_url == "http://localhost:8000"
    assert config.token == "token-123"
    assert config.site_id == 10000


def test_load_runtime_config_uses_timeout_and_poll_interval_env(monkeypatch) -> None:
    monkeypatch.setenv("AI_VIDEO_AGENT_BASE_URL", "https://ai.cnvp.cn")
    monkeypatch.setenv("AI_VIDEO_AGENT_TOKEN", "token-123")
    monkeypatch.setenv("AI_VIDEO_AGENT_SITE_ID", "10000")
    monkeypatch.setenv("AI_VIDEO_AGENT_TIMEOUT", "180")
    monkeypatch.setenv("AI_VIDEO_AGENT_POLL_INTERVAL", "3")

    config = load_runtime_config()

    assert config.base_url == "https://ai.cnvp.cn"
    assert config.token == "token-123"
    assert config.site_id == 10000
    assert config.timeout == 180.0
    assert config.poll_interval == 3.0
