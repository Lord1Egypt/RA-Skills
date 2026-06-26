"""
EngageLab OTP API client.

Wraps all OTP REST API endpoints: send OTP, custom OTP, verify, custom messages,
and template CRUD. Handles authentication, request construction, and error handling.

Usage:
    from otp_client import EngageLabOTP

    client = EngageLabOTP("YOUR_DEV_KEY", "YOUR_DEV_SECRET")

    # Send platform-generated OTP
    result = client.send_otp("+6591234567", "my-template")

    # Verify
    verification = client.verify(result["message_id"], "123456")
"""

import base64
import json
import requests
from typing import Optional, Union


BASE_URL = "https://otp.api.engagelab.cc"


class EngageLabOTPError(Exception):
    """Raised when the OTP API returns an error response."""

    def __init__(self, code: int, message: str, http_status: int):
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(f"[{http_status}] Error {code}: {message}")


class EngageLabOTP:
    """Client for the EngageLab OTP REST API."""

    def __init__(self, dev_key: str, dev_secret: str, base_url: str = BASE_URL):
        auth = base64.b64encode(f"{dev_key}:{dev_secret}".encode()).decode()
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }
        self._base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, payload: Optional[dict] = None) -> dict:
        url = f"{self._base_url}{path}"
        resp = requests.request(method, url, headers=self._headers, json=payload)

        if resp.status_code >= 400:
            try:
                body = resp.json()
            except (ValueError, json.JSONDecodeError):
                body = {"code": resp.status_code, "message": resp.text}
            raise EngageLabOTPError(
                code=body.get("code", resp.status_code),
                message=body.get("message", resp.text),
                http_status=resp.status_code,
            )

        if not resp.content:
            return {}
        return resp.json()

    # ── OTP Send (platform-generated code) ──────────────────────────

    def send_otp(
        self,
        to: str,
        template_id: str,
        language: str = "default",
        params: Optional[dict] = None,
    ) -> dict:
        """
        Send a platform-generated OTP code.

        Returns dict with `message_id` and `send_channel`.
        Use `message_id` with `verify()` to validate the code.
        """
        template = {"id": template_id, "language": language}
        if params:
            template["params"] = params
        return self._request("POST", "/v1/messages", {"to": to, "template": template})

    # ── Custom OTP Send (user-generated code) ───────────────────────

    def send_custom_otp(
        self,
        to: str,
        code: str,
        template_id: str,
        language: str = "default",
        params: Optional[dict] = None,
    ) -> dict:
        """
        Send a user-generated OTP code. No verification API call needed afterward.

        Returns dict with `message_id` and `send_channel`.
        """
        template = {"id": template_id, "language": language}
        if params:
            template["params"] = params
        return self._request("POST", "/v1/codes", {"to": to, "code": code, "template": template})

    # ── OTP Verify ──────────────────────────────────────────────────

    def verify(self, message_id: str, verify_code: str) -> dict:
        """
        Verify a platform-generated OTP code.

        Returns dict with `message_id`, `verify_code`, and `verified` (bool).
        Successfully verified codes cannot be verified again.
        """
        return self._request("POST", "/v1/verifications", {
            "message_id": message_id,
            "verify_code": verify_code,
        })

    # ── Custom Messages Send ────────────────────────────────────────

    def send_custom_message(
        self,
        to: Union[str, list],
        template_id: str,
        params: Optional[dict] = None,
    ) -> dict:
        """
        Send a custom template message (verification, notification, or marketing).

        `to` can be a single recipient (str) or multiple (list).
        For verification code templates, `params` must include `code`.

        Returns dict with `message_id` and `send_channel`.
        """
        template = {"id": template_id}
        if params:
            template["params"] = params
        return self._request("POST", "/v1/custom-messages", {"to": to, "template": template})

    # ── Template Management ─────────────────────────────────────────

    def create_template(self, template_config: dict) -> dict:
        """
        Create an OTP template.

        `template_config` must include at minimum:
          - template_id (str): unique ID
          - send_channel_strategy (str): e.g. "sms", "whatsapp|sms"
          - channel-specific config (sms_config, whatsapp_config, etc.)

        Returns dict with `code` and `message`.
        """
        return self._request("POST", "/v1/template-configs", template_config)

    def list_templates(self) -> list:
        """Return a list of all templates (brief, without detailed content)."""
        return self._request("GET", "/v1/template-configs")

    def get_template(self, template_id: str) -> dict:
        """Return full template details including channel configurations."""
        return self._request("GET", f"/v1/template-configs/{template_id}")

    def delete_template(self, template_id: str) -> dict:
        """Delete a template. Returns dict with `code` and `message`."""
        return self._request("DELETE", f"/v1/template-configs/{template_id}")


if __name__ == "__main__":
    DEV_KEY = "YOUR_DEV_KEY"
    DEV_SECRET = "YOUR_DEV_SECRET"

    client = EngageLabOTP(DEV_KEY, DEV_SECRET)

    # -- Send OTP and verify --
    # result = client.send_otp("+6591234567", "my-template")
    # print(f"Sent! message_id={result['message_id']}, channel={result['send_channel']}")
    # verification = client.verify(result["message_id"], "123456")
    # print(f"Verified: {verification['verified']}")

    # -- Send custom OTP (your own code) --
    # result = client.send_custom_otp("+6591234567", "398210", "my-template")
    # print(f"Custom OTP sent! message_id={result['message_id']}")

    # -- Send custom message (notification) --
    # result = client.send_custom_message(
    #     ["+6591234567"],
    #     "notification-template",
    #     params={"order": "ORD-9876"},
    # )
    # print(f"Notification sent! message_id={result['message_id']}")

    # -- List templates --
    # templates = client.list_templates()
    # for t in templates:
    #     print(f"  {t['template_id']}: {t.get('description', '')} (status={t['status']})")

    pass
