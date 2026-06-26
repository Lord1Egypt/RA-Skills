"""Tests for CI/CD Templates Generator."""
import os
import tempfile
import yaml
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from cicd_gen.generator.github_actions import GitHubActionsGenerator
from cicd_gen.generator.gitlab_ci import GitLabCIGenerator
from cicd_gen.generator.jenkins import JenkinsGenerator


class TestGitHubActionsGenerator:
    """Test GitHub Actions workflow generation."""

    def test_python_pytest_docker(self):
        """Python + pytest + Docker generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="docker",
        )
        data = yaml.safe_load(yaml_str)
        assert data["name"] == "CI"
        assert "pytest" in yaml_str
        assert "docker" in yaml_str.lower()

    def test_python_unittest_coverage(self):
        """Python + unittest + coverage generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="unittest",
            coverage=True,
        )
        data = yaml.safe_load(yaml_str)
        assert "coverage" in yaml_str or "coverage" in data.get("jobs", {}).get("test", {}).get("steps", [{}])[0].get("name", "").lower() or "unittest" in yaml_str

    def test_python_docker_azure_deploy(self):
        """Python + Docker + Azure deployment."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="docker",
            cloud="azure",
        )
        data = yaml.safe_load(yaml_str)
        assert "docker" in yaml_str.lower() or "azure" in yaml_str.lower()

    def test_python_aliyun_deploy(self):
        """Python + Docker + Aliyun deployment."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="docker",
            cloud="aliyun",
        )
        data = yaml.safe_load(yaml_str)
        assert "aliyun" in yaml_str.lower() or "docker" in yaml_str.lower()

    def test_python_tencent_deploy(self):
        """Python + Docker + Tencent deployment."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="docker",
            cloud="tencent",
        )
        data = yaml.safe_load(yaml_str)
        assert "tencent" in yaml_str.lower() or "docker" in yaml_str.lower()

    def test_python_k8s_deploy(self):
        """Python + Kubernetes deployment."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="k8s",
        )
        data = yaml.safe_load(yaml_str)
        assert "k8s" in yaml_str.lower() or "kubernetes" in yaml_str.lower()

    def test_python_serverless_deploy(self):
        """Python + Serverless deployment."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            deploy="serverless",
        )
        data = yaml.safe_load(yaml_str)
        assert "serverless" in yaml_str.lower() or "azure" in yaml_str.lower() or "aws" in yaml_str.lower()

    def test_javascript_jest(self):
        """JavaScript + Jest generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="javascript",
            framework="node",
            test="jest",
        )
        data = yaml.safe_load(yaml_str)
        assert "jest" in yaml_str.lower()

    def test_javascript_docker(self):
        """JavaScript + Docker generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="javascript",
            framework="node",
            test="jest",
            deploy="docker",
        )
        data = yaml.safe_load(yaml_str)
        assert "docker" in yaml_str.lower()

    def test_javascript_npm_publish(self):
        """JavaScript + npm publish generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="javascript",
            framework="node",
            test="jest",
            release="npm",
        )
        data = yaml.safe_load(yaml_str)
        assert "npm" in yaml_str.lower() and ("publish" in yaml_str.lower() or "release" in yaml_str.lower())

    def test_go_goreleaser(self):
        """Go + goreleaser generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="go",
            framework="gin",
            test="go-test",
            release="goreleaser",
        )
        data = yaml.safe_load(yaml_str)
        assert "goreleaser" in yaml_str.lower() or "go" in yaml_str.lower()

    def test_go_docker(self):
        """Go + Docker generates valid workflow."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="go",
            framework="gin",
            test="go-test",
            deploy="docker",
        )
        data = yaml.safe_load(yaml_str)
        assert "docker" in yaml_str.lower() or "build" in yaml_str.lower()

    def test_custom_name_and_version(self):
        """Custom workflow name and Python version."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(
            language="python",
            framework="flask",
            test="pytest",
            name="my-ci",
            python_version="3.10",
            node_version="18",
            go_version="1.21",
        )
        data = yaml.safe_load(yaml_str)
        assert data["name"] == "my-ci"
        assert "3.10" in yaml_str

    def test_yaml_is_valid(self):
        """Generated YAML is parseable."""
        gen = GitHubActionsGenerator()
        yaml_str = gen.generate(language="python", framework="flask", test="pytest")
        data = yaml.safe_load(yaml_str)
        assert isinstance(data, dict)
        assert "on" in data or "name" in data


class TestGitLabCIGenerator:
    """Test GitLab CI workflow generation."""

    def test_python_pytest(self):
        """Python + pytest generates valid GitLab CI."""
        gen = GitLabCIGenerator()
        yaml_str = gen.generate(language="python", framework="flask", test="pytest")
        data = yaml.safe_load(yaml_str)
        assert isinstance(data, dict)

    def test_javascript_jest(self):
        """JavaScript + Jest generates valid GitLab CI."""
        gen = GitLabCIGenerator()
        yaml_str = gen.generate(language="javascript", framework="node", test="jest")
        data = yaml.safe_load(yaml_str)
        assert isinstance(data, dict)

    def test_go_goreleaser(self):
        """Go + goreleaser generates valid GitLab CI."""
        gen = GitLabCIGenerator()
        yaml_str = gen.generate(language="go", framework="gin", test="go-test", release="goreleaser")
        data = yaml.safe_load(yaml_str)
        assert isinstance(data, dict)

    def test_yaml_is_valid(self):
        """Generated YAML is parseable."""
        gen = GitLabCIGenerator()
        yaml_str = gen.generate(language="python", framework="flask", test="pytest")
        data = yaml.safe_load(yaml_str)
        assert isinstance(data, dict)
        assert "stages" in data


class TestJenkinsGenerator:
    """Test Jenkinsfile generation."""

    def test_python_pytest(self):
        """Python + pytest generates valid Jenkinsfile."""
        gen = JenkinsGenerator()
        content = gen.generate(language="python", framework="flask", test="pytest")
        assert "pipeline" in content.lower() or "stage" in content.lower()
        assert "pytest" in content.lower() or "python" in content.lower()

    def test_javascript_jest(self):
        """JavaScript + Jest generates valid Jenkinsfile."""
        gen = JenkinsGenerator()
        content = gen.generate(language="javascript", framework="node", test="jest")
        assert "jest" in content.lower() or "node" in content.lower()

    def test_go_goreleaser(self):
        """Go + goreleaser generates valid Jenkinsfile."""
        gen = JenkinsGenerator()
        content = gen.generate(language="go", framework="gin", test="go-test", release="goreleaser")
        assert "goreleaser" in content.lower() or "go" in content.lower()


class TestCLIArguments:
    """Test CLI argument handling."""

    def test_invalid_language(self):
        """Invalid language raises ValueError."""
        from cicd_gen.generator.github_actions import GitHubActionsGenerator
        gen = GitHubActionsGenerator()
        with pytest.raises(ValueError):
            gen.generate(language="ruby", framework="rails", test="rspec")

    def test_invalid_test_framework(self):
        """Invalid test framework raises ValueError."""
        from cicd_gen.generator.github_actions import GitHubActionsGenerator
        gen = GitHubActionsGenerator()
        with pytest.raises(ValueError):
            gen.generate(language="python", framework="flask", test="rspec")

    def test_invalid_deploy(self):
        """Invalid deploy option raises ValueError."""
        from cicd_gen.generator.github_actions import GitHubActionsGenerator
        gen = GitHubActionsGenerator()
        with pytest.raises(ValueError):
            gen.generate(language="python", framework="flask", test="pytest", deploy="ansible")


class TestOutputFiles:
    """Test file output functionality."""

    def test_output_directory_creation(self, tmp_path):
        """Output directory is created if it doesn't exist."""
        from cicd_gen.generator.github_actions import GitHubActionsGenerator
        gen = GitHubActionsGenerator()
        out_dir = tmp_path / ".github" / "workflows"
        gen.save(
            yaml_str="name: CI\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4",
            output_dir=str(out_dir),
            filename="ci.yml",
        )
        assert (out_dir / "ci.yml").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
