---
name: claude-code-controller
description: 专门控制 Claude Code 的技能。提供简化的命令接口，支持快速任务、长时间任务、并行任务和进度跟踪。
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["claude"] },
        "install":
          [
            {
              "id": "node-claude",
              "kind": "node",
              "package": "@anthropic-ai/claude-code",
              "bins": ["claude"],
              "label": "Install Claude Code CLI (npm)",
            },
          ],
      },
  }
---

# Claude Code 控制器

专门用于控制 Claude Code 的技能，提供简化的命令接口和最佳实践。

## 📋 核心原则

1. **简单任务直接用** - 一行命令搞定
2. **复杂任务后台跑** - 后台模式 + 进度跟踪
3. **并行任务用 worktree** - 多分支并行处理
4. **永远不要在家目录跑** - 只在项目目录或临时目录运行

## 🚀 快速开始

### 模式一：快速任务（Foreground）

适合：简单修改、代码审查、文件读取等 5 分钟内能完成的任务

```bash
# 在当前目录运行
claude --permission-mode bypassPermissions --print "你的任务描述"

# 在指定项目目录运行
cd /path/to/project && claude --permission-mode bypassPermissions --print "你的任务描述"
```

### 模式二：长时间任务（Background）

适合：功能开发、重构、测试编写等需要较长时间的任务

```bash
# 启动后台任务
bash workdir:/path/to/project background:true command:"claude --permission-mode bypassPermissions --print '你的任务描述'"
# 返回 sessionId 用于跟踪

# 查看进度
process action:log sessionId:XXX limit:50

# 检查是否完成
process action:poll sessionId:XXX

# 完成任务后清理
process action:kill sessionId:XXX
```

### 模式三：并行任务（Parallel）

适合：同时处理多个 issue、批量代码审查等

```bash
# 为每个任务创建独立 worktree
git worktree add /tmp/feature-a main
git worktree add /tmp/feature-b main

# 并行启动多个 Claude Code 实例
bash workdir:/tmp/feature-a background:true command:"claude --permission-mode bypassPermissions --print '开发功能 A'"
bash workdir:/tmp/feature-b background:true command:"claude --permission-mode bypassPermissions --print '开发功能 B'"

# 监控所有任务
process action:list

# 完成后清理
git worktree remove /tmp/feature-a
git worktree remove /tmp/feature-b
```

## 📝 常用命令模板

### 代码开发
```bash
# 开发新功能
claude --permission-mode bypassPermissions --print "
开发一个用户登录功能，要求：
1. 使用 JWT 认证
2. 包含密码加密
3. 添加速率限制
4. 编写单元测试

完成后运行：openclaw system event --text 'Done: 用户登录功能开发完成' --mode now
"

# 修复 bug
claude --permission-mode bypassPermissions --print "
修复 issue #123 中的空指针异常。
错误日志：[粘贴错误信息]
相关代码：[文件路径]

完成后运行：openclaw system event --text 'Done: Bug #123 已修复' --mode now
"
```

### 代码审查
```bash
# 审查 PR
claude --permission-mode bypassPermissions --print "
审查这个 PR 的改动：
1. 检查代码质量
2. 找出潜在 bug
3. 建议改进点
4. 确认是否符合项目规范

git diff origin/main...origin/pr/123
"
```

### 文件操作
```bash
# 批量重构
claude --permission-mode bypassPermissions --print "
将所有 .js 文件转换为 .ts：
1. 添加类型注解
2. 修复类型错误
3. 更新 import/export

完成后运行：openclaw system event --text 'Done: JS 转 TS 完成' --mode now
"
```

## ⚠️ 安全规则

1. **不要在家目录运行** - 只在项目目录或临时目录
2. **不要给完全权限** - 使用 `--permission-mode bypassPermissions` 而非 `--yolo`
3. **敏感操作要确认** - 删除、推送、发布等操作需要用户确认
4. **不要在 OpenClaw 目录运行** - 避免读取敏感配置文件

## 📊 进度跟踪

### 检查任务状态
```bash
# 列出所有运行中的任务
process action:list

# 查看特定任务输出
process action:log sessionId:XXX limit:100

# 检查任务是否还在运行
process action:poll sessionId:XXX timeout:5000
```

### 发送输入给 Claude
```bash
# 发送简单确认
process action:write sessionId:XXX data:"y"

# 发送带换行的输入
process action:submit sessionId:XXX data:"yes"

# 粘贴多行文本
process action:paste sessionId:XXX text:"多行内容"
```

## 🎯 最佳实践

### 任务描述技巧
1. **具体明确** - 不要说"改进代码"，要说"添加错误处理和日志记录"
2. **分步骤** - 复杂任务分解成清晰的步骤
3. **设定边界** - 说明哪些文件可以修改，哪些不能
4. **添加完成通知** - 让 Claude 完成后运行通知命令

### 示例好的任务描述
```
❌ 坏的："修复这个 bug"
✅ 好的："修复 src/auth/login.js 中的空指针异常，
         当用户名为 null 时抛出 ValidationError，
         添加单元测试覆盖这个场景"

❌ 坏的："改进性能"
✅ 好的："优化 src/api/users.js 中的数据库查询，
         使用批量查询替代 N+1 查询，
         目标是将响应时间从 500ms 降到 100ms 以下"
```

### 完成通知模板
在任务描述末尾添加：
```
当完全完成后，运行这个命令通知我：
openclaw system event --text "Done: [简要总结完成的工作]" --mode now
```

## 🔧 故障排除

### Claude 卡住了
```bash
# 查看最后输出
process action:log sessionId:XXX limit:20

# 发送中断信号
process action:send-keys sessionId:XXX keys:["C-c"]

# 如果还不行，终止任务
process action:kill sessionId:XXX
```

### 权限问题
```bash
# 确保在项目目录运行
cd /path/to/project && claude --permission-mode bypassPermissions --print "任务"

# 如果需要写权限，确保目录可写
chmod -R u+w /path/to/project
```

### 输出太多
```bash
# 只看最新输出
process action:log sessionId:XXX offset:100 limit:50

# 搜索特定内容
process action:log sessionId:XXX | grep "ERROR"
```

## 📚 使用场景

| 场景 | 推荐模式 | 示例 |
|------|----------|------|
| 快速修复 | Foreground | `claude --print "修复拼写错误"` |
| 功能开发 | Background | `bash background:true command:"claude --print '开发用户系统'"` |
| 代码审查 | Foreground | `claude --print "审查这个 PR"` |
| 批量重构 | Parallel | 多个 worktree + 多个后台任务 |
| 学习探索 | Foreground | `claude --print "解释这段代码"` |

---

## 💡 提示

- **保持任务专注** - 一个任务做一件事，不要试图一次性完成太多
- **善用完成通知** - 长时间任务一定要添加完成通知
- **定期检查进度** - 后台任务每 10-15 分钟检查一次进度
- **保留会话日志** - 重要任务的输出可以保存到文件供后续参考
