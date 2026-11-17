<div align="center">

# anti-ai-foolish

**反AI傻味 · 去AI终检**

🇨🇳 **简体中文** | 🇬🇧 [English](README.en.md)

</div>

---

发文前的AI味守门员：它回答一个问题——**这篇稿子能不能发，还是读起来仍然像AI写的？**

判定依据全部来自实测：1,108 条规则在 **52 个带真实朱雀检测标签的片段**上逐条做过 A/B 测试（95% 置信区间）。没通过检验的规则如实标注，不冒充有效。

## 快速开始

```bash
git clone https://github.com/forrestneo/anti-ai-foolish.git
cd anti-ai-foolish

# 一键终检：六硬门 + Z分 + 人味弹药 → 可发 / 改后复检 / 停下手术
python scripts/preflight.py your_article.md
```

输出示例：

```
# Preflight — your_article.md
正文 2689 字 | Z分 0（AI确认1 − 人味确认1）
  ✓ 冒号=0: 0处
  ✓ 破折号=0: 0处
  ...
门通过 7/7 → ✅ 可发（朱雀切块复测后发布）
```

## 安装

标准 Agent Skill 格式，适用于 Claude Code / Codex / ZCode 等任何支持 Agent Skills 的工具。把本仓库 clone 或下载后，整个目录复制进你的技能目录：

```bash
# ZCode
cp -r anti-ai-foolish ~/.zcode/skills/anti-ai-foolish
# Claude Code
cp -r anti-ai-foolish ~/.claude/skills/anti-ai-foolish
```

依赖：Python 3.8+，纯标准库，零第三方依赖，离线运行，不上传任何文本。

## 工作原理

四步工作流（详见 `SKILL.md`）：

```
① 机械筛          python scripts/preflight.py → 六硬门 + Z分
② 人工判据        经历之我vs姿态之我 / 人是不是主体 / 论证对称排比
③ 七刀手术        冒号→概念引用腔→数据罗列→金句对称→结构→词表→换骨架
④ 复检+平台实测   重跑preflight至✅；朱雀按1000-2000字切块贴，目标≤0.40
```

**三条被实测推翻的流行常识**（n=52，95%CI）：

| 流行说法 | 实测真相 |
|---|---|
| 排比是AI味，要拆 | 口语重复排比在人写文本密度更高（r=-0.37）；只有论证对称金句（"可以X却不能Y"×3）有害 |
| 加口语词降分 | 不护体（r=-0.25）；装出来的口语出现在0.99的段落里 |
| 删心理描写 | 过时（r=-0.24），AI已学会不写 |

**确认的真信号**：冒号（r=+0.43，最强单项）、概念引用腔（给术语加引号，AI是人的5.5倍）、疑问句密度、破折号。

**核心发现——骨架-燃料定律**：同一作者、同一母题，亲历做骨架 → 朱雀 **0.09**；概念做骨架、真事当燃料 → **0.75~0.995**。决定分数的不是谁的口吻用什么词，是骨架是"谁在做什么"还是"一个概念在推演"。

## 实战成绩

- 未手术AI稿（朱雀实测0.91 / 0.93）→ preflight 正确拦截 ✓
- 手术后稿件 → 7/7门放行，朱雀复测主体进入**人工特征区间**（AIGC 0.14）✓
- 13篇存量稿全流程手术后全部通过机械门

## 项目结构

```
anti-ai-foolish/
├── SKILL.md            # skill入口：工作流 + 铁律 + 边界
├── scripts/
│   ├── preflight.py    # 发文终检（六硬门+Z分+判定）
│   ├── scanner.py      # 规则引擎（1108规则→分层报告+修法）
│   └── abtest.py       # A/B重验（语料更新即全量重估）
├── rules/              # 13个规则分库（每条带status/evidence/fix/exempt）
├── validation/         # 52片段朱雀标签语料 + 验证结果
└── references/         # 方法论、证据链、评测报告、路线图
```

每条规则五个状态之一：`confirmed`（过CI）/ `reversed`（方向反转）/ `directional` / `no_signal` / `insufficient`。

## 诚实声明

- 召回97%、特异53%——它是**发布质量门**，宁可误拦不放过；Z<0不等于"证明是人写的"
- 机械上限约0.8相关，剩余方差靠人工判据三问（SKILL.md第二步）
- 语料文体为中文自媒体评论；换文体请把新语料放进 `validation/corpus/` 重跑 `scripts/abtest.py`
- 只做语言层优化，不做事实伪造——所有修法以不改变事实与原意为前提

## ⚠️ fork/搬运者注意

`validation/corpus/` 含检测报告原文片段。公开你自己的副本前，确认对语料提供者无隐私影响；删除该目录不影响工具运行。

## License

MIT
