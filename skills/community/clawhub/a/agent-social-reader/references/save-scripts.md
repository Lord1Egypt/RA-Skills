# Save Scripts

Built-in fallback scripts for archiving content to Notion and Obsidian. These are used when no native Notion/Obsidian tool is available in the current runtime.

For the ima OpenAPI (Scene 2 & 3), see `references/tool-details.md` §9.

Use these scripts only after the current user request explicitly asks to save or archive the current item. Do not run them during read-only summarization. Confirm the target destination for the current item before writing.

Credential helpers in this file read only the explicit environment variables and config paths named below. They must not enumerate arbitrary environment variables or scan the user's home directory. Prefer platform secret storage or environment variables; read local plaintext config only if the user previously approved local config storage.

---

## Save to ima (Scene 2 & 3 — OpenAPI)

**When to use**: User says "save to ima" and no native ima skill is available (i.e., not running inside ima). Use this after completing the scene detection in SKILL.md.

Before writing, confirm the target ima scenario and knowledge base for the current item.

### Scene Detection Function

```python
import os
from pathlib import Path

def detect_ima_scene():
    """
    Detect which ima write path to use.
    Returns: "ima-native" | "workbuddy" | "external-api" | None
    """
    # Scene 1: ima native skills — check via runtime skill discovery
    # (ima-knowledge and ima-note are skills, not shell commands;
    # implementation varies by runtime: check <available_skills>, skill registry,
    # or platform-specific tool list. If you can call use_skill("ima-knowledge")
    # and it succeeds → return "ima-native".)
    # TODO: replace with actual runtime skill discovery when running inside ima.
    # For now, fall through to check env vars / config files below.

    # Scene 2: WorkBuddy — requires platform-specific signal, not just env vars.
    # IMA_CLIENT_ID + IMA_API_KEY only mean OpenAPI is configured; they are present
    # in ALL OpenAPI environments (WorkBuddy, OpenClaw, Claude Code, etc.).
    # Use WorkBuddy-specific indicators: runtime tool/connector presence, or ask user.
    # If you detect WorkBuddy-specific runtime tools or connectors → return "workbuddy"
    # If only env vars are present but no WorkBuddy signal → return "external-api"
    if os.environ.get("IMA_CLIENT_ID") and os.environ.get("IMA_API_KEY"):
        # These env vars alone only prove OpenAPI is configured.
        # Do NOT assume WorkBuddy without a platform-specific signal.
        return "external-api"

    # Scene 3: External agent — read only the documented config files
    # after the user has approved local plaintext config storage.
    config_dir = Path.home() / ".config" / "ima"
    if config_dir.exists():
        client_id_file = config_dir / "client_id"
        api_key_file = config_dir / "api_key"
        if client_id_file.exists() and api_key_file.exists():
            return "external-api"

    # Also check OpenClaw skill config after user-approved local storage.
    skill_config = Path.home() / ".agent-social-reader" / "config.json"
    if skill_config.exists():
        try:
            import json
            with open(skill_config) as f:
                cfg = json.load(f)
                if cfg.get("imaClientId") and cfg.get("imaApiKey"):
                    return cfg.get("imaScenario", "external-api")
        except Exception:
            pass

    return None  # Cannot detect — ask user
```

### Save to ima via OpenAPI (Way B — Upload Markdown)

Three-step: `create_media` → COS upload → `add_knowledge`. Full API details in `references/tool-details.md` §9.

```python
import os
import urllib.request
import urllib.error
import json
import time
import subprocess
import shutil
import re
from pathlib import Path

# ── helpers ────────────────────────────────────────────────────────────────────

def _slugify(title):
    slug = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", title.strip(), flags=re.UNICODE)
    slug = slug.strip(".-")[:80]
    return slug or "untitled"

def _get_ima_credentials():
    """Load ima credentials from env vars or config files."""
    client_id = os.environ.get("IMA_CLIENT_ID")
    api_key = os.environ.get("IMA_API_KEY")
    if client_id and api_key:
        return client_id, api_key

    # Fallback: read from documented config files only after user-approved
    # local plaintext config storage.
    cfg_dir = Path.home() / ".config" / "ima"
    client_id_file = cfg_dir / "client_id"
    api_key_file = cfg_dir / "api_key"
    if client_id_file.exists() and api_key_file.exists():
        return (
            client_id_file.read_text().strip(),
            api_key_file.read_text().strip()
        )

    # Fallback: user-approved skill config.
    skill_cfg = Path.home() / ".agent-social-reader" / "config.json"
    if skill_cfg.exists():
        with open(skill_cfg) as f:
            cfg = json.load(f)
            return cfg.get("imaClientId", ""), cfg.get("imaApiKey", "")

    raise ValueError("ima credentials not found. Set IMA_CLIENT_ID / IMA_API_KEY or configure ~/.config/ima/")

def _get_ima_kb_id(client_id=None, api_key=None):
    """
    Get the ima Knowledge Base ID to save content into.
    Checks env var IMA_KNOWLEDGE_BASE_ID, then skill config, then queries the API.

    Returns:
        kb_id (str): The knowledge base ID

    Raises:
        ValueError: If no KB ID can be determined
    """
    # 1. env var
    kb_id = os.environ.get("IMA_KNOWLEDGE_BASE_ID")
    if kb_id:
        return kb_id

    # 2. user-approved skill config
    skill_cfg = Path.home() / ".agent-social-reader" / "config.json"
    if skill_cfg.exists():
        with open(skill_cfg) as f:
            cfg = json.load(f)
            kb_id = cfg.get("imaKnowledgeBaseId", "")
            if kb_id:
                return kb_id

    # 3. query API — return options so the agent can ask the user to choose
    if client_id and api_key:
        url = "https://ima.qq.com/openapi/wiki/v1/get_addable_knowledge_base_list"
        body = json.dumps({}).encode("utf-8")
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "ima-openapi-clientid": client_id,
                    "ima-openapi-apikey": api_key,
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.load(resp)
        except Exception:
            result = {}

        if result.get("retcode") == 0:
            kb_list = result.get("data", {}).get("addable_knowledge_base_list", [])
            if len(kb_list) == 1:
                return kb_list[0].get("id", "")
            if len(kb_list) > 1:
                options = [
                    f"{item.get('name', '(unnamed)')} ({item.get('id', '')})"
                    for item in kb_list
                ]
                raise ValueError(
                    "Multiple ima knowledge bases are available. Ask the user to choose one, "
                    "then save its id as IMA_KNOWLEDGE_BASE_ID or imaKnowledgeBaseId. Options: "
                    + "; ".join(options)
                )

    raise ValueError(
        "ima Knowledge Base ID not found. Set IMA_KNOWLEDGE_BASE_ID, "
        "configure imaKnowledgeBaseId in ~/.agent-social-reader/config.json, "
        "or ensure client_id + api_key can query get_addable_knowledge_base_list."
    )

def _ima_api_request(endpoint, payload, client_id, api_key):
    """Make an ima OpenAPI request. Returns parsed JSON."""
    url = f"https://ima.qq.com/openapi/wiki/v1/{endpoint}"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.load(resp)
    if result.get("retcode") != 0:
        raise RuntimeError(f"ima API error: {result.get('errmsg')} (code {result.get('retcode')})")
    return result

def _upload_to_ima_cos(tmp_path):
    """
    Upload the markdown file to COS using ima-provided tooling.

    Do not hand-roll the COS Authorization header here: Tencent COS REST signing
    requires a full signature or a pre-signed URL, and ima's create_media response
    should be uploaded with ima_cos_util / cos-upload.cjs or an official COS SDK.
    A COS SDK implementation would need create_media's cos_credential fields
    (bucket_name, region, cos_key, secret_id, secret_key, token).
    """
    if shutil.which("ima_cos_util"):
        subprocess.run(["ima_cos_util", "-f", tmp_path], check=True, timeout=120)
        return

    cos_upload = shutil.which("cos-upload.cjs")
    if cos_upload:
        subprocess.run(["node", cos_upload, "-f", tmp_path], check=True, timeout=120)
        return

    raise RuntimeError(
        "COS upload helper not found. Install/use ima_cos_util or the ima skills package "
        "(cos-upload.cjs), or replace _upload_to_ima_cos with an official COS SDK upload "
        "after verifying create_media's cos_credential format."
    )

# ── main save function ────────────────────────────────────────────────────────

def save_to_ima(title, source_url, platform, summary, full_text, kb_id, client_id, api_key):
    """
    Save content to ima knowledge base via OpenAPI (Way B — upload Markdown).

    Args:
        title: Content title
        source_url: Original URL
        platform: Platform name
        summary: AI-generated summary
        full_text: Full article/post text
        kb_id: Knowledge base ID
        client_id: ima Client ID
        api_key: ima API Key
    """
    slug = _slugify(title)
    markdown_body = (
        f"# {title}\n\n"
        f"**Source**: {source_url}\n"
        f"**Platform**: {platform}\n\n"
        f"## Summary\n\n{summary}\n\n"
        f"## Full Text\n\n{full_text}\n"
    )
    byte_size = len(markdown_body.encode("utf-8"))
    timestamp = int(time.time())

    # Write temp file for COS upload
    tmp_path = f"/tmp/asr_ima_{slug}.md"
    Path(tmp_path).write_text(markdown_body, encoding="utf-8")

    # Step 1: create_media
    media_result = _ima_api_request(
        "create_media",
        {
            "file_name": f"{slug}.md",
            "file_size": byte_size,
            "content_type": "text/markdown",
            "knowledge_base_id": kb_id,
            "file_ext": "md"
        },
        client_id,
        api_key
    )
    media_id = media_result["data"]["media_id"]
    cos_cred = media_result["data"]["cos_credential"]

    # Step 2: COS upload
    cos_key = cos_cred["cos_key"]
    _upload_to_ima_cos(tmp_path)

    # Step 3: add_knowledge
    _ima_api_request(
        "add_knowledge",
        {
            "media_type": 7,
            "media_id": media_id,
            "title": title,
            "knowledge_base_id": kb_id,
            "folder_id": kb_id,
            "file_info": {
                "cos_key": cos_key,
                "file_size": byte_size,
                "file_name": f"{slug}.md",
                "last_modify_time": timestamp
            }
        },
        client_id,
        api_key
    )

    # Cleanup temp file
    Path(tmp_path).unlink(missing_ok=True)
    return True
```

**Usage**:
```python
client_id, api_key = _get_ima_credentials()
kb_id = _get_ima_kb_id(client_id, api_key)
save_to_ima(
    title="Article Title",
    source_url="https://example.com/article",
    platform="Web",
    summary="AI summary here",
    full_text="Full article text",
    kb_id=kb_id,
    client_id=client_id,
    api_key=api_key
)
```

**Note**: For Windows PowerShell 5.1 environments, the request body must be explicitly encoded as UTF-8 bytes. See `references/tool-details.md` §10 for the PowerShell workaround.

---

## Save to Notion

**When to use**: User says "save to Notion" and no native Notion tool (notion-cli, mcporter-notion, custom Notion connector) is available.

**Dependencies**: urllib standard library only — no external packages required.

```python
import urllib.request, urllib.error, json

def _paragraph_blocks(text, chunk_size=1900):
    """Split text into Notion paragraph blocks, respecting the 1900-char limit per block."""
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)] or [""]
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]}
        }
        for chunk in chunks
    ]

def save_to_notion(token, target_id, title, source_url, platform, summary, full_text="", target_type="database"):
    """
    Archive content to Notion.

    Args:
        token: Notion Integration Token
        target_id: Database ID (target_type="database") or Page ID (target_type="page")
        title: Page title
        source_url: Original URL
        platform: Platform name (e.g. "Twitter", "Instagram", "Web")
        summary: AI-generated summary
        full_text: Full article/post text (optional)
        target_type: "database" (default) or "page"
    """
    body_text = f"Source: {source_url}\nPlatform: {platform}\n\nSummary:\n{summary}\n\nFull text:\n{full_text}"
    children = _paragraph_blocks(body_text)

    if len(children) > 100:
        raise ValueError(
            f"Notion content too long: {len(children)} blocks exceeds 100-block single-request limit. "
            "Ask the user whether to save the summary only, or use batched PATCH append requests."
        )

    if target_type == "database":
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"database_id": target_id},
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": title[:2000]}}]},
                "Source": {"url": source_url}
            },
            "children": children
        }
        method = "POST"
    else:
        url = f"https://api.notion.com/v1/blocks/{target_id}/children"
        payload = {"children": children}
        method = "PATCH"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        },
        method=method
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)
```

**Usage**:
```python
result = save_to_notion(
    token="secret_xxx",
    target_id="database_or_page_id",
    title="Article Title",
    source_url="https://example.com/article",
    platform="Twitter",
    summary="AI summary here",
    full_text="Full article text here",
    target_type="database"  # or "page"
)
```

**Notes**:
- Default database schema assumed: title property `Name`, URL property `Source`. If different, ask user for the actual property names.
- Notion API limits children to 100 blocks per single request. If content exceeds 100 blocks, raise ValueError and ask user.
- Never silently truncate content.

---

## Save to Obsidian

**When to use**: User says "save to Obsidian" and no native Obsidian integration tool is available.

Before writing, confirm the vault path and note title for the current item.

**Dependencies**: pathlib + re standard library only — no external packages required.

```python
from pathlib import Path
import re

def slugify(title):
    """
    Convert title to a safe filename slug.
    - Replaces non-alphanumeric characters (except Chinese chars, dots, hyphens) with hyphens
    - Strips leading/trailing hyphens and dots
    - Truncates to 80 characters
    - Returns 'untitled' if result is empty
    """
    slug = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", title.strip(), flags=re.UNICODE)
    slug = slug.strip(".-")[:80]
    return slug or "untitled"

def unique_note_path(vault, slug):
    note_path = vault / f"{slug}.md"
    if not note_path.exists():
        return note_path
    counter = 2
    while True:
        candidate = vault / f"{slug}-{counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1

def save_to_obsidian(vault_path, title, source_url, summary, full_text=""):
    """
    Write content as a Markdown note in an Obsidian vault.

    Args:
        vault_path: Absolute path to the Obsidian vault root
        title: Note title (used for filename and H1)
        source_url: Original URL
        summary: AI-generated summary
        full_text: Full article/post text (optional)

    Returns:
        Absolute path to the created note

    Raises:
        FileNotFoundError: vault_path does not exist or is not a directory
        ValueError: Filename would escape vault directory (path traversal attempt)
    """
    vault = Path(vault_path).expanduser().resolve()
    if not vault.exists() or not vault.is_dir():
        raise FileNotFoundError(f"Obsidian vault path does not exist: {vault}")

    note_path = unique_note_path(vault, slugify(title))
    body = (
        f"# {title}\n\n"
        f"Source: {source_url}\n\n"
        f"## Summary\n\n{summary}\n\n"
        f"## Full Text\n\n{full_text}\n"
    )

    # Security: ensure path stays within vault (prevent path traversal)
    resolved_path = note_path.resolve()
    if not str(resolved_path).startswith(str(vault.resolve())):
        raise ValueError(f"Filename would escape vault: {note_path}")

    note_path.write_text(body, encoding="utf-8")
    return str(note_path)
```

**Usage**:
```python
note_path = save_to_obsidian(
    vault_path="/Users/user/Documents/my-vault",
    title="Article Title",
    source_url="https://example.com/article",
    summary="AI summary here",
    full_text="Full article text here"
)
print(f"Saved to: {note_path}")
```

**Notes**:
- slugify supports Unicode (Chinese, Japanese, etc.) via `\u4e00-\u9fff` range
- Existing notes are not overwritten; duplicate titles create `-2`, `-3`, etc. suffixes
- Path traversal protection: filename is always relative to vault root; absolute paths in title are rejected
- If vault_path contains symlinks, `resolve()` normalizes them — ensure the final path is within the vault
