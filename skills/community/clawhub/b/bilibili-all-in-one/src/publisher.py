"""Bilibili video uploading and publishing module."""

import os
import json
import asyncio
from typing import Optional, Dict, Any, List
import logging

import httpx

from .auth import BilibiliAuth
from .utils import DEFAULT_HEADERS, API_BASE

_logger = logging.getLogger("bilibili.publisher")


# Publishing API endpoints
PREUPLOAD_URL = "https://member.bilibili.com/preupload"
MEMBER_API_BASE = "https://member.bilibili.com"
ADD_VIDEO_URL = f"{MEMBER_API_BASE}/x/vu/web/add"
EDIT_VIDEO_URL = f"{MEMBER_API_BASE}/x/vu/web/edit"
COVER_UPLOAD_URL = f"{MEMBER_API_BASE}/x/vu/web/cover/up"

# Destructive actions that mutate the user's Bilibili account. These MUST be
# confirmed explicitly by the caller (dry_run=False AND confirm=True) before
# any side effect is performed. This mitigates "Tool Misuse and Exploitation"
# where an upstream agent might invoke publish/edit actions without explicit
# user approval.
_DESTRUCTIVE_ACTIONS = {"upload", "draft", "schedule", "edit"}


def _build_plan(action: str, **params: Any) -> Dict[str, Any]:
    """Build a human-readable plan describing a destructive publishing action.

    The plan is returned to the caller (agent/user) when `dry_run=True` or
    `confirm=False` so that the *exact* title, tags, schedule, target video
    and file path can be reviewed before the action is actually executed.
    """
    redacted = {k: v for k, v in params.items() if k not in ("credential",)}
    return {
        "success": True,
        "dry_run": True,
        "action": action,
        "will_mutate_account": True,
        "preview": redacted,
        "message": (
            "Dry-run preview. No request was sent to Bilibili. "
            "Review the preview above, then re-invoke with "
            "dry_run=False AND confirm=True to actually perform the action."
        ),
    }


class BilibiliPublisher:
    """Publish videos to Bilibili.

    Supports uploading videos, setting metadata, scheduling publications,
    and managing drafts.
    """

    def __init__(self, auth: BilibiliAuth):
        """Initialize BilibiliPublisher.

        Args:
            auth: BilibiliAuth instance (required for publishing).

        Raises:
            ValueError: If auth is not provided or not authenticated.
        """
        if not auth or not auth.is_authenticated:
            raise ValueError("Valid authentication is required for publishing")
        self.auth = auth

    def _get_client(self) -> httpx.AsyncClient:
        """Get an authenticated HTTP client."""
        return self.auth.get_client()

    async def upload(
        self,
        file_path: str,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        category: str = "171",
        cover_path: Optional[str] = None,
        dynamic: str = "",
        no_reprint: int = 1,
        open_elec: int = 0,
        dry_run: bool = True,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """Upload and publish a video to Bilibili.

        Args:
            file_path: Path to the video file.
            title: Video title (max 80 chars).
            description: Video description (max 2000 chars).
            tags: List of tags (max 12 tags, each max 20 chars).
            category: Category TID (default '171' for electronic gaming).
            cover_path: Path to cover image (optional).
            dynamic: Dynamic/feed text.
            no_reprint: 1 = original, 0 = repost.
            open_elec: 1 = enable charging, 0 = disable.
            dry_run: If True (default), return a preview without calling the
                     Bilibili API. The caller MUST review the preview and
                     re-invoke with dry_run=False + confirm=True to actually
                     publish. This is a safety guardrail against agents
                     inadvertently mutating the user's public channel.
            confirm: Must be set to True together with dry_run=False to
                     authorize the publish action.

        Returns:
            Upload result with video info, or a dry-run preview.
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": f"File not found: {file_path}"}

        # Validate inputs
        if len(title) > 80:
            return {"success": False, "message": "Title must be 80 characters or less"}

        tags = tags or ["bilibili"]
        if len(tags) > 12:
            tags = tags[:12]

        # Safety guardrail: require explicit confirmation before mutating
        # the user's public Bilibili channel.
        if dry_run or not confirm:
            return _build_plan(
                "upload",
                file_path=file_path,
                title=title,
                description=description,
                tags=tags,
                category=category,
                cover_path=cover_path,
                dynamic=dynamic,
                no_reprint=no_reprint,
                open_elec=open_elec,
            )
        _logger.warning(
            "[publisher] Executing CONFIRMED upload: title=%r tags=%r file=%r",
            title, tags, file_path,
        )

        # Step 1: Pre-upload to get upload params
        preupload_result = await self._preupload(file_path)
        if not preupload_result.get("success"):
            return preupload_result

        # Step 2: Upload video file
        upload_result = await self._upload_file(
            file_path,
            preupload_result,
        )
        if not upload_result.get("success"):
            return upload_result

        # Step 3: Upload cover if provided
        cover_url = ""
        if cover_path and os.path.exists(cover_path):
            cover_result = await self._upload_cover(cover_path)
            if cover_result.get("success"):
                cover_url = cover_result.get("url", "")

        # Step 4: Submit video
        submit_result = await self._submit_video(
            filename=upload_result["filename"],
            title=title,
            desc=description,
            tags=tags,
            tid=int(category),
            cover=cover_url,
            dynamic=dynamic,
            no_reprint=no_reprint,
            open_elec=open_elec,
        )

        return submit_result

    async def draft(
        self,
        file_path: str,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        category: str = "171",
        cover_path: Optional[str] = None,
        dry_run: bool = True,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """Save a video as draft.

        Args:
            file_path: Path to the video file.
            title: Video title.
            description: Video description.
            tags: List of tags.
            category: Category TID.
            cover_path: Path to cover image.
            dry_run: See `upload()`. Default True.
            confirm: See `upload()`. Default False.

        Returns:
            Draft save result, or a dry-run preview.
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": f"File not found: {file_path}"}

        tags = tags or ["bilibili"]

        if dry_run or not confirm:
            return _build_plan(
                "draft",
                file_path=file_path,
                title=title,
                description=description,
                tags=tags,
                category=category,
                cover_path=cover_path,
            )
        _logger.warning(
            "[publisher] Executing CONFIRMED draft save: title=%r file=%r",
            title, file_path,
        )

        # Upload video file
        preupload_result = await self._preupload(file_path)
        if not preupload_result.get("success"):
            return preupload_result

        upload_result = await self._upload_file(file_path, preupload_result)
        if not upload_result.get("success"):
            return upload_result

        # Upload cover if provided
        cover_url = ""
        if cover_path and os.path.exists(cover_path):
            cover_result = await self._upload_cover(cover_path)
            if cover_result.get("success"):
                cover_url = cover_result.get("url", "")

        # Save as draft (use the same add API with draft=1)
        async with self._get_client() as client:
            resp = await client.post(
                ADD_VIDEO_URL,
                params={"csrf": self.auth.csrf},
                json={
                    "videos": [{
                        "filename": upload_result["filename"],
                        "title": title,
                        "desc": "",
                    }],
                    "title": title,
                    "desc": description,
                    "tag": ",".join(tags),
                    "tid": int(category),
                    "cover": cover_url,
                    "copyright": 1,
                    "no_reprint": 1,
                    "open_elec": 0,
                    "draft": 1,
                    "csrf": self.auth.csrf,
                },
            )
            if resp.status_code != 200:
                return {"success": False, "message": f"HTTP {resp.status_code}: {resp.text[:500]}"}
            try:
                data = resp.json()
            except Exception:
                return {"success": False, "message": f"Invalid JSON response: {resp.text[:500]}"}

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "Draft save failed")}

        return {
            "success": True,
            "draft_id": data.get("data", {}).get("aid"),
            "message": "Draft saved successfully",
        }

    async def schedule(
        self,
        file_path: str,
        title: str,
        schedule_time: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        category: str = "171",
        cover_path: Optional[str] = None,
        dry_run: bool = True,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """Schedule a video for future publication.

        Args:
            file_path: Path to the video file.
            title: Video title.
            schedule_time: Scheduled publish time (ISO 8601 format).
            description: Video description.
            tags: List of tags.
            category: Category TID.
            cover_path: Path to cover image.
            dry_run: See `upload()`. Default True.
            confirm: See `upload()`. Default False.

        Returns:
            Schedule result, or a dry-run preview.
        """
        import datetime

        if not os.path.exists(file_path):
            return {"success": False, "message": f"File not found: {file_path}"}

        # Parse schedule time
        try:
            dt = datetime.datetime.fromisoformat(schedule_time.replace("Z", "+00:00"))
            timestamp = int(dt.timestamp())
        except ValueError:
            return {"success": False, "message": f"Invalid schedule time format: {schedule_time}"}

        tags = tags or ["bilibili"]

        if dry_run or not confirm:
            return _build_plan(
                "schedule",
                file_path=file_path,
                title=title,
                schedule_time=schedule_time,
                description=description,
                tags=tags,
                category=category,
                cover_path=cover_path,
            )
        _logger.warning(
            "[publisher] Executing CONFIRMED schedule: title=%r schedule_time=%r file=%r",
            title, schedule_time, file_path,
        )

        # Upload video file
        preupload_result = await self._preupload(file_path)
        if not preupload_result.get("success"):
            return preupload_result

        upload_result = await self._upload_file(file_path, preupload_result)
        if not upload_result.get("success"):
            return upload_result

        # Upload cover if provided
        cover_url = ""
        if cover_path and os.path.exists(cover_path):
            cover_result = await self._upload_cover(cover_path)
            if cover_result.get("success"):
                cover_url = cover_result.get("url", "")

        # Submit with schedule
        submit_result = await self._submit_video(
            filename=upload_result["filename"],
            title=title,
            desc=description,
            tags=tags,
            tid=int(category),
            cover=cover_url,
            dtime=timestamp,
        )

        if submit_result.get("success"):
            submit_result["scheduled_time"] = schedule_time

        return submit_result

    async def edit(
        self,
        bvid: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        cover_path: Optional[str] = None,
        file_path: Optional[str] = None,
        dry_run: bool = True,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """Edit an existing video's metadata.

        Args:
            bvid: BV number of the video to edit.
            title: New title (if changing).
            description: New description (if changing).
            tags: New tags (if changing).
            cover_path: New cover image path (if changing).
            file_path: Path to video file (required for re-upload).
            dry_run: See `upload()`. Default True.
            confirm: See `upload()`. Default False.

        Returns:
            Edit result, or a dry-run preview.
        """
        if dry_run or not confirm:
            return _build_plan(
                "edit",
                bvid=bvid,
                title=title,
                description=description,
                tags=tags,
                cover_path=cover_path,
                file_path=file_path,
            )
        _logger.warning(
            "[publisher] Executing CONFIRMED edit: bvid=%r title=%r file=%r",
            bvid, title, file_path,
        )

        # First get current video info
        async with self._get_client() as client:
            resp = await client.get(
                f"{API_BASE}/x/web-interface/view",
                params={"bvid": bvid},
            )
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "Video not found")}

        video = data["data"]

        # Re-upload video file to get a fresh filename
        if file_path and os.path.exists(file_path):
            preupload_result = await self._preupload(file_path)
            if not preupload_result.get("success"):
                return preupload_result
            upload_result = await self._upload_file(file_path, preupload_result)
            if not upload_result.get("success"):
                return upload_result
            new_filename = upload_result["filename"]
        else:
            return {"success": False, "message": "file_path is required for editing (B站 requires re-upload)"}

        # Build edit payload with videos info
        new_title = title or video.get("title")
        videos = [{
            "filename": new_filename,
            "title": new_title,
            "desc": "",
        }]

        edit_data = {
            "aid": video["aid"],
            "videos": videos,
            "title": new_title,
            "desc": description if description is not None else video.get("desc", ""),
            "tag": ",".join(tags) if tags else ",".join(
                t.get("tag_name", "") for t in video.get("tags", []) if t.get("tag_name")
            ),
            "tid": video.get("tid"),
            "copyright": video.get("copyright", 1),
            "csrf": self.auth.csrf,
        }

        # Upload new cover if provided
        if cover_path and os.path.exists(cover_path):
            cover_result = await self._upload_cover(cover_path)
            if cover_result.get("success"):
                edit_data["cover"] = cover_result.get("url", "")

        async with self._get_client() as client:
            resp = await client.post(
                EDIT_VIDEO_URL,
                params={"csrf": self.auth.csrf},
                json=edit_data,
            )
            if resp.status_code != 200:
                return {"success": False, "message": f"HTTP {resp.status_code}: {resp.text[:500]}"}
            try:
                result = resp.json()
            except Exception:
                return {"success": False, "message": f"Invalid JSON response: {resp.text[:500]}"}

        if result.get("code") != 0:
            return {"success": False, "message": result.get("message", "Edit failed")}

        return {
            "success": True,
            "bvid": bvid,
            "message": "Video edited successfully",
        }

    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute a publisher action.

        Args:
            action: Action name ('upload', 'draft', 'schedule', 'edit').
            **kwargs: Additional parameters for the action.

        Returns:
            Action result dict.
        """
        actions = {
            "upload": self.upload,
            "draft": self.draft,
            "schedule": self.schedule,
            "edit": self.edit,
        }

        handler = actions.get(action)
        if not handler:
            return {"success": False, "message": f"Unknown action: {action}"}

        import inspect
        sig = inspect.signature(handler)
        valid_params = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return await handler(**valid_params)

    async def _preupload(self, file_path: str) -> Dict[str, Any]:
        """Request pre-upload parameters from Bilibili.

        Args:
            file_path: Path to the video file.

        Returns:
            Pre-upload parameters dict.
        """
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        async with self._get_client() as client:
            resp = await client.get(
                PREUPLOAD_URL,
                params={
                    "name": file_name,
                    "size": file_size,
                    "r": "upos",
                    "profile": "ugcupos/bup",
                    "ssl": 0,
                    "version": "2.14.0",
                    "build": 2140000,
                    "upcdn": "bda2",
                    "probe_version": 20221109,
                },
            )
            data = resp.json()

        if "upos_uri" not in data:
            return {"success": False, "message": "Pre-upload failed"}

        return {
            "success": True,
            "upos_uri": data["upos_uri"],
            "auth": data.get("auth"),
            "biz_id": data.get("biz_id"),
            "chunk_size": data.get("chunk_size", 4 * 1024 * 1024),
            "endpoints": data.get("endpoints", []),
            "file_size": file_size,
            "file_name": file_name,
        }

    async def _upload_file(
        self,
        file_path: str,
        preupload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Upload a video file in chunks.

        Args:
            file_path: Path to the video file.
            preupload: Pre-upload parameters from _preupload().

        Returns:
            Upload result with filename.
        """
        upos_uri = preupload["upos_uri"]
        auth = preupload.get("auth")
        biz_id = preupload.get("biz_id")
        chunk_size = preupload.get("chunk_size", 4 * 1024 * 1024)
        file_size = preupload["file_size"]

        # Extract upos key from URI
        upos_key = upos_uri.replace("upos://", "")
        filename = upos_key.split("/")[-1].split(".")[0]

        # Calculate chunk count
        chunk_count = (file_size + chunk_size - 1) // chunk_size

        # Init upload
        upload_base = f"https://upos-sz-upcdnbda2.bilivideo.com/{upos_key}"

        async with self._get_client() as client:
            # Fetch upload ID
            resp = await client.post(
                upload_base,
                params={
                    "uploads": "",
                    "output": "json",
                },
                headers={"X-Upos-Auth": auth} if auth else {},
            )

            try:
                init_data = resp.json()
                upload_id = init_data.get("upload_id", "")
            except Exception:
                return {"success": False, "message": "Failed to initialize upload"}

        # Upload chunks
        with open(file_path, "rb") as f:
            for chunk_idx in range(chunk_count):
                chunk_data = f.read(chunk_size)
                start = chunk_idx * chunk_size
                end = min(start + len(chunk_data), file_size)

                async with self._get_client() as client:
                    resp = await client.put(
                        upload_base,
                        params={
                            "partNumber": chunk_idx + 1,
                            "uploadId": upload_id,
                            "chunk": chunk_idx,
                            "chunks": chunk_count,
                            "size": len(chunk_data),
                            "start": start,
                            "end": end,
                            "total": file_size,
                        },
                        headers={
                            "X-Upos-Auth": auth or "",
                            "Content-Type": "application/octet-stream",
                        },
                        content=chunk_data,
                    )

                    if resp.status_code not in (200, 202):
                        return {
                            "success": False,
                            "message": f"Upload chunk {chunk_idx + 1}/{chunk_count} failed",
                        }

        # Complete upload
        parts = [{"partNumber": i + 1, "eTag": "etag"} for i in range(chunk_count)]

        async with self._get_client() as client:
            resp = await client.post(
                upload_base,
                params={
                    "output": "json",
                    "name": preupload["file_name"],
                    "profile": "ugcupos/bup",
                    "uploadId": upload_id,
                    "biz_id": biz_id or 0,
                },
                json={"parts": parts},
                headers={"X-Upos-Auth": auth or ""},
            )

        return {
            "success": True,
            "filename": filename,
            "upos_uri": upos_uri,
        }

    async def _upload_cover(self, cover_path: str) -> Dict[str, Any]:
        """Upload a cover image.

        Args:
            cover_path: Path to the cover image.

        Returns:
            Upload result with cover URL.
        """
        if not os.path.exists(cover_path):
            return {"success": False, "message": f"Cover file not found: {cover_path}"}

        with open(cover_path, "rb") as f:
            cover_data = f.read()

        # Detect MIME type
        if cover_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif cover_path.lower().endswith((".jpg", ".jpeg")):
            mime_type = "image/jpeg"
        else:
            mime_type = "image/jpeg"

        import base64
        cover_b64 = f"data:{mime_type};base64,{base64.b64encode(cover_data).decode()}"

        async with self._get_client() as client:
            resp = await client.post(
                COVER_UPLOAD_URL,
                data={
                    "cover": cover_b64,
                    "csrf": self.auth.csrf,
                },
            )
            data = resp.json()

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "Cover upload failed")}

        return {
            "success": True,
            "url": data.get("data", {}).get("url", ""),
        }

    async def _submit_video(
        self,
        filename: str,
        title: str,
        desc: str = "",
        tags: Optional[List[str]] = None,
        tid: int = 171,
        cover: str = "",
        dynamic: str = "",
        no_reprint: int = 1,
        open_elec: int = 0,
        dtime: int = 0,
    ) -> Dict[str, Any]:
        """Submit a video for publishing.

        Args:
            filename: Uploaded video filename.
            title: Video title.
            desc: Description.
            tags: Tags list.
            tid: Category TID.
            cover: Cover image URL.
            dynamic: Dynamic text.
            no_reprint: Original flag.
            open_elec: Charging flag.
            dtime: Scheduled publish timestamp (0 = immediate).

        Returns:
            Submit result.
        """
        tags = tags or ["bilibili"]

        payload = {
            "videos": [{
                "filename": filename,
                "title": title,
                "desc": "",
            }],
            "title": title,
            "desc": desc,
            "tag": ",".join(tags),
            "tid": tid,
            "cover": cover,
            "dynamic": dynamic,
            "copyright": 1 if no_reprint else 2,
            "no_reprint": no_reprint,
            "open_elec": open_elec,
            "csrf": self.auth.csrf,
        }

        if dtime > 0:
            payload["dtime"] = dtime

        async with self._get_client() as client:
            params = {"csrf": self.auth.csrf}
            resp = await client.post(
                ADD_VIDEO_URL,
                params=params,
                json=payload,
            )
            if resp.status_code != 200:
                return {
                    "success": False,
                    "message": f"HTTP {resp.status_code}: {resp.text[:500]}",
                }
            try:
                data = resp.json()
            except Exception:
                return {
                    "success": False,
                    "message": f"Invalid JSON response: {resp.text[:500]}",
                }

        if data.get("code") != 0:
            return {"success": False, "message": data.get("message", "Submit failed")}

        result_data = data.get("data", {})
        return {
            "success": True,
            "aid": result_data.get("aid"),
            "bvid": result_data.get("bvid"),
            "message": "Video published successfully",
        }
