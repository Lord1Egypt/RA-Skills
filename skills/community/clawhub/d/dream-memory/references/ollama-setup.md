# Ollama + OpenViking 详细配置

## Ollama 安装

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# 下载 bge-m3 模型
ollama pull bge-m3

# 启动服务
ollama serve &
```

## OpenViking 配置

文件：`~/.openviking/ov.conf`

```json
{
  "server": { "host": "127.0.0.1", "port": 1933, "cors_origins": ["*"] },
  "storage": {
    "workspace": "~/.openviking/data",
    "vectordb": { "name": "context", "backend": "local", "project": "default" },
    "agfs": { "port": 1833, "log_level": "warn", "backend": "local" }
  },
  "log": { "level": "WARNING", "rotation": true, "rotation_days": 3 },
  "embedding": {
    "dense": {
      "provider": "openai",
      "model": "bge-m3",
      "api_key": "dummy",
      "api_base": "http://localhost:11434/v1",
      "dimension": 1024
    }
  }
}
```

## OpenClaw 配置

```json
{
  "plugins": {
    "allow": ["openviking"],
    "slots": { "contextEngine": "openviking" },
    "entries": {
      "openviking": {
        "enabled": true,
        "config": { "mode": "local", "configPath": "~/.openviking/ov.conf", "port": 1933 }
      }
    }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "sources": ["memory", "sessions"],
        "experimental": { "sessionMemory": true },
        "provider": "openai",
        "remote": { "baseUrl": "http://localhost:11434/v1" },
        "model": "bge-m3",
        "chunking": { "tokens": 250, "overlap": 60 },
        "query": {
          "maxResults": 10,
          "minScore": 0.15,
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.75,
            "textWeight": 0.25,
            "candidateMultiplier": 8,
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": true, "halfLifeDays": 90 }
          }
        }
      }
    }
  }
}
```

## 关键参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `dimension` | 1024 | bge-m3 输出维度（不能 2048） |
| `chunking.tokens` | 250 | 分块大小 |
| `chunking.overlap` | 60 | 块间重叠 |
| `minScore` | 0.15 | 最低匹配分 |
| `hybrid.vectorWeight` | 0.75 | 向量权重 |
| `hybrid.textWeight` | 0.25 | 文本权重 |
| `hybrid.mmr.lambda` | 0.7 | MMR 去重 |
| `hybrid.temporalDecay.halfLifeDays` | 90 | 时间衰减半衰期 |

## 更新向量索引

```bash
curl -X POST http://127.0.0.1:1933/api/v1/resources
curl -X POST http://127.0.0.1:1933/api/v1/system/wait
```

## 已知问题与解决

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| vectordb LOCK 残留 | 进程异常退出 | 杀进程 → 删 LOCK → restart |
| Embedding 维度不匹配 | 默认 2048 | 配置 `"dimension": 1024` |
| OpenViking 无响应 | 进程未启动 | `openclaw gateway restart` |
