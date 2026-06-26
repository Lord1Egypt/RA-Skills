# Risk Matrix

## Green
- Normal task flow
- Trusted local state
- No unusual process, session, or config behavior

## Yellow
- Unexpected but not clearly malicious behavior
- Untrusted content that may be steering the agent
- Session instability, restart windows, or partial failures
- Host anomalies that need verification

## Red
- Credential exposure risk
- Prompt injection or hostile instruction source
- Unexpected privileged process or listener
- Evidence of compromise or unsafe state
- Any action that would mutate the system without explicit authorization

## Default responses
- Green: proceed
- Yellow: verify first
- Red: stop side effects, preserve evidence, contain