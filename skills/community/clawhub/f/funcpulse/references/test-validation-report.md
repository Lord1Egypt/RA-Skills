# 业务测试验证报告模板

## 业务测试验证报告模板

```markdown
# 业务测试验证报告: {{FUNCTION_NAME}}

**远程记录地址**: {{REMOTE_REPORT_URL}}
**日期**: {{REPORT_DATE}}
**测试人员**: {{TESTER_NAME}}
**版本**: {{VERSION_INFO}}
**代码库地址**: {{CODEBASE_URL}}
**涉及的仓库**: {{INVOLVED_REPOS}}

## 执行摘要

- **测试用例总数**: {{TEST_CASE_COUNT}}
- **已覆盖用例**: {{COVERED_CASES}}
- **未覆盖用例**: {{UNCVERED_CASES}}
- **测试覆盖率**: {{COVERAGE_RATE}}
- **关键发现**: {{KEY_FINDINGS}}

## 需求-代码映射分析

{{REQUIREMENT_CODE_MAPPING}}

## 测试用例验证结果

{{TEST_CASE_RESULTS}}

## 未覆盖需求分析

{{UNCOVERED_REQUIREMENTS}}

## 缺陷列表

### [关键] {{CRITICAL_DEFECT_TITLE}}
- **关联需求**: {{CRITICAL_REQUIREMENT_ID}}
- **关联用例**: {{CRITICAL_TEST_CASE_ID}}
- **位置**: {{CRITICAL_DEFECT_LOCATION}}
- **重现步骤**:
  {{CRITICAL_DEFECT_STEPS}}
- **期望结果**: {{CRITICAL_DEFECT_EXPECTED}}
- **实际结果**: {{CRITICAL_DEFECT_ACTUAL}}
- **影响**: {{CRITICAL_DEFECT_IMPACT}}
- **修复建议**: {{CRITICAL_DEFECT_FIX}}

### [高] {{HIGH_DEFECT_TITLE}}
- **关联需求**: {{HIGH_REQUIREMENT_ID}}
- **关联用例**: {{HIGH_TEST_CASE_ID}}
- **位置**: {{HIGH_DEFECT_LOCATION}}
- **描述**: {{HIGH_DEFECT_DESCRIPTION}}
- **影响**: {{HIGH_DEFECT_IMPACT}}
- **修复建议**: {{HIGH_DEFECT_FIX}}

### [中] {{MEDIUM_DEFECT_TITLE}}
- **关联需求**: {{MEDIUM_REQUIREMENT_ID}}
- **关联用例**: {{MEDIUM_TEST_CASE_ID}}
- **详情**: {{MEDIUM_DEFECT_DETAILS}}

### [低] {{LOW_DEFECT_TITLE}}
- **关联需求**: {{LOW_REQUIREMENT_ID}}
- **关联用例**: {{LOW_TEST_CASE_ID}}
- **详情**: {{LOW_DEFECT_DETAILS}}

## 需求-用例-代码追踪矩阵

{{TRACEABILITY_MATRIX}}

## 代码变更-测试用例覆盖分析

### 变更概览
- **总变更数**: {{TOTAL_CHANGES}}
- **已覆盖变更**: {{COVERED_CHANGES}}
- **未覆盖变更**: {{UNCOVERED_CHANGES}}
- **变更覆盖率**: {{CHANGE_COVERAGE_RATE}}

### 未覆盖变更详情
{{UNCOVERED_CHANGES_DETAILS}}

### 变更-用例映射矩阵
{{CHANGE_CASE_MAPPING_MATRIX}}

## 建议

{{PRIORITIZED_RECOMMENDATIONS}}
```

## 模板变量说明（新增）

- `{{TOTAL_CHANGES}}` - 代码变更总数
- `{{COVERED_CHANGES}}` - 已覆盖的变更数
- `{{UNCOVERED_CHANGES}}` - 未覆盖的变更数
- `{{CHANGE_COVERAGE_RATE}}` - 变更覆盖率百分比
- `{{UNCOVERED_CHANGES_DETAILS}}` - 未覆盖变更的详细分析
- `{{CHANGE_CASE_MAPPING_MATRIX}}` - 变更与测试用例的映射矩阵

## 模板变量说明

- `{{FUNCTION_NAME}}` - 被验证的功能名称
- `{{REMOTE_REPORT_URL}}` - 远程记录地址（报告上传成功后由服务端返回）
- `{{REPORT_DATE}}` - 报告生成日期 (YYYY-MM-DD格式)
- `{{TESTER_NAME}}` - 测试人员姓名
- `{{VERSION_INFO}}` - 版本信息 (分支及版本号)
- `{{CODEBASE_URL}}` - 主代码库URL
- `{{INVOLVED_REPOS}}` - 涉及的代码仓库列表
- `{{TEST_CASE_COUNT}}` - 测试用例总数
- `{{COVERED_CASES}}` - 已覆盖的测试用例数量
- `{{UNCVERED_CASES}}` - 未覆盖的测试用例数量
- `{{COVERAGE_RATE}}` - 测试覆盖率百分比
- `{{KEY_FINDINGS}}` - 关键发现摘要
- `{{REQUIREMENT_CODE_MAPPING}}` - 需求与代码映射分析
- `{{TEST_CASE_RESULTS}}` - 测试用例验证结果
- `{{UNCOVERED_REQUIREMENTS}}` - 未覆盖需求分析
- `{{CRITICAL_DEFECT_*}}` - 关键缺陷相关信息
- `{{HIGH_DEFECT_*}}` - 高优先级缺陷相关信息
- `{{MEDIUM_DEFECT_*}}` - 中优先级缺陷相关信息
- `{{LOW_DEFECT_*}}` - 低优先级缺陷相关信息
- `{{TRACEABILITY_MATRIX}}` - 需求-用例-代码追踪矩阵
- `{{PRIORITIZED_RECOMMENDATIONS}}` - 按优先级排序的建议列表

## 使用说明

1. 所有模板变量必须被实际数据替换，不能保留占位符
2. 表格格式必须保持一致，包括对齐方式
3. 严重程度必须使用标准定义：CRITICAL、HIGH、MEDIUM、LOW
4. 建议必须按优先级排序：立即、高优先级、中优先级、低优先级
5. 每个缺陷必须关联到具体的需求ID和测试用例ID
6. 追踪矩阵必须清晰展示需求、用例和代码实现的对应关系
