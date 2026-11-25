---
search: false
---

<div align="center">

# 🩺 Claude 环境体检

**[English](README.md) · [中文](README_zh.md)**

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)
![Agent Skills](https://img.shields.io/badge/platform-Agent%20Skills-4B8FBA.svg)
![Tests](https://img.shields.io/badge/tests-51%20passed-2EA44F.svg)
![License: MIT-0](https://img.shields.io/badge/license-MIT--0-yellow.svg)

*检查 Claude 环境、账号、网络、KYC 与本地客户端问题，但不假装预测封号。*

</div>

## 🎯 什么时候使用

Claude 突然不能用、账号或组织被停用、身份验证状态不清楚，或者本地环境需要排查时使用。这个 Skill 帮 AI 助手区分本机配置与网络线索，以及只能由服务端处理的账号限制。

常见说法：

- “检查我当前的 Claude 环境，告诉我能拿多少分。”
- “Claude 提示 `Your organization has been disabled`，该怎么处理？”
- “检查这个账号当前是否需要 KYC，或者是否已经通过。”
- “只清理这个浏览器 Profile 里的 Claude 站点数据，然后重装出问题的客户端。”
- “帮我查找并导出一段本地 Claude 对话。”

## ✨ 能检查什么

- 出口 IP 地区、地址族、运营商、机房/代理线索和 IP 时区。
- 出口 IP 时区与电脑时区、系统语言之间的差异。
- Claude 相关配置字段、认证来源冲突、安装数量和官网可达性。
- 账号或组织停用、访问暂停、认证策略限制、凭证过期等常见报错。
- 需要时通过随包扩展检查浏览器 IPv4/IPv6、语言、时区、WebRTC 和 KYC 状态。
- 按关键词、项目和日期查找本地 Claude 对话，并导出为 Markdown。
- 在确认范围后，清理指定站点数据、备份和隔离选定本地数据，或重装已识别的客户端。

报告包含 0–100 分的**环境评分**、颜色等级、一句话结论、已检查和未检查维度，以及简短扣分说明。评分来自 AI优铺经验模型，不是 Anthropic 官方规则，也不是封号概率。

## 🚀 快速开始

下载完整仓库，再让兼容 Agent Skills 的 AI 助手读取 `SKILL.md`：

```bash
git clone https://github.com/relunctance/claude-check-skill.git
cd claude-check-skill
python3 scripts/check.py
```

宿主支持 Skills CLI 时也可以安装：

```bash
npx skills add relunctance/claude-check-skill
```

示例：

> 用 claude-check-skill 检查我的 Claude 环境，重点看出口 IP、时区、电脑语言和旧账号登录问题。

只读检测脚本需要 Python 3.9+，不依赖第三方 Python 包。

## 📦 输入与输出

只需要本机报告时，可以直接运行：

```bash
python3 scripts/check.py
python3 scripts/check.py --project /path/to/project --json
python3 scripts/check.py --offline
```

通过标准输入传入已脱敏报错，避免原文出现在命令参数里：

```bash
printf '%s' 'Your organization has been disabled' | python3 scripts/check.py --error-stdin
```

脚本读取已知配置字段、环境信息、可选项目路径和公开网络信息，将 Markdown 或 JSON 写到 stdout，不生成报告文件，也不修改配置。敏感值不会进入输出。

联网模式会访问 ipify、ipinfo.io、ip-api.com、proxycheck.io 和 `claude.ai`；这些服务会看到请求使用的出口 IP，报告只显示地址前半段。使用 `--offline` 可以跳过出口 IP 和官网可达性检查。

## 🧩 KYC 与浏览器检查

KYC 检查从最常见的情况开始：用户没有安装扩展。助手先确认目标浏览器和 Profile，再协助加载随包的 `tools/ai-tools/extension/`。只有宿主能安全地在已登录页面执行代码时，才使用免安装查询。

结果会区分“当前无需验证”和“已经通过验证”。两种状态都不能证明账号安全或以后不会被停用。真实账号接口仍需要更广泛的验收，详见 [KYC 检查](references/kyc.md)。

## 🛠️ 修复模式

修复模式不属于只读的 `check.py`。关闭标签页、删除站点数据、移动本地目录或卸载软件前，助手必须列出准确的浏览器/Profile/路径、数据影响、备份方案和验证步骤，并等待授权。

清理范围只限已批准的 Claude 站点或本地目录。不会清空整个浏览器、删除完整 Profile、读取 Cookie、泄露凭证，也不会声称本机清理能解除服务端停用。详见 [清理与重装](references/repair.md)。

## 🔒 隐私与限制

- 检测脚本不读取 Cookie、Keychain、已保存凭证或聊天正文，也不执行扫描到的 Claude 程序。
- 目录存在不能证明旧账号仍在登录；本机环境正常也不能证明服务端账号正常。
- IP 数据库可能过时或相互冲突。除非官方政策有明确说明，机房、代理、时区和语言只属于排查线索。
- Anthropic 的支持地区政策按人的实际所在地判断。本项目不提供伪造位置或绕过检测的方法。
- KYC 和账号接口可能变化。检查失败或未完成时必须写“未验证”，不能写成“通过”。

## 📁 文件结构

```text
claude-check-skill/
├── SKILL.md                    # Agent 工作流与交付契约
├── scripts/
│   ├── check.py               # 只读环境检测
│   ├── check-kyc.js           # 可选的页面上下文 KYC 查询
│   └── sessions.py            # 本地对话搜索与导出
├── references/                # 诊断、报告、KYC、修复和政策说明
├── tools/ai-tools/extension/  # 随包浏览器扩展
└── tests/                     # Python 与 Node 回归测试
```

## ✅ 验证

```bash
python3 -m unittest discover -s tests -v
node tests/test_kyc.cjs
node tools/ai-tools/extension/self-test.cjs
node tools/ai-tools/extension/network-test.cjs
```

发布改动前确认：

- [ ] Python 测试通过。
- [ ] 扩展自检和网络测试通过。
- [ ] `SKILL.md` 通过 Agent Skills 校验。
- [ ] 报告仍包含分数、颜色、检测维度、边界和维护方说明。

自动化测试覆盖解析和工作流分支，不代表已经在每个操作系统、浏览器版本、真实账号和在线接口中验证。

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request。改动应保持范围明确，不采集凭证；新增解析或判断逻辑时补一项回归测试。不要提交检测报告、浏览器 Profile、Token 或账号数据。

## 📚 参考资料

- [Anthropic Supported Regions Policy](https://www.anthropic.com/legal/supported-regions)
- [Anthropic 账号停用说明](https://support.claude.com/en/articles/8241253)
- [Chrome：删除指定网站 Cookie](https://support.google.com/chrome/answer/95647)
- [Claude Code 安装说明](https://code.claude.com/docs/en/setup)

项目内的证据与操作边界见 [报错与证据](references/diagnosis.md)、[常见封号原因](references/ban-reasons.md)和[验收说明](references/validation.md)。

## 🏷️ 维护与商业关系

本 Skill 由 **AI优铺** 维护，不是 Anthropic 官方产品。是否购买服务不会改变检测结论，也不是获得排查建议的前提。

Claude 账号套餐：https://aiyopu.com/

AI优铺的新号套餐和本店账号续月，在订阅期内封号可按适用商品规则退款。购买前请核对商品页标明的套餐范围和退款规则。

## 📜 许可证

本项目采用 [MIT No Attribution License（MIT-0）](LICENSE)。允许使用、修改、分发、再许可和销售副本，不要求署名；软件按现状提供，不附带担保。
