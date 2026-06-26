# 共享规范

**适用角色**: 所有子代理

---

## 项目归属与防范

⚠️ 提示词首行的 **项目归属** 声明了你正在为哪个项目工作。

| 规则 | 说明 |
|------|------|
| 确认项目路径 | 执行前 `cd {project_path}` 确认工作目录 |
| 产出物写入项目目录 | 代码、文档等产出物写入任务单指定的输出文件路径 |
| JSON结果写入临时目录 | `/tmp/autocraft_output/{task_id}_*_result.json` |
| 路径基于项目根目录 | 所有文件路径相对于 `project_path` 解析 |

---

## 任务单信息查询

如需确认任务单原始信息（对提示词内容有疑问时），可调用API查询：

```bash
# 查询任务完整信息
curl -s http://localhost:9001/api/v2/tasks/{task_id}/status | python3 -m json.tool

# 只查看关键字段
curl -s http://localhost:9001/api/v2/tasks/{task_id}/status | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('project_path:', d.get('input_data', {}).get('project_path', '未知'))
print('requirements:', d.get('input_data', {}).get('requirements', '无'))
print('expected_output_files:', d.get('input_data', {}).get('expected_output_files', []))
"
```

---

## 产出物与结果文件（两个目录，职责分离）

**项目目录**(产出物): 按任务单 `expected_output_files` 指定的路径写入

**临时目录**(JSON结果文件，引擎通信用): `/tmp/autocraft_output/`

⚠️ 不要把产出物(代码/文档)写入 `/tmp/autocraft_output/`，该目录仅供引擎通信。

---

## 执行结果JSON格式

**路径**: `/tmp/autocraft_output/{task_id}_execution_result.json`

```json
{
  "success": true,
  "task_no": "M01-BE-L2-001",
  "task_name": "任务名称",
  "execution_log": "执行过程描述",
  "output_files": ["/data/projects/{project}/backend/xxx.py"],
  "key_changes": ["关键变更列表"],
  "issues": [],
  "test_raw_records": [],
  "execution_time_minutes": 5
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| success | ✅ | 任务是否成功完成 |
| task_no | ✅ | 任务编号 |
| execution_log | ✅ | 执行过程描述 |
| output_files | ✅ | 实际生成的文件路径列表 |
| key_changes | ✅ | 关键变更列表 |
| issues | ✅ | 发现的问题列表（无则空数组） |
| test_raw_records | BUILD-TEST必填 | 测试原始运行记录 |
| execution_time_minutes | ✅ | 执行耗时(分钟) |

---

## 验证结果JSON格式

**路径**: `/tmp/autocraft_output/{task_id}_verification_result.json`

```json
{
  "verification_success": true,
  "verification_report": "完整验证报告",
  "dimension_results": {
    "完整性": "PASS",
    "正确性": "PASS",
    "可运行性": "PASS",
    "一致性": "PASS",
    "安全性": "PASS",
    "架构合理性": "PASS"
  },
  "issues_found": [],
  "improvements_suggested": [],
  "design_document_check": {
    "documents_checked": ["API设计-v1.2.md"],
    "coverage_percentage": 100,
    "missing_endpoints": [],
    "missing_functions": [],
    "field_mismatches": []
  }
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| verification_success | ✅ | 任一维度FAIL则为false |
| dimension_results | ✅ | 6维度判定结果 |
| issues_found | ✅ | 发现的问题列表 |
| improvements_suggested | ✅ | 改进建议列表 |
| design_document_check | 有input_files时必填 | 设计文档对照检查结果 |

---

## 铁律（所有子代理必须遵守）

1. **必须写JSON结果文件** — 引擎通过读取JSON获取结果，无需手动调用API
2. **一次性执行** — 完成后立即结束
3. **忽略之前的上下文** — 只关注当前任务
4. **产出物必须真实存在** — 不写不存在的文件路径
5. **有疑问必须质疑** — 遇到模糊、有歧义、或与实际代码不一致的地方，在日志中标注⚠️疑问点，说明理解和假设
6. **基于事实评估** — 验证时检查真实文件，不编造结果
7. **不改代码让测试通过** — TEST-RUN角色不得修改任何代码
8. **不要调webhook** — 结果由引擎自动读取

---

## 常用命令

```bash
# 运行后端测试
cd /data/projects/{project} && python -m pytest tests/ -v --tb=short

# 运行前端测试
cd /data/projects/{project} && npx vitest run tests/frontend/ --reporter=verbose

# 运行lint
cd /data/projects/{project} && python -m ruff check .
```
