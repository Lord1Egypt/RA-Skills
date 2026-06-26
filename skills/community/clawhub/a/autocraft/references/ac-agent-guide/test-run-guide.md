# TEST-RUN 执行规范

**适用**: 执行子代理执行TEST-RUN任务时使用（L2/L3）
**核心原则**: 独立运行测试，如实记录结果，不修改任何代码

---

## TEST-RUN 职责

```
运行测试 → 记录原始结果 → 生成断言报告 → 结束
```

**产出物**: 测试运行报告

---

## 执行流程

### 1. 读取输入

- 读取任务单中的测试命令和测试文件列表
- 读取断言报告（BUILD-TEST产出）

### 2. 运行测试

**如实运行，不改任何代码**：

```bash
# 后端L2
cd /data/projects/{project}/backend && python -m pytest tests/L2/ -v

# 前端L3
cd /data/projects/{project} && npx playwright test tests/e2e/ --reporter=list
```

### 3. 记录结果

如实记录每个测试的通过/失败/SKIP状态，**不分析、不判断、不修改**：

写入 `/tmp/autocraft_output/{task_id}_execution_result.json`：

```json
{
  "success": true,
  "task_no": "任务编号",
  "task_name": "任务名称",
  "execution_log": "运行了N个测试文件，X通过Y失败Z跳过",
  "output_files": [],
  "issues": [],
  "test_raw_records": [
    {
      "run_index": 1,
      "command": "实际运行的命令",
      "total": 27,
      "passed": 20,
      "failed": 5,
      "skipped": 2,
      "failures": [
        {
          "test_name": "测试完整名称",
          "file": "测试文件路径",
          "error": "错误信息原文",
          "error_type": "AssertionError / TypeError / ReferenceError 等",
          "classification": "code_issue / test_issue / env_issue"
        }
      ]
    }
  ]
}
```

### 4. 失败分类

对每个失败的测试，给出初步分类（仅分类，不修复）：

| 分类 | 判断标准 | 示例 |
|------|---------|------|
| code_issue | 测试逻辑正确，程序返回了错误结果 | API返回了空列表但应该返回3条数据 |
| test_issue | 测试代码有误（路径错误、断言写错） | import路径不存在、断言值与文档不一致 |
| env_issue | 环境配置问题 | 数据库未初始化、服务未启动 |

### 5. 结束

**不要修复任何问题！不要修改任何代码！**

---

## ⛔ 铁律

1. **不得修改测试代码** — 不是你的职责
2. **不得修改程序代码** — 绝对禁止
3. **不得跳过失败测试重跑** — 一次运行，如实记录
4. **不得尝试修复问题** — 即使看起来很简单
5. **AI调用超时=SKIP** — 不标记为FAIL，不重试

---

## 前端 vs 后端测试识别

| 特征 | 后端L2 (pytest) | 前端L3 (Playwright) |
|------|-----------|-----------|
| 文件后缀 | test_*.py / *_test.py | *.spec.ts / *.test.ts |
| 运行命令 | `python -m pytest <文件>` | `npx playwright test <文件>` |
| 目录 | tests/L2/ | tests/e2e/ |
| 浏览器 | 不需要 | 需要真实浏览器 |
