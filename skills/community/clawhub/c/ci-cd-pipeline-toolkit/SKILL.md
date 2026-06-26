# CI/CD Pipeline Toolkit

## Metadata
- **Name**: ci-cd-pipeline-toolkit
- **Display Name**: CI/CD Pipeline Toolkit | CI/CD流水线工具包
- **Description**: 
  - EN: Automated CI/CD pipeline management supporting GitHub Actions, GitLab CI, and Jenkins. Automate build, test, and deployment workflows.
  - ZH: 自动化CI/CD流水线管理，支持GitHub Actions、GitLab CI和Jenkins。自动化构建、测试和部署工作流。
- **Version**: 1.0.0
- **Author**: Kimi Claw
- **Tags**: cicd, devops, github-actions, gitlab-ci, jenkins, pipeline, automation, deployment
- **Category**: DevOps
- **Icon**: 🔄

## Capabilities

### Actions

#### github_actions_workflow_create
Create GitHub Actions workflow file
- **workflow_name**: Workflow name (string, required)
- **trigger_events**: Trigger events (array, required) - push, pull_request, schedule, workflow_dispatch
- **jobs**: Job configurations (object, required)
  - build: Build job steps
  - test: Test job steps  
  - deploy: Deploy job steps
- **runs_on**: Runner type (string) - ubuntu-latest, windows-latest, macos-latest

#### gitlab_ci_config_generate
Generate GitLab CI/CD configuration
- **stages**: Pipeline stages (array, required) - build, test, deploy
- **jobs**: Job definitions (object, required)
- **variables**: Environment variables (object)
- **cache_paths**: Cache paths (array)

#### jenkins_pipeline_create
Create Jenkins pipeline script
- **pipeline_type**: Type (string) - declarative, scripted
- **stages**: Stage definitions (array, required)
- **agent**: Agent label (string)
- **tools**: Required tools (object)

#### pipeline_status_check
Check CI/CD pipeline execution status
- **platform**: Platform (string, required) - github, gitlab, jenkins
- **pipeline_id**: Pipeline/Run ID (string, required)
- **repository**: Repository name (string, required)

#### deployment_trigger
Trigger deployment to environment
- **environment**: Target environment (string, required) - dev, staging, production
- **version**: Deployment version (string, required)
- **platform**: Deployment platform (string) - k8s, docker, aws, azure

## Requirements
- Python 3.8+
- PyYAML >= 6.0
- Requests >= 2.28.0
- python-jenkins >= 1.8.0 (optional, for Jenkins API)

## Examples

### GitHub Actions Workflow
```python
from cicd_toolkit import GitHubActionsWorkflow

# Create Python CI workflow
workflow = GitHubActionsWorkflow("python-ci")
workflow.add_trigger("push", branches=["main", "dev"])
workflow.add_trigger("pull_request")

# Add jobs
workflow.add_job("test", {
    "runs-on": "ubuntu-latest",
    "steps": [
        {"uses": "actions/checkout@v4"},
        {"uses": "actions/setup-python@v4", "with": {"python-version": "3.11"}},
        {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
        {"name": "Run tests", "run": "pytest"}
    ]
})

workflow.save(".github/workflows/python-ci.yml")
```

### GitLab CI Configuration
```python
from cicd_toolkit import GitLabCIConfig

# Generate CI config
config = GitLabCIConfig()
config.add_stage("build")
config.add_stage("test")
config.add_stage("deploy")

config.add_job("build_app", {
    "stage": "build",
    "script": ["npm install", "npm run build"],
    "artifacts": {"paths": ["dist/"]}
})

config.add_job("test_app", {
    "stage": "test",
    "script": ["npm run test"],
    "needs": ["build_app"]
})

config.save(".gitlab-ci.yml")
```

## Scripts
- `scripts/github_workflow_generator.py`: GitHub Actions工作流生成器
- `scripts/gitlab_ci_generator.py`: GitLab CI配置生成器
- `scripts/jenkins_pipeline_generator.py`: Jenkins流水线生成器
- `scripts/pipeline_monitor.py`: 流水线监控工具

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Generate GitHub Actions workflow
python scripts/github_workflow_generator.py --name python-ci --type pytest

# Generate GitLab CI config
python scripts/gitlab_ci_generator.py --stages build,test,deploy

# Monitor pipeline status
python scripts/pipeline_monitor.py --platform github --repo owner/repo
```

## License
MIT License
