#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator | GitHub Actions工作流生成器
"""

import argparse
import yaml
import os
from pathlib import Path


class GitHubActionsWorkflow:
    """GitHub Actions工作流生成器"""
    
    def __init__(self, name):
        self.name = name
        self.triggers = {}
        self.jobs = {}
        self.env = {}
    
    def add_trigger(self, event, branches=None, tags=None):
        """添加触发器"""
        if event not in self.triggers:
            self.triggers[event] = {}
        if branches:
            self.triggers[event]["branches"] = branches
        if tags:
            self.triggers[event]["tags"] = tags
    
    def add_job(self, name, config):
        """添加任务"""
        self.jobs[name] = config
    
    def set_env(self, env_vars):
        """设置环境变量"""
        self.env.update(env_vars)
    
    def to_dict(self):
        """转换为字典"""
        workflow = {
            "name": self.name,
            "on": self.triggers,
            "jobs": self.jobs
        }
        if self.env:
            workflow["env"] = self.env
        return workflow
    
    def save(self, path):
        """保存工作流文件"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)


def generate_python_ci_workflow(name="python-ci"):
    """生成Python CI工作流"""
    workflow = GitHubActionsWorkflow(name)
    
    # 触发器
    workflow.add_trigger("push", branches=["main", "develop"])
    workflow.add_trigger("pull_request")
    
    # 测试任务
    workflow.add_job("test", {
        "runs-on": "ubuntu-latest",
        "strategy": {
            "matrix": {
                "python-version": ["3.9", "3.10", "3.11"]
            }
        },
        "steps": [
            {"uses": "actions/checkout@v4"},
            {"uses": "actions/setup-python@v4", "with": {"python-version": "${{ matrix.python-version }}"}},
            {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
            {"name": "Run linting", "run": "flake8 src/"},
            {"name": "Run tests", "run": "pytest --cov=src --cov-report=xml"},
            {"name": "Upload coverage", "uses": "codecov/codecov-action@v3", "with": {"file": "./coverage.xml"}}
        ]
    })
    
    return workflow


def generate_docker_deploy_workflow(name="docker-deploy"):
    """生成Docker部署工作流"""
    workflow = GitHubActionsWorkflow(name)
    
    workflow.add_trigger("push", branches=["main"])
    workflow.add_trigger("workflow_dispatch")
    
    workflow.add_job("build-and-push", {
        "runs-on": "ubuntu-latest",
        "steps": [
            {"uses": "actions/checkout@v4"},
            {"name": "Set up Docker Buildx", "uses": "docker/setup-buildx-action@v3"},
            {"name": "Login to Docker Hub", "uses": "docker/login-action@v3", "with": {"username": "${{ secrets.DOCKER_USERNAME }}", "password": "${{ secrets.DOCKER_PASSWORD }}"}},
            {"name": "Build and push", "uses": "docker/build-push-action@v5", "with": {"context": ".", "push": True, "tags": "${{ secrets.DOCKER_USERNAME }}/app:${{ github.sha }}"}}
        ]
    })
    
    return workflow


def main():
    parser = argparse.ArgumentParser(description="GitHub Actions Workflow Generator")
    parser.add_argument("--name", default="python-ci", help="Workflow name")
    parser.add_argument("--type", default="python", choices=["python", "docker", "node"], help="Workflow type")
    parser.add_argument("--output", default=".github/workflows/ci.yml", help="Output file path")
    args = parser.parse_args()
    
    # 生成工作流
    if args.type == "python":
        workflow = generate_python_ci_workflow(args.name)
    elif args.type == "docker":
        workflow = generate_docker_deploy_workflow(args.name)
    else:
        workflow = generate_python_ci_workflow(args.name)
    
    # 保存
    workflow.save(args.output)
    print(f"✅ GitHub Actions workflow generated: {args.output}")


if __name__ == "__main__":
    main()
