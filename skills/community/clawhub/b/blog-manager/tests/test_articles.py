"""Tests for article management commands (7 operations)."""

from __future__ import annotations

from blog_manager import articles


class TestListArticles:
    def test_calls_correct_path_and_params(self, mock_client):
        articles.list_articles(mock_client, page=2, size=5, lid=3, keyword="test")
        mock_client.get.assert_called_once_with(
            "/api/articles",
            params={"page": 2, "size": 5, "lid": 3, "keyword": "test"},
        )

    def test_omits_empty_keyword(self, mock_client):
        articles.list_articles(mock_client, page=1, size=10, lid=0, keyword="")
        call = mock_client.get.call_args
        assert "keyword" not in call.kwargs["params"]

    def test_returns_data_and_kind(self, mock_client):
        data, kind = articles.list_articles(mock_client)
        assert kind == "articles_list"
        assert data == {"code": 200, "data": []}


class TestCreateArticle:
    def test_required_fields(self, mock_client):
        articles.create_article(mock_client, title="t", content="c")
        call = mock_client.post.call_args
        assert call.args[0] == "/api/articles"
        assert call.kwargs["json"]["title"] == "t"
        assert call.kwargs["json"]["content"] == "c"

    def test_optional_fields(self, mock_client):
        articles.create_article(
            mock_client, title="t", content="c",
            uid=2, lid=3, img="/x.png", heat=5,
        )
        payload = mock_client.post.call_args.kwargs["json"]
        assert payload == {
            "title": "t", "content": "c", "uid": 2, "lid": 3,
            "img": "/x.png", "heat": 5,
        }

    def test_img_none_omitted(self, mock_client):
        articles.create_article(mock_client, title="t", content="c", img=None)
        payload = mock_client.post.call_args.kwargs["json"]
        assert "img" not in payload

    def test_returns_id_kind(self, mock_client):
        _, kind = articles.create_article(mock_client, title="t", content="c")
        assert kind == "id_response"


class TestGetArticle:
    def test_path_with_id(self, mock_client):
        articles.get_article(mock_client, article_id=42)
        mock_client.get.assert_called_once_with("/api/articles/42")

    def test_kind(self, mock_client):
        _, kind = articles.get_article(mock_client, article_id=1)
        assert kind == "article_get"


class TestUpdateArticle:
    def test_partial_update(self, mock_client):
        articles.update_article(mock_client, article_id=5, heat=99)
        mock_client.put.assert_called_once_with(
            "/api/articles/5", json={"heat": 99}
        )

    def test_all_fields(self, mock_client):
        articles.update_article(
            mock_client, article_id=5, title="new", content="nc",
            lid=2, img="/i.png", heat=10,
        )
        payload = mock_client.put.call_args.kwargs["json"]
        assert len(payload) == 5

    def test_empty_payload_when_all_none(self, mock_client):
        articles.update_article(mock_client, article_id=5)
        mock_client.put.assert_called_once_with("/api/articles/5", json={})

    def test_kind(self, mock_client):
        _, kind = articles.update_article(mock_client, article_id=1)
        assert kind == "message_response"


class TestDeleteArticle:
    def test_soft_default_true(self, mock_client):
        articles.delete_article(mock_client, article_id=7)
        mock_client.delete.assert_called_once_with(
            "/api/articles/7", params={"soft": "true"}
        )

    def test_hard_delete(self, mock_client):
        articles.delete_article(mock_client, article_id=7, soft=False)
        mock_client.delete.assert_called_once_with(
            "/api/articles/7", params={"soft": "false"}
        )

    def test_soft_serialized_as_lowercase_string(self):
        """soft must be a lowercase string so requests serializes soft=true."""
        from blog_manager.client import BlogClient
        from conftest import make_mock_session

        session = make_mock_session(200, {"code": 200, "message": "deleted"})
        c = BlogClient(base_url="http://h:1", session=session)
        articles.delete_article(c, article_id=3, soft=True)
        assert session.request.call_args.kwargs["params"] == {"soft": "true"}

        session2 = make_mock_session(200, {"code": 200, "message": "deleted"})
        c2 = BlogClient(base_url="http://h:1", session=session2)
        articles.delete_article(c2, article_id=3, soft=False)
        assert session2.request.call_args.kwargs["params"] == {"soft": "false"}

    def test_kind(self, mock_client):
        _, kind = articles.delete_article(mock_client, article_id=1)
        assert kind == "message_response"


class TestRestoreArticle:
    def test_path(self, mock_client):
        articles.restore_article(mock_client, article_id=7)
        mock_client.post.assert_called_once_with("/api/articles/7/restore")

    def test_kind(self, mock_client):
        _, kind = articles.restore_article(mock_client, article_id=1)
        assert kind == "message_response"


class TestTopHeat:
    def test_path_and_limit(self, mock_client):
        articles.top_articles(mock_client, limit=3)
        mock_client.get.assert_called_once_with(
            "/api/articles/heat/top", params={"limit": 3}
        )

    def test_kind(self, mock_client):
        _, kind = articles.top_articles(mock_client)
        assert kind == "articles_top"
