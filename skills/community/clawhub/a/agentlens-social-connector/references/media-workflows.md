# Understanding Media Files

Use this file when the user asks the agent to understand image/video media, analyze visual post content, summarize video, transcribe audio, or reason over media beyond the text returned by the AgentLens API.

## AgentLens API Inputs

Use the normalized AgentLens API result from `references/agentlens-api.md`:

- `text`: caption, article body, post text, or title text
- `subtitle`: transcript/subtitle when available
- `media`: normalized `data.media[]`
- `media[].type`: single-item responses use `video` or `image`; helper workflows also handle `audio` when returned or normalized by the runtime
- `media[].source_url`: preferred direct media URL when returned
- `media[].cdn_url`: fallback direct media URL when `source_url` is missing
- `media[].cover`: thumbnail/cover URL; do not use it as the original media file when direct media URLs are missing

Prefer text and subtitles when they are sufficient. However, for image-first or video-first content, if the AgentLens API returns image or video URLs, media is part of the content. Read all returned media before summarizing by default. For mixed-format platforms such as X/Twitter, Weibo, LinkedIn, or Facebook, decide from the returned item structure: short text, high media count, video, long image, screenshot, infographic, tutorial image, comparison image, poster, or chat screenshot should be treated as media-first. Answer from text/subtitle/metadata alone only when the content is clearly text-first, or when media is unavailable or cannot be processed and that limitation is stated clearly.

## Routing

```text
AgentLens API result is available
 -> User only needs text summary and the content is clearly text-first:
      summarize text/title + subtitle + metadata
 -> Content is from an image/video-first platform, or a mixed-format platform item is media-first, and image URLs are returned:
      run Understand Image Content
 -> Content is from an image/video-first platform, or a mixed-format platform item is media-first, video URLs are returned, and subtitle exists:
      summarize from subtitle + text/title + metadata; sample video frames only if the user asks for visual-level understanding
 -> Content is from an image/video-first platform, or a mixed-format platform item is media-first, video URLs are returned, and subtitle is missing:
      run Video Summary SOP
 -> AgentLens API returns media URLs but no readable text:
      attempt to understand the necessary media; if that fails, say that only media metadata is available
```

## Capability Checks

Use host-native transcription, vision, or media tools first when available and authorized. If no native tool is available, check local tools before asking the user to install or configure anything:

```bash
command -v ffmpeg
command -v ffprobe
command -v faster-whisper
python3 -c "import faster_whisper; print('faster_whisper import ok')"
```

Before treating a local dependency check as conclusive, identify the runtime that will execute the media task. Prefer a host-provided or user-approved managed runtime when one is available, and run the import check with that runtime rather than relying only on a bare `python3` from the shell path. A failed check in one interpreter does not prove that the capability is absent elsewhere in the current runtime. Do not persist machine-specific executable paths, virtual-environment paths, or tool-discovery results as cross-runtime configuration.

Interpretation:

- If a host-native vision/image-reading tool exists, use it for image understanding and follow this skill's source, temporary-file, and uncertainty rules.
- If no image-reading capability exists, do not pretend to understand images. Offer a user-approved multimodal model, image-reading tool, or runtime if one is configured.
- If a host-native transcription tool exists, use it and follow this skill's source, temporary-file, and uncertainty rules.
- If `faster_whisper` imports successfully, local Whisper is available. Do not ask the user to install it.
- Do not report a tool as unavailable until the selected execution runtime has been checked. If a prior runtime check was incomplete, correct it before asking the user to install or configure anything.
- If video must be converted to audio and `ffmpeg` is missing, check for another host media extraction tool before asking about ffmpeg.
- If external speech-to-text may require audio compression or chunking, check `ffmpeg` and `ffprobe` before downloading large media or calling the API.
- Ask about installation, configuration, model switching, or paid APIs only after the checks above fail or require permission.

## Failure Attribution

When media understanding cannot be completed, report the precise verified blocker. Distinguish between:

- AgentLens API returned no media or no direct media URL;
- media URL download failed or expired;
- runtime has no image/vision capability;
- video requires frame extraction but no frame extraction path is available;
- video requires speech understanding but no transcription path is available;
- file is too large for the current runtime;
- required permission/credential is missing;
- external API or model service is unavailable.

Do not say the model/runtime cannot read images or video unless that exact capability check failed in the current runtime. If the issue is a video-only response with no extracted frames yet, say frame extraction or transcription is unavailable/pending, not that image reading is blocked.

Audio extraction command when `ffmpeg` is available:

```bash
ffmpeg -y -i /tmp/agentlens_{platform}_{timestamp}.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/agentlens_audio_{timestamp}.wav
```

## Understand Image Content

Read and understand image content when the user asks what images show, or when the item is from an image-first platform and image URLs are returned.

Steps:

1. Select all returned image URLs by default. Only when media cannot be downloaded, has expired, or exceeds the current runtime's practical count/size limits should the agent state the limitation and ask whether to process media in batches, process a subset, or provide a limited summary.
2. Download selected images to `/tmp/agentlens_{platform}_{timestamp}_{index}.{ext}`.
3. Check whether the current runtime has a usable native image/vision capability for local files.
4. If a vision capability exists, read the local image files with it.
5. If no vision capability exists, do not pretend to understand the images. Tell the user that this runtime cannot read images directly, then offer to:
   - continue with a limited summary from text/caption/subtitle/source metadata;
   - switch to a user-approved multimodal model, image-reading tool, or runtime if one is configured;
   - save the image URLs or downloaded filenames for later review.
6. When image understanding succeeds, combine visual findings with `text`, `title`, author/source, and platform metadata.
7. State which conclusions come from image understanding and which come from text/caption.

If an image cannot be downloaded or read, say so and summarize the available text instead of guessing.

## Video Summary SOP

Use this SOP when the user asks to summarize a video and the AgentLens API did not return `subtitle`.

```text
Step 1: Confirm the available media
 -> Prefer media[].type == "audio" when available
 -> Otherwise use media[].type == "video"
 -> If no audio/video URL exists:
      tell the user the AgentLens API returned no downloadable media for transcription;
      summarize available text/title/metadata only

Step 2: Resolve transcription path before asking the user to choose
 -> Complete Capability Checks above before choosing a path
 -> Check host-native transcription/media tools
 -> Check local faster-whisper availability
 -> Check ffmpeg/ffprobe availability if video-to-audio extraction, compression, or chunking may be needed
 -> If the user says a transcriber is already installed, verify it and use it if it works

Step 3: If a working transcription path exists
 -> Download only the needed audio/video file to /tmp/agentlens_*
 -> Extract audio if needed
 -> If using OpenAI Whisper or another file-size-limited speech-to-text API, check the audio file size before upload
 -> If the audio is too large for one request, compress and split it into smaller overlapping chunks, then transcribe chunks in order
 -> Transcribe
 -> Summarize transcript + text/title + source metadata
 -> If a provisional summary was sent while transcription was running, label it as provisional. When transcription finishes, proactively deliver one consolidated final answer that uses the transcript and explicitly states whether the provisional summary was corrected, supplemented, or retained without change.
 -> When using chunked transcription, treat repeated or broken words near chunk boundaries as transcription artifacts
 -> Mention whether the summary is transcript-based, metadata-only, or combined

Step 4: If no working transcription path exists
 -> Ask the user which path to use before downloading large media or spending paid quota:
    A) Configure/use local transcription, if they want a local free path
    B) Use an approved speech-to-text API, if they have a key or runtime connector
    C) Continue with text/title/media metadata only
 -> If the user chooses A or B, continue with Step 3 after the tool/key is available
 -> If the user chooses C or declines, summarize only the available metadata and state the limitation
```

## Long-Running Media Tasks

When a media download, extraction, or transcription continues after an interim response, retain the task state and report completion without requiring the user to ask again. The completion response must include the requested transcript or media result and a final summary. If an interim summary was provided, reconcile it against the completed evidence instead of leaving two potentially inconsistent summaries.

Suggested user prompt when no transcription path is available:

```text
The AgentLens API did not return subtitles for this video. To summarize the spoken content, I need a transcription path. I checked the current runtime and did not find a working one.

Options:
A) Use or configure local transcription
B) Use an approved speech-to-text API
C) Continue with the title, caption, and media metadata only
Which would you prefer?
```

## Execution Helpers

Use these helpers when no host-native tool already performs the requested step. They are intentionally small and standard-library based so an agent can copy them into the current runtime with minimal changes.

### Media Selection And Download Helper

Choose media according to the current task. For media-first summary or analysis, process all returned direct-URL media by default. For narrow tasks, prefer direct audio for transcription, otherwise video for video summaries, and selected images for image understanding.

```python
import mimetypes
import time
import urllib.parse
import urllib.request
from pathlib import Path


def _media_type(item):
    return str(item.get("type") or item.get("media_type") or "").lower()


def _media_url(item):
    return item.get("source_url") or item.get("cdn_url")


def select_media(media, *, want):
    """want: 'audio', 'video', 'image', or 'images'."""
    typed = [item for item in (media or []) if _media_url(item)]
    if want == "audio":
        for item in typed:
            if _media_type(item) == "audio":
                return [item]
        for item in typed:
            if _media_type(item) == "video":
                return [item]
        return []
    if want == "video":
        for item in typed:
            if _media_type(item) == "video":
                return [item]
        return []
    if want == "image":
        for item in typed:
            if _media_type(item) in ("pic", "image", "photo"):
                return [item]
        return []
    if want == "images":
        return [item for item in typed if _media_type(item) in ("pic", "image", "photo")]
    raise ValueError("want must be audio, video, image, or images")


def _extension_from_url(url, default_ext):
    path = urllib.parse.urlparse(url).path
    guessed = Path(path).suffix.lower()
    if guessed and len(guessed) <= 6:
        return guessed
    return default_ext


def download_media_item(item, platform="social", index=0, timeout=120):
    url = _media_url(item)
    if not url:
        raise ValueError("media_url_missing: media item has no source_url or cdn_url")
    kind = _media_type(item)
    default_ext = ".mp4" if kind == "video" else ".mp3" if kind == "audio" else ".jpg"
    ext = _extension_from_url(url, default_ext)
    ts = int(time.time())
    target = Path(f"/tmp/agentlens_{platform}_{ts}_{index}{ext}")
    req = urllib.request.Request(url, headers={"User-Agent": "AgentLensSocialConnector/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        target.write_bytes(resp.read())
    if target.stat().st_size == 0:
        raise RuntimeError(f"downloaded media is empty: {target}")
    return str(target)
```

Use the returned local path with the runtime's native vision/transcription tool. If a download fails, state that media understanding/transcription could not be completed and continue with text/subtitle metadata only unless the user asks to retry.

Items without `source_url` and `cdn_url` must be reported as `media_url_missing`. Do not substitute `cover` as the original media file; it is only thumbnail/preview evidence.

### Audio Extraction Helper

Use this only when the selected media is video and transcription requires an audio file. If a host-native media extraction tool exists, use that first.

```python
import subprocess
import time
from pathlib import Path


def extract_audio_with_ffmpeg(video_path):
    audio_path = f"/tmp/agentlens_audio_{int(time.time())}.wav"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path,
    ]
    subprocess.run(cmd, check=True, timeout=300)
    if not Path(audio_path).exists() or Path(audio_path).stat().st_size == 0:
        raise RuntimeError("ffmpeg did not create a usable audio file")
    return audio_path
```

### Local Whisper Helper

Use only after `python3 -c "import faster_whisper"` succeeds, or after the user approves installing/configuring local transcription.

```python
def transcribe_with_faster_whisper(audio_path, model_name="base"):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path)
    text_parts = []
    timed_segments = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            text_parts.append(text)
            timed_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": text,
            })
    return {
        "text": " ".join(text_parts).strip(),
        "segments": timed_segments,
        "language": getattr(info, "language", None),
    }
```

### Speech-To-Text API Helper

Use this only after the user chooses or has already approved an external speech-to-text API. The default documented path is OpenAI audio transcription because `OPENAI_API_KEY` is declared in this skill metadata. Do not call this API when a working native/local transcription path is available unless the user specifically prefers it.

```python
import json
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path


OPENAI_TRANSCRIPTION_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"


def _multipart_form(fields, files, boundary):
    body = bytearray()
    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")
    for name, spec in files.items():
        filename, content_type, data = spec
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode())
        body.extend(data)
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    return bytes(body)


def transcribe_with_openai(audio_path, api_key, model="whisper-1", timeout=180):
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI transcription")
    path = Path(audio_path)
    if path.stat().st_size >= 24 * 1024 * 1024:
        raise ValueError("audio file is too large for one OpenAI transcription request; split it first")
    boundary = "----AgentLensBoundary7MA4YWxkTrZu0gW"
    data = path.read_bytes()
    body = _multipart_form(
        {"model": model},
        {"file": (path.name, "audio/mpeg" if path.suffix.lower() == ".mp3" else "audio/wav", data)},
        boundary,
    )
    req = urllib.request.Request(
        OPENAI_TRANSCRIPTION_ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return {"text": result.get("text", ""), "raw": result}


def compress_and_split_audio(audio_path, chunk_seconds=300, overlap_seconds=2):
    """Requires ffmpeg/ffprobe. Returns MP3 chunks with slight overlap for safer summaries."""
    base = Path(tempfile.mkdtemp(prefix="agentlens_audio_chunks_"))
    normalized = base / "audio_16k_64k.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", audio_path,
        "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "libmp3lame", "-b:a", "64k",
        str(normalized),
    ], check=True, timeout=300)
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(normalized),
    ]).decode("utf-8").strip())
    step = max(30, chunk_seconds - overlap_seconds)
    chunks = []
    start = 0.0
    index = 0
    while start < duration:
        chunk = base / f"chunk_{index:03d}.mp3"
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(max(0, start)),
            "-t", str(chunk_seconds),
            "-i", str(normalized),
            "-c", "copy",
            str(chunk),
        ], check=True, timeout=300)
        chunks.append(str(chunk))
        start += step
        index += 1
    return chunks


def transcribe_openai_with_chunks(audio_path, api_key):
    path = Path(audio_path)
    if path.stat().st_size < 24 * 1024 * 1024:
        return transcribe_with_openai(str(path), api_key)["text"]
    chunks = compress_and_split_audio(str(path), chunk_seconds=300)
    texts = []
    for chunk in chunks:
        if Path(chunk).stat().st_size >= 24 * 1024 * 1024:
            raise ValueError(f"audio chunk is still too large: {chunk}")
        texts.append(transcribe_with_openai(chunk, api_key)["text"])
    return "\n".join(text for text in texts if text).strip()
```

The 24MB threshold intentionally leaves buffer below OpenAI's documented 25MB file limit; if provider limits change, use the lower current limit. Chunked transcription may duplicate or cut a few words near chunk boundaries. When summarizing chunked transcripts, treat boundary repetitions or abrupt sentence breaks as transcription artifacts.

If `OPENAI_API_KEY` is missing, ask the user whether to provide it for the current transcription request, use/configure local transcription instead, or continue with metadata-only summary. Never print the key.

### Video Summary Runner Pattern

Use this end-to-end pattern after an AgentLens API result has been normalized and no `subtitle` is available:

```python
def video_summary_transcript_path(agentlens_result, *, platform, stt_choice=None, openai_key=None):
    media = agentlens_result.get("media") or []
    selected = select_media(media, want="audio")
    if not selected:
        return {"ok": False, "reason": "AgentLens API returned no downloadable audio/video media"}
    item = selected[0]
    local_path = download_media_item(item, platform=platform)
    if _media_type(item) == "video":
        audio_path = extract_audio_with_ffmpeg(local_path)
    else:
        audio_path = local_path
    if stt_choice == "openai":
        text = transcribe_openai_with_chunks(audio_path, openai_key)
        return {"ok": True, "transcript": text, "source": "openai"}
    result = transcribe_with_faster_whisper(audio_path)
    return {"ok": True, "transcript": result["text"], "source": "faster-whisper"}
```

Before running this pattern, complete the capability checks and user approval rules from the Video Summary SOP. If the runner fails, report the failed step and offer: retry, switch transcription path, or continue with metadata-only summary.

## Download Rules

- Download only media needed for the current request.
- Use `/tmp/agentlens_*` filenames only.
- Use bounded download timeouts when the runtime supports them.
- Do not use cookies, social account credentials, or browser sessions to retrieve media.
- Do not treat returned media URLs as permanent archive links.
- Do not bulk-delete temporary files without showing the affected files and getting user confirmation.

## Output Pattern

For combined text and media summaries, prefer:

```markdown
**Summary**
...

**Visual/Media Interpretation**
- ...

**Transcript Notes**
- ...

**Source**
Platform: ...
Author: ...
```

If image/video understanding was not performed, do not imply it was. Say that the answer is based on text/subtitle metadata returned by the AgentLens API.
