# Known Failures and Fallbacks

这份文档记录最可能遇到的失败场景，以及该 skill 应该如何降级，而不是中途悄悄改变目标。

## 一、BrightData MCP 未配置

### 症状
- 无法调用 `mcp__brightdata__*` 系列工具
- 工具不存在或连接失败

### 正确处理
1. 检查是否已安装 BrightData CLI 作为备选：`which brightdata`
2. 如果 CLI 也不可用，告知用户需要配置 BrightData（MCP 或 CLI 二选一）
3. MCP 安装命令：`claude mcp add --transport sse brightdata "https://mcp.brightdata.com/sse?token=<your-api-token>"`
4. CLI 安装命令：`npm install -g @brightdata/cli` → `brightdata login`
5. MCP 配置完成后需要重启 Claude Code 会话
6. 降级：如果用户能提供候选名单，改做"验证与整理"模式

## 二、BrightData 已配置但搜索/抓取失败

### 症状
- MCP 工具可调用但返回错误
- CLI 命令执行失败
- API token 过期或额度用尽
- 网络连接问题

### 正确处理
- 重试一次，确认是否为临时问题
- 如果 MCP 失败但 CLI 可用（或反之），切换到另一种方式
- 如果持续失败，告知用户可能的原因（token、额度、网络）
- 已获取的部分结果仍然保留并输出

## 二.5、BrightData CLI 未安装

### 症状
- `which brightdata` 返回空
- `brightdata: command not found`

### 正确处理
1. 自动尝试安装：`npm install -g @brightdata/cli`
2. 安装后提示用户运行 `brightdata login` 完成认证
3. 如果同时 MCP 也不可用，搜索和抓取能力均不可用，需降级

## 三、lark-cli 未安装

### 症状
- `which lark-cli` 返回空
- `lark-cli: command not found`

### 正确处理
1. 自动尝试安装：
   ```bash
   npm install -g @larksuite/cli
   npx skills add https://github.com/larksuite/cli -y -g
   ```
2. 安装后提示用户运行 `lark-cli config init` 完成配置
3. 如果 npm 也不可用，告知用户需要先安装 Node.js

## 四、lark-cli 已安装但未认证

### 症状
- `lark-cli auth status` 显示未登录
- 执行文档操作时返回认证错误

### 正确处理
1. 提示用户运行 `lark-cli auth login --recommend`
2. 说明此步骤需要在浏览器中确认授权
3. 等待用户完成后重新检查状态
4. 降级：先输出完整 Markdown，标注"尚未写入飞书"

## 五、lark-cli 已认证但缺少特定权限

### 症状
- 执行操作时返回 `Permission denied` 或 `缺少权限 "xxx"`
- lark-cli 的错误信息通常会包含修复命令

### 正确处理
1. 读取错误信息中的修复命令
2. 提示用户执行该命令（如 `lark-cli auth login --scope "docs:doc:readonly"`）
3. 如果需要在飞书后台授权，告知用户操作步骤

## 六、没有目标文档 ID

### 症状
- 用户要求"整理到飞书"，但没有给 doc_id / URL
- 当前上下文里也没有目标文档

### 正确处理
- 明确区分：
  - 是要新建文档
  - 还是要追加到已有文档
- 在未确认前，不要假设目标文档
- 如果上下文对话中之前出现过文档 URL，可以直接复用

## 七、无法读取历史文档内容

### 症状
- 用户要求"不重复写"
- 但当前环境无法读取历史飞书文档

### 正确处理
- 只能完成"本轮内部去重"
- 必须明确告诉用户：无法保证已与历史文档完全去重

## 八、subagent/worktree 失败

### 症状
- 当前目录不是 git 仓库
- git 没有 commit
- `HEAD` 无法解析
- 无法创建 worktree

### 正确处理
- 如果用户允许，自动补 git 初始化与初始 commit
- 否则退化为主代理串行执行

## 九、Markdown 写入格式崩坏

### 症状
- 飞书文档里换行失效
- 内容挤成一团
- URL 被 shell 误解释

### 正确处理
- 使用真实换行
- 不要在 URL 外面包反引号
- 避免脆弱的多行 shell 拼接
- 先构造完整 Markdown，再一次性写入

## 十、npm / Node.js 不可用

### 症状
- 无法安装 lark-cli
- `npm: command not found`

### 正确处理
- 告知用户需要先安装 Node.js 环境
- 提供 Node.js 官方下载地址或推荐使用 nvm
- 降级：先输出完整 Markdown，等环境准备好后再写入飞书

## 降级原则

遇到环境问题时，不要假装任务已经完整执行。应明确说明：
- 哪一步能做
- 哪一步做不了
- 当前输出是什么
- 用户若想完整执行，还缺什么前置条件

**优先级：** 尽量多做能做的步骤，而不是因为一个环节缺失就完全放弃。例如：搜索和抓取已完成但飞书不可写，仍应输出完整的结构化结果。
