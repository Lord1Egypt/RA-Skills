"""GitHub Actions workflow generator."""

import yaml
from . import BaseGenerator


class GitHubActionsGenerator(BaseGenerator):
    """Generator for GitHub Actions workflows."""

    def generate(self, language, framework=None, test=None, deploy=None,
                 release=None, coverage=None, cloud=None, name="CI",
                 python_version="3.11", node_version="20", go_version="1.22",
                 **kwargs):
        self.validate(language, framework, test, deploy, release)

        if language == "python":
            return self._generate_python(
                framework, test, deploy, coverage, cloud, name, python_version
            )
        elif language == "javascript":
            return self._generate_javascript(
                framework, test, deploy, release, name, node_version
            )
        elif language == "go":
            return self._generate_go(
                framework, test, deploy, release, name, go_version
            )

    def _generate_python(self, framework, test, deploy, coverage, cloud,
                         name, python_version):
        workflow = {
            "name": name,
            "on": {"push": {"branches": ["main", "master"]},
                   "pull_request": {"branches": ["main", "master"]}},
        }

        jobs = {}

        # Pure Docker deploy: add Docker build+push to test job
        if deploy == "docker" and cloud is None:
            test_job = self._build_python_test_job(
                framework, test, coverage, deploy, cloud, python_version
            )
            docker_steps = self._docker_build_push_steps()
            test_job["steps"].extend(docker_steps)
            jobs["test"] = test_job
        else:
            test_job = self._build_python_test_job(
                framework, test, coverage, deploy, cloud, python_version
            )
            jobs["test"] = test_job

            if deploy and deploy != "docker":
                deploy_job = self._build_python_deploy_job(
                    framework, deploy, cloud, python_version
                )
                jobs["deploy"] = deploy_job
                test_job["needs"] = ["deploy"]
            elif deploy == "docker" and cloud:
                # Docker + cloud: create a combined deploy job
                deploy_job = self._build_docker_plus_cloud_job(
                    cloud, python_version
                )
                jobs["deploy"] = deploy_job
                test_job["needs"] = ["deploy"]

        workflow["jobs"] = jobs
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)

    def _build_python_test_job(self, framework, test, coverage, deploy, cloud,
                                python_version):
        steps = [
            {"name": "Checkout code", "uses": "actions/checkout@v4"},
            {
                "name": f"Set up Python {python_version}",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": python_version},
            },
            {"name": "Install dependencies",
             "run": "pip install -r requirements.txt" +
                    (" pytest pytest-cov" if test == "pytest" and coverage else
                     " pytest" if test == "pytest" else "")},
        ]

        if test == "pytest":
            cov_cmd = "pytest --cov=. --cov-report=xml" if coverage else "pytest"
            steps.append({"name": "Run tests", "run": cov_cmd})
        elif test == "unittest":
            cov_flag = " --coverage" if coverage else ""
            steps.append({
                "name": "Run unittest",
                "run": f"python -m unittest discover -v{cov_flag}"
            })

        if coverage:
            steps.append({
                "name": "Upload coverage",
                "uses": "codecov/codecov-action@v4",
                "with": {"token": "${{ secrets.CODECOV_TOKEN }}"},
            })

        return {
            "runs-on": "ubuntu-latest",
            "steps": steps,
        }

    def _docker_build_push_steps(self):
        return [
            {
                "name": "Log in to Docker Hub",
                "uses": "docker/login-action@v3",
                "with": {
                    "username": "${{ secrets.DOCKERHUB_USERNAME }}",
                    "password": "${{ secrets.DOCKERHUB_TOKEN }}",
                },
            },
            {
                "name": "Build and push Docker image",
                "uses": "docker/build-push-action@v5",
                "with": {
                    "context": ".",
                    "push": True,
                    "tags": "${{ secrets.DOCKERHUB_USERNAME }}/app:latest",
                },
            },
        ]

    def _build_python_deploy_job(self, framework, deploy, cloud, python_version):
        steps = [
            {"name": "Checkout code", "uses": "actions/checkout@v4"},
            {
                "name": f"Set up Python {python_version}",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": python_version},
            },
            {"name": "Install dependencies",
             "run": "pip install -r requirements.txt"},
        ]

        if deploy == "azure":
            steps.extend([
                {"name": "Login to Azure",
                 "uses": "azure/login@v2",
                 "with": {"creds": "${{ secrets.AZURE_CREDENTIALS }}"}},
                {"name": "Deploy to Azure Web App",
                 "uses": "azure/webapps-deploy@v3",
                 "with": {
                     "app-name": "${{ secrets.AZURE_WEBAPP_NAME }}",
                     "slot-name": "production",
                     "publish-profile": "${{ secrets.AZURE_PUBLISH_PROFILE }}",
                 }},
            ])
        elif deploy == "aliyun":
            steps.extend([
                {"name": "Setup Aliyun CLI",
                 "uses": "montagestudio/aliyun-cli@v3",
                 "with": {"access-key-id": "${{ secrets.ALIYUN_ACCESS_KEY_ID }}",
                          "access-key-secret": "${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}",
                          "region": "cn-beijing"}},
                {"name": "Deploy to Aliyun ECS",
                 "run": "aliyun ecs DeployInstance --instance-id ${{ secrets.ALIYUN_INSTANCE_ID }}"},
            ])
        elif deploy == "tencent":
            steps.extend([
                {"name": "Setup Tencent Cloud CLI",
                 "run": "pip install tccli"},
                {"name": "Deploy to Tencent Cloud",
                 "run": "tccli cls deploy --region ap-guangzhou"},
            ])
        elif deploy == "k8s":
            steps.extend([
                {"name": "Configure kubectl",
                 "uses": "azure/k8s-set-context@v3",
                 "with": {"kubeconfig": "${{ secrets.KUBE_CONFIG }}"}},
                {"name": "Deploy to Kubernetes",
                 "uses": "azure/k8s-deploy@v5",
                 "with": {"manifests": "k8s/", "namespace": "default"}},
            ])
        elif deploy == "serverless":
            steps.extend([
                {"name": "Install serverless framework",
                 "run": "npm install -g serverless"},
                {"name": "Deploy serverless app",
                 "run": "serverless deploy",
                 "env": {"AWS_ACCESS_KEY_ID": "${{ secrets.AWS_ACCESS_KEY_ID }}",
                         "AWS_SECRET_ACCESS_KEY": "${{ secrets.AWS_SECRET_ACCESS_KEY }}"}},
            ])

        return {"runs-on": "ubuntu-latest", "steps": steps}

    def _build_docker_plus_cloud_job(self, cloud, python_version):
        steps = [
            {"name": "Checkout code", "uses": "actions/checkout@v4"},
            {
                "name": f"Set up Python {python_version}",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": python_version},
            },
            {"name": "Install dependencies",
             "run": "pip install -r requirements.txt"},
        ]

        # Docker build + push
        steps.extend([
            {
                "name": "Log in to Docker Hub",
                "uses": "docker/login-action@v3",
                "with": {
                    "username": "${{ secrets.DOCKERHUB_USERNAME }}",
                    "password": "${{ secrets.DOCKERHUB_TOKEN }}",
                },
            },
            {
                "name": "Build and push Docker image",
                "uses": "docker/build-push-action@v5",
                "with": {
                    "context": ".",
                    "push": True,
                    "tags": "${{ secrets.DOCKERHUB_USERNAME }}/app:latest",
                },
            },
        ])

        # Cloud-specific deployment steps
        if cloud == "azure":
            steps.extend([
                {"name": "Login to Azure",
                 "uses": "azure/login@v2",
                 "with": {"creds": "${{ secrets.AZURE_CREDENTIALS }}"}},
                {"name": "Deploy to Azure Web App",
                 "uses": "azure/webapps-deploy@v3",
                 "with": {
                     "app-name": "${{ secrets.AZURE_WEBAPP_NAME }}",
                     "slot-name": "production",
                     "publish-profile": "${{ secrets.AZURE_PUBLISH_PROFILE }}",
                 }},
            ])
        elif cloud == "aliyun":
            steps.extend([
                {"name": "Setup Aliyun CLI",
                 "uses": "montagestudio/aliyun-cli@v3",
                 "with": {
                     "access-key-id": "${{ secrets.ALIYUN_ACCESS_KEY_ID }}",
                     "access-key-secret": "${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}",
                     "region": "cn-beijing"}},
                {"name": "Deploy to Aliyun ECS",
                 "run": "aliyun ecs DeployInstance --instance-id ${{ secrets.ALIYUN_INSTANCE_ID }}"},
            ])
        elif cloud == "tencent":
            steps.extend([
                {"name": "Setup Tencent Cloud CLI",
                 "run": "pip install tccli"},
                {"name": "Deploy to Tencent Cloud",
                 "run": "tccli cls deploy --region ap-guangzhou"},
            ])

        return {"runs-on": "ubuntu-latest", "steps": steps}

    def _generate_javascript(self, framework, test, deploy, release, name,
                              node_version):
        workflow = {
            "name": name,
            "on": {"push": {"branches": ["main", "master"]},
                   "pull_request": {"branches": ["main", "master"]}},
        }

        jobs = {}
        test_job = self._build_js_test_job(
            framework, test, deploy, release, node_version
        )
        jobs["test"] = test_job

        if release == "npm":
            jobs["publish"] = self._build_npm_publish_job(node_version)
            jobs["publish"]["needs"] = ["test"]

        if deploy == "docker":
            jobs["docker"] = self._build_docker_job(node_version)
            jobs["docker"]["needs"] = ["test"]

        if deploy in ("azure", "aliyun", "tencent"):
            jobs["deploy"] = self._build_js_cloud_deploy_job(deploy, node_version)
            jobs["deploy"]["needs"] = ["test"]

        workflow["jobs"] = jobs
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)

    def _build_js_test_job(self, framework, test, deploy, release,
                             node_version):
        steps = [
            {"name": "Checkout code", "uses": "actions/checkout@v4"},
            {
                "name": f"Set up Node.js {node_version}",
                "uses": "actions/setup-node@v4",
                "with": {"node-version": node_version,
                         "cache": "npm"},
            },
            {"name": "Install dependencies", "run": "npm ci"},
        ]

        if test == "jest":
            steps.append({"name": "Run Jest tests", "run": "npm test"})
        elif test == "mocha":
            steps.append({"name": "Run Mocha tests",
                          "run": "npm run test:mocha"})

        return {"runs-on": "ubuntu-latest", "steps": steps}

    def _build_npm_publish_job(self, node_version):
        return {
            "runs-on": "ubuntu-latest",
            "needs": ["test"],
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {
                    "name": f"Set up Node.js {node_version}",
                    "uses": "actions/setup-node@v4",
                    "with": {"node-version": node_version,
                             "registry-url": "https://registry.npmjs.org"},
                },
                {"name": "Publish to npm",
                 "run": "npm publish",
                 "env": {"NODE_AUTH_TOKEN": "${{ secrets.NPM_TOKEN }}"}},
            ],
        }

    def _build_docker_job(self, node_version):
        return {
            "runs-on": "ubuntu-latest",
            "needs": ["test"],
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {"name": "Log in to Docker Hub",
                 "uses": "docker/login-action@v3",
                 "with": {"username": "${{ secrets.DOCKERHUB_USERNAME }}",
                          "password": "${{ secrets.DOCKERHUB_TOKEN }}"}},
                {
                    "name": "Build and push Docker image",
                    "uses": "docker/build-push-action@v5",
                    "with": {
                        "context": ".",
                        "push": True,
                        "tags": "${{ secrets.DOCKERHUB_USERNAME }}/app:latest",
                    },
                },
            ],
        }

    def _build_js_cloud_deploy_job(self, cloud, node_version):
        steps = [
            {"name": "Checkout code", "uses": "actions/checkout@v4"},
            {
                "name": f"Set up Node.js {node_version}",
                "uses": "actions/setup-node@v4",
                "with": {"node-version": node_version},
            },
            {"name": "Install dependencies", "run": "npm ci"},
        ]

        if cloud == "azure":
            steps.extend([
                {"name": "Login to Azure",
                 "uses": "azure/login@v2",
                 "with": {"creds": "${{ secrets.AZURE_CREDENTIALS }}"}},
                {"name": "Deploy to Azure Web App",
                 "uses": "azure/webapps-deploy@v3",
                 "with": {"app-name": "${{ secrets.AZURE_WEBAPP_NAME }}",
                          "slot-name": "production"}},
            ])
        elif cloud == "aliyun":
            steps.extend([
                {"name": "Setup Aliyun CLI",
                 "uses": "montagestudio/aliyun-cli@v3",
                 "with": {"access-key-id": "${{ secrets.ALIYUN_ACCESS_KEY_ID }}",
                          "access-key-secret": "${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}"}},
            ])
        elif cloud == "tencent":
            steps.extend([
                {"name": "Setup Tencent Cloud CLI", "run": "pip install tccli"},
            ])

        return {"runs-on": "ubuntu-latest", "needs": ["test"], "steps": steps}

    def _generate_go(self, framework, test, deploy, release, name, go_version):
        workflow = {
            "name": name,
            "on": {"push": {"branches": ["main", "master"]},
                   "pull_request": {"branches": ["main", "master"]}},
        }

        jobs = {}
        test_job = self._build_go_test_job(framework, test, go_version)
        jobs["test"] = test_job

        if release == "goreleaser":
            jobs["release"] = self._build_goreleaser_job(go_version)
            jobs["release"]["needs"] = ["test"]

        if deploy == "docker":
            jobs["docker"] = self._build_go_docker_job(go_version)
            jobs["docker"]["needs"] = ["test"]

        workflow["jobs"] = jobs
        return yaml.dump(workflow, default_flow_style=False, sort_keys=False,
                         allow_unicode=True)

    def _build_go_test_job(self, framework, test, go_version):
        return {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {
                    "name": f"Set up Go {go_version}",
                    "uses": "actions/setup-go@v5",
                    "with": {"go-version": go_version},
                },
                {"name": "Run tests", "run": "go test -v ./..."},
            ],
        }

    def _build_goreleaser_job(self, go_version):
        return {
            "runs-on": "ubuntu-latest",
            "needs": ["test"],
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {
                    "name": f"Set up Go {go_version}",
                    "uses": "actions/setup-go@v5",
                    "with": {"go-version": go_version},
                },
                {"name": "Run GoReleaser",
                 "uses": "goreleaser/goreleaser-action@v5",
                 "with": {"version": "latest",
                          "args": "release --clean"},
                 "env": {"GITHUB_TOKEN": "${{ secrets.GITHUB_TOKEN }}"}},
            ],
        }

    def _build_go_docker_job(self, go_version):
        return {
            "runs-on": "ubuntu-latest",
            "needs": ["test"],
            "steps": [
                {"name": "Checkout code", "uses": "actions/checkout@v4"},
                {"name": "Log in to Docker Hub",
                 "uses": "docker/login-action@v3",
                 "with": {"username": "${{ secrets.DOCKERHUB_USERNAME }}",
                          "password": "${{ secrets.DOCKERHUB_TOKEN }}"}},
                {
                    "name": "Build and push Docker image",
                    "uses": "docker/build-push-action@v5",
                    "with": {
                        "context": ".",
                        "push": True,
                        "tags": "${{ secrets.DOCKERHUB_USERNAME }}/app:latest",
                    },
                },
            ],
        }
