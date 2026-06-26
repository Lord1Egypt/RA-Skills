# Hooks 系统

> 源码位置：`restored-src/src/types/hooks.ts` + `restored-src/src/skills/loadSkillsDir.ts`

## 支持的事件类型

```typescript
type HookEvent =
  | 'PreToolUse'         // 工具执行前
  | 'PostToolUse'        // 工具执行后
  | 'PostToolUseFailure' // 工具执行失败
  | 'UserPromptSubmit'   // 用户消息提交前
  | 'SessionStart'       // session 启动时
  | 'Setup'              // 设置时
  | 'SubagentStart'      // 子 agent 启动时
  | 'PermissionRequest' // 权限请求时
  | 'PermissionDenied'  // 权限被拒绝时
  | 'Elicitation'        // 用户选择提示时
  | 'Notification'       // 通知时
  | 'CwdChanged'         // 工作目录改变时
  | 'FileChanged'        // 文件改变时
  | 'WorktreeCreate'     // Worktree 创建时
```

---

## Hook 响应类型

```typescript
// 同步响应
const syncHookResponseSchema = z.object({
  continue: z.boolean().optional(),         // 默认 true
  suppressOutput: z.boolean().optional(),   // 隐藏输出
  decision: z.enum(['approve', 'block']).optional(),
  systemMessage: z.string().optional(),     // 显示给用户
  hookSpecificOutput: z.object({...}).optional()
})

// 异步响应
const asyncHookResponseSchema = z.object({
  async: z.literal(true),
  asyncTimeout: z.number().optional()
})

// PreToolUse 的 hookSpecificOutput 可以：
// - 修改输入：updatedInput
// - 注入权限决策：permissionDecision
// - 添加上下文：additionalContext

// PostToolUse 的 hookSpecificOutput 可以：
// - 修改 MCP 工具输出：updatedMCPToolOutput
```

---

## Hook 执行流程

```typescript
// 工具调用顺序：
// 1. validateInput() — 验证输入格式
// 2. Hooks('PreToolUse') — 可修改 input，可 block
// 3. checkPermissions() — 权限检查
// 4. Tool.call() — 实际执行
// 5. Hooks('PostToolUse') — 可修改输出
// 6. Hooks('PostToolUseFailure') — 失败处理

// Hook 匹配：glob 模式，任意匹配就触发
// "Bash(git *)" 匹配 git push, git commit, git status 等
```

---

## SKILL.md 里的 Hook 配置

```yaml
hooks:
  preToolUse:
    - if: "Bash(git *)"      # glob 模式匹配
      run: "echo 'Running git'"
  postToolUse:
    - if: "Bash(commit *)"
      run: "git log -1 --oneline"
```

---

## Hook 匹配规则的关键细节

```typescript
// BashTool.tsx — bashPermissions.ts

// Hook 的 if 是"no match → skip"语义
// 所以复合命令（ls && git push）需要 split 成多个子命令逐个匹配

// parseForSecurity 把 shell 命令解析成 AST：
// `ls && git push` → { commands: [{argv: ['ls']}, {argv: ['git', 'push']}] }
// "ls" 不匹配 Bash(git *)，但 "git push" 匹配
// 因为有子命令匹配 → 整个命令触发 hook
```

### SedEdit 的特殊处理（安全关键）

```typescript
// BashTool.tsx — _simulatedSedEdit 字段解决安全漏洞：

// 问题：
// 1. 用户想执行 sed -i 's/foo/bar/' file
// 2. sed 执行后文件已修改（不可逆）
// 3. 如果用户拒绝权限，命令应该不执行

// 解决：
// 1. sed 被拦截，显示预览给用户
// 2. 用户批准后，_simulatedSedEdit 包含 { filePath, newContent }
// 3. Tool.call() 检测到 _simulatedSedEdit，绕过 sed 直接 Write
// 4. _simulatedSedEdit 在 inputSchema 中被 omit，模型不能自己设置！

// 关键：_simulatedSedEdit 不在 inputSchema 里
// 如果把 _simulatedSedEdit 加入 schema，模型可以构造任意文件写入
```
