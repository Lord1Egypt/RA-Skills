# 项目记忆 — ai-video-auto-generator

## 核心原则：执行路径即身份（2026-07-15 修订版）

**不靠全局 env 区分平台，靠哪个 Python 文件被 invoke。**
**配置跟 skill 副本和 project 目录走，不跟宿主平台目录名走。**

### Layer 1 — Skill 根目录
- `scripts/_paths.py` — `resolve_skill_root(__file__)` 向上找 SKILL.md marker
- 三个平台同时跑 → 各 `__file__` 不同 → `skill_root` 不同 → 互不干扰
- 禁止代码中出现 `.workbuddy`、`skills/ai-video-auto-generator` 等平台路径字符串

### Layer 2 — 运行时配置（分层合并）
- `load_config(skill_root, project)` 显式传参，无全局 env
- 优先级（高 → 低）：`<project>/config/keys.env` → `<project>/config/config.toml` → `<skill_root>/config/keys.env` → `<skill_root>/config/config.toml`
- 支持 keys.env（KEY=VALUE 格式）+ config.toml 两种格式
- 入口脚本调用 `init_config(skill_root, project)` 后，`get(section, key)` 可用

### Layer 3 — 用户项目
- 通过 `--project <path>` 指定，与 skill 安装位置无关

### 二进制工具路径
- `resolve_tool("ffmpeg", skill_root)` / `resolve_tool("node", skill_root)`
- 优先级：vendor/ → config/tools.toml → 系统 PATH → legacy（仅标记）
- `resolve_node_modules(skill_root)` — 找 node_modules 目录

### Legacy 兼容
- `.legacy-workbuddy` 标记控制 `~/.workbuddy/config.toml` 是否被读取
- 当前 WorkBuddy 环境有此标记（向后兼容）
- 迁移到 `<skill_root>/config/` 后可删除标记

### 关键约束
- 无 `AI_VIDEO_*` 全局环境变量
- 不读 `~/.workbuddy/config.toml`（除非有 `.legacy-workbuddy` 标记）
- 文档用 `<skill-root>` 占位符或相对路径（`python3 scripts/pipeline.py ...`）
- `~/.agnes-api-key` 等共享凭证仅作最后 fallback（同一用户多平台共用 API Key 时）

## ⚠️ 代码重构现实（2026-07-16 重新核实 — 修正旧记忆）
- `poll_loop.py` 已删除（全仓无此文件）。
- `video_api.py` / `image_api.py` **仍然存在**，位于 `skills/agnes-ai/scripts/modules/`，分别保留 `MAX_API_RETRY=6` / `MAX_UPLOAD_RETRY=4`。它们是 agnes-ai 子 skill 的 standalone 图片/视频生成实现，并非被删除。
- 重试封顶两层并存：
  - agnes-ai standalone：`video_api.py`/`image_api.py` `MAX_API_RETRY=6`（图片 `min(2**n,300)` 退避；视频 `min(30*2**(n-1),300)` 退避）。
  - project-generate Provider 模式：`agnes_provider.py` 内 `generate_character`/`generate_scene` 用 `max_attempts=5`，rate_limit 时固定 `sleep(30)`（注意：无 `submit_image`/`generate_video` 方法；图片 4xx→return None 实际在 `image_api.generate_image`）。
- 轮询在 `pipeline.py::_run_poll`，`timeout=1800`（已核实）。
- 自愈循环在 `project_commands/__init__.py:_auto_repair_assets`，`max_attempts=10`（已核实；无 `_run_repair`）。
- **旧记忆"video_api.py/image_api.py 已被删除、MAX_API_RETRY=6 失效"是错误的** —— 这两个文件及其常量仍有效，可作证据。

## 🔒 版本号同步铁律（2026-07-16 由 doc-rot 复检暴露的系统性根因）
- **根因**：每次发版只在 CHANGELOG.md 顶部新增/升版本号，忘记同步 3 个 SKILL.md 的 frontmatter `version:`，导致二者**永远差一个版本**（CHANGELOG 领先一版）。
- **铁律**：任何一次 `CHANGELOG.md` 顶部版本号变更（新增条目或升版本），**必须同时**把以下 3 处 frontmatter `version:` 改成同一值：
  1. `SKILL.md`（主 skill，根目录）
  2. `skills/agnes-ai/SKILL.md`
  3. `skills/project-generate/SKILL.md`
- **验证方法**（改完随手跑）：`grep -rn "^version:" SKILL.md skills/*/SKILL.md` 应与 `CHANGELOG.md` 顶部 `## x.y.z` 完全一致。
- 现状（2026-07-16 复检后）：CHANGELOG 顶部 = 2.6.4，3 处 frontmatter 已同步为 2.6.4。
- CHANGELOG 条目内的「版本号」bullet 要写**本次变更前后**的真实值（如 2.6.3→2.6.4），严禁复制粘贴上一条的旧值。

## ⚠️ 代码层 doc-rot（2026-07-16 全量审计，已逐条代码核实）
- 本次审计针对**脚本代码**（非文档），发现 5 处 [BROKEN] 会直接让 `auto` 流水线崩溃，均 grep/读码核实。
- **2026-07-16 已全部修复**（+ 死代码清理），5 个修改后文件均 compile 通过：
  - ✅ ④ project_verify.py：增 `verify_character_assets`/`_detailed` / `verify_scene_assets`/`_detailed` / `verify_troop_assets`/`_detailed`（6 函数，遍历目录调已有 `_verify_character_image`/`_verify_scene_image`）。
  - ✅ ③ base_provider.py：增 `generate_characters(project, data, force)` 循环调 `generate_character`（项目_commands:330 签名已匹配，无需改调用方）。
  - ✅ ② base_provider.py + agnes_provider.py：增 `generate_first_frame(project, shot, script_data)`。BaseProvider 默认返回 None；AgnesProvider 完整实现（`build_first_frame` → `generate_prompt_template` → `generate_image`，返回 `{"status":"ok","path":...,"final":...}`）。
  - ✅ ⑤ video_utils.py：增 `get_shot_mode`/`get_shot_info`/`ref_image`/`resolve_ref_images`（4 模块函数，base_provider 委托调用生效）。
  - ✅ ① project_commands:593 + video_utils:151：`submit_video` 调用修正——从 shot/script 字典中提取 `shot_id`/`prompt`/`duration`/`aspect`/`ref_img`，逐项传 keyword 参数，匹配 Provider 签名。
  - 🗑️ 死代码：`_paths`(54)、`_create_provider`(81)、`api.py` shim(零引用) 已清理。
  - ⏳ 未动：`_cmd_verify`(453 未 dispatch)、`fix_script_narrative`(282 零调用)、11 个 CLI 占位桩。

## ⚠️ CHANGELOG 2.6.0 "13 处修复" — 2026-07-16 复查已落地（修正旧记忆）
- 重新核实（2026-07-16 当天）：CHANGELOG 列出的路径/stage/retry/e2e 修复**确实已落地**：
  - 所有裸 `scripts/pipeline.py` 路径均已改为 `skills/project-generate/scripts/pipeline.py`（README/SKILL.md/sample/README/pipeline-diagram.svg/pipeline.py:154）。
  - project-generate/SKILL.md 阶段数已为 9（0→8），无 while-True。
  - 主 SKILL.md retry 已为 max 10；agnes-ai/SKILL.md 无 poll_loop/moot；troubleshooting 无已删文件引用、retry=5；e2e=13 目录。
- **旧记忆"全部仍坏 / CHANGELOG 不可信"已过时** —— 上述项当前正确，排查以当前文件为准。
- 旧审计（docs-audit-2026-07-16.md）列的「仍过时」5 项，已于 **2.6.1/2.6.2 全部修复落地**（压缩段改写、img_host 重试表、退避描述、SVG 5类·9阶段、select_mode 引用、版本号）。该审计报告本身已过时，排查以当前文件为准。
- **2026-07-16 第二轮全量审计（对照 live 代码）发现的新 doc-rot（当前仍真实）**：
  1. agnes-ai/SKILL.md 重试表(476-481 行)方法名臆造：`agnes_provider.py submit_image`/`generate_video` 两方法不存在；实际重试在 `generate_character`/`generate_scene`(max_attempts=5)，图片 4xx→return None 在 `image_api.generate_image`。
  2. agnes-ai/SKILL.md 重试表 `image_api.py upload_to_url` 退避写成「10→20→30→**60**s」，实际 `min(10*attempt,60)` 且 MAX_UPLOAD_RETRY=4 → 实际 10/20/30/**40**s（60 仅 attempt≥6）。CHANGELOG 2.6.2「10→60s」是范围描述无误，但文档显式序列写错。
  3. e2e-walkthrough.md:177「每角色 11 张」与同文档:97「数量随角色卡而定」矛盾（2.6.2 #6 只改了 :97，漏改 :177）。
  4. agnes-ai/SKILL.md:485 把 `_classify_failure()` 归属 `video_utils.py`；实为 `video_utils.py:8` 从 `error_utils.classify` 导入的别名，5 类函数在 `error_utils.classify`。
  5. 主 SKILL.md:97 / README:30「运行 `fix_script_narrative` 12 维修复」——`fix_script_narrative`(project_verify.py:282) 全仓零调用，auto 流水线实际走 `OptimizerV2`(project_commands:501，经 `optimize` 命令)；该函数疑似 dead code，文档入口函数名错误。
  6. project-generate/SKILL.md 架构图把 `project_commands/` 画成 `modules/` 同级，实际路径 `scripts/modules/project_commands/`。
