# Loop State

state: disarmed
last_changed: YYYY-MM-DD
start_trigger: /loop-start
stop_trigger: /loop-stop

Notes:
- When disarmed, the monitoring jobs should no-op.
- When armed, the monitoring jobs resume normal stall detection and recovery.
