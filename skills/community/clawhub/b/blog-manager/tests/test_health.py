"""Tests for health check command (1 operation)."""

from __future__ import annotations

from blog_manager import health


class TestHealthCheck:
    def test_path_is_root_health(self, mock_client):
        health.health_check(mock_client)
        mock_client.get.assert_called_once_with("/health")

    def test_not_under_api_prefix(self, mock_client):
        health.health_check(mock_client)
        path = mock_client.get.call_args.args[0]
        assert not path.startswith("/api")

    def test_kind(self, mock_client):
        _, kind = health.health_check(mock_client)
        assert kind == "health"
