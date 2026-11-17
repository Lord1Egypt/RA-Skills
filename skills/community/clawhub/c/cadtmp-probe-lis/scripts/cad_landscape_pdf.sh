#!/usr/bin/env bash
# PDF → 园林识图候选
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_cad.py" cad_landscape_pdf "$@"
