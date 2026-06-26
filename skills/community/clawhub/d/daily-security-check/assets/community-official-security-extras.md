# 社区与官方：额外必做 / 推荐安全配置

在 [source-article-security-config.md](source-article-security-config.md)（Bruce Van 7 步）基础上，社区与官方文档常提到的**额外**必做或强烈推荐项。可作为每日巡检的扩展检查项或一次性加固清单。

**官方文档**：<https://docs.openclaw.ai/zh-CN/gateway/security/index>

---

## 一、官方 CLI 与审计

- **定期运行**（配置变更后或定期执行）：
  ```bash
  openclaw security audit
  openclaw security audit --deep
  openclaw security audit --fix
  ```
- `--fix` 会：收紧 `~/.openclaw` 权限（700/600）、恢复 `logging.redactSensitive`、将 `groupPolicy="open"` 收紧为 `allowlist` 等。
- **审计优先级**（按官方建议顺序处理）：模型选择 → 插件/扩展 → 权限 → 浏览器控制暴露 → 公共网络暴露 → 「开放 + 工具」组合（先锁私信/群组，再收紧工具/沙箱）。

---

## 二、身份与访问控制

- **DM 配对**：`dmPolicy: "pairing"`（推荐），或 `allowlist`；避免长期使用 `open`。
- **Token**：至少 32 字符随机 token；部分建议 256 位；每 30 天轮换。
- **群组策略**：生产环境避免 `groupPolicy: "open"`；用 `allowlist` + 提及门控。
- **控制 UI**：生产环境禁用或仅限 localhost/HTTPS；勿启用 `allowInsecureAuth` 或 `dangerouslyDisableDeviceAuth`（仅紧急调试用）。

---

## 三、工具与沙箱（Tool Policy / Sandbox）

- **工具策略**：**默认拒绝、显式放行**（allowlist，不用 blocklist 思维）。
- **exec**：生产环境用 `allowlist` 或 `deny`；禁止 `full`。示例 allowlist：`git *`, `npm run *`, `bash skills/*` 等。
- **高风险工具**：浏览器自动化限制到可信域名；文件写入限制到指定目录（如 `~/openclaw/tmp/`）。
- **沙箱**：`sandbox.mode: "non-main"` 或容器化；非 root 运行。

---

## 四、网络与部署

- **绑定**：仅 `127.0.0.1` / loopback，禁止 `0.0.0.0` 暴露（除非在反向代理后且认证完备）。
- **mDNS**：生产环境禁用。
- **反向代理**：若用 nginx/Caddy/Traefik，配置 `gateway.trustedProxies`，避免认证绕过；使用 TLS。
- **防火墙**：系统防火墙开启，仅放行必要端口。
- **自定义端口（社区推荐）**：OpenClaw 默认网关端口为 **18789**。为降低被扫描/误暴露时的风险，建议改为自定义端口（见下方「改端口说明」）。

---

## 五、敏感数据与凭证

- **配置项**：`security.sensitiveData.patterns`（如 `["sk-*"]`）过滤敏感输出。
- **凭证**：API Key / token 用环境变量或密钥管理器；不硬编码。
- **文件权限**：配置与凭证目录 `chmod 600`（文件）、`700`（目录）；`openclaw security audit --fix` 会协助收紧。

---

## 六、已知漏洞与版本

- **CVE-2026-25253**：v2026.1.24 及以前存在参数注入 RCE；升级至 v2026.1.29+。
- **ClawJacked**：恶意网站可经浏览器暴力破解本地网关密码；**v2026.2.26** 已修复，建议升级至 2026.2.26+。
- **技能安装**：禁止未信任源的自动安装；要求人工确认。

---

## 七、日志与运维

- **审计日志**：启用并保留 90–365 天（建议 365）。
- **插件**：仅启用信任的插件；减少攻击面。
- **会话日志**：`~/.openclaw/agents/*/sessions/*.jsonl` 在磁盘上，需通过 `~/.openclaw` 权限与访问控制保护。

---

## 八、官方安全原则摘要

- **访问控制优先于智能**：假设模型可被操纵，通过身份与范围限制影响。
- **身份优先**：谁可以和机器人对话（配对/白名单）。
- **范围其次**：机器人在哪里能执行操作（群组、工具、沙箱、设备权限）。
- **从最小权限开始**，再随信心逐步放宽。

---

以上项可与每日巡检 5 项合并使用：前 5 项为每日必查，本清单可作为季度/变更后加固或巡检扩展参考。
