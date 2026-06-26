---
name: amcjt-lottery-pro
description: 专业彩票助手 - 支持双色球开奖查询、彩票OCR识别、中奖核对、开奖提醒。触发词：彩票、双色球、开奖、中奖、lottery。
license: MIT
allowed-tools:
  - get_lottery_result
  - ocr_lottery_ticket
  - check_lottery_win
  - get_lottery_countdown
  - get_lottery_calendar
  - Bash(node:*)
  - Bash(npx:*)
  - Bash(mcporter:*)
metadata:
  openclaw:
    icon: "🏆"
    category: "lifestyle"
    author: "amcjt"
    bins: [ "node", "mcporter" ]
    os: [ "darwin", "linux", "win32" ]
    user-invocable: true
---

# 专业彩票助手

> ⚠️ **重要前提**：本技能依赖 **OpenClaw 内置的 mcporter 技能** 来调用 MCP 工具。使用前请确保：
> 1. 已启用 mcporter 技能
> 2. mcporter 已配置并注册 **amcjt-mcp-server**

mcporter 调用集成 amcjt-mcp-server 提供的彩票服务，支持双色球相关操作。

## 环境要求

### 必需依赖

- **OpenClaw mcporter 技能**: 用于调用 MCP 工具（请确保已启用并配置 amcjt-mcp-server）

### 支持系统

- macOS, Linux, Windows

## 触发条件

当用户提到以下关键词时触发：

- "彩票"、"双色球"、"开奖"、"中奖"、"lottery"
- 用户上传图片文件（彩票照片）
- "我中了没"、"查一下开奖"、"看看中奖号码"

## 核心功能

> 💡 **工具调用方式**：以下所有 MCP 工具均通过 **mcporter 技能** 调用，确保 mcporter 已正确配置 amcjt-mcp-server。

### 1. 查询开奖结果

用户询问某期开奖号码时：

1. 提取期号（格式：YYYY + 3位序号，如 2026020）
2. 如未提供期号，查询最新一期
3. 通过 mcporter 调用 amcjt-mcp-server 的 `get_lottery_result` MCP 工具获取结果
4. 展示：开奖日期、红球号码（6个）、蓝球号码（1个）、奖池金额、中奖注数

### 2. 彩票OCR识别

用户上传彩票图片时：

1. 读取彩票图片文件
2. 获取彩票图片完整路径
3. 通过 mcporter 调用 amcjt-mcp-server 的 `ocr_lottery_ticket` MCP 工具识别号码
4. 展示识别的红球和蓝球号码

### 3. 中奖核对

用户提供投注号码时：

1. 获取期号（用户输入或查询最新）
2. 获取投注号码（6个红球 01-33，1个蓝球 01-16）
3. 通过 mcporter 调用 amcjt-mcp-server 的 `check_lottery_win` MCP 工具核对
4. 展示中奖等级和奖金

## 工作流程

### 流程1：查询指定期号开奖

```
用户：查一下2026020期双色球开奖
↓
提取期号：2026020
↓
通过 mcporter 调用 MCP 工具：get_lottery_result
  命令：mcporter call 'amcjt-mcp-server.get_lottery_result(issueNo: "2026020", lottoType: "101")'
↓
解析返回，格式化展示
```

**mcporter call 示例：**

```bash
# 使用函数调用语法
 mcporter call 'amcjt-mcp-server.get_lottery_result(issueNo: "2026020", lottoType: "101")'

# 输出 JSON 格式
 mcporter call amcjt-mcp-server.get_lottery_result issueNo:2026020 lottoType:101 --output json
```

### 流程2：识别彩票图片

```
用户上传 lottery.jpg
↓
读取图片完整路径：/root/.openclaw/workspace/lottery.jpg
↓
通过 mcporter 调用 MCP 工具：ocr_lottery_ticket
  命令： mcporter call 'amcjt-mcp-server.ocr_lottery_ticket(image: "/root/.openclaw/workspace/lottery.jpg", lottoType: "101")'
↓
展示识别结果，询问是否核对中奖
```

**mcporter OCR 调用示例：**

```bash
# 调用 OCR 工具（传入图片路径）
# 使用函数调用语法
 mcporter call 'amcjt-mcp-server.ocr_lottery_ticket(image: "/root/.openclaw/workspace/lottery.jpg", lottoType: "101")'
```

### 流程3：核对中奖

```
用户：我买的 01 13 14 21 24 30 + 02，中了没？
↓ 
提取红球：[01,13,14,21,24,30]，蓝球：[02]
↓
获取期号（最新或指定）
↓
通过 mcporter 调用 MCP 工具：check_lottery_win
  命令： mcporter call 'amcjt-mcp-server.check_lottery_win(issueNo: "2026020", lottoType: "101", bets: [{redNumbers: ["01","13","14","21","24","30"], blueNumbers: ["02"]}, {redNumbers: ["03","08","15","22","28","31"], blueNumbers: ["09"]}])'
↓
展示中奖等级和奖金
```

**mcporter 中奖核对示例：**

```bash
# 核对单注号码
# 核对多注号码
 mcporter call 'amcjt-mcp-server.check_lottery_win(issueNo: "2026020", lottoType: "101", bets: [{redNumbers: ["01","13","14","21","24","30"], blueNumbers: ["02"]}, {redNumbers: ["03","08","15","22","28","31"], blueNumbers: ["09"]}])'
```

### 流程4：开奖倒计时查询

```
用户：下次双色球什么时候开奖？
↓
通过 mcporter 调用 MCP 工具：get_lottery_countdown
  命令： mcporter call amcjt-mcp-server.get_lottery_countdown
↓
展示倒计时信息
```

**mcporter 调用示例：**

```bash
# 获取开奖倒计时
 mcporter call amcjt-mcp-server.get_lottery_countdown

# 获取开奖日历
 mcporter call amcjt-mcp-server.get_lottery_calendar
```

## 数据格式

### 投注号码格式

```json
{
  "redNumbers": [
    "01",
    "13",
    "14",
    "21",
    "24",
    "30"
  ],
  "blueNumbers": [
    "02"
  ]
}
```

### 红球范围：01-33（选6个）

### 蓝球范围：01-16（选1个）

## mcporter 故障排除

### 1. 检查 mcporter 安装

```bash
# 验证 mcporter 是否安装
 mcporter --version

# 查看帮助
 mcporter --help
```

### 2. 检查 MCP 服务器配置

```bash
# 列出所有已配置的 MCP 服务器
 mcporter list

# 查看特定服务器的详细信息
 mcporter list amcjt-mcp-server --schema

# 查看配置来源
 mcporter list --verbose
```

### 3. 测试工具调用

```bash
# 测试连接
 mcporter call amcjt-mcp-server.get_lottery_countdown --output json

# 查看详细日志
 mcporter call amcjt-mcp-server.get_lottery_countdown --log-level debug
```

### 4. 配置问题排查

```bash
# 查看当前使用的配置文件路径
 mcporter config list

# 添加/修改配置
 mcporter config add test-mcp https://your-mcp-server-url.com/mcp

# 导入其他编辑器的配置（Cursor、Claude、VS Code 等）
 mcporter config import cursor --copy
```

### 5. 环境变量未生效

如果使用 `${ENV_VAR}` 语法但变量未生效：

```bash
# 检查环境变量是否设置
echo $MOONSHOT_API_KEY  # Linux/Mac
# 或
echo %MOONSHOT_API_KEY%  # Windows

# 直接在命令行传递（覆盖配置文件）
MOONSHOT_API_KEY=your-key  mcporter call amcjt-mcp-server.ocr_lottery_ticket ...
```

## 参考链接

- [mcporter npm 包](https://www.npmjs.com/package/mcporter)
- [Model Context Protocol 规范](https://github.com/modelcontextprotocol/specification)
- [mcporter CLI 参考](https://github.com/steipete/mcporter/blob/main/docs/cli-reference.md)
- [mcporter 工具调用指南](https://github.com/steipete/mcporter/blob/main/docs/tool-calling.md)

## 注意事项

1. **mcporter 配置**: 使用前请确保 mcporter 已正确安装并配置，且已注册 amcjt-mcp-server
2. 图片调用 amcjt-mcp-server 的 ocr_lottery_ticket 识别时需要传入图片完整文件路径，不能用相对路径
3. 双色球 lottoType 的值需要为字符串 "101"，mcporter 调用建议使用函数调用语法来传递参数，规避 lottoType:101 传参被识别成 number 的问题
4. 期号格式：年份 + 3位序号（如2026020）, mcporter调用传递给mcp时也要为字符串
