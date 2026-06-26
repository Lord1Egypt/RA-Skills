# Usage Examples

List managed devices:

```bash
node src/cli.js list_devices '{"region_code":"440000","online_status":"OFFLINE","limit":20}'
```

Get device detail and status:

```bash
node src/cli.js get_device_detail '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_device_online_status '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Alert operations:

```bash
node src/cli.js list_device_alerts '{"region_code":"440000","event_type":"ALARM","limit":20}'
node src/cli.js get_alert_detail '{"alert_id":"00000000-0000-4000-8000-000000000000"}'
node src/cli.js calculate_alert_number '{"device_identifiers":["AA:BB:CC:DD:EE:FF"]}'
node src/cli.js mark_alerts_as_read '{"alert_ids":["00000000-0000-4000-8000-000000000000"]}'
```

Network tools:

```bash
node src/cli.js get_network_topology '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_stats '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
node src/cli.js get_network_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_station_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
```

Stats and load:

```bash
node src/cli.js get_device_stats '{"region_code":"440000"}'
node src/cli.js get_fault_counter '{"region_code":"440000"}'
node src/cli.js get_device_load '{"device_identifier":"AA:BB:CC:DD:EE:FF","load_type":"basic"}'
```

Real-time query commands:

```bash
node src/cli.js get_master_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_slave_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_agent_version '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Diagnosis workflows:

```bash
node src/cli.js diagnose_device_offline '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_network_slow '{"device_identifier":"AA:BB:CC:DD:EE:FF","symptom":"卧室网慢"}'
node src/cli.js explain_fttrai_copilot_usage '{"user_goal":"排查区域离线"}'
```
