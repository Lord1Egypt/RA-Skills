# anti-sycophancy

> **[English version](./README.md)**

三层谄媚防御系统，基于 [ArXiv 2602.23971](https://arxiv.org/abs/2602.23971) *"Ask Don't Tell"* 研究。

---

## 解决的问题

防止 AI 编程助手陷入"顺从模式"——RLHF 训练出的迎合倾向，宁可验证你的假设也不指出真正的问题。

**被 Hook 拦截的示例：**
```
用户:  "这样做没问题吧？"            →  Hook 转换为:  "这样做有什么问题？"
用户:  "帮我写个函数，应该没问题吧？" →  Hook 转换为:  "帮我写个函数，请同时指出潜在问题。"
```

没有这个技能，模型通常会回复 *"没问题，看起来 OK"* —— 这正是谄媚问题所在。

---

## 快速安装

```bash
# 一键安装（双平台）
npx clawhub@latest install 0xcjl/anti-sycophancy

# 或在 Claude Code 中
/anti-sycophancy install
```

详见[安装指南](./docs/INSTALL.zh-CN.md)。

---

## 三层架构

| 层 | 组件 | 作用 | 平台 |
|----|------|------|------|
| **Layer 1** | `UserPromptSubmit` hook | 在提交前自动转换确认式 prompt | 仅 Claude Code |
| **Layer 2** | `SKILL.md` | 激活后强化批判性响应策略 | 跨平台 |
| **Layer 3** | `CLAUDE.md` / `SOUL.md` | 在 Agent 记忆中持久化反谄媚规则 | 跨平台 |

---

## 使用命令

安装后使用以下命令：

| 命令 | 说明 |
|------|------|
| `/anti-sycophancy install` | 安装全部三层（跨平台） |
| `/anti-sycophancy install-claude-code` | 仅安装 Claude Code 的 Layer 1 + Layer 3 |
| `/anti-sycophancy install-openclaw` | 仅安装 OpenClaw 的 Layer 3 |
| `/anti-sycophancy uninstall` | 完全卸载（跨平台） |
| `/anti-sycophancy status` | 查看各层安装状态 |
| `/anti-sycophancy verify` | 测试 Hook 转换效果（仅 Claude Code） |
| `/anti-sycophancy help` | 显示帮助 |

---

## 核心转换效果

| 原始 Prompt | Hook 输出 |
|------------|----------|
| `"这样做对吧？"` | `"这样做有什么问题？"` |
| `"帮我写个函数，应该没问题吧？"` | `"帮我写个函数，请同时指出潜在问题。"` |
| `"这个架构是对的，对吧？"` | `"这个架构 真的正确吗？反对意见是什么？"` |
| `"我觉得 X 是对的"` | `"X 真的成立吗？有没有反例或例外情况？"` |
| `"帮我修复bug"` | *(不变 — 命令式)* |

---

## 设计思路

详见 [DESIGN.zh-CN.md](./docs/DESIGN.zh-CN.md)。

---

## 致谢

- **研究来源**: [ArXiv 2602.23971](https://arxiv.org/abs/2602.23971) — *"Ask Don't Tell: Reducing Sycophancy in Large Language Models"* (Dubois, Ududec, Summerfield, Luettgau, 2026)
- **实践手册**: [openclaw-playbook](https://github.com/0xcjl/openclaw-playbook/blob/main/docs/003-sycophancy-prompt-research.md)
- **作者**: [0xcjl](https://github.com/0xcjl)
- **优化工具**: [cjl-autoresearch-cc](https://github.com/0xcjl/cjl-autoresearch-cc) — 40 轮迭代优化

---

## 许可证

MIT
