# Failure Patterns

## Specification Gaps

**Symptoms:**
- Unclear module boundaries
- No clock/reset definition
- Contradictory IO behavior

**Action:**
- Stop and ask the user, or record explicit assumptions before continuing

## RTL Issues

**Symptoms:**
- Syntax errors
- Undeclared signals
- Width mismatch warnings
- Unintended latch inference

**Action:**
- Fix RTL first
- Avoid changing the testbench unless failure points to a testbench mismatch

## Testbench Issues

**Symptoms:**
- Compilation succeeds but runtime checks fail unexpectedly
- No waveform dump generated
- Reset/clock generation missing

**Action:**
- Inspect testbench expectations
- Verify clock/reset sequencing
- Add clearer self-checks and logging

## Synthesis Issues

**Symptoms:**
- Hierarchy/top module not found
- Unsupported constructs
- Blackbox or missing module errors

**Action:**
- Verify top module name
- Flatten dependencies
- Replace unsupported simulation-only code with synthesizable alternatives

## Backend Issues

**Symptoms:**
- OpenLane stops before floorplan
- Routing/timing violations explode
- No final GDS generated
- Placement utilization exceeds 100%

**Action:**
- Check configuration and environment first
- If utilization exceeds 100%, increase `DIE_AREA` before modifying RTL
- If the flow succeeds but result collection finds no `runs/`, check `constraints/runs/`
- Then inspect design size and constraints
- Only then consider RTL restructuring
