"""Tests for file upload management commands (4 operations)."""

from __future__ import annotations

import pytest

from blog_manager import uploads


class TestUploadFile:
    def test_calls_upload_endpoint(self, mock_client, tmp_upload_file):
        uploads.upload_file(mock_client, tmp_upload_file)
        mock_client.post.assert_called_once()
        call = mock_client.post.call_args
        assert call.args[0] == "/api/upload"
        assert "files" in call.kwargs

    def test_files_key_is_file(self, mock_client, tmp_upload_file):
        uploads.upload_file(mock_client, tmp_upload_file)
        files = mock_client.post.call_args.kwargs["files"]
        assert "file" in files

    def test_kind(self, mock_client, tmp_upload_file):
        _, kind = uploads.upload_file(mock_client, tmp_upload_file)
        assert kind == "upload_single"

    def test_raises_for_missing_file(self, mock_client):
        with pytest.raises(FileNotFoundError):
            uploads.upload_file(mock_client, "/nonexistent/path/file.txt")


class TestUploadFiles:
    def test_calls_multiple_endpoint(self, mock_client, tmp_upload_file):
        uploads.upload_files(mock_client, [tmp_upload_file, tmp_upload_file])
        call = mock_client.post.call_args
        assert call.args[0] == "/api/upload/multiple"

    def test_multiple_files_in_multipart(self, mock_client, tmp_upload_file):
        uploads.upload_files(mock_client, [tmp_upload_file, tmp_upload_file])
        files = mock_client.post.call_args.kwargs["files"]
        assert isinstance(files, list)
        assert len(files) == 2
        assert all(f[0] == "files" for f in files)

    def test_kind(self, mock_client, tmp_upload_file):
        _, kind = uploads.upload_files(mock_client, [tmp_upload_file])
        assert kind == "upload_multiple"

    def test_raises_for_missing_file(self, mock_client):
        with pytest.raises(FileNotFoundError):
            uploads.upload_files(mock_client, ["/nope.txt"])


class TestListUploads:
    def test_path(self, mock_client):
        uploads.list_uploads(mock_client)
        mock_client.get.assert_called_once_with("/api/uploads/list")

    def test_kind(self, mock_client):
        _, kind = uploads.list_uploads(mock_client)
        assert kind == "uploads_list"


class TestDeleteUpload:
    def test_path(self, mock_client):
        uploads.delete_upload(mock_client, filename="abc.png")
        mock_client.delete.assert_called_once_with("/api/uploads/abc.png")

    def test_kind(self, mock_client):
        _, kind = uploads.delete_upload(mock_client, filename="x.png")
        assert kind == "message_response"

    def test_filename_with_spaces_is_url_encoded(self, mock_client):
        uploads.delete_upload(mock_client, filename="my file.png")
        mock_client.delete.assert_called_once_with("/api/uploads/my%20file.png")

    def test_filename_with_special_chars_is_url_encoded(self, mock_client):
        uploads.delete_upload(mock_client, filename="中文文件.png")
        mock_client.delete.assert_called_once_with(
            "/api/uploads/%E4%B8%AD%E6%96%87%E6%96%87%E4%BB%B6.png"
        )
