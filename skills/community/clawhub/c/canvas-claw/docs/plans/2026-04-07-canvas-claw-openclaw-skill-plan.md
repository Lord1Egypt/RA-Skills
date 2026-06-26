# Canvas Claw OpenClaw Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a new OpenClaw skill package in `/Users/apple/bangongziliao/hebing/canvas-claw` that talks to `AI-video-agent` over HTTP and supports four phase-one capabilities: image create, image remix, video create, and video animate.

**Architecture:** The skill will be a standalone Python package with thin CLI wrappers under `scripts/`. Shared modules will handle auth, model selection, media upload, task submission, polling, downloads, and metadata writing. The skill will use `AI-video-agent` endpoints `/api/login`, `/api/models`, `/api/assets/materialize-binary`, and `/api/tasks`.

**Tech Stack:** Python 3, `urllib` or `httpx`, `pytest`, OpenClaw skill metadata, local CLI scripts.

---

### Task 1: Scaffold The Package Layout

**Files:**
- Create: `./pyproject.toml`
- Create: `./SKILL.md`
- Create: `./INSTALL.md`
- Create: `./canvas_claw/__init__.py`
- Create: `./canvas_claw/errors.py`
- Create: `./tests/__init__.py`

**Step 1: Write the failing test**

Create `./tests/test_package_layout.py` with:

```python
from pathlib import Path


def test_project_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "pyproject.toml").exists()
    assert (root / "SKILL.md").exists()
    assert (root / "INSTALL.md").exists()
    assert (root / "canvas_claw" / "__init__.py").exists()
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_package_layout.py -v
```

Expected: FAIL because the package files do not exist yet.

**Step 3: Write minimal implementation**

- Add `pyproject.toml` with package metadata and `pytest` test config.
- Add empty `canvas_claw/__init__.py`.
- Add `canvas_claw/errors.py` with a base `CanvasClawError`.
- Add placeholder `SKILL.md` and `INSTALL.md` sections.

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_package_layout.py -v
```

Expected: PASS.

**Step 5: Commit**

If this directory has a git repo:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add pyproject.toml SKILL.md INSTALL.md canvas_claw/__init__.py canvas_claw/errors.py tests/__init__.py tests/test_package_layout.py && git commit -m "chore: scaffold canvas-claw package"
```

### Task 2: Add Runtime Config And HTTP Client

**Files:**
- Create: `./canvas_claw/config.py`
- Create: `./canvas_claw/client.py`
- Create: `./tests/test_auth.py`

**Step 1: Write the failing test**

Create `./tests/test_auth.py` with:

```python
from canvas_claw.config import RuntimeConfig


def test_runtime_config_requires_base_url_and_site_id() -> None:
    config = RuntimeConfig(
        base_url="http://localhost:8000",
        token="token-123",
        site_id=10000,
    )
    assert config.base_url == "http://localhost:8000"
    assert config.token == "token-123"
    assert config.site_id == 10000
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_auth.py -v
```

Expected: FAIL because `RuntimeConfig` does not exist.

**Step 3: Write minimal implementation**

- Add `RuntimeConfig` dataclass to `config.py`.
- Add `CanvasClawClient` to `client.py` with:
  - `_build_headers()`
  - `login()`
  - `list_models()`
  - `create_task()`
  - `get_task()`
  - `materialize_binary()`

Prefer a single request helper:

```python
def request_json(self, method: str, path: str, *, data: bytes | None = None, headers: dict[str, str] | None = None) -> dict:
    ...
```

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_auth.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add canvas_claw/config.py canvas_claw/client.py tests/test_auth.py && git commit -m "feat: add runtime config and api client"
```

### Task 3: Build The Model Registry And Selection Rules

**Files:**
- Create: `./canvas_claw/model_registry.py`
- Create: `./tests/test_model_registry.py`

**Step 1: Write the failing test**

Create `./tests/test_model_registry.py` with:

```python
from canvas_claw.model_registry import resolve_model


def test_resolve_default_text_to_image_model() -> None:
    model = resolve_model(capability="image-create", catalog_key=None)
    assert model.catalog_key == "image-plus"
    assert model.provider == "vg"
    assert model.model_id == "qwen-image-2"
    assert model.task_type == "text_to_image"
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_model_registry.py -v
```

Expected: FAIL because `resolve_model` does not exist.

**Step 3: Write minimal implementation**

In `model_registry.py`, create:

- `ModelSpec` dataclass
- `IMAGE_MODEL_SPECS`
- `VIDEO_MODEL_SPECS`
- `resolve_model(capability, catalog_key=None)`
- `list_models_for_capability(capability)`

Initial registry entries:

```python
ModelSpec("image-plus", "vg", "qwen-image-2", "text_to_image")
ModelSpec("image-multi", "vg", "nano-banana-2", "image_to_image")
ModelSpec("video-dream-standard", "vg", "seedance-1-5-pro", "text_to_video")
ModelSpec("video-dream-standard", "vg", "seedance-1-5-pro", "image_to_video")
```

Also add phase-one supported options per model, for example:

- image: `aspect_ratio`, `resolution`
- video: `aspect_ratio`, `resolution`, `duration`, `sound`

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_model_registry.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add canvas_claw/model_registry.py tests/test_model_registry.py && git commit -m "feat: add model registry for phase one capabilities"
```

### Task 4: Implement Local File And URL Media Resolution

**Files:**
- Create: `./canvas_claw/media.py`
- Create: `./tests/test_media.py`

**Step 1: Write the failing test**

Create `./tests/test_media.py` with:

```python
from pathlib import Path

from canvas_claw.media import classify_media_input


def test_classify_local_path(tmp_path: Path) -> None:
    path = tmp_path / "frame.png"
    path.write_bytes(b"fake")
    result = classify_media_input(str(path))
    assert result.kind == "file"
    assert result.path == path
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_media.py -v
```

Expected: FAIL because media helpers do not exist.

**Step 3: Write minimal implementation**

In `media.py`, add:

- `ResolvedMediaInput` dataclass
- `classify_media_input(raw: str)`
- `materialize_input(client, raw: str, media_type: str)`
- `materialize_many(client, values: list[str], media_type: str)`

Rules:

- `http://` or `https://` => return as remote URL
- existing local path => upload bytes through `client.materialize_binary(...)`
- anything else => raise `CanvasClawError`

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_media.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add canvas_claw/media.py tests/test_media.py && git commit -m "feat: add media input materialization helpers"
```

### Task 5: Implement Task Submission, Polling, And Normalized Results

**Files:**
- Create: `./canvas_claw/tasks.py`
- Create: `./tests/test_task_runner.py`

**Step 1: Write the failing test**

Create `./tests/test_task_runner.py` with:

```python
from canvas_claw.tasks import build_image_request


def test_build_text_to_image_request() -> None:
    payload = build_image_request(
        prompt="a red fox",
        capability="image-create",
        provider="vg",
        model_id="qwen-image-2",
        image_urls=[],
        aspect_ratio="1:1",
        resolution="2K",
    )
    assert payload["type"] == "text_to_image"
    assert payload["input"]["prompt"] == "a red fox"
    assert payload["input"]["image_urls"] == []
    assert payload["options"]["aspect_ratio"] == "1:1"
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_task_runner.py -v
```

Expected: FAIL because `build_image_request` does not exist.

**Step 3: Write minimal implementation**

Add to `tasks.py`:

- `build_image_request(...)`
- `build_video_request(...)`
- `submit_and_poll(...)`
- `poll_until_terminal(...)`
- `normalize_task_result(...)`

Polling rules:

- status `queued` or `running` => sleep `poll_interval`
- status `failed` => raise `CanvasClawError`
- status `succeeded` => return normalized result dict

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_task_runner.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add canvas_claw/tasks.py tests/test_task_runner.py && git commit -m "feat: add task payload builders and polling"
```

### Task 6: Implement Output Downloading And Metadata Writing

**Files:**
- Create: `./canvas_claw/download.py`
- Create: `./canvas_claw/output.py`
- Create: `./tests/test_output.py`

**Step 1: Write the failing test**

Create `./tests/test_output.py` with:

```python
import json
from pathlib import Path

from canvas_claw.output import write_metadata


def test_write_metadata(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    metadata_path = write_metadata(
        output_dir=output_dir,
        payload={"task_id": "123", "status": "succeeded"},
    )
    assert metadata_path.exists()
    data = json.loads(metadata_path.read_text())
    assert data["task_id"] == "123"
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_output.py -v
```

Expected: FAIL because `write_metadata` does not exist.

**Step 3: Write minimal implementation**

Add:

- `download_url(url, destination)`
- `download_many(urls, output_dir, kind)`
- `write_metadata(output_dir, payload)`
- `save_result_bundle(output_dir, result, kind)`

Image file naming:

- `image_1.jpg`
- `image_2.jpg`

Video file naming:

- single result: `video.mp4`
- multi result: `video_1.mp4`

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_output.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add canvas_claw/download.py canvas_claw/output.py tests/test_output.py && git commit -m "feat: add output download and metadata writing"
```

### Task 7: Implement `generate_image.py` For Image Create And Image Remix

**Files:**
- Create: `./scripts/generate_image.py`
- Create: `./tests/test_generate_image_cli.py`

**Step 1: Write the failing test**

Create `./tests/test_generate_image_cli.py` with:

```python
from canvas_claw.tasks import build_image_request


def test_reference_images_switch_to_image_to_image() -> None:
    payload = build_image_request(
        prompt="portrait",
        capability="image-remix",
        provider="vg",
        model_id="nano-banana-2",
        image_urls=["https://example.com/ref.png"],
        aspect_ratio="3:4",
        resolution="2K",
    )
    assert payload["type"] == "image_to_image"
    assert payload["input"]["image_urls"] == ["https://example.com/ref.png"]
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_generate_image_cli.py -v
```

Expected: FAIL until the CLI wiring and payload logic exist together.

**Step 3: Write minimal implementation**

Implement `scripts/generate_image.py` with:

- argument parsing
- config loading
- model resolution
- reference image materialization
- image task payload creation
- task polling
- output bundle writing

Suggested CLI surface:

```bash
python3 scripts/generate_image.py \
  --prompt "cinematic portrait" \
  --catalog-key "image-plus" \
  --aspect-ratio "3:4" \
  --resolution "2K"
```

Reference mode:

```bash
python3 scripts/generate_image.py \
  --prompt "same character, winter coat" \
  --reference-image "/tmp/char.png" \
  --catalog-key "image-multi"
```

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_generate_image_cli.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add scripts/generate_image.py tests/test_generate_image_cli.py canvas_claw/tasks.py canvas_claw/media.py canvas_claw/output.py && git commit -m "feat: add image generation cli"
```

### Task 8: Implement `generate_video.py` For Video Create And Video Animate

**Files:**
- Create: `./scripts/generate_video.py`
- Create: `./tests/test_generate_video_cli.py`

**Step 1: Write the failing test**

Create `./tests/test_generate_video_cli.py` with:

```python
from canvas_claw.tasks import build_video_request


def test_first_frame_switches_to_image_to_video() -> None:
    payload = build_video_request(
        prompt="slow camera push",
        capability="video-animate",
        provider="vg",
        model_id="seedance-1-5-pro",
        image_urls=["https://example.com/frame.png"],
        aspect_ratio="16:9",
        resolution="720p",
        duration=8,
        generate_audio=True,
    )
    assert payload["type"] == "image_to_video"
    assert payload["options"]["sound"] is True
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_generate_video_cli.py -v
```

Expected: FAIL before the CLI and task builder are complete.

**Step 3: Write minimal implementation**

Implement `scripts/generate_video.py` with:

- text-to-video mode when there is no `--first-frame`
- image-to-video mode when `--first-frame` is present
- support:
  - `--catalog-key`
  - `--aspect-ratio`
  - `--resolution`
  - `--duration`
  - `--generate-audio`
  - `--output-dir`

Suggested command:

```bash
python3 scripts/generate_video.py \
  --prompt "a rainy city street, cinematic" \
  --catalog-key "video-dream-standard" \
  --resolution "720p" \
  --duration "8"
```

Image-to-video command:

```bash
python3 scripts/generate_video.py \
  --prompt "the character turns and smiles" \
  --first-frame "/tmp/frame.png" \
  --catalog-key "video-dream-standard"
```

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_generate_video_cli.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add scripts/generate_video.py tests/test_generate_video_cli.py canvas_claw/tasks.py canvas_claw/media.py canvas_claw/output.py && git commit -m "feat: add video generation cli"
```

### Task 9: Implement Model Listing CLIs

**Files:**
- Create: `./scripts/image_models.py`
- Create: `./scripts/video_models.py`
- Create: `./tests/test_models_cli.py`

**Step 1: Write the failing test**

Create `./tests/test_models_cli.py` with:

```python
from canvas_claw.model_registry import list_models_for_capability


def test_image_models_are_filtered() -> None:
    models = list_models_for_capability("image-create")
    assert any(model.catalog_key == "image-plus" for model in models)
    assert all(model.task_type in {"text_to_image", "image_to_image"} for model in models)
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_models_cli.py -v
```

Expected: FAIL until the registry listing helpers are finished.

**Step 3: Write minimal implementation**

Implement:

- `scripts/image_models.py`
- `scripts/video_models.py`

Each script should:

- read the local registry
- optionally cross-check `/api/models`
- print `catalog_key`, `provider`, `model_id`, `task_type`, and default hints

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_models_cli.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add scripts/image_models.py scripts/video_models.py tests/test_models_cli.py canvas_claw/model_registry.py && git commit -m "feat: add model listing commands"
```

### Task 10: Finalize SKILL.md And INSTALL.md For OpenClaw

**Files:**
- Modify: `./SKILL.md`
- Modify: `./INSTALL.md`
- Create: `./tests/test_skill_docs.py`

**Step 1: Write the failing test**

Create `./tests/test_skill_docs.py` with:

```python
from pathlib import Path


def test_skill_metadata_mentions_canvas_agent_env() -> None:
    skill = Path(__file__).resolve().parents[1] / "SKILL.md"
    text = skill.read_text()
    assert "AI_VIDEO_AGENT_TOKEN" in text
    assert "generate_image.py" in text
    assert "generate_video.py" in text
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_skill_docs.py -v
```

Expected: FAIL because the docs are still placeholders.

**Step 3: Write minimal implementation**

Update `SKILL.md` to include:

- new skill name and description
- OpenClaw metadata:
  - `bins: ["python3"]`
  - required env: `AI_VIDEO_AGENT_BASE_URL`, `AI_VIDEO_AGENT_TOKEN`, `AI_VIDEO_AGENT_SITE_ID`
  - primary env: `AI_VIDEO_AGENT_TOKEN`
- four clean capability names
- examples for each command

Update `INSTALL.md` to include:

- required env vars
- login helper usage
- image and video generation examples
- model list examples
- troubleshooting

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest tests/test_skill_docs.py -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add SKILL.md INSTALL.md tests/test_skill_docs.py && git commit -m "docs: finalize openclaw skill docs"
```

### Task 11: Run The Full Local Test Suite

**Files:**
- No file changes required unless tests fail

**Step 1: Run the full test suite**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && pytest -v
```

Expected: all tests PASS.

**Step 2: Fix any failures**

- If failures are isolated, patch only the relevant module.
- Re-run the narrow failing test first.
- Re-run the full suite after fixes.

**Step 3: Smoke-test the commands**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && python3 scripts/image_models.py
cd /Users/apple/bangongziliao/hebing/canvas-claw && python3 scripts/video_models.py
```

If a local `AI-video-agent` instance is available and env vars are configured, also run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && python3 scripts/generate_image.py --prompt "test image" --catalog-key "image-plus"
cd /Users/apple/bangongziliao/hebing/canvas-claw && python3 scripts/generate_video.py --prompt "test video" --catalog-key "video-dream-standard" --duration "8"
```

Expected:

- model list commands print valid models
- generate commands create `./output/metadata.json`

**Step 4: Commit**

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && git add -A && git commit -m "test: verify canvas-claw phase one flows"
```

### Task 12: Optional Publish Preparation

**Files:**
- Create later if publishing: `./_meta.json`

**Step 1: Keep local-only by default**

- Do not create `_meta.json` until the skill is ready for ClawHub publishing.

**Step 2: If publishing is needed**

- add `_meta.json`
- verify naming, slug, and release metadata
- manually validate from an OpenClaw installation path

**Step 3: Final verification**

Run:

```bash
cd /Users/apple/bangongziliao/hebing/canvas-claw && find . -maxdepth 3 -type f | sort
```

Expected: package layout matches the design doc.

## Notes For Execution

- This directory is currently not a git repository, so commit steps are conditional. If version history matters, initialize git before implementation.
- Do not copy any existing `neo-ai-1.0.1` file verbatim. Rebuild the new package around `AI-video-agent` contracts only.
- Keep phase one narrow: no `batch_video.py`, no `motion_control.py`, no universal multi-modal pipeline.

Plan complete and saved to `docs/plans/2026-04-07-canvas-claw-openclaw-skill-plan.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
