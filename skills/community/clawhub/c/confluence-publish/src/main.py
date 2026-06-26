"""Confluence publish skill for creating/updating pages via REST API."""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth


ALLOWED_CONFLUENCE_HOST = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)\.atlassian\.net$"
)


def read_env_file(env_path: str) -> Dict[str, str]:
    """Parse .env-like files supporting KEY=VALUE and KEY:VALUE forms."""
    parsed: Dict[str, str] = {}
    pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*(.*)\s*$")

    for raw_line in Path(env_path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = pattern.match(raw_line)
        if not match:
            continue

        key, value = match.groups()
        parsed[key] = value.strip().strip('"').strip("'")

    return parsed


def normalize_base_url(domain_or_url: str) -> str:
    """Normalize and validate Atlassian Confluence Cloud base URL."""
    value = domain_or_url.strip()
    if not value:
        raise ValueError("DOMAIN is required.")

    if value.startswith("http://") or value.startswith("https://"):
        parsed = urlparse(value)
        if parsed.scheme.lower() != "https":
            raise ValueError("Confluence DOMAIN/base_url must use https.")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Confluence DOMAIN/base_url cannot include auth, query, or fragment.")

        host = (parsed.hostname or "").lower()
        if not ALLOWED_CONFLUENCE_HOST.fullmatch(host):
            raise ValueError("Confluence DOMAIN/base_url must target *.atlassian.net.")

        normalized_path = parsed.path.rstrip("/")
        if normalized_path not in ("", "/wiki"):
            raise ValueError("Confluence DOMAIN/base_url path may only be '/wiki'.")

        base = f"https://{host}"
    else:
        bare = value.lower().rstrip("/")
        if "/" in bare or ":" in bare:
            raise ValueError("Confluence DOMAIN must be a tenant or *.atlassian.net host.")

        host = bare if bare.endswith(".atlassian.net") else f"{bare}.atlassian.net"
        if not ALLOWED_CONFLUENCE_HOST.fullmatch(host):
            raise ValueError("Confluence DOMAIN must resolve to a valid *.atlassian.net host.")
        base = f"https://{host}"

    if not base.endswith("/wiki"):
        base = f"{base}/wiki"
    return base


def parse_page_document(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """Extract JSON metadata from first HTML comment and body below it."""
    metadata: Optional[Dict[str, Any]] = None
    body_start = 0

    for match in re.finditer(r"<!--(.*?)-->", raw_text, flags=re.DOTALL):
        comment_text = match.group(1).strip()
        try:
            candidate = json.loads(comment_text)
        except json.JSONDecodeError:
            continue

        if isinstance(candidate, dict):
            metadata = candidate
            body_start = match.end()
            break

    body_html = raw_text[body_start:].lstrip()
    if metadata is None:
        return {}, raw_text.strip()
    return metadata, body_html


class ConfluenceClient:
    """Confluence REST helper with upsert support."""

    def __init__(self, email: str, api_token: str, base_url: str, session: Any = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.auth = HTTPBasicAuth(email, api_token)
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )

    def request(self, method: str, path: str, **kwargs) -> Any:
        response = self.session.request(
            method, f"{self.base_url}{path}", timeout=30, **kwargs
        )
        if not response.ok:
            raise RuntimeError(
                f"Confluence API error {response.status_code}: {response.text[:1000]}"
            )
        return response

    def test_connection(self) -> Dict[str, Any]:
        payload = self.request("GET", "/rest/api/user/current").json()
        return {
            "displayName": payload.get("displayName"),
            "accountId": payload.get("accountId"),
            "type": payload.get("type"),
        }

    def find_page_by_title(self, space_key: str, title: str) -> Optional[Dict[str, Any]]:
        response = self.request(
            "GET",
            "/rest/api/content",
            params={
                "spaceKey": space_key,
                "title": title,
                "expand": "version",
                "limit": 1,
            },
        )
        results = response.json().get("results", [])
        return results[0] if results else None

    def create_page(
        self,
        space_key: str,
        title: str,
        body_html: str,
        parent_page_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {"storage": {"value": body_html, "representation": "storage"}},
        }
        if parent_page_id:
            payload["ancestors"] = [{"id": str(parent_page_id)}]
        return self.request("POST", "/rest/api/content", json=payload).json()

    def update_page(
        self, page_id: str, title: str, body_html: str, version_number: int
    ) -> Dict[str, Any]:
        payload = {
            "id": str(page_id),
            "type": "page",
            "title": title,
            "version": {"number": version_number + 1},
            "body": {"storage": {"value": body_html, "representation": "storage"}},
        }
        return self.request("PUT", f"/rest/api/content/{page_id}", json=payload).json()

    def upsert_page(
        self,
        space_key: str,
        title: str,
        body_html: str,
        parent_page_id: Optional[str] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        existing = self.find_page_by_title(space_key=space_key, title=title)
        if existing:
            result = self.update_page(
                page_id=existing["id"],
                title=title,
                body_html=body_html,
                version_number=existing["version"]["number"],
            )
            return "updated", result

        result = self.create_page(
            space_key=space_key,
            title=title,
            body_html=body_html,
            parent_page_id=parent_page_id,
        )
        return "created", result


class ConfluencePublishSkill:
    """Skill actions for Confluence publishing."""

    ACTIONS = ["publish_page", "test_connection"]

    def _resolve_safe_file(self, path_value: str, field_name: str) -> Path:
        read_root = Path.cwd().resolve()
        candidate = Path(path_value).expanduser()
        if not candidate.is_absolute():
            candidate = read_root / candidate

        try:
            resolved = candidate.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ValueError(f"{field_name} does not exist: {path_value}") from exc

        try:
            resolved.relative_to(read_root)
        except ValueError as exc:
            raise ValueError(
                f"{field_name} must point to a file under the workspace: {read_root}"
            ) from exc

        if not resolved.is_file():
            raise ValueError(f"{field_name} must point to a regular file: {path_value}")

        return resolved

    def _resolve_credentials(self, config: Dict[str, Any]) -> Dict[str, str]:
        credentials = dict(config.get("credentials", {}))

        env_file = config.get("env_file")
        if env_file:
            safe_env_path = self._resolve_safe_file(str(env_file), "env_file")
            credentials = {**read_env_file(str(safe_env_path)), **credentials}

        email = credentials.get("EMAIL") or credentials.get("email") or os.getenv("EMAIL")
        domain = credentials.get("DOMAIN") or credentials.get("domain") or os.getenv("DOMAIN")
        api_token = (
            credentials.get("API_TOKEN")
            or credentials.get("api_token")
            or os.getenv("API_TOKEN")
        )

        missing = [
            name
            for name, value in {"EMAIL": email, "DOMAIN": domain, "API_TOKEN": api_token}.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Missing Confluence credentials: {missing}")

        return {
            "email": str(email),
            "domain": str(domain),
            "api_token": str(api_token),
        }

    def _build_client(self, config: Dict[str, Any]) -> ConfluenceClient:
        creds = self._resolve_credentials(config)
        base_url = normalize_base_url(str(config.get("base_url") or creds["domain"]))
        return ConfluenceClient(
            email=creds["email"], api_token=creds["api_token"], base_url=base_url
        )

    def _load_page_content(self, input_data: str, config: Dict[str, Any]) -> Dict[str, Any]:
        text_content = input_data.strip()
        if config.get("page_path"):
            safe_page_path = self._resolve_safe_file(str(config["page_path"]), "page_path")
            text_content = safe_page_path.read_text(encoding="utf-8")
        if not text_content and not config.get("body_html"):
            raise ValueError("No page content provided. Use input, page_path, or config.body_html.")

        metadata, parsed_body = parse_page_document(text_content) if text_content else ({}, "")
        body_html = str(config.get("body_html") or parsed_body).strip()
        space_key = str(config.get("space_key") or metadata.get("space_key") or "").strip()
        page_title = str(config.get("page_title") or metadata.get("page_title") or "").strip()
        parent_page_id = (
            config.get("parent_page_id")
            if "parent_page_id" in config
            else metadata.get("parent_page_id")
        )

        missing = [k for k, v in {"space_key": space_key, "page_title": page_title}.items() if not v]
        if missing:
            raise ValueError(
                f"Missing required page metadata: {missing}. Provide metadata comment, config keys, or both."
            )
        if not body_html:
            raise ValueError("Page body is empty.")

        return {
            "space_key": space_key,
            "page_title": page_title,
            "parent_page_id": parent_page_id,
            "body_html": body_html,
        }

    def publish_page(self, input_data: str, config: Dict[str, Any]) -> Dict[str, Any]:
        page = self._load_page_content(input_data=input_data, config=config)
        client = self._build_client(config)
        operation, payload = client.upsert_page(
            space_key=page["space_key"],
            title=page["page_title"],
            body_html=page["body_html"],
            parent_page_id=page["parent_page_id"],
        )
        webui = payload.get("_links", {}).get("webui")
        page_url = f"{client.base_url}{webui}" if webui else None

        return {
            "operation": operation,
            "page_id": payload.get("id"),
            "title": payload.get("title"),
            "url": page_url,
            "space_key": page["space_key"],
        }

    def test_connection(self, _input_data: str, config: Dict[str, Any]) -> Dict[str, Any]:
        client = self._build_client(config)
        connection = client.test_connection()
        return {"base_url": client.base_url, **connection}

    def process(self, action: str, input_data: str, config: Dict[str, Any]) -> Dict[str, Any]:
        if action not in self.ACTIONS:
            raise ValueError(f"Unknown action: {action}. Available: {self.ACTIONS}")
        return getattr(self, action)(input_data=input_data, config=config)


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """ClawHub entrypoint."""
    del context
    skill = ConfluencePublishSkill()
    action = event.get("action", "publish_page")
    input_data = event.get("input", "")
    config = event.get("config", {})

    try:
        result = skill.process(action=action, input_data=input_data, config=config)
        return {"status": "success", "action": action, **result}
    except Exception as exc:
        return {"status": "error", "action": action, "error": str(exc)}
