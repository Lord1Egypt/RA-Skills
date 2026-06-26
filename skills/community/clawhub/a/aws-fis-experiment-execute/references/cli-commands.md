# CLI Commands Reference

AWS CLI command reference for FIS experiment stack verification and execution.
All commands use `{PLACEHOLDERS}` for values that must be replaced.

**Note:** This skill does NOT deploy infrastructure. For deployment commands, see
the `aws-fis-experiment-prepare` skill.

---

## CloudFormation Stack Verification Commands

### Check Stack Status

```bash
aws cloudformation describe-stacks \
  --stack-name "{STACK_NAME}" \
  --region {REGION} \
  --query 'Stacks[0].{
    StackName: StackName,
    StackStatus: StackStatus,
    CreationTime: CreationTime,
    LastUpdatedTime: LastUpdatedTime,
    StackStatusReason: StackStatusReason
  }' --output table
```

### Get Stack Outputs

```bash
aws cloudformation describe-stacks \
  --stack-name "{STACK_NAME}" \
  --query 'Stacks[0].Outputs' \
  --region {REGION} --output table
```

### Extract Experiment Template ID from Stack Outputs

```bash
TEMPLATE_ID=$(aws cloudformation describe-stacks \
  --stack-name "{STACK_NAME}" \
  --query 'Stacks[0].Outputs[?OutputKey==`ExperimentTemplateId`].OutputValue' \
  --output text --region {REGION})

echo "Experiment Template ID: ${TEMPLATE_ID}"
```

### Get Stack Events (for debugging failed stacks)

```bash
aws cloudformation describe-stack-events \
  --stack-name "{STACK_NAME}" \
  --region {REGION} \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`].{
    Resource: LogicalResourceId,
    Status: ResourceStatus,
    Reason: ResourceStatusReason,
    Time: Timestamp
  }' --output table
```

### List All Stack Resources

```bash
aws cloudformation list-stack-resources \
  --stack-name "{STACK_NAME}" \
  --region {REGION} \
  --query 'StackResourceSummaries[].{
    Resource: LogicalResourceId,
    Type: ResourceType,
    Status: ResourceStatus,
    PhysicalId: PhysicalResourceId
  }' --output table
```

---

## FIS Experiment Template Commands

### Get Experiment Template Details

```bash
aws fis get-experiment-template \
  --id "{TEMPLATE_ID}" \
  --region {REGION}
```

### List Experiment Templates

```bash
aws fis list-experiment-templates \
  --query 'experimentTemplates[].{id:id, description:description, tags:tags}' \
  --region {REGION} --output table
```

### Verify Template Exists

```bash
aws fis get-experiment-template \
  --id "{TEMPLATE_ID}" \
  --region {REGION} \
  --query '{
    Id: experimentTemplate.id,
    Description: experimentTemplate.description,
    StopConditions: experimentTemplate.stopConditions,
    Actions: experimentTemplate.actions
  }' --output json
```

---

## FIS Experiment Execution Commands

### Start Experiment

```bash
EXPERIMENT_RESPONSE=$(aws fis start-experiment \
  --experiment-template-id "{TEMPLATE_ID}" \
  --region {REGION} \
  --output json)

EXPERIMENT_ID=$(echo "$EXPERIMENT_RESPONSE" | jq -r '.experiment.id')
echo "Experiment ID: $EXPERIMENT_ID"
```

### Get Experiment Status

```bash
aws fis get-experiment \
  --id "{EXPERIMENT_ID}" \
  --region {REGION} \
  --query '{
    Status: experiment.state.status,
    Reason: experiment.state.reason,
    StartTime: experiment.startTime,
    EndTime: experiment.endTime
  }' --output table
```

### Get Experiment Action Details

```bash
aws fis get-experiment \
  --id "{EXPERIMENT_ID}" \
  --region {REGION} \
  --query 'experiment.actions' --output json
```

### Stop Experiment (Emergency)

```bash
aws fis stop-experiment \
  --id "{EXPERIMENT_ID}" \
  --region {REGION}
```

### List Recent Experiments

```bash
aws fis list-experiments \
  --query 'experiments[?state.status!=`completed`].{id:id, status:state.status, templateId:experimentTemplateId}' \
  --region {REGION} --output table
```

### List All Experiments for Template

```bash
aws fis list-experiments \
  --query "experiments[?experimentTemplateId==\`{TEMPLATE_ID}\`].{
    id:id,
    status:state.status,
    startTime:startTime,
    endTime:endTime
  }" \
  --region {REGION} --output table
```

---

## Monitoring Commands (During Experiment)

### Poll Experiment Status (loop)

```bash
EXPERIMENT_ID="{EXPERIMENT_ID}"
REGION="{REGION}"
MAX_POLL=30  # max 30 polls × 30s = 15 minutes
POLL_COUNT=0

while [ $POLL_COUNT -lt $MAX_POLL ]; do
  STATUS=$(aws fis get-experiment \
    --id "${EXPERIMENT_ID}" \
    --region ${REGION} \
    --query 'experiment.state.status' --output text 2>/dev/null)
  echo "$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M:%S'): Status = $STATUS"
  if [ -z "$STATUS" ] || [ "$STATUS" = "None" ]; then
    echo "ERROR: Failed to get experiment status (invalid experiment ID or API error)"
    break
  fi
  case "$STATUS" in
    completed|stopped|failed) break ;;
    *) POLL_COUNT=$((POLL_COUNT + 1)); sleep 30 ;;
  esac
done

if [ $POLL_COUNT -ge $MAX_POLL ]; then
  echo "WARN: Polling timed out after $((MAX_POLL * 30 / 60)) minutes"
fi
```

### Check Alarm State

```bash
aws cloudwatch describe-alarms \
  --alarm-names "FIS-StopCondition-{SCENARIO}-{SERVICE}" \
  --query 'MetricAlarms[].{Name:AlarmName, State:StateValue, Reason:StateReason}' \
  --region {REGION} --output table
```

### Get Recent Metric Data

```bash
aws cloudwatch get-metric-statistics \
  --namespace "{NAMESPACE}" \
  --metric-name "{METRIC}" \
  --dimensions "Name={DIM_NAME},Value={DIM_VALUE}" \
  --start-time "$(TZ=UTC date -v-30M +%Y-%m-%dT%H:%M:%S)" \
  --end-time "$(TZ=UTC date +%Y-%m-%dT%H:%M:%S)" \
  --period 60 \
  --statistics Average \
  --region {REGION} --output table
```

### Get Dashboard URL

```
https://{REGION}.console.aws.amazon.com/cloudwatch/home?region={REGION}#dashboards:name=FIS-{SCENARIO}
```

---

## Cleanup Commands

### Delete Stack (Recommended)

Deleting the stack removes all resources created by it (IAM role, alarms, dashboard, FIS template).

```bash
aws cloudformation delete-stack \
  --stack-name "{STACK_NAME}" \
  --region {REGION}

aws cloudformation wait stack-delete-complete \
  --stack-name "{STACK_NAME}" \
  --region {REGION}
```

### Delete Experiment Template Only

If you need to delete just the FIS template (without the full stack):

```bash
aws fis delete-experiment-template \
  --id "{TEMPLATE_ID}" \
  --region {REGION}
```

### Delete CloudWatch Alarms Only

```bash
aws cloudwatch delete-alarms \
  --alarm-names "FIS-StopCondition-{SCENARIO}-{SERVICE}" \
  --region {REGION}
```

### Delete CloudWatch Dashboard Only

```bash
aws cloudwatch delete-dashboards \
  --dashboard-names "FIS-{SCENARIO}" \
  --region {REGION}
```

---

## FIS Action Discovery Commands

### List All FIS Actions in Region

```bash
aws fis list-actions \
  --region {REGION} \
  --query 'actions[].{id:id, description:description}' \
  --output table
```

### List Actions for Specific Service

```bash
aws fis list-actions \
  --region {REGION} \
  --query 'actions[?starts_with(id, `aws:{SERVICE}:`)].{id:id, description:description}' \
  --output table
```

### Get Action Details

```bash
aws fis get-action \
  --id "{ACTION_ID}" \
  --region {REGION}
```

---

## Status Reference

### Stack Status Values

| Status | Meaning | Action |
|---|---|---|
| `CREATE_COMPLETE` | Stack created successfully | Ready for experiment |
| `UPDATE_COMPLETE` | Stack updated successfully | Ready for experiment |
| `CREATE_IN_PROGRESS` | Stack being created | Wait and re-check |
| `UPDATE_IN_PROGRESS` | Stack being updated | Wait and re-check |
| `CREATE_FAILED` | Stack creation failed | Check events, fix, redeploy |
| `ROLLBACK_COMPLETE` | Creation failed, rolled back | Check events, fix, redeploy |
| `DELETE_COMPLETE` | Stack deleted | Stack no longer exists |
| `DELETE_IN_PROGRESS` | Stack being deleted | Wait for deletion |

### Experiment Status Values

| Status | Meaning |
|---|---|
| `initiating` | Experiment is starting |
| `running` | Experiment is in progress |
| `completed` | Experiment finished successfully |
| `stopping` | Being stopped (by user or stop condition) |
| `stopped` | Stopped before completion |
| `failed` | Experiment failed |
