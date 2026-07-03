# Business Process Analysis Report Template

## Document Information

| Field | Content |
|------|------|
| Analyzed Process | [Process Name] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |
| Process Owner | [Name + Department] |

---

## 1. Process Overview

### 1.1 Basic Process Attributes

| Attribute | Content |
|------|------|
| Process Name | |
| Process ID | |
| Process Type | Core / Support / Management |
| Trigger Event | |
| Process Output | |
| Involved Departments | |
| Involved Systems | |
| Key SLA/KPI | |
| Reference Documentation | |

### 1.2 SIPOC Overview

| Supplier | Input | Process | Output | Customer |
|----------|-------|---------|--------|----------|
| | | | | |

---

## 2. As-Is Process Analysis

### 2.1 Process Flow Diagram (BPMN 2.0)

[Insert BPMN 2.0 process flow diagram or text description here]

### 2.2 Detailed Process Steps

| Step | Role | Input | Action | Output | System | Time (min) | Wait (min) |
|------|------|------|------|------|------|----------|----------|
| | | | | | | | |

### 2.3 Process Metrics

| Metric | Current Value | Industry Benchmark | Gap |
|------|--------|---------|------|
| Total Process Duration (End-to-End) | | | |
| Value-Added Time (VAT) | | | |
| Non-Value-Added Time | | | |
| Process Efficiency (VAT / Total Duration) | | | |
| First-Pass Yield | | | |
| Rework Rate | | | |
| Unit Cost | | | |
| Error Rate | | | |

### 2.4 Value Stream Analysis

```
Timeline:
|VAT|----Wait----|VAT|-------Wait------|VAT|--Wait--|
0   5           20  25                 50  55     70 (hours)

Value-Added Time (VAT) = 15 hours
Total Lead Time = 70 hours
Process Efficiency = 15/70 = 21.4%
```

---

## 3. Pain Point Analysis

### 3.1 Pain Point Inventory

| Pain Point | Location (Which Step) | Type | Impact | Severity (1-5) | Root Cause |
|------|------------|------|------|-----------|------|
| | | | | | |

### 3.2 Root Cause Analysis (5 Whys / Fishbone)

#### Pain Point X Root Cause Analysis
```
Why 1: [Why does this problem exist?]
Why 2: [Why did Why 1 occur?]
Why 3: [Why did Why 2 occur?]
Why 4: [Why did Why 3 occur?]
Why 5: [Why did Why 4 occur?]
→ Root Cause: [Root cause]
```

### 3.3 Pain Point Quantification

| Pain Point | Annual Occurrences | Loss per Occurrence (Time/¥) | Annual Total Loss |
|------|----------|----------------|---------|
| | | | |
| **Total** | | | ¥[XXX]/year |

---

## 4. To-Be Process Design

### 4.1 Improvement Directions

| Improvement Type | Specific Measures | Affected Pain Points |
|---------|---------|----------|
| **Eliminate** | Remove unnecessary steps | |
| **Simplify** | Simplify complex steps | |
| **Integrate** | Merge related steps | |
| **Automate** | Steps completed automatically by system | |
| **Parallelize** | Steps that can run concurrently | |

### 4.2 To-Be Process Flow Diagram

[Insert To-Be BPMN 2.0 process flow diagram here]

### 4.3 To-Be Metric Forecast

| Metric | As-Is | To-Be | Improvement |
|------|-------|-------|---------|
| Total Process Duration | | | ↓XX% |
| Process Efficiency | | | ↑XX% |
| First-Pass Yield | | | ↑XX% |
| Unit Cost | | | ↓XX% |

### 4.4 Change Impact

| Affected Role | Change | Estimated Resistance | Management Strategy |
|-----------|------|---------|---------|
| | | | |

---

## 5. Implementation Recommendations

### 5.1 Improvement Prioritization

| No. | Improvement Measure | Difficulty | Impact | Priority | Timeline |
|------|---------|------|------|--------|------|
| | | | | | |

### 5.2 Implementation Roadmap

| Phase | Content | Timeline | Dependencies |
|------|------|------|------|
| Quick Wins (0-30 days) | | | |
| Short-Term (1-3 months) | | | |
| Mid-Term (3-6 months) | | | |
| Long-Term (6-12 months) | | | |

---

## 6. Process Monitoring

### 6.1 KPI Definition

| KPI | Definition | Current Value | Target Value | Monitoring Frequency |
|-----|------|--------|--------|---------|
| | | | | |

### 6.2 Continuous Improvement Mechanism
- Process Review Frequency: [Monthly / Quarterly]
- Process Owner Responsibilities:
- Exception Escalation Path:


---

## v1.1.0 New: EventStorming Analysis

### EventStorming Workshop Design
| Phase | Time | Activity | Output |
|------|------|------|------|
| 1. Domain Event Identification | 30 min | Orange sticky notes: all "what happened" | Event Wall |
| 2. Timeline Sequencing | 15 min | Arrange left to right chronologically | Event Timeline |
| 3. Hotspot Marking | 15 min | Pink sticky notes: disputes/questions/pain points | Hotspot Map |
| 4. Command Identification | 20 min | Blue sticky notes: actions that trigger events | Command-Event Pairs |
| 5. Aggregate Identification | 20 min | Yellow sticky notes: business entities | Aggregate Boundaries |
| 6. Bounded Context | 20 min | Dashed boxes: domain boundaries | Context Map |

### Domain Event Examples
| Event | Triggering Command | Aggregate | Bounded Context |
|------|---------|------|----------|
| Order Created | Submit Order | Order | Order Management |
| Payment Completed | Confirm Payment | Payment | Payment Management |
| Inventory Deducted | Deduct Inventory | Inventory | Inventory Management |
| Shipment Order Generated | Create Shipment Order | Logistics | Logistics Management |

### EventStorming Key Outputs
- Event Timeline: End-to-end business process panorama
- Aggregate Boundaries: Transactional consistency boundaries
- Bounded Contexts: Basis for microservice/module splitting
- Hotspot Inventory: Business issues to be clarified/resolved