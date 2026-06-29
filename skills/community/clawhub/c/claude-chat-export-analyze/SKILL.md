---
name: claude-chat-export-analyze
description: 当用户要导出并分析与 Claude.ai 网页版的全部聊天历史(用于回顾、检索、复盘、生成报告、做时间线、找具体某次对话)时,加载本 skill。典型触发:用户提到 "claude 聊天记录"、"claude conversations.json"、"导出 claude 对话"、"分析我和 claude 的对话"、"翻翻以前和 claude 聊的"、"哪次 claude 跟我说过 X" 等。注意:本 skill 只覆盖 Claude.ai 网页版/claude.ai 的官方导出,不包括 Claude Code 本地 JSONL(那是不同的产物,需要另一套解析)。
---

# Claude.ai 聊天历史导出与分析

## Skill 适用边界

本 skill 专门处理 **Claude.ai 网页版(https://claude.ai)** 的官方导出流程与产物。
如果用户提到的是 **Claude Code**(`~/.claude/projects/*.jsonl`)或 **Anthropic Console / API**,本 skill **不适用**,需要走另外的解析路径。

## 第一步:引导用户导出(必走,别跳过)

不要一上来就让用户贴文件。先确认他们已经下载了 `conversations.json`。如果还没有,按下面引导走。

### 引导文案(可以直接复制给用户)

> 把你跟 Claude 的全部聊天导出,大概走这几步:
>
> 1. 打开 https://claude.ai 并登录
> 2. 左下角点你的**头像** → **Settings**
> 3. 左侧菜单选 **Privacy**
> 4. 找到 **Export your data** 区域,点 **Request export** 或 **Export data** 按钮
> 5. 同意条款,点 **Confirm**
> 6. 等几分钟到几小时,Anthropic 会把下载链接发到你**注册邮箱**
> 7. 邮箱里点链接,下载 ZIP,解压
> 8. ZIP 里面有一个 `conversations.json`,这就是你的全部聊天记录
>
> 文件可能 10MB~500MB+,内容越多越大。**别打开它,别复制粘贴,直接告诉我解压后的完整路径,我自己用工具读。**

### 关键提醒

- **必须让用户给完整文件路径**,不要让用户贴内容——这个文件通常很大(>16MB),用 `cat` / `Read` 都吃力
- 引导用户时**用第三人称解释"你自己导出"**——不要让用户以为这是 hack
- 如果用户说"我账号有 N 个项目 / Workspace",提醒他:导出的 JSON 包含**所有项目**的对话,不区分 workspace

## 第二步:校验文件格式

拿到 `conversations.json` 之后,先用 `jq` 快速校验结构。预期结构:

```bash
# 顶层是 array
jq 'type' /path/to/conversations.json
# → "array"

# session 总数
jq 'length' /path/to/conversations.json

# 单条 session 字段
jq '.[0] | keys' /path/to/conversations.json
# 预期: ["account","chat_messages","created_at","name","summary","updated_at","uuid"]
```

如果结构不符(比如顶层是 object 而不是 array,或者字段名不同),**先停下来**:
- 可能是旧版导出格式
- 可能是 Claude Code 产物(应拒绝)
- 可能是 API 抓的数据

**不要硬解析**,问用户来源。

## 第三步:按用户需求执行分析

下面是用户最常问的 7 类问题,以及对应的处理方式。

### A. "帮我找到 X 那次对话"(关键词定位)

```bash
# 关键词定位(搜 assistant 回复)
jq -r '
  .[] as $c
  | $c.chat_messages[]?
  | select(.sender == "assistant")
  | select(.text | tostring | test("关键词1|关键词2"; "i"))
  | $c.uuid + " | " + ($c.name // "(no name)") + " | " + $c.created_at + " | " + (.text | gsub("\n"; " ") | .[0:200])
' /path/to/conversations.json
```

输出形如:
```
195284e2-... | 摘要接收 | 2026-02-24T15:07:05Z | 收到,少卿...
```

然后:
1. 按**时间排序**,找最早/最晚/指定范围
2. 把命中的 session 全列出来,**不要**只给一个——让用户自己选
3. 必要时输出对应 session 的**完整消息流**(用下面 D 的方法)

### B. "按时间线看看我都聊了什么"(总览)

```bash
# 列出所有 session 的概览
jq -r '
  .[]
  | .uuid + " | " + .created_at + " | " + (.name // "(unnamed)") + " | msgs=" + (.chat_messages | length | tostring)
' /path/to/conversations.json | sort
```

然后:
- 按月/周聚合,告诉用户**活跃度趋势**
- 标出**突然活跃/突然安静**的区间
- 标出**会话特别长**(`msgs > 30`)的 session——通常说明那段时间在攻坚

### C. "找那些 assistant 给出过明确建议/方案的对话"(意图挖掘)

```bash
# 找"我建议你 / 你应该 / 我的建议"等强建议语
jq -r '
  .[] as $c
  | $c.chat_messages[]?
  | select(.sender == "assistant")
  | select(.text | test("我建议|建议你|你应该|我的建议|我推荐|最好的做法|不应该|我反对|我不接|我不建议|我不会"))
  | $c.uuid + "|" + $c.name + "|" + (.created_at) + "|" + (.text | gsub("\n"; " ") | .[0:200])
' /path/to/conversations.json
```

### D. "给我看那次对话的完整内容"(单 session 展开)

```bash
# 展开单个 session 的所有消息
jq -r '
  .[] | select(.uuid == "目标UUID")
  | .chat_messages[] | "[" + .sender + " | " + .created_at + "]\n" + .text + "\n---"
' /path/to/conversations.json
```

**输出策略**:
- session 消息数 < 20:全部输出
- 20~50:输出 + 标注"完整版 X 条消息,我可以分段"
- > 50:先给**前 5 条 + 关键转折点 + 后 5 条**,问用户要不要全量

### E. "找贯穿聊天的一个主题 / 一条线"(主题提炼)

适合场景:"我和 claude 聊过哪些次工作相关的事?""那次写过的代码都在哪几个 session?""我和 claude 讨论 X 技术是什么时候开始的?"

```bash
# 1. 跑关键词扫描(关键词从用户描述中拆出)
# 2. 命中后人工/AI 归并到主题
# 3. 按时间排序
# 4. 画时间线
```

详见 `chat-event-timeline` skill——那个 skill 就是干这个的。

### F. "导出里有多少 token / 多少钱?"(体量统计)

```bash
# session 总数
jq 'length' /path/to/conversations.json

# 消息总数
jq '[.[].chat_messages[]] | length' /path/to/conversations.json

# assistant vs human 消息分布
jq '[.[].chat_messages[] | .sender] | group_by(.) | map({(.[0]): length}) | add' /path/to/conversations.json

# 最长/最短 session
jq -r '.[] | (.chat_messages | length | tostring) + " | " + .uuid + " | " + (.name // "(no name)")' /path/to/conversations.json | sort -n
```

### G. "把这些对话变成可读的网页/报告"(可视化)

走 `visual-summary` skill(已经存在),把分析结果包装成 HTML。

## 第四步:安全与隐私(必须告知)

- 文件里**所有内容都是用户和 Claude 的对话**,可能含 API key、密码、个人敏感信息
- 解析过程中**不要把内容 echo 回给任何外部服务**——所有分析在本地完成
- 输出报告时,**默认对敏感字段打码**(邮箱、手机号、身份证、API key 模式)——除非用户明确说不用
- 提示用户:**导出文件用完后建议删除或移出工作目录**——告诉用户你已经处理完了,文件可以收起来

## 常见坑(踩过就标这里)

- ❌ **不要用 `Read` 工具读 conversations.json**——16MB+ 直接爆上下文
- ❌ **不要 cat 输出整个文件**——只会浪费 token
- ✅ **永远用 `jq` 配合 `--raw-output` / `-r` 和选择性 path 提取**
- ✅ **如果 `jq` 慢**(文件 > 100MB),考虑先按时间窗口分片:`jq '[.[] | select(.created_at >= "2026-01" and .created_at < "2026-02")]'` 然后保存中间产物
- ✅ **注意时区**——`created_at` 是 UTC,跟用户本地时间差 8 小时,引用时间时要注明"UTC 时间"或换算到用户时区
- ⚠️ **`chat_messages` 数组里 `text` 字段有时是 null**(附件/工具调用),要用 `(.text // "")` 兜底
- ⚠️ **`sender` 字段值是 `"human"` / `"assistant"`,不是 `"user"` / `"assistant"`**——别想当然
