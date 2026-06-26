# 项目操作参考

本文档覆盖项目相关的辅助操作：获取工作流状态、任务类型、自定义字段、优先级配置等。

## 获取工作流状态

创建任务时需要 `taskflowstatusId`（只能使用 `kind=start` 的状态）。

```bash
# 获取所有状态
uv run scripts/get_taskflow_statuses.py <projectId>

# 只获取可用于创建任务的初始状态
uv run scripts/get_taskflow_statuses.py <projectId> --only-start

# 按名称搜索
uv run scripts/get_taskflow_statuses.py <projectId> --q '进行中'
```

返回字段：
- `id`：状态 ID（用于 `--taskflowstatus-id`）
- `name`：状态名称
- `kind`：`start`（初始）/ `process`（进行中）/ `end`（完成）

---

## 获取任务类型（ScenarioFieldConfig）

```
GET v3/project/{projectId}/scenariofieldconfig/list
```

```python
import call_api
data = call_api.get(f"v3/project/{project_id}/scenariofieldconfig/list")
```

返回字段：`id`（用于 `--scenariofieldconfig-id`）、`name`、`isDefault`

---

## 获取自定义字段

```
GET v3/project/{projectId}/customfield/list
```

```python
import call_api
data = call_api.get(f"v3/project/{project_id}/customfield/list")
```

**重要**：查询时字段 ID 为 `cfId`，更新时字段 ID 为 `customfieldId`（不同！）

自定义字段类型：`select`、`multiselect`、`text`、`number`、`date`、`member`、`file`

---

## 获取企业优先级配置

```bash
uv run scripts/get_priority_list.py <organizationId>
```

组织 ID 从项目详情获取：
```bash
uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId
```

---

## 项目归档/恢复

```
PUT v3/project/{projectId}/archive     # 归档
PUT v3/project/{projectId}/unarchive   # 恢复
```

```python
import call_api
call_api.put(f"v3/project/{project_id}/archive")
```
