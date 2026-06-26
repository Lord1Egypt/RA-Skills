# Xiaoyuzhou Podcast Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 podcast pipeline 中新增 `platform: "xiaoyuzhou"`，通过 OpenCLI 抓取小宇宙节目列表和可选转录文本。

**Architecture:** 小宇宙仍是 `type: "podcast"` 的一个 platform，不新增 source layer。`scripts/fetch-podcast.py` 负责从小宇宙 URL 提取 podcast id、调用 `opencli xiaoyuzhou` JSON 命令、归一化 episode，并复用现有 `transcript_status` 合同。schema、validator 和 config editor 只同步枚举，不把小宇宙逻辑扩散到 merge/digest。

**Tech Stack:** Python 3.8+ standard library, `unittest`, `unittest.mock`, JSON Schema draft-07, vanilla JavaScript config editor, OpenCLI subprocess backend.

---

## File Structure

- `scripts/fetch-podcast.py`
  - 新增小宇宙 platform 推断、URL id 解析、OpenCLI JSON subprocess helper、metadata fetch 和 transcript enrich。
  - 保持 RSS / YouTube 现有函数不重构。

- `config/schema.json`
  - 扩展 podcast `platform` 和 `transcript.backend` 枚举。

- `scripts/validate-config.py`
  - 同步 schema 外的手写校验枚举。

- `tools/config-editor/server.py`
  - 同步后端保存校验枚举。

- `tools/config-editor/app.js`
  - 同步表格 dropdown 枚举。

- `tools/config-editor/README.md`
  - 同步编辑器说明。

- `tests/test_fetch_podcast.py`
  - 增加小宇宙平台推断、URL 解析、OpenCLI helper、metadata normalization、source error、transcript success/failure 的 mock 测试。

- `tests/test_config.py`
  - 增加 validator 接受小宇宙 platform 和 opencli transcript backend 的测试。

- `tests/test_config_editor_server.py`
  - 增加 config editor server 接受新枚举的测试。

---

### Task 1: Config Enum Support

**Files:**
- Modify: `tests/test_config.py`
- Modify: `tests/test_config_editor_server.py`
- Modify: `config/schema.json`
- Modify: `scripts/validate-config.py`
- Modify: `tools/config-editor/server.py`
- Modify: `tools/config-editor/app.js`
- Modify: `tools/config-editor/README.md`

- [ ] **Step 1: Write failing config validator tests**

Add these methods to `TestPodcastConfigValidation` in `tests/test_config.py`:

```python
    def test_validate_source_types_accepts_xiaoyuzhou_platform(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    id="whynottv-podcast",
                    url="https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
                    platform="xiaoyuzhou",
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))

    def test_validate_source_types_accepts_opencli_transcript_backend(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    platform="xiaoyuzhou",
                    transcript={
                        "enabled": True,
                        "backend": "opencli",
                    },
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))
```

- [ ] **Step 2: Write failing config editor server test**

In `tests/test_config_editor_server.py`, update `test_post_accepts_podcast_source_on_save` so `payload_source` uses Xiaoyuzhou values:

```python
            payload_source = {
                "sources": [
                    {
                        "id": "whynottv-podcast",
                        "type": "podcast",
                        "name": "WhynotTV Podcast",
                        "enabled": True,
                        "priority": True,
                        "topics": ["podcast"],
                        "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
                        "platform": "xiaoyuzhou",
                        "transcript": {
                            "enabled": True,
                            "backend": "opencli",
                            "languages": [],
                        },
                    }
                ]
            }
```

Also update the saved assertions in that test:

```python
                    self.assertEqual(saved["sources"][0]["type"], "podcast")
                    self.assertEqual(saved["sources"][0]["platform"], "xiaoyuzhou")
                    self.assertEqual(saved["sources"][0]["transcript"]["backend"], "opencli")
```

- [ ] **Step 3: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_config.TestPodcastConfigValidation.test_validate_source_types_accepts_xiaoyuzhou_platform tests.test_config.TestPodcastConfigValidation.test_validate_source_types_accepts_opencli_transcript_backend tests.test_config_editor_server.TestConfigEditorServer.test_post_accepts_podcast_source_on_save -v
```

Expected: FAIL because `xiaoyuzhou` and `opencli` are not accepted yet.

- [ ] **Step 4: Update config schema enums**

In `config/schema.json`, change the `platform` enum to:

```json
          "enum": ["auto", "rss", "youtube", "xiaoyuzhou"],
```

Change the `transcript.backend` enum to:

```json
              "enum": ["auto", "yt-dlp", "opencli"],
```

- [ ] **Step 5: Update script validator enums**

In `scripts/validate-config.py`, update the podcast platform check:

```python
            if platform not in {"auto", "rss", "youtube", "xiaoyuzhou"}:
                errors.append(
                    f"Podcast source '{source_id}' has invalid platform: {platform}"
                )
```

Update the transcript backend check:

```python
                    if backend not in {"auto", "yt-dlp", "opencli"}:
                        errors.append(
                            f"Podcast source '{source_id}' has invalid transcript backend: {backend}"
                        )
```

- [ ] **Step 6: Update config editor enums**

In `tools/config-editor/server.py`, update constants near the top:

```python
    _ALLOWED_PODCAST_PLATFORMS = {"auto", "rss", "youtube", "xiaoyuzhou"}
    _ALLOWED_TRANSCRIPT_BACKENDS = {"auto", "yt-dlp", "opencli"}
```

In `tools/config-editor/app.js`, update constants:

```javascript
  const PODCAST_PLATFORMS = ["auto", "rss", "youtube", "xiaoyuzhou"];
  const PODCAST_TRANSCRIPT_BACKENDS = ["auto", "yt-dlp", "opencli"];
```

- [ ] **Step 7: Update config editor README**

In `tools/config-editor/README.md`, update the podcast field list:

```markdown
- 表格模式额外支持 `type: "podcast"` 的字段：
  - `platform`（可选）：`auto` / `rss` / `youtube` / `xiaoyuzhou`
  - `transcript.enabled`（可选）：布尔值
  - `transcript.backend`（可选）：`auto` / `yt-dlp` / `opencli`
  - `transcript.languages`（可选）：字符串数组
```

- [ ] **Step 8: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests.test_config.TestPodcastConfigValidation tests.test_config_editor_server.TestConfigEditorServer.test_post_accepts_podcast_source_on_save -v
```

Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add config/schema.json scripts/validate-config.py tools/config-editor/server.py tools/config-editor/app.js tools/config-editor/README.md tests/test_config.py tests/test_config_editor_server.py
git commit -m "feat: allow xiaoyuzhou podcast config"
```

---

### Task 2: Xiaoyuzhou Platform Inference and URL Parsing

**Files:**
- Modify: `tests/test_fetch_podcast.py`
- Modify: `scripts/fetch-podcast.py`

- [ ] **Step 1: Write failing platform inference and URL parsing tests**

In `TestPodcastPlatformInference` in `tests/test_fetch_podcast.py`, add:

```python
    def test_infers_xiaoyuzhou_platform(self):
        self.assertEqual(
            fetch_podcast.infer_platform("https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"),
            "xiaoyuzhou",
        )
        self.assertEqual(
            fetch_podcast.infer_platform("https://xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"),
            "xiaoyuzhou",
        )

    def test_extracts_xiaoyuzhou_podcast_id(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"
            ),
            "686a1832222ae2de21fea940",
        )

    def test_extract_xiaoyuzhou_podcast_id_rejects_non_podcast_url(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc"
            ),
            "",
        )
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestPodcastPlatformInference -v
```

Expected: FAIL with missing `extract_xiaoyuzhou_podcast_id` and incorrect platform inference.

- [ ] **Step 3: Implement platform inference helpers**

In `scripts/fetch-podcast.py`, add this constant near the other top-level constants:

```python
XIAOYUZHOU_HOSTS = {"xiaoyuzhoufm.com", "www.xiaoyuzhoufm.com"}
```

Replace `infer_platform` with:

```python
def infer_platform(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}:
        return "youtube"
    if host in XIAOYUZHOU_HOSTS and parsed.path.startswith("/podcast/"):
        return "xiaoyuzhou"
    return "rss"
```

Add this helper after `infer_platform`:

```python
def extract_xiaoyuzhou_podcast_id(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in XIAOYUZHOU_HOSTS:
        return ""
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0] == "podcast":
        return parts[1]
    return ""
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestPodcastPlatformInference -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-podcast.py tests/test_fetch_podcast.py
git commit -m "feat: infer xiaoyuzhou podcast platform"
```

---

### Task 3: OpenCLI JSON Command Helpers

**Files:**
- Modify: `tests/test_fetch_podcast.py`
- Modify: `scripts/fetch-podcast.py`

- [ ] **Step 1: Write failing OpenCLI helper tests**

Add this class to `tests/test_fetch_podcast.py` after `TestPodcastSourceLoading`:

```python
class TestOpenCliHelpers(unittest.TestCase):
    @patch.dict("os.environ", {"OPENCLI_BIN": "/custom/opencli"})
    def test_resolve_opencli_bin_from_env(self):
        self.assertEqual(fetch_podcast.resolve_opencli_bin(), "/custom/opencli")

    @patch("shutil.which", return_value="/usr/local/bin/opencli")
    def test_resolve_opencli_bin_from_path(self, _which):
        self.assertEqual(fetch_podcast.resolve_opencli_bin(), "/usr/local/bin/opencli")

    @patch("shutil.which", return_value=None)
    def test_resolve_opencli_bin_returns_none_when_missing(self, _which):
        self.assertIsNone(fetch_podcast.resolve_opencli_bin())

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=0,
            stdout='[{"eid":"episode-one"}]',
            stderr="",
        ),
    )
    def test_run_opencli_json_parses_stdout(self, run):
        payload = fetch_podcast.run_opencli_json(
            "/usr/local/bin/opencli",
            ["xiaoyuzhou", "podcast-episodes", "pid", "--limit", "20", "-f", "json"],
        )

        self.assertEqual(payload, [{"eid": "episode-one"}])
        self.assertEqual(run.call_args.args[0][0], "/usr/local/bin/opencli")
        self.assertIn("-f", run.call_args.args[0])
        self.assertIn("json", run.call_args.args[0])

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=78,
            stdout="",
            stderr="Missing Xiaoyuzhou credentials. Expected /Users/test/.opencli/xiaoyuzhou.json",
        ),
    )
    def test_run_opencli_json_raises_on_nonzero_exit(self, _run):
        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.run_opencli_json(
                "/usr/local/bin/opencli",
                ["xiaoyuzhou", "podcast-episodes", "pid", "-f", "json"],
            )

        self.assertIn("Missing Xiaoyuzhou credentials", str(context.exception))

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=0,
            stdout="{not-json",
            stderr="",
        ),
    )
    def test_run_opencli_json_raises_on_invalid_json(self, _run):
        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.run_opencli_json(
                "/usr/local/bin/opencli",
                ["xiaoyuzhou", "podcast-episodes", "pid", "-f", "json"],
            )

        self.assertIn("valid JSON", str(context.exception))
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestOpenCliHelpers -v
```

Expected: FAIL because helper functions do not exist.

- [ ] **Step 3: Implement OpenCLI helpers**

In `scripts/fetch-podcast.py`, add `import shutil` near the imports:

```python
import shutil
```

Add helpers after `resolve_ytdlp_bin`:

```python
def resolve_opencli_bin() -> Optional[str]:
    configured = os.environ.get("OPENCLI_BIN")
    if configured:
        return configured
    return shutil.which("opencli")


def run_opencli_json(opencli_bin: str, args: List[str], timeout: int = 90) -> Any:
    import subprocess

    cmd = [opencli_bin] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("opencli command timed out") from exc
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "opencli command failed").strip()
        raise RuntimeError(message[:300])

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("opencli output was not valid JSON") from exc
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestOpenCliHelpers -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-podcast.py tests/test_fetch_podcast.py
git commit -m "feat: add opencli podcast helpers"
```

---

### Task 4: Xiaoyuzhou Metadata Normalization and Fetching

**Files:**
- Modify: `tests/test_fetch_podcast.py`
- Modify: `scripts/fetch-podcast.py`

- [ ] **Step 1: Write failing normalization tests**

Add this class to `tests/test_fetch_podcast.py` after `TestYoutubeMetadataNormalization`:

```python
class TestXiaoyuzhouMetadataNormalization(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "whynottv-podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        self.cutoff = utc("2026-01-01T00:00:00Z")

    def test_normalizes_xiaoyuzhou_episode_rows(self):
        rows = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Danfei Xu",
                "duration": "137:23",
                "plays": 11915,
                "date": "2026-05-01",
            },
            {
                "eid": "old",
                "title": "Old Episode",
                "date": "2025-01-01",
            },
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Danfei Xu")
        self.assertEqual(
            episodes[0]["link"],
            "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
        )
        self.assertEqual(episodes[0]["guid"], "xiaoyuzhou:69f441cd5390b7cc928acdcc")
        self.assertEqual(episodes[0]["date"], "2026-05-01T00:00:00+00:00")
        self.assertEqual(episodes[0]["platform"], "xiaoyuzhou")
        self.assertEqual(episodes[0]["show_name"], "WhynotTV Podcast")
        self.assertEqual(episodes[0]["transcript_status"], "disabled")

    def test_normalizes_xiaoyuzhou_rows_newest_first(self):
        rows = [
            {"eid": "older", "title": "Older", "date": "2026-05-01"},
            {"eid": "newer", "title": "Newer", "date": "2026-05-03"},
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual([episode["guid"] for episode in episodes], ["xiaoyuzhou:newer", "xiaoyuzhou:older"])

    def test_normalize_xiaoyuzhou_metadata_rejects_non_list_payload(self):
        with self.assertRaises(RuntimeError):
            fetch_podcast.normalize_xiaoyuzhou_metadata({"eid": "one"}, self.source, self.cutoff)
```

- [ ] **Step 2: Write failing fetch source tests**

In `TestPodcastCliOutput`, add:

```python
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_uses_opencli(self, _resolve, run_opencli):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        run_opencli.return_value = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Danfei Xu",
                "date": "2026-05-01",
            }
        ]

        episodes = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            {"metadata": {}, "transcripts": {}},
            no_cache=True,
        )

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["guid"], "xiaoyuzhou:69f441cd5390b7cc928acdcc")
        run_opencli.assert_called_once_with(
            "/usr/local/bin/opencli",
            [
                "xiaoyuzhou",
                "podcast-episodes",
                "686a1832222ae2de21fea940",
                "--limit",
                str(fetch_podcast.MAX_EPISODES_PER_SOURCE),
                "-f",
                "json",
            ],
        )

    @patch("fetch_podcast.resolve_opencli_bin", return_value=None)
    def test_fetch_xiaoyuzhou_source_requires_opencli(self, _resolve):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
        }

        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.fetch_xiaoyuzhou_source(
                source,
                utc("2026-01-01T00:00:00Z"),
                {"metadata": {}, "transcripts": {}},
                no_cache=True,
            )

        self.assertIn("opencli is not available", str(context.exception))

    def test_fetch_source_routes_xiaoyuzhou_platform(self):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
        }
        cutoff = utc("2026-01-01T00:00:00Z")

        with patch.object(fetch_podcast, "fetch_xiaoyuzhou_source", return_value=[]) as fetch_xiaoyuzhou:
            result = fetch_podcast.fetch_source(source, cutoff, {"transcripts": {}}, no_cache=True)

        fetch_xiaoyuzhou.assert_called_once()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["platform"], "xiaoyuzhou")
```

- [ ] **Step 3: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestXiaoyuzhouMetadataNormalization tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_uses_opencli tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_requires_opencli tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_source_routes_xiaoyuzhou_platform -v
```

Expected: FAIL because Xiaoyuzhou functions and routing do not exist.

- [ ] **Step 4: Implement Xiaoyuzhou date parsing and normalization**

In `scripts/fetch-podcast.py`, add after `parse_youtube_date`:

```python
def parse_xiaoyuzhou_date(value: Any) -> Optional[datetime]:
    if not value:
        return None
    text = str(value).strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        try:
            return datetime.strptime(text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return parse_podcast_date(text)
```

Add after `normalize_youtube_metadata`:

```python
def normalize_xiaoyuzhou_metadata(
    payload: Any,
    source: Dict[str, Any],
    cutoff: datetime,
) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        raise RuntimeError("opencli xiaoyuzhou podcast-episodes output was not a list")

    episodes: List[Dict[str, Any]] = []
    seen_episode_ids: Set[str] = set()
    for entry in payload:
        if not isinstance(entry, dict):
            continue

        episode_id = str(entry.get("eid") or "").strip()
        title = str(entry.get("title") or "").strip()
        published = parse_xiaoyuzhou_date(entry.get("date"))
        if not episode_id or not title or not published or published < cutoff:
            continue
        if episode_id in seen_episode_ids:
            continue
        seen_episode_ids.add(episode_id)

        episode = build_episode(
            source,
            title,
            f"https://www.xiaoyuzhoufm.com/episode/{episode_id}",
            published,
            f"xiaoyuzhou:{episode_id}",
            "xiaoyuzhou",
        )
        episodes.append(episode)

    return newest_episodes(episodes)
```

- [ ] **Step 5: Implement Xiaoyuzhou source fetcher**

In `scripts/fetch-podcast.py`, add this function before `fetch_source`:

```python
def fetch_xiaoyuzhou_source(
    source: Dict[str, Any],
    cutoff: datetime,
    cache: Dict[str, Any],
    no_cache: bool,
) -> List[Dict[str, Any]]:
    podcast_id = extract_xiaoyuzhou_podcast_id(source.get("url", ""))
    if not podcast_id:
        raise RuntimeError("Xiaoyuzhou podcast URL must use the /podcast/{id} path")

    opencli_bin = resolve_opencli_bin()
    if not opencli_bin:
        raise RuntimeError("opencli is not available")

    payload = run_opencli_json(
        opencli_bin,
        [
            "xiaoyuzhou",
            "podcast-episodes",
            podcast_id,
            "--limit",
            str(MAX_EPISODES_PER_SOURCE),
            "-f",
            "json",
        ],
    )
    episodes = normalize_xiaoyuzhou_metadata(payload, source, cutoff)
    return [
        enrich_episode_transcript(episode, source, cache, no_cache=no_cache)
        for episode in episodes
    ]
```

Update `fetch_source` routing:

```python
        if platform == "youtube":
            articles = fetch_youtube_source(source, cutoff, cache, no_cache)
        elif platform == "xiaoyuzhou":
            articles = fetch_xiaoyuzhou_source(source, cutoff, cache, no_cache)
        elif platform == "rss":
            articles = fetch_rss_source(source, cutoff, cache, no_cache)
        else:
            raise RuntimeError(f"Unsupported podcast platform: {platform}")
```

- [ ] **Step 6: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestXiaoyuzhouMetadataNormalization tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_uses_opencli tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_requires_opencli tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_source_routes_xiaoyuzhou_platform -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/fetch-podcast.py tests/test_fetch_podcast.py
git commit -m "feat: fetch xiaoyuzhou podcast episodes"
```

---

### Task 5: OpenCLI Transcript Enrichment

**Files:**
- Modify: `tests/test_fetch_podcast.py`
- Modify: `scripts/fetch-podcast.py`

- [ ] **Step 1: Write failing transcript tests**

In `TestTranscriptBackend.setUp`, keep the existing YouTube source and episode unchanged. Add this method to the class:

```python
    def xiaoyuzhou_source(self):
        return {
            "id": "whynottv-podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "topics": ["podcast"],
            "transcript": {
                "enabled": True,
                "backend": "opencli",
            },
        }

    def xiaoyuzhou_episode(self):
        return {
            "title": "Danfei Xu",
            "link": "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
            "date": "2026-05-01T00:00:00+00:00",
            "guid": "xiaoyuzhou:69f441cd5390b7cc928acdcc",
            "topics": ["podcast"],
            "show_name": "WhynotTV Podcast",
            "platform": "xiaoyuzhou",
            "transcript_status": "missing",
        }
```

Add these tests to `TestTranscriptBackend`:

```python
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_opencli_transcript_success_attaches_text(self, _resolve, run_opencli):
        with tempfile.TemporaryDirectory() as tmpdir:
            text_file = Path(tmpdir) / "transcript.txt"
            text_file.write_text("Segment one.\nSegment two.\n", encoding="utf-8")
            run_opencli.return_value = [
                {
                    "status": "success",
                    "segments": "2",
                    "text_file": str(text_file),
                }
            ]

            result = fetch_podcast.enrich_episode_transcript(
                self.xiaoyuzhou_episode(),
                self.xiaoyuzhou_source(),
                {},
                no_cache=True,
            )

        self.assertEqual(result["transcript_status"], "ok")
        self.assertEqual(result["transcript"], "Segment one.\nSegment two.")
        run_opencli.assert_called_once()
        self.assertIn("transcript", run_opencli.call_args.args[1])

    @patch("fetch_podcast.resolve_opencli_bin", return_value=None)
    def test_opencli_transcript_backend_unavailable_keeps_episode(self, _resolve):
        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            self.xiaoyuzhou_source(),
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "backend_unavailable")
        self.assertIn("transcript_error", result)
        self.assertNotIn("transcript", result)

    @patch("fetch_podcast.run_opencli_json", side_effect=RuntimeError("Transcript URL not found"))
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_opencli_transcript_failure_keeps_episode(self, _resolve, _run_opencli):
        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            self.xiaoyuzhou_source(),
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "error")
        self.assertIn("Transcript URL not found", result["transcript_error"])
        self.assertNotIn("transcript", result)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestTranscriptBackend.test_opencli_transcript_success_attaches_text tests.test_fetch_podcast.TestTranscriptBackend.test_opencli_transcript_backend_unavailable_keeps_episode tests.test_fetch_podcast.TestTranscriptBackend.test_opencli_transcript_failure_keeps_episode -v
```

Expected: FAIL because `opencli` transcript backend is not supported.

- [ ] **Step 3: Implement Xiaoyuzhou episode id extraction from guid**

In `scripts/fetch-podcast.py`, add after `extract_xiaoyuzhou_podcast_id`:

```python
def xiaoyuzhou_episode_id_from_episode(episode: Dict[str, Any]) -> str:
    guid = str(episode.get("guid") or "").strip()
    if guid.startswith("xiaoyuzhou:"):
        return guid.split(":", 1)[1].strip()
    link = str(episode.get("link") or "").strip()
    parsed = urlparse(link)
    host = (parsed.hostname or "").lower()
    if host in XIAOYUZHOU_HOSTS:
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2 and parts[0] == "episode":
            return parts[1]
    return ""
```

- [ ] **Step 4: Implement OpenCLI transcript runner**

Add after `run_ytdlp_transcript`:

```python
def run_opencli_transcript(
    opencli_bin: str,
    episode: Dict[str, Any],
    timeout: int = 120,
) -> Dict[str, str]:
    episode_id = xiaoyuzhou_episode_id_from_episode(episode)
    if not episode_id:
        return {"status": "error", "error": "Xiaoyuzhou episode id not found"}

    with tempfile.TemporaryDirectory(prefix="follow-news-xiaoyuzhou-transcript-") as tmpdir:
        try:
            payload = run_opencli_json(
                opencli_bin,
                [
                    "xiaoyuzhou",
                    "transcript",
                    episode_id,
                    "--output",
                    tmpdir,
                    "-f",
                    "json",
                ],
                timeout=timeout,
            )
        except RuntimeError as exc:
            return {"status": "error", "error": str(exc)[:200]}

        rows = payload if isinstance(payload, list) else [payload]
        for row in rows:
            if not isinstance(row, dict):
                continue
            text_file = str(row.get("text_file") or "").strip()
            if not text_file or text_file == "-":
                continue
            try:
                transcript = Path(text_file).read_text(encoding="utf-8", errors="replace").strip()
            except OSError as exc:
                return {"status": "error", "error": str(exc)[:200]}
            if transcript:
                return {"status": "ok", "transcript": transcript}

    return {"status": "missing", "error": "No transcript text returned by opencli"}
```

- [ ] **Step 5: Route transcript backend by platform/backend**

In `enrich_episode_transcript`, replace the backend validation and runner block with:

```python
    backend = config.get("backend", "auto")
    if backend not in {"auto", "yt-dlp", "opencli"}:
        episode["transcript_status"] = "error"
        episode["transcript_error"] = f"Unsupported transcript backend: {backend}"
        return episode

    if backend == "opencli" or episode.get("platform") == "xiaoyuzhou":
        opencli_bin = resolve_opencli_bin()
        if not opencli_bin:
            result = {"status": "backend_unavailable", "error": "opencli is not available"}
        else:
            result = run_opencli_transcript(opencli_bin, episode)
    else:
        ytdlp_bin = resolve_ytdlp_bin()
        if not ytdlp_bin:
            result = {"status": "backend_unavailable", "error": "yt-dlp is not available"}
        else:
            result = run_ytdlp_transcript(ytdlp_bin, episode, transcript_languages(source))
```

Keep the existing code below this block that copies `result` into `episode` and stores cache entries.

- [ ] **Step 6: Run transcript tests**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestTranscriptBackend -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/fetch-podcast.py tests/test_fetch_podcast.py
git commit -m "feat: enrich xiaoyuzhou transcripts with opencli"
```

---

### Task 6: Xiaoyuzhou Metadata Cache

**Files:**
- Modify: `tests/test_fetch_podcast.py`
- Modify: `scripts/fetch-podcast.py`

- [ ] **Step 1: Write failing cache test**

Add this test to `TestPodcastCliOutput`:

```python
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_reuses_metadata_cache(self, _resolve, run_opencli):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        payload = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Cached Episode",
                "date": "2026-05-01",
            }
        ]
        cache = {
            "metadata": {
                fetch_podcast.metadata_cache_key(source): {
                    "payload": payload,
                    "ts": time.time(),
                }
            },
            "transcripts": {},
        }

        episodes = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        run_opencli.assert_not_called()
        self.assertEqual(episodes[0]["title"], "Cached Episode")
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_reuses_metadata_cache -v
```

Expected: FAIL because `fetch_xiaoyuzhou_source` does not consult metadata cache yet.

- [ ] **Step 3: Update metadata cache key**

Replace `metadata_cache_key` in `scripts/fetch-podcast.py` with:

```python
def metadata_cache_key(source: Dict[str, Any]) -> str:
    platform = source.get("platform") or infer_platform(source.get("url", ""))
    if platform == "xiaoyuzhou":
        identity = extract_xiaoyuzhou_podcast_id(source.get("url", "")) or source.get("url", "")
    else:
        identity = source.get("url", "")
    return f"{platform}:{identity}:{MAX_EPISODES_PER_SOURCE}:v{METADATA_CACHE_VERSION}"
```

- [ ] **Step 4: Use cache in Xiaoyuzhou fetcher**

In `fetch_xiaoyuzhou_source`, replace direct `run_opencli_json` assignment with:

```python
    cache_key = metadata_cache_key(source)
    now = time.time()
    cached = None if no_cache else cache.get("metadata", {}).get(cache_key)
    if isinstance(cached, dict) and metadata_cache_entry_valid(cached, now):
        payload = cached["payload"]
    else:
        payload = run_opencli_json(
            opencli_bin,
            [
                "xiaoyuzhou",
                "podcast-episodes",
                podcast_id,
                "--limit",
                str(MAX_EPISODES_PER_SOURCE),
                "-f",
                "json",
            ],
        )
        if not no_cache:
            cache.setdefault("metadata", {})[cache_key] = {
                "payload": payload,
                "ts": now,
            }
```

- [ ] **Step 5: Run cache test**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast.TestPodcastCliOutput.test_fetch_xiaoyuzhou_source_reuses_metadata_cache -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch-podcast.py tests/test_fetch_podcast.py
git commit -m "feat: cache xiaoyuzhou podcast metadata"
```

---

### Task 7: Documentation and Full Verification

**Files:**
- Modify: `README.md`
- Modify: `README_CN.md`
- Modify: `SKILL.md`
- Modify: `tests/test_config.py`

- [ ] **Step 1: Extend docs test for Xiaoyuzhou OpenCLI support**

In `TestReadmeCounts.test_podcast_runtime_docs_include_youtube_and_ytdlp`, add these assertions inside the per-doc loop:

```python
                self.assertIn("xiaoyuzhou", lowered)
                self.assertIn('"platform": "xiaoyuzhou"', content)
                self.assertIn('"backend": "opencli"', content)
```

- [ ] **Step 2: Run docs test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_config.TestReadmeCounts.test_podcast_runtime_docs_include_youtube_and_ytdlp -v
```

Expected: FAIL because README and SKILL docs do not mention Xiaoyuzhou yet.

- [ ] **Step 3: Update README.md podcast config example**

In `README.md`, add a Xiaoyuzhou example near the existing podcast example:

```json
    {
      "id": "whynottv-podcast",
      "type": "podcast",
      "name": "WhynotTV Podcast",
      "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
      "platform": "xiaoyuzhou",
      "enabled": true,
      "priority": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "opencli"
      }
    }
```

Also add this paragraph near the podcast runtime notes:

```markdown
Xiaoyuzhou podcast sources use `platform: "xiaoyuzhou"` and require OpenCLI plus local Xiaoyuzhou credentials at `~/.opencli/xiaoyuzhou.json`. The fetcher calls `opencli xiaoyuzhou` JSON commands and does not call Xiaoyuzhou APIs directly.
```

- [ ] **Step 4: Update README_CN.md**

Add the same JSON example with English keys and values:

```json
    {
      "id": "whynottv-podcast",
      "type": "podcast",
      "name": "WhynotTV Podcast",
      "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
      "platform": "xiaoyuzhou",
      "enabled": true,
      "priority": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": true,
        "backend": "opencli"
      }
    }
```

Add this Chinese paragraph:

```markdown
小宇宙播客源使用 `platform: "xiaoyuzhou"`，需要 OpenCLI 以及本地小宇宙凭据 `~/.opencli/xiaoyuzhou.json`。fetcher 只调用 `opencli xiaoyuzhou` JSON 命令，不会在本项目内直接调用小宇宙 API。
```

- [ ] **Step 5: Update SKILL.md runtime docs**

In `SKILL.md`, add Xiaoyuzhou to podcast capability descriptions. Include this config example in the source configuration section:

```json
{
  "id": "whynottv-podcast",
  "type": "podcast",
  "name": "WhynotTV Podcast",
  "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
  "platform": "xiaoyuzhou",
  "enabled": true,
  "priority": true,
  "topics": ["podcast"],
  "transcript": {
    "enabled": true,
    "backend": "opencli"
  }
}
```

Add this runtime note:

```markdown
- Xiaoyuzhou podcast sources require OpenCLI and `~/.opencli/xiaoyuzhou.json`; the fetcher delegates Xiaoyuzhou API behavior to OpenCLI.
```

- [ ] **Step 6: Run docs test**

Run:

```bash
python3 -m unittest tests.test_config.TestReadmeCounts.test_podcast_runtime_docs_include_youtube_and_ytdlp -v
```

Expected: PASS.

- [ ] **Step 7: Run targeted fetcher and config tests**

Run:

```bash
python3 -m unittest tests.test_fetch_podcast tests.test_config.TestPodcastConfigValidation tests.test_config_editor_server.TestConfigEditorServer -v
```

Expected: PASS.

- [ ] **Step 8: Run config validation smoke**

Run:

```bash
python3 scripts/validate-config.py --defaults config/defaults --verbose
```

Expected: exit code 0 and source type validation passed.

- [ ] **Step 9: Run podcast fetcher smoke**

Run:

```bash
python3 scripts/fetch-podcast.py --defaults config/defaults --hours 1 --output /tmp/td-podcast.json --force --verbose
```

Expected: exit code 0. Existing RSS podcast sources may return zero or more articles depending on live feed freshness. No Xiaoyuzhou source is required in defaults.

- [ ] **Step 10: Commit**

```bash
git add README.md README_CN.md SKILL.md tests/test_config.py
git commit -m "docs: document xiaoyuzhou podcast sources"
```

---

## Final Verification

- [ ] **Step 1: Run full relevant unit suite**

```bash
python3 -m unittest tests.test_fetch_podcast tests.test_config tests.test_config_editor_server -v
```

Expected: PASS.

- [ ] **Step 2: Inspect git status**

```bash
git status --short
```

Expected: no unstaged implementation files. If a smoke command created only `/tmp/td-podcast.json`, it will not appear in git status.

- [ ] **Step 3: Optional manual Xiaoyuzhou smoke with credentials**

Create a temporary overlay config:

```bash
mkdir -p /tmp/follow-news-xiaoyuzhou-config
cat > /tmp/follow-news-xiaoyuzhou-config/follow-news-sources.json <<'JSON'
{
  "sources": [
    {
      "id": "whynottv-podcast",
      "type": "podcast",
      "name": "WhynotTV Podcast",
      "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
      "platform": "xiaoyuzhou",
      "enabled": true,
      "priority": true,
      "topics": ["podcast"],
      "transcript": {
        "enabled": false,
        "backend": "opencli"
      }
    }
  ]
}
JSON
python3 scripts/fetch-podcast.py --defaults config/defaults --config /tmp/follow-news-xiaoyuzhou-config --hours 720 --output /tmp/td-xiaoyuzhou.json --force --verbose
python3 -m json.tool /tmp/td-xiaoyuzhou.json >/tmp/td-xiaoyuzhou.pretty.json
```

Expected with valid OpenCLI Xiaoyuzhou credentials: exit code 0 and `/tmp/td-xiaoyuzhou.json` includes a source with `platform: "xiaoyuzhou"` and recent articles.

Expected without credentials: exit code 0 and the Xiaoyuzhou source has `status: "error"` with a message mentioning Xiaoyuzhou credentials.
