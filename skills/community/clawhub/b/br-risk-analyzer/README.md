# BR Risk Analyzer

## Purpose
Implements systematic code risk analysis following the `codeReview.md` protocol. Analyzes code changes against requirement documents to identify and prioritize risks with evidence-based findings.

## Features
- Requirement-driven code review workflow
- Strict adherence to codeReview.md execution protocol  
- Evidence-based risk identification with file paths and method names
- Layered risk analysis across 8 dimensions (correctness, boundaries, concurrency, etc.)
- Priority classification (P0/P1/P2/P3) with clear criteria
- Structured output template matching team standards
- Knowledge persistence for continuous improvement

## Usage
Provide in a single message:
1. **Requirement/Design Summary** - Key functional and non-functional requirements
2. **Code Scope** - Repository paths, modules, branches, or ticket references  
3. **Output Expectations** - Risk list only, or include test recommendations

## Output Format
Follows mandatory template:
- Review summary with scope and priority counts
- Risk inventory table with ID, description, location, impact, and recommendations
- Requirement coverage assessment
- Optional testing recommendations for high-priority risks

## Integration
- Built on DTS project architecture knowledge
- Implements codeReview.md standard workflow and checklist
- Complements existing code-review skill with requirement-focused analysis
- Maintains project understanding repository for context continuity

## Requirements
- Access to code repository for semantic search and file examination
- Clear requirement documentation or design specifications
- Defined scope boundaries for focused analysis

## Based On
- `D:\code\dts\dts\codeReview.md` protocol standard
- DTS Project Architecture from `D:\code\dts\dts\DTS项目全景报告.md`