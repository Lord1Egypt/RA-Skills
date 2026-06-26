---
name: ai-cli-design
version: 1.0.0
description: "Design CLI tools as local APIs for AI agents. TTY detection, --json output, stderr/stdout separation, exit codes. | 为 AI 设计 CLI 工具的规范：TTY 检测、JSON 输出、stderr/stdout 分离、退出码。"
user_invocable: false
---

# AI-CLI Design - 给 AI 设计 CLI 工具的规范

## 核心理念 / Core Principle

> CLI 不是"命令行界面"，是"AI 可调用的本地 API"。
> Unix 风格 = 最便宜、最稳定、最通用的 API 协议。

## 规范 / Specification

### 1. TTY 检测：终端 vs AI

检测 stdout 是否连接终端，自动切换输出模式：

```go
import "golang.org/x/term"

isTTY := term.IsTerminal(int(os.Stdout.Fd()))
```

| 场景 | stdout | 行为 |
|------|--------|------|
| 人在终端敲命令 | TTY | 进度条、颜色、交互提示 |
| AI/脚本调用 | pipe | 纯文本、无 ANSI、无进度条 |
| `--json` 显式指定 | 任意 | 强制 JSON 输出 |

**规则：如果不是 TTY，绝对不输出 ANSI 转义码、进度条、spinner。**

### 2. stdout/stderr 分离

这是最关键的设计：

```
stdout = 结果数据（机器读）
stderr = 日志/进度/调试信息（人读）
```

AI 调用时：`tool action 2>/dev/null` 拿到纯净数据。
人调试时：stderr 能看到过程信息。

**绝对不要把日志和结果混在 stdout 里。**

```go
// 日志 → stderr
func log(format string, a ...any) {
    if !jsonMode && !quiet {
        fmt.Fprintf(os.Stderr, format+"\n", a...)
    }
}

// 结果 → stdout
func output(data any) {
    if jsonMode {
        json.NewEncoder(os.Stdout).Encode(data)
    } else {
        // tab-separated 纯文本
        fmt.Println(formatTSV(data))
    }
}
```

### 3. 双模输出：默认 + --json

#### 默认模式（人 + 简单脚本）

Tab-separated，可 grep/awk/cut：

```
OK	/media/usb1	31 files	500KB	25ms	20MB/s
OK	/media/usb2	31 files	500KB	26ms	19MB/s
FAIL	/media/usb3	0 files	0B	1ms	0B/s
```

```bash
# 脚本用法
tool list | grep FAIL
tool list | awk '{print $2}'
tool list | wc -l
```

#### --json 模式（AI 专用）

```json
{
  "ok": true,
  "data": [...],
  "error": null
}
```

**JSON 输出契约（必须遵守）：**

```
顶层必有 "ok": bool          → AI 判断成功/失败
失败时必有 "error": string    → AI 读取错误信息
列表用数组 []                 → 不要换行拼接字符串
字段名用 snake_case           → 统一风格
数值不要格式化                → bytes 用数字，不用 "1.5MB"
```

完整 JSON 响应结构模板：

```go
type Response struct {
    OK      bool        `json:"ok"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
    Stats   *Stats      `json:"stats,omitempty"`
}

type Stats struct {
    Elapsed  string `json:"elapsed"`
    Count    int    `json:"count,omitempty"`
}
```

### 4. 退出码规范

```
0 = 成功
1 = 运行时错误（部分失败、IO 错误）
2 = 参数/用法错误
```

AI 用 `$?` 快速判断：

```bash
tool action --json && echo "success" || echo "failed: $?"
```

**不要用奇怪的退出码（比如 137、255）。简单的 0/1/2 足够。**

### 5. 命令设计 = API 设计

把每个子命令看作一个 API endpoint：

| CLI 命令 | 等价 API | 说明 |
|----------|----------|------|
| `tool list --json` | `GET /items` | 查询 |
| `tool get ID --json` | `GET /items/:id` | 获取 |
| `tool create --name foo --json` | `POST /items` | 创建 |
| `tool delete ID --json` | `DELETE /items/:id` | 删除 |
| `tool scan --json` | `POST /scan` | 动作 |

**设计原则：**
- 一个命令做一件事（Unix 哲学）
- 参数用 `--flag value` 不用交互式输入（AI 没法交互）
- 支持 `--yes` / `--no-input` 跳过确认（AI 不能回答 y/n）
- 幂等操作优先（重复执行不出错）

### 6. 标准 flag 集

每个 AI-friendly CLI 都应该支持这些 flag：

```
--json           结构化 JSON 输出
--quiet, -q      只输出结果，不输出日志
--verbose, -v    详细日志
--no-input       禁用交互式提示
--yes, -y        自动确认所有提示
--version        版本号
```

### 7. Go 实现模板

参考 `templates/tty.go.tmpl` 获取完整的 Go 代码模板，包含：
- TTY 检测
- stdout/stderr 分离
- --json / --quiet / --verbose 三模式
- 退出码处理
- JSON 响应结构

## 检查清单 / Checklist

设计一个新的 CLI 工具时，逐项检查：

- [ ] stdout 只输出结果数据，stderr 输出日志
- [ ] 支持 `--json` 输出结构化 JSON
- [ ] JSON 顶层有 `ok` 和 `error` 字段
- [ ] TTY 检测：非终端时不输出 ANSI/进度条
- [ ] 退出码：0=成功，1=失败，2=参数错误
- [ ] 默认输出 tab-separated 可 grep
- [ ] 支持 `--quiet` 和 `--verbose`
- [ ] 不需要交互式输入（或有 `--yes` 跳过）
- [ ] 参数全部通过 flag 传递，不依赖 stdin 交互

## 实际案例 / Real Example

fastcp（本规范的第一个实践项目）：

```bash
# AI 调用方式
fastcp --json --verify /source /target1 /target2 2>/dev/null
# 返回 {"ok":true, "targets":[...], "elapsed":"25ms"}

# 人工调用方式
fastcp --verify /source /target1 /target2
# stderr 显示进度条，stdout 显示 OK/FAIL 汇总

# 脚本调用方式
fastcp -q /source /target1 /target2 | grep FAIL
```
