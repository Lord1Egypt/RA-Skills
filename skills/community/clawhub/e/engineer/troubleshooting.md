# Troubleshooting

Use this file when a system is unstable, inconsistent, or failing intermittently.
The first job is to learn something reliable from the next test, not to look busy.

## Troubleshooting Sequence

1. define the failure precisely
2. identify when it does and does not happen
3. isolate one variable at a time
4. capture evidence before resetting the system
5. test the highest-probability mechanism first

If the problem is urgent, contain first and investigate second.

## Evidence to Capture

- exact symptom
- timestamp and operating condition
- recent changes
- inputs, loads, materials, or environmental conditions
- alarms, measurements, and operator observations

Without timestamps and conditions, patterns stay invisible.

## Fast Filters

Check these early:
- what changed recently
- what is overloaded or starved
- what drifts over time
- what depends on manual intervention
- what only fails at startup, shutdown, or transition

## Avoid These Moves

- changing multiple things together
- wiping the evidence with a restart
- assuming the last visible component is the root cause
- closing the issue because the symptom stopped once
- treating anecdote as a trend

## Minimum Output

Return:
1. failure definition
2. leading hypotheses
3. next test
4. data to capture
5. containment while learning
