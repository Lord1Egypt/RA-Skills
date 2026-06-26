#!/usr/bin/env bash
# rename-output-dir.sh
#
# Extracts the FIS experiment template ID from CFN stack outputs, then
# renames the output directory to append the template ID.
#
# Usage:
#   ./rename-output-dir.sh <output-dir> <stack-name> <region>
#
# Example:
#   ./rename-output-dir.sh \
#     ./2026-04-11-10-30-00-pod-delete-payment \
#     fis-pod-delete-payment-a3x7k2 \
#     us-east-1
#
# Output (stdout):
#   The new (renamed) directory path
#
# Exit codes:
#   0  — renamed successfully; new path printed to stdout
#   1  — template ID not found in stack outputs

set -euo pipefail

OUTPUT_DIR="${1:?Usage: $0 <output-dir> <stack-name> <region>}"
STACK_NAME="${2:?stack-name required}"
REGION="${3:?region required}"

TEMPLATE_ID=$(aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query 'Stacks[0].Outputs[?OutputKey==`ExperimentTemplateId`].OutputValue' \
    --output text --region "${REGION}")

if [ -z "${TEMPLATE_ID}" ] || [ "${TEMPLATE_ID}" = "None" ]; then
    echo "ERROR: ExperimentTemplateId not found in outputs of stack ${STACK_NAME}" >&2
    exit 1
fi

NEW_OUTPUT_DIR="${OUTPUT_DIR}-${TEMPLATE_ID}"

mv "${OUTPUT_DIR}" "${NEW_OUTPUT_DIR}"

echo "${NEW_OUTPUT_DIR}"
