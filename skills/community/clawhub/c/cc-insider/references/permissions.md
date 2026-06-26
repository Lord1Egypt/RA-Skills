# 权限系统

> 源码位置：`restored-src/src/utils/permissions/` + `restored-src/src/tools/BashTool/bashPermissions.ts`

## PermissionResult 类型

```typescript
type PermissionResult =
  | { behavior: 'allow', updatedInput?: Record<string, unknown> }  // 直接通过
  | { behavior: 'deny', reason?: string }                         // 直接拒绝
  | { behavior: 'prompt', message?: string }                      // 询问用户
  | { behavior: 'block', reason?: string }                         // 阻止并显示原因
```

---

## 权限检查链（BashTool）

```typescript
async function bashToolHasPermission(input, context): Promise<PermissionResult> {
  // 1. preparePermissionMatcher：构建 pattern matcher
  // 解析 hook 规则中的 Bash(*) glob 模式

  // 2. parseForSecurity：解析命令为 AST
  // 复合命令（ls && git push）会 split 成多个子命令
  // "ls && git push" 匹配 Bash(git *) 因为有子命令匹配

  // 3. 遍历 rules，找第一条匹配的
  // Hook 的 if 是"no match → skip"语义

  // 4. 检查 sandbox 是否可用
  // 用户配置的危险命令（如 sandbox.excludedCommands）
  // 或 tengu_sandbox_disabled_commands 中的命令 → 不进 sandbox
}
```

---

## isConcurrencySafe 的意义

```typescript
// buildTool 的 TOOL_DEFAULTS：
isConcurrencySafe: (_input) => false

// 这个标志告诉 QueryEngine：
// - false：不允许同时运行两个这个工具
// - true：可以并行

// 实际用途：
// - BashTool: false（写操作不能并行）
// - GrepTool: true（只读，可以并行）
// - WebFetchTool: true（只读，可以并行）

// QueryEngine 在并行工具调用时检查这个标志
// 如果工具 A 是 false 且已在运行，B 也要调用 A → B 等待 A 完成
```

---

## SedEdit 的安全设计

```typescript
// _simulatedSedEdit 解决安全漏洞：

// 问题：
// 1. 用户想执行 sed -i 's/foo/bar/' file
// 2. sed 执行后文件已修改（不可逆）
// 3. 如果用户拒绝权限，命令应该不执行

// 解决：
// 1. sed 被拦截，显示预览给用户
// 2. 用户批准后，_simulatedSedEdit 包含 { filePath, newContent }
// 3. Tool.call() 检测到 _simulatedSedEdit，绕过 sed 直接 Write
// 4. _simulatedSedEdit 在 inputSchema 中被 omit，模型不能自己设置！

// inputSchema：
// const inputSchema = lazySchema(() =>
//   fullInputSchema().omit({ _simulatedSedEdit: true })  // 对模型不可见
// )
```

---

## Sleep 检测（防止轮询）

```typescript
// BashTool.tsx — detectBlockedSleepPattern
// 检测 `sleep N` 模式（N >= 2秒）
// 如果命令中有 sleep → 拒绝执行，建议用 Monitor 工具

// 为什么：
// sleep N + check 是轮询模式
// Monitor 工具是事件驱动（条件满足才通知）
// 轮询浪费资源，事件驱动更高效

// `sleep 0.5` 允许（速率限制、延迟）
// `sleep 5 && check_api` → "use Monitor { command: check_api }"
```

---

## PTY vs 非 PTY

```typescript
// utils/Shell.js — exec 函数
// Claude Code 默认不使用 PTY（pseudo-terminal）
// 为什么：输出需要可解析（用于 ToolSearch、进度追踪）
// PTY 会让输出带 ANSI 转义序列，难以解析

// PTY 用于：需要交互式输入的命令（ssh, vim 等）
// 非 PTY 用于：管道、重定向、文件输出
```
