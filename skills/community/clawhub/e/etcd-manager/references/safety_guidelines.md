# etcd Safety Guidelines

## Core Principles

### 1. Read-First Approach
- Always prefer read operations over write operations
- Verify current state before making changes
- Use `list` and `get` to understand the data structure

### 2. Backup Before Modification
- Always show the old value before `put` operations
- Always backup before `delete` operations
- Keep audit logs of all modifications

### 3. Production Protection
- Be extra cautious with production environments
- Require explicit confirmation for prod operations
- Implement rate limiting for prod writes

### 4. Environment Awareness
- Clearly identify environment (dev/test/prod)
- Apply different safety levels per environment
- Use environment-specific endpoints

## Safety Levels

### Development Environment
- **Risk Level**: Low
- **Allowed Operations**: All
- **Safety Checks**: Basic backup
- **Confirmation Required**: No

### Test Environment
- **Risk Level**: Medium
- **Allowed Operations**: All
- **Safety Checks**: Full backup
- **Confirmation Required**: For destructive operations

### Production Environment
- **Risk Level**: High
- **Allowed Operations**: Read-heavy, limited writes
- **Safety Checks**: Full backup + audit
- **Confirmation Required**: Always for writes

## Operation Safety Matrix

| Operation | Dev Safety | Test Safety | Prod Safety |
|-----------|------------|-------------|-------------|
| **list**  | ✅ Safe    | ✅ Safe     | ✅ Safe     |
| **get**   | ✅ Safe    | ✅ Safe     | ✅ Safe     |
| **put**   | ⚠️ Medium  | ⚠️ Medium   | 🔴 High     |
| **delete**| 🔴 High    | 🔴 High     | 🔴 Critical |

## Safety Procedures

### Before Any Write Operation
1. **Identify environment**
2. **Check operation safety level**
3. **Backup current state**
4. **Get user confirmation** (if required)
5. **Execute with caution**

### After Any Write Operation
1. **Verify the change**
2. **Log the operation**
3. **Report success/failure**
4. **Provide backup reference**

## Backup Strategy

### What to Backup
- Key being modified
- Old value (if exists)
- Timestamp of operation
- User/agent who performed operation
- Reason for modification

### Backup Storage
```bash
# Example backup format
BACKUP_DIR="/var/backup/etcd/$(date +%Y%m%d)"
echo "KEY: $KEY" >> "$BACKUP_DIR/backup.log"
echo "OLD_VALUE: $OLD_VALUE" >> "$BACKUP_DIR/backup.log"
echo "NEW_VALUE: $NEW_VALUE" >> "$BACKUP_DIR/backup.log"
echo "TIME: $(date)" >> "$BACKUP_DIR/backup.log"
echo "OPERATOR: $USER" >> "$BACKUP_DIR/backup.log"
echo "---" >> "$BACKUP_DIR/backup.log"
```

## Error Handling

### Connection Errors
- Retry with exponential backoff
- Log connection failures
- Notify administrators for persistent failures

### Permission Errors
- Check authentication credentials
- Verify key permissions
- Escalate if permission issues persist

### Data Corruption
- Restore from backup
- Validate data integrity
- Investigate root cause

## Audit Logging

### Required Log Fields
- **Timestamp**: When the operation occurred
- **Operation**: What was done (list/get/put/delete)
- **Key**: Which key was affected
- **Old Value**: Previous value (for modifications)
- **New Value**: New value (for modifications)
- **Environment**: dev/test/prod
- **Operator**: Who performed the operation
- **Status**: Success/failure
- **Error Message**: If operation failed

### Log Retention
- **Development**: 7 days
- **Test**: 30 days
- **Production**: 90 days

## Recovery Procedures

### Data Recovery
1. Identify when corruption occurred
2. Locate latest clean backup
3. Restore affected keys
4. Validate restoration
5. Update audit logs

### Service Recovery
1. Check etcd cluster health
2. Restart failed nodes
3. Verify data consistency
4. Resume normal operations

## Best Practices

### 1. Regular Backups
- Schedule daily backups
- Test backup restoration
- Store backups in multiple locations

### 2. Monitoring
- Monitor etcd cluster health
- Alert on abnormal patterns
- Track operation rates

### 3. Access Control
- Use RBAC for production
- Limit write permissions
- Regularly review access logs

### 4. Documentation
- Document all procedures
- Keep runbooks updated
- Train team members

## Emergency Contacts

### Development Issues
- Primary: Team Lead
- Secondary: DevOps Engineer

### Production Issues
- Primary: On-call Engineer
- Secondary: Infrastructure Lead
- Escalation: CTO

---

**Remember**: When in doubt, don't proceed. Always err on the side of caution when dealing with etcd operations.