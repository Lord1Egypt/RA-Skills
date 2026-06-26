# AGENT.md

本文件给在本仓库工作的 coding agent 使用。目标是让改动贴合 Follow ScoutX 的产品边界，避免把面向终端用户隐藏的后端细节重新暴露出来。

## 项目定位

Follow ScoutX 是一个可安装的 agent skill，用于从中心化 ScoutX public feed 拉取候选内容，并基于用户本地偏好生成个性化 digest。

核心原则：

- 终端用户通过自然语言配置频率、时间、主题、语言、摘要风格和投递目标。
- 终端用户可以选择 `ScoutX` 定制优质媒体源、一手信息源（X 平台与播客），或两者都看。
- 如果两类信息源都启用，OpenClaw recurring delivery 默认仍只创建一个 cron job；digest 内部按一手信息源 / ScoutX 优质自媒体分区排版。
- 默认条数按消息组平分；用户可以用 `--max-first-party-items` 和 `--max-scoutx-items` 分别设置上限。
- 如果飞书消息超长，脚本应在投递前拆成多条连续消息，而不是回退成多个 cron job。
- 终端用户不应该被要求配置 `BASE_URL`、API token、feed endpoint 或 raw JSON filter。
- 终端用户不应该被要求配置 X bearer token、播客 RSS 或转写服务 API key。
- ScoutX 后端负责集中采集和清洗内容；本仓库的 skill 只负责本地偏好、拉取、筛选、摘要输出和 OpenClaw cron 辅助。
- OpenClaw recurring delivery 应优先使用 `follow_scoutx.py deliver` 输出 stdout，再由 OpenClaw `--announce --channel <channel> --to <target>` 完成真正投递。

## 重要文件

- `SKILL.md`: skill 的主说明和 agent 执行流程。
- `README.md`: 面向安装者/用户的项目说明。
- `scripts/follow_scoutx.py`: 本地配置、预览、投递和 OpenClaw cron 生成逻辑。
- `service.json`: 打包时随 skill 分发的中心服务地址。
- `prompts/digest_intro.md`: digest 总体写作要求。
- `prompts/summarize_content.md`: 单条内容摘要要求。
- `prompts/summarize_tweets.md`: X 平台一手信息源摘要要求。
- `prompts/summarize_podcast.md`: 播客一手信息源摘要要求。
- `prompts/translate.md`: 翻译要求。

## 本地状态

运行脚本会在用户本地创建或更新：

```text
~/.follow_scoutx/
```

常见文件：

- `profile.json`
- `state.json`
- `prompt_sync_state.json`
- `service.json`
- `prompts/*.md`

测试或验证时如需隔离本地状态，使用 `FOLLOW_SCOUTX_HOME` 指向临时目录，避免污染真实用户配置。
- `ensure_local_files()` 会自动同步 skill 内置 prompts 到 `~/.follow_scoutx/prompts/`；旧版或未托管 prompt 会先备份到 `prompts/backups/`，已经被用户手改过的 prompt 默认保留不覆盖。

示例：

```bash
FOLLOW_SCOUTX_HOME=/tmp/follow-scoutx-test python3 scripts/follow_scoutx.py configure
```

## 常用命令

初始化或更新本地 profile：

```bash
python3 scripts/follow_scoutx.py configure \
  --frequency daily \
  --time 09:00 \
  --language zh-CN \
  --source-mode scoutx \
  --delivery-channel in_chat \
  --topics "AI Agent,编程工具" \
  --keywords-include "OpenAI,Anthropic,Cursor" \
  --max-items 8 \
  --length short
```

切换为一手信息源：

```bash
python3 scripts/follow_scoutx.py configure --source-mode first_party
```

同时使用 ScoutX 定制优质媒体源、X 平台和播客：

```bash
python3 scripts/follow_scoutx.py configure --source-types "scoutx,x,podcast"
```

分别设置两类消息上限：

```bash
python3 scripts/follow_scoutx.py configure --max-first-party-items 6 --max-scoutx-items 4
```

查看当前 profile：

```bash
python3 scripts/follow_scoutx.py show-profile
```

查看服务配置：

```bash
python3 scripts/follow_scoutx.py show-service
```

使用本地 feed fixture 预览，避免依赖网络：

```bash
python3 scripts/follow_scoutx.py preview --feed-file /path/to/feed.json
```

输出适合 OpenClaw `--announce` 的确定性 digest：

```bash
python3 scripts/follow_scoutx.py deliver --feed-file /path/to/feed.json
```

生成 OpenClaw cron 命令：

```bash
python3 scripts/follow_scoutx.py show-openclaw-cron
```

安装 OpenClaw cron 前先 dry run：

```bash
python3 scripts/follow_scoutx.py install-openclaw-cron
```

确认 dry run 输出中的 `delivery_diagnostics.stable` 为 `true` 后再执行：

```bash
python3 scripts/follow_scoutx.py install-openclaw-cron --apply
```

如果 `delivery_diagnostics` 显示 `channel=last`，默认不要直接安装。默认稳定策略是保存明确的飞书投递目标：

```bash
python3 scripts/follow_scoutx.py configure --delivery-channel feishu --delivery-target ou_xxx
```

如果目标是当前聊天，使用主会话 system event 路径，而不是硬编码 `last`：

```bash
python3 scripts/follow_scoutx.py install-openclaw-cron --main-session-system-event
python3 scripts/follow_scoutx.py install-openclaw-cron --main-session-system-event --apply
```

只有在已经确认当前 OpenClaw 安装可以稳定路由 `last` 时，才加 `--allow-channel-last`。如果需要替换已有任务，优先使用：

```bash
python3 scripts/follow_scoutx.py install-openclaw-cron --replace-existing --apply
```

它会先用 `openclaw cron list --json` 过滤出 id，再用 `openclaw cron rm <id>` 删除。

## 开发约定

- 优先保持 Python 标准库实现，除非有明确理由引入依赖。
- 不要把后端服务地址、token、raw filter 等配置暴露给普通用户流程。
- 不要让普通用户配置 X API、播客 RSS、podcast transcript 服务；这些属于中心 feed/operator 责任。
- 如果 `service.json` 指向 placeholder 域名，应把它视为 operator packaging 问题，不要向终端用户索要 feed URL。
- 修改 OpenClaw cron 逻辑时，保持 Feishu 外部投递必须使用明确的 `--channel feishu --to <target>`。
- 当前聊天投递使用 `--session main --system-event`，不要默认使用 `--channel last`。
- `--main-session-system-event` 只允许用于当前聊天；如果 `delivery.channel=feishu`，应直接拒绝安装并要求显式 `--channel feishu --to <target>`。
- 混合源 recurring delivery 默认只生成一个 cron job；旧版遗留的 `-first-party` / `-scoutx` 任务在 `--replace-existing` 时应一并清理。
- 替换旧定时任务时使用 `--replace-existing`，不要依赖 name 更新；OpenClaw 资源管理以 id 为准。
- 不要把 Feishu 定时任务配置成 `delivery.mode=session` + `sessionTarget=isolated`；isolated session 没有可继承的当前聊天通道。
- 不要默认安装 `channel=last` 的 recurring job；`install-openclaw-cron --apply` 应要求显式 Feishu target 或 `--main-session-system-event`，除非用户主动传 `--allow-channel-last`。
- 默认 recurring delivery 使用 `deliver`；但如果 `language` 是 `zh-CN` 或 `bilingual` 且启用了一手信息源（`x` / `podcast`），应优先切到 `prepare-digest`，否则一手信息源会保持原文语言。
- 如果 `language=zh-CN` 且走 `prepare-digest`，一手信息源的标题和摘要都必须中文化，而不是只把分区标题翻成中文。
- 如果走 `prepare-digest`，必须保持“每个选中 item 对应一个编号条目”；禁止把第 4 条以后折叠成“更多动态/更多精选内容”。
- 做验收或排查时，优先读取 `preview --json` / `deliver --json` 原始字段；不要额外生成 `AI相关: ✅/⚠️/❌`、`边界内容` 之类的二次判断标签。
- 做“真实执行”验收时，优先读取 `deliver --json` 的 `group_counts` 与 `errors`，不要自己推断 first_party / scoutx 条数。
- 选中的 feed 只要有一个拉取失败，默认可以降级成 partial result，但必须显式暴露 `status=partial`、`failed_source_types` 和 `errors`；不要把抓取故障误报成过滤后 0 条。
- prompt 文案应保持直接、紧凑、面向 builder，不要加入营销口吻。
- 修改脚本行为时，同步检查 `SKILL.md` 和 `README.md` 是否需要更新。

## 验证建议

本仓库当前没有独立测试框架。做脚本改动时至少运行：

```bash
python3 -m py_compile scripts/follow_scoutx.py
```

对涉及 profile 或 digest 输出的改动，建议用临时 home 和本地 feed fixture 验证：

```bash
FOLLOW_SCOUTX_HOME=/tmp/follow-scoutx-test python3 scripts/follow_scoutx.py configure --topics "AI Agent" --language zh-CN
FOLLOW_SCOUTX_HOME=/tmp/follow-scoutx-test python3 scripts/follow_scoutx.py preview --feed-file /path/to/feed.json
```

对 OpenClaw cron 相关改动，先检查 dry run 或 JSON 输出：

```bash
python3 scripts/follow_scoutx.py show-openclaw-cron --json
python3 scripts/follow_scoutx.py install-openclaw-cron
```

## Git 注意事项

仓库可能存在用户未提交改动。工作前查看：

```bash
git status --short
```

不要回滚自己没有创建的改动。只修改当前任务需要的文件。
