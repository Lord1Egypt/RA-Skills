# Integration Guide

## Standalone Python

```python
from roundtable import RoundtableCore

core = RoundtableCore()
result = core.create_discussion(topic="...", participants=[...])
```

## Generic Adapter (error-safe)

```python
from roundtable.adapters.generic import Roundtable

rt = Roundtable(db_path="/tmp/rt.db")
result = rt.init(topic="...", participants=[...])
# Errors returned as {"error": "..."}, never raised
```

## Hermes Agent

The Hermes adapter auto-discovers and registers when Hermes imports it.

### Profile config

```yaml
toolsets:
  - roundtable
```

### Manual registration

```python
from tools.registry import registry
from roundtable.adapters.hermes import register_roundtable_tools

register_roundtable_tools(registry)
```

### DB path

By default, uses `~/.roundtable/roundtable.db`. To use Hermes' home:

```bash
export ROUNDTABLE_DB=~/.hermes/roundtable.db
```

## LangChain (future)

```python
# Placeholder for LangChain tool adapter
from roundtable.adapters.langchain import get_roundtable_tools
tools = get_roundtable_tools()
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ROUNDTABLE_DB` | SQLite database path | `~/.roundtable/roundtable.db` |
