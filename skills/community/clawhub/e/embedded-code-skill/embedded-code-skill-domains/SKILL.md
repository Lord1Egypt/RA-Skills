---
name: embed-code-domains
description: Industry domain requirements. Aerospace (DO-178C), Military (MIL-STD), Industrial (IEC 61508), Automotive (ISO 26262).
---

# Industry Domain Requirements

## Detection

| Domain | Keywords |
|--------|----------|
| Aerospace | DO-178C, DAL, ARINC, flight |
| Military | 1553B, SpaceWire, MIL-STD, radar |
| Industrial | IEC 61508, SIL, PLC, SCADA |
| Automotive | ISO 26262, ASIL, CANFD |

---

## Aerospace (DO-178C)

**DAL Levels**: A (MC/DC 100%), B (MC/DC 100%), C (Statement/Branch)

```c
/**
 * @file navigation.c
 * @brief Navigation processing
 *
 * ### Safety Level: DAL-B ###
 * - DO-178C compliance
 * - MC/DC coverage required
 *
 * ### Software Level Database ###
 * - Req ID: NAV-001
 */
```

**Requirements**:
- No dynamic allocation
- Deterministic behavior
- No recursion
- Complexity < 10

---

## Military (MIL-STD-1553B)

```c
/**
 * @file missile_ctrl.c
 * @brief Missile guidance control
 *
 * ### Standards ###
 * - MIL-STD-1553B
 * - SEU protection required
 * - BIT coverage > 95%
 */
```

**Requirements**:
- Hardware redundancy
- SEU protection
- BIT diagnostics

---

## Industrial (IEC 61508)

**SIL Levels**: 1, 2, 3, 4

```c
/**
 * @file plc_comm.c
 * @brief PLC communication
 *
 * ### IEC 61508 SIL-2 ###
 * - Safe state on failure
 * - Diagnostic coverage > 90%
 */
```

**Requirements**:
- Safe state defined
- Watchdog supervision
- Deterministic response

---

## Automotive (ISO 26262)

**ASIL Levels**: A, B, C, D

```c
/**
 * @file abs_controller.c
 * @brief ABS control
 *
 * ### ASIL-B ###
 * - ISO 26262 Part 2-6
 * - SPFM > 90%, LFM > 60%
 */
```

**Requirements**:
- ASIL decomposition
- Hardware fault tolerance
- Freedom from interference

---

## Default (General Embedded)

```c
/**
 * @file sensor_driver.c
 * @brief Temperature sensor driver
 *
 * ### Architecture ### ARM Cortex-M4
 * ### Domain ### General Embedded
 */
```

No special safety requirements.

---

## Quick Ref

| Domain | Standard | Level | Key |
|--------|----------|-------|-----|
| Aerospace | DO-178C | DAL-A/B/C | MC/DC |
| Military | MIL-STD-1553B | - | SEU |
| Industrial | IEC 61508 | SIL-1-4 | Safe state |
| Automotive | ISO 26262 | ASIL-A/B | SPFM/LFM |
