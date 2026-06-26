<div align="center">

# 🦀 ClawScan

**适用于 OpenClaw 部署环境的安全扫描技能**

[![版本](https://img.shields.io/badge/技能版本-0.1.3-blue?style=flat-square&logo=semanticrelease)](./references/api-contract.md)
[![API](https://img.shields.io/badge/API-v0.1-informational?style=flat-square&logo=fastapi)](./references/api-contract.md)
[![平台](https://img.shields.io/badge/平台-macOS%20%7C%20Linux-lightgrey?style=flat-square&logo=linux)](.)
[![Python](https://img.shields.io/badge/python-3.8%2B-yellow?style=flat-square&logo=python)](./scripts)
[![许可证](https://img.shields.io/badge/许可证-MIT-green?style=flat-square)](.)
[![English Docs](https://img.shields.io/badge/Docs-English-blue?style=flat-square&logo=googletranslate)](./README.md)

*查看 [English 英文版](./README.md)*

</div>

---

ClawScan 是一个**只读安全技能**，用于对本地 OpenClaw 环境进行初步威胁评估。它通过连接 ClawScan 云服务，将您的安装环境与已知漏洞数据库、恶意技能哈希库和网络暴露规则进行匹配 —— 全程不上传密钥、提示词或完整文件内容。

---

## 🛡️ ClawScan 能识别哪些风险？

| 模块 | 风险类别 | 检测内容 |
|---|---|---|
| 🔍 **vulnerability** | CVE / 版本风险 | OpenClaw 版本是否落入已知漏洞范围 |
| 🧬 **skills-check** | 供应链 / 恶意软件 | 已安装技能文件的 SHA-256 是否命中恶意哈希库 |
| 🌐 **port-check** | 网络暴露 | 服务是否绑定到 `0.0.0.0` 或 `::` 等可能被外部访问的地址 |
| 🔄 **update-check** | 工具过期 | 当前安装的 ClawScan 技能版本是否落后于最新发布 |
| ⏰ **scheduled-scan** | 持续监控 | 按配置间隔自动运行上述全部检查 — 仅在发现风险时发出告警 |

> **范围说明：** ClawScan 只报告其语料库中的*已知*问题。检查通过意味着未匹配到已知威胁，并不代表环境绝对安全。

---

## 📦 运行要求

- 本地已安装 **OpenClaw**（OpenClaw）
- **Python 3.8+**（用于运行附带的辅助脚本）
- 可访问 `https://clawscan.autosec.dev`
- 系统中存在 `ss` 或 `lsof`（用于端口扫描）

---

## 🚀 快速开始

### 1. 安装技能

将 `clawscan` 技能目录放置到 OpenClaw 的技能根目录下：

```bash
# 默认技能位置
~/.openclaw/skills/clawscan/
```

### 2. 注册客户端

首次使用时，注册客户端以获取持久化的匿名 ID：

```
对 OpenClaw 说："注册我的 ClawScan 客户端"
```

这会在 `~/.openclaw/clawscan/client.json` 中生成一个随机 UUID，不涉及任何硬件指纹信息。

### 3. 运行首次扫描

```
对 OpenClaw 说："运行完整的 ClawScan 检查"
```

---

## 🔧 各模块使用说明

### 🔍 `vulnerability` — 版本漏洞检查

检查已安装的 OpenClaw 版本是否落入任何已知漏洞范围。

```
"我的 OpenClaw 版本有漏洞吗？"
"检查 OpenClaw 版本风险"
```

**示例报告：**

```
模块：vulnerability
状态：正常  |  风险：高

发现：OC-2026-001 — 示例漏洞
  受影响版本：<= 1.2.3  |  当前版本：1.2.3  |  修复版本：1.2.4
  建议：升级到 1.2.4 或更高版本

范围说明：此检查仅针对已知漏洞版本范围。
```

---

### 🧬 `skills-check` — 恶意技能哈希检测

为已安装技能的每个文件计算 SHA-256 哈希值，并与 ClawScan 威胁语料库比对。**仅上传哈希值，不上传文件内容。**

```
"检查我的已安装技能是否含恶意内容"
"扫描技能哈希"
```

也可直接运行采集脚本：

```bash
python scripts/collect_skill_hashes.py ~/.openclaw/skills ./skills
```

**无威胁时：**

```
未匹配到已知恶意技能哈希。
这并不证明已安装的技能是安全的。
```

**命中威胁时：**

```
⚠️  在已安装的技能集中匹配到已知恶意内容。

技能：foo  |  风险：高  |  匹配类型：精确哈希
  文件：run.py  →  KnownMaliciousSkill.A
  建议：立即停用并移除该技能
```

---

### 🌐 `port-check` — 网络暴露检查

通过 `ss`（优先）或 `lsof` 检查本地 TCP 监听器，标记所有绑定到非回环地址的服务。

```
"OpenClaw 是否暴露在网络上？"
"检查监听端口"
```

也可直接运行监听器脚本：

```bash
python scripts/list_listeners.py
```

**示例发现：**

```
模块：port-check
状态：正常  |  风险：高

发现：openclaw 监听于 0.0.0.0:3000
  此服务正在所有接口上监听，这会增加暴露风险。
  建议：绑定到 127.0.0.1，或在其前部署经过身份验证的反向代理

范围说明：此结果基于本地监听器状态，并非完整的外部可达性测试。
```

> ClawScan 不会将 `0.0.0.0` 直接判定为"公网暴露" —— 实际暴露程度取决于您的防火墙、NAT、安全组和网络拓扑。

---

### 🔄 `update-check` — ClawScan 技能更新检查

检查当前安装的 ClawScan 技能版本是否落后于最新发布版本。

```
"我的 ClawScan 是最新版本吗？"
```

---

### ⏰ `scheduled-scan` — 定时自动安全扫描

按配置间隔自动运行完整扫描（vulnerability + skills-check + port-check）。**仅在发现安全风险时汇报 —— 若所有检查通过则保持完全静默。**

```
"每 60 分钟启用一次定时 ClawScan"
"设置每 30 分钟自动安全扫描"
```

**设置确认：**

```
ClawScan 定时扫描已启用。
- 间隔：每 60 分钟
- 下次运行：2026-03-09T11:00:00Z
- 汇报方式：仅在发现风险时汇报
```

**检测到风险时：**

```
[ClawScan 定时检查 — 2026-03-09T11:00:00Z]
检测到安全风险，详细报告如下。

... （各模块的标准报告）
```

**一切正常时：**（无任何输出）

调度状态持久化保存在 `~/.openclaw/clawscan/schedule.json`。

---

## 📂 项目结构

```
clawscan/
├── SKILL.md                       # 技能定义（英文）
├── SKILL.zh-CN.md                 # 技能定义（中文）
├── agents/
│   └── openai.yaml                # OpenAI Agent 接口定义
├── references/
│   └── api-contract.md            # 完整 API 请求 / 响应参考
└── scripts/
    ├── collect_skill_hashes.py    # 计算已安装技能的 SHA-256 哈希
    └── list_listeners.py          # 通过 ss / lsof 枚举 TCP 监听器
```

---

## 🔒 隐私与数据最小化

ClawScan 遵循最小必要数据原则：

- ✅ 发送：匿名客户端 UUID、版本字符串、文件哈希值、监听器元数据
- ❌ 绝不发送：文件内容、环境变量、提示词、API 密钥、完整主目录路径（除非用户明确要求）
- 🔑 客户端 ID 为随机 UUID，不使用任何硬件指纹

---

## ⚠️ 使用限制

- ClawScan 仅能检测其当前语料库中收录的**已知**威胁
- 端口检查结果反映的是**本地监听器状态**，而非经过确认的外部可达性
- 漏洞匹配基于**版本范围**，而非运行时行为分析
- 扫描通过意味着**未匹配到已知威胁**，并非安全保证

---

## 🗺️ 路线图

- [ ] 支持 `POST /scan` 聚合端点
- [ ] 扩展恶意技能语料库
- [ ] SBOM / 依赖风险检测模块
- [ ] 定时扫描的 Webhook / 通知集成

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request。请勿在贡献内容中包含真实的威胁特征、凭证或私钥。

---

<div align="center">

为 OpenClaw 生态系统而生 · [English Docs →](./README.md)

</div>
