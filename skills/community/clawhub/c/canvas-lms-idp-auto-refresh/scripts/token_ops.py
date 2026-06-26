from __future__ import annotations

import html
import logging
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import requests

from auth_session import AppConfig, FlowError, mask

LOGGER = logging.getLogger("elearning_login")


@dataclass
class ExistingTokenEntry:
    purpose: str
    delete_url: str
    token_id: str | None


class CanvasTokenManager:
    def __init__(self, *, session: requests.Session, config: AppConfig) -> None:
        self.session = session
        self.config = config

    def create_canvas_token(self, csrf_token: str) -> dict[str, Any]:
        settings_res = self.session.get(
            self.config.settings_referer,
            timeout=self.config.timeout_seconds,
        )
        settings_res.raise_for_status()

        form_info = extract_token_form_info(settings_res.text)
        token_api_url = form_info["action"] if form_info else self.config.token_api_url

        headers = {
            "X-CSRF-Token": csrf_token,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self.config.settings_referer,
            "Origin": "https://elearning.fudan.edu.cn",
        }
        data: dict[str, str] = {
            "token[purpose]": self.config.token_purpose,
            "token[expires_at]": "",
        }
        if form_info:
            data["utf8"] = "✓"
            data["authenticity_token"] = form_info["authenticity_token"]

        res = self.session.post(
            token_api_url,
            headers=headers,
            data=data,
            timeout=self.config.timeout_seconds,
        )
        if res.status_code != 200:
            raise FlowError(
                f"Token 创建失败: HTTP {res.status_code} | body={res.text[:500]}"
            )

        body = res.json()
        LOGGER.info("Token 创建成功。id=%s", body.get("id"))
        return body

    def cleanup_old_tokens_by_purpose(
        self,
        *,
        csrf_token: str,
        purpose: str,
        keep_token_id: str | None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        settings_res = self.session.get(
            self.config.settings_referer,
            timeout=self.config.timeout_seconds,
        )
        settings_res.raise_for_status()

        all_tokens = extract_existing_tokens_from_settings(settings_res.text)
        targets = select_tokens_for_cleanup(
            all_tokens,
            purpose=purpose,
            keep_token_id=keep_token_id,
        )

        summary: dict[str, Any] = {
            "purpose": purpose,
            "keep_token_id": keep_token_id,
            "matched": len([t for t in all_tokens if normalize_space(t.purpose) == normalize_space(purpose)]),
            "to_delete": len(targets),
            "deleted": 0,
            "failed": [],
            "dry_run": dry_run,
        }

        if not targets:
            LOGGER.info("清理模式：未找到可删除旧 token。purpose=%s", purpose)
            return summary

        headers = {
            "X-CSRF-Token": csrf_token,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self.config.settings_referer,
            "Origin": "https://elearning.fudan.edu.cn",
        }

        for token in targets:
            delete_url = token.delete_url
            if not delete_url.startswith("http"):
                delete_url = urljoin(self.config.settings_referer, delete_url)

            if dry_run:
                LOGGER.info("[dry-run] 将删除 token: purpose=%s id=%s url=%s", token.purpose, token.token_id, delete_url)
                summary["deleted"] = int(summary["deleted"]) + 1
                continue

            res = self.session.delete(
                delete_url,
                headers=headers,
                timeout=self.config.timeout_seconds,
            )
            if res.status_code in {200, 204}:
                summary["deleted"] = int(summary["deleted"]) + 1
                continue

            summary["failed"].append(
                {
                    "url": delete_url,
                    "status": res.status_code,
                    "body": (res.text or "")[:300],
                }
            )
            LOGGER.warning("删除旧 token 失败: status=%s url=%s", res.status_code, delete_url)

        LOGGER.info(
            "清理完成。purpose=%s to_delete=%s deleted=%s failed=%s",
            purpose,
            summary["to_delete"],
            summary["deleted"],
            len(summary["failed"]),
        )
        return summary


def extract_token_form_info(html_text: str) -> dict[str, str] | None:
    form_match = re.search(
        r'<form[^>]*action="(https://elearning\.fudan\.edu\.cn/api/v1/users/self/tokens)"[\s\S]*?</form>',
        html_text,
        flags=re.IGNORECASE,
    )
    if not form_match:
        return None

    form_html = form_match.group(0)
    action = html.unescape(form_match.group(1))
    auth_match = re.search(
        r'name="authenticity_token"\s+value="([^"]+)"',
        form_html,
        flags=re.IGNORECASE,
    )
    if not auth_match:
        return None

    return {
        "action": action,
        "authenticity_token": html.unescape(auth_match.group(1)),
    }


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_token_id_from_url(url: str) -> str | None:
    match = re.search(r"/api/v1/users/self/tokens/(\d+)$", url)
    if not match:
        return None
    return match.group(1)


def extract_existing_tokens_from_settings(html_text: str) -> list[ExistingTokenEntry]:
    rows = re.findall(
        r'<tr[^>]*class="[^"]*access_token[^"]*"[^>]*>(.*?)</tr>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    results: list[ExistingTokenEntry] = []

    for row in rows:
        purpose_match = re.search(
            r'<td[^>]*class="purpose"[^>]*>(.*?)</td>',
            row,
            flags=re.IGNORECASE | re.DOTALL,
        )
        delete_match = re.search(
            r'<a[^>]*(?=[^>]*class="[^"]*delete_key_link[^"]*")(?=[^>]*rel="([^"]+)")[^>]*>',
            row,
            flags=re.IGNORECASE,
        )
        show_match = re.search(
            r'<a[^>]*(?=[^>]*class="[^"]*show_token_link[^"]*")(?=[^>]*rel="([^"]+)")[^>]*>',
            row,
            flags=re.IGNORECASE,
        )

        if not purpose_match or not delete_match:
            continue

        purpose_text = normalize_space(html.unescape(strip_tags(purpose_match.group(1))))
        delete_url = html.unescape(delete_match.group(1))
        show_url = html.unescape(show_match.group(1)) if show_match else ""
        token_id = parse_token_id_from_url(show_url)

        results.append(
            ExistingTokenEntry(
                purpose=purpose_text,
                delete_url=delete_url,
                token_id=token_id,
            )
        )

    return results


def select_tokens_for_cleanup(
    tokens: list[ExistingTokenEntry],
    *,
    purpose: str,
    keep_token_id: str | None,
) -> list[ExistingTokenEntry]:
    target = normalize_space(purpose)
    keep = keep_token_id.strip() if keep_token_id else None

    matched = [t for t in tokens if normalize_space(t.purpose) == target]
    if not keep:
        return matched

    return [t for t in matched if t.token_id != keep]
