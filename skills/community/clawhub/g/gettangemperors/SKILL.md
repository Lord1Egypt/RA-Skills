---
name: tang-emperors-api
description: Query local backend API for Tang Dynasty emperor information. Use when user asks about Tang emperors, needs to fetch emperor data from local API, or references唐朝皇帝 / 唐朝前3代皇帝 / 唐朝帝王. The API runs at http://127.0.0.1:8080 with GET /api/v1/test endpoint.
---

# Tang Emperors API

## Overview

This skill provides integration with a local backend API that returns information about the first three emperors of the Tang Dynasty (唐朝前3代皇帝). The API is deployed locally at `http://127.0.0.1:8080` with the endpoint `GET /api/v1/test`.

## Quick Start

Fetch Tang Dynasty emperor information:

```bash
python3 scripts/get_tang_emperors.py
```

Output formatted as human-readable text:
```bash
python3 scripts/get_tang_emperors.py
```

Output raw JSON:
```bash
python3 scripts/get_tang_emperors.py --json
```

## API Details

- **Base URL**: `http://127.0.0.1:8080`
- **Endpoint**: `/api/v1/test`
- **Method**: GET
- **Returns**: JSON data about the first three Tang Dynasty emperors

## Error Handling

The script includes comprehensive error handling:

- **Connection errors**: Backend not running or unreachable
- **Timeout errors**: API response timeout (10s default)
- **HTTP errors**: Invalid HTTP responses (404, 500, etc.)
- **JSON parsing errors**: Malformed response data
- **Unexpected errors**: Other runtime errors

## Usage Patterns

**Direct API call:**
```bash
curl http://127.0.0.1:8080/api/v1/test
```

**Via Python script (recommended):**
```bash
python3 scripts/get_tang_emperors.py
```

**Programmatic access in Python:**
```python
from scripts.get_tang_emperors import get_tang_emperors, format_emperor_data

data = get_tang_emperors()
formatted = format_emperor_data(data)
print(formatted)
```

## Resources

### scripts/get_tang_emperors.py

Python client for the Tang Emperors API with:

- `get_tang_emperors()`: Fetches raw JSON data from API
- `format_emperor_data()`: Formats data for human-readable output
- CLI support with `--json` flag for raw JSON output
- Comprehensive error handling and timeout management

The script can be:
- Executed directly from command line
- Imported as a module in other Python code
- Used by Codex for automated API interactions

## Notes

- Ensure the local backend is running before making API calls
- The API expects a GET request with no parameters
- Response format may vary; the script handles common patterns (list, dict with 'emperors' key, dict with 'data' key)
- Default timeout is 10 seconds; adjust in script if needed for your environment
