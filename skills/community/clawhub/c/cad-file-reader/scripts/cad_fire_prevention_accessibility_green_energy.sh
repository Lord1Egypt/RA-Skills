#!/usr/bin/env bash
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_deep_geometry --pack fire_prevention_accessibility_green_energy "$@"
