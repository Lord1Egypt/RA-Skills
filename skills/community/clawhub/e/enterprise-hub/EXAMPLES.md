# Usage Examples

## Example 1: Permission Check Across Multiple Systems

### Scenario
Employee needs access to customer data that exists in multiple enterprise systems.

### Agent Prompt
```
Check if john.doe@company.com has permission to view Customer C-12345
data across Salesforce, SAP, and Workday
```

### Execution
```bash
curl -X POST http://localhost:3000/api/v1/permissions/check \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "john.doe@company.com",
    "resource": {
      "type": "customer",
      "id": "C-12345"
    },
    "action": "read",
    "systems": ["salesforce", "sap", "workday"]
  }'
```

### Response
```json
{
  "allowed": true,
  "reason": "User has read permission in all required systems",
  "permissionTopology": [
    {
      "system": "salesforce",
      "allowed": true,
      "permissions": ["read", "write"],
      "conflicts": []
    },
    {
      "system": "sap",
      "allowed": true,
      "permissions": ["read"],
      "conflicts": []
    },
    {
      "system": "workday",
      "allowed": false,
      "permissions": [],
      "conflicts": [
        {
          "type": "ACCESS_MISMATCH",
          "severity": "HIGH",
          "description": "User not in HR group",
          "resolution": {
            "strategy": "allow_intersection",
            "policy": "default_intersection_policy"
          }
        }
      ]
    }
  ],
  "effectivePermissions": ["read"],
  "auditId": "audit-abc-123",
  "metadata": {
    "cacheHit": false,
    "latencyMs": 42
  }
}
```

## Example 2: Automated Customer Onboarding Workflow

### Scenario
When a new customer is created in Salesforce, automatically provision accounts across all enterprise systems.

### Agent Prompt
```
Create a workflow that automatically onboards new customers across
Salesforce, SAP, and Jira when a customer is created
```

### Workflow Definition
```yaml
workflow:
  name: "Enterprise Customer Onboarding"
  description: "Automatically provision customer across all systems"

  trigger:
    type: "event"
    event: "customer.created"
    source: "salesforce"

  steps:
    - id: "validate_permissions"
      name: "Validate User Permissions"
      type: "permission_check"
      action: "verify_user_can_create_customer"
      systems: ["salesforce", "sap", "jira"]
      onFailure: "abort"

    - id: "create_sap_account"
      name: "Create SAP Customer Account"
      type: "system_call"
      target:
        system: "sap"
        action: "create_customer_account"
      parameters:
        customerId: "{{ trigger.customerId }}"
        name: "{{ trigger.customerName }}"
        email: "{{ trigger.customerEmail }}"
        status: "Active"
      retry:
        maxAttempts: 3
        backoff: "exponential"
      onFailure: "continue"

    - id: "create_jira_project"
      name: "Create Jira Support Project"
      type: "system_call"
      target:
        system: "jira"
        action: "create_project"
      parameters:
        name: "{{ trigger.customerName }} Support"
        key: "{{ trigger.customerId }}"
        lead: "{{ trigger.accountOwner }}"
        projectType: "customer_support"

    - id: "notify_team"
      name: "Notify Sales Team"
      type: "notification"
      target:
        channel: "slack"
        webhook: "{{ env.SLACK_WEBHOOK }}"
      message: |
        New customer onboarded: {{ trigger.customerName }}
        - Salesforce: ✓
        - SAP: ✓
        - Jira: ✓
        Account Owner: {{ trigger.accountOwner }}
```

### Deployment
```bash
curl -X POST http://localhost:3000/api/v1/workflows \
  -H "Content-Type: application/yaml" \
  --data-binary @customer-onboarding.yaml
```

### Monitoring
```bash
# Get workflow status
curl http://localhost:3000/api/v1/workflows/customer-onboarding/status

# View execution history
curl http://localhost:3000/api/v1/workflows/customer-onboarding/executions?limit=10
```

## Example 3: Compliance Audit Report

### Scenario
Generate a compliance report showing all access to sensitive customer financial data for the last quarter.

### Agent Prompt
```
Generate a compliance audit report showing who accessed Customer C-12345
financial data in Q1 2026, including all systems
```

### Execution
```bash
curl -X GET "http://localhost:3000/api/v1/audit/export" \
  --data-urlencode "resourceType=customer" \
  --data-urlencode "resourceId=C-12345" \
  --data-urlencode "dataType=financial" \
  --data-urlencode "startDate=2026-01-01" \
  --data-urlencode "endDate=2026-03-31" \
  --data-urlencode "systems=salesforce,sap,workday" \
  --data-urlencode "format=csv" \
  -o audit-report-q1-2026.csv
```

### Sample Report Output (CSV)

```csv
timestamp,user_id,user_name,resource_type,resource_id,action,system,decision,reason,ip_address,latency_ms
2026-01-15 10:30:45,alice@company.com,Alice Smith,customer,C-12345,read,salesforce,allowed,Valid permission,192.168.1.100,42
2026-01-15 10:30:46,alice@company.com,Alice Smith,customer,C-12345,read,sap,allowed,Valid permission,192.168.1.100,38
2026-02-03 14:22:10,bob@company.com,Bob Johnson,customer,C-12345,write,salesforce,allowed,Valid permission,192.168.1.150,45
2026-02-03 14:22:15,bob@company.com,Bob Johnson,customer,C-12345,write,sap,denied,Insufficient permissions,192.168.1.150,35
2026-03-10 09:15:33,charlie@company.com,Charlie Davis,customer,C-12345,read,workday,allowed,Valid permission,192.168.1.200,40
```

### Anomaly Detection
```bash
# Detect unusual access patterns
curl -X POST http://localhost:3000/api/v1/audit/anomalies \
  -H "Content-Type: application/json" \
  -d '{
    "resourceId": "C-12345",
    "timeRange": {
      "start": "2026-01-01",
      "end": "2026-03-31"
    },
    "detectPatterns": [
      "unusual_time",
      "unusual_user",
      "high_frequency",
      "permission_elevation"
    ]
  }'
```

### Response
```json
{
  "anomalies": [
    {
      "type": "unusual_time",
      "severity": "medium",
      "timestamp": "2026-02-10 02:30:00",
      "userId": "dave@company.com",
      "description": "Access outside normal business hours",
      "context": {
        "normalHours": "8:00-18:00",
        "accessTime": "02:30"
      }
    },
    {
      "type": "high_frequency",
      "severity": "high",
      "userId": "eve@company.com",
      "description": "Unusual number of access attempts",
      "context": {
        "normalFrequency": "5 per day",
        "actualFrequency": "50 per day",
        "date": "2026-03-15"
      }
    }
  ],
  "totalAnomalies": 2,
  "riskScore": 7.5
}
```

## Example 4: Real-Time Permission Conflict Resolution

### Scenario
Two systems have conflicting permissions for the same user and resource.

### Agent Prompt
```
Resolve permission conflict: User has Salesforce access to Customer C-12345
but SAP denies access. What should be the effective permission?
```

### Conflict Detection
```bash
curl -X POST http://localhost:3000/api/v1/permissions/check \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "frank@company.com",
    "resource": {
      "type": "customer",
      "id": "C-12345",
      "attributes": {
        "sensitivity": "high",
        "dataType": "financial"
      }
    },
    "action": "read",
    "systems": ["salesforce", "sap"],
    "resolveConflicts": true
  }'
```

### Response with Conflict Resolution
```json
{
  "allowed": false,
  "reason": "Conflict resolution: DENY due to high-sensitivity resource",
  "permissionTopology": [
    {
      "system": "salesforce",
      "allowed": true,
      "permissions": ["read", "write"]
    },
    {
      "system": "sap",
      "allowed": false,
      "permissions": [],
      "reason": "User not in finance group"
    }
  ],
  "conflicts": [
    {
      "type": "ACCESS_MISMATCH",
      "severity": "HIGH",
      "systems": ["salesforce", "sap"],
      "resolution": {
        "strategy": "deny_on_high_sensitivity",
        "policy": "financial_data_protection_policy",
        "reasoning": "For high-sensitivity financial data, require access in ALL systems",
        "appliedAt": "2026-03-07T10:30:00Z"
      }
    }
  ],
  "effectivePermissions": [],
  "auditId": "audit-conflict-xyz-789"
}
```

### Custom Policy Definition (Rego)
```rego
package enterprise.permissions

# Policy: Financial data requires access in ALL systems
default allow_financial_data = false

allow_financial_data {
    input.resource.attributes.dataType == "financial"
    input.resource.attributes.sensitivity == "high"

    # Require permission in ALL systems
    salesforce_allowed := data.permissions.salesforce[input.userId].allowed
    sap_allowed := data.permissions.sap[input.userId].allowed

    salesforce_allowed == true
    sap_allowed == true
}
```

## Example 5: System Health Monitoring

### Scenario
Monitor the health and status of all connected enterprise systems.

### Agent Prompt
```
Check the health status of all connected systems and show any degraded services
```

### Execution
```bash
curl http://localhost:3000/api/v1/health
```

### Response
```json
{
  "status": "degraded",
  "timestamp": "2026-03-07T10:30:00Z",
  "components": [
    {
      "name": "database",
      "status": "healthy",
      "latency": 5,
      "lastCheck": "2026-03-07T10:30:00Z"
    },
    {
      "name": "redis",
      "status": "healthy",
      "latency": 2,
      "lastCheck": "2026-03-07T10:30:00Z"
    },
    {
      "name": "salesforce",
      "status": "healthy",
      "latency": 120,
      "circuitState": "closed",
      "lastCheck": "2026-03-07T10:30:00Z"
    },
    {
      "name": "sap",
      "status": "degraded",
      "latency": 850,
      "circuitState": "half_open",
      "lastCheck": "2026-03-07T10:30:00Z",
      "error": "High latency detected"
    },
    {
      "name": "jira",
      "status": "unhealthy",
      "circuitState": "open",
      "lastCheck": "2026-03-07T10:30:00Z",
      "error": "Connection timeout"
    }
  ],
  "degradedServices": ["sap"],
  "unhealthyServices": ["jira"],
  "recommendation": "SAP experiencing high latency. Jira circuit breaker is OPEN, using cached data."
}
```

## Example 6: Graceful Degradation Demo

### Scenario
Demonstrate how the system continues operating when a connected system fails.

### Before Failure
```bash
# Normal operation
curl -X POST http://localhost:3000/api/v1/permissions/check \
  -d '{"userId": "user@company.com", "resource": "customer:C-001", "systems": ["salesforce", "sap"]}'

# Response: 45ms, both systems queried live
```

### Simulate Failure
```bash
# Kill SAP adapter (for demo purposes)
curl -X POST http://localhost:3000/api/admin/test/kill-adapter \
  -d '{"adapter": "sap"}'
```

### During Failure (Degraded Mode)
```bash
# Same permission check
curl -X POST http://localhost:3000/api/v1/permissions/check \
  -d '{"userId": "user@company.com", "resource": "customer:C-001", "systems": ["salesforce", "sap"]}'

# Response: 50ms
# - Salesforce: queried live
# - SAP: returned from cache (degraded=true)
```

### Response
```json
{
  "allowed": true,
  "permissionTopology": [
    {
      "system": "salesforce",
      "allowed": true,
      "source": "live"
    },
    {
      "system": "sap",
      "allowed": true,
      "source": "cached",
      "degraded": true,
      "reason": "Circuit breaker open",
      "cacheAge": "2 minutes"
    }
  ],
  "warning": "SAP adapter is degraded, using cached data",
  "auditId": "audit-degraded-123"
}
```

### Recovery
```bash
# SAP recovers
curl -X POST http://localhost:3000/api/admin/test/recover-adapter \
  -d '{"adapter": "sap"}'

# System automatically detects recovery and resumes normal operation
```

## Integration with AI Agents

### Example: Claude Code Agent

```typescript
// Agent detects permission-related request
const userMessage = "Check if alice@company.com can access customer C-001 data in Salesforce and SAP";

// Agent recognizes this requires Enterprise Agent OS skill
if (containsKeywords(userMessage, ['permission', 'access', 'salesforce', 'sap'])) {
  // Use the skill
  const response = await fetch('http://localhost:3000/api/v1/permissions/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: 'alice@company.com',
      resource: { type: 'customer', id: 'C-001' },
      action: 'read',
      systems: ['salesforce', 'sap']
    })
  });

  const result = await response.json();

  // Report back to user
  return `Permission check complete:
    - Salesforce: ${result.permissionTopology.salesforce.allowed ? '✓ Allowed' : '✗ Denied'}
    - SAP: ${result.permissionTopology.sap.allowed ? '✓ Allowed' : '✗ Denied'}
    - Effective permissions: ${result.effectivePermissions.join(', ')}
    - Audit ID: ${result.auditId}`;
}
```

## Common Patterns

### Pattern 1: Pre-flight Permission Check

Before executing a cross-system operation, check permissions first:

```bash
# 1. Check permissions
curl -X POST /api/v1/permissions/check -d '{...}'

# 2. If allowed, execute operation
if [ $? -eq 0 ]; then
  curl -X POST /api/v1/workflows/execute -d '{...}'
fi
```

### Pattern 2: Audit-First Operations

Log intent before executing sensitive operations:

```bash
# 1. Create audit entry (intent)
curl -X POST /api/v1/audit/intent -d '{
  "operation": "customer_data_export",
  "userId": "admin@company.com",
  "resourceId": "C-001",
  "reason": "Customer request for data export (GDPR)"
}'

# 2. Execute operation
curl -X POST /api/v1/operations/export -d '{...}'

# 3. Update audit entry (completion)
curl -X PUT /api/v1/audit/${AUDIT_ID}/complete
```

### Pattern 3: Bulk Permission Checks

Check permissions for multiple users/resources at once:

```bash
curl -X POST /api/v1/permissions/check/bulk -d '{
  "checks": [
    {"userId": "user1@company.com", "resource": "customer:C-001"},
    {"userId": "user2@company.com", "resource": "customer:C-002"},
    {"userId": "user3@company.com", "resource": "customer:C-003"}
  ],
  "action": "read",
  "systems": ["salesforce", "sap"]
}'
```

## Performance Tips

1. **Use Caching**: Most permission checks hit cache (< 10ms)
2. **Batch Operations**: Use bulk APIs when possible
3. **Async Workflows**: Long-running workflows execute asynchronously
4. **Monitor Latency**: Set up alerts for p95 latency > 100ms
5. **Pre-warm Cache**: Warm permission cache for frequently accessed resources
