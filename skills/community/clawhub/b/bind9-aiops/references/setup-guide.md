# Setup

Install from local source with `uv sync --dev`. Install BIND 9 utilities so `rndc`, `named-checkconf` and `dig` are on `PATH`, or set their trusted paths in `config.yaml`. Run `uv run bind9-aiops init` for a basic local target. An existing config may set `rndc_config` and `named_config` paths. Give the process account only the access required for intended RNDC commands; reload, refresh and cache flush can affect live DNS. Run `uv run bind9-aiops doctor` and `uv run bind9-aiops diagnose example.org`.

For a remote DNS service, this first slice assumes `rndc` is configured by the operator and can reach it. It does not provision RNDC keys, open a remote control channel, or change BIND configuration.
