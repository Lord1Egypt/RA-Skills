# IBM ACE Deployment

## BAR File Overview

A BAR (Broker Archive) file is the deployment artifact for ACE. It is a ZIP file containing:
- Compiled message flow bytecode (`.cmf` files)
- ESQL compiled classes
- Message schemas (XSD, DFDL)
- Resources and configuration
- `META-INF/MANIFEST.MF` — deployment metadata

BAR files are the **only** way to deploy flows to a running integration server.

---

## Building a BAR File

### From ACE Toolkit
1. Right-click application project → **New > BAR File**
2. Select artifacts to include
3. Click **Build and Save**
4. BAR saved to project root or custom path

### From CLI
```bash
# Source ACE environment first
source /opt/ibm/ace-12.0.x.x/server/bin/mqsiprofile

# Create BAR for a single application
mqsibar -c -a /path/to/output/MyApp.bar \
  -w /path/to/workspace \
  -k MyApplicationProject

# Include multiple projects (application + library)
mqsibar -c -a /path/to/output/MyApp.bar \
  -w /path/to/workspace \
  -k MyApplicationProject \
  -k MySharedLibrary
```

### From Maven (CI/CD)
```xml
<plugin>
  <groupId>com.ibm.ace</groupId>
  <artifactId>ibm-ace-maven-plugin</artifactId>
  <version>12.0.x.x</version>
  <executions>
    <execution>
      <phase>package</phase>
      <goals><goal>createbar</goal></goals>
      <configuration>
        <applicationName>MyApplicationProject</applicationName>
      </configuration>
    </execution>
  </executions>
</plugin>
```

---

## BAR Override Properties

Override deployment-time properties (endpoints, credentials, etc.) without rebuilding:

### Generate override properties template
```bash
mqsireadbar -b MyApp.bar -o overrides.properties
```

### overrides.properties format
```properties
# Node properties: FlowName#NodeLabel.propertyName=value
MyFlow#MQInputNode.queueName=PROD.INPUT.QUEUE
MyFlow#HTTPInputNode.path=/api/v1/payments
MyFlow#ComputeNode.dataSourceName=ProdDB
```

### Apply overrides
```bash
mqsiapplybaroverride -b MyApp.bar -p overrides.properties
```

---

## Deploying to an Integration Node

### Basic deployment
```bash
mqsideploy NODENAME \
  -e SERVERNAME \
  -a /path/to/MyApp.bar \
  -w 60
```

### Incremental deployment (add to existing)
```bash
mqsideploy NODENAME \
  -e SERVERNAME \
  -a /path/to/MyApp.bar \
  -m                      # merge with existing deployments
  -w 60
```

### Full replacement (delete all, then deploy)
```bash
# Step 1: Remove existing
mqsideploy NODENAME -e SERVERNAME -d -w 30

# Step 2: Deploy new BAR
mqsideploy NODENAME -e SERVERNAME -a /path/to/MyApp.bar -w 60
```

### Delta deployment (only changed flows)
```bash
mqsideploy NODENAME \
  -e SERVERNAME \
  -a /path/to/MyApp.bar \
  -w 60 \
  -f                      # force redeploy even if unchanged
```

---

## Deploying to Stand-Alone Integration Server

### Via REST API
```bash
# Deploy
curl -X POST http://localhost:7600/apiv2/deploy \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @MyApp.bar

# Check deployed applications
curl http://localhost:7600/apiv2/servers/default/applications

# Undeploy
curl -X DELETE \
  http://localhost:7600/apiv2/servers/default/applications/MyApplicationProject
```

### Via filesystem (Docker)
Mount BAR files to the server's `run/` directory:
```bash
docker run --rm \
  -v /path/to/MyApp.bar:/home/aceuser/ace-server/run/MyApp.bar \
  ibmcom/ace:12.0.x.x
```

---

## Docker / Container Deployment

### Official ACE Docker image
```dockerfile
FROM ibmcom/ace:12.0.x.x

# Copy BAR file
COPY MyApp.bar /home/aceuser/ace-server/run/

# Optional: server.conf.yaml
COPY server.conf.yaml /home/aceuser/ace-server/

EXPOSE 7600 7800
```

### Docker Compose
```yaml
version: '3.8'
services:
  ace-server:
    image: ibmcom/ace:12.0.x.x
    ports:
      - "7600:7600"   # Admin REST API
      - "7800:7800"   # HTTP listener
    volumes:
      - ./MyApp.bar:/home/aceuser/ace-server/run/MyApp.bar
      - ./server.conf.yaml:/home/aceuser/ace-server/server.conf.yaml
    environment:
      - LICENSE=accept
```

---

## CI/CD Pipeline Pattern

```yaml
# Example GitHub Actions / Jenkins pipeline
stages:
  - build
  - test
  - deploy

build-bar:
  script:
    - source /opt/ibm/ace-12/server/bin/mqsiprofile
    - mqsibar -c -a target/MyApp.bar -w . -k MyApplicationProject

apply-overrides:
  script:
    - mqsiapplybaroverride -b target/MyApp.bar -p config/${ENV}.properties

deploy-to-server:
  script:
    - mqsideploy ${ACE_NODE} -e ${ACE_SERVER} -a target/MyApp.bar -w 120
```

---

## Deployment Verification

### Check deployment status
```bash
mqsilist NODENAME -e SERVERNAME -d
```

### Expected output
```
BIP8071I: Successful command completion.
  Application: MyApplicationProject
    Message flow: MyFlow (running)
    Message flow: AnotherFlow (running)
```

### Check via REST API
```bash
curl http://localhost:7600/apiv2/servers/default/applications/MyApplicationProject/messageflows
```

---

## Configuration Service (Policy-Based Config)

For environment-specific configuration without BAR rebuilds:

```bash
# Create policy project in workspace
# PolicyProject/MyMQPolicy.policyxml

# Deploy policy project as a BAR
mqsibar -c -a Policies.bar -w . -k PolicyProject
mqsideploy NODENAME -e SERVERNAME -a Policies.bar
```

Policy XML example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<policies>
  <policy policyType="MQEndpoint" policyName="MyMQPolicy" policyTemplate="MQEndpoint">
    <queueManagerHostname>mq-host</queueManagerHostname>
    <listenerPortNumber>1414</listenerPortNumber>
    <queueManagerName>QMGR</queueManagerName>
  </policy>
</policies>
```

Reference in flow node: `{PolicyProjectName}:MyMQPolicy`

---

## Common Deployment Errors

| Error | Cause | Fix |
|-------|-------|-----|
| BIP2230E: Flow already exists | Duplicate deployment | Use `-m` (merge) or delete first |
| BIP3701E: Queue manager not available | MQ not running | Start MQ before deploying |
| BIP1009E: ESQL compilation error | Syntax error in ESQL | Fix and rebuild BAR |
| BIP2628E: Node class not found | Missing node library | Add required JAR to BAR |
| Timeout waiting for deployment | Slow server or large BAR | Increase `-w` timeout |
