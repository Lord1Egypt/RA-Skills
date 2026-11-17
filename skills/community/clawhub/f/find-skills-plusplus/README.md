# Find Skills++ 🔍⚡

> **English TL;DR** — Find Skills++ is a community supercharged fork of `find-skills`: an all-in-one **skill security-curation · install-gate · ecosystem-governance** toolkit (discovery included) for AI agents. 20 subcommands, **zero dependencies** (pure Python stdlib), 140 passing tests. Its edge over the originals: ① AST-level **pre-install security scan** (4-tier EXTREME/HIGH/MEDIUM/LOW risk + file/network/command permission inventory, EXTREME blocks install); ② true **offline catalog** via `sync`; ③ **reference-integrity check** (flags skills referencing non-existent tools); ④ 0-100 **quality rating**; ⑤ full **lifecycle** management (update / uninstall-to-trash / clean-dupes). MIT, derived from `guipi888/find-skills`.

### 安装前安全闸门 · 装后生态治理 · 智能发现

> **技能生态的「安全审查 → 安装闸门 → 全生命周期治理」全能工具，智能发现作为顺带能力。**
> **52 项增强** · AST 级安全闸门 · 四级风险 · 真·离线全能 · 质量评级 · 全生命周期
>
> 派生自 [`guipi888/find-skills`](https://github.com/guipi888/find-skills)（MIT，99.4 万下载），
> 源头为 [`vercel-labs/skills`](https://github.com/vercel-labs/skills) 的 `find-skills`。
> **带完整署名的社区超级增强版，非官方替代品。**

[![CI](https://github.com/cdhewei/find-skills-plusplus/actions/workflows/ci.yml/badge.svg)](https://github.com/cdhewei/find-skills-plusplus/actions)
[![License: MIT-0](https://img.shields.io/badge/license-MIT--0-blue.svg)](#许可证与署名)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB.svg)](#)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-140%20passing-brightgreen.svg)](#测试)
[![Updated](https://img.shields.io/badge/last%20updated-2026--09--21-brightgreen.svg)](#)

---

## 30 秒了解它

装 AI 技能 = 运行别人的代码。但生态里**没有工具真正帮你审查过**。

`find-skills++` 补上这一环：

| 别人帮你「找技能」 | 它帮你「敢装、会管」 |
|---|---|
| 推荐一堆，你不知道哪个安全 | **AST 语法树级安检** + 四级风险 + 权限清单 |
| 离线就残废 | **在线目录同步到本地**，断网照样搜 |
| 好看的技能可能引用了不存在的工具 | **引用完整性校验**，假优直接被打下来 |
| 装了就没法管 | **update / uninstall（进回收站）/ clean-dupes** |

一句话：**如果你只想找技能，原版够用；如果你在意装得安全、管得明白，用 find-skills++。**

```bash
python findskills.py elevator   # 30 秒电梯演讲
python findskills.py demo       # 端到端演示（5 场景，可录屏）
python findskills.py promote    # 一键生成 5000+ 字推广素材
```

## 竞品对比

| 能力 | 官方 find-skills | guipi888/find-skills<br>(99.4万下载) | skill-vetter<br>(31万) | **find-skills++** |
|---|---|---|---|---|
| 多源联合搜索 | 部分 | ✅ 六层 | — | ✅ 跨源合并去重 |
| 安装前安全扫描 | 建议清单 | ❌ 无 | ✅ 纯 prompt 清单 | ✅ **AST 级可执行闸门** |
| 风险分级 | 无 | 无 | 定性描述 | ✅ **四级 + 权限清单** |
| 离线可用 | 弱 | 弱 | — | ✅ **目录同步型离线全能** |
| 质量评级 | 无 | 推荐理由 | 无 | ✅ **七维 0-100** |
| 引用真实性校验 | 无 | 无 | 无 | ✅ **独有** |
| 更新 / 卸载 | 无 | 无 | — | ✅ **回收站可还原** |
| 重复安装治理 | 无 | 无 | 无 | ✅ **自动去重** |
| 可执行工具 + 测试 | 无 | 无 | 无 | ✅ **CLI + pytest** |
| 自我推广素材生成 | 无 | 无 | 无 | ✅ **promote 引擎** |

---

## 为什么是 ++（而不是官方 find-skills）

上游 `find-skills` 自 2026-03 起未再迭代。它把**外部 SkillHub 当首选源**、**安装前无安全闸门**、**不去重不管更新**、**客户端判定 macOS 专属**、**只信 API 返回的分**。在真实 Windows / 中文 / 多源环境里，这些全是坑。

`find-skills++` 在其流程之上做了 **52 项实质增强**（详见文末清单），并参考了 [`sandbaseai/workbuddy-skill`](https://github.com/sandbaseai/workbuddy-skill) 的「真实脚本化安全审查」思路（本仓库 `scripts/security_scan.py` 为独立自研、零依赖实现，非复制）。

**对标生态头部技能看齐**：`self-improving-agent`（121 万下载，生态第一）、`agent-browser`（82 万）、`skill-vetter`（31 万，同类头部）。对齐项包括 frontmatter 规范（`version` + `metadata`）、渐进式披露 `references/` 拆分、四级风险分类与权限清单、市场标准卡 `market-card.md`（含 Known Risks & Mitigations）。

**相对成熟竞品 `sandbaseai/workbuddy-skill` 的差异化定位**：我们不强求"索引多少万技能"（那是它的护城河），而是主打 **离线可信 + 安全可控 + 好挑好选**——内置离线注册表、真实的预安装安全扫描、综合排序与来源信誉门槛。

## 特性

- 🛡️ **安装前真实安全扫描（正则 + AST 双引擎）** — 零依赖 `security_scan.py`，正则分诊 + `ast`/`shlex` 语法树级检测 `os.system`/`subprocess(shell=True)`/`eval`/`exec`/`pickle.loads`/动态拼接 `rm -rf`/`base64+exec` 组合/`curl|sh`，P0 直接阻断，带误报控制
- 🔀 **跨源合并去重** — 原生市场 + SkillHub + ClawHub + 本地缓存合并成统一候选表，取全网最优版本
- 🏅 **来源信誉门槛** — 官方源加权、低信誉（未知作者且低星标/低安装）降权标记
- 💾 **离线兜底 + 离线注册表 + 在线缓存** — API 挂了也能推荐；内置 `registry.json` 精选可信技能，`sync` 再把 SkillHub 全量目录拉到本地缓存（TTL 24h），真·离线全能
- 🔌 **已连连接器感知** — 结合当前已连连接器（如金融/邮件类）加权推荐
- 📊 **中文结构化卡片 + 综合排序** — 匹配/热度/时效/信誉四维加权，长期未维护自动标记
- 🔄 **全生命周期（安装/更新/卸载/清理）** — `install`/`update`/`uninstall`（进回收站可还原）/`clean-dupes`（保留最新、其余进回收站）/ 安装历史可追溯
- 🪟 **跨平台** — Windows / Linux / macOS 健壮判定，不依赖 macOS 专属变量
🤝 **多 agent 支持** — 自动识别 WorkBuddy / CodeBuddy / OpenClaw / Claude Code 技能目录；`list`/`audit`/`clean-dupes` 默认也扫描 OpenClaw、Claude Code 已装技能，实现跨 agent 治理；安装用 `--target openclaw|claude` 显式指定
- 🧠 **语义匹配** — 内置意图同义词词典，自然语言需求（如"处理pdf"）映射到技能意图，离线、零依赖、不依赖 embedding API
- ⭐ **技能质量评级（含引用完整性）** — 七维（frontmatter/示例/参考/文档长度/新鲜度/可操作性/引用完整性）给出 0-100 分，**引用的本地文件或跨技能若不存在则大幅降级**，专治假优
- 🔍 **冗余检测** — 区分「重复安装（同名多份）」与「功能冗余（不同名但相似）」，中文去停用+bigram 降误报
- 🧹 **瘦身建议** — 基于重复安装+功能冗余+质量偏弱，给出只读的保留/清理建议（诚实标注非真实使用追踪）
- 🗂️ **discover 榜单 + 跨源版本仲裁** — `discover [--new|--trending]` 新上架/热门榜单；三源版本不一致自动选最高版并标出落后源
- 🚦 **四级风险分类** — 对标 `skill-vetter`：按「执行块 vs 文档提及」归并为 EXTREME / HIGH / MEDIUM / LOW，每级映射明确动作（禁止安装 / 需人工批准 / 完整审查 / 可安装）
- 📋 **权限清单** — 自动提取技能实际需要的**文件 / 网络 / 命令**三类权限，回答"是否超出声明目的的最小集"
- 🛡️ **17 项红旗覆盖** — 除常规混淆执行外，补齐 `~/.ssh`/`~/.aws`/`id_rsa` 凭据目录、`MEMORY.md`/`IDENTITY.md` 等 Agent 身份文件、裸 IP 直连、浏览器 cookie/session、`chmod 777`、静默装包、系统目录写入
- 🪜 **5 级信任层级** — 官方源 → 知名源 → 已知作者 → 未知来源 → 索取凭据（一律人工批准）
- 🔒 **隐私** — 不收集、不上传、不外传任何本地数据；扫描全本地静态分析
- 🚦 **`outdated` 版本巡检** — 比对已装版本与注册表/缓存最新版，一眼看出哪些技能该更新（生命周期闭环）
- 🩺 **`doctor` 环境体检** — 自动诊断 frontmatter 错、质量分低、重复安装、缺依赖连接器、硬编码路径/密钥泄露，非运维用户也能自查
- 🚪 **`publish` 发布就绪校验（上架闸门）** — 发布前自检市场门槛（frontmatter/LICENSE/market-card/占位符/硬编码）+ 端到端冒烟自证，任一不过即 FAIL

## 安装

```bash
# 方式一：直接放到用户级技能目录（推荐，agent 可直接调用）
git clone https://github.com/cdhewei/find-skills-plusplus.git
cp -r find-skills-plusplus ~/.workbuddy/skills/find-skills-plusplus

# 方式二：SkillHub / ClawHub（发布后）
# 在对应市场搜索 find-skills++ 一键安装

# 多 agent：安装到其它 agent（默认自动识别当前 agent，也可显式指定）
python findskills.py install <slug> --target openclaw   # 装到 OpenClaw
python findskills.py install <slug> --target claude     # 装到 Claude Code
# 注：list / audit / clean-dupes 默认也扫描 OpenClaw、Claude Code 已装技能，实现跨 agent 治理
```

## 使用

在对话里说"帮我找个能做 X 的技能"即可触发。流程：

1. 本地优先搜索（你已装的，秒回防重复）
2. 原生市场搜索（首选，复用宿主鉴权）
3. 社区源搜索（SkillHub / ClawHub）并与原生结果**合并去重**
4. 安全审查闸门（社区源必过）
5. 中文卡片综合排序呈现 → 等你确认装哪些

（附带的 `findskills.py` 已内置语义匹配、质量评级、冗余检测等智能子命令，详见下方「命令行工具」。）

## 开发者

```bash
# 跑安全扫描器自测
python scripts/security_scan.py --path . --lang zh-CN

# 跑测试
python -m pytest tests/ -q
```

> **关于自扫结果**：扫描器是「第三方技能审计工具」。直接扫描本仓库（`--path .`）会如实返回 **HIGH / 需人工批准**——因为本工具自身使用 `subprocess` 且文档化了大量攻击模式（正是它要检测的）。这是**预期且诚实的**，不代表本工具可疑；它的价值在于审计**第三方**技能：`scripts/smoke.py` 用 5 组恶意样本验证必拦 EXTREME、干净样本必判 LOW。

贡献方式见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 命令行工具

附带零依赖 `findskills.py`，让发现/审查/安装脱离 agent 也能跑、可演示、可测试：

```bash
python findskills.py search <query> [--offline] [--limit N]   # 搜索（本地+注册表+缓存+SkillHub），语义匹配+合并去重+综合排序
python findskills.py scan <path>                            # 安全静态扫描（正则+AST，P0/P1/P2，退出码 2/1/0）
python findskills.py install <slug> [--yes] [--force]       # 下载社区技能→AST安全扫描→解压（P0 阻断）
python findskills.py update <slug> [--yes] [--force]        # 重下最新并覆盖已装（同样过安全网关）
python findskills.py uninstall <slug>                       # 卸载本地技能（进回收站，可还原）
python findskills.py clean-dupes                            # 清理重复安装（保留最新一份，其余进回收站）
python findskills.py sync [--limit N]                       # 拉取 SkillHub 全量目录到本地缓存（离线全能）
python findskills.py list | audit                           # 列出/审计本地已装
python findskills.py registry validate|show|add             # 离线注册表管理
python findskills.py quality <slug> [--path DIR]            # 评估单个技能质量（0-100，七维含引用完整性）
python findskills.py redundancy                             # 检测本地已装重复安装与功能冗余
python findskills.py prune                                  # 基于静态信号给出瘦身建议（只读）
python findskills.py discover [--new|--trending]             # 新上架/热门榜单（含跨源版本仲裁）
python findskills.py outdated                              # 巡检已装技能是否有新版本可更新
python findskills.py doctor                               # 环境体检（frontmatter/质量/重复安装/连接器依赖/硬编码路径）
python findskills.py publish [--path DIR] [--no-smoke] [--strict]  # 发布就绪校验（上架闸门，含冒烟自证）
```

## 隐私

本技能**不收集、不上传、不外传**任何本地数据：

- 搜索请求仅发往用户主动指定的注册中心（SkillHub / ClawHub / 原生市场）。
- 安装历史、缓存、注册表均**只写在本地**（`~/.workbuddy/` 下）。
- 安全扫描为**全本地静态分析**，不上传被扫描技能的任何内容。
- 不记录密钥/令牌/密码；扫描器识别到凭据索取时只作**风险提示**。
- `sync` 仅在用户显式执行时联网，`--offline` 可完全禁用网络。

## 已知限制（诚实标注）

- `prune` / `redundancy` 基于**静态信号**，不是真实使用追踪。
- 语义匹配为**同义词词典召回**，非 embedding 语义向量。
- 安全扫描为**静态分析**：无法覆盖运行时行为、动态加载、条件触发的恶意逻辑。
  **扫描干净 ≠ 安全保证**，须结合人工审阅。
- `registry.json` 为手工精选（15 条），`downloads: null` 表示未核实，**不编造数据**；
  全量目录靠 `sync` 拉取。

## 项目结构

```
find-skills-plusplus/
├── SKILL.md                  # 核心指令（精炼，渐进式披露）
├── market-card.md             # 市场标准卡（License / Known Risks & Mitigations）
├── README.md                 # 本文件（含竞品对比与 30 秒介绍）
├── CHANGELOG.md              # 演进记录（1.0 → 5.3.0）
├── findskills.py             # 零依赖 CLI（20 个子命令，含 promote/demo/elevator）
├── registry.json             # 离线可信注册表（手工精选）
├── references/               # 渐进式披露专题文档
│   ├── security.md           #   四级风险 / 17 项红旗 / 权限清单 / 信任层级
│   ├── cli.md                #   CLI 完整用法
│   ├── ranking.md            #   排序公式 / 信誉 / 语义匹配
│   ├── enhancements.md       #   52 项优化清单
│   └── roadmap.md            #   Roadmap 与已知限制
├── scripts/security_scan.py  # 零依赖安全扫描器（正则 + AST）
├── scripts/smoke.py          # 端到端冒烟自证（真跑子命令 + 检测力 + 文档一致性）
└── tests/                    # pytest 测试套件（140 项）
```

### 自证：别听我说，跑一遍

```bash
python scripts/smoke.py
```

真跑 20 个子命令与 7 组参数变体，用 5 组恶意样本验证安全闸门（须全判 EXTREME）、
用干净样本验证不误报（须判 LOW），并校验文档里的每个数字与实现一致。任一项不过即 FAIL。

## Roadmap

**Phase 1（骨架，可演示 ✅）**
- [x] 52 项增强 + 真实安全扫描脚本 `scripts/security_scan.py`
- [x] 零依赖 `findskills` CLI（search / scan / install / list / audit / registry 子命令）
- [x] 离线可信注册表 `registry.json`（离线优先，用信誉分代替编造下载量）
- [x] pytest 测试套件（扫描器/排序/去重/注册表/CLI，CI 自动跑）

**Phase 2（智能层，已完成 ✅）**
- [x] 语义匹配（轻量离线意图词典，不依赖 embedding）
- [x] 技能质量评级（七维含引用完整性 0-100，search 直接标注）
- [x] 冗余检测（区分重复安装 vs 功能冗余，中文去停用+bigram）
- [x] 瘦身建议（只读，诚实标注非真实使用追踪）

**Phase 3（硬核安全 + 全生命周期，已完成 ✅）**
- [x] AST 级安全分析（替换正则浅扫描，`ast`/`shlex` 语法树级检测混淆调用）
- [x] 在线目录 `sync` + 本地缓存（真·离线全能，TTL 24h）
- [x] 环境感知引用校验（质量评级新增引用完整性维度，专治假优）
- [x] `update` / `uninstall`（进回收站可还原） / `clean-dupes` 子命令
- [x] `discover` 榜单（新上架/热门）+ 跨源版本仲裁
- [x] 测试套件扩展到 140 项（覆盖 AST/缓存/引用/生命周期/发现/凭据定级/自评级/日期混排）

**Phase 4（对标头部看齐，已完成 ✅）**
- [x] 红旗补齐 8 项（对标 `skill-vetter`：凭据目录 / Agent 身份文件 / 裸 IP / cookie / chmod 777 / 静默装包 / 混淆转义 / 系统目录写入）
- [x] 四级风险分类（EXTREME/HIGH/MEDIUM/LOW + 动作映射）
- [x] 权限清单（文件 / 网络 / 命令）
- [x] 5 级信任层级
- [x] frontmatter 标准化（`version` + `metadata`）+ 渐进式披露 `references/` 拆分
- [x] 市场标准卡 `market-card.md` + 隐私条款

**Phase 5（自我营销 + 合规，已完成 ✅）**
- [x] **`promote` 自我营销引擎**：一键生成 5000+ 字推广素材（简介/banner/卖点/对比表/社交文案/发布清单）
- [x] **`demo` 可录屏演示**：5 场景端到端，带耗时与退出码，可直接录 GIF
- [x] **`elevator` 30 秒电梯演讲**：对话中可直接引用的差异化自述
- [x] 市场 SEO 元数据 + 触发文案重写（`xiaping_*` / `displayName` / 全覆盖触发词）
- [x] `CHANGELOG.md` 演进记录 + 作者品牌区
- [x] **许可证结案**：上游确认为 MIT（guipi888/find-skills，Copyright 2026 Kyle），派生合规前提成立

**Phase 6（兑现承诺：实测修真缺陷，已完成 ✅）**
- [x] **凭据窃取定级修复**：AST 判定字符串是否被危险 sink 真正使用，偷读 `~/.ssh/id_rsa` 从 MEDIUM 修正为 **EXTREME**
- [x] `discover --new` 崩溃修复（日期字符串 / 毫秒时间戳混排）
- [x] `quality` 支持自检（`self` / slug / 别名）
- [x] **`scripts/smoke.py` 端到端冒烟自证**：真跑子命令 + 检测力 + 文档数字一致性，接入 CI
- [x] 回归测试 123 → 140 项，文档与实现数字全面对齐

**Phase 7（生命周期闭环 + 发布闸门，已完成 ✅）**
- [x] **`outdated` 版本巡检**：比对已装版本与注册表/缓存，输出可更新清单
- [x] **`doctor` 环境体检**：frontmatter/质量/重复安装/连接器依赖/硬编码路径密钥，逐技能排查
- [x] **`publish` 发布就绪校验（上架闸门）**：查市场门槛 + 跑 `scripts/smoke.py` 端到端冒烟自证

**Phase 8（可选演进）**
- [ ] 已装技能使用追踪：接入宿主使用信号，判断哪些真正被用过
- [ ] 语义匹配升级：若宿主提供 embedding API，升级为真实语义向量召回
- [ ] 生态体检报告：一键生成「本地技能生态体检」Markdown 报告
- [ ] 多源许可证合规扫描：标出与项目许可冲突的已装技能

## 许可证与署名（✅ 已核实）

- **最近的派生上游**：[`guipi888/find-skills`](https://github.com/guipi888/find-skills) —
  经核实为 **MIT License, Copyright (c) 2026 Kyle**（SkillHub 99.4 万下载）。
  **派生、修改、再分发、署名发布均被明确允许。**
- 源头：[`vercel-labs/skills`](https://github.com/vercel-labs/skills) 的 `find-skills`（Vercel 官方）。
- 思路参考：[`sandbaseai/workbuddy-skill`](https://github.com/sandbaseai/workbuddy-skill)；
  红旗清单对标 `skill-vetter`（31 万下载）。

本仓库新增内容（`scripts/security_scan.py`、`findskills.py`、++ 增强、文档）以 **MIT-0** 提供，
扫描器与 CLI 均为独立自研、纯标准库、零依赖实现。**保留上游 MIT 许可与署名**，
明确标注"基于 find-skills 修改"，不伪装成官方替代品。详见 [LICENSE](./LICENSE)。

## 作者

**何巍** · find-skills++ 新增内容作者

> 完整演进记录见 [CHANGELOG.md](./CHANGELOG.md)（1.0 → 5.3.0）

---

*find-skills++ —— 技能生态的「发现 → 安全策展 → 安装 → 治理」全能工具。*
