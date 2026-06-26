---
name: blue-green-deployer
version: 2.0.0
description: A specialized skill for safely managing and testing OpenClaw configuration changes using a Blue/Green deployment pattern. Use when you need to test new settings, tools, or channel configurations without risking the stability of the main (Blue) session.
dependencies:
  - openclaw
  - jq
---

# Blue/Green Deployer

This skill provides a structured pre-production testing workflow for OpenClaw configuration changes using a Blue/Green deployment pattern.

## Workflow

### 1. Setup the Green Environment
Initialize the testing area by creating the Green configuration from your current Blue master.
- Command: `bash <skill-path>/scripts/deploy.sh`

### 2. Experiment
Modify the files within the `green` configuration folder or the `openclaw.json.green` file directly using your preferred editor.

### 3. Audit and Validate
Verify that the changes in the Green environment are valid and do not break the OpenClaw service.
- **Step A**: Check JSON syntax: `jq empty openclaw.json.green`
- **Step B**: Run the deployment script to perform the symlink-based validation check.

### 4. Promote or Rollback
- **To Promote**: If the audit passes, the `deploy.sh` script will automatically promote the Green configuration to Blue.
- **To Rollback**: If the audit fails, the `deploy.sh` (or manual action) will revert the Blue configuration to its previous state using the `.bak` file.

## Troubleshooting

- **Validation Error**: If the script reports a failure, check the `openclaw.json.green` file for syntax errors (missing commas, brackets) or invalid keys.
- **Manual Check**: Always use `openclaw status` after any deployment to ensure the live service is operational.
