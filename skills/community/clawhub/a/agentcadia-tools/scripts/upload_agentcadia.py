#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
import zipfile
from pathlib import Path

WORKSPACE_SIGNALS = {"AGENTS.md", "SOUL.md", "USER.md", "MEMORY.md"}
MAX_SKILL_ZIP_BYTES = 10 * 1024 * 1024
REQUIRED_METADATA_FIELDS = ["title", "summary", "detailDescription", "category", "tags"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload a local OpenClaw-style workspace into an Agentcadia draft"
    )
    parser.add_argument("--task-id", required=True, help="Agentcadia upload task id")
    parser.add_argument("--origin", required=True, help="Agentcadia origin, for example https://agentcadia.ai")
    parser.add_argument("--workspace", default="", help="Explicit workspace path")
    parser.add_argument(
        "--metadata-file",
        default="",
        help="Path to a JSON file containing title/summary/detailDescription/category/tags and optional metadata fields",
    )
    parser.add_argument(
        "--metadata-json",
        default="",
        help="Inline metadata JSON containing title/summary/detailDescription/category/tags and optional metadata fields",
    )
    return parser.parse_args()


def is_workspace(path: Path) -> bool:
    if not path.is_dir():
        return False
    entries = {p.name for p in path.iterdir()}
    return (
        bool(entries.intersection(WORKSPACE_SIGNALS))
        or (path / "skills").is_dir()
        or (path / "memory").is_dir()
    )


def resolve_workspace(explicit: str) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"Workspace path does not exist: {path}")
        if not path.is_dir():
            raise SystemExit(f"Workspace path is not a directory: {path}")
        return path

    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if is_workspace(candidate):
            return candidate

    raise SystemExit("Could not determine workspace path. Pass --workspace explicitly.")


def collect_markdown_files(workspace: Path):
    return sorted(
        [p for p in workspace.iterdir() if p.is_file() and p.suffix.lower() == ".md"],
        key=lambda p: p.name.lower(),
    )


def find_skill_dirs(workspace: Path):
    skills_root = workspace / "skills"
    if not skills_root.is_dir():
        return []
    return [
        child
        for child in sorted(skills_root.iterdir(), key=lambda p: p.name.lower())
        if child.is_dir() and (child / "SKILL.md").is_file()
    ]


def zip_skill_dir(skill_dir: Path, temp_dir: Path):
    zip_path = temp_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            arcname = Path(skill_dir.name) / file_path.relative_to(skill_dir)
            zf.write(file_path, arcname.as_posix())
    return zip_path


def make_multipart(fields, files):
    boundary = f"----AgentcadiaBoundary{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")

    for name, filepath, content_type in files:
        filename = os.path.basename(filepath)
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
        body.extend(Path(filepath).read_bytes())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode())
    return boundary, bytes(body)


def http_json(url, method="GET", headers=None, payload=None):
    data = None
    req_headers = headers or {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers = {**req_headers, "Content-Type": "application/json"}

    request = urllib.request.Request(url, data=data, method=method, headers=req_headers)
    with urllib.request.urlopen(request) as response:
        raw = response.read().decode("utf-8")
        return response.status, json.loads(raw)


def http_multipart(url, headers, fields, files):
    boundary, body = make_multipart(fields, files)
    req_headers = {
        **headers,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    request = urllib.request.Request(url, data=body, method="POST", headers=req_headers)
    with urllib.request.urlopen(request) as response:
        raw = response.read().decode("utf-8")
        return response.status, json.loads(raw)


def load_metadata(args):
    if args.metadata_file:
        raw = Path(args.metadata_file).expanduser().read_text(encoding="utf-8")
    elif args.metadata_json:
        raw = args.metadata_json
    else:
        raise SystemExit(
            "Metadata is required. Pass --metadata-file or --metadata-json with title/summary/detailDescription/category/tags."
        )

    try:
        payload = json.loads(raw)
    except Exception as exc:
        raise SystemExit(f"Invalid metadata JSON: {exc}")

    if not isinstance(payload, dict):
        raise SystemExit("Metadata JSON must be an object.")

    missing = []
    for field in REQUIRED_METADATA_FIELDS:
        value = payload.get(field)
        if field == "tags":
            if not isinstance(value, list) or not [item for item in value if isinstance(item, str) and item.strip()]:
                missing.append(field)
        else:
            if not isinstance(value, str) or not value.strip():
                missing.append(field)

    if missing:
        raise SystemExit(f"Metadata JSON missing required fields: {', '.join(missing)}")

    if not isinstance(payload.get("description"), str) or not payload.get("description", "").strip():
        payload["description"] = f"{payload['summary'].strip()}\n\n{payload['detailDescription'].strip()}"

    payload["tags"] = [item.strip() for item in payload.get("tags", []) if isinstance(item, str) and item.strip()]
    return payload


def extract_metadata_preview(agent_payload):
    if not isinstance(agent_payload, dict):
        return None
    return {
        "title": agent_payload.get("title"),
        "titleEn": agent_payload.get("titleEn"),
        "category": agent_payload.get("category"),
        "tags": agent_payload.get("tags"),
        "tagsEn": agent_payload.get("tagsEn"),
        "summary": agent_payload.get("summary"),
        "summaryEn": agent_payload.get("summaryEn"),
        "detailDescription": agent_payload.get("detailDescription"),
        "detailDescriptionEn": agent_payload.get("detailDescriptionEn"),
        "tagline": agent_payload.get("tagline"),
        "taglineEn": agent_payload.get("taglineEn"),
    }


def main():
    args = parse_args()
    origin = args.origin.rstrip("/")
    metadata_payload = load_metadata(args)

    claim_status, claim_data = http_json(
        f"{origin}/api/upload-tasks/claim",
        method="POST",
        payload={"taskId": args.task_id},
    )

    task = claim_data.get("task") or {}
    agent_id = task.get("agentId")
    upload_token = task.get("uploadToken")
    upload_url = task.get("uploadUrl")
    complete_url = task.get("completeUrl")
    metadata_url = task.get("metadataUrl")
    context = task.get("context") or "edit"
    task_lang = task.get("lang") or "en"

    if claim_status >= 400 or not (agent_id and upload_token and upload_url and complete_url and metadata_url):
        raise SystemExit(f"Failed to claim upload task: {json.dumps(claim_data, ensure_ascii=False)}")

    workspace = resolve_workspace(args.workspace)
    markdown_files = collect_markdown_files(workspace)
    skill_dirs = find_skill_dirs(workspace)

    if not markdown_files and not skill_dirs:
        raise SystemExit("Nothing to upload: no root markdown files and no skill directories found.")

    with tempfile.TemporaryDirectory(prefix="agentcadia-publisher-") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        zipped_skills = [zip_skill_dir(skill_dir, temp_dir) for skill_dir in skill_dirs]

        oversized = [path for path in zipped_skills if path.stat().st_size > MAX_SKILL_ZIP_BYTES]
        if oversized:
            names = ", ".join(path.name for path in oversized)
            raise SystemExit(f"Skill package exceeds 10MB limit: {names}")

        upload_files = []
        for markdown_file in markdown_files:
            content_type = mimetypes.guess_type(markdown_file.name)[0] or "text/markdown"
            upload_files.append(("configFiles", str(markdown_file), content_type))
        for skill_zip in zipped_skills:
            upload_files.append(("skillFiles", str(skill_zip), "application/zip"))

        auth_headers = {"Authorization": f"Bearer {upload_token}"}
        upload_status, upload_data = http_multipart(upload_url, auth_headers, [], upload_files)

        metadata_status = 0
        metadata_data = {"success": False}
        metadata_error = None
        metadata_attempted = False
        metadata_succeeded = False
        metadata_preview = None

        if bool(upload_data.get("success")):
            metadata_attempted = True
            metadata_payload = {
                **metadata_payload,
                "uiLanguage": metadata_payload.get("uiLanguage") or task_lang,
            }
            try:
                metadata_status, metadata_data = http_json(
                    metadata_url,
                    method="POST",
                    headers=auth_headers,
                    payload=metadata_payload,
                )
                metadata_succeeded = bool(metadata_data.get("success"))
                metadata_preview = extract_metadata_preview(metadata_data.get("agent"))
                if not metadata_preview or not metadata_preview.get("summary") or not metadata_preview.get("detailDescription"):
                    metadata_succeeded = False
                    metadata_error = "Metadata API returned success but the resulting agent payload is missing summary/detailDescription."
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="ignore")
                try:
                    metadata_data = json.loads(body)
                except Exception:
                    metadata_data = {"success": False, "error": f"HTTP {exc.code}", "body": body}
                metadata_status = exc.code
                metadata_error = metadata_data.get("error") if isinstance(metadata_data, dict) else f"HTTP {exc.code}"

        complete_status = 0
        complete_data = {"success": False}
        try:
            complete_status, complete_data = http_json(
                complete_url,
                method="POST",
                payload={
                    "taskId": args.task_id,
                    "workspacePath": str(workspace),
                    "skillRoots": [str(workspace / "skills")] if skill_dirs else [],
                    "uploadedConfigCount": len(markdown_files),
                    "uploadedSkillCount": len(zipped_skills),
                    "autofillMetadata": False,
                    "status": "completed" if metadata_succeeded else "failed",
                    "lastErrorCode": None if metadata_succeeded else "METADATA_WRITEBACK_REQUIRED",
                    "lastErrorMessage": None if metadata_succeeded else (metadata_error or "Metadata writeback failed after file upload."),
                },
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            try:
                complete_data = json.loads(body)
            except Exception:
                complete_data = {"success": False, "error": f"HTTP {exc.code}", "body": body}
            complete_status = exc.code

        share = complete_data.get("share") if isinstance(complete_data, dict) else None
        notification = share.get("notification") if isinstance(share, dict) else None
        host_reply = share.get("hostReply") if isinstance(share, dict) else None
        runtime_actions = share.get("runtimeActions") if isinstance(share, dict) else None

        share_image_url = share.get("shareImageUrl") if isinstance(share, dict) else None
        agent_url = share.get("agentUrl") if isinstance(share, dict) else None
        message_text = notification.get("text") if isinstance(notification, dict) else None
        message_caption = notification.get("caption") if isinstance(notification, dict) else None
        preferred_owner_delivery = None
        if isinstance(host_reply, dict) and host_reply.get("imageUrl"):
            preferred_owner_delivery = {
                "mode": "image_first",
                "target": "current_chat",
                "imageUrl": host_reply.get("imageUrl"),
                "caption": host_reply.get("caption") or message_caption,
                "fallbackText": host_reply.get("fallbackText") or message_text,
                "linkUrl": host_reply.get("linkUrl") or agent_url,
            }
        elif share_image_url:
            preferred_owner_delivery = {
                "mode": "image_first",
                "target": "current_chat",
                "imageUrl": share_image_url,
                "caption": message_caption,
                "fallbackText": message_text,
                "linkUrl": agent_url,
            }
        elif message_text or agent_url:
            preferred_owner_delivery = {
                "mode": "text_only",
                "target": "current_chat",
                "text": message_text,
                "linkUrl": agent_url,
            }

        overall_success = bool(upload_data.get("success")) and bool(complete_data.get("success")) and metadata_succeeded
        incomplete_reason = None
        if bool(upload_data.get("success")) and bool(complete_data.get("success")) and not metadata_succeeded:
            incomplete_reason = "METADATA_WRITEBACK_REQUIRED"

        result = {
            "success": overall_success,
            "taskId": args.task_id,
            "agentId": agent_id,
            "workspace": str(workspace),
            "context": context,
            "uiLanguage": task_lang,
            "metadataEndpoint": metadata_url,
            "metadataWritebackRequired": True,
            "metadataPreviewRequired": True,
            "metadataWritebackAttempted": metadata_attempted,
            "metadataWritebackSucceeded": metadata_succeeded,
            "metadataPreview": metadata_preview,
            "metadataError": metadata_error,
            "incompleteReason": incomplete_reason,
            "shareImageDeliveryRequired": bool(share_image_url or (isinstance(host_reply, dict) and host_reply.get("imageUrl"))),
            "ownerDeliveryPlan": {
                "separateMessagesRequired": True,
                "step1": "send_metadata_summary_text",
                "step2": "send_share_image_message",
                "finalStepMustBeImage": True,
                "downloadImageFirstIfNeeded": True,
            },
            "uploadedMarkdownFiles": [path.name for path in markdown_files],
            "uploadedSkillPackages": [path.name for path in zipped_skills],
            "claim": {"status": claim_status, "response": claim_data},
            "upload": {"status": upload_status, "response": upload_data},
            "complete": {"status": complete_status, "response": complete_data},
            "metadata": {"status": metadata_status, "response": metadata_data, "request": metadata_payload},
            "share": share,
            "notification": notification,
            "hostReply": host_reply,
            "runtimeActions": runtime_actions,
            "preferredOwnerDelivery": preferred_owner_delivery,
            "messageText": message_text,
            "messageCaption": message_caption,
            "shareImageUrl": share_image_url,
            "agentUrl": agent_url,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        print(
            json.dumps(
                {"success": False, "error": f"HTTP {exc.code}", "body": body},
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)
