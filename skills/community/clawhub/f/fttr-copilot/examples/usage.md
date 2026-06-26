# Usage Examples

List bound devices:

```bash
node src/cli.js list_my_devices
```

Return help:

```bash
node src/cli.js --help
```

Get device detail:

```bash
node src/cli.js get_device_detail '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Get online status:

```bash
node src/cli.js get_device_online_status '{"device_identifier":"客厅主网关"}'
```

Update device alias:

```bash
node src/cli.js update_device_alias '{"device_identifier":"AA:BB:CC:DD:EE:FF","new_alias":"客厅主网关"}'
```

List alerts:

```bash
node src/cli.js list_device_alerts '{"event_type":"ALARM","limit":20}'
```

Get network topology:

```bash
node src/cli.js get_network_topology '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Get station metrics:

```bash
node src/cli.js get_station_stats '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
```

Get network experience:

```bash
node src/cli.js get_network_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Get station RSSI experience:

```bash
node src/cli.js get_station_experience '{"device_identifier":"AA:BB:CC:DD:EE:FF","sta_mac":"11:22:33:44:55:66"}'
```

Get customer-scope stats:

```bash
node src/cli.js get_device_stats
node src/cli.js get_fault_counter
node src/cli.js get_device_load '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Run real-time device commands:

```bash
node src/cli.js get_master_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_slave_gateway_info '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js get_agent_version '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
```

Run diagnosis workflows:

```bash
node src/cli.js diagnose_device_offline '{"device_identifier":"AA:BB:CC:DD:EE:FF"}'
node src/cli.js diagnose_network_slow '{"device_identifier":"AA:BB:CC:DD:EE:FF","symptom":"卧室网慢"}'
node src/cli.js explain_fttrai_copilot_usage '{"user_goal":"排查网慢"}'
```
