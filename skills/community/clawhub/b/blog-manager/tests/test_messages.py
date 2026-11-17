"""Tests for message management commands (4 operations)."""

from __future__ import annotations

from blog_manager import messages


class TestListMessages:
    def test_path(self, mock_client):
        messages.list_messages(mock_client)
        mock_client.get.assert_called_once_with("/api/messages")

    def test_kind(self, mock_client):
        _, kind = messages.list_messages(mock_client)
        assert kind == "messages_list"


class TestCreateMessage:
    def test_payload(self, mock_client):
        messages.create_message(mock_client, uid=1, content="hello")
        mock_client.post.assert_called_once_with(
            "/api/messages", json={"uid": 1, "content": "hello"}
        )

    def test_kind(self, mock_client):
        _, kind = messages.create_message(mock_client, uid=1, content="x")
        assert kind == "id_response"


class TestReplyMessage:
    def test_uses_reply_endpoint(self, mock_client):
        messages.reply_message(mock_client, uid=1, mid=3, content="reply")
        mock_client.post.assert_called_once_with(
            "/api/messages/reply",
            json={"uid": 1, "mid": 3, "content": "reply"},
        )

    def test_kind(self, mock_client):
        _, kind = messages.reply_message(mock_client, uid=1, mid=1, content="x")
        assert kind == "id_response"


class TestDeleteMessage:
    def test_path(self, mock_client):
        messages.delete_message(mock_client, message_id=7)
        mock_client.delete.assert_called_once_with("/api/messages/7")

    def test_kind(self, mock_client):
        _, kind = messages.delete_message(mock_client, message_id=1)
        assert kind == "message_response"
