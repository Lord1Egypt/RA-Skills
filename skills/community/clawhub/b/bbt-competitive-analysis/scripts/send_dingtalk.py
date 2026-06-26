from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class DingTalkResult:
    ok: bool
    response: dict[str, Any]


class DingTalkWebhookClient:
    def __init__(self, webhook: str, secret: str | None = None, timeout_seconds: int = 20) -> None:
        self.webhook = webhook
        self.secret = secret
        self.timeout_seconds = timeout_seconds

    def send_markdown(self, title: str, markdown_text: str) -> DingTalkResult:
        payload = {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": markdown_text},
        }
        response = self._post(payload)
        success = response.get("errcode") in (0, "0", None)
        return DingTalkResult(ok=success, response=response)

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = self._signed_url()
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))

    def _signed_url(self) -> str:
        if not self.secret:
            return self.webhook

        # DingTalk signed webhook:
        # sign = urlEncode(base64(hmac_sha256(secret, f"{timestamp}\n{secret}")))
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}".encode("utf-8")
        hmac_digest = hmac.new(self.secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
        sign_b64 = base64.b64encode(hmac_digest).decode("utf-8")

        parsed = urllib.parse.urlparse(self.webhook)
        query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        query.append(("timestamp", timestamp))
        # NOTE: let urlencode do the encoding exactly once
        query.append(("sign", sign_b64))
        new_query = urllib.parse.urlencode(query, quote_via=urllib.parse.quote_plus)
        return urllib.parse.urlunparse(parsed._replace(query=new_query))


def build_summary_markdown(
    report_title: str,
    category: str,
    executive_summary: str,
    key_findings: list[dict[str, Any]],
    markdown_url: str,
    html_url: str,
) -> str:
    lines = [
        f"## {report_title}",
        "",
        f"- 品类：`{category}`",
        f"- Markdown：{markdown_url}",
        f"- HTML：{html_url}",
        "",
        "### 执行摘要",
        executive_summary,
        "",
        "### 关键发现",
    ]
    for item in key_findings:
        dimension = item.get("维度") or item.get("项目") or "发现"
        conclusion = item.get("核心结论") or item.get("结论") or ""
        lines.append(f"- {dimension}：{conclusion}")
    return "\n".join(lines)
