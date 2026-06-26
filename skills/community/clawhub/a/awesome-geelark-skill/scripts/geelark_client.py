#!/usr/bin/env python3
"""GeeLark API Client — Mandatory rules enforced in code

Mandatory rules:
1. Always add energySavingMode=1 when starting cloud phones
2. Automatically close cloud phones after operations
3. Double confirmation required for deletion (raise exception, no direct calls)
4. Only call documented endpoints, no guessing
"""

import requests
import time

from .utils import generate_traceid, get_token, get_base_url
from .cloudphone_logger import CloudPhoneLog


# ============================================
# Whitelist: Only these endpoints are allowed, guessing causes errors
# NOTE: /open/v1/phone/delete is intentionally EXCLUDED
#       Must use execute_phone_deletion() after double confirmation
# ============================================
ALLOWED_ENDPOINTS = {
    # Cloud Phone (delete intentionally excluded)
    "/open/v1/phone/list", "/open/v1/phone/status", "/open/v1/phone/start",
    "/open/v1/phone/stop", "/open/v1/phone/gps/set",
    "/open/v1/phone/addNew", "/open/v1/phone/screenShot",
    # Balance / Billing
    "/open/v1/pay/wallet", "/open/v1/billing/transaction/detail",
    # Group / Tag / Proxy
    "/open/v1/group/list", "/open/v1/group/delete", "/open/v1/tag/delete",
    "/open/v1/proxy/add", "/open/v1/proxy/delete", "/open/v1/proxy/list",
    # App Management
    "/open/v1/app/installable/list", "/open/v1/app/install", "/open/v1/app/list",
    "/open/v1/app/start", "/open/v1/app/stop", "/open/v1/app/uninstall",
    # ADB
    "/open/v1/adb/getData", "/open/v1/adb/setStatus",
    # Task Management
    "/open/v1/task/query", "/open/v1/task/detail", "/open/v1/task/cancel",
    "/open/v1/task/restart", "/open/v1/task/historyRecords", "/open/v1/task/flow/list",
    "/open/v1/task/flow/export", "/open/v1/task/flow/import", "/open/v1/task/rpa/add",
    # RPA Tasks - TikTok
    "/open/v1/rpa/task/tiktokLogin", "/open/v1/rpa/task/tiktokRandomFollow",
    "/open/v1/rpa/task/tiktokRandomFollowAsia", "/open/v1/rpa/task/tiktokRandomStar",
    "/open/v1/rpa/task/tiktokRandomStarAsia", "/open/v1/rpa/task/tiktokRandomComment",
    "/open/v1/rpa/task/tiktokRandomCommentAsia", "/open/v1/rpa/task/tiktokEdit",
    "/open/v1/rpa/task/tiktokDel", "/open/v1/rpa/task/tiktokDelAsia",
    "/open/v1/rpa/task/tiktokHide", "/open/v1/rpa/task/tiktokHideAsia",
    # RPA Tasks - Instagram
    "/open/v1/rpa/task/instagramLogin", "/open/v1/rpa/task/instagramPubReels",
    "/open/v1/rpa/task/instagramPubReelsImages", "/open/v1/rpa/task/instagramEdit",
    "/open/v1/rpa/task/instagramWarmup",
    # RPA Tasks - Facebook
    "/open/v1/rpa/task/faceBookLogin", "/open/v1/rpa/task/faceBookPublish",
    "/open/v1/rpa/task/faceBookPubReels", "/open/v1/rpa/task/faceBookAutoComment",
    "/open/v1/rpa/task/faceBookActiveAccount",
    # RPA Tasks - YouTube
    "/open/v1/rpa/task/youtubePubShort", "/open/v1/rpa/task/youtubePubVideo",
    "/open/v1/rpa/task/youTubeActiveAccount",
    # RPA Tasks - Reddit
    "/open/v1/rpa/task/redditImage", "/open/v1/rpa/task/redditVideo",
    "/open/v1/rpa/task/redditWarmup",
    # RPA Tasks - Threads
    "/open/v1/rpa/task/threadsImage", "/open/v1/rpa/task/threadsVideo",
    # RPA Tasks - Pinterest
    "/open/v1/rpa/task/pinterestImage", "/open/v1/rpa/task/pinterestVideo",
    # RPA Tasks - X
    "/open/v1/rpa/task/xPublish",
    # RPA Tasks - Google
    "/open/v1/rpa/task/googleLogin", "/open/v1/rpa/task/googleAppDownload",
    "/open/v1/rpa/task/googleAppBrowser",
    # RPA Tasks - Shein
    "/open/v1/rpa/task/sheinLogin",
    # RPA Tasks - Other
    "/open/v1/rpa/task/fileUpload", "/open/v1/rpa/task/keyboxUpload",
    "/open/v1/rpa/task/importContacts", "/open/v1/rpa/task/multiPlatformVideoDistribution",
}


class GeeLarkForbiddenError(Exception):
    """Rule violation exception"""
    pass


class GeeLarkClient:
    def __init__(self, token: str = None, base_url: str = None, task_name: str = None, phone_id: str = None):
        if token is None:
            # Load token from config file
            token = get_token()

        if base_url is None:
            # Load base URL from config file
            base_url = get_base_url()

        self.token = token
        self.base_url = base_url
        self._phones_started = set()  # Track started phones, must close after use
        
        # Initialize logger if task_name and phone_id are provided
        self._log = None
        if task_name and phone_id:
            self._log = CloudPhoneLog(task_name, phone_id)
            self._log.info("GeeLarkClient initialized")

    def call(self, endpoint: str, data: dict, timeout: int = 20) -> dict:
        """Call API with mandatory rule checks"""
        # Rule 4: Endpoint whitelist, block guessing
        if endpoint not in ALLOWED_ENDPOINTS:
            raise GeeLarkForbiddenError(
                f"🚫 Endpoint {endpoint} not in whitelist, call blocked.\n"
                f"Must consult SKILL.md or https://github.com/GeeLark/geelark-openapi to confirm endpoint exists."
            )

        # Rule 1: Auto-add energySavingMode when starting cloud phones
        if endpoint == "/open/v1/phone/start":
            if "energySavingMode" not in data:
                data["energySavingMode"] = 1
                print("  ⚡ Auto-enabled energySavingMode=1 (saves costs)")

        resp = requests.post(
            f"{self.base_url}{endpoint}",
            headers={"Content-Type": "application/json", "traceId": generate_traceid(),
                     "Authorization": f"Bearer {self.token}"},
            json=data, timeout=timeout
        )
        body = resp.json()

        # Log API call
        if self._log:
            try:
                self._log.api_call(endpoint, data, body.get('code'), body.get('data'))
            except Exception:
                pass  # Fail silently, don't interrupt main flow

        # Track started phones
        if endpoint == "/open/v1/phone/start" and body.get("code") == 0:
            phone_ids = data.get("ids", [])
            self._phones_started.update(phone_ids)

        return body

    def execute_phone_deletion(self, phone_ids: list, timeout: int = 30, confirmation_code: str = None) -> dict:
        """
        Execute phone deletion - ONLY after double confirmation.

        ⚠️ CRITICAL: This method requires a confirmation_code to prevent accidental calls.
        MUST only be called after:
        1. Listing phones and showing to user
        2. User manually enters phone IDs to confirm
        3. User types 'YES' to final confirmation

        Use delete_helper.delete_cloud_phones_with_confirmation() instead of calling this directly.

        Args:
            phone_ids: List of phone IDs to delete
            timeout: Request timeout in seconds
            confirmation_code: Required confirmation string (must be 'DELETE_CONFIRMED')

        Returns:
            API response dict

        Raises:
            GeeLarkForbiddenError: If confirmation_code is not provided or invalid
        """
        if confirmation_code != 'DELETE_CONFIRMED':
            raise GeeLarkForbiddenError(
                "🚫 Deletion blocked: Missing or invalid confirmation_code.\n"
                "Must use delete_helper.delete_cloud_phones_with_confirmation() for safe deletion."
            )

        if not phone_ids:
            raise GeeLarkForbiddenError("🚫 Cannot delete empty phone ID list")
        
        print(f"  ⚠️  Executing deletion for {len(phone_ids)} phone(s): {phone_ids}")
        
        resp = requests.post(
            f"{self.base_url}/open/v1/phone/delete",
            headers={"Content-Type": "application/json", "traceId": generate_traceid(),
                     "Authorization": f"Bearer {self.token}"},
            json={"ids": phone_ids}, timeout=timeout
        )
        body = resp.json()

        # Log deletion
        if self._log:
            try:
                self._log.api_call("/open/v1/phone/delete", {"ids": phone_ids}, body.get('code'), body.get('data'))
            except Exception:
                pass  # Fail silently, don't interrupt main flow

        if body.get("code") == 0:
            print(f"  ✅ Successfully deleted {len(phone_ids)} phone(s)")
        else:
            print(f"  ❌ Deletion failed: {body.get('msg', 'Unknown error')}")

        return body

    def stop_started_phones(self):
        """Rule 2: Close all started cloud phones"""
        if not self._phones_started:
            return
        print(f"\n  🛑 Auto-closing started cloud phones: {self._phones_started}")
        for phone_id in list(self._phones_started):
            try:
                self.call("/open/v1/phone/stop", {"ids": [phone_id]})
                print(f"    ✅ Closed {phone_id}")
            except Exception as e:
                print(f"    ⚠️ Failed to close {phone_id}: {e}")
        self._phones_started.clear()

    def save_log(self):
        """Save operation log to file"""
        if self._log:
            self._log.save()
            self._log = None

    # ============================================
    # Convenience methods
    # ============================================

    def phone_list(self):
        return self.call("/open/v1/phone/list", {})

    def phone_status(self, phone_ids):
        return self.call("/open/v1/phone/status", {"ids": phone_ids})

    def phone_stop(self, phone_ids):
        return self.call("/open/v1/phone/stop", {"ids": phone_ids})

    def phone_screenshot(self, phone_id):
        return self.call("/open/v1/phone/screenShot", {"id": phone_id})

    def wallet(self):
        return self.call("/open/v1/pay/wallet", {})

    def billing_transactions(self):
        return self.call("/open/v1/billing/transaction/detail", {})

    def task_history(self, page=1, page_size=50):
        return self.call("/open/v1/task/historyRecords", {"page": page, "pageSize": page_size})

    def rpa_task(self, task_name, params):
        """Generic RPA task creation"""
        return self.call(f"/open/v1/rpa/task/{task_name}", params)
