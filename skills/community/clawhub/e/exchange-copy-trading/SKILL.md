---
name: exchange-copy-trading
description: >-
  Guides OpenClaw to open a browser and complete exchange copy-trading (follow a
  trader) on supported venues: navigate to the copy-trading settings URL, fill the
  follow amount, and confirm. Use when the user asks for 跟单, copy trading, Bitget
  follow-trader flow, or browser automation for exchange copy trading. Requires an
  already-logged-in session and sufficient USDT (≥50). Bitget is supported; Binance
  and OKX are reserved for future URLs in reference.md.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
---

# 交易所跟单（浏览器引导）

本技能指导 **OpenClaw** 使用其 **浏览器 / 网页自动化能力**（如内置浏览器控制、截图与点击链等，以当前运行时实际能力为准）在完成前提条件后，在网页上完成 **跟单** 操作。

## 核心原则

- **不做登录、不收集密码/2FA**：假定用户已在 OpenClaw 将使用的浏览器会话中完成登录。
- **不冒充官方**：仅打开用户确认过的链接；若域名或页面与官方不一致，应中止并提示用户核实（钓鱼风险）。
- **金额与风险**：跟单涉及资金与合约风险；由用户确认金额与条款后再执行自动化步骤。
- **能力退化**：若页面结构变更导致无法可靠定位控件，应停止自动点击，改为逐步引导用户手动完成。

## 执行前检查（必须）

在打开跟单页面前，向用户确认或协助核对：

1. **已登录**目标交易所（当前为 Bitget Web）。
2. **账户可用 USDT ≥ 50**（与用户提供场景一致；若页面有更高中限以页面为准）。
3. 用户已提供 **跟单金额**（数字，单位与页面一致，一般为 USDT）。

任一条件不满足时：**不要**继续自动提交跟单；说明缺什么、如何补齐。

## Bitget：合约跟单（当前已支持）

### 目标链接（示例交易员/策略页，由业务提供）

`https://www.bitget.fit/zh-CN/copy-trading/setting/bfb7477187b73155a395/futures`

> 若需更换交易员或策略，只替换路径中对应 ID 或完整 URL；上架包内默认以上为例。**务必**由用户确认链接来源可信。

### 操作步骤（OpenClaw）

1. **打开浏览器**并导航到上述 URL；等待主内容加载完成（可配合网络空闲或关键文案出现）。
2. 在页面中找到 **跟单金额 / 投入金额** 类输入框（常为 number 或带货币单位的输入框）。
3. 将输入框 **清空后** 填入用户指定的跟单金额；校验为合理正数，且满足页面上的最小/最大提示（若有）。
4. 定位并点击 **跟单 / 确认跟单 / 立即跟单** 等主按钮（以页面实际文案为准）。
5. 若出现 **二次确认、风险提示、协议勾选**，按页面要求完成勾选后再确认；**不得**代用户同意其未明示接受的法律条款——必要时暂停并请用户手动勾选。
6. 观察结果：成功提示、订单/跟单列表变更；失败则收集页面错误或 Toast 文案反馈给用户。

### 失败与重试

- 网络超时、验证码、人机验证：中止自动化，提示用户人工处理后再继续。
- 控件定位失败：截图或描述可见结构，改为 **逐步手动指引**。

## 其他交易所（预留）

Binance、OKX 等的入口 URL、页面结构与选择器不在此版本硬编码。扩展时请将 **权威链接与注意事项** 写入同目录下的 [reference.md](reference.md)，并在本节增加对应 `###` 小节。

## 附加资源

- 交易所与入口对照、占位说明：[reference.md](reference.md)
