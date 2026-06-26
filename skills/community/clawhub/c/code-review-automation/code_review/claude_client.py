"""Claude API integration for code analysis."""

import os
from typing import Optional
from pathlib import Path

from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

from .exceptions import AuthenticationError, APIError as CustomAPIError, ConfigurationError
from .logger import setup_logger, log_exception

# Load environment variables from .env file
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"
load_dotenv(ENV_FILE)

logger = setup_logger(__name__)


class ClaudeConfig:
    """Manage Claude API credentials and connection."""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def get_client(self) -> Anthropic:
        """Get authenticated Claude client.

        Returns:
            Authenticated Anthropic client

        Raises:
            ConfigurationError: If ANTHROPIC_API_KEY is not configured
            AuthenticationError: If API key authentication fails
        """
        if not self.api_key:
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            raise ConfigurationError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please set ANTHROPIC_API_KEY in .env file or environment.",
                suggestion="Create a .env file with: ANTHROPIC_API_KEY=your_key_here"
            )

        try:
            logger.debug("Creating Anthropic client with API key")
            client = Anthropic(api_key=self.api_key)
            logger.debug("Anthropic client created successfully")
            return client

        except APIConnectionError as e:
            logger.error(f"Failed to connect to Anthropic API: {e}")
            raise CustomAPIError(
                f"Failed to connect to Anthropic API: {e}",
                suggestion="Check your network connection"
            )

        except RateLimitError as e:
            logger.error(f"Anthropic API rate limit exceeded: {e}")
            raise CustomAPIError(
                "Anthropic API rate limit exceeded",
                suggestion="Wait for rate limit to reset or check your usage limits"
            )

        except APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise AuthenticationError(
                f"Failed to authenticate with Anthropic: {e}",
                suggestion="Check that your ANTHROPIC_API_KEY is valid"
            )

        except Exception as e:
            log_exception(logger, e, "Failed to create Anthropic client")
            raise ConfigurationError(
                f"Failed to create Anthropic client: {e}",
                suggestion="Check your network connection and ANTHROPIC_API_KEY"
            )

    def is_configured(self) -> bool:
        """Check if Claude API is configured.

        Returns:
            True if ANTHROPIC_API_KEY is set, False otherwise
        """
        configured = bool(self.api_key)
        if configured:
            logger.debug("Claude API is configured")
        else:
            logger.warning("Claude API is not configured - ANTHROPIC_API_KEY not set")
        return configured
