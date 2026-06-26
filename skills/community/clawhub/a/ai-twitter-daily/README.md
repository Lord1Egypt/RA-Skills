# AI Twitter Daily Report

每日追踪 AI 领域顶级研究者和公司的 Twitter 动态。

## 配置

在使用前需要设置 Grok API 密钥：

```bash
export GROK_API_KEY="your-api-key-here"
```

可选配置：
```bash
export GROK_API_URL="https://api.cheaprouter.club/v1/chat/completions"
export GROK_MODEL="grok-4.20-beta"
```

## 使用

```bash
python3 scripts/daily_report.py
```

## 追踪的账号

包括 22+ 顶级 AI 研究者和组织，详见 `references/users.txt`。
