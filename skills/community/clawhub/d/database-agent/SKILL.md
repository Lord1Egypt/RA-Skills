---
name: database-agent
description: 本技能应用于 Java 后端开发场景中的数据库操作。提供慢 SQL 智能分析、表结构规范巡检、安全数据订正与测试数据自动生成的自动化辅助能力。当用户请求数据库优化、schema 验证、安全数据更新或需要为数据库生成测试数据时使用此技能。
---

# Database Agent 数据库智能助手

## 概述

本技能为 Java 后端开发提供智能数据库辅助能力，支持慢 SQL 分析、表结构规范巡检、安全数据订正和测试数据生成等自动化功能。可自动识别索引缺失、全表扫描、字段不规范等问题，生成优化建议与修复脚本；在数据订正时自动校验风险，防止无 WHERE 条件更新删除；并根据表结构智能生成业务合规的测试数据，大幅提升数据库开发与维护效率。

## 核心能力

### 1. 慢 SQL 分析

**何时使用：** 用户报告慢查询、性能问题或需要 SQL 优化时。

**功能特性：**
- 解析 SQL 执行计划，识别性能瓶颈
- 检测全表扫描、缺失索引和低效 JOIN
- 分析慢查询日志，定位问题查询
- 生成优化建议和索引创建脚本

**使用方法：**
1. 使用 `scripts/analyze_slow_sql.py` 分析 SQL 语句或执行计划
2. 参考 `references/sql_optimization_rules.md` 了解优化模式
3. 生成包含具体建议的报告

**示例场景：**
- "分析这条慢 SQL：SELECT * FROM orders WHERE user_id = ?"
- "优化这个执行太慢的查询"
- "查找这个查询为什么做全表扫描"

### 2. 表结构规范巡检

**何时使用：** 用户需要根据最佳实践和标准验证数据库 schema 时。

**功能特性：**
- 检查字段命名规范（snake_case、无保留字）
- 验证数据类型和长度
- 检测缺失的主键或索引
- 识别不合规的默认值或可空字段
- 生成规范报告和修复脚本

**使用方法：**
1. 使用 `scripts/check_schema_compliance.py` 检查表结构
2. 参考 `references/database_standards.md` 了解规范规则
3. 使用 `scripts/generate_report.py` 导出结果到 Excel 报告

**示例场景：**
- "检查这个表结构是否符合最佳实践"
- "验证我们的数据库 schema 是否符合标准"
- "为所有表生成规范报告"

### 3. 安全数据订正

**何时使用：** 用户需要安全地执行批量数据更新或删除时。

**功能特性：**
- 验证 UPDATE/DELETE 语句的安全风险
- 检测缺失的 WHERE 子句（防止全表更新/删除）
- 识别危险操作（如更新主键）
- 要求对高风险操作进行确认
- 生成备份和回滚脚本

**使用方法：**
1. 使用 `scripts/validate_data_correction.py` 检查 SQL 安全性
2. 参考 `references/safe_operation_guidelines.md` 了解风险模式
3. 执行前必须生成回滚脚本

**示例场景：**
- "将所有用户状态更新为激活"
- "删除 1 年前的记录"
- "帮我安全地订正这些数据"

**关键安全规则：**
- 永远不要执行没有 WHERE 子句的 UPDATE/DELETE
- 始终生成备份脚本
- 对影响超过 1000 行的操作要求明确确认
- 记录所有数据订正操作

### 4. 测试数据生成

**何时使用：** 用户需要用真实数据填充测试环境时。

**功能特性：**
- 根据表结构智能生成测试数据
- 遵循外键关系
- 支持自定义数据模式（邮箱、电话、日期）
- 生成业务合规数据（如有效的订单金额、真实的姓名）
- 按正确的依赖顺序创建数据

**使用方法：**
1. 使用 `scripts/generate_test_data.py` 创建测试数据
2. 参考 `references/test_data_patterns.md` 了解数据生成规则
3. 通过 JSON 配置文件配置数量和模式

**示例场景：**
- "为数据库生成 1000 个测试用户"
- "创建包含真实数据的样本订单"
- "用样本数据填充测试环境"

## 工作流程

### SQL 分析任务
1. 接收 SQL 语句或执行计划
2. 运行 `scripts/analyze_slow_sql.py` 识别问题
3. 生成优化建议
4. 可选地创建索引创建脚本

### Schema 验证任务
1. 连接数据库或接收 DDL 语句
2. 运行 `scripts/check_schema_compliance.py`
3. 生成规范报告
4. 可选地生成修复脚本

### 数据订正任务
1. 接收 UPDATE/DELETE SQL 语句
2. 运行 `scripts/validate_data_correction.py` 进行安全检查
3. 如果安全，生成备份脚本
4. 要求用户确认
5. 执行并记录日志

### 测试数据生成任务
1. 接收表结构或连接数据库
2. 配置数据模式和数量
3. 运行 `scripts/generate_test_data.py`
4. 按依赖顺序生成 INSERT 语句

## 资源

### scripts/ 脚本目录
- `analyze_slow_sql.py` - 分析 SQL 性能并生成优化建议
- `check_schema_compliance.py` - 根据标准验证表结构
- `validate_data_correction.py` - 验证数据修改操作的安全性
- `generate_test_data.py` - 根据表结构生成智能测试数据
- `generate_report.py` - 导出分析结果到 Excel 格式
- `database_connector.py` - JDBC 数据库连接工具

### references/ 参考文档
- `sql_optimization_rules.md` - SQL 优化最佳实践和模式
- `database_standards.md` - 数据库命名约定和设计标准
- `safe_operation_guidelines.md` - 数据操作的风险模式和安全规则
- `test_data_patterns.md` - 数据生成模式和业务规则

### assets/ 资产文件
- `compliance_rules.json` - 可配置的规范规则定义
- `test_data_config.json` - 测试数据生成配置模板
- `report_template.xlsx` - 规范报告的 Excel 报告模板

## 重要提示

- 执行数据库操作前始终验证用户权限
- 记录所有操作以便审计追踪
- 为任何数据修改生成回滚脚本
- 首先在非生产环境中测试生成的脚本
- 遵守数据库连接限制和查询超时
- 对大数据量使用批量操作
