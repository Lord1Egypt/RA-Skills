# n8n MCP Server Implementation

Complete MCP server implementation for bidirectional n8n integration.

## Server Architecture

```python
# mcp-servers/n8n-mcp-bidirectional/n8n_mcp_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os, json, aiohttp, logging

# Configuration
N8N_API_KEY = os.getenv('N8N_API_KEY')
N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')

server = Server("n8n-automation")
```

## N8N API Client

```python
class N8NClient:
    """Async n8n API client"""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'X-N8N-API-KEY': self.api_key,
                    'Content-Type': 'application/json'
                }
            )

    async def _request(self, method: str, endpoint: str, **kwargs):
        await self._ensure_session()
        url = f"{self.base_url}{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def list_workflows(self, active_only=False):
        params = {'active': 'true'} if active_only else {}
        result = await self._request('GET', '/api/v1/workflows', params=params)
        return result.get('data', [])

    async def get_workflow(self, workflow_id: str):
        return await self._request('GET', f'/api/v1/workflows/{workflow_id}')

    async def create_workflow(self, workflow: dict):
        return await self._request('POST', '/api/v1/workflows', json=workflow)

    async def update_workflow(self, workflow_id: str, workflow: dict):
        return await self._request('PUT', f'/api/v1/workflows/{workflow_id}', json=workflow)

    async def delete_workflow(self, workflow_id: str):
        await self._request('DELETE', f'/api/v1/workflows/{workflow_id}')
        return True

    async def activate_workflow(self, workflow_id: str):
        workflow = await self.get_workflow(workflow_id)
        workflow['active'] = True
        return await self.update_workflow(workflow_id, workflow)

    async def deactivate_workflow(self, workflow_id: str):
        workflow = await self.get_workflow(workflow_id)
        workflow['active'] = False
        return await self.update_workflow(workflow_id, workflow)

    async def execute_workflow(self, workflow_id: str, data=None):
        return await self._request('POST', f'/api/v1/workflows/{workflow_id}/execute',
                                   json={'data': data or {}})

    async def get_executions(self, workflow_id: str, limit=10):
        result = await self._request('GET', '/api/v1/executions',
                                     params={'workflowId': workflow_id, 'limit': limit})
        return result.get('data', [])
```

## Tool Definitions

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_workflows",
            description="List all n8n workflows",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(name="get_workflow", description="Get workflow details",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="activate_workflow", description="Activate workflow",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="deactivate_workflow", description="Deactivate workflow",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="execute_workflow", description="Execute workflow manually",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "data": {"type": "object"}}, "required": ["workflow_id"]}),
        Tool(name="delete_workflow", description="Delete workflow",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="get_executions", description="Get execution history",
             inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["workflow_id"]})
    ]
```

## Tool Execution

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "list_workflows":
            workflows = await n8n_client.list_workflows(arguments.get("active_only", False))
            summary = {
                "total": len(workflows),
                "active": sum(1 for w in workflows if w.get("active")),
                "workflows": [{"id": w["id"], "name": w["name"], "active": w.get("active", False)} for w in workflows]
            }
            return [TextContent(type="text", text=json.dumps(summary, indent=2))]

        elif name == "get_workflow":
            workflow = await n8n_client.get_workflow(arguments["workflow_id"])
            info = {
                "id": workflow["id"],
                "name": workflow["name"],
                "active": workflow.get("active", False),
                "nodes": len(workflow.get("nodes", []))
            }
            return [TextContent(type="text", text=json.dumps(info, indent=2))]

        elif name == "activate_workflow":
            result = await n8n_client.activate_workflow(arguments["workflow_id"])
            return [TextContent(type="text", text=json.dumps({"success": True, "workflow_id": result["id"]}, indent=2))]

        elif name == "deactivate_workflow":
            result = await n8n_client.deactivate_workflow(arguments["workflow_id"])
            return [TextContent(type="text", text=json.dumps({"success": True, "workflow_id": result["id"]}, indent=2))]

        elif name == "execute_workflow":
            result = await n8n_client.execute_workflow(arguments["workflow_id"], arguments.get("data"))
            return [TextContent(type="text", text=json.dumps({"success": True, "execution_id": result.get("id")}, indent=2))]

        elif name == "delete_workflow":
            await n8n_client.delete_workflow(arguments["workflow_id"])
            return [TextContent(type="text", text=json.dumps({"success": True, "workflow_id": arguments["workflow_id"]}, indent=2))]

        elif name == "get_executions":
            executions = await n8n_client.get_executions(arguments["workflow_id"], arguments.get("limit", 10))
            summary = [{"id": e["id"], "status": "success" if e.get("finished") else "failed"} for e in executions]
            return [TextContent(type="text", text=json.dumps(summary, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": True, "message": str(e)}, indent=2))]
```

## Server Startup

```python
async def main():
    logging.info("Starting n8n MCP Server...")
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    finally:
        await n8n_client.session.close() if n8n_client.session else None

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Deployment

### requirements.txt
```
mcp>=0.1.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
```

### Environment Setup
```bash
# .env
N8N_API_KEY=n8n_api_xxxxxxxxxxxxx
N8N_BASE_URL=http://localhost:5678
LOG_LEVEL=INFO
```

### Installation
```bash
cd mcp-servers/n8n-mcp-bidirectional
pip install -r requirements.txt
python n8n_mcp_server.py
```

## Error Handling

```python
class N8NError(Exception):
    pass

class N8NAPIError(N8NError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"API Error {status_code}: {message}")
```

## Validation

```python
def validate_workflow(workflow: dict) -> tuple[bool, list[str]]:
    errors = []
    if "name" not in workflow:
        errors.append("Missing workflow name")
    if "nodes" not in workflow or not workflow["nodes"]:
        errors.append("Workflow must have at least one node")
    return len(errors) == 0, errors
```

## Complete Implementation

See `mcp-servers/n8n-mcp-bidirectional/n8n_mcp_server.py` for the full production-ready implementation.
