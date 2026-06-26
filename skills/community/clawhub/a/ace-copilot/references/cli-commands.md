# IBM ACE CLI Commands

All commands run from the ACE command console or shell with the ACE environment sourced:
```bash
source /opt/ibm/ace-12.0.x.x/server/bin/mqsiprofile
```

---

## Integration Node Management

### Create Integration Node
```bash
mqsicreatebroker NODENAME \
  -q QMGR_NAME \
  -e SERVICE_USER \
  -a SERVICE_PASSWORD \
  -p 4414              # admin port (default 4414)
```

### Start/Stop Integration Node
```bash
mqsistart NODENAME
mqsistop NODENAME
mqsistop NODENAME -i   # immediate stop (force)
```

### List Integration Nodes
```bash
mqsilist                           # list all nodes on host
mqsilist NODENAME                  # list servers in node
mqsilist NODENAME -e SERVERNAME    # list deployed flows
```

### Change Integration Node Properties
```bash
mqsichangebroker NODENAME \
  -c MAXHEAPSIZE \     # e.g., -c 1024 (MB)
  -u SERVICE_USER
```

### Delete Integration Node
```bash
mqsideletbroker NODENAME
```

---

## Integration Server Management

### Create Integration Server
```bash
mqsicreateexecutiongroup NODENAME -e SERVERNAME
```

### Start/Stop Integration Server
```bash
mqsistartmsgflow NODENAME -e SERVERNAME -m FLOWNAME   # start specific flow
mqsstopmsgflow  NODENAME -e SERVERNAME -m FLOWNAME    # stop specific flow
```

### List Flows in a Server
```bash
mqsilist NODENAME -e SERVERNAME -d   # detailed listing
```

---

## Stand-Alone Integration Server

```bash
# Create and start a stand-alone server
IntegrationServer --name SERVERNAME \
  --work-dir /var/mqsi/work \
  --admin-rest-api 7600

# Or with ACE command:
mqsistart SERVERNAME   # if server.conf.yaml exists in work dir
```

### server.conf.yaml (stand-alone config)
```yaml
BrokerRegistry:
  brokerKeystoreFile: ''
  brokerKeystoreType: ''
  brokerKeystorePass: ''

RestAdminListener:
  port: 7600

Statistics:
  Snapshot:
    publicationOn: 'inactive'
```

---

## BAR File Operations

### Create BAR File
```bash
mqsibar -c \                         # create mode
  -a MyApplication.bar \            # output BAR file
  -w /path/to/workspace \           # workspace directory
  -k MyApplicationProject           # application/library to include
```

### Add to Existing BAR
```bash
mqsibar -a MyApplication.bar \
  -w /path/to/workspace \
  -k AnotherProject
```

### List BAR File Contents
```bash
mqsibar -l -a MyApplication.bar
```

### Apply BAR Override (change properties without rebuild)
```bash
mqsiapplybaroverride \
  -b MyApplication.bar \
  -p override.properties \
  -r                    # read-only check
```

---

## Deployment Commands

### Deploy BAR File to Integration Server
```bash
mqsideploy NODENAME \
  -e SERVERNAME \
  -a /path/to/MyApplication.bar \
  -w 60                            # wait timeout seconds
```

### Undeploy All from Server
```bash
mqsideploy NODENAME \
  -e SERVERNAME \
  -d                               # delete all deployed flows
```

### Deploy to Stand-Alone Server (REST API)
```bash
curl -X POST http://localhost:7600/apiv2/deploy \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @MyApplication.bar
```

---

## Trace and Diagnostic Commands

### Enable User Trace
```bash
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l debug \              # trace level: none, normal, debug
  -u                      # user trace (application level)
```

### Enable Service Trace
```bash
mqsichangetrace NODENAME \
  -e SERVERNAME \
  -l debug \
  -s                      # service trace (internal ACE)
```

### Read Trace
```bash
mqsireadlog NODENAME \
  -e SERVERNAME \
  -u                       # user trace
  -o /tmp/trace.txt        # output file
```

### Format Trace Output
```bash
mqsiformatlog -f /tmp/trace.txt | more
```

### Capture Diagnostic Data
```bash
mqsicapture NODENAME        # create diagnostic zip
```

---

## Security Commands

### Create Security Profile
```bash
mqsicreatecredentials NODENAME \
  -c MQ \
  -o QMGR_NAME \
  -u mquser \
  -p mqpassword
```

### Set Policy
```bash
mqsisetdbparms NODENAME \
  -n jdbc::myDataSource \
  -u dbuser \
  -p dbpassword
```

---

## Useful Utility Commands

### Check Node Version
```bash
mqsiservice NODENAME -v
```

### Report Integration Node Status
```bash
mqsireportbroker NODENAME
```

### Verify BAR File
```bash
mqsibar -v -a MyApplication.bar   # validate BAR
```

### Import ACE Project (CLI)
```bash
# Import from ZIP into workspace
mqsiimportproject -w /workspace -z myproject.zip
```

---

## Environment Setup

```bash
# Source ACE environment (required before any mqsi* command)
source /opt/ibm/ace-12.0.x.x/server/bin/mqsiprofile

# Verify environment
mqsiservice --version

# Common environment variables
export MQSI_WORKPATH=/var/mqsi
export MQSI_REGISTRY=/var/mqsi/registry
```

---

## Return Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Warning |
| 2 | Error |
| 71 | Node not found |
| 72 | Server not found |
| 73 | Flow not found |

---

## ACE REST Admin API (v2)

Base URL: `http://hostname:7600/apiv2`

| Method | Path | Action |
|--------|------|--------|
| GET | `/` | Node info |
| GET | `/servers` | List integration servers |
| GET | `/servers/{name}/applications` | List deployed applications |
| POST | `/deploy` | Deploy BAR file |
| DELETE | `/servers/{name}/applications/{app}` | Undeploy application |
| GET | `/servers/{name}/statistics/snapshot` | Flow statistics |
