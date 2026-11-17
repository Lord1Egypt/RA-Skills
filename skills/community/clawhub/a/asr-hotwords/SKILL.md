# ASR Hotwords — OpenClaw Skill

## 功能

从 OpenClaw 所有 agent 的对话记录中自动挖掘热词/歧义词表，供 ASR 模型提升语音转录准确性。

**Pipeline**: 提取所有 session 对话 → 本地热词挖掘（jieba 分词 + LLM 精炼） → 输出歧义词表 → 自动导出 hotwords.md

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

将 skill 安装到 `~/.openclaw/skills/asr-hotwords/`。

```bash
# 如果是从其他位置安装
cp -r <source> ~/.openclaw/skills/asr-hotwords/
```

### Step 2: 旧版迁移（自动）

运行迁移脚本，自动检测旧版 per-agent 安装并合并数据：

```bash
cd SKILL_DIR && python3 migrate.py
```

迁移脚本会：
- 扫描所有 agent workspace 下的旧版 `asr-hotwords` 或 `asr-personal-hotwords` 目录
- 合并 `output/vocab_*.json` 历史挖掘结果到新位置（不覆盖）
- 迁移 `.installed` / `.cron_configured` 标记文件
- 迁移 `hotwords.md`
- 在旧目录写入 `MIGRATED.md` 标记

如果没有旧版安装，脚本会提示"无需迁移"并跳过。

### Step 3: 安装依赖

```bash
pip3 install -r SKILL_DIR/requirements.txt --quiet
```

### Step 4: 验证 OpenClaw LLM 配置

检查 `~/.openclaw/openclaw.json` 中是否存在有效的 provider 配置（apiKey + baseUrl）。

### Step 5: 测试运行

用前一天的数据跑一次完整 pipeline，确认端到端流程正常：

```bash
cd SKILL_DIR && nohup bash run.sh > run.log 2>&1 &
```

运行完成后会自动导出 hotwords.md。可通过 `tail -f SKILL_DIR/run.log` 查看进度。

### Step 6: 设置安装标记

```bash
touch SKILL_DIR/.installed
```

安装完成，通知用户 skill 已就绪。

## 首次使用引导

当用户首次触发此 skill 时（通过触发条件中的关键词），检查 SKILL_DIR 下是否存在 `.cron_configured` 文件：

**如果 `.cron_configured` 不存在（首次使用）：**

在执行挖掘之前，先向用户提问：

> "这是首次使用热词挖掘 skill。是否需要设置**每日定时执行**？（推荐：每天凌晨自动挖掘前一天的对话热词并更新 hotwords.md）"

- **用户同意**：询问执行时间（默认 02:00），创建 OpenClaw cron 定时任务（sub-agent 方式），然后创建 `.cron_configured` 文件
- **用户拒绝**：直接创建 `.cron_configured` 文件（标记为已询问，不再重复提问）

```bash
touch SKILL_DIR/.cron_configured
```

**如果 `.cron_configured` 已存在：** 跳过引导，直接执行。

## 手动执行

### 默认：挖掘前一天

```bash
cd SKILL_DIR && nohup bash run.sh > run.log 2>&1 &
```

### 指定日期

```bash
cd SKILL_DIR && nohup bash run.sh --date 2026-04-26 > run.log 2>&1 &
```

### 指定日期范围

```bash
cd SKILL_DIR && nohup bash run.sh --start 2026-04-20 --end 2026-04-26 > run.log 2>&1 &
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

## DMWork 语音纠错上下文注入

挖掘完成后，run.py 会自动通过 `openclaw gateway call agent` 发送结构化消息给 agent。

agent 收到消息后必须执行：
1. 读取 SKILL_DIR/hotwords.md
2. 调用 `dmwork_management(action="voice-context-update", content=文件内容)`
3. 调用 `dmwork_management(action="voice-context-read")` 验证注入成功

如果是手动执行挖掘，agent 在汇报结果后也应主动执行上述注入步骤。

## 配置

编辑 `config.yaml`：
- `extract.agents`：要提取的 agent 列表（`["*"]` 为全部，或指定如 `["main", "claude"]`）
- `extract.max_content_len`：单条消息最大字符数
- `extract.min_freq`：最低词频阈值

LLM API key 和模型信息自动从 `~/.openclaw/openclaw.json` 读取，无需手动配置。

## 锚点词表机制

- **首次运行**：anchors 为空
- **后续运行**：自动加载 `output/` 目录下所有历史 vocab 结果作为 anchors（合并去重）
- 词表只增不减，持续积累
