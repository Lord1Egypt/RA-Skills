# Cotrace 安装与配置

交互式引导流程。agent 应尽量自动完成每一步，只在必须用户操作时（下载客户端、浏览器登录）才请用户介入。

---

## 第一步：用户端配置（需要用户操作）

> 这一步必须由用户自己完成，agent 无法代替。

发送以下消息给用户：

```
请先按照这份文档配置好 Pieces 和 Cotrace 桌面端：

https://nxwu5gzs9f9.feishu.cn/wiki/DsVrwc2QMiVhR4kigdMct8XKntg

文档里包含：
1. 下载安装 Pieces OS
2. 配置系统采集权限
3. 下载安装 Cotrace 桌面应用
4. 完成 Cotrace 连接配置

配置过程中如果遇到问题，可以直接问我，我来帮你排查。
如果实在无法解决，请联系管理员协助。

完成后告诉我一声，我来继续后面的步骤。
```

等待用户确认完成后，继续下一步。

---

## 第二步：安装 ftc CLI（agent 自动执行）

```bash
npm install -g @autolabz/ftc-cli@latest
```

验证：
```bash
ftc -v
```

如果已安装则跳过。

---

## 第三步：添加 Cotrace 资源（agent 自动执行）

```bash
ftc resource add https://ftc-bridge.apiservice.autolab-server.site

ftc alias add cotrace https://ftc-bridge.apiservice.autolab-server.site/api/80noahia7rhpdoipbihqe
```

---

## 第四步：登录（需要用户操作）

> **关键：`ftc login` 是阻塞命令，会持续轮询直到用户在浏览器完成授权。**
> **必须在后台运行此命令，否则 agent 的命令超时会终止它，导致授权丢失。**

执行流程：

1. **在后台启动登录**（设置足够长的超时，至少 300 秒）：

```bash
ftc login &
FTC_PID=$!
```

2. **获取输出中的登录链接**，发送给用户：

```
请在浏览器中打开以下链接完成授权：

<链接>

User Code：<验证码>

⚠️ 请尽快完成，授权窗口有时间限制。完成后告诉我一声！
```

3. **等待用户确认后**，检查后台进程是否成功：

```bash
wait $FTC_PID 2>/dev/null
ftc health cotrace
```

如果 health check 失败，说明授权未成功保存，需要重新执行本步骤。

> 注意：必须在第三步（添加资源）之后再执行登录。

---

## 第五步：健康检查（agent 自动执行）

```bash
ftc health cotrace
```

- `"ok":true` → 安装成功，进入第六步
- `"ok":false` + `BRIDGE_OFFLINE` → Cotrace 桌面应用未运行，提示用户启动 Cotrace 并确认连接状态为 Connected，然后重新检查
- 其他错误 → 回到第一步确认用户端配置，或联系管理员

---

## 第六步：验证数据采集（agent 自动执行）

```bash
echo '{"tool":"get_workstream_summaries","args":{"created":{}}}' | ftc call cotrace
```

如果返回包含工作记录数据 → 配置完成。
如果返回空 → Pieces 可能需要运行一段时间积累数据，属于正常现象，告知用户即可。

---

## 自动化原则

| 步骤 | 谁执行 | 说明 |
|------|--------|------|
| 第一步：用户端配置 | 用户 | 发送文档链接，等待确认 |
| 第二步：安装 ftc | agent | 自动执行，已安装则跳过 |
| 第三步：添加资源 | agent | 自动执行 |
| 第四步：登录 | 用户 | agent 执行命令，用户完成浏览器授权 |
| 第五步：健康检查 | agent | 自动执行，失败则引导排查 |
| 第六步：验证 | agent | 自动执行 |

---

## 常见问题

| 问题 | 解决 |
|------|------|
| `ftc: command not found` | 运行 `npm install -g @autolabz/ftc-cli@latest` |
| health check 返回 BRIDGE_OFFLINE | 启动 Cotrace 桌面应用，确认连接状态为 Connected |
| 无数据返回 | Pieces OS 需要运行一段时间积累数据，正常现象 |
| 登录失败 | 确认先执行了 `ftc resource add`，再执行 `ftc login` |
| 用户端配置问题 | 参考飞书文档或联系管理员 |
