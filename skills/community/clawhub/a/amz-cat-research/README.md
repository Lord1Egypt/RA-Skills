# Amazon Category Research Skill

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-orange)

> **中文** | [English](README.en.md)

> 🤖 **OpenClaw Agent Skill** — 把亚马逊类目调研从「一整天」缩短到「十分钟」，自动采集数据、自动生成飞书研报。

***

## 📋 目录

- [💥 一句话：为什么要装？](#-一句话为什么要装)
- [⚡ 一句话安装与使用](#-一句话安装与使用)
- [🤖 Agent 执行规范（Agent 必读）](#-agent-执行规范agent-必读)
- [🎯 调研能力详解](#-调研能力详解)
- [📊 输出报告内容](#-输出报告内容)
- [📁 项目结构](#-项目结构)
- [⚠️ 环境要求](#-环境要求)
- [📄 许可证](#-许可证)

***
## 💥 一句话：为什么要装？

**手工调研一个类目 → 至少一天。装上这个 Skill → 十分钟。**

| 你的痛点                | 安装之后                  |
| ------------------- | --------------------- |
| 卖家精灵 / SIF 数据一条条手动搬 | Agent 自动采集，6 秒一个 ASIN |
| 多平台数据分散，整合到头大       | 多来源数据自动整合到一张表         |
| 手动写研报，格式乱七八糟        | 自动生成飞书文档，专业排版         |
| 花一整天做调研还是漏数据        | 系统化采集，自动校验完整性         |

***

## 🎬 效果演示

> 实际测试使用 **GLM-5.1** 模型，一轮调研（20个ASIN）约 **5 分钟**完成。遇到网络堵塞或大模型延迟时可能稍久。

| 阶段 | 截图 |
| :--- | :--- |
| 🚀 **开始调研** — 传入关键词/ASIN，Agent 启动采集流程 | ![开始](Demo/start.png) |
| ⏳ **采集中** — 逐个 ASIN 采集卖家精灵 + SIF 数据 | ![采集中-1](Demo/progress1.png) |
| ⏳ **采集中** — 数据校验与自动补充 | ![采集中-2](Demo/progress2.png) |
| ✅ **调研完成** — 生成飞书研报，返回文档链接 | ![完成](Demo/end.png) |

***

## ⚡ 一句话安装与使用

### 安装（仅需一次）

直接在对话中告诉 Agent（OpenClaw 用户）：

```text
帮我安装亚马逊类目调研 Skill：clawhub install amz-cat-research
```

Agent 会依次完成：

1. `clawhub install amz-cat-research` → 从 ClawHub 安装 Skill
2. 重启加载 SKILL.md
3. 拉起浏览器 → 执行 `scripts/init.py check` → 检测卖家精灵和 SIF 插件状态
4. 根据检查结果自动引导你安装/登录插件
5. 全部就绪后回复 "可以开始调研"

> ⚠️ 首次安装时 Agent 会自动跑 init.py 做配置检查。**后续使用时 Agent 跳过检查，直接进入采集流程**。

### 使用（天天用）

安装成功后，直接给 Agent 发调研需求：

```text
帮我调研 camping lantern 类目，站点 US
```

或者带 ASIN 列表：

```text
类目：户外露营灯 | 关键词：camping lantern
ASIN：B07VGRJDFY, B08N5WRWNW, B09G9HD6YF | 站点：US
```

Agent 自动采集 → 校验 → 生成飞书云文档 → 回复链接，**全程 10 分钟**。

***

## 🤖 Agent 执行规范（Agent 必读）

> 以下内容仅对 Agent 有效。Agent 收到用户请求后必须严格按此规范执行。

### 1. 安装流程（收到安装请求时）

```
Step 1 — 仓库部署
  ├─ git clone → skill 目录
  ├─ 重启加载 Skill
  └─ 确认 SKILL.md 已加载

Step 2 — 初始化配置检查（init.py）
  ├─ browser navigate → 亚马逊测试商品页（如 /dp/B0CC27124P?th=1）
  ├─ 等待 5 秒
  ├─ python3 scripts/init.py check → 生成检查 JS
  ├─ browser act(kind="evaluate", fn=检查JS) → 获取结果
  ├─ python3 scripts/init.py report '<json>' → 生成报告
  └─ 按分流逻辑回复用户
```

**分流逻辑**：

| 状态 | 含义 | Agent 行为 |
| --- | --- | --- |
| **ready** | 浏览器正常、插件齐全并已登录 | ✅ 回复 ready 话术，提示可以开始调研 |
| **partial** | 插件已安装但未登录 | ⚠️ 回复 partial 话术，引导用户登录 |
| **blocked** | 缺少必要插件 | ❌ 回复 blocked 话术，给出安装步骤 |

**引导话术**：

<details>
<summary>状态 = ready</summary>

```
✅ Amazon Category Research Skill 安装完成！

配置检查全部通过：
- Chrome 浏览器：就绪
- 卖家精灵插件：已安装 ✅ 已登录 ✅
- SIF 插件：已安装 ✅ 已登录 ✅

现在可以直接使用，例如：
"帮我调研 camping lantern 类目，站点 US"
```
</details>

<details>
<summary>状态 = partial（以卖家精灵未登录为例）</summary>

```
⚠️ Skill 已安装，但配置未完全就绪。

检测结果：
- 卖家精灵插件：已安装 ✅ 未登录 ❌
- SIF 插件：已安装 ✅ 已登录 ✅

请在浏览器中登录卖家精灵账号，然后回复"继续"。
你也可以回复"跳过"直接使用（部分字段将缺失）。
```
</details>

<details>
<summary>状态 = blocked（以卖家精灵未安装为例）</summary>

```
❌ Skill 已安装，但缺少必要插件。

检测结果：
- 卖家精灵插件：未安装 ❌

请按以下步骤安装：
1. 访问 https://www.sellersprite.com/ 下载插件
2. 安装到 Chrome 浏览器（OpenClaw profile）
3. 登录卖家精灵账号
4. 回复"继续"重新检查
```
</details>

### 2. 调研流程（收到调研请求时）

与 [SKILL.md](SKILL.md)「执行步骤」章节完全对齐：

```
Step 0 ─ 飞书授权检查（必做）
  ├─ 检查当前对话用户飞书 OAuth 授权状态
  ├─ 不完善 → feishu_oauth_batch_auth 一次性全量授权
  └─ 必须用用户身份创建文档，不能用机器人身份

Step 1 ─ 解析输入 + 确定 ASIN List
  ├─ 场景 A：用户直接给了 ASIN → 校验格式后直接进入 Step 3
  ├─ 场景 B：用户只给关键词 → navigate 搜索结果页 → evaluate 提取 ASIN
  ├─ 场景 C：用户只给类目名 → navigate BSR 页面 → evaluate 提取 ASIN
  └─ ASIN 上限 20 个，确定后告知用户采集范围

Step 2 ─ 确认浏览器可用
  ├─ browser status → 确认 openclaw profile 可用
  ├─ 异常 → browser start 重接管
  └─ 三件套验证：tabs → navigate → snapshot

Step 3 ─ 生成提取 JS
  ├─ python3 scripts/run_all.py generate → 合并后的采集 JS
  └─ JS 是 IIFE 格式 (() => { ... })()

Step 4 ─ 逐个 ASIN 采集
  ├─ browser navigate → 商品详情页 (?th=1)
  ├─ 等待 6 秒（反爬 + 插件注入）
  ├─ browser act(kind="evaluate", fn=采集JS)
  ├─ python3 scripts/parse_raw.py all '<json>' → 解析
  ├─ python3 scripts/validate.py '<解析后JSON>' → 校验
  ├─ 校验报 missing → 进入 Step 5 自愈
  └─ 每 2-3 个 ASIN 暂停 20 秒

Step 5 ─ 自愈流程（条件触发）
  ├─ python3 scripts/healer.py diagnose '<missing_ids>'
  ├─ browser act(kind="evaluate", fn=诊断JS)
  ├─ python3 scripts/healer.py propose '<诊断结果>'
  └─ 确认后 python3 scripts/healer.py apply <field_id> <new_selector>

Step 6 ─ 生成飞书文档
  ├─ 汇总所有 ASIN → 组装 Markdown 内容
  ├─ 保存 MD 源文件到 workspace（权威备份）
  ├─ feishu_create_doc 创建云文档
  └─ 标题格式：亚马逊类目调研｜{关键词}｜{YYYY-MM-DD}

Step 7 ─ 回复用户
  ├─ DM 只发：文档链接 + 200 字以内摘要
  └─ 禁止在 DM 中发送完整报告正文
```

### 3. 浏览器操作约束

| 约束 | 说明 |
| --- | --- |
| **profile** | 必须使用 `profile=openclaw`，不得使用 `profile=user` |
| **端口** | 不得直接连接 9222 / 9229 端口 |
| **web_fetch** | 禁止使用 `web_fetch` 采集亚马逊页面 |
| **执行方式** | JS 通过 `browser act(kind="evaluate", fn=js)` 执行 |
| **脚本启动** | 本地 Python 脚本仅生成 JS / 解析数据，不拉起浏览器 |

### 4. 配置检查清单

| 序号 | 检查项 | 检查方式 | 通过标准 |
| --- | --- | --- | --- |
| 1 | Chrome 浏览器 | `browser navigate` | 页面成功加载 |
| 2 | 卖家精灵插件 | 执行 `init.py check` 生成的 JS | `spirit_installed == true` |
| 3 | 卖家精灵登录 | 执行 `init.py check` 生成的 JS | `spirit_logged_in == true` |
| 4 | SIF 插件 | 执行 `init.py check` 生成的 JS | `sif_installed == true` |
| 5 | SIF 登录 | 执行 `init.py check` 生成的 JS | `sif_logged_in == true` |
| 6 | 飞书配置 | 检查飞书 Token 可用 | 可创建文档 |

### 5. 错误处理

| 异常 | 策略 |
| --- | --- |
| 反爬页 | 等待 15 秒刷新 1 次，仍失败标记反爬 |
| navigate 超时 | 查 tabs 复用，重试 1 次，仍失败标记加载失败 |
| evaluate 返回空 | 检查 targetId，用 snapshot(compact=true) 复核 |
| 字段获取失败 | 记录"未获取/需人工复核" + 来源方法 |
| 插件未加载 | 标记"需卖家精灵/SIF插件" |
| 浏览器控制链异常 | browser start 重启，仍失败 → 停止，输出 partial |
| 选择器失效 | healer.py 自愈 |

***

## 🎯 调研能力详解

### 五大调研维度

| 维度         | 采集内容                                   | 数据来源              |
| ---------- | -------------------------------------- | ----------------- |
| **产品基础信息** | 标题、售价、星级、Review数、品牌、卖家、变体、活动标识         | 亚马逊前台             |
| **卖家精灵数据** | 30天销量（父体/子体）、FBA费、毛利率、上架时间、BSR排名       | 卖家精灵插件            |
| **SIF 数据** | 全部流量词、自然/广告流量构成、SP/SB/SBV/AC广告分析、月流量趋势 | SIF 插件            |
| **竞对综合实力** | 品牌矩阵、店铺数量、卖家归属地、店铺产品线、商标注册情况           | 亚马逊 + Trademarkia |
| **运营策略**   | 日常价/活动价/历史最低价、销量趋势、推新过程分析              | SIF + 卖家精灵        |

### 数据可信度

- ✅ **来源可靠**：数据直接来自卖家精灵和 SIF 官方插件，与插件界面完全一致
- ✅ **实时采集**：从亚马逊前台实时获取，数据新鲜度高
- ✅ **多重校验**：自动检测数据完整性与异常值
- ✅ **可复核**：重要决策数据支持人工二次验证

***

## 📊 输出报告内容

调研完成后，自动生成飞书云文档（含本地 Markdown 备份）：

| 模块            | 内容                                |
| ------------- | --------------------------------- |
| 📋 **输入摘要**   | 类目名称、关键词、ASIN 列表、采集时间             |
| ✅ **数据完整性**   | 已采集 / 需复核 / 未获取字段统计               |
| 📦 **产品基础信息** | ASIN、主图、标题、品牌、售价、星级、Review、变体、BSR |
| 🏢 **竞对综合实力** | 品牌矩阵、店铺数量、卖家归属地评估                 |
| 🔍 **流量架构**   | 自然/广告流量构成、关键词分布、广告趋势              |
| 📈 **运营策略**   | 价格走势、销量趋势、推新过程复盘                  |
| 🎯 **类目评估结论** | 适合打法、上架建议、风险点、上新时间规划、类目延展建议       |

> 💡 飞书文档支持团队协作、评论批注、版本历史，阅读体验远超 Excel。

***

## 📁 项目结构

```
amazon-category-research/
├── scripts/                 # 核心脚本（10个文件）
│   ├── init.py              # Agent 初始化配置检查
│   ├── run_all.py           # 采集编排器
│   ├── selector_registry.py # DOM 选择器注册表
│   ├── gen_product.py       # 产品基础字段 JS 生成器
│   ├── gen_spirit.py        # 卖家精灵字段 JS 生成器
│   ├── gen_sif.py           # SIF 字段 JS 生成器
│   ├── gen_variants.py      # 变体字段 JS 生成器
│   ├── gen_bsr.py           # BSR 排名字段 JS 生成器
│   ├── parse_raw.py         # 插件原始数据解析器
│   ├── validate.py          # 数据校验器
│   └── healer.py            # 自愈诊断
├── references/              # 参考文档
├── SKILL.md                 # OpenClaw Skill 定义
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md                # 中文文档（本文件）
└── README.en.md             # English
```

***

## ⚠️ 环境要求

| 项目     | 要求                        | 说明                 |
| ------ | ------------------------- | ------------------ |
| 框架     | **OpenClaw Framework**    | 必须，提供浏览器控制能力       |
| 浏览器    | Chrome `profile=openclaw` | Agent 自动拉起         |
| 卖家精灵   | 浏览器插件 + 已登录               | 提供销量/FBA费等数据       |
| SIF    | 浏览器插件 + 已登录               | 提供流量词/广告分析数据       |
| 飞书     | 飞书账号                      | 强烈推荐，生成专业云文档       |
| Python | 3.8+                      | 仅用于本地脚本（生成JS/解析数据） |

***

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)。

***

## 🔗 相关链接

- [ClawHub Skill 页面](https://clawhub.ai/yuancheng888/amz-cat-research)
- [OpenClaw Framework](https://github.com/openclaw)
- [卖家精灵](https://www.sellersprite.com/)
- [SIF](https://www.sif.com/)

***

*Built for Amazon Sellers — 把时间还给策略，把数据交给 Agent。*

*免责声明：本项目仅供交流学习使用。*
