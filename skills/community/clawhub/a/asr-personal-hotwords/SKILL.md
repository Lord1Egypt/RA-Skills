# ASR Personal Hotword Miner — OpenClaw Skill

## 功能

从 OpenClaw 对话记录中自动挖掘热词/歧义词表，供 ASR 模型提升语音转录准确性。

**Pipeline**: 提取 session 对话 → 调用远端 asr-corrector 服务 → 输出歧义词表 → 自动导出 hotwords.md

## 触发条件

用户说以下类似的话时触发此 skill：
- "挖掘对话中的热词"
- "提取对话歧义词"
- "跑一下热词挖掘"
- "更新热词表"

## 安装流程

当用户要求安装/启用此 skill 时，按以下步骤执行：

**注意：以下所有路径中的 `SKILL_DIR` 指此 SKILL.md 所在目录（即 skill 的根目录）。执行时用 `read` 工具获取本文件路径，取其父目录即可。**

### Step 1: 安装 Skill

将 skill 安装到当前 agent 的工作空间 skills 目录下。

**安装位置解析步骤：**
1. 获取当前 session 的 agent 名称（如 `main`、`doctor`）
2. 读取 `~/.openclaw/openclaw.json`，在 `agents.list` 中找到该 agent 的 `workspace` 配置；如果 agent 没有独立 `workspace`，则使用 `agents.defaults.workspace`
3. 将 skill 安装到 `{workspace}/skills/asr-personal-hotwords/`

**示例：**
- main agent（workspace: `~/.openclaw/workspace`）→ `~/.openclaw/workspace/skills/asr-personal-hotwords/`
- doctor agent（workspace: `~/.openclaw/workspace-doctor`）→ `~/.openclaw/workspace-doctor/skills/asr-personal-hotwords/`

### Step 2: 检查依赖

```bash
pip3 install requests pyyaml --quiet
```

### Step 3: 验证远端服务

```bash
curl -s http://124.174.11.138:65000/health
```

如果服务不可用，通知用户并中止安装。

### Step 4: 验证 OpenClaw LLM 配置

检查 `~/.openclaw/openclaw.json` 中是否存在有效的 provider 配置（apiKey + baseUrl）。

### Step 5: 测试运行

用前一天的数据跑一次完整 pipeline，确认端到端流程正常：

```bash
cd SKILL_DIR && bash run.sh
```

运行完成后会自动导出 hotwords.md。

### Step 6: 记录热词表路径

在当前 agent 工作空间的 `TOOLS.md` 中追加热词表配置（路径根据实际 workspace 动态生成）：

```markdown
## ASR 热词（歧义词）表
- **路径**: {workspace}/skills/asr-personal-hotwords/hotwords.md
- **用途**: 使用 ASR 模型转录语音时，自动读取此文件注入 prompt
- **更新**: 手动执行或定时自动更新
```

其中 `{workspace}` 替换为 Step 1 中解析到的实际路径。

### Step 7: 询问执行方式

向用户提问：

> "热词挖掘 skill 安装成功！默认为手动执行模式。
> 是否需要设置**每日定时执行**？（推荐：每天凌晨自动挖掘前一天的对话热词并更新 hotwords.md）"

**如果用户同意定时执行：**

1. 询问用户期望的执行时间（默认建议：每天 02:00）
2. 使用 OpenClaw cron 创建定时任务，任务内容：
   - 以 sub-agent 方式执行（`sessions_spawn`, `runtime: "subagent"`, `mode: "run"`）
   - 任务步骤：
     1. `cd SKILL_DIR && bash run.sh`
     2. 将结果摘要推送到 Telegram + 飞书
   - 执行完 sub-agent 自动销毁

**如果用户拒绝：**

仅确认安装完成，后续用户手动触发即可。

## 手动执行

当用户触发此 skill 时：

### 默认：挖掘前一天

```bash
cd SKILL_DIR && bash run.sh
```

### 指定日期

```bash
cd SKILL_DIR && bash run.sh --date 2026-04-26
```

### 指定日期范围

```bash
cd SKILL_DIR && bash run.sh --start 2026-04-20 --end 2026-04-26
```

### 仅导出热词表（不重新挖掘）

```bash
cd SKILL_DIR && bash run.sh --export-only
cd SKILL_DIR && bash run.sh --export-only -f json -o hotwords.json
cd SKILL_DIR && bash run.sh --export-only -f csv -o hotwords.csv
cd SKILL_DIR && bash run.sh --export-only -f txt
```

执行完成后，向用户汇报：
- 提取了多少条消息
- 挖掘出多少条热词
- 展示 top 10 热词

## 输出文件

| 文件 | 说明 |
|------|------|
| `output/vocab_{date}.json` | 原始挖掘结果（按日期存档） |
| `hotwords.md` | 热词表（每次运行自动导出，prompt 格式，供 ASR 模型直接使用） |

## 配置

编辑 `config.yaml`：
- `server_url`：asr-corrector 远端服务地址
- `extract.agents`：要提取的 agent 列表（`["self"]` 为当前 agent，`["*"]` 为全部）
- `extract.max_content_len`：单条消息最大字符数
- `extract.min_freq`：最低词频阈值

LLM API key 和模型信息自动从 `~/.openclaw/openclaw.json` 读取，无需手动配置。

## 锚点词表机制

- **首次运行**：anchors 为空
- **后续运行**：自动加载 `output/` 目录下所有历史 vocab 结果作为 anchors（合并去重）
- 词表只增不减，持续积累
