---
name: coze-workflow-runner
description: 调用 Coze 工作流执行自动化任务，支持生成图片、处理数据等操作
---

# Coze 工作流运行器

## 概述

通过 Coze API 调用工作流，执行自动化任务。目前支持生成宠物知识卡片等图像生成工作流。

## 快速开始

### 1. 配置令牌

服务令牌存储在：`~/workspace-prod/coze/coze-tokens.md`

首次使用时确认令牌有效。

### 2. 查看可用工作流

工作流列表存储在：`~/workspace-prod/coze/workflows.md`

包含每个工作流的 ID、链接和用途说明。

### 3. 调用工作流

使用 `cozepy` 库调用：

```python
import cozepy

# 认证
auth = cozepy.TokenAuth(token='你的服务令牌')
coze = cozepy.Coze(auth=auth, base_url='https://api.coze.cn')

# 调用工作流
response = coze.workflows.runs.create(
    workflow_id='工作流ID',
    parameters={'input': '输入参数'}
)
```

## 现有工作流

### 短视频文案拆解（13层逻辑）

- **工作流 ID**: 7610429408704413759
- **用途**: 通过13层逻辑拆解短视频文案，输入抖音口令链接即可提取并分析底层逻辑
- **输入**: 抖音口令链接（如 7:/ xxx）
- **返回**: 短视频文案内容 + 13层逻辑拆解结果

**调用示例**:
```python
import cozepy

auth = cozepy.TokenAuth(token='你的服务令牌')
coze = cozepy.Coze(auth=auth, base_url='https://api.coze.cn')

response = coze.workflows.runs.create(
    workflow_id='7610429408704413759',
    parameters={'input': '7:/ xxx:】'}
)
```

### 生成宠物知识卡片

- **工作流 ID**: 7610527662062665754
- **用途**: 生成宠物知识卡片图片（5张）
- **输入**: 宠物名称和描述文本
- **返回**: 5个图片 URL（短链接形式）

**调用示例**:
```python
import cozepy

auth = cozepy.TokenAuth(token='你的服务令牌')
coze = cozepy.Coze(auth=auth, base_url='https://api.coze.cn')

response = coze.workflows.runs.create(
    workflow_id='7610527662062665754',
    parameters={'input': '布偶猫宠物知识卡片：布偶猫又称布拉多尔猫，是体型和体重最大的猫品种之一。'}
)

# 返回: {"output": ["https://s.coze.cn/t/xxx/", ...]}
```

### 处理返回的短链接

工作流返回的是短链接，需要跟随跳转才能获取真实图片 URL：

```python
import subprocess

urls = response['data']['output']
for i, url in enumerate(urls, 1):
    # curl -L 自动跟随跳转，直接下载图片
    subprocess.run(['curl', '-sL', url, '-o', f'pet_card_{i}.png'])
```

## 资源

### 配置目录
- `~/workspace-prod/coze/coze-tokens.md` - 服务令牌
- `~/workspace-prod/coze/workflows.md` - 工作流列表

---

*最后更新：2026-03-24*
