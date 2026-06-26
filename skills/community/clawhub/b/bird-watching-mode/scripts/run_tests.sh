#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 bird_json_util_test.py
python3 set_region_test.py
python3 append_sighting_test.py
python3 identify_photo_test.py
python3 export_csv_test.py
echo "OK: all bird-watching-mode script tests passed"
