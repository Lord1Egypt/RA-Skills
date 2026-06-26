# Smoke Tests

每项能力的最小验证命令。在 preflight 阶段使用，快速判断能力是否可用。

## 1. BrightData 搜索能力

**验证方式 A（MCP）：** 执行一次最小搜索
```
使用 mcp__brightdata__search_engine 工具搜索 "test"
```

**验证方式 B（CLI）：**
```bash
brightdata search "test" 2>&1 | head -5
```

**成功标志：** 返回搜索结果列表
**失败标志：** 工具不存在、连接失败、command not found、或返回错误

## 2. BrightData 抓取能力

**验证方式 A（MCP）：** 抓取一个简单页面
```
使用 mcp__brightdata__scrape_as_markdown 抓取 "https://example.com"
```

**验证方式 B（CLI）：**
```bash
brightdata scrape https://example.com 2>&1 | head -10
```

**成功标志：** 返回页面 Markdown 内容
**失败标志：** 工具不存在、连接失败、command not found、或返回错误

## 2.5. BrightData CLI 安装与认证状态

**验证命令：**
```bash
which brightdata 2>/dev/null && brightdata --version
```

**认证检查：**
```bash
brightdata config 2>&1
```

**成功标志：** 输出版本号和配置信息
**失败标志：** command not found 或未认证提示

## 3. lark-cli 安装状态

**验证命令：**
```bash
which lark-cli 2>/dev/null && lark-cli --version
```

**成功标志：** 输出版本号
**失败标志：** command not found

## 4. lark-cli 认证状态

**验证命令：**
```bash
lark-cli auth status
```

**成功标志：** 显示已登录的身份信息
**失败标志：** 未登录提示、或权限不足提示

## 5. 飞书文档读取

**验证方式：** 尝试读取目标文档
```bash
lark-cli docs +fetch --doc "<target_doc_url>" --as user
```

**成功标志：** 返回文档内容（JSON 包含 markdown 字段）
**失败标志：** Permission denied、文档不存在、或认证过期

## 6. 飞书文档写入

**验证方式：** 对目标文档做一次 dry-run 或最小追加测试
建议先读取文档确认权限，不要在 smoke test 阶段实际写入内容。

## 7. subagent/worktree 前置条件

**验证命令：**
```bash
git rev-parse --is-inside-work-tree 2>/dev/null && git rev-parse HEAD 2>/dev/null
```

**成功标志：** 第一行输出 `true`，第二行输出 commit hash
**失败标志：** 不在 git 仓库、或 HEAD 无法解析

## Preflight 判定矩阵

| 能力 | 通过 | 可自动修复 | 需用户介入 |
|------|------|-----------|-----------|
| BrightData 搜索（MCP） | smoke test 1A 通过 | - | 需用户配置 MCP + API token |
| BrightData 搜索（CLI） | smoke test 1B 通过 | 可自动 `npm install -g @brightdata/cli` | 需用户 `brightdata login` |
| BrightData 抓取（MCP） | smoke test 2A 通过 | - | 同上 |
| BrightData 抓取（CLI） | smoke test 2B 通过 | 同上 | 同上 |
| lark-cli 安装 | smoke test 3 通过 | 可自动 `npm install -g @larksuite/cli` | - |
| lark-cli 认证 | smoke test 4 通过 | 可提示命令 | 需用户扫码/确认 |
| 文档读取 | smoke test 5 通过 | - | 权限问题需用户处理 |
| subagent | smoke test 7 通过 | 可自动 `git init && git commit` | - |

**注意：** MCP 和 CLI 两种 BrightData 接入方式任一可用即满足搜索/抓取能力要求。MCP 对 agent 更友好（直接工具调用），CLI 对终端操作和管道组合更灵活。
