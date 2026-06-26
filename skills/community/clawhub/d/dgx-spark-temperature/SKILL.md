# dgx-spark-temperature

Read hardware temperature sensors on the DGX Spark via SNMP.

## When to use

- User asks for body temperature, DGX Spark temp, hardware temps, how hot things are running
- Any temperature/hardware health check request for the DGX Spark

## How to use

Run `exec` with:
```
bash <workspace>/skills/dgx-spark-temperature/check_temperature.sh
```

The script uses:
- `snmpwalk -v2c -c licpub dgx-spark1.fiber.house 1.3.6.1.4.1.2021.13.16.2.1`
- Parses LM-SENSORS MIB table: `lmTempSensorsIndex`, `lmTempSensorsDevice`, `lmTempSensorsValue`
- Values are in milliCelsius — divide by 1000 for °C

## Sensor mapping (16 sensors)

| IDX | Sensor Name           | Notes                           |
|-----|-----------------------|---------------------------------|
| 1   | asic                  | GPU/GB10 ASIC                   |
| 2   | Module0               | GPU Module 0                    |
| 3   | mlx5-pci-0100:asic    | Mellanox NIC #1 ASIC            |
| 4   | mlx5-pci-0100:Module0 | Mellanox NIC #1 module          |
| 5   | temp1                 | Generic thermal sensor          |
| 6   | temp2                 | Generic thermal sensor          |
| 7   | temp3                 | Generic thermal sensor          |
| 8   | temp4                 | Generic thermal sensor          |
| 9   | temp5                 | Generic thermal sensor          |
| 10  | temp6                 | Generic thermal sensor          |
| 11  | temp7                 | Generic thermal sensor          |
| 12  | mlx5-pci-20101:asic   | Mellanox NIC #3 ASIC            |
| 13  | mlx5-pci-0101:asic    | Mellanox NIC #2 ASIC            |
| 14  | Composite             | Overall/aggregate temp          |
| 15  | Sensor 1              | Additional thermal probe        |
| 16  | Sensor 2              | Additional thermal probe        |

## File layout

```
skills/dgx-spark-temperature/
  SKILL.md                    ← this file
  check_temperature.sh        ← the script
```

## Notes

- Community string is `licpub` (read-only)
- SNMPv2c, no auth/privacy
- DGX Spark runs Ubuntu 24.04 kernel 6.17, aarch64 (NVIDIA)
- Location: "Basement" (per SNMP sysLocation)
- Hostname: `bseitz-spark1`
