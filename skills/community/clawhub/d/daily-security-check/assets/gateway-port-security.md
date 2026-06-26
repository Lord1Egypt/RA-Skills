# OpenClaw 网关改端口 — 安全说明与操作指南

社区与安全实践中常提到：**为安全起见，建议把 OpenClaw 自己配置的默认端口改掉**。本文说明来源、原因和具体改法。

用户可在 `openclaw.json` 中设置自定义端口（示例：`41631`），并确保浏览器扩展、Control UI 等处的 URL 与之一致。

---

## 一、来源与依据

- **官方文档**  
  - [Gateway 配置](https://docs.openclaw.ai/zh-CN/gateway/configuration)：`gateway.port` 默认 **18789**，可通过配置/环境变量/CLI 覆盖。  
  - [安全性](https://docs.openclaw.ai/zh-CN/gateway/security)：强调绑定 loopback、防火墙、不暴露 `0.0.0.0`；未强制要求改端口，但端口与「网络暴露」同属一类配置。

- **社区/实践**  
  - 与「防火墙仅放行必要端口」一致：若你只放行「自己定的端口」，而不是默认 18789，可减少对默认端口的依赖。  
  - 通用安全习惯：默认端口易被扫描脚本、自动化工具和文档示例针对；改用非默认端口是常见的**纵深加固**手段（在绑定 + 认证 + 防火墙之外多一层）。

- **本 skill 的扩展清单**  
  - `community-official-security-extras.md` 已将「自定义端口」列为网络与部署下的推荐项。

---

## 二、为什么建议改端口？

1. **降低“默认端口”暴露面**  
   一旦将来有人误把网关暴露到局域网或做了端口转发，使用非默认端口会比 18789 更不容易被全网扫描脚本直接命中。

2. **与防火墙策略一致**  
   「仅放行必要端口」时，若你只放行自己选定的端口（例如 41631），就不会依赖 18789 这个众所周知的默认值。

3. **不替代、只补充**  
   改端口**不能**替代：  
   - `gateway.bind: "loopback"`  
   - 强认证（token/密码）  
   - 系统防火墙  
   它是在这些基础上的额外可选加固。

---

## 三、如何修改端口

### 1. 配置文件（推荐）

在 **`openclaw.json`**（项目根或 `~/.openclaw/openclaw.json`）的 `gateway` 中：

```json5
{
  "gateway": {
    "port": 41631,   // 示例端口，请改成你选定的端口
    "mode": "local",
    "bind": "loopback",
    "remote": {
      "url": "ws://127.0.0.1:41631"   // 必须与上面 port 一致
    }
    // ... 其余 gateway 配置不变
  }
}
```

**注意**：`gateway.remote.url` 里的端口必须与 `gateway.port` 一致，否则本地/远程 CLI 连接会失败。

### 2. 环境变量

- **`OPENCLAW_GATEWAY_PORT`**  
  可覆盖配置里的 `gateway.port`（例如设为 `28789`）。  
  若用环境变量，则 `gateway.remote.url` 中的端口也需与之一致（或同样用环境变量构造 URL，若你的部署支持）。

### 3. 命令行

- 启动时临时指定：  
  `openclaw gateway start --port 41631`  
  与配置文件/环境变量同时存在时，**`--port` 优先级最高**（官方说明：`--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > 默认 18789）。

---

## 四、改端口后必须同步修改的地方

| 位置 | 说明 |
|------|------|
| **`gateway.port`** | 改为新端口（如 41631）。 |
| **`gateway.remote.url`** | 例如 `ws://127.0.0.1:41631`，端口与 `gateway.port` 一致。 |
| **浏览器扩展 / Control UI** | 若扩展或书签里写死了 `http://127.0.0.1:18789`，需改成新端口（如 `http://127.0.0.1:41631`）。 |
| **Tailscale / 反向代理** | 若通过 Tailscale Serve 或 nginx/Caddy 等转发到网关，后端端口需改为新端口。 |
| **脚本 / cron / 文档** | 任何写死 18789 的脚本或文档中的 URL/端口都要更新。 |

改完后执行一次 `openclaw gateway restart`（或先 stop 再 start），并确认 Control UI 和 CLI 都能正常连上。

---

## 五、端口号选择建议

- 建议使用 **1024–65535** 之间、不常见的高位端口（例如 41631、53417），避免与常见服务（22、80、443、3000 等）冲突。  
- 若多实例同机，每个实例需使用**不同**的 `gateway.port`（及对应 `gateway.remote.url`）。

---

## 六、与每日安全巡检的关系

- 每日安全巡检会检查 `gateway.bind`、防火墙、认证等，**不会**自动检查端口是否为非默认值。  
- 若你采纳「自定义端口」建议，可在巡检报告或备注中自行注明「已改用非默认端口」便于日后审计。  
- 本说明为 skill 内参考文档，安装后位于 skill 目录下的 `assets/gateway-port-security.md`。
