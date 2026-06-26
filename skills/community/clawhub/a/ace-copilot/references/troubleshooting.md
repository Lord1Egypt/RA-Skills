# IBM ACE Troubleshooting

## Diagnostic Hierarchy

1. **Check integration node/server status** — is it running?
2. **Check application/flow status** — is the flow deployed and running?
3. **Enable user trace** — capture message-level diagnostics
4. **Enable service trace** — capture ACE internal diagnostics (last resort)
5. **Read system logs** — OS syslog, ACE event log
6. **Capture diagnostic data** — `mqsicapture` for IBM support

---

## Quick Status Checks

```bash
# Is the integration node running?
mqsilist NODENAME

# List all flows and their status
mqsilist NODENAME -e SERVERNAME -d

# Check via REST API (stand-alone server)
curl http://localhost:7600/apiv2/servers/default/health
curl http://localhost:7600/apiv2/servers/default/applications
```

---

## User Trace

User trace captures the message content and path at each node in a flow. Use this for debugging transformation logic and routing.

### Enable user trace for a server
```bash
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l debug \
  -u
```

### Enable user trace for a specific flow only
```bash
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l debug \
  -u \
  -m FlowName
```

### Send test message and reproduce issue, then read trace
```bash
mqsireadlog NODENAME \
  -e SERVERNAME \
  -u \
  -o /tmp/user_trace.txt

# Format for readability
mqsiformatlog -f /tmp/user_trace.txt | more
```

### Disable user trace (always do this when done!)
```bash
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l none \
  -u
```

---

## Service Trace

Service trace captures ACE internal processing — use only when directed by IBM Support or for deep infrastructure issues.

```bash
# Enable service trace
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l debug \
  -s

# Read service trace
mqsireadlog NODENAME -e SERVERNAME -s -o /tmp/service_trace.txt

# Disable service trace
mqsichangetrace NODENAME -e SERVERNAME -l none -s
```

**Warning:** Service trace generates large volumes of data and impacts performance. Only use briefly.

---

## Log File Locations

| Log | Location |
|-----|----------|
| ACE system log | `/var/mqsi/log/` |
| Integration node log | `/var/mqsi/registry/NODENAME/log/` |
| User trace | Retrieved via `mqsireadlog` |
| Service trace | Retrieved via `mqsireadlog -s` |
| Docker container logs | `docker logs container_name` |
| Event log (Windows) | Windows Event Viewer → Application |

---

## Common Errors and Fixes

### Flow Not Starting

**Symptom:** Flow shows as "stopped" after deployment

```bash
# Check flow status
mqsilist NODENAME -e SERVERNAME -d -m FlowName

# Try starting the flow
mqsistartmsgflow NODENAME -e SERVERNAME -m FlowName

# Check user trace for startup errors
mqsichangetrace NODENAME -e SERVERNAME -l debug -u
```

**Common causes:**
- MQ queue/queue manager not available
- HTTP listener port conflict
- Missing credentials (database, MQ)
- ESQL runtime error on startup

---

### BIP2230E: Flow Already Exists

```bash
# Undeploy existing first
mqsideploy NODENAME -e SERVERNAME -d -w 30

# Then redeploy
mqsideploy NODENAME -e SERVERNAME -a MyApp.bar -w 60
```

---

### BIP1009E: ESQL Compilation Error

Check the error message for line/column number, then:
1. Open the `.esql` file in ACE Toolkit
2. Fix the syntax error
3. Rebuild the BAR file
4. Redeploy

Common ESQL mistakes:
- Missing semicolons at end of statements
- Wrong case (`SET` not `set`)
- Referencing non-existent tree path
- Array index out of bounds (check `CARDINALITY()`)

---

### BIP3701E: Queue Manager Not Available

```bash
# Check MQ queue manager status
dspmq -m QMGR_NAME

# Start queue manager if stopped
strmqm QMGR_NAME

# Verify MQ listener is running
runmqlsr -m QMGR_NAME -t TCP -p 1414 &
```

---

### HTTP Input Node Not Receiving Messages

```bash
# Check if HTTP listener is active
netstat -an | grep 7800    # default HTTP port

# Test with curl
curl -v http://localhost:7800/flowpath -d '{"test":"data"}' \
  -H 'Content-Type: application/json'

# Check for port conflict
lsof -i :7800
```

---

### Message Stuck / Not Processing

```bash
# Enable user trace and send a test message
mqsichangetrace NODENAME -e SERVERNAME -l debug -u

# Check for messages on input queue
amqsget INPUT.QUEUE QMGR_NAME

# Read trace to see where message stopped
mqsireadlog NODENAME -e SERVERNAME -u -o /tmp/trace.txt
mqsiformatlog -f /tmp/trace.txt | grep -i "error\|exception\|fail"
```

---

### Database Connection Failures

```bash
# Test ODBC connectivity
mqsitestdsn NODENAME -n DataSourceName

# Re-set credentials
mqsisetdbparms NODENAME -n jdbc::myDataSource -u user -p password

# Check ODBC configuration
cat /etc/odbc.ini | grep -A10 DataSourceName
```

---

### Memory/Performance Issues

```bash
# Check heap usage
mqsireportbroker NODENAME

# Increase heap size
mqsichangebroker NODENAME -c 2048   # 2GB heap

# Check flow statistics
curl http://localhost:7600/apiv2/servers/default/statistics/snapshot

# Identify slow flows via user trace
mqsichangetrace NODENAME -e SERVERNAME -l normal -u
```

---

## Trace Reading Guide

User trace entries look like:

```
2024-01-15 10:23:45.123456  [debug] BIP2539I: Node 'MyFlow.ComputeNode'
  (type 'ComputeNode') in message flow 'MyFlow' caught exception ...
  --- Message Body ---
  <root><value>test</value></root>
```

Key BIP codes in traces:

| BIP Code | Meaning |
|----------|---------|
| BIP2539I | Exception caught in node |
| BIP2230E | Resource not found |
| BIP3701E | MQ error |
| BIP5377W | ESQL runtime warning |
| BIP2268E | ESQL exception |
| BIP4048E | Database error |
| BIP1009E | Compilation error |

---

## Capturing Diagnostics for IBM Support

```bash
# Creates a comprehensive diagnostic zip
mqsicapture NODENAME \
  -e SERVERNAME \
  -o /tmp/ace_diagnostic.zip

# Zip contains:
# - Configuration
# - Recent logs
# - Flow definitions
# - System information
```

---

## Docker Troubleshooting

```bash
# Check container logs
docker logs ace-container

# Execute into container
docker exec -it ace-container /bin/bash

# Inside container: check server status
source /opt/ibm/ace-12.0.x.x/server/bin/mqsiprofile
mqsilist

# Check if work directory has correct permissions
ls -la /home/aceuser/ace-server/

# Restart container
docker restart ace-container
```

---

## Preventive Practices

1. **Always disable trace when done** — trace runs have performance overhead
2. **Monitor error queues** — set up alerts on `SYSTEM.DEAD.LETTER.QUEUE`
3. **Use TryCatch nodes** in flows for graceful error handling
4. **Set flow statistics to 'archive' mode** in production for post-mortem analysis
5. **Keep BAR builds reproducible** — pin dependency versions in workspace
6. **Test deployments in dev/test** before production
