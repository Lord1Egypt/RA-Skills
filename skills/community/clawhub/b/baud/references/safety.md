# Serial Hardware Safety and Diagnosis

## Before Opening A Port

- Confirm voltage levels, ground reference, connector orientation, and whether the adapter drives target power.
- Identify the adapter with USB metadata instead of relying only on a COM or tty name.
- Determine whether opening the port or changing DTR/RTS resets the target or enters a bootloader.
- Find the firmware's line protocol, encoding, baud rate, and harmless status commands.
- Identify physical outputs that could move, heat, inject, erase, energize, or store persistent configuration.

## Transmission Ladder

Use the lowest sufficient level:

1. Enumerate ports.
2. Monitor without transmitting.
3. Send a documented read-only query.
4. Probe alternate line endings with known-safe queries.
5. Change one reversible configuration value.
6. Read the value back independently.
7. Run one guarded physical cycle.
8. Increase duration, count, or load only after verified results.

## Diagnose Communication Direction

Interpret evidence by direction:

- Startup output with no command response: device TX to host RX works; host TX to device RX, pin mapping, or the firmware command loop may not work.
- No startup output and no response: port identity, wiring, target power, baud rate, or firmware state remains unknown.
- Echo without a semantic response: bytes may loop locally or firmware may echo before command processing. Do not count echo as command success.
- Response to one line ending only: preserve that ending explicitly in later commands and workflows.

Use raw byte length and Base64 evidence when text decoding could hide NULs, invalid UTF-8, or partial banners.

## Diagnose Resets And Disconnects

- Treat a startup banner repeated after a command as a probable reset.
- Treat a disappearing and reappearing port as a USB reset or mode change until proven otherwise.
- Separate a fixed command response timeout from a physical disconnect.
- Check whether a long initialization path prevents firmware from reaching its command loop even though setup printed a banner.
- Avoid high-frequency debugger reads that pause the CPU and trigger a watchdog; use bounded samples.

## Gate Physical Actions

Before transmitting an action command, verify all device-specific invariants, for example:

- expected firmware/build identity;
- power and fault status;
- sensor presence;
- target or setpoint read-back;
- trigger enable and latch state;
- safe initial position;
- one-cycle count;
- timeout and stop behavior.

Express these invariants as earlier workflow assertions. Make the action step `dangerous: true` and list the successful assertion steps in `requires`.

Never infer safety from ACK alone. Require a snapshot, status query, physical input, or another independent confirmation appropriate to the device.

## Port Ownership

On a busy port, report the exact open error and re-enumerate ports. Do not terminate a process unless the user has identified it and authorized that action. Always close the serial handle on success, assertion failure, timeout, interruption, and disconnect.
