"""
EngageLab WhatsApp Business API client.

Wraps all WhatsApp REST API endpoints: send messages (template, text, image,
video, audio, document, sticker), and template CRUD. Handles authentication,
request construction, and error handling.

Usage:
    from whatsapp_client import EngageLabWhatsApp

    client = EngageLabWhatsApp("YOUR_DEV_KEY", "YOUR_DEV_SECRET")

    # Send template message
    result = client.send_template(
        to=["00447911123456"],
        template_name="code",
        language="en",
        body_params=[{"type": "text", "text": "12345"}],
    )

    # Send text message (requires 24h user reply window)
    result = client.send_text(["8613800138000"], "Hello!")
"""

import base64
import json
import requests
from typing import Optional


BASE_URL = "https://wa.api.engagelab.cc"


class EngageLabWhatsAppError(Exception):
    """Raised when the WhatsApp API returns an error response."""

    def __init__(self, code: int, message: str, http_status: int):
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(f"[{http_status}] Error {code}: {message}")


class EngageLabWhatsApp:
    """Client for the EngageLab WhatsApp Business REST API."""

    def __init__(self, dev_key: str, dev_secret: str, base_url: str = BASE_URL):
        auth = base64.b64encode(f"{dev_key}:{dev_secret}".encode()).decode()
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }
        self._base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, payload: Optional[dict] = None, params: Optional[dict] = None):
        url = f"{self._base_url}{path}"
        resp = requests.request(method, url, headers=self._headers, json=payload, params=params)

        if resp.status_code >= 400:
            try:
                body = resp.json()
            except (ValueError, json.JSONDecodeError):
                body = {"code": resp.status_code, "message": resp.text}
            raise EngageLabWhatsAppError(
                code=body.get("code", resp.status_code),
                message=body.get("message", resp.text),
                http_status=resp.status_code,
            )

        if not resp.content:
            return {}
        return resp.json()

    def _send(
        self,
        to: list,
        body: dict,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        payload = {"to": to, "body": body}
        if from_number:
            payload["from"] = from_number
        if request_id:
            payload["request_id"] = request_id
        if custom_args:
            payload["custom_args"] = custom_args
        return self._request("POST", "/v1/messages", payload)

    # ── Message Sending ─────────────────────────────────────────────

    def send_template(
        self,
        to: list,
        template_name: str,
        language: str,
        components: Optional[list] = None,
        header_params: Optional[list] = None,
        body_params: Optional[list] = None,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """
        Send a template message. Can be sent proactively (no 24h window needed).

        Use `components` for full control, or use the convenience params
        `header_params` and `body_params` to build components automatically.

        Each param in header_params/body_params is a dict like:
            {"type": "text", "text": "value"}
            {"type": "image", "image": {"link": "https://..."}}
        """
        template = {"name": template_name, "language": language}

        if components:
            template["components"] = components
        else:
            built_components = []
            if header_params:
                built_components.append({"type": "header", "parameters": header_params})
            if body_params:
                built_components.append({"type": "body", "parameters": body_params})
            if built_components:
                template["components"] = built_components

        return self._send(
            to=to,
            body={"type": "template", "template": template},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_text(
        self,
        to: list,
        text: str,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send a text message. Requires 24h user reply window."""
        return self._send(
            to=to,
            body={"type": "text", "text": {"body": text}},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_image(
        self,
        to: list,
        link: str,
        caption: Optional[str] = None,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send an image message. JPEG/PNG, max 5MB. Requires 24h window."""
        image = {"link": link}
        if caption:
            image["caption"] = caption
        return self._send(
            to=to,
            body={"type": "image", "image": image},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_video(
        self,
        to: list,
        link: str,
        caption: Optional[str] = None,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send a video message. MP4/3GPP, max 16MB. Requires 24h window."""
        video = {"link": link}
        if caption:
            video["caption"] = caption
        return self._send(
            to=to,
            body={"type": "video", "video": video},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_audio(
        self,
        to: list,
        link: str,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send an audio message. AAC/MP4/AMR/MPEG/OGG, max 16MB. Requires 24h window."""
        return self._send(
            to=to,
            body={"type": "audio", "audio": {"link": link}},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_document(
        self,
        to: list,
        link: str,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send a document/file message. Any MIME type, max 100MB. Requires 24h window."""
        doc = {"link": link}
        if filename:
            doc["filename"] = filename
        if caption:
            doc["caption"] = caption
        return self._send(
            to=to,
            body={"type": "document", "document": doc},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    def send_sticker(
        self,
        to: list,
        link: str,
        from_number: Optional[str] = None,
        request_id: Optional[str] = None,
        custom_args: Optional[dict] = None,
    ) -> dict:
        """Send a sticker message. WebP only, static 100KB / animated 500KB. Requires 24h window."""
        return self._send(
            to=to,
            body={"type": "sticker", "sticker": {"link": link}},
            from_number=from_number,
            request_id=request_id,
            custom_args=custom_args,
        )

    # ── Template Management ─────────────────────────────────────────

    def list_templates(
        self,
        name: Optional[str] = None,
        language_code: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list:
        """
        List WABA templates with optional filters.

        Args:
            name: Fuzzy match on template name.
            language_code: Language code (e.g., "en", "zh_CN").
            category: AUTHENTICATION, MARKETING, or UTILITY.
            status: APPROVED, PENDING, REJECTED, DISABLED, etc.
        """
        params = {}
        if name:
            params["name"] = name
        if language_code:
            params["language_code"] = language_code
        if category:
            params["category"] = category
        if status:
            params["status"] = status
        return self._request("GET", "/v1/templates", params=params)

    def get_template(self, template_id: str) -> dict:
        """Get full details of a specific template by ID."""
        return self._request("GET", f"/v1/templates/{template_id}")

    def create_template(
        self,
        name: str,
        language: str,
        category: str,
        components: list,
    ) -> dict:
        """
        Create a WABA message template.

        Args:
            name: Lowercase letters, numbers, underscores only.
            language: Language code (e.g., "en", "zh_CN").
            category: AUTHENTICATION, MARKETING, or UTILITY.
            components: Template components (HEADER, BODY, FOOTER, BUTTONS).

        Returns dict with template_id on success.
        """
        return self._request("POST", "/v1/templates", {
            "name": name,
            "language": language,
            "category": category,
            "components": components,
        })

    def update_template(self, template_id: str, components: list) -> dict:
        """Update a template's components by template ID."""
        return self._request("PUT", f"/v1/templates/{template_id}", {
            "components": components,
        })

    def delete_template(self, template_name: str) -> dict:
        """
        Delete a template by name. Deletes ALL language variants.

        Note: Uses template name (not ID) in the URL path.
        """
        return self._request("DELETE", f"/v1/templates/{template_name}")


if __name__ == "__main__":
    DEV_KEY = "YOUR_DEV_KEY"
    DEV_SECRET = "YOUR_DEV_SECRET"

    client = EngageLabWhatsApp(DEV_KEY, DEV_SECRET)

    # -- Send template message --
    # result = client.send_template(
    #     to=["00447911123456"],
    #     template_name="code",
    #     language="en",
    #     body_params=[{"type": "text", "text": "12345"}],
    # )
    # print(f"Sent! message_id={result['message_id']}")

    # -- Send text message (requires 24h window) --
    # result = client.send_text(["8613800138000"], "Hello, your order has shipped!")
    # print(f"Sent! message_id={result['message_id']}")

    # -- Send image --
    # result = client.send_image(
    #     ["8613800138000"],
    #     "https://example.com/product.jpg",
    #     caption="Your product photo",
    # )
    # print(f"Image sent! message_id={result['message_id']}")

    # -- List templates --
    # templates = client.list_templates(status="APPROVED")
    # for t in templates:
    #     print(f"  {t['id']}: {t['name']} ({t['language']}) - {t['status']}")

    # -- Create template --
    # result = client.create_template(
    #     name="welcome_message",
    #     language="en",
    #     category="UTILITY",
    #     components=[
    #         {"type": "BODY", "text": "Welcome {{1}}! Your account is ready.",
    #          "example": {"body_text": [["John"]]}},
    #     ],
    # )
    # print(f"Created template: {result['template_id']}")

    # -- Delete template (all languages) --
    # client.delete_template("welcome_message")

    pass
