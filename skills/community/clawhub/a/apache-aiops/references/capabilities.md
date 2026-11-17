# Capabilities

Fourteen Apache reads: `apache_version`, `apache_build`, `apache_config_check`, `apache_runtime_config`, `apache_config_includes`, `apache_vhosts`, `apache_modules`, `apache_compiled_modules`, `apache_static_directives`, `apache_probe`, `apache_server_status`, `apache_error_log`, `apache_access_status`, `apache_diagnose`. The access summary returns HTTP status codes only, with no raw URLs, IPs or headers; unsupported log formats report `unparsedLines` and `sampleParseComplete: false`. One write: `apache_graceful_reload`. Two common governance tools: `undo_list`, `undo_apply`.

Unsupported in this slice: vhost editing, hard restart, TLS certificate management, mod_status setup and module changes. Request missing capabilities with an Apache version and real command output in an issue or PR.
