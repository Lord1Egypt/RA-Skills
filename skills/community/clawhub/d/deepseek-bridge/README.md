# DeepSeek Bridge · DeepSeek API 桥接

## 快速使用

```bash
# 启动桥接
python D:\ollama-intel\deepseek_bridge.py

# 健康检查
curl http://127.0.0.1:8080/health

# 调用
curl -X POST http://127.0.0.1:8080/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "你好"}'
```

## 文件

- `SKILL.md` — 完整说明文档
- （核心代码位于 `D:\ollama-intel\deepseek_bridge.py` 和 `D:\openclaw-data\db_shared.py`）

## 依赖

- Python 3
- Flask
- requests

```bash
pip install flask requests
```

## 端口

- 桥接服务：`127.0.0.1:8080`
- 状态数据库：`D:\openclaw-data\chat_shared.db`