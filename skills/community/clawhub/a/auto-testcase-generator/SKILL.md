---
name: testcase-generator
version: 1.1.0
description: Automated test case generation from project documents. This skill should be used when generating structured test cases from requirements documents, API specifications, or project documentation. It extracts test variables, analyzes embedded images and flowcharts, creates flow diagrams, performs path coverage analysis, and outputs Excel test case files following standard templates.
---

> ✍️ **作者：十年腾讯测试小白**

# 测试用例生成器

- **当前版本**：v1.1.0
- **v1.1.0**：新增「端到端流程」第七维度覆盖设计
- **v1.0.0**：初始版本，支持六维度覆盖设计、四阶段工作流、三层交叉验证

从需求文档（PDF、Word、Markdown）自动生成结构化 Excel 测试用例，支持图片/流程图智能分析，确保测试覆盖完整。

## 核心能力

1. **文档解析**：PDF、Word、Markdown 需求文档，提取文本和嵌入图片/流程图
2. **图片处理**：解读流程图/状态图/序列图，转化为可测试场景
3. **变量提取**：识别测试变量、边界值、边界条件
4. **流程可视化**：生成 Mermaid 格式流程图
5. **路径覆盖**：确保所有执行路径和决策点完全覆盖
6. **用例生成**：按标准模板生成 Excel 文件，单工作表按模块分组
7. **验证报告**：三层交叉验证（规则→用例、用例→规则、标准→用例）

## 依赖工具

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | ≥3.8 | 脚本运行 |
| PyMuPDF (fitz) | ≥1.23 | PDF图片提取 |
| openpyxl | ≥3.1 | Excel生成 |

## Checklist 规范（强制执行）

每阶段必须：列表展示checklist → 逐项打勾 → 输出上下文传递卡 → 等待用户确认。

## 标准工作流程

### 阶段零：测试范围确认

接收文档后先划清测试边界，三区域划分：
- **Zone 1（核心区）**：直接测试的功能，完整分析并生成用例
- **Zone 2（交互区）**：有交互的外部模块，仅作背景知识
- **Zone 3（外部区）**：无关内容，排除

输出范围确认表 → checklist → 传递卡 → 用户确认。

### 阶段一：需求深度分析（仅 Zone 1）

入口引用阶段零传递卡，执行：
1. 文档解析（文本+图片），Zone 2 精简为背景知识
2. 需求建模：提取规则（DR/BR/PR/CR/SR）、记录缺口和假设
3. 需求缺口识别：标注严重程度
4. 测试标准定义：正确性/性能/可靠性验收标准
5. 风险评估：Top 5 关键风险
6. 输出需求分析简报（格式参考 `references/analysis_template.md`）

输出 checklist → 传递卡 → 用户确认。

### 阶段二：模块识别与用例设计

入口引用阶段一传递卡，执行：
1. 功能模块划分
2. **七维度覆盖设计**：功能/异常/边界/集成/性能/安全/端到端
3. 模块复杂度评估（🟢低5~10条/🟡中10~25条/🔴高25~50+条）
4. 同步分配优先级（P0/P1/P2/P3）和测试类型
5. 端到端流程独立分组，串联完整业务路径（3~10条）
6. 模块-维度覆盖矩阵

达标标准：规则覆盖100%、每模块≥5/7维度、缺口覆盖100%、单模块≥5条。

输出 checklist → 传递卡 → 用户确认。

### 阶段三：Excel 输出

入口引用阶段二传递卡，执行：
1. 读取模板（有则用，无则默认格式），格式参考 `references/excel_format.md`
2. 12列标准结构：用例编号/优先级/测试类型/模块/场景/测试点/操作步骤/预期结果/测试结果/用例生成依据/图像来源/截图
3. 格式自检：列数完整、编号连续、优先级着色、测试类型合规、换行符chr(10)、模块分隔行`【模块名称】`
4. 优先级分布：P0:10~15%, P1:30~40%, P2:30~40%, P3:10~20%

输出 checklist → 传递卡 → 用户确认。

### 阶段四：三层交叉验证

入口引用阶段三传递卡+阶段一验证基准，执行：
- **第一层（规则→用例）**：每条规则至少1条用例覆盖，100%覆盖率
- **第二层（用例→规则）**：每条用例可追溯到规则，0条孤立用例
- **第三层（标准→用例）**：验收标准和Top5风险有对应用例

未通过自动修复→重新验证，直到全部通过。

输出验证汇总报告 → checklist → 传递卡 → 用户确认。

### 阶段五：交付

交付物：Excel用例文件 + 需求分析简报 + 验证报告 + 全流程Checklist汇总表 + 关键指标汇总。

## 视觉内容处理

| 类型 | 方法 | 影响 |
|------|------|------|
| 流程图 | 提取决策节点和路径 | 路径和分支用例 |
| 状态图 | 提取状态和转换条件 | 状态转换用例 |
| 序列图 | 识别消息流和时序 | 集成和时序用例 |
| UI原型 | 分析界面元素 | UI交互用例 |

PDF图片提取使用 `scripts/extract_pdf_images.py`（xref+MD5去重+质量过滤）。

## 最佳实践

1. 按阶段零→一→二→三→四→五顺序执行，每阶段用户确认后才进入下一步
2. 每阶段输出可见checklist和上下文传递卡
3. 单工作表输出，模块分隔用`【模块名称】`（不用`=`开头）
4. 换行符用chr(10)+wrap_text，不用字符串`\n`
5. 每条用例标注生成依据，确保可追溯
6. 需求缺口标注"待确认"并给出测试假设
7. 交付前必须通过三层交叉验证

## 资源说明

- `scripts/extract_pdf_images.py`：PDF图片优化提取
- `references/excel_format.md`：Excel输出格式规范
- `references/analysis_template.md`：需求分析简报模板
- `references/image_processing.md`：图片处理最佳实践
