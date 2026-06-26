# 你聊我干 🐋🧠

<p align="center">
  <strong>你在 DeepSeek 里聊天，我在 OpenClaw 帮你干活。</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/platform-OpenClaw-orange" alt="platform">
  <img src="https://img.shields.io/badge/skill%20type-automation-purple" alt="type">
</p>

<p align="center">
  <strong>🐋 让免费的 DeepSeek 网页版当牛做马出设计、写代码、反复打磨</strong><br>
  <strong>🧠 我负责扫尾——抓过来跑起来、改 bug、接上线</strong><br>
  <em>省了 API 订阅费，还不用手动复制粘贴，省钱又省命。</em>
</p>

---

## 🤔 你肯定遇到过

在 DeepSeek 网页版聊了一下午，设计了一套完美架构，迭代了七八轮，生成了十几个文件——然后你盯着分享链接，开始了一个一个复制粘贴、建文件夹、对齐路径的苦力活。

**这个 Skill 就是为了干掉这几步而生的。**

## 🎬 之前 vs 之后

| 之前（手动） | 之后（你聊我干） |
|---|---|
| 😤 手动 Copy 每个代码块 | 🤖 自动提取全部文件 |
| 😤 手动建文件夹、对齐路径 | 🤖 按项目结构树写入 |
| 😤 分不清哪个版本是最新的 | 🤖 多轮对话自动取最后一版 |
| 😤 代码片段散落各地不知放哪 | 🤖 标记为 FRAGMENTS_TODO |
| 😤 读完后忘了要干什么 | 🤖 生成 README + TODO |
| 😤 从零开始写剩下的 | 🤖 接着聊天记录继续开发 |

## ⚡ 怎么用

丢个链接就行：

```
https://chat.deepseek.com/share/abc123 帮我继续开发
```

Skill 自动五步走：

```
🔗 检测链接 → 🖥️ 渲染页面 → 📦 提取代码 → 💾 写入项目 → 🔧 继续开发
```

## 🎯 支持这些场景

| 场景 | 怎么处理 |
|------|----------|
| 🕸️ 单文件网页 | 自动抓取 HTML 完整内容 |
| 📱 多文件项目 | 按项目结构树分文件写入 |
| 🔄 多轮迭代对话 | 只取每个文件的**最新版本** |
| 📝 代码片段/关键要点 | 收集到 `FRAGMENTS_TODO.md` 而非乱放 |
| 🧩 缺文件 | 对比结构树，列出缺失清单 |

## 📦 安装

```bash
openclaw skills install deepseek-dev-assistant
```

或直接放入 `skills/` 目录。

依赖：Puppeteer（首次用自动安装）

## 🏗️ 设计哲学

DeepSeek 网页版——免费、强力、支持多轮打磨。但它只负责「生成」，不管「落地」。

OpenClaw——你桌上的管家，管文件、跑命令、开浏览器。

把前者当「设计院」，后者当「施工队」。一个出图，一个干活。

**API 按 token 计价，网页版按小时免费。把重体力活交给网页版，把收尾整合交给 OpenClaw。**

## 📁 项目结构

```
deepseek-dev-assistant/
├── README.md                              ← 本文件
├── SKILL.md                               ← Skill 执行指令（给 AI 看的）
├── _meta.json                             ← 发布元数据
└── references/
    ├── deepseek-page-structure.md         ← DeepSeek 页面结构参考
    └── example.md                         ← 端到端使用示例
```

## 🧪 实战验证过

不是纸上谈兵。真实跑通的项目：

- ✅ 2048 网页游戏（单文件 HTML，746 行）
- ✅ WatchDose 服药提醒 App（11 个 Swift 文件，~1100 行）
- ✅ 结构树检测 + 缺失标注 + 代码片段收集

## ⚠️ 限制

- 需要 Puppeteer（读取 JS 渲染页面）
- DeepSeek 分享页结构变化需要更新 references
- 私密/过期链接无法访问（这是 DeepSeek 的限制）

## 📜 License

MIT — 随便用，欢迎 PR。
