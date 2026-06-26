---
name: code-archaeology
description: Analyze legacy codebases to extract business rules, technical specifications, and migration requirements. Use when analyzing PHP, Java, Python, or other legacy systems for modernization planning.
---

# Code Archaeology Skill

## Overview

Code Archaeology is a systematic analysis methodology for understanding legacy codebases and extracting actionable insights for modernization. This skill provides tools and workflows for:

- **Business Rule Extraction**: Identify and document business logic from legacy code
- **Technical Specification Generation**: Extract data models, API contracts, and system architecture  
- **Security Risk Assessment**: Identify security vulnerabilities and technical debt
- **Migration Planning**: Generate detailed migration requirements and task breakdowns
- **AI Plan Generator Integration**: Convert analysis results into AI-executable context documents

## Unified Directory Structure

Code Archaeology results are organized in a standardized directory structure:

```
{project}_code_archaeology/
├── results/                    # Primary analysis outputs (for AI integration)
│   ├── {project}_api_analysis.md
│   ├── {project}_security_audit_results.md
│   ├── {project}_performance_analysis.md
│   ├── {project}_technical_debt_assessment.md
│   ├── {project}_optimization_recommendations.md
│   └── {project}_code_archaeology_final_report.md
├── process/                   # Detailed analysis artifacts (30+ files)
│   ├── 01-system-constants-analysis.md
│   ├── 02-database-schema-analysis.md
│   ├── 03-business-domain-file-list.md
│   ├── {domain}-analysis.md (per business domain)
│   └── round2_progress.json
├── source/                    # Original source code reference
│   └── {project}/
└── {project}_archaeology_status.json  # Analysis status tracking
```

## Core Capabilities

### 1. Multi-Round Analysis
- **Round 1**: Business domain mapping and core architecture analysis
- **Round 2**: Deep technical assessment (security, performance, optimization)

### 2. Domain-Specific Analysis
- **Financial Management**: Payment processing, invoicing, reconciliation
- **Customer Management**: User authentication, profile management
- **Contract Management**: Contract lifecycle, status transitions
- **Supply Chain**: Inventory, procurement, logistics

### 3. Security Risk Identification
- **Critical**: Hardcoded credentials, SQL injection vulnerabilities
- **High**: Weak password storage, session management issues
- **Medium**: XSS/CSRF protection gaps, insecure file permissions

### 4. Technical Debt Assessment
- **Architecture**: Monolithic limitations, lack of layered architecture
- **Code Quality**: Code duplication, outdated language features
- **Maintainability**: Missing documentation, poor test coverage
- **Performance**: Database query optimization, caching mechanisms

## AI Plan Generator Integration

Code Archaeology results can be directly consumed by AI Plan Generator to create:

- **Campaign Documents**: Strategic migration plans with clear boundaries
- **Context Documents**: AI-executable business rules and technical specifications  
- **Task Decomposition**: Detailed implementation tasks with priorities and dependencies
- **Validation Standards**: Comprehensive testing requirements and acceptance criteria

### Integration Workflow
```bash
# 1. Run Code Archaeology analysis
code-archaeology analyze legacy-project --output-dir legacy_project_code_archaeology

# 2. Generate AI Plan Generator context from archaeology results  
ai-plan-generator generate-context-from-archaeology \
  /path/to/legacy_project_code_archaeology \
  context-documents \
  finance

# 3. Validate context document completeness
ai-plan-generator analyze-completeness context-documents

# 4. Create ClawTeam migration team
clawteam create --name "finance-migration" --description-file campaign.md
```

## Usage Guidelines

### When to Use
- **Legacy System Modernization**: Planning migration from PHP 5.x, legacy Java, etc.
- **Business Logic Documentation**: Extracting undocumented business rules
- **Security Remediation**: Identifying and prioritizing security vulnerabilities
- **Technical Debt Reduction**: Planning systematic codebase improvements

### Input Requirements
- **Source Code Access**: Full access to legacy codebase
- **Business Context**: Understanding of business domains and requirements  
- **Target Architecture**: Clear vision of target modern architecture

### Output Artifacts
- **Comprehensive Reports**: Executive summaries and detailed technical analysis
- **Actionable Recommendations**: Prioritized improvement and migration tasks
- **Risk Assessments**: Security and business continuity risk evaluations
- **Integration Ready**: Structured data for AI Plan Generator consumption

## Best Practices

### Analysis Process
1. **Start Broad**: Begin with high-level business domain mapping
2. **Go Deep**: Focus on critical domains (financial, security-sensitive)
3. **Validate Findings**: Cross-reference analysis results with business stakeholders
4. **Iterate**: Refine analysis based on feedback and new discoveries

### Documentation Standards
- **Machine Readable**: Structure outputs for AI consumption
- **Human Understandable**: Provide clear explanations for business stakeholders  
- **Action Oriented**: Focus on actionable insights and recommendations
- **Version Controlled**: Track analysis evolution over time

### Integration Patterns
- **ClawTeam Orchestration**: Use analysis results to drive multi-agent coordination
- **Continuous Validation**: Regularly validate AI interpretations against original code
- **Feedback Loops**: Use implementation results to refine future analyses

## Example Use Cases

### Financial Module Migration
**Input**: Legacy PHP financial system with hardcoded credentials
**Analysis**: Identifies payment processing logic, security vulnerabilities, data models
**Output**: Complete migration plan with security remediation and validation standards

### User Authentication Modernization  
**Input**: Custom authentication system with weak password storage
**Analysis**: Extracts user management workflows, identifies security gaps
**Output**: Modern authentication implementation plan with proper security controls

### API Standardization
**Input**: Inconsistent RPC-style APIs across multiple modules
**Analysis**: Documents all API endpoints, request/response formats, error handling
**Output**: RESTful API redesign specification with backward compatibility strategy

Code Archaeology transforms legacy code understanding from an art into a systematic, repeatable science that powers AI-driven modernization.

## Integration Scripts

This skill includes integration scripts for converting Code Archaeology results to AI Plan Generator format:

- `convert-to-ai-plan-generator.cjs`: Main conversion utility
- `code-archaeology-integrator.cjs`: Core parsing and extraction logic  
- `process-file-manager.cjs`: File location and organization management

### Usage
```bash
node convert-to-ai-plan-generator.cjs /path/to/archaeology-results output-dir domain
```