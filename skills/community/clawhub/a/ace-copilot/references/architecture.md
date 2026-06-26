# IBM ACE Architecture

## Runtime Hierarchy

```
Integration Node (Broker)
└── Integration Server (Execution Group)
    └── Message Flows
        └── Nodes (Input → Processing → Output)
```

### Integration Node
- Top-level runtime container (formerly called "broker" in WebSphere Message Broker)
- Manages multiple integration servers
- Hosts the ACE configuration database
- Created with `mqsicreatebroker` / `IntegrationNodeAdministrator`
- Each node has a unique name on the host

### Integration Server
- Execution environment for message flows (formerly "execution group")
- Isolated JVM process within the integration node
- Flows deployed here run independently
- Created with `mqsicreateexecutiongroup`

### Integration Node vs. Stand-Alone Integration Server
- **Node-managed**: Traditional setup — node hosts servers, all managed via node
- **Stand-alone**: Integration server runs without a parent integration node (lighter weight, container-friendly)
- Stand-alone servers are preferred for Docker/Kubernetes deployments

---

## Key Components

### Message Flows
- Directed graphs of connected nodes
- Process messages end-to-end
- Defined in `.msgflow` files in ACE Toolkit
- Deployed in BAR files

### Nodes
- Individual processing units within a flow
- Built-in nodes (MQ, HTTP, Compute, Filter, etc.) + Java/custom nodes
- Connected by terminals (input terminals → output terminals)

### Policies
- Reusable configuration objects (MQ endpoints, JDBC credentials, HTTP endpoints)
- Stored in policy projects
- Referenced by flows using policy descriptors

### ODBC/JDBC Data Sources
- Database connectivity for DatabaseInput/DatabaseRetrieve nodes and ESQL `SELECT` statements
- Configured at the integration node level

---

## Workspace Structure (ACE Toolkit)

```
workspace/
├── ApplicationProject/        # Application container
│   ├── .application           # Application descriptor
│   ├── *.msgflow              # Message flow definitions
│   ├── *.esql                 # ESQL source files
│   ├── *.xsd / *.dfdl.xsd     # Message models
│   └── resources/             # Additional resources
├── LibraryProject/            # Shared library (reusable subflows, schemas)
│   └── *.subflow
├── PolicyProject/             # Policy definitions
│   └── *.policyxml
└── BARFile.bar                # Built deployment artifact
```

### Applications
- Self-contained deployable unit
- References shared libraries
- Contains message flows, ESQL, schemas

### Libraries
- Shared subflows, schemas, ESQL modules reused across applications
- Deployed independently or embedded in BAR

---

## Supported Message Transports

| Transport | Input Node | Output Node |
|-----------|-----------|------------|
| IBM MQ | MQInput | MQOutput |
| HTTP/REST | HTTPInput | HTTPReply / HTTPRequest |
| SOAP/Web Services | SOAPInput | SOAPReply / SOAPRequest |
| File | FileInput | FileOutput |
| Email | EmailInput | — |
| JMS | JMSInput | JMSOutput |
| Kafka | KafkaConsumer | KafkaProducer |
| Database | DatabaseInput | DatabaseOutput |
| Timer | TimeoutNotification | — |

---

## IBM FTM Context

In IBM Financial Transaction Manager (FTM) environments:
- ACE acts as the integration layer between payment systems
- Message flows process SWIFT, ISO 20022, FPS, CHAPS payment messages
- Flows route between MQ queues managed by FTM orchestration
- ESQL transforms payment message formats
- Integration nodes are typically clustered for HA
