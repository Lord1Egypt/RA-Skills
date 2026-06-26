# AWS Alert Formats

Format reference for the three structured AWS alert shapes this skill
parses, plus guidance on disambiguation and out-of-scope formats.

## Table of contents

- [Security Hub ASFF](#security-hub-asff)
- [Inspector v2](#inspector-v2)
- [CloudWatch Alarm (EventBridge envelope)](#cloudwatch-alarm-eventbridge-envelope)
- [CloudWatch Alarm (SNS direct)](#cloudwatch-alarm-sns-direct)
- [SNS envelope](#sns-envelope)
- [Out-of-scope formats](#out-of-scope-formats)
- [Disambiguation tips](#disambiguation-tips)

---

## Security Hub ASFF

AWS Security Finding Format. One schema across Security Hub's upstream
sources (Inspector, GuardDuty, Macie, IAM Access Analyzer, Config) and
3rd-party integrations.

Distinguishing fields:
- `"SchemaVersion": "2018-10-08"`
- `"ProductArn"` starts with `arn:aws:securityhub:`
- Single finding or `{"Findings": [...]}` envelope

Key fields:
```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "arn:aws:...",
  "ProductArn": "arn:aws:securityhub:us-west-2::product/aws/guardduty",
  "AwsAccountId": "123456789012",
  "Severity": { "Label": "HIGH", "Normalized": 70 },
  "Title": "...",
  "Description": "...",
  "Resources": [{"Id": "arn:aws:...", "Type": "..."}],
  "Region": "us-west-2",
  "CreatedAt": "2026-04-22T21:04:00.000Z"
}
```

Source-subtype derivation (from `ProductArn`):

| ProductArn contains | source_subtype |
|---|---|
| `product/aws/inspector` | `inspector` |
| `product/aws/guardduty` | `guardduty` |
| `product/aws/macie` | `macie` |
| `product/aws/access-analyzer` | `access-analyzer` |
| `product/aws/config` | `config` |
| `product/aws/firewall-manager` | `firewall-manager` |
| `product/aws/health` | `health` |
| `product/aws/ssm-patch-manager` | `ssm-patch` |
| Anything else | `other` (full `ProductArn` preserved in `raw`) |

Multi-finding caveat: when the envelope contains >1 finding, the parser
emits only the first. EventBridge rules default to one-per-delivery; if
you expect batches, split them upstream.

---

## Inspector v2

Amazon Inspector v2 native finding format. Can arrive as:
- Raw API format (single finding object with `findingArn`, `severity`, `type`)
- EventBridge envelope (`detail-type: "Inspector2 Finding"`, `detail` = finding)
- API list-response shape (`{"findings": [...]}`) — parser emits the first

When to use this vs ASFF: if you subscribe to Security Hub, Inspector
findings arrive as ASFF (use `parse-asff.sh`). If you subscribe directly
to Inspector via EventBridge, they arrive as Inspector v2 format (use
this parser). Most orgs running Inspector without Security Hub route
findings this way.

Key fields (in `detail` when EventBridge-wrapped):
```json
{
  "findingArn": "arn:aws:inspector2:...",
  "awsAccountId": "123456789012",
  "type": "PACKAGE_VULNERABILITY | NETWORK_REACHABILITY | CODE_VULNERABILITY",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL | UNTRIAGED",
  "status": "ACTIVE | SUPPRESSED | CLOSED",
  "title": "CVE-2026-xxxxx - openssl",
  "description": "...",
  "resources": [{
    "type": "AWS_ECR_CONTAINER_IMAGE | AWS_EC2_INSTANCE | AWS_LAMBDA_FUNCTION",
    "id": "arn:aws:...",
    "region": "us-west-2",
    "details": { ... }
  }],
  "inspectorScore": 7.5,
  "firstObservedAt": "...",
  "packageVulnerabilityDetails": { "vulnerabilityId": "CVE-...", ... }
}
```

EventBridge envelope (when routed via EventBridge):
```json
{
  "source": "aws.inspector2",
  "detail-type": "Inspector2 Finding",
  "account": "123456789012",
  "region": "us-west-2",
  "detail": { /* the finding */ }
}
```

Source-subtype derivation (from `.type`, lowercased and hyphenated):

| Inspector type | source_subtype |
|---|---|
| `PACKAGE_VULNERABILITY` | `package-vulnerability` |
| `NETWORK_REACHABILITY` | `network-reachability` |
| `CODE_VULNERABILITY` | `code-vulnerability` |
| anything else | `<type>` lowercased with `_` → `-` |

Severity `UNTRIAGED` is mapped to `INFORMATIONAL` — Inspector's initial
state for some finding types isn't a real severity signal until scoring
completes.

The parser extracts `inspectorScore` (CVSS 0.0-10.0) as a separate
`inspector_score` field in the normalized output when present. Useful
for threshold-based downstream routing.

Multi-finding caveat: the API list-response (`{"findings": [...]}`)
and any batched delivery paths emit only the first finding. The parser
logs a stderr warning when it detects >1 finding. EventBridge delivers
one finding per event by default, so this only matters for batch
imports via the API path.

Note: Inspector2 "Scan" and "Coverage" events (`detail-type: Inspector2
Scan` / `Inspector2 Coverage`) are NOT parsed by this skill. They
indicate scan lifecycle events, not incidents. If you need those, write
a separate handler.

---

## CloudWatch Alarm (EventBridge envelope)

Alarm state changes routed via EventBridge. Common for modern setups.

Distinguishing fields:
- `"source": "aws.cloudwatch"`
- `"detail-type": "CloudWatch Alarm State Change"`
- Alarm state in `detail`

```json
{
  "source": "aws.cloudwatch",
  "detail-type": "CloudWatch Alarm State Change",
  "account": "123456789012",
  "region": "us-west-2",
  "time": "2026-04-22T21:04:00Z",
  "resources": ["arn:aws:cloudwatch:us-west-2:123456789012:alarm:my-alarm"],
  "detail": {
    "alarmName": "my-alarm",
    "state": { "value": "ALARM", "reason": "Threshold Crossed: ..." },
    "previousState": { "value": "OK" }
  }
}
```

EventBridge does not include the alarm's `AlarmDescription`. If context
text matters for triage (e.g. cert-expiry alarms where the description
explains what the threshold means), enrich upstream or switch to the
SNS-direct shape.

---

## CloudWatch Alarm (SNS direct)

Alarms posted directly to SNS without an EventBridge rule. Older or
simpler setups.

Distinguishing fields:
- Top-level `"AlarmName"` and `"NewStateValue"`
- No `source` / `detail-type`
- Usually wrapped in an SNS Notification envelope

```json
{
  "AlarmName": "my-alarm",
  "AlarmDescription": "...",
  "AWSAccountId": "123456789012",
  "NewStateValue": "ALARM",
  "NewStateReason": "Threshold Crossed: ...",
  "OldStateValue": "OK",
  "Region": "US West (Oregon)",
  "StateChangeTime": "2026-04-22T21:04:00.000+0000"
}
```

`Region` here is the human-readable name, not the region code. The parser
normalizes it (full map in `scripts/parse-cloudwatch-alarm.sh`).

This shape includes `AlarmDescription` — useful when the alarm name is
terse and the description carries intent (e.g. "Certificate expires in
90 days; renewal in 30").

---

## SNS envelope

SNS HTTPS subscriptions deliver payloads wrapped:

```json
{
  "Type": "Notification",
  "MessageId": "...",
  "TopicArn": "arn:aws:sns:...",
  "Subject": "...",
  "Message": "<the alert JSON, escaped as a string>",
  "Timestamp": "...",
  "Signature": "...",
  "SigningCertURL": "..."
}
```

`parse-alert.sh` unwraps automatically — pipe in the outer envelope and
it extracts `.Message`, re-parses as JSON, and dispatches to the right
format-specific parser. No manual unwrap needed.

### SubscriptionConfirmation

The first payload from a new SNS subscription is:

```json
{
  "Type": "SubscriptionConfirmation",
  "Token": "...",
  "SubscribeURL": "https://sns.../..."
}
```

Not an alert — it's the one-time handshake. `parse-alert.sh` detects this
and exits 4 with a hint. To confirm, GET the `SubscribeURL` or run
`aws sns confirm-subscription`.

---

## Out-of-scope formats

The skill does NOT parse:

| Format | Why | What to do |
|---|---|---|
| Custom-formatted Slack messages (Lambda formatters) | No standard schema; varies per-org | Write a per-org companion skill, or subscribe upstream to the raw SNS topic |
| AWS Chatbot-rendered Slack output | Rendering is proprietary and changes silently | Same — subscribe upstream for raw JSON |
| AWS Cost Anomaly findings | Different shape (anomaly-level + N root-cause subsections) | Use [`anomaly-explainer`](https://clawhub.ai/anmolnagpal/anomaly-explainer) |
| AWS Health events | Account-level, different schema | Separate handler; potentially a future v0.2 addition |
| AWS Inspector v2 "Scan" events (`Inspector2 Scan`) | Lifecycle event, not an incident | Separate handler or ignore |
| AWS Inspector v2 "Coverage" events (`Inspector2 Coverage`) | Resource scan-coverage changes, not incidents | Separate handler or ignore |
| Billing / budget alerts | Different shape | Use a cost-focused skill |

---

## Disambiguation tips

If `parse-alert.sh` auto-detect can't place a payload:

1. *Is it wrapped?* SNS envelopes (`Type: Notification`) and EventBridge
   envelopes (top-level `source` + `detail-type`) are unwrapped
   automatically by `parse-alert.sh`. If you're calling a format-specific
   parser directly, unwrap first.

2. *Is it an SNS subscription handshake?* Look for
   `Type: SubscriptionConfirmation`. That's the one-time confirmation,
   not an alert.

3. *Is it a batched ASFF?* `{"Findings": [...]}` with >1 finding — the
   parser emits the first. Split batches upstream for full coverage.

4. *Is it Inspector v2?* Look for `findingArn`, `severity`, and `type`
   fields. If wrapped in EventBridge, `detail-type` is `Inspector2
   Finding`.

5. *Neither ASFF, Inspector v2, nor CloudWatch?* If it references AWS
   resources but doesn't match any known format, it's likely one of the
   out-of-scope shapes above. Pass the raw text to `incident-triage`
   with `source=aws-unknown` and let triage work from the unstructured
   description.
