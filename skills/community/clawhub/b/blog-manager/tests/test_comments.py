"""Tests for comment management commands (3 operations)."""

from __future__ import annotations

from blog_manager import comments


class TestCreateComment:
    def test_payload(self, mock_client):
        comments.create_comment(mock_client, uid=1, aid=5, content="nice")
        mock_client.post.assert_called_once_with(
            "/api/comments", json={"uid": 1, "aid": 5, "content": "nice"}
        )

    def test_kind(self, mock_client):
        _, kind = comments.create_comment(mock_client, uid=1, aid=1, content="x")
        assert kind == "id_response"


class TestListComments:
    def test_path_with_aid(self, mock_client):
        comments.list_comments(mock_client, aid=5)
        mock_client.get.assert_called_once_with("/api/comments/5")

    def test_kind(self, mock_client):
        _, kind = comments.list_comments(mock_client, aid=1)
        assert kind == "comments_list"


class TestDeleteComment:
    def test_path(self, mock_client):
        comments.delete_comment(mock_client, comment_id=9)
        mock_client.delete.assert_called_once_with("/api/comments/9")

    def test_kind(self, mock_client):
        _, kind = comments.delete_comment(mock_client, comment_id=1)
        assert kind == "message_response"
