---
name: data-cleaning-claw
description: |
  数据自动化清洗虾。处理脏数据、重复数据与广告噪音，输出高质量干净数据。
  触发场景：用户提到"清洗数据"、"去重"、"数据清理"、"脏数据"、"数据标准化"、"格式统一"、"去噪"、"数据预处理"、"数据质量"、"缺失值处理"，或上传了 CSV/Excel/JSON 文件并要求清洗处理时。
  支持：Excel/CSV/JSON 输入，去重、缺失值填充、格式标准化（日期/金额/电话）、HTML去噪、数据验证，输出清洗后文件 + 清洗报告。
---

# 数据自动化清洗虾

处理脏数据的专用 skill。核心脚本：`scripts/data_clean.py`。

## 工作流程

### 1. 接收数据

用户可通过以下方式提供数据：
- 上传文件（CSV / Excel / JSON）→ 保存到 workspace，记录路径
- 直接粘贴数据 → 写入临时 CSV 文件

### 2. 确认清洗需求

如果用户没有明确说明，询问以下信息（可一次性问完）：
- 需要哪些清洗操作（去重/缺失值/格式标准化/HTML去噪/数据验证）？
- 去重时是否有关键字段（如手机号、邮箱）？
- 输出格式（CSV/Excel/JSON）？

如果用户说"全部清洗"或"帮我清洗一下"，默认执行所有规则：`strip-html,deduplicate,fill-missing,standardize,validate`。

### 3. 执行清洗

使用 `exec` 运行脚本：

```bash
python3 ~/.openclaw/skills/data-cleaning-claw/scripts/data_clean.py \
  --input "<输入文件路径>" \
  --output "<输出文件路径>" \
  --rules "strip-html,deduplicate,fill-missing,standardize,validate" \
  --key-fields "<可选：去重关键字段，逗号分隔>"
```

可用规则（`--rules` 参数，逗号分隔）：
- `strip-html` — 去除 HTML 标签和广告噪音
- `deduplicate` — 去重（默认全字段；`--key-fields` 指定关键字段）
- `fill-missing` — 缺失值填充（数值→中位数，文本→"未知"）
- `standardize` — 格式标准化（自动识别日期/金额/电话列）
- `validate` — 数据验证，异常行添加 `_数据质量标记` 列

可选字段强制指定参数：
- `--date-fields` — 强制指定日期列（逗号分隔列名）
- `--amount-fields` — 强制指定金额列
- `--phone-fields` — 强制指定电话列

### 4. 输出结果

脚本自动生成两个文件：
- `<output>` — 清洗后的数据文件
- `<output>.report.json` — 清洗报告（删除行数、各列处理情况）

向用户展示清洗报告摘要，并发送清洗后的文件。

## 参考资料

需要了解具体规则时读取：
- `references/cleaning-rules.md` — 去重、缺失值、格式标准化的详细规则
- `references/noise-patterns.md` — HTML噪音、广告文案、无效字符的识别模板
- `references/data-types.md` — 日期、金额、电话、邮箱的识别正则

## 注意事项

- 清洗前提醒用户备份原始数据（如果是重要数据）
- 默认策略是**标记**异常值（添加 `_数据质量标记` 列），不直接删除，保留人工复核
- 脚本依赖：`pandas numpy openpyxl beautifulsoup4`，如缺少依赖先运行 `pip install pandas numpy openpyxl beautifulsoup4`
