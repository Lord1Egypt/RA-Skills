---
name: data-extractor
description: Extract structured data from unstructured sources. Parse JSON, CSV, logs, and mixed formats into clean, usable data. Handle malformed data, nested structures, and large files efficiently. Use when extracting data from messy inputs, parsing logs, or cleaning datasets. Triggers on "extract data", "parse json", "parse csv", "clean data", "log parser".
---

# Data Extractor

Extract structured, clean data from unstructured or messy sources. Turn chaos into usable data.

## Supported Formats

### JSON
- Nested objects
- Arrays of objects
- Mixed types
- Malformed JSON
- Large files (streaming)

### CSV
- Headers or headerless
- Various delimiters
- Quoted fields
- Multiline values
- Large files (streaming)

### Logs
- Application logs
- Server logs
- Error logs
- Access logs
- Custom formats

### Text
- Key-value pairs
- Tables
- Lists
- Mixed content

## Common Patterns

### Extract JSON from Text

```
Input: "The response was {'status': 'ok', 'data': [1, 2, 3]} and then..."
Output: {"status": "ok", "data": [1, 2, 3]}
```

```python
import re
import json

def extract_json(text):
    # Find JSON-like structures
    pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(pattern, text)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    return None
```

### Parse CSV with Issues

```
# Handle: missing values, inconsistent quotes, mixed delimiters
```

```python
import csv
from io import StringIO

def parse_messy_csv(text):
    lines = text.strip().split('\n')
    
    # Detect delimiter
    delimiters = [',', ';', '\t', '|']
    delimiter = ','
    for d in delimiters:
        if lines[0].count(d) > lines[0].count(delimiter):
            delimiter = d
    
    # Parse with error handling
    reader = csv.reader(StringIO(text), delimiter=delimiter)
    rows = []
    for row in reader:
        # Clean each field
        cleaned = [field.strip().strip('"').strip("'") for field in row]
        rows.append(cleaned)
    
    return rows
```

### Extract Key-Value Pairs

```
Input: "name: John, age: 30, city: New York"
Output: {"name": "John", "age": "30", "city": "New York"}
```

```python
import re

def extract_key_value(text):
    patterns = [
        r'(\w+)\s*:\s*([^,\n]+)',      # key: value
        r'(\w+)\s*=\s*([^,\n]+)',      # key=value
        r'"?(\w+)"?\s*[:=]\s*"?([^,"\n]+)"?',  # quoted variants
    ]
    
    result = {}
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for key, value in matches:
            result[key.strip()] = value.strip()
    
    return result
```

### Parse Logs

```
# Common log formats
```

```python
import re
from datetime import datetime

def parse_log_line(line):
    # Try common patterns
    
    # Apache/Nginx access log
    pattern = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) ([^"]+) HTTP/\d\.\d" (\d+) (\d+)'
    match = re.match(pattern, line)
    if match:
        return {
            "ip": match.group(1),
            "timestamp": match.group(2),
            "method": match.group(3),
            "path": match.group(4),
            "status": int(match.group(5)),
            "size": int(match.group(6))
        }
    
    # JSON log
    if line.startswith('{'):
        try:
            return json.loads(line)
        except:
            pass
    
    # Key-value log
    if '=' in line:
        return extract_key_value(line)
    
    return {"raw": line}
```

## Handling Edge Cases

### Malformed JSON

```python
def fix_json(text):
    # Common fixes
    
    # Single quotes to double quotes
    text = re.sub(r"'([^']*)'", r'"\1"', text)
    
    # Unquoted keys
    text = re.sub(r'(\w+):', r'"\1":', text)
    
    # Trailing commas
    text = re.sub(r',\s*([}\]])', r'\1', text)
    
    # Missing quotes around values
    text = re.sub(r':\s*([a-zA-Z_]\w*)(?=[,}\]])', r': "\1"', text)
    
    return text
```

### Large Files

```python
def stream_jsonl(file_path):
    """Stream JSON Lines (JSONL) format"""
    with open(file_path, 'r') as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

def stream_csv(file_path, chunk_size=1000):
    """Stream CSV in chunks"""
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        chunk = []
        for row in reader:
            chunk.append(dict(zip(headers, row)))
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        
        if chunk:
            yield chunk
```

### Mixed Formats

```python
def detect_and_parse(content):
    """Auto-detect format and parse"""
    
    content = content.strip()
    
    # JSON
    if content.startswith('{') or content.startswith('['):
        try:
            return json.loads(content)
        except:
            pass
    
    # JSONL
    if '\n{' in content:
        try:
            return [json.loads(line) for line in content.split('\n') if line.strip()]
        except:
            pass
    
    # CSV
    if ',' in content and '\n' in content:
        lines = content.split('\n')
        if len(lines) > 1:
            return parse_messy_csv(content)
    
    # Key-value
    if '=' in content or ':' in content:
        return extract_key_value(content)
    
    # Lines
    return content.split('\n')
```

## Data Cleaning

### Remove Duplicates

```python
def deduplicate(data, key=None):
    if isinstance(data, list):
        if key:
            seen = set()
            result = []
            for item in data:
                val = item.get(key) if isinstance(item, dict) else item
                if val not in seen:
                    seen.add(val)
                    result.append(item)
            return result
        return list(set(data))
    return data
```

### Normalize Values

```python
def normalize(data):
    if isinstance(data, dict):
        return {k: normalize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize(item) for item in data]
    elif isinstance(data, str):
        # Lowercase, trim, standardize whitespace
        data = data.lower().strip()
        data = re.sub(r'\s+', ' ', data)
        
        # Convert common values
        if data in ('true', 'yes', 'on'):
            return True
        if data in ('false', 'no', 'off'):
            return False
        if data in ('null', 'none', 'n/a', ''):
            return None
        
        # Try numeric
        try:
            return int(data)
        except:
            try:
                return float(data)
            except:
                pass
        
        return data
    return data
```

### Validate Schema

```python
def validate(data, schema):
    errors = []
    
    # Required fields
    for field in schema.get('required', []):
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Type checking
    for field, expected_type in schema.get('types', {}).items():
        if field in data and not isinstance(data[field], expected_type):
            errors.append(f"Field {field} should be {expected_type.__name__}")
    
    # Value ranges
    for field, (min_val, max_val) in schema.get('ranges', {}).items():
        if field in data:
            if not (min_val <= data[field] <= max_val):
                errors.append(f"Field {field} out of range: {data[field]}")
    
    return len(errors) == 0, errors
```

## Output Formats

### To JSON

```python
import json

def to_json(data, pretty=True):
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)
```

### To CSV

```python
import csv
from io import StringIO

def to_csv(data, headers=None):
    if not data:
        return ""
    
    output = StringIO()
    
    if isinstance(data[0], dict):
        headers = headers or list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    else:
        writer = csv.writer(output)
        if headers:
            writer.writerow(headers)
        writer.writerows(data)
    
    return output.getvalue()
```

### To Markdown Table

```python
def to_markdown_table(data):
    if not data:
        return ""
    
    if isinstance(data[0], dict):
        headers = list(data[0].keys())
        rows = [[str(row.get(h, '')) for h in headers] for row in data]
    else:
        headers = [f"Col {i+1}" for i in range(len(data[0]))]
        rows = data
    
    # Build table
    result = []
    result.append('| ' + ' | '.join(headers) + ' |')
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    for row in rows:
        result.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
    
    return '\n'.join(result)
```

## Usage Examples

### Example 1: Extract JSON from API Response

```
Input (messy):
"API returned: {status: 'success', data: {users: [{id: 1, name: 'John'}, {id: 2, name: 'Jane'}]}, timestamp: '2026-03-16'}"

Output (clean):
{
  "status": "success",
  "data": {
    "users": [
      {"id": 1, "name": "John"},
      {"id": 2, "name": "Jane"}
    ]
  },
  "timestamp": "2026-03-16"
}
```

### Example 2: Parse Mixed Log

```
Input:
192.168.1.1 - - [16/Mar/2026:12:00:00 +0000] "GET /api HTTP/1.1" 200 1234
{"level": "INFO", "message": "User logged in", "user_id": 123}
name=John action=login time=12:00

Output:
[
  {"ip": "192.168.1.1", "timestamp": "16/Mar/2026:12:00:00 +0000", "method": "GET", "path": "/api", "status": 200, "size": 1234},
  {"level": "INFO", "message": "User logged in", "user_id": 123},
  {"name": "John", "action": "login", "time": "12:00"}
]
```

### Example 3: Clean CSV

```
Input (messy):
name,age,city
"John", 30, "New York"
'Jane',,Los Angeles
"Bob","forty","Chicago"

Output (clean):
[
  {"name": "John", "age": 30, "city": "New York"},
  {"name": "Jane", "age": null, "city": "Los Angeles"},
  {"name": "Bob", "age": "forty", "city": "Chicago"}
]
```

## Best Practices

1. **Always validate input** - Check format before parsing
2. **Handle errors gracefully** - Log and continue or fail cleanly
3. **Stream large files** - Don't load everything into memory
4. **Normalize consistently** - Same rules for all data
5. **Document transformations** - What changed and why
6. **Preserve originals** - Keep raw data until confirmed clean
7. **Test edge cases** - Empty, null, malformed, very large
8. **Use appropriate types** - Numbers as numbers, dates as dates

## Performance Tips

1. **Use streaming** for files > 10MB
2. **Batch processing** for database inserts
3. **Parallel parsing** for independent chunks
4. **Lazy evaluation** with generators
5. **Cache parsed results** if reused frequently