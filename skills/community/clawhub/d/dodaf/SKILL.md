---
name: dodaf
description: Create, verify, and document DoDAF 2.0/2.1 architecture models with comprehensive completeness and consistency checks. Guides users step-by-step through professional defense architecture design. Outputs consolidated PDF/Word report with all views integrated.
---

# DoDAF Skill

## What This Skill Does

This skill creates **DoDAF-compliant architecture descriptions** for defense and military systems. It guides users through a structured, professional workflow:

1. **Step-by-Step Interview**: Asks clear questions to gather requirements from users who may not know DoDAF terminology
2. **Automatic Data Collection**: Searches for defense standards, doctrine, and best practices when information is insufficient
3. **Professional View Generation**: Creates all required DoDAF views following official standards
4. **Completeness Verification**: Ensures all mandatory views and elements are present
5. **Consistency Checking**: Validates cross-view relationships and naming conventions
6. **Consolidated Report**: Merges all views, diagrams, and matrices into a single well-structured PDF/Word document
7. **Reviewable Report**: Delivers comprehensive documentation with findings and recommendations

---

## Complete DoDAF Workflow

### Phase 1: Stakeholder & Context Interview

**Goal**: Understand the system purpose and stakeholders

**Guided Questions**:
- "What is the main mission or purpose of this system?"
- "Who are the key users or organizations that will use this system?"
- "What are the operational environments (land, sea, air, space, cyber)?"
- "Are there any security classification requirements?"
- "What are the key constraints (budget, timeline, technology)?"

**Automatic Data Collection**:
- Search for relevant defense doctrine (e.g., Joint Publication 3-0)
- Gather service-specific requirements (Army, Navy, Air Force, Marines)
- Collect industry best practices for similar systems

**Output Artifacts**:
- `docs/01-stakeholder-context.md` - Stakeholder analysis document
- `diagrams/AV-1-overview.drawio` - AV-1 Overview and Summary Information

---

### Phase 2: Operational Analysis

**Goal**: Define operational concepts and activities

**Guided Questions**:
- "What are the main operational scenarios?"
- "Who are the external actors (friendly, neutral, adversary)?"
- "What information needs to be exchanged between entities?"
- "What are the key operational tasks?"

**Generated Products**:
- **OV-1**: High-Level Operational Concept Graphic
- **OV-2**: Operational Resource Flow Description
- **OV-3**: Operational Information Exchange Matrix
- **OV-5**: Activity Model

**Output Artifacts**:
- `docs/02-operational-analysis.md` - Operational analysis document
- `diagrams/OV-1-operational-concept.drawio` - OV-1 diagram
- `diagrams/OV-2-resource-flow.drawio` - OV-2 diagram
- `docs/OV-3-information-exchange-matrix.md` - OV-3 matrix
- `diagrams/OV-5-activity-model.drawio` - OV-5 diagram

**Completeness Checks**:
- [ ] All operational scenarios are identified
- [ ] All external actors are defined
- [ ] Information flows are bidirectional where needed
- [ ] Activity decomposition is at appropriate level

**Consistency Checks**:
- [ ] Actor names are consistent across all views
- [ ] Information flow sources/destinations match actors
- [ ] Activity names align with operational tasks

---

### Phase 3: Capability Definition

**Goal**: Define required capabilities and dependencies

**Guided Questions**:
- "What capabilities does the system need to provide?"
- "Which capabilities depend on others?"
- "What is the timeline for capability delivery?"

**Generated Products**:
- **CV-1**: Capability Taxonomy
- **CV-2**: Capability Phasing
- **CV-3**: Capability Dependencies

**Output Artifacts**:
- `docs/03-capability-definition.md` - Capability definition document
- `diagrams/CV-1-capability-taxonomy.drawio` - CV-1 diagram
- `diagrams/CV-2-capability-phasing.drawio` - CV-2 diagram
- `diagrams/CV-3-capability-dependencies.drawio` - CV-3 diagram

**Completeness Checks**:
- [ ] All operational needs map to capabilities
- [ ] Capability hierarchy is complete
- [ ] Dependencies are identified for all capabilities
- [ ] Phasing is defined for each capability

**Consistency Checks**:
- [ ] Capability names match across all views
- [ ] Dependencies form valid chains (no cycles)
- [ ] Phasing aligns with project timeline

---

### Phase 4: System Design

**Goal**: Define system functions and interfaces

**Guided Questions**:
- "What functions must the system perform?"
- "What are the major system components?"
- "How do components communicate?"

**Generated Products**:
- **SV-1**: Systems Interface Description
- **SV-2**: Systems Communication Description
- **SV-4**: Systems Functionality Description
- **SV-5**: Operational Activity to Systems Function Traceability

**Output Artifacts**:
- `docs/04-system-design.md` - System design document
- `diagrams/SV-1-systems-interface.drawio` - SV-1 diagram
- `diagrams/SV-2-systems-communication.drawio` - SV-2 diagram
- `diagrams/SV-4-systems-functionality.drawio` - SV-4 diagram
- `docs/SV-5-traceability-matrix.md` - SV-5 matrix

**Completeness Checks**:
- [ ] All capabilities are realized by system functions
- [ ] All interfaces are defined
- [ ] Function decomposition is complete
- [ ] Traceability matrix is populated

**Consistency Checks**:
- [ ] System function names align with capabilities
- [ ] Interface names match data exchange definitions
- [ ] Traceability links are bidirectional
- [ ] No orphan functions (unconnected to capabilities)

---

### Phase 5: Data Architecture

**Goal**: Define data models and information exchanges

**Guided Questions**:
- "What data needs to be stored and processed?"
- "What are the data formats and standards?"
- "How is data exchanged between systems?"

**Generated Products**:
- **DIV-1**: Data Model Description
- **DIV-2**: Data Dictionary
- **DIV-3**: Data Exchange Matrix

**Output Artifacts**:
- `docs/05-data-architecture.md` - Data architecture document
- `diagrams/DIV-1-data-model.drawio` - DIV-1 diagram
- `docs/DIV-2-data-dictionary.md` - DIV-2 dictionary
- `docs/DIV-3-data-exchange-matrix.md` - DIV-3 matrix

**Completeness Checks**:
- [ ] All data elements are defined
- [ ] Data relationships are specified
- [ ] Exchange formats are identified
- [ ] Data ownership is assigned

**Consistency Checks**:
- [ ] Data element names are consistent
- [ ] Data flows match system interfaces
- [ ] Data types are correctly defined

---

### Phase 6: Technical Architecture

**Goal**: Define technology standards and infrastructure

**Guided Questions**:
- "What technologies will be used?"
- "What standards must be followed?"
- "What are the security requirements?"

**Generated Products**:
- **TV-1**: Technical Standards Profile
- **TV-2**: Technical Measures
- **TV-3**: Technical Architecture Framework

**Output Artifacts**:
- `docs/06-technical-architecture.md` - Technical architecture document
- `docs/TV-1-technical-standards.md` - TV-1 standards
- `docs/TV-2-technical-measures.md` - TV-2 measures
- `diagrams/TV-3-technical-framework.drawio` - TV-3 diagram

**Completeness Checks**:
- [ ] All technology standards are identified
- [ ] Security controls are defined
- [ ] Performance requirements are specified
- [ ] Compliance requirements are addressed

**Consistency Checks**:
- [ ] Standards are compatible with each other
- [ ] Security measures align with classification
- [ ] Technology choices support system functions

---

### Phase 7: Project Planning

**Goal**: Define acquisition strategy and timeline

**Guided Questions**:
- "What is the implementation timeline?"
- "What are the major milestones?"
- "What resources are required?"

**Generated Products**:
- **PV-1**: Project Timeline
- **PV-2**: Project Structure
- **PV-3**: Project Resource Flow

**Output Artifacts**:
- `docs/07-project-planning.md` - Project planning document
- `diagrams/PV-1-project-timeline.drawio` - PV-1 diagram
- `diagrams/PV-2-project-structure.drawio` - PV-2 diagram
- `diagrams/PV-3-project-resource-flow.drawio` - PV-3 diagram

**Completeness Checks**:
- [ ] Timeline covers all capability phases
- [ ] Milestones are defined
- [ ] Resource requirements are estimated
- [ ] Risk mitigation is addressed

**Consistency Checks**:
- [ ] Timeline aligns with capability phasing
- [ ] Resource allocation matches project structure
- [ ] Milestones are realistic

---

### Phase 8: Overview & Integration

**Goal**: Create comprehensive overview and integrated dictionary

**Generated Products**:
- **AV-1**: Overview and Summary Information (final)
- **AV-2**: Integrated Dictionary
- **AV-3**: Concept of Operations (CONOPS)

**Output Artifacts**:
- `docs/08-integration-verification.md` - Integration and verification document
- `diagrams/AV-1-overview-summary.drawio` - AV-1 final diagram
- `docs/AV-2-integrated-dictionary.md` - AV-2 dictionary
- `docs/AV-3-conops.md` - AV-3 CONOPS
- `docs/verification-report.md` - Verification report
- `docs/traceability-matrix.md` - Full traceability matrix

**Completeness Checks**:
- [ ] All views are referenced in overview
- [ ] Dictionary includes all key terms
- [ ] CONOPS describes operational concept
- [ ] Standards profile is complete

**Consistency Checks**:
- [ ] Terminology is consistent across all views
- [ ] Overview accurately summarizes architecture
- [ ] Dictionary definitions match usage

---

### Phase 9: Consolidated Report Generation

**Goal**: Merge all views, diagrams, and matrices into a single well-structured document

**This is the final and critical phase** that transforms scattered artifacts into a professional, deliverable report.

#### 9.1 Report Assembly

**Step 1: Create Consolidated Markdown Document**

Assemble all phase documents into a single Markdown file with the following chapter structure:

```
# [Project Name] DoDAF Architecture Description Report

## Document Control
- Version / Date / Classification / Authors

## Table of Contents (auto-generated)

## Chapter 1: Executive Summary (AV-1)
  - Architecture purpose, scope, findings, recommendations

## Chapter 2: Stakeholder & Context Analysis
  - Mission statement, stakeholders, environment, constraints

## Chapter 3: Operational Architecture (OV)
  - 3.1 High-Level Operational Concept (OV-1) + diagram
  - 3.2 Operational Resource Flow (OV-2) + diagram
  - 3.3 Information Exchange Matrix (OV-3)
  - 3.4 Activity Model (OV-5) + diagram

## Chapter 4: Capability Architecture (CV)
  - 4.1 Capability Taxonomy (CV-1) + diagram
  - 4.2 Capability Phasing (CV-2) + diagram
  - 4.3 Capability Dependencies (CV-3) + diagram

## Chapter 5: Systems Architecture (SV)
  - 5.1 Systems Interface Description (SV-1) + diagram
  - 5.2 Systems Communication (SV-2) + diagram
  - 5.3 Systems Functionality (SV-4) + diagram
  - 5.4 Traceability Matrix (SV-5)

## Chapter 6: Data Architecture (DIV)
  - 6.1 Data Model (DIV-1) + diagram
  - 6.2 Data Dictionary (DIV-2)
  - 6.3 Data Exchange Matrix (DIV-3)

## Chapter 7: Technical Architecture (TV)
  - 7.1 Technical Standards (TV-1)
  - 7.2 Technical Measures (TV-2)
  - 7.3 Technical Framework (TV-3) + diagram

## Chapter 8: Project Planning (PV)
  - 8.1 Project Timeline (PV-1) + diagram
  - 8.2 Project Structure (PV-2) + diagram
  - 8.3 Resource Flow (PV-3) + diagram

## Chapter 9: Concept of Operations (AV-3)
  - Operational scenarios, organization, information flows

## Chapter 10: Verification & Validation
  - 10.1 Completeness Verification
  - 10.2 Consistency Verification
  - 10.3 Traceability Matrix
  - 10.4 Findings & Recommendations

## Appendix A: Integrated Dictionary (AV-2)
## Appendix B: Technical Standards Reference (TV-1 detailed)
## Appendix C: Data Dictionary (DIV-2 detailed)
```

**Step 2: Embed Diagrams**

For each diagram referenced in the report:
1. Export draw.io diagrams to PNG/SVG format (if draw.io CLI available)
2. Embed images inline in the Markdown document using `![diagram](path)`
3. If export not available, reference the .drawio file path for manual export

**Step 3: Generate Final Output**

Generate the consolidated report in the user's preferred format:

| Format | Method | Notes |
|--------|--------|-------|
| **Markdown** | Direct assembly | Always generated as base format |
| **PDF** | Use `pandoc` or browser print | Professional typesetting, page numbers |
| **Word (DOCX)** | Use `pandoc` | Editable, track changes possible |
| **HTML** | Use `pandoc` | Interactive, hyperlinked |

**Pandoc command examples**:
```bash
# Markdown to PDF
pandoc consolidated-report.md -o report.pdf --pdf-engine=xelatex -V mainfont="SimSun" -V geometry:margin=2.5cm --toc --toc-depth=3 -V numbersections

# Markdown to DOCX
pandoc consolidated-report.md -o report.docx --toc --toc-depth=3 --reference-doc=template.docx

# Markdown to HTML
pandoc consolidated-report.md -o report.html --standalone --toc --toc-depth=3 --metadata title="DoDAF Architecture Report"
```

**Output Artifacts**:
- `report/consolidated-report.md` - Single consolidated Markdown file
- `report/[project-name]-dodaf-report.pdf` - PDF report (if pandoc available)
- `report/[project-name]-dodaf-report.docx` - Word report (if pandoc available)

#### 9.2 Report Quality Checklist

- [ ] All 23 DoDAF view products are included as chapters/sections
- [ ] All diagrams are embedded or referenced
- [ ] Cross-references between sections are accurate
- [ ] Table of contents is complete
- [ ] Document control information is filled
- [ ] Classification markings are present on each page (if required)
- [ ] Page numbers and headers/footers are set
- [ ] Acronyms and abbreviations are defined in dictionary

---

## Comprehensive Verification Checklist

### Completeness Verification

| Check | Description | Status |
|-------|-------------|--------|
| CV-1 | Capability taxonomy covers all operational needs | ☐ |
| CV-2 | Capability phasing is defined | ☐ |
| CV-3 | Capability dependencies are mapped | ☐ |
| OV-1 | High-level operational concept exists | ☐ |
| OV-2 | Resource flows are described | ☐ |
| OV-3 | Information exchange matrix is complete | ☐ |
| OV-5 | Activity model is defined | ☐ |
| SV-1 | System interfaces are described | ☐ |
| SV-2 | System communications are defined | ☐ |
| SV-4 | System functionality is described | ☐ |
| SV-5 | Traceability matrix is populated | ☐ |
| DIV-1 | Data model is defined | ☐ |
| DIV-2 | Data dictionary is complete | ☐ |
| DIV-3 | Data exchange matrix is populated | ☐ |
| TV-1 | Technical standards are identified | ☐ |
| TV-2 | Technical measures are defined | ☐ |
| TV-3 | Technical architecture framework is defined | ☐ |
| PV-1 | Project timeline is defined | ☐ |
| PV-2 | Project structure is defined | ☐ |
| PV-3 | Project resource flow is defined | ☐ |
| AV-1 | Overview document exists | ☐ |
| AV-2 | Integrated dictionary is complete | ☐ |
| AV-3 | CONOPS is complete | ☐ |

### Consistency Verification

| Check | Description | Status |
|-------|-------------|--------|
| Naming | All elements have consistent naming conventions | ☐ |
| Traceability | Cross-view traceability is complete and bidirectional | ☐ |
| Capability-System | Every capability maps to at least one system function | ☐ |
| Function-Interface | Every function uses defined interfaces | ☐ |
| Data-Interface | Every data exchange uses defined interfaces | ☐ |
| No Orphans | No orphan elements (elements without connections) | ☐ |
| No Cycles | No circular dependencies in capability hierarchy | ☐ |
| Standards | All technology choices comply with specified standards | ☐ |
| Security | Security requirements are addressed throughout | ☐ |
| Terminology | Dictionary terms match usage in all views | ☐ |

---

## Traceability Matrix Template

| Capability | Operational Activity | System Function | Data Element | Interface | Technical Standard | Project Milestone |
|------------|---------------------|-----------------|--------------|-----------|-------------------|-------------------|
|            |                     |                 |              |           |                   |                   |
|            |                     |                 |              |           |                   |                   |
|            |                     |                 |              |           |                   |                   |

---

## Viewpoint Relationships

```
AV (Overview)
    |
    +-- OV (Operational) ----------------+
    |       |                            |
    |       +--> CV (Capability) <-------+
    |               |                    |
    |               +--> SV (Systems) <--+
    |                       |            |
    |                       +--> DIV (Data) --+--> Cross-View Traceability
    |                       +--> TV (Tech) ---+
    |                       +--> PV (Project) +
    |                                       |
    +---------------------------------------+
```

---

## Output Artifacts

### Per-Phase Artifacts (Scattered)

Each phase generates:
- **Markdown documents**: Detailed descriptions, matrices, dictionaries in `docs/`
- **draw.io diagrams**: Visual architecture views in `diagrams/`

### Final Consolidated Report (Phase 9)

| Artifact | Format | Description |
|----------|--------|-------------|
| Consolidated Report (MD) | Markdown | Single file with all chapters |
| Consolidated Report (PDF) | PDF | Professional printable report |
| Consolidated Report (DOCX) | Word | Editable report for review |
| Diagram Files | drawio/PNG | All architecture diagrams |

---

## Agent Integration

This skill calls external agents as needed:

| Agent | Purpose | Trigger |
|-------|---------|---------|
| **WebSearch** | Search defense doctrine, standards, case studies | When user provides insufficient information |
| **drawio** | Generate draw.io format architecture diagrams | Each phase with visual views |
| **DataAnalysis** | Analyze operational data and metrics | When quantitative analysis is needed |

---

## Tool Dependencies

| Tool | Purpose | Required | Install |
|------|---------|----------|---------|
| draw.io Desktop | Export diagrams to PNG/SVG | No | https://github.com/jgraph/drawio-desktop |
| Pandoc | Convert Markdown to PDF/DOCX | No | https://pandoc.org/installing.html |
| XeLaTeX | PDF engine for CJK support | No (for PDF) | TeX Live / MiKTeX |

> Note: If pandoc or draw.io CLI is not available, the skill will still generate the consolidated Markdown report and .drawio diagram files. Users can manually export or convert later.

---

## Reference Documents

- `references/dodaf-views.md` - Complete DoDAF 2.0 viewpoint reference
- `references/dodaf-terminology.md` - Official DoDAF terminology
- `references/dodaf-best-practices.md` - Industry best practices

---

## Changelog

### v2.0 (2026-05)
- **Added Phase 9**: Consolidated report generation (PDF/Word/HTML output)
- **Added output artifact tracking**: Each phase now specifies exact file paths
- **Added drawio skill integration**: Diagrams generated as .drawio files
- **Added tool dependencies section**: Pandoc, XeLaTeX, draw.io CLI
- **Enhanced verification**: 23 view products tracked (was 19)
- **Improved workflow**: Sequential phase execution with per-phase verification
