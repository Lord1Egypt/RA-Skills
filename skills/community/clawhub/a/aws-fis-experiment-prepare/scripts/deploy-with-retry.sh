#!/usr/bin/env bash
# deploy-with-retry.sh
#
# Single attempt: validate + deploy + on-failure delete. The agent drives
# the retry loop (SKILL.md Step 6) — this script handles one iteration:
# validate template syntax, deploy, and on failure extract errors and
# delete the failed stack so the caller can fix the template and re-invoke.
#
# Usage:
#   ./deploy-with-retry.sh <template-file> <stack-name> <region> [cfn-role-arn] [parameter-overrides...]
#
# Example:
#   ./deploy-with-retry.sh ./cfn-template.yaml fis-pod-delete-payment-a3x7k2 us-east-1 \
#     "" \
#     ExperimentName=pod-delete-payment-a3x7k2 RandomSuffix=a3x7k2
#
# Exit codes:
#   0  — deployment succeeded
#   1  — validation failed (fix template syntax and retry)
#   2  — deployment failed, stack deleted (caller should fix and re-invoke)

set -euo pipefail

TEMPLATE_FILE="${1:?Usage: $0 <template-file> <stack-name> <region> [cfn-role-arn] [param-overrides...]}"
STACK_NAME="${2:?stack-name required}"
REGION="${3:?region required}"
CFN_ROLE_ARN="${4:-}"
shift 4 || true
PARAM_OVERRIDES=("$@")

ROLE_FLAG=()
if [ -n "${CFN_ROLE_ARN}" ]; then
    ROLE_FLAG=(--role-arn "${CFN_ROLE_ARN}")
fi

# Step 1: Validate template syntax
echo "Validating template: ${TEMPLATE_FILE}" >&2
if ! aws cloudformation validate-template \
        --template-body "file://${TEMPLATE_FILE}" \
        --region "${REGION}" >/dev/null 2>&1; then
    VALIDATE_ERR=$(aws cloudformation validate-template \
        --template-body "file://${TEMPLATE_FILE}" \
        --region "${REGION}" 2>&1 || true)
    echo "ERROR: Template validation failed:" >&2
    echo "${VALIDATE_ERR}" >&2
    exit 1
fi

# Step 2: Deploy
echo "Deploying stack: ${STACK_NAME}" >&2

DEPLOY_CMD=(aws cloudformation deploy
    --template-file "${TEMPLATE_FILE}"
    --stack-name "${STACK_NAME}"
    --capabilities CAPABILITY_NAMED_IAM
    --region "${REGION}"
    --no-fail-on-empty-changeset)

if [ ${#PARAM_OVERRIDES[@]} -gt 0 ]; then
    DEPLOY_CMD+=(--parameter-overrides "${PARAM_OVERRIDES[@]}")
fi

if [ ${#ROLE_FLAG[@]} -gt 0 ]; then
    DEPLOY_CMD+=("${ROLE_FLAG[@]}")
fi

if "${DEPLOY_CMD[@]}"; then
    echo "Deployment succeeded: ${STACK_NAME}" >&2
    exit 0
fi

# Step 3: Deployment failed — extract reason and delete stack
echo "" >&2
echo "ERROR: Deployment failed. Extracting failure reason from stack events..." >&2

FAILED_EVENTS=$(aws cloudformation describe-stack-events \
    --stack-name "${STACK_NAME}" \
    --region "${REGION}" \
    --query 'StackEvents[?contains(ResourceStatus, `FAILED`)].{Resource:LogicalResourceId, Reason:ResourceStatusReason}' \
    --output json 2>/dev/null || echo "[]")

echo "Failed resources:" >&2
echo "${FAILED_EVENTS}" | jq -r '.[] | "  - \(.Resource): \(.Reason)"' >&2

echo "" >&2
echo "Deleting failed stack..." >&2

DELETE_CMD=(aws cloudformation delete-stack
    --stack-name "${STACK_NAME}"
    --region "${REGION}")

if [ ${#ROLE_FLAG[@]} -gt 0 ]; then
    DELETE_CMD+=("${ROLE_FLAG[@]}")
fi

"${DELETE_CMD[@]}" || true

aws cloudformation wait stack-delete-complete \
    --stack-name "${STACK_NAME}" \
    --region "${REGION}" 2>/dev/null || true

echo "Stack deleted. Fix cfn-template.yaml and re-run." >&2
exit 2
