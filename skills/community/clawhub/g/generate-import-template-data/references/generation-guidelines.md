# Generation Guidelines

Use this reference when the template is non-trivial or the user's scenario is underspecified.

## Scenario Checklist

Capture these items before generating rows:

- business object: customer, account, order, merchant, employee, product, transaction
- row count
- valid date range
- amount distribution
- statuses or lifecycle states
- geographic or organizational scope
- whether data should look realistic, synthetic, minimal, or stress-test oriented

## Field Mapping Heuristics

- Map names ending with `编码`, `编号`, `代码`, `Code`, or `ID` to stable identifiers, not free text.
- Map names ending with `名称`, `Name`, or `描述` to human-readable labels.
- Map columns containing `日期`, `时间`, `Date`, or `Time` to one consistent date or datetime format across all rows.
- Map `金额`, `余额`, `数量`, `单价`, `税额`, or similar numeric columns to values with realistic ranges and consistent decimal precision.
- Map `状态`, `类型`, `渠道`, `币种`, `地区`, `组织`, or similar enum-like columns to a small consistent value set.

## Output Checks

- Keep headers unchanged.
- Keep row width identical to the template width.
- Ensure related columns stay logically consistent within a row.
- Avoid mixing incompatible currencies, departments, or lifecycle states unless the scenario explicitly calls for it.
- Keep primary identifiers unique unless the template explicitly models parent-child relationships.

## Failure Cases

Do not pretend certainty when:

- the workbook only contains blank headers with no business context
- required code dictionaries are missing
- the target import sheet cannot be distinguished from instruction sheets
- the user asks for "real" production data that is not available locally

In those cases, state the blocker and request the smallest missing detail.
