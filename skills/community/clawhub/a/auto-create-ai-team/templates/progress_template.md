# {{PROJECT_NAME}} - Project Progress

## 📋 {{PROJECT_INFO}}
- **{{PROJECT_NAME_LABEL}}**: {{PROJECT_NAME}}
- **{{CREATION_TIME}}**: {{CREATION_DATE}}
- **{{PROJECT_TYPE_LABEL}}**: {{PROJECT_TYPE}}
- **{{TEAM_TYPE}}**: {{TEAM_MODE_DESC}}

## 🤖 {{TEAM_STRUCTURE}}
{% if TEAM_MODE == "dual" %}
### {{INTERNAL_TEAM_SECTION}}
- **{{TEAM_SIZE_LABEL}}**: {{INTERNAL_TEAM_SIZE}}
- **{{MAIN_ROLES}}**: {{INTERNAL_TEAM_ROLES}}
- **{{CORE_RESPONSIBILITIES}}**: {{PRODUCT_DEV}}

### {{INTERNET_TEAM_SECTION}}  
- **{{TEAM_SIZE_LABEL}}**: {{INTERNET_TEAM_SIZE}}
- **{{MAIN_ROLES}}**: {{INTERNET_TEAM_ROLES}}
- **{{CORE_RESPONSIBILITIES}}**: {{MARKETING_GROWTH}}

{% elif TEAM_MODE == "single" %}
### {{SINGLE_TEAM_SECTION}}
- **{{TEAM_SIZE_LABEL}}**: {{TEAM_SIZE}}
- **{{MAIN_ROLES}}**: {{TEAM_ROLES}}
- **{{CORE_RESPONSIBILITIES}}**: {{FULL_PROCESS}}

{% else %}
### Custom Team
- **Configuration file**: custom_team_config.json
- **Details**: See custom configuration file

{% endif %}

## 🎯 {{CURRENT_STATUS}}
- **{{TEAM_CREATED}}**: ✅ {{COMPLETED}}
- **{{CONFIG_FILES}}**: ✅ {{GENERATED}}
- **{{AUTOMATION_SCRIPTS}}**: ✅ {{DEPLOYED}}
- **{{RUNTIME_LOGS}}**: ✅ {{ENABLED}}

## 📈 {{NEXT_STEPS}}
1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2}}
3. {{NEXT_STEP_3}}
4. {{NEXT_STEP_4}}

## 📁 {{DIRECTORY_STRUCTURE}}
```
{{PROJECT_PATH}}/
├── ai-team/
│   ├── team-info/          # {{TEAM_INFO_DIR}}
│   {% if TEAM_MODE == "dual" %}
│   ├── internal-team/      # {{INTERNAL_TEAM_DIR}}
│   └── internet-team/      # {{INTERNET_TEAM_DIR}}
│   {% else %}
│   └── single-team/        # {{SINGLE_TEAM_DIR}}
│   {% endif %}
└── [{{ORIGINAL_DIRS}}]
```

---
*{{AUTO_GENERATED}}*
