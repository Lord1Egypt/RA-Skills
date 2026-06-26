# 百度星河社区 ERNIE-Image API 参考文档

## 接口基础信息

| 项目 | 值 |
|---|---|
| 基础域名 | `https://aistudio.baidu.com/llm/lmapi/v3` |
| 文生图接口 | `POST /images/generations` |
| 完整 URL | `https://aistudio.baidu.com/llm/lmapi/v3/images/generations` |
| 接口格式 | 兼容 OpenAI images.generate 格式 |

## 认证方式

在 HTTP Header 中传递 Bearer Token：

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**获取 Access Token 地址：** https://aistudio.baidu.com/account/accessToken

## 请求参数

### Request Body（JSON）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 模型名称，见下表 |
| `prompt` | string | 是 | 图像生成描述文本 |
| `response_format` | string | 否 | `url`（返回链接）或 `b64_json`（返回base64），默认 `url` |
| `n` | integer | 否 | 生成图片数量，默认 1 |

### 可用模型

| 模型名称 | 特点 |
|---|---|
| `ERNIE-Image` | 完整版，图像质量更高，生成较慢 |
| `ERNIE-Image-Turbo` | 快速版（推荐），仅8步推理，速度快 |
| `Stable-Diffusion-XL` | SDXL 模型，风格多样 |

## 响应格式

```json
{
  "created": 1714000000,
  "data": [
    {
      "url": "https://...",        // response_format=url 时返回
      "b64_json": "iVBORw0KGgo..."  // response_format=b64_json 时返回
    }
  ]
}
```

## 示例代码

### Python（纯标准库，无需第三方包）

```python
import urllib.request
import json
import base64

ACCESS_TOKEN = "your_access_token_here"

payload = json.dumps({
    "model": "ERNIE-Image-Turbo",
    "prompt": '将文字"张伟"设计成中国风书法艺术字，金色，红色背景',
    "response_format": "b64_json",
    "n": 1
}).encode("utf-8")

req = urllib.request.Request(
    url="https://aistudio.baidu.com/llm/lmapi/v3/images/generations",
    data=payload,
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read())

# 保存图片
with open("output.png", "wb") as f:
    f.write(base64.b64decode(result["data"][0]["b64_json"]))
```

### Python（使用 openai 包）

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_access_token_here",
    base_url="https://aistudio.baidu.com/llm/lmapi/v3"
)

result = client.images.generate(
    model="ERNIE-Image-Turbo",
    prompt='将文字"张伟"设计成中国风书法艺术字，金色，红色背景',
    response_format="b64_json"
)
```

## 配置文件格式

Skill 配置文件 `config.json` 位于 skill 安装目录根路径下（即 `SKILL.md` 同级目录）。

```json
{
  "access_token": "your_access_token_here",
  "model": "ERNIE-Image-Turbo",
  "output_dir": "./art_names"
}
```

通过脚本自动写入（推荐）：
```bash
python3 scripts/generate_art_name.py --set-token YOUR_TOKEN
```

## Prompt 写作技巧（艺术字）

好的艺术字 Prompt 应包含：
1. **明确标注文字内容**：用引号将名字括起来，如 `将文字"张三"设计成...`
2. **指定字体风格**：书法、印刷体、手写体等
3. **颜色描述**：主色调、渐变方向
4. **背景/氛围**：背景颜色或场景
5. **质量要求**：高分辨率、清晰可辨、精细质感

### 示例 Prompt

```
将文字"张伟"设计成中国传统书法艺术字，毛笔字体，水墨风格，金色文字，
红色背景，古典纹样装饰，大气磅礴，文字清晰可辨，高分辨率，正方形构图
```

## 注意事项

- Access Token 有效期：登录后长期有效，但 Token 泄露需立即重置
- 免费额度：每账户 100万 Tokens
- 超时设置：建议 timeout=120 秒（模型推理时间较长）
- 生成失败常见原因：Token 无效、Prompt 触发审核、网络超时
