---
name: alicloud-dataworks
description: Manage Alibaba Cloud DataWorks via OpenAPI/MCP Server. Use for data development, workflow operations, data quality, metadata lineage, workspace management, and troubleshooting across the entire DataWorks platform through a single skill.
---

Category: service

# DataWorks (dataworks-public)

Use Alibaba Cloud OpenAPI (RPC) with official SDKs, OpenAPI Explorer, or MCP Server to manage all DataWorks resources through a unified interface.

## Workflow

1) Confirm region, project/resource identifiers, and desired action.
2) Discover available APIs and required parameters (see references and scripts).
3) Call API via MCP Server, SDK, or OpenAPI Explorer.
4) Verify results with describe/list/get APIs.

## AccessKey priority (must follow)

1) Environment variables: `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
Region policy: `ALICLOUD_REGION_ID` is an optional default. If unset, decide the most reasonable region for the task; if unclear, ask the user.
2) Shared config file: `~/.alibabacloud/credentials`

## API discovery

- Product code: `dataworks-public`
- Default API version: `2024-05-18`
- Use OpenAPI metadata endpoints to list APIs and get schemas (see references).
- MCP Server tools discovery: `https://dataworks.data.aliyun.com/pop-mcp-tools`

The MCP Server supports dynamic tool filtering via environment variables:
- `TOOL_CATEGORIES`: Comma-separated category filter (e.g. `DATA_DEVELOP,OPS_CENTER,DATA_QUALITY`)
- `TOOL_NAMES`: Comma-separated API name filter (e.g. `ListProjects,GetProject,CreateNode`)

## MCP Server integration (preferred method)

Install and configure the MCP Server for direct AI agent access:

```bash
npm install -g alibabacloud-dataworks-mcp-server
```

MCP client configuration:

```json
{
  "mcpServers": {
    "alibabacloud-dataworks-mcp-server": {
      "command": "npx",
      "args": ["alibabacloud-dataworks-mcp-server"],
      "env": {
        "REGION": "cn-shanghai",
        "ALIBABA_CLOUD_ACCESS_KEY_ID": "your_access_key_id",
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "your_access_key_secret"
      }
    }
  }
}
```

The MCP Server dynamically loads tool definitions from the DataWorks metadata endpoint, so it always reflects the latest available APIs without hardcoding.

## High-frequency operation patterns

### Data Development (数据开发)
- Nodes: `CreateNode` / `UpdateNode` / `DeleteNode` / `GetNode` / `ListNodes`
- Resources: `CreateResource` / `UpdateResource` / `GetResource` / `MoveResource`
- Functions: `MoveFunction`
- Workflows: `CreateWorkflowDefinition` / `UpdateWorkflowDefinition` / `RenameWorkflowDefinition` / `DeleteWorkflowDefinition`
- Pipeline runs: `ListPipelineRuns` / `GetPipelineRun`

### Operations Center (运维中心)
- Workflows: `ListWorkflows` / `ListWorkflowInstances`
- Task instances: `ListTaskInstances` / `GetTaskInstance` / `UpdateTaskInstances`
- Lifecycle: `ResumeTaskInstances` / `SuspendTaskInstances` / `StopTaskInstances`
- Alerts: `CreateAlertRule` / `UpdateAlertRule` / `DeleteAlertRule`

### Data Map (数据地图)
- Tables/columns: `ListTables` / `GetColumn` / `ListColumns`
- Databases/catalogs: `GetDatabase` / `ListCatalogs`
- Lineage: `ListLineages` / `GetLineageRelationship`
- Metadata: `UpdateMetaCollection` / `DeleteMetaCollection` / `UpdateColumnBusinessMetadata`

### Data Quality (数据质量)
- Rules: `CreateDataQualityRule` / `GetDataQualityRule` / `UpdateDataQualityRule` / `DeleteDataQualityRule`
- Evaluation: `CreateDataQualityEvaluationTask` / `UpdateDataQualityEvaluationTask` / `AttachDataQualityRulesToEvaluationTask`

### Workspace Management (空间管理)
- Projects: `GetProject` / `ListProjects`
- Members: `ListProjectMembers` / `GetProjectMember` / `DeleteProjectMember`
- Roles: `ListProjectRoles` / `GetProjectRole` / `GrantMemberProjectRoles`

### Data Integration (数据集成)
- DI jobs: `GetDIJob` / `DeleteDIAlarmRule`

### Data Source (数据源)
- Datasource: `GetDataSource` / `DeleteDataSource`

### Resource Groups (资源组管理)
- Resources: `GetResourceGroup` / `GetNetwork` / `GetRoute` / `ListNetworks`

## Minimal executable quickstart

Use metadata-first discovery before calling business APIs:

```bash
python scripts/list_openapi_meta_apis.py
```

Optional overrides:

```bash
python scripts/list_openapi_meta_apis.py --product-code dataworks-public --version 2024-05-18
```

The script writes API inventory artifacts under the skill output directory.

## Destructive operation policy

Before executing delete, stop, or suspend operations, always summarize the affected resources and confirm with the user.

## Timestamp handling

DataWorks APIs use millisecond timestamps. Convert between human-readable dates and timestamps as needed.

## Output policy

If you need to save responses or generated artifacts, write them under:
`output/alicloud-dataworks/`

## Selection questions (ask when unclear)

1. Which DataWorks project (project ID or name)?
2. Which region? (common: `cn-shanghai`, `cn-beijing`, `cn-hangzhou`, `cn-shenzhen`)
3. What type of operation? (data development / operations / data quality / metadata / workspace)
4. For task operations: target node ID, workflow, or instance ID?

## References

- MCP Server integration: `references/mcp_server.md`
- Sources: `references/sources.md`
