---
name: aliyun-image
description: "阿里云百炼图像生成、编辑与翻译。文生图：根据文本生成图像，支持复杂文字渲染。图像编辑：单图编辑、多图融合、风格迁移、物体增删。图像翻译：翻译图像中的文字，保留原始排版，支持11种源语言和14种目标语言。触发词：生成图片、AI作画、文生图、图像编辑、修图、换背景、风格迁移、多图融合、图像翻译、图片翻译。模型：qwen-image-plus(默认)、qwen-image-max、qwen-image-edit-plus(默认)、qwen-image-edit-max、qwen-mt-image。"
metadata:
  {
    "openclaw":
      {
        "repository": "https://github.com/StanleyChanH/aliyun-image-skill",
        "clawhub": "https://clawhub.com/skill/aliyun-image",
        "sync": "GitHub 和 ClawHub 同步更新"
      }
  }
---

# 阿里云百炼图像生成与编辑

> 🔄 **同步更新**：本项目在 [GitHub](https://github.com/StanleyChanH/aliyun-image-skill) 和 [ClawHub](https://clawhub.com/skill/aliyun-image) 同步发布。

## 快速开始

### 前提条件

```bash
# 配置 API Key
export DASHSCOPE_API_KEY="sk-xxxx"
```

### 文生图

```python
import os, requests

resp = requests.post(
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    headers={"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"},
    json={
        "model": "qwen-image-plus",
        "input": {"messages": [{"role": "user", "content": [{"text": "一只橘猫在阳光下打盹"}]}]},
        "parameters": {"prompt_extend": True, "watermark": False}
    }
)
print(resp.json()["output"]["choices"][0]["message"]["content"][0]["image"])
```

### 图像编辑

```python
resp = requests.post(
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    headers={"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"},
    json={
        "model": "qwen-image-edit-plus",
        "input": {"messages": [{"role": "user", "content": [
            {"image": "https://example.com/photo.jpg"},
            {"text": "把背景换成星空"}
        ]}]},
        "parameters": {"prompt_extend": True, "watermark": False}
    }
)
print(resp.json()["output"]["choices"][0]["message"]["content"][0]["image"])
```

### 图像翻译

```python
import os, requests, time

# 1. 创建翻译任务
resp = requests.post(
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis",
    headers={
        "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
        "X-DashScope-Async": "enable"
    },
    json={
        "model": "qwen-mt-image",
        "input": {
            "image_url": "https://example.com/english-poster.jpg",
            "source_lang": "en",
            "target_lang": "zh"
        }
    }
)
task_id = resp.json()["output"]["task_id"]

# 2. 轮询获取结果
while True:
    time.sleep(3)
    result = requests.get(
        f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"}
    ).json()
    if result["output"]["task_status"] == "SUCCEEDED":
        print(result["output"]["image_url"])
        break
```

---

## 默认配置

| 场景 | 默认模型 | 高质量模型 |
|------|----------|------------|
| 文生图 | `qwen-image-plus` | `qwen-image-max` |
| 图像编辑 | `qwen-image-edit-plus` | `qwen-image-edit-max` |
| 图像翻译 | `qwen-mt-image` | - |

**规则**：默认使用 Plus 系列，仅当用户明确要求"最好的"、"最高质量"时使用 Max 系列。

### 默认参数

```json
{
  "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感",
  "prompt_extend": true,
  "watermark": false
}
```

---

## 详细参考

按需加载以下文档：

| 文档 | 用途 |
|------|------|
| [references/text-to-image.md](references/text-to-image.md) | 文生图完整API参考：模型列表、分辨率、所有参数 |
| [references/image-edit.md](references/image-edit.md) | 图像编辑完整API参考：单图编辑、多图融合、输入要求 |
| [references/image-translate.md](references/image-translate.md) | 图像翻译完整API参考：支持语言、异步调用、术语定义 |

---

## 工具脚本

| 脚本 | 用途 |
|------|------|
| [scripts/client.py](scripts/client.py) | 封装好的API客户端，支持文生图、图像编辑和图像翻译 |

**使用脚本**：

```bash
# 文生图
python scripts/client.py generate "一只橘猫在阳光下打盹" --size 1920*1080

# 图像编辑
python scripts/client.py edit "https://example.com/photo.jpg" "把背景换成星空" -n 2

# 图像翻译
python scripts/client.py translate "https://example.com/english.jpg" --source en --target zh
```

---

## 关键注意事项

1. **图像URL有效期**：生成的图像URL仅保留 **24小时**，请及时下载
2. **地域**：API Key 和请求地址必须属于同一地域（北京/新加坡）
3. **费用**：按成功生成的图像张数计费

---

## 常见错误

| 错误码 | 原因 | 解决方案 |
|--------|------|----------|
| `InvalidApiKey` | API Key无效 | 检查环境变量配置 |
| `InvalidParameter` | 参数错误 | 检查请求格式 |
| `DataInspectionFailed` | 内容审核失败 | 修改输入内容 |
