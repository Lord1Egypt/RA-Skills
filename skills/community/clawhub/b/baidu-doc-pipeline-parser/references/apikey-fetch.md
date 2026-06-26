# 百度文档解析 API Key 配置指南

## BAIDU_DOC_AI_API_KEY 和 BAIDU_DOC_AI_SECRET_KEY 未配置

当环境变量 `BAIDU_DOC_AI_API_KEY` 和 `BAIDU_DOC_AI_SECRET_KEY` 未设置时，按照以下步骤操作：

### 1. 获取 API Key 和 Secret Key

访问：**https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk**

- 登录百度云账号
- 创建应用或查看已有的 API Key 和 Secret Key
- 复制你的 **API Key** 和 **Secret Key**

### 2. 领取免费测试资源

访问：**https://ai.baidu.com/ai-doc/OCR/dk3iqnq51**

### 3. 配置环境变量

#### 方式一：直接设置环境变量

```bash
export BAIDU_DOC_AI_API_KEY="your_actual_api_key_here"
export BAIDU_DOC_AI_SECRET_KEY="your_actual_secret_key_here"
```

#### 方式二：通过配置文件

编辑配置文件：`~/.claude/settings.json` 或项目 `.claude/settings.json`

添加以下结构：

```json
{
  "skills": {
    "entries": {
      "baidu-doc-pipeline-parser": {
        "env": {
          "BAIDU_DOC_AI_API_KEY": "your_actual_api_key_here",
          "BAIDU_DOC_AI_SECRET_KEY": "your_actual_secret_key_here"
        }
      }
    }
  }
}
```

将 `your_actual_api_key_here` 替换为你的实际 API Key，`your_actual_secret_key_here` 替换为你的实际 Secret Key。

### 4. 验证配置

```bash
# 验证 access_token 是否可正常获取
curl -X POST 'https://aip.baidubce.com/oauth/2.0/token' \
  -d 'grant_type=client_credentials' \
  -d 'client_id={your_api_key}' \
  -d 'client_secret={your_secret_key}'
```

成功返回示例：

```json
{
  "access_token": "24.xxxxx.xxxxxx.xxxxxxx-xxxxxxx",
  "expires_in": 2592000
}
```

`expires_in` 为 2592000 秒（30 天），到期后需重新获取。

### 5. 测试

```bash
python3 scripts/baidu_doc_parser.py --file_url "https://example.com/test.pdf" --file_name "test.pdf"
python3 scripts/baidu_doc_parser.py --file_data "<文件的base64编码>" --file_name "test.pdf"
```

## 常见问题

- 确保环境变量已正确设置（可通过 `echo $BAIDU_DOC_AI_API_KEY` 验证）
- 确认 API Key 有效且已开通百度智能文档分析平台服务
- 检查百度云账户余额或免费额度
- access_token 有效期 30 天，过期后会自动重新获取

## 相关链接

- [获取 AK/SK 文档](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk)
- [领取免费资源](https://ai.baidu.com/ai-doc/OCR/dk3iqnq51)
- [百度云控制台](https://console.bce.baidu.com/ai/)
