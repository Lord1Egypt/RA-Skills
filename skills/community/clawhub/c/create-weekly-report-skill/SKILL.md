# create_weekly_report_skill

## Description
This skill generates a weekly report based on the given tasks and saves it as a Markdown file.

## Input Schema
- `tasks`: An array of strings representing the tasks completed during the week.
  Example: `["完成用户调研报告", "修复登录页面的bug", "参加产品评审会"]`

## Output Schema
- `report_path`: The path to the generated weekly report file.

## Actions
1. **Generate Weekly Report**: Use the provided tasks to generate a Markdown-formatted weekly report.
2. **Save Report**: Write the generated report to a specified file path.

## Example Usage
```json
{
  "tasks": [
    "完成用户调研报告",
    "修复登录页面的bug",
    "参加产品评审会"
  ]
}
