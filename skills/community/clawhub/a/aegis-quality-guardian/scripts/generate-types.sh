#!/usr/bin/env bash
# aegis/scripts/generate-types.sh — Generate shared types from OpenAPI spec
# Usage: bash generate-types.sh /path/to/project
#
# Extracts component schemas from api-spec.yaml and generates TypeScript interfaces.
# Requires: python3 + pyyaml (auto-installs if missing)

set -euo pipefail

# Ensure pyyaml is available
if ! python3 -c "import yaml" 2>/dev/null; then
  echo "📦 Installing pyyaml..."
  python3 -m pip install --user pyyaml --quiet 2>/dev/null || {
    echo "❌ pyyaml is required but could not be installed. Install manually: pip install pyyaml"
    exit 1
  }
fi

PROJECT_PATH="${1:?Usage: generate-types.sh <project-path>}"
SPEC_FILE="$PROJECT_PATH/contracts/api-spec.yaml"
OUTPUT_FILE="$PROJECT_PATH/contracts/shared-types.ts"

if [ ! -f "$SPEC_FILE" ]; then
  echo "❌ API spec not found: $SPEC_FILE"
  exit 1
fi

echo "🔄 Generating shared types from: $SPEC_FILE"

python3 << 'PYTHON_SCRIPT' "$SPEC_FILE" "$OUTPUT_FILE"
import sys
import yaml
import json
from datetime import datetime

spec_file = sys.argv[1]
output_file = sys.argv[2]

with open(spec_file) as f:
    spec = yaml.safe_load(f)

schemas = spec.get("components", {}).get("schemas", {})
if not schemas:
    print("⚠️  No schemas found in components.schemas")
    sys.exit(0)

def yaml_type_to_ts(prop, required=False):
    """Convert OpenAPI type to TypeScript type."""
    if "$ref" in prop:
        ref_name = prop["$ref"].split("/")[-1]
        return ref_name
    
    t = prop.get("type", "unknown")
    fmt = prop.get("format", "")
    
    if t == "string":
        if "enum" in prop:
            return " | ".join(f'"{v}"' for v in prop["enum"])
        return "string"
    elif t == "integer" or t == "number":
        return "number"
    elif t == "boolean":
        return "boolean"
    elif t == "array":
        items_type = yaml_type_to_ts(prop.get("items", {}))
        return f"{items_type}[]"
    elif t == "object":
        if "properties" in prop:
            return "object"  # Will be expanded inline
        if "additionalProperties" in prop:
            val_type = yaml_type_to_ts(prop["additionalProperties"])
            return f"Record<string, {val_type}>"
        return "Record<string, unknown>"
    else:
        return "unknown"

lines = []
lines.append("// contracts/shared-types.ts")
lines.append(f"// ⚠️ AUTO-GENERATED from api-spec.yaml — DO NOT EDIT MANUALLY")
lines.append(f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append(f"// Regenerate: bash scripts/generate-types.sh <project-path>")
lines.append("")

for name, schema in schemas.items():
    desc = schema.get("description", "")
    required_fields = set(schema.get("required", []))
    properties = schema.get("properties", {})
    
    if desc:
        lines.append(f"/** {desc} */")
    
    # Handle allOf (extends)
    if "allOf" in schema:
        extends = []
        own_props = {}
        own_required = set()
        for item in schema["allOf"]:
            if "$ref" in item:
                extends.append(item["$ref"].split("/")[-1])
            elif "properties" in item:
                own_props.update(item.get("properties", {}))
                own_required.update(item.get("required", []))
        
        extends_str = f" extends {', '.join(extends)}" if extends else ""
        lines.append(f"export interface {name}{extends_str} {{")
        for pname, pschema in own_props.items():
            opt = "" if pname in own_required else "?"
            ts_type = yaml_type_to_ts(pschema)
            pdesc = pschema.get("description", "")
            if pdesc:
                lines.append(f"  /** {pdesc} */")
            lines.append(f"  {pname}{opt}: {ts_type};")
        lines.append("}")
    elif properties:
        lines.append(f"export interface {name} {{")
        for pname, pschema in properties.items():
            opt = "" if pname in required_fields else "?"
            ts_type = yaml_type_to_ts(pschema)
            pdesc = pschema.get("description", "")
            if pdesc:
                lines.append(f"  /** {pdesc} */")
            lines.append(f"  {pname}{opt}: {ts_type};")
        lines.append("}")
    elif "enum" in schema:
        values = " | ".join(f'"{v}"' for v in schema["enum"])
        lines.append(f"export type {name} = {values};")
    else:
        ts_type = yaml_type_to_ts(schema)
        lines.append(f"export type {name} = {ts_type};")
    
    lines.append("")

with open(output_file, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Generated {len(schemas)} type(s) → {output_file}")
PYTHON_SCRIPT

echo "Done."
