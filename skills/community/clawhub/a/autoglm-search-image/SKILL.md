---
name: autoglm-search-image
description: >
  使用 AutoGLM 搜图接口，根据用户输入的关键词搜索相关图片。当用户需要搜索图片、查找图片素材等场景时使用此 skill。
  Token 通过本地服务 http://127.0.0.1:53699/get_token 自动获取，无需手动配置环境变量。
compatibility:
  requires:
    - Python 3.x（标准库，无需额外安装）
---

# AutoGLM Search Image Skill

根据用户输入的关键词，调用 AutoGLM 搜图 API 返回相关图片列表。

---

## API

| 项目 | 内容 |
|------|------|
| 地址 | `https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/search-image` |
| 方式 | POST |
| 请求体 | `{"query": "<搜索关键词>"}` |

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

使用同目录下的 `search-image.py`：
```bash
python search-image.py "猫咪"
```

无需安装第三方依赖，仅使用 Python 标准库。

---

## 返回结果处理

### 响应结构
```json
{
  "code": 0,
  "msg": "SUCCESS",
  "data": {
    "results": [
      {
        "original_url": "图片链接",
        "caption": "图片描述",
        "source": "来源",
        "original_width": 1267,
        "original_height": 845
      }
    ],
    "query": "搜索词",
    "count": 4
  }
}
```

### 输出要求

遍历 `data.results`，以 Markdown 格式展示每张图片及其描述：
```markdown
**1. 图片描述（来源）**
![图片描述](original_url)
```
