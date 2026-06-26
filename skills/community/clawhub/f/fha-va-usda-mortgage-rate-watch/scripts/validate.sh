#!/usr/bin/env bash
set -euo pipefail

test -f README.md
test -f SKILL.md
test -f references/loan-programs.md
test -f references/newsletter-template.md
test -f scripts/payment_calc.py
grep -q '^name:' SKILL.md
grep -q '^description:' SKILL.md
python3 scripts/payment_calc.py --principal 250000 --rate 6.5 --years 30 > /dev/null
echo "validation passed"
