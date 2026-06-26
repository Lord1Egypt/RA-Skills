# Claude Code + MiniMax-M2.5 配置与使用完全指南

使用 MiniMax-M2.5 模型通过 Claude Code 进行 AI 编程的完整教程。

---

## 一、什么是 Claude Code？

Claude Code 是 Anthropic 推出的 AI 编程助手，可以：
- 读写代码、创建/修改文件
- 执行命令、运行测试
- 帮你完成编程任务
- 支持上下文理解和连续对话

**注意**：默认使用 Anthropic API，接入 MiniMax 后可使用国产模型。

---

## 二、配置步骤

### 前置要求
1. 已安装 Claude Code
2. 已拥有 MiniMax API Key（从 platform.minimaxi.com 获取）

### 重要提示

> 在配置前，请确保清除以下 Anthropic 相关的环境变量，以免影响 MiniMax API 的正常使用：
> - `ANTHROPIC_AUTH_TOKEN`
> - `ANTHROPIC_BASE_URL`

### 方式一：cc-switch（推荐，最简单）

cc-switch 是一个可视化工具，可以快速切换 Claude Code 的 API 配置。

#### 1. 安装 cc-switch

```bash
# macOS / Linux
brew tap farion1231/ccswitch
brew install --cask cc-switch

# Windows
# 前往 https://github.com/farion1231/cc-switch/releases 下载安装包
```

#### 2. 添加 MiniMax 配置

1. 启动 cc-switch 应用
2. 点击右上角 **"+"** 按钮
3. 在预设供应商列表中选择 **MiniMax**
4. 填写您的 MiniMax API Key
5. 点击确认

#### 3. 配置模型名称

1. 在配置列表中，找到刚添加的 MiniMax 配置
2. 将模型名称修改为：`MiniMax-M2.5`（全部模型都要改）
3. 点击右下角 **"添加"**

#### 4. 启用配置

1. 回到 cc-switch 首页
2. 找到您的 MiniMax 配置
3. 点击 **"启用"** 按钮

#### 5. 编辑配置文件

编辑 `~/.claude.json` 文件（如果不存在则创建）：

```json
{
  "hasCompletedOnboarding": true
}
```

---

### 方式二：手动配置（适合高级用户）

#### 1. 编辑 ~/.claude/settings.json

```bash
# 如果文件不存在则创建
touch ~/.claude/settings.json
```

添加以下内容（将 `你的MINIMAX_API_KEY` 替换为实际 API Key）：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "你的MINIMAX_API_KEY",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_SMALL_FAST_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.5"
  }
}
```

#### 2. 编辑 ~/.claude.json

```bash
# 如果文件不存在则创建
touch ~/.claude.json
```

添加以下内容：

```json
{
  "hasCompletedOnboarding": true
}
```

---

### 方式三：VS Code 插件配置

如果你使用 VS Code，可以配置 Claude Code 插件。

#### 1. 安装插件

在 VS Code 扩展商店搜索 "Claude Code" 并安装。

#### 2. 配置模型

两种方式：

**方式A：设置界面**
1. 打开 VS Code 设置
2. 搜索 "Claude Code: Selected Model"
3. 输入 `MiniMax-M2.5`

**方式B：settings.json**
```json
{
  "claude-code.selectedModel": "MiniMax-M2.5"
}
```

#### 3. 配置环境变量

1. 打开 VS Code 设置
2. 点击 "Edit in settings.json"
3. 添加以下配置：

```json
"claudeCode.environmentVariables": [
  {
    "name": "ANTHROPIC_BASE_URL",
    "value": "https://api.minimaxi.com/anthropic"
  },
  {
    "name": "ANTHROPIC_AUTH_TOKEN",
    "value": "你的MINIMAX_API_KEY"
  },
  {
    "name": "API_TIMEOUT_MS",
    "value": "3000000"
  },
  {
    "name": "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
    "value": "1"
  },
  {
    "name": "ANTHROPIC_MODEL",
    "value": "MiniMax-M2.5"
  },
  {
    "name": "ANTHROPIC_SMALL_FAST_MODEL",
    "value": "MiniMax-M2.5"
  },
  {
    "name": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "value": "MiniMax-M2.5"
  },
  {
    "name": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "value": "MiniMax-M2.5"
  },
  {
    "name": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "value": "MiniMax-M2.5"
  }
]
```

---

## 三、使用方法

### 3.1 启动 Claude Code

```bash
# 进入项目目录
cd 你的项目文件夹

# 启动对话模式
claude

# 或直接指定任务（一次性执行）
claude "帮我写一个 Python 脚本"
```

### 3.2 首次使用设置

首次启动时：
1. Claude Code 会询问是否信任当前目录
2. 输入 `y` 选择 **"Trust This Folder"**
3. 即可开始对话

### 3.3 核心命令

| 命令 | 说明 |
|------|------|
| `claude` | 启动交互式对话 |
| `claude -p "任务描述"` | 一次性任务模式 |
| `Ctrl+C` | 中断当前对话 |
| `Ctrl+L` | 清屏 |
| `y` | 确认执行代码修改 |
| `n` | 拒绝执行 |

### 3.4 对话流程

```bash
# 1. 启动
$ cd myproject
$ claude

# 2. 首次信任目录
The current directory is /path/to/myproject. Type 'y' to allow Claude to read and edit files in this directory, or 'n' to exit.
→ y

# 3. 开始对话
Hello! How can I help you today?

# 4. 提出需求
> 帮我写一个 Python 脚本，批量重命名文件

# 5. Claude 会先展示计划
# 然后输入 y 确认执行
→ y

# 6. 查看结果
# 文件已创建完成
```

### 3.5 常用场景

#### 场景1：写新代码
```
> 帮我写一个 Python 脚本，读取 CSV 文件并生成统计图表
```

#### 场景2：调试代码
```
> 这个代码运行报错：xxx，请帮我修复
```

#### 场景3：代码审查
```
> 请审查 src/app.py 的代码质量，并提出改进建议
```

#### 场景4：重构代码
```
> 请重构这个函数，使其更易读和高效
```

#### 场景5：写测试
```
> 为 src/utils.py 编写单元测试
```

#### 场景6：解释代码
```
> 解释这段代码的功能：
```

#### 场景7：项目初始化
```
> 帮我创建一个 React 项目，使用 TypeScript
```

### 3.6 对话技巧

1. **明确需求**：越具体越好
   - ❌ "帮我写个程序"
   - ✅ "帮我写一个 Python 脚本，读取 /data/users.csv，统计每个城市的用户数量，输出为 JSON 文件"

2. **分步进行**：复杂任务分多次对话
   ```
   # 第一次
   > 先帮我设计数据库结构
   
   # 第二次
   > 基于这个结构，帮我写 CRUD API
   ```

3. **查看文件**：让 Claude 读取现有代码
   ```
   > 读取 src/index.js，然后帮我添加登录功能
   ```

---

## 四、VS Code 插件使用

### 4.1 打开插件

- 侧边栏点击 Claude Code 图标
- 或使用快捷键 `Cmd+Shift+L` (Mac) / `Ctrl+Shift+L` (Windows)

### 4.2 对话方式

1. 在输入框输入需求
2. Claude 会分析代码并给出方案
3. 点击 "Accept" 应用修改

---

## 五、故障排除

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 认证失败 | API Key 错误 | 检查 MiniMax API Key 是否正确 |
| 连接超时 | 网络问题 | 确认网络可访问 api.minimaxi.com |
| 模型不响应 | 配置错误 | 检查 ANTHROPIC_MODEL 是否为 MiniMax-M2.5 |
| 请求超时 | 超时时间太短 | 增加 API_TIMEOUT_MS 到 3000000 |

### 调试命令

```bash
# 查看详细日志
claude --verbose

# 查看当前配置
cat ~/.claude/settings.json

# 测试 API 连接
curl -H "Authorization: Bearer 你的APIKEY" https://api.minimaxi.com/anthropic/v1/models
```

### 重新配置

如果配置出错：
1. 删除配置文件：`rm ~/.claude/settings.json`
2. 重新按教程配置

---

## 六、注意事项

1. **环境变量优先级**：命令行设置的环境变量 > 配置文件
2. **API Key 安全**：不要将 API Key 提交到公开仓库
3. **使用配额**：注意 MiniMax API 的调用配额限制
4. **超时设置**：长代码生成建议设置 5 分钟超时
5. **清除旧配置**：如果之前配置过 Anthropic，需要清除相关环境变量

---

## 七、获取帮助

- MiniMax 平台：https://platform.minimaxi.com
- Claude Code 文档：https://docs.claude.com
- cc-switch GitHub：https://github.com/farion1231/cc-switch
