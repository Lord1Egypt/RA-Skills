# DataWorks Open API Cookbook (API Version: 2024-05-18)

Verified patterns, pitfalls, and working code snippets collected from real-world usage.

## Verified API quick reference

| Category   | API                          | Status   | Notes                                         |
| ---------- | ---------------------------- | -------- | --------------------------------------------- |
| Workspace  | ListProjects                 | Verified |                                               |
| Node       | CreateNode                   | Verified | Must use FlowSpec JSON in `spec` param        |
| Node       | GetNode                      | Verified | `spec` field is JSON string; parse to get SQL |
| Node       | UpdateNode                   | Verified | Send full spec back after modification        |
| Node       | ListNodes                    | Verified |                                               |
| File       | ListFiles                    | Verified | Response at `resp.body.data.files`            |
| File       | SubmitFile                   | Verified | `file_id` = node ID (same value)              |
| File       | DeployFile                   | Verified | Must wait ~10 s after SubmitFile              |
| Adhoc      | ExecuteAdhocWorkflowInstance | Verified | One-off DDL/DML/SELECT; `biz_date` = `YYYYMMDD` |
| Workflow   | GetWorkflowInstance          | Verified | Poll `status`; fields: `started_time`/`finished_time` (ms) |
| Schedule   | ListTaskInstances            | Verified | `bizdate` is **millisecond** timestamp        |
| Schedule   | GetTaskInstance              | Verified | Returns full instance attributes              |
| Schedule   | GetTaskInstanceLog           | Verified |                                               |
| Schedule   | RerunTaskInstances           | Verified | Accepts list of IDs                           |
| Resource   | ListResourceGroups           | Verified |                                               |
| DataSource | ListDataSources              | Verified |                                               |
| Quality    | CreateDataQualityRule        | Verified | Needs typed Request sub-objects               |
| Quality    | ListDataQualityRules         | Verified |                                               |
| Workflow   | CreateWorkflowDefinition     | Verified | Creates a workflow container for nodes         |
| Deploy     | GetDeployment                | Verified | Poll pipeline status after deploy              |
| Trigger    | CreateWorkflowInstances      | Verified | Smoke-test / manual trigger                    |
| Trigger    | GetCreateWorkflowInstancesResult | Verified | Poll for workflow creation completion      |
| Workflow   | ImportWorkflowDefinition     | Verified | Create workflow + nodes in one call (CycleWorkflow FlowSpec) |
| DataMap    | GetTable                     | Verified | Get table info by GUID from data map       |
| Quality    | CreateDataQualityScan        | Verified | Create a quality scan task                  |
| Quality    | CreateDataQualityScanRun     | Verified | Execute a quality scan                      |
| Quality    | GetDataQualityRule           | Verified | Get quality rule details                    |
| Quality    | CreateDataQualityEvaluationTask | Verified | Create a monitoring task for a table     |
| Quality    | GetDataQualityEvaluationTask | Verified | Query evaluation task details              |
| Quality    | AttachDataQualityRulesToEvaluationTask | Verified | Bind rules to an evaluation task |
| Quality    | DeleteDataQualityRule        | Verified | Delete a quality rule by ID                 |
| Quality    | DeleteDataQualityEvaluationTask | Verified | Delete an evaluation task by ID           |
| DI         | CreateDIJob                  | Verified | Create data integration job (batch/realtime) |
| DI         | GetDIJob                     | Verified | Get DI job details                          |
| DI         | ListDIJobs                   | Verified | List DI jobs                                |
| DI         | CreateNode (DI type)         | Verified | Create DI offline sync node via FlowSpec    |

## Pitfalls and key discoveries

### 1. Node ID = File ID

`CreateNode` returns a node ID that doubles as the file ID for `SubmitFile` / `DeployFile`. No separate file-creation step is needed.

### 2. SubmitFile → wait → DeployFile

After `SubmitFile`, the internal pipeline needs **~10 seconds** to prepare before `DeployFile` can succeed. Calling `DeployFile` too early returns a "pipeline not ready" error.

```python
submit_resp = client.submit_file(submit_request)
time.sleep(10)   # required wait
deploy_resp = client.deploy_file(deploy_request)
```

### 3. `bizdate` must be a millisecond timestamp string

`ListTaskInstances` expects `bizdate` as a **string of milliseconds since epoch**, not a date string.

```python
from datetime import datetime, timedelta
bizdate = str(int((datetime.now() - timedelta(days=1)).timestamp() * 1000))
```

### 4. `GetNode` spec is a JSON string

The `spec` field returned by `GetNode` is a JSON string (or an SDK object). Always parse before use:

```python
spec = node.spec
if isinstance(spec, str):
    spec_dict = json.loads(spec)
else:
    spec_dict = spec.to_map() if hasattr(spec, 'to_map') else spec
sql = spec_dict['spec']['nodes'][0]['script']['content']
```

### 5. Response parsing varies by API generation

- **New-generation APIs** (ListProjects, ListNodes, etc.): response at `resp.body.paging_info.*`
- **Old-generation APIs** (ListFiles): response at `resp.body.data.*`

Use `to_map()` when the response is an SDK object:

```python
paging = resp.body.paging_info
result = paging.to_map() if hasattr(paging, 'to_map') else paging
```

### 6. CreateDataQualityRule requires typed sub-objects

Do **not** pass dicts; use the SDK model classes:

```python
target = models.CreateDataQualityRuleRequestTarget(
    type="Table",
    database_type="maxcompute",
    table_guid="odps.<project>.<table>",
    partition_spec="dt=$[yyyymmdd-1]",
)
checking_config = models.CreateDataQualityRuleRequestCheckingConfig(type="Fixed")

request = models.CreateDataQualityRuleRequest(
    project_id=PROJECT_ID,
    name="rule_name",
    enabled=True,
    severity="High",
    target=target,
    template_code="SYSTEM:table:table_count:fixed:0",
    checking_config=checking_config,
)
```

### 7. Throttling (Throttling.Resource)

API calls can hit rate limits. Retry with exponential backoff or wait before retrying.

### 8. CreateNode spec: `inputs` and `outputs` are required

Omitting `inputs` or `outputs` from the FlowSpec causes silent failures or scheduling issues. Always include at least:
- `inputs.nodeOutputs`: `[{"data": "project_root", "artifactType": "NodeOutput"}]` (root dependency)
- `outputs.nodeOutputs`: `[{"data": "<name>_output", "artifactType": "NodeOutput", "refTableName": "<name>"}]`

### 9. CycleWorkflow FlowSpec: create workflow + nodes in one call

Besides `CreateNode` (kind: `Node`), you can use `ImportWorkflowDefinition` with kind `CycleWorkflow` to create a full workflow with embedded nodes in a single API call:

```json
{
    "version": "1.1.0",
    "kind": "CycleWorkflow",
    "spec": {
        "name": "<workflow-name>",
        "type": "CycleWorkflow",
        "workflows": [{
            "script": { "path": "root/<workflow-name>", "runtime": {"command": "WORKFLOW"} },
            "trigger": { "type": "Scheduler", "cron": "00 00 02 * * ?", ... },
            "strategy": { "timeout": 0, "instanceMode": "T+1", "rerunMode": "Allowed", "rerunTimes": 3, "rerunInterval": 180000, "failureStrategy": "Break" },
            "name": "<workflow-name>",
            "nodes": [{
                "recurrence": "Normal",
                "script": { "path": "root/<workflow-name>/<node-name>", "runtime": {"command": "ODPS_SQL"}, "content": "SELECT 1;" },
                "trigger": { "type": "Scheduler", "cron": "00 00 02 * * ?", ... },
                "name": "<node-name>",
                "outputs": { "nodeOutputs": [{"data": "<node-name>_output", "artifactType": "NodeOutput"}] }
            }],
            "dependencies": []
        }]
    }
}
```

Call via generalized SDK: `action="ImportWorkflowDefinition"`, body param `Spec` = the JSON above.

### 10. SmokeTest: `WorkflowId` is always 1 for periodic tasks

When triggering a smoke test via `CreateWorkflowInstances`, set `WorkflowId=1` for periodic (scheduled) tasks. This is a fixed convention.

### 11. DeployFile retry on "pipeline not ready"

If `DeployFile` fails with a message containing "流水线未准备好" or "pipeline", wait a few more seconds and retry:

```python
resp = deploy_file(...)
if "流水线未准备好" in error_msg or "pipeline" in error_msg.lower():
    time.sleep(5)
    resp = deploy_file(...)  # retry
```

### 12. SubmitFile: `SkipAllDeployFileExtensions` parameter

Pass `SkipAllDeployFileExtensions='true'` to skip extension checks during submit (e.g. in HTTP-style calls). SDK-style calls may not need this.

### 13. Data service APIs are on older API version

`ListDataServicePublishedApis` and other data-service-related APIs belong to the **old API version `2020-05-18`**, not the current `2024-05-18`. If you need data service capabilities, use the older version endpoint.

### 14. MaxCompute as DI source: use CreateNode, NOT CreateDIJob

**Critical**: `CreateDIJob` API's `SourceDataSourceType` enum does **not include MaxCompute**. To sync data **from** MaxCompute (e.g. MaxCompute → Hologres), you must use `CreateNode` with DI type instead:

| Method | MaxCompute as source | How |
|--------|---------------------|-----|
| `CreateDIJob` | Not supported | `SourceDataSourceType` has no MC option |
| `CreateNode` (DI type) | Supported | `stepType: "odps"` in the DI config |

### 15. DI node: `command` must be `"DI"` with `commandTypeId: 23`

When creating a DI node via `CreateNode`, the `script.runtime` must have:
- `command`: `"DI"` (not `"ODPS_SQL"`)
- `commandTypeId`: `23`
- `script.language`: `"json"` (the content is a JSON DI config, not SQL)

### 16. `biz_date` in ExecuteAdhocWorkflowInstance vs `bizdate` in ListTaskInstances

These two use **completely different formats** — easy to confuse:

| API | Param | Format | Example |
|-----|-------|--------|---------|
| `ExecuteAdhocWorkflowInstance` | `biz_date` | `YYYYMMDD` string | `"20260315"` |
| `ListTaskInstances` | `bizdate` | Millisecond timestamp string | `"1710460800000"` |

### 17. ExecuteAdhocWorkflowInstance: `owner` required at BOTH levels

`owner` must be set on both the task object AND the workflow request itself. Missing either causes an error.

### 18. ExecuteAdhocWorkflowInstance: `client_unique_code` is REQUIRED

Despite being marked optional in some docs, omitting `client_unique_code` causes `MissingClientUniqueCode` error. Always provide one:

```python
import uuid
client_unique_code = str(uuid.uuid4()).replace('-', '')[:20]
```

### 19. ExecuteAdhocWorkflowInstance: `type` must be ALL_CAPS with underscores

```python
# WRONG formats:
type="hologres_sql"    # lowercase
type="HologresSql"     # camelCase
type="holo"            # abbreviation

# CORRECT formats:
type="HOLOGRES_SQL"    # Hologres SQL
type="ODPS_SQL"        # MaxCompute SQL
```

Supported task `type` values:

| type | Engine | Data source example |
|------|--------|---------------------|
| `ODPS_SQL` | MaxCompute SQL | mc_datasource |
| `HOLOGRES_SQL` | Hologres SQL | holo_datasource |
| `MYSQL_SQL` | MySQL SQL | mysql_datasource |
| `POSTGRESQL_SQL` | PostgreSQL SQL | pg_datasource |

### 20. `CreatePipelineRun` is NOT for running nodes — it's for publishing

Common mistake: `CreatePipelineRun` is a **deployment** pipeline (build → check → publish to production), not an execution API. Use the right API for each intent:

| API | Purpose | Flow |
|-----|---------|------|
| `CreatePipelineRun` | Publish node to production | Build → Check → Deploy (slow) |
| `ExecuteAdhocWorkflowInstance` | Run SQL directly | Immediate execution |
| `RerunTaskInstances` | Re-run existing instance | Needs an existing instance |

### 21. Task instance status values

| Status | Meaning |
|--------|---------|
| `NotRun` | Not yet started |
| `WaitTime` | Waiting for scheduled time |
| `WaitResource` | Waiting for available resource slot |
| `Running` | Executing |
| `Success` | Completed successfully |
| `Failure` | Failed |

### 22. Deployment pipeline status values (GetDeployment)

| Status | Meaning |
|--------|---------|
| `Success` | Deploy succeeded |
| `Fail` | Deploy failed |
| `Termination` | Deploy terminated |
| `Cancel` | Deploy cancelled |

### 23. FileType codes (for old-generation CreateFile API)

| Code | Engine |
|------|--------|
| 10 | ODPS SQL |
| 20 | Shell |
| 30 | Python |

### 24. CycleWorkflow FlowSpec: `outputs.tables` for table lineage

In `ImportWorkflowDefinition`, a node's `outputs` can include a `tables` array to register output table lineage:

```json
"outputs": {
    "nodeOutputs": [{"data": "<name>_output", "artifactType": "NodeOutput"}],
    "tables": [{"guid": "odps.<project>.<table>"}]
}
```

### 25. DI sync: target table must exist before running

DI sync will fail with `can not found table "public"."<table>"` if the target table does not exist. Create it first, e.g. via `ExecuteAdhocWorkflowInstance` with `HOLOGRES_SQL`:

```python
sql = "CREATE TABLE IF NOT EXISTS public.<table> (id BIGINT, name TEXT, value DOUBLE PRECISION);"
# Execute via adhoc workflow (see Recipe 3)
```

### 26. DI sync: partition format requires single quotes

For partitioned source tables, the `partition` parameter requires single quotes around the value:

```python
# WRONG
step['parameter']['partition'] = ["dt=20260315"]        # no quotes → error

# CORRECT
step['parameter']['partition'] = ["dt='20260315'"]      # with single quotes
```

Error if missing: "分区信息没有配置.由于源头表:xxx 为分区表, 所以您需要配置其分区信息"

### 27. DI sync: `splitMode` must be `'record'` or `'partition'`

```python
# WRONG
step['parameter']['splitMode'] = False          # → error

# CORRECT
step['parameter']['splitMode'] = 'record'       # split by records
step['parameter']['splitMode'] = 'partition'     # split by partitions
```

### 28. Old API `UpdateFile`: use for direct SQL content updates

The old-generation `UpdateFile` API can update file content directly (without going through FlowSpec):

```python
call_api('UpdateFile', {
    'ProjectId': PROJECT_ID,
    'FileId': file_id,
    'Content': new_sql_content,
    'AutoParsing': 'false',
})
# Then: SubmitFile → DeployFile as usual
```

### 29. HTTP API signing: GET vs POST use different string-to-sign

- POST: `'POST&%2F&' + encoded_params`
- GET: `'GET&%2F&' + encoded_params`

Using the wrong HTTP method prefix causes signature verification failure.

### 30. Deleting DQ rules and evaluation tasks: rules first, then task

Deletion order: **delete rules first**, then delete the evaluation task. Rules can be deleted directly without detaching from the task first.

```python
# 1. Delete rules
call_api('DeleteDataQualityRule', {'ProjectId': PROJECT_ID, 'Id': rule_id})

# 2. Delete evaluation task (after all rules are removed)
call_api('DeleteDataQualityEvaluationTask', {'ProjectId': PROJECT_ID, 'Id': task_id})
```

Both APIs only require `ProjectId` + `Id`. No detach step needed.

### 31. DQ for Hologres tables: metadata collection required first (no API!)

Creating DQ rules for Hologres tables fails with "表（holo.xxx.public.xxx）不存在" because DQ monitoring depends on **data map metadata**. The table must first be registered via metadata collection.

**DataWorks API does NOT provide metadata collection APIs.** You must do this manually:

```
DataWorks Console → Data Map → Metadata Collection → Configure data source → Execute sync
```

Workaround: skip DQ rules entirely and use `ExecuteAdhocWorkflowInstance` with `HOLOGRES_SQL` to run `SELECT COUNT(*)` checks directly.

### 32. `CreateDataQualityEvaluationTask`: `DataSourceId` is mandatory

Error: `DataSourceId is mandatory for this action.`

You must pass the **numeric** data source ID (not the name). Get it from `ListDataSources`:

```python
ds_resp = call_api('ListDataSources', {'ProjectId': PROJECT_ID, 'PageSize': 50})
data_source_id = ds_resp['Data']['DataSourceModelList'][0]['Id']  # numeric ID
```

### 33. DQ evaluation task: partition table must set `PartitionSpec` in `Target`

Error: "分区表xxx的数据范围必须设置"

```python
'Target': json.dumps({
    'DatabaseType': 'maxcompute',
    'TableGuid': 'odps.<project>.<table>',
    'PartitionSpec': 'pt=$[yyyymmdd-1]'    # required for partitioned tables!
})
```

### 34. DQ `AttachDataQualityRulesToEvaluationTask`: parameter names have `DataQuality` prefix

```python
# WRONG — short names
'EvaluationTaskId': task_id,
'RuleIds': json.dumps([rule_id])

# CORRECT — full names with DataQuality prefix
'DataQualityEvaluationTaskId': task_id,
'DataQualityRuleIds': json.dumps([rule_id])
```

### 35. DI sync: `bizdate` vs partition date mismatch

DI sync tasks use `bizdate` which is usually **yesterday**. If the source table partition is **today's** date, the sync may find no data. Solutions:

1. Use an explicit partition value: `["dt='20260315'"]`
2. Use system parameters: `${cyctime}` or `${bizdate}`

### 36. Hologres SQL node FlowSpec differs from ODPS_SQL

Creating a Hologres SQL node via `CreateNode` requires different FlowSpec values:

| Field | ODPS_SQL | HOLOGRES_SQL |
|-------|----------|--------------|
| `datasource.type` | (not needed) | `"holo"` |
| `script.language` | (not needed) | `"hologres-sql"` |
| `script.runtime.command` | `"ODPS_SQL"` | `"HOLOGRES_SQL"` |
| `script.runtime.commandTypeId` | (not needed) | `1093` |
| `script.runtime.cu` | (not needed) | `"0.25"` |
| `script.path` engine folder | `MaxCompute` | `Hologres` |

### 37. DQ deletion is permanent — no undo

`DeleteDataQualityRule` and `DeleteDataQualityEvaluationTask` are irreversible. After deletion, querying the ID returns "not found".

### 38. `ExecuteAdhocWorkflowInstance`: `resource_group_id` must come from `ListResourceGroups`

Error: "资源组ID#xxx,对应的资源组不存在"

The resource group ID is a long string like `Serverless_res_group_<numbers>`. Always query dynamically:

```python
req = models.ListResourceGroupsRequest(project_id=PROJECT_ID, page_number=1, page_size=10)
resp = client.list_resource_groups(req)
groups = resp.body.paging_info.to_map().get('ResourceGroupList', [])
RESOURCE_GROUP_ID = groups[0].get('Id')
# e.g. "Serverless_res_group_<account-id>_<group-id>"
```

### 39. `ExecuteAdhocWorkflowInstance`: `data_source.name` must match an existing data source

Error: "数据源不存在"

Get the correct name from the node spec (`datasource.name`), `ListDataSources`, or task logs (e.g. `dstDs=<name>`).

### 40. Workflow elapsed time uses millisecond math

```python
if wf.finished_time and wf.started_time:
    elapsed_seconds = (wf.finished_time - wf.started_time) / 1000
```

---

## End-to-end lifecycle: Create → Write → Submit → Deploy → Run → Monitor

Every API-driven DataWorks workflow follows this pipeline. This section is designed for **copy-paste reuse**.

### Quick-reference cheat sheet

| Step | API | Key params | Wait | Pitfall | If it fails |
|------|-----|-----------|------|---------|-------------|
| **0. Init** | `ListResourceGroups`, `ListDataSources` | `project_id` | — | #38 #39 | Check project ID, IAM permissions |
| **1. Create** | `CreateNode` | `scene="DATAWORKS_PROJECT"`, `spec` (JSON) | — | #1 #8 #9 #36 | Check FlowSpec structure, inputs/outputs |
| **1. Create (alt)** | `ImportWorkflowDefinition` | `spec` (kind: `CycleWorkflow`) | — | #9 | Check FlowSpec, workflow path |
| **2. Update** | `UpdateNode` (new API) | `id`, `spec` (full JSON) | — | — | Re-fetch spec with `GetNode` first |
| **2. Update (alt)** | `UpdateFile` (old API) | `FileId`, `Content`, `AutoParsing=false` | — | #28 | Check FileId is correct |
| **3. Submit** | `SubmitFile` | `file_id` = `node_id` | 2s after create | #1 | `SkipAllDeployFileExtensions=true` if extensions block |
| **4. Deploy** | `DeployFile` | `file_id` = `node_id` | **10s after submit** | #2 #11 #22 | Retry after 5–15s; first-time node → deploy manually once |
| **4. Poll** | `GetDeployment` | `id` = deploy response | 3s interval | #22 | Status: `Success` / `Fail` / `Termination` / `Cancel` |
| **5a. Run (scheduled)** | _(automatic via cron)_ | — | — | — | Check trigger config in FlowSpec |
| **5b. Run (ad-hoc)** | `ExecuteAdhocWorkflowInstance` | 6 required params (see below) | — | #16–19 #38 #39 | See checklist below |
| **5c. Run (smoke test)** | `CreateWorkflowInstances` | `type=SmokeTest`, `workflow_id=1` | — | #10 | Node must be deployed to production first |
| **6. Monitor** | Per-path (see table below) | — | 2–10s poll | #21 #40 | `GetTaskInstanceLog` for failure details |

### Step 0: INIT — Discover resource group and data source

**Always query dynamically** — never hardcode these values.

```python
import os, json, time, uuid
from datetime import datetime, timedelta
from alibabacloud_dataworks_public20240518.client import Client
from alibabacloud_dataworks_public20240518 import models
from alibabacloud_tea_openapi.models import Config

client = Client(Config(
    access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    endpoint='dataworks.<region>.aliyuncs.com',
))
PROJECT_ID = <your-project-id>

rg = client.list_resource_groups(models.ListResourceGroupsRequest(
    project_id=PROJECT_ID, page_number=1, page_size=10
))
RESOURCE_GROUP_ID = rg.body.paging_info.to_map()['ResourceGroupList'][0]['Id']
# e.g. "Serverless_res_group_<account-id>_<group-id>"

ds = client.list_data_sources(models.ListDataSourcesRequest(
    project_id=PROJECT_ID, page_number=1, page_size=50
))
DATASOURCE_NAME = ds.body.paging_info.data_sources[0].name
```

### Step 1: CREATE — Create a node

Two approaches:

| Approach | API | FlowSpec `kind` | Use case |
|----------|-----|-----------------|----------|
| Single node | `CreateNode` | `Node` | Add a node to an existing workflow |
| Workflow + nodes | `ImportWorkflowDefinition` | `CycleWorkflow` | Create workflow container and all nodes together |

**CreateNode rules:**
- `scene` must be `"DATAWORKS_PROJECT"`
- `spec` is a JSON string (kind: `Node`)
- Returns `node_id` which **equals** `file_id` (Pitfall 1)
- `inputs` and `outputs` are **required** (Pitfall 8)

**FlowSpec varies by engine** (Pitfall 36):

| Field | ODPS_SQL | HOLOGRES_SQL |
|-------|----------|--------------|
| `datasource` | `{"name": "<mc-ds>"}` | `{"name": "<holo-ds>", "type": "holo"}` |
| `script.language` | _(omit)_ | `"hologres-sql"` |
| `script.runtime.command` | `"ODPS_SQL"` | `"HOLOGRES_SQL"` |
| `script.runtime.commandTypeId` | _(omit)_ | `1093` |
| `script.runtime.cu` | _(omit)_ | `"0.25"` |
| `script.path` engine folder | `MaxCompute` | `Hologres` |

```python
def build_node_spec(node_name, sql, engine="ODPS_SQL", datasource_name=DATASOURCE_NAME,
                    resource_group_id=RESOURCE_GROUP_ID):
    node = {
        "recurrence": "Normal", "timeout": 0, "instanceMode": "T+1",
        "rerunMode": "Allowed", "rerunTimes": 3, "rerunInterval": 180000,
        "datasource": {"name": datasource_name},
        "script": {
            "path": f"Business_flow/api_test/MaxCompute/{node_name}",
            "runtime": {"command": engine},
            "content": sql
        },
        "trigger": {
            "type": "Scheduler", "cron": "00 30 06 * * ?",
            "startTime": "1970-01-01 00:00:00", "endTime": "9999-01-01 00:00:00",
            "timezone": "Asia/Shanghai"
        },
        "runtimeResource": {"resourceGroup": resource_group_id},
        "name": node_name,
        "inputs": {"nodeOutputs": [{"data": "project_root", "artifactType": "NodeOutput"}]},
        "outputs": {"nodeOutputs": [{"data": f"{node_name}_output", "artifactType": "NodeOutput"}]}
    }
    if engine == "HOLOGRES_SQL":
        node["datasource"]["type"] = "holo"
        node["script"]["language"] = "hologres-sql"
        node["script"]["runtime"]["commandTypeId"] = 1093
        node["script"]["runtime"]["cu"] = "0.25"
        node["script"]["path"] = f"Business_flow/api_test/Hologres/{node_name}"

    return {"version": "1.1.0", "kind": "Node", "spec": {"nodes": [node]}}

spec = build_node_spec("my_node", "SELECT 1;")
node_id = client.create_node(models.CreateNodeRequest(
    project_id=PROJECT_ID, scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)).body.id
```

### Step 2: WRITE / UPDATE — Modify node content

**Path A — New API (`UpdateNode`):** Fetch full spec, modify, push back.

```python
node = client.get_node(models.GetNodeRequest(
    project_id=PROJECT_ID, id=str(node_id)
)).body.node
spec = json.loads(node.spec) if isinstance(node.spec, str) else node.spec.to_map()
spec['spec']['nodes'][0]['script']['content'] = "SELECT 2 AS new_result;"

client.update_node(models.UpdateNodeRequest(
    project_id=PROJECT_ID, id=str(node_id),
    spec=json.dumps(spec, ensure_ascii=False)
))
```

**Path B — Old API (`UpdateFile`):** Directly overwrite SQL content by `FileId`. Simpler but only modifies content.

```python
call_api('UpdateFile', {
    'ProjectId': PROJECT_ID,
    'FileId': node_id,
    'Content': "SELECT 2 AS new_result;",
    'AutoParsing': 'false',          # must be 'false' to skip auto-parsing
})
```

> After either update, changes are **only in dev**. You **must** continue to Submit + Deploy.

### Step 3: SUBMIT — Push to dev environment

`SubmitFile` uses `file_id` = `node_id` (they are the same value — Pitfall 1).

```python
time.sleep(2)
submit_resp = client.submit_file(models.SubmitFileRequest(
    project_id=PROJECT_ID,
    file_id=str(node_id),
    comment="submit via API"
))
deployment_id = submit_resp.body.data
```

> **Tip**: If submit fails because extension checks block it, pass `SkipAllDeployFileExtensions='true'` in the HTTP API (or the equivalent SDK parameter) to bypass extensions.

### Step 4: DEPLOY — Publish to production

**Critical**: Wait **~10 seconds** after submit for the pipeline to prepare (Pitfall 2).

```python
def deploy_with_retry(client, project_id, node_id, max_retries=3):
    """Deploy with automatic retry for pipeline-not-ready errors."""
    for attempt in range(max_retries):
        wait = 10 + attempt * 5          # 10s, 15s, 20s
        time.sleep(wait)
        try:
            resp = client.deploy_file(models.DeployFileRequest(
                project_id=project_id,
                file_id=str(node_id),
                comment="deploy via API"
            ))
            deploy_id = resp.body.data
            # Poll deployment status
            for _ in range(20):
                dep = client.get_deployment(models.GetDeploymentRequest(
                    project_id=project_id, id=str(deploy_id)
                ))
                status = dep.body.pipeline.status
                if status == "Success":
                    return deploy_id
                elif status in ("Fail", "Termination", "Cancel"):
                    raise RuntimeError(f"Deploy {status}: {dep.body.pipeline.message}")
                time.sleep(3)
        except Exception as e:
            err = str(e)
            if '流水线' in err or 'pipeline' in err.lower():
                print(f"Pipeline not ready (attempt {attempt+1}), retrying...")
                continue
            raise
    raise RuntimeError("Deploy failed after max retries")

deploy_id = deploy_with_retry(client, PROJECT_ID, node_id)
```

**Deployment status values** (Pitfall 22): `Success` | `Fail` | `Termination` | `Cancel`

> For **brand-new nodes that have never been deployed**, the first deploy may need to be done **manually in the DataWorks console**. Subsequent deploys via API work fine.

### Step 5: RUN — Three execution paths

```
                                ┌─── A. Scheduled ──── (automatic via cron, no API)
                                │
After Deploy ─── Choose path ───┼─── B. Ad-hoc SQL ─── ExecuteAdhocWorkflowInstance
                                │                       (DDL/DML/SELECT, no deploy needed)
                                │
                                └─── C. Smoke test ─── CreateWorkflowInstances
                                                        (manual trigger of deployed node)
```

**When to use which:**

| Scenario | Path |
|----------|------|
| Node runs daily/hourly per schedule | A (scheduled) |
| One-off `CREATE TABLE`, ad-hoc query, temp DDL | B (ad-hoc) |
| Test a deployed node before going live | C (smoke test) |
| Create a Hologres table before DI sync | B (ad-hoc with `HOLOGRES_SQL`) |

#### Path A: Scheduled execution

No API call needed. After deploy, the node runs per `trigger.cron`. Monitor via `ListTaskInstances`.

#### Path B: Ad-hoc SQL execution (ExecuteAdhocWorkflowInstance)

Run SQL immediately **without** submit/deploy. Supports multiple SQL engines.

**6 required parameters checklist** (Pitfall 16–19, 38–39):

| # | Parameter | Value | Common mistake |
|---|-----------|-------|---------------|
| 1 | `client_unique_code` | `str(uuid.uuid4()).replace('-','')[:20]` | Missing → `MissingClientUniqueCode` |
| 2 | `type` | `ODPS_SQL`, `HOLOGRES_SQL`, `MYSQL_SQL`, `POSTGRESQL_SQL` | Must be **ALL_CAPS** with underscores |
| 3 | `owner` | User ID string | Must be set at **both** task and request level |
| 4 | `resource_group_id` | From `ListResourceGroups` | Format: `Serverless_res_group_...` |
| 5 | `data_source.name` | From node spec / `ListDataSources` | Must match existing data source exactly |
| 6 | `biz_date` | `YYYYMMDD` string (e.g. `20260315`) | Not millisecond timestamp! |

```python
def run_adhoc_sql(client, project_id, sql, engine="ODPS_SQL",
                  datasource_name=DATASOURCE_NAME, owner=OWNER,
                  resource_group_id=RESOURCE_GROUP_ID):
    """Run ad-hoc SQL and return workflow_instance_id."""
    task = models.ExecuteAdhocWorkflowInstanceRequestTasks(
        name=f"adhoc_{datetime.now().strftime('%H%M%S')}",
        type=engine,
        owner=owner,
        client_unique_code=str(uuid.uuid4()).replace('-', '')[:20],
        script=models.ExecuteAdhocWorkflowInstanceRequestTasksScript(content=sql),
        data_source=models.ExecuteAdhocWorkflowInstanceRequestTasksDataSource(name=datasource_name),
        runtime_resource=models.ExecuteAdhocWorkflowInstanceRequestTasksRuntimeResource(
            resource_group_id=resource_group_id
        ),
        timeout=7200
    )
    resp = client.execute_adhoc_workflow_instance(
        models.ExecuteAdhocWorkflowInstanceRequest(
            project_id=project_id,
            biz_date=datetime.now().strftime('%Y%m%d'),
            name=f"adhoc_wf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            owner=owner,
            tasks=[task]
        )
    )
    return resp.body.workflow_instance_id

wf_id = run_adhoc_sql(client, PROJECT_ID, "SELECT 1;")
```

**Hologres example** — create a target table before DI sync:

```python
holo_sql = """
CREATE TABLE IF NOT EXISTS public.my_target (
    id BIGINT, name TEXT, value DOUBLE PRECISION
);
"""
wf_id = run_adhoc_sql(
    client, PROJECT_ID, holo_sql,
    engine="HOLOGRES_SQL",
    datasource_name="<holo-datasource-name>"
)
```

#### Path C: Smoke test (CreateWorkflowInstances)

Manually trigger a **deployed** node. The node **must** already be in production.

```python
biz_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

trigger_resp = client.create_workflow_instances(models.CreateWorkflowInstancesRequest(
    project_id=PROJECT_ID,
    type="SmokeTest",
    workflow_id=1,                  # always 1 for periodic tasks (Pitfall 10)
    name=f"smoke_{datetime.now().strftime('%H%M%S')}",
    auto_start_enabled=True,
    default_run_properties=json.dumps({"RootTaskIds": [node_id]}),
    periods=json.dumps({"BizDates": [{"StartBizDate": biz_date, "EndBizDate": biz_date}]}),
))
operation_id = trigger_resp.body.operation_id
```

### Step 6: MONITOR — Track execution status

| Run path | Poll API | Final status values |
|----------|----------|-------------------|
| A (scheduled) | `ListTaskInstances` → `GetTaskInstance` | `NotRun` / `WaitTime` / `WaitResource` / `Running` / `Success` / `Failure` |
| B (ad-hoc) | `GetWorkflowInstance` | `Success` / `Failure` |
| C (smoke test) | `GetCreateWorkflowInstancesResult` → `GetTaskInstance` | `Created` / `CreateFailure` → same as A |

**Reusable monitor functions:**

```python
def wait_adhoc(client, wf_id, timeout=120, interval=2):
    """Monitor ad-hoc workflow (Path B). Returns (status, elapsed_seconds)."""
    for _ in range(timeout // interval):
        time.sleep(interval)
        wf = client.get_workflow_instance(
            models.GetWorkflowInstanceRequest(id=str(wf_id))
        ).body.workflow_instance
        if wf.status in ('Success', 'Failure'):
            elapsed = 0
            if wf.finished_time and wf.started_time:
                elapsed = (wf.finished_time - wf.started_time) / 1000
            return wf.status, elapsed
    return 'Timeout', 0

def wait_scheduled(client, project_id, bizdate_ms, node_name=None, timeout=600, interval=10):
    """Monitor scheduled instances (Path A). Returns list of (id, name, status)."""
    results = []
    for _ in range(timeout // interval):
        time.sleep(interval)
        instances = client.list_task_instances(models.ListTaskInstancesRequest(
            project_id=project_id, bizdate=bizdate_ms,
            page_number=1, page_size=50
        )).body.paging_info.task_instances or []
        for inst in instances:
            if node_name and inst.task_name != node_name:
                continue
            if inst.status in ('Success', 'Failure'):
                results.append((inst.id, inst.task_name, inst.status))
        if results:
            return results
    return results

def wait_smoke_test(client, operation_id, timeout_create=300, timeout_run=600):
    """Monitor smoke test (Path C). Returns list of (task_id, status)."""
    # Phase 1: wait for workflow creation
    task_ids = []
    for _ in range(timeout_create // 5):
        time.sleep(5)
        result = client.get_create_workflow_instances_result(
            models.GetCreateWorkflowInstancesResultRequest(operation_id=operation_id)
        ).body.result
        if result.status == "Created":
            task_ids = result.workflow_task_instance_ids
            break
        elif result.status == "CreateFailure":
            return [("N/A", "CreateFailure")]

    # Phase 2: wait for each task instance
    results = []
    for tid in task_ids:
        for _ in range(timeout_run // 10):
            time.sleep(10)
            inst = client.get_task_instance(
                models.GetTaskInstanceRequest(id=str(tid))
            ).body.task_instance
            if inst.status in ('Success', 'Failure'):
                if inst.status == 'Failure':
                    log = client.get_task_instance_log(
                        models.GetTaskInstanceLogRequest(id=str(tid))
                    ).body.task_instance_log
                    results.append((tid, 'Failure', log))
                else:
                    results.append((tid, 'Success', ''))
                break
    return results
```

### Error recovery reference

| Step | Error | Recovery |
|------|-------|----------|
| Create | `InvalidSpec` / FlowSpec error | Check `inputs`/`outputs` required; validate JSON structure; see Pitfall 8, 9 |
| Create | `Throttling.Resource` | Retry with exponential backoff (Pitfall 7) |
| Submit | Extension check blocks submit | Add `SkipAllDeployFileExtensions='true'` |
| Deploy | "pipeline not ready" / "流水线未准备好" | Wait 10–20s more and retry; use `deploy_with_retry()` above |
| Deploy | First-time deploy fails | Deploy once manually from DataWorks console, then API works |
| Run (ad-hoc) | `MissingClientUniqueCode` | Add `client_unique_code=str(uuid.uuid4())[:20]` (Pitfall 18) |
| Run (ad-hoc) | Type format error | Must be ALL_CAPS: `ODPS_SQL`, `HOLOGRES_SQL` (Pitfall 19) |
| Run (ad-hoc) | "资源组不存在" | Fetch from `ListResourceGroups` dynamically (Pitfall 38) |
| Run (ad-hoc) | "数据源不存在" | Fetch from `ListDataSources` or node spec (Pitfall 39) |
| Run (smoke) | "node not found" | Node must be deployed to **production** first |
| Monitor | Task stuck in `WaitResource` | Resource group may be full; check quota |

### Complete example: Full lifecycle (ODPS_SQL)

```python
import os, json, time, uuid
from datetime import datetime, timedelta
from alibabacloud_dataworks_public20240518.client import Client
from alibabacloud_dataworks_public20240518 import models
from alibabacloud_tea_openapi.models import Config

client = Client(Config(
    access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    endpoint='dataworks.<region>.aliyuncs.com',
))
PROJECT_ID = <your-project-id>
OWNER = "<owner-id>"

# 0. INIT
rg = client.list_resource_groups(models.ListResourceGroupsRequest(project_id=PROJECT_ID))
RG_ID = rg.body.paging_info.to_map()['ResourceGroupList'][0]['Id']
ds = client.list_data_sources(models.ListDataSourcesRequest(project_id=PROJECT_ID, page_number=1, page_size=50))
DS_NAME = ds.body.paging_info.data_sources[0].name
node_name = f"lifecycle_{datetime.now().strftime('%Y%m%d%H%M')}"

# 1. CREATE
spec = {
    "version": "1.1.0", "kind": "Node",
    "spec": {"nodes": [{
        "recurrence": "Normal", "timeout": 0, "instanceMode": "T+1",
        "rerunMode": "Allowed", "rerunTimes": 3, "rerunInterval": 180000,
        "datasource": {"name": DS_NAME},
        "script": {
            "path": f"Business_flow/api_test/MaxCompute/{node_name}",
            "runtime": {"command": "ODPS_SQL"},
            "content": "SELECT 1 AS id, 'hello' AS msg;"
        },
        "trigger": {
            "type": "Scheduler", "cron": "00 30 06 * * ?",
            "startTime": "1970-01-01 00:00:00", "endTime": "9999-01-01 00:00:00",
            "timezone": "Asia/Shanghai"
        },
        "runtimeResource": {"resourceGroup": RG_ID},
        "name": node_name,
        "inputs": {"nodeOutputs": [{"data": "project_root", "artifactType": "NodeOutput"}]},
        "outputs": {"nodeOutputs": [{"data": f"{node_name}_output", "artifactType": "NodeOutput"}]}
    }]}
}
node_id = client.create_node(models.CreateNodeRequest(
    project_id=PROJECT_ID, scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)).body.id
print(f"[1/5] Created: node_id={node_id}")

# 2. SUBMIT
time.sleep(2)
dep_id = client.submit_file(models.SubmitFileRequest(
    project_id=PROJECT_ID, file_id=str(node_id), comment="submit"
)).body.data
print(f"[2/5] Submitted: deployment_id={dep_id}")

# 3. DEPLOY (with retry)
for attempt in range(3):
    time.sleep(10 + attempt * 5)
    try:
        deploy_id = client.deploy_file(models.DeployFileRequest(
            project_id=PROJECT_ID, file_id=str(node_id), comment="deploy"
        )).body.data
        for _ in range(20):
            d = client.get_deployment(models.GetDeploymentRequest(project_id=PROJECT_ID, id=str(deploy_id)))
            if d.body.pipeline.status == "Success":
                print(f"[3/5] Deployed: {d.body.pipeline.status}")
                break
            elif d.body.pipeline.status in ("Fail", "Termination", "Cancel"):
                print(f"[3/5] Deploy failed: {d.body.pipeline.status}")
                break
            time.sleep(3)
        break
    except Exception as e:
        if '流水线' in str(e) or 'pipeline' in str(e).lower():
            print(f"  Pipeline not ready (attempt {attempt+1}), retrying...")
            continue
        raise

# 4. RUN (ad-hoc)
task = models.ExecuteAdhocWorkflowInstanceRequestTasks(
    name="adhoc_run", type="ODPS_SQL", owner=OWNER,
    client_unique_code=str(uuid.uuid4()).replace('-', '')[:20],
    script=models.ExecuteAdhocWorkflowInstanceRequestTasksScript(content="SELECT 1;"),
    data_source=models.ExecuteAdhocWorkflowInstanceRequestTasksDataSource(name=DS_NAME),
    runtime_resource=models.ExecuteAdhocWorkflowInstanceRequestTasksRuntimeResource(resource_group_id=RG_ID),
    timeout=7200
)
wf_id = client.execute_adhoc_workflow_instance(models.ExecuteAdhocWorkflowInstanceRequest(
    project_id=PROJECT_ID, biz_date=datetime.now().strftime('%Y%m%d'),
    name=f"adhoc_{datetime.now().strftime('%H%M%S')}", owner=OWNER, tasks=[task]
)).body.workflow_instance_id
print(f"[4/5] Running: workflow_instance_id={wf_id}")

# 5. MONITOR
for _ in range(30):
    time.sleep(2)
    wf = client.get_workflow_instance(
        models.GetWorkflowInstanceRequest(id=str(wf_id))
    ).body.workflow_instance
    if wf.status in ('Success', 'Failure'):
        elapsed = ''
        if wf.finished_time and wf.started_time:
            elapsed = f" ({(wf.finished_time - wf.started_time) / 1000:.1f}s)"
        print(f"[5/5] Done: {wf.status}{elapsed}")
        break
```

### Complete example: Full lifecycle (HOLOGRES_SQL — create table + ad-hoc)

```python
# Uses same INIT as above. Only CREATE and RUN differ.

node_name = f"holo_node_{datetime.now().strftime('%Y%m%d%H%M')}"
HOLO_DS = "<holo-datasource-name>"
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS public.my_target (
    id BIGINT, name TEXT, value DOUBLE PRECISION, ts TIMESTAMPTZ DEFAULT NOW()
);
"""

# 1. CREATE (Hologres node)
spec = {
    "version": "1.1.0", "kind": "Node",
    "spec": {"nodes": [{
        "recurrence": "Normal", "timeout": 0, "instanceMode": "T+1",
        "rerunMode": "Allowed", "rerunTimes": 3, "rerunInterval": 180000,
        "datasource": {"name": HOLO_DS, "type": "holo"},
        "script": {
            "path": f"Business_flow/api_test/Hologres/{node_name}",
            "language": "hologres-sql",
            "runtime": {"command": "HOLOGRES_SQL", "commandTypeId": 1093, "cu": "0.25"},
            "content": CREATE_SQL.strip()
        },
        "trigger": {
            "type": "Scheduler", "cron": "00 30 06 * * ?",
            "startTime": "1970-01-01 00:00:00", "endTime": "9999-01-01 00:00:00",
            "timezone": "Asia/Shanghai"
        },
        "runtimeResource": {"resourceGroup": RG_ID},
        "name": node_name,
        "inputs": {"nodeOutputs": [{"data": "project_root", "artifactType": "NodeOutput"}]},
        "outputs": {"nodeOutputs": [{"data": f"{node_name}_output", "artifactType": "NodeOutput"}]}
    }]}
}
node_id = client.create_node(models.CreateNodeRequest(
    project_id=PROJECT_ID, scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)).body.id
print(f"[1] Created Holo node: {node_id}")

# 2–3. SUBMIT + DEPLOY (same as ODPS_SQL above)
time.sleep(2)
client.submit_file(models.SubmitFileRequest(project_id=PROJECT_ID, file_id=str(node_id), comment="submit"))
time.sleep(10)
client.deploy_file(models.DeployFileRequest(project_id=PROJECT_ID, file_id=str(node_id), comment="deploy"))

# 4. RUN (ad-hoc Hologres SQL)
task = models.ExecuteAdhocWorkflowInstanceRequestTasks(
    name="holo_create_table", type="HOLOGRES_SQL", owner=OWNER,
    client_unique_code=str(uuid.uuid4()).replace('-', '')[:20],
    script=models.ExecuteAdhocWorkflowInstanceRequestTasksScript(content=CREATE_SQL.strip()),
    data_source=models.ExecuteAdhocWorkflowInstanceRequestTasksDataSource(name=HOLO_DS),
    runtime_resource=models.ExecuteAdhocWorkflowInstanceRequestTasksRuntimeResource(resource_group_id=RG_ID),
    timeout=7200
)
wf_id = client.execute_adhoc_workflow_instance(models.ExecuteAdhocWorkflowInstanceRequest(
    project_id=PROJECT_ID, biz_date=datetime.now().strftime('%Y%m%d'),
    name=f"holo_adhoc_{datetime.now().strftime('%H%M%S')}", owner=OWNER, tasks=[task]
)).body.workflow_instance_id

# 5. MONITOR
for _ in range(30):
    time.sleep(2)
    wf = client.get_workflow_instance(
        models.GetWorkflowInstanceRequest(id=str(wf_id))
    ).body.workflow_instance
    if wf.status in ('Success', 'Failure'):
        elapsed = (wf.finished_time - wf.started_time) / 1000 if wf.finished_time else 0
        print(f"[Done] {wf.status} ({elapsed:.1f}s)")
        break
```

---

## Recipes

### Recipe 1: Create an ODPS SQL node (FlowSpec)

The `CreateNode` API uses FlowSpec JSON. Minimal working structure:

```python
import json
from alibabacloud_dataworks_public20240518 import models

spec = {
    "version": "1.1.0",
    "kind": "Node",
    "spec": {
        "nodes": [{
            "recurrence": "Normal",
            "timeout": 0,
            "instanceMode": "T+1",
            "rerunMode": "Allowed",
            "rerunTimes": 3,
            "rerunInterval": 180000,
            "datasource": {"name": "<datasource-name>"},
            "script": {
                "path": "Business_flow/<workflow-name>/MaxCompute/<node-name>",
                "runtime": {"command": "ODPS_SQL"},
                "content": "SELECT 1;"
            },
            "trigger": {
                "type": "Scheduler",
                "cron": "00 30 06 * * ?",
                "startTime": "1970-01-01 00:00:00",
                "endTime": "9999-01-01 00:00:00",
                "timezone": "Asia/Shanghai",
                "delaySeconds": 0
            },
            "runtimeResource": {"resourceGroup": "<resource-group-id>"},
            "name": "<node-name>",
            "inputs": {
                "nodeOutputs": [{"data": "project_root", "artifactType": "NodeOutput"}]
            },
            "outputs": {
                "nodeOutputs": [{
                    "data": "<node-name>_output",
                    "artifactType": "NodeOutput",
                    "refTableName": "<node-name>"
                }]
            }
        }]
    }
}

request = models.CreateNodeRequest(
    project_id=PROJECT_ID,
    scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)
resp = client.create_node(request)
node_id = resp.body.id
```

Key fields:

- `scene`: must be `"DATAWORKS_PROJECT"`
- `script.path`: follows `Business_flow/<workflow>/<engine>/<name>` convention
- `script.runtime.command`: `"ODPS_SQL"` for MaxCompute SQL
- `inputs.nodeOutputs[0].data`: `"project_root"` for root dependency
- `runtimeResource.resourceGroup`: get from `ListResourceGroups`

### Recipe 2: Full submit-and-deploy flow

```python
import time

def submit_and_deploy(client, project_id, node_id, wait_seconds=10):
    # 1. Submit
    submit_req = models.SubmitFileRequest(
        project_id=project_id,
        file_id=str(node_id),
        comment="submit via API"
    )
    submit_resp = client.submit_file(submit_req)
    deployment_id = submit_resp.body.data

    # 2. Wait for pipeline to be ready
    time.sleep(wait_seconds)

    # 3. Deploy
    deploy_req = models.DeployFileRequest(
        project_id=project_id,
        file_id=str(node_id),
        comment="deploy via API"
    )
    deploy_resp = client.deploy_file(deploy_req)
    return deploy_resp.body.data
```

### Recipe 3: Execute ad-hoc SQL (ExecuteAdhocWorkflowInstance)

Supports DDL (`CREATE TABLE`), DML (`INSERT INTO`), and queries (`SELECT`).

**Key points before calling:**
- Fetch resource group ID dynamically via `ListResourceGroups` (filter `ResourceGroupType=3` for scheduling groups).
- Fetch data source name via `ListDataSources`.
- `biz_date` format is `YYYYMMDD` string (NOT millisecond timestamp — see Pitfall 16).
- `owner` is required at **both** task level and request level (see Pitfall 17).
- `client_unique_code` is **required** — omitting it causes `MissingClientUniqueCode` error (see Pitfall 18).
- `tasks` is a **list** — you can chain multiple tasks in one workflow.

```python
import uuid

resource_groups = client.list_resource_groups(
    models.ListResourceGroupsRequest(project_id=PROJECT_ID)
)
resource_group_id = resource_groups.body.paging_info.resource_groups[0].id

script = models.ExecuteAdhocWorkflowInstanceRequestTasksScript(content="SELECT 1;")
datasource = models.ExecuteAdhocWorkflowInstanceRequestTasksDataSource(name="<datasource-name>")
runtime = models.ExecuteAdhocWorkflowInstanceRequestTasksRuntimeResource(
    resource_group_id=resource_group_id
)

task = models.ExecuteAdhocWorkflowInstanceRequestTasks(
    name="adhoc_task",
    type="ODPS_SQL",
    owner="<owner-id>",
    script=script,
    data_source=datasource,
    runtime_resource=runtime,
    timeout=7200,
    client_unique_code=str(uuid.uuid4())[:8]
)

request = models.ExecuteAdhocWorkflowInstanceRequest(
    project_id=PROJECT_ID,
    biz_date=datetime.now().strftime('%Y%m%d'),
    name=f"adhoc_{datetime.now().strftime('%H%M%S')}",
    owner="<owner-id>",
    tasks=[task]
)
resp = client.execute_adhoc_workflow_instance(request)
workflow_instance_id = resp.body.workflow_instance_id
```

Then poll with `GetWorkflowInstance`:

```python
for _ in range(30):
    time.sleep(2)
    status_resp = client.get_workflow_instance(
        models.GetWorkflowInstanceRequest(id=str(workflow_instance_id))
    )
    wf = status_resp.body.workflow_instance
    status = wf.status
    elapsed = ''
    if wf.finished_time and wf.started_time:
        elapsed = f" ({(wf.finished_time - wf.started_time) / 1000:.1f}s)"
    print(f"Status: {status}{elapsed}")
    if status in ('Success', 'Failure'):
        break
```

> **Note:** `workflow_instance` fields are `started_time` / `finished_time` (millisecond epoch), NOT `start_time` / `end_time`.

### Recipe 4: Create a data quality rule (table not empty)

```python
target = models.CreateDataQualityRuleRequestTarget(
    type="Table",
    database_type="maxcompute",
    table_guid="odps.<project>.<table>",
    partition_spec="dt=$[yyyymmdd-1]",
)
checking_config = models.CreateDataQualityRuleRequestCheckingConfig(type="Fixed")

request = models.CreateDataQualityRuleRequest(
    project_id=PROJECT_ID,
    name="table_not_empty_check",
    description="Row count must be > 0",
    enabled=True,
    severity="High",
    target=target,
    template_code="SYSTEM:table:table_count:fixed:0",
    checking_config=checking_config,
)
resp = client.create_data_quality_rule(request)
rule_id = resp.body.id
```

Common quality rule template codes:

| Template code                             | Level  | Description                  |
| ----------------------------------------- | ------ | ---------------------------- |
| `SYSTEM:table:table_count:fixed:0`        | Table  | Row count > 0                |
| `SYSTEM:table:table_count:fixed`          | Table  | Row count matches fixed N    |
| `SYSTEM:table:table_size:fixed`           | Table  | Table size matches fixed     |
| `SYSTEM:field:null_value:fixed:0`         | Field  | Null value count = 0         |
| `SYSTEM:field:duplicated_count:fixed:0`   | Field  | Duplicated count = 0         |
| `SYSTEM:field:count_distinct:fixed`       | Field  | Distinct count matches fixed |
| `SYSTEM:column:null_count:fixed:0`        | Column | Column null count = 0        |
| `SYSTEM:column:unique_count:fixed:N`      | Column | Column unique count = N      |
| `SYSTEM:user_defined_sql`                 | Custom | User-defined SQL (DSL)       |

DQ evaluation task trigger types: `ByManual` (manual trigger) or `ByScheduledTaskInstance` (bound to scheduled task).

### Recipe 5: Look up resource group and data source dynamically

Always query these at runtime rather than hardcoding:

```python
# Resource groups
rg_resp = client.list_resource_groups(
    models.ListResourceGroupsRequest(project_id=PROJECT_ID, page_number=1, page_size=10)
)
rg_list = rg_resp.body.paging_info.to_map().get('ResourceGroupList', [])
resource_group_id = rg_list[0]['Id']

# Data sources
ds_resp = client.list_data_sources(
    models.ListDataSourcesRequest(project_id=PROJECT_ID, page_number=1, page_size=50)
)
datasources = ds_resp.body.paging_info.data_sources or []
```

### Recipe 6: Update node SQL content

Get the existing spec, modify the SQL, and push the full spec back:

```python
# 1. Get current node spec
get_req = models.GetNodeRequest(project_id=PROJECT_ID, id=str(node_id))
node = client.get_node(get_req).body.node

spec = node.spec
if isinstance(spec, str):
    spec_dict = json.loads(spec)
else:
    spec_dict = spec.to_map() if hasattr(spec, 'to_map') else spec

# 2. Modify SQL
spec_dict['spec']['nodes'][0]['script']['content'] = "SELECT 2 AS new_result;"

# 3. Update node (send the full spec back)
update_req = models.UpdateNodeRequest(
    project_id=PROJECT_ID,
    id=str(node_id),
    spec=json.dumps(spec_dict, ensure_ascii=False)
)
client.update_node(update_req)
```

### Recipe 7: Create a workflow definition

Before creating nodes, you may need to create a workflow container:

```python
wf_req = models.CreateWorkflowDefinitionRequest(
    project_id=PROJECT_ID,
    name="<workflow-name>",
    description="Workflow description"
)
wf_resp = client.create_workflow_definition(wf_req)
workflow_id = wf_resp.body.workflow_id
```

### Recipe 8: Trigger a smoke-test run and wait for completion

```python
from datetime import datetime, timedelta

biz_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

trigger_req = models.CreateWorkflowInstancesRequest(
    project_id=PROJECT_ID,
    type="SmokeTest",
    workflow_id=1,
    name=f"smoke_test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
    comment="smoke test via API",
    auto_start_enabled=True,
    default_run_properties=json.dumps({"RootTaskIds": [node_id]}),
    periods=json.dumps({"BizDates": [{"StartBizDate": biz_date, "EndBizDate": biz_date}]}),
)
trigger_resp = client.create_workflow_instances(trigger_req)
operation_id = trigger_resp.body.operation_id

# Poll for workflow creation result
for _ in range(60):
    time.sleep(5)
    result_req = models.GetCreateWorkflowInstancesResultRequest(operation_id=operation_id)
    result_resp = client.get_create_workflow_instances_result(result_req)
    status = result_resp.body.result.status
    if status == "Created":
        task_instance_ids = result_resp.body.result.workflow_task_instance_ids
        break
    elif status == "CreateFailure":
        raise RuntimeError("Workflow creation failed")

# Poll task instance until done
for task_inst_id in task_instance_ids:
    for _ in range(60):
        time.sleep(10)
        inst = client.get_task_instance(models.GetTaskInstanceRequest(id=str(task_inst_id)))
        if inst.body.task_instance.status in ('Success', 'Failure'):
            break
```

### Recipe 9: Poll deployment status with GetDeployment

After `DeployFile`, optionally poll for the pipeline result:

```python
def wait_for_deployment(client, project_id, deployment_id, timeout=60):
    for _ in range(timeout // 3):
        resp = client.get_deployment(models.GetDeploymentRequest(
            project_id=project_id, id=str(deployment_id)
        ))
        pipeline = resp.body.pipeline
        status = pipeline.status
        if status == "Success":
            return True
        elif status in ("Fail", "Termination", "Cancel"):
            return False
        time.sleep(3)
    return None  # timeout
```

### Recipe 10: Look up table metadata from data map

```python
resp = client.get_table(models.GetTableRequest(
    database_type="maxcompute",
    table_guid="odps.<project>.<table>"
))
```

The `table_guid` format for MaxCompute tables is `odps.<mc-project-name>.<table-name>`.

### Recipe 11: Run a data quality scan

After creating a rule, trigger and monitor a quality scan:

```python
# 1. Create a scan task
scan_resp = client.create_data_quality_scan(models.CreateDataQualityScanRequest(
    project_id=PROJECT_ID, rule_id=rule_id
))
scan_id = scan_resp.body.id

# 2. Execute the scan
run_resp = client.create_data_quality_scan_run(models.CreateDataQualityScanRunRequest(
    project_id=PROJECT_ID, id=scan_id
))
```

### Recipe 12: Complete data quality monitoring flow (3 steps)

The full DQ monitoring setup requires three API calls in sequence:

```python
import json

# Step 1: Create an evaluation task (monitoring task for a table)
task_params = {
    'ProjectId': PROJECT_ID,
    'DataSourceId': <datasource-id>,            # numeric ID from ListDataSources
    'Name': '<table>_quality_monitor',
    'Description': 'Data quality monitoring for <table>',
    'Target': json.dumps({
        'DatabaseType': 'maxcompute',
        'TableGuid': 'odps.<project>.<table>',
        'PartitionSpec': 'pt=$[yyyymmdd-1]'     # yesterday's partition
    }),
    'Trigger': json.dumps({
        'Type': 'ByManual'                      # or 'BySchedule' for auto
    })
}
task_result = call_api('CreateDataQualityEvaluationTask', task_params)
evaluation_task_id = task_result['Id']

# Step 2: Create a quality rule (see Recipe 4 for SDK approach)
rule_params = {
    'ProjectId': PROJECT_ID,
    'Name': 'table_not_empty_check',
    'TemplateCode': 'SYSTEM:table:table_count:fixed:0',
    'Target': json.dumps({
        'Type': 'Table',
        'DatabaseType': 'maxcompute',
        'TableGuid': 'odps.<project>.<table>',
        'PartitionSpec': 'pt=$[yyyymmdd-1]'
    }),
    'Enabled': 'true',
    'Severity': 'High',
    'CheckingConfig': json.dumps({
        'Type': 'Fixed',
        'Thresholds': {
            'Expected': {'Operator': '>', 'Value': '0'}
        }
    })
}
rule_result = call_api('CreateDataQualityRule', rule_params)
rule_id = rule_result['Id']

# Step 3: Bind rule to the evaluation task
attach_result = call_api('AttachDataQualityRulesToEvaluationTask', {
    'ProjectId': PROJECT_ID,
    'DataQualityEvaluationTaskId': evaluation_task_id,
    'DataQualityRuleIds': json.dumps([rule_id])
})
```

> **Note:** The binding API parameter names are `DataQualityEvaluationTaskId` and `DataQualityRuleIds` (with `DataQuality` prefix).

### Recipe 13: Create a custom SQL (DSL) quality rule

For flexible checks beyond built-in templates, use `SYSTEM:user_defined_sql`:

```python
rule_params = {
    'ProjectId': PROJECT_ID,
    'Name': 'custom_sql_check',
    'TemplateCode': 'SYSTEM:user_defined_sql',
    'Target': json.dumps({
        'Type': 'Table',
        'DatabaseType': 'maxcompute',
        'TableGuid': 'odps.<project>.<table>',
        'PartitionSpec': 'pt=$[yyyymmdd-1]'
    }),
    'Enabled': 'true',
    'Severity': 'High',
    'SamplingConfig': json.dumps({
        'Metric': 'UserDefinedSql',
        'MetricParameters': json.dumps({
            'SQL': 'SELECT COUNT(1) AS cnt FROM ${tableName} WHERE pt = ${bizdate}'
        })
    }),
    'CheckingConfig': json.dumps({
        'Type': 'Fixed',
        'Thresholds': {
            'Expected': {'Operator': '>', 'Value': '0'},
            'Critical': {'Operator': '<=', 'Value': '0'}
        }
    })
}
rule_result = call_api('CreateDataQualityRule', rule_params)
```

Built-in placeholders for custom SQL: `${tableName}`, `${bizdate}`.

### Recipe 14: Delete DQ rules and evaluation task (cleanup)

Complete cleanup flow — delete rules first, then the evaluation task:

```python
# 1. Delete all rules associated with the evaluation task
rule_ids = [rule_id_1, rule_id_2]
for rid in rule_ids:
    result = call_api('DeleteDataQualityRule', {
        'ProjectId': PROJECT_ID,
        'Id': rid
    })
    print(f"Rule {rid}: {'deleted' if result.get('Success') else result}")

# 2. Delete the evaluation task itself
result = call_api('DeleteDataQualityEvaluationTask', {
    'ProjectId': PROJECT_ID,
    'Id': evaluation_task_id
})
print(f"Task {evaluation_task_id}: {'deleted' if result.get('Success') else result}")
```

> **Note:** Rules can be deleted directly without calling a detach/unbind API first. Delete rules before the evaluation task to avoid orphaned references.

### Recipe 15: Create a DI offline sync node (e.g. MaxCompute → Hologres)

Use `CreateNode` with a DI-type FlowSpec. The `script.content` is a JSON config with Reader/Writer steps:

```python
di_config = {
    "extend": {
        "mode": "wizard",
        "resourceGroup": "<resource-group-id>",
        "cu": 0.5,
        "__new__": True
    },
    "type": "job",
    "version": "2.0",
    "steps": [
        {
            "stepType": "odps",       # MaxCompute source
            "parameter": {
                "datasource": "<mc-datasource-name>",
                "table": "<source-table>",
                "column": ["col1", "col2", "col3"],
                "enableWhere": False
            },
            "name": "Reader",
            "category": "reader"
        },
        {
            "stepType": "holo",       # Hologres target
            "parameter": {
                "datasource": "<holo-datasource-name>",
                "table": "public.<target-table>",
                "column": ["col1", "col2", "col3"],
                "writeMode": "insert",
                "truncate": True
            },
            "name": "Writer",
            "category": "writer"
        }
    ],
    "setting": {
        "errorLimit": {"record": "0"},
        "speed": {"throttle": False, "concurrent": 2}
    }
}

spec = {
    "version": "1.1.0",
    "kind": "Node",
    "spec": {
        "nodes": [{
            "recurrence": "Normal",
            "timeout": 0,
            "instanceMode": "T+1",
            "rerunMode": "Allowed",
            "script": {
                "path": "Business_flow/<workflow>/DI/<node-name>",
                "language": "json",
                "runtime": {
                    "command": "DI",
                    "commandTypeId": 23,
                    "cu": "0.5"
                },
                "content": json.dumps(di_config, ensure_ascii=False),
                "parameters": [
                    {"name": "bizdate", "value": "$bizdate", "type": "System"}
                ]
            },
            "trigger": {
                "type": "Scheduler",
                "cron": "00 00 05 * * ?",
                "cycleType": "Daily"
            },
            "runtimeResource": {"resourceGroup": "<resource-group-id>"},
            "name": "<node-name>",
            "inputs": {"nodeOutputs": [{"data": "project_root"}]},
            "outputs": {"nodeOutputs": [{"data": "<node-name>_output"}]}
        }]
    }
}

request = models.CreateNodeRequest(
    project_id=PROJECT_ID,
    scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)
resp = client.create_node(request)
```

DI stepType reference:

| stepType | Engine | Reader/Writer |
|----------|--------|---------------|
| `odps` | MaxCompute | Both |
| `holo` | Hologres | Both |
| `mysql` | MySQL | Both |
| `oracle` | Oracle | Reader |
| `sqlserver` | SQL Server | Reader |
| `postgresql` | PostgreSQL | Reader |
| `mongodb` | MongoDB | Reader |
| `oss` | OSS | Writer |
| `datahub` | DataHub | Writer |

writeMode options: `insert`, `update`, `delete`.

### Recipe 16: Create a DI Job (CreateDIJob) for database-level sync

For database-level offline/realtime sync where MaxCompute is NOT the source:

```python
result = call_api('CreateDIJob', {
    'ProjectId': PROJECT_ID,
    'Name': '<job-name>',
    'JobName': '<job-name>',
    'JobType': 'DatabaseOfflineMigration',
    'MigrationType': 'Full',
    'SourceDataSourceType': 'Hologres',
    'DestinationDataSourceType': 'Hologres',
    'SourceDataSourceSettings': json.dumps([{"DataSourceName": "<src-datasource>"}]),
    'DestinationDataSourceSettings': json.dumps([{"DataSourceName": "<dest-datasource>"}]),
    'TableMappings': json.dumps([{
        "SourceObjectSelectionRules": [{
            "Action": "Include",
            "ExpressionType": "Exact",
            "Expression": "<table-name>",
            "ObjectType": "Table"
        }],
        "TransformationRules": []
    }]),
    'ResourceSettings': json.dumps({
        "OfflineResourceSettings": {
            "ResourceGroupIdentifier": "<resource-group-id>",
            "RequestedCu": 4
        }
    }),
    'Description': 'sync job'
})
job_id = result.get('DIJobId') or result.get('Id')
```

JobType values: `DatabaseOfflineMigration`, `DatabaseRealtimeMigration`, `SingleTableRealtimeMigration`

MigrationType values: `Full`, `OfflineIncremental`, `FullAndOfflineIncremental`, `RealtimeIncremental`, `FullAndRealtimeIncremental`

Supported source types: PolarDB, MySQL, Kafka, LogHub, Hologres, Oracle, OceanBase, MongoDB, RedShift, Hive, SQLServer, Doris, ClickHouse

Supported destination types: Hologres, OSS-HDFS, OSS, MaxCompute, LogHub, StarRocks, DataHub, AnalyticDB_For_MySQL, Kafka, Hive

### Recipe 17: Create a Hologres SQL node (CreateNode FlowSpec)

```python
import json

NODE_NAME = "holo_create_table_node"
SQL_CONTENT = "CREATE TABLE IF NOT EXISTS public.my_table (id BIGINT, name TEXT);"

spec = {
    "version": "1.1.0",
    "kind": "Node",
    "spec": {
        "nodes": [{
            "recurrence": "Normal",
            "timeout": 0,
            "instanceMode": "T+1",
            "rerunMode": "Allowed",
            "rerunTimes": 3,
            "rerunInterval": 180000,
            "datasource": {"name": "<holo_datasource_name>", "type": "holo"},
            "script": {
                "path": f"Business_flow/<flow>/Hologres/{NODE_NAME}",
                "language": "hologres-sql",
                "runtime": {
                    "command": "HOLOGRES_SQL",
                    "commandTypeId": 1093,
                    "cu": "0.25"
                },
                "content": SQL_CONTENT
            },
            "trigger": {
                "type": "Scheduler",
                "cron": "00 30 06 * * ?",
                "cycleType": "Daily",
                "startTime": "1970-01-01 00:00:00",
                "endTime": "9999-01-01 00:00:00",
                "timezone": "Asia/Shanghai"
            },
            "runtimeResource": {"resourceGroup": RESOURCE_GROUP_ID},
            "name": NODE_NAME,
            "inputs": {"nodeOutputs": [{"data": "<project>_root", "artifactType": "NodeOutput"}]},
            "outputs": {"nodeOutputs": [{"data": f"{NODE_NAME}_output", "artifactType": "NodeOutput"}]}
        }]
    }
}

request = models.CreateNodeRequest(
    project_id=PROJECT_ID,
    scene="DATAWORKS_PROJECT",
    spec=json.dumps(spec, ensure_ascii=False)
)
resp = client.create_node(request)
node_id = resp.body.id
```

> See **Pitfall 36** for the full FlowSpec field differences between ODPS_SQL and HOLOGRES_SQL nodes.

### Recipe 18: End-to-end node lifecycle

See the **"End-to-end lifecycle"** section above for:
- **Quick-reference cheat sheet** — single table mapping every step to API, params, wait times, pitfalls, and error recovery
- **Reusable helper functions**: `build_node_spec()`, `deploy_with_retry()`, `run_adhoc_sql()`, `wait_adhoc()`, `wait_scheduled()`, `wait_smoke_test()`
- **Two complete copy-paste scripts**: ODPS_SQL and HOLOGRES_SQL full lifecycle
- **Decision tree** for choosing between scheduled / ad-hoc / smoke-test execution
- **Error recovery reference** table with specific fixes for each step

---

## Data quality rule response structure

After `CreateDataQualityRule`, the rule object contains:

```json
{
    "Id": 12345678,
    "Name": "table_not_empty_check",
    "Enabled": true,
    "Severity": "High",
    "TemplateCode": "SYSTEM:table:table_count:fixed",
    "Target": {
        "Type": "Table",
        "DatabaseType": "maxcompute",
        "TableGuid": "odps.<project>.<table>"
    },
    "CheckingConfig": {
        "Type": "Fixed",
        "Thresholds": {
            "Expected": {"Expression": "$checkValue > 0.0", "Operator": ">", "Value": "0.0"},
            "Critical": {"Expression": "$checkValue <= 0.0", "Operator": "<=", "Value": "0.0"}
        }
    },
    "SamplingConfig": {
        "Metric": "Count",
        "MetricParameters": "{\"scope\":[]}"
    }
}
```

---

## Response field reference

### GetTaskInstance attributes

| Field                  | Type | Description                                                           |
| ---------------------- | ---- | --------------------------------------------------------------------- |
| `id`                   | int  | Task instance ID                                                      |
| `task_id`              | int  | Task (node) ID                                                        |
| `task_name`            | str  | Task name                                                             |
| `task_type`            | str  | `VIRTUAL`, `ODPS_SQL`, etc.                                           |
| `status`               | str  | `Success`, `Failure`, `Running`, `NotRun`, `WaitTime`, `WaitResource` |
| `bizdate`              | int  | Business date (ms timestamp)                                          |
| `trigger_time`         | int  | Trigger time (ms timestamp)                                           |
| `trigger_type`         | str  | `Scheduler`, `Manual`                                                 |
| `started_time`         | int  | Start time (ms timestamp)                                             |
| `finished_time`        | int  | Finish time (ms timestamp)                                            |
| `owner`                | str  | Owner UID                                                             |
| `project_id`           | int  | Project ID                                                            |
| `project_env`          | str  | `Prod` or `Dev`                                                       |
| `workflow_id`          | int  | Workflow ID                                                           |
| `workflow_instance_id` | int  | Parent workflow instance ID                                           |
| `trigger_recurrence`   | str  | Trigger recurrence (`Normal`, etc.)                                   |
| `waiting_resource_time`| int  | Time spent waiting for resources (ms)                                 |
| `waiting_trigger_time` | int  | Time spent waiting for trigger (ms)                                   |
| `priority`             | int  | Instance priority                                                     |
| `rerun_mode`           | str  | Rerun mode                                                            |
| `runtime_resource`     | dict | Runtime resource info (resource group)                                |
| `outputs`              | dict | Output artifacts                                                      |
| `script`               | dict | Script info                                                           |

### ListFiles item attributes

| Field                  | Type | Description                            |
| ---------------------- | ---- | -------------------------------------- |
| `file_id`              | int  | File ID                                |
| `file_name`            | str  | File name                              |
| `file_type`            | int  | 10 = ODPS SQL, 20 = Shell, 30 = Python |
| `node_id`              | int  | Associated node ID                     |
| `commit_status`        | int  | 0 = uncommitted, 1 = committed         |
| `connection_name`      | str  | Data source name                       |
| `absolute_folder_path` | str  | Full path                              |

### GetNode attributes

| Field         | Type     | Description                                       |
| ------------- | -------- | ------------------------------------------------- |
| `id`          | int      | Node ID                                           |
| `name`        | str      | Node name                                         |
| `owner`       | str      | Owner UID                                         |
| `project_id`  | int      | Project ID                                        |
| `spec`        | str/dict | FlowSpec JSON (contains SQL, schedule, etc.)      |
| `create_time` | int      | Creation time (ms timestamp)                      |
| `modify_time` | int      | Last modification time (ms timestamp)             |
| `task_id`     | int      | Associated task ID (after deploy to production)   |

### GetWorkflowInstance attributes

| Field           | Type | Description                  |
| --------------- | ---- | ---------------------------- |
| `status`        | str  | `Success`, `Failure`, `Running` |
| `name`          | str  | Workflow instance name       |
| `started_time`  | int  | Start time (ms timestamp)    |
| `finished_time` | int  | Finish time (ms timestamp)   |

---

## FAQ

**Q: `DeployFile` fails with "pipeline not ready"**
A: Wait longer after `SubmitFile`. Default 10 s; increase to 15–20 s if it keeps failing. For brand-new nodes, a first manual deploy from the console may be required.

**Q: `CreateNode` returns an error about invalid spec**
A: Ensure the FlowSpec JSON matches the structure above exactly. Common mistakes: missing `inputs`/`outputs`, wrong `script.runtime.command` value, or incorrect `scene` parameter (must be `"DATAWORKS_PROJECT"`).

**Q: How to get the data source name for a node?**
A: Use `ListDataSources` to list all data sources, or extract it from an existing node's spec via `GetNode` → `spec.spec.nodes[0].datasource.name`.

**Q: Timestamps in responses are huge numbers — what format?**
A: All timestamps are **milliseconds** since Unix epoch. Divide by 1000 for Python `datetime.fromtimestamp()`.

**Q: How to trigger a smoke-test run of a node?**
A: Use `CreateWorkflowInstances` with `Type="SmokeTest"`, passing the node ID in `DefaultRunProperties.RootTaskIds`. Then poll `GetCreateWorkflowInstancesResult` → `GetTaskInstance` for status. See Recipe 8.

**Q: `ExecuteAdhocWorkflowInstance` fails — what to check?**
A: Verify: (1) `client_unique_code` is provided (required!), (2) resource group ID is correct — fetch dynamically with `ListResourceGroups`, (3) data source name matches exactly — fetch with `ListDataSources`, (4) `type` is ALL_CAPS format (`ODPS_SQL`, `HOLOGRES_SQL`, etc.), (5) `owner` is set on **both** the task object and the request, (6) `biz_date` uses `YYYYMMDD` format (not millisecond timestamp), (7) SQL syntax is valid, (8) IAM permissions are sufficient.

**Q: How to view task execution logs?**
A: Use `GetTaskInstanceLog` with the task instance ID.

**Q: Node was published but smoke test says "node not found"?**
A: Ensure the node is deployed to **production** (not just submitted to dev). Brand-new nodes may need a first manual deploy from the DataWorks console.

**Q: `UpdateNode` seems to succeed but changes don't take effect?**
A: After `UpdateNode`, you must `SubmitFile` + `DeployFile` again to push changes to production.

**Q: How to sync data FROM MaxCompute to another engine (e.g. Hologres)?**
A: Do NOT use `CreateDIJob` — its `SourceDataSourceType` does not include MaxCompute. Instead, use `CreateNode` with DI type (`command: "DI"`, `commandTypeId: 23`) and set `stepType: "odps"` for the Reader step. See Recipe 12.

**Q: What's the difference between `CreateDIJob` and `CreateNode` (DI type)?**
A: `CreateDIJob` creates database-level sync jobs (whole-database offline/realtime migration) and has a limited source type enum. `CreateNode` (DI type) creates a single sync node with full flexibility over Reader/Writer stepTypes, supporting MaxCompute as source.

**Q: DI sync fails with "can not found table" — what to do?**
A: The target table must exist before running a DI sync. Create it first using `ExecuteAdhocWorkflowInstance` with the appropriate SQL type (e.g. `HOLOGRES_SQL` for Hologres targets). See Pitfall 25.

**Q: DI sync fails with partition error on source table?**
A: Partitioned source tables require `partition` config in the Reader step. The partition value must be wrapped in **single quotes**: `["dt='20260315'"]`, not `["dt=20260315"]`. See Pitfall 26.

**Q: How to set up a complete data quality monitoring pipeline?**
A: Three steps: (1) `CreateDataQualityEvaluationTask` to create a monitoring task, (2) `CreateDataQualityRule` to create rules, (3) `AttachDataQualityRulesToEvaluationTask` to bind rules to the task. See Recipe 12.

**Q: How to create a custom SQL quality rule?**
A: Use `TemplateCode: "SYSTEM:user_defined_sql"` with `SamplingConfig.Metric: "UserDefinedSql"`. The SQL supports `${tableName}` and `${bizdate}` placeholders. See Recipe 13.

**Q: `CreatePipelineRun` doesn't seem to run my node — why?**
A: `CreatePipelineRun` is a **publish** pipeline (build → check → deploy), not an execution API. To run SQL directly, use `ExecuteAdhocWorkflowInstance`. To re-run an existing scheduled instance, use `RerunTaskInstances`. See Pitfall 20.

**Q: How to delete data quality rules and monitoring tasks?**
A: Delete rules first with `DeleteDataQualityRule`, then delete the evaluation task with `DeleteDataQualityEvaluationTask`. No detach step needed — rules can be deleted directly. See Recipe 14 and Pitfall 30.

**Q: Creating DQ rules for a Hologres table fails with "table not found"?**
A: DQ rules depend on **data map metadata**. Hologres tables must first be registered via metadata collection in the DataWorks Console (Data Map → Metadata Collection). There is **no API** for metadata collection. As a workaround, use `ExecuteAdhocWorkflowInstance` with `HOLOGRES_SQL` to run SQL-based checks directly. See Pitfall 31.

**Q: `CreateDataQualityEvaluationTask` fails with "DataSourceId is mandatory"?**
A: Pass the numeric data source ID obtained from `ListDataSources`. Do not pass the data source name. See Pitfall 32.

**Q: How to create a Hologres SQL node (not ad-hoc)?**
A: Use `CreateNode` with a FlowSpec that has `datasource.type: "holo"`, `script.language: "hologres-sql"`, `script.runtime.command: "HOLOGRES_SQL"`, and `commandTypeId: 1093`. See Recipe 17 and Pitfall 36.

**Q: `ExecuteAdhocWorkflowInstance` fails with "资源组不存在"?**
A: The `resource_group_id` must be fetched dynamically from `ListResourceGroups`. It is a long string like `Serverless_res_group_<numbers>`, not a short numeric ID. See Pitfall 38.
