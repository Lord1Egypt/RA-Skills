# 成均内容安全 Skill

通过调用成均平台的HTTP API接口，检测文本中的敏感信息、语法错误、标点符号问题等。

## 快速开始

### 1. 配置 API 凭证

**方式：直接使用Token**
https://platform.vsbclub.com/
```bash
export CHENGJUN_API_KEY="your_http_api_token"
```

### 2. 测试

```bash
python3 test_skill.py
```

或直接调用：

```bash
python3 main.py "创建特色社会主义道路，为深入学习贯彻党的二十精神"
```

## API 说明

- **生产环境 Base URL**: https://api.vsbclub.com
- **获取Token**: https://platform.vsbclub.com/
- **文本预检接口**: POST /pre-sys/precheck/text
- **认证方式**: Authorization Bearer Token
- **文本限制**: 不超过 5000 字符

## 返回格式

```json
{
  "code": 200,
  "msg": "检测成功",
  "precheck": {
    "leader": [],
    "officer": [],
    "forbidden": [],
    "grammar_word": [],
    "sensitive": [...],
    "punctuation": [],
    "wordNum": 481
  }
}
```

## 技术实现

- 使用 Python 标准库（urllib），无需额外依赖
- 支持 Token 缓存，避免频繁请求
- 兼容 OpenClaw 对话式调用

## 故障排查

如果调用失败，可能的原因：

1. **网络问题**: 检查是否能访问 https://api.vsbclub.com
2. **凭证错误**: 确认环境变量设置正确
3. **Token过期**: Token有效期约2小时，会自动重新获取
4. **文本过长**: 确保不超过5000字符
5. **服务问题**: 服务可能暂时不可用，稍后重试

## 作为 OpenClaw Skill 使用

将此目录作为 skill 安装到 OpenClaw：

```bash
openclaw skills install ./chengjun-content-security
```

## 获取 API 凭证

直接获取可用的 HTTP API Token https://platform.vsbclub.com/
