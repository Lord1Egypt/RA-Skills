---
name: dingtalk-shanji
description: 从钉钉闪记提取听记数据，包括列表、转写文本、摘要、待办等。当用户提到"钉钉闪记"、"听记"、"会议录音"、"转写文本"、"shanji"、"dws minutes"时触发此技能。
---

# 钉钉闪记数据提取技能

使用官方 `dws` CLI 工具从钉钉闪记提取数据。

## 前置条件检查

在执行任何操作前，先检查 `dws` 是否已安装：

```bash
command -v dws && dws --version || echo "dws 未安装"
```

## 安装 dws

如果 `dws` 未安装，按以下顺序尝试安装：

### 方式1：npm 安装（优先）

```bash
npm install -g dingtalk-workspace-cli
```

### 方式2：sh 脚本安装（npm 失败时）

**macOS / Linux：**

```bash
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh
```

**Windows (PowerShell)：**

```powershell
irm https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.ps1 | iex
```

### 安装后验证

```bash
dws --version
dws minutes --help
```

## 首次使用认证

首次使用需要登录认证：

```bash
dws login
```

按照提示完成 OAuth 设备流认证。

---

## 命令参考

### 列出听记

```bash
# 列出所有听记
dws minutes list all

# 列出我创建的听记
dws minutes list mine --max 20

# 列出分享给我的听记
dws minutes list shared

# 按关键词搜索
dws minutes list all --keyword "医美"

# 按时间范围筛选
dws minutes list all --start-time "2025-05-01" --end-time "2025-05-31"

# 输出JSON格式
dws minutes list all -f json
```

### 获取听记详情

```bash
# 获取基本信息（标题、时长、参与者）
dws minutes get info --id <taskUuid>

# 获取转写文本
dws minutes get transcription --id <taskUuid>

# 获取AI摘要
dws minutes get summary --id <taskUuid>

# 获取待办事项
dws minutes get todos --id <taskUuid>

# 获取关键词
dws minutes get keywords --id <taskUuid>

# 批量获取多个听记详情
dws minutes get batch --id <id1>,<id2>,<id3>
```

### 其他操作

```bash
# 更新标题
dws minutes update title --id <taskUuid> --title "新标题"

# 更新摘要
dws minutes update summary --id <taskUuid> --summary "新摘要"

# 替换转写文本中的错误
dws minutes replace-text --id <taskUuid> --find "错误文本" --replace "正确文本"

# 生成思维导图
dws minutes mind-graph create --id <taskUuid>

# 上传录音文件创建听记
dws minutes upload create --file "recording.mp3"
```

---

## 典型工作流程

### 1. 列出最近的听记

```bash
# 列出我创建的听记（JSON格式）
dws minutes list mine -f json
```

### 2. 获取特定听记的转写文本

```bash
# 先获取听记的taskUuid
dws minutes list mine --max 1 -f json | jq -r '.result.minutesDetails[0].taskUuid'

# 获取转写文本（使用 --id 参数）
dws minutes get transcription --id <taskUuid>

# 示例：
dws minutes get transcription --id 76327569643331323336383832345f3237323535323932305f32
```

### 3. 获取完整听记数据

```bash
# 获取详情（使用 --id 参数）
dws minutes get info --id <taskUuid> -f json

# 获取转写
dws minutes get transcription --id <taskUuid>

# 获取摘要
dws minutes get summary --id <taskUuid>

# 获取待办
dws minutes get todos --id <taskUuid>

# 示例：
TASK_UUID="76327569643331323336383832345f3237323535323932305f32"
dws minutes get info --id $TASK_UUID -f json
dws minutes get transcription --id $TASK_UUID
dws minutes get summary --id $TASK_UUID
```

---

## 输出格式

使用 `-f json` 参数获取JSON格式输出，便于程序处理：

```bash
dws minutes list all -f json
```

JSON输出示例：

```json
[
  {
    "id": "76327569643331323336383832345f3237323535323932305f32",
    "title": "05-29 医美行业AI销售智能解决方案",
    "creator": "张三",
    "createTime": "2025-05-29T10:00:00Z",
    "duration": 7470,
    "participantCount": 5
  }
]
```

---

## 常用参数

| 参数        | 说明                 |
| ----------- | -------------------- |
| `-f json`   | JSON格式输出         |
| `-f table`  | 表格格式输出（默认） |
| `-f raw`    | 原始格式输出         |
| `--help`    | 查看帮助             |
| `--verbose` | 详细日志             |

---

## 注意事项

1. **首次使用需登录**：执行 `dws login` 完成认证
2. **企业授权**：需要企业管理员授权才能访问数据
3. **权限控制**：只能访问自己有权限的听记
4. **命令行工具**：比浏览器方案更轻量、更高效

---

## 与浏览器方案对比

| 特性     | dws CLI        | 浏览器方案           |
| -------- | -------------- | -------------------- |
| 安装     | 简单（npm/sh） | 复杂（Playwright）   |
| 速度     | 快             | 慢                   |
| 资源消耗 | 低             | 高                   |
| 维护     | 官方维护       | 需自己维护           |
| 认证     | OAuth设备流    | Cookie注入           |
| 稳定性   | 高             | 低（页面变化会失效） |
