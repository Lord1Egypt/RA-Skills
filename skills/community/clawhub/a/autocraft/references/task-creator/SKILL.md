---
name: task-creator
description: AutoCraft任务单创建标准流程。指导主代理正确创建任务单并导入AutoCraft系统，包括数据格式规范、必填字段、workflow_type映射、输入文件配置等。触发场景：需要为AutoCraft执行引擎创建任务单时。
---

# AutoCraft 任务单创建标准流程

**版本：** v1.0  
**更新：** 2026-05-12

---

## 创建方式

### 方式1：API创建（推荐）

通过 `/api/v2/tasks/` API 批量创建任务单：

```bash
curl -X POST http://localhost:9001/api/v2/tasks/ \
  -H "Content-Type: application/json" \
  -d '[{
    "task_no": "M02-BE-001",
    "task_name": "创建知识图谱API端点",
    "task_type": "BUILD",
    "plan_id": "plan_xxx",
    "status": "pending",
    "input_data": {
      "workflow_type": "BUILD-CODE",
      "project_path": "/data/projects/deeptutor-lite",
      "input_files": [
        "/data/projects/deeptutor-lite/docs/design/04-技术方案-DeepTutor-Lite.md"
      ],
      "requirements": "创建知识图谱管理API",
      "expected_output": "路由文件，包含所有API端点",
      "expected_output_files": [
        "/data/projects/deeptutor-lite/backend/api/routers/knowledge_graph.py"
      ]
    }
  }]'
```

**返回值**：
```json
{
  "status": "success",
  "created_count": 1,
  "task_ids": [540],
  "errors": null
}
```

**支持批量**：数组中放入多个任务对象即可批量创建。

**错误处理**：如果某个任务创建失败（如task_no重复），会在errors中返回错误信息，其他任务仍正常创建。

### 方式2：直接写数据库（仅调试用）

⚠️ 不推荐日常使用，仅当API不可用时作为备选：

```python
from database import SessionLocal
from models.task_v2 import TaskV2
import json

db = SessionLocal()
task = TaskV2(
    plan_id='<plan_id>',
    task_no='<task_no>',
    task_name='<task_name>',
    task_type='<task_type>',
    status='pending',
    input_data=json.dumps({...}, ensure_ascii=False)  # ⚠️ 必须是JSON字符串
)
db.add(task)
db.commit()
db.refresh(task)
print(f'任务创建成功: id={task.id}')
db.close()
```

---

## 数据库字段规范

| 字段 | 类型 | 数据库必填 | 业务必填 | 说明 |
|------|------|-----------|---------|------|
| `task_no` | VARCHAR(20) | ✅ | ✅ | 任务编号，plan_id内唯一 |
| `task_name` | VARCHAR(200) | ✅ | ✅ | 任务名称 |
| `task_type` | VARCHAR(50) | ⬜ | ✅ | 任务类型，决定子代理读哪个执行指引 |
| `plan_id` | VARCHAR(50) | ⬜ | ✅ | 所属工作计划ID，缺失则前端找不到任务 |
| `status` | VARCHAR(30) | ⬜ | ✅ | 默认"pending" |
| `input_data` | TEXT | ⬜ | ✅ | JSON字符串，核心任务数据，缺失则无法执行 |

⚠️ `input_data` 字段必须是 **JSON字符串**（`json.dumps()`），不是dict对象。

---

## input_data 标准格式

```json
{
  "workflow_type": "BUILD-CODE",
  "project_path": "/data/projects/{project}",
  "input_files": [
    "/data/projects/{project}/docs/design/04-技术方案-{project}.md",
    "/data/projects/{project}/docs/design/07-API设计-{project}.md"
  ],
  "requirements": "详细的任务要求描述，必须具体、可执行",
  "expected_output": "详细的预期输出描述，必须可验证",
  "expected_output_files": [
    "/data/projects/{project}/backend/services/xxx.py"
  ],
  "deliverables": ["产出物描述1", "产出物描述2"],
  "source_file": "/data/projects/{project}/docs/design/04-技术方案-{project}.md"
}
```

### 字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `workflow_type` | ✅ | string | 工作流类型，决定子代理行为（见映射表） |
| `project_path` | ✅ | string | 项目根目录，**绝对路径** |
| `input_files` | ✅ | string[] | 输入文件路径列表，**绝对路径**，至少包含1个设计文档 |
| `requirements` | ✅ | string | 任务要求，必须详细具体 |
| `expected_output` | ✅ | string | 预期输出描述，必须可验证 |
| `expected_output_files` | ✅ | string[] | 预期输出文件路径，**绝对路径** |
| `deliverables` | ⬜ | string[] | 产出物描述列表 |
| `source_file` | ⬜ | string | 主要参考文档路径 |

### ⚠️ 铁律

1. **所有路径必须是绝对路径** — 禁止相对路径
2. **project_path 必须指向正确的项目根目录** — 错误的project_path会导致产出物写入错误位置
3. **input_files 至少包含1个设计文档** — 子代理自行查找设计文档不可靠
4. **requirements 必须详细具体** — 不能是"无具体要求"
5. **expected_output 必须可验证** — 不能是"根据任务描述生成相应产出物"
6. **expected_output_files 必须列出所有预期文件** — 绝对路径

---

## workflow_type 与 task_type 映射

### task_type（数据库字段）

数据库的 `task_type` 字段值可以自定义，但推荐使用标准值：

| task_type | 说明 | 典型场景 |
|-----------|------|---------|
| `BUILD` | 构建/开发 | 创建代码、文件、组件 |
| `BUILD-CODE` | 代码构建 | 编写功能代码 |
| `BUILD-TEST` | 测试构建 | 编写测试用例 |
| `BUILD-ENV` | 环境构建 | 配置开发环境 |
| `TEST-RUN` | 测试执行 | 运行测试，不改代码 |
| `VERIFY` | 验证 | 验证现有代码/文档 |
| `DOC` | 文档 | 编写文档 |
| `DESIGN` | 设计 | 设计方案 |
| `INFRA` | 基础设施 | 项目骨架搭建 |
| `bug_fix` | 修复 | 修复BUG |

### workflow_type（input_data字段）

`workflow_type` 决定子代理读取哪个执行指引子文档：

| workflow_type | 子代理行为 | 对应executor-guide子文档 |
|---------------|-----------|------------------------|
| `BUILD-CODE` | 编写功能代码，写JSON结果 | 执行流程 → BUILD-CODE |
| `BUILD-TEST` | 编写测试代码，**不运行** | 执行流程 → BUILD-TEST |
| `TEST-RUN` | 运行测试，**不改任何代码** | 执行流程 → TEST-RUN |
| `BUILD-ENV` | 配置环境 | 执行流程 → BUILD-ENV |
| `DOC` | 编写文档 | 执行流程 → DOC |
| `DESIGN` | 设计方案 | 执行流程 → DESIGN |
| `FIX` | 修复代码BUG | 执行流程 → BUILD-CODE |
| `VERIFY` | 验证现有代码/文档 | 执行流程 → VERIFY |
| `INFRA` | 基础设施搭建 | 执行流程 → BUILD-CODE |

### 推荐组合

| 场景 | task_type | workflow_type |
|------|-----------|---------------|
| 功能开发 | `BUILD` | `BUILD-CODE` |
| 编写测试 | `BUILD` | `BUILD-TEST` |
| 运行测试 | `TEST-RUN` | `TEST-RUN` |
| 修复BUG | `BUILD-CODE` | `FIX` |
| 文档编写 | `DOC` | `DOC` |
| 环境配置 | `INFRA` | `INFRA` |
| 项目骨架 | `INFRA` | `INFRA` |

---

## input_files 配置指南

### 设计文档路径模板

```
/data/projects/{project}/docs/design/01-PRD-{project}.md
/data/projects/{project}/docs/design/03-系统功能设计-{project}.md
/data/projects/{project}/docs/design/04-技术方案-{project}.md
/data/projects/{project}/docs/design/05-UI设计-{project}.md
/data/projects/{project}/docs/design/06-组件规范-{project}.md
/data/projects/{project}/docs/design/07-API设计-{project}.md
/data/projects/{project}/docs/design/08-数据库设计-{project}.md
```

### 按任务类型选择输入文件

| 任务类型 | 推荐输入文件 |
|---------|-------------|
| 后端API开发 | 技术方案 + API设计 + 数据库设计 |
| 前端组件开发 | UI设计 + 组件规范 + 技术方案 |
| 测试编写 | 技术方案 + API设计 + 对应源码 |
| 环境配置 | 技术方案 |
| 文档编写 | 相关设计文档 |
| BUG修复 | 技术方案 + 对应源码 + 测试报告 |

### ⚠️ input_files 注意事项

- **必须用绝对路径** — ❌ `docs/design/04-xxx.md` ✅ `/data/projects/{project}/docs/design/04-xxx.md`
- **文件必须存在** — 子代理会读取这些文件，不存在会导致执行失败
- **数量适中** — 2-4个设计文档最佳，太多会稀释关键信息
- **优先技术方案** — 技术方案是最核心的输入，几乎所有任务都需要

---

## 执行与验证

### 提交执行

```bash
curl -X POST http://localhost:9001/api/v2/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": <task_id>,
    "model": "glm-5.1",
    "label": "执行任务XXX"
  }'
```

### 查询状态

```bash
curl http://localhost:9001/api/v2/tasks/{task_id}/status
```

### 状态流转

```
pending → in_progress → completed → verifying → verified
                     ↓                          ↓
                   failed              verification_failed
```

- `verified` = 执行+验证全通过 ✅
- `verification_failed` = 执行完成但验证未通过，需检查
- `failed` = 执行失败，可重新执行

### 模型配置

| 用途 | 模型 | 说明 |
|------|------|------|
| 执行 | `glm-5.1` | 代码生成能力强 |
| 执行（备选） | `deepseek-v3.2` | 思考更深入，速度较慢 |
| 验证 | `deepseek-v3.2-thinking` | 自动调用，无需指定 |

---

## 批量创建示例

### 示例：通过API创建一批后端API开发任务

```python
import requests
import json

tasks = [
    {
        "task_no": "M02-BE-001",
        "task_name": "创建知识图谱API端点",
        "task_type": "BUILD",
        "plan_id": "plan_xxx",
        "status": "pending",
        "input_data": {
            "workflow_type": "BUILD-CODE",
            "project_path": "/data/projects/deeptutor-lite",
            "input_files": [
                "/data/projects/deeptutor-lite/docs/design/04-技术方案-DeepTutor-Lite.md",
                "/data/projects/deeptutor-lite/docs/design/07-API设计-DeepTutor-Lite.md",
                "/data/projects/deeptutor-lite/docs/design/08-数据库设计-DeepTutor-Lite.md"
            ],
            "requirements": "创建知识图谱管理API，包含CRUD操作、节点关系管理、图谱可视化数据接口",
            "expected_output": "knowledge_graph.py路由文件，包含所有API端点，代码可被Python导入无报错",
            "expected_output_files": [
                "/data/projects/deeptutor-lite/backend/api/routers/knowledge_graph.py"
            ],
            "deliverables": ["知识图谱路由文件"],
            "source_file": "/data/projects/deeptutor-lite/docs/design/07-API设计-DeepTutor-Lite.md"
        }
    },
    # ... 更多任务
]

response = requests.post(
    "http://localhost:9001/api/v2/tasks/",
    json=tasks,
    headers={"Content-Type": "application/json"}
)
result = response.json()
print(f"创建{result['created_count']}个任务，IDs: {result['task_ids']}")
if result.get('errors'):
    print(f"错误: {result['errors']}")
```

---

## 常见错误与修复

| 错误 | 原因 | 修复 |
|------|------|------|
| 产出物写入autocraft目录 | project_path缺失或错误 | 必须指定正确的project_path |
| 子代理找不到设计文档 | input_files为空或路径错误 | 检查文件存在，用绝对路径 |
| 任务执行失败"无具体要求" | requirements为空 | 必须填写详细的requirements |
| 验证提示"不可验证" | expected_output太模糊 | 必须填写具体的expected_output |
| 文件生成到错误路径 | expected_output_files用了相对路径 | 必须用绝对路径 |
| task_no重复 | 同一plan_id内编号重复 | 确保plan内task_no唯一 |
| input_data存储为dict | ORM存入dict而非JSON字符串 | 必须json.dumps() |

---

## 检查清单

创建任务单前，逐项确认：

- [ ] `task_no` 在 plan_id 内唯一
- [ ] `task_name` 清晰描述任务内容
- [ ] `workflow_type` 与任务性质匹配
- [ ] `project_path` 是正确的绝对路径
- [ ] `input_files` 至少包含1个设计文档，路径为绝对路径且文件存在
- [ ] `requirements` 详细具体，子代理能直接执行
- [ ] `expected_output` 可验证，验证子代理能据此判定
- [ ] `expected_output_files` 列出所有预期产出文件，绝对路径
- [ ] `input_data` 已通过 `json.dumps()` 转为JSON字符串
