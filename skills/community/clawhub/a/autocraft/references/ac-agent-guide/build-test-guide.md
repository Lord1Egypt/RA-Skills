# BUILD-TEST 执行规范

**适用**: 执行子代理执行BUILD-TEST任务时使用（L2/L3）
**核心原则**: 只写测试代码，不运行测试

---

## BUILD-TEST 职责

```
写测试代码 → 保存到指定路径 → 生成断言报告 → 写JSON结果 → 结束
```

**产出物**: 测试代码文件 + 断言报告

---

## 执行流程

### 1. 读取输入

- 读取任务单中的设计文档、测试方案、组件规范
- 读取被测组件/模块的源代码
- **重点读取测试方案中的预设数据和预期结果**

### 2. 编写测试代码

按照设计文档和测试方案编写测试，注意：

#### 后端L2测试（pytest + 真实数据库）

- **必须使用真实数据库**，禁止mock数据库
- **必须按测试方案文档插入预设数据**，禁止自己编造数据
- **必须按测试方案文档验证预期结果**，禁止自己推断预期
- 每个测试用例的断言必须精确验证数据内容，不能只验证状态码
- AI服务真实调用，超时跟生产配置走（从config.py/环境变量读取）
- AI调用超时标记为SKIP，不阻塞其他测试

#### 前端L3测试（Playwright + 真实浏览器）

- **使用真实浏览器**，禁止jsdom/vitest
- **必须按测试方案文档验证页面数据**，不能只验证页面能渲染
- 断言必须验证用户可见的内容（文本、数量、状态）
- L3-S：单功能测试，打开目标页面直接测试
- L3-M：单模块流程测试，覆盖完整用户操作
- L3-L：跨模块场景测试，验证数据流转正确性

### 3. 生成断言报告

为每个测试用例生成断言报告，格式：

```
TC-{用例ID}: {断言数量} assertions
  - assert {断言内容1}           ← 精确/⚠️太弱
  - assert {断言内容2}           ← 精确
  ...
```

标记规则：
- 验证具体数据值 → 标记"精确"
- 只验证状态码/非空 → 标记"⚠️太弱"

### 4. 保存文件

将测试文件和断言报告保存到任务单指定的产出物路径。

### 5. 写JSON结果

写入 `/tmp/autocraft_output/{task_id}_execution_result.json`：

```json
{
  "success": true,
  "task_no": "任务编号",
  "task_name": "任务名称",
  "execution_log": "编写了N个测试文件，覆盖X个测试用例",
  "output_files": ["测试代码路径", "断言报告路径"],
  "key_changes": ["新建 xxx 测试文件"],
  "issues": [],
  "test_case_count": {
    "文件名": 用例数
  },
  "assertion_report": {
    "TC-001": {"count": 3, "weak": 0},
    "TC-002": {"count": 1, "weak": 1}
  }
}
```

---

## ⛔ 铁律

1. **不得运行测试** — 运行测试是TEST-RUN的职责
2. **不得修改程序代码** — 只写测试代码
3. **不得自己编造预设数据** — 严格照搬测试方案文档
4. **不得自己推断预期结果** — 严格照搬测试方案文档
5. **不得降低断言标准** — 禁止只验证状态码不验证数据
6. **后端L2禁止mock数据库** — 使用真实数据库
7. **前端L3禁止使用vitest/jsdom** — 使用Playwright
8. **测试代码必须能独立运行** — import路径正确、依赖完整

---

## 断言质量标准

### 后端L2

| 设计文档要求 | ✅ 正确断言 | ❌ 降级断言 |
|-------------|-----------|-----------|
| 筛选返回正确结果 | `assert data[0]["subject"] == "数学"` | `assert response.status_code == 200` |
| 数据落库正确 | `assert db_record.status == "completed"` | `assert db_record is not None` |
| 分页返回总数 | `assert pagination["total"] == 3` | `assert "pagination" in response.json()` |
| 错误码正确 | `assert data["code"] == "VALIDATION_ERROR"` | `assert response.status_code == 400` |

### 前端L3

| 设计文档要求 | ✅ 正确断言 | ❌ 降级断言 |
|-------------|-----------|-----------|
| 列表显示正确数量 | `expect(items).toHaveCount(3)` | `expect(page).toBeVisible()` |
| 筛选标签显示 | `expect(tag).toContainText('数学')` | `expect(tag).toBeVisible()` |
| 对话显示AI回复 | `expect(reply).not.toBeEmpty()` | `expect(replyArea).toBeVisible()` |
| 状态显示完成 | `expect(status).toContainText('已完成')` | `expect(status).toBeVisible()` |
