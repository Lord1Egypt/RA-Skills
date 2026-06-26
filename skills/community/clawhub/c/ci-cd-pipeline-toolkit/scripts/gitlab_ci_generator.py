#!/usr/bin/env python3
"""
GitLab CI Configuration Generator | GitLab CI配置生成器
"""

import argparse
import yaml


class GitLabCIConfig:
    """GitLab CI配置生成器"""
    
    def __init__(self):
        self.stages = []
        self.jobs = {}
        self.variables = {}
        self.cache = {}
    
    def add_stage(self, stage):
        """添加阶段"""
        if stage not in self.stages:
            self.stages.append(stage)
    
    def add_job(self, name, config):
        """添加任务"""
        self.jobs[name] = config
    
    def set_variable(self, key, value):
        """设置变量"""
        self.variables[key] = value
    
    def set_cache(self, paths, key=None):
        """设置缓存"""
        self.cache["paths"] = paths
        if key:
            self.cache["key"] = key
    
    def to_dict(self):
        """转换为字典"""
        config = {}
        if self.stages:
            config["stages"] = self.stages
        if self.variables:
            config["variables"] = self.variables
        if self.cache:
            config["cache"] = self.cache
        config.update(self.jobs)
        return config
    
    def save(self, path):
        """保存配置文件"""
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, allow_unicode=True)


def generate_python_pipeline():
    """生成Python项目CI/CD流水线"""
    config = GitLabCIConfig()
    
    # 阶段
    config.add_stage("build")
    config.add_stage("test")
    config.add_stage("deploy")
    
    # 变量
    config.set_variable("PIP_CACHE_DIR", "$CI_PROJECT_DIR/.cache/pip")
    config.set_cache([".cache/pip", "venv/"], key="${CI_COMMIT_REF_SLUG}")
    
    # Build任务
    config.add_job("build", {
        "stage": "build",
        "image": "python:3.11",
        "script": [
            "python -m venv venv",
            "source venv/bin/activate",
            "pip install -r requirements.txt",
            "pip install -e ."
        ],
        "artifacts": {
            "paths": ["venv/"],
            "expire_in": "1 hour"
        }
    })
    
    # Test任务
    config.add_job("test", {
        "stage": "test",
        "image": "python:3.11",
        "needs": ["build"],
        "script": [
            "source venv/bin/activate",
            "pytest --cov=src --cov-report=xml --cov-report=term"
        ],
        "coverage": "/TOTAL.+ ([0-9]+%)$/",
        "artifacts": {
            "reports": {"coverage_report": {"coverage_format": "cobertura", "path": "coverage.xml"}}
        }
    })
    
    # Deploy任务
    config.add_job("deploy_staging", {
        "stage": "deploy",
        "image": "python:3.11",
        "needs": ["test"],
        "script": ["echo 'Deploying to staging...'"],
        "environment": {
            "name": "staging",
            "url": "https://staging.example.com"
        },
        "only": ["develop"]
    })
    
    return config


def main():
    parser = argparse.ArgumentParser(description="GitLab CI Configuration Generator")
    parser.add_argument("--stages", default="build,test,deploy", help="Comma-separated stages")
    parser.add_argument("--output", default=".gitlab-ci.yml", help="Output file path")
    args = parser.parse_args()
    
    # 生成配置
    config = generate_python_pipeline()
    
    # 保存
    config.save(args.output)
    print(f"✅ GitLab CI configuration generated: {args.output}")


if __name__ == "__main__":
    main()
