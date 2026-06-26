#!/usr/bin/env python3
"""
Polling helper for ai-email-gateway.

Workflow:
1) Trigger manual sync for [last_checked_at, now)
2) Wait for sync job completion
3) Query incoming messages in same range
4) Print only unseen messages and update local state

Environment variables:
- GATEWAY_BASE_URL
- GATEWAY_API_KEY
- ACCOUNT_ID (single account mode)
- ACCOUNT_IDS (comma-separated account ids for multi-account mode)

Optional:
- STATE_FILE (default: .agent_state_email.json)
- SYNC_FOLDERS (comma-separated, default: INBOX)
- INCLUDE_SUBFOLDERS (true/false, default: true)
- LIMIT_PER_FOLDER (default: 500)
- LIST_LIMIT (default: 200)
- REPORT_SUSPICIOUS_COUNT (true/false, default: false)
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib import error, request


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_iso(value: str) -> str:
    if value.endswith("Z"):
        return value
    return value + "Z"


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required env var: {name}")
    return value


@dataclass
class Config:
    base_url: str
    api_key: str
    account_ids: list[str]
    state_file: str
    folders: list[str]
    include_subfolders: bool
    limit_per_folder: int
    list_limit: int
    report_suspicious_count: bool


def load_config() -> Config:
    base_url = env_required("GATEWAY_BASE_URL").rstrip("/")
    api_key = env_required("GATEWAY_API_KEY")
    raw_account_ids = os.getenv("ACCOUNT_IDS", "").strip()
    if raw_account_ids:
        account_ids = [v.strip() for v in raw_account_ids.split(",") if v.strip()]
    else:
        account_ids = [env_required("ACCOUNT_ID")]
    # Keep order but remove duplicates.
    account_ids = list(dict.fromkeys(account_ids))
    state_file = os.getenv("STATE_FILE", ".agent_state_email.json")
    raw_folders = os.getenv("SYNC_FOLDERS", "INBOX")
    folders = [v.strip() for v in raw_folders.split(",") if v.strip()]
    include_subfolders = os.getenv("INCLUDE_SUBFOLDERS", "true").lower() in {"1", "true", "yes"}
    limit_per_folder = int(os.getenv("LIMIT_PER_FOLDER", "500"))
    list_limit = int(os.getenv("LIST_LIMIT", "200"))
    report_suspicious_count = os.getenv("REPORT_SUSPICIOUS_COUNT", "false").lower() in {"1", "true", "yes"}
    return Config(
        base_url=base_url,
        api_key=api_key,
        account_ids=account_ids,
        state_file=state_file,
        folders=folders,
        include_subfolders=include_subfolders,
        limit_per_folder=limit_per_folder,
        list_limit=list_limit,
        report_suspicious_count=report_suspicious_count,
    )


def api_request(cfg: Config, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{cfg.base_url}{path}"
    body = None
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, method=method, data=body, headers=headers)
    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"http {exc.code} {method} {path}: {details}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"network error for {method} {path}: {exc}") from exc


def load_state(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {"last_checked_at": "1970-01-01T00:00:00Z", "seen_ids": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(path: str, state: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def _default_account_state() -> dict[str, Any]:
    return {"last_checked_at": "1970-01-01T00:00:00Z", "seen_ids": []}


def _state_for_account(state: dict[str, Any], account_id: str) -> dict[str, Any]:
    accounts = state.get("accounts")
    if isinstance(accounts, dict):
        account_state = accounts.get(account_id)
        if isinstance(account_state, dict):
            return {
                "last_checked_at": account_state.get("last_checked_at", "1970-01-01T00:00:00Z"),
                "seen_ids": account_state.get("seen_ids", []),
            }
        return _default_account_state()

    # Backward compatibility: legacy single-account state shape.
    return {
        "last_checked_at": state.get("last_checked_at", "1970-01-01T00:00:00Z"),
        "seen_ids": state.get("seen_ids", []),
    }


def _set_state_for_account(state: dict[str, Any], account_id: str, account_state: dict[str, Any]) -> None:
    accounts = state.get("accounts")
    if not isinstance(accounts, dict):
        accounts = {}
        state["accounts"] = accounts
    accounts[account_id] = account_state
    # Remove legacy top-level keys after migrating to multi-account shape.
    state.pop("last_checked_at", None)
    state.pop("seen_ids", None)


def wait_for_job(cfg: Config, job_id: str, timeout_s: int = 120) -> dict[str, Any]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status = api_request(cfg, "GET", f"/v1/jobs/{job_id}")
        state = status.get("status")
        if state in {"done", "failed", "canceled"}:
            return status
        time.sleep(1.0)
    raise RuntimeError(f"job timeout after {timeout_s}s: {job_id}")


def main() -> int:
    try:
        cfg = load_config()
        state = load_state(cfg.state_file)
        results: list[dict[str, Any]] = []

        for account_id in cfg.account_ids:
            account_state = _state_for_account(state, account_id)
            now_iso = utc_now_iso()
            since_iso = normalize_iso(account_state.get("last_checked_at", "1970-01-01T00:00:00Z"))

            sync_payload = {
                "folders": cfg.folders,
                "since": since_iso,
                "until": now_iso,
                "include_subfolders": cfg.include_subfolders,
                "limit_per_folder": cfg.limit_per_folder,
            }
            sync_job = api_request(cfg, "POST", f"/v1/accounts/{account_id}/sync", sync_payload)
            job_id = sync_job.get("job_id")
            if not job_id:
                raise RuntimeError(f"sync failed to return job_id for {account_id}: {sync_job}")
            final_status = wait_for_job(cfg, job_id)
            if final_status.get("status") != "done":
                raise RuntimeError(f"sync job did not complete successfully for {account_id}: {final_status}")

            list_payload = {
                "since": since_iso,
                "until": now_iso,
                "direction": "incoming",
                "limit": cfg.list_limit,
                "offset": 0,
                "include_body": True,
            }
            listed = api_request(cfg, "POST", f"/v1/accounts/{account_id}/messages:list", list_payload)
            messages = listed.get("messages", [])
            seen_ids = set(account_state.get("seen_ids", []))
            unseen = [m for m in messages if m.get("id") not in seen_ids]
            output: dict[str, Any] = {
                "account_id": account_id,
                "new_message_count": len(unseen),
                "messages": unseen,
            }

            if cfg.report_suspicious_count:
                suspicious_payload = {
                    **list_payload,
                    "include_body": False,
                    "exclude_suspicious": False,
                }
                all_listed = api_request(cfg, "POST", f"/v1/accounts/{account_id}/messages:list", suspicious_payload)
                all_messages = all_listed.get("messages", [])
                unseen_all = [m for m in all_messages if m.get("id") not in seen_ids]
                suspicious = [m for m in unseen_all if (m.get("safety") or {}).get("is_suspicious")]
                output["suspicious_count"] = len(suspicious)

            results.append(output)

            seen_ids.update([m.get("id") for m in unseen if m.get("id")])
            _set_state_for_account(
                state,
                account_id,
                {
                    "seen_ids": sorted(seen_ids),
                    "last_checked_at": now_iso,
                },
            )

        if len(results) == 1:
            print(json.dumps(results[0], indent=2))
        else:
            print(json.dumps({"account_count": len(results), "accounts": results}, indent=2))

        save_state(cfg.state_file, state)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
