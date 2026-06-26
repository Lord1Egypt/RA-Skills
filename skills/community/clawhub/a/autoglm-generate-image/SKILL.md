---
name: autoglm-generate-image
description: >
  使用 AutoGLM 文生图接口，根据用户输入的文字描述生成图片。当用户需要生成图片、文字转图片、AI绘图等场景时使用此 skill。
  Token 通过本地服务 http://127.0.0.1:53699/get_token 自动获取，无需手动配置环境变量。
compatibility:
  requires:
    - Python 3、hashlib（内置）
---

# AutoGLM Generate Image Skill

根据用户输入的文字描述，调用 AutoGLM 文生图 API 生成图片并返回图片链接。

---

## API

| 项目 | 内容 |
|------|------|
| 地址 | `https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image` |
| 方式 | POST |
| 请求体 | `{"text": "<图片描述文字>"}` |

脚本启动时会先向本地服务发起 HTTP GET 请求获取 token：

| 项目 | 内容 |
|------|------|
| 地址 | `http://127.0.0.1:53699/get_token` |
| 方式 | GET |
| 返回 | `Bearer xxx`（直接作为 Authorization 头使用） |

> 若返回值不含 `Bearer` 前缀，脚本会自动补全。

**签名 Headers（每次动态生成）：**

- `X-Auth-Appid`: `100003`
- `X-Auth-TimeStamp`: 当前秒级 Unix 时间戳
- `X-Auth-Sign`: MD5(`100003 + "&" + timestamp + "&" + 38d2391985e2369a5fb8227d8e6cd5e5`)

---

## 执行脚本

使用同目录下的 `generate-image.py`：
```bash
python generate-image.py "澳洲龙虾"
```

---

## 返回结果处理

### 响应结构
```json
{
  "code": 0,
  "msg": "SUCCESS",
  "data": {
    "image_url": "https://..."
  }
}
```

### 输出要求

1. 从响应中提取 `data.image_url`
2. 以 Markdown 图片格式展示给用户：
```markdown
![生成图片](image_url)
```
