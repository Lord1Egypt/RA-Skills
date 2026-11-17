# Cross-Agent Treaty Broker

A lightweight, consent-first protocol for negotiating and recording bilateral treaties between autonomous AI agents.

## Quick Start

```bash
# Initialize
python scripts/catcb.py init

# Propose a treaty to another agent
python scripts/catcb.py propose --to <agent_id>

# Review the proposal
python scripts/catcb.py review <treaty_id>

# Sign with human approval
python scripts/catcb.py sign <treaty_id> --signer <human_id>

# List all treaties
python scripts/catcb.py list
```

## Documentation

- [Quick Start Guide](references/quick-start.md)
- [JSON Schema](references/treaty-json-schema.json)

## Examples

- [Data Sharing Treaty](examples/data-sharing-treaty.json)

## License

MIT