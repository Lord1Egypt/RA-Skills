---
slug: deepseek-bridge
displayName: DeepSeek Bridge · DeepSeek API 桥接
version: 1.0.0
summary: 轻量级 HTTP 桥接程序，将 DeepSeek Chat API 封装为本地 /ask 接口，支持状态持久化
license: MIT
---

# DeepSeek Bridge · DeepSeek API 桥接

> 将 DeepSeek Chat API 封装为本地 HTTP 接口，供本地 Agent 调用。

---

## 架构

```
Agent → POST /ask → deepseek_bridge.py → DeepSeek API → SQLite 持久化
                              ↓
                         端口 8080
```

**两个核心文件：**
- `deepseek_bridge.py` — Flask 桥接服务（端口 8080）
- `db_shared.py` — SQLite 共享数据库（chat_shared.db）

---

## 接口

### `GET /health`

健康检查：

```bash
curl http://127.0.0.1:8080/health
# {"status":"ok","model":"deepseek-chat"}
```

### `POST /ask`

提交问题，返回 DeepSeek 回答：

```bash
curl -X POST http://127.0.0.1:8080/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "你好，DeepSeek"}'
# {"answer": "你好！有什么可以帮你的？"}
```

**请求体：**
```json
{
  "question": "你的问题"
}
```

**响应：**
```json
{
  "answer": "DeepSeek 的回答"
}
```

**错误响应：**
```json
{"error": "错误信息"}
```

---

## 状态持久化

每次 `/ask` 调用会在 `chat_shared.db`（SQLite）中记录：

| 字段 | 说明 |
|:---|:---|
| id | 记录 ID |
| question | 用户问题 |
| answer | DeepSeek 回答 |
| status | pending / completed / error |
| created_at | 创建时间 |

---

## 启动与管理

### 启动桥接

```powershell
# 方式一：直接运行
python D:\ollama-intel\deepseek_bridge.py

# 方式二：后台运行（Windows）
Start-Process python -ArgumentList "D:\ollama-intel\deepseek_bridge.py" -WindowStyle Hidden
```

### 检查状态

```powershell
# 检查端口是否在监听
netstat -ano | findstr ":8080 "

# 健康检查
curl http://127.0.0.1:8080/health
```

### 关闭桥接

```powershell
# 查找进程
netstat -ano | findstr ":8080 "

# 强制关闭（替换 PID）
taskkill /PID 18052 /F
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|:---|:---|:---|
| `DEEPSEEK_API_KEY` | （必填，无默认值） | DeepSeek API Key，从 platform.deepseek.com 申请 |

---

## Node.js 调用示例

```javascript
async function askDeepSeek(question) {
  const resp = await fetch('http://127.0.0.1:8080/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  const data = await resp.json();
  if (data.error) throw new Error(data.error);
  return data.answer;
}

// 使用
const answer = await askDeepSeek('用一句话解释量子计算');
console.log(answer);
```

---

## 路由触发词

当用户说以下内容时激活本技能：

- "问 DeepSeek"、"问下 DeepSeek"
- "帮我问 DeepSeek"、"问一下这个"
- "DeepSeek 怎么说"、"DeepSeek怎么看"
- "用 DeepSeek 查一下"

---

## 注意事项

1. **先检查后调用**：使用前先 `GET /health` 确认桥接已启动
2. **未启动则自动启动**：健康检查失败时，调用方应自动拉起桥接进程
3. **API Key**：默认使用内置 Key，也可通过环境变量覆盖
4. **超时**：API 超时 60 秒，超时返回 504
5. **依赖**：Flask + requests（`pip install flask requests`）

---

*Created by Worker-A · 2026-06-27*