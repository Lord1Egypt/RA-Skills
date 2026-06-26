<h1 align="center">🤫 Agent Hush</h1>

<p align="center">
  <strong>给你的 AI Agent 装上隐私安检——推代码前自动拦截敏感数据泄露</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.6+-green.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.6+"></a>
  <a href="https://github.com/elliotllliu/agent-hush/stargazers"><img src="https://img.shields.io/github/stars/elliotllliu/agent-hush?style=for-the-badge" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#安装">安装</a> · <a href="./README_EN.md">English</a> · <a href="#装了之后是什么样">效果演示</a> · <a href="#检测范围">检测范围</a>
</p>

---

## 为什么需要 Agent Hush？

你让 Agent 帮你推代码、发布 Skill、同步文件——但你有没有想过，这些文件里可能藏着：

- 🔑 "帮我推代码" → config 里的 **API Key 一起被推上 GitHub 了**，全世界都能看到
- 🏠 "帮我同步 workspace" → MEMORY.md 里写了你的 **真实姓名、手机号、服务器 IP**，全部公开了
- 🔐 "帮我发布这个 Skill" → 忘了 Skill 目录里还有一个 **带密码的数据库连接串**
- 📁 "帮我分享这个项目" → 文件路径暴露了你的 **用户名和系统结构**
- 🗝️ "帮我 commit" → .env 没加 .gitignore，**Discord Bot Token 直接进了 git 历史**

**这些事每天都在发生。** GitHub 上每天有上千个密钥被意外提交。

**Agent Hush 让你不用操心这件事：**

装上之后，你照常工作。Agent 在每次对外操作前自动过一遍安检——有问题就拦住告诉你，没问题你甚至不知道它检查过。

**就像机场安检：你只管走，它帮你看。**

## 安装

复制下面这句话发给你的 Agent：

```
帮我安装 Agent Hush：https://raw.githubusercontent.com/elliotllliu/agent-hush/main/docs/install.md
```

装完了。没有第二步。

## 装了之后是什么样？

### 🔑 推代码时拦住密钥泄露

```
用户：帮我推代码

Agent：等一下，config.json 第 12 行有个 GitHub Token (ghp_***abcd)，
      推上去会泄露。我帮你替换掉再推？

用户：好

Agent：搞定，已经替换并推送了 ✅
```

### 🏠 发布 Skill 时拦住个人信息

```
用户：帮我把这个 Skill 发到 ClawHub

Agent：你的 SKILL.md 里有一个真实的服务器 IP (49.51.***.114)
      和一条 SSH 命令。发布后所有人都能看到。要我处理掉吗？

用户：处理掉

Agent：已替换，发布成功 ✅
```

### 📁 同步 workspace 时提醒隐私风险

```
用户：帮我同步到 GitHub

Agent：MEMORY.md 里有你的真实姓名和手机号，
      TOOLS.md 里有服务器 IP 和 SSH 密钥路径。
      这些会跟着一起推上去，要我先处理吗？

用户：MEMORY.md 的处理掉，TOOLS.md 的不用管

Agent：好的，MEMORY.md 已脱敏，已推送 ✅
```

### ✅ 没问题时——你什么都感觉不到

```
用户：帮我推代码

Agent：已推送 ✅

（Agent 其实检查过了，但没问题就不打扰你）
```

**你不需要学任何命令，不需要改任何习惯。装上就行。**

## 智能白名单

检测到的东西不一定都要处理。告诉 Agent "这个不用管"，它就永远不会再提醒：

```
Agent：你要推的文件里有个 192.168.1.100，要处理吗？

用户：不用管，这是测试 IP

Agent：好的，以后不会再提醒这个了 ✅
```

支持通配符——比如"所有 example.com 的邮箱都不用管"：

```
用户：以后 example.com 的邮箱都别提醒了

Agent：好的，已加入白名单：*@example.com ✅
```

白名单保存在项目目录里，跟着项目走。你不需要编辑任何配置文件。

## 检测范围

**🔴 高置信度（自动拦截）：**
- AWS Key（`AKIA` 开头）、GitHub Token（`ghp_`）、OpenAI Key（`sk-proj-`）
- Slack Token、Discord Bot Token、Anthropic Key
- 私钥文件块（`-----BEGIN PRIVATE KEY-----`）
- 数据库连接串（`mysql://user:pass@host`）
- 身份证号、银行卡号

**🟡 低置信度（提醒但不阻断）：**
- 通用 `password=xxx`、`token=xxx` 赋值
- 内网 IP（192.168.x.x、10.x.x.x）
- SSH 密钥路径、SSH 命令
- 邮箱地址、手机号
- 绝对路径（`/root/`、`/home/user/`）

## 安全性

做隐私保护的工具，自己必须先过关：

- 🔒 **纯本地运行** — 所有扫描和脱敏都在你本机完成，不会把你的文件发送到任何服务器
- 👀 **完全开源** — 每一行代码都可以审查，没有藏着掖着的东西
- 📦 **零依赖** — 只用 Python 标准库，不引入任何第三方包，不存在供应链攻击风险
- 🛡️ **默认不改你的文件** — 扫描和检查只读不写，脱敏输出到副本，原件不动
- 💾 **修改前自动备份** — 即使你选择直接修改，也会先备份到 `.bak_sanitize/`

## 贡献

每个行业、每个平台都有自己独特的密钥格式和隐私数据。我们不可能全部覆盖，但你可以：

**🔧 发现了没覆盖的敏感信息类型？**
某个云平台的 API Key、某个支付系统的凭证、某个国家的证件号格式——提 [Issue](https://github.com/elliotllliu/agent-hush/issues) 告诉我们，或者直接 [PR](https://github.com/elliotllliu/agent-hush/pulls) 加规则。

**⚡ 想让它多检测一种类型？**
告诉你的 Agent："帮我加一条规则，检测 XXX 格式的密钥"，Agent 会自动帮你配好。

你贡献的每一条规则，都在帮其他开发者避免一次泄露。

## 技术细节

- **语言**：Python 3.6+，零依赖（纯标准库）
- **检测**：220+ 条正则规则，置信度分层
- **来源**：Gitleaks 社区规则 + AI 生态专有规则 + 国标 PII 格式

### 如何区分"高置信度"和"低置信度"？

基于学术研究和工业实践中验证过的方法：

- **格式唯一性判定**（[NDSS 2019 "How Bad Can It Git?"](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/)）— `AKIA` 是 AWS 独有前缀，全球只有 AWS 使用这个格式 →  高置信度。`password=xxx` 任何代码都可能出现 → 低置信度
- **Shannon 信息熵分析** — 真实密钥的字符分布接近随机（高熵），代码变量名是可读单词（低熵）。Agent Hush 通过结构分析识别函数调用、环境变量引用、模板变量等代码模式，自动过滤低熵匹配
- **行业对标** — TruffleHog（Verified / Unverified 分层）和 GitHub Secret Scanning（精确匹配 / 模糊匹配分层）均采用类似方法

结果：**高置信度自动处理不出错，低置信度只提醒不搞坏代码。**

## ⭐ 为什么值得 Star

这个工具保护的是你自己的隐私。我们会一直维护它。

- 各大平台出了新的 Key 格式，我们会第一时间加上检测规则
- 社区提交的新规则，审核后会合入主线，所有人受益
- Agent 生态在变化，我们会持续适配新的工作流和场景

你的每一次 push、每一次 publish，都不应该成为一次隐私泄露。

Star 一下，下次推代码前想起来用它。⭐

## 致谢

密钥检测规则基于 [Gitleaks](https://github.com/gitleaks/gitleaks)（MIT License）的开源规则库，由社区 200+ 贡献者维护。Agent Hush 在此基础上增加了 PII 检测、基础设施信息检测、置信度分层和 Agent 生态集成。

## 开源协议

MIT

---

_🤫 Hush — 让秘密留在该在的地方。_
