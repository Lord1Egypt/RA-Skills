# Correlation Plugin Deployment Guide

## Prerequisites

Before deploying the correlation plugin, ensure you have:

1. OpenClaw >= 2026.1.26 installed
2. Access to the OpenClaw workspace directory
3. Git installed and configured
4. Proper permissions to modify the OpenClaw configuration

## Deployment Steps

### 1. Clone the Repository

```bash
cd ~/.openclaw/extensions
git clone https://github.com/ether-btc/openclaw-correlation-plugin.git correlation-memory
```

### 2. Install Dependencies

```bash
cd ~/.openclaw/extensions/correlation-memory
npm install
```

### 3. Configure Plugin

Add the plugin to your `openclaw.json` configuration file:

```json
{
  "plugins": {
    "allow": ["correlation-memory"]
  }
}
```

### 4. Create Correlation Rules

Create `memory/correlation-rules.json` in your workspace with your correlation rules:

```json
{
  "rules": [
    {
      "id": "cr-001",
      "trigger_context": "config-change",
      "trigger_keywords": ["config", "setting", "change"],
      "must_also_fetch": ["backup-location", "rollback-instructions"],
      "relationship_type": "constrains",
      "confidence": 0.95
    }
  ]
}
```

### 5. Restart OpenClaw Gateway

```bash
openclaw gateway restart
```

## Failsafe Checklist

### Pre-Deployment Validation

- [ ] Backup current OpenClaw configuration
- [ ] Verify OpenClaw version compatibility
- [ ] Test plugin installation in isolated environment
- [ ] Validate correlation rules syntax
- [ ] Document rollback procedure

### Deployment Verification

- [ ] Confirm plugin loads without errors
- [ ] Test basic correlation functionality
- [ ] Verify no performance degradation
- [ ] Check gateway logs for warnings
- [ ] Validate rule matching behavior

### Post-Deployment Monitoring

- [ ] Monitor memory usage
- [ ] Check for unexpected correlations
- [ ] Review user feedback
- [ ] Validate production rule effectiveness
- [ ] Schedule follow-up evaluation

## Rollback Procedure

If issues arise after deployment:

### 1. Immediate Action

```bash
# Stop gateway
openclaw gateway stop

# Remove plugin from configuration
# Edit openclaw.json to remove "correlation-memory" from plugins.allow
```

### 2. Restore Configuration

```bash
# Restore from backup if available
cp ~/.openclaw/openclaw.json.backup ~/.openclaw/openclaw.json
```

### 3. Restart Services

```bash
# Restart gateway
openclaw gateway start
```

### 4. Verify Stability

- [ ] Confirm gateway is running
- [ ] Check logs for errors
- [ ] Validate normal functionality

## Error Classification

### Critical Errors (Immediate Rollback)

- Gateway fails to start
- Memory corruption detected
- Performance degradation >50%
- Security violations

### Major Errors (Investigate Within 24 Hours)

- Incorrect correlation results
- Performance degradation 20-50%
- Configuration conflicts
- User experience issues

### Minor Errors (Monitor and Address)

- Minor performance impact (<20%)
- Non-critical logging issues
- Cosmetic display problems
- Documentation inconsistencies

## Testing Procedures

### Unit Tests

Run the built-in test suite:

```bash
cd ~/.openclaw/extensions/correlation-memory
npm test
```

### Integration Tests

1. Test rule matching with sample queries
2. Verify correlation results accuracy
3. Check performance impact on memory searches
4. Validate configuration edge cases

### Production Validation

1. Deploy to staging environment first
2. Monitor for 24 hours with representative workload
3. Collect user feedback
4. Address any issues before production rollout

## Troubleshooting

### Common Issues

1. **Plugin not loading**
   - Check OpenClaw version compatibility
   - Verify plugin directory structure
   - Confirm entry in plugins.allow

2. **No correlations returned**
   - Validate correlation rules syntax
   - Check rule confidence thresholds
   - Verify matching mode settings

3. **Performance issues**
   - Review correlation rule complexity
   - Check for circular dependencies
   - Monitor memory usage patterns

### Diagnostic Commands

```bash
# Check gateway status
openclaw gateway status

# View recent logs
openclaw logs --lines 100

# Validate configuration
openclaw doctor

# Test correlation manually
openclaw exec correlation_check --context "your-test-context"
```

## Monitoring

### Key Metrics to Watch

- Memory search response time
- Correlation rule match rate
- False positive correlation rate
- User interaction with correlated results
- Gateway stability metrics

### Alerting Thresholds

- Response time >2x baseline
- Error rate >1%
- Memory usage >80% of limit
- Correlation match rate <5% (may indicate rules need tuning)