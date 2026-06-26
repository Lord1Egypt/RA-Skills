# DevOps Insight Skill

Intelligent DevOps incident management system integrating monitoring, GitHub, and ticket management.

## Quick Start

### 1. Configure MCP Servers

Copy configuration example:

```bash
cp config.example.json config.json
```

Edit `config.json` to configure your monitoring system connection information.

### 2. Configure GitHub

Ensure GitHub CLI is installed:

```bash
gh auth login
```

### 3. Configure Ticket Database

Create database schema:

```sql
CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  severity VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  root_cause TEXT,
  affected_services TEXT[],
  monitoring_data JSONB,
  related_commits TEXT[],
  assignee VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_severity ON tickets(severity);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

## Usage Examples

### Analyze Production Alerts

```
Analyze current API response time alerts
```

### Create Ticket

```
Create a ticket for this database connection timeout issue
```

### Code Impact Analysis

```
Analyze the potential impact of PR #456 on production
```

### Health Check

```
Check overall system health status
```

## Architecture

```
┌─────────────────────────────────────────┐
│  Kubernetes, PostgreSQL, Redis, Neo4j   │
│  Elasticsearch, Metrics, Skywalking     │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
                 ▼
┌─────────────────────────────────────────┐
│           DevOps Insight Agent                  │
│  ┌─────────────────────────────────┐   │
│  │  Monitoring Data Collection      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  AI-Powered Root Cause Analysis  │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Ticket Management               │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Code Review & Auto-Fix          │   │
│  └─────────────────────────────────┘   │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│ GitHub │  │ Ticket │  │ Claude   │
│        │  │   DB   │  │ Analysis │
└────────┘  └────────┘  └──────────┘
```

## Workflow

1. **Monitoring Data Collection**: Fetch data from monitoring systems via MCP
2. **Intelligent Analysis**: Use Claude for root cause analysis and issue diagnosis
3. **Ticket Management**: Automatically create, update, and correlate tickets
4. **Code Review**: Analyze related code changes, provide fix suggestions
5. **Auto-Fix**: (Optional) Automatically generate fix code and submit PR

## Configuration Options

See [config.example.json](config.example.json)

Main configuration items:

- `mcpServers`: MCP server configuration
- `ticketDatabase`: Ticket database configuration
- `github`: GitHub integration configuration
- `analysis`: Analysis behavior configuration
- `alerts`: Alert threshold configuration

## Security Considerations

1. Do not commit `config.json` containing sensitive information to version control
2. Use environment variables to store passwords and keys
3. Limit database and API access permissions
4. Enable audit logging for all operations
5. Production environment changes require manual approval

## Troubleshooting

### MCP Connection Issues

```bash
# Test MCP server connection
mcp-client test --server kubernetes
```

### Database Connection Issues

```bash
# Test database connection
psql -h localhost -U tickets_user -d tickets -c "SELECT 1"
```

### GitHub Authentication Issues

```bash
# Check GitHub authentication status
gh auth status
```

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License
