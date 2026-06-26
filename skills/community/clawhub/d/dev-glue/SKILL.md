---
name: dev-glue
description: JSON transformation, schema validation, text diffing, document conversion. Four developer utility micro-services. Use for data transformation, validation, and format conversion.
---

# Dev Glue

Four utility services for data transformation and validation.

## Services

### /transform-json — JSON Transformation
Apply expressions to transform JSON data.
```
POST /x402s/transform-json
Body: {"input": {"users": [...]}, "expression": "users[0].name"}
Response: {"output": "Alice", "expression": "users[0].name"}
Price: $0.001 USDC
```

### /validate-json — Schema Validation
Validate JSON against schema with human-readable errors.
```
POST /x402s/validate-json
Body: {"input": {...}, "schema": {...}}
Response: {"valid": false, "errors": [{"path": ["name"], "message": "required", "rule": "required"}]}
Price: $0.001 USDC
```

### /compare-text — Text Diff
Semantic diff between two texts with similarity score.
```
POST /x402s/compare-text
Body: {"text1": "Hello world", "text2": "Hello there world"}
Response: {"similarity": 0.647, "additions": 6, "deletions": 0, "diffs": [...]}
Price: $0.001 USDC
```

### /convert-doc — Format Conversion
Markdown to HTML to plain text.
```
POST /x402s/convert-doc
Body: {"input": "# Hello\n**bold**", "from_format": "markdown", "to_format": "html"}
Response: {"output": "<h1>Hello</h1><p><strong>bold</strong></p>"}
Price: $0.002 USDC
```

## Payment
x402 protocol — USDC on Base.
