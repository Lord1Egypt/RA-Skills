# Usage Patterns

## AI 决策流程（标准操作）

### 核心原则：先查找，后激活

所有窗口切换操作应遵循 **"查找 → 确认 → 激活"** 三步流程：

```
┌─────────────────┐
│  用户请求切窗口  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ find-window <关键词> 5   │
│       --json            │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  分析返回结果            │
│  • 完全匹配？→ 直接激活  │
│  • 部分匹配？→ 询问用户  │
│  • 无匹配？  → 重试/报错 │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ activate-window <k> <n> │
└─────────────────────────┘
```

### 完全匹配判定标准

满足以下任一条件视为"完全匹配"，可直接激活：

1. `items[0].title` 包含用户说的关键词（忽略大小写、连字符）
2. 用户说的关键词是 `items[0].title` 的缩写/别名（如"企微"→"企业微信"）
3. `items[0].title` 与用户描述在语义上一致

### 需要询问用户的情况

- 返回多个候选，且置信度相近
- `items[0]` 与用户描述差异较大
- 用户描述过于模糊（如"文档"可能指多个窗口）

---

## 模糊匹配能力

### 支持的匹配类型

| 匹配方式 | 示例查询 | 可匹配窗口 |
|----------|----------|------------|
| 精确匹配 | "企业微信" | 企业微信 |
| 缩写/别名 | "企微" | 企业微信 |
| 部分匹配 | "微信" | 企业微信、微信 |
| 跳跃匹配 | "qiyou" | 企业微信 |
| 忽略连字符 | "企业微信文档" | 企业微信-文档 |
| 英文别名 | "vscode" | Visual Studio Code |

### 内置别名表

```
企微、企业微 → 企业微信 (WeChat Work)
wx、vx       → 微信 (WeChat)
qq           → QQ、TIM
code、vscode → Visual Studio Code
vs           → Visual Studio、VS Code
idea         → IntelliJ IDEA
pycharm      → PyCharm
chrome       → Google Chrome
edge         → Microsoft Edge
wt、终端     → Windows Terminal
cmd          → Command Prompt
docker       → Docker Desktop
```

---

## 命令详解

### find-window（查找窗口）

**用途**：获取候选窗口列表，支持模糊匹配

**参数**：
- `<关键字>`：窗口标题关键词，支持缩写/别名
- `[数量]`：返回候选数，默认 3，建议 5
- `[--json]`：输出 JSON 格式

**示例**：
```bash
# 基础查找
scripts\d-switch.cmd find-window "企微" 3

# 推荐用法（AI 使用）
scripts\d-switch.cmd find-window "企微" 5 --json

# 英文别名
scripts\d-switch.cmd find-window "vscode" 3 --json
```

**JSON 输出**：
```json
{
  "mode": "find",
  "query": "企微",
  "choice": 1,
  "status": "ok",
  "count": 3,
  "items": [
    {
      "rank": 1,
      "title": "企业微信",
      "processName": "WXWork",
      "state": "Visible"
    }
  ]
}
```

---

### activate-window（激活窗口）

**用途**：激活指定候选窗口

**参数**：
- `<关键字>`：窗口关键词（应与 find-window 一致）
- `[序号]`：候选序号，默认 1
- `[--json]`：输出 JSON 格式

**示例**：
```bash
# 激活第一个候选
scripts\d-switch.cmd activate-window "企微" 1 --json

# 激活第二个候选
scripts\d-switch.cmd activate-window "企微" 2 --json
```

---

### activate-process（按进程激活）

**用途**：按进程名激活，适合标题变化频繁的应用

**场景**：VS Code、IDEA 等编辑器窗口标题随文件变化

**示例**：
```bash
scripts\d-switch.cmd activate-process "Code" 1 --json
scripts\d-switch.cmd activate-process "idea64" 1 --json
```

---

### list-windows（列出窗口）

**用途**：查看所有可切换窗口

**示例**：
```bash
scripts\d-switch.cmd list-windows --json
```

---

### Dalt / Dctrl（快捷键模拟）

**用途**：模拟键盘快捷键切换

**场景**：
- `Dalt`：在应用间切换（Alt+Tab 的替代）
- `Dctrl`：在应用内切换标签页（Ctrl+Tab）

**示例**：
```bash
# Alt+Tab 一次
scripts\d-switch.cmd Dalt -1

# Ctrl+Tab 三次
scripts\d-switch.cmd Dctrl -3
```

**降级策略**：当 `activate-window` 失败时，可降级到 `Dalt -1`

---

## AI 完整交互示例

### 示例 1：高置信度直接激活

```
用户：切到企微

AI 内部：
  → find-window "企微" 3 --json
  ← items[0].title = "企业微信"
  → 判定：完全匹配（别名命中）
  → activate-window "企微" 1 --json

AI 回复：已切换到企业微信
```

### 示例 2：需要用户确认

```
用户：打开文档

AI 内部：
  → find-window "文档" 5 --json
  ← 返回 4 个候选：WPS.xlsx、企业微信-文档、report.md、笔记.docx
  → 判定：需用户确认

AI 回复：
找到多个包含"文档"的窗口：
1. WPS表格 - 销售数据.xlsx
2. 企业微信-文档
3. VS Code - report.md
4. Word - 笔记.docx

请回复序号（1-4）：

用户：2

AI 内部：
  → activate-window "文档" 2 --json

AI 回复：已切换到企业微信-文档
```

### 示例 3：未找到

```
用户：切到不存在的窗口

AI 内部：
  → find-window "不存在的窗口" 3 --json
  ← count = 0, status = "not_found"
  → 尝试更短关键词：find-window "窗口" 3 --json
  ← 仍无匹配

AI 回复：
未找到名为"不存在的窗口"的窗口。
当前运行的窗口有：
- 企业微信
- Chrome
- VS Code

请检查窗口名称或尝试其他关键词。
```

---

## 失败恢复策略

### 激活失败时

```
activate-window 返回 activation_failed：
  1. 重试一次相同命令
  2. 仍失败 → 降级到 Dalt -1
  3. 提示用户："尝试切换失败，请手动选择窗口"
```

### 别名未命中时

```
find-window "未知别名" 返回 not_found：
  1. 尝试拆分关键词（如"微信文档"→先找"微信"）
  2. 尝试 list-windows 查看所有窗口
  3. 询问用户具体窗口名称
```

---

## 平台差异

| 功能 | Windows | macOS |
|------|---------|-------|
| find-window | ✅ 支持 | ❌ 不支持 |
| activate-window | ✅ 支持 | ❌ 不支持 |
| Dalt | ✅ 支持 | ❌ 仅建议快捷键 |
| Dctrl | ✅ 支持 | ❌ 仅建议快捷键 |

**macOS 降级方案**：
- 窗口切换：`Cmd+Tab`
- 标签切换：`Ctrl+Tab` 或 `Cmd+Shift+]`
