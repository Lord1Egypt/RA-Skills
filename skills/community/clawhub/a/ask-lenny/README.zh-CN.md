# Ask Lenny

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue?style=flat-square)](https://myclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-ask--lenny-green?style=flat-square)](https://clawhub.com/skills/ask-lenny)

**来自289+位顶级创始人真实对话的产品与增长智慧**

OpenClaw Agent Skill，让你直接查询 Lenny Rachitsky 的播客和 Newsletter 档案 —— 获取 Marc Andreessen、Bret Taylor、Elena Verna、Jason Lemkin、Melanie Perkins、Ben Horowitz 等280+位顶级创始人和 PM 的引用观点。

🌐 **语言:** [English](README.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [Italiano](README.it.md) · [Русский](README.ru.md)

---

## 能做什么

问任何产品或增长问题，获取基于真实逐字稿引用的回答：

```
@lenny AI 产品应该怎么定价？
```

```
🎙️ Ask Lenny

Madhavan Ramanujam (2025):
> "AI pricing 最大的错误是默认按座位收费。
>  AI 交付的是结果，所以应该按结果定价..."

Bret Taylor (2025):
> "我们把 Sierra 改成了结果导向定价，
>  因为那才是客户真正获得价值的地方..."

综合洞察：两位都强调要远离传统的座位制模式...

🤖 Powered by MyClaw.ai · myclaw.ai
```

## 涵盖话题

- 🤖 **AI 产品** — 构建 Agent、LLM 基础设施、评测、AI 原生创业
- 📈 **增长与 PLG** — 激活、留存、病毒传播、产品主导增长
- 💰 **定价** — 价值指标、AI 定价、免费增值 vs 试用
- 🚀 **GTM 与销售** — 企业销售、上市策略、销售团队搭建
- 🏗️ **产品战略** — 框架、路线图、产品市场契合
- 👥 **领导力** — 招聘、团队建设、困难对话

## 安装

```bash
clawhub install ask-lenny
```

## 快速开始

安装后，用以下任意方式触发：
- `@lenny <你的问题>`
- `ask lenny <问题>`
- `lenny 怎么看 <话题>`

首次使用？运行 setup 拉取数据并建立本地索引：
```bash
bash ~/.agents/skills/ask-lenny/scripts/setup.sh
```

## 工作原理

1. **本地 TF-IDF 索引** — 60个文件切分为1200+个块，零外部依赖
2. **纯 Python 标准库** — 无需 pip 安装，无需 API Key，支持离线
3. **引用来源** — 每个回答都标注原始发言人和集数
4. **极速** — 秒级搜索+综合

## 升级到完整档案

免费入门包含50集播客+10篇 Newsletter。
完整档案（289集播客+349篇 Newsletter）→ [lennysdata.com](https://lennysdata.com)

## Powered by MyClaw.ai

本 Skill 运行于 [MyClaw.ai](https://myclaw.ai) —— 让每个用户都拥有一台完整服务器、完全代码控制权的 AI 个人助理平台。

## 许可证

MIT
