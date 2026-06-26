# KB Preparation Patterns

Patterns for preparing JSON-converted documents for local knowledge base (RAG).

## Chunking by Section

Split a course-standard JSON into per-section chunks for embedding:

```python
import json

def chunk_by_section(data, parent_key=""):
    """Yield (section_title, text_content) pairs."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "表格" or key == "列表":
                continue  # skip structured data for now
            elif isinstance(value, (dict, list)) and not isinstance(value, str):
                yield from chunk_by_section(value, parent_key=key)
            elif isinstance(value, str) and value.strip():
                title = f"{parent_key}/{key}" if parent_key else key
                yield (title.strip("/"), value.strip())
```

## Table Flattening

Convert table arrays into flat row dicts:

```python
def flatten_tables(data):
    """Extract all tables as list of (section, header_dict) pairs."""
    results = []
    if isinstance(data, dict):
        for key, val in data.items():
            if key == "表格" and isinstance(val, list):
                for table in val:
                    if len(table) >= 2:
                        headers = table[0]
                        for row in table[1:]:
                            row_dict = {}
                            for h, c in zip(headers, row):
                                row_dict[h] = c
                            results.append(row_dict)
            else:
                results.extend(flatten_tables(val))
    elif isinstance(data, list):
        for item in data:
            results.extend(flatten_tables(item))
    return results
```

## Cleaning Text

Remove MinerU artifacts and normalize whitespace:

```python
import re

def clean_text(text):
    """Clean MinerU markdown artifacts."""
    text = re.sub(r"<[^>]+>", "", text)  # strip any leftover HTML
    text = re.sub(r"\n{3,}", "\n\n", text)  # normalize line breaks
    text = re.sub(r"\s+", " ", text)  # normalize spaces
    return text.strip()
```

## Full Pipeline Example

```python
import json

def prepare_for_rag(json_path, chunk_size=500):
    """Load JSON, chunk by section, clean text, return chunks."""
    with open(json_path) as f:
        data = json.load(f)

    chunks = []
    for title, text in chunk_by_section(data):
        cleaned = clean_text(text)
        if len(cleaned) > 50:  # skip very short chunks
            chunks.append({
                "title": title,
                "text": cleaned,
                "source": json_path
            })
    return chunks
```
