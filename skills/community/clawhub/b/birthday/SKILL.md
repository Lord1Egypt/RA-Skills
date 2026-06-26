---
name: birthday
description: 处理中文生日提醒场景，支持从中国身份证号码提取生日、按农历或公历保存生日、为每条记录设置独立的提前提醒天数，并生成当天或未来几天的提醒结果。当用户要实现、维护或运行“农历生日提醒”“身份证生日解析”“生日台账管理”“生日到期检查”这类任务时使用此技能。
---

当任务涉及中文生日提醒时，优先使用这个技能，尤其是下面几类场景：

- 需要把生日按农历保存，并在每年自动换算到当年的公历提醒日期
- 需要同时支持农历和公历两种记录方式
- 需要为每条记录单独设置提前提醒天数，而不是全局统一配置
- 需要本地脚本来维护生日数据、列出最近生日、检查提醒结果

## 主要资源

- Python 主脚本：`{baseDir}/scripts/birthday_manager.py`
- JavaScript 主脚本：`{baseDir}/scripts/birthday_manager.js`
- Node.js 包定义：`{baseDir}/package.json`
- 默认通知配置：`{baseDir}/data/notification.json`
- 数据格式说明：`{baseDir}/references/data-format.md`

## 快速用法

先确认 Python 3 或 Node.js 可用，然后直接运行对应主脚本。

```bash
python3 {baseDir}/scripts/birthday_manager.py --help
node {baseDir}/scripts/birthday_manager.js --help
npm --prefix {baseDir} run help
```

默认数据文件：

```text
{baseDir}/data/birthdays.json
```

也可以通过 `--data-file` 指定其他路径。

## 常见任务

### 1. 从身份证添加生日

推荐优先使用统一入口 `add`。脚本会自动判断传入值是身份证还是生日文本；身份证默认会把公历生日转换成农历后保存，并默认提前 1 天提醒。

```bash
python3 {baseDir}/scripts/birthday_manager.py add "张三" 11010519491231002X
node {baseDir}/scripts/birthday_manager.js add "张三" 11010519491231002X
```

如果想按公历保存：

```bash
python3 {baseDir}/scripts/birthday_manager.py add "张三" 11010519491231002X --calendar solar
node {baseDir}/scripts/birthday_manager.js add "张三" 11010519491231002X --calendar solar
```

如果想提前 3 天提醒：

```bash
python3 {baseDir}/scripts/birthday_manager.py add "张三" 11010519491231002X --remind-before 3
node {baseDir}/scripts/birthday_manager.js add "张三" 11010519491231002X --remind-before 3
```

### 2. 手动添加生日

手动添加农历生日：

```bash
python3 {baseDir}/scripts/birthday_manager.py add "李四" "农历:1992-8-15"
node {baseDir}/scripts/birthday_manager.js add "李四" "农历:1992-8-15"
```

手动添加公历生日：

```bash
python3 {baseDir}/scripts/birthday_manager.py add "王五" "公历:1988-10-01" --remind-before 7
node {baseDir}/scripts/birthday_manager.js add "王五" "公历:1988-10-01" --remind-before 7
```

如果是农历闰月生日，显式加上 `--leap-month`，例如：

```bash
python3 {baseDir}/scripts/birthday_manager.py add "赵六" "农历:8-15" --leap-month
```

### 3. 查看记录

```bash
python3 {baseDir}/scripts/birthday_manager.py list
python3 {baseDir}/scripts/birthday_manager.py list --upcoming --days 30
python3 {baseDir}/scripts/birthday_manager.py next

node {baseDir}/scripts/birthday_manager.js list
node {baseDir}/scripts/birthday_manager.js list --upcoming --days 30
node {baseDir}/scripts/birthday_manager.js next
```

### 4. 检查提醒

按每条记录自己的 `remind_before_days` 检查是否需要提醒。命中后默认通知当前 agent；如果需要企业微信、Webhook 等渠道，配置 `notification.json` 后再运行。

```bash
python3 {baseDir}/scripts/birthday_manager.py check
node {baseDir}/scripts/birthday_manager.js check
```

指定检查日期，便于测试：

```bash
python3 {baseDir}/scripts/birthday_manager.py check --today 2026-03-13
node {baseDir}/scripts/birthday_manager.js check --today 2026-03-13
```

如果要做批处理或定时任务，直接读取脚本输出即可。

## 默认配置变量

默认通知配置文件是 `data/notification.json`。开箱即用时会启用 `agent` 渠道，`email` 渠道默认关闭。

启用邮件时，优先填写或导出这些环境变量：

- `BIRTHDAY_SMTP_HOST`
- `BIRTHDAY_SMTP_PORT`
- `BIRTHDAY_SMTP_USERNAME`
- `BIRTHDAY_SMTP_PASSWORD`
- `BIRTHDAY_EMAIL_FROM`
- `BIRTHDAY_EMAIL_TO`

如果只需要当前 agent 收到提醒，保持默认配置即可。

## OpenClaw 定时器

当数据文件从 0 条变成 1 条，且脚本检测到当前环境是 openclaw 时，会额外输出一行：

```text
OPENCLAW_AUTOMATION_SUGGESTION {...}
```

调用这个 skill 的 AI 应读取这行 JSON，并为 openclaw 创建一个每日定时检查自动化。默认建议每天 09:00 执行 `check`。

## 工作规则

1. 优先保留结构化数据，不要只在 Markdown 里手工维护生日表。
2. 从身份证提取到的是公历生日。
3. 当用户没有特别说明时，统一 `add` 入口对身份证默认转成农历保存，对手输生日默认按农历解析。
4. 每条记录默认 `remind_before_days=1`，但允许单独覆盖。
5. 对农历生日，提醒时必须先换算为目标年份的公历日期，再计算剩余天数。
6. `check` 命中后默认通知当前 agent；其他通知渠道必须通过配置文件显式配置。
7. 输出给用户时，同时显示“存储口径”和“本次实际提醒的公历日期”，避免混淆。

## 数据与实现说明

- 数据字段见 `references/data-format.md`
- Python 与 JavaScript 脚本共用同一种 JSON 数据结构
- `package.json` 不包含第三方依赖，适合本地直接运行
- 脚本内置了 1900-2099 年的农历换算表，不依赖第三方库
- 身份证支持 18 位，也兼容 15 位老身份证
- 如果遇到超出农历换算表范围的年份，应直接报错，不要默默给出错误结果

## 修改建议

如果用户后续要接入企业微信、短信、邮件或系统通知：

1. 保持 `birthday_manager.py` 的数据层与提醒计算层不变
2. 在外层增加发送器脚本，只消费 `check` 的结果
3. 不要把发送逻辑硬编码进生日计算核心逻辑
