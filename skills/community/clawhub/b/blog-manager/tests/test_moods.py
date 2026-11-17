"""Tests for mood management commands (3 operations)."""

from __future__ import annotations

from blog_manager import moods


class TestListMoods:
    def test_path(self, mock_client):
        moods.list_moods(mock_client)
        mock_client.get.assert_called_once_with("/api/moods")

    def test_kind(self, mock_client):
        _, kind = moods.list_moods(mock_client)
        assert kind == "moods_list"


class TestCreateMood:
    def test_required_content(self, mock_client):
        moods.create_mood(mock_client, content="心情不错")
        mock_client.post.assert_called_once()
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["content"] == "心情不错"

    def test_defaults(self, mock_client):
        moods.create_mood(mock_client, content="c")
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["title"] == ""
        assert payload["src"] == ""

    def test_all_fields(self, mock_client):
        moods.create_mood(mock_client, content="c", title="t", src="/img.jpg")
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload["src"] == "/img.jpg"

    def test_kind(self, mock_client):
        _, kind = moods.create_mood(mock_client, content="x")
        assert kind == "id_response"


class TestDeleteMood:
    def test_path(self, mock_client):
        moods.delete_mood(mock_client, mood_id=4)
        mock_client.delete.assert_called_once_with("/api/moods/4")

    def test_kind(self, mock_client):
        _, kind = moods.delete_mood(mock_client, mood_id=1)
        assert kind == "message_response"
