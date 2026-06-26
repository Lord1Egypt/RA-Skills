"""
EngageLab App Push API client.

Wraps main Push REST API endpoints: create push, batch push (regid/alias),
device tags/alias (get/set), delete user, message recall, test push (validate),
tag count, push plan (create/list), and scheduled tasks (CRUD). Uses HTTP Basic
Authentication with AppKey and Master Secret.

Usage:
    from push_client import EngageLabPush

    client = EngageLabPush("YOUR_APP_KEY", "YOUR_MASTER_SECRET")

    # Broadcast notification
    result = client.push(to="all", body={
        "platform": "all",
        "notification": {"alert": "Hello!", "android": {"title": "Hi"}, "ios": {"sound": "default"}},
        "options": {"apns_production": False},
    })
    print(result["msg_id"])

    # Get device tags/alias
    info = client.get_device("registration_id_xxx")
    # Set tags/alias
    client.set_device("registration_id_xxx", tags_add=["tag1"], alias="user1")
"""

import json
import requests
from typing import Any, Optional

BASE_URL = "https://pushapi-sgp.engagelab.com"


class EngageLabPushError(Exception):
    """Raised when the App Push API returns an error response."""

    def __init__(self, code: int, message: str, http_status: int):
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(f"[{http_status}] Error {code}: {message}")


class EngageLabPush:
    """Client for the EngageLab App Push REST API (v4)."""

    def __init__(self, app_key: str, master_secret: str, base_url: str = BASE_URL):
        self._auth = (app_key, master_secret)
        self._headers = {"Content-Type": "application/json"}
        self._base_url = base_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        payload: Optional[dict] = None,
        params: Optional[Any] = None,
    ) -> dict:
        url = f"{self._base_url}{path}"
        resp = requests.request(
            method,
            url,
            auth=self._auth,
            headers=self._headers,
            json=payload,
            params=params,
        )

        if resp.status_code >= 400:
            try:
                body = resp.json()
                err = body.get("error", body)
                code = err.get("code", resp.status_code)
                msg = err.get("message", resp.text)
            except (ValueError, json.JSONDecodeError):
                code = resp.status_code
                msg = resp.text
            raise EngageLabPushError(code=code, message=msg, http_status=resp.status_code)

        if not resp.content:
            return {}
        return resp.json()

    # ── Create Push ──────────────────────────────────────────────────

    def push(
        self,
        to: Any,
        body: dict,
        from_sender: str = "push",
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """
        Create push (POST /v4/push).

        `to`: "all" or dict e.g. {"tag": ["t1"]}, {"alias": ["a1"]}, {"registration_id": ["id1"]}.
        `body`: must include platform and one of notification, message, live_activity, voip.
        Returns dict with msg_id and optional request_id.
        """
        payload = {"from": from_sender, "to": to, "body": body}
        if request_id is not None:
            payload["request_id"] = request_id
        if custom_args is not None:
            payload["custom_args"] = custom_args
        return self._request("POST", "/v4/push", payload)

    # ── Batch Single Push ────────────────────────────────────────────

    def batch_push_regid(self, requests_list: list) -> dict:
        """
        Batch push by registration_id (POST /v4/batch/push/regid).
        Each item: target, platform, notification/message, options, custom_args.
        Max 500 items; target must be unique per batch.
        """
        return self._request("POST", "/v4/batch/push/regid", {"requests": requests_list})

    def batch_push_alias(self, requests_list: list) -> dict:
        """
        Batch push by alias (POST /v4/batch/push/alias).
        Same structure as batch_push_regid; target is alias.
        """
        return self._request("POST", "/v4/batch/push/alias", {"requests": requests_list})

    # ── Device (Tag / Alias) ─────────────────────────────────────────

    def get_device(self, registration_id: str) -> dict:
        """Get device tags and alias (GET /v4/devices/{registration_id})."""
        return self._request("GET", f"/v4/devices/{registration_id}")

    def set_device(
        self,
        registration_id: str,
        tags_add: Optional[list] = None,
        tags_remove: Optional[list] = None,
        alias: Optional[str] = None,
    ) -> dict:
        """
        Set device tags and/or alias (POST /v4/devices/{registration_id}).
        tags_add / tags_remove: lists of tag strings.
        alias: single string (one alias per device).
        """
        payload = {}
        if tags_add is not None or tags_remove is not None:
            payload["tags"] = {}
            if tags_add:
                payload["tags"]["add"] = tags_add
            if tags_remove:
                payload["tags"]["remove"] = tags_remove
        if alias is not None:
            payload["alias"] = alias
        return self._request("POST", f"/v4/devices/{registration_id}", payload)

    def delete_device(self, registration_id: str) -> dict:
        """Delete user and all related data (DELETE /v4/devices/{registration_id}). Async."""
        return self._request("DELETE", f"/v4/devices/{registration_id}")

    # ── Tag count ─────────────────────────────────────────────────────

    def tags_count(self, tags: list, platform: str) -> dict:
        """Query tag counts (GET /v4/tags_count). platform: android, ios, or hmos. Up to 1000 tags."""
        params = [("platform", platform)]
        for t in tags:
            params.append(("tags", t))
        return self._request("GET", "/v4/tags_count", params=params)

    # ── Message recall ────────────────────────────────────────────────

    def recall(self, msg_id: str) -> dict:
        """Recall a message (DELETE /v4/push/withdraw/{msg_id}). Only within one day."""
        return self._request("DELETE", f"/v4/push/withdraw/{msg_id}")

    # ── Test push (validate) ──────────────────────────────────────────

    def validate_push(
        self,
        to: Any,
        body: dict,
        from_sender: str = "push",
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Validate push request without sending (POST /v4/push/validate). Same body as push."""
        payload = {"from": from_sender, "to": to, "body": body}
        if request_id is not None:
            payload["request_id"] = request_id
        if custom_args is not None:
            payload["custom_args"] = custom_args
        return self._request("POST", "/v4/push/validate", payload)

    # ── Push plan ────────────────────────────────────────────────────

    def push_plan_create_or_update(self, plan_id: str, plan_description: Optional[str] = None) -> dict:
        """Create or update push plan (POST /v4/push_plan)."""
        payload = {"plan_id": plan_id}
        if plan_description is not None:
            payload["plan_description"] = plan_description
        return self._request("POST", "/v4/push_plan", payload)

    def push_plan_list(
        self,
        page_index: int = 1,
        page_size: int = 20,
        send_source: Optional[int] = None,
        search_description: Optional[str] = None,
    ) -> dict:
        """List push plans (GET /v4/push_plan/list). send_source: 0=API, 1=Console."""
        params = {"page_index": page_index, "page_size": page_size}
        if send_source is not None:
            params["send_source"] = send_source
        if search_description is not None:
            params["search_description"] = search_description
        return self._request("GET", "/v4/push_plan/list", params=params)

    # ── Scheduled tasks ──────────────────────────────────────────────

    def schedule_create(self, name: str, trigger: dict, push: dict, enabled: bool = True) -> dict:
        """Create scheduled task (POST /v4/schedules). trigger: single/periodical/intelligent."""
        return self._request("POST", "/v4/schedules", {
            "name": name,
            "enabled": enabled,
            "trigger": trigger,
            "push": push,
        })

    def schedule_get(self, schedule_id: str) -> dict:
        """Get scheduled task (GET /v4/schedules/{schedule_id})."""
        return self._request("GET", f"/v4/schedules/{schedule_id}")

    def schedule_update(self, schedule_id: str, name: Optional[str] = None, enabled: Optional[bool] = None, trigger: Optional[dict] = None, push: Optional[dict] = None) -> dict:
        """Update scheduled task (PUT /v4/schedules/{schedule_id})."""
        payload = {}
        if name is not None:
            payload["name"] = name
        if enabled is not None:
            payload["enabled"] = enabled
        if trigger is not None:
            payload["trigger"] = trigger
        if push is not None:
            payload["push"] = push
        return self._request("PUT", f"/v4/schedules/{schedule_id}", payload)

    def schedule_delete(self, schedule_id: str) -> dict:
        """Delete scheduled task (DELETE /v4/schedules/{schedule_id})."""
        return self._request("DELETE", f"/v4/schedules/{schedule_id}")

    # ── Statistics ────────────────────────────────────────────────────

    def message_detail(self, message_ids: list) -> dict:
        """Get message statistics (GET /v4/status/detail). Up to 100 message_ids. Data up to one month."""
        params = {"message_ids": ",".join(message_ids)}
        return self._request("GET", "/v4/status/detail", params=params)


if __name__ == "__main__":
    APP_KEY = "YOUR_APP_KEY"
    MASTER_SECRET = "YOUR_MASTER_SECRET"

    client = EngageLabPush(APP_KEY, MASTER_SECRET)

    # -- Broadcast push (uncomment with real credentials) --
    # r = client.push("all", {
    #     "platform": "all",
    #     "notification": {"alert": "Hello!", "android": {"title": "Hi"}, "ios": {"sound": "default"}},
    #     "options": {"apns_production": False},
    # })
    # print("msg_id:", r["msg_id"])

    # -- Get device --
    # info = client.get_device("REGISTRATION_ID")
    # print("tags:", info.get("tags"), "alias:", info.get("alias"))

    pass
