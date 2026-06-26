---
name: devops-insight
description: This skill should be used when the user asks to "analyze incidents", "troubleshoot production issues", "investigate alerts", "create tickets", "root cause analysis", "check monitoring", or discusses DevOps/SRE automation, incident management, or observability integration.
---

# DevOps Insight - Intelligent DevOps Incident Management

DevOps Insight is an intelligent DevOps incident management system that integrates multiple monitoring systems, GitHub, and ticket databases to enable automated fault analysis, root cause identification, and issue resolution.

## System Architecture

### Core Components

1. **Monitoring Data Source Integration** (via MCP)
   - Kubernetes: Cluster status, Pod logs, events
   - PostgreSQL: Database performance metrics
   - Redis: Cache status and performance
   - Neo4j: Graph database monitoring
   - Elasticsearch: Log platform
   - Metrics: General metrics collection
   - APM (Skywalking): Application performance monitoring

2. **Code Management**
   - GitHub integration (via gitnexus Nexus-skill)
   - Code review and commits
   - Automated fix commits

3. **EvoMap Integration**
   - Capsule creation and publishing
   - Gene + Capsule bundle publishing
   - Automated quality validation
   - Network reputation tracking

4. **AI Agent**
   - Problem clue identification via LLM
   - Root cause analysis
   - Code review and fix suggestions
   - Index construction decisions

## Workflow

### 1. Monitoring Data Collection

When receiving an alert or analyzing an issue:

```bash
# Retrieve Kubernetes monitoring data via MCP
# Assumes MCP server connections to each monitoring system are configured
```

**Steps:**
- Retrieve Pod status, logs, and events from Kubernetes
- Retrieve application performance traces from APM (Skywalking)
- Retrieve relevant logs from Elasticsearch
- Retrieve performance metrics from the Metrics system
- Retrieve status information from databases (PostgreSQL/Redis/Neo4j)

### 2. Intelligent Analysis and Root Cause Identification

Perform multi-dimensional analysis using Claude:

**Analysis Dimensions:**
1. **Problem Clue Identification**
   - Analyze alert information and monitoring data
   - Identify anomalous patterns and trends
   - Correlate with historical events

2. **Root Cause Analysis**
   - Code level: Recent code changes
   - Configuration level: Configuration changes and environment differences
   - Infrastructure level: Resource usage and network issues
   - Dependency level: Third-party services and databases

3. **Impact Assessment**
   - Affected services and users
   - Business impact severity
   - Urgency determination

### 3. Capsule Publishing

**Capsule Creation Workflow:**

```typescript
// Capsule data structure example
interface Capsule {
  asset_type: 'Capsule';
  asset_id: string; // sha256 hash
  title: string;
  body: string;
  signals: string[];
  confidence: number; // 0.0 to 1.0
  blast_radius: number;
  solution: {
    type: 'code_change' | 'config_change' | 'investigation';
    files: Array<{
      path: string;
      diff?: string;
      content?: string;
    }>;
    description: string;
  };
  context: {
    monitoring_data?: any;
    root_cause?: string;
    affected_services?: string[];
  };
  metadata: {
    created_at: string;
    model_name?: string;
  };
}

// Gene data structure example
interface Gene {
  asset_type: 'Gene';
  asset_id: string; // sha256 hash
  title: string;
  body: string;
  signals: string[];
  category: 'repair' | 'optimize' | 'innovate' | 'regulatory';
  strategy: string;
  confidence: number;
  metadata: {
    created_at: string;
    model_name?: string;
  };
}
```

**Publishing Operations:**
- Automatic Gene + Capsule bundle creation (based on analysis results)
- SHA-256 hash computation for asset verification
- Quality validation (confidence >= 0.8 recommended)
- Network reputation tracking
- Automatic promotion when quality thresholds are met

### 4. Code Review and Fixes

**GitHub Integration:**

1. **Code Review**
   - Review recent commits
   - Identify code changes that may have caused issues
   - Provide fix suggestions

2. **Automated Fixes**
   - Generate fix code
   - Create fix branch
   - Submit Pull Request
   - Update ticket status

3. **Index Construction Decisions**
   - Determine if additional monitoring metrics are needed
   - Determine if alert rules need modification
   - Update APM tracing configuration

### 5. Audit and Production Changes

**Important Reminder:**
- ⚠️ Audit and production changes - This step carries risk
- All changes require approval process
- Record all operation logs
- Support rollback mechanism

## Use Cases

### Scenario 1: Production Environment Alert Response

```
User: "Production API response time suddenly increased, help me analyze"

DevOps Insight Workflow:
1. Retrieve API response time trends from APM
2. Check Pod status and resource usage from Kubernetes
3. Query related error logs from Elasticsearch
4. Check query performance from database monitoring
4. Analyze root cause (e.g., slow database queries, memory leaks, traffic spikes)
5. Publish Gene + Capsule bundle to EvoMap network
6. If it's a code issue, review recent commits and provide fix suggestions
7. Update monitoring index, add relevant metrics
```

### Scenario 2: Fault Root Cause Analysis

```
User: "Help me analyze last night's service outage"

DevOps Insight Workflow:
1. Query related Capsules from EvoMap network
2. Retrieve all monitoring data for the event time period
3. Analyze timeline:
   - Code deployment time
   - Configuration change time
   - Resource usage changes
   - Error log appearance time
4. Identify root cause
5. Generate detailed post-incident analysis report
6. Provide preventive measure recommendations
```

### Scenario 3: Proactive Issue Discovery

```
User: "Check if there are any potential system issues"

DevOps Insight Workflow:
1. Scan all monitoring metrics
2. Identify anomalous trends (e.g., continuous memory growth, rising error rates)
3. Check resource usage
4. Analyze warning messages in logs
5. Generate health report
6. Publish warning Capsules for potential issues to EvoMap network
```

### Scenario 4: Code Change Impact Analysis

```
User: "Will this PR affect the production environment?"

DevOps Insight Workflow:
1. Analyze code change content
2. Identify affected services and components
3. Check related monitoring metrics
4. Query historical impact of similar changes
5. Assess risk level
6. Provide monitoring recommendations (which metrics to watch)
7. Suggest if new monitoring points are needed
```

## Configuration Requirements

### MCP Server Configuration

The following MCP servers need to be configured to connect to each monitoring system:

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "mcp-server-kubernetes",
      "args": ["--kubeconfig", "/path/to/kubeconfig"]
    },
    "postgresql": {
      "command": "mcp-server-postgresql",
      "args": ["--connection-string", "postgresql://..."]
    },
    "redis": {
      "command": "mcp-server-redis",
      "args": ["--host", "redis.example.com"]
    },
    "elasticsearch": {
      "command": "mcp-server-elasticsearch",
      "args": ["--url", "https://es.example.com"]
    },
    "skywalking": {
      "command": "mcp-server-skywalking",
      "args": ["--url", "http://skywalking.example.com"]
    }
  }
}
```

### GitHub Integration

Ensure gitnexus Nexus-skill is installed and configured:

```bash
# Check if gitnexus is available
gh --version

# Configure GitHub authentication
gh auth login
```

### EvoMap API Configuration

Configure EvoMap API connection for publishing Capsules:

```json
{
  "evomap": {
    "apiUrl": "https://evomap.ai/a2a",
    "nodeId": "node_your_unique_id",
    "enableHeartbeat": true,
    "heartbeatInterval": 900000,
    "autoPublish": true,
    "minConfidence": 0.8
  }
}
```

**Configuration Options:**
- `apiUrl`: EvoMap A2A protocol endpoint
- `nodeId`: Your agent's unique node identifier (obtained from registration)
- `enableHeartbeat`: Enable automatic heartbeat to stay online (recommended)
- `heartbeatInterval`: Heartbeat interval in milliseconds (default: 15 minutes)
- `autoPublish`: Automatically publish high-confidence solutions as Capsules
- `minConfidence`: Minimum confidence threshold for auto-publishing (0.0-1.0)

## Best Practices

### 1. Monitoring Data Collection

- Prioritize retrieving the most relevant monitoring data
- Set reasonable time ranges (avoid data overload)
- Use filter conditions for precise queries

### 2. Root Cause Analysis

- Adopt multi-dimensional analysis methods
- Correlate historical data and patterns
- Consider time factors (change time, alert time)
- Validate hypotheses (verify with additional data)

### 3. Capsule Publishing

- Publish high-quality solutions promptly
- Document analysis process and conclusions in detail
- Associate all relevant monitoring data and code
- Maintain confidence >= 0.8 for auto-publishing
- Use appropriate signals for better discoverability

### 4. Code Changes

- Exercise caution with production environment changes
- Thoroughly test fix solutions
- Maintain small, incremental changes
- Prepare for rollback

### 5. Security Considerations

- Audit all production change operations
- Follow principle of least privilege
- Sanitize sensitive information
- Maintain complete operation logs

## Command Examples

### Analyze Current Alerts

```
Analyze current production alerts
```

### Create Incident Ticket

```
Create a ticket for this API timeout issue
```

### Code Impact Analysis

```
Analyze the impact of PR #123 on production environment
```

### Health Check

```
Check system health status
```

### Root Cause Analysis

```
Analyze the root cause of yesterday's 20:00 service outage
```

## Important Notes

1. **Permission Management**
   - Ensure sufficient permissions to access monitoring systems
   - GitHub operations require appropriate repository permissions
   - EvoMap API requires valid node registration

2. **Data Security**
   - Do not expose sensitive information (passwords, keys, etc.) in tickets
   - Log data may contain user information, ensure sanitization
   - Comply with data protection regulations

3. **Change Risks**
   - Exercise extra caution with production environment changes
   - Recommend testing in test environment first
   - Maintain change traceability

4. **Performance Considerations**
   - Large monitoring data queries may be slow
   - Set reasonable query ranges and limits
   - Consider using caching mechanisms

## Extended Features

### Future Plans

- [ ] Automated fix execution (requires stricter security controls)
- [ ] Machine learning predictions (predict failures based on historical data)
- [ ] Multi-cluster support
- [ ] Custom alert rules
- [ ] Integration with more monitoring systems
- [ ] Mobile alert notifications
- [ ] Collaboration features (team collaboration for incident handling)

## Troubleshooting

### Common Issues

**Q: MCP server connection failure**
```
A: Check MCP server configuration and network connection
   Verify authentication information is correct
   Review MCP server logs
```

**Q: GitHub operation failure**
```
A: Confirm gh CLI is properly configured
   Check repository permissions
   Verify gitnexus skill is available
```

**Q: Capsule publishing failure**
```
A: Check EvoMap API connection and node registration
   Verify confidence score meets minimum threshold
   Ensure asset_id hash is computed correctly
   Review EvoMap API response for error details
```

**Q: Incomplete monitoring data**
```
A: Check time range settings
   Verify monitoring system is running normally
   Confirm query conditions are not too restrictive
```

## Related Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub CLI Documentation](https://cli.github.com/)
- [Kubernetes Monitoring Best Practices](https://kubernetes.io/docs/tasks/debug/)
- [SkyWalking Documentation](https://skywalking.apache.org/)
- [Elasticsearch Query Guide](https://www.elastic.co/guide/)
- [EvoMap A2A Protocol](https://evomap.ai/wiki/05-a2a-protocol)
- [EvoMap Agent Guide](https://evomap.ai/wiki/03-for-ai-agents)

## Contributing

Issues and improvement suggestions are welcome!

## License

MIT License
