---
name: dkey-switch
description: AI 窗口切换技能。用于定位并激活 Windows 上的目标窗口，支持智能模糊匹配、窗口查找、进程匹配、句柄激活与标签切换回退。
argument-hint: <窗口关键字|进程名|窗口句柄>
metadata: {
   "clawdbot":{
      "emoji":"🪟",
      "requires":{
         "bins":["powershell"]
      },
      "install":[
         {"id":"winget-powershell","kind":"winget","package":"Microsoft.PowerShell","bins":["powershell"],"label":"Install PowerShell (winget)"}
      ]
   }
}
---

## 核心定位

本技能可以 **直接执行窗口切换动作**，而非仅提供快捷键建议。

**关键特性**：
- **智能模糊匹配**：支持缩写（如"企微"→"企业微信"）、拼音首字母、跳跃匹配
- **双步安全流程**：先 `find-window` 确认，再 `activate-window` 激活
- **精确回退机制**：激活失败时自动降级到 `Dalt` 或 `Dctrl`

---

## 命令速查表

| 命令 | 用途 | 示例 |
|------|------|------|
| `find-window <关键字> [数量] [--json]` | **首选**：查找候选窗口 | `find-window 企微 3 --json` |
| `activate-window <关键字> [序号] [--json]` | 激活指定候选 | `activate-window 企微 1 --json` |
| `activate-process <进程名> [--json]` | 按进程名激活 | `activate-process Code --json` |
| `activate-handle <句柄> [--json]` | 精确句柄激活 | `activate-handle 0x2072C --json` |
| `list-windows [--json]` | 列出所有窗口 | `list-windows --json` |
| `Dalt -N` | Alt+Tab 切换 N 次 | `Dalt -1` |
| `Dctrl -N` | Ctrl+Tab 标签切换 | `Dctrl -1` |

---

## AI 标准操作流程（重要）

### Step 1: 总是先执行 find-window

```bash
scripts\d-switch.cmd find-window <用户关键词> 5 --json
```

### Step 2: 分析返回结果

**情况 A：完全匹配（高置信度）**
- 条件：`items[0].title` 与用户说的窗口名**基本一致**
- 操作：**直接激活**，无需询问用户

**情况 B：部分匹配（需确认）**
- 条件：有候选结果，但第一项不完全匹配用户描述
- 操作：**列出候选列表，询问用户确认**

**情况 C：无匹配**
- 条件：`count == 0` 或 `status == "not_found"`
- 操作：尝试更通用关键词，或告知用户未找到

### Step 3: 执行激活

```bash
# 用户确认后（或高置信度直接激活）
scripts\d-switch.cmd activate-window <关键词> <用户选择的序号> --json
```

### 流程图

```
用户："切到企微文档"
  ↓
AI：执行 find-window "企微" 5 --json
  ↓
检查 items[0]:
  ├─ 标题 ≈ "企业微信-文档" → 直接 activate-window "企微" 1
  ├─ 标题不匹配 → 列出列表让用户选择
  └─ 无结果 → 尝试其他关键词或告知未找到
```

---

## 模糊匹配规则

### 支持的匹配类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **缩写/别名** | 内置常见应用别名 | "企微"→"企业微信", "vx"→"微信" |
| **跳跃匹配** | 字符顺序一致即可 | "qiyou"→"企业微信" |
| **子串匹配** | 包含即可 | "微信"→"企业微信" |
| **连字符兼容** | `-` `_` 自动忽略 | "企业微信文档"→"企业微信-文档" |

### 内置别名表

| 别名 | 匹配目标 |
|------|----------|
| 企微, 企业微 | 企业微信 |
| wx, vx | 微信 |
| qq | QQ, TIM |
| code, vscode | Visual Studio Code |
| vs | Visual Studio |
| idea | IntelliJ IDEA |
| chrome | Google Chrome |
| edge | Microsoft Edge |
| wt, 终端 | Windows Terminal |
| cmd | Command Prompt |

---

## 状态处理与错误恢复

### JSON 返回状态

| status | 含义 | 处理建议 |
|--------|------|----------|
| `ok` | 查找成功 | 检查 `items` 内容决定下一步 |
| `activated` | 激活成功 | 流程结束 |
| `not_found` | 未找到 | 尝试别名/更短关键词 |
| `choice_out_of_range` | 序号越界 | 重新查找获取有效序号 |
| `activation_failed` | 激活失败 | 重试1次，仍失败则降级 `Dalt -1` |

### 退出码

| 码 | 含义 |
|----|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 未找到目标 |
| 3 | 找到但激活失败 |
| 4 | 候选序号越界 |

---

## 典型场景示例

### 场景 1：用户说"切到企微"

```bash
# AI 执行：
scripts\d-switch.cmd find-window "企微" 3 --json

# 假设返回 items[0].title = "企业微信"
# 判定：完全匹配 → 直接激活

scripts\d-switch.cmd activate-window "企微" 1 --json
```

### 场景 2：用户说"切到文档"（有多个候选）

```bash
# AI 执行：
scripts\d-switch.cmd find-window "文档" 5 --json

# 假设返回多个：WPS文档、企业微信-文档、VS Code文档...
# 判定：不完全确定 → 询问用户

# AI 回复：找到以下窗口，请确认：
# 1. WPS文档
# 2. 企业微信-文档  
# 3. VS Code - document.txt
# 请输入序号（1-3）：

# 用户回复：2
scripts\d-switch.cmd activate-window "文档" 2 --json
```

### 场景 3：用户说"切到浏览器"

```bash
# AI 执行：
scripts\d-switch.cmd find-window "浏览器" 3 --json

# 返回：Chrome、Edge、Firefox...
# 判定：有歧义 → 询问用户
```

### 场景 4：只知道进程名

```bash
# 适合标题频繁变化的应用（如 VS Code）
scripts\d-switch.cmd activate-process "Code" 1 --json
```

### 场景 5：窗口内切换标签

```bash
# 先激活窗口，再切标签
scripts\d-switch.cmd activate-window "chrome" 1 --json
scripts\d-switch.cmd Dctrl -1
```

---

## 非触发场景（不执行脚本）

以下情况**不应**调用本技能：
- 用户仅询问快捷键知识（如"Alt+Tab 是什么"）
- 用户仅讨论原理/概念（如"怎么切换窗口"但无执行意图）
- 用户明确说"不要执行"

---

## 平台兼容性

| 平台 | 入口 | 备注 |
|------|------|------|
| Windows | `scripts\d-switch.cmd ...` | 首选 |
| PowerShell | `powershell -File scripts/d-switch.ps1 ...` | 备选 |
| Git Bash/WSL | `bash scripts/d-switch.sh ...` | 兼容 |
| macOS | 无脚本支持 | 降级为快捷键建议 |

---

## 最佳实践

1. **总是先 find-window**：除非用户明确指定了进程名或句柄
2. **优先使用 --json**：便于程序化解析结果
3. **高置信度直接执行**：第一项完全匹配时无需询问
4. **低置信度询问确认**：有候选但不完全匹配时列出选项
5. **失败时友好提示**：未找到时建议用户可能的关键词

---

## 快速参考卡

```
用户："切到XXX"
  ↓
find-window "XXX" 5 --json
  ↓
items[0] 匹配？ ──Yes──→ activate-window "XXX" 1
    │
    No
    ↓
列出选项询问用户
    ↓
activate-window "XXX" <用户选择>
```
