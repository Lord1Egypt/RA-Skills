# case-writing：商学院教学案例写作总纲

一套从灵感（一句话想法）到成稿（规范教学案例 + Teaching Note）的完整方法论技能，融合 HBS 的「决策者故事」、Wharton 的「数据分析密度」与 Ivey/RSM 的国际共识。

## 功能

- **五段流水线**：灵感捕捉与选题验证 → 案例简报（10 问）→ 骨架搭建 → 正文起草 → 去 AI 味与交付
- **HBS 标准结构模板**：Title → Opening → Background → Development → Decision Point → Exhibits
- **写作铁律十条**：一个案例一个决策焦点、教学笔记先行、作者隐身、信息不完整是刻意设计等
- **中英双语写作规范**：两版事实数字一致，各自语言习惯，非机械翻译
- **humanizer 集成**：24 类 AI 味模式清单 + 案例写作特有重灾区（排比三连、空洞升华、AI 高频词）
- **质量检查清单**：结构、文体、内容、双语、合规五个维度自检

## 使用方式

将本技能放入 agent 工作区的 `skills/case-writing/` 目录，或在 OpenClaw 中安装后，向 agent 给出一个灵感（如「某公司做下沉市场失败了」），即可产出：

1. 选题验证卡（决策焦点测试句 + 三性验证 + 查重提示）
2. 案例简报（10 问）+ 教学笔记草案
3. 案例正文（第三人称、过去时、数据融入叙事）+ Exhibits
4. 配套 Teaching Note

## 目录结构

```
case-writing/
├── SKILL.md                    # 技能总纲
├── templates/
│   └── case-outline.md         # 带 Exhibit 编号的章节大纲模板
├── README.md
└── LICENSE
```

## 配套技能（可按需自建或检索社区）

teaching-note（教学笔记）、case-method-facilitation（案例教学法）、case-publishing（投稿发表）、case-analysis-writing（学生案例分析作业）、humanizer（去 AI 味）。

## 许可

MIT License。作者：妙笔先生（Miaobi）。

## 免责声明

本技能为方法论框架，不含任何真实公司数据；使用者在写作真实案例时，须自行核实事实、脱敏敏感信息并取得必要授权。
