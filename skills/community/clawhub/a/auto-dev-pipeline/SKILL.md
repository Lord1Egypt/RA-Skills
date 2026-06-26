---
name: auto-dev-pipeline
description: Complete automated development pipeline for one-person companies. Use when a user provides a simple app idea and wants a fully automated development process from requirements to tested code. This skill coordinates prd-skill, dev-skill, and qa-skill to create a seamless PRD → Development → Testing workflow without manual intervention.
---

# Auto Dev Pipeline - One-Person Company Development Automation

## Overview

The Auto Dev Pipeline is a complete automated development system that transforms natural language app ideas into fully tested iOS applications. It orchestrates three specialized skills to create a seamless, hands-off development process:

1. **PRD Generation** (`prd-skill`): Requirements → Structured PRD
2. **Development** (`dev-skill`): PRD → SwiftUI iOS Code
3. **Quality Assurance** (`qa-skill`): Code → Test Cases & Validation

## Pipeline Architecture

### 1. Trigger Mechanism
The pipeline is triggered by natural language app ideas:
- "做一个待办事项App"
- "开发一个健身追踪应用"
- "创建一个社交网络应用"

### 2. Automated Coordination
The pipeline uses OpenClaw's session management to automatically:
1. Spawn `prd-skill` sub-agent with user requirements
2. Monitor PRD completion and trigger `dev-skill`
3. Monitor code generation and trigger `qa-skill`
4. Collect final outputs and provide summary

### 3. Data Flow
```
User Input → prd-skill → PRD Document → dev-skill → SwiftUI Project → qa-skill → Test Suite
```

## Complete Workflow

### Phase 1: Requirements Analysis (prd-skill)
**Input:** Natural language app description
**Process:**
1. Parse and analyze requirements
2. Generate structured PRD with:
   - Product overview and target audience
   - Functional requirements with priorities
   - User flows and screen specifications
   - Technical requirements and constraints
3. Save PRD to `output/prd/[timestamp]-[app-name].md`

**Auto-Trigger:** Upon PRD completion, spawn `dev-skill` with PRD as input

### Phase 2: Development Implementation (dev-skill)
**Input:** PRD document from Phase 1
**Process:**
1. Analyze PRD for technical requirements
2. Generate complete SwiftUI project with:
   - MVVM architecture
   - Data models and services
   - UI components and navigation
   - Business logic implementation
3. Create Xcode project in `output/dev/[app-name]/`

**Auto-Trigger:** Upon code generation, spawn `qa-skill` with project as input

### Phase 3: Quality Assurance (qa-skill)
**Input:** SwiftUI project from Phase 2
**Process:**
1. Analyze code structure and requirements
2. Generate comprehensive test suite:
   - Unit tests for business logic
   - UI tests for user flows
   - Integration tests for data flow
3. Create test documentation and quality report
4. Save to `output/qa/[app-name]-tests/`

**Completion:** Pipeline ends with final summary and deliverables

## Session Management

### Sub-Agent Spawning
```python
# Example coordination logic
def trigger_pipeline(user_requirements):
    # Step 1: Spawn PRD skill
    prd_session = sessions_spawn(
        task=f"Generate PRD for: {user_requirements}",
        runtime="subagent",
        agentId="prd-skill"
    )
    
    # Step 2: Monitor and trigger dev skill
    wait_for_completion(prd_session)
    prd_output = read_prd_output()
    
    dev_session = sessions_spawn(
        task=f"Develop iOS app from PRD: {prd_output}",
        runtime="subagent", 
        agentId="dev-skill"
    )
    
    # Step 3: Monitor and trigger QA skill
    wait_for_completion(dev_session)
    code_output = read_code_output()
    
    qa_session = sessions_spawn(
        task=f"Generate tests for: {code_output}",
        runtime="subagent",
        agentId="qa-skill"
    )
    
    # Step 4: Collect results
    wait_for_completion(qa_session)
    return compile_final_report()
```

### Error Handling
- **PRD Generation Failures**: Retry with clarified requirements
- **Code Generation Errors**: Fallback to simpler implementation
- **Test Generation Issues**: Provide manual test guidelines
- **Session Timeouts**: Resume from last successful checkpoint

## Output Structure

```
output/
├── prd/
│   ├── 20240319-1430-todo-app.md
│   └── 20240319-1500-fitness-tracker.md
├── dev/
│   ├── TodoApp/
│   │   ├── TodoApp.xcodeproj
│   │   ├── Sources/
│   │   └── README.md
│   └── FitnessTracker/
│       ├── FitnessTracker.xcodeproj
│       ├── Sources/
│       └── README.md
└── qa/
    ├── TodoApp-tests/
    │   ├── UnitTests/
    │   ├── UITests/
    │   └── TestReport.md
    └── FitnessTracker-tests/
        ├── UnitTests/
        ├── UITests/
        └── TestReport.md
```

## Example: Complete Pipeline Execution

### User Input
"做一个待办事项App，支持分类、提醒和分享功能"

### Pipeline Execution
1. **Phase 1 (PRD)**: 2 minutes
   - Output: `output/prd/20240319-1430-todo-app.md`
   - Contains: 5 sections, 15 features, technical specs

2. **Phase 2 (Development)**: 5 minutes  
   - Output: `output/dev/TodoApp/` (Xcode project)
   - Contains: 12 Swift files, Core Data model, UI components

3. **Phase 3 (QA)**: 3 minutes
   - Output: `output/qa/TodoApp-tests/` (Test suite)
   - Contains: 28 test cases, test plan, quality report

### Final Delivery
- **Total Time**: 10 minutes
- **Code Coverage**: 85%
- **Features Implemented**: 12/15 (P0+P1)
- **Test Cases**: 28 automated tests
- **Ready for**: Xcode build and deployment

## Configuration Options

### Model Selection
```yaml
pipeline:
  prd_model: "deepseekchat"  # For requirements analysis
  dev_model: "deepseekchat"  # For code generation  
  qa_model: "deepseekchat"   # For test generation
```

### Output Customization
```yaml
output:
  directory: "./auto-dev-output"
  keep_intermediate: true
  generate_readme: true
  include_build_instructions: true
```

### Quality Settings
```yaml
quality:
  min_code_coverage: 70
  require_ui_tests: true
  accessibility_check: true
  performance_benchmarks: true
```

## Best Practices

### For Users
1. **Be Specific**: Provide clear app descriptions
2. **Set Expectations**: Understand MVP vs full feature set
3. **Review Outputs**: Check PRD before development starts
4. **Provide Feedback**: Help improve pipeline accuracy

### For Pipeline Maintenance
1. **Monitor Performance**: Track execution times and success rates
2. **Update Skills**: Keep prd/dev/qa skills current with best practices
3. **Collect Metrics**: Measure code quality and user satisfaction
4. **Iterate Improvements**: Continuously enhance automation logic

## Troubleshooting

### Common Issues
1. **Vague Requirements**: Pipeline asks for clarification
2. **Complex Features**: May require manual intervention
3. **Technical Constraints**: iOS limitations are documented
4. **Timeouts**: Pipeline resumes from last checkpoint

### Resolution Steps
1. Check session logs for error details
2. Review intermediate outputs
3. Adjust requirements and retry
4. Contact pipeline maintainer for complex issues

## Future Enhancements

### Planned Features
1. **Deployment Automation**: App Store Connect integration
2. **CI/CD Pipeline**: GitHub Actions automation
3. **Design Generation**: Figma mockup creation
4. **Documentation**: User manuals and API docs
5. **Monitoring**: App analytics and crash reporting

### Integration Opportunities
1. **App Store**: Automated submission and review
2. **Backend Services**: Firebase/CloudKit integration
3. **Analytics**: Mixpanel/Amplitude setup
4. **Marketing**: App store optimization tools