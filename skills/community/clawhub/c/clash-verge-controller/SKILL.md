---
name: clash-verge-controller
description: |
  Clash Verge 外部控制（RESTful API）技能。基于 mihomo 内核，提供完整的 API 调用指南、配置说明和代码示例。
  当用户提到以下场景时触发：
  - Clash Verge 外部控制、RESTful API、远程管理
  - 通过 API 切换节点、查看连接、管理规则
  - clash-verge、clash.meta、mihomo 控制器配置
  - 获取代理信息、测试延迟、重启内核等操作
---

# Clash Verge 外部控制

##必要信息
开始前需要获取用户的clash verge外部监听地址和密钥，并确认clash verge外部监听已打开。


## 核心原理

Clash Verge 内置 **mihomo (Clash.Meta)** 内核，通过 RESTful API 实现外部控制，支持切换节点、管理规则、监控连接等操作。

## 配置文件设置

在 Clash 配置文件中添加：

```yaml
# 外部控制 (API) 配置
external-controller: 127.0.0.1:9090

# API 访问密钥（强烈建议设置）
secret: "your-secret-key-here"

# CORS 跨域配置
external-controller-cors:
  allow-origins:
    - '*'
  allow-private-network: true
```

**配置说明：**

| 配置项 | 说明 |
|--------|------|
| `external-controller` | API 监听地址，`127.0.0.1` 仅本地，`0.0.0.0` 允许外部访问 |
| `secret` | API 密钥，开启后请求需携带 `Authorization: Bearer ${secret}` |

## 常用 API 接口

**基础调用格式：**
```bash
# 无密钥
curl http://127.0.0.1:9090/{endpoint}

# 有密钥
curl -H "Authorization: Bearer ${secret}" http://127.0.0.1:9090/{endpoint}
```

### 代理操作

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取代理列表 | GET | `/proxies` | 查看所有代理和策略组 |
| 切换节点 | PUT | `/proxies/{name}` | `{"name": "香港节点"}` |
| 测试延迟 | GET | `/proxies/{name}/delay?url=https://www.google.com&timeout=5000` | 返回延迟(ms) |

### 策略组操作

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取策略组 | GET | `/group` | 列出所有策略组 |
| 获取指定组 | GET | `/group/{name}` | 查看特定策略组详情 |
| 清除自动选择 | DELETE | `/group/{name}` | 清除 auto 组 fixed 选择 |

### 配置操作

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取配置 | GET | `/configs` | 查看当前配置 |
| 更新配置 | PATCH | `/configs` | `{"mixed-port": 7890}` |
| 重启内核 | POST | `/restart` | 重载配置 |
| 更新 GEO | POST | `/configs/geo` | `{"path": "", "payload": ""}` |

### 监控操作

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 实时日志 | WS | `/logs?level=info` | WebSocket 获取日志 |
| 流量信息 | WS | `/traffic` | 实时流量(kbps) |
| 连接列表 | GET | `/connections` | 查看所有连接 |
| 关闭连接 | DELETE | `/connections` | 关闭所有连接 |
| DNS 查询 | GET | `/dns/query?name=example.com&type=A` | 查询 DNS 记录 |

## 完整 API 参考

详细 API 文档（包含所有端点、参数、返回值）见：
[references/api_reference.md](references/api_reference.md)

## 代码示例

### Python

```python
import requests

API = "http://127.0.0.1:9090"
SECRET = "your-secret-key"
headers = {"Authorization": f"Bearer {SECRET}"}

# 获取代理列表
proxies = requests.get(f"{API}/proxies", headers=headers).json()

# 切换节点
requests.put(
    f"{API}/proxies/Proxy",
    headers=headers,
    json={"name": "香港节点-01"}
)

# 测试延迟
result = requests.get(
    f"{API}/proxies/香港节点/delay",
    params={"url": "https://www.google.com", "timeout": 5000}
).json()
print(f"延迟: {result.get('delay')}ms")
```

### Node.js

```javascript
const axios = require('axios');

const API = 'http://127.0.0.1:9090';
const SECRET = 'your-secret-key';
const headers = { Authorization: `Bearer ${SECRET}` };

// 获取代理列表
const { data } = await axios.get(`${API}/proxies`, { headers });

// 切换节点
await axios.put(
  `${API}/proxies/Proxy`,
  { name: '香港节点-01' },
  { headers }
);
```

## 安全建议

1. **使用密钥**：生产环境务必设置 `secret`
2. **限制监听**：仅本地用 `127.0.0.1`，需要远程访问再改 `0.0.0.0`
3. **配合防火墙**：开启外部访问时限制 IP
4. **使用 HTTPS**：敏感网络配置 TLS

## 官方文档

- Clash Verge Rev: https://github.com/clash-verge-rev/clash-verge-rev
- mihomo API 文档: https://wiki.metacubex.one/api/
