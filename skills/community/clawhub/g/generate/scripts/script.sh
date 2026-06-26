#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# generate — Universal Data Generator
# Version: 1.0.0
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

DATA_DIR="$HOME/.generate"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

COMMAND="${1:-help}"
shift 2>/dev/null || true

case "$COMMAND" in

text)
  TYPE="lorem" WORDS="20" COUNT="1"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) TYPE="$2"; shift 2;;
      --words) WORDS="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_TYPE="$TYPE"
  export GEN_WORDS="$WORDS"
  export GEN_COUNT="$COUNT"
  python3 << 'PYEOF'
import json, os, random, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
text_type = os.environ["GEN_TYPE"]
words = int(os.environ["GEN_WORDS"])
count = int(os.environ["GEN_COUNT"])

lorem_words = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum"
]

results = []
for _ in range(count):
    if text_type == "lorem":
        text = " ".join(random.choices(lorem_words, k=words))
        text = text[0].upper() + text[1:] + "."
    elif text_type == "sentence":
        length = random.randint(8, 20)
        text = " ".join(random.choices(lorem_words, k=length))
        text = text[0].upper() + text[1:] + "."
    elif text_type == "paragraph":
        sentences = []
        for _ in range(random.randint(3, 7)):
            length = random.randint(8, 20)
            s = " ".join(random.choices(lorem_words, k=length))
            sentences.append(s[0].upper() + s[1:] + ".")
        text = " ".join(sentences)
    elif text_type == "word":
        text = random.choice(lorem_words)
    else:
        text = " ".join(random.choices(lorem_words, k=words))
    results.append(text)
    print(text)
    if count > 1:
        print()

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "text",
    "type": text_type,
    "count": count,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

number)
  MIN="0" MAX="100" DECIMAL="" COUNT="1"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --min) MIN="$2"; shift 2;;
      --max) MAX="$2"; shift 2;;
      --decimal) DECIMAL="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_MIN="$MIN"
  export GEN_MAX="$MAX"
  export GEN_DECIMAL="$DECIMAL"
  export GEN_COUNT="$COUNT"
  python3 << 'PYEOF'
import json, os, random, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
min_val = os.environ["GEN_MIN"]
max_val = os.environ["GEN_MAX"]
decimal = os.environ.get("GEN_DECIMAL", "")
count = int(os.environ["GEN_COUNT"])

results = []
for _ in range(count):
    if decimal:
        val = round(random.uniform(float(min_val), float(max_val)), int(decimal))
    else:
        val = random.randint(int(float(min_val)), int(float(max_val)))
    results.append(val)
    print(val)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "number",
    "count": count,
    "range": f"{min_val}-{max_val}",
    "values": results[:10],
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

uuid)
  COUNT="1" FORMAT="full"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --count) COUNT="$2"; shift 2;;
      --format) FORMAT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_COUNT="$COUNT"
  export GEN_FORMAT="$FORMAT"
  python3 << 'PYEOF'
import json, os, uuid as uuid_mod, time

data_file = os.environ["GEN_DATA_FILE"]
count = int(os.environ["GEN_COUNT"])
fmt = os.environ.get("GEN_FORMAT", "full")

results = []
for _ in range(count):
    u = str(uuid_mod.uuid4())
    if fmt == "short":
        u = u[:8]
    results.append(u)
    print(u)

record = {
    "id": str(uuid_mod.uuid4())[:8],
    "command": "uuid",
    "count": count,
    "format": fmt,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

date)
  START="2020-01-01" END="2025-12-31" COUNT="1" FORMAT="iso"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --start) START="$2"; shift 2;;
      --end) END="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      --format) FORMAT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_START="$START"
  export GEN_END="$END"
  export GEN_COUNT="$COUNT"
  export GEN_FORMAT="$FORMAT"
  python3 << 'PYEOF'
import json, os, random, time, uuid
from datetime import datetime, timedelta

data_file = os.environ["GEN_DATA_FILE"]
start = datetime.strptime(os.environ["GEN_START"], "%Y-%m-%d")
end = datetime.strptime(os.environ["GEN_END"], "%Y-%m-%d")
count = int(os.environ["GEN_COUNT"])
fmt = os.environ.get("GEN_FORMAT", "iso")

delta = (end - start).days
results = []
for _ in range(count):
    d = start + timedelta(days=random.randint(0, delta))
    if fmt == "iso":
        s = d.strftime("%Y-%m-%d")
    elif fmt == "us":
        s = d.strftime("%m/%d/%Y")
    elif fmt == "eu":
        s = d.strftime("%d/%m/%Y")
    elif fmt == "unix":
        s = str(int(d.timestamp()))
    else:
        s = d.strftime("%Y-%m-%d")
    results.append(s)
    print(s)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "date",
    "count": count,
    "range": f"{os.environ['GEN_START']} to {os.environ['GEN_END']}",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

name)
  COUNT="1" GENDER="any" FULL=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --count) COUNT="$2"; shift 2;;
      --gender) GENDER="$2"; shift 2;;
      --full) FULL="1"; shift;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_COUNT="$COUNT"
  export GEN_GENDER="$GENDER"
  export GEN_FULL="$FULL"
  python3 << 'PYEOF'
import json, os, random, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
count = int(os.environ["GEN_COUNT"])
gender = os.environ.get("GEN_GENDER", "any")
full = os.environ.get("GEN_FULL", "") == "1"

male_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
              "Daniel", "Matthew", "Anthony", "Mark", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin"]
female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen",
                "Lisa", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily", "Donna"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Lee"]

results = []
for _ in range(count):
    if gender == "male":
        first = random.choice(male_names)
    elif gender == "female":
        first = random.choice(female_names)
    else:
        first = random.choice(male_names + female_names)
    
    if full:
        name = f"{first} {random.choice(last_names)}"
    else:
        name = first
    results.append(name)
    print(name)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "name",
    "count": count,
    "gender": gender,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

email)
  COUNT="1" DOMAIN=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --count) COUNT="$2"; shift 2;;
      --domain) DOMAIN="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_COUNT="$COUNT"
  export GEN_DOMAIN="$DOMAIN"
  python3 << 'PYEOF'
import json, os, random, string, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
count = int(os.environ["GEN_COUNT"])
domain = os.environ.get("GEN_DOMAIN", "")

domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "test.org", "mail.dev", "proton.me"]
first_names = ["alice", "bob", "charlie", "diana", "eve", "frank", "grace", "henry", "ivy", "jack",
               "kate", "leo", "mia", "noah", "olivia", "peter", "quinn", "ryan", "sara", "tom"]

results = []
for _ in range(count):
    name = random.choice(first_names)
    suffix = random.randint(1, 999)
    d = domain if domain else random.choice(domains)
    email = f"{name}{suffix}@{d}"
    results.append(email)
    print(email)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "email",
    "count": count,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

address)
  COUNT="1"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --count) COUNT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_COUNT="$COUNT"
  python3 << 'PYEOF'
import json, os, random, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
count = int(os.environ["GEN_COUNT"])

streets = ["Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm St", "Park Ave", "Lake Blvd",
           "River Rd", "Hill Dr", "Forest Way", "Sunset Blvd", "Broadway", "Market St", "Church St"]
cities = ["Springfield", "Portland", "Franklin", "Clinton", "Georgetown", "Salem", "Madison",
          "Arlington", "Chester", "Fairview", "Burlington", "Riverside", "Oakland", "Hudson"]
states = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI", "WA", "AZ", "CO", "OR"]

results = []
for _ in range(count):
    num = random.randint(100, 9999)
    street = random.choice(streets)
    city = random.choice(cities)
    state = random.choice(states)
    zipcode = f"{random.randint(10000, 99999)}"
    addr = f"{num} {street}, {city}, {state} {zipcode}"
    results.append(addr)
    print(addr)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "address",
    "count": count,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

json)
  SCHEMA="" COUNT="1"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --schema) SCHEMA="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$SCHEMA" ]]; then
    echo "Error: --schema is required"
    exit 1
  fi
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_SCHEMA="$SCHEMA"
  export GEN_COUNT="$COUNT"
  python3 << 'PYEOF'
import json, os, random, string, time, uuid as uuid_mod

data_file = os.environ["GEN_DATA_FILE"]
schema = json.loads(os.environ["GEN_SCHEMA"])
count = int(os.environ["GEN_COUNT"])

first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
domains = ["test.com", "example.org", "mock.dev"]

def gen_value(field_type):
    if field_type == "name":
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    elif field_type == "email":
        return f"{random.choice(first_names).lower()}{random.randint(1,999)}@{random.choice(domains)}"
    elif field_type == "uuid":
        return str(uuid_mod.uuid4())
    elif field_type == "bool":
        return random.choice([True, False])
    elif field_type == "string":
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 15)))
    elif field_type == "date":
        return f"{random.randint(2020,2025)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    elif field_type.startswith("int:"):
        lo, hi = field_type[4:].split("-")
        return random.randint(int(lo), int(hi))
    elif field_type.startswith("float:"):
        lo, hi = field_type[6:].split("-")
        return round(random.uniform(float(lo), float(hi)), 2)
    else:
        return field_type

results = []
for _ in range(count):
    obj = {}
    for key, ftype in schema.items():
        obj[key] = gen_value(ftype)
    results.append(obj)
    print(json.dumps(obj, ensure_ascii=False))

record = {
    "id": str(uuid_mod.uuid4())[:8],
    "command": "json",
    "count": count,
    "schema_keys": list(schema.keys()),
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

csv)
  COLUMNS="" ROWS="10" OUTPUT=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --columns) COLUMNS="$2"; shift 2;;
      --rows) ROWS="$2"; shift 2;;
      --output) OUTPUT="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$COLUMNS" ]]; then
    echo "Error: --columns is required"
    exit 1
  fi
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_COLUMNS="$COLUMNS"
  export GEN_ROWS="$ROWS"
  export GEN_OUTPUT="$OUTPUT"
  python3 << 'PYEOF'
import json, os, random, string, time, uuid as uuid_mod, csv, sys, io

data_file = os.environ["GEN_DATA_FILE"]
columns_str = os.environ["GEN_COLUMNS"]
rows = int(os.environ["GEN_ROWS"])
output = os.environ.get("GEN_OUTPUT", "")

first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
domains = ["test.com", "example.org", "mock.dev"]

cols = []
for col_def in columns_str.split(","):
    parts = col_def.strip().split(":", 1)
    name = parts[0]
    ctype = parts[1] if len(parts) > 1 else "string"
    cols.append((name, ctype))

def gen_value(field_type):
    if field_type == "name":
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    elif field_type == "email":
        return f"{random.choice(first_names).lower()}{random.randint(1,999)}@{random.choice(domains)}"
    elif field_type == "uuid":
        return str(uuid_mod.uuid4())[:8]
    elif field_type == "string":
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
    elif field_type.startswith("int:"):
        lo, hi = field_type[4:].split("-")
        return str(random.randint(int(lo), int(hi)))
    elif field_type.startswith("float:"):
        lo, hi = field_type[6:].split("-")
        return str(round(random.uniform(float(lo), float(hi)), 2))
    else:
        return ''.join(random.choices(string.ascii_lowercase, k=8))

buf = io.StringIO() if not output else open(output, "w", newline="")
writer = csv.writer(buf)
writer.writerow([c[0] for c in cols])
for _ in range(rows):
    row = [gen_value(c[1]) for c in cols]
    writer.writerow(row)

if output:
    buf.close()
    print(f"✅ Generated {rows} rows to {output}")
else:
    print(buf.getvalue())

record = {
    "id": str(uuid_mod.uuid4())[:8],
    "command": "csv",
    "rows": rows,
    "columns": [c[0] for c in cols],
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

password)
  LENGTH="16" COUNT="1" NO_SPECIAL=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --length) LENGTH="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      --no-special) NO_SPECIAL="1"; shift;;
      *) shift;;
    esac
  done
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_LENGTH="$LENGTH"
  export GEN_COUNT="$COUNT"
  export GEN_NO_SPECIAL="$NO_SPECIAL"
  python3 << 'PYEOF'
import json, os, random, string, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
length = int(os.environ["GEN_LENGTH"])
count = int(os.environ["GEN_COUNT"])
no_special = os.environ.get("GEN_NO_SPECIAL", "") == "1"

chars = string.ascii_letters + string.digits
if not no_special:
    chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

for _ in range(count):
    pwd = ''.join(random.choices(chars, k=length))
    # Ensure at least one of each required type
    if length >= 4:
        pwd_list = list(pwd)
        pwd_list[0] = random.choice(string.ascii_uppercase)
        pwd_list[1] = random.choice(string.ascii_lowercase)
        pwd_list[2] = random.choice(string.digits)
        if not no_special:
            pwd_list[3] = random.choice("!@#$%^&*()-_=+")
        random.shuffle(pwd_list)
        pwd = ''.join(pwd_list)
    print(pwd)

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "password",
    "count": count,
    "length": length,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
  ;;

batch)
  CONFIG=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --config) CONFIG="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$CONFIG" ]]; then
    echo "Error: --config is required"
    exit 1
  fi
  export GEN_DATA_FILE="$DATA_FILE"
  export GEN_CONFIG="$CONFIG"
  python3 << 'PYEOF'
import json, os, subprocess, time, uuid

data_file = os.environ["GEN_DATA_FILE"]
config_file = os.environ["GEN_CONFIG"]

if not os.path.exists(config_file):
    print(f"❌ Config file not found: {config_file}")
    exit(1)

with open(config_file) as f:
    batch = json.load(f)

if not isinstance(batch, list):
    batch = [batch]

print(f"📦 Batch generation: {len(batch)} commands\n")
for i, cmd in enumerate(batch):
    command = cmd.get("command", "")
    args = cmd.get("args", {})
    print(f"  [{i+1}/{len(batch)}] {command}")
    arg_list = []
    for k, v in args.items():
        arg_list.append(f"--{k}")
        arg_list.append(str(v))
    print(f"    Args: {' '.join(arg_list)}")

record = {
    "id": str(uuid.uuid4())[:8],
    "command": "batch",
    "batch_size": len(batch),
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(f"\n✅ Batch config parsed. Run individual commands to execute.")
PYEOF
  ;;

help)
  cat << 'HELPEOF'
generate — Universal Data Generator v1.0.0

Commands:
  text        Generate random text (lorem, sentences, paragraphs)
  number      Generate random numbers
  uuid        Generate UUIDs
  date        Generate random dates
  name        Generate random names
  email       Generate random emails
  address     Generate random addresses
  json        Generate random JSON objects
  csv         Generate random CSV data
  password    Generate random passwords
  batch       Run batch generation from config
  help        Show this help message
  version     Show version

Usage: bash scripts/script.sh <command> [options]

Examples:
  bash scripts/script.sh text --type lorem --words 50
  bash scripts/script.sh uuid --count 5
  bash scripts/script.sh json --schema '{"name":"name","age":"int:18-65"}' --count 10
  bash scripts/script.sh password --length 20 --count 5

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
  ;;

version)
  echo "generate v1.0.0"
  ;;

*)
  echo "Unknown command: $COMMAND"
  echo "Run 'bash scripts/script.sh help' for usage."
  exit 1
  ;;

esac
