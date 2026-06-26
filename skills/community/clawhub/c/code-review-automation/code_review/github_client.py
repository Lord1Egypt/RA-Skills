"""GitHub API configuration and management."""

import os
from pathlib import Path
from typing import Optional

from github import Github, GithubException, RateLimitExceededException
from dotenv import load_dotenv

from .exceptions import AuthenticationError, RateLimitError, ConfigurationError
from .logger import setup_logger, log_exception

# Load environment variables from .env file
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"
load_dotenv(ENV_FILE)

logger = setup_logger(__name__)


class GitHubConfig:
    """Manage GitHub API credentials and connection."""

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")

    def get_client(self) -> Github:
        """Get authenticated GitHub client.

        Returns:
            Authenticated Github client

        Raises:
            ConfigurationError: If GITHUB_TOKEN is not configured
            AuthenticationError: If token authentication fails
        """
        if not self.github_token:
            logger.error("GITHUB_TOKEN not found in environment variables")
            raise ConfigurationError(
                "GITHUB_TOKEN not found in environment variables. "
                "Please set GITHUB_TOKEN in .env file or environment.",
                suggestion="Create a .env file with: GITHUB_TOKEN=your_token_here"
            )

        try:
            logger.debug("Creating GitHub client with token")
            client = Github(self.github_token)

            # Test authentication
            user = client.get_user()
            logger.debug(f"Authenticated as: {user.login}")

            return client

        except RateLimitExceededException as e:
            logger.error(f"GitHub API rate limit exceeded: {e}")
            reset_time = e.reset.timestamp() if hasattr(e, 'reset') else None
            raise RateLimitError(reset_time=reset_time)

        except GithubException as e:
            logger.error(f"GitHub API authentication failed: {e}")
            raise AuthenticationError(
                f"Failed to authenticate with GitHub: {e}",
                suggestion="Check that your GITHUB_TOKEN is valid and has the necessary permissions"
            )

        except Exception as e:
            log_exception(logger, e, "Failed to create GitHub client")
            raise ConfigurationError(
                f"Failed to create GitHub client: {e}",
                suggestion="Check your network connection and GITHUB_TOKEN"
            )

    def is_configured(self) -> bool:
        """Check if GitHub API is configured.

        Returns:
            True if GITHUB_TOKEN is set, False otherwise
        """
        configured = bool(self.github_token)
        if configured:
            logger.debug("GitHub API is configured")
        else:
            logger.warning("GitHub API is not configured - GITHUB_TOKEN not set")
        return configured
