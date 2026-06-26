---
name: aws-fis-experiment-execute
description: >
  Use when the user wants to run a prepared AWS FIS experiment where the
  CloudFormation stack has already been deployed. Triggers on "execute FIS
  experiment", "run FIS experiment", "start chaos experiment", "执行 FIS 实验",
  "运行混沌实验", "执行故障注入实验", "run the experiment in [directory]",
  or when the user provides an FIS experiment template ID (e.g. EXT1a2b3c4d5e6f7).
  Does NOT deploy infrastructure — only checks that it is already deployed.
---

# AWS FIS Experiment Execute

Verify that infrastructure is already deployed, run an AWS FIS experiment,
monitor its progress, and generate a results report. Reads configuration from
a prepared experiment directory whose CloudFormation stack has already been
deployed.

## Output Language Rule

Detect the language of the user's conversation and use the **same language** for all output.
- Chinese input -> Chinese output
- English input -> English output

## Prerequisites

Required tools:
- **AWS CLI** — `aws fis`, `aws cloudwatch`, `aws cloudformation`, `aws logs`
- **kubectl**  — configured with access to target EKS cluster. 
- A prepared experiment directory (from aws-fis-experiment-prepare skill)
- The CloudFormation stack for this experiment **must already be deployed**

**REQUIRED SUB-SKILL:** `app-service-log-analysis` must be installed. Loaded at
runtime for application discovery, log collection, and analysis. Without it, the
experiment can still run but log analysis will be skipped.

## Workflow

```dot
digraph execute_flow {
    "User input:\npath or template ID?" [shape=diamond];
    "Search CWD for\nmatching directory" [shape=box];
    "Directory found?" [shape=diamond];
    "Ask user for full path" [shape=box, style=bold];
    "Validate files" [shape=box];
    "Read README for stack name" [shape=box];
    "Check CFN stack status" [shape=diamond];
    "Extract template ID from outputs" [shape=box];
    "Display actionIds" [shape=box];
    "Pre-experiment health check" [shape=box, color=blue];
    "All resources healthy?" [shape=diamond];
    "Wait / prompt user" [shape=box];
    "Discover apps + start logs\n(app-service-log-analysis)" [shape=box];
    "User confirms experiment start" [shape=diamond, style=bold, color=red];
    "Start experiment" [shape=box];
    "Monitor experiment\n+ log insights" [shape=box];
    "Experiment complete?" [shape=diamond];
    "Wait 3 min post-baseline" [shape=box];
    "Stop logs + analyze\n(app-service-log-analysis)" [shape=box];
    "Generate results report" [shape=box];

    "User input:\npath or template ID?" -> "Validate files" [label="Full path"];
    "User input:\npath or template ID?" -> "Search CWD for\nmatching directory" [label="Template ID"];
    "Search CWD for\nmatching directory" -> "Directory found?";
    "Directory found?" -> "Validate files" [label="Yes (1 match)"];
    "Directory found?" -> "Ask user for full path" [label="No match"];
    "Ask user for full path" -> "Validate files" [label="User provides path"];
    "Validate files" -> "Read README for stack name";
    "Read README for stack name" -> "Check CFN stack status";
    "Check CFN stack status" -> "Extract template ID from outputs" [label="CREATE_COMPLETE"];
    "Check CFN stack status" -> "Generate results report" [label="Not deployed / failed, abort"];
    "Extract template ID from outputs" -> "Display actionIds";
    "Display actionIds" -> "Pre-experiment health check";
    "Pre-experiment health check" -> "All resources healthy?";
    "All resources healthy?" -> "Discover apps + start logs\n(app-service-log-analysis)" [label="Yes"];
    "All resources healthy?" -> "Wait / prompt user" [label="No"];
    "Wait / prompt user" -> "Pre-experiment health check" [label="Retry (poll 60s,\nmax 10 min non-interactive)"];
    "Wait / prompt user" -> "Discover apps + start logs\n(app-service-log-analysis)" [label="User override"];
    "Wait / prompt user" -> "Generate results report" [label="Abort"];
    "Discover apps + start logs\n(app-service-log-analysis)" -> "User confirms experiment start";
    "User confirms experiment start" -> "Start experiment" [label="Yes, I confirm"];
    "User confirms experiment start" -> "Stop logs + analyze\n(app-service-log-analysis)" [label="No, abort"];
    "Start experiment" -> "Monitor experiment\n+ log insights";
    "Monitor experiment\n+ log insights" -> "Experiment complete?";
    "Experiment complete?" -> "Monitor experiment\n+ log insights" [label="No, poll again"];
    "Experiment complete?" -> "Wait 3 min post-baseline" [label="Yes"];
    "Wait 3 min post-baseline" -> "Stop logs + analyze\n(app-service-log-analysis)";
    "Stop logs + analyze\n(app-service-log-analysis)" -> "Generate results report";
}
```

### Step 1: Resolve and Validate Experiment Directory

The user provides either:
- **(a)** the full path to the experiment directory, OR
- **(b)** an FIS experiment template ID (e.g., `EXT1a2b3c4d5e6f7`)

#### Step 1a: Resolve directory from template ID

If the user provides a template ID, search CWD for directories ending with that ID:

```bash
find . -maxdepth 1 -type d -name "*${TEMPLATE_ID_INPUT}" 2>/dev/null
```

- **1 match** → use it, inform user
- **Multiple matches** → list and ask user to choose
- **No match** → ask user for full path. Do NOT proceed without a valid path.

#### Step 1b: Extract template ID from directory name

The experiment directory name ends with the template ID (e.g.,
`2026-04-11-az-power-int-my-cluster-EXT1a2b3c4d5e6f7`). Extract it:

```bash
TEMPLATE_ID=$(basename "${EXPERIMENT_DIR}" | grep -oE 'EXT[a-zA-Z0-9]+$')
```

Store as `TEMPLATE_ID`. This is used in all subsequent steps.

#### Step 1c: Validate required files

Verify `EXPERIMENT_DIR` contains: `cfn-template.yaml`, `README.md`.

### Step 2: Read README and Extract Experiment Metadata

Read `README.md` from the experiment directory to extract:

1. **Scenario name** — from the H1 heading (e.g., `# FIS Experiment: AZ Power Interruption`)
2. **Target region** — from `**Region:** {REGION}`
3. **Target AZ** — from `**Target AZ:** {AZ_ID}` (if applicable)
4. **Estimated duration** — from `**Estimated Duration:** {DURATION}`
5. **Affected resources** — from the "Affected Resources" table
6. **CFN Stack Name** — from `**CFN Stack:** {STACK_NAME}` (for cleanup reference only)

Present a summary to the user with all extracted information.

### Step 3: Display Experiment Actions

Use `TEMPLATE_ID` (extracted from directory name in Step 1b) to query the experiment
template via AWS CLI and display all action IDs:

```bash
aws fis get-experiment-template \
  --id "{TEMPLATE_ID}" \
  --region {REGION} \
  --query 'experimentTemplate.actions' --output json
```

Extract all `actionId` values from the actions map and display them to the user:

```
Actions found:
  - {actionId_1}
  - {actionId_2}
  ...
```

Proceed directly to Step 3.5 (resource health check).

### Step 3.5: Pre-Experiment Resource Health Check

Before starting log collection or the experiment itself, verify that every target
resource referenced by the FIS experiment template is in a healthy baseline state.
Starting an experiment against already-degraded resources makes results unattributable
and may amplify impact on fragile infrastructure.

**Scope:** All resources listed in the FIS experiment template's `targets` map
(from the Step 3 query). This covers any managed service — RDS, Aurora, MSK,
ElastiCache (Redis/Memcached), EKS clusters and nodegroups, EC2, OpenSearch,
DocumentDB, etc. — whatever the template targets.

**Procedure:**

1. For each target in the experiment template, extract its `resourceType` (e.g.
   `aws:rds:db`, `aws:msk:cluster`, `aws:elasticache:replicationgroup`) and the
   actual resource identifiers (from `resourceArns` or resolved from `resourceTags`).
2. For each resource, call the appropriate AWS describe API for its service and
   read the canonical status field. Use your knowledge of AWS services to pick the
   right API and the right "healthy" value (e.g. RDS `available`, MSK `ACTIVE`,
   ElastiCache `available`, EKS `ACTIVE`, EC2 `running` with status check `ok`).
3. Present a table to the user:

   ```
   Resource             Type                              Status        Healthy?
   {id_1}               {resourceType_1}                  {status_1}    {✓ or ✗}
   {id_2}               {resourceType_2}                  {status_2}    {✓ or ✗}
   ...
   ```

4. If the resource type is unfamiliar or the API call fails, mark the resource as
   **unchecked** and treat it as unhealthy for decision purposes.

**Decision rules:**

- **All resources healthy** → proceed to Step 4.
- **One or more resources unhealthy / unchecked:**
  - **Interactive session** (you can prompt the user and get a response):
    warn the user, list the problem resources with their current states, and wait
    for explicit input. Accept: `proceed` (override and continue), `abort`
    (stop the workflow), or `retry` (re-run the health check now).
  - **Non-interactive session** (no user available to respond): automatically
    poll every **60 seconds** for up to **10 minutes**. Recheck every target
    resource each cycle. If all resources become healthy within the window,
    continue to Step 4 automatically. If the 10-minute window expires with any
    resource still unhealthy, **abort** and output a diagnostic summary listing
    each unhealthy resource, its current state, and the duration of the wait.

**How to determine interactive vs non-interactive:** Use your own judgment based
on the runtime context (e.g. whether a TTY is attached, whether you can invoke
interactive prompts, or environment signals suggesting a CI/automated run). When
uncertain, default to interactive behavior.

### Step 4: Discover EKS Applications and Start Log Collection

**REQUIRED:** You MUST use the `skill` tool to load the `app-service-log-analysis`
skill NOW, before proceeding. Call: `skill(name="app-service-log-analysis")`.
This injects the skill's instructions into your context so you can execute its
steps. If the skill is not installed or cannot be loaded, inform the user and
skip log collection (the experiment can still run without it).

This step runs **BEFORE** the experiment starts — discovering applications after the
experiment begins risks missing early log entries that get rotated or overwritten.

Execute from `app-service-log-analysis` skill:

1. **Its Step 2 (Read Service List)** — extracts affected AWS services from the
   experiment directory's `expected-behavior.md`
2. **Its Step 2.5 (Detect and Collect Managed Service Logs)** — checks managed service
   CloudWatch logging status, records log groups for later analysis
3. **Its "Multi-Cluster EKS Discovery and Kubeconfig Isolation" section** — discovers
   all EKS clusters in the target region, generates isolated kubeconfig per cluster
   (never overwrites `~/.kube/config`), verifies access to each cluster
4. **Its Step 3 (Collect Application Dependencies — Deep Scan)** — resolves service
   endpoints, deep-scans all accessible clusters in parallel, confirms discovered
   dependencies with user
5. **Its Step 4 (Log Collection — Real-time Mode)** — starts background `kubectl logs -f`
   for all confirmed applications across all clusters

### Step 5: Start Experiment (CRITICAL CONFIRMATION)

**This is the most dangerous step. The experiment WILL affect real resources.**

Before starting, present a clear warning:

```
WARNING: Starting this FIS experiment will cause REAL impact:

Scenario:    {SCENARIO_NAME}
Region:      {REGION}
Target AZ:   {AZ_ID}
Duration:    {DURATION}
Stack:       {STACK_NAME} (verified: CREATE_COMPLETE)
Template ID: {TEMPLATE_ID}

Resources that WILL be affected:
  - {list each affected resource type and count from README}

Stop Conditions:
  - {list each alarm that will stop the experiment}

Applications being monitored:
  - {list each namespace/deployment from SERVICE_APP_MAP}

Managed service log collection:
  - {list each service with logging status from MANAGED_LOG_GROUPS}

Log directory: {LOG_DIR}
Post-experiment baseline: 3 minutes (automatic)

Type "Yes, start experiment" to proceed, or "No" to abort.
```

**Only proceed if the user explicitly confirms.** If user aborts, proceed to Step 7
to stop log collection and clean up first.

Save the returned `experiment.id`.

### Step 6: Monitor Experiment

Poll the experiment status and display progress. See `references/cli-commands.md` for
polling commands and experiment status reference.

**Polling strategy:**
- Poll every 30 seconds for the first 5 minutes
- Poll every 60 seconds after that
- Show current status after each poll
- **Record timestamps** for each status change and action state transition — these
  feed into the per-service timeline in the final report
- **Track per-service events**: For each service affected by the experiment, note when
  it was impacted (action started), when it recovered, and any intermediate states.
  Query service-specific status (e.g., RDS instance status, ElastiCache replication
  group status, EKS node status) during monitoring to capture detailed observations.

**Log insights during each poll cycle:** Execute `app-service-log-analysis` Step 5
(Real-time Monitoring Display) — read recent logs, count errors/warnings, display
per-app summary, detect recovery signals. The skill must already be loaded from Step 4.

**During monitoring, remind the user:**
- Check the CloudWatch dashboard for real-time metrics
- The experiment can be stopped at any time (see `references/cli-commands.md` for stop command)

### Step 7: Post-Experiment Baseline, Stop Log Collection and Analyze

After the experiment completes (any terminal state):

#### Post-Experiment Baseline (3 minutes)

Continue collecting logs for **3 minutes** after the experiment ends to capture
recovery behavior. This applies to both application logs and managed service logs.
Display a countdown to the user:

```
Experiment completed. Collecting post-experiment baseline logs...
Remaining: {countdown} (3 minutes total)
```

After the 3-minute baseline window ends, proceed to analysis.

#### Generate Application Log Analysis

Execute `app-service-log-analysis` Steps 7-8:
- **Its Step 7 (Generate Analysis Report)** — analyze error patterns, peak rates, recovery
  times, and generate the "Application Log Analysis" section of the report. The analysis
  time window extends 3 minutes past the experiment end time to cover the baseline period.
- **Its Step 8 (Cleanup)** — kill background `kubectl logs` processes

The application log analysis output is embedded into the experiment results report
(see Step 10 below), NOT saved as a separate file.

### Step 10: Save Results Report to Local File

After the experiment completes (any terminal state), generate a results report and
**write it directly to a local markdown file** in the experiment directory.

See `references/report-template.md` for the complete report structure, file naming
convention, and timestamp format rules.

**Per-service analysis:** Identify all services affected by the experiment from the
README's "Affected Resources" table. For each service, create a sub-section with:
(1) timeline events, (2) observed behavior, (3) key findings. Include indirectly
affected services.

After saving, print a brief terminal summary:
- File path, experiment ID, final status
- Start/end time and duration (ISO 8601 with timezone)
- Per-action status (one line each)
- Per-service recovery status (one line each)
- Application log summary — total errors per app
- Issues requiring attention (if any)
- Cleanup instructions

## Safety Rules

1. **Never auto-start experiments.** Always require explicit user confirmation.
2. **Show every CLI command** before executing it.
3. **Display impact warning** before experiment start with specific resource list.
4. **Provide abort instructions** at every step.
5. **Never delete resources** without user confirmation.
6. **Never deploy infrastructure.** This skill only checks existing deployments.
7. **Recommend dry-run first** — suggest the user review all files before starting.
8. **Never start an experiment against unhealthy resources.** Step 3.5 verifies every
   target resource is in its service's healthy baseline state. In interactive mode,
   any unhealthy or unchecked resource requires explicit user override. In
   non-interactive mode, poll every 60 seconds for up to 10 minutes; abort if still
   unhealthy when the window expires.

## Cleanup Guide

After the experiment, offer cleanup. See `references/cli-commands.md` for commands.

## Error Handling

| Error | Cause | Resolution |
|---|---|---|
| Stack name not found in README | README missing `**CFN Stack:**` field | Check if the experiment was prepared with a recent version of aws-fis-experiment-prepare |
| Stack not found (`ValidationError`) | Stack does not exist or was deleted | Deploy the stack first using aws-fis-experiment-prepare |
| Stack in `CREATE_FAILED` / `ROLLBACK_COMPLETE` | Stack deployment failed | Check stack events for failure reason, fix and redeploy |
| `ExperimentTemplateId` not in outputs | Stack template missing output | Check cfn-template.yaml for the output definition |
| `AccessDeniedException` | Insufficient permissions | Check IAM permissions for FIS, CloudWatch, CloudFormation |
| `ResourceNotFoundException` on targets | Tagged resources not found | Verify resource tags match experiment template |
| Experiment stuck in `initiating` | IAM role propagation delay | Wait 30 seconds and check again |
| `kubectl: command not found` | kubectl not installed | Install kubectl and configure kubeconfig |
| `error: You must be logged in` | kubeconfig not configured | Run `aws eks update-kubeconfig --name {cluster}` |
| `/.pids: Permission denied` | `LOG_DIR` variable empty due to `&&` chain | Use multi-line script with `export LOG_DIR=...`, NOT `&&` chains |
| No EKS apps discovered | No pods reference affected service endpoints | Ask user to manually specify namespace/deployment pairs |
