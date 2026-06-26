# 百度文档解析（PaddleOCR-VL）API Key 配置指南

## BAIDU_DOC_AI_API_KEY 和 BAIDU_DOC_AI_SECRET_KEY 未配置

当环境变量未设置时，按照以下步骤操作：

### 1. 获取 API Key 和 Secret Key

访问：**https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk**

- 登录百度云账号
- 创建应用或查看已有的 API Key 和 Secret Key
- 复制你的 **API Key** 和 **Secret Key**

### 2. 领取免费测试资源

访问：**https://ai.baidu.com/ai-doc/OCR/dk3iqnq51**

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
      "baidu-doc-vlm-parser": {
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
python3 scripts/baidu_doc_vlm_parser.py --file_url "https://example.com/test.pdf" --file_name "test.pdf"
```

## 相关链接

- [获取 AK/SK 文档](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu#1-获取aksk)
- [领取免费资源](https://ai.baidu.com/ai-doc/OCR/dk3iqnq51)
- [百度云控制台](https://console.bce.baidu.com/ai/)
