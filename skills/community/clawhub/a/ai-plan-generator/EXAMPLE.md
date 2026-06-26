# AI Plan Generator - Usage Examples

## Basic Usage
```
Generate AI-executable development plan from Code Archaeology results in /Users/admin/.openclaw/workspace/code-archaeology-v2/.code-archaeology-zbs-php
```

## Natural Language Flexibility
The key advantage of this skill is language-agnostic task generation:

### For Java Migration
```
User: "Use clawteam to rebuild this dms-erp system in Java with Spring Boot"
AI Plan Generator: Provides business function tasks
ClawTeam: Executes tasks using Java/Spring Boot implementation
```

### For Python Migration  
```
User: "Convert this legacy PHP system to Python with Django"
AI Plan Generator: Provides the same business function tasks  
ClawTeam: Executes tasks using Python/Django implementation
```

### For Node.js Modernization
```
User: "Modernize this system using Node.js and Express"
AI Plan Generator: Provides identical business function tasks
ClawTeam: Executes tasks using Node.js/Express implementation  
```

## Expected Output Structure

### ai_execution_plan.md (Primary Output)
- **Business-focused task descriptions** without language-specific implementation details
- **Complete business context** including rules, workflows, and data models
- **Clear validation criteria** based on business requirements
- **Phase-based organization** with proper priority ordering

### ai_execution_plan.json (Backup Output)
- **Machine-processable task objects** with standardized structure
- **Task dependencies** for proper execution ordering
- **Business context metadata** for AI agent understanding

## Input Requirements

The skill expects Code Archaeology results in the standard structure:
```
analysis_directory/
├── domains/
│   ├── contract_management.analysis.md    # Business rules analysis
│   ├── contract_management.flows.json     # Business workflow definitions
│   └── contract_management.model.json     # Data model specifications
├── memory/
│   └── FINDINGS.jsonl                    # Security vulnerabilities (optional)
└── [other directories...]
```

## Integration with ClawTeam

The generated tasks are designed for seamless ClawTeam integration:

1. **Task Assignment**: Each business function becomes a separate ClawTeam agent task
2. **Agent Specialization**: Agents can be specialized by business domain (contract, customer, financial, etc.)
3. **Dependency Management**: ClawTeam handles task dependencies automatically
4. **Language Flexibility**: Agents implement tasks in whatever language the user specifies

## Typical Workflow

1. **Run Code Archaeology** on legacy system to extract business intelligence
2. **Generate AI Plan** using this skill to create business function tasks
3. **Execute with ClawTeam** using natural language instruction specifying target language/framework
4. **Monitor and Supervise** using ClawTeam's built-in monitoring capabilities

This creates a clean separation between **business functionality specification** (AI Plan Generator) and **technical implementation** (ClawTeam agents), enabling maximum flexibility and reusability.