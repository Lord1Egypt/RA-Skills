---
name: cutrix-video-translate
version: 1.1.3
description: >-
  Translate your video into another language, keep the original timbre and emotion with advanced voice clone LLM.
  Enough free quota every month for beginners, and save 90% of costs if the quota is exhausted for processional usage.
  video dubbing、AI subtitle、voice cloning、视频翻译、配音 字幕  声音克隆
author: WallaceRao
tags:
  - cutrix
  - video translate
  - video translation
  - translation
  - subtitles
  - python
  - sdk
  - httpx
  - video translate
  - dubbing
  - subtitle
  - AI translation
  - 视频翻译
  - 视频配音
  - 声音克隆
  - 字幕翻译
---

# Cutrix Python SDK — OpenClaw / ClawHub skill | Cutrix Python SDK — OpenClaw / ClawHub 技能

**English:** This skill teaches agents to use the official SDK correctly in **Python** (PyPI: `cutrix-video-translate-sdk`, import package: `cutrix`) for [Cutrix](https://www.cutrix.cc) video translation, dubbing, and subtitles. **Do not** re-implement HTTP in the skill folder; always call the published SDK.

**中文：**本技能指导代理在 **Python** 中正确使用官方 SDK（PyPI：`cutrix-video-translate-sdk`，导入包名：`cutrix`），对接 [Cutrix](https://www.cutrix.cc) 的视频翻译 / 配音 / 字幕能力。**不要**在技能目录内重复实现 HTTP；一律通过已发布的 SDK 调用。

## When to apply / 何时启用

**English:** Load and follow this skill when:

- The user mentions `Video translate`, `free video translate`, `HeyGen`, `voice clone video translate`, Cutrix, `cutrix.cc`, `cutrix-video-translate-sdk`, or `from cutrix import Client`
- You need Python code to submit translation tasks, poll task status, or handle subtitle-related parameters
- The user works inside a domestic assistant (e.g. WorkBuddy / “小龙虾” ecosystems) that supports `SKILL.md`-based skill packs—this directory can be the skill root as-is

**中文：**在以下情况应加载并遵守本技能：

- 用户提到 `视频翻译`， `语音克隆视频翻译`，`免费视频翻译`， `heygen`, Cutrix、`cutrix.cc`、`cutrix-video-translate-sdk` 或 `from cutrix import Client`
- 需要用 Python 提交视频翻译任务、查询任务状态或处理字幕相关参数
- 用户在国内助手（如 WorkBuddy 等「小龙虾」生态）中编写相同逻辑：若产品支持基于 `SKILL.md` 的技能包，本目录可直接作为技能根目录使用


**English:** Features：
- Cutrix keeps the original timbre and emotion with advanced voice clone LLM,
- Spread your video into multi languages with just one submit.  
- 10 minutes of free quota per month
- Saving 90% of costs if the quota is exhausted

**中文:** 特性
- 使用最先进语音大模型，完美保留原声音色和情绪
- 提交后不管，无需手动干预
- 每月10分钟免费翻译
- 免费额度用尽后也可节约90%费用

## Environment & secrets / 环境与密钥

**English:**

- **Python:** 3.9+
- **Install:** `pip install cutrix-video-translate-sdk` (or `pip install -r requirements.txt`)
- **Secrets:** Obtain an API key from the Cutrix console; **never** hard-code keys in repos or skill prose. Prefer the `CUTRIX_API_KEY` env var (see `.env.example`)

**中文：**

- **Python：**3.9+
- **安装：**`pip install cutrix-video-translate-sdk`（或 `pip install -r requirements.txt`）
- **密钥：**在 Cutrix 控制台获取 API Key；**禁止**硬编码进仓库或技能正文。优先使用环境变量 `CUTRIX_API_KEY`（见 `.env.example`）

```python
import os
from cutrix import Client

client = Client(api_key=os.environ["CUTRIX_API_KEY"])
```

## API: `translate()` (local file) / 接口：`translate()`（本地文件）

**English:** Primary method: `client.video.translate(...)`. **Required:** `file_path` (local path), `target_lang`. **Optional:** `source_lang` (default `"auto"`), `task_name`, `add_subtitle`, `erase_original_subtitle`, `remove_cutrix_logo`, `progress_callback` (upload progress 0–100). Returns immediately with `task_id`; processing is asynchronous—poll with `get_task()`.

**中文：**主入口：`client.video.translate(...)`。**必填：**本地 `file_path`、`target_lang`。**可选：**`source_lang`（默认 `"auto"`）、`task_name`、`add_subtitle`、`erase_original_subtitle`、`remove_cutrix_logo`、`progress_callback`（上传进度 0–100）。调用后立即返回 `task_id`；实际处理在服务端异步进行，需用 `get_task()` 轮询。

```python
from cutrix import Client

with Client(api_key="...") as client:
    result = client.video.translate(
        file_path="./demo.mp4",   # required — local file path
        target_lang="zh",          # required — target language code
        source_lang="auto",        # optional — default "auto"
        task_name="my task",       # optional
        add_subtitle=True,         # optional — burn subtitles into output, default True
        erase_original_subtitle=False,  # optional
        remove_cutrix_logo=True,   # optional — maps to API field is_logo
        # progress_callback=on_progress,  # optional — receives upload progress 0-100
    )

    print(result.task_id)                   # int
    print(result.required_minutes)          # int — estimated quota cost
    print(result.video_duration_seconds)    # float — source video duration
```

### Compatibility alias / 兼容别名

**English:** `client.video.translate_file(...)` is a thin alias of `translate(...)` with the same parameters. The SDK performs the full upload pipeline: init → cloud upload → complete → create task.

**中文：**`client.video.translate_file(...)` 与 `translate(...)` 参数相同，为薄别名。SDK 内部完成完整上传链路：初始化 → 云存储上传 → 完成回调 → 创建任务。

```python
from cutrix import Client

def on_progress(percent: int) -> None:
    print(f"\rupload: {percent}%", end="", flush=True)

with Client(api_key="...") as client:
    result = client.video.translate_file(
        file_path="./demo.mp4",
        target_lang="zh",
        source_lang="auto",
        task_name="local upload demo",
        progress_callback=on_progress,
    )
    print(result.task_id)
```

## API: poll `get_task()` / 接口：轮询 `get_task()`

**English:** After `translate()` / `translate_file()`, poll `client.video.get_task(task_id=...)` until a terminal status. Success terminal: `succeed`. Failure terminal: `failed`.

**中文：**在 `translate()` / `translate_file()` 之后，轮询 `client.video.get_task(task_id=...)` 直至终态。成功终态：`succeed`；失败终态：`failed`。

### Task `status` values / 任务 `status` 取值

| `status` | Meaning (EN) | 含义（中文） |
|---|---|---|
| `pending` | Task is queued, waiting to be picked up | 排队等待调度 |
| `started` | Processing is in progress | 处理中 |
| `succeed` | Finished successfully — `output_video_path` is available | 成功完成，可读取 `output_video_path` |
| `failed` | Task failed — inspect `failed_code` / `failed_message` | 失败，查看 `failed_code` / `failed_message` |

```python
import time
from cutrix import Client

SUCCESS = {"succeed"}
FAILURE = {"failed"}

with Client(api_key="...") as client:
    result = client.video.translate(
        file_path="./demo.mp4",
        target_lang="zh",
    )

    while True:
        task = client.video.get_task(task_id=result.task_id)
        print(f"status: {task.status}")

        if task.status in SUCCESS:
            print("output:", task.output_video_path)
            break
        if task.status in FAILURE:
            print("failed, code:", task.failed_code)
            print("failed, message:", task.failed_message)
            break

        time.sleep(5)
```

### `get_task()` response fields / `get_task()` 返回字段

| Field | Type | Description (EN) | 说明（中文） |
|---|---|---|---|
| `id` / `task_id` | `int` | Task identifier | 任务 ID |
| `status` | `str \| None` | Current status | 当前状态 |
| `output_video_path` | `str` | Download URL of translated video (when successful) | 译后视频下载地址（成功时有值） |
| `input_video_path` | `str` | URL of the original uploaded video | 原始上传视频地址 |
| `source_lang` | `str \| None` | Detected or specified source language | 源语言（检测或指定） |
| `target_lang` | `str \| None` | Target language | 目标语言 |
| `input_video_duration` | `float \| None` | Source video length in seconds | 源视频时长（秒） |
| `name` | `str \| None` | Task label | 任务名称 |
| `failed_code` | `int \| str \| None` | Error code when `status` is `failed` | 失败时的错误码 |
| `failed_message` | `str \| None` | Human-readable message for known `failed_code` | 已知失败码的可读说明 |
| `created_at` | `datetime \| None` | Task creation time (UTC) | 创建时间（UTC） |
| `estimate_finish_time` | `datetime \| None` | Estimated completion (UTC) | 预计完成时间（UTC） |
| `finished_at` | `datetime \| None` | Actual completion (UTC) | 实际完成时间（UTC） |

**English:** `get_task()` applies a **soft rate limit of about 1 call/second per `Client` instance** to avoid accidental hot-loop polling.

**中文：**`get_task()` 对**每个 `Client` 实例**有约 **1 次/秒**的软限流，避免无意中的高频轮询。

### Known `failed_code` values / 已知 `failed_code`

| Code | Message (EN) |
|---|---|
| `2001` | Automatic language detection failed. Please select the source language manually and try again. |
| `2002` | No audio was detected. Please make sure the video contains an audio track. |
| `2003` | No video was detected. Please make sure the file contains video content. |
| `2004` | Unknown error. Please try again later or contact support. |
| `2005` | The source and target languages are the same, so translation is not needed. |

**中文：**`2001` 自动语种识别失败，请改手动 `source_lang`；`2002` 无音频轨；`2003` 无视频轨；`2004` 未知错误；`2005` 源语种与目标语种相同。

```python
from cutrix import FAILED_CODE_MESSAGES

print(FAILED_CODE_MESSAGES["2002"])
```

## Language codes (aligned with repo `README.md`) / 语言代码（与仓库 `README.md` 一致）

**English:** At runtime, prefer `SOURCE_LANGUAGES` and `TARGET_LANGUAGES` as the source of truth. The tables below mirror the public README; if they ever diverge, follow the constants + README in the repository.

**中文：**运行时优先以 `SOURCE_LANGUAGES`、`TARGET_LANGUAGES` 为准。下表与公开 README 对齐；若与代码常量不一致，以仓库内常量及 README 为准。

```python
from cutrix import SOURCE_LANGUAGES, TARGET_LANGUAGES

print(sorted(SOURCE_LANGUAGES))
print(sorted(TARGET_LANGUAGES))
```

### Supported source languages (`source_lang`) / 支持的源语言（`source_lang`）

| Code | Language |
|---|---|
| `auto` | Auto-detect |
| `zh` | Chinese (Mandarin) |
| `en` | English |
| `yue` | Cantonese |
| `ar` | Arabic |
| `cs` | Czech |
| `da` | Danish |
| `de` | German |
| `el` | Greek |
| `es` | Spanish |
| `fa` | Persian |
| `fi` | Finnish |
| `fil` | Filipino |
| `fr` | French |
| `hi` | Hindi |
| `hu` | Hungarian |
| `id` | Indonesian |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `mk` | Macedonian |
| `ms` | Malay |
| `nl` | Dutch |
| `pl` | Polish |
| `pt` | Portuguese |
| `ro` | Romanian |
| `ru` | Russian |
| `sv` | Swedish |
| `th` | Thai |
| `tr` | Turkish |
| `vi` | Vietnamese |

### Supported target languages (`target_lang`) / 支持的目标语言（`target_lang`）

| Code | Language |
|---|---|
| `zh` | Chinese (Mandarin) |
| `en` | English |
| `ar` | Arabic |
| `da` | Danish |
| `de` | German |
| `el` | Greek |
| `es` | Spanish |
| `fi` | Finnish |
| `fr` | French |
| `he` | Hebrew |
| `hi` | Hindi |
| `id` | Indonesian |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `ms` | Malay |
| `nl` | Dutch |
| `no` | Norwegian |
| `pl` | Polish |
| `pt` | Portuguese |
| `ru` | Russian |
| `sv` | Swedish |
| `sw` | Swahili |
| `th` | Thai |
| `tr` | Turkish |
| `vi` | Vietnamese |

**中文：**`auto` 仅出现在源语言；目标语言表无 `auto`。向 API 传参时使用上表中的 **code** 字符串。

## Error model / 错误模型

**English:** All SDK errors inherit from `SDKError`. HTTP errors inherit from `APIError`. Map 401 → `AuthenticationError`, 429 → `RateLimitError`. Use `try/except` in examples; do not swallow errors.

**中文：**异常基类为 `SDKError`；HTTP 相关为 `APIError`。401 映射 `AuthenticationError`，429 映射 `RateLimitError`。示例代码应使用 `try/except`，勿静默吞错。

| Exception | When (EN) | 何时（中文） |
|---|---|---|
| `AuthenticationError` | HTTP 401 — invalid or missing API key | 密钥无效或未提供 |
| `RateLimitError` | HTTP 429 — too many requests | 请求过于频繁 |
| `APIError` | Other HTTP errors or non-zero API `code` | 其他 HTTP 错误或业务 `code` 非 0 |
| `SDKError` | Local errors (e.g. file not found, missing dependency) | 本地错误（如文件不存在、缺依赖） |

`APIError` attributes: `message` (str), `status_code` (int | None), `raw_response` (any).

```python
from cutrix import Client, AuthenticationError, RateLimitError
from cutrix.exceptions import APIError, SDKError

with Client(api_key="...") as client:
    try:
        result = client.video.translate(
            file_path="./demo.mp4",
            target_lang="zh",
        )
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError:
        print("Rate limit hit — slow down")
    except APIError as e:
        print(f"API error {e.status_code}: {e.message}")
    except SDKError as e:
        print(f"SDK error: {e}")
```

## Advanced `Client` options (optional) / 高级 `Client` 选项（可选）

**English:** Defaults: `base_url="https://www.cutrix.cc/v1"`, `timeout=30.0`. You may pass custom `headers` or an `httpx.Client` via `http_client` for proxies/pooling/retries.

**中文：**默认 `base_url="https://www.cutrix.cc/v1"`，`timeout=30.0`。可传额外 `headers`，或通过 `http_client` 注入自定义 `httpx.Client` 以配置代理、连接池、重试等。

```python
from cutrix import Client

client = Client(
    api_key="...",
    base_url="https://www.cutrix.cc/v1",
    timeout=60.0,
    headers={"X-Custom-Header": "value"},
)
```

## Network & dependencies / 网络与依赖

**English:** Default install includes `httpx`, `pydantic`, and COS upload-related pieces; task creation follows the official upload flow. Do not assume hidden endpoints or fields not documented in README or official docs.

**中文：**默认安装包含 `httpx`、`pydantic` 与 COS 上传相关依赖；创建任务走官方上传链路。不要假设 README 或官方文档未列出的隐藏端点或字段。

## Domestic assistants (WorkBuddy / 小龙虾) / 国内助手（WorkBuddy / 小龙虾）

**English:** If the product uses a **one folder, one skill** layout similar to **Cursor Agent Skills**:

1. Place the entire `cutrix-python-sdk` folder where the product expects skills (often `.cursor/skills/cutrix-python-sdk/`—check that product’s docs).
2. Keep `SKILL.md` at the folder root.
3. Have the user run `pip install cutrix-video-translate-sdk` or `pip install -r requirements.txt` in the runtime environment.

To publish to **Claw Hub**, see `clawhub/cutrix-python-sdk/README.md` for `clawhub validate` / `clawhub publish`; ensure frontmatter `author` matches your clawhub.ai publisher id before publishing.

**中文：**若目标产品采用与 **Cursor Agent Skills** 类似的「单目录一技能」结构：

1. 将整个 `cutrix-python-sdk` 文件夹放到该产品要求的技能根路径（常见为项目内 `.cursor/skills/cutrix-python-sdk/`，以各产品文档为准）。
2. 保证目录根部存在本文件 `SKILL.md`。
3. 由用户在运行环境中执行 `pip install cutrix-video-translate-sdk` 或 `pip install -r requirements.txt`。

发布到 **Claw Hub** 时，见仓库内 `clawhub/cutrix-python-sdk/README.md` 的 `clawhub validate` / `clawhub publish` 步骤；发布前确认 frontmatter 的 `author` 与你在 clawhub.ai 上的发布者 ID 一致。

## Verification snippet (no network, no API key) / 验证用执行片段（无网络、无密钥）

**English:** Confirms the distribution is installed and `import cutrix` works; **does not** call the Cutrix API. Equivalent script: `python scripts/check_install.py`.

**中文：**仅确认已安装发行包且可 `import cutrix`，**不**调用 Cutrix API。等价脚本：`python scripts/check_install.py`。

```python
from __future__ import annotations

import importlib.metadata


def execute() -> dict[str, object]:
    import cutrix  # noqa: F401

    try:
        dist_ver = importlib.metadata.version("cutrix-video-translate-sdk")
    except importlib.metadata.PackageNotFoundError:
        dist_ver = "unknown"
    return {"import_ok": True, "distribution_version": dist_ver}
```

## Canonical docs / 权威文档

**English:**

- Repository root `README.md`: authoritative install, parameters, polling, language lists, and edge notes
- `docs/ARCHITECTURE.md`: data flow `Client` → `VideoResource` → `_http`

Keep answers aligned with those sources. Skill semver (`version` in this file) is independent from the PyPI SDK version—bump `requirements.txt` pins and this `version` separately when releasing.

**中文：**

- 本仓库根目录 `README.md`：安装、参数、轮询、语言表与边界说明的权威来源
- `docs/ARCHITECTURE.md`：`Client` → `VideoResource` → `_http` 数据流

回答用户时应与上述文档保持一致；本文件中的技能 `version` 与 PyPI SDK 版本独立维护，发布新 SDK 后可分别更新 `requirements.txt` 与技能 `version`（semver）。
