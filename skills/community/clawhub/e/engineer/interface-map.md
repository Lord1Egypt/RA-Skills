# Interface Map

Use this file when the problem crosses teams, tools, machines, processes, or ownership boundaries.
Most engineering failures happen at interfaces, not inside a single box.

## Map the Handoffs

For each boundary, identify:
- what goes in
- what comes out
- who owns it
- what format, tolerance, or timing matters
- how failure is detected

Typical interfaces:
- operator to machine
- team to team
- supplier to plant
- lab to production
- design to build
- data source to decision

## Questions That Expose Hidden Breaks

- What assumption does each side believe the other side already knows?
- Where does information arrive late, incomplete, or in the wrong format?
- Which interface has no explicit owner?
- Which handoff depends on tribal knowledge rather than visible rules?

## Interface Risks

Watch for:
- incompatible units, formats, or tolerances
- unclear ownership
- latency and queue buildup
- manual workarounds that hide recurring failure
- one side optimizing for speed while the other optimizes for stability

## Minimum Output

Return:
1. boundary map
2. risky interfaces
3. owner per interface
4. checks or controls needed at each handoff

## Rule of Thumb

If the system looks confusing, draw the interfaces before debating solutions.
A bad boundary definition can make every local fix look wrong.
