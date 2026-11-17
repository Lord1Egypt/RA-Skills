"""Tests for user management commands (2 operations)."""

from __future__ import annotations

from blog_manager import users


class TestListUsers:
    def test_path(self, mock_client):
        users.list_users(mock_client)
        mock_client.get.assert_called_once_with("/api/users")

    def test_kind(self, mock_client):
        _, kind = users.list_users(mock_client)
        assert kind == "users_list"


class TestCreateUser:
    def test_required_uname(self, mock_client):
        users.create_user(mock_client, uname="alice")
        mock_client.post.assert_called_once()
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["uname"] == "alice"

    def test_defaults(self, mock_client):
        users.create_user(mock_client, uname="bob")
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["img"] == "img/moren.jpg"
        assert payload["phone"] == ""

    def test_all_fields(self, mock_client):
        users.create_user(
            mock_client, uname="c", phone="123", pwd="p",
            email="e@e.com", img="/a.png",
        )
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["phone"] == "123"

    def test_kind(self, mock_client):
        _, kind = users.create_user(mock_client, uname="x")
        assert kind == "id_response"
