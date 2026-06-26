---
name: openclaw-plugin
description: "创建和管理 OpenClaw 插件使用 before_prompt_build hook。触发词：'create plugin'、'add hook'、'inject context'、'modify gateway'。适用于使用 hook 系统扩展 OpenClaw 功能。"
---

# 🔌 OpenClaw 插件技能

> 使用 before_prompt_build hook 创建和管理插件

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

使用 OpenClaw hook 系统创建和管理插件。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| "创建插件" | 初始化新插件 |
| "添加 hook" | 注册新 hook |
| "注入上下文" | 使用 hook 注入上下文 |
| "修改网关" | 配置网关 |

---

## 2. Hook 系统

### 可用 Hooks

| Hook | 触发时机 | 用途 |
|------|----------|------|
| before_prompt_build | 构建提示前 | 注入上下文、修改消息 |
| after_response | 响应后 | 日志、监控 |
| on_error | 错误时 | 错误处理 |

### Hook 位置

```
~/.openclaw/plugins/<plugin-name>/
├── plugin.json       # 插件配置
├── hooks/
│   └── before_prompt_build.js
└── README.md
```

---

## 3. 创建插件

### 步骤 1：创建目录

```bash
mkdir -p ~/.openclaw/plugins/<plugin-name>/hooks
```

### 步骤 2：创建 plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "hooks": [
    {
      "name": "before_prompt_build",
      "file": "hooks/before_prompt_build.js"
    }
  ],
  "description": "插件描述"
}
```

### 步骤 3：创建 Hook 文件

```javascript
// hooks/before_prompt_build.js
module.exports = async function(context) {
  // 添加上下文
  context.systemMessage = "你的系统消息";
  
  // 或修改用户消息
  // context.messages[0].content = "修改后的内容";
  
  return context;
};
```

---

## 4. 注册插件

```bash
# 启用插件
openclaw plugin enable <plugin-name>

# 禁用插件
openclaw plugin disable <plugin-name>

# 列出所有插件
openclaw plugin list
```

---

## 5. 插件示例

### 上下文注入插件

```javascript
// hooks/before_prompt_build.js
module.exports = async function(context) {
  // 添加时间上下文
  const now = new Date();
  context.systemMessage += `\n当前时间：${now.toISOString()}`;
  
  return context;
};
```

### 消息修改插件

```javascript
module.exports = async function(context) {
  // 检查用户消息
  if (context.messages[0].content.includes("密码")) {
    // 添加安全警告
    context.messages[0].content += "\n\n⚠️ 安全提示：请勿分享敏感信息";
  }
  
  return context;
};
```

---

## 6. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| Hook 抛出错误 | 记录错误，继续执行 |
| 插件冲突 | 禁用冲突插件 |
| Hook 无效 | 检查语法和路径 |
| 插件加载失败 | 检查 plugin.json 格式 |

---

_In Altum Per Plugin._
🔌 OpenClaw 插件 v1.0