"""Tests for label management commands (2 operations)."""

from __future__ import annotations

from blog_manager import labels


class TestListLabels:
    def test_path(self, mock_client):
        labels.list_labels(mock_client)
        mock_client.get.assert_called_once_with("/api/lables")

    def test_kind(self, mock_client):
        _, kind = labels.list_labels(mock_client)
        assert kind == "labels_list"


class TestCreateLabel:
    def test_payload(self, mock_client):
        labels.create_label(mock_client, lname="技术")
        mock_client.post.assert_called_once_with(
            "/api/lables", json={"lname": "技术"}
        )

    def test_kind(self, mock_client):
        _, kind = labels.create_label(mock_client, lname="x")
        assert kind == "label_create"
