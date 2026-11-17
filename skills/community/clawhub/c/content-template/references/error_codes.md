# 错误码定义 - content-template

> 来源: skills/content-template/SKILL.md 异常处理表

## 错误码列表

| 错误码 | 描述 | 处理方案 |
|:-------|:-----|:---------|
| TEMPLATE_NOT_FOUND | 模板不存在 | 返回错误提示 |
| MISSING_VARIABLES | 变量缺失 | 返回缺失变量列表 |
| INVALID_PARAMS | 参数无效 | 返回参数校验错误 |
| INSUFFICIENT_SAMPLE | A/B 测试样本不足 | 返回当前数据,标注样本不足 |
| CT-ERR-05 | 父模板不存在 | 返回错误提示 |
| CT-ERR-06 | Jinja2 不可用 | 降级为简单字符串替换 |
| CT-ERR-07 | Jinja2 语法错误 | 降级为简单字符串替换 |

## 错误处理说明

### TEMPLATE_NOT_FOUND

- 触发条件: template_id 在 `data/content/templates/` 中不存在
- 处理: 返回 `{"success": false, "error": "模板不存在", "code": "TEMPLATE_NOT_FOUND"}`
- 降级: 无降级,需提供有效的 template_id

### MISSING_VARIABLES

- 触发条件: 渲染时缺少必需变量且无默认值
- 处理: 返回缺失变量列表,使用默认值降级渲染 (如有默认值)

### INVALID_PARAMS

- 触发条件: action 参数无效或必填参数缺失
- 处理: 返回参数校验错误信息

### INSUFFICIENT_SAMPLE

- 触发条件: A/B 测试样本量不足以达到统计显著性 (p < 0.05)
- 处理: 返回当前数据,标注"样本不足",不标记优胜模板

### CT-ERR-05 (父模板不存在)

- 触发条件: 模板继承时 `{% extends "parent_id" %}` 中的 parent_id 不存在
- 处理: 返回错误提示,无法渲染继承模板

### CT-ERR-06 (Jinja2 不可用)

- 触发条件: Jinja2 库未安装或导入失败
- 处理: 降级为简单字符串替换 (engine_used="simple_string_replace")
- 影响: 不支持条件渲染/循环/继承,仅支持变量替换

### CT-ERR-07 (Jinja2 语法错误)

- 触发条件: 模板内容包含 Jinja2 语法错误
- 处理: 降级为简单字符串替换 (engine_used="simple_string_replace")
- 影响: 语法错误部分按原样输出或忽略
