#!/usr/bin/env bash
set -u

# Detect KylinOS version: outputs "v11", "v10sp1", or "unknown"
desc=$(lsb_release -d 2>/dev/null)

if echo "$desc" | grep -qi 'V11'; then
  echo "v11"
elif echo "$desc" | grep -qi 'V10.*SP1'; then
  echo "v10sp1"
else
  echo "unknown"
fi
