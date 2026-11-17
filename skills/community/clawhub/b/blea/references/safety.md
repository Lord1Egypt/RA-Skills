# BLE safety policy

## Risk levels

- Read-only: scan, service discovery, characteristic reads, bounded notifications.
- State-changing: writes, pairing changes, bonding removal, configuration, control commands.
- High impact: locks, medical devices, vehicles, access control, firmware update, calibration,
  factory reset, actuators, or commands whose meaning is unknown.

## Required checks before a write

1. Resolve exactly one device and retain its platform identifier.
2. Inspect the characteristic properties and protocol documentation or prior observed behavior.
3. Establish a harmless prerequisite read or assertion when possible.
4. Show the target identifier, characteristic, encoding, exact bytes, and expected effect.
5. Obtain authorization for that operation.
6. Enable the BLEA write guard and confirm the exact resolved identifier.
7. Prefer write-with-response and read-back or notification verification.

Do not infer that a short UUID is safe, that a writable characteristic is configuration-only, or
that a nearby device belongs to the user. Do not repeatedly retry an unknown write.

Client-side MCP approvals are additional protection, not a replacement for BLEA's server-side
guard.
