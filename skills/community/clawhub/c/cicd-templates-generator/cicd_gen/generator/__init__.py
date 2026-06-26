"""Base generator class for CI/CD templates."""

import os
from abc import ABC, abstractmethod
from pathlib import Path


class BaseGenerator(ABC):
    """Abstract base class for CI/CD workflow generators."""

    LANGUAGES = {"python", "javascript", "go"}
    PYTHON_TEST_FRAMEWORKS = {"pytest", "unittest"}
    JS_TEST_FRAMEWORKS = {"jest", "mocha"}
    GO_TEST_FRAMEWORKS = {"go-test"}
    DEPLOY_OPTIONS = {"docker", "azure", "aliyun", "tencent", "k8s", "serverless"}
    RELEASE_OPTIONS = {"npm", "goreleaser"}

    def __init__(self):
        self.errors = []

    def validate(self, language, framework=None, test=None, deploy=None,
                 release=None, coverage=None, cloud=None):
        """Validate input parameters."""
        if language not in self.LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported: {', '.join(sorted(self.LANGUAGES))}"
            )

        if test:
            valid_tests = {
                "python": self.PYTHON_TEST_FRAMEWORKS,
                "javascript": self.JS_TEST_FRAMEWORKS,
                "go": self.GO_TEST_FRAMEWORKS,
            }.get(language, set())
            if test not in valid_tests:
                raise ValueError(
                    f"Unsupported test framework '{test}' for {language}. "
                    f"Supported: {', '.join(sorted(valid_tests))}"
                )

        if deploy and deploy not in self.DEPLOY_OPTIONS:
            raise ValueError(
                f"Unsupported deploy option: {deploy}. "
                f"Supported: {', '.join(sorted(self.DEPLOY_OPTIONS))}"
            )

        if release and release not in self.RELEASE_OPTIONS:
            raise ValueError(
                f"Unsupported release option: {release}. "
                f"Supported: {', '.join(sorted(self.RELEASE_OPTIONS))}"
            )

    def save(self, yaml_str, output_dir, filename="ci.yml"):
        """Save generated content to a file."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        file_path = out_path / filename
        file_path.write_text(yaml_str, encoding="utf-8")
        return str(file_path)

    @abstractmethod
    def generate(self, language, framework=None, test=None, deploy=None,
                 release=None, coverage=None, cloud=None, name="CI",
                 python_version="3.11", node_version="20", go_version="1.22",
                 **kwargs):
        """Generate CI/CD workflow content. Must be implemented by subclasses."""
        pass
