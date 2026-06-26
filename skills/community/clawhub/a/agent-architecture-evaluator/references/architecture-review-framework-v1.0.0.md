# Architecture Review Framework v1.0.0

Use this file when assessing an agent architecture or multi-agent system.

## Inventory fields

Capture:

- component name
- responsibility
- inputs
- outputs
- internal state or memory
- downstream dependencies
- failure signals

## Architecture questions

- Are responsibilities clearly separated?
- Does routing send work to the correct place?
- Is memory helpful or contaminating?
- Where is human review required?
- Which failure can cascade across the system?
- Which metrics are missing today?

## Test scenario categories

- normal path
- ambiguous request path
- missing context path
- tool outage path
- stale memory path
- slow component path
- recovery path

## Expected outputs

- architecture inventory
- failure map
- test plan
- optimization roadmap
- measurement plan
