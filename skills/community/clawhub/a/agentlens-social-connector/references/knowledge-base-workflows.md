# Knowledge Base Workflows

Use this file when the user asks to save, archive, capture, add, export, or send retrieved social content to a knowledge base, notes app, workspace document, or other destination.

This skill does not run a background write service or automatic archive. Use the current runtime's native destination tools first; when no native tool exists, adapt the destination-specific fallback helpers in this file.

For Notion and Obsidian specifically, first check whether the runtime already exposes a user-approved default connector, tool, app, MCP server, or installed skill for that destination. If one exists and matches the requested destination, use it. Use the fallback helpers below only when the default/native destination tool is unavailable, lacks permission, or fails.

## Safety Boundary

- Save only the current retrieved item or the items explicitly selected by the user.
- Confirm the destination when it is not clear from the current request.
- Ask before writing to an external service, creating a new local file, or storing credentials.
- Do not create recurring archives, background syncs, default save targets, or broad auto-save behavior.
- Do not save full API keys, cookies, session tokens, or private account data.

## Save Flow

```text
User asks to save/archive current social item
 -> Reuse the current-task AgentLens result or saved response JSON when available
 -> Fetch only if no usable result exists, or the user explicitly requests refresh
 -> After a new successful fetch, save the full response JSON as a current-task artifact when possible
 -> If media understanding or transcript was requested, complete that first
 -> Build a clean markdown note
 -> Confirm destination if unclear
 -> If the user explicitly asked to preserve media files, select and download only the requested/current media
 -> Use runtime-native write/save tool for that destination
 -> If save succeeds, report what was saved and where
 -> If save fails, follow the save failure policy below
```

For saves after summarization, media understanding, or transcription, first look for the in-memory result or task-local JSON such as `/tmp/agentlens_{platform}_{timestamp}_response.json`. Do not re-fetch only to save. If the response is missing, corrupt, stale, or URL-mismatched, tell the user another AgentLens call may consume quota before fetching again.

## Note Shape

Prepare portable markdown before sending it to a destination:

Use the user's current conversation language for visible labels and headings in the note. The English labels below are examples; localize them for Chinese or other-language conversations. Preserve user-provided templates, existing Notion/database property names, and API/schema field names exactly. Never preserve or echo credential values in notes.

```markdown
# {title or concise source label}

Source: {url}
Platform: {platform}
Author/Source: {author}
Handle/Account ID: {handle_or_author_id, if available}
Title: {title}
Published: {published_at or unknown}
Retrieved: {YYYY-MM-DD}

## Summary
...

## Key Points
- ...

## Transcript Or Caption Notes
...

## Media Interpretation
...

## Original Text
...
```

Omit empty sections. Keep raw JSON out unless the user asks for it.

## Destination Patterns

### Credential And Target Lookup Guidance

The prompts below include common ways to find folders, vault paths, integration tokens, and database/data-source IDs. For ima, do not ask the user to find or provide a `knowledge_base_id`: with current-session permission and credentials, retrieve writable bases through the OpenAPI lookup and let the user choose from that list. This guidance reflects common product UIs at the time this Skill was written. If the destination UI has changed and the agent cannot verify it live, ask the user to follow the destination's latest official help or developer documentation.

### Destination Setup Memory (Opt-in)

After a successful save that required destination setup, before closing the task offer one separate yes/no choice to remember the minimum setup for that destination. Do not treat a prior credential, a successful save, or a request to save another item as consent.

- Store secrets such as API keys and tokens only in an approved runtime secret store. Do not put them in chat memory, reports, or a plain local file unless the user explicitly approves that exact storage location.
- A knowledge base/database ID, vault path, and optional destination folder are private configuration metadata. Store them only in an approved, destination-scoped connector configuration or memory mechanism after the user explicitly approves; otherwise keep them for the current session only.
- If this runtime does not expose an approved persistence mechanism, say so and do not create or scan local configuration directories as a substitute.
- When no setup is available in the current session, do not search conversation history, general memory, home directories, or unrelated local files to recover it. Ask the user to choose or provide it again.

Suggested prompt after an ima or Obsidian save:

```text
Would you like me to remember this destination for future saves? I can store credentials only in this runtime's approved secret store and the selected knowledge-base/vault location only in its approved destination configuration. If you say no, I will use it only for this session.
```

### Directory And Naming Suggestions

When the destination supports folders or a directory-like structure, prefer the user's existing organization first. If no convention exists and the user has not specified a folder, suggest a stable structure that groups saves by platform and account:

```text
Social Reads/
  {platform}/
    {handle_or_author_id_or_unknown}/
      {YYYYMMDD-HHMM}-{platform}-{handle_or_author_id_or_unknown}-{short_title_or_text_slug}.{ext}
```

For destinations that do not expose folders, use the same parts in the title, database properties, tags, or note body instead. Do not create a new folder hierarchy unless the user confirms the destination and path, or the runtime already has an approved default folder for social saves.

### Explicit Media Preservation

By default, save summary, key points, original text/body, media interpretation, and source/media URLs in the note. Put summary and key points near the top, and original text/body lower in the note. Do not download or upload every returned media file just because a destination supports attachments.

Treat a request to save the text/body together with images, video, media, or a graphic post as an explicit request to preserve those named media. Do not reinterpret it as a text-only save. For ima image preservation, create one `media_type=20` HTML document with the requested images embedded as base64 data; do not silently downgrade to Markdown or URL-only import. For Notion, use verified native media blocks when available; otherwise disclose the limitation and obtain approval before a links-only or text-only downgrade.

Use this clarification when the user asks to save a post and media URLs are present, but the user did not explicitly ask to preserve original media files:

```text
By default, I will save the summary, source link, media interpretation, and media URLs. If you need long-term preservation of the original image/video files, tell me and I will handle them through the destination-supported workflow.
```

When the user explicitly asks to preserve media files, save the media through the selected destination's supported attachment workflow:

1. Confirm which media to preserve when the AgentLens API returned multiple media items, unless the user asked for all media.
2. Download only the selected media to `/tmp/agentlens_*` for the current request.
3. Use a durable filename based on date/time, platform, author/source id, and a short title/text slug.
4. Attach or upload media through the destination's supported path:
   - Notion: use the native Notion connector's file/media blocks when available. If only the fallback API helper is available, include source/media URLs and local filenames in the page body unless the runtime has a verified Notion file upload helper.
   - Obsidian/local vault: put media in a vault-relative attachments folder, such as `attachments/`, `assets/`, or the user's existing convention, then link files from the Markdown note.
   - ima: follow the ima-specific rules below. Do not upload images as separate unlinked knowledge items by default. For long-term video preservation, do not claim durable embedded video support unless the current runtime confirms a native/video upload path.
   - Local/workspace file: save media beside the note or under a sibling assets folder, then link files from the note.
5. If the destination cannot support durable media upload, preserve exact filenames, source URLs, and expiry notes in the note, and offer a local folder export when appropriate.

Suggested confirmation before media download:

```text
I can preserve the original media files. Please confirm whether to save all media or only selected items. I will use the destination's supported attachment workflow; some destinations may only support links or filenames, not durable embedded media.
```

Do not base64-embed large videos by default. Do not treat TikTok, Instagram, or similar platform CDN/source URLs as durable archives.

### Local Markdown Or Workspace File

Use when the user asks to save as a file, local note, markdown, project note, or workspace artifact.

1. Confirm path if not specified.
2. Write one markdown file with a safe filename based on platform/title/date.
3. Include source URL, platform, author/source, handle/account ID when available, published date, and retrieved date.
4. Avoid overwriting existing files unless the user confirms.
5. If the user asked to preserve media, save files beside the note or in a sibling assets folder and link them with relative Markdown paths.

Suggested prompt when the path is missing:

```text
Where should I save this note? Please provide a folder path or workspace location. You can usually copy the path by opening the target folder in Finder/File Explorer, or by using `pwd` in a terminal opened at that folder. I can suggest a filename based on date, platform, handle, and title, and I will not overwrite an existing file unless you confirm.
```

### Obsidian

Use when the user asks to save to Obsidian or a vault.

1. Before asking for a vault path, establish the writable filesystem boundary. If the agent runs on the user's local machine and the user explicitly asks to save to Obsidian, it may use an approved native Obsidian integration, a system picker, a registered-vault list, or a bounded scan of locally approved locations to discover candidate vaults and ask the user to choose one. Do not perform a broad home-directory scan, inspect note contents, or retain discovered paths without opt-in.
2. If the agent runs remotely, check whether it can use one of: its own reachable vault filesystem, an approved Obsidian connector/app bridge/MCP server, a paired local node with approved file-write capability, or an explicitly configured reachable vault mirror/sync path. A path from the user's laptop/desktop is not writable merely because the user sends it to a remote/server-hosted agent.
3. If no approved remote route exists, say so before accepting any local path as a save target; do not claim, imply, or queue a direct local-vault write.
4. When no writable route is available, offer a choice: (a) keep the result in Obsidian by pairing a local node, connecting an approved writer, or selecting a reachable synced vault/mirror; or (b) use a separately approved non-Obsidian export, such as a Markdown file or chat attachment. Do not call option (b) an Obsidian save.
5. Ask for a path only after the user chooses an available Obsidian route and the target filesystem is actually reachable; for a local discovery flow, ask the user to select from the candidate vaults before writing.
6. Create a markdown note in the confirmed, reachable vault path.
7. Prefer frontmatter only if the user or vault convention calls for it.
8. Include tags only if requested or obvious from the user's workflow.
9. If the user asked to preserve media, use the vault's existing attachment convention when known; otherwise ask for or propose a vault-relative attachments folder.
10. Do not recursively or broadly scan the user's home directory for vaults. Candidate discovery is limited to an approved native picker, a registered-vault list, user-provided paths, or a bounded scan of locally approved locations; do not inspect note contents, configuration, or credentials while discovering candidates.
11. If the vault is unreachable, mark the Obsidian save as failed. Offering a downloadable file or chat attachment is an optional, separately approved export; it is not a completed Obsidian save.
12. After a successful save, the agent may offer **Destination Setup Memory (Opt-in)** if the vault/path was supplied for this task and has not already been approved for persistence. It must not retain the destination without explicit consent.

Suggested prompt when vault/path is missing. You may shorten it based on the user's context, but keep the required destination, path, and permission checks:

```text
For a local host after a user asks to save to Obsidian: `I can access approved local locations and found these candidate vaults: {names/paths}. Which one should I use?` Do not read note contents during discovery.

For a remote host without a write route: `I cannot currently write to an Obsidian vault on your computer because this remote host has no approved route to it. Would you like to keep it in Obsidian by pairing a local node, connecting an approved Obsidian writer, or choosing a reachable synced vault/mirror? Or, if you prefer not to set that up, I can provide a Markdown export or chat attachment instead. That export is not an Obsidian save.`
```

#### Obsidian Local Vault Helper

Use this helper when Obsidian is available as a local vault path and the user has approved writing a file there.

Required inputs:

- `vault_dir`: confirmed Obsidian vault directory.
- `folder`: optional folder inside the vault, such as `Social Reads`.
- `title`: note title.
- `content`: markdown note content from the Note Shape above.

Execution pattern:

```text
Confirm vault_dir and optional folder
 -> Build one markdown note
 -> Generate a safe file name
 -> Refuse overwrite unless user approved it
 -> Write the note to the selected vault path
 -> Report the vault-relative path
```

Portable Python skeleton:

```python
from pathlib import Path
import re


def _safe_filename(title):
    name = re.sub(r"[\\/:*?\"<>|#\\[\\]]+", "-", title).strip(" .-")
    return (name or "social-read")[:120] + ".md"


def save_to_obsidian(vault_dir, title, content, folder=None, overwrite=False):
    vault = Path(vault_dir).expanduser().resolve()
    if not vault.exists() or not vault.is_dir():
        raise RuntimeError("Obsidian vault path does not exist or is not a directory")
    target_dir = vault / folder if folder else vault
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / _safe_filename(title)
    if target.exists() and not overwrite:
        raise RuntimeError(f"Note already exists: {target.relative_to(vault)}")
    target.write_text(content, encoding="utf-8")
    return str(target.relative_to(vault))
```

If the runtime has a native Obsidian/MCP connector, prefer that connector over direct filesystem writes. Use direct filesystem writes only after the user confirms the vault path.

### Notion

Use when the user asks to save to Notion.

1. Check first for the user's default Notion connector, app, MCP server, or installed Notion writing skill. Use it when available.
2. If the native connector is unavailable or disconnected, do not conclude that Notion writing is unavailable. Before asking the user for another token, check only the current runtime secret store or a user-approved Notion/AgentLens configuration for an existing `notion_token`; do not scan home directories, general memory, or conversation history to discover one.
3. If an approved token is available, use the Notion API helper below after confirming the target parent and save mode. If no approved token is available, explain the missing requirement and ask the user to provide/connect it.
4. Confirm whether the user wants a page-based archive or a database/data-source archive when unclear.
5. Save title, source URL, platform, author/source, handle/account ID when available, published date, retrieved date, summary, key points, transcript notes, media interpretation, and original text/body. Put summary and key points first, and original text/body lower in the page.
6. If the user asked to preserve media, use native Notion media/file blocks when the runtime supports them; otherwise include source/media URLs and exact local filenames in the page body instead of pretending the fallback helper uploaded files.
7. Ask before storing a Notion token. Do not print the token or raw authorization header.

Suggested prompt when Notion destination or credentials are missing. You may shorten it based on the user's context, but keep the token, target parent, save mode, and schema checks:

```text
I can save this to Notion. Do you want a regular page or a database/data-source entry?

If you have a Notion connector already available here, I can use that. If not, please provide:
- a Notion integration token, preferably through the runtime's secret store;
- the target parent page ID for regular page mode, or the database/data-source ID for database mode;
- for database mode, the title property name and any optional property names/types you want filled.

Where to find these, based on the common Notion setup when this Skill was written: create or open an internal integration from Notion's integration/developer settings and copy its secret; share the target page or database/data source with that integration; copy the target page or database/data-source link from Notion and use the ID in that link. If the Notion UI has changed, follow Notion's latest official integration/API documentation.

I will use the token only for this save unless you explicitly approve secure storage.
```

#### Notion Save Modes

> **Terminology note:** Notion's user interface may call structured collections "databases"; the current Notion API may use `data_source` for the parent object. This skill uses "database/data-source" for user intent, and uses the correct API field such as `data_source_id` or `database_id` in implementation.

Support two Notion modes:

| Mode | Best for | Tradeoff |
|:--|:--|:--|
| Page archive | One-off saves, richer page body, fewer schema requirements, better fit for media-heavy notes | Each save creates a new child page; large volumes can become messy unless the parent page is organized |
| Database/data-source archive | Ongoing collections, sortable records, tags/status/platform/source fields, easier long-term management | Requires a prepared schema and correct title property; media-heavy content may still need to live in the created page body |

Selection guidance:

- If the user says "save this to Notion" without a preferred structure, ask whether they want a simple child page or a managed database entry.
- For a single article/post/video summary, page archive is usually the lowest-friction option.
- For repeated saves, monitoring, research collections, CRM-style tracking, or anything the user will sort/filter later, recommend a database/data-source archive.
- For database/data-source mode, ask for the target data source and title property when the runtime cannot inspect schema. Also ask which optional properties to populate, such as `Platform`, `Source URL`, `Author`, `Handle`, `Published`, `Retrieved`, `Tags`, or `Status`.
- For media-heavy saves, create a Notion page body containing the summary, media interpretation, transcript notes, and source/media URLs. Use database properties only for metadata that should be sortable or filterable.

When the fields are uncertain, use this clarification:

```text
Would you like to save this as a regular Notion page, or write it into a database/data source? If you want database/data-source mode, please provide the target data source ID, the title property name, and any existing optional property names and types. If the fields are uncertain, I recommend creating a regular page first to avoid schema mismatch errors.
```

#### Notion API Helper

Use this helper when no native Notion connector exists and the user has provided or approved a Notion integration token and target parent.

Required inputs:

- `notion_token`: Notion integration token from the runtime secret store or user input.
- `parent_id`: target parent page id or data source id. In user-facing language, Notion may call this a database; in the current API, the structured collection parent is a data source.
- `parent_type`: `page` for page archive, or `data_source` for database/data-source archive.
- `title`: page title.
- `content`: markdown note content from the Note Shape above.
- `title_property`: title property name when writing to a data source, defaulting to `Name` only if the user confirms that property.
- `extra_properties`: optional database/data-source properties that match the user's schema.

Common `extra_properties` examples, only after the user confirms these property names and types exist:

```python
extra_properties = {
    "Platform": {"select": {"name": "TikTok"}},
    "Source URL": {"url": "https://example.com/post"},
    "Author": {"rich_text": [{"text": {"content": "creator name"}}]},
    "Handle": {"rich_text": [{"text": {"content": "@creator"}}]},
    "Published": {"date": {"start": "2026-07-20"}},
    "Retrieved": {"date": {"start": "2026-07-21"}},
    "Tags": {"multi_select": [{"name": "social-read"}]},
    "Status": {"select": {"name": "Saved"}},
}
```

Execution pattern:

```text
Confirm Notion destination, save mode, and token source
 -> For page mode, create a child page under the selected parent page
 -> For database/data-source mode, create a record page under the selected data source
 -> Write page body with children paragraph blocks by default
 -> Do not send a nonstandard "markdown" field unless the runtime provides a verified Notion markdown helper
 -> If parent/properties are rejected, ask for the correct target, title property, or property schema
 -> Report the created page URL
```

Portable Python skeleton:

```python
import json
import os
import urllib.error
import urllib.request

# Prefer an approved runtime config if one exists. The fallback version writes
# page content as children blocks, which is the stable Notion API path.
# Do not send a raw "markdown" field by default; Notion may reject it and can
# return a misleading 401 even when the token is valid.
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2022-06-28")


def _notion_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _paragraph_blocks(text, chunk_size=1900):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)] or [""]
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            },
        }
        for chunk in chunks
    ]


def _post_notion_page(notion_token, payload):
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode("utf-8"),
        headers=_notion_headers(notion_token),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        lower = detail.lower()
        if "notion-version" in lower or "version" in lower:
            raise RuntimeError(
                "Notion rejected the API version. Use a supported Notion-Version, "
                "a native Notion connector, or the children-block fallback."
            )
        raise RuntimeError(f"Notion save failed: HTTP {exc.code} {detail[:500]}")


def _build_parent_and_properties(parent_id, parent_type, title, title_property, extra_properties):
    if parent_type == "page":
        return {"page_id": parent_id}, {"title": [{"text": {"content": title[:2000]}}]}
    if parent_type == "data_source":
        prop = title_property or "Name"
        properties = {prop: {"title": [{"text": {"content": title[:2000]}}]}}
        if extra_properties:
            properties.update(extra_properties)
        return {"data_source_id": parent_id}, properties
    if parent_type == "database":
        prop = title_property or "Name"
        properties = {prop: {"title": [{"text": {"content": title[:2000]}}]}}
        if extra_properties:
            properties.update(extra_properties)
        return {"database_id": parent_id}, properties
    raise RuntimeError("parent_type must be 'page', 'data_source', or 'database'")


def create_notion_page(
    notion_token,
    parent_id,
    parent_type,
    title,
    content,
    title_property=None,
    extra_properties=None,
    prefer_markdown=False,
):
    parent, properties = _build_parent_and_properties(
        parent_id, parent_type, title, title_property, extra_properties
    )
    base_payload = {"parent": parent, "properties": properties}

    if prefer_markdown:
        try:
            result = _post_notion_page(notion_token, {**base_payload, "markdown": content})
            return result.get("url") or result.get("id")
        except RuntimeError as exc:
            message = str(exc).lower()
            can_fallback = (
                "markdown" in message
                or "body" in message
                or "validation" in message
                or "version" in message
                or "notion-version" in message
                or "unauthorized" in message
                or "token is invalid" in message
            )
            if not can_fallback:
                raise

    children = _paragraph_blocks(content)
    if len(children) > 100:
        raise ValueError(
            f"Notion content too long: {len(children)} blocks exceeds the 100-block create-page limit. "
            "Ask the user whether to save summary only, split the note, or use a native Notion connector."
        )
    result = _post_notion_page(notion_token, {**base_payload, "children": children})
    return result.get("url") or result.get("id")
```

For page archive mode, the `properties` body should only carry the page title. For database/data-source archive mode, every property key and property type must match the target schema. Do not guess property types from names alone. If a mapped `select` or `multi_select` value is not already an allowed option, do not silently create or alter the option: ask the user whether that schema change is allowed, then either create it through the approved destination capability or omit that optional property. If the user does not know the schema and no native Notion tool can inspect it, ask whether to create a simple child page instead. If a database/data-source write fails with a validation error, ask for the correct title property and optional property types, or fall back to page archive.

### ima

Use when the user asks to save to ima.

Important ima video boundary: the OpenAPI fallback has no verified independent-video `media_type`. A single HTML file may contain a bounded base64-embedded video when the user explicitly requests it and the current runtime has verified the whole HTML upload and in-ima playback path. Because the bytes are embedded, successful playback does not depend on the platform CDN URL remaining valid; unknown ima file/media-size limits and normal ima retention/access rules still apply.

1. Prefer native ima skills/tools only after verifying they are callable in the current session. A UI-level connector/authorization is not enough if no callable tool is exposed to the agent.
2. If no callable native ima tool exists, or the native tool fails, use the three-step `create_media -> COS PUT -> add_knowledge` OpenAPI flow below.
3. Ask for or load only the ima credentials and target knowledge base explicitly approved for the current environment.
4. Confirm the target knowledge base before writing if not already clear. With the user's permission and the current-session ima credentials, use the ima/OpenAPI knowledge-base lookup (for example, `search_knowledge_base`) to list the writable bases and let the user choose; then check that the selected base is writable before upload. Do not treat a share-link token as a `knowledge_base_id`.
5. Save a text-first note by default. Include image interpretation, source URL, and media references, but do not upload images as separate knowledge items unless the user explicitly asks.
6. If the user needs image-preserving output, prefer a single HTML document with embedded base64 images when the runtime and ima workflow support it. The current supplied ima uploader constraint treats `media_type=20` as one HTML file with a **10 MB total limit**: all HTML markup and every `data:...;base64,...` image/video share that budget. Base64 expands binary data by roughly one third, so measure the final HTML file before upload and leave headroom; do not treat the image-file limit as an additional allowance. For videos in that HTML, use bounded `<video controls>` blocks with a source URL only as short-term previews; TikTok, Instagram, and similar platform URLs can expire. If the user explicitly asks to preserve video bytes in the HTML, download only the AgentLens-returned media URL, verify the local file, and use a single `media_type=20` HTML artifact only when its final size is within the 10 MB limit and the current runtime can upload it. Check playback in ima when possible. A verified base64-embedded playback path does not depend on CDN URL expiry, but does not override normal ima retention/access rules. The tested ima OpenAPI media types do not include a working independent video file type; do not attempt an independent video upload through the OpenAPI fallback unless the current runtime confirms a supported native/video upload path. `.docx` with embedded images has been observed working in the current ima workflow. PDF is allowed only after the PDF font/render validation below passes; do not present docx/PDF as a verified playable-video alternative.

Do not read `~/.config/ima`, `~/.agentlens`, or other local config paths unless the user already approved that local configuration or requests it for the current save workflow.

Suggested prompt when ima credentials or target knowledge base are missing. You may shorten it based on context, but keep the credential, target knowledge base, and latest-docs caveat:

```text
I can save this to ima. If a native ima tool is available here, I can use that first. Otherwise, for the OpenAPI fallback I need:
- IMA_OPENAPI_CLIENTID;
- IMA_OPENAPI_APIKEY;
- permission to use the current-session ima/OpenAPI lookup to list your writable knowledge bases and let you choose one.

Where to find these, based on the common ima setup when this Skill was written: open https://ima.qq.com/agent-interface to find Client ID and API Key on the same page. Client ID maps to the `ima-openapi-clientid` header, and API Key maps to the `ima-openapi-apikey` header. Do not ask the user to find or paste a `knowledge_base_id`: after receiving permission, call the current-session ima/OpenAPI knowledge-base lookup (such as `search_knowledge_base`), show only the minimum non-secret identifiers needed for the user to choose a writable base, and use the returned `knowledge_base_id` internally. A normal ima Share/Settings URL may expose a `shareId` or other sharing token, but that is not the OpenAPI `knowledge_base_id` and must never be sent to `create_media` or `add_knowledge`. If lookup is unavailable, explain that the OpenAPI fallback cannot safely select a destination and stop; do not ask the user to find an id or copy a share link. If the ima UI has changed, follow the latest ima OpenAPI documentation.

If the internally selected `knowledge_base_id` is rejected, do not retry unchanged. With the user's permission, refresh the writable-base list through the current-session ima/OpenAPI lookup and ask the user to select again. If lookup is unavailable, explain that the OpenAPI fallback cannot safely proceed and stop; never ask the user for an id or substitute a share-link token.

Please provide credentials through the runtime's secret store when possible. I will not print them, and I will use them only for this save unless you explicitly approve secure storage.
```

After a successful ima save, follow **Destination Setup Memory (Opt-in)**. Treat `IMA_OPENAPI_APIKEY` as a secret; treat the selected `knowledge_base_id` as private destination metadata. Do not write either into unapproved local files or conversation memory.

### ima Image Handling

Verified behavior: Markdown or note content that references external/COS image URLs may not render inline in ima, and uploading images separately creates separate knowledge entries without a reliable index relationship to the main note.

Use this policy:

- Default: save one text-first note containing summary, key points, original text/body, image interpretation, original source URL, and media URL references. Put summary and key points first, and original text/body lower in the note.
- Do not batch-upload images as standalone ima attachments for a post summary; this clutters the knowledge base and loses the relationship between images and the main note.
- Do not rely on Markdown image syntax such as `![](url)` for ima image display when URLs require authorization.
- If the user wants visual fidelity, ask whether to create one HTML document with base64-embedded images. Use this only when the runtime can generate and upload that single file.
- For video media in HTML, use `<video controls preload="metadata" src="...">` with CSS size constraints and a plain URL fallback only as a short-term preview. Returned CDN video links may expire, especially on TikTok, Instagram, and similar platforms; do not claim that a particular CDN URL is universally unplayable.
- A base64-embedded video inside one `media_type=20` HTML artifact is permitted only after explicit user request and only as a bounded, current-runtime-tested exception. Build it from a downloaded AgentLens-returned media file, not a platform-specific alternate fetcher. The final HTML, including base64 text, must be at most 10 MB under the current supplied ima uploader constraint. When ima playback is verified, the embedded bytes are independent of CDN URL expiry; still state the tested artifact size and do not claim playback beyond that 10 MB package boundary without a new test.
- For long-term video preservation in ima, tell the user that the current workflow cannot make a stable, independently uploaded video archive. The tested ima OpenAPI media types do not include a working video file type, so do not attempt independent video upload through the OpenAPI fallback unless the current runtime confirms a supported native/video upload path.
- Word `.docx` with embedded images has been observed working in the current ima workflow; still verify the target environment when possible.
- PDF with embedded images can work in the current ima workflow when generated with fonts that match the user-visible output language and pass the render/text checks below. Simplified Chinese output has been observed working with ReportLab `STSong-Light` CID. Adobe Acrobat and macOS Preview may silently fall back to local fonts and hide broken embedded fonts, while ima/browser viewers can render the same PDF as garbled text.
- If image-preserving save fails, keep the text-first note and offer local HTML/docx/PDF export instead of creating multiple unlinked image items.

Use recognizable titles and filenames for ima and other knowledge-base writes:

```text
YYYYMMDD-HHMM-{platform}-{author_or_handle}-{first_10_words_or_chars}
```

If the author/handle is unknown, use `unknown`. Keep the final name filesystem-safe and append the correct extension, such as `.md`, `.html`, or `.mp4`. For separately uploaded videos, use the same base name as the main note when possible and add a suffix such as `-video-1.mp4`; list that exact filename in the note.

### PDF Font Gate

Use this gate before uploading a generated PDF to ima:

1. Choose the PDF font according to the user-visible output language.
2. For Simplified Chinese ima PDFs, prefer ReportLab with `UnicodeCIDFont("STSong-Light")` and encoding `UniGB-UCS2-H`. This route has been observed to upload and render correctly in ima with `media_type=1`, zero Poppler font mismatch warnings, and readable `pdftotext` output.
3. For English/Latin-only PDFs, use a standard Latin font or a validated embedded Latin font.
4. For Japanese, Korean, Traditional Chinese, or mixed-language PDFs, choose a font that matches the script/locale, or use a validated multi-script font with the correct face/index.
5. If embedding a local font file for Simplified Chinese, use a Simplified Chinese font such as `NotoSansCJKsc`, `Source Han Sans SC`, `PingFang SC`, or `Microsoft YaHei`.
6. Do not use `NotoSansCJKJP` for Simplified Chinese archives.
7. Avoid `fpdf2` with a `.ttc` CJK collection unless the font face index is explicitly controlled and the output is validated. In testing, default `.ttc` registration selected the JP face and produced embedded-font mismatch warnings.
8. If using WeasyPrint, make sure fontconfig can find the target font and set it explicitly in CSS.
9. If using ReportLab with a local `.ttf`/`.otf`, register a real font matching the output language with `TTFont()` and validate it.
10. Render at least the first page with `pdftoppm` or an equivalent Poppler renderer. If the renderer reports `Mismatch between font type and embedded font file`, reject the PDF and regenerate it.
11. When available, run `pdffonts` and confirm the intended font is present. `STSong-Light` CID may show `emb=no`; that is acceptable for Simplified Chinese if Poppler renders without warnings and text extraction is readable. Run `pdftotext` and confirm extracted text is readable.
12. If the PDF fails any of these checks, use `.docx` or HTML instead of uploading the broken PDF to ima.

## ima OpenAPI Helper

Use this helper pattern only after the user has selected ima as the destination and approved the target knowledge base. It is intentionally embedded here instead of shipped as a separate script, so the agent can adapt it to the current runtime.

### Required Inputs

- `IMA_OPENAPI_CLIENTID`: ima OpenAPI client id, from the current runtime secret store or user input.
- `IMA_OPENAPI_APIKEY`: ima OpenAPI API key, from the current runtime secret store or user input.
- `knowledge_base_id`: internal id returned for the ima knowledge base selected by the user; never a value supplied by the user.
- `title`: note or file title.
- `content`: markdown text note, or complete HTML string if preserving images.

Do not print these credentials. After the user selects ima as the destination, ask permission to use the current-session ima/OpenAPI lookup (such as `search_knowledge_base`) to list/search available knowledge bases, then let the user select one and prefer entries whose `role_type` indicates writable permission. The returned id is an internal request value; do not ask the user to provide it. If lookup is unavailable, explain that the OpenAPI fallback cannot safely select a destination and stop; do not infer an id from a share link.

`knowledge_base_id` is the ima knowledge base id, not a Notion database id, a generic "database ID", or a share-link `shareId`. In current verified UI/API behavior, the value may look base64-like and can end with `=`. Obtain it only from the authorized current-session ima/OpenAPI lookup after the user selects a writable base. If `create_media` returns `invalid knowledge_base_id`, do not retry unchanged; with permission, refresh the writable-base list and let the user select again. If lookup is unavailable, explain that the OpenAPI fallback cannot safely proceed and stop; never ask the user for an id or retry with a share-link token.

### Media Types

Use the narrowest file type that preserves the user's intent:

| Content | `media_type` | MIME | Extension |
|:--|:--|:--|:--|
| Text-first note in Markdown | `7` | `text/markdown` | `md` |
| Image-preserving HTML | `20` | `text/html` | `html` |
| Word document | `3` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | `docx` |
| PDF | `1` | `application/pdf` | `pdf` |
| Independent video file | Not supported by the tested ima OpenAPI fallback; use only if the current runtime confirms a native/video upload path | Source-dependent, such as `video/mp4` | `mp4` or source extension |

Use native ima note tools for ima notes when available. The OpenAPI fallback skeleton below implements Markdown (`7`) and HTML (`20`) only. The tested ima OpenAPI accepts Markdown (`7`), HTML (`20`), Word (`3`), and PDF (`1`), but no tested video `media_type` worked. If the runtime cannot confirm a supported native/video upload path, tell the user that long-term video preservation must be handled outside the current automated ima flow.

### Upload Sequence

```text
Build one file in memory or in /tmp
 -> POST /openapi/wiki/v1/create_media with file metadata and media_type
 -> Read media_id and cos_credential from response
 -> PUT the exact bytes to Tencent COS using the returned temporary credential
 -> POST /openapi/wiki/v1/add_knowledge with media_id, media_type, title, and knowledge_base_id
 -> Report destination and title
```

The COS credential returned by `create_media` is temporary and file-specific. Do not ask the user for a separate COS key. Do not invent a simplified COS authorization header; Tencent COS PUT requires SDK signing or a valid HMAC-SHA1 authorization string, plus `x-cos-security-token`.

### COS Endpoint Resolution And Bounded Recovery

- Use an endpoint explicitly returned by the current ima/COS contract when one is present. Otherwise begin with the credential's bucket/region default endpoint.
- A bucket with Tencent COS global acceleration enabled may require the global-acceleration endpoint (`{bucket}.cos.accelerate.myqcloud.com`), but this is bucket-specific; do not hard-code it for every ima upload or substitute an unrelated CDN/share domain.
- If the selected endpoint has a DNS or `403` failure, report the failed upload. Where the bucket is confirmed to support global acceleration, one immediate retry using its acceleration endpoint is allowed. Recompute the COS authorization for the new `Host`; never reuse a signature made for the prior endpoint.
- Do not silently fall back to an `import_urls`-style source-link entry when the user requested a complete file/HTML upload. Explain the reduced result and ask for approval. If the temporary credential has expired, restart from `create_media` and run the three steps without delay.
- Use the same declared media type throughout the three steps: HTML is `20`; Markdown is `7`. Do not label an HTML upload as Markdown.

### Portable Python Skeleton

Prefer the runtime's native ima tool when available. If no native tool exists, adapt this Python skeleton. It uses only the standard library and performs the manual COS signing needed for the second step.

```python
import hashlib
import hmac
import json
import os
import re
import time
import urllib.parse
import urllib.request
from http.client import HTTPSConnection

IMA_API = "https://ima.qq.com"


def _ima_headers(client_id, api_key):
    return {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json",
    }


def _safe_part(value, fallback="unknown", limit=80):
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value or "", flags=re.UNICODE)
    text = text.strip(".-")
    return (text or fallback)[:limit]


def archive_basename(platform, author_or_handle, title_or_text, timestamp=None):
    timestamp = timestamp or time.time()
    date_part = time.strftime("%Y%m%d-%H%M", time.localtime(timestamp))
    words = re.findall(r"[\w\u4e00-\u9fff]+", title_or_text or "", flags=re.UNICODE)
    if re.search(r"[\u4e00-\u9fff]", title_or_text or ""):
        summary_part = "".join(words)[:10]
    else:
        summary_part = "-".join(words[:10])
    return "-".join([
        date_part,
        _safe_part(platform, limit=32),
        _safe_part(author_or_handle, limit=48),
        _safe_part(summary_part, fallback="untitled", limit=80),
    ])


def _post_json(url, headers, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    code = body.get("code", body.get("retcode", 0))
    if code not in (0, "0", None):
        raise RuntimeError(body.get("msg") or body.get("errmsg") or "ima API request failed")
    return body.get("data", body)


def create_media(client_id, api_key, knowledge_base_id, file_name, content_type, media_type, file_bytes):
    payload = {
        "media_type": media_type,
        "file_name": file_name,
        "file_size": len(file_bytes),
        "content_type": content_type,
        "knowledge_base_id": knowledge_base_id,
        "file_ext": file_name.rsplit(".", 1)[-1],
    }
    return _post_json(f"{IMA_API}/openapi/wiki/v1/create_media", _ima_headers(client_id, api_key), payload)


def get_addable_knowledge_bases(client_id, api_key, limit=20):
    payload = {"cursor": "", "limit": limit}
    data = _post_json(
        f"{IMA_API}/openapi/wiki/v1/get_addable_knowledge_base_list",
        _ima_headers(client_id, api_key),
        payload,
    )
    return data.get("addable_knowledge_base_list") or data.get("list") or []


def assert_cos_credential(cos_credential):
    required = ["bucket_name", "region", "cos_key", "secret_id", "secret_key", "token"]
    missing = [key for key in required if not cos_credential.get(key)]
    if missing:
        raise RuntimeError(
            "ima create_media response is missing COS credential fields: "
            + ", ".join(missing)
            + ". Re-check the ima OpenAPI response shape or use a native ima/COS SDK helper."
        )


def _sha1_hex(value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha1(value).hexdigest()


def _hmac_sha1_hex(key, value):
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hmac.new(key, value, hashlib.sha1).hexdigest()


def _cos_auth(secret_id, secret_key, method, pathname, headers, start_time, expired_time):
    key_time = f"{start_time};{expired_time}"
    sign_key = _hmac_sha1_hex(secret_key, key_time)
    lowered = {k.lower(): str(v) for k, v in headers.items()}
    keys = sorted(lowered.keys())
    header_string = "&".join(
        f"{k}={urllib.parse.quote(lowered[k], safe='')}" for k in keys
    )
    http_string = f"{method.lower()}\n{pathname}\n\n{header_string}\n"
    string_to_sign = f"sha1\n{key_time}\n{_sha1_hex(http_string)}\n"
    signature = _hmac_sha1_hex(sign_key, string_to_sign)
    return "&".join([
        "q-sign-algorithm=sha1",
        f"q-ak={secret_id}",
        f"q-sign-time={key_time}",
        f"q-key-time={key_time}",
        f"q-header-list={';'.join(keys)}",
        "q-url-param-list=",
        f"q-signature={signature}",
    ])


def upload_to_cos(cos_credential, file_bytes, content_type):
    assert_cos_credential(cos_credential)
    bucket = cos_credential["bucket_name"]
    region = cos_credential["region"]
    cos_key = cos_credential["cos_key"]
    host = f"{bucket}.cos.{region}.myqcloud.com"
    pathname = "/" + urllib.parse.quote(cos_key, safe="/-_.~")
    now = int(time.time())
    start_time = int(cos_credential.get("start_time") or now - 60)
    expired_time = int(cos_credential.get("expired_time") or now + 1800)
    headers = {
        "content-length": str(len(file_bytes)),
        "content-type": content_type,
        "host": host,
        "x-cos-security-token": cos_credential["token"],
    }
    headers["authorization"] = _cos_auth(
        cos_credential["secret_id"],
        cos_credential["secret_key"],
        "put",
        pathname,
        headers,
        start_time,
        expired_time,
    )
    conn = HTTPSConnection(host, timeout=120)
    conn.request("PUT", pathname, body=file_bytes, headers=headers)
    resp = conn.getresponse()
    detail = resp.read().decode("utf-8", errors="replace")
    if resp.status not in (200, 201):
        if resp.status in (401, 403):
            raise RuntimeError(
                f"COS upload authorization failed: HTTP {resp.status}. "
                "Check temporary credential fields, x-cos-security-token, signing time, and COS key. "
                f"Detail: {detail[:300]}"
            )
        raise RuntimeError(f"COS upload failed: HTTP {resp.status} {detail[:300]}")


def add_knowledge(client_id, api_key, knowledge_base_id, media_id, media_type, title):
    payload = {
        "knowledge_base_id": knowledge_base_id,
        "media_id": media_id,
        "media_type": media_type,
        "title": title,
    }
    return _post_json(f"{IMA_API}/openapi/wiki/v1/add_knowledge", _ima_headers(client_id, api_key), payload)


def save_to_ima(
    client_id,
    api_key,
    knowledge_base_id,
    title,
    content,
    *,
    as_html=False,
    platform="unknown",
    author_or_handle="unknown",
    related_video_filenames=None,
):
    base_name = archive_basename(platform, author_or_handle, title)
    if as_html:
        file_name = f"{base_name}.html"
        content_type = "text/html"
        media_type = 20
    else:
        file_name = f"{base_name}.md"
        content_type = "text/markdown"
        media_type = 7
    if related_video_filenames:
        file_list = "\n".join(f"- {name}" for name in related_video_filenames)
        content += (
            "\n\n## Independently Uploaded Video Files\n\n"
            "ima may not keep platform CDN video links playable long term. "
            "The related video file(s) were uploaded as separate knowledge items:\n\n"
            f"{file_list}\n"
        )
    file_bytes = content.encode("utf-8")
    created = create_media(client_id, api_key, knowledge_base_id, file_name, content_type, media_type, file_bytes)
    media_id = created["media_id"]
    cos_credential = created["cos_credential"]
    upload_to_cos(cos_credential, file_bytes, content_type)
    return add_knowledge(client_id, api_key, knowledge_base_id, media_id, media_type, title)
```

When preserving images in ima, build `content` as a complete HTML document and embed images as `data:image/...;base64,...` URLs. Do not upload those images as separate ima image media unless the user explicitly wants independent image entries. For videos, use bounded player markup only as a short-term preview. For long-term preservation, do not use the OpenAPI fallback for video upload unless the current runtime confirms a supported native/video path; otherwise list the source URL, expiry warning, and any user-provided local filename in the note:

```html
<style>
  .agentlens-video {
    width: min(100%, 720px);
    max-height: 420px;
    aspect-ratio: 16 / 9;
    object-fit: contain;
    background: #111;
    display: block;
  }
  .agentlens-video.vertical {
    width: min(100%, 360px);
    max-height: 640px;
    aspect-ratio: 9 / 16;
  }
</style>
<video class="agentlens-video" controls preload="metadata" src="{video_source_url}"></video>
<p><a href="{video_source_url}">Original video link</a> (may expire)</p>
<p>Long-term video file is not embedded in this ima note. Local/reference filename, if provided: {exact_video_filename}</p>
```

## Save Failure Policy

Knowledge-base writes are not the same as AgentLens API fetch retries. A failed write may have partially succeeded, so do not blindly repeat it.

If saving fails:

1. Keep the prepared markdown note in memory for the current response.
2. Explain the failure in user-facing terms without printing credentials or raw auth headers.
3. Do not retry more than once unless the user asks.
4. Before retrying, check whether the destination may already contain the item when the runtime gives enough information to do so.
5. If the error is authentication or permission related, ask the user to refresh credentials or choose another destination.
6. If the target database, page, vault, folder, or knowledge base is missing, ask the user to choose a valid target.
7. If the content is too long or exceeds block/file limits, offer summary-only, split-note, or local Markdown fallback.
8. If the error is duplicate/conflict, ask whether to rename, overwrite, merge, or skip.
9. If the external service remains unavailable, offer to save the prepared markdown note as a local file or return it in the chat.

Common handling:

| Failure type | Action |
|:--|:--|
| Auth failed / unauthorized | Ask for refreshed credentials or another destination |
| Permission denied | Ask user to grant access or pick a writable target |
| Target not found | Ask user to confirm database/page/vault/folder/KB |
| Rate limit / timeout | Offer one retry, then local Markdown fallback |
| Content too long | Offer summary-only or split-note save |
| Duplicate/conflict | Ask to rename, overwrite, merge, or skip |
| Partial success uncertain | Do not retry blindly; ask user whether to check destination or save locally |

## Completion Message

After saving, report:

- Destination name.
- Item title/source.
- Any media/transcript limitation that affects the saved note.

Do not print credentials, raw authorization headers, or full API responses.
