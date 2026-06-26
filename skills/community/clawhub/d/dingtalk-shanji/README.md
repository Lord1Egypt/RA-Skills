# 钉钉闪记数据提取技能

使用官方 `dws` CLI 工具从钉钉闪记提取数据。

## 功能

- 📋 列出听记列表
- 📝 获取转写文本
- 📊 获取AI摘要
- ✅ 获取待办事项
- 🔍 搜索听记
- 🎯 获取关键词

## 快速开始

### 1. 检查是否已安装 dws

```bash
command -v dws && dws --version || echo "dws 未安装"
```

### 2. 安装 dws

**npm 安装（推荐）：**
```bash
npm install -g dingtalk-workspace-cli
```

**或 sh 脚本安装：**
```bash
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh
```

### 3. 登录认证

```bash
dws login
```

### 4. 使用命令

```bash
# 列出我的听记
dws minutes list mine

# 获取转写文本
dws minutes get transcription <minutes-id>

# 获取摘要
dws minutes get summary <minutes-id>
```

## 命令列表

### 列出听记

```bash
dws minutes list all          # 所有听记
dws minutes list mine         # 我创建的
dws minutes list shared       # 分享给我的
```

### 获取详情

```bash
# 注意：需要使用 --id 参数指定 taskUuid
dws minutes get info --id <taskUuid>          # 基本信息
dws minutes get transcription --id <taskUuid> # 转写文本
dws minutes get summary --id <taskUuid>       # AI摘要
dws minutes get todos --id <taskUuid>         # 待办事项
dws minutes get keywords --id <taskUuid>      # 关键词
```

### 其他操作

```bash
dws minutes update title      # 更新标题
dws minutes update summary    # 更新摘要
dws minutes replace-text      # 替换文本
dws minutes mind-graph create # 生成思维导图
```

## 输出格式

```bash
# JSON格式（便于程序处理）
dws minutes list all -f json

# 表格格式（默认，便于阅读）
dws minutes list all -f table

# 原始格式
dws minutes list all -f raw
```

## 典型用例

### 用例1：获取最近听记的转写文本

```bash
# 获取最近的听记 taskUuid
TASK_UUID=$(dws minutes list mine --max 1 -f json | jq -r '.result.minutesDetails[0].taskUuid')

# 获取转写文本
dws minutes get transcription --id $TASK_UUID
```

### 用例2：搜索并导出听记

```bash
# 搜索包含"医美"的听记
dws minutes list all --query "医美" --max 10 -f json

# 获取转写文本并保存
dws minutes get transcription --id <taskUuid> > transcript.txt
```

### 用例3：获取完整听记数据

```bash
# 定义 taskUuid
TASK_UUID="76327569643331323336383832345f3237323535323932305f32"

# 获取详情
dws minutes get info --id $TASK_UUID -f json

# 获取转写
dws minutes get transcription --id $TASK_UUID

# 获取摘要
dws minutes get summary --id $TASK_UUID

# 获取待办
dws minutes get todos --id $TASK_UUID
```

## 相关资源

- [GitHub 仓库](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [命令文档](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/docs/command-index.md)
- [中文文档](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/README_zh.md)

## License

MIT
