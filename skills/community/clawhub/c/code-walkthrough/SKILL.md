---
name: code-walkthrough
description: 调用链路追踪 + 代码标注 + 信任边界标注。生成可视化的代码理解页面，让模块结构和数据流一目了然。
---

# Code Walkthrough

生成可视化的代码理解页面，将传统的纯文本代码说明转化为**带调用链路、代码标注、信任边界标注**的 HTML 页面，让审查者一眼看清代码的形状。

## 何时使用

- 需要解释某个模块的调用链路和数据流
- 新人 onboarding 时理解代码结构
- 代码审查中解释复杂逻辑
- 标记安全边界和外部依赖

## 核心能力

### 1. 调用链路追踪
- 从入口到出口的完整数据流
- 模块间依赖关系图（boxes & arrows）
- 每个步骤标注文件路径和行号

### 2. 代码标注
- 关键逻辑逐步骤 Walkthrough
- 可展开/折叠的源码块
- 每个步骤的解释说明

### 3. 信任边界标注
- 标注安全边界（哪些是可信的，哪些不可信）
- 外部依赖标注
- 数据验证点标注

## HTML 输出

**始终输出一个自包含的 HTML 文件**，可通过 `<canvas>` 工具呈现。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Module] — Code Walkthrough</title>
<style>
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --green: #2ea043;
    --yellow: #d29922;
    --red: #da3633;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    max-width: 960px;
    margin: 0 auto;
    padding: 24px 16px;
  }
  h1 { font-size: 24px; margin-bottom: 4px; }
  h2 { font-size: 20px; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  h3 { font-size: 16px; margin: 16px 0 8px; }
  .meta { color: var(--text-muted); font-size: 14px; margin-bottom: 16px; }
  
  /* Request path diagram */
  .request-path { display: flex; align-items: center; gap: 8px; margin: 16px 0; flex-wrap: wrap; }
  .path-node {
    padding: 8px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 13px;
  }
  .path-node.trust { border-color: var(--green); }
  .path-node.untrusted { border-color: var(--yellow); }
  .path-arrow { color: var(--text-muted); font-size: 18px; }
  
  /* Call stack steps */
  .step {
    margin: 16px 0;
    padding: 16px;
    background: var(--surface);
    border-radius: 8px;
    border-left: 4px solid var(--accent);
  }
  .step-num {
    display: inline-block;
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--accent);
    color: var(--bg);
    text-align: center;
    line-height: 24px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 8px;
  }
  .step-title { font-weight: 600; }
  .step-file { font-family: monospace; font-size: 12px; color: var(--text-muted); }
  .step-desc { color: var(--text-muted); margin: 8px 0; }
  
  /* Collapsible code */
  details { margin: 8px 0; }
  summary { cursor: pointer; color: var(--accent); font-size: 13px; padding: 8px 0; }
  summary:hover { text-decoration: underline; }
  pre {
    background: var(--bg);
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 13px;
    line-height: 1.5;
  }
  
  /* Trust boundary */
  .trust-boundary {
    padding: 12px 16px;
    margin: 12px 0;
    border: 2px dashed var(--yellow);
    border-radius: 8px;
    background: rgba(210,153,34,0.05);
  }
  .trust-boundary strong { color: var(--yellow); }
  
  /* Annotation */
  .annotation {
    padding: 8px 12px;
    margin: 8px 0;
    background: rgba(88,166,255,0.1);
    border-left: 3px solid var(--accent);
    border-radius: 0 6px 6px 0;
    font-size: 13px;
  }
  
  @media (max-width: 640px) {
    .request-path { flex-direction: column; }
    .path-arrow { transform: rotate(90deg); }
  }
</style>
</head>
<body>
  <!-- Content goes here -->
</body>
</html>
```

## 使用指南

### 步骤 1：识别入口点

从用户可触达的入口开始（API endpoint、CLI 命令、Webhook 等）。

### 步骤 2：追踪调用链

沿数据流追踪到最终输出（数据库写入、响应返回、外部调用等）。
记录每一步：
- 文件路径和行号
- 函数名
- 关键逻辑说明

### 步骤 3：标注信任边界

标记：
- **可信区域**：经过验证的数据、内部服务
- **不可信区域**：用户输入、外部 API、第三方服务
- **验证点**：数据校验、权限检查的位置

### 步骤 4：生成 HTML

将以上信息组织成自包含的 HTML 页面，包含：
1. **Request Path 图** — 可视化数据流
2. **Call Stack Walkthrough** — 逐步骤代码注解
3. **Trust Boundary** — 安全边界标注

## 示例输出结构

```
## Request Path

[Browser] → [LB] → [API /api/session] → [verifyToken middleware] → [SessionStore] → [sessions table]

## Call Stack Walkthrough

1. src/app/providers/AuthProvider.tsx:22-48
   On mount, the React provider issues GET /api/session...
   [show source]

2. src/server/routes/session.ts:9-27
   The route is thin — returns whatever req.ctx.session attached...
   [show source]

3. src/middleware/auth.ts:14-31 ← TRUST BOUNDARY
   This is the trust boundary. verifyToken reads the signed cookie...
   [show source]

## Trust Boundary

Everything below verifyToken is trusted. Everything above it is not.
```
