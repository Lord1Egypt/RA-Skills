---
name: cron-creator
description: 【针对飞书优化】定时任务创建指引，专门针对飞书、尤其是多 Agent 场景进行优化，解决定时任务不稳定问题。
required_tools:
  - openclaw CLI
  - read
required_files:
  - openclaw.json
  - current_chat_context (user_id/chat_id)
---

# 🤖 定时任务创建专家

声明：本工具依赖 openclaw CLI 执行任务。在执行命令前，你可能需要通过上下文或 `read` 工具获取 `user_id`/`chat_id` 以及 `openclaw.json` 中的多 Agent 配置 (`channels.feishu.accounts`)。这些信息是配置飞书定时任务中的必要参数，否则任务不能触发。**如果你发现自己当前没有权限读取这些信息，或者上下文中缺失这些信息，请务必先向用户询问补全，绝不可自行编造。**

## 🎯 应用场景与触发条件
当用户表达出需要在未来某个时间点或按照特定周期进行提醒、执行任务时触发。
- **典型触发语**：“5分钟后提醒我做xxx”、“每天8点提醒我xxx”、“工作日每两个小时提醒我喝水”等。

---

## 🛑 核心铁律
1. **唯一创建方式**：必须使用 CLI 指令 `openclaw cron add` 创建任务。
2. **禁止直接手写**：创建时**严禁**直接修改 `cron/jobs.json`（仅在修改/更新已有任务时允许）。
3. **禁用系统功能**：**严禁**使用系统默认 `crontab`，**严禁**使用延时脚本 (`sleep` 等) 触发任务。

---

## ⚙️ 执行逻辑与参数拆解

在生成命令前，必须严格按照以下四个步骤收集并处理参数：

### 步骤 1：信息内容拆解
* **提取诉求 `{message}`**：整理用户的具体需求。
    * 如果任务很简单，则提取一句话作为 message。
    * 如果用户的诉求比较明确且清晰，就直接将用户的指令作为 message，换行符用 `\n` 代替。
    * 如果任务较为复杂，需将其拆分为多个步骤（1、2、3...），然后合并为一段话，换行符必须使用 `\n` 代替。
* **生成名称 `{cron_name}`**：提取简短、有代表性的纯英文/拼音名称。

### 步骤 2：时间规则拆解
判断任务是“一次性任务”还是“周期性任务”，默认用户所指时间均为 **东八区 (Asia/Shanghai)**。

* **A. 一次性任务**
    * 必须计算出目标执行的精确时间，并将其转换为 **UTC 标准时间**。
    * 格式必须为 `YYYY-MM-DDThh:mm:ssZ`（例如北京时间 2026-02-02 00:00:00，应转换为 `2026-02-01T16:00:00Z`）。
    * 使用参数：`--at "<UTC时间>"` 和 `--delete-after-run`（执行后即删除）。

* **B. 周期性任务**
    * 需根据需求生成标准的 5 位 Cron 表达式 `{cron_expression}`。
        * *Cron 规则参考：`* * * * *` (分 时 日 月 星期)。例如：每天早上8点为 `0 8 * * *`，工作日每两小时为 `0 */2 * * 1-5`。*
    * 必须指定时区参数，如果用户没有指定时区则为东八区：`--tz "Asia/Shanghai"`。
    * **必须** 添加防并发打散参数：`--stagger`（随机设置 `30s` 到 `5m` 之间的值，如 `30s`, `1m`, `2m` 等）。
    * 使用参数：`--cron "<Cron表达式>"`。

### 步骤 3：发送目标与渠道拆解
分析指令的来源环境，确定消息发送的渠道参数：

* 一、**判断来源**：
    分析指令的触发环境，**必须完整明确以下三个维度的信息**：
    1. **渠道归属**：来自后台 Terminal 还是飞书等 IM 渠道？
    2. **对话类型**（若为飞书）：当前是 **私聊** 还是 **群聊**？
    3. **部署模式**（若为飞书）：当前系统是 **单 Agent** 还是 **多 Agent** 配置？
* 二、如果指令来源于飞书，**必须**完成以下两项数据提取：
    1. **获取目标 ID**：
        * **私聊场景** -> 提取当前对话中用户的 `user_id`（必须以 `ou_` 开头）。
        * **群聊场景** -> 提取当前群聊对应的 `chat_id`（必须以 `oc_` 开头）。
    2. **判定 Agent 模式**：
        * 读取 `openclaw.json` 文件。
        * 检查 `channels.feishu` 下是否存在 `accounts` 字段：**有**则为多 Agent，**无**则为单 Agent。
* 三、如果为后台触发或者非飞书 IM 渠道按其对应默认规则处理。

根据上述判断，生成对应的目标参数集：
* **情形 A：后台触发**
    * 参数：`--announce`
* **情形 B：飞书单 Agent 私聊**
    * 参数：`--announce --channel feishu --to "{user_id}"`
* **情形 C：飞书单 Agent 群聊**
    * 参数：`--announce --channel feishu --to "{chat_id}"`
* **情形 D：飞书多 Agent 私聊**
    * 参数：`--announce --channel feishu --to "user:{user_id}" --account "{account}"` *(注意：此处的 to 参数必须加上 `user:` 前缀)*
* **情形 E：飞书多 Agent 群聊**
    * 参数：`--announce --channel feishu --to "chat:{chat_id}" --account "{account}"` *(注意：此处的 to 参数必须加上 `chat:` 前缀)*

### 步骤 4：基础运行时配置
所有任务必须附带以下基础运行参数：
- `--session isolated`（**绝对不能**选择 main）
- `--wake now`

---

## 🛠️ 指令合成与示例

综合以上 4 个步骤，最终生成的指令结构如下（请根据实际情况组合参数）：

### 示例 1：一次性任务（飞书多 Agent 环境群聊）
**场景**：用户在飞书（多Agent环境，account为`assistant`）要求“明早8点提醒我开早会”。
```bash
openclaw cron add \
  --name "morning_meeting_reminder" \
  --at "2026-03-01T00:00:00Z" \
  --session isolated \
  --message "记得参加早会哦！" \
  --wake now \
  --delete-after-run \
  --announce \
  --channel feishu \
  --to "chat:oc_1a2b3c4d5e6f" \
  --account "assistant"
```

### 示例 2：周期性任务（飞书单 Agent 环境私聊）
**场景**：用户在飞书要求“每天晚上10点提醒我写日报”。
```bash
openclaw cron add \
  --name "daily_report" \
  --cron "0 22 * * *" \
  --stagger 2m \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "该写日报啦！\n1. 总结今日进度\n2. 规划明日目标\n3. 归纳并调用 message 工具发送给用户" \
  --wake now \
  --announce \
  --channel feishu \
  --to "ou_9z8y7x6w5v4u"
```

### 示例 3：周期性任务（后台触发）
**场景**：系统管理员在后台要求“每 2 个小时检查一次系统日志”。
```bash
openclaw cron add \
  --name "check_system_logs" \
  --cron "0 */2 * * *" \
  --stagger 30s \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "请执行系统日志常规检查。" \
  --wake now \
  --announce
```

