# ClawStatus Rules

## System Configuration Change Rules (Highest Priority)

- Before modifying any system configuration (services, ports, processes, system files), thoroughly check for logic errors first
- Always verify the change won't cause resource exhaustion (infinite loops, memory leaks, runaway processes)
- Test configuration changes in isolation before applying to the live system
- Never blindly restart or reconfigure system services without understanding the current state
- When editing code that controls system resources (processes, sockets, threads), review the full execution path for correctness before saving
