# Creator SKILL — 支付自动化（OpenClaw）

**生产（skill.deinai.ai）：路径 C** — 给用户 `checkoutUrl`，Agent 轮询 orders，**先 MCP 直连搜索、再异步 `openclaw mcp set`**

目标：生产环境**绝不**走后门 automation API。

---

## OpenClaw TUI — 路径 C（推荐）

完整 Prompt：[openclaw-tui-prompt.txt](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/openclaw-tui-prompt.txt) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/openclaw-tui-prompt.txt)

```
注册 → checkout → 提示用户 Stripe 支付 → 轮询 orders → Token → 直连 MCP 搜索 → 汇报 → 异步 mcp set creator-skill-v2
```

在 `openclaw tui` 中整段粘贴 `openclaw-tui-prompt.txt` 即可全自动开通。

---

## 路径 C — 退路

browser 不可用时：把 `checkoutUrl` 给用户手动支付，Agent 仍自动轮询 orders。

---

## Agent 禁止行为

- 向 Stripe API 发送原始卡号
- 用 `sk_sess_` 调 MCP
- `paymentPending` 时建 Token / 搜索
- 在 coding CLI 跑需要 browser 的支付流程

---

## 相关

- [onboarding.md](https://clawhub.ai/api/v1/skills/creator-skill-v2/file?path=references/onboarding.md) · [SkillHub](https://skill.deinai.ai/portal/docs/creator-skill-v2/references/onboarding.md)
