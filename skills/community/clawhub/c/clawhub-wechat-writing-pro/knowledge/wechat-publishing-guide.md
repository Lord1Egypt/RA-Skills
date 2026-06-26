# 📤 微信公众号发布完整指南

> 从创作到发布的全流程操作手册

---

## 📋 发布流程概览

```
创作内容 → Markdown排版 → 生成HTML → 上传图片 → 创建草稿 → 发布/预览
```

---

## 一、发布前置准备

### 1.1 必需凭证（已脱敏）

| 凭证 | 说明 | 获取方式 |
|:-----|:-----|:---------|
| `App ID` | 公众号唯一标识 | 公众号后台 → 开发 → 基本配置 |
| `App Secret` | 公众号密钥 | 公众号后台 → 开发 → 基本配置 |
| `Access Token` | 接口调用凭证 | 通过 API 自动获取 |

### 1.2 可选配置

| 配置项 | 用途 |
|:-------|:-----|
| 默认封面图 `thumb_media_id` | 文章封面（无封面时使用） |
| 作者名称 | 显示在标题下方 |
| 摘要 | 不填则自动截取正文前54字 |

---

## 二、发布 API 接口

### 2.1 获取 Access Token

```bash
curl -X GET "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
```

**响应示例：**
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

### 2.2 上传图片（封面图）

**接口：** `POST https://api.weixin.qq.com/cgi-bin/material/add_material`

**参数：**
- `access_token`: 接口调用凭证
- `type`: `thumb`（封面图）
- `media`: 图片文件

**响应：**
```json
{
  "media_id": "THUMB_MEDIA_ID",
  "url": "https://mmbiz.qpic.cn/..."
}
```

### 2.3 上传正文图片

**接口：** `POST https://api.weixin.qq.com/cgi-bin/media/uploadimg`

**用途：** 上传文章内嵌图片，返回 URL 直接用于 `<img src="url">`

**响应：**
```json
{
  "url": "https://mmbiz.qpic.cn/mmbiz_png/..."
}
```

### 2.4 创建草稿

**接口：** `POST https://api.weixin.qq.com/cgi-bin/draft/add`

**请求体：**
```json
{
  "articles": [
    {
      "title": "文章标题",
      "author": "作者名称",
      "content": "<p>HTML正文内容</p>",
      "thumb_media_id": "封面图素材ID",
      "digest": "摘要（可选）",
      "content_source_url": "阅读原文链接（可选）",
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
}
```

**响应：**
```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

### 2.5 发布草稿

**接口：** `POST https://api.weixin.qq.com/cgi-bin/freepublish/submit`

**请求体：**
```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

**响应：**
```json
{
  "publish_id": "PUBLISH_ID",
  "msg_data_id": "MSG_DATA_ID"
}
```

### 2.6 查询发布状态

**接口：** `POST https://api.weixin.qq.com/cgi-bin/freepublish/get`

**请求体：**
```json
{
  "publish_id": "PUBLISH_ID"
}
```

**状态值：**
- `0`: 成功
- `1`: 发布中
- `2`: 失败

---

## 三、图片处理规范

### 3.1 封面图规范

| 项目 | 要求 |
|:-----|:-----|
| **尺寸** | 900×383 px（头条）、200×200 px（次条） |
| **格式** | JPG、PNG |
| **大小** | ≤ 2MB |
| **比例** | 2.35:1（头条）、1:1（次条） |

### 3.2 正文图规范

| 项目 | 要求 |
|:-----|:-----|
| **宽度** | 建议 900px（显示最大 677px） |
| **格式** | JPG、PNG、GIF |
| **大小** | ≤ 2MB |
| **数量** | 每 300 字配 1 张图 |

### 3.3 图片上传流程

```python
# 伪代码示例
def upload_image_to_wechat(image_path, access_token):
    """上传图片到微信"""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
    
    with open(image_path, 'rb') as f:
        files = {'media': f}
        response = requests.post(url, files=files)
    
    return response.json()['url']
```

---

## 四、Markdown 转 HTML 排版

### 4.1 推荐工具

| 工具 | 用途 | 地址 |
|:-----|:-----|:-----|
| **人言兑.md** | Markdown → 微信排版 | https://md.axiaoxin.com |
| **wechat_publisher** | OpenClaw 内置工具 | 自动排版 + 发布 |

### 4.2 排版样式要点

```html
<!-- 标题 -->
<h1 style="font-size:24px;font-weight:bold;color:#2c3e50;">标题</h1>

<!-- 小标题 -->
<h2 style="font-size:18px;font-weight:bold;color:#3498db;margin-top:24px;">小标题</h2>

<!-- 正文 -->
<p style="font-size:16px;line-height:1.8;color:#333;">正文内容</p>

<!-- 图片 -->
<p style="text-align:center;margin:16px 0;">
  <img src="图片URL" style="width:100%;max-width:677px;border-radius:8px;" />
</p>

<!-- 图片说明 -->
<p style="text-align:center;font-size:13px;color:#888;">📷 图片说明</p>

<!-- 引用 -->
<blockquote style="border-left:4px solid #3498db;padding-left:16px;color:#666;">
  引用内容
</blockquote>
```

---

## 五、完整发布流程（Python 示例）

```python
import requests
import json

class WeChatPublisher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        """获取 Access Token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        response = requests.get(url)
        return response.json()['access_token']
    
    def upload_image(self, image_path):
        """上传图片"""
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.access_token}"
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, files=files)
        return response.json()['url']
    
    def create_draft(self, title, content_html, thumb_media_id, author="", digest=""):
        """创建草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.access_token}"
        data = {
            "articles": [{
                "title": title,
                "author": author,
                "content": content_html,
                "thumb_media_id": thumb_media_id,
                "digest": digest
            }]
        }
        response = requests.post(url, json=data)
        return response.json()['media_id']
    
    def publish(self, media_id):
        """发布草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={self.access_token}"
        data = {"media_id": media_id}
        response = requests.post(url, json=data)
        return response.json()

# 使用示例
publisher = WeChatPublisher(APP_ID, APP_SECRET)

# 1. 上传封面图
thumb_url = publisher.upload_image("cover.jpg")

# 2. 创建草稿
draft_id = publisher.create_draft(
    title="文章标题",
    content_html="<p>正文内容</p>",
    thumb_media_id="THUMB_MEDIA_ID"
)

# 3. 发布
result = publisher.publish(draft_id)
print(f"发布状态: {result}")
```

---

## 六、使用 OpenClaw 内置工具发布

### 6.1 wechat_publisher 工具

OpenClaw 内置了 `wechat_publisher` 工具，可一键完成排版+发布：

```python
# 格式化 Markdown
wechat_publisher.format_markdown(
    markdown_content="# 标题\n正文内容...",
    theme_name="科技蓝"
)

# 创建草稿
wechat_publisher.create_draft(
    title="文章标题",
    content_html="<p>排版后的HTML</p>",
    thumb_media_id="封面图ID"
)

# 发布草稿
wechat_publisher.publish_draft(media_id="DRAFT_ID")

# 查询发布状态
wechat_publisher.query_publish_status(publish_id="PUBLISH_ID")
```

### 6.2 一键发布流程

```python
# 完整自动化发布
result = wechat_publisher.full_auto_publish(
    title="文章标题",
    markdown_content="Markdown正文",
    theme_name="科技蓝",
    thumb_media_id="封面图ID",
    publish_now=False  # False=仅创建草稿
)
```

---

## 七、常见问题排查

### 7.1 错误码对照

| 错误码 | 说明 | 解决方案 |
|:-------|:-----|:---------|
| `40001` | AppSecret 错误 | 检查 AppSecret 是否正确 |
| `40002` | AppID 无效 | 检查 AppID 是否正确 |
| `40014` | Access Token 无效 | 重新获取 Access Token |
| `45001` | 文件大小超限 | 压缩图片至 2MB 以下 |
| `45002` | 文章内容过长 | 控制在 20000 字以内 |
| `45007` | 图片尺寸不符 | 调整图片尺寸 |

### 7.2 发布失败常见原因

1. **封面图未上传** → 先调用 `add_material` 上传
2. **Access Token 过期** → 重新获取（有效期 2 小时）
3. **内容含敏感词** → 检查并修改敏感内容
4. **图片链接失效** → 使用 `uploadimg` 上传到微信

---

## 八、最佳实践

### 8.1 发布时机选择

| 时段 | 推荐度 | 说明 |
|:-----|:------:|:-----|
| **07:00-09:00** | ⭐⭐⭐⭐⭐ | 早间通勤高峰 |
| **12:00-13:00** | ⭐⭐⭐⭐ | 午休时段 |
| **18:00-20:00** | ⭐⭐⭐⭐⭐ | 晚间下班高峰 |
| **21:00-22:00** | ⭐⭐⭐⭐ | 睡前阅读 |

### 8.2 发布前检查清单

- [ ] 标题 ≤ 64 字
- [ ] 摘要 ≤ 120 字（不填则自动截取）
- [ ] 正文 ≤ 20000 字
- [ ] 封面图尺寸正确
- [ ] 正文图片已上传微信
- [ ] 无外链（仅 mp.weixin.qq.com）
- [ ] 已在手机预览效果

---

## 九、安全注意事项

1. **Access Token 保护**：不要硬编码在代码中，使用环境变量
2. **AppSecret 保护**：定期更换，不要提交到代码仓库
3. **IP 白名单**：在公众号后台设置服务器 IP 白名单
4. **内容审核**：发布前人工审核，避免敏感内容

---

*版本 1.0.0 | 2026-04-02 | JARVIS AI Agent*