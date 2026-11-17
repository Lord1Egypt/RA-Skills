# Capabilities

Sixteen DNS reads: `bind_status`, `bind_config_check`, `bind_zone_status`, `bind_dnssec_validation`, `bind_dnssec_zone_status`, `bind_managed_keys_status`, `bind_serve_stale_status`, `bind_show_zone`, `bind_query`, `bind_query_server`, `bind_compare_soa`, `bind_diagnose_zone`, `bind_fetch_limits`, `bind_security_roots`, `bind_tcp_timeouts`, `bind_signing_status`. Five writes: `bind_reload_zone`, `bind_refresh_zone`, `bind_flush_name`, high-risk `bind_retransfer_zone`, and `bind_notify_zone`. Two common governance tools: `undo_list`, `undo_apply`.

Unsupported in this slice: zone-file editing, dynamic updates, full-cache flush, DNSSEC key rollover and service restarts. Request missing features with a BIND version and real command output in an issue or PR.
