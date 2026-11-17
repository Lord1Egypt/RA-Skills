# resume-jd-review 最终审查清单

> 审查时间：2026-08-14 ｜ 版本：2.0.0 ｜ 状态：全部测试 PASS，端到端可运行

---

## 一、核心能力审查

### 能力 1：简历评分（`--stage review`）

按《校招产品经理能力评价体系》5 大维度规则驱动评分（总分 100），零大模型依赖：

| 维度 | 权重 | 考察内容 | 对应规则 |
| --- | --- | --- | --- |
| 过往经验匹配度 | 20% | 实习/项目方向与 JD 行业一致性；实际性工作闭环（调研→PRD→评审→落地→复盘）；专业是否计算机相关 | `industry_match`、`substance_work`、`major_relevance` |
| 逻辑能力 | 30% | 背景/产出/价值衡量/北极星指标四要素；长期 roadmap | `logic_elements`、`roadmap_presence` |
| 表达能力 | 20% | 冗余检测；跨境行业英语工作能力 | `redundancy_check`、`english_ability` |
| AI 探索能力 | 15% | AI 应用 + 落地/提效证据 | `ai_exploration` |
| 个人素养 | 15% | 责任心/创造力/逻辑严谨/热爱四要素 | `soft_quality` |

- 规则引擎共 **21 种规则**（`rule_engine.py` RULE_REGISTRY 已全部注册）
- 每条得分**可追溯**：报告含命中证据（如"已覆盖 4/5 个实际性工作环节"）
- 维度标准**可替换**：`--dimensions` 传入自定义 JSON

### 能力 2：简历一键优化（`--stage review --optimize-instruction "..."`）

- 优化指令自动识别意图：量化补充 / 重点突出 / 精简 / JD 对齐 / 规范化
- 直接生成 `02_优化后简历.md`，**不编造数据**，待补数字标注【待补充量化数据】
- 附优化摘要与逐条变更日志

### 能力 3：模拟面试题（`--stage interview`）

- JD 职责拆解 + 简历项目/实习深挖，生成 7 大类 30+ 题
- 附 JD 高频考察点附录 + AI 方向专项题（自动检测 JD 是否含 AI 要求）

### 输入 / 输出

- 简历 PDF/图片 → 自动 OCR；简历纯文本 → 直接输入
- 输出 4 份文件：`01_评分报告.md`、`02_优化后简历.md`、`03_简历画像.md`、`04_模拟面试题.md`

---

## 二、使用到的比赛矩阵内 Skill 清单

| # | 矩阵内 Skill | 调用能力 | 用途 |
| --- | --- | --- | --- |
| 1 | `tencentcloud-ocr` | GeneralAccurateOCR（通用高精度识别） | 简历图片/PDF → 全文文本 |
| 2 | `tencentcloud-ocr-extractdocagent` | ExtractDocAgent（实时文档抽取 Agent） | 按自定义字段抽取姓名/学校/实习/项目等关键信息 |

- 两技能均在 `skills/` 目录中实际存在，属"腾讯云 AI Skills 技能矩阵"内能力
- 统一环境变量：`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`
- 依赖包：`tencentcloud-sdk-python>=3.0.1100`（`requirements.txt` 已声明）

> 注：`scripts/llm_client.py`、`scripts/ocr_utils.py` 为遗留文件，仅作对照保留，**非矩阵内技能调用**，不参与主流程。

---

## 三、验证结果（最终审查实测）

- 单元测试 `tests/test_unit.py`：**ALL PASS**（含 5 维度断言、9 类新规则、AI 高分组对照）
- 端到端 `tests/test_e2e.py`：PASS
- 样例实测：`--stage review` 正常运行，输出 4 份报告 + 评分 JSON，综合评分可追溯
- 打包 `resume-jd-review.zip`：可解压独立运行

---

## 四、审查结论

✅ 评分体系与用户 Excel 标准一致（5 维度 / 权重 20-30-20-15-15）
✅ 规则引擎完整（21 种规则，纯本地计算，得分可追溯）
✅ 矩阵内技能使用合规（仅依赖 2 个 OCR 技能，均有实际调用）
✅ 三大能力（评分 / 优化 / 面试题）齐全
✅ 测试全绿，打包产物可独立运行
