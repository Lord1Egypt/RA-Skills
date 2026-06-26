"""
auth.py - Authentication and Token management module

Responsibilities:
  - AES encrypt password (ECB/PKCS7 compatible with frontend CryptoJS)
  - Call login API to get authToken (password mode or email verification code mode)
  - Token file cache (.token_cache) and auto refresh
"""

import os
import sys
import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from common.config import config, LOGIN_MODE_EMAIL

# AES key (same as frontend)
AES_KEY = "loo2vrx79g87luhvj06lodb0c3lp3gqw"

# Token cache file path (in project directory)
_TOKEN_CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".token_cache")

# Max retry attempts for verification code login
_MAX_CODE_ATTEMPTS = 3


class AuthError(Exception):
    """Authentication error exception"""
    pass


def encrypt_password(plain_password: str, disabled: bool = False) -> str:
    """
    Encrypt password using AES-ECB, return Base64 encoded string.
    Compatible with frontend CryptoJS.AES.encrypt (ECB mode, PKCS7 padding).
    
    Args:
        plain_password: Plaintext password
        disabled: Whether to disable encryption (return plaintext directly)
    """
    if disabled:
        return plain_password
    
    key = AES_KEY.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plain_password.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode("utf-8")


def send_verification_code(email: str) -> dict:
    """
    Send verification code to the given email address.

    POST {base_url}/drapi/user/verificationCode
    Payload: {"email": email}

    Args:
        email: Target email address
    Returns:
        Parsed JSON response dict
    Raises:
        AuthError: If the request fails or API returns failure
    """
    url = f"{config.base_url}/drapi/user/verificationCode"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }
    payload = {"email": email}

    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise AuthError(f"Failed to send verification code: {e}")

    data = resp.json()
    if not data.get("Success"):
        raise AuthError(f"Failed to send verification code: {data.get('Message', data)}")

    return data


def _prompt_verification_code(email: str) -> str:
    """
    Prompt user to enter the verification code received via email.
    Prints prompt to stderr to avoid polluting stdout JSON output.

    Args:
        email: The email address where the code was sent
    Returns:
        The verification code string (stripped)
    Raises:
        AuthError: If input is empty or stdin is not available (EOFError)
    """
    print(f"\nVerification code has been sent to {email}", file=sys.stderr)
    print("Please check your email and enter the verification code.", file=sys.stderr)

    try:
        code = input("Verification code: ").strip()
    except EOFError:
        raise AuthError(
            "Cannot read verification code: no interactive input available. "
            "Email verification code login requires interactive terminal input."
        )

    if not code:
        raise AuthError("Verification code cannot be empty.")

    return code


def _login_with_email() -> str:
    """
    Login using email and verification code.

    Flow:
      1. Send verification code to config.email
      2. Prompt user to enter the code
      3. Encrypt the code using AES-ECB (same as password encryption)
      4. POST /nephele/login with authType=authCode

    Allows up to _MAX_CODE_ATTEMPTS retries for incorrect codes.
    Returns authToken string, raises AuthError on failure.
    """
    email = config.email

    # Step 1: Send verification code
    send_verification_code(email)

    # Step 2-4: Prompt code and attempt login (with retry)
    url = f"{config.base_url}/nephele/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }

    last_error = None
    for attempt in range(1, _MAX_CODE_ATTEMPTS + 1):
        code = _prompt_verification_code(email)
        encrypted_code = encrypt_password(code)

        payload = {
            "userName": email,
            "password": encrypted_code,
            "authType": "authCode",
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise AuthError(f"Login request failed: {e}")

        data = resp.json()
        if data.get("success"):
            token = data.get("data", {}).get("authToken")
            if not token:
                raise AuthError(f"authToken not found in login response: {data}")
            return token

        # Login failed - possibly wrong code
        last_error = data
        remaining = _MAX_CODE_ATTEMPTS - attempt
        if remaining > 0:
            print(
                f"Login failed (incorrect code or code expired). "
                f"{remaining} attempt(s) remaining.",
                file=sys.stderr,
            )

    raise AuthError(f"Login failed after {_MAX_CODE_ATTEMPTS} attempts: {last_error}")


def _login_with_password() -> str:
    """
    Login using username and password (one-click launch version).

    POST {base_url}/nephele/login
    Return authToken string, raise AuthError on failure.
    """
    url = f"{config.base_url}/nephele/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
    }
    payload = {
        "userName": config.username,
        "password": encrypt_password(config.password),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise AuthError(f"Login request failed: {e}")

    data = resp.json()
    if not data.get("success"):
        raise AuthError(f"Login failed: {data}")

    token = data.get("data", {}).get("authToken")
    if not token:
        raise AuthError(f"authToken not found in login response: {data}")

    return token


def _login() -> str:
    """
    Call login API to get authToken.
    Dispatches to password or email login based on config.login_mode.
    """
    if config.login_mode == LOGIN_MODE_EMAIL:
        return _login_with_email()
    return _login_with_password()


def _save_token(token: str) -> None:
    """Write token to cache file"""
    with open(_TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(token)


def _load_token() -> str | None:
    """Read token from cache file, return None if not exists"""
    if not os.path.exists(_TOKEN_CACHE_FILE):
        return None
    try:
        with open(_TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
            return token if token else None
    except Exception:
        return None


def _clear_token() -> None:
    """Clear cached token file"""
    if os.path.exists(_TOKEN_CACHE_FILE):
        os.remove(_TOKEN_CACHE_FILE)


def get_token() -> str:
    """
    Get current valid authToken.
    Read from cache file first, auto login and cache if not exists.
    """
    token = _load_token()
    if token:
        return token

    token = _login()
    _save_token(token)
    return token


def refresh_token() -> str:
    """
    Force refresh token: clear cache → re-login → cache new token.
    """
    _clear_token()
    token = _login()
    _save_token(token)
    return token
