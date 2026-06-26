"""Jenkins Pipeline generator."""

from . import BaseGenerator


DOCKER_SCRIPT_BLOCK = """
        stage('Build & Push Docker') {{
            steps {{
                script {{
                    def img = docker.build("${{env.DOCKERHUB_USERNAME}}}/app")
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {{
                        img.push()
                    }}
                }}
            }}
        }}"""


class JenkinsGenerator(BaseGenerator):
    """Generator for Jenkins Pipeline (Jenkinsfile)."""

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
        test_cmd = self._python_test_cmd(test, coverage)
        deploy_block = self._python_deploy_block(deploy, cloud)

        return (
            "pipeline {\n"
            "    agent { docker { image 'python:" + python_version + "-slim' } }\n"
            "\n"
            "    stages {\n"
            "        stage('Checkout') {\n"
            "            steps { echo 'Cloning repository...' }\n"
            "        }\n"
            "\n"
            "        stage('Install') {\n"
            "            steps {\n"
            "                sh 'pip install -r requirements.txt'\n"
            "            }\n"
            "        }\n"
            "\n"
            "        stage('Test') {\n"
            "            steps {\n"
            "                sh '" + test_cmd + "'\n"
            "            }\n"
            "        }" + deploy_block + "\n"
            "    }\n"
            "}\n"
        )

    def _python_test_cmd(self, test, coverage):
        if test == "pytest":
            return "pytest --cov=. --cov-report=xml" if coverage else "pytest"
        elif test == "unittest":
            return "python -m unittest discover -v"

    def _python_deploy_block(self, deploy, cloud):
        if not deploy:
            return ""

        if deploy == "docker":
            return DOCKER_SCRIPT_BLOCK

        elif deploy == "azure":
            return """
        stage('Deploy to Azure') {
            steps {
                sh 'pip install azure-cli'
                sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID'
                sh 'az webapp up --name $AZURE_WEBAPP_NAME --location eastus'
            }
        }"""

        elif deploy == "k8s":
            return """
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }"""

        elif deploy == "serverless":
            return """
        stage('Deploy Serverless') {
            steps {
                sh 'npm install -g serverless'
                sh 'serverless deploy'
            }
        }"""

        return ""

    def _generate_javascript(self, framework, test, deploy, release,
                             node_version):
        test_cmd = "npm test" if test == "jest" else "npm run test:mocha"
        stages = self._js_stages(deploy, release)

        return (
            "pipeline {\n"
            "    agent { docker { image 'node:" + node_version + "' } }\n"
            "\n"
            "    stages {\n"
            "        stage('Checkout') {\n"
            "            steps { echo 'Cloning repository...' }\n"
            "        }\n"
            "\n"
            "        stage('Install') {\n"
            "            steps {\n"
            "                sh 'npm ci'\n"
            "            }\n"
            "        }\n"
            "\n"
            "        stage('Test') {\n"
            "            steps {\n"
            "                sh '" + test_cmd + "'\n"
            "            }\n"
            "        }" + stages + "\n"
            "    }\n"
            "}\n"
        )

    def _js_stages(self, deploy, release):
        result = ""
        if release == "npm":
            result += """
        stage('Publish npm') {
            steps {
                sh 'npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN'
                sh 'npm publish --access public'
            }
        }"""

        if deploy == "docker":
            result += DOCKER_SCRIPT_BLOCK

        return result

    def _generate_go(self, framework, test, release, deploy, go_version):
        deploy_block = self._go_deploy_block(release, deploy)

        return (
            "pipeline {\n"
            "    agent { docker { image 'golang:" + go_version + "' } }\n"
            "\n"
            "    stages {\n"
            "        stage('Checkout') {\n"
            "            steps { echo 'Cloning repository...' }\n"
            "        }\n"
            "\n"
            "        stage('Test') {\n"
            "            steps {\n"
            "                sh 'go test -v ./...'\n"
            "            }\n"
            "        }" + deploy_block + "\n"
            "    }\n"
            "}\n"
        )

    def _go_deploy_block(self, release, deploy):
        result = ""
        if release == "goreleaser":
            result += """
        stage('Release with GoReleaser') {
            steps {
                sh 'curl -sL https://git.io/goreleaser | bash'
            }
        }"""

        if deploy == "docker":
            result += DOCKER_SCRIPT_BLOCK

        return result
