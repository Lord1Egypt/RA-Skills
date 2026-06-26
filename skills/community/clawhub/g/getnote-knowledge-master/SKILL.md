---
name: getnote-knowledge-master
description: |
  Get笔记 · 六步抄作业版。复刻 AI 大神卡帕西的知识管理方法论，融合 Get笔记 API + @getnote/cli 实现一键式六步知识管理流程。

  **何时激活：**
  (1) 用户提到"六步抄作业"、"卡帕西知识管理"、"知识库抄作业"
  (2) 用户要执行完整知识管理流程（建库→存入→整理→搜索→反哺→体检）
  (3) 用户一句话触发多步骤知识管理操作，如"帮我把最近AI进展整理一下存到知识库"
  (4) 用户提到"Get笔记升级版"、"知识沉淀"、"知识复利"
  (5) 常规 Get笔记 操作（保存/搜索/知识库/标签）但带有工作流意味（批量、自动化、定期）

  **默认主阵地："得到"知识库（topic_id: `eYzMmvnm`）**
  张公子的主要工作环境在此知识库，六步法的所有操作默认以此为上下文，除非用户明确指定其他知识库。

  本 Skill 基于 Get笔记 API + @getnote/cli，通过 orchestrated 多步骤流程实现六步法。
---

# Get笔记 · 六步抄作业版

## 核心理念

> "AI 已把'怎么做'的门槛变得极低，'做什么'反而比'怎么做'更有价值。"

六步法固化进 Skill 后，张公子只需要**一句话**，整套知识管理流程自动跑完。

## 工具配置

### 优先使用 @getnote/cli

**已验证可用的 CLI 命令（优先使用）：**

```bash
# 认证状态
getnote auth status

# 语义搜索 ← 核心！解决 recall API 404 问题
getnote search "<关键词>" --kb eYzMmvnm --limit 5 -o json

# 列出知识库
getnote kbs -o json

# 列出某知识库全部笔记
getnote kb eYzMmvnm --all -o json

# 存入内容（链接/文字/图片）
getnote save <url|文字> --tag <标签> -o json
# 链接笔记自动轮询抓取，完成后返回完整内容

# 给笔记加标签
getnote tag add <note_id> <标签>

# 查看单条笔记
getnote note <note_id> -o json

# 新建知识库
getnote kb create <名称> --desc <描述>
```

**环境变量（自动从 openclaw.json 读取）：**
- `GETNOTE_API_KEY` → openclaw.json skills.entries.getnote.apiKey
- `GETNOTE_CLIENT_ID` → openclaw.json skills.entries.getnote.env.GETNOTE_CLIENT_ID

### 原始 API（CLI 不可用时的降级方案）

- Base URL: `https://openapi.biji.com`
- Int64 ID 必须做字符串化处理

## 六步法快速索引

| 步骤 | 指令关键词 | 说明 |
|------|----------|------|
| 第1步 | "建库"、"创建知识库" | 30 秒搭建目标知识库 |
| 第2步 | "存到"、"记一下"、"收藏" | 零门槛存入内容 |
| 第3步 | "整理"、"自动归类" | 全自动整理与打标签 |
| 第4步 | "搜一下"、"对比分析"、"梳理" | 向知识库提问（用CLI语义搜索） |
| 第5步 | "存成笔记"、"反哺"、"沉淀" | 反哺知识库形成复利 |
| 第6步 | "体检"、"报告" | 每周知识库体检 |

---

## 指令路由

### 自然语言路由规则

```
"建" + 知识库名称     → 第1步（创建知识库）
URL 或 "存到"        → 第2步（存入内容）
"整理"               → 第3步（自动整理）
"搜"、"对比"、"梳理"  → 第4步（语义搜索与分析）
"存成笔记"、"反哺"    → 第5步（沉淀结果）
"体检"、"报告"       → 第6步（知识库体检）
```

---

## 第1步：创建知识库

**优先使用 CLI：**
```bash
getnote kb create <知识库名称> --desc <用途描述>
```

**示例：**
```
帮我建"内容素材库"知识库，用途是"收集做内容用的案例、数据、观点"
```
→ `getnote kb create 内容素材库 --desc 收集做内容用的案例、数据、观点`

---

## 第2步：存入内容

**优先使用 CLI：**
```bash
getnote save <url|文字|图片路径> --tag <标签> -o json
```

**特点：** 链接笔记自动异步抓取内容，CLI自动轮询直至完成，无需手动等待。

| 类型 | 检测信号 | 处理方式 |
|------|---------|---------|
| 链接 | URL格式 | `getnote save <url> --tag <标签>` |
| 文字 | 普通文本 | `getnote save "<文字>" --tag <标签>` |
| 图片 | 图片路径 | `getnote save <path> --tag <标签>` |

**链接存档示例：**
```
把这个链接存到内容素材库：https://...
```
→ `getnote save https://... --tag 内容素材`

**语音/录音存档：**
> ⚠️ CLI `save` 不支持直接上传音频。录音笔记存为文字笔记，在内容中写入 AI 生成的摘要。

**批量存入：**
多条内容可一次性存入，每条之间换行，CLI自动逐条处理。

---

## 第3步：自动整理

**优先使用 CLI：**
```bash
# 获取知识库内全部笔记
getnote kb <topic_id> --all -o json

# 给笔记打标签
getnote tag add <note_id> <标签>
```

**执行流程：**
1. `getnote kb <topic_id> --all -o json` 获取该知识库全部笔记
2. 语义判断归属分类，生成整理报告
3. 用 `getnote tag add` 补充缺失标签

**整理报告格式：**
```
📋 整理报告 · {知识库名}
- 笔记总数：X 篇
- 分类归入：
  · AI技术进展：X 篇
  · 成长与心理：X 篇
  · 社会观察：X 篇
  · 产出记录：X 篇
- 标签补全：X 篇
```

---

## 第4步：语义搜索与分析

> ✅ **已解决**：使用 `getnote search` CLI 命令，完美替代返回404的 recall API。

**优先使用 CLI：**
```bash
getnote search "<关键词>" --kb <topic_id> --limit <n> -o json
```

**基础搜索：**
```
在内容素材库里搜一下：关于 AI Agent 的最新进展
```
→ `getnote search "AI Agent最新进展" --kb eYzMmvnm --limit 5 -o json`
→ 解析JSON结果，自然语言整理输出

**对比分析（最体现知识库价值）：**
```
对比分析内容素材库里关于"大模型开源 vs 闭源"的正反观点
```
→ `getnote search "开源闭源优势" --kb eYzMmvnm --limit 10 -o json`
→ `getnote search "开源闭源劣势" --kb eYzMmvnm --limit 10 -o json`
→ 语义分类正方/反方观点，输出对比框架

**全局脉络梳理：**
```
梳理一下 AI 行业观察库里关于 RAG 的全局脉络
```
→ `getnote search "RAG" --kb eYzMmvnm --limit 10 -o json`
→ 按时间线组织，输出脉络图谱

**搜索结果示例格式：**
```
🔍 找到 X 条相关笔记：

第1条：{标题}（{日期}）
  {语义相关性最高的片段摘要}

第2条：{标题}（{日期}）
  {次相关内容片段}
```

---

## 第5步：反哺知识库

**优先使用 CLI：**
```bash
getnote save "<标题>" --title "<标题>" --tag <标签> -o json
```

**沉淀分析结果：**
```
把刚才关于 AI Agent 的分析结果存成新笔记，标题叫"AI Agent 发展脉络"
```
→ `getnote save "<完整分析内容>" --title "AI Agent 发展脉络" --tag AI,沉淀 -o json`

**沉淀创作产出：**
```
把我刚写的文章存到内容素材库
```

---

## 第6步：每周体检

**优先使用 CLI：**
```bash
# 统计所有知识库
getnote kbs -o json

# 统计某知识库笔记数
getnote kb <topic_id> --all -o json
```

**执行流程：**
1. `getnote kbs -o json` → 获取知识库列表 + 笔记数
2. 各知识库逐一 `getnote kb <topic_id> --all -o json` → 语义分析内容覆盖
3. 识别内容空白，生成体检报告
4. `getnote save` → 存入体检报告

**体检报告格式：**
```
🏥 知识库体检报告 · {知识库名}

📊 总览
- 笔记总数：X 篇
- 知识库数量：X 个

📂 分类索引
- AI技术进展（X篇）
- 成长与心理（X篇）
- 社会观察（X篇）
- 产出记录（X篇）

❌ 内容空白
- 尚未覆盖：X、X、X

💡 优化建议
1. ...
2. ...
```

---

## 错误处理

| 错误场景 | 解决方案 |
|---------|---------|
| `getnote: command not found` | `npm install -g @getnote/cli` |
| 鉴权失败 | `getnote auth login --api-key <key>` 或检查环境变量 |
| QPS 限流 | CLI自动处理，链接存档有内部重试；写操作建议2-5秒间隔 |
| 笔记不存在 | 确认note_id正确性，用 `getnote note <id> -o json` 验证 |
| 知识库操作失败 | 回退到 `GET /resource/knowledge/list` API |

---

## 分级归档原则

收到"整理全部笔记"指令时，按以下优先级决定是否移入"得到"知识库：

| 优先级 | 内容类型 | 处理 |
|--------|---------|------|
| ⭐⭐⭐ | AI/大模型/知识管理/用户产出（日志简报/Skill笔记）| 必须移入 |
| ⭐⭐ | 深度文章解读（心理学/经济学/科技分析）| 值得移入 |
| ⭐ | 轻量内容/无正文ref笔记 | 不移入 |

**注意**：重复内容（同一标题多个来源）保留正文最完整的一个，其余删除。

---

## 工作流编排原则

1. **先问目标，再执行**：用户说"帮我整理"，先确认是哪个知识库
2. **多步骤自动串接**：第3步整理完成后主动问"是否存入索引笔记"
3. **闭环提醒**：搜索结果后提醒"是否把分析沉淀成新笔记"
4. **批量优先**：多篇内容尽量批量处理，避免多次 API 调用触发限流
5. **CLI优先**：所有操作优先用 `getnote` CLI，API作为降级方案

---


## 每日知识沉淀（Cron 专用）

> ⚠️ **此节为 Cron 任务专用流程，普通六步法用户请忽略。**

### 核心原则

执行每日知识沉淀时，必须遵循以下关键规则：

1. **必须轮询所有知识库**：不能只查 `eYzMmvnm`（"得到"库），必须用 `getnote kbs -o json` 获取全部知识库列表，**逐一**对每个知识库执行 `kb <topic_id> --all -o json`，筛选目标日期的笔记
2. **必须使用 `getnote search` 补充全局搜索**：单独用 `kb --all` 只能查特定库，存在笔记分散在不同库的情况。必须用 `getnote search "YYYY-MM-DD" --limit 20 -o json` 做全局补充检索
3. **写入结果放在"得到"知识库**：日志简报最终写入 `eYzMmvnm`（"得到"知识库），输出笔记的 tag 设为 `日志简报`

### 标准流程

**第一步：获取全部知识库列表**
```bash
getnote kbs -o json
```
获取所有知识库的 `topic_id`，构建列表 `[EJl3xRj0, yYv9rmDn, eYzMmvnm, ...]`

**第二步：轮询每个知识库**
```bash
# 对每个 knowledge_base 执行
getnote kb <topic_id> --all -o json
# 筛选 created_at 包含目标日期的笔记（如 2026-04-24）
```

**第三步：全局搜索补充**
```bash
# 用日期做关键词全局搜索
getnote search "YYYY-MM-DD" --limit 20 -o json
```

**第四步：读取本地记忆文件**
```bash
# 检查记忆文件
~/.openclaw/workspace/memory/YYYY-MM-DD.md
~/.openclaw/workspace/memory/YYYY-MM-DD-tech-news.md
```

**第五步：生成日志简报**

汇总所有来源数据，按标准格式生成日志简报（参考上方格式）。

**第六步：三端归档**


| 平台 | 操作 |
|------|------|
| 本地文件 | 写入 `~/.openclaw/workspace/日志管理/YYYY-MM-DD-日志简报.md` |
| Get笔记 | `getnote save <content> --title "日志简报 YYYY-MM-DD | 张公子" --tag 日志简报` → 写入 `eYzMmvnm` |
| 飞书文档 | 创建 docx 并写入内容，链接同步到飞书群 |
| 飞书知识库 | 在个人知识库 wiki 中创建对应节点 |


**第七步：发送完成通知**

通过飞书群发送通知，包含：数据统计、核心发现摘要、三端链接。
