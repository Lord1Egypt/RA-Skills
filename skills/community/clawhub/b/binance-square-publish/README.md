# Binance Square Post

一个让用户可以自定义配置 API Key 并发送内容到 Binance Square 的 Skill。

## 快速开始

### 1. 配置 API Key

编辑 `SKILL.md` 文件，在 `config` 部分添加你的 API Key：

```yaml
config:
  accounts:
    - name: default
      api_key: 你的Binance_Square_OpenAPI_Key
```

### 2. 使用

告诉闪电你想发的内容，例如：
- "发一条帖子，内容是Hello World"
- "发一条BTC行情分析"

## 获取 API Key

1. 登录 Binance 账户
2. 访问 https://www.binance.com/zh-CN/square/openapi
3. 创建 OpenAPI Key

## 示例

```bash
# 测试发帖
curl -X POST 'https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add' \
  -H 'X-Square-OpenAPI-Key: 你的API密钥' \
  -H 'Content-Type: application/json' \
  -H 'clienttype: binanceSkill' \
  -d '{"bodyTextOnly": "Hello Binance Square! $BTC #Crypto"}'
```
