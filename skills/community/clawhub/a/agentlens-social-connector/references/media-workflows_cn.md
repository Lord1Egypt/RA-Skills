# 媒体文件理解工作流

当用户要求看图、分析视觉内容、总结视频、转写音频，或需要理解 AgentLens API 文本结果之外的媒体信息时，使用本文档。

## AgentLens API 返回内容

先使用 `references/agentlens-api_cn.md` 中规范化后的结果：

- `text`：正文、说明文案、文章内容、帖子文本或标题文本
- `subtitle`：字幕或转写文本，如有
- `media`：规范化后的 `data.media[]`
- `media[].type`：单作品响应使用 `video` 或 `image`；如果运行环境或响应规范化出 `audio`，辅助流程也能处理
- `media[].source_url`：下载或读取原始媒体时，默认使用这个地址
- `media[].cdn_url`：如果没有 `source_url`，再使用这个地址
- `media[].cover`：封面或缩略图；即使没有可下载的媒体地址，也不要把它当作原始媒体文件使用

原则：文本和字幕足够回答时，不下载媒体。但对图片/视频主导内容，如果 AgentLens API 返回图片或视频 URL，媒体是内容的一部分，默认必须读取全部返回媒体后再总结。X/Twitter、微博、LinkedIn、Facebook 等混合型平台按单条内容结构判断：短正文、多媒体、视频、长图、截图、信息图、教程图、对比图、海报或聊天截图按媒体主导处理。只有文字主导内容，或媒体不可用/无法处理并已明确说明时，才可以只基于文本、字幕和元数据回答。

## 判断路径

```text
已有 AgentLens API 结果
 -> 用户只需要文本总结，且内容明显是文字主导：
      基于标题、正文、字幕和来源信息总结
 -> 内容来自图片/视频主导平台，或混合型平台中单条内容呈媒体主导，且返回图片 URL：
      执行“理解图片内容”
 -> 内容来自图片/视频主导平台，或混合型平台中单条内容呈媒体主导，返回视频 URL，且 AgentLens API 返回 subtitle：
      基于字幕 + 正文 + 来源信息总结；如果用户要求画面级理解，再抽样读取视频画面
 -> 内容来自图片/视频主导平台，或混合型平台中单条内容呈媒体主导，返回视频 URL，但没有 subtitle：
      执行“视频总结 SOP”
 -> AgentLens API 只返回媒体链接，没有可读文本：
      必须尝试理解必要媒体；如果失败，说明只能基于媒体元数据作有限判断
```

## 能力检查

优先使用当前环境中已经授权可用的原生图片理解、转写或媒体处理工具。如果没有，再检查本地工具；检查失败后，才询问用户是否切换模型、安装工具、配置或使用付费 API。

```bash
command -v ffmpeg
command -v ffprobe
command -v faster-whisper
python3 -c "import faster_whisper; print('faster_whisper import ok')"
```

在把本地依赖检查当作最终结论前，先确认实际会执行媒体任务的运行时。若存在宿主提供或用户批准的受管运行时，优先用该运行时做导入检查，而不是只依赖 shell 路径中的裸 `python3`。一个解释器中的检查失败，不能证明当前运行环境的其他可用运行时也缺少该能力。不得把机器特定的可执行文件路径、虚拟环境路径或工具发现结果持久化为跨运行时配置。

判断规则：

- 如果当前环境有原生图片读取/视觉工具，优先使用，同时遵守本 Skill 的来源、临时文件和不确定性说明规则。
- 如果当前环境不能读取图片，不要假装已经看过图片；如果已配置用户授权的多模态模型、图片读取工具或其他可看图运行环境，询问是否切换过去处理。
- 如果当前环境有原生转写工具，优先使用，同时遵守本 Skill 的来源、临时文件和不确定性说明规则。
- 如果 `faster_whisper` 能成功 import，说明本地 Whisper 可用，不要再要求用户安装。
- 未检查选定执行运行时前，不得报告工具不可用。若先前运行时检查不完整，应先更正，再询问用户安装或配置。
- 如果必须从视频提取音频但 `ffmpeg` 不可用，先检查是否有其他媒体处理工具，再询问用户是否配置 ffmpeg。
- 如果外部语音转文字 API 可能需要压缩或切分音频，下载大媒体或调用 API 前先检查 `ffmpeg` 和 `ffprobe`。
- 只有上述检查失败或权限不足时，才询问安装、配置、切换模型或使用付费 API。

## 失败归因

当媒体理解无法完成时，报告已经验证过的具体阻塞原因。需要区分：

- AgentLens API 没有返回媒体，或没有返回直接媒体 URL；
- 媒体 URL 下载失败或已过期；
- 当前运行环境没有图片/视觉能力；
- 视频需要抽帧，但没有可用抽帧路径；
- 视频需要理解语音，但没有可用转写路径；
- 文件超过当前运行环境可处理范围；
- 缺少必要权限或凭据；
- 外部 API 或模型服务不可用。

除非当前运行环境的对应能力检查确实失败，不要说模型或运行时不能看图/看视频。如果问题是返回内容只有视频且尚未抽帧，应说抽帧或转写路径不可用/未完成，不要说图片读取被拦截。

可用 `ffmpeg` 时，音频提取命令如下：

```bash
ffmpeg -y -i /tmp/agentlens_{platform}_{timestamp}.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/agentlens_audio_{timestamp}.wav
```

## 理解图片内容

当用户询问图片内容，或内容来自图片主导平台且返回了图片 URL 时，读取并理解图片内容。

步骤：

1. 默认选择全部返回图片 URL。只有媒体无法下载、已失效，或数量/体积超出当前运行环境可处理范围时，才说明限制并询问是否分批处理、只处理部分媒体，或改为有限总结。
2. 将选中的图片下载到 `/tmp/agentlens_{platform}_{timestamp}_{index}.{ext}`。
3. 先确认当前运行环境是否能直接读取本地图片。
4. 如果有可用的原生视觉能力，用它读取本地图片内容。
5. 如果当前环境不能读取图片，不要假装已经看过图片。明确告诉用户当前环境无法直接理解图片，并提供选择：
   - 先基于正文、说明文案、字幕和来源信息做有限总结；
   - 如果当前 agent 已配置用户授权的多模态模型、图片读取工具或其他可看图的运行环境，询问是否切换过去处理；
   - 先保存图片 URL 或已下载文件名，方便之后查看。
6. 图片理解成功后，将视觉结论与 `text`、`title`、作者/来源和平台信息合并。
7. 回答时区分哪些信息来自图片理解，哪些来自正文或说明文案。

如果图片无法下载或无法读取，直接说明原因，并基于已有文本总结；不要猜测未读取图片的内容。

## 视频总结 SOP

当用户要求总结视频，但 AgentLens API 没有返回 `subtitle` 时，使用这个 SOP。

```text
Step 1：确认可用媒体
 -> 优先使用 media[].type == "audio"
 -> 没有 audio 时使用 media[].type == "video"
 -> 如果没有 audio/video URL：
      告诉用户 AgentLens API 没有返回可用于转写的媒体；
      只基于标题、正文和来源信息总结

Step 2：先确定转写路径，不要一上来让用户选安装/API
 -> 先完成上方“能力检查”
 -> 检查当前环境是否有原生转写或媒体处理工具
 -> 检查本地 faster-whisper 是否可用
 -> 如果可能需要从视频提取音频、压缩或切分音频，检查 ffmpeg/ffprobe
 -> 如果用户说某个转写工具已经装好，先验证；可用就直接用

Step 3：如果已有可用转写路径
 -> 只下载当前任务需要的 audio/video 到 /tmp/agentlens_*
 -> 必要时提取音频
 -> 如果使用 OpenAI Whisper 或其他有文件大小限制的语音转文字 API，上传前先检查音频文件大小
 -> 如果音频过大，先压缩并切成带少量重叠的小段，再按顺序转写
 -> 转写音频
 -> 结合转写文本、正文和来源信息总结
 -> 若在转写进行中已发送初稿，必须标注为“初稿”。转写完成后，主动交付一份使用逐字稿的整合最终答复，并明确初稿是被修正、补充，还是核验后无需修改。
 -> 使用分块转写时，把分块边界附近的重复或断句视为转写 artifacts
 -> 说明总结依据：转写文本、页面文案、画面理解，或它们的组合

Step 4：如果没有可用转写路径
 -> 下载大文件或消耗付费额度前，先询问用户：
    A) 使用或配置本地转写
    B) 使用已授权的语音转文字 API
    C) 不转写，只基于标题、正文和媒体元数据总结
 -> 用户选择 A 或 B 后，工具/key 可用时回到 Step 3
 -> 用户选择 C 或拒绝时，只总结已有信息，并说明没有口播转写
```

## 长时媒体任务

当下载、抽取或转写在发送中间答复后仍继续运行，必须保留任务状态，并在完成时主动告知用户，无需等待用户追问。完成答复必须包含用户请求的逐字稿或媒体结果与最终总结；若曾提供初稿，必须用已完成证据与其核对，不能留下两份可能不一致的总结。

没有可用转写路径时，可使用这段提示：

```text
AgentLens API 没有返回这个视频的字幕。要总结口播内容，需要先转写音频。
我检查了当前环境，暂时没有找到可直接使用的转写路径。

你可以选择：
A) 使用或配置本地转写
B) 使用已授权的语音转文字 API
C) 先不转写，只基于标题、文案和媒体元数据总结
你希望用哪种方式？
```

## 执行辅助代码

如果当前环境没有原生工具可以完成对应步骤，使用下面的辅助代码。代码只依赖标准库，方便 agent 根据当前运行环境做少量调整后执行。

### 媒体选择与下载

按当前任务选择媒体。对媒体主导内容的总结/分析，默认处理所有带直接 URL 的返回媒体；对窄任务，转写优先选直接音频，其次选视频，理解图片内容时只下载当前任务需要读取的图片。

```python
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

下载得到的本地路径可交给当前环境的图片理解或转写工具。如果下载失败，说明媒体理解/转写未完成，并基于已有文本、字幕或元数据继续；只有用户要求时再重试。

如果媒体项同时缺少 `source_url` 和 `cdn_url`，必须记录为 `media_url_missing`。不要把 `cover` 替代为原始媒体文件；它只能作为封面/缩略图证据。

### 音频提取

只有当选中的媒体是视频，且转写需要音频文件时才使用。若当前环境有原生媒体处理工具，优先用原生工具。

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

### 本地 Whisper

仅在 `python3 -c "import faster_whisper"` 成功，或用户同意安装/配置本地转写后使用。

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

### 语音转文字 API

仅当用户选择或已经批准使用外部语音转文字 API 时使用。默认文档化路径为 OpenAI 音频转写，因为本 Skill 元数据中声明了 `OPENAI_API_KEY`。如果当前环境已有可用的原生/本地转写路径，不要调用这个 API，除非用户明确偏好。

```python
import json
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

24MB 阈值是为了给 OpenAI 文档中的 25MB 文件上限留 buffer；如果服务商限制变化，以当前更低限制为准。分块转写可能在块边界附近重复或截断少量词句；总结时应把边界重复或突然断句视为转写 artifacts。

如果缺少 `OPENAI_API_KEY`，询问用户是否为本次转写提供 key、改用/配置本地转写，或只基于元数据总结。不要打印 key。

### 视频总结端到端模式

在 AgentLens API 结果已规范化、且没有 `subtitle` 时，可使用这个模式：

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

运行前仍必须先完成“视频总结 SOP”里的能力检查和用户授权。如果失败，说明失败步骤，并提供：重试、切换转写路径，或只基于元数据总结。

## 下载规则

- 只下载当前请求需要的媒体。
- 临时文件只使用 `/tmp/agentlens_*` 命名。
- 当前环境支持时，下载应设置超时。
- 不要使用 cookie、社交账号凭据或浏览器 session 获取媒体。
- 不要把 AgentLens API 返回的媒体 URL 当作长期归档链接。
- 批量删除临时文件前，先展示受影响文件并获得用户确认。

## 输出格式

文本和媒体结合总结时，建议使用：

```markdown
**摘要**
...

**视觉/媒体解读**
- ...

**转写说明**
- ...

**来源**
平台：...
作者/来源：...
```

没有执行图片/视频理解或视频转写时，不要暗示已经读取了媒体内容。明确说明回答基于 AgentLens API 返回的文本、字幕或元数据。
