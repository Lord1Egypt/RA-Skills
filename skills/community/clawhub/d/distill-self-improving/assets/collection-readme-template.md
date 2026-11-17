# <collection-name>

- slug: <stable-ascii-slug>
- source_root: <exact-source-root>
- directory_type: <document-collection|code-project-docs|mixed-general>
- classification_evidence: <user-statement-and-observed-evidence>
- handling_strategy: <recursive-document-processing|selected-project-docs|all-files-root-audit>
- owner_boundary: <exact-non-overlapping-boundary>
- scope_mode: <user-confirmed|authoritative-migration>
- expected_files: <count>
- groups: <count>
- sensitivity: <normal|sensitive|strict-sensitive>
- last_verified: <YYYY-MM-DD>

## 范围与排除

- included: <user-confirmed-rule>
- excluded: <rule-and-count-per-rule>
- source_of_expected_scope: <user-request-or-authoritative-inventory>
- path_to_group: `scope.csv` 是上游真值，不能从结果目录或 summary 反推。

## 处理契约

- `scope.csv`、`inventory.csv`、`manifest.csv` 的 path 集合唯一且相同。
- 每个可安全整理的文件只有一个独立结果；每个合法 skip 有具体原因。
- summary 只做跨文件综合与结果链接，不替代独立结果。
- 原文件与当前现场优先；历史提取仅在 identity 核验一致时辅助读取。

## 现场复核

- <known-limitations-and-required-rechecks>
