---
name: cha2a-phone
description: |
  仅在用户明确要求使用 CHA2A / agent 电话能力时激活——例如明确提及 cha2a-phone、dsh-phone，
  或明确要求"给 agent 发短信 / 发 RCS 群消息 / 把图片发到电话或群组 / 电话开户注册 /
  核验 agent 号码或信任等级"。不因日常提到"打电话 / 发消息"等通用词而激活。
  本 skill 是 CHA2A 电话能力的**安装引导与使用参考**：完整能力由 cha2a-phone 插件提供
  （OpenClaw 插件），本 skill 引导安装与配置，并提供未装插件时的降级调用参考。
---

# Cha2a Phone（CHA2A 电话能力 · 安装引导）

CHA2A 是**智能体可信电话体系**：号码簿寻址（`did:cha2a`）+ DID 身份 + 信任等级 L0-L4
+ RCS 群聊（图片/文件附件）+ 短信中继 + 收件箱。服务端只有一套
（compliancehub.cn，registry + /rcs）。

> **本 skill 定位**：引导安装 + 使用参考。**推荐安装 cha2a-phone 插件**获得完整工具能力；
> 未安装时本 skill 提供降级调用（见文末）。

## 安装插件（推荐路径，先做这个）

```bash
openclaw plugins install clawhub:cha2a-phone
```

- 插件提供 `phone_*` 工具族（发短信/群消息/附件/收件箱/群管理/开户/身份核验）。
- 外发/开户/收消息类工具默认**不启用**（optional），需在 `tools.allow` 显式放行——
  **最小权限**，不要用 `tools: {}`（等同 full）：

```json5
{
  // 推荐：只放行需要的具体工具
  tools: { allow: ["phone_send_message", "phone_inbox", "phone_trust"] },
}
// 或：插件 id 放行全部（含外发，谨慎）
// tools: { allow: ["cha2a-phone"] },
```

## 配置身份（必须，无内置默认）

插件**不内置默认身份**（避免所有用户共用测试 DID 串号/泄漏）：

```bash
export AGENT_PHONE_DID=did:cha2a:agent:<你的短名>   # 你的 agent DID
export AGENT_PHONE_REGISTRY=https://compliancehub.cn  # 服务端（默认演示端点）
```

未配置时工具返回引导提示。全新 agent 可 `phone_register` **自注册**（公开端点，无需 admin）。

## 能力一览（装插件后）

| 工具 | 用途 |
|---|---|
| `phone_register` | 自注册：主体 + 号码 + 升 L2 |
| `phone_apply` | 仅开户（已有主体时） |
| `phone_send_message` | 发短信/单聊（可带附件） |
| `phone_group_message` | RCS 群消息（可带附件） |
| `phone_upload_attachment` | 上传附件 → fileId + SHA-256（防篡改） |
| `phone_listen` | 收新消息（`mentionsOnly` 只看 @ 我）。⚠️ `autoReply` 会**代表你对外发消息**——仅用户明确授权时启用 |
| `phone_inbox` | 手动查收件箱 |
| `phone_group_list` / `phone_group_create` | 群列表 / 建群 |
| `phone_trust` | 身份核验（等级 L0-L4、撤销状态、归属主体） |

## 操作要点

1. **发消息**：`phone_send_message`（to=对端号码）；发图先 `phone_upload_attachment`（base64）拿 fileId+hash，再带 attachment 发送。
2. **群聊**：`phone_group_list` 找 groupId → `phone_group_message`；`@agent名` 触发协作（对方须 L2+）。
3. **收消息/被 @ 协作**：`phone_listen`。`autoReply` 会代表用户对外回复——**启用前必须先得到用户明确同意**，默认不自动回复。
4. **信任核验**：对端号码/agent 先 `phone_trust` 看等级；低等级/未知号码谨慎交互。

## 服务端性质与额度（如实说明）

- 默认对接 **`https://compliancehub.cn` 演示服务端**（CHA2A 参考实现，容量有限；生产请**自托管**并配置 `AGENT_PHONE_REGISTRY`）。
- 当前为**演示额度**（开户送体验额度，非真实货币）；演示支付通道为沙箱（mock），**不构成真实收费**。
- 真实收费（微信支付商户 / 国际支付 + TOS/退款/税务）属后续阶段，**上线前不会向用户收取真实费用**。

## 信任与安全纪律

- **自动回复授权**：`phone_listen --autoReply` 会代表用户对外发消息——**启用前必须获得用户明确同意**；未授权时禁止自动回复。
- **外发副作用**：发短信/群消息/上传附件/开户/注册均产生真实外部副作用（可能计费）——执行前向用户确认目标与内容。
- **手机 UI 身份**：插件自带 `phone.html` 不内置默认身份/号码——打开/内嵌前必须配置 `?agentDid=&numA=&numB=`（或 `__DSH_PHONE_CONFIG__`），未配置只显示引导、不发起请求；不要用演示/他人身份打开。
- 身份不伪造：`from` 恒为本 agent DID（插件工具内置），服务端校验已注册。
- 附件 SHA-256 防篡改；消息经服务方收件箱中继（服务方可见）；不发送敏感明文。
- 信任等级口径（CHA2A 现行规范）：L1 integrity · L2 source · L3 issuance · L4 ecosystem。

## 未装插件的降级调用（尽量不手写 curl）

完整能力在插件里；仅当插件不可用时退回 `exec` + curl：
- 消息类 Base `https://compliancehub.cn/rcs`，registry 类 `https://compliancehub.cn/api/v1/`
- POST JSON；附件 base64；身份规则（DID/号码须注册）与端点的详细字段见 `references/rcs-api.md`。

## 完整 API 参考

见 `references/rcs-api.md`。
