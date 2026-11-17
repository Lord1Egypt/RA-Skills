# Douyin Chat Insight（抖音聊天转知识库）

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/GitHub-tars1230%2Fdouyin--chat--insight-black)](https://github.com/tars1230/douyin-chat-insight)

> **把你已经拥有的群聊 / 私聊导出，变成一页可执行的会话情报。**
> 本地优先 · 零 IM 登录 · 不强制云端 Key · 可审计 Agent Skill

**Chat → Insight**：面向社群主理人、知识博主、顾问与内容研究者。
**不是**爬群工具，**不是**「静默导出任意会话」的灰产脚本。

与 [douyin-creator-insight](https://github.com/tars1230/douyin-creator-insight)（公开作品洞察）构成平行组合：

| 维度 | Creator Insight | **Douyin Chat Insight** |
|------|-----------------|-------------------------|
| 输入 | 公开主页 / 作品 | **用户自备**的聊天导出 |
| 问题 | 他在讲什么？ | **粉丝/客户在问什么？** |
| 登录 | 公开页/浏览器（见该项目规则） | **本 skill 内零登录** |

---

## 你能得到什么

一次深挖输出 **四块证据包**（HTML / Markdown / JSON）：

1. **硬事实** — 可核对的陈述 + 原话出处
2. **开放矛盾** — 不同发言之间的张力（启发式，需人审）
3. **需求原话墙** — 用户真实问句，避免「感觉大家都想要」
4. **可执行动作** — 按优先级整理的跟进项

另含：

- **Inventory（概况）**：多会话时先列表，再选编号深挖
- **可选增强端口**：检测到抖音链接/分享卡片时给出说明；**文字主路径永不强制阿里百炼**
- **质量门禁**：无会话编号不深挖；路径脱敏；空导出拒绝装像样报告

> 启发式草稿 ≠ 终审定论。对外使用前请按报告内清单人工过一遍。

---

## 30 秒最短路径

```bash
git clone https://github.com/tars1230/douyin-chat-insight.git
cd douyin-chat-insight

# 一键体检（期望 RESULT: READY）
python3 scripts/doctor.py

# 可选：写入输出目录 / 群主别名（不问 Key、不登 IM）
python3 scripts/setup.py

# 1) 先看概况
python3 scripts/run.py -i tests/fixtures/sample_group.jsonl

# 2) 再深挖指定会话
python3 scripts/run.py -i tests/fixtures/sample_group.jsonl --conv 1

# 3) 打开报告（macOS）
open output/douyin-chat-insight/latest.html
```

用你自己的导出：

```bash
python3 scripts/run.py -i /path/to/export.jsonl
python3 scripts/run.py -i /path/to/export.jsonl --conv 1 --owner-alias '群主昵称'
```

支持：**ChatLab JSONL**、简单 **JSON 数组**、纯文本「昵称: 内容」、含多文件的**目录**。
如何自备导出（可选第三方，**非本包依赖**）：见 [`references/how-to-get-exports.md`](references/how-to-get-exports.md)。

---

## 作为 Agent Skill 安装

### 本机共享（Hermes / Codex / Claude 等）

```bash
mkdir -p ~/.shared/skills
ln -sfn "$(pwd)" ~/.shared/skills/douyin-chat-insight
# 若已装 publish-agent-skill：
python3 ~/.shared/skills/publish-agent-skill/scripts/link_shared_skill.py douyin-chat-insight --apply
```

对话示例：

> 用 douyin-chat-insight 分析这个导出：`/path/to/export.jsonl`
> 先 inventory，不要直接深挖。

### ClawHub（Agent 市场）

当前公开版：`douyin-chat-insight@0.1.5`（Moderation CLEAN，本机 `install` + `doctor` 已 READY）。

```bash
clawhub install douyin-chat-insight
# 装完进 skill 目录：python3 scripts/doctor.py  # 期望 READY
```

**延迟说明（正常，不是故障）：** `publish` 成功后，`latest` / 审核 / `install` 解析常有 **数分钟～数十分钟** 延迟。期间可能仍见旧版或 `pending.publication`。等索引跟上后**单次**重试即可，**不要连续 bump 版本硬刷**。

源码兜底：

```bash
git clone https://github.com/tars1230/douyin-chat-insight.git
cd douyin-chat-insight && python3 scripts/doctor.py
```

公开页：https://clawhub.ai/tars1230/douyin-chat-insight

### Gitee 镜像

GitHub 为源码真相源；Gitee 镜像配置完成后可作为国内下载入口（仓库名与 GitHub 对齐）。

---

## 要不要阿里百炼 / ASR？

| 场景 | 需要吗 |
|------|--------|
| 默认：分析文字聊天 | **不需要** |
| 会话里出现抖音链接、分享卡片 | **仍不需要**（识别 + 计数 + 文字四块） |
| 你**主动**要求对某条链接做口播转写 | **可选** — 见 [`references/optional-douyin-link-asr.md`](references/optional-douyin-link-asr.md) |

设计原则：

1. 核心路径 **零 Key**；`setup.py` **永不索要** AppKey
2. **预留端口**：仅探测 `DASHSCOPE_API_KEY` / `BAILIAN_API_KEY` 是否存在（状态展示）
3. 需要链接分析时 → **配置/路由指导**，不在 `run.py` 内静默扣费转写

---

## CLI 速查

```bash
python3 scripts/run.py --version
python3 scripts/run.py -i <导出>                  # 默认 inventory
python3 scripts/run.py -i <导出> --conv 1         # 深挖
python3 scripts/run.py -i <导出> --conv 1 --person '某人'
python3 scripts/run.py -i <导出> --conv 1 --json  # 机器可读
python3 scripts/run.py -i <导出> -o ./my-out --formats html,md,json
python3 scripts/setup.py --check --json
python3 scripts/doctor.py
python3 scripts/search.py "关键词"
```

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 2 | 可预期业务失败（缺文件、未选会话、门禁未过等），stderr 为中文说明 |

---

## 项目结构

```
douyin-chat-insight/
├── SKILL.md                 # Agent 触发与状态机
├── README.md                # 本文件
├── LICENSE                  # MIT
├── requirements.txt         # 核心路径仅标准库
├── scripts/
│   ├── run.py               # 主入口
│   ├── doctor.py            # 发布/安装体检
│   ├── setup.py             # 可选配置
│   ├── load_export.py       # 多格式加载
│   ├── inventory.py         # 概况
│   ├── analyze.py           # 四块分析 + 可选增强元数据
│   ├── report_builder.py    # HTML/MD/JSON
│   └── quality_gate.py      # 门禁
├── references/              # 格式、边界、导出、可选 ASR
├── docs/                    # 安装、GTM、清单、样例
└── tests/                   # unittest + fixtures
```

---

## 安全与隐私

- 默认只读你**显式传入**的本地路径
- 不要求 cookie / sessionid / 密码
- 报告中的来源路径会脱敏，避免泄漏本机目录结构
- 示例与 `docs/examples` 使用脱敏 fixture
- 详见 [`SECURITY.md`](SECURITY.md)

**请勿**把完整真实私聊上传到公共 Issue 或不明「代分析」网站。

---

## 开发与测试

```bash
python3 scripts/doctor.py
python3 -m unittest discover -s tests -v
```

运行时核心路径 **仅 Python 标准库**（见 `requirements.txt`）。

版本与变更：[`CHANGELOG.md`](CHANGELOG.md) · 当前 **v0.1.5**

---

## 定位与商业（摘要）

开源核心永久免费（MIT）。可选增值在服务层：脱敏代分析、社群诊断工作坊、与 Creator Insight 打包的「账号体检」——**不**售卖任意群爬取 API。
完整叙事见 [`docs/GTM.md`](docs/GTM.md)。

---

## 常见问题

**Q: 没有导出文件能分析吗？**
A: 不能。请先自备 JSONL/JSON/文本。可选导出途径见 `references/how-to-get-exports.md`，那些工具**不是**本 skill 依赖。

**Q: 能帮我登录抖音/微信拉群吗？**
A: 不能。本仓库分析层与采集层严格分离。

**Q: 报告会不会把猜的当成事实？**
A: 启发式会标证据；`meta` 与文案明确「草稿需终审」。门禁在空结果时失败而非瞎编。

**Q: 和 douyin-creator-insight 冲突吗？**
A: 不冲突。一个看主页作品，一个看会话记录；可同机安装、输出目录分离。

---

## 许可证

[MIT](LICENSE) © 2026 douyin-chat-insight contributors

问题与改进：[https://github.com/tars1230/douyin-chat-insight/issues](https://github.com/tars1230/douyin-chat-insight/issues)
