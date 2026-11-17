#!/usr/bin/env bash
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_deep_geometry --pack doors_windows_stairs_insulation_waterproof "$@"
