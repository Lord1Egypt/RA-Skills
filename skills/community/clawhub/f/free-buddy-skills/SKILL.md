---
title: "Free Buddy Skills"
summary: "一键配置 opencode.ai 免费 AI 模型到 WorkBuddy,无需 API Key"
read_when:
  - 用户需要配置免费 AI 模型
  - 用户提到"免费模型"、"opencode"、"free model"
---

# Free Buddy Skills

自动检测和配置 opencode.ai 的免费 AI 模型到 WorkBuddy。

## 触发词

当用户说以下内容时,使用此技能:

- "帮我配置 opencode.ai 的免费模型"
- "配置免费模型"
- "添加 opencode 模型"
- "免费 AI 模型"
- "更新免费模型"
- "free model"
- "opencode.ai"

## 功能

1. **查询免费模型**: 从 opencode.ai 获取最新的免费模型列表
2. **自动配置**: 将免费模型添加到 `~/.workbuddy/models.json`
3. **定期更新**: 保持模型配置的时效性

## 权限说明

- **无需 API Key**: 使用公开的 `"public"` 作为 API Key
- **无需认证**: opencode.ai 免费模型无需登录
- **仅本地操作**: 只读取和写入本地的 `~/.workbuddy/models.json`

## 快速使用

用户只需发送一句话:

**首次配置:**
> "帮我配置 opencode.ai 的免费模型"

WorkBuddy 会自动:
1. 查询最新的免费模型列表
2. 添加到 `~/.workbuddy/models.json`
3. 验证配置是否可用

**更新模型:**
> "更新免费模型"

WorkBuddy 会自动:
1. 查询最新的免费模型列表
2. 对比现有配置
3. 添加新模型,跳过已存在的

## 使用流程

### 方法 1: 使用 Python 脚本 (推荐)

```bash
# 所有平台通用 (macOS / Linux / Windows)
python3 update-free-models.py
# 或
python update-free-models.py
```

### 方法 2: 手动配置

#### 步骤 1: 查询可用免费模型

```bash
curl -sS https://opencode.ai/zen/v1/models | jq '.data[].id' | grep -i free
```

#### 步骤 2: 获取模型详细信息

```bash
curl -sS https://opencode.ai/zen/v1/models | jq '.data[] | select(.id | contains("free"))'
```

#### 步骤 3: 读取现有配置

读取 `~/.workbuddy/models.json` (macOS/Linux) 或 `%USERPROFILE%\.workbuddy\models.json` (Windows) 检查是否已存在相同模型。

#### 步骤 4: 添加或更新模型配置

为每个免费模型添加以下配置:

```json
{
  "id": "模型ID",
  "name": "模型显示名称",
  "vendor": "OpenCode AI",
  "url": "https://opencode.ai/zen/v1/chat/completions",
  "apiKey": "使用 public (无需真实密钥)",
  "maxInputTokens": 262144,
  "supportsToolCall": true,
  "supportsImages": false,
  "supportsReasoning": true
}
```

### 步骤 5: 验证配置

使用 `read_file` 工具读取 `~/.workbuddy/models.json` 确认配置已正确添加。

## 当前免费模型列表

| 模型 ID | 名称 | 工具调用 | 图像 | 推理 |
|---------|------|----------|------|------|
| minimax-m2.5-free | MiniMax M2.5 Free | ✅ | ❌ | ✅ |
| trinity-large-preview-free | Trinity Large Preview Free | ✅ | ✅ | ✅ |
| nemotron-3-super-free | Nemotron-3 Super Free | ✅ | ✅ | ✅ |

## 配置保存位置

- **macOS/Linux**: `~/.workbuddy/models.json`
- **Windows**: `%USERPROFILE%\.workbuddy\models.json` (即 `C:\Users\你的用户名\.workbuddy\models.json`)
- **跨平台**: `$HOME/.workbuddy/models.json` (Git Bash/WSL 下通用)

## 注意事项

1. opencode.ai 的免费模型使用 `"public"` 作为 API Key
2. 所有免费模型共享同一个端点: `https://opencode.ai/zen/v1/chat/completions`
3. 脚本需要用户确认后才会修改配置文件
4. 非交互模式下运行将跳过自动添加,需手动确认
