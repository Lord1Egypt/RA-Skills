# 投标模拟评标 · 评标表逆向工程（v1.2.0）

投标人侧「评标表逆向工程」三合一技能——把一份《评标表》榨成三件事：
- **A 模拟评标**（魔鬼评委）：逐项打分，找最弱评分项与可提分空间。
- **B 得分点导航 + 响应覆盖审计**：得分点地图 + 响应是否漏了评分项（隐性丢分/废标风险）+ 评分索引表。
- **C 评标表合规审查**（质疑弹药）：找《评标表》本身的歧视/违规条款，生成可质疑点清单 + 法条依据。

**v1.2.0 提示工程增强**（吸收外部深度诊断）：脚本降级为可选加速器（无脚本时 LLM 直接结构化抽取，流程不中断）；新增输入完整性预检、多标段识别、价格分开标前策略、法条核验声明与内置硬法条速查表；最弱项排序升级为多维补强优先级矩阵；三模式输出骨架内联、评分索引表增加评委视角。详见 `SKILL.md`。

## 快速开始

```bash
# 通用预处理
python scripts/parse_score_table.py demo/eval_table.docx --out demo/criteria.json        # 抽评标表
python scripts/parse_score_table.py --mode response demo/response.docx --out demo/response.txt  # 抽响应
python scripts/parse_score_table.py --mode audit --criteria demo/criteria.json demo/response.docx --out demo/coverage_hints.json  # 覆盖初判

# 然后把 criteria.json / response.txt / coverage_hints.json 交给本技能（LLM），
# 按 SKILL.md 选 A / B / C 模式产出对应报告：
#   A → templates/mock-eval-report.md
#   B → templates/coverage-audit-report.md
#   C → templates/compliance-report.md
```

## 目录

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 评标表逆向工程专家系统提示（三模式 + 共享护栏） |
| `scripts/parse_score_table.py` | 抽评标表→criteria.json（含 `is_knockout` 否决红线标记）；`--mode response` 抽响应；`--mode audit` 覆盖初判→coverage_hints.json |
| `references/mock-evaluation-method.md` | 模式 A 打分方法论（客观看证据/主观给估算/最弱项公式） |
| `references/score-point-navigation.md` | 模式 B 得分点地图 + 覆盖审计方法论 |
| `references/compliance-review.md` | 模式 C 六维度合规审查方法论 |
| `templates/mock-eval-report.md` | 模式 A 报告模板 |
| `templates/coverage-audit-report.md` | 模式 B 报告模板 |
| `templates/compliance-report.md` | 模式 C 报告模板 |
| `demo/` | eval_table.docx / response.docx / eval_table_noncompliant.docx（问题表）+ 解析产物 + 样例报告 |
| `test_cases/cases.md` | 用例 L（解析+打分）/ M（合规审查）/ N（覆盖审计） |

## 护栏

- 禁止编造响应中不存在的证据；找不到即 0 分 / missing + 标注。
- 不提供任何骗分/绕合规建议；补强只限真实材料补充或真实表述优化。
- 主观项一律标「估算/置信低」。
- 合规审查只识别不捏造；质疑点须基于真实存在的条款；法条以现行法 + IMA 知识库核实为准。
- 总价/覆盖结论仅自检参考，非真实评标结果。
