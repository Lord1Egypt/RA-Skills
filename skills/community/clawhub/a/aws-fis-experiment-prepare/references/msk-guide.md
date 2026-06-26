# Amazon MSK — FIS Experiment Guide

## Contents

- Scope
- Architecture Overview
- MSK Broker Reboot — Full Example
  - SSM Automation Runbook
  - IAM Permissions
  - Discovery: List Broker IDs
- CFN Template Integration (SSM Document, IAM Roles, FIS Action)
- IAM Design — Two-Role Pattern
- Scenario Slug
- Key Constraints
- Common Mistakes

## Scope

MSK has **no native FIS action**. Fault injection relies on an SSM Automation
runbook that calls the MSK API directly.

**Supported fault:** Broker reboot via `kafka:RebootBroker` — validates Kafka
consumer and producer resilience when a broker restarts.

**Use this guide when:**
- The user wants to inject a fault into MSK (broker reboot / restart)
- The user mentions "Kafka broker failure" or similar intent

**Do NOT use this guide when:**
- The fault is network-level (e.g., pod-to-MSK latency or packet loss) — use
  `aws:network:disrupt-connectivity` or `aws:eks:pod-network-*` instead
- The fault is AZ-level (MSK impact during AZ power interruption) — use
  `references/az-power-interruption-guide.md`

## Architecture Overview

```
FIS Experiment Template
  └── Action: aws:ssm:start-automation-execution
        ├── documentArn: arn:aws:ssm:{REGION}:{ACCOUNT_ID}:document/{DOC_NAME}
        ├── documentParameters: {"ClusterArn": "...", "BrokerId": "1"}
        └── maxDuration: PT15M
              │
              v
SSM Automation Runbook (schema 0.3)
  ├── Step 1: RebootMskBroker       (aws:executeAwsApi -> kafka:RebootBroker)
  └── Step 2: WaitForClusterActive  (aws:waitForAwsResourceProperty -> kafka:DescribeCluster)
```

## MSK Broker Reboot — Full Example

### SSM Automation Runbook

Schema version **0.3** is required for all Automation documents.

```yaml
description: 'FIS: Reboot MSK broker to test Kafka client resilience'
schemaVersion: '0.3'
assumeRole: '{{ AutomationAssumeRoleArn }}'
parameters:
  AutomationAssumeRoleArn:
    type: String
    description: IAM Role ARN for SSM Automation to assume
  ClusterArn:
    type: String
    description: MSK cluster ARN
  BrokerId:
    type: String
    description: 'Broker ID to reboot (e.g., 1, 2, 3)'
mainSteps:
  - name: RebootMskBroker
    action: aws:executeAwsApi
    inputs:
      Service: kafka
      Api: RebootBroker
      ClusterArn: '{{ ClusterArn }}'
      BrokerIds:
        - '{{ BrokerId }}'
    outputs:
      - Name: ClusterArn
        Selector: $.ClusterArn
        Type: String
      - Name: ClusterOperationArn
        Selector: $.ClusterOperationArn
        Type: String

  - name: WaitForClusterActive
    action: aws:waitForAwsResourceProperty
    timeoutSeconds: 600
    inputs:
      Service: kafka
      Api: DescribeCluster
      ClusterArn: '{{ ClusterArn }}'
      PropertySelector: $.ClusterInfo.State
      DesiredValues:
        - ACTIVE
```

### IAM Permissions

The **SSM Automation Role** (trusted by `ssm.amazonaws.com`) requires the
following MSK API permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "kafka:RebootBroker",
    "kafka:DescribeCluster"
  ],
  "Resource": "{MSK_CLUSTER_ARN}"
}
```

### Discovery: List Broker IDs

Run this command to retrieve valid broker IDs for the target cluster:

```bash
aws kafka list-nodes --cluster-arn {CLUSTER_ARN} \
  --query 'NodeInfoList[].BrokerNodeInfo.BrokerId' --output json
```

Ask the user which broker(s) to reboot. If unspecified, default to the first
broker for a minimal-impact test.

## CFN Template Integration

### SSM Document Resource

Deploy the SSM Automation runbook as an `AWS::SSM::Document` resource in the
same CloudFormation template as the FIS experiment template.

```yaml
Resources:
  SSMAutomationDocument:
    Type: AWS::SSM::Document
    Properties:
      DocumentType: Automation
      DocumentFormat: YAML
      Name: !Sub 'fis-${ExperimentName}-runbook'
      Content:
        description: 'FIS: Reboot MSK broker to test Kafka client resilience'
        schemaVersion: '0.3'
        assumeRole: '{{ AutomationAssumeRoleArn }}'
        parameters:
          AutomationAssumeRoleArn:
            type: String
            description: IAM Role ARN
          ClusterArn:
            type: String
            description: MSK cluster ARN
          BrokerId:
            type: String
            description: 'Broker ID to reboot'
        mainSteps:
          # ... (paste full mainSteps from the runbook example above)

  SSMAutomationRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub 'fis-ssm-auto-role-${RandomSuffix}'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ssm.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: MskApiAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Sid: MskBrokerAccess
                Effect: Allow
                Action:
                  - kafka:RebootBroker
                  - kafka:DescribeCluster
                Resource: !Ref ClusterArn
```

### FIS Experiment Template Action

```yaml
FISExperimentTemplate:
  Type: AWS::FIS::ExperimentTemplate
  DependsOn:
    - FISExperimentRole
    - SSMAutomationDocument
  Properties:
    Description: !Sub 'FIS: ${ExperimentName}'
    RoleArn: !GetAtt FISExperimentRole.Arn
    StopConditions:
      - Source: 'none'
    Tags:
      Name: !Ref ExperimentName
    Targets: {}  # No targets — SSM Automation handles targeting
    Actions:
      ExecuteSSMAutomation:
        ActionId: aws:ssm:start-automation-execution
        # CFN ExperimentTemplate.Actions.Parameters is Map<String, String>,
        # not the list-of-strings format used by the FIS API.
        Parameters:
          documentArn: !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:document/fis-${ExperimentName}-runbook'
          documentParameters: !Sub >-
            {"AutomationAssumeRoleArn":"${SSMAutomationRole.Arn}",
             "ClusterArn":"${ClusterArn}",
             "BrokerId":"${BrokerId}"}
          maxDuration: 'PT15M'
```

### FIS Experiment Role

The FIS Experiment Role needs the `AWSFaultInjectionSimulatorSSMAccess` managed
policy **plus** `iam:PassRole` to hand off the SSM Automation Role:

```yaml
FISExperimentRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: !Sub 'fis-role-${RandomSuffix}'
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: fis.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorSSMAccess
    Policies:
      - PolicyName: PassSSMAutomationRole
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Sid: PassRoleToSSM
              Effect: Allow
              Action: iam:PassRole
              Resource: !GetAtt SSMAutomationRole.Arn
              Condition:
                StringEquals:
                  iam:PassedToService: ssm.amazonaws.com
```

## IAM Design — Two-Role Pattern

MSK broker reboot via SSM Automation requires **two separate IAM roles**:

| Role | Trusted By | Purpose | Permissions |
|---|---|---|---|
| FIS Experiment Role | `fis.amazonaws.com` | FIS starts the SSM Automation execution | `AWSFaultInjectionSimulatorSSMAccess` + `iam:PassRole` for SSM Automation Role |
| SSM Automation Role | `ssm.amazonaws.com` | SSM Automation calls `kafka:RebootBroker` | `kafka:RebootBroker`, `kafka:DescribeCluster` |

**Why two roles?** FIS uses its own role to call `ssm:StartAutomationExecution`.
The SSM Automation runbook then needs a separate role (trusted by
`ssm.amazonaws.com`) to call `kafka:RebootBroker`. The FIS role trusts
`fis.amazonaws.com` and cannot be reused by SSM Automation.

## Scenario Slug

| Scenario | SCENARIO_SLUG | Example Stack Name |
|---|---|---|
| MSK broker reboot | `ssm-auto-msk-reboot` | `fis-ssm-auto-msk-reboot-my-cluster-a3x7k2` |

See `references/slug-conventions.md` for the general SSM Automation slug
pattern: `ssm-auto-<service>-<operation>`.

## Key Constraints

| Constraint | Detail |
|---|---|
| `aws:executeAwsApi` max duration | 25 seconds per step execution. `RebootBroker` returns quickly, so this is not a concern. |
| SSM document naming | Max 128 characters. Follow the `fis-{ExperimentName}-runbook` convention. |
| `documentParameters` in FIS | Must be a **JSON string**, not a JSON object. FIS passes this as a single string to `StartAutomationExecution`. |
| SSM Automation concurrency | Default limit: 25 concurrent executions per account per region. Request a quota increase for high-frequency experiments. |
| Rollback | `kafka:RebootBroker` is self-recovering — the broker comes back online automatically. No explicit rollback step is needed. |
| MSK cluster state during reboot | The cluster transitions to `REBOOTING_BROKER` then back to `ACTIVE`. The `WaitForClusterActive` step handles this transition. |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using FIS Experiment Role as SSM Automation `assumeRole` | The FIS role trusts `fis.amazonaws.com`, not `ssm.amazonaws.com`. Create a dedicated SSM Automation Role. |
| Passing `documentParameters` as a JSON object instead of a string | In CFN, use `!Sub` to produce a stringified JSON value. In CLI, wrap the JSON in single quotes. |
| Forgetting `iam:PassRole` on the FIS Experiment Role | FIS must pass the SSM Automation Role to SSM. Add `iam:PassRole` with the condition `iam:PassedToService: ssm.amazonaws.com`. |
| Omitting the recovery wait step | Without `aws:waitForAwsResourceProperty`, the experiment ends immediately after the API call — before the broker has restarted. Always include the `WaitForClusterActive` step. |
| Hardcoding region or account in the document ARN | Use `!Sub` with `${AWS::Region}` and `${AWS::AccountId}` in CFN templates. |
| Wrong broker ID | Run `aws kafka list-nodes` to retrieve valid broker IDs before generating the template. Do not assume IDs start at 1 — they correspond to each node's physical position. |
