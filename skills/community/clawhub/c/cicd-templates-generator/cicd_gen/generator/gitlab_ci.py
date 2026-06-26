"""GitLab CI workflow generator."""

import yaml
from . import BaseGenerator


class GitLabCIGenerator(BaseGenerator):
    """Generator for GitLab CI/CD pipelines."""

    def generate(self, language, framework=None, test=None, deploy=None,
                 release=None, coverage=None, cloud=None, name="CI",
                 python_version="3.11", node_version="20", go_version="1.22",
                 **kwargs):
        self.validate(language, framework, test, deploy, release)

        if language == "python":
            return self._generate_python(framework, test, coverage, deploy,
                                          cloud, python_version)
        elif language == "javascript":
            return self._generate_javascript(framework, test, deploy, release,
                                             node_version)
        elif language == "go":
            return self._generate_go(framework, test, release, deploy,
                                     go_version)

    def _generate_python(self, framework, test, coverage, deploy, cloud,
                          python_version):
        stages = ["test", "deploy"]
        if coverage:
            stages.insert(1, "coverage")

        image = f"python:{python_version}-slim"

        test_script = []
        if test == "pytest":
            test_script.append("pip install pytest pytest-cov")
            cov = "pytest --cov=. --cov-report=xml" if coverage else "pytest"
            test_script.append(cov)
        elif test == "unittest":
            test_script.append("pip install coverage")
            cov = "python -m coverage run -m unittest discover" if coverage \
                else "python -m unittest discover"
            test_script.append(cov)

        if coverage:
            test_job = {
                "image": image,
                "stage": "coverage",
                "script": test_script + [
                    "coverage xml",
                ],
                "coverage": "/TOTAL.*\\s+(\\d+%)$/",
                "artifacts": {"reports": {"cobertura": "coverage.xml"}},
            }
        else:
            test_job = {"image": image, "stage": "test", "script": test_script}

        deploy_job = None
        if deploy == "docker":
            deploy_job = {
                "image": {"name": "docker:latest", "entrypoint": [""]},
                "stage": "deploy",
                "services": ["docker:dind"],
                "script": [
                    "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY",
                    "docker build -t $CI_REGISTRY_IMAGE:latest .",
                    "docker push $CI_REGISTRY_IMAGE:latest",
                ],
            }
        elif deploy == "k8s":
            deploy_job = {
                "image": {"name": "bitnami/kubectl:latest", "entrypoint": [""]},
                "stage": "deploy",
                "script": [
                    "kubectl apply -f k8s/",
                    "-n default",
                ],
            }
        elif cloud == "azure":
            deploy_job = {
                "image": image,
                "stage": "deploy",
                "script": [
                    "pip install azure-cli",
                    "az login --service-principal -u $AZURE_CLIENT_ID "
                    "-p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID",
                    "az webapp up --name $AZURE_WEBAPP_NAME --location eastus",
                ],
            }

        pipeline = {
            "stages": stages if coverage or deploy else ["test"],
        }
        pipeline["test"] = test_job
        if coverage:
            pipeline["coverage"] = {
                "image": image, "stage": "coverage",
                "script": ["curl -s https://codecov.io/bash | bash"],
                "needs": ["test"],
            }
        if deploy_job:
            deploy_job["needs"] = ["test"]
            pipeline["deploy"] = deploy_job

        return yaml.dump(pipeline, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)

    def _generate_javascript(self, framework, test, deploy, release,
                              node_version):
        stages = ["test"]
        if release or deploy:
            stages.append("deploy")

        image = f"node:{node_version}-slim"

        test_script = []
        if test == "jest":
            test_script.append("npm ci")
            test_script.append("npm test")
        elif test == "mocha":
            test_script.append("npm ci")
            test_script.append("npm run test:mocha")

        test_job = {"image": image, "stage": "test", "script": test_script}

        deploy_job = None
        if release == "npm":
            deploy_job = {
                "image": image,
                "stage": "deploy",
                "script": [
                    "npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN",
                    "npm publish --access public",
                ],
                "only": ["tags"],
            }
        elif deploy == "docker":
            deploy_job = {
                "image": {"name": "docker:latest", "entrypoint": [""]},
                "stage": "deploy",
                "services": ["docker:dind"],
                "script": [
                    "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY",
                    "docker build -t $CI_REGISTRY_IMAGE:latest .",
                    "docker push $CI_REGISTRY_IMAGE:latest",
                ],
            }

        pipeline = {"stages": stages}
        pipeline["test"] = test_job
        if deploy_job:
            deploy_job["needs"] = ["test"]
            pipeline["deploy"] = deploy_job

        return yaml.dump(pipeline, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)

    def _generate_go(self, framework, test, release, deploy, go_version):
        stages = ["test"]
        if release or deploy:
            stages.append("deploy")

        test_job = {
            "image": f"golang:{go_version}-alpine",
            "stage": "test",
            "script": [
                "apk add --no-cache git",
                "go test -v ./...",
            ],
        }

        deploy_job = None
        if release == "goreleaser":
            deploy_job = {
                "image": {"name": "goreleaser/goreleaser:latest", "entrypoint": [""]},
                "stage": "deploy",
                "script": ["goreleaser release --clean --snapshot"],
                "only": ["tags"],
            }
        elif deploy == "docker":
            deploy_job = {
                "image": {"name": "docker:latest", "entrypoint": [""]},
                "stage": "deploy",
                "services": ["docker:dind"],
                "script": [
                    "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY",
                    "docker build -t $CI_REGISTRY_IMAGE:latest .",
                    "docker push $CI_REGISTRY_IMAGE:latest",
                ],
            }

        pipeline = {"stages": stages, "test": test_job}
        if deploy_job:
            deploy_job["needs"] = ["test"]
            pipeline["deploy"] = deploy_job

        return yaml.dump(pipeline, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)
