"""GitHub repository and PR operations."""

import time
from typing import List, Dict, Any

from github import Github, PullRequest, Repository
from github import UnknownObjectException, GithubException, RateLimitExceededException

from .exceptions import (
    RepositoryError,
    PullRequestError,
    RateLimitError as CustomRateLimitError,
    APIError,
    ValidationError
)
from .logger import (
    setup_logger,
    log_exception,
    log_api_call
)

logger = setup_logger(__name__)


class GitHubRepo:
    """GitHub repository operations."""

    def __init__(self, client: Github, repo_name: str):
        """
        Initialize GitHub repo operations.

        Args:
            client: Authenticated GitHub client
            repo_name: Repository name (e.g., "owner/repo")

        Raises:
            RepositoryError: If repository cannot be accessed
        """
        self.client = client
        self.repo_name = repo_name

        try:
            logger.debug(f"Getting repository: {repo_name}")
            start_time = time.time()
            self.repo: Repository = client.get_repo(repo_name)
            duration = time.time() - start_time
            log_api_call(logger, "GET", f"/repos/{repo_name}", 200, duration)
            logger.info(f"Connected to repository: {repo_name}")

        except UnknownObjectException as e:
            logger.error(f"Repository not found: {repo_name} - {e}")
            raise RepositoryError(
                f"Repository '{repo_name}' not found or you don't have access",
                suggestion="Check repository name and your GitHub permissions"
            )

        except RateLimitExceededException as e:
            logger.error(f"GitHub API rate limit exceeded: {e}")
            reset_time = e.reset.timestamp() if hasattr(e, 'reset') else None
            raise CustomRateLimitError(reset_time=reset_time)

        except GithubException as e:
            log_exception(logger, e, f"Failed to access repository: {repo_name}")
            raise RepositoryError(
                f"Failed to access repository: {e}",
                status_code=getattr(e, 'status', None)
            )

        except Exception as e:
            log_exception(logger, e, f"Failed to connect to repository: {repo_name}")
            raise RepositoryError(
                f"Failed to connect to repository: {e}"
            )

    def get_prs(self, state: str = "open", limit: int = 10) -> List[PullRequest]:
        """Get pull requests from repository.

        Args:
            state: PR state (open, closed, all)
            limit: Maximum number of PRs to return

        Returns:
            List of PullRequest objects

        Raises:
            RepositoryError: If PRs cannot be retrieved
        """
        try:
            logger.debug(f"Getting PRs with state={state}, limit={limit}")
            start_time = time.time()
            pulls = self.repo.get_pulls(state=state)

            pr_list = []
            count = 0
            for pr in pulls:
                if count >= limit:
                    break
                pr_list.append(pr)
                count += 1

            duration = time.time() - start_time
            log_api_call(logger, "GET", f"/repos/{self.repo_name}/pulls", 200, duration)
            logger.info(f"Retrieved {len(pr_list)} PRs from {self.repo_name}")

            return pr_list

        except RateLimitExceededException as e:
            logger.error(f"GitHub API rate limit exceeded: {e}")
            reset_time = e.reset.timestamp() if hasattr(e, 'reset') else None
            raise CustomRateLimitError(reset_time=reset_time)

        except GithubException as e:
            log_exception(logger, e, f"Failed to get PRs from {self.repo_name}")
            raise RepositoryError(
                f"Failed to get PRs: {e}",
                status_code=getattr(e, 'status', None)
            )

    def get_pr(self, pr_number: int) -> PullRequest:
        """Get a specific pull request.

        Args:
            pr_number: Pull request number

        Returns:
            PullRequest object

        Raises:
            PullRequestError: If PR cannot be retrieved
        """
        try:
            logger.debug(f"Getting PR #{pr_number} from {self.repo_name}")
            start_time = time.time()
            pr = self.repo.get_pull(pr_number)
            duration = time.time() - start_time
            log_api_call(logger, "GET", f"/repos/{self.repo_name}/pulls/{pr_number}", 200, duration)
            logger.info(f"Retrieved PR #{pr_number} from {self.repo_name}")

            return pr

        except UnknownObjectException as e:
            logger.error(f"PR #{pr_number} not found in {self.repo_name}")
            raise PullRequestError(
                f"Pull request #{pr_number} not found",
                suggestion="Check that the PR number is correct"
            )

        except RateLimitExceededException as e:
            logger.error(f"GitHub API rate limit exceeded: {e}")
            reset_time = e.reset.timestamp() if hasattr(e, 'reset') else None
            raise CustomRateLimitError(reset_time=reset_time)

        except GithubException as e:
            log_exception(logger, e, f"Failed to get PR #{pr_number}")
            raise PullRequestError(
                f"Failed to get PR #{pr_number}: {e}",
                status_code=getattr(e, 'status', None)
            )

    def get_pr_diff(self, pr_number: int):
        """Get files changed in a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            List of file objects

        Raises:
            PullRequestError: If files cannot be retrieved
        """
        try:
            logger.debug(f"Getting files for PR #{pr_number}")
            pr = self.get_pr(pr_number)
            files = pr.get_files()
            logger.info(f"Retrieved {len(files)} files for PR #{pr_number}")

            return files

        except GithubException as e:
            log_exception(logger, e, f"Failed to get files for PR #{pr_number}")
            raise PullRequestError(
                f"Failed to get files for PR: {e}",
                status_code=getattr(e, 'status', None)
            )

    def get_pr_diff_content(self, pr_number: int) -> str:
        """Get the actual diff content for a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            Diff content as string

        Raises:
            PullRequestError: If diff content cannot be retrieved
        """
        try:
            logger.debug(f"Getting diff content for PR #{pr_number}")
            pr = self.get_pr(pr_number)
            files = pr.get_files()

            diff_lines = []
            for file in files:
                diff_lines.append(f"--- a/{file.filename}")
                diff_lines.append(f"+++ b/{file.filename}")
                if file.patch:
                    diff_lines.append(file.patch)
                diff_lines.append("")

            diff_content = "\n".join(diff_lines)
            logger.debug(f"Generated diff content for PR #{pr_number} ({len(diff_content)} chars)")

            return diff_content

        except Exception as e:
            log_exception(logger, e, f"Failed to generate diff for PR #{pr_number}")
            raise PullRequestError(
                f"Failed to generate diff: {e}"
            )

    def get_pr_info(self, pr_number: int) -> Dict[str, Any]:
        """Get comprehensive information about a pull request.

        Args:
            pr_number: Pull request number

        Returns:
            Dictionary with PR information

        Raises:
            PullRequestError: If PR info cannot be retrieved
        """
        try:
            logger.debug(f"Getting detailed info for PR #{pr_number}")
            pr = self.get_pr(pr_number)

            info = {
                "number": pr.number,
                "title": pr.title,
                "description": pr.body or "",
                "author": pr.user.login,
                "state": pr.state,
                "created_at": pr.created_at,
                "updated_at": pr.updated_at,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "mergeable": pr.mergeable,
                "mergeable_state": pr.mergeable_state,
                "labels": [label.name for label in pr.labels],
            }

            logger.debug(f"Retrieved info for PR #{pr_number}: {info['title']}")
            return info

        except Exception as e:
            log_exception(logger, e, f"Failed to get info for PR #{pr_number}")
            raise PullRequestError(
                f"Failed to get PR info: {e}"
            )
