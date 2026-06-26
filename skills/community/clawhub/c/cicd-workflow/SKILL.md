---
name: cicd-workflow
description: CI/CD workflow skill for Java + Vue projects. Supports GitLab CI and Jenkins pipelines with code linting, unit testing, build packaging, Docker image building, Kubernetes deployment, and notification feedback. Use when: (1) Setting up CI/CD pipelines for Java/Vue projects, (2) Configuring GitLab CI or Jenkins workflows, (3) Building Docker images and deploying to Kubernetes, (4) Implementing automated code quality checks and testing, (5) Setting up deployment notifications.
---

# CI/CD Workflow Skill

Complete CI/CD pipeline templates for Java + Vue full-stack projects, supporting GitLab CI and Jenkins with Kubernetes deployment.

## Interactive Configuration (NEW)

This skill supports interactive step-by-step configuration with numbered options.

### Configuration Flow

```
1. Choose Platform (GitLab CI / Jenkins)
        ↓
2. Choose Project Type (Java / Vue / Java+Vue)
        ↓
3. Choose Deployment Target (K8s / Docker / SSH)
        ↓
4. Choose Trigger Method (Manual / Auto / Scheduled)
        ↓
5. Choose Pipeline Steps (Multi-select)
        ↓
6. Generate Configuration
```

### Step 1: Platform

| # | Platform | Config File |
|---|----------|-------------|
| 1 | **GitLab CI** | `.gitlab-ci.yml` |
| 2 | **Jenkins** | `Jenkinsfile` |

### Step 2: Project Type

| # | Type | Description |
|---|------|-------------|
| 1 | **Java Backend** | Spring Boot project only |
| 2 | **Vue Frontend** | Vue.js project only |
| 3 | **Java + Vue Fullstack** | Both backend and frontend |

### Step 3: Deployment Target

| # | Target | Description |
|---|--------|-------------|
| 1 | **Kubernetes** | Deploy to K8s cluster with kubectl |
| 2 | **Docker Server** | Deploy to Docker host |
| 3 | **Traditional Server (SSH)** | Deploy via SSH to remote server |

### Step 4: Trigger Method

| # | Method | Description |
|---|--------|-------------|
| 1 | **Manual** | Trigger by "Build Now" button |
| 2 | **Push Auto** | Trigger on every push |
| 3 | **Scheduled** | Trigger by cron schedule |

### Step 5: Pipeline Steps (Multi-select)

| # | Step | Description |
|---|------|-------------|
| 1 | **Lint** | Code quality checks |
| 2 | **Test** | Unit tests with coverage |
| 3 | **Build** | Compile and package |
| 4 | **Dockerize** | Build and push Docker images |
| 5 | **Deploy** | Deploy to target environment |
| 6 | **Notify** | Send notifications |

### Input Format

**Complete in one line:**
```
Platform,Project,Target,Trigger,Steps
```

**Examples:**
- `1,3,1,1,123456` = GitLab CI + Java/Vue + K8s + Manual + All steps
- `2,1,3,1,12356` = Jenkins + Java + SSH + Manual + No Docker
- `1,2,1,2,123456` = GitLab CI + Vue + K8s + Auto trigger + All steps

**Or step by step:**
Reply with one number at a time, the skill will guide you through each step.

## Generated Output

When generating CI/CD configuration, this skill produces a complete package including:

### For Jenkins
```
cicd-output/
├── Jenkinsfile.txt          # Pipeline configuration (rename to Jenkinsfile when using)
├── setup-guide.md           # Complete setup instructions
├── systemd/
│   └── [app-name].service   # systemd service file (for SSH deployment)
└── README.md                # Quick reference
```

### For GitLab CI
```
cicd-output/
├── .gitlab-ci.yml.txt       # Pipeline configuration (rename to .gitlab-ci.yml when using)
├── setup-guide.md           # Complete setup instructions
├── docker-compose.yml       # Local development setup
└── README.md                # Quick reference
```

### Setup Guide Contents

The automatically generated `setup-guide.md` includes:

**1. Prerequisites**
- Required Jenkins/GitLab version
- Required plugins and extensions
- Server/environment requirements

**2. Credential Configuration**
- Detailed list of required credentials
- Step-by-step credential creation guide
- Security best practices

**3. Platform-Specific Setup**
- Jenkins: Pipeline job creation, plugin installation
- GitLab CI: Runner setup, variable configuration

**4. Deployment Target Setup**
- Kubernetes: Cluster access, namespace setup
- Docker: Registry configuration, daemon setup
- SSH: User creation, key exchange, systemd service

**5. Troubleshooting**
- Common errors and solutions
- Debug tips and log locations
- Verification steps

**6. Customization Guide**
- How to modify environment variables
- How to add custom stages
- How to adjust resource limits

## Pipeline Stages

1. **Prepare** - 环境检查和初始化
2. **Lint** - 代码质量检查 (SpotBugs, PMD, Checkstyle for Java; ESLint, Prettier for Vue)
3. **Test** - 单元测试与覆盖率报告
4. **Build** - 编译打包，同时进行**静态资源安全扫描**
5. **Security Scan** - Trivy 镜像安全扫描（可选）
6. **Dockerize** - 构建并推送 Docker 镜像
7. **Deploy** - 部署到 Kubernetes 集群
8. **Notify** - 发送部署状态通知

## Supported Platforms

- **GitLab CI** (`.gitlab-ci.yml`)
- **Jenkins** (`Jenkinsfile`)

## Quick Start

### GitLab CI

1. Copy `assets/gitlab-ci.yml.txt` to your project root as `.gitlab-ci.yml`
2. Update variables in the file:
   - `DOCKER_REGISTRY` - Your Docker registry URL
   - `DOCKER_NAMESPACE` - Your registry namespace
   - `K8S_NAMESPACE` - Kubernetes namespace
3. Configure CI/CD variables in GitLab:
   - `CI_REGISTRY_USER` / `CI_REGISTRY_PASSWORD` - Docker registry credentials
   - `KUBE_CONFIG` - Base64 encoded kubeconfig
   - `WEBHOOK_URL` - Notification webhook URL
4. Push to trigger pipeline (manual trigger for dockerize and deploy stages)

### Jenkins

1. Copy `assets/Jenkinsfile.txt` to your project root as `Jenkinsfile`
2. Install recommended plugins:
   - Pipeline
   - Docker Pipeline
   - Kubernetes CLI
   - JUnit (for test results)
   - JaCoCo (optional, for coverage)
   - HTTP Request (for notifications)
3. Create Jenkins credentials:
   - `docker-registry-credentials` - Docker registry login (username/password)
   - `kubeconfig` - Kubernetes config file (secret file)
   - `webhook-url` - Notification webhook URL (secret text)
4. Create a new Pipeline job pointing to your repository
5. Run manually via "Build Now"

**Jenkinsfile Features:**
- ✅ Conditional builds based on file changes (`when { changeset }`)
- ✅ Static resource security scan during build
- ✅ Graceful handling of missing plugins
- ✅ Resource limits for Docker agents
- ✅ Multi-environment deployment support
- ✅ Rich notification cards for Feishu/DingTalk

## Project Structure

```
project-root/
├── backend/              # Java Spring Boot project
│   ├── src/
│   ├── pom.xml
│   └── Dockerfile        # Copy from assets/Dockerfile.java.txt
├── frontend/             # Vue.js project
│   ├── src/
│   ├── package.json
│   └── Dockerfile        # Copy from assets/Dockerfile.vue.txt
├── .gitlab-ci.yml        # Copy from assets/.gitlab-ci.yml.txt
├── Jenkinsfile           # Copy from assets/Jenkinsfile.txt
└── k8s/
    └── deployment.yml    # Kubernetes manifests (from assets/)
```

## Assets Reference

### Dockerfiles

- `assets/Dockerfile.java.txt` - Java backend Docker image (multi-stage, Alpine-based)
- `assets/Dockerfile.vue.txt` - Vue frontend Docker image (multi-stage, Nginx-based)

**Note:** Rename `.txt` files to remove the extension when using in your project.
- `Dockerfile.java.txt` → `Dockerfile`
- `Dockerfile.vue.txt` → `Dockerfile`

### Security Features

#### 1. Static Resource Security (Vue Projects)

**自动排除的文件类型：**
- `.vue` - Vue 单文件组件源码
- `*.config.js/ts/mjs/cjs/json` - 各种配置文件
- `vite.config.*` - Vite 配置
- `webpack.config.*` - Webpack 配置
- `babel.config.*` - Babel 配置
- `tailwind.config.*` - Tailwind 配置
- `postcss.config.*` - PostCSS 配置
- `eslint.config.*` / `.eslintrc.*` - ESLint 配置
- `.prettierrc.*` - Prettier 配置
- `*.map` - Source map 文件

**防护层级：**

| 层级 | 位置 | 机制 |
|------|------|------|
| 构建时 | Dockerfile | `find` 命令删除上述文件 |
| 运行时 | Nginx | `location` 规则返回 404 |
| CI/CD | Jenkinsfile | 构建阶段扫描并删除 |

#### 2. Nginx Security Configuration

```nginx
# 拒绝访问源码文件
location ~* \.vue$ { return 404; }

# 拒绝访问配置文件
location ~* (config|vite|webpack|babel|tailwind|postcss|eslint|prettier)\.config\.(js|ts|mjs|cjs|json)$ {
    return 404;
}

# 拒绝访问 source map
location ~* \.map$ { return 404; }
```

### Kubernetes

- `assets/k8s-deployment.yml` - Complete K8s manifests including:
  - Deployments with health checks
  - Services (ClusterIP)
  - Ingress with TLS
  - HorizontalPodAutoscaler (HPA)

### Nginx Config

- `assets/nginx.conf.txt` - Optimized Nginx configuration for Vue SPA with:
  - Gzip compression
  - Static asset caching
  - API proxy to backend
  - Health check endpoint
  - Security rules (blocks .vue, config files, source maps)

**Note:** Copy and rename to `nginx.conf` when using.

## Scripts

### Notification Script

`scripts/notify.sh` - Send deployment notifications to:
- 飞书 (Feishu)
- 钉钉 (DingTalk)
- Slack
- 企业微信 (WeChat Work)

Usage:
```bash
export WEBHOOK_TYPE=feishu
export WEBHOOK_URL=https://open.feishu.cn/...
export PROJECT_NAME=my-app
export VERSION=1.0.0
./scripts/notify.sh success
```

## Customization Guide

### 1. Adjust Resource Limits

Edit `assets/k8s-deployment.yml`:
```yaml
resources:
  requests:
    memory: "512Mi"  # Adjust based on your app
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### 2. Change Trigger Strategy

**GitLab CI** - Remove `when: manual` to auto-trigger:
```yaml
dockerize-java:
  # ...
  # when: manual  # Remove or comment this line
```

**Jenkins** - Add SCM polling:
```groovy
triggers {
    pollSCM('H/5 * * * *')  // Check every 5 minutes
}
```

### 3. Add Environment Stages

Add staging deployment between build and production:

**GitLab CI:**
```yaml
stages:
  - lint
  - test
  - build
  - dockerize
  - deploy-staging    # Add this
  - deploy-production # Rename from deploy
  - notify

deploy-staging:
  stage: deploy-staging
  script:
    - kubectl set image ... -n staging
  environment:
    name: staging
  when: manual
```

### 4. Custom Quality Gates

Add SonarQube analysis:
```yaml
sonarqube:
  stage: test
  image: sonarsource/sonar-scanner-cli
  script:
    - sonar-scanner
      -Dsonar.projectKey=$CI_PROJECT_NAME
      -Dsonar.sources=.
      -Dsonar.host.url=$SONAR_URL
      -Dsonar.login=$SONAR_TOKEN
```

### 5. Multi-Environment Support

Use GitLab environments or Jenkins branches:

**GitLab:**
```yaml
deploy:
  script:
    - |
      if [ "$CI_COMMIT_REF_NAME" == "main" ]; then
        kubectl set image ... -n production
      else
        kubectl set image ... -n staging
      fi
```

## Troubleshooting

### Static Resource Security Violation

**Error:** Build fails with "Security violation found: *.vue files in dist"

**Cause:** Vue build configuration may be including source files

**Solution:**
1. Check `vite.config.js` / `vue.config.js` for incorrect `publicDir` or `assetsInclude`
2. Verify `.gitignore` excludes source files from build
3. Manual fix in Dockerfile already handles cleanup:
```dockerfile
RUN find /usr/share/nginx/html -type f \
    -name "*.vue" -o \
    -name "*.config.js" \
    -delete
```

### Jenkins Plugin Not Found

**Error:** `No such DSL method 'publishTestResults'`

**Solution:** 
- Jenkinsfile now uses standard `junit` plugin instead of custom publishers
- Install **JUnit Plugin** from Jenkins plugin manager
- Or disable test publishing by removing the `post { always { junit ... } }` blocks

### Docker Build Context Issues

**Error:** `unable to prepare context: unable to evaluate symlinks`

**Solution:**
```groovy
// Use explicit build context
Dockerfile: "-f backend/Dockerfile backend/"
// Not: "-f backend/Dockerfile ."
```

### Kubectl Commands Fail
- Verify `KUBE_CONFIG` is base64 encoded correctly
- Check cluster name matches the context in kubeconfig
- Ensure service account has deployment permissions

### Image Pull Errors
- Verify image tags are pushed correctly
- Check image pull secrets if using private registry
- Verify pod has `imagePullPolicy: Always` for latest tags

### Rollout Hangs
- Check pod events: `kubectl describe pod <pod-name>`
- Verify resource limits are not too low
- Check application logs: `kubectl logs <pod-name>`

## Security Best Practices

1. **Never commit credentials** - Always use CI/CD variables
2. **Use specific image tags** - Avoid `:latest` in production
3. **Enable RBAC** - Limit service account permissions
4. **Scan images** - Add Trivy or Clair vulnerability scanning
5. **Network policies** - Restrict pod-to-pod communication
6. **Resource quotas** - Set namespace limits

## References

- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Kubernetes Deployment Guide](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
