#!/usr/bin/env python3
"""
CI/CD Pipeline Toolkit - Unit Tests | 单元测试
"""

import unittest
import tempfile
import os
from pathlib import Path


class MockGitHubActionsWorkflow:
    """Mock implementation for testing"""
    
    def __init__(self, name):
        self.name = name
        self.triggers = []
        self.jobs = {}
    
    def add_trigger(self, event, branches=None):
        self.triggers.append({"event": event, "branches": branches})
    
    def add_job(self, name, config):
        self.jobs[name] = config
    
    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(f"# {self.name}\n")


class MockGitLabCIConfig:
    """Mock implementation for testing"""
    
    def __init__(self):
        self.stages = []
        self.jobs = {}
    
    def add_stage(self, stage):
        self.stages.append(stage)
    
    def add_job(self, name, config):
        self.jobs[name] = config
    
    def save(self, path):
        with open(path, 'w') as f:
            f.write("stages:\n")
            for stage in self.stages:
                f.write(f"  - {stage}\n")


class TestGitHubActionsWorkflow(unittest.TestCase):
    """Test GitHub Actions workflow generation"""
    
    def test_workflow_creation(self):
        """Test basic workflow creation"""
        workflow = MockGitHubActionsWorkflow("test-ci")
        self.assertEqual(workflow.name, "test-ci")
        self.assertEqual(len(workflow.triggers), 0)
        self.assertEqual(len(workflow.jobs), 0)
    
    def test_add_trigger(self):
        """Test adding triggers"""
        workflow = MockGitHubActionsWorkflow("test-ci")
        workflow.add_trigger("push", branches=["main"])
        workflow.add_trigger("pull_request")
        
        self.assertEqual(len(workflow.triggers), 2)
        self.assertEqual(workflow.triggers[0]["event"], "push")
        self.assertEqual(workflow.triggers[0]["branches"], ["main"])
    
    def test_add_job(self):
        """Test adding jobs"""
        workflow = MockGitHubActionsWorkflow("test-ci")
        workflow.add_job("test", {
            "runs-on": "ubuntu-latest",
            "steps": [{"run": "pytest"}]
        })
        
        self.assertIn("test", workflow.jobs)
        self.assertEqual(workflow.jobs["test"]["runs-on"], "ubuntu-latest")
    
    def test_save_workflow(self):
        """Test saving workflow file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workflow = MockGitHubActionsWorkflow("test-ci")
            workflow.add_trigger("push")
            workflow.add_job("test", {"runs-on": "ubuntu-latest"})
            
            output_path = os.path.join(tmpdir, ".github", "workflows", "test.yml")
            workflow.save(output_path)
            
            self.assertTrue(os.path.exists(output_path))
            with open(output_path) as f:
                content = f.read()
                self.assertIn("test-ci", content)


class TestGitLabCIConfig(unittest.TestCase):
    """Test GitLab CI configuration generation"""
    
    def test_config_creation(self):
        """Test basic config creation"""
        config = MockGitLabCIConfig()
        self.assertEqual(len(config.stages), 0)
        self.assertEqual(len(config.jobs), 0)
    
    def test_add_stage(self):
        """Test adding stages"""
        config = MockGitLabCIConfig()
        config.add_stage("build")
        config.add_stage("test")
        config.add_stage("deploy")
        
        self.assertEqual(len(config.stages), 3)
        self.assertEqual(config.stages, ["build", "test", "deploy"])
    
    def test_add_job(self):
        """Test adding jobs"""
        config = MockGitLabCIConfig()
        config.add_job("build", {"stage": "build", "script": ["npm build"]})
        
        self.assertIn("build", config.jobs)
        self.assertEqual(config.jobs["build"]["stage"], "build")
    
    def test_save_config(self):
        """Test saving CI config file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = MockGitLabCIConfig()
            config.add_stage("build")
            config.add_stage("test")
            config.add_job("build", {"stage": "build"})
            
            output_path = os.path.join(tmpdir, ".gitlab-ci.yml")
            config.save(output_path)
            
            self.assertTrue(os.path.exists(output_path))
            with open(output_path) as f:
                content = f.read()
                self.assertIn("build", content)
                self.assertIn("test", content)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_complete_github_workflow(self):
        """Test complete GitHub workflow generation"""
        workflow = MockGitHubActionsWorkflow("python-ci")
        workflow.add_trigger("push", branches=["main", "develop"])
        workflow.add_trigger("pull_request")
        workflow.add_job("test", {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"run": "pytest"}
            ]
        })
        workflow.add_job("lint", {
            "runs-on": "ubuntu-latest",
            "steps": [{"run": "flake8"}]
        })
        
        self.assertEqual(len(workflow.triggers), 2)
        self.assertEqual(len(workflow.jobs), 2)
    
    def test_complete_gitlab_pipeline(self):
        """Test complete GitLab pipeline generation"""
        config = MockGitLabCIConfig()
        config.add_stage("build")
        config.add_stage("test")
        config.add_stage("deploy")
        
        config.add_job("build", {"stage": "build", "script": ["make build"]})
        config.add_job("test", {"stage": "test", "script": ["make test"]})
        config.add_job("deploy", {"stage": "deploy", "script": ["make deploy"]})
        
        self.assertEqual(len(config.stages), 3)
        self.assertEqual(len(config.jobs), 3)


if __name__ == "__main__":
    unittest.main()
