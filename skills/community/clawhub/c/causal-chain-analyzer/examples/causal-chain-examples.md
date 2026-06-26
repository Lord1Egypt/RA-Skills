# Causal Chain Analysis - Real-World Examples

Comprehensive examples of causal chain analysis across different domains, demonstrating how to identify root causes, trace effects, and understand system dependencies.

## 1. IT Debugging - Infrastructure Failure Chain

### Scenario
A web application experiences a cascading failure starting from a power supply issue. We need to trace the complete impact chain.

### Graph Schema

**Nodes:**
- `PowerSupply_1` (Hardware component)
- `Server_A` (Physical server)
- `DatabaseService` (Database instance)
- `CacheService` (Redis cache)
- `APIGateway` (API entry point)
- `UserAuthService` (Authentication service)
- `Dashboard` (Frontend service)
- `UserSessions` (Session data)

**Relationships (Causal):**
```
PowerSupply_1 --causes--> Server_A (weight: 0.95, confidence: 0.99)
Server_A --leads_to--> DatabaseService (weight: 0.9, confidence: 0.95)
Server_A --leads_to--> CacheService (weight: 0.85, confidence: 0.90)
DatabaseService --results_in--> APIGateway (weight: 0.8, confidence: 0.85)
CacheService --propagates_to--> APIGateway (weight: 0.7, confidence: 0.80)
APIGateway --triggers--> UserAuthService (weight: 0.95, confidence: 0.98)
UserAuthService --depends_on--> UserSessions (weight: 0.99, confidence: 0.99)
UserAuthService --leads_to--> Dashboard (weight: 0.9, confidence: 0.95)
```

### Analysis Queries

#### Query 1: Root Cause Analysis
**Question:** "What caused the Dashboard to go down?"

**Analysis:**
```
find_root_causes(target="Dashboard")

Traversal (backward):
Dashboard ← UserAuthService ← APIGateway ← (DatabaseService | CacheService) ← Server_A ← PowerSupply_1

Root causes: [PowerSupply_1]
Chain depth: 5 hops
Confidence score: 0.95 * 0.9 * 0.8 * 0.9 = 0.6156
```

**Result:**
```json
{
  "target": "Dashboard",
  "root_causes": [
    {
      "node": "PowerSupply_1",
      "type": "hardware_failure",
      "distance": 5,
      "confidence": 0.6156,
      "causal_path": ["PowerSupply_1", "Server_A", "DatabaseService", "APIGateway", "UserAuthService", "Dashboard"]
    }
  ],
  "immediate_causes": ["UserAuthService"],
  "chain_depth": 5,
  "affected_nodes": 6
}
```

#### Query 2: Effect Propagation
**Question:** "What was affected by the Server_A failure?"

**Analysis:**
```
trace_effects(source="Server_A")

Forward traversal:
Server_A → DatabaseService → APIGateway
         → CacheService  → APIGateway
APIGateway → UserAuthService → UserSessions
                           → Dashboard

Effects: [DatabaseService, CacheService, APIGateway, UserAuthService, UserSessions, Dashboard]
Propagation depth: 3 levels
Impact breadth: 2 (initial branches from Server_A)
```

**Result:**
```json
{
  "source": "Server_A",
  "direct_effects": ["DatabaseService", "CacheService"],
  "all_effects": ["DatabaseService", "CacheService", "APIGateway", "UserAuthService", "UserSessions", "Dashboard"],
  "propagation_paths": [
    ["Server_A", "DatabaseService", "APIGateway"],
    ["Server_A", "DatabaseService", "APIGateway", "UserAuthService"],
    ["Server_A", "DatabaseService", "APIGateway", "UserAuthService", "Dashboard"],
    ["Server_A", "CacheService", "APIGateway"],
    ["Server_A", "CacheService", "APIGateway", "UserAuthService"],
    ["Server_A", "CacheService", "APIGateway", "UserAuthService", "Dashboard"]
  ],
  "total_affected": 6,
  "max_propagation_depth": 4
}
```

#### Query 3: Impact Analysis with Confidence Filtering
**Question:** "Which are the most critical impact paths?"

**Analysis:**
```
trace_effects_ranked(source="Server_A", confidence_threshold=0.75)

Rank chains by cumulative confidence:
1. Server_A → DatabaseService → APIGateway: 0.9 * 0.8 = 0.72
2. Server_A → CacheService → APIGateway: 0.85 * 0.7 = 0.595 (filtered - below 0.75)

High-confidence path selected
```

**Result:**
```json
{
  "source": "Server_A",
  "confidence_threshold": 0.75,
  "ranked_paths": [
    {
      "path": ["Server_A", "DatabaseService", "APIGateway"],
      "cumulative_confidence": 0.72,
      "risk_level": "MEDIUM"
    }
  ],
  "filtered_low_confidence": 2,
  "critical_path": ["Server_A", "DatabaseService", "APIGateway", "UserAuthService", "Dashboard"]
}
```

---

## 2. Root Cause Analysis - Medical Incident

### Scenario
A patient developed a serious complication post-surgery. Analyze what chain of events led to the complication.

### Graph Schema

**Nodes:**
- `Surgery_Procedure` (Surgical intervention)
- `Anesthesia_Complication` (Drug reaction)
- `BloodPressureDrop` (Vital sign issue)
- `InsufficientOxygenation` (Physiological state)
- `OrganDamage_Heart` (Organ impact)
- `CardiacArrhythmia` (Heart rhythm issue)
- `PatientCritical` (Overall patient status)

**Relationships:**
```
Surgery_Procedure --triggers--> Anesthesia_Complication (confidence: 0.85)
Anesthesia_Complication --leads_to--> BloodPressureDrop (confidence: 0.92)
BloodPressureDrop --results_in--> InsufficientOxygenation (confidence: 0.96)
InsufficientOxygenation --causes--> OrganDamage_Heart (confidence: 0.89)
OrganDamage_Heart --leads_to--> CardiacArrhythmia (confidence: 0.94)
CardiacArrhythmia --propagates_to--> PatientCritical (confidence: 0.97)
```

### Analysis Query

**Question:** "What was the root cause of the patient's critical condition?"

**Analysis:**
```
find_root_causes(
  target="PatientCritical",
  algorithm="DFS",
  calculate_confidence=true
)

Backward chain:
PatientCritical ← CardiacArrhythmia ← OrganDamage_Heart ← 
InsufficientOxygenation ← BloodPressureDrop ← Anesthesia_Complication ← Surgery_Procedure

Root cause: Surgery_Procedure
Confidence product: 0.97 * 0.94 * 0.89 * 0.96 * 0.92 * 0.85 = 0.6156
```

**Result:**
```json
{
  "target": "PatientCritical",
  "root_cause": {
    "node": "Surgery_Procedure",
    "severity": "HIGH",
    "confidence": 0.6156
  },
  "contributing_factors": ["Anesthesia_Complication", "BloodPressureDrop"],
  "causal_chain": [
    "Surgery_Procedure",
    "Anesthesia_Complication",
    "BloodPressureDrop",
    "InsufficientOxygenation",
    "OrganDamage_Heart",
    "CardiacArrhythmia",
    "PatientCritical"
  ],
  "intervention_points": ["Anesthesia_Complication", "BloodPressureDrop"],
  "recommendation": "Improve anesthesia protocols and monitoring"
}
```

---

## 3. Dependency Tracing - Microservices Architecture

### Scenario
A microservices application experiences degraded performance. Trace service dependencies to identify the bottleneck.

### Graph Schema

**Services:**
- `UserService`
- `ProductService`
- `OrderService`
- `PaymentService`
- `InventoryService`
- `NotificationService`
- `APIGateway`

**Dependencies (Causal/Functional):**
```
APIGateway --depends_on--> UserService (latency: 50ms)
APIGateway --depends_on--> ProductService (latency: 100ms)
OrderService --depends_on--> UserService (latency: 30ms)
OrderService --depends_on--> ProductService (latency: 80ms)
OrderService --depends_on--> InventoryService (latency: 120ms)
PaymentService --depends_on--> OrderService (latency: 200ms)
InventoryService --depends_on--> ProductService (latency: 90ms)
NotificationService --depends_on--> OrderService (latency: 50ms)
```

### Analysis Queries

#### Query: Find Services Affected by ProductService Degradation

**Question:** "If ProductService becomes slow, which services are impacted?"

**Analysis:**
```
trace_effects(
  source="ProductService",
  relationship_type="depends_on",
  direction="reverse"
)

Services that depend on ProductService:
- APIGateway (direct)
- OrderService (direct)
- InventoryService (direct)
- PaymentService (via OrderService)
- NotificationService (via OrderService)
```

**Result:**
```json
{
  "degraded_service": "ProductService",
  "direct_dependents": ["APIGateway", "OrderService", "InventoryService"],
  "indirect_dependents": ["PaymentService", "NotificationService"],
  "critical_path": ["ProductService", "OrderService", "PaymentService"],
  "affected_services_count": 5,
  "recommended_action": "Scale ProductService or optimize queries"
}
```

#### Query: Chain Analysis for Payment Processing

**Question:** "What is the full dependency chain for payments?"

**Analysis:**
```
analyze_chain_structure(
  source="PaymentService",
  direction="backward"
)

Dependency chain (what PaymentService depends on):
PaymentService → OrderService → ProductService
             → OrderService → UserService
             → OrderService → InventoryService
```

---

## 4. Risk Analysis - Security Threat Propagation

### Scenario
A security vulnerability is discovered. Analyze potential propagation paths to understand impact.

### Graph Schema

**Vulnerabilities & Systems:**
- `SQLInjectionVulnerability`
- `UserDatabase`
- `CustomerData`
- `AuthenticationSystem`
- `AdminPanel`
- `BackupSystem`

**Threat Propagation:**
```
SQLInjectionVulnerability --exploits--> UserDatabase (severity: CRITICAL)
UserDatabase --exposes--> CustomerData (severity: HIGH)
UserDatabase --compromises--> AuthenticationSystem (severity: CRITICAL)
AuthenticationSystem --leads_to--> AdminPanel (severity: CRITICAL)
AuthenticationSystem --leads_to--> BackupSystem (severity: HIGH)
AdminPanel --can_access--> BackupSystem (severity: CRITICAL)
```

### Analysis Query

**Question:** "What is the full blast radius of this vulnerability?"

**Analysis:**
```
trace_effects(
  source="SQLInjectionVulnerability",
  algorithm="BFS",
  include_severity=true
)

Level 0: SQLInjectionVulnerability
Level 1: UserDatabase (CRITICAL)
Level 2: CustomerData (HIGH), AuthenticationSystem (CRITICAL)
Level 3: AdminPanel (CRITICAL), BackupSystem (HIGH)
```

**Result:**
```json
{
  "vulnerability": "SQLInjectionVulnerability",
  "blast_radius": {
    "critical_assets_at_risk": ["AuthenticationSystem", "AdminPanel", "BackupSystem"],
    "sensitive_data_exposed": ["CustomerData"],
    "total_affected_systems": 6,
    "propagation_levels": 3
  },
  "risk_score": 0.92,
  "remediation_priority": [
    {"system": "UserDatabase", "action": "patch", "priority": 1},
    {"system": "AuthenticationSystem", "action": "rotate_credentials", "priority": 2},
    {"system": "AdminPanel", "action": "restrict_access", "priority": 3}
  ]
}
```

---

## 5. Event Propagation - Workflow Execution

### Scenario
A business workflow progresses through multiple steps with branching logic. Analyze how an event in one step affects downstream steps.

### Graph Schema

**Workflow Steps:**
- `OrderCreated`
- `PaymentProcessed` / `PaymentFailed`
- `InventoryReserved` / `InventoryUnavailable`
- `ShippingScheduled` / `BackorderCreated`
- `CustomerNotified`
- `TransactionClosed`

**Process Flow:**
```
OrderCreated --leads_to--> PaymentProcessed (probability: 0.95)
OrderCreated --leads_to--> PaymentFailed (probability: 0.05)

PaymentProcessed --leads_to--> InventoryReserved (probability: 0.90)
PaymentProcessed --leads_to--> InventoryUnavailable (probability: 0.10)

InventoryReserved --leads_to--> ShippingScheduled (probability: 0.99)
InventoryUnavailable --leads_to--> BackorderCreated (probability: 1.0)

ShippingScheduled --leads_to--> CustomerNotified (probability: 0.98)
BackorderCreated --leads_to--> CustomerNotified (probability: 1.0)

CustomerNotified --leads_to--> TransactionClosed (probability: 0.95)
PaymentFailed --leads_to--> TransactionClosed (probability: 1.0)
```

### Analysis Queries

#### Query 1: All Possible Outcomes
**Question:** "What are all possible end states from a single order?"

**Analysis:**
```
find_all_paths(
  source="OrderCreated",
  destination="TransactionClosed"
)

Paths with probabilities:
1. OrderCreated → PaymentProcessed → InventoryReserved → ShippingScheduled → CustomerNotified → TransactionClosed
   Probability: 0.95 * 0.90 * 0.99 * 0.98 * 0.95 = 0.794
   
2. OrderCreated → PaymentProcessed → InventoryUnavailable → BackorderCreated → CustomerNotified → TransactionClosed
   Probability: 0.95 * 0.10 * 1.0 * 1.0 * 0.95 = 0.0903
   
3. OrderCreated → PaymentFailed → TransactionClosed
   Probability: 0.05 * 1.0 = 0.05
```

#### Query 2: Critical Path
**Question:** "What is the most likely success path?"

**Analysis:**
```
find_critical_path(
  source="OrderCreated",
  destination="TransactionClosed",
  metric="probability"
)

Critical path: OrderCreated → PaymentProcessed → InventoryReserved → ShippingScheduled → CustomerNotified → TransactionClosed
Probability: 0.794 (79.4%)
```

---

## 6. Organizational Impact - Decision Consequences

### Scenario
A company makes a strategic decision. Analyze the cascading organizational impacts.

### Graph Schema

**Decision & Impacts:**
- `CutSoftwareBudget` (Decision)
- `ReducedDeveloperHeadcount`
- `SlowerFeatureDevelopment`
- `IncreasedTechnicalDebt`
- `ProductQualityDegradation`
- `CustomerChurn`
- `RevenueDecline`
- `CompanyValuationDrop`
- `InvestorConfidenceLoss`

**Causal Relationships:**
```
CutSoftwareBudget --leads_to--> ReducedDeveloperHeadcount (confidence: 0.99)
ReducedDeveloperHeadcount --leads_to--> SlowerFeatureDevelopment (confidence: 0.95)
SlowerFeatureDevelopment --results_in--> IncreaseedTechnicalDebt (confidence: 0.90)
IncreaseedTechnicalDebt --contributes_to--> ProductQualityDegradation (confidence: 0.85)
ProductQualityDegradation --leads_to--> CustomerChurn (confidence: 0.80)
CustomerChurn --results_in--> RevenueDecline (confidence: 0.95)
RevenueDecline --leads_to--> CompanyValuationDrop (confidence: 0.90)
CompanyValuationDrop --propagates_to--> InvestorConfidenceLoss (confidence: 0.88)
```

### Analysis Query

**Question:** "What are all the downstream consequences of cutting the software budget?"

**Analysis:**
```
trace_effects(
  source="CutSoftwareBudget",
  include_confidence_scores=true,
  include_severity=true
)

Direct effects: [ReducedDeveloperHeadcount]
Indirect effects: [SlowerFeatureDevelopment, IncreaseedTechnicalDebt, ProductQualityDegradation]
Ultimate impact: [CompanyValuationDrop, InvestorConfidenceLoss]
Total affected areas: 8
```

**Result:**
```json
{
  "decision": "CutSoftwareBudget",
  "impact_chain": {
    "immediate": ["ReducedDeveloperHeadcount"],
    "short_term": ["SlowerFeatureDevelopment"],
    "medium_term": ["IncreaseedTechnicalDebt", "ProductQualityDegradation"],
    "long_term": ["CustomerChurn", "RevenueDecline"],
    "strategic": ["CompanyValuationDrop", "InvestorConfidenceLoss"]
  },
  "cumulative_confidence": 0.5886,
  "warning": "Cutting software budget leads to chain reaction of negative consequences",
  "recommendation": "Consider alternative cost reduction strategies"
}
```

---

## Common Analysis Patterns

### Pattern 1: Root Cause Analysis (Backward Traversal)
Find all nodes with no incoming edges for a given target:
```python
def find_root_causes(graph, target):
    visited = set()
    roots = []
    
    def dfs_backward(node):
        if node in visited:
            return
        visited.add(node)
        
        incoming = graph.get_incoming_edges(node)
        if not incoming:
            roots.append(node)  # No incoming edges = root cause
        else:
            for source, _ in incoming:
                dfs_backward(source)
    
    dfs_backward(target)
    return roots
```

### Pattern 2: Effect Tracing (Forward Traversal)
Find all affected nodes from a given source:
```python
def trace_effects(graph, source):
    visited = set()
    effects = []
    queue = [source]
    
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        
        outgoing = graph.get_outgoing_edges(node)
        for target, edge_data in outgoing:
            effects.append(target)
            queue.append(target)
    
    return effects
```

### Pattern 3: Confidence-Based Filtering
Filter paths by cumulative confidence:
```python
def filter_by_confidence(graph, paths, threshold):
    results = []
    
    for path in paths:
        confidence = 1.0
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i+1])
            confidence *= edge.get('confidence', 1.0)
        
        if confidence >= threshold:
            results.append((path, confidence))
    
    return sorted(results, key=lambda x: x[1], reverse=True)
```

---

**Causal Chain Analysis is essential for:**
- Root cause analysis and incident response
- Impact assessment and risk management
- System debugging and optimization
- Decision impact analysis and planning


