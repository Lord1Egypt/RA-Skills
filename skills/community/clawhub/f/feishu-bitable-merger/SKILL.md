---
name: feishu-bitable-merger
description: Feishu Bitable Merger - Merge multiple Feishu bitable data into one table
metadata:
  openclaw:
    requires:
      bins: []
---

# Feishu Bitable Merger

Merge multiple Feishu bitable data into one target table, features:
- Auto match same field names
- Preserve original data format
- Support incremental merge
- Support field mapping configuration
- Support deduplication after merge

## Usage

```bash
# Merge multiple tables to target
openclaw feishu-bitable-merger merge --source "https://example1.com/base/xxx" "https://example2.com/base/xxx" --target "https://example.com/base/yyy"

# Merge with field mapping
openclaw feishu-bitable-merger merge --source "source1" "source2" --target "target" --map "oldField:newField"
```

## Configuration

Required Feishu API permissions:
- `bitable:app:read`
- `bitable:app:write`
- `bitable:record:read`
- `bitable:record:write`
