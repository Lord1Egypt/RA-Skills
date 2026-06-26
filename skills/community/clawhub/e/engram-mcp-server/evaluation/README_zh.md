# Engram 案例评测

[English](./README.md) | 中文

这个目录提供一套轻量、可复现的对比方法：

- baseline（同模型，不加载 Engram）
- Engram（同模型，加载 Engram）

目标不是做排行榜，而是输出可公开复核的案例结论，验证 Engram 是否带来质量提升。

## 1）准备评测用例

复制模板并填写：

```bash
cp evaluation/case_study_template.json evaluation/my_case_study.json
```

每个 case 至少补全：

- `baseline_answer`
- `engram_answer`
- `expected_keywords`（应该出现的关键点）
- `forbidden_keywords`（不该出现的幻觉/反模式）
- `checkpoints`（带权重的规则检查，支持 `mode=all/any`）

当前评分维度：

- **content**：checkpoint 通过率（若未配置 checkpoints，则回退为 expected_keywords 覆盖率）
- **safety**：forbidden_keywords 触发惩罚
- **structure**：是否有结构化输出/步骤信号/风险提示信号

默认权重：content 0.65 + safety 0.25 + structure 0.10  
可在单个 case 里通过 `weights` 覆盖。

## 2）执行打分

```bash
python3 evaluation/score_case_study.py --input evaluation/my_case_study.json
```

可选导出 CSV：

```bash
python3 evaluation/score_case_study.py \
  --input evaluation/my_case_study.json \
  --csv evaluation/my_case_study_report.csv
```

## 3）公开案例时建议附带

- 模型名称与版本
- 使用的提示词模板
- 用例文件
- baseline/Engram 原始回答
- 生成的评测报告

这样外部才能复现实验并验证你的结论。

## 关于“主观性”的说明

- 这个脚本是**规则打分**，不依赖评审模型，结果可复现。
- 但它仍然无法完整衡量深层推理质量。
- 建议配套一份人工复核表（比如正确性/完整性/可执行性 1-5 分）一起公开。
