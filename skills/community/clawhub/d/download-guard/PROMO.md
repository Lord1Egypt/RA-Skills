# C 盘天天红？AI Agent 偷偷往你 C 盘塞了几十个 G 的垃圾

> 花了三个月给 AI Agent 装了一堆 Skill，最后发现最该先装的是这个。

---

## 你是怎么发现问题的？

我猜你大概率是这么发现的：

> 某天给 AI Agent 说「帮我装个 PyTorch」→ Agent 敲了一行 `pip install torch` → 装完了 → 你问「下到哪了？」→ Agent 沉默了。

或者更惨的版本：

> 外接硬盘装满了模型 → 拔了 → 过了两天发现 C 盘直接红了 → 一看 Agent 默默把东西全写回了 C 盘，十几 GB 的模型文件。

这**不是** Agent 的 bug。这是因为——**Agent 默认就用系统当前目录，而当前目录大概率在 C 盘**。

---

## 我统计了一下：AI Agent 一个月能在 C 盘写多少东西

| 操作 | 单次大小 | 月度频率 | 月总量 |
|------|---------|---------|--------|
| `pip install torch` | ~2.1 GB | 3 次 | 6.3 GB |
| `ollama pull llama3` | ~5.2 GB | 2 次 | 10.4 GB |
| `huggingface-cli download` | ~14 GB | 1 次 | 14 GB |
| npm 全局包 | ~200 MB | 5 次 | 1 GB |
| git clone 大仓库 | ~500 MB | 10 次 | 5 GB |
| pip 缓存积累 | ~3 GB | 持续 | 3 GB |
| **合计** | | | **~40 GB/月** |

**一个月 40 GB，C 盘能不红吗？**

---

## 市面上的方案为什么都不好用？

| 方案 | 问题 |
|------|------|
| 「手动改路径」 | pip/npm/ollama 每个都要单独配，换了工具又得重新配 |
| 「挂载大硬盘做 C 盘」 | 治标不治本，换电脑怎么办 |
| 「用 Disk Cleanup 清理」 | 临时文件好清，但 pip cache、npm cache 你都找不到在哪 |
| 「每次问 Agent 下哪了」 | 你不可能盯着每一个命令 |
| 「不用 AI Agent」 | ……那不现实 |

**问题的本质是：下载这件事对用户完全不透明。** Agent 知道下到哪了，但不告诉你。

---

## 所以我做了 Download Guard

一句话描述：

> **一个 AI Agent Skill，每次下载都告诉你下到哪了 + 磁盘还剩多少空间 + 路径有问题宁可阻止也不偷偷写 C 盘。**

把它装到你的 WorkBuddy / OpenClaw 里，它会**自动拦截所有下载命令**：

```
🛡️ Download Guard
📦 文件     : torch-2.3.0.whl
📏 大小     : 2.1 GB
📂 写入至   : F:\AI-Downloads\2026-05-26\
💾 F 盘     : 132 GB 可用  ✅ OK
💿 C 盘     : 58 GB 可用   ✅ OK
🔒 路径可用 : ✅ OK
▶ 继续执行...
```

**再也不会不知道下到哪了。**

---

## 这是它最狠的三个设计

### 1. 路径不可用 → 直接阻止，绝不回退 C 盘

这是市面上没有第二个方案能做到的。

> 你把外接盘拔了 → Agent 想说「路径没了那我写 C 盘吧」→ Download Guard 直接 **BLOCK**。

```
🚫 Download Guard · BLOCKED
❌ 路径不可用 : F:\AI-Downloads
⚠️ 原因       : Drive F: not found
🛑 操作       : 已阻止下载，未回退 C 盘
💡 请重新连接磁盘或修改下载目录
```

**宁可不下，也不偷偷写 C 盘。** 这就是铁则。

### 2. 日志自动清理，不是光记不看

每次下载都记日志，但日志也是垃圾——所以它**自动归档 + 自动清理**：

- 超过 30 天的日志自动归档
- 归档文件超过 10 MB 自动删除
- 每天第一次交互自动给你出个环境快报

你不需要管理日志，它自己管自己。

### 3. C 盘缓存一键迁移

很多人不知道：pip 缓存、npm 缓存、ollama 模型全堆在 C 盘。Download Guard 一键帮你扫出来并迁走：

```
🛡️ Download Guard · 缓存扫描

  pip cache    : F:\pip-cache       ✅ 已迁走
  npm prefix   : E:\node_global     ✅ 已迁走
  npm cache    : E:\node_cache      ✅ 已迁走
  ollama models: C:\Users\...       ⚠️ C 盘！建议迁移

说「迁移缓存」一键迁走 →
```

---

## 安装只需要一步

```bash
clawhub install download-guard
```

或者手动：

```bash
git clone https://github.com/nihaoljx/download-guard.git
cp -r download-guard ~/.workbuddy/skills/download-guard/
```

第一次触发下载时，它自动扫描磁盘、推荐最优路径，你确认一下就行。**之后再也不用管了。**

---

## 对 AI 说这些话就能用

| 你说 | 它做 |
|------|------|
| 「下载了什么」 | 查看最近 20 条下载记录 |
| 「缓存在哪」 | 扫描所有工具缓存位置 |
| 「迁移缓存」 | C 盘缓存一键迁走 |
| 「磁盘空间」 | 查看各盘剩余空间 |
| 「刚才下的在哪」 | 最近一次下载位置 |
| 「检查路径」 | 验证下载目录是否健康 |
| 「修改下载目录」 | 更换下载目录 |
| 「下载版本」 | 当前版本号 |

---

## 覆盖 14 种工具

pip · npm · pnpm · bun · conda · cargo · go · git clone · ollama · huggingface-cli · docker · winget · choco · scoop · curl · wget

**智能跳过 venv 内的 `pip install`** — 不影响项目本地环境。

---

## 核心价值总结

| 之前 | 之后 |
|------|------|
| 下载了不知道去哪 | 每次下载实时告知位置和状态 |
| C 盘天天红 | 下载自动走大盘，路径不可用直接阻止 |
| 日志垃圾堆成山 | 自动归档+清理，设好就不用管 |
| 缓存全在 C 盘 | 一键扫描+一键迁移 |
| 外接盘拔了 Agent 静默写 C 盘 | 宁可阻止，绝不回退 |

---

## 一句话

**如果你用 AI Agent 下载任何东西，你需要 Download Guard。**

👉 [GitHub 仓库](https://github.com/nihaoljx/download-guard) | 👉 `clawhub install download-guard`

---

*觉得有用？给个 ⭐ Star，让更多被 C 盘困扰的人看到它。*
