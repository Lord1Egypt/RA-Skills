#!/usr/bin/env python3
"""
CI/CD Pipeline Toolkit - Basic Usage Example | 基础使用示例
"""

from cicd_toolkit import GitHubActionsWorkflow, GitLabCIConfig


def github_actions_example():
    """GitHub Actions workflow creation example"""
    # Create a Python CI workflow
    workflow = GitHubActionsWorkflow("python-ci")
    
    # Add triggers
    workflow.add_trigger("push", branches=["main", "develop"])
    workflow.add_trigger("pull_request")
    
    # Add test job
    workflow.add_job("test", {
        "runs-on": "ubuntu-latest",
        "steps": [
            {"uses": "actions/checkout@v4"},
            {"uses": "actions/setup-python@v4", "with": {"python-version": "3.11"}},
            {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
            {"name": "Run tests", "run": "pytest --cov=src --cov-report=xml"}
        ]
    })
    
    # Save workflow
    workflow.save(".github/workflows/python-ci.yml")
    print("✅ GitHub Actions workflow created!")


def gitlab_ci_example():
    """GitLab CI configuration example"""
    # Create GitLab CI config
    config = GitLabCIConfig()
    
    # Add stages
    config.add_stage("build")
    config.add_stage("test")
    config.add_stage("deploy")
    
    # Add jobs
    config.add_job("build_app", {
        "stage": "build",
        "script": ["npm install", "npm run build"],
        "artifacts": {"paths": ["dist/"], "expire_in": "1 hour"}
    })
    
    config.add_job("test_app", {
        "stage": "test",
        "script": ["npm run test:unit", "npm run test:e2e"],
        "needs": ["build_app"],
        "coverage": '/Coverage: \d+\.\d+%/' 
    })
    
    config.add_job("deploy_staging", {
        "stage": "deploy",
        "script": ["npm run deploy:staging"],
        "environment": {"name": "staging", "url": "https://staging.example.com"},
        "only": ["develop"]
    })
    
    # Save config
    config.save(".gitlab-ci.yml")
    print("✅ GitLab CI configuration created!")


if __name__ == "__main__":
    print("🔄 CI/CD Pipeline Toolkit - Basic Examples")
    print("=" * 50)
    
    github_actions_example()
    gitlab_ci_example()
    
    print("\n✨ Examples completed! Check generated files.")
