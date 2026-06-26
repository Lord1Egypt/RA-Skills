#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${ENV_FILE:-.env}"
ALIAS_SPEC_FILE="${ALIAS_SPEC_FILE:-}"
REQUIRED_GROUPS="${REQUIRED_GROUPS:-}"
AUDIT_MODE="${AUDIT_MODE:-strict}"

if [[ "$AUDIT_MODE" != "report" && "$AUDIT_MODE" != "strict" ]]; then
  echo "ERROR: AUDIT_MODE must be 'report' or 'strict' (got: $AUDIT_MODE)" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: ENV_FILE not found: $ENV_FILE" >&2
  exit 1
fi

if [[ -n "$ALIAS_SPEC_FILE" && ! -f "$ALIAS_SPEC_FILE" ]]; then
  echo "ERROR: ALIAS_SPEC_FILE not found: $ALIAS_SPEC_FILE" >&2
  exit 1
fi

python3 - "$ENV_FILE" "$ALIAS_SPEC_FILE" "$REQUIRED_GROUPS" "$AUDIT_MODE" <<'PY'
import re
import sys
from pathlib import Path


def parse_env_file(path: Path):
    values = {}
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[7:].strip()
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
            continue
        values[key] = value.strip()
    return values


def parse_alias_spec(text: str):
    groups = {}
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            raise ValueError(f'invalid alias spec line {idx}: missing "="')
        canonical, aliases_raw = line.split('=', 1)
        canonical = canonical.strip()
        if not canonical:
            raise ValueError(f'invalid alias spec line {idx}: empty canonical key')
        aliases = [a.strip() for a in aliases_raw.split(',') if a.strip()]
        members = [canonical] + [a for a in aliases if a != canonical]
        groups[canonical] = members
    return groups


def default_groups():
    text = """
STRIPE_API_KEY=STRIPE_KEY,STRIPE_SECRET
STRIPE_PRICE_ID=STRIPE_PRICE,STRIPE_MONTHLY_PRICE,STRIPE_MONTHLY_PRICE_ID
STRIPE_ENDPOINT_SECRET=STRIPE_SIGNING_SECRET,STRIPE_WEBHOOK_SECRET
DATABASE_URL=POSTGRES_PRISMA_URL,POSTGRES_URL,POSTGRES_URL_NON_POOLING,DATABASE_URL_NON_POOLING
DIRECT_URL=DATABASE_DIRECT_URL,PRISMA_DIRECT_URL
SHADOW_DATABASE_URL=DATABASE_SHADOW_URL,PRISMA_SHADOW_DATABASE_URL
""".strip()
    return parse_alias_spec(text)


def short(value: str):
    if value == '':
        return '(empty)'
    if len(value) <= 16:
        return value
    return value[:8] + '…' + value[-4:]


env_file = Path(sys.argv[1])
alias_spec_file = sys.argv[2]
required_raw = sys.argv[3]
audit_mode = sys.argv[4]

env_values = parse_env_file(env_file)
if alias_spec_file:
    groups = parse_alias_spec(Path(alias_spec_file).read_text(encoding='utf-8'))
else:
    groups = default_groups()

if not groups:
    print('ERROR: no alias groups defined', file=sys.stderr)
    sys.exit(1)

required = [k.strip() for k in required_raw.split(',') if k.strip()]
unknown_required = [k for k in required if k not in groups]
if unknown_required:
    print('ERROR: REQUIRED_GROUPS includes unknown canonical keys: ' + ', '.join(unknown_required), file=sys.stderr)
    sys.exit(1)

failures = []
warns = []
ok = 0

for canonical, members in groups.items():
    present = [(k, env_values[k]) for k in members if k in env_values and env_values[k] != '']
    distinct = sorted({v for _, v in present})

    if len(distinct) > 1:
        preview = ', '.join([f'{k}={short(v)}' for k, v in present])
        failures.append(f'{canonical}: conflicting values across aliases ({preview})')
        print(f'FAIL {canonical} -> conflict across {len(present)} keys')
        continue

    if canonical in required and not present:
        message = f'{canonical}: required group not set'
        if audit_mode == 'strict':
            failures.append(message)
            print(f'FAIL {canonical} -> missing required value')
        else:
            warns.append(message)
            print(f'WARN {canonical} -> missing required value (report mode)')
        continue

    if present and canonical not in dict(present):
        alias_name = present[0][0]
        warns.append(f'{canonical}: alias-only usage via {alias_name}')
        print(f'WARN {canonical} -> alias-only ({alias_name})')
        continue

    print(f'OK   {canonical} -> ' + (short(present[0][1]) if present else 'unset'))
    ok += 1

print('---')
print(f'SUMMARY: groups={len(groups)} ok={ok} warn={len(warns)} fail={len(failures)} mode={audit_mode}')

if warns:
    print('WARNINGS:')
    for item in warns:
        print(f'- {item}')

if failures:
    print('FAILURES:', file=sys.stderr)
    for item in failures:
        print(f'- {item}', file=sys.stderr)
    sys.exit(1)

sys.exit(0)
PY
