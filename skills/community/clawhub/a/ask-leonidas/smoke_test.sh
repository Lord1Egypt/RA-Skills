#!/usr/bin/env bash
set -euo pipefail

python3 "$(dirname "$0")/healthcheck.py"

python3 "$(dirname "$0")/ask_leonidas.py"   --pain-point "I'm overwhelmed by repetitive follow-up emails after sales calls."   --return-candidates
