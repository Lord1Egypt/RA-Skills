# 可研报告撰写引擎 · 技能包使用说明

> 本包是给 AI 智能体（Claude/GPT/豆包/千问/DeepSeek/Hermes 等）使用的**技能（Skill）**，
> 让任何智能体都能写出"专业机构级"的可行性研究报告。源自 300 亿海洋产业集群大单实战。

## 〇、技能形态与路线图

**本技能 = 可研报告撰写的「Word 完整版 + Excel 测算套表」版**（对外交付形态：Word 报告全稿 + Excel 测算套表 + 编制说明，三件套）。

同一业务族按**交付形态**规划为系列技能：

| 技能 | 交付形态 | 状态 |
|------|---------|------|
| **feasibility-report-engine（本包）** | Word 完整版 + Excel 测算套表 | ✅ 已沉淀（v1.6）|
| PPT 版可研演示稿 Skill | PPT（路演/汇报演示稿，面向资方/评审会）| 🚧 规划中 |
| PDF 版可研报告 Skill | PDF（正式印刷/报批版）| ✅ 已含转换配方（见 SKILL.md 4.2）|

PPT / PDF 版沿用本包的尽调、测算、去 AI 痕方法论，只换排版引擎与交付物形态。

## 一、包结构

```
feasibility-report-engine/
├── SKILL.md                 # ★ 主文件：完整作战手册（工作流/规范/陷阱/验证清单），喂给智能体
├── scripts/                 # ★ 一键脚本（排版/测算/编制说明/视觉验收/报告QA/流水线自检）
│   ├── docx_polish.py       #   排版净化：AI痕迹清除+样式重建+表格美化（最常用）
│   ├── face_docx.py         #   加门面：封面/签署页/自动目录/页眉页码
│   ├── gen_report_docx.py   #   从零起骨架（封面+样式体系）
│   ├── gen_model_xlsx_v2.py #   投资测算套表（公式全搭好，蓝=输入）
│   ├── gen_model_xlsx.py    #   测算套表简版
│   ├── gen_shuoming.py      #   编制说明与资料需求清单（1-2页）
│   ├── vision_check.py      #   视觉验收：docx渲染成图→多模型交叉审查
│   ├── report_qa.py         #   ★ 长文档 QA：缓存/正则查改/断言验收/规模体检（纯标准库）
│   └── pipeline_check.py    #   ★ 流水线自检：来源/不确定性/反方/结论/结构/数字口径（纯标准库）
├── references/              # 官方大纲全文（发改投资规〔2023〕304号）+ 测算口径
│   ├── gov-dagang-2023.md       #   政府投资项目通用大纲（11章）
│   ├── ent-dagang-2023.md       #   企业投资项目参考大纲（10章）
│   ├── modeling-standards.md    #   财务测算口径、四表勾稽检查表、指标判据、敏感性
│   └── data-request-list.md     #   资料需求清单模板（三批）
└── templates/               # 可直接套用的文本模板
    ├── report-plan.md           #   章节规划清单（写之前填，留白就退回补料）
    └── review-checklist.md      #   质量三关审查清单 + 修正记录表
```

## 二、怎么用

### 方式 A：智能体直接读 SKILL.md（推荐）
把 `SKILL.md` 全文作为系统提示/技能注入你的智能体，它会按手册里的
「六步工作流 → 分工写作 → 质量三关 → 排版工程 → 报告QA → 视觉验收 → 交付」自动执行。

### 方式 B：人 + 脚本半自动（不想全自动时）
```
pip install python-docx pymupdf xlsxwriter   # 一次性装依赖
# 1) AI 生成初稿 docx（任意方式）→
# 2) 排版净化
python3 scripts/docx_polish.py 初稿.docx 交付版.docx "项目全称" --title "XX项目可行性研究报告"
# 3) 生成测算套表
python3 scripts/gen_model_xlsx_v2.py 套表.xlsx "项目名" 总投资万元 达产收入万元 建设期 运营期
# 4) 生成编制说明
python3 scripts/gen_shuoming.py 说明.docx "项目名称" "约XX亿元"
# 5) 数字与口径体检（断言验收：把客户要求写成断言，一条命令自证全中）
python3 scripts/report_qa.py check 交付版.docx baseline.json
python3 scripts/report_qa.py grep  交付版.docx "旧口径|旧数字"
# 6) 内容完整性自检（来源标注/不确定性/反方视角/结论/结构）
python3 scripts/pipeline_check.py 报告.md
# 7) 视觉验收（可选但有 key 强烈建议）
export DEEPSEEK_API_KEY=sk-...   # 或 DASHSCOPE_API_KEY / ZHIPU_API_KEY / MIMO_API_KEY
python3 scripts/vision_check.py 交付版.docx --models deepseek-vision,mimo
```

### 方式 C：先要料再动笔
`templates/report-plan.md` 十章清单填满再开写；`references/data-request-list.md` 一次性把三批资料要齐。

## 三、依赖

| 工具 | 用途 | 安装 |
|------|------|------|
| python3 + pip | 跑脚本 | - |
| python-docx | docx 读写 | pip install python-docx |
| xlsxwriter | 测算套表 | pip install xlsxwriter |
| pymupdf (fitz) | docx→PDF 渲染（视觉验收用）| pip install pymupdf |
| LibreOffice soffice | docx→PDF 渲染/交付 | sudo apt install libreoffice-writer |
| 视觉模型 key（可选）| 排版看图验收 | 任一：DeepSeek/DashScope/智谱/小米 |

> `report_qa.py` 与 `pipeline_check.py` **只用 Python 标准库**，不装任何依赖即可运行。

## 四、三条铁律（交付前自检）

1. **编制单位/日期/落款留空** —— 客户自己署名，我们不出现
2. **零 AI 痕迹** —— 「」→“”、无 Markdown 残留、元数据清空、文件名不带"终版/AI"
3. **正文 12pt 仿宋 + 首行缩进 2 字符 + 标题样式驱动** —— 这是"像人排的"底线

> 完整交付前检查见 `SKILL.md` 第九章「交付前验证清单」（10 项逐条打勾）。

## 五、本次升级（v1.6）能多给你什么

| 升级项 | 之前 | 现在 |
|--------|------|------|
| 交付前质检 | 靠人眼通读、凭经验判断 | **两个零依赖脚本**：`pipeline_check.py` 机械拦截"没来源/没反方/没结论/太短"，`report_qa.py` 把客户每条要求写成断言、一条命令自证全中 |
| 长文档改稿 | 改完再人工找旧数字，漏网就翻车 | 缓存加速 ~14 倍 + 正则全表扫描（**含表格单元格**）+ 禁用词断言，改一遍验一遍 |
| Word 版式翻车 | 只在交付后才被客户发现 | 新增「分页与图片铁律」：图片被固定行距裁切、大表整表跳页、孤行页、封面占位横线——**症状→根因→修复**对照表，查 XML 就能定位 |
| 客户中途改数 | 只改主数字，衍生数字与汉字形态漏改 | 新增「改稿与口径对齐」章：7 项自上而下排查清单（含"92.6亿/九十二点六亿"双形态扫描）|
| 财务测算 | 知道要算，口径靠记忆 | 新增「四表勾稽检查表」6 项 + 投资构成反向推导法 + 敏感性临界点要求，评审第一眼看的勾稽有了标准动作 |
| PDF 交付形态 | 手册未提 | 新增 PDF 版转换配方（大纲自动成书签、页码域占位属正常、大文件交付提示）|

**一句话：这次升级把"写得好"变成了"可验证地写好"——质检有脚本、版式有铁律、改稿有清单。**

## 六、版本

- v1.0 / v1.1 · 2026-09 · 实战沉淀（300亿海洋产业集群·九大分册·20万字交付）
- v1.2 · 2026-09 · 补分页与图片铁律、PDF 版转换、生图审核词等实战陷阱
- v1.5 · 2026-09 · 补作者与咨询入口
- **v1.6 · 2026-09 · 能力升级**：新增 `report_qa.py`、`pipeline_check.py`（纯标准库零依赖）；新增质量三关、四表勾稽检查表、改稿口径对齐清单、交付前验证清单 10 项；补分页/图片铁律与 PDF 交付配方
