#!/usr/bin/env bash
# precheck-cfn-permissions.sh
#
# Detects whether the current IAM identity requires a CFN service role.
# If a `cloudformation:RoleArn` condition is found in the caller's inline
# policies, extracts the role ARN and prints it. Otherwise runs IAM policy
# simulation to verify CloudFormation permissions exist.
#
# Usage:
#   ./precheck-cfn-permissions.sh
#
# Output (on stdout):
#   - If a service role is required: the role ARN (one line)
#   - If no service role is required: empty output, exit 0
#   - If the caller lacks CFN permissions: exit 1 with guidance on stderr
#
# The caller can capture the ARN into CFN_ROLE_ARN:
#   CFN_ROLE_ARN=$(./precheck-cfn-permissions.sh)

set -euo pipefail

CALLER_ARN=$(aws sts get-caller-identity --query 'Arn' --output text)
ROLE_NAME=$(echo "${CALLER_ARN}" | grep -oE 'role/[^/]+' | sed 's|role/||' || true)

if [ -z "${ROLE_NAME}" ]; then
    # Not a role (could be user), skip condition check, go straight to simulation
    ROLE_NAME=""
fi

CFN_ROLE_ARN=""

# 1. Check inline policies for cloudformation:RoleArn condition
if [ -n "${ROLE_NAME}" ]; then
    POLICY_NAMES=$(aws iam list-role-policies --role-name "${ROLE_NAME}" \
        --query 'PolicyNames[]' --output text 2>/dev/null || true)

    for POLICY_NAME in ${POLICY_NAMES}; do
        POLICY_DOC=$(aws iam get-role-policy --role-name "${ROLE_NAME}" \
            --policy-name "${POLICY_NAME}" --query 'PolicyDocument' --output json 2>/dev/null || true)

        # Extract any cloudformation:RoleArn value from the policy document
        EXTRACTED_ARN=$(echo "${POLICY_DOC}" | jq -r '
            (.Statement | if type=="array" then . else [.] end)
            | map(select(
                (.Action | if type=="array" then . else [.] end)
                | any(test("cloudformation:(Create|Update|Delete)Stack"))
            ))
            | map(.Condition.StringEquals["cloudformation:RoleArn"] // empty)
            | map(if type=="array" then .[0] else . end)
            | .[0] // empty
        ' 2>/dev/null || true)

        if [ -n "${EXTRACTED_ARN}" ] && [ "${EXTRACTED_ARN}" != "null" ]; then
            CFN_ROLE_ARN="${EXTRACTED_ARN}"
            break
        fi
    done
fi

# 2. If a service role ARN was found, return it
if [ -n "${CFN_ROLE_ARN}" ]; then
    echo "${CFN_ROLE_ARN}"
    exit 0
fi

# 3. No condition found — simulate CloudFormation permissions
SIM_RESULTS=$(aws iam simulate-principal-policy \
    --policy-source-arn "${CALLER_ARN}" \
    --action-names cloudformation:CreateStack cloudformation:UpdateStack cloudformation:DeleteStack \
    --query 'EvaluationResults[].EvalDecision' \
    --output text 2>/dev/null || echo "FAIL")

if echo "${SIM_RESULTS}" | grep -qv "allowed"; then
    echo "ERROR: Caller ${CALLER_ARN} lacks CloudFormation permissions." >&2
    echo "" >&2
    echo "Either:" >&2
    echo "  1. Use a CFN service role (see setup guide:" >&2
    echo "     https://panlm.github.io/others/cfn-service-role-for-fis-experiment-setup-guide/)" >&2
    echo "  2. Grant broader IAM permissions for CloudFormation" >&2
    exit 1
fi

# All CloudFormation actions are allowed — no service role needed
exit 0
