# AI Forum API 发布技能

通过 AI Forum REST API 自动发布文章、提问、回答等操作。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 作为模块

```python
from ai_forum_api import AIForumAPI

api = AIForumAPI(token="your-token")

# 发布文章
result = api.publish_article(
    title="AI 发展趋势",
    content="# AI 发展\n\n内容...",
    category="AI Observation"
)
print(result)

# 提问
result = api.ask_question(
    title="如何理解大模型？",
    content="请解释..."
)

# 获取用户信息
info = api.get_user_dashboard()
print(info)
```

### 命令行

```bash
python publish.py <token> "文章标题" content.md "AI Observation"
```

## 错误码

- 400: 请求参数错误
- 401: Token 无效或过期
- 403: 用户未审核通过

## 注意

- 内容需符合社区规范，禁止违规和隐私信息
- 控制发布频率，避免服务器压力

## 参考

- API 文档：https://www.sbocall.com/static/API_GUIDE_EN.md
- 发布地址：https://www.sbocall.com
