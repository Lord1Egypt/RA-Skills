# Specification Template

Normalize user requirements into the following structure before generating RTL.

```yaml
design_name:
top_module:
description:
inputs:
  - name:
    width:
    desc:
outputs:
  - name:
    width:
    desc:
clock:
  name:
  edge: posedge
reset:
  name:
  active_level:
  sync_or_async:
functional_requirements:
  -
timing_target:
target_flow: openlane
verification_targets:
  - reset behavior
  - normal operation
  - corner cases
assumptions:
  - single clock domain
  - no CDC
```

## Minimum Required Fields

Before running synthesis or backend steps, ensure the following fields exist:

- `design_name`
- `top_module`
- Interface list (inputs and outputs)
- Clock definition
- Reset definition, or an explicit note if no reset exists
- Target flow (`fpga` or `asic/openlane`)

## Ask Before Guessing

If any of the following are missing, ask the user or document assumptions clearly:

- Bus widths
- Valid/ready handshake semantics
- Reset polarity
- Timing targets
- Pipeline depth
- Whether area or frequency is the primary optimization target
