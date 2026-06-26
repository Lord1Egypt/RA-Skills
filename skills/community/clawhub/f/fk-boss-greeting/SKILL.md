---
name: fk-boss-greeting
description: Boss直聘打招呼自动化工具。用于搜索职位并向HR主动打招呼。当用户要求在Boss直聘(老板直聘)上发打招呼、投递简历、搜索职位并沟通时使用。支持：搜索Java/架构师/技术经理等职位，自动过滤黑名单公司(阿里、百度、腾讯、字节、京东等)和无关岗位(算法、AI、测试、产品经理等)，逐个排队打招呼(间隔1秒)，记录已打招呼避免重复。
---

# Boss 直聘打招呼自动化

## 前置条件

本工具依赖 `boss` CLI，默认路径 `~/.local/bin/boss`。

### 登录

从 Chrome 浏览器读取登录态（用户需先在 Chrome 登录 zhipin.com）：

```bash
~/.local/bin/boss login --cookie-source chrome
```

**禁止使用二维码登录**。如凭证过期或异常，先 `boss logout` 再重新登录。

### 工具版本

安装路径：`~/.local/bin/boss`（通过 uv tool 安装）
升级命令：

```bash
cd /Users/huguiqi/Public/javaWorkspace/github/boss-cli && git pull && uv tool install --reinstall .
```

## 打招呼流程

### 1. 读取过滤规则

过滤规则文件：[references/filter-rules.json](references/filter-rules.json)

规则包括：
- **公司黑名单**：阿里、百度、腾讯、字节、京东、拼多多、滴滴、快手、小米、华为、蚂蚁等
- **职位黑名单**：算法、AI、测试、产品经理、初级、实习、大模型等
- **搜索关键词**：Java架构师、技术经理、软件工程师、研发经理、微服务架构师等（共10个）
- **城市优先级**：上海 > 北京 > 苏州 > 杭州 > 无锡
- **每次上限**：30 个
- **打招呼间隔**：1 秒

### 2. 搜索职位

对每个关键词 × 每个城市依次搜索，间隔 1.5 秒：

```bash
~/.local/bin/boss search "Java架构师" --city 上海
```

过滤逻辑：
1. 排除公司黑名单中的公司
2. 排除职位黑名单中的关键词（算法、AI、测试、产品经理等）
3. 只保留 Java 相关职位（包含 java、架构师、技术经理、微服务、spring、技术负责人、研发经理、服务端）
4. 去重（按 securityId）

### 3. 逐个排队打招呼

**禁止使用 `batch-greet`**（会并行发送，触发风控）。必须逐个执行：

```bash
~/.local/bin/boss greet <securityId>
```

每次间隔 **1 秒**，每轮最多 **30 个**。

搜索和打招呼均可使用脚本：[scripts/boss_auto_greet.sh](scripts/boss_auto_greet.sh)

### 4. 限速处理

如遇 "频繁" 或 "限速" 错误：
- 等待 30 秒后重试
- 如遇 code=32（账户封禁）或 code=36（异常行为），停止操作并告知用户

## 去重机制

- 每次打招呼的 securityId 记录到日志
- 同一会话内不重复打招呼
- 识别"开聊提醒"（已沟通过的）避免重复

## 注意事项

1. **不并行**：所有打招呼必须排队，逐个执行
2. **控制频率**：每次最多 30 个，避免账户被封
3. **只打 Java 相关**：过滤非 Java 的无关职位
4. **登录态**：Boss 直聘 Web 登录态有效期短，每次操作前重新执行 `boss login --cookie-source chrome`
5. **停用定时任务时**：需明确告知用户当前状态
