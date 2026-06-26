# AIDSO虾搜 · GEO 一体化 Skill

## 统一 API Key

四个能力共用同一个 API Key 配置：

```bash
AIDSO_GEO_API_KEY
```

读取优先级：

1. 系统环境变量 `AIDSO_GEO_API_KEY`
2. 当前 Skill 目录 `.env` 文件中的 `AIDSO_GEO_API_KEY`

绑定：

```bash
python3 bind_api_key.py --api-key "你的 API Key"
```

检查：

```bash
python3 check_api_key.py
```

