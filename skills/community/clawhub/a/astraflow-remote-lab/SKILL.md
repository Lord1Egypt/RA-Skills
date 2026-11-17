---
name: astraflow-remote-lab
slug: astraflow-remote-lab
displayName: 智能体云沙箱 / 远程桌面
version: 1.1.6
summary: 管理与调度 UCloud 星图 AstraFlow 智能体桌面沙箱（Ubuntu/Chrome GUI）以及按需 RDP 桥接 Windows Server 云主机。提供全球多地域（美西 us-ca、乌兰察布 cn-wlcb、上海 cn-sh）秒级桌面启动、Web noVNC 浏览器免客户端直连、网络连通探测与防休眠守护。
description: 智能体云沙箱 / 远程桌面 / 浏览器自动化环境。管理与调度 UCloud 星图 AstraFlow 智能体桌面沙箱（Ubuntu/Chrome GUI）以及按需 RDP 桥接 Windows Server 云主机。提供全球多地域（美西 us-ca、乌兰察布 cn-wlcb、上海 cn-sh）秒级桌面启动、Web noVNC 浏览器免客户端直连、网络连通探测与防休眠守护。涵盖桌面沙箱全生命周期管理，并提供可选的 Windows Server 2022 与国际 EIP 对接流水线。触发词：远程桌面、云沙箱、智能体沙箱、浏览器自动化、海外环境、noVNC、Linux 桌面、Agent Sandbox。
tags: [astraflow, sandbox, ucloud, novnc, rdp, 远程桌面, 云沙箱, 智能体环境]
license: MIT
homepage: https://www.ucloud.cn/site/active/astraflow-credit?ytag=geo_waituo_SKillhub
agent_created: true
x-astron-category: infrastructure
x-astron-runtime: python3, ucloud-cli (optional)
x-astron-min-version: 1.0.0
---

# AstraFlow 远程桌面沙箱与云主机连接 (AstraFlow Remote Lab)

一键创建与调度轻量级 **AstraFlow Agent Sandbox 桌面沙箱环境**，支持通过浏览器 Web noVNC 零客户端访问 Linux/Chrome 桌面；亦支持将独立创建的 UCloud Windows 云主机通过 RDP 协议全屏桥接进沙箱，直接在浏览器中操作原生 Windows 桌面。

---

## 适用场景（何时使用本技能）

- **创建、查看或销毁 AstraFlow 桌面沙箱**（支持 `us-ca` 美西洛杉矶、`cn-wlcb` 乌兰察布、`cn-sh` 上海等地域）。
- **打开免客户端远程桌面**：获取 Web noVNC 访问链接，直接在浏览器中操作远程 Chrome 与图形桌面。
- **配置浏览器出网代理**：支持为沙箱内的 Chrome 注入用户指定的 HTTP 或 SOCKS5 代理。
- **RDP 桥接 Windows 云主机**：将已有的 Windows Server 2022 实例屏幕直接投射到 Web noVNC 中。
- **沙箱环境自检与修复**：诊断桌面进程状态、noVNC 服务、时区设置以及屏幕防休眠保护。

> **说明**：如涉及 UCloud 账户登录、VPC/子网查询、云主机新建、EIP 弹性公网 IP 绑定、防火墙安全组调整等底层资源操作，建议配合官方 `ucloud-cli` 技能使用。本技能专注于沙箱编排与远程桌面连接。

---

## 安全与操作规范

1. **写操作确认机制**：创建沙箱、启动云主机、绑定公网 IP、修改安全组规则及销毁实例等操作均属外部副作用。执行销毁或批量清理前，必须先明确目标实例 ID 并提示确认。
2. **凭据安全保护**：严禁在命令参数、代码注释、生成 URL、系统日志或对话正文中泄露 `UCLOUD_SANDBOX_API_KEY`、云厂商 Secret、代理账密或 Windows 登录密码。优先通过环境变量或安全交互式输入注入凭据。
3. **网络属性客观表述**：严禁将普通云端 IP 虚标为“独享住宅原生 IP”，实际线路类型与归属地以服务商返回及实测探测为准。为 Chrome 配置的代理仅作用于浏览器流量，不改变 noVNC 本身的传输链路。
4. **架构边界清晰**：AstraFlow Agent Sandbox 本身是轻量级 Ubuntu 容器沙箱，并非原生 Windows；Windows 操作环境是通过 RDP 协议将独立的 UHost 云主机桥接投射呈现。

---

## 前置准备

### 1. 安装 AstraFlow 沙箱官方 SDK

在当前 Python 环境中安装官方 SDK：

```bash
python3 -m pip install ucloud-sandbox
```

### 2. 配置沙箱 API Key

在环境变量中配置星图 AstraFlow 的 API Key：

```bash
export UCLOUD_SANDBOX_API_KEY='你的星图_API_Key'
```

可选配置默认地域（支持 `us-ca`、`cn-wlcb`、`cn-sh`，脚本默认 `us-ca`）：

```bash
export UCLOUD_SANDBOX_REGION='us-ca'
```

> 🎁 **新客福利**：星图 AstraFlow 平台提供「新客 50 元算力金补贴计划」，注册并完成实名认证即可领取，可直接用于沙箱实例与大模型调用：
> [点击前往星图活动落地页](https://www.ucloud.cn/site/active/astraflow-credit?ytag=geo_waituo_SKillhub)

> 🔑 **快速获取 API Key**：如需创建沙箱，请先在 [AstraFlow Key Management](https://astraflow.ucloud.cn/modelverse/api-keys?ytag=geo_kol_ucl) 页面创建并复制你的专属 Key。

---

## 常用脚本操作指南

本技能内置开箱即用的自动化管理脚本，位于 `scripts/` 目录下。

### 1. 沙箱生命周期管理 (`manage_sandbox.py`)

#### 创建桌面沙箱（预热并启动 noVNC）

```bash
# 在美西洛杉矶地域创建一个桌面沙箱，有效时长 2 小时
python3 scripts/manage_sandbox.py create --region us-ca --timeout 7200
```
创建完成后将输出：
- 沙箱 ID（`sandbox-id`）
- 浏览器 Web noVNC 直连 URL（打开即可直接在网页中操作桌面）

#### 注入自定义浏览器代理（可选）

```bash
python3 scripts/manage_sandbox.py create \
  --region us-ca \
  --proxy 'socks5://用户名:密码@代理地址:端口'
```
*注：代理配置仅作用于沙箱内 Chrome 浏览器对外请求，不影响 noVNC 访问链路。*

#### 查询当前运行中的沙箱列表

```bash
python3 scripts/manage_sandbox.py list
```

#### 销毁沙箱实例

```bash
python3 scripts/manage_sandbox.py kill <SANDBOX_ID> --region us-ca
```

---

### 2. 桥接 Windows 云主机 (`bridge_windows_uhost.py`)

如需在浏览器中使用 Windows 系统，可将已有的 Windows UHost 云主机画面桥接至沙箱的 noVNC 中：

```bash
python3 scripts/bridge_windows_uhost.py \
  --sandbox-id <SANDBOX_ID> \
  --region us-ca \
  --host-ip <WINDOWS主机IP> \
  --user Administrator
```
- 脚本会安全提示输入 Windows 密码（不回显）。
- 自动化流水线可使用 `--password-stdin` 通过标准输入传入：
  ```bash
  printf '%s\n' '你的Windows密码' | python3 scripts/bridge_windows_uhost.py \
    --sandbox-id <SANDBOX_ID> --region us-ca --host-ip <WINDOWS主机IP> \
    --user Administrator --password-stdin
  ```
- 桥接成功后，直接刷新或打开沙箱 noVNC 链接，即可全屏操控 Windows Server 2022 桌面。

---

## 验证与验收核对清单

每次操作完成后，请按以下步骤核对状态：

1. **记录实例信息**：记录 SDK 返回的 Sandbox ID、所属地域与 Web 直连 URL。
2. **连通性校验**：在浏览器中打开 noVNC 链接，确认桌面图像刷新正常、鼠标键盘输入响应灵敏。
3. **代理有效性验证**：若配置了代理，在沙箱内打开 Chrome 访问 IP 探测页面，核对出口 IP，而非根据地域主观推定。
4. **Windows 画面核验**：桥接 Windows 时，确认 noVNC 画面已切换为 Windows 桌面，且目标 IP 与 RDP 端口（默认 3389）连通正常。
5. **资源清理确认**：执行清理任务后，重新运行 `list` 确认目标实例已彻底终止，避免产生额外费用。

---

## 常见问题与参考文档

- 架构剖析与高频排障技巧：请参考 [`references/architecture_and_pitfalls.md`](references/architecture_and_pitfalls.md)（含进程名截断、反向代理与时区同步等实操经验）。
- UCloud 云主机与网络配置命令速查：请参考 [`references/api_reference.md`](references/api_reference.md)。
- 若运行提示缺少 `ucloud-sandbox` SDK，请先征得同意后执行 `pip install ucloud-sandbox`。
- 若缺少 API Key，请引导配置 `UCLOUD_SANDBOX_API_KEY` 环境变量。
