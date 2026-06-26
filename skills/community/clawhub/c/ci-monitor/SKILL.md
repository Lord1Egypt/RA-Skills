---
name: ci-monitor
description: >
  Monitor and interact with CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI).
  Check build status, trigger builds, analyze failed jobs, view logs.
  Use when: (1) checking build/pipeline status, (2) triggering test builds,
  (3) analyzing CI failures, (4) monitoring deployment status,
  (5) "查看构建状态", "Jenkins", "流水线", "CI失败了", "触发构建".
  Requires: curl for API calls. Jenkins needs JENKINS_URL and JENKINS_TOKEN env vars.
  NOT for: configuring CI pipelines (edit Jenkinsfile/yaml directly), or managing
  infrastructure.
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: [curl]
---

# CI Monitor

Monitor, trigger, and analyze CI/CD pipeline status.

## When to Use

✅ **USE this skill when:**
- Checking build/pipeline status
- Analyzing why a CI job failed
- Triggering builds or test runs
- Monitoring deployment progress
- "Jenkins 构建状态怎么样" / "CI 挂了看看什么原因"

❌ **DON'T use this skill when:**
- Writing/editing Jenkinsfile or CI config → edit files directly
- Managing infrastructure → use DevOps tools
- Code review → use platform web UI or `gh` CLI directly

## Jenkins

### Setup

```bash
# Set environment variables
export JENKINS_URL="https://jenkins.example.com"
export JENKINS_USER="admin"
export JENKINS_TOKEN="your-api-token"
```

### Common Operations

```bash
# List all jobs
curl -s "$JENKINS_URL/api/json?tree=jobs[name,color]" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | jq '.jobs[] | "\(.name): \(.color)"'

# Get last build status
curl -s "$JENKINS_URL/job/{job-name}/lastBuild/api/json" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | jq '{result,duration,timestamp,builtOn}'

# Get console output of last build
curl -s "$JENKINS_URL/job/{job-name}/lastBuild/consoleText" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | tail -50

# Trigger a build
curl -s -X POST "$JENKINS_URL/job/{job-name}/build" \
  --user "$JENKINS_USER:$JENKINS_TOKEN"

# Trigger with parameters
curl -s -X POST "$JENKINS_URL/job/{job-name}/buildWithParameters?BRANCH=develop&ENV=staging" \
  --user "$JENKINS_USER:$JENKINS_TOKEN"

# Get build queue
curl -s "$JENKINS_URL/queue/api/json" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | jq '.items[] | {task: .task.name, why}'
```

### Failure Analysis

When a build fails:

1. **Get build result and duration**:
```bash
curl -s "$JENKINS_URL/job/{job}/lastBuild/api/json" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | jq '{result,duration,timestamp}'
```

2. **Get failed test report**:
```bash
curl -s "$JENKINS_URL/job/{job}/lastBuild/testReport/api/json" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | jq '{failCount,passCount,skipCount,suites[].cases[] | select(.status=="FAILED") | {name,errorDetails}}'
```

3. **Get console log (last 200 lines)**:
```bash
curl -s "$JENKINS_URL/job/{job}/lastBuild/consoleText" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" | tail -200 | grep -i -E "error|fail|exception" 
```

4. **Summarize findings** in this format:
```
🔴 Build #{number} FAILED
⏱️ Duration: Xm Ys
📋 Tests: X passed, Y failed, Z skipped
❌ Failed tests:
  - TestClass.testMethod: error message
  - TestClass.testMethod2: error message
🔍 Root cause: [analysis based on logs]
💡 Suggestion: [fix suggestion]
```

## GitHub Actions

Uses `gh` CLI or REST API:

```bash
# List recent workflow runs
gh run list --repo owner/repo --limit 10

# View specific run
gh run view {run-id} --repo owner/repo

# View failed step logs
gh run view {run-id} --repo owner/repo --log-failed

# Re-run failed jobs
gh run rerun {run-id} --failed --repo owner/repo

# Trigger workflow
gh workflow run {workflow-name} --repo owner/repo --ref main
```

## GitLab CI

```bash
# Set variables
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="your-private-token"
export PROJECT_ID="123"

# List pipelines
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/pipelines?per_page=5" | jq '.[] | {id,status,ref,created_at}'

# Get pipeline jobs
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/pipelines/{pipeline-id}/jobs" | jq '.[] | {name,status,duration}'

# Get job log
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/jobs/{job-id}/trace" | tail -100

# Retry failed pipeline
curl -s -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/pipelines/{pipeline-id}/retry"
```

## Build Status Summary Format

When reporting build status, use:

```
📊 CI Status Report - {project}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Build #123 (main)    - PASSED  2m 30s
🔴 Build #122 (develop) - FAILED  5m 10s
🟡 Build #124 (feature) - RUNNING 1m 20s
⚪ Build #125 (hotfix)  - QUEUED
```
