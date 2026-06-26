---
name: bole-story-creator
description: "Bole Story Creator is a skill that calls Bole AI platform to generate short drama stories, including story creation, storyboard generation, and video production."
license: MIT
compatibility: "需要 Python 3.8+，无特殊依赖。"
metadata:
  author: jiajianrong
  version: "1.0.0"
  python-version: ">=3.8"
  dependencies:
    - urllib
    - json
    - os
    - time
    - datetime
    - uuid
  tags:
    - story
    - video
    - creation
    - bole
    - ai
  env:
    - name: BOLE_ACCESS_KEY
      required: true
      desc: "Bole AI platform access key"
---

# Bole Story Creator

一个用于调用博乐AI平台生成短剧故事的 OpenClaw 技能。

## 功能介绍

该技能可以：
- 根据用户提供的故事创意生成完整的短剧故事
- 自动创建分镜脚本
- 生成视频内容
- 返回故事创作结果和视频链接

## 工作流程

1. 获取博乐AI平台访问令牌
2. 创建剧集和工作空间
3. 生成故事板
4. 初始化轨道并等待准备完成
5. 初始化视频生成并等待完成
6. 进行最终编辑并等待处理完成
7. 获取最终视频链接并返回结果

## 使用方法

### 环境变量配置

需要设置以下环境变量：

```bash
BOLE_ACCESS_KEY=your_bole_access_key
```

### 调用方式

作为 OpenClaw 技能调用：

```python
{
  "text": "生成一个关于友谊的故事"
}
```

### 执行命令

```bash
python scripts/main.py "{\"text\": \"生成友谊的故事\"}"
```

### 示例输入输出

**输入：**
```json
{
  "text": "生成乌鸦喝水的故事"
}
```

**输出：**
```json
{
  "result": "故事创作完成！projectId=2033716579396616193, episodeId=1234567890, workspaceId=0987654321。控制台链接：https://bole.bonanai.com/story/2033716579396616193?episodeId=1234567890 。视频链接：https://example.com/video.mp4"
}
```

## 注意事项

1. 调用前请确保已设置有效的 `BOLE_ACCESS_KEY`
2. 生成过程可能需要较长时间（3-5分钟），请耐心等待
3. 输出结果包含项目信息和视频链接，可直接访问查看
4. 请确保网络连接正常，能够访问博乐AI平台 API

## 故障排除

- **认证失败**：检查 `BOLE_ACCESS_KEY` 是否正确设置
- **网络错误**：确保网络连接正常，能够访问博乐AI平台
- **执行超时**：生成视频可能需要较长时间，请增加超时设置
- **结果为空**：检查博乐AI平台的服务状态

## 版本历史

- **v1.0.0**：初始版本，支持故事生成、分镜脚本创建和视频生成功能
