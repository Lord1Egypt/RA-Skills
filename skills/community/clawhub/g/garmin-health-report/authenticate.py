#!/usr/bin/env python3
"""
Garmin Connect Authentication Module using garth library.

Implements OAuth2 authentication for Garmin Connect API.
Completely standalone - no dependencies on garmer.
"""

import json
import os
import getpass
import sys
from pathlib import Path

try:
    import garth
except ImportError:
    print("Error: garth library not installed.", file=sys.stderr)
    print("Please install garth: pip3 install garth", file=sys.stderr)
    print("garth is not official Garmin Connect authentication library.", file=sys.stderr)
    sys.exit(1)


class GarminAuthError(Exception):
    """Base exception for Garmin authentication errors."""
    pass


class GarminAuthClient:
    """
    Garmin Connect OAuth2 authentication client using garth.

    Completely standalone - no garmer dependencies.
    """

    DEFAULT_TOKEN_DIR = Path.home() / ".garmin-health-report"
    DEFAULT_TOKEN_FILE = "tokens.json"

    def __init__(self, token_dir: str = None, is_cn: bool = None):
        """
        Initialize authentication client.

        Args:
            token_dir: Directory to store authentication tokens.
                       Defaults to ~/.garmin-health-report
            is_cn: Whether to use China region (garmin.cn).
                     If None, reads from config.json
        """
        if token_dir is None:
            self.token_dir = self.DEFAULT_TOKEN_DIR
        else:
            self.token_dir = Path(token_dir)

        self.token_file = self.DEFAULT_TOKEN_FILE
        self.is_cn = self._check_is_cn(is_cn)

        # Configure domain if using China region
        if self.is_cn:
            self._configure_cn_domain()

    def _check_is_cn(self, is_cn: bool) -> bool:
        """
        Check if user is in China region.

        Args:
            is_cn: Explicit value, or None to read from config

        Returns:
            True if using China region
        """
        # If explicitly provided, use it
        if is_cn is not None:
            return is_cn

        # Otherwise, read from config file
        config_file = self.token_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('is_cn', False)
            except Exception:
                pass

        # Default to China region (garmin.cn)
        return True

    def _configure_cn_domain(self):
        """Configure garth to use China region (garmin.cn)."""
        try:
            garth.configure(domain="garmin.cn")
        except Exception as e:
            print(f"Warning: Failed to configure China region: {e}", file=sys.stderr)

    def is_authenticated(self) -> bool:
        """
        Check if user has valid authentication tokens.

        Returns:
            True if authenticated, False otherwise
        """
        # Check if garth has any token files
        # garth.save() creates oauth1_token.json and oauth2_token.json
        oauth1 = self.token_dir / "oauth1_token.json"
        oauth2 = self.token_dir / "oauth2_token.json"

        if oauth1.exists() and oauth2.exists():
            try:
                # Try to resume session from saved tokens
                self._configure_cn_domain()
                garth.resume(self.token_dir)
                return True
            except Exception:
                return False

        return False

    @property
    def token_path(self) -> Path:
        """Get full path to token file."""
        return self.token_dir / self.token_file

    def login(self, username: str = None, password: str = None) -> dict:
        """
        Authenticate with Garmin Connect.

        Args:
            username: Garmin Connect username/email. If not provided, prompts user.
            password: Garmin Connect password. If not provided, prompts user.

        Returns:
            Dictionary containing authentication tokens

        Raises:
            GarminAuthError: If authentication fails
        """
        if username is None:
            username = input("Garmin Connect username/email: ")

        if password is None:
            password = getpass.getpass("Garmin Connect password: ")

        print("Authenticating with Garmin Connect...")

        try:
            # Configure domain before login if using China region
            self._configure_cn_domain()

            # Perform login
            garth.login(username, password)

            print("✓ Authentication successful!")
            print(f"  Username: {username}")

            # Save tokens
            self.save_tokens()

            return {
                "username": username,
                "is_cn": self.is_cn,
                "token_path": str(self.token_path)
            }

        except Exception as e:
            raise GarminAuthError(f"Authentication failed: {e}") from e

    def _configure_domain_if_needed(self):
        """Configure garth domain if using China region."""
        if self.is_cn:
            try:
                garth.configure(domain="garmin.cn")
            except Exception:
                pass

    def logout(self):
        """Logout and remove saved tokens."""
        if self.token_path.exists():
            try:
                self.token_path.unlink()
                print("✓ Logged out. Tokens removed.")
            except Exception as e:
                print(f"Warning: Failed to delete tokens: {e}", file=sys.stderr)

    def save_tokens(self):
        """
        Save authentication tokens to file.

        Creates token directory if it doesn't exist.
        """
        try:
            # Create directory if it doesn't exist
            self.token_dir.mkdir(parents=True, exist_ok=True)

            # Save tokens using garth
            garth.save(self.token_dir)
            print(f"  Tokens saved to: {self.token_dir}")

        except Exception as e:
            raise GarminAuthError(f"Failed to save tokens: {e}")

    def load_tokens(self) -> bool:
        """
        Load saved authentication tokens.

        Returns:
            True if tokens were loaded successfully
        """
        if not self.token_path.exists():
            return False

        try:
            # Configure domain before resume if using China region
            self._configure_domain_if_needed()

            # Resume session from saved tokens
            garth.resume(self.token_dir)
            return True

        except Exception as e:
            print(f"Warning: Failed to load tokens: {e}", file=sys.stderr)
            return False

    def get_client(self):
        """
        Get: underlying garth client for API calls.

        Returns:
            The garth Client instance

        Raises:
            GarminAuthError: If not authenticated
        """
        if not self.is_authenticated():
            raise GarminAuthError(
                "Not authenticated. Please run 'python3 authenticate.py' first."
            )

        return garth.client

    def ensure_authenticated(self):
        """
        Ensure we have valid authentication.

        Raises:
            GarminAuthError: If not authenticated
        """
        if not self.is_authenticated():
            raise GarminAuthError(
                "Not authenticated. Please run 'python3 authenticate.py' first."
            )


def main():
    """Command-line interface for authentication."""
    print("Garmin Connect Authentication")
    print("=" * 40)

    import argparse

    parser = argparse.ArgumentParser(description='Garmin Connect Authentication')
    parser.add_argument('mode', nargs='?', choices=['auto', 'international'],
                       help='Authentication mode (auto=domestic, international=international)')
    args = parser.parse_args()

    print("Garmin Connect Authentication")
    print("=" * 40)

    # Default to domestic (China region) unless explicitly set to international
    if args.mode == 'international':
        is_cn_arg = False
        print("Mode: 国际版 - garmin.com")
    elif args.mode == 'auto':
        is_cn_arg = True
        print("Mode: 国内版 - garmin.cn (默认)")
    else:
        # No argument, default to domestic
        is_cn_arg = True
        print("Mode: 国内版 - garmin.cn (默认)")

    client = GarminAuthClient(is_cn=is_cn_arg)

    # Check current authentication status
    if client.is_authenticated():
        print("Currently authenticated.")
        print()

        choice = input("Do you want to logout? [y/N]: ").strip().lower()
        if choice == 'y':
            client.logout()
        else:
            print("Keeping current authentication.")
        return

    # Not authenticated, prompt for login
    print("No active authentication found.")
    print("Please provide your Garmin Connect credentials.")
    print()

    try:
        client.login()
        print()
        print("You can now generate health reports!")
        print("Run: python3 health_daily_report.py")
    except GarminAuthError as e:
        print(f"❌ Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAuthentication cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()
