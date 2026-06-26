---
name: eyes
description: 全球热点事件监控与影响分析。覆盖全球局势、地缘冲突、重大政策、创新技术等可能影响经济、市场和投资的事件，并按行业、汇率、大宗商品链路分析影响。含定时消息推送与全渠道分段推送能力。用于 Cron 定时推送热点摘要(早8点/晚8点/整点扫描)。
triggers:
  - 今日热点
  - 热点摘要
  - 大眼看世界
  - 今晚热点
  - 今日大事
  - 国际市场
  - 全球热点
  - 大眼
  - eyes

  - 升级Eyes
  - 更新Eyes
  - 帮我升级
---

# 👁️ Eyes · 大眼看世界

## 📋 功能概览

Eyes 是一款 **全球热点事件监控与影响分析工具**，自动追踪全球政治、经济、科技、市场重大事件，量化分析对 A 股/港股/美股的行业影响。

**核心功能：**
- **🌍 全球实时监控** — 覆盖地缘冲突、央行政策、贸易制裁、科技突破、自然灾害等
- **🔴 P0/P1/P2 三级分级** — 自动判断事件严重程度，重大事件优先推送
- **📊 市场影响分析** — 事件→行业→汇率/大宗/板块→具体标的，完整影响链路
- **⏰ 定时推送** — 早8点(过去12h)、整点扫描(9:00-19:00)、晚8点(全天复盘)
- **📈 A股关联** — 行业轮动分析，结合用户偏好板块（半导体/AI/新能源/光模块等）
- **🔮 明日关注** — 大盘判断+板块机会+风险提示
- **🔍 本地脚本** — eyes-utils.py 自动去重、分级、影响分析、格式化

## 行为规则

**触发即执行**:用户说出任意触发词(大眼/大眼看世界/今日热点等),自动搜索全球热点+市场分析输出汇总。不等待用户进一步指令。
- 时段自动判断:8:00-12:00按早间流程,12:00-20:00按晚间流程,其余时段按整点扫描
- 无新事件也输出当日综览(不低于简单说明)

## 时区规则

- 执行前先读取 `USER.md` 中的 `Timezone:` 字段，获取用户的本地时区
- 所有时间（当前时间、事件时间、时间窗口判断）都转换为该时区显示
- 例：Timezone=Asia/Shanghai 且当前 UTC 05:00 → 报告为「北京时间周日13:00」
- 若 USER.md 未配置 Timezone，则回退到 `date +%Z` 或 `TZ` 环境变量

## 核心能力

1. 全球热点实时监控 + 市场影响分析(按P0/P1/P2分级)
2. 定时推送:早8:00/9:00-19:00整点/20:00
3. A股行业轮动&影响链路分析(按用户偏好:半导体/AI/光模块/新能源/中小市值科技)
4. **本地脚本**:scripts/eyes-utils.py 文件维护+搜索模板+事件分级+影响分析+格式化

## 事件分级

| 级别 | 定义 | 响应 |
|------|------|------|
| P0 | 全球性重大事件（战争/制裁/崩盘/自然灾害/央行重大决策） | 立即推送 |
| P1 | 重大政策/经济数据/行业突破/市场剧烈波动 | 限时窗口内推送 |
| P2 | 常规事件/局部影响/一般行业动态 | 直推 |
| P3 | 无关噪音 | 丢弃 |

> 初步分级: `eyes-utils.py classify` 基于关键词给出。模型在初步分级基础上修正。

## 时间窗口

| 场景 | 窗口 |
|------|------|
| 早间(08:00) | 过去12h(前一晚20:00→今早8:00) |
| 整点扫描(9:00-19:00) | 过去1h |
| 晚间(20:00) | 当日全天(8:00-20:00) |

## 推送格式

品牌标记: `👁️ Eyes · 大眼看世界`
所有定时推送使用通用分段推送（不限字数），**使用 `**粗体**` 标记标题和关键信息**，方便阅读。

统一格式参考：
```
👁️ **Eyes · 大眼看世界** 🌙 晚8点

**📊 今日要闻**
**🔴 P1 事件标题**
事件描述+影响分析→影响行业/板块/标的

**🔴 P1 另一事件**
事件描述+影响分析

**🟡 P2 常规事件**
描述（可多条合并）

**📈 A股收盘**
大盘概括+板块轮动+资金流向

**🔮 明日关注**
大盘判断+板块机会+个股关注+风险提示
💬 想关注什么方向的股票？
```

## 通用分段推送（全渠道）

所有定时推送若内容超长，使用 `openclaw message send` 分段发送，自动适配当前渠道（Feishu/Telegram/Discord/Signal等）。

### 获取投递目标
```bash
# 从cron配置中获取自己的投递目标（channel:target）
my_name="eyes-evening"  # 替换为当前cron的名字
cron_data=$(openclaw cron list --json)
target=$(echo "$cron_data" | python3 -c "import json,sys;d=json.load(sys.stdin);next((j['delivery']['to'] for j in d['jobs'] if j['name']=='$my_name'), 'last')")
channel=$(echo $target | cut -d':' -f1)
target_id=$(echo $target | cut -d':' -f2-)
```

### 发送单条消息（仅备用）
```bash
openclaw message send --channel "$channel" --target "$target_id" --message "消息内容" --json
```

### 分段发送（标准方式，使用 send-segments）
**必须使用 `eyes-utils.py send-segments`**，禁止手动逐段调用 `openclaw message send`。

JSON通过 argv 传入（避免 stdin 被占用）：
```bash
# 生成内容 + 发送（单行命令，避免shell转义问题）
formatted=$(python3 skills/eyes/scripts/eyes-utils.py format --scene hourly --segments)
python3 skills/eyes/scripts/eyes-utils.py send-segments "{\"content\": \"$formatted\", \"channel\": \"feishu\", \"target\": \"ou_98247e4c0c80df2da79f25d0b65a6d61\"}"
```

或在模型调用时直接构造 JSON（最可靠）：
```bash
python3 skills/eyes/scripts/eyes-utils.py send-segments '{"content":"第一段内容\n---SEGMENT---\n第二段内容","channel":"feishu","target":"ou_xxx"}'
```

### 完整推送流程
1. 生成完整内容（不限字数，不再是以前那种单条推送，不需要压缩长度）
2. **合并为 3-5 段**：不要按段落逐条发。把相关内容合并，每段 500-1000字（最长不超过1500字）。每段要写丰富，事件要写明影响链路（→ 影响什么行业/板块/个股）。
3. **加粗排版（参考bigA风格）**：使用 `**粗体**` 标记分段标题（如 `**📊 今日要闻**`）、事件级别（如 `**🔴 P1**`）和事件标题，结构清晰如：
```
**🔴 P1 事件标题**
详细描述 + → 影响分析

**🟡 P2 事件**
详细描述
```
4. **【强制规则】**：必须调用 `eyes-utils.py send-segments` 发送内容，**禁止**手动调用 `openclaw message send`。`send-segments` 命令内置自动解析 `---SEGMENT---` 标记、分段发送、失败重试（3次），模型只需生成内容+调命令。具体调用方式：
   ```bash
   # JSON通过argv传入（最可靠）
   python3 skills/eyes/scripts/eyes-utils.py send-segments '{"content":"完整内容（含---SEGMENT---分隔）","channel":"feishu","target":"ou_98247e4c0c80df2da79f25d0b65a6d61"}'
   ```
5. **【发送校验】**：`send-segments` 命令本身内置重试机制（3次/段），调用完成后检查返回的 `sent` 字段是否等于 `total`。若发送失败，模型不得直接回复确认，必须上报错误。
6. 最终回复只允许输出一句话确认（如 ✅ 已发送），**禁止**将完整内容作为会话回复输出。

> 无需降级回退，`openclaw message send` 是本机gateway调用，不会失败

> 无需关心用户用什么渠道，gateway自动处理所有通道适配

## 用户手动触发

用户说出触发词（今日热点/大眼看世界/全球热点等）时，在当前对话中执行：
1. `python3 skills/eyes/scripts/eyes-utils.py clean` 获取已有事件列表
2. `python3 skills/eyes/scripts/eyes-utils.py templates --scene [时段]` 获取搜索模板
3. 按模板搜索(2次)
4. `eyes-utils.py dedup` 去重 → `classify` 分级 → `impact` 影响分析
5. 模型修正分级 + 填充分析
6. `eyes-utils.py format --scene [时段] --segments --manual` 生成分段框架（手动触发时不带时间标签）
   - 输出按 `---SEGMENT---` 分隔，段数自动适配
   - **解析规则**：`---SEGMENT---` 仅用作分隔标记，解析后**必须剔除**（不发送给用户），每段内容纯净无分隔符
7. message send 分段推送
8. **手动触发输出约束**：内容合并≤3段，总字数≤1500字，搜索精简为1-2次，避免超时
9. **【发送校验】**：推送完成后检查本轮是否调用过 `openclaw message send`，若未曾调用则立即补发完整内容后再输出确认

## 用户升级

用户说出「升级Eyes/更新Eyes/帮我升级」时，在当前对话中执行：
1. 执行 `clawhub update eyes`（不带 `--no-input`，用户可在对话中看到确认提示）
2. 若提示已是最新版 → 回复「✅ Eyes 已是最新版本」
3. 若执行更新成功（输出含 "updating" 或版本变化）→ 读取 `skills/eyes/references/cron-install-shell.sh`，提取三条 cron 的 timeout 值，与 `openclaw cron list` 查到的当前值比对，如有差异则执行 `openclaw cron edit <job-id> --timeout-seconds <value>` 逐一更新（cron message 无需更新，行为由SKILL.md驱动）
4. 回复确认：如「✅ Eyes 已升级到 x.x.x，cron 已同步」

## 定时器配置

用户说「帮我安装」→ cron add 3个job，**全部通过通用分段推送**（全渠道适配，不限字数）：
- 先获取当前对话的渠道和目标（如 feishu:ou_xxx），通过 `openclaw directory` 或会话上下文确定
- 然后执行 `openclaw cron add` 时带上 `--channel <渠道> --to <目标>`，不能只用 `--announce`（新实例无历史会话时 `--announce` 会找不到投递目标）
- 模板见 `references/cron-templates.json`
- 安装完成后创建标记文件 `workspace/memory/eyes-installed`

## 工作流程

### 通用前置（每次触发先执行）
1. `python3 skills/eyes/scripts/eyes-utils.py clean` 清理已发送事件
2. 交易日检查: 非交易日跳过A股分析
3. 版本检查: 读取origin.json检查更新

### 核心工作流（三个场景通用）
1. 脚本: `eyes-utils.py templates --scene [morning/hourly/evening]` 获取搜索模板
2. 搜索: 按模板2-3次
3. 去重: `eyes-utils.py dedup`
4. 分级: `eyes-utils.py classify`
5. 影响分析: `eyes-utils.py impact`
6. 模型修正分级
7. 格式化: `eyes-utils.py format --scene [场景] --segments`
   - 输出按 `---SEGMENT---` 分隔，段数自动适配内容量
   - **解析规则**：`---SEGMENT---` 仅用作分隔标记，解析后**必须剔除**（不发送给用户），每段内容纯净无分隔符
8. **发送：必须调用 `eyes-utils.py send-segments`**，自动解析 `---SEGMENT---` 并逐段发送，失败自动重试3次/段
9. **【发送校验】**：检查 `send-segments` 返回的 `sent==total`。若不相等，立即重试仍未成功则输出 `⚠️ 推送部分失败` 并记录失败段内容，禁止直接输出完整内容作为确认

### 场景差异
| 环节 | 早8点 | 整点 | 晚8点 |
|------|------|------|------|
| 搜索次数 | 2 | 2 | 3 |
| 时间窗口 | 12h | 1h | 全天 |
| 输出 | 要闻+市场 | 仅要闻 | 要闻+市场+明日 |

### 输出约束
- **严禁输出思考过程、中间步骤、调试信息**（如"正在检查"、"读取文件"、"更新记录"、"搜索完成"、"评估标准"等）
- 只推送最终整理后的内容
- **定时推送（cron）**：通过通用分段推送（全渠道），不限总字数，每段≤1500字
- **手动触发**：通过 `openclaw message send` 分段推送，内容合并≤3段，总字数≤1500字
- 无新事件→不推送(但早/晚若无热点仍推股票关注板块)
- 末尾加互动:💬 想关注什么方向的股票?

## 附:市场影响分析

遇P0/P1事件,输出:事件→行业影响→汇率/大宗/板块→具体标的
(分析链路见 references/event-impact-matrix.md)

## 文件索引

### 运行时(workspace/memory/)
- `eyes-sent-events.md` - 已推送事件(去重)
- `eyes-retry-queue.md` - 推送失败重试
- `eyes-installed` - 安装标记
### 参考(references/)
- `cron-templates.json` - Cron job模板
- `cron-install-shell.sh` - 安装脚本
- `event-impact-matrix.md` - 事件影响分析框架
- `user-preferences.md` - 用户偏好