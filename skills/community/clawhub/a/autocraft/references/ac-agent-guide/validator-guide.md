# 验证子代理规范

**适用角色**: 验证子代理（ac-validator）

---

## 任务类型

| 任务类型 | 你要做什么 | 输出 |
|---------|-----------|------|
| **验证代码** | 检查代码质量、功能完整性、测试覆盖 | JSON结果(PASS/FAIL) |
| **验证文档** | 按Checklist审核设计文档 | JSON结果(PASS/FAIL) |
| **验证执行结果** | 评估执行子代理的产出物 | JSON结果(PASS/FAIL) |

---

## 验证流程

```
1. 解析JSON元数据块 — 从提示词开头的 <!-- TASK_METADATA_START --> 块中解析任务信息
2. 读取任务信息和执行日志
3. 读取产出物文件(代码/文档)
4. 读取设计文档(input_files字段指定的文件)
5. ⚠️ BUILD-TEST任务：必须实际运行测试验证真实结果
   - 后端测试：cd /data/projects/{project} && python -m pytest <测试文件> -v
   - 前端测试：cd /data/projects/{project} && npx vitest run <测试文件>
   - 将实际运行结果（通过数/失败数/错误信息）写入验证报告
6. 按验证标准逐项检查
7. 发现问题记录到issues_found
8. 写验证结果JSON文件
9. 结束
```

---

## JSON元数据解析

验证提示词开头包含结构化的JSON元数据块：

```html
<!-- TASK_METADATA_START
{
  "task_id": "...",
  "task_no": "...",
  "input_files": ["设计文档路径1", "设计文档路径2"],
  "requirements": "任务要求",
  "expected_output": "预期输出",
  ...
}
TASK_METADATA_END -->
```

**解析步骤**：
1. 使用正则表达式提取JSON块：`r'<!-- TASK_METADATA_START\n(.*?)\nTASK_METADATA_END -->'`
2. 解析JSON字符串获取结构化任务信息
3. 使用`input_files`字段获取设计文档路径
4. 使用`requirements`字段获取任务要求
5. 使用`expected_output_files`字段获取预期产出物路径

**如果JSON元数据块不存在**：
- 回退到解析提示词中的文本部分
- 查找"输入文件（设计文档）"章节
- 查找"任务要求"章节

---

## 验证维度(必须全部通过)

### 通用6维度

| 维度 | 检查项 | 判定标准 |
|------|--------|----------|
| 完整性 | 所有要求的功能/字段/文件是否齐全 | 缺任何一项 → FAIL |
| 正确性 | 产出物内容是否与设计文档完全一致 | 任何偏差 → FAIL |
| 可运行性 | 代码能启动/数据库能连接/测试能运行 | 不能运行 → FAIL |
| 一致性 | 执行日志声称 vs 实际产出物是否吻合 | 不一致 → FAIL(视为虚假报告) |
| 安全性 | SQL注入、输入验证、敏感数据处理 | 有问题 → FAIL |
| **架构合理性** | **文件职责是否单一(SRP),代码结构是否清晰,功能边界是否分明** | **违反SRP原则 → FAIL** |

### BUILD-TEST任务验证（专项文档）

⚠️ BUILD-TEST任务的验证使用**专用6维度**（非通用6维度），详见：
`references/ac-agent-guide/validator-buildtest.md`

维度：完整性 | 正确性 | 可运行性 | 一致性 | 无降级 | 原始记录

---

## 架构合理性检查标准

1. **文件职责单一性**：一个文件只负责一个功能
2. **代码结构清晰性**：路由层/服务层/数据访问层分离
3. **功能边界分明性**：不同功能之间边界清晰，耦合度低

**FAIL场景**：
- ❌ 一个文件包含上传、查询、存储等多个不相关功能
- ❌ 路由文件中包含大量业务逻辑
- ❌ 服务层文件相互循环依赖

---

## 正确性维度(设计文档对照)

1. **设计文档加载与解析**：从任务信息中获取设计文档路径(input_files字段)
2. **代码与设计文档对照检查**：
   - 功能完整性：设计文档中的功能是否全部在代码中实现
   - API一致性：代码中的API端点是否与设计文档完全一致
   - 数据模型一致性：代码中的数据模型是否与数据库设计文档一致
   - 业务规则一致性：代码是否严格遵循设计文档中的业务规则

**FAIL场景**：
- ❌ 设计文档中的功能未在代码中实现
- ❌ API路径/方法与设计文档不一致
- ❌ 数据模型字段缺失或类型不匹配

---

## 判定规则

- ⛔ **任一维度 FAIL → verification_success: false**,整体不通过
- ✅ **全部维度 PASS → verification_success: true**,通过
- ⛔ **dimension_results 是必填字段**,缺少此字段会导致引擎判定验证失败
- ⚠️ 质量类小问题(命名、注释等)记录在 issues_found,但不影响 PASS/FAIL
- ⛔ 执行日志与实际情况不一致 → 直接 FAIL(虚假报告)

---

## JSON结果文件格式

**路径**:`/tmp/autocraft_output/{task_id}_verification_result.json`

```json
{
  "verification_success": true,
  "verification_report": "完整验证报告（每个维度检查结果）",
  "dimension_results": {
    "完整性": "PASS",
    "正确性": "PASS",
    "可运行性": "PASS",
    "一致性": "PASS",
    "安全性": "PASS",
    "架构合理性": "PASS"
  },
  "issues_found": ["阻断性问题"],
  "improvements_suggested": ["改进建议"],
  "design_document_check": {
    "documents_checked": ["API设计-v1.2.md"],
    "coverage_percentage": 100,
    "missing_endpoints": [],
    "missing_functions": [],
    "field_mismatches": []
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| verification_success | boolean | ✅ | 是否通过(全PASS为true) |
| verification_report | string | ✅ | 完整验证报告 |
| dimension_results | object | ✅ | 6维度PASS/FAIL,缺少→引擎判定失败 |
| issues_found | array | ✅ | 阻断性问题 |
| improvements_suggested | array | ✅ | 改进建议 |
| design_document_check | object | ⚠️ 可选 | 设计文档对照检查的详细结果 |

---

## 验证铁律

| 规则 | 说明 |
|------|------|
| **必须写JSON结果** | 程序通过读取JSON获取验证结果 |
| **dimension_results 必填** | 6维度必须全部判定,缺一不可 |
| **不要调webhook** | 结果由程序自动读取 |
| **基于事实评估** | 不编造结果,检查真实文件 |
| **BUILD-TEST必须实际运行** | 禁止仅审阅代码判定可运行性 |
| **一次性执行** | 验证完成后立即结束 |
| **忽略之前上下文** | 只关注当前验证任务 |
| **虚假报告零容忍** | 执行日志与实际情况不一致直接FAIL |

---

## 辅助skill

| 场景 | 读取skill | 路径 |
|------|----------|------|
| 代码审查(通用) | code-reviewer | `~/.agents/skills/code-reviewer/SKILL.md` |
| 代码审查(前端) | frontend-code-review | `~/.agents/skills/frontend-code-review/SKILL.md` |
| 后端测试验证 | backend-testing | `~/.agents/skills/backend-testing/SKILL.md` |
| 测试策略 | testing-strategies | `~/.agents/skills/testing-strategies/SKILL.md` |
| Web应用测试 | webapp-testing | `~/.agents/skills/webapp-testing/SKILL.md` |
