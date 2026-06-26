---
name: dp-ops-advisor
description: |
  DP 数据处理平台运维顾问。当用户提到检查平台、作业失败、作业状态、吞吐量分析、故障诊断、运维报告等运维需求时激活。
---

# dp-ops-advisor

## Purpose

Monitor, diagnose, and advise on **DP Data Processing Platform** job operations. This skill provides intelligent operational support: checking job health, interpreting metrics, diagnosing failures, suggesting fixes, and generating incident reports.

## Environment Configuration

The DP platform runs at `${DP_SERVER_URL}`.

Required environment variables:
```bash
 DP_SERVER_URL=${DP_SERVER_URL}   # REQUIRED — DP platform base URL
DP_API_KEY=${DP_API_KEY}         # REQUIRED — obtain from platform「API Key 管理」page
```

ALL curl commands MUST use `-H 'X-DP-API-Key: ${DP_API_KEY}'`. No other authentication method is supported.

## 首次使用引导

```bash
# 校验 DP_API_KEY — 未配置则终止
if [ -z "${DP_API_KEY}" ]; then
  echo "======================================"
  echo "  DP Platform — API Key 必填"
  echo "======================================"
  echo "错误：未检测到 DP_API_KEY，无法继续。"
  echo ""
  echo "请按以下步骤配置："
  echo "1. 访问 DP 平台控制台：${DP_SERVER_URL}"
  echo "2. 注册账号（如需邀请码请联系管理员）"
  echo "3. 进入「API Key 管理」→「申请新 Key」"
  echo "4. 将生成的 Key 配置到 DP_API_KEY 环境变量"
  echo ""
  echo "免费版：100次/月。超额后需升级订阅套餐。"
  echo "======================================"
  exit 1
fi
echo "API Key 已验证：${DP_API_KEY:0:8}****"
```

## 配额说明

- **免费版**：100 次/月 API 调用额度
- 超额时响应中会包含 `quota_exceeded: true` 字段
- 响应中的 `upgrade_url` 字段指向订阅升级页面
- 升级套餐可获得更多额度：BASIC(1000次)、PRO(10000次)、ENTERPRISE(不限)

---

## Capabilities

- Real-time health check of all jobs (running/failed/stalled)
- Per-operator throughput and latency analysis
- Failure root-cause analysis from error logs
- Auto-restart policy evaluation and execution
- Stall detection (job running but no data flowing)
- Historical run trend analysis
- Generate incident report summaries
- Recommend configuration tuning based on observed metrics

---

## Context Files

| File | Purpose |
|---|---|
| `dp-api-reference.md` | REST API endpoints for status, logs, progress |
| `dp-operator-catalog.json` | Operator descriptions to contextualize metrics |

---

## Prerequisites Check

```bash
# Verify DP Server connectivity
curl -s --connect-timeout 3 ${DP_SERVER_URL}/homepage && echo "DP Server OK" || echo "DP Server NOT running"

# Auth: API Key is REQUIRED — no session fallback allowed
if [ -z "${DP_API_KEY}" ]; then
  echo "ERROR: DP_API_KEY is not set. Please configure DP_API_KEY environment variable."
  exit 1
fi
AUTH="-H 'X-DP-API-Key: ${DP_API_KEY}'"
echo "Auth: API Key mode (${DP_API_KEY:0:8}****)"
```

---

## Workflow

### Mode 1: Platform Health Check (全局健康检查)

Triggered when user says: "检查平台状态" / "哪些作业有问题" / "平台健不健康"

```bash
# Get all job statuses
ALL_STATUS=$(curl -H "X-DP-API-Key: ${DP_API_KEY}" -s "${DP_SERVER_URL}/job/status")

# Parse and categorize
echo "$ALL_STATUS" | python3 -c "
import sys, json
jobs = json.load(sys.stdin)

running = [j for j in jobs if j.get('state') == 'RUNNING']
failed  = [j for j in jobs if j.get('state') == 'FAILED']
stoping = [j for j in jobs if j.get('state') == 'STOPING']
waiting = [j for j in jobs if j.get('state') == 'Waiting']
finished= [j for j in jobs if j.get('state') == 'FINISHED']
idle    = [j for j in jobs if not j.get('state')]

print('=== DP Platform Health Report ===')
print(f'Total jobs: {len(jobs)}')
print(f'  RUNNING  : {len(running)}')
print(f'  FAILED   : {len(failed)}')
print(f'  FINISHED : {len(finished)}')
print(f'  WAITING  : {len(waiting)}')
print(f'  IDLE     : {len(idle)}')
print()

if failed:
    print('!! FAILED JOBS (need attention):')
    for j in failed:
        print(f'   - {j.get("jobID","?")} | {j.get("state")}')
    print()

if running:
    print('OK RUNNING JOBS:')
    for j in running:
        print(f'   - {j.get("jobID","?")}')
"
```

**After health check, proactively**:
- For each FAILED job: offer to diagnose (Mode 3)
- For each RUNNING job: offer to check throughput (Mode 2)

---

### Mode 2: Job Throughput Analysis (吞吐量分析)

Triggered when user says: "看一下 [job] 的运行情况" / "数据有没有在流动" / "作业跑的快不快"

```bash
JOB_ID="$1"  # job ID from user or from health check

# Get per-operator metrics
PROGRESS=$(curl -H "X-DP-API-Key: ${DP_API_KEY}" -s "${DP_SERVER_URL}/job/progress?id=$JOB_ID")

echo "$PROGRESS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Job: {data["name"]} (ID: {data["id"]})')
print(f'Path: {data.get("path","")}')
print()
print(f'{'Operator':<30} {'Status':<12} {'Records In':<15} {'Records Out':<15} {'Speed(rec/s)':<15} {'ByteSpeed':<12}')
print('-' * 100)
for op in data.get('data', []):
    status = op.get('status', '-')
    r_in   = op.get('recordsRead', '-')
    r_out  = op.get('recordsWritten', '-')
    speed  = op.get('speed', '-')
    bspeed = op.get('byteSpeed', '-')
    name   = op.get('name', op.get('id', '?'))[:28]
    
    # Flag potential stall: speed=0 but status=RUNNING
    flag = ' !! STALLED?' if status == 'RUNNING' and speed == '0' else ''
    print(f'{name:<30} {status:<12} {r_in:<15} {r_out:<15} {speed:<15} {bspeed:<12}{flag}')
"
```

**Stall Detection Logic**:

A job is stalled if:
- `status = RUNNING` but `speed = 0` AND `recordsRead` has not changed over 2 consecutive checks

When stall detected:
```bash
# Take two readings 30 seconds apart and compare recordsRead
PROG1=$(curl -H "X-DP-API-Key: ${DP_API_KEY}" -s "${DP_SERVER_URL}/job/progress?id=$JOB_ID")
sleep 30
PROG2=$(curl -H "X-DP-API-Key: ${DP_API_KEY}" -s "${DP_SERVER_URL}/job/progress?id=$JOB_ID")

python3 -c "
import sys, json
p1 = json.loads('$PROG1')
p2 = json.loads('$PROG2')
ops1 = {op['id']: op for op in p1.get('data',[])}
ops2 = {op['id']: op for op in p2.get('data',[])}
print('Stall detection (30s interval):')
for pid, op2 in ops2.items():
    op1 = ops1.get(pid, {})
    r1 = op1.get('recordsRead','0')
    r2 = op2.get('recordsRead','0')
    if r1 == r2 and op2.get('status') == 'RUNNING':
        print(f'  STALLED: {op2.get("name",pid)} - records unchanged at {r2}')
    else:
        delta = str(int(r2 or 0) - int(r1 or 0)) if r1 != '-' and r2 != '-' else '?'
        print(f'  OK: {op2.get("name",pid)} - processed +{delta} records')
"
```

---

## Response Format

Always structure responses with:

```
[Health]: Overall platform/job status

[Findings]: Specific issues identified

[Diagnosis]: Root cause analysis

[Actions]: What was done or should be done

[Status]: Current state after any actions
```

---

## Limitations & Guardrails

1. **Never auto-restart without user confirmation** in production scenarios.
2. **Never modify job configurations** — only report and advise (use `dp-pipeline-designer` skill to make changes).
3. **Do not expose raw stack traces** to non-technical users — summarize the error in plain language.
4. **If DP Server is unreachable**, guide user to check and start services. Provide the startup command.
5. **Session refresh**: If API returns "Authentication required", automatically re-login before retrying.
