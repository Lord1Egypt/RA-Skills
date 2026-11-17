#!/usr/bin/env bash
# Convert DWG/DWT to DXF using vendored ezdwg.
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" convert_dwg "$@"
