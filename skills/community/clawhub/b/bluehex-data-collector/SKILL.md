---
name: bluehex-data-collector
version: 0.1.3
description: BlueHex AI PM 项目
license: MIT-0
---

# BlueHex Data Collector · 会话持续录制

把每个 OpenClaw 龙虾与用户（包括飞书直聊和群聊）的全量对话与交换媒体，**每 2 小时一批**：脱敏 → 写本地 markdown → 滚动 daily PR 推送到 `BlueFocusContentUniverse/bluehex-data-monitoring`。

> 这是 ai-pm 体系的**数据底座**：监控保持**纯原始捕获**，项目识别、retroactive 标签、vector RAG、SOP 自改进全部由 ai-pm skill 在下游消费时完成。

## 用途与边界

**做什么**
- 每 2h 扫描本机 OpenClaw transcript（`~/.openclaw/agents/main/sessions/`），把窗口期内的对话提取出来。
- 用 `process-catl.py --monitor` 脱敏：凭证字面值**就地**改 `<credential>`，PII 掩码，high/medium/toxic 只 flag 不丢 turn。
- 按 `<slug-name>_<open_id>/YYYY-MM-DD/HHMM-<host>.md` 写入。
- 滚动 daily PR：每 host 每天一个分支 `monitoring/<host>/YYYY-MM-DD`，2h flush 累加 commits，一天一个 PR（fork + cross-repo）。

**不做什么 / 别人做**
- ❌ 项目标签（`project:`） → 下游 ai-pm 蒸馏时做。原因：2h 时间片切割导致上下文丢失，session-level 也不够可靠。
- ❌ vector 索引 / RAG → ai-pm 监听 git repo 起 indexer。
- ❌ 每 turn 实时拦截 → OpenClaw 无 per-turn hook（仅 `agent:bootstrap` / `command` / 会话生命周期 + 注册式 JS 插件），不走这条路。
- ❌ 群聊里 bot 自己跨用户合并 → 群聊 sender 仅 prompt 文本前缀 `ou_<32hex>:`，每条独立归属。

## 触发词

「录制对话」「monitoring 数据」「bluehex data 底座」「持续录制」「推到 monitoring 仓库」「2h 数据沉淀」

## 装机入口

```bash
# 1. 安装 skill（一次性）
clawhub install bluehex-data-monitoring   # 或本仓直接 cp 到 ~/.openclaw/workspace/skills/

# 2. 首次安装（交互式：host 名 + GitHub user + 注册 2h cron）
bash ~/.openclaw/workspace/skills/bluehex-data-monitoring/scripts/install-cron.sh

# 3. 手动测试一次（dry-run，不真发 PR）
bash ~/.openclaw/workspace/skills/bluehex-data-monitoring/scripts/record.sh --dry-run
```

## 架构

```
~/.openclaw/agents/main/sessions/
  ├─ <sid>.jsonl              ← direct: type=message 行直接读
  └─ <sid>.trajectory.jsonl   ← group: prompt.submitted 文本里解析 ou_<32hex>: 前缀
            │
            ▼
   ┌──────────────────┐
   │ extract-turns.py │ direct + group 两条路径 → 统一 turns JSON
   └──────────────────┘
            │
            ▼  按 open_id 分组
   ┌──────────────────┐  ┌────────────────────┐
   │  resolve-name.sh │←→│ lark-cli contact   │（缓存到 ~/.openclaw/cache/）
   └──────────────────┘  └────────────────────┘
            │  open_id → display name
            ▼
   ┌─────────────────────────────────┐
   │ process-catl.py --monitor       │  全量录制：凭证就地改、PII 掩码、敏感打 flag
   └─────────────────────────────────┘
            │  sanitized text + report
            ▼
   <slug-name>_<open_id>/YYYY-MM-DD/HHMM-<host>.md   ← 写文件（frontmatter）
            │
            ▼
   preflight.sh --sync-only → fetch upstream + push fork main
            │
            ▼
   commit on monitoring/<host>/YYYY-MM-DD branch → push fork → ensure PR open
            │
            ▼
   watermark 推进（仅在 PR push 成功后）
```

## 数据布局

仓库 `BlueFocusContentUniverse/bluehex-data-monitoring`：

```
qizhang_ou_2165be6a.../
  ├─ 2026-06-01/
  │   ├─ 0015-<host>.md          ← 一个 2h flush
  │   ├─ 0215-<host>.md
  │   ├─ media/
  │   │   └─ om_<id>.png         ← 交换媒体（outbound + 有落盘的 inbound）
  │   └─ ...
  └─ 2026-06-02/
shejinming_ou_8d3f.../
  └─ ...
group_oc_8da3.../                ← 群聊（无法逐用户解析时的兜底）
  └─ ...
```

每个 `.md` 的 frontmatter：

```yaml
---
user_name: Qi Zhang
user_open_id: ou_2165be6a...
window: ["2026-06-01T00:15+08:00", "2026-06-01T02:15+08:00"]
host: <host-id>
chat_type: feishu:direct         # 或 feishu:group:oc_<chatid>
session_ids: [f5b13ff7-..., ...]
message_ids: [om_x100b50dd7..., ...]
sensitivity: medium              # process-catl.py 给的标签
flagged: true                    # high_hits 或 is_toxic 命中
credentials_redacted: 0
pii_masked: 3
high_hits: ["中创新航"]
---

## conversation

[user 09:51:02] [REDACTED → sanitized content]
[assistant 09:51:12] ...
...
```

## 每 2h 流程（record.sh）

每次 cron 触发：

1. 读 watermark：`~/.openclaw/state/bluehex-monitor/watermark.txt`（首次 = 2h 前）。
2. 扫 `~/.openclaw/agents/main/sessions/<uuid>.jsonl`，**白名单**：跳过 `*.trajectory*`、`*.lock`、`sessions.json`、`.usage-cost-cache.json`、`*.deleted.*`、`*.reset.*`、`*.bak-*`、`*.clobbered.*`。
3. 每个 candidate session：调 `extract-turns.py --jsonl <p> --trajectory <p> --since <ws> --until <now>` → JSON 数组 of turns。
4. 把所有 turns 按 `open_id` 分桶（direct → sessionKey；group → 行内 `ou_xxx:` 前缀）。
5. 每桶：调 `resolve-name.sh <open_id>` 拿 slug-name → 组装 markdown 文本 → `process-catl.py --monitor` 脱敏 → 写文件。
6. 调 `preflight.sh --sync-only` 同步 fork 上 main。
7. `git checkout -B monitoring/<host>/$(date +%F)`（首次 flush）/ `git checkout monitoring/<host>/$(date +%F)`（同一天后续）；`git add … && git commit -m "record(<host>): <ts> — N users, M turns"`。
8. `git push -u origin monitoring/<host>/<date>`；如果当天还没 PR：`gh pr create --repo BlueFocusContentUniverse/bluehex-data-monitoring --base main --head <gh-user>:monitoring/<host>/<date> ...`；浏览器兜底。
9. 仅在以上**全部成功**后才推进 watermark。失败 → watermark 不动 → 下一次自动重做该窗口。

## 凭证 / 鉴权

- **GitHub fork 推送**：每台 host 用**自己**的 GitHub 身份（fork + cross-repo PR），不共享凭证。SSH key 已 `ssh -T git@github.com` 验证。
- **PR 创建**：`gh auth login` / `glab` / `GH_TOKEN`，三者皆无则浏览器兜底。
- **lark-cli**：必须 `contact:user.base:readonly` scope（用于 `open_id → display name`）。
- **BlueAI relay**：`process-catl.py --monitor` 跑分类用，配置同 `catl-harness-pr`（`~/.openclaw/openclaw.json` 里的 `models.providers.openai-compat.apiKey`）。
- **任何 token 出问题**：联系金明（@Dr-xiaoming），不要自己改、不要在 commit/PR/聊天里贴。

## 故障排查

- record.sh 没生成 PR → 查 watermark 是否动了；查 `~/.openclaw/state/bluehex-monitor/record.log`。
- "open_id 解析为空 name" → lark-cli 没拿到 `contact:user.base:readonly` scope，或没 `lark-cli auth login --as user`。folder 会兜底为 open_id-only。
- "群聊 sender 全是 unknown" → 新版 OpenClaw 改了 prompt 格式（不再 `ou_<32hex>:` 前缀），看 `references/transcript-schema.md` 是否需要扩展 `extract-turns.py` 的 `inbound_meta` 分支。
- "PR 没自动开" → 没装 `gh`/`glab`，浏览器兜底链接已经打到 log 里；或当天分支已存在但首条 commit 没建 PR，手动 `gh pr create` 一次后续会自动复用。
- "cron 没触发" → `openclaw cron list`；`openclaw cron runs --id <jobid>`。

## Bundled resources

- `scripts/record.sh` — 2h cron 主入口
- `scripts/extract-turns.py` — direct + group transcript 解析
- `scripts/process-catl.py` — **bundled** from `catl-harness-pr` v0.6.0+（带 `--monitor`）
- `scripts/resolve-name.sh` — `open_id → display-name`（lark-cli + 缓存）
- `scripts/preflight.sh` — 环境检查 + fork 同步（adapted from catl-harness-pr）
- `scripts/setup-fork.sh` — fork 创建 / remote 布局（adapted）
- `scripts/install-cron.sh` — 首次安装向导，注册单条 `15 */2 * * *` cron
- `references/recorder-pipeline.md` — record.sh 流程详解
- `references/transcript-schema.md` — OpenClaw transcript 格式备忘（direct 与 group 差异）
- `references/monitor-sanitization.md` — `process-catl.py --monitor` 在本 skill 中的行为速查

## CHANGELOG

### v0.1.3 (2026-06-02)

- 更名：ClawHub skill slug `bluehex-data-monitoring` → `bluehex-data-collector`，display name 改为 "BlueHex Data Collector"（旧 slug 保留为 redirect）。仅 skill 标识更名——GitHub 数据仓 `BlueFocusContentUniverse/bluehex-data-monitoring`、cron/state 名称、脚本内部引用均保持不变。

### v0.1.2 (2026-06-02)

- 修复 `setup-fork.sh`：新版 `gh` 在带 `<repo>` 参数时拒绝 `--remote`（即使 `--remote=false` 也算“已提供”），去掉该 flag，只保留 `--clone=false`
- `setup-fork.sh` 新增空仓自愈：upstream 没有任何 commit 时（GitHub 不能 fork 空仓）自动写一个初始 `README.md` 把 `main` 建出来，再 fork
- **移除 `HEX_RECORDER_USER_OPEN_ID`（业务员 open_id）配置**：不再在安装时询问、不再写 `.env`、不再做 cron 失败告警私聊。录制本身已把每条会话的 open_id 内联进数据，无需单独指定接收人；失败只写 `record.log`。cron 改用 `--no-deliver` 静默运行。这也彻底消除了下一条 stdin 串扰 bug 的影响面
- 修复 `install-cron.sh` 交互输入：`ask()` 改为只从 `/dev/tty` 读，绝不消费 stdin——此前被管道/复用的 stdin 会把答案串错（曾把 open_id 填成无关字符串 `xiaoming`）。非交互安装请用环境变量 `HEX_RECORDER_HOST` / `HEX_RECORDER_GH_USER`

### v0.1.0 (2026-06-01)

- 初始发布 — bluehex AI PM 项目数据底座
- 直读 transcript（无 hook）+ direct/group 双解析路径
- `--monitor` 脱敏（bundled process-catl.py from catl-harness-pr v0.6.0）
- fork + cross-repo PR，rolling daily PR per host
- watermark 推进仅在 PR 成功后，避免数据丢失
- folder = `<slug-name>_<open_id>`（lark-cli 解析 name）；ai-pm 在下游做项目标签、向量与蒸馏
