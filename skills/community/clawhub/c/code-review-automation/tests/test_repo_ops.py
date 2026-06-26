"""Tests for repository operations."""

import pytest
from unittest.mock import MagicMock, patch

from code_review.repo_ops import GitHubRepo


class TestGitHubRepo:
    """Test GitHub repository operations."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitHub client."""
        client = MagicMock()
        mock_repo = MagicMock()
        client.get_repo.return_value = mock_repo
        return client

    def test_init(self, mock_client):
        """Test GitHubRepo initialization."""
        repo_ops = GitHubRepo(mock_client, "owner/repo")
        assert repo_ops.client == mock_client
        assert repo_ops.repo_name == "owner/repo"
        mock_client.get_repo.assert_called_once_with("owner/repo")

    def test_get_prs_open(self, mock_client):
        """Test getting open pull requests."""
        mock_pr1 = MagicMock()
        mock_pr1.number = 1
        mock_pr1.title = "PR 1"
        mock_pr1.user.login = "user1"
        mock_pr1.state = "open"
        mock_pr1.changed_files = 5
        mock_pr1.additions = 100
        mock_pr1.deletions = 50

        mock_pr2 = MagicMock()
        mock_pr2.number = 2
        mock_pr2.title = "PR 2"
        mock_pr2.user.login = "user2"
        mock_pr2.state = "open"
        mock_pr2.changed_files = 3
        mock_pr2.additions = 75
        mock_pr2.deletions = 25

        mock_repo = mock_client.get_repo.return_value
        mock_pulls = MagicMock()
        mock_pulls.__iter__ = MagicMock(return_value=iter([mock_pr1, mock_pr2]))
        mock_repo.get_pulls.return_value = mock_pulls

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        prs = repo_ops.get_prs(state="open", limit=10)

        assert len(prs) == 2
        assert prs[0].number == 1
        assert prs[1].number == 2
        mock_repo.get_pulls.assert_called_once_with(state="open")

    def test_get_prs_with_limit(self, mock_client):
        """Test getting pull requests with limit."""
        mock_pr = MagicMock()
        mock_pr.number = 1

        mock_repo = mock_client.get_repo.return_value
        mock_pulls = MagicMock()
        mock_pulls.__iter__ = MagicMock(return_value=iter([mock_pr] * 20))
        mock_repo.get_pulls.return_value = mock_pulls

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        prs = repo_ops.get_prs(state="open", limit=5)

        assert len(prs) == 5

    def test_get_pr(self, mock_client):
        """Test getting a specific pull request."""
        mock_pr = MagicMock()
        mock_pr.number = 123
        mock_pr.title = "Test PR"

        mock_repo = mock_client.get_repo.return_value
        mock_repo.get_pull.return_value = mock_pr

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        pr = repo_ops.get_pr(123)

        assert pr.number == 123
        mock_repo.get_pull.assert_called_once_with(123)

    def test_get_pr_diff(self, mock_client):
        """Test getting files changed in a PR."""
        mock_file1 = MagicMock()
        mock_file1.filename = "file1.py"
        mock_file1.additions = 10
        mock_file1.deletions = 5
        mock_file1.status = "modified"
        mock_file1.patch = "@@ -1,1 +1,1 @@" + "\n-old line"
        mock_file1.patch += "\n+new line"

        mock_file2 = MagicMock()
        mock_file2.filename = "file2.py"
        mock_file2.additions = 20
        mock_file2.deletions = 0
        mock_file2.status = "added"
        mock_file2.patch = None

        mock_pr = MagicMock()
        mock_pr.get_files.return_value = [mock_file1, mock_file2]

        mock_repo = mock_client.get_repo.return_value
        mock_repo.get_pull.return_value = mock_pr

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        files = repo_ops.get_pr_diff(123)

        assert len(files) == 2
        assert files[0].filename == "file1.py"
        assert files[1].filename == "file2.py"

    def test_get_pr_diff_content(self, mock_client):
        """Test getting diff content as string."""
        mock_file = MagicMock()
        mock_file.filename = "test.py"
        mock_file.status = "modified"
        mock_file.patch = "@@ -1,1 +1,1 @@\n-old\n+new"

        mock_pr = MagicMock()
        mock_pr.get_files.return_value = [mock_file]

        mock_repo = mock_client.get_repo.return_value
        mock_repo.get_pull.return_value = mock_pr

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        diff_content = repo_ops.get_pr_diff_content(123)

        assert "--- a/test.py" in diff_content
        assert "+++ b/test.py" in diff_content
        assert "-old" in diff_content
        assert "+new" in diff_content

    def test_get_pr_info(self, mock_client):
        """Test getting detailed PR information."""
        mock_label = MagicMock()
        mock_label.name = "bug"

        mock_pr = MagicMock()
        mock_pr.number = 123
        mock_pr.title = "Test PR"
        mock_pr.body = "Test description"
        mock_pr.user.login = "testuser"
        mock_pr.state = "open"
        mock_pr.created_at = "2024-01-01"
        mock_pr.updated_at = "2024-01-02"
        mock_pr.additions = 100
        mock_pr.deletions = 50
        mock_pr.changed_files = 5
        mock_pr.mergeable = True
        mock_pr.mergeable_state = "clean"
        mock_pr.labels = [mock_label]

        mock_repo = mock_client.get_repo.return_value
        mock_repo.get_pull.return_value = mock_pr

        repo_ops = GitHubRepo(mock_client, "owner/repo")
        info = repo_ops.get_pr_info(123)

        assert info["number"] == 123
        assert info["title"] == "Test PR"
        assert info["author"] == "testuser"
        assert info["additions"] == 100
        assert info["deletions"] == 50
        assert info["changed_files"] == 5
        assert info["mergeable"] is True
        assert "bug" in info["labels"]
