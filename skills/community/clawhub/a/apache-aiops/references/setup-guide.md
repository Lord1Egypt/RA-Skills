# Setup

Install from local source with `uv sync --dev`. Ensure `apachectl` is on `PATH`, or set the operator-trusted `apachectl_bin` path in `~/.apache-aiops/config.yaml`. Run `uv run apache-aiops init` for a basic local target; include a health URL if Apache serves one. An optional `status_url` should point to a restricted `/server-status?auto`, and `error_log` and `access_log` are absolute operator-selected files. `access-status` parses only common/combined access log formats and never returns raw paths, IPs or headers. Run `uv run apache-aiops doctor` and `uv run apache-aiops diagnose`.

The process account needs read permission for Apache configuration and the selected error/access logs, and permission for graceful reload if used. Do not add a URL containing credentials. The tool does not install Apache, enable `mod_status`, or edit configuration.
