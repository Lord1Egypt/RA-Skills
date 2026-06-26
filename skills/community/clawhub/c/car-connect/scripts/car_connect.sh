#!/usr/bin/env bash
# Car Connect — OpenClaw skill wrapper
# Base dir is relative to this script's location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$BASE_DIR/car_connect.py" "$@"
