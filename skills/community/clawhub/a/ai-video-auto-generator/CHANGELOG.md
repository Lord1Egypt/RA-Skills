# Changelog

## 2.7.0 (2026-07-16)

### New Features
- **`generate-troops` / `gt`**：读 `troop_cards`，调用 Provider 批量生成辅助资产图（白背景前/侧/背 3 视角），写入 `images/troops/`。自愈循环阶段 3 配套生效
- **`diff-all`**：扫描 `images/storyboard/backup/` 或 `*_old.png`，批量生成 shot-by-shot 新旧首帧图对比页（side-by-side + 滑块）输出到 `output/`，并生成 `output/diff_index.html` 索引页
- **`repair`**：自动修复提示词文件——先调用 `build-prompts` 重建 assets prompts，再修复 first_frame/video 提示词问题
- **`tracker-sync`**：`FeishuTracker.sync_to_local()` 反向同步（飞书→本地 task_tracker.json），供跨机接力用
- **`preview` / `report` 已实现**：`_cmd_preview` 调用 `project_preview.generate_preview()` 生成交互式 HTML；`_cmd_report` 调用 `project_stats.generate_stats()` 生成统计报告

### Fixes
- **`agnes-ai/SKILL.md` **：`_regenerate_first_frame()` 虚构函数名修正为真实调用链 `_resubmit_shot(regen_first_frame=True)` 及 `provider.generate_first_frame()`（:489/:494）
- **删除死代码**：`state.py` 孤儿重复模块、`_cmd_verify`/`_cmd_validate_prompts` 未接线函数、`stitch_ffmpeg.py` 转场相关 6 个死函数（`_get_transitions`/`_has_any_transition`/`_build_xfade_filter`/`run_with_transitions`/`_get_durations`/`_seg_duration`）及对应常量 (`TRANSITION_MAP`/`DEF_TRANS`/`DEF_DUR`)

### Removed (纯桩子命令清理)
- 删除以下从未实现的 CLI 子命令及其 import/parser/dispatch：`export-csv`、`export-template`、`init-from-template`、`check-refs`、`collect`、`dry-run`。对应函数体、`project_generate.py` 导入行、argparse 定义、分发分支全部移除。`project-generate/SKILL.md` 命令表同步删除这些行

## 2.6.5 (2026-07-16)

### Fixes (doc-rot 修正，纯文档不动代码)
- **project-generate/SKILL.md 视频流水线表**：`poll` 命令说明的轮询间隔「每 30 分钟检查一次」修正为「每 10 分钟检查一次」——代码 `time.sleep(600)`（auto stage 8 循环，日志自打"10分钟（600秒）"）与独立 `poll` 命令 `next_poll_at = now + 600`（video_utils.py:332）均为 600 秒 = 10 分钟
- **版本号**：主 SKILL.md / agnes-ai/SKILL.md / project-generate/SKILL.md 的 `version: 2.6.4` → 2.6.5（与 CHANGELOG 对齐）

## 2.6.4 (2026-07-16)

### Fixes (doc-audit 第二轮残留修正，纯文档不动代码)
- **script-json-checklist.md**：第 40 行「需要完整的 11 张资产图」修正为「多视图资产图（数量随角色卡而定：标准 4 视图 front/face/side/back + 动态持械/动作视图）」，与第 142 行及 e2e-walkthrough.md :97 一致（2.6.3 仅修了同文件第 142 行措辞，漏掉第 40 行不同措辞）
- **script-optimizer/SKILL.md**：入口命令 `optimize/__init__.py` 修正为 `python3 scripts/optimize/__init__.py`（该文件实为包 `__init__.py`，无 `scripts/optimize.py`）；调用方式表补全完整命令；同步修正 `optimize/__init__.py` docstring 的 `python3 scripts/optimize.py` 错误文件名
- **asset-generation.md**：第 9 行「11 种必须资产」改为「8 类必须资产（标准共 11 个文件）」以对齐第 68 行资产类别表；第 68 行补充说明 11 个文件为标准基数，含动态持械/动作视图时更多
- **project-generate/SKILL.md**：架构图删除重复的 `provider_factory.py` 行
- **版本号**：主 SKILL.md / agnes-ai/SKILL.md / project-generate/SKILL.md 的 `version: 2.6.3` → 2.6.4（与 CHANGELOG 对齐）

## 2.6.3 (2026-07-16)

### Fixes (doc-audit 残留修正，纯文档不动代码)
- **agnes-ai/SKILL.md 重试表**：原 `agnes_provider.py submit_image` / `generate_video` 两个方法实际不存在；改为真实存在的图片生成方法 `generate_character` / `generate_scene`（max_attempts=5，仅 rate_limit 时 sleep 30s），并修正 4xx 语义为「经 `apply_image_strategy` 调整提示词后重试、耗尽才 return None」，非「立即 return None」
- **agnes-ai/SKILL.md 重试表**：`image_api.py upload_to_url` 退避序列「10s→20s→30s→60s」修正为「10s→20s→30s→40s」（MAX_UPLOAD_RETRY=4，attempt 1–4 对应 10/20/30/40，60s 仅 attempt≥6 才触及）
- **agnes-ai/SKILL.md 错误分类**：`_classify_failure()` 实际位于 `error_utils.classify()`（在 `agnes_provider.py` / `video_utils.py` 中 import 为 `_classify_failure`），非 `video_utils.py` 自有函数
- **主 SKILL.md / README.md**：脚本优化入口「`fix_script_narrative`」改为真实入口「`optimize` 命令（OptimizerV2）」（`fix_script_narrative` 在 project_verify.py 仍存在但全仓无调用，非主路径）
- **e2e-walkthrough.md / script-json-checklist.md**：补全 2.6.2 漏改的「每角色 11 张」→「每角色视图数随角色卡而定（标准 4 视图 + 动态持械/动作视图）」（与 e2e-walkthrough.md :97 一致）
- **project-generate/SKILL.md 架构图**：`project_commands/` 从「`project_generate.py` 直接子目录」修正为「位于 `modules/` 下」（实际路径 `scripts/modules/project_commands/`）
- **project-generate/SKILL.md 首帧生成段**：`agnes_provider.py 的 submit_image` 修正为真实方法 `agnes_provider.generate_image` / `image_api.generate_image`（无 `submit_image`）

## 2.6.2 (2026-07-16)

### Fixes (doc-audit 补充修正)
- **README.md**：`create_project.py --list` 修正为 `--list-types`（`--list` 非有效参数，直接 `unrecognized arguments`）
- **README.md**：「方式 3 从飞书文档导入」删除不存在的 `project_generate.py init-from-feishu` 子命令，改为正确的 `create_project.py --feishu-doc-url <url>` 入口
- **agnes-ai/SKILL.md**：参考图托管段不再把行为错误归属到 `img_host.py`，改为明确默认 Agnes 走 `image_api.py upload_to_url`（GitHub 分支上传原图不压缩，与自查清单一致）
- **agnes-ai/SKILL.md 重试表**：补充默认 Agnes 上传路径 `image_api.py upload_to_url` 的真实语义（MAX_UPLOAD_RETRY=4 / 401·403→raise ValueError / 退避 10→60s / 耗尽 raise RuntimeError），原表仅覆盖小云雀路径
- **e2e-walkthrough.md**：角色视图计数改为准确的「标准 4 视图 + 按武器·动作动态生成」，去掉与代码不符的「4 全身照 + 11 张」固定数字
- **版本号**：主 SKILL.md / agnes-ai/SKILL.md / project-generate/SKILL.md 的 `version: 2.6.0` → 2.6.2（与 CHANGELOG 对齐）

## 2.6.1 (2026-07-16)

### Fixes (doc-rot 全修)
- **agnes-ai/SKILL.md 退避与重试表更正**：`agnes_provider.py` 实际为「错误感知重试」——`max_attempts=5`，仅 `rate_limit` 时固定 `sleep 30s`，其余类别不 sleep（非指数退避 2→300s，也非 1s→2s→4s→60s）；`img_host.py` 实际 `MAX_RETRIES=3`、固定 2s 退避、仅 `429/500/502/503` 重试、`401/403` 与耗尽均 `return None`（非 `raise` 异常）
- **agnes-ai/SKILL.md 参考图托管段重写**：早期「PIL 压缩 + 强制 PUT」策略已移除；现改为「先 GET 查 sha，已存在则跳过 PUT」的 skip-if-exists 优化，不压缩、不抛异常
- **agnes-ai/SKILL.md 模式选择函数引用修正**：`select_mode()` 实际位于 `video_api.py`（非不存在的 `agnes.py`）
- **project-generate/SKILL.md 标题与退避描述修正**：章节标题去掉「指数退避」（实际非指数），正文改为「错误感知重试 + 固定 30s rate_limit 退避」
- **pipeline-diagram.svg 文案更正**：`<desc>` 阶段数 six→nine（与主 SKILL.md 9 阶段一致）；自愈层 `classify(6 categories)`→`classify(5 categories)`（error_utils 实际 5 类：rate_limit/invalid_image/transient/bad_request/unknown）
- **README.md 去重**：删除与「💬 AI Agent 一键出片」重复的「方式 1：AI Agent 生成」段落，并重编号方式 1/2/3

## 2.6.0 (2026-07-15)

### New Features
- **独立 `stitch` 子命令**：`project_generate.py --project <dir> stitch --tracker local` 单独跑拼接（HF 无字幕渲染 → ffmpeg 烧录分段字幕 → 叠加音频/BGM → 输出 final.mp4），脱离 poll 复用，用于只改字幕/编码后重拼

### Fixes
- **HF 渲染恢复 headless shell 自动发现**：移除 `hyperframes_stitch.py` 强制注入 `HYPERFRAMES_BROWSER_PATH`/`PUPPETEER_EXECUTABLE_PATH` 指向 Edge 的代码（该注入会让 headed 浏览器发现链走 Edge → GPU 探测失败 Code:0 → 渲染级联失败回退 ffmpeg）。现回归 `resolveHeadlessShellPath` 自动发现 `~/.cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell.exe`，约 2.7min 渲染 18 镜头 2258 帧
- **safe-delete 沙箱坑修复**：`os.remove(final_hf.mp4)` / `os.unlink(_temp.mp4)` 被托管 Python safe-delete 钩子（无回收站抛 `SAFE_DELETE_FAIL_CLOSED`）拦截后原样上抛，被 `run_first` 当成拼接致命错误 → 误报失败。现已包 try/except，删不掉仅 `[warn]` 不致命
- **音视频合成步超时**：`timeout=600` → `1800`（防高负载误杀）
- **文档部分过时描述修复**（⚠️ 原记录"13 处"有夸大——约 5 条落地，~9 条仍需后续修复）：
  - 已落地：SKILL.md frontmatter version 与架构图阶段数(9→0-8)；setup-guide 命令/路径；troubleshooting 函数名/"非无限"措辞；provider-config/project-generate 包名引用；脚本死 fallback 分支清理
  - 仍坏但已漏修（2026-07-16 复查+修复）：README/SKILL.md/sample/README/pipeline-diagram.svg/pipeline.py:154 的 `scripts/pipeline.py` 路径；project-generate/SKILL.md 阶段数(10→0→9)/while True 无限重试/两份同步；agnes-ai/SKILL.md 全篇(version/引用已删文件/poll_loop/moot 警告)；主 SKILL.md retry(max5)；troubleshooting 引用已删文件+3次(应为5次)；e2e 11目录(实13)；README 方式3重复；project-generate 设计决策编号乱序

### Changed
- **字幕分段规则**：`_split_long_subtitle()` 改为**按空格分隔的词边界切分**，绝不按时间/纯字数硬切（避免劈开一个完整词 → 一句话分两段）。长文本按完整词累积到 max_chars(15字/行) 后切段
- **字幕字体/编码**：`force_style='FontName=Microsoft YaHei,FontSize=14,...'`；成片默认 `-crf 18`
- **字幕时间轴对齐实际时长**：`generate_srt()` 接收 `actual_durations`（ffprobe 真实视频时长），替代 script 计划 `duration_seconds`
- 更新 SKILL.md 命令列表 + 设计决策 §8–§11、troubleshooting.md §五 浏览器选择 + 字幕分段规则

## 2.5.0 (2026-07-10)

### New Features
- **Hyperframes auto-install**: `ensure_installed()` checks + auto npm installs hyperframes to managed node workspace; `--mode setup` includes HF detection; pipeline pre-check at startup
- **HF stitch + subtitle overlay**: HF renders video, then ffmpeg post-processing generates TTS audio + burns SRT subtitles into final output
- **voice_over vs dialogue split**: `speech.py` treats `voice_over` (TTS+subtitle) and `dialogue` (subtitle only) independently; `dialogue` shots skip TTS generation since Agnes video already contains character voices
- **voice_over narrative quality rules** (SKILL.md + optimize):
  - 5 validation rules: dialogue without characters (P1), dialogue on wide shots (P2), voice_over too long (P2), voice_over contains shot type keywords (P1), voice_over copied from description (P2)
  - 4 auto-fixes: dialogue→voice_over on wide shots, voice_over truncation, dialogue→character matching, voice_over cleanup (remove shot types/camera directions/character positioning)
  - Punctuation → spaces for TTS (with logical phrase break rules)
  - Broken phrase detection (segments ≤2 chars flagged P2)
- **Local mode stitch**: removed `feishu_doc_id` dependency, `--tracker local` now completes full stitch pipeline

### Fixes
- `_load_state()` now uses `utf-8-sig` encoding to tolerate BOM from PowerShell-written state files
- `.poll_state.json` interval check no longer skips stitch when state cleared

### Changed
- SKILL.md voice_over generation rules: narrative language, no shot types/camera directions, spaces instead of punctuation, logical phrase breaks (5-10 chars per segment, preserve subject-verb-object)
- `generate_all_voiceovers()` prioritizes `voice_over` field for TTS; falls to `dialogue` for subtitle-only
- **Major codebase refactoring (all internal, zero behavior change)**:
  - `project_commands.py` → `project_commands/` 包, `state.py` extracted, 9 pipeline stages split into standalone `_auto_stage0~8` functions
  - `optimize.py` → `optimize/` 包, `rules.py` extracted (constants/defaults centralized)
  - `scripts/_shared_tools.py` created: unified 6 utility functions + logging system + config loader (`_load()`/`get()`/`_legacy()`)
  - Both `config.py` (project-generate + agnes-ai) now import from `_shared_tools`, eliminating ~300 lines of duplicate code
  - Removed `_auto_detect_model()` dead code, log listener/callback hook system, `_sync_log()` sync function
  - `_cmd_optimize` + 3 prompt_builder commands converted from `subprocess.run` to direct Python import
  - Directory renamed `video-script-generator` → `ai-video-auto-generator` (with junction for backward compat)
  - HF composition subtitle timing now uses `ffprobe` actual video durations instead of planned `duration_seconds`

---

## 2.4.0 (2026-07-09)

### Changed
- Script optimizer expanded to 16 validation rules (character naming, clause punctuation, shot continuity)
- Pipeline compressed from 10 to 9 stages (narrative repair merged into optimize stage)
- `--fix-prompts` enabled by default in `optimize`
- Duration deviation threshold tightened from 15% to 10%
- `validate_script_narrative` logic fully absorbed into `optimize` for pre-asset validation
- Total duration auto-fix: proportional scaling to match `script.duration_seconds`

### New Features
- **Character inheritance engine**: auto-merge/complete `characters` field across scene groups, handles new-entrance and partial-overlap cases
- **Clause boundary fixer**: auto-insert commas at Chinese clause boundaries
- **Shot continuity checks**: action transition, perspective jump, spatial consistency
- **Scene group transition fixer**: auto-add transition descriptions between scene groups
- **Video prompt accuracy validation**: 5 content checks (character coverage, action coverage, scene consistency, dialogue presence, fuzzy count words)
- **Prompt directory reorganization**: video prompts → `prompts/videos/`, first frame prompts → `prompts/storyboard/`
- `generate-troops` / `gt` CLI command for troop card asset generation

### Fixes
- `fix_prompts` now actually triggers prompt file validation (previously only validated script.json)
- `config` module name collision between agnes-ai and project-generate fixed
- Continuous "突然" duplication prevention in hook-insertion logic
- Scene name redundancy removed from dialogue lines
- Empty character removal on close-ups no longer breaks continuity chain

### Cleanup
- `sync` CLI command removed (dual-copy sync no longer needed)
- `hf-stitch` CLI entry removed (function already deleted)
- Script optimizer test section removed from docs
- `update-prompts add` mode removed (never implemented)
- `upload_multiple_images` dead code removed
- GitHub upload: skip PUT for existing files, skip compression

---

## 2.3.0 (2026-07-08)
