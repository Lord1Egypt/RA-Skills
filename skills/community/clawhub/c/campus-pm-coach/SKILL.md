---
name: resume-jd-review
description: 校招/实习互联网产品经理简历评分与面试模拟技能。当用户需要按《校招产品经理能力评价体系》对简历评分、优化简历，或基于 JD 生成模拟面试题时应使用此技能。支持简历图片/PDF（腾讯云 OCR）或纯文本输入，输出评分报告（5 维度：经验匹配20%/逻辑30%/表达20%/AI探索15%/素养15%）、优化后简历与 7 大类面试题，零大模型依赖、得分可追溯。
description_zh: 校招/实习产品经理简历评分与面试模拟：规则驱动评分、一键优化防幻觉、基于 JD 生成模拟面试题，零大模型依赖、得分可追溯。
description_en: Resume scoring & interview prep for campus/intern PM roles: rule-based scoring, hallucination-safe resume optimization, JD-based mock interview questions. No LLM dependency, traceable scores.
version: 2.1.0
---

# 校招产品经理简历评分与面试模拟（resume-jd-review）

> 面向人群：**校招 / 实习 · 互联网产品经理**求职者
> 定位：四大能力一体 —— **⓪ 首轮诊断（三部分一体化） ① 简历评分 ② 简历一键优化 ③ 基于 JD 的模拟面试题**
> 技术路线：**矩阵内技能（腾讯云 OCR 全家桶）+ 本地规则引擎，零大模型依赖、零推理费用、得分可追溯**

## 〇、首轮诊断（`--stage quick`）

拿到简历 + JD 后**直接一次性输出三部分**，适合首轮沟通/面试前快速预览：

1. **① 简历评分 + 细项原因描述** —— 总分 + 5 维度得分表 + 每条规则的命中证据与失分原因
2. **② 可能问到的问题** —— 按 JD 匹配度与简历短板排序的 Top 8 面试问题
3. **③ 综合判断** —— 匹配度结论（高/中/低）、核心竞争力、关键风险点、投递前必改项、投递建议

输出 1 份 `00_首轮诊断报告.md`（规则化推导，零大模型、可追溯）。

## 一、四大能力

### ⓪ 首轮诊断（`--stage quick`）

见上文「〇、首轮诊断」。

### ① 简历评分（`--stage review`）

按《校招产品经理能力评价体系》5 大维度进行规则驱动评分（总分 100）：

| 维度 | 权重 | 考察内容 | 关键规则 |
| --- | --- | --- | --- |
| 过往经验匹配度 | 20% | 实习/项目方向与 JD 行业一致性；实际性工作（调研→PRD→评审→落地→复盘闭环）；专业是否计算机相关 | `industry_match`、`substance_work`、`major_relevance` |
| 逻辑能力 | 30% | 项目是否讲清 背景（为什么做）/ 产出（做什么）/ 价值衡量（怎么衡量）/ 北极星指标；能否看到核心价值与长期 roadmap | `logic_elements`、`roadmap_presence` |
| 表达能力 | 20% | 描述是否重复累赘；跨境行业英语是否可作为工作语言 | `redundancy_check`、`english_ability` |
| AI 探索能力 | 15% | 是否通过 AI 落地产品、输出产出、实现提效 | `ai_exploration` |
| 产品经理个人素养 | 15% | 责任心（不半途而废）/ 创造力 / 逻辑严谨（定量定性+规划）/ 热爱（持续体验产品有成绩） | `soft_quality` |

- 每条得分**可追溯**：报告第四部分列出每条规则命中证据（如"已覆盖 4/5 个实际性工作环节"、"专业命中计算机相关关键词"）
- 维度标准**可替换**：编辑 `config/default_dimensions.json` 或 `--dimensions` 传入自定义 JSON

### ② 简历一键优化（`--stage review --optimize-instruction "..."`）

- 指令自动识别意图：量化补充 / 重点突出 / 精简 / JD 对齐 / 规范化
- 直接生成新简历文档 `02_优化后简历.md`，**不编造数据**，待补数字以 `> 待补充量化数据` 引用提示行标出（不写入正文，避免干扰重新评分）
- 附优化摘要与逐条变更日志
- **防幻觉原则**：只做原有内容上的表达/结构调整——
  - 不新增任何非本人执行的细节（不新增经历、数据、头衔、成果）
  - 不把"参与/协助"夸大为"主导/独立"等强所有权词（动词升级保持保守）
  - 每轮优化后自动执行**防幻觉校验**（数字溯源 + 所有权词强度比对），发现疑似新增内容即告警并需人工核对
- **高评分方向优化**：默认清理口语/空话词（大概/基本上/等等…）并做弱动词升级；评分规则中「负责/参与/协助」等正常强动词不计为重复口水词，避免"优化动词反而触发扣分"
- **闭环复评**：每轮优化后自动用评分引擎对优化稿正文复评，验证分数不低于原文；若异常下降会明确告警
- **评分公平性**：评分与结构化解析前自动剥离优化稿的元信息（头部声明、量化提示、优化摘要、三部分诊断），保证"优化稿重新评分"与"原文评分"在同一口径下对比，杜绝"优化后反而低分"的假象
- **三部分输出约定**：每一轮优化简历之后，输出结构都包含三部分——**① 简历评分 + 细项原因描述 ② 可能问到的问题 ③ 综合判断**（追加在优化稿文档末尾「本轮优化后的三部分诊断」）

### ③ 模拟面试题（`--stage interview`）

- 基于 JD 职责拆解 + 简历项目/实习深挖，生成 7 大类 30+ 题：
  自我介绍与产品认知 / 需求分析与产品设计 / 数据思维与数据分析 / 项目与实习经历深挖 / 行为面试 / 开放设计题 / 反问环节
- 附 JD 高频考察点附录与 AI 方向专项题（自动检测 JD 是否含 AI 相关要求）

## 二、输入方式

| 方式 | 命令 |
| --- | --- |
| 首轮诊断（三部分一体化） | `python3 main.py --resume-text "$(cat resume.txt)" --jd jd.txt --stage quick -o output/` |
| 简历 PDF/图片 | `python3 main.py --resume-doc resume.pdf --jd jd.txt --stage all -o output/`（自动调用矩阵内 OCR + 文档抽取） |
| 简历纯文本 | `python3 main.py --resume-text "$(cat resume.txt)" --jd jd.txt --stage all -o output/` |
| 一键优化 | 追加 `--optimize-instruction "突出实习经历，补充量化表达"` |
| 自定义维度 | `--dimensions my_dims.json` |

输出文件：
- `00_首轮诊断报告.md`（`--stage quick`）：三部分一体化（评分+细项原因 / 可能问到的问题 / 综合判断）
- `01_评分报告.md`、`03_评分结果.json`：评分与依据
- `02_优化后简历.md`（含优化指令时）：优化稿 + 末尾附「本轮优化后的三部分诊断」
- `04_模拟面试题.md`（`--stage interview` / `all`）：7 大类题库

## 三、矩阵内技能依赖

| 依赖技能 | 用途 |
| --- | --- |
| `tencentcloud-ocr` | GeneralAccurateOCR 通用高精度识别（简历图片/PDF → 全文） |
| `tencentcloud-ocr-extractdocagent` | ExtractDocAgent 文档抽取（按字段抽取姓名/学校/实习/项目等） |

环境变量（与矩阵内 OCR 技能一致）：`TENCENTCLOUD_SECRET_ID`、`TENCENTCLOUD_SECRET_KEY`。

## 四、测试与验证

```bash
cd scripts
python3 tests/test_unit.py   # 规则引擎 + 解析 + 评分 + 优化 + 面试题
python3 tests/test_e2e.py    # 全流程端到端
```

## 五、目录结构

```
resume-jd-review/
├── _meta.json                     # 技能元数据（场景/能力/依赖）
├── SKILL.md                       # 本说明
├── config/
│   ├── default_dimensions.json    # ★ 评分维度（按你的 Excel 标准）
│   └── interview_templates.json   # 面试题分类模板
├── sample/                        # 样例简历/JD/输出
├── scripts/
│   ├── main.py                    # 入口编排
│   ├── ocr_service.py             # 矩阵内 OCR + 文档抽取封装
│   ├── resume_parser.py           # 本地结构化解析
│   ├── rule_engine.py             # ★ 规则引擎（21 种规则）
│   ├── evaluator.py               # 评分引擎
│   ├── optimizer.py               # 简历优化
│   ├── interviewer.py             # 面试题生成
│   ├── formatter.py               # 报告格式化
│   └── tests/                     # 单元 + 端到端测试
```
