# 验真脚本模板规格

> 适用场景：1 网页采集 / 2 文档字段提取 / 3 SQL 生成
> 配套方法论：M7（验真闭环）+ M2（防幻觉三招）

## 触发场景

| 场景 | 用途 | 与 Prompt 的关系 |
|------|------|----------------|
| 1 采集 | 检查抓取结果完整性 + 字段缺失 | Prompt 末尾"验真抽查"段引用此脚本 |
| 2 提取 | 检查提取字段完整性 + 格式合规 | 同上 |
| 3 SQL | 检查 SQL 输出符合 JSON Schema | 同上 |

## 模板结构（Python 脚本，可执行）

```python
"""
{场景名} 验真脚本 — {日期}
配套 Prompt：见 SKILL.md Step A4 输出
用法：python verify_{场景}_{日期}.py --input {输出文件} --template {模板文件}
"""
import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Any


def check_required_fields(data: List[Dict], required_fields: List[str]) -> List[str]:
    """检查必填字段是否为空"""
    errors = []
    for i, row in enumerate(data, 1):
        for field in required_fields:
            if field not in row or not row[field] or str(row[field]).strip() == "":
                errors.append(f"行 {i}: 必填字段 '{field}' 为空")
    return errors


def check_format(data: List[Dict], field_rules: Dict[str, str]) -> List[str]:
    """检查字段格式是否符合规则（正则）"""
    errors = []
    for i, row in enumerate(data, 1):
        for field, pattern in field_rules.items():
            if field in row and row[field]:
                if not re.match(pattern, str(row[field])):
                    errors.append(f"行 {i}: 字段 '{field}' 格式不合规，值='{row[field]}'，期望 pattern='{pattern}'")
    return errors


def check_enum(data: List[Dict], field_enums: Dict[str, List[str]]) -> List[str]:
    """检查枚举字段取值合法"""
    errors = []
    for i, row in enumerate(data, 1):
        for field, allowed in field_enums.items():
            if field in row and row[field] and str(row[field]) not in allowed:
                errors.append(f"行 {i}: 字段 '{field}' 值 '{row[field]}' 不在允许列表 {allowed}")
    return errors


def check_anomaly_markers(data: List[Dict], anomaly_field: str) -> List[str]:
    """检查异常标记列是否有未处理项"""
    errors = []
    for i, row in enumerate(data, 1):
        if anomaly_field in row and row[anomaly_field] and "待" in str(row[anomaly_field]):
            errors.append(f"行 {i}: 异常标记 '{row[anomaly_field]}' 待人工处理")
    return errors


def check_duplicates(data: List[Dict], key_field: str) -> List[str]:
    """检查主键重复"""
    errors = []
    seen = set()
    for i, row in enumerate(data, 1):
        if key_field in row and row[key_field]:
            if row[key_field] in seen:
                errors.append(f"行 {i}: 主键 '{key_field}={row[key_field]}' 重复")
            seen.add(row[key_field])
    return errors


def run_verification(input_file: str, template_file: str) -> Dict[str, Any]:
    """主验真流程"""
    # 读取模板定义
    with open(template_file, "r", encoding="utf-8") as f:
        template = json.load(f) if template_file.endswith(".json") else None

    # 读取数据
    # (根据场景调整：Excel/CSV/JSON)
    data = []  # TODO: 按场景实现读取逻辑

    all_errors = []

    # 1. 必填字段检查
    required = []  # TODO: 从 template 提取
    all_errors.extend(check_required_fields(data, required))

    # 2. 格式检查
    format_rules = {}  # TODO: 从 template 提取
    all_errors.extend(check_format(data, format_rules))

    # 3. 枚举检查
    enum_rules = {}  # TODO: 从 template 提取
    all_errors.extend(check_enum(data, enum_rules))

    # 4. 异常标记检查
    all_errors.extend(check_anomaly_markers(data, "异常标记"))

    # 5. 主键重复检查
    all_errors.extend(check_duplicates(data, "序号"))

    return {
        "total_rows": len(data),
        "total_errors": len(all_errors),
        "errors": all_errors[:50],  # 最多显示 50 条
        "passed": len(all_errors) == 0,
    }


def main():
    parser = argparse.ArgumentParser(description="{场景名} 验真脚本")
    parser.add_argument("--input", required=True, help="待验证的输出文件")
    parser.add_argument("--template", required=True, help="模板定义文件")
    parser.add_argument("--output", default="verify_report.json", help="验真报告输出路径")
    args = parser.parse_args()

    result = run_verification(args.input, args.template)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"验真完成：{result['total_rows']} 行数据，{result['total_errors']} 个错误")
    if result["passed"]:
        print("✅ 全部通过")
    else:
        print("❌ 存在问题，详见报告")


if __name__ == "__main__":
    main()
```

## 生成规则

### Step 1: 从访谈快照提取验真规则

读取 SKILL.md Step A2 的 5 要素完备快照：
- 必填字段清单（来自访谈 + 模板定义）
- 字段格式规则（来自模板的 validation 段落）
- 枚举字段取值（来自模板）
- 异常标记列名（默认 "异常标记"）
- 主键字段名（默认 "序号" 或 "匹配键"）

### Step 2: 按场景调整检查项

#### 场景 1 网页采集

必检项：
- 必填字段：序号 / 标题 / 来源 URL / 抓取时间
- 格式：URL 正则 / 日期格式
- 重复：URL 不应重复（同 URL 多次抓取需警示）
- 时间：抓取时间应接近当前时间（防旧数据）

#### 场景 2 文档字段提取

必检项：
- 必填字段：序号 / 文档名 / 姓名
- 格式：电话正则 / 学历枚举
- 异常标记：未处理的"待人工核查"项
- 重复：文档名不应重复（除非多份同源）

#### 场景 3 SQL 生成

必检项（基于 JSON Schema）：
- 必填字段：schema.required 数组
- 格式：schema.pattern 规则
- 枚举：schema.enum 列表
- 业务口径：检查"待确认"字段是否仍未明确

### Step 3: 注入 M7 验真闭环三要素

验真脚本必须包含 M7 的三要素：

| 要素 | 实现 |
|------|------|
| 标注依据 | 每个错误必须标注"违反了哪条规则" |
| 抽查 | 脚本默认抽查前 100 条 + 随机 50 条（大数据量时） |
| 异常标记 | check_anomaly_markers 函数 |

### Step 4: 注入 M2 防幻觉三招

1. **亮证据**：错误信息包含具体行号 + 字段值
2. **给示弱**：异常项不直接报错，标记"待人工核查"
3. **禁脑补**：脚本不做"自动修复"，只报告问题

### Step 5: 输出验真报告

验真脚本运行后输出 JSON 报告：

```json
{
  "total_rows": 200,
  "total_errors": 5,
  "errors": [
    "行 3: 必填字段 '电话' 为空",
    "行 17: 字段 '电话' 格式不合规，值='138abc'，期望 pattern='^1[3-9]\\d{9}$'",
    "行 25: 字段 '学历' 值 '高中' 不在允许列表 ['大专', '本科', '硕士', '博士', '其他']",
    "行 42: 异常标记 '待人工核查' 待人工处理",
    "行 88: 主键 '序号=88' 重复"
  ],
  "passed": false
}
```

## 与其他模块的接口

| 接口 | 调用方 | 依赖 |
|------|--------|------|
| 上游 | excel-template-spec.md | 字段定义 + validation 规则 |
| 上游 | ddl-template-spec.md | 字段 + 业务口径检查 |
| 上游 | json-schema-spec.md | schema 校验规则 |
| 上游 | tag-tree-template-spec.md | 标签合法性检查 |
| 下游 | SKILL.md Step A4 "验真抽查建议" 段 | 引用此脚本 |
| 关联方法论 | M7 验真闭环 | 三要素 |
| 关联方法论 | M2 防幻觉三招 | 亮证据 + 给示弱 + 禁脑补 |
