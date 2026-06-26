---
name: ai-plan-generator
description: Generates comprehensive campaign documents, task decompositions, and context documents from minimal input for ClawTeam continuous iteration. Supports Code Archaeology integration with unified directory structure.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📋","os":["darwin","linux","win32"],"requires":{"bins":["node","git","bash"]}}}
---

# AI Plan Generator v2

AI Plan Generator v2 extends the original business functionality decomposition with **comprehensive campaign document generation**, **task decomposition**, **context document generation**, and **Code Archaeology integration** for ClawTeam continuous iteration.

## Core Capabilities

### 1. Campaign Document Generation
- **Minimal Input Processing**: Only 4 key inputs required (project name, business goal, scope boundary, code location)
- **Multi-Language Support**: Java, Python, Go, C#, Rust, JavaScript
- **Project Type Detection**: Automatically identifies new vs iteration projects
- **Domain-Specific Templates**: Finance, User Management, General domains

### 2. Task Decomposition  
- **Detailed Task Generation**: Complete tasks with priorities, dependencies, acceptance criteria
- **Multiple Output Formats**: JSON, Markdown, ClawTeam formats
- **Domain-Specific Tasks**: Finance (payment, invoicing, reconciliation), User (auth, permissions)
- **Source File Location**: Precise source code location tracking

### 3. Context Document Generation
- **Business Rules**: AI-executable business constraints and validation rules
- **Technical Specifications**: Data models, API contracts, integration specifications  
- **Validation Standards**: Comprehensive testing requirements and coverage criteria
- **Integration Configuration**: External system configuration with timeout/retry settings

### 4. Code Archaeology Integration
- **Unified Directory Structure**: results/, process/, source/ subdirectories
- **Real Analysis Results**: Extracts precise information from actual Code Archaeology output
- **Completeness Analysis**: Validates document completeness and AI executability
- **Clarification Questions**: Automatically generates questions for missing/incomplete information

## Unified Workflow

### Complete End-to-End Process
```bash
# 1. Generate complete workflow from minimal input
ai-plan-generator generate-complete-workflow input.json /path/to/code-archaeology

# 2. Creates standardized directory structure:
project-name/
├── project-name-campaign.md          # Campaign document
├── task-decomposition/              # Task decomposition  
│   ├── tasks.json                   # JSON format
│   ├── tasks.md                     # Markdown format
│   └── clawteam-tasks.json          # ClawTeam format
├── context-documents/               # Context documents
│   ├── business-rules.json          # Business rules
│   ├── technical-specs.yaml         # Technical specifications
│   ├── validation-standards.md      # Validation standards
│   ├── integration-config.json       # Integration configuration
│   └── analysis-report.json         # Completeness analysis report
└── process-files-report.json        # Process file location report
```

### Code Archaeology Integration
```bash
# Convert Code Archaeology results to AI Plan Generator format
ai-plan-generator generate-context-from-archaeology \
  /path/to/project_code_archaeology \
  context-documents \
  finance
```

## Minimal Input Requirements

Only 4 key pieces of information are required:

```json
{
  "projectName": "dms-erp-finance-migration-v1",
  "businessGoal": "Migrate financial module to Java", 
  "scopeBoundary": "Backend services only, no frontend",
  "codeLocation": "src/main/java/com/dms/financialmanagement/"
}
```

## Domain-Specific Intelligence

### Financial Domain
- **Payment Processing**: Contract payment handling with amount validation
- **Invoice Generation**: Tax calculation, invoice types, compliance  
- **Account Reconciliation**: Partial refunds, multiple reconciliations
- **Security Requirements**: Hardcoded credential removal, SQL injection prevention

### User Management Domain  
- **Authentication**: Registration, login, session management
- **Authorization**: Role-based permissions, fine-grained access control
- **Security**: Password complexity, OAuth integration, CSRF protection

## ClawTeam Integration

Generated artifacts are directly compatible with ClawTeam:

- **Campaign Documents**: Used as team description for `clawteam create`
- **Task Decomposition**: Directly importable as `clawteam task create` commands  
- **Context Documents**: Provide AI-executable reference for agent implementation
- **Completeness Analysis**: Ensures high-quality input before team creation

## Best Practices

### Input Quality
- **Project Name**: Include domain keywords (finance, user, order)
- **Business Goal**: Be specific about core business value
- **Scope Boundary**: Clearly define inclusions/exclusions
- **Code Location**: Use complete package paths

### Iteration Strategy
- **Start Simple**: Begin with minimal input, let AI infer details
- **Validate Early**: Run completeness analysis before team creation  
- **Clarify Issues**: Address high-priority clarification questions
- **Iterate Refinement**: Use feedback to improve subsequent iterations

## Example Use Cases

### Legacy PHP to Java Migration
**Input**: Financial module migration from zbs_php to dms-erp
**Output**: Complete campaign document with security remediation, task decomposition with data migration tasks, context documents with precise business rules

### New Microservice Development  
**Input**: Create new user authentication service
**Output**: Campaign document with architecture decisions, task decomposition with OAuth integration, context documents with security requirements

### API Modernization
**Input**: Standardize legacy RPC APIs to RESTful design
**Output**: Campaign document with versioning strategy, task decomposition with backward compatibility, context documents with API specifications

AI Plan Generator v2 transforms minimal input into comprehensive, AI-executable documentation that powers successful ClawTeam continuous iteration.