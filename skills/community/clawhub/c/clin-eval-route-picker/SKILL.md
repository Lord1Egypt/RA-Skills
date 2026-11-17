---
name: clin-eval-route-picker
description: 临床评价路径选择器 — 免临床目录、同品种路径、临床试验三条路怎么选说不清，资料写到一半才发现路走错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读） 适用场景：当需要临床评价路径选择器能力时使用本技能；触发词：clin-eval-route-picker。
slug: clin-eval-route-picker
version: 1.0.1
display_name: 临床评价路径选择器
display_name_en: Clinical Evaluation Route Picker
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: 医疗器械合规
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "临床评价路径选择器 — 免临床目录、同品种路径、临床试验三条路怎么选说不清，资料写到一半才发现路走错了（零依赖，确定性输出，rc=0/1/2，--json 机器可读）"
description_en: "Pick among three clinical evaluation routes (exempt catalog, same-device equivalence, clinical trial) before writing dossiers down the wrong path (zero-dependency, deterministic JSON IR)."
classification:
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "data-analytics", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [clin-eval-route-picker, 医疗器械合规]
ai_protocol: true

read_when:
  - 用户提及本技能触发词或面临描述中的典型问题时
  - 用户说「clin-eval-route-picker」或需要该能力时

changelog: "1.0.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：[skill-quality-gate](../skill-quality-gate/SKILL.md)


## English

### When to use
1. **Uncertain R&D route**: at drug/device kickoff, when complex attributes (novelty, dosage form, indication) make regulatory matching unclear.
2. **Dossier correction**: half-way through a clinical submission, the chosen route no longer fits the product and compliance must be re-evaluated.
3. **Cross-org collaboration**: a machine-readable decision basis (JSON) is needed for automated systems or R&D platforms.
4. **Standardized compliance review**: the R&D system requires a deterministic route report to avoid human-judgment stalls.

### Usage
```bash
python clin_eval_route_picker.py --input "product features" --output json
```
- `--input`: key data to assess (JSON or structured text) describing novelty, indication, and R&D stage.
- `--output`: `json` or `text`; use `--json` for machine-readable mode.
- `rc-mode`: decision code (rc=0 recommended, rc=1 needs verification, rc=2 high risk).
- Zero-dependency; only Python and `clin_eval_route_picker.py` are needed.

### Process
1. Prepare product data: preclinical data, submission checklist, and core R&D attributes.
2. Build the input as a JSON object in `--input`.
3. Run `python clin_eval_route_picker.py` with the configured params.
4. Read the recommended-route text or JSON from the terminal.
5. Check the rc field (0/1/2) to judge decision quality.
6. Act: rc=0 proceeds to submission; rc>1 triggers a second evaluation meeting.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 1.0.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用
1. **研发路径不确定性**：在药物或医疗器械立项阶段，面对复杂属性（如创新程度、剂型、适应症）无法快速匹配监管要求时。
2. **资料撰写纠错**：临床申报文档编写至一半后，发现已选路径不符合当前产品定位，需重新评估合规性风险时。
3. **跨机构协作对接**：需要机器可读的决策依据（如 JSON 格式），用于自动化系统或内部 R&D 管理平台的数据流转时。
4. **标准化合规审查**：企业研发管理体系要求提供确定性的路径选择报告，避免人为判断偏差导致流程停滞时。

## 用法
**命令：**
```bash
python clin_eval_route_picker.py --input "产品特征" --output json
```
**参数说明：**
*   `--input`: 输入待评估的关键数据（支持 JSON 格式或结构化文本），描述产品的创新程度、适应症及研发阶段。
*   `--output`: 指定输出格式，可选 `json` 或 `text`。当配合 `--json` 标签时开启机器可读模式。
*   `rc-mode`: 定义返回的决策编码逻辑（rc=0 为推荐路径，rc=1 为需验证，rc=2 为高风险）。
*   **依赖：** 该技能零依赖运行，仅需 Python 环境及脚本文件 `clin_eval_route_picker.py`。

## 流程
1. 准备产品数据：整理待评估产品的临床前数据、申报资料清单及核心研发属性。
2. 构建输入指令：将产品特征封装为 JSON 对象，写入命令行参数 `--input`。
3. 执行脚本运行：调用 `python clin_eval_route_picker.py` 并传递配置后的参数。
4. 解析结果输出：读取终端返回的推荐路径文本或 JSON 结构数据。
5. 验证状态码 (rc)：根据返回值中的 rc 字段判断决策质量（0/1/2）。
6. 制定后续行动：依据 rc=0 直接走申报流程，rc>1 则触发二次评估会议。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
