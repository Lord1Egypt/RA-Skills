# Keynote MCP Server

> **通过 Model Context Protocol 让 AI 直接操作 macOS Keynote**
>
> 版本: 1.0
> 平台: macOS 12.0+ (Monterey 及以上)
> 语言: Python 3.10+

---

## 项目简介

这是一个 **MCP (Model Context Protocol) Server**，封装了 AppleScript 和 JavaScript for Automation (JXA) 调用，让 Claude 和其他兼容 MCP 的 AI 助手可以直接操作 macOS 上的 Keynote.app。

**核心能力：**
- 创建新的 Keynote 演示文稿
- 添加/删除/排列幻灯片
- 设置标题、正文、图片等内容
- 应用 Keynote 主题和母版
- 控制文本格式（字体、大小、颜色）
- 播放/停止/跳转到指定幻灯片
- 导出为 PDF、PPTX、MOV、图片等格式
- 查询当前文档信息和幻灯片结构

**运行方式：**
1. 在 macOS 上安装本 server
2. 在 Claude Desktop 配置文件中注册
3. Claude 即可自动调用 Keynote 操作工具

---

## 目录结构

```
keynote-mcp-server/
├── README.md                          # 本文件（详细说明）
├── pyproject.toml                     # 项目配置（uv/pip 兼容）
├── requirements.txt                   # pip 依赖列表
├── server.py                          # MCP Server 主程序（FastMCP）
├── quickstart.py                      # 本地测试脚本（无需 MCP 环境）
├── keynote_tools/                     # Keynote 操作模块
│   ├── __init__.py
│   ├── applescript.py                 # AppleScript 执行引擎
│   └── keynote_controller.py          # 高层 Keynote 控制器
├── examples/
│   ├── claude_desktop_config.json     # Claude Desktop 配置示例
│   └── demo_presentation.key          # 示例文件（可选）
├── install.sh                         # 一键安装脚本（macOS）
└── test_connection.py                 # 本地连接性测试
```

---

## 快速开始（3 步）

### 步骤 1: 安装依赖

```bash
cd keynote-mcp-server

# 方式 A: 使用一键安装脚本（推荐）
./install.sh

# 方式 B: 手动安装
pip install "mcp[cli]"
```

### 步骤 2: 测试本地脚本（可选但推荐）

```bash
# 先确认 Keynote 可以被 AppleScript 控制
python3 quickstart.py --test

# 创建一个简单的演示文稿（会打开 Keynote）
python3 quickstart.py --demo
```

### 步骤 3: 配置 Claude Desktop

**找到配置文件：**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**编辑配置文件，添加以下内容（替换 YOUR_PATH 为实际路径）：**

```json
{
  "mcpServers": {
    "keynote": {
      "type": "stdio",
      "command": "/usr/bin/python3",
      "args": [
        "/YOUR_PATH/keynote-mcp-server/server.py"
      ]
    }
  }
}
```

**重启 Claude Desktop**，然后在聊天中就可以让 AI 操作 Keynote 了！

---

## 可用工具（MCP Tools）

### 文档管理

| 工具名 | 说明 |
|--------|------|
| `keynote_create` | 创建新的 Keynote 文档 |
| `keynote_open` | 打开现有的 .key 文件 |
| `keynote_save` | 保存当前文档 |
| `keynote_close` | 关闭当前文档 |
| `keynote_export` | 导出为 PDF/PPTX/MOV/图片 |

### 幻灯片操作

| 工具名 | 说明 |
|--------|------|
| `keynote_add_slide` | 添加新幻灯片（可指定母版/布局） |
| `keynote_delete_slide` | 删除指定幻灯片 |
| `keynote_list_slides` | 列出文档中所有幻灯片 |
| `keynote_duplicate_slide` | 复制幻灯片 |
| `keynote_move_slide` | 移动幻灯片位置 |

### 内容编辑

| 工具名 | 说明 |
|--------|------|
| `keynote_set_title` | 设置幻灯片标题 |
| `keynote_set_body` | 设置幻灯片正文 |
| `keynote_add_text` | 添加任意文本框 |
| `keynote_add_image` | 添加图片到幻灯片 |
| `keynote_add_shape` | 添加形状 |
| `keynote_add_chart` | 添加图表（简化版） |

### 演示控制

| 工具名 | 说明 |
|--------|------|
| `keynote_start_show` | 开始演示 |
| `keynote_stop_show` | 停止演示 |
| `keynote_next_slide` | 下一张 |
| `keynote_prev_slide` | 上一张 |
| `keynote_go_to_slide` | 跳转到指定幻灯片 |

### 查询

| 工具名 | 说明 |
|--------|------|
| `keynote_get_info` | 获取当前文档信息（幻灯片数、尺寸等） |
| `keynote_get_slide_content` | 获取指定幻灯片的完整内容 |
| `keynote_list_masters` | 列出可用的母版/布局 |
| `keynote_is_running` | 检查 Keynote 是否运行中 |

---

## 使用示例

### 在 Claude 中这样说

#### 示例 1: 创建简单发布会

```
用 Keynote 创建一个产品发布会演示文稿。
标题是 "2026 春季新品发布"。
包含以下幻灯片：
1. 封面 - 大标题 + 副标题
2. 议程 - 列出 5 个章节
3. 产品介绍 - 列出核心亮点
4. 技术规格 - 双列布局
5. 感谢页

请使用深色背景风格。
```

#### 示例 2: 打开并分析现有文档

```
打开 /Users/me/Documents/发布会.key，
告诉我这个文档有多少张幻灯片，
以及每张幻灯片的标题和主要内容。
```

#### 示例 3: 控制演示播放

```
请开始播放 Keynote 演示文稿，
每隔 5 秒自动切换到下一张，
直到最后一张幻灯片。
```

---

## 设计规范

为确保最佳视觉效果，建议遵循以下规范（与 keynote-skill 的设计规范一致）：

### 画布
- 默认尺寸: 1920 × 1080 (16:9, 全高清)
- 也支持 1680 × 1050 (16:10)

### 字体
- 中文: 苹方 (PingFang SC)
- 英文: SF Pro / Helvetica Neue
- 标题: 88-120pt
- 副标题: 44-56pt
- 正文: 28-36pt

### 配色
- Apple 深色发布会: 黑底 + 白字 + (#007AFF / #34C759)
- 科技风格: 深蓝黑 + 霓虹蓝/绿
- 品牌风格: 白底 + 品牌色

### 动画
- 推荐: "神奇移动 (Magic Move)" 作为过渡
- 每个元素的动画效果保持简洁
- 不要过度使用动画

---

## 安全性与权限

### 首次运行时的权限请求

当 server 第一次通过 AppleScript 控制 Keynote 时，macOS 会弹出权限请求：

```
"python3" 想要控制 "Keynote"
允许/不允许
```

请点击 **"允许"**。

### 如果没有弹出权限请求

手动授予权限：
1. 打开 "系统设置" → "隐私与安全性" → "自动化"
2. 找到 python3（或你的 Python 解释器）
3. 勾选 Keynote 复选框

---

## 调试与故障排除

### 问题 1: Claude 无法连接到 server

**症状:** 在 Claude 中调用 Keynote 工具超时或失败

**检查:**
```bash
# 1. 检查 server 脚本路径是否正确
ls -l /YOUR_PATH/keynote-mcp-server/server.py

# 2. 检查 Python 路径是否正确
which python3
/usr/bin/python3 --version

# 3. 手动测试 server 是否可以启动
python3 /YOUR_PATH/keynote-mcp-server/server.py
# (按 Ctrl+C 退出，正常启动后会等待 MCP 协议消息)
```

### 问题 2: AppleScript 执行失败

**症状:** 收到 "Keynote got an error" 消息

**检查:**
```bash
# 测试 AppleScript 是否可以控制 Keynote
osascript -e 'tell application "Keynote" to return "OK"'

# 如果失败，检查权限
# 系统设置 → 隐私与安全性 → 自动化 → 允许 Python 控制 Keynote
```

### 问题 3: 想查看 server 的运行日志

server 把调试日志写入 stderr（MCP 协议用 stdin/stdout 通信，
所以日志不能干扰 stdout）。你可以在启动时重定向日志：

```bash
# 临时调试：修改 server 启动参数
# 但注意：Claude Desktop 会自动启动 server，不需要手动运行
```

### 问题 4: Keynote 版本兼容性

- 支持 Keynote 12.0+（macOS 12 Monterey 及以上）
- 部分高级功能需要 Keynote 13.0+

---

## 开发与扩展

### 添加新工具

在 `server.py` 中，使用 `@mcp.tool()` 装饰器添加新工具：

```python
@mcp.tool()
def keynote_my_custom_tool(param1: str, param2: int) -> str:
    """
    工具的简要说明（会作为 tool description 发送给 AI）

    Args:
        param1: 参数 1 的说明
        param2: 参数 2 的说明

    Returns:
        操作结果的说明
    """
    # 调用 keynote_controller 执行操作
    result = keynote_controller.my_custom_operation(param1, param2)
    return result
```

### 添加新的 AppleScript 命令

在 `keynote_tools/applescript.py` 中添加：

```python
def run_my_script(some_param: str) -> str:
    """执行自定义 AppleScript"""
    script = f'''
    tell application "Keynote"
        -- 你的 AppleScript 代码
        return "结果"
    end tell
    '''
    return run_applescript(script)
```

---

## 架构说明

```
┌──────────────────────────────────────────────────────┐
│  Claude Desktop / Claude Code                       │
│  (AI Assistant)                                      │
└────────────────┬─────────────────────────────────────┘
                 │ MCP 协议 (stdio: JSON-RPC 2.0 over stdin/stdout)
                 ▼
┌──────────────────────────────────────────────────────┐
│  server.py (FastMCP)                                │
│  - 工具注册 (@mcp.tool)                             │
│  - 请求处理 / 参数校验                              │
└────────────────┬─────────────────────────────────────┘
                 │ 函数调用
                 ▼
┌──────────────────────────────────────────────────────┐
│  keynote_tools/                                      │
│  ├── keynote_controller.py (高层 API)               │
│  │    create_presentation()                         │
│  │    add_slide()                                   │
│  │    set_title()                                   │
│  │    ...                                           │
│  └── applescript.py (底层执行)                      │
│       run_applescript(script)                       │
│       run_jxa(script)                               │
└────────────────┬─────────────────────────────────────┘
                 │ osascript / osalang (macOS 原生工具)
                 ▼
┌──────────────────────────────────────────────────────┐
│  macOS                                              │
│  └── Keynote.app                                    │
│      (Apple Event / Automation)                     │
└──────────────────────────────────────────────────────┘
```

---

## 参考资源

- **MCP 官方文档**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Keynote AppleScript 指南**: https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/Keynote_Scripting_Guide/
- **AppleScript 语言指南**: https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/

---

## 许可证

MIT License - 详见代码文件头部。

---

**开始使用**: 运行 `./install.sh` 安装，然后配置 `claude_desktop_config.json`，重启 Claude Desktop 即可！
