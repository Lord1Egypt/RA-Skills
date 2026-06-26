# Zeelin API 配置指南

## 获取API Key

1. 访问 https://desearch.zeelin.cn
2. 注册/登录账号
3. 进入个人中心 -> API管理
4. 创建新的API Key

## 配置方式

### 方式1：环境变量（推荐）

```bash
export ZEELIN_API_KEY="your-api-key"
```

### 方式2：配置文件

创建 `~/.openclaw/zeelin-config.json`:

```json
{
  "api_key": "your-api-key",
  "base_url": "https://desearch.zeelin.cn/api",
  "default_mode": "deep",
  "default_interval": 30,
  "default_timeout": 3600
}
```

### 方式3：在OpenClaw中配置

```bash
openclaw config set plugins.entries.zeelin-deep-research.config.apiKey "your-api-key"
```

## 测试配置

```bash
# 测试API连接
python3 scripts/submit_research.py --query "测试" --mode basic

# 应该返回task_id
```
