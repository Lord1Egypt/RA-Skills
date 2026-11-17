# OpenClaw 多模态预处理配置参考

## multimodalPreprocess 配置

在 `openclaw.json` 中添加：

```json
{
  "multimodalPreprocess": {
    "enable": true,
    "visionSkillId": "nex-n2-image-analyzer",
    "promptTemplate": "以下是图片的完整分析结果，请严格基于该内容回答用户问题：\n{{skillResult}}\n\n用户问题：{{userQuery}}"
  },
  "skills": {
    "entries": {
      "nex-n2-image-analyzer": {
        "enabled": true,
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "NEXN2_API_KEY"
        },
        "env": {
          "NEXN2_BASE_URL": "https://api.siliconflow.cn/v1",
          "NEXN2_MODEL_NAME": "nex-agi/Nex-N2-Pro",
          "NEXN2_IMAGE_COMPRESS": "true",
          "NEXN2_CACHE_ENABLE": "true",
          "NEXN2_CACHE_TTL_DAYS": "7",
          "NEXN2_TIMEOUT_MS": "30000"
        }
      }
    }
  }
}
```

## 配置项说明

| 字段 | 说明 |
|------|------|
| `multimodalPreprocess.enable` | 开启全局图片预处理 |
| `multimodalPreprocess.visionSkillId` | 指定处理图片的 Skill 名称 |
| `multimodalPreprocess.promptTemplate` | 拼接结果的模板，`{{skillResult}}` 是 Skill 返回的 content，`{{userQuery}}` 是用户消息 |

## 切换至 OpenRouter

如果使用 OpenRouter 代替 SiliconFlow：

```json
{
  "NEXN2_BASE_URL": "https://openrouter.ai/api/v1",
  "NEXN2_MODEL_NAME": "nex-agi/nex-n2-pro"
}
```

> 注意：OpenRouter 上的模型 ID 可能与 SiliconFlow 略有不同，以实际注册名称为准。

## 不使用全局预处理

如果仅需工具调用模式（非自动触发），保留 `skills.entries` 配置但**不添加** `multimodalPreprocess` 块，并在系统提示词中补充工具调用指令：

> 当用户发送图片、截图、照片、文档截图时，请调用 analyze_image_by_nexn2 工具获取图片的文字与内容描述，再基于返回结果作答。
