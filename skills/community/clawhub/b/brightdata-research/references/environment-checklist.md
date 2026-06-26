# Environment Checklist

在执行 `brightdata-research` 之前，先做这份环境自检。每项分为三类：可自动修复、需用户介入、不可修复（需降级）。

## 一、必需能力

### 1. 搜索能力

**检测：**
- MCP 方式：检查 `mcp__brightdata__search_engine` 工具是否可用
- CLI 方式：`which brightdata 2>/dev/null && brightdata --version`

**可自动修复：**
- BrightData CLI 未安装 → 可自动执行 `npm install -g @brightdata/cli`

**需用户介入：**
- MCP 方式：需要用户配置 MCP 服务器并提供 API token
- CLI 方式：需要用户运行 `brightdata login` 完成认证

**修复指引：** 见 `references/brightdata-mcp-setup.md`

MCP 和 CLI 任一可用即满足搜索能力要求。

缺失时降级：
- 不能执行"扩充候选池"模式
- 只能对用户给定名单做验证与整理

### 2. 网页抓取能力

**检测：**
- MCP 方式：检查 `mcp__brightdata__scrape_as_markdown` 工具是否可用
- CLI 方式：`brightdata scrape https://example.com`

**可自动修复：** 同搜索能力
**需用户介入：** 同搜索能力（MCP 和 CLI 共用 BrightData 账户/认证）
**修复指引：** 见 `references/brightdata-mcp-setup.md`

缺失时降级：
- 不要把搜索摘要直接当事实
- 只能给出低置信度线索，并明确说明证据不足

### 3. 飞书写入能力

**检测：**
```bash
which lark-cli 2>/dev/null && lark-cli auth status
```

**可自动修复：**
- lark-cli 未安装 → 可自动执行 `npm install -g @larksuite/cli`
- lark-cli skills 未安装 → 可自动执行 `npx skills add https://github.com/larksuite/cli -y -g`

**需用户介入：**
- 首次配置需要扫码 → `lark-cli config init`
- 首次登录需要浏览器确认 → `lark-cli auth login --recommend`
- 权限不足需要用户在飞书后台授权

**修复指引：** 见 `references/lark-cli-install-and-auth.md`

缺失时降级：
- 先输出结构化 Markdown
- 不要假装已写入飞书

### 4. 本地文件与命令执行能力

为了读写 skill、保存评测结果、执行 lark-cli 等命令，需要基础文件系统与命令执行能力。

## 二、推荐能力

### 1. subagent / Agent 能力

**检测：**
```bash
git rev-parse --is-inside-work-tree 2>/dev/null && git rev-parse HEAD 2>/dev/null
```

**可自动修复：**
- 不在 git 仓库 → 可自动 `git init`
- 没有 commit → 可自动 `git add -A && git commit -m "init"`

**需用户介入：** 无（如果允许自动初始化 git）

缺失时降级：
- 改为主代理串行执行
- 保留同样的去重与汇总纪律

## 三、执行前必查项

每次开始前按以下清单检查：

1. [ ] 搜索能力是否可用
2. [ ] 网页抓取能力是否可用
3. [ ] lark-cli 是否已安装
4. [ ] lark-cli 是否已认证
5. [ ] 若要写飞书，是否已知道目标 doc_id 或目标文档 URL
6. [ ] 若要历史去重，是否能读取已有飞书文档内容
7. [ ] 若要用 subagent/worktree，git 仓库和 HEAD 是否正常
8. [ ] 当前任务是"继续追加"还是"新建文档"

## 四、快速判断

### 可以完整执行标准流程
满足：
- 搜索 + 抓取 + 飞书写入都可用
- 已知目标文档或能创建目标文档
- 需要时可读取历史文档做去重
→ 进入 **Mode A**

### 需要先修复再执行
任一情况成立：
- lark-cli 未安装（可自动修复）
- git 仓库不存在（可自动修复）
→ 进入 **Mode B**，修复后转 Mode A

### 只能执行降级流程
任一情况成立：
- BrightData MCP 未配置（需用户 API token）
- lark-cli 已安装但用户未完成扫码授权
- 没有历史文档内容且任务要求历史去重
→ 明确告知用户哪一步能做、哪一步做不了
