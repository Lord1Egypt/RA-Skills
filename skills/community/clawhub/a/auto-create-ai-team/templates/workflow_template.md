# {{WORKFLOW_TITLE}}

## {{PROJECT_TYPE_LABEL}}: {{project_type}}

## {{TEAM_TYPE}}: {{team_mode}}

{% if team_mode == "dual" %}
### {{DUAL_WORKFLOW}}

#### {{INTERNAL_TEAM}} ({{PRODUCT_DEV_LABEL}})
- **Creative Designer**: Product ideation and core feature design
- **Technical Developer**: Technical implementation and tool integration
- **QA Engineer**: Product quality and user experience
- **Content Curator**: Content management and categorization

#### {{INTERNET_TEAM}} ({{MARKETING_GROWTH_LABEL}})  
- **Product Manager**: Product planning and commercialization strategy
- **Marketing Expert**: Brand promotion and user acquisition
- **Social Media Operator**: Platform content distribution and community operations
- **Data Analyst**: User behavior analysis and product optimization
- **Business Development Manager**: Partnership relations and revenue expansion
- **UX Researcher**: User feedback collection and demand research

#### {{COLLABORATION_MECHANISM}}
1. **{{WEEKLY_SYNC}}**: Dual team regular progress synchronization
2. **{{SHARED_DOCS}}**: All documents managed in unified directory
3. **{{CROSS_REVIEW}}**: Important decisions require dual team confirmation
4. **{{DATA_SHARING}}**: User and product data bidirectional flow

{% elif team_mode == "single" %}
### {{SINGLE_WORKFLOW}}

#### Core Roles
- **Team Leader**: Overall coordination and task assignment
- **Specialist Roles**: Configured based on project type
- **Quality Assurance**: Output quality and consistency

#### Workflow Steps
1. **Task Assignment**: Team Leader assigns specific tasks
2. **Parallel Execution**: Each role executes their tasks simultaneously
3. **Quality Check**: QA role validates output quality
4. **Integration**: Integrate outputs to form final deliverables

{% else %}
### {{CUSTOM_WORKFLOW}}

Execute workflow according to user-specified custom configuration.

{% endif %}

## {{MULTI_MODEL_SUPPORT}}
- **{{FREE_FIRST}}**: Simple tasks use free models
- **{{PAID_PRECISION}}**: Complex tasks use high-performance paid models
- **{{AUTO_FALLBACK}}**: Auto-switch to free models when paid unavailable
- **{{RESULT_AGGREGATION}}**: Multi-model comparison for quality assurance

## {{AUTOMATION}}
- **{{SCHEDULED_TASKS}}**: Regular data updates and analysis
- **{{EVENT_TRIGGERED}}**: Specific events trigger team actions
- **{{PROGRESS_MONITORING}}**: Real-time task execution status monitoring
- **{{EXCEPTION_HANDLING}}**: Automatic handling of common errors
