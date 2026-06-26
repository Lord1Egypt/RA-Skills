# 成均内容安全 Skill

name: 成均内容安全 description: 通过调用成均平台的HTTP API接口，检测文本中的敏感信息、语法错误、标点符号问题等，保障内容合规。

## 简介

这是一个用于检测文本敏感信息的 Skill，通过调用成均智能平台（[博达智能体开放平台](https://platform.vsbclub.com/)）的内容安全接口，快速识别文本内容中的敏感数据、语法错误等问题，适用于内容审核、数据合规等场景。

本技能支持检测以下内容：
- 敏感词汇
- 领导人称谓
- 官员称谓
- 禁用词汇
- 语法错误
- 标点符号问题

> ⚠️ **重要配置说明**
>
> **API 认证配置**：
>
> **方式：直接使用Token**
> ```bash
> export CHENGJUN_API_KEY="your_http_api_token"
> ```
>
>
> **服务信息**：
>
> -   生产环境 Base URL: https://api.vsbclub.com/
> -   获取Token: https://platform.vsbclub.com/

## 功能特性

-   支持多种内容安全检查（敏感词、领导人称谓、官员称谓、禁用词、语法词、标点符号）
-   支持直接Token和自动获取Token两种认证方式
-   Token自动缓存管理，避免频繁请求
-   标准化的 JSON 格式输入输出
-   完善的错误处理和超时机制
-   兼容 OpenClaw 对话式调用
-   文本长度限制：5000 字符
-   使用 Python 标准库，无需额外依赖

## 安全说明

### API 认证

-   支持直接传入 Token 
-   Token 通过 Authorization 请求头传递

### 数据安全

-   预检结果不会被服务端保存
-   单次请求文本长度不超过 5000 字符
-   使用 HTTPS 协议传输数据

## 技术实现

### 使用的技术栈

技术

用途

Python 3.8+

主要开发语言

urllib (标准库)

HTTP 请求库

### 依赖安装

本 skill 使用 Python 标准库，无需安装额外依赖。

## 使用方法

### 对话式调用

```
请帮我检测这段文本是否包含敏感信息：{待检测文本内容}
```

### API 认证配置

**方式：直接使用Token**

```bash
export CHENGJUN_API_KEY="your_http_api_token"
```

### 参数说明

参数名

类型

必传

说明

text

string

是

待检测的文本内容（不超过5000字符）

api_key

string

否

API密钥（可选，默认从环境变量读取）

### 返回格式

```json
{
  "code": 200,
  "msg": "检测成功",
  "precheck": {
    "leader": [],
    "officer": [],
    "forbidden": [],
    "grammar_word": [],
    "sensitive": [
      {
        "word": "党的二十",
        "correct": ["党的二十大"],
        "misdescription": null,
        "category": "中国共产党相关表述",
        "sentence": "为深入学习贯彻党的二十精神",
        "explain": null,
        "startInSentence": 9,
        "riskLevel": "middle",
        "level": "疑似错误",
        "start": 9,
        "end": 13,
        "priority": 2,
        "typeNum": 1
      }
    ],
    "punctuation": [],
    "urlBody": null,
    "wordNum": 481
  }
}
```

### 检查项说明

检查项

说明

leader

领导人称谓检查结果

officer

官员称谓检查结果

forbidden

禁用词检查结果

grammar_word

语法词检查结果

sensitive

敏感词检查结果

punctuation

标点符号检查结果

### 错误码说明

#### 通用错误码

错误码

说明

200

检测成功

-1

业务逻辑错误（文本为空或超长）

#### API 调用错误

错误码

说明

401

认证失败（Token无效或凭证错误）

403

权限不足

429

请求频率超限

500

服务器内部错误

-2

API 调用失败（网络或服务问题）

## 示例代码

```python
from main import check_content, run

# 方式1：使用环境变量中的Token
# export CHENGJUN_API_KEY="your_http_api_token"
result = check_content(
    text="创建特色社会主义道路，为深入学习贯彻党的二十精神"
)

# 方式2：直接传入Token
result = check_content(
    text="创建特色社会主义道路，为深入学习贯彻党的二十精神",
    api_key="your_http_api_token"
)

# 使用run函数（兼容OpenClaw）
result = run({
    "text": "创建特色社会主义道路，为深入学习贯彻党的二十精神"
})

# 打印结果
print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 注意事项

1.  使用前需要配置API认证（Token）
2.  单次请求文本长度不超过 5000 字符
3.  预检结果不会被服务端保存
4.  接口调用超时时间为 30 秒
5.  Token自动缓存，有效期内的请求不会重复获取

## API 接口文档

详细文档请参考：https://platform.vsbclub.com/docs/zh/webber/content_check.html


### 文本预检接口

- **请求地址**：POST https://api.vsbclub.com/pre-sys/precheck/text
- **请求头**：Authorization: {token}
- **请求参数**：text（待检测文本）
- **返回**：precheck（检测结果）

## 故障排查

如果调用失败，检查：

1. **网络连接**：`curl -I https://api.vsbclub.com/`
2. **Token配置**：确认 CHENGJUN_API_KEY 设置正确
3. **文本长度**：确保不超过5000字符
4. **服务状态**：服务可能暂时不可用，稍后重试

## 获取 API Token

直接获取可用的 HTTP API Token https://platform.vsbclub.com/
