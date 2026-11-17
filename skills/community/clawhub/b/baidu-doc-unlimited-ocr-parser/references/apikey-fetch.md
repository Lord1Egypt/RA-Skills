# 百度文档解析（Unlimited-OCR）API Key 配置指南

## BAIDU_DOC_AI_API_KEY 和 BAIDU_DOC_AI_SECRET_KEY 未配置

当环境变量未设置时，按照以下步骤操作：

### 1. 获取 API Key 和 Secret Key

访问：**https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk**

- 登录百度云账号
- 创建应用或查看已有的 API Key 和 Secret Key
- 复制你的 **API Key** 和 **Secret Key**

### 2. 领取免费测试资源

Unlimited-OCR **接口限时免费**，登录[文字识别控制台](https://console.bce.baidu.com/ai/)自动领取：

- 个人实名认证用户：200 页
- 企业实名认证用户：1000 页

### 3. 配置环境变量

```bash
export BAIDU_DOC_AI_API_KEY="your_actual_api_key_here"
export BAIDU_DOC_AI_SECRET_KEY="your_actual_secret_key_here"
```

或通过配置文件 `~/.claude/settings.json`：

```json
{
  "skills": {
    "entries": {
      "baidu-doc-Unlimited-OCR-parser": {
        "env": {
          "BAIDU_DOC_AI_API_KEY": "your_actual_api_key_here",
          "BAIDU_DOC_AI_SECRET_KEY": "your_actual_secret_key_here"
        }
      }
    }
  }
}
```

### 4. 验证配置

```bash
curl -X POST 'https://aip.baidubce.com/oauth/2.0/token' \
  -d 'grant_type=client_credentials' \
  -d 'client_id={your_api_key}' \
  -d 'client_secret={your_secret_key}'
```

### 5. 测试

```bash
python3 scripts/baidu_doc_unlimited_ocr_parser.py --file_url "https://example.com/test.pdf" --file_name "test.pdf"
```

## 相关链接

- [获取 AK/SK 文档](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk)
- [官方技术文档](https://cloud.baidu.com/doc/OCR/s/fmr1p39gb)
- [百度云控制台](https://console.bce.baidu.com/ai/)
