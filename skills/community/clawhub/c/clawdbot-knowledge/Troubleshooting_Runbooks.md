# RAG-Enhanced N8N System - Troubleshooting & Operational Runbooks

## 📋 **Document Information**

- **Document Version**: 1.0
- **Last Updated**: 2024-01-08
- **Document Type**: Operational Runbooks
- **Audience**: System Administrators, DevOps Engineers, Support Teams
- **Classification**: Operational Documentation

---

## 🎯 **Runbook Overview**

This document provides comprehensive troubleshooting procedures and operational runbooks for the RAG-Enhanced N8N System. It includes step-by-step procedures for common issues, emergency response protocols, and maintenance procedures.

### **Runbook Structure**

Each runbook follows a standardized format:
- **Issue Description**: Clear description of the problem
- **Symptoms**: Observable signs and error messages
- **Severity Level**: Critical, High, Medium, Low
- **Prerequisites**: Required access and tools
- **Diagnostic Steps**: Step-by-step investigation procedures
- **Resolution Steps**: Detailed remediation procedures
- **Verification**: Steps to confirm resolution
- **Prevention**: Measures to prevent recurrence

---

## 🚨 **Emergency Response Procedures**

### **Incident Severity Levels**

```yaml
Severity Levels:
  Critical (P1):
    - Complete system outage
    - Data loss or corruption
    - Security breach
    - Response Time: 15 minutes
    - Resolution Target: 4 hours

  High (P2):
    - Major functionality unavailable
    - Performance severely degraded
    - Multiple users affected
    - Response Time: 30 minutes
    - Resolution Target: 8 hours

  Medium (P3):
    - Minor functionality issues
    - Performance degradation
    - Limited user impact
    - Response Time: 2 hours
    - Resolution Target: 24 hours

  Low (P4):
    - Cosmetic issues
    - Enhancement requests
    - Single user impact
    - Response Time: 8 hours
    - Resolution Target: 72 hours
```

### **Emergency Contact Escalation**

```yaml
Escalation Matrix:
  Level 1 - On-Call Engineer:
    - Initial response and triage
    - Basic troubleshooting
    - Escalation decision

  Level 2 - Senior Engineer:
    - Complex technical issues
    - System architecture problems
    - Security incidents

  Level 3 - Engineering Manager:
    - Major outages
    - Business impact decisions
    - External communication

  Level 4 - CTO/VP Engineering:
    - Critical business impact
    - Public relations issues
    - Executive decisions
```

---

## 🔧 **System Health Diagnostics**

### **Runbook 1: System Health Check**

**Issue**: Routine system health verification  
**Severity**: Preventive  
**Frequency**: Daily

**Diagnostic Commands**:
```bash
# Check Kubernetes cluster health
kubectl get nodes
kubectl get pods --all-namespaces | grep -v Running
kubectl top nodes
kubectl top pods --all-namespaces

# Check service status
kubectl get services -n n8n-mcp-prod
kubectl get ingress -n n8n-mcp-prod

# Check database connectivity
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- pg_isready
kubectl exec -it redis-master-0 -n n8n-mcp-prod -- redis-cli ping
curl -f http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/health

# Check application health
curl -f https://api.n8n-mcp.yourdomain.com/health
curl -f https://api.n8n-mcp.yourdomain.com/api/v1/health/detailed
```

**Health Check Script**:
```bash
#!/bin/bash
# health_check.sh

echo "=== RAG-Enhanced N8N System Health Check ==="
echo "Timestamp: $(date)"
echo

# Function to check service health
check_service() {
    local service_name=$1
    local health_url=$2
    
    echo "Checking $service_name..."
    if curl -f -s "$health_url" > /dev/null; then
        echo "✓ $service_name: Healthy"
    else
        echo "✗ $service_name: Unhealthy"
        return 1
    fi
}

# Check core services
check_service "API Gateway" "https://api.n8n-mcp.yourdomain.com/health"
check_service "RAG Engine" "https://api.n8n-mcp.yourdomain.com/api/v1/rag/health"
check_service "Workflow Engine" "https://api.n8n-mcp.yourdomain.com/api/v1/workflows/health"
check_service "Monitoring" "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/health"

# Check databases
echo "Checking databases..."
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- pg_isready && echo "✓ PostgreSQL: Connected" || echo "✗ PostgreSQL: Connection failed"
kubectl exec -it redis-master-0 -n n8n-mcp-prod -- redis-cli ping | grep -q PONG && echo "✓ Redis: Connected" || echo "✗ Redis: Connection failed"

echo
echo "Health check completed."
```

---

## 🔍 **Performance Issues**

### **Runbook 2: High Response Time Investigation**

**Issue**: API response times exceeding 5 seconds  
**Severity**: High  
**Symptoms**: Slow user interface, timeout errors, user complaints

**Diagnostic Steps**:

1. **Check System Resources**:
```bash
# CPU and Memory usage
kubectl top nodes
kubectl top pods -n n8n-mcp-prod

# Check for resource constraints
kubectl describe nodes | grep -A 5 "Allocated resources"
kubectl get pods -n n8n-mcp-prod -o wide
```

2. **Analyze Application Metrics**:
```bash
# Check response time metrics
curl -s "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/metrics?metric=response_time&duration=1h" | jq

# Check error rates
curl -s "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/metrics?metric=error_rate&duration=1h" | jq

# Check database performance
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;"
```

3. **Check Cache Performance**:
```bash
# Redis cache hit rate
kubectl exec -it redis-master-0 -n n8n-mcp-prod -- redis-cli info stats | grep hit_rate

# Application cache metrics
curl -s "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/metrics?metric=cache_hit_rate" | jq
```

**Resolution Steps**:

1. **Scale Application Pods**:
```bash
# Scale up if CPU/Memory usage is high
kubectl scale deployment n8n-mcp-api -n n8n-mcp-prod --replicas=5
kubectl scale deployment n8n-mcp-rag -n n8n-mcp-prod --replicas=3

# Verify scaling
kubectl get pods -n n8n-mcp-prod | grep n8n-mcp
```

2. **Optimize Database Queries**:
```bash
# Identify slow queries
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements 
WHERE mean_exec_time > 1000 
ORDER BY mean_exec_time DESC;"

# Add missing indexes if needed
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
CREATE INDEX CONCURRENTLY idx_workflows_created_at ON workflows(created_at);
CREATE INDEX CONCURRENTLY idx_executions_workflow_id ON executions(workflow_id);"
```

3. **Clear and Warm Cache**:
```bash
# Clear Redis cache if needed
kubectl exec -it redis-master-0 -n n8n-mcp-prod -- redis-cli flushdb

# Warm up cache with common queries
curl -X POST "https://api.n8n-mcp.yourdomain.com/api/v1/cache/warmup" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

**Verification**:
```bash
# Monitor response times for 10 minutes
for i in {1..10}; do
  response_time=$(curl -o /dev/null -s -w '%{time_total}' https://api.n8n-mcp.yourdomain.com/api/v1/health)
  echo "Response time: ${response_time}s"
  sleep 60
done
```

### **Runbook 3: Memory Leak Investigation**

**Issue**: Continuously increasing memory usage  
**Severity**: High  
**Symptoms**: Out of memory errors, pod restarts, performance degradation

**Diagnostic Steps**:

1. **Monitor Memory Usage Trends**:
```bash
# Check memory usage over time
kubectl top pods -n n8n-mcp-prod --sort-by=memory
kubectl describe pod <pod-name> -n n8n-mcp-prod | grep -A 10 "Limits\|Requests"

# Get detailed memory metrics
curl -s "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/metrics?metric=memory_usage&duration=24h" | jq
```

2. **Analyze Application Logs**:
```bash
# Check for memory-related errors
kubectl logs -n n8n-mcp-prod deployment/n8n-mcp-api --tail=1000 | grep -i "memory\|oom\|heap"

# Check garbage collection logs (for Java/Node.js apps)
kubectl logs -n n8n-mcp-prod deployment/n8n-mcp-api --tail=1000 | grep -i "gc\|garbage"
```

3. **Generate Memory Dump** (if applicable):
```bash
# For Python applications
kubectl exec -it <pod-name> -n n8n-mcp-prod -- python -c "
import tracemalloc
tracemalloc.start()
# Application code here
current, peak = tracemalloc.get_traced_memory()
print(f'Current memory usage: {current / 1024 / 1024:.1f} MB')
print(f'Peak memory usage: {peak / 1024 / 1024:.1f} MB')
"
```

**Resolution Steps**:

1. **Restart Affected Pods**:
```bash
# Rolling restart to clear memory
kubectl rollout restart deployment/n8n-mcp-api -n n8n-mcp-prod
kubectl rollout status deployment/n8n-mcp-api -n n8n-mcp-prod
```

2. **Adjust Memory Limits**:
```bash
# Update deployment with higher memory limits
kubectl patch deployment n8n-mcp-api -n n8n-mcp-prod -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [
          {
            "name": "api",
            "resources": {
              "limits": {
                "memory": "4Gi"
              },
              "requests": {
                "memory": "2Gi"
              }
            }
          }
        ]
      }
    }
  }
}'
```

3. **Implement Memory Monitoring**:
```bash
# Add memory alerts
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: memory-alerts
  namespace: n8n-mcp-prod
spec:
  groups:
  - name: memory
    rules:
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage detected"
EOF
```

---

## 🗄️ **Database Issues**

### **Runbook 4: Database Connection Issues**

**Issue**: Database connection failures  
**Severity**: Critical  
**Symptoms**: "Connection refused", "Too many connections", application errors

**Diagnostic Steps**:

1. **Check Database Status**:
```bash
# PostgreSQL status
kubectl get pods -n n8n-mcp-prod | grep postgresql
kubectl logs -n n8n-mcp-prod postgresql-0 --tail=100

# Check connection limits
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "
SELECT setting FROM pg_settings WHERE name = 'max_connections';
SELECT count(*) FROM pg_stat_activity;
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
```

2. **Test Connectivity**:
```bash
# Test from application pod
kubectl exec -it deployment/n8n-mcp-api -n n8n-mcp-prod -- nc -zv postgresql 5432

# Test authentication
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "SELECT version();"
```

**Resolution Steps**:

1. **Restart Database Service**:
```bash
# Restart PostgreSQL pod
kubectl delete pod postgresql-0 -n n8n-mcp-prod
kubectl get pods -n n8n-mcp-prod | grep postgresql

# Wait for pod to be ready
kubectl wait --for=condition=ready pod/postgresql-0 -n n8n-mcp-prod --timeout=300s
```

2. **Increase Connection Limits**:
```bash
# Update PostgreSQL configuration
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();"

# Verify change
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "
SELECT setting FROM pg_settings WHERE name = 'max_connections';"
```

3. **Kill Long-Running Queries**:
```bash
# Identify long-running queries
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "
SELECT pid, now() - pg_stat_activity.query_start AS duration, query 
FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';"

# Kill specific queries if needed
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "
SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
WHERE (now() - pg_stat_activity.query_start) > interval '10 minutes';"
```

### **Runbook 5: Qdrant Vector Database Issues**

**Issue**: Vector search failures or slow performance  
**Severity**: High  
**Symptoms**: RAG queries failing, slow search responses, indexing errors

**Diagnostic Steps**:

1. **Check Qdrant Status**:
```bash
# Service status
kubectl get pods -n n8n-mcp-prod | grep qdrant
kubectl logs -n n8n-mcp-prod deployment/qdrant --tail=100

# Health check
curl -f http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/health
```

2. **Check Collection Status**:
```bash
# List collections
curl -X GET "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections"

# Get collection info
curl -X GET "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents"

# Check collection statistics
curl -X GET "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents/cluster"
```

**Resolution Steps**:

1. **Restart Qdrant Service**:
```bash
# Rolling restart
kubectl rollout restart deployment/qdrant -n n8n-mcp-prod
kubectl rollout status deployment/qdrant -n n8n-mcp-prod
```

2. **Recreate Collection** (if corrupted):
```bash
# Backup existing collection
curl -X POST "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents/snapshots"

# Delete and recreate collection
curl -X DELETE "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents"

curl -X PUT "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }'
```

3. **Optimize Collection**:
```bash
# Optimize collection for better performance
curl -X POST "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents/index" \
  -H "Content-Type: application/json" \
  -d '{
    "wait": true
  }'
```

---

## 🔐 **Security Incidents**

### **Runbook 6: Security Breach Response**

**Issue**: Suspected security breach or unauthorized access  
**Severity**: Critical  
**Symptoms**: Unusual login patterns, unauthorized data access, security alerts

**Immediate Response Steps**:

1. **Isolate Affected Systems**:
```bash
# Block suspicious IP addresses
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-suspicious-ips
  namespace: n8n-mcp-prod
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 192.168.1.100/32  # Suspicious IP
EOF
```

2. **Disable Compromised Accounts**:
```bash
# Disable user account
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.disable_user \
  --user-id "compromised_user_id" \
  --reason "Security incident"

# Revoke all sessions
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.revoke_all_sessions \
  --user-id "compromised_user_id"
```

3. **Collect Evidence**:
```bash
# Export audit logs
kubectl exec -it n8n-mcp-security-0 -n n8n-mcp-prod -- python -m scripts.export_audit_logs \
  --start-time "2024-01-08T00:00:00Z" \
  --end-time "2024-01-08T23:59:59Z" \
  --output "/tmp/security-incident-logs.json"

# Export security events
kubectl exec -it n8n-mcp-security-0 -n n8n-mcp-prod -- python -m scripts.export_security_events \
  --severity "high,critical" \
  --output "/tmp/security-events.json"
```

4. **Notify Stakeholders**:
```bash
# Send security alert
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.send_security_alert \
  --incident-type "unauthorized_access" \
  --severity "critical" \
  --description "Suspicious login activity detected"
```

**Investigation Steps**:

1. **Analyze Access Patterns**:
```bash
# Check recent logins
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
SELECT user_id, ip_address, user_agent, timestamp, success
FROM auth_audit_log 
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;"
```

2. **Review Data Access**:
```bash
# Check data access logs
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
SELECT user_id, resource, action, timestamp
FROM audit_logs 
WHERE event_type = 'data_access' 
AND timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;"
```

**Recovery Steps**:

1. **Reset Compromised Credentials**:
```bash
# Force password reset for affected users
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.force_password_reset \
  --user-id "affected_user_id"

# Rotate API keys
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.rotate_api_keys \
  --all-users
```

2. **Update Security Policies**:
```bash
# Enable additional security measures
kubectl exec -it n8n-mcp-security-0 -n n8n-mcp-prod -- python -m scripts.update_security_policy \
  --policy "enhanced_monitoring" \
  --enabled true

# Require MFA for all users
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.enforce_mfa \
  --all-users
```

---

## 🔄 **Backup and Recovery**

### **Runbook 7: Data Recovery Procedures**

**Issue**: Data loss or corruption requiring recovery  
**Severity**: Critical  
**Symptoms**: Missing data, corrupted files, database errors

**Assessment Steps**:

1. **Assess Data Loss Scope**:
```bash
# Check database integrity
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables 
ORDER BY schemaname, tablename;"

# Check file system integrity
kubectl exec -it qdrant-0 -n n8n-mcp-prod -- ls -la /qdrant/storage/
```

2. **Identify Recovery Point**:
```bash
# List available backups
aws s3 ls s3://your-backup-bucket/postgresql/ --recursive
aws s3 ls s3://your-backup-bucket/qdrant/ --recursive

# Check backup integrity
aws s3 cp s3://your-backup-bucket/postgresql/latest.sql.gz /tmp/
gunzip -t /tmp/latest.sql.gz && echo "Backup integrity OK" || echo "Backup corrupted"
```

**Recovery Steps**:

1. **Stop Application Services**:
```bash
# Scale down applications to prevent data writes
kubectl scale deployment n8n-mcp-api -n n8n-mcp-prod --replicas=0
kubectl scale deployment n8n-mcp-rag -n n8n-mcp-prod --replicas=0
kubectl scale deployment n8n-mcp-workflows -n n8n-mcp-prod --replicas=0
```

2. **Restore Database**:
```bash
# Download backup
aws s3 cp s3://your-backup-bucket/postgresql/n8n_mcp_20240108_020000.sql.gz /tmp/

# Restore PostgreSQL
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "DROP DATABASE n8n_mcp;"
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -c "CREATE DATABASE n8n_mcp;"

gunzip /tmp/n8n_mcp_20240108_020000.sql.gz
kubectl exec -i postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp < /tmp/n8n_mcp_20240108_020000.sql
```

3. **Restore Vector Database**:
```bash
# Download Qdrant backup
aws s3 cp s3://your-backup-bucket/qdrant/documents_20240108.snapshot /tmp/

# Restore Qdrant collection
curl -X PUT "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents/snapshots/upload" \
  --data-binary @/tmp/documents_20240108.snapshot
```

4. **Verify Recovery**:
```bash
# Check database connectivity
kubectl exec -it postgresql-0 -n n8n-mcp-prod -- psql -U postgres -d n8n_mcp -c "SELECT COUNT(*) FROM workflows;"

# Check Qdrant collection
curl -X GET "http://qdrant.n8n-mcp-prod.svc.cluster.local:6333/collections/documents"

# Restart applications
kubectl scale deployment n8n-mcp-api -n n8n-mcp-prod --replicas=3
kubectl scale deployment n8n-mcp-rag -n n8n-mcp-prod --replicas=2
kubectl scale deployment n8n-mcp-workflows -n n8n-mcp-prod --replicas=2
```

---

## 📊 **Monitoring and Alerting**

### **Runbook 8: Alert Investigation and Response**

**Issue**: System alerts requiring investigation  
**Severity**: Varies by alert  
**Symptoms**: Alert notifications, performance degradation

**Alert Response Matrix**:

```yaml
Critical Alerts:
  - System Down: Follow emergency response procedures
  - Data Loss: Initiate backup recovery procedures
  - Security Breach: Follow security incident response

High Priority Alerts:
  - High CPU/Memory: Scale resources, investigate root cause
  - Database Issues: Check connections, optimize queries
  - API Errors: Check logs, restart services if needed

Medium Priority Alerts:
  - Performance Degradation: Monitor trends, plan optimization
  - Cache Miss Rate: Investigate cache configuration
  - Disk Space: Clean up logs, expand storage

Low Priority Alerts:
  - Minor Performance Issues: Schedule maintenance
  - Configuration Warnings: Plan configuration updates
  - Capacity Planning: Review resource allocation
```

**Standard Alert Response**:

1. **Acknowledge Alert**:
```bash
# Acknowledge alert in monitoring system
curl -X POST "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/alerts/{alert_id}/acknowledge" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

2. **Investigate Root Cause**:
```bash
# Check system status
kubectl get pods -n n8n-mcp-prod
kubectl top nodes
kubectl top pods -n n8n-mcp-prod

# Review logs
kubectl logs -n n8n-mcp-prod deployment/n8n-mcp-api --tail=100
```

3. **Implement Resolution**:
```bash
# Apply appropriate resolution based on alert type
# (See specific runbooks above)
```

4. **Verify Resolution**:
```bash
# Monitor metrics for improvement
curl -s "https://api.n8n-mcp.yourdomain.com/api/v1/monitoring/metrics?metric=response_time&duration=30m" | jq
```

5. **Document Incident**:
```bash
# Create incident report
kubectl exec -it n8n-mcp-api-0 -n n8n-mcp-prod -- python -m scripts.create_incident_report \
  --alert-id "alert_123" \
  --resolution "Scaled application pods" \
  --root-cause "High traffic load"
```

This comprehensive troubleshooting guide provides systematic approaches to resolving common issues in the RAG-Enhanced N8N System. Regular practice of these procedures ensures rapid response and minimal downtime during incidents.
