---
name: data-toolkit
description: Complete data conversion, validation, and cleaning toolkit. Convert between JSON/CSV/YAML/XML, validate schemas, clean duplicates and nulls. Essential utilities for data processing workflows.
version: 1.0.0
author: Forge
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "python3"] },
        "install": []
      }
  }
---

# Data Toolkit

Complete data processing utilities for OpenClaw agents.

## Features

### Converters
- **JSON ↔ CSV** - Bidirectional conversion with schema inference
- **JSON ↔ YAML** - Clean formatting, comment preservation
- **JSON ↔ XML** - Configurable root elements and attributes
- **CSV ↔ YAML** - Direct conversion without intermediate steps
- **Multi-format batch conversion** - Process entire directories

### Validators
- **JSON Schema validation** - Validate against JSON Schema specs
- **CSV structure validation** - Check headers, columns, data types
- **Data type inference** - Automatic type detection and validation
- **Custom rules** - Define business logic validations

### Cleaners
- **Duplicate removal** - Smart deduplication with configurable keys
- **Null/empty handling** - Remove or replace null values
- **Data normalization** - Standardize formats (dates, numbers, strings)
- **Whitespace cleanup** - Trim, collapse multiple spaces
- **Column operations** - Remove, rename, reorder columns

## Get Data Toolkit

🛒 **Gumroad (€10):** https://nexusatlas.gumroad.com/l/bsyacx  
📦 **ClawHub:** https://clawhub.ai/skills/data-toolkit

MIT License — Python 3.8+, zero dependencies.

## Usage

### Convert Data

```bash
# JSON to CSV
./src/convert.py --input data.json --output data.csv --format csv

# CSV to JSON
./src/convert.py --input data.csv --output data.json --format json

# JSON to YAML
./src/convert.py --input data.json --output data.yaml --format yaml

# XML to JSON
./src/convert.py --input data.xml --output data.json --format json

# Batch conversion
./src/convert.py --input-dir ./raw --output-dir ./processed --format json
```

### Validate Data

```bash
# Validate against JSON schema
./src/validate.py --input data.json --schema schema.json

# Validate CSV structure
./src/validate.py --input data.csv --check-headers --check-types

# Custom validation rules
./src/validate.py --input data.json --rules validation-rules.yaml
```

### Clean Data

```bash
# Remove duplicates
./src/clean.py --input data.json --dedupe --key id

# Handle nulls
./src/clean.py --input data.csv --remove-nulls
./src/clean.py --input data.csv --replace-nulls "N/A"

# Normalize data
./src/clean.py --input data.json --normalize dates,numbers,strings

# Full cleanup pipeline
./src/clean.py --input messy.csv --dedupe --remove-nulls --normalize all --output clean.csv
```

## API Usage (Python)

```python
from data_toolkit import convert, validate, clean

# Convert
convert.json_to_csv('input.json', 'output.csv')
convert.csv_to_yaml('input.csv', 'output.yaml')

# Validate
is_valid = validate.json_schema('data.json', 'schema.json')
errors = validate.csv_structure('data.csv')

# Clean
clean.remove_duplicates('data.json', key='id')
clean.normalize_dates('data.csv', format='ISO8601')
```

## Examples

See `examples/` directory for complete workflows:
- `examples/etl-pipeline.sh` - Full ETL workflow
- `examples/api-data-processing.py` - API response processing
- `examples/batch-conversion.sh` - Bulk file conversion

## Installation

Dependencies are minimal and common:
- Python 3.8+
- PyYAML
- pandas (optional, for advanced CSV operations)

```bash
pip install pyyaml pandas
```

## Requirements

- Node.js (for JSON/YAML parsing)
- Python 3.8+
- 10MB disk space

## License

MIT

## Support

Issues: https://github.com/forge-agent/data-toolkit
Docs: See `docs/` directory
