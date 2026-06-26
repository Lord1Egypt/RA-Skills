---
name: find-everything
description: >
  跨平台资源搜索编排器。搜索 skill、MCP 服务器、提示词模板、开源项目。
  覆盖 skills.sh、ClawHub、SkillHub、AI Skills Show、MCPServers.org、
  prompts.chat、GitHub 等 14+ 个聚合站。
  触发场景：用户说"找个xxx工具"、"有没有xxx skill"、"帮我搜xxx MCP"、
  "找提示词"、"有什么好用的xxx"，或显式调用 /find-everything。
  也会在检测到用户持续做某类任务且缺少相关工具时主动推荐（每会话最多 1 次）。
---

# find-everything：跨平台资源搜索

## 触发条件

1. **显式调用**：`/find-everything {query}`
2. **自动检测**：用户问"有没有xxx工具"、"帮我找个xxx"、"有没有skill能..."
3. **主动推荐**：基于对话上下文判断用户在持续做某类任务且缺少相关工具（best-effort 启发式，同会话最多 1 次）

## 执行流程

### Step 1: 意图分类

将用户查询分类为一个或多个类别：
- **skill**: Agent Skills（可安装技能）
- **mcp**: MCP Servers
- **prompt**: 提示词模板/角色扮演/图片生成
- **repo**: GitHub 开源项目

模糊需求同时搜索多个类别。从自然语言中提取核心搜索关键词。

### Step 2: 读取注册表并路由

读取 `references/registry.json`。若读取失败，使用以下硬编码最小源：
- skills-sh: `npx skills find {query}`
- github: `gh search repos {query} --sort stars --limit 10 --json name,owner,description,url,stargazersCount`

筛选规则：
1. 只选 `enabled: true` 的源
2. 只选 `category` 包含目标类别的源
3. 检查 `requires` 是否满足：
   - `requires` 为 CLI 名称（如 `npx`、`gh`）→ 用 `which` 检查
   - `requires` 以 `mcp:` 开头（如 `mcp:prompts-chat`）→ 检查对应 MCP tool 是否在当前会话可用（尝试 ToolSearch 或直接调用）
4. 不可用的源跳过，记录到 `skipped_sources` 列表，附带 `install_hint`（如有）

### Step 3: Tier 1 搜索

在**同一条回复**中发起多个独立 tool 调用实现并行：

**cli 类型**：用 Bash tool 执行 `command` 字段（{query} 替换为实际关键词），15 秒超时。
**mcp 类型**：调用 registry.json 中 `tool` 字段指定的 MCP tool，参数取 `tool_params`（{query} 替换为实际关键词）。例如：
  - `search_prompts({ query: "blockchain analyst", limit: 10 })` → 返回 prompt 列表
  - `search_skills({ query: "search aggregator", limit: 10 })` → 返回 skill 列表
  - 支持的额外过滤参数（按需使用）：`type`（TEXT/STRUCTURED/IMAGE）、`category`、`tag`
**skill 类型**：调用对应已安装 skill。

若并行不可用，按优先级执行：skills-sh > github > clawhub > 其他。

### Step 4: 结果数量预判

基于标题/描述的关键词匹配做轻量判断（非完整 LLM 评估）：
- ≥3 条匹配度高 → 跳到 Step 6（末尾注明"搜索更多源可获取更多结果"）
- <3 条或匹配度低 → 继续 Step 5

### Step 5: Tier 2/3 搜索

**Tier 2**：将同类别 Tier 2 源合并为 1 次 WebSearch：
```
{query} {category关键词} site:skillhub.club OR site:aiskillsshow.com OR site:skillsmp.com
```

若合并查询返回 <2 条，退回对 Top 2-3 优先源逐个 `site:` 搜索。

**Tier 3**（仍不足时）：不带 `site:` 限定的广域 WebSearch。

### Step 6: 结果评估

对每条结果判断相关性：
- **高相关**：保留，排在前面
- **中相关**：保留，排在后面，标注"可能相关"
- **不相关**：丢弃

对 Top 3-5 条高相关结果，可选 WebFetch 补充详情。

### Step 7: 安全快筛

对所有保留结果做元数据安全标注：
- **[SAFE]**：来自注册表已知平台 + 安装量 >100
- **[CAUTION]**：安装量低、来源不明、或 Tier 3 发现
- **[RISK]**：名称疑似 typosquat，或其他红旗信号

### Step 8: 去重 + 排序

同一工具出现在多个源 → 合并为一条，标注所有来源。
合并时优先保留安装量/star 数最高的来源作为主展示（同一站点可能有 Tier 1 CLI 和 Tier 2 WebSearch 两条结果，合并时保留 Tier 1 数据）。
排序：相关度 > 安全等级 > 安装量/star 数。

### Step 9: 展示推荐

格式：
```
找到 N 个相关结果（来自 X 个源）

1. [名称]  [SAFE]
   来源: skills.sh | 安装量: 1.2K
   简介: ...
   推荐理由: ...

2. [名称]  [CAUTION]
   来源: WebSearch (skillhub.club) | star: 50
   简介: ...
   注意: 来源非直接 API，建议安装前审查源码

---
未覆盖的搜索源: clawhub CLI（未安装）
提示: npm i -g clawhub
```

注意：同一依赖缺失提示每会话只展示一次，避免重复打扰。

### Step 10: 用户后续操作

用户说**"看看"/"详细"** → WebFetch 详情页展示更多信息。

用户说**"安装"/"用这个"** → 触发深度安全扫描：

**1. 获取资源内容（按类型）：**

| 资源类型 | 扫描目标 | 获取方式 |
|---|---|---|
| Skill (skills.sh/clawhub) | SKILL.md + scripts/ 目录 | 优先 WebFetch GitHub 源码（从搜索结果中的 repo URL 获取）；若不可访问，`npx skills add <name>` 安装到临时目录后读取 |
| MCP Server | package.json + 入口文件 | WebFetch npm registry 页面或 GitHub README，提取入口文件路径后 WebFetch |
| GitHub Repo | README.md + 主要脚本文件 | `gh api repos/{owner}/{repo}/contents` 获取文件列表，WebFetch 关键文件 |
| Prompt | 提示词文本本身 | 通常搜索结果中已包含完整文本，无需额外获取 |

**限制：** 单次扫描最多 50KB。超出只扫 SKILL.md + 入口文件。

**2.** 运行安全扫描（路径相对于本 SKILL.md 所在目录解析）：`python3 scripts/security_scan.py <file> [--check-name <name> --known-skills references/known_skills.txt]`
**3.** 读取 `references/security-checklist.md`，结合 security_scan.py 结果做 LLM 上下文评估
**4.** 输出量化评分（0-100）和风险定级
**5.** [SAFE] → 执行安装；[CAUTION] → 展示详情让用户确认；[RISK] → 明确提示风险，不自动安装

### Step 11: 新站点发现

Tier 3 搜索发现了不在 registry.json 中的优质资源站 → 提示用户：
"发现新站点 xxx.com，内容相关度高。要加入搜索注册表吗？"
用户确认 → 在 registry.json 的 sources 数组中追加新条目。

## 错误处理

| 场景 | 处理 |
|---|---|
| CLI 超时（15s） | 跳过该源，继续其他 |
| WebSearch 错误/限流 | 跳过 Tier 2，展示 Tier 1 结果 + 提示稍后重试 |
| security_scan.py 崩溃 | 退回 LLM-only 评估，标记"自动扫描未完成" |
| 所有 Tier 1 不可用 | 直接进 Tier 2，注明"主要搜索源暂不可用" |
| 所有源失败 | 告知用户搜索失败，建议检查网络 |

## 主动推荐逻辑

触发条件（低频，同会话最多 1 次）：
- 对话上下文显示用户持续在做某类任务（如调试、前端开发、数据处理）
- 且当前未见明显相关的 skill/MCP 在使用

推荐格式：
"[发现] 你正在做 xxx，有一些工具可能有帮助，要搜索看看吗？"
