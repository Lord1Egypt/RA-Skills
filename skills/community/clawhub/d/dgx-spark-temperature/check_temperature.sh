#!/usr/bin/env bash
# check_temperature — read DGX Spark temps via SNMP and format nicely
# Usage: bash check_temperature.sh
#
# Requires: snmpwalk (net-snmp-utils)
# SNMP target: dgx-spark1.fiber.house, v2c, community "licpub"
# MIB: LM-SENSORS (UCD-SNMP-MIB) OID 1.3.6.1.4.1.2021.13.16.2.1

SNMPDST="dgx-spark1.fiber.house"
COMMUNITY="licpub"
OID_BASE="1.3.6.1.4.1.2021.13.16.2.1"

# Fetch all name/value columns
WALK=$(snmpwalk -v2c -c "$COMMUNITY" "$SNMPDST" "$OID_BASE" 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$WALK" ]; then
  echo "ERROR: SNMP walk failed"
  exit 1
fi

# Parse SNMP output using gawk
# OID format: iso.3.6.1.4.1.2021.13.16.2.1.COL.INDEX
# COL 1 = index (lmTempSensorsIndex), 2 = name (lmTempSensorsDevice), 3 = value (lmTempSensorsValue)
echo "$WALK" | gawk '
BEGIN {
  count = 0
}
{
  # Split the OID (first field) by dots to get column type and index
  split($1, oid_parts, ".")
  n = length(oid_parts)
  idx = oid_parts[n] + 0
  col = oid_parts[n-1] + 0

  if (col == 1 && idx > 0) {
    # lmTempSensorsIndex
    if (!(idx in names)) {
      count++
      indices[count] = idx
    }
  }
  else if (col == 2 && idx > 0) {
    # lmTempSensorsDevice — extract quoted string from line
    if (match($0, /"([^"]+)"/, s)) {
      names[idx] = s[1]
    }
  }
  else if (col == 3 && idx > 0) {
    # lmTempSensorsValue — Gauge32
    if (match($0, /Gauge32: ([0-9]+)/, v)) {
      vals[idx] = v[1] + 0
    }
  }
}
END {
  printf "\n=== DGX Spark Temperature Report ===\n\n"
  printf "%-4s %-30s %10s\n", "IDX", "SENSOR", "TEMP (°C)"
  printf "%-4s %-30s %10s\n", "---", "------------------------------", "----------"

  max_c = -999
  min_c = 999
  max_name = ""
  min_name = ""
  sum = 0
  cnt = 0

  for (i = 1; i <= count; i++) {
    idx = indices[i]
    name = (idx in names) ? names[idx] : "unknown"
    val = (idx in vals) ? vals[idx] : -1

    if (val >= 0) {
      temp = val / 1000.0
      printf "%-4s %-30s %8.1f°C\n", idx, name, temp
      sum += temp
      cnt++
      if (temp > max_c) { max_c = temp; max_name = name }
      if (temp < min_c) { min_c = temp; min_name = name }
    } else {
      printf "%-4s %-30s %10s\n", idx, name, "N/A"
    }
  }

  printf "\n=== Summary ===\n"
  if (cnt > 0) {
    printf "  Avg: %.1f°C\n", sum / cnt
    printf "  Max: %.1f°C (%s)\n", max_c, max_name
    printf "  Min: %.1f°C (%s)\n", min_c, min_name
  }
}
'
