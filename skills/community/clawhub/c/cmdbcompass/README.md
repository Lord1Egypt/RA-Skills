# CMDB Compass

> The first CMDB governance skill for ServiceNow.

Audit, remediate, and govern your ServiceNow CMDB from any AI agent. Health scoring, duplicate detection, relationship analysis, stale CI cleanup, and governed remediation with full rollback and audit trail on every write.

## Install

```bash
clawhub install cmdbcompass
```

Or manually:

```bash
git clone https://github.com/cmdbcompass/cmdbcompass
cd cmdbcompass
bash scripts/install-mcp.sh
```

## Configure

Add to your MCP client config:

```json
{
  "mcpServers": {
    "cmdb-compass": {
      "command": "python",
      "args": ["-m", "servicenow_mcp.server"],
      "env": {
        "SERVICENOW_INSTANCE_URL": "https://your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your_username",
        "SERVICENOW_PASSWORD": "your_password"
      }
    }
  }
}
```

Works with Claude Desktop, Cursor, VS Code, or any MCP-compatible client.

## Capabilities

Audit tools cover health scoring, duplicate detection, relationship integrity, discovery gaps, stale CI identification, and CSDM 5.0 compliance. All audit operations are read-only and unlimited.

Write operations including merging duplicates, retiring stale CIs, bulk field updates, and relationship healing create an immutable audit trail and can be fully rolled back by session.

## Requirements

Python 3.10+ and a ServiceNow instance with REST API access.

## License

MIT. See LICENSE for details.

## Contact

[hello@cmdbcompass.com](mailto:hello@cmdbcompass.com) · [Issues](https://github.com/cmdbcompass/cmdbcompass/issues)
