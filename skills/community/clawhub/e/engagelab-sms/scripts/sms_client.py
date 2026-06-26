"""
EngageLab SMS API client.

Wraps all SMS REST API endpoints: send messages, template CRUD, and
signature (sender ID) CRUD. Handles authentication, request construction,
and error handling.

Usage:
    from sms_client import EngageLabSMS

    client = EngageLabSMS("YOUR_DEV_KEY", "YOUR_DEV_SECRET")

    # Send SMS
    result = client.send_sms(["+6591234567"], "my-template", params={"code": "1234"})

    # Manage templates
    templates = client.list_templates()
    detail = client.get_template("123456789")
"""

import base64
import json
import requests
from typing import Optional, Union


BASE_URL = "https://smsapi.engagelab.com"


class EngageLabSMSError(Exception):
    """Raised when the SMS API returns an error response."""

    def __init__(self, code: int, message: str, http_status: int, plan_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.http_status = http_status
        self.plan_id = plan_id
        super().__init__(f"[{http_status}] Error {code}: {message}")


class EngageLabSMS:
    """Client for the EngageLab SMS REST API."""

    def __init__(self, dev_key: str, dev_secret: str, base_url: str = BASE_URL):
        auth = base64.b64encode(f"{dev_key}:{dev_secret}".encode()).decode()
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }
        self._base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, payload: Optional[dict] = None) -> Union[dict, list]:
        url = f"{self._base_url}{path}"
        resp = requests.request(method, url, headers=self._headers, json=payload)

        if resp.status_code >= 400:
            try:
                body = resp.json()
            except (ValueError, json.JSONDecodeError):
                body = {"code": resp.status_code, "message": resp.text}
            raise EngageLabSMSError(
                code=body.get("code", resp.status_code),
                message=body.get("message", resp.text),
                http_status=resp.status_code,
            )

        if not resp.content:
            return {}
        return resp.json()

    # ── Send SMS ────────────────────────────────────────────────────

    def send_sms(
        self,
        to: list,
        template_id: str,
        params: Optional[dict] = None,
        plan_name: Optional[str] = None,
        schedule_time: Optional[int] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """
        Send SMS to one or more recipients.

        Args:
            to: List of phone numbers with country code (e.g. ["+6591234567"]).
            template_id: ID of an approved SMS template.
            params: Template variable values (e.g. {"name": "Bob", "code": "1234"}).
            plan_name: Optional plan name, defaults to "-".
            schedule_time: Unix timestamp for scheduled delivery; omit for immediate.
            custom_args: Custom tracking parameters.

        Returns:
            dict with plan_id, total_count, accepted_count, and optionally
            message_id (single target) or schedule_info (scheduled send).

        Raises:
            EngageLabSMSError: If the API returns an error code.
        """
        payload = {
            "to": to,
            "template": {"id": template_id},
        }
        if params:
            payload["template"]["params"] = params
        if plan_name is not None:
            payload["plan_name"] = plan_name
        if schedule_time is not None:
            payload["schedule_time"] = schedule_time
        if custom_args is not None:
            payload["custom_args"] = custom_args

        result = self._request("POST", "/v1/messages", payload)

        if result.get("code") and result["code"] != 0:
            raise EngageLabSMSError(
                code=result["code"],
                message=result.get("message", "Unknown error"),
                http_status=200,
                plan_id=result.get("plan_id"),
            )
        return result

    # ── Template Management ─────────────────────────────────────────

    def list_templates(self) -> list:
        """Return a list of all SMS templates."""
        return self._request("GET", "/v1/template-configs")

    def get_template(self, template_id: str) -> dict:
        """Return details of a specific template."""
        return self._request("GET", f"/v1/template-configs/{template_id}")

    def create_template(
        self,
        template_name: str,
        template_type: str,
        template_content: str,
        country_codes: str,
        add_signature: bool = False,
        sign_id: Optional[str] = None,
        sign_position: Optional[int] = None,
    ) -> dict:
        """
        Create an SMS template. Returns dict with template_id.

        Template enters Pending Review (status=1) after creation.
        Content cannot contain: 【 】 、 测试 test [ ]

        Args:
            template_name: Up to 255 characters.
            template_type: "utility" (notification) or "marketing".
            template_content: SMS body with {var} placeholders.
            country_codes: Comma-separated country codes (e.g. "CN,US").
            add_signature: Whether to attach a sender ID signature.
            sign_id: Required if add_signature is True.
            sign_position: Required if add_signature is True. 1=Prefix, 2=Suffix.
        """
        payload = {
            "template_name": template_name,
            "template_type": template_type,
            "template_content": template_content,
            "country_codes": country_codes,
            "add_signature": add_signature,
        }
        if add_signature:
            if sign_id:
                payload["sign_id"] = sign_id
            if sign_position is not None:
                payload["sign_position"] = sign_position
        return self._request("POST", "/v1/template-configs", payload)

    def update_template(
        self,
        template_id: str,
        template_name: str,
        template_type: str,
        template_content: str,
        country_codes: str,
        add_signature: bool = False,
        sign_id: Optional[str] = None,
        sign_position: Optional[int] = None,
    ) -> dict:
        """
        Update an SMS template. All fields are required.

        Cannot update templates in Pending Review or tied to active plans.
        After update, status reverts to Pending Review.
        """
        payload = {
            "template_name": template_name,
            "template_type": template_type,
            "template_content": template_content,
            "country_codes": country_codes,
            "add_signature": add_signature,
        }
        if add_signature:
            if sign_id:
                payload["sign_id"] = sign_id
            if sign_position is not None:
                payload["sign_position"] = sign_position
        return self._request("PUT", f"/v1/template-configs/{template_id}", payload)

    def delete_template(self, template_id: str) -> dict:
        """Delete an SMS template. Cannot delete if tied to active plans."""
        return self._request("DELETE", f"/v1/template-configs/{template_id}")

    # ── Signature (Sender ID) Management ────────────────────────────

    def list_signatures(self) -> list:
        """Return a list of all sender ID signatures."""
        return self._request("GET", "/v1/sign-configs")

    def get_signature(self, sign_id: str) -> dict:
        """Return details of a specific signature."""
        return self._request("GET", f"/v1/sign-configs/{sign_id}")

    def create_signature(self, sign_name: str) -> dict:
        """
        Create a sender ID signature. Returns dict with sign_id.

        Name must be 2–60 characters, cannot contain 【 】 [ ].
        Names must be unique within the same business.
        Enters Pending Review (status=1) after creation.
        """
        return self._request("POST", "/v1/sign-configs", {"sign_name": sign_name})

    def update_signature(self, sign_id: str, sign_name: str) -> dict:
        """
        Update a signature's name.

        Cannot update signatures in Pending Review or tied to active plans.
        After update, status reverts to Pending Review.
        """
        return self._request("PUT", f"/v1/sign-configs/{sign_id}", {"sign_name": sign_name})

    def delete_signature(self, sign_id: str) -> dict:
        """Delete a sender ID signature. Cannot delete if tied to active plans."""
        return self._request("DELETE", f"/v1/sign-configs/{sign_id}")


if __name__ == "__main__":
    DEV_KEY = "YOUR_DEV_KEY"
    DEV_SECRET = "YOUR_DEV_SECRET"

    client = EngageLabSMS(DEV_KEY, DEV_SECRET)

    # -- Send SMS --
    # result = client.send_sms(
    #     ["+6591234567"],
    #     "my-template-id",
    #     params={"code": "039487"},
    # )
    # print(f"Sent! plan_id={result['plan_id']}, message_id={result.get('message_id')}")

    # -- Scheduled SMS --
    # import time
    # result = client.send_sms(
    #     ["+6591234567"],
    #     "my-template-id",
    #     params={"code": "039487"},
    #     schedule_time=int(time.time()) + 3600,  # 1 hour from now
    # )
    # print(f"Scheduled! task_id={result['schedule_info']['task_id']}")

    # -- Template management --
    # new = client.create_template(
    #     template_name="Welcome SMS",
    #     template_type="utility",
    #     template_content="Hi {name}, welcome to our platform!",
    #     country_codes="US,GB",
    # )
    # print(f"Created template: {new['template_id']}")

    # templates = client.list_templates()
    # for t in templates:
    #     print(f"  {t['template_id']}: {t['template_name']} (status={t['status']})")

    # -- Signature management --
    # sig = client.create_signature("MyCompany")
    # print(f"Created signature: {sig['sign_id']}")

    # signatures = client.list_signatures()
    # for s in signatures:
    #     print(f"  {s['sign_id']}: {s['sign_name']} (status={s['status']})")

    pass
