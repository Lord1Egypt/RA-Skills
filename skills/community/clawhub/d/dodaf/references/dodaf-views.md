# DoDAF 2.0/2.1 Viewpoints Reference

## Overview

DoDAF (Department of Defense Architecture Framework) provides a standardized way to describe defense architectures. This reference covers all key viewpoints and products.

## DoDAF Viewpoints

### All View (AV)

**Purpose**: Provide overview and context for the architecture description.

**Products**:
- **AV-1**: Overview and Summary Information - Executive-level overview of the architecture
- **AV-2**: Integrated Dictionary - Unified terminology and definitions across all views
- **AV-3**: Concept of Operations (CONOPS) - Operational concept narrative
- **AV-4**: Standards Profile - Applicable standards and conventions

### Operational View (OV)

**Purpose**: Describe the operational context, activities, and information flows.

**Products**:
- **OV-1**: High-Level Operational Concept Graphic - Visual overview of operational concept
- **OV-2**: Operational Resource Flow Description - Resources exchanged between operational nodes
- **OV-3**: Operational Information Exchange Matrix - Detailed information exchange requirements
- **OV-4**: Organizational Relationships Chart - Command and organizational structure
- **OV-5**: Operational Activity Model - Decomposition of operational activities
- **OV-5a**: Activity Decomposition Tree - Hierarchical activity breakdown
- **OV-5b**: Activity Sequence and Timing Description - Temporal ordering of activities
- **OV-6a**: Operational Rules Model - Business rules constraining operations
- **OV-6b**: State Transition Description - States and transitions of operational processes
- **OV-6c**: Event-Trace Description - Sequence of events in operational scenarios

### Capability View (CV)

**Purpose**: Describe capabilities and their dependencies.

**Products**:
- **CV-1**: Capability Taxonomy - Hierarchical classification of capabilities
- **CV-2**: Capability Phasing - Capability evolution over time periods
- **CV-3**: Capability Dependencies - Interdependencies between capabilities
- **CV-4**: Capability to Systems Mapping - Mapping capabilities to realizing systems

### Systems View (SV)

**Purpose**: Describe system functions, interfaces, and data exchanges.

**Products**:
- **SV-1**: Systems Interface Description - Systems and their interfaces
- **SV-2**: Systems Communication Description - Communication links and protocols
- **SV-3**: Systems-Systems Matrix - Relationships between systems
- **SV-4**: Systems Functionality Description - System functions and their decomposition
- **SV-5**: Operational Activity to Systems Function Traceability Matrix - Activity-to-function mapping
- **SV-6**: Systems Event-Trace Description - System-level event sequences
- **SV-7**: Systems Performance Parameters Matrix - Performance requirements
- **SV-8**: Systems Evolution Description - System evolution over time
- **SV-9**: Systems Technology Forecast - Technology insertion opportunities
- **SV-10a**: Systems Rules Model - System-level constraints
- **SV-10b**: Systems State Transition Description - System state machines
- **SV-10c**: Systems Event-Trace Description - System event traces
- **SV-11**: Physical Schema - Physical data model

### Data and Information View (DIV)

**Purpose**: Describe data models and information exchanges.

**Products**:
- **DIV-1**: Data Model Description - Conceptual/logical data model
- **DIV-2**: Data Dictionary - Detailed data element definitions
- **DIV-3**: Data Exchange Matrix - System-level data exchange specifications
- **DIV-4**: Data Flow Diagram - Data flow between systems

### Project View (PV)

**Purpose**: Describe acquisition strategy and timeline.

**Products**:
- **PV-1**: Project Timeline - Milestones and schedule
- **PV-2**: Project Structure - Organizational structure for the project
- **PV-3**: Project Resource Flow - Resource allocation and dependencies
- **PV-4**: Project Measures of Effectiveness - Success criteria

### Technical View (TV)

**Purpose**: Describe technical standards and constraints.

**Products**:
- **TV-1**: Technical Standards Profile - Applicable standards and policies
- **TV-2**: Technical Measures - Technical performance measures
- **TV-3**: Technical Architecture Framework - Technology infrastructure

## Viewpoint Relationships

```
AV (Overview)
  |
  +-- OV (Operational) -----+
  |       |                  |
  |       +--> CV (Capability)
  |               |          |
  |               +--> SV (Systems) --+
  |                       |           |
  |                       +--> DIV (Data) --+--> Traceability
  |                       +--> TV (Tech) ---+
  |                       +--> PV (Project) +
  |                                      |
  +--------------------------------------+
```

## Core View Products for Typical Projects

For most projects, the following 23 products form the minimum viable set:

| Viewpoint | Products | Count |
|-----------|----------|-------|
| AV | AV-1, AV-2, AV-3 | 3 |
| OV | OV-1, OV-2, OV-3, OV-5 | 4 |
| CV | CV-1, CV-2, CV-3 | 3 |
| SV | SV-1, SV-2, SV-4, SV-5 | 4 |
| DIV | DIV-1, DIV-2, DIV-3 | 3 |
| TV | TV-1, TV-2, TV-3 | 3 |
| PV | PV-1, PV-2, PV-3 | 3 |
| **Total** | | **23** |

## Key Terms

| Term | Definition |
|------|------------|
| **Viewpoint** | A specification of the conventions for constructing and using a view |
| **View** | A representation of a system from the perspective of a related set of concerns |
| **Product** | A specific deliverable within a viewpoint |
| **Architecture Description** | The complete set of products that describe an architecture |
| **Operational Node** | An element of the operational architecture that performs a function |
| **Needline** | A requirement for information flow between operational nodes |
| **Capability** | The ability to achieve a desired effect under specified conditions |
| **Traceability** | The ability to link elements across different views |

## Domain-Specific Standards (Chinese Defense)

| Standard | Name | Scope |
|----------|------|-------|
| GJB 7686 | Military Diesel Engine General Specification | Engine technical requirements |
| GJB 150A | Equipment Laboratory Environmental Test Methods | Environmental testing |
| GJB 9001C | Quality Management System Requirements | Quality system |
| GJB 3206A | Configuration Management | Technical state management |
| GJB 811 | Military Vehicle Engine Test Methods | Engine testing |
| GJB 450B | Equipment Reliability General Requirements | Reliability engineering |
| GJB 451A | Reliability, Maintainability, Supportability Terms | RMS terminology |
