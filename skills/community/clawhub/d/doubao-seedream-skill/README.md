# Seedream 图片生成 API

调用火山引擎 Seedream 图片生成模型，支持文生图功能。

## 环境配置

1. 安装依赖：
   ```bash
   pip install requests python-dotenv
   ```

2. 配置环境变量：
   ```
   VOLCENGINE_API_KEY=你的火山引擎API Key
   ```

## 快速使用

```bash
python seedream_api.py "一只可爱的橘猫"
```

## 支持的模型

| 名称 | Model ID | 说明 |
|------|----------|------|
| 5.0 (默认) | `doubao-seedream-5-0-260128` | 最新版本 |
| 4.5 | `doubao-seedream-4-5-251128` | |
| 4.0 | `doubao-seedream-4-0-250828` | |
| 3.0-t2i | `doubao-seedream-3-0-t2i-250415` | 仅文生图 |

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 图片描述 | 必填 |
| -m, --model | 模型版本 | 5.0 |
| -s, --size | 图片尺寸 | 2048x2048 |
| -o, --output-dir | 输出目录 | output |
| --steps | 推理步数 1-50 | 50 |
| --guidance | 引导系数 1-20 | 7.5 |
| --seed | 随机种子 | - |
| --negative | 负向提示词 | - |

## 使用示例

```bash
# 默认 5.0 模型
python seedream_api.py "一只可爱的橘猫"

# 指定 4.5 模型
python seedream_api.py "一只可爱的橘猫" -m 4.5

# 指定尺寸
python seedream_api.py "一只可爱的橘猫" -s "1024x1024"
```

## Python 代码调用

```python
from seedream_api import generate_image

# 简单调用
result = generate_image("一只可爱的橘猫")
print(result["local_paths"])

# 高级调用
result = generate_image(
    prompt="一只可爱的橘猫",
    model="5.0",
    size="2048x2048",
    guidance_scale=7.5,
    seed=42,
    negative_prompt="模糊、低质量"
)
```

## 功能说明

- **文生图**: 输入文本提示词生成图片

## 输出

生成图片自动保存到 `output` 目录。
