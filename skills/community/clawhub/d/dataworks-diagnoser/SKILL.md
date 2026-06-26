---
name: dataworks-diagnoser
description: DataWorks task instance log fetcher and diagnostician. Use when: user needs to troubleshoot failed DataWorks task instances, analyze error logs, get diagnostic recommendations for task failures, or understand why a DataWorks node failed. Requires Alibaba Cloud credentials. Supports all DataWorks task types including ODPS SQL, Sync, Shell, Python, etc.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl", "python3"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
          ],
      },
  }
---

# DataWorks Task Instance Diagnostician

Fetches task instance logs from Alibaba Cloud DataWorks API and provides intelligent diagnostic recommendations.

## Quick Start

**Diagnose a failed task:**
```bash
python3 scripts/dataworks_diagnose.py <instance_id>
```

**Example:**
```bash
python3 scripts/dataworks_diagnose.py 123456789
```

## When to Use

✅ **USE this skill when:**

- DataWorks task instance failed and you need to know why
- You have an instance ID and need to fetch error logs
- You want automated diagnosis and solutions for task failures
- Troubleshooting ODPS SQL, Data Integration, Shell, Python nodes
- Need to analyze error patterns across multiple failures
- Preparing incident reports for failed tasks

## When NOT to Use

❌ **DON'T use this skill when:**

- You need real-time task monitoring (use DataWorks console)
- You want to modify task configurations (use console or API directly)
- You need historical analytics across many tasks (use DataWorks reports)
- The task is still running (wait for completion first)
- You don't have Alibaba Cloud credentials (need AccessKey)

## Prerequisites

### 1. Alibaba Cloud Credentials

One of the following is required:

**Option A: Environment Variables (Recommended)**
```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=your_access_key
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_access_secret
```

**Option B: Config File**
Create `~/.alibabacloud/credentials`:
```json
{
  "access_key_id": "your_access_key",
  "access_key_secret": "your_access_secret"
}
```

**Option C: Aliyun CLI Config**
If you have Aliyun CLI configured, credentials will be loaded automatically.

### 2. Required Permissions

The AccessKey needs these permissions:
- `dataworks:GetInstanceLog` - Fetch task instance logs
- `dataworks:QueryTask` - Query task information

### 3. Network Access

- Access to Alibaba Cloud API endpoints
- If using VPC, ensure proper network configuration

## Core Workflows

### 1. Quick Diagnosis (Recommended)

Fetch log and get diagnosis in one command:

```bash
python3 scripts/dataworks_diagnose.py <instance_id>
```

**Example:**
```bash
python3 scripts/dataworks_diagnose.py 123456789
```

**Output:**
```
🔍 开始诊断 DataWorks 任务实例：123456789
📍 区域：cn-hangzhou
------------------------------------------------------------

📥 步骤 1/2: 获取任务日志...
✅ 日志获取成功

🔬 步骤 2/2: 分析诊断中...
✅ 诊断完成

============================================================
📋 诊断报告
============================================================
🔍 DataWorks 任务实例诊断报告
============================================================
实例 ID: 123456789
发现问题数：2

----------------------------------------------------------------------
🔴 问题 1: 资源配额不足
   类型：resource_quota
   严重程度：HIGH
   
   相关日志:
     > ERROR: quota exceeded for resource group 'default'
     > No available slots in queue
   
   建议解决方案:
     1. 检查当前资源组的使用情况，释放闲置资源
     2. 联系管理员提升资源配额
     3. 优化任务配置，减少资源消耗
     4. 考虑错峰调度，避开资源使用高峰
   
   参考文档：https://help.aliyun.com/.../resource-group.html
```

### 2. Fetch Log Only

```bash
python3 scripts/fetch_instance_log.py <instance_id> [options]
```

**Options:**
```bash
# Specify region
python3 scripts/fetch_instance_log.py 123456789 --region cn-shanghai

# Output as JSON
python3 scripts/fetch_instance_log.py 123456789 --json

# Show full log (default: last 50 lines)
python3 scripts/fetch_instance_log.py 123456789 --verbose

# Save to file
python3 scripts/fetch_instance_log.py 123456789 > log.txt
```

### 3. Diagnose Existing Log

```bash
python3 scripts/diagnose_log.py <log_file>
```

**Examples:**
```bash
# From file
python3 scripts/diagnose_log.py error.log

# From stdin
cat log.txt | python3 scripts/diagnose_log.py

# With instance ID
python3 scripts/diagnose_log.py error.log --instance-id 123456789

# JSON output
python3 scripts/diagnose_log.py error.log --json

# Summary only
python3 scripts/diagnose_log.py error.log --summary
```

## Scripts

This skill includes three scripts:

### `dataworks_diagnose.py` - All-in-One Tool
Fetches log and provides diagnosis automatically.

**Usage:**
```bash
python3 scripts/dataworks_diagnose.py <instance_id> [options]
```

**Options:**
- `--region, -r` - Alibaba Cloud region (default: cn-hangzhou)
- `--json, -j` - Output as JSON
- `--verbose, -v` - Show full log
- `--save-log FILE` - Save raw log to file
- `--save-report FILE` - Save diagnostic report to file

### `fetch_instance_log.py` - Log Fetcher
Fetches task instance log from DataWorks API.

**Usage:**
```bash
python3 scripts/fetch_instance_log.py <instance_id> [options]
```

**Options:**
- `--region, -r` - Region (default: cn-hangzhou)
- `--access-key` - Access Key ID
- `--access-secret` - Access Key Secret
- `--json, -j` - JSON output
- `--verbose, -v` - Full log

### `diagnose_log.py` - Log Analyzer
Analyzes log content and provides diagnostic recommendations.

**Usage:**
```bash
python3 scripts/diagnose_log.py <log_file_or_stdin> [options]
```

**Options:**
- `--instance-id` - Task instance ID
- `--json, -j` - JSON output
- `--summary, -s` - Summary only

## Detected Error Patterns

The diagnostician recognizes these error types:

| Error Type | Severity | Examples |
|------------|----------|----------|
| 🔴 resource_quota | High | "quota exceeded", "资源不足" |
| 🔴 resource_expired | High | "expired", "独享资源组已过期", "bill exception" |
| 🔴 connection_timeout | High | "connection timeout", "network unreachable" |
| 🔴 permission_denied | High | "permission denied", "access denied" |
| 🟡 syntax_error | Medium | "syntax error", "parse error" |
| 🟡 table_not_found | Medium | "table not found", "doesn't exist" |
| 🟡 data_quality | Medium | "quality check failed" |
| 🔴 memory_overflow | High | "out of memory", "heap space" |
| 🔴 disk_full | High | "disk full", "no space left" |
| 🟡 dependency_failed | Medium | "dependency failed", "upstream failed" |
| 🟡 api_rate_limit | Medium | "rate limit exceeded" |

See `references/error_codes.md` for detailed error patterns and solutions.

## Common Regions

| Region | Code |
|--------|------|
| 华东 1 (杭州) | cn-hangzhou |
| 华东 2 (上海) | cn-shanghai |
| 华北 1 (青岛) | cn-qingdao |
| 华北 2 (北京) | cn-beijing |
| 华南 1 (深圳) | cn-shenzhen |
| 香港 | cn-hongkong |
| 新加坡 | ap-southeast-1 |

## API Reference

**API:** GetTaskInstanceLog  
**Version:** 2024-05-18  
**Endpoint:** `https://dataworks-public.{region}.aliyuncs.com/`

**Request Parameters:**
- `InstanceId` (required) - Task instance ID
- `RegionId` (required) - Region ID

**Response:**
```json
{
  "Data": {
    "LogContent": "...",
    "InstanceStatus": "FAILED",
    "CycleTime": "2024-01-15 10:30:00"
  },
  "Code": "200"
}
```

**Documentation:**
https://api.aliyun.com/api/dataworks-public/2024-05-18/GetTaskInstanceLog

## Examples

### Example 1: Quick Diagnosis
```bash
python3 scripts/dataworks_diagnose.py 123456789
```

### Example 2: Save Report
```bash
python3 scripts/dataworks_diagnose.py 123456789 --save-report diagnosis.txt
```

### Example 3: Different Region
```bash
python3 scripts/dataworks_diagnose.py 123456789 --region cn-shanghai
```

### Example 4: Analyze Saved Log
```bash
python3 scripts/diagnose_log.py saved_log.txt --instance-id 123456789
```

### Example 5: Batch Analysis
```bash
for id in 123 456 789; do
  python3 scripts/diagnose_log.py --instance-id $id < log_$id.txt
done
```

## Troubleshooting

### "Credentials not found"
```bash
# Set environment variables
export ALIBABA_CLOUD_ACCESS_KEY_ID=your_key
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_secret
```

### "Instance not found"
- Verify the instance ID is correct
- Check if the instance exists in DataWorks console
- Ensure you're using the correct region

### "Permission denied"
- Verify AccessKey has required permissions
- Check RAM role configuration
- Contact administrator for access

### "Request timeout"
- Check network connectivity
- Try increasing timeout in script
- Verify API endpoint is accessible

## Tips

💡 **Pro tips:**

1. **Save logs for failed tasks** - Use `--save-log` to keep records
2. **Generate reports** - Use `--save-report` for documentation
3. **Batch processing** - Script supports multiple instance IDs
4. **JSON output** - Use `--json` for programmatic processing
5. **Region matters** - Always use the correct region for your workspace

## Security

⚠️ **Important:**

- Never commit AccessKeys to version control
- Use RAM roles instead of main account keys
- Rotate keys regularly
- Use environment variables or secure config files
- Restrict key permissions to minimum required

## References

- `references/error_codes.md` - Complete error code reference
- [DataWorks Documentation](https://help.aliyun.com/product/27728.html)
- [API Reference](https://api.aliyun.com/api/dataworks-public)
- [Error Codes](https://help.aliyun.com/document_detail/dataworks/error-codes.html)
