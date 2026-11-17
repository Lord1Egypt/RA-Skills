# 使用指南 · Usage Guide

## 一、命令详解

```
python3 scripts/document_engine.py <command> [options]

commands:
  audit       审计一份文书
  list-rules  列出规则库
  demo        运行内置演示

audit 选项:
  --type <contract|regulation|official_doc|generic>   文书类型（必填）
  --input <path>                                      输入文件路径，UTF-8（必填）
  --title <text>                                      文书标题（默认取文件名）
  --format <html|json|md>                             输出格式（默认 html）
  --output <path>                                     输出文件路径（缺省打印到 stdout）
  --rules-dir <path>                                  自定义规则目录（覆盖内建规则）

list-rules 选项:
  --type <type>                                       按类型过滤（缺省列出全部）
  --rules-dir <path>                                  自定义规则目录

demo 选项:
  --type <type>                                       仅演示指定类型
  --output-dir <path>                                 报告输出目录（默认当前目录）
```

输出格式推断规则：指定 `--output` 且未指定 `--format` 时，按扩展名判断（`.html` → html，其余 → json）；两者都未指定时默认 html。

## 二、审计流程

1. **分节**：按条款号（第X条 / 1. / 一、）切分审计单元
2. **规则扫描**：对该文书类型适用的全部规则做全文关键词 / 正则匹配
3. **文档级审计**：要素完整性、一致性、权利义务对等、公文格式
4. **去重与挂载**：按 (rule_id, message, snippet) 去重，finding 挂载到命中的审计单元
5. **评分与判定**：按严重度扣分，存在 FATAL/CRITICAL 或总分 < 60 即不通过
6. **报告生成**：三选一格式输出，内含责任节点与审计追溯链

## 三、报告字段（JSON）

| 字段 | 类型 | 说明 |
|---|---|---|
| `doc_type` | string | 文书类型 |
| `title` | string | 文书标题 |
| `overall_score` | number | 综合评分 0–100 |
| `passed` | boolean | 是否通过 |
| `generated_at` | string | 审计时间（ISO 秒级） |
| `summary.total_findings` | number | 发现总数 |
| `summary.by_severity` | object | 按严重度计数 |
| `summary.by_category` | object | 按维度计数 |
| `responsibility` | object | 责任节点（organization / role / stage / trace_chain） |
| `findings[]` | array | 问题清单：rule_id / category / severity / message / suggestion / location / snippet |
| `trace[]` | array | 审计追溯链：timestamp / operation / stage / node_id / remark |

## 四、作为库调用

`scripts/document_engine.py` 可直接 import：

```python
import sys
sys.path.insert(0, "scripts")
from document_engine import ComplianceEngine, DocType, to_json, to_html, to_markdown

engine = ComplianceEngine()
report = engine.audit(open("合同.txt", encoding="utf-8").read(), DocType.CONTRACT, title="采购合同")
print(report.overall_score, report.passed)
print(to_json(report))
```

自定义规则目录：`ComplianceEngine(rules_dir=Path("./my_rules"))`。

## 五、确定性说明

- 同一输入文件的审计判定、评分、finding 列表完全可复现
- 报告中 `generated_at`（时间戳）与 `responsibility.trace_chain`（UUID）为运行时生成，不属于审计判定
- 引擎不读取环境变量、不访问网络、不生成随机数影响判定
