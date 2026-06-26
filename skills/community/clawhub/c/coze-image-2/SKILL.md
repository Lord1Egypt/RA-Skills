---
name: coze-image
description: |
  扣子(Coze) Seedream 4.5 图片生成工具。通过 Coze API 调用图片生成工作流，支持文本生成图片。
  当用户要求"生成图片"、"AI画图"、"用Coze生成图片"时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
    emoji: "🎨"
    homepage: https://www.coze.cn
    os:
      - darwin
      - linux
      - win32
---

# 扣子图片生成工具

你是"AI图片生成助手"。当前置配置完成后，用户要求生成图片时，按以下流程执行：

## 前置配置

在 `coze_image.py` 中配置：
```python
CONFIG = {
    "api_token": "YOUR_COZE_API_TOKEN",    # Coze API Token
    "workflow_id": "YOUR_WORKFLOW_ID",     # 图片生成工作流 ID
    "api_url": "https://api.coze.cn/v1/workflow/run"
}
```

**获取方式**：
- API Token：登录 https://www.coze.cn → API管理 → 授权 → 创建Token
- Workflow ID：在工作流URL中查找，如 `workflow_id=7644576791978033769`

## 使用方式

用户说"生成一张图片"或类似需求时：
1. 确认图片描述（提示词）
2. 运行命令：`python coze_image.py generate "描述内容"`
3. 返回生成的图片 URL

## 输出

返回格式：`https://s.coze.cn/t/xxx/` 的图片链接