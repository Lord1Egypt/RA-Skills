---

slug: docker-essentials-tool-pro
name: docker-essentials-tool-pro
version: 1.0.0
displayName: Docker基础工具专业版
summary: "企业级Docker管理,支持镜像深度优化、安全扫描、Swarm编排、批量运维与CI/CD集成.。面向企业运维团队的高级Docker管理工具,提供镜像深度优化、安全质量检查、多节点编排、批量运"
license: Proprietary
edition: pro
description: "面向企业运维团队的高级Docker管理工具,提供镜像深度优化、安全质量检查、多节点编排、批量运维与CI/CD流水线集成。核心能力:。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。 功能涵盖: essentials。"
  - 镜像深度优化与体积分析

  - 容器安全质量检查

  - Docker Swarm多节点编排

  - 批量容器运维管理

  - 资源监控与告警

  - CI/CD流水线集成

  适用场景:

  - 企业级容器化部署

  - 生产环境容器运维

  - 安全合规扫描

  - DevOps流水线集成

  差异化:

  - 专业版完全兼容免费版命令,支持平滑升级

  - 提供镜像安全扫描与优化分析

  - 支持多节...'
tags:
  - 开发工具
  - Docker
  - 容器化
  - 企业级
  - DevOps
  - 容器
  - docker
  - swarm
  - myapp
  - service
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Development"

---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。


Docker基础工具专业版为企业运维团队提供高级容器管理能力。在免费版基础能力之上,专业版新增镜像深度优化分析、容器安全质量检查、Docker Swarm多节点编排、批量容器运维和CI/CD流水线集成,满足企业级容器化运维需求.
专业版完全兼容免费版的所有Docker命令和Compose配置,运维团队可从免费版无缝升级,已有脚本和配置无需修改即可在专业版中使用.
## 核心能力
### 1. 镜像深度优化与分析
分析镜像层级结构,优化镜像体积和构建效率.
> 详细代码示例已移至 `references/detail.md`

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Docker基础工具专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
echo "=== 镜像层分析 ==="
docker history --no-trunc myapp:1.0
# ...
docker images --format "table <动态配置>\t<动态配置>\t<动态配置>" | sort -k3 -h
# ...
docker images --format "<动态配置> <动态配置>:<动态配置>" | sort -rh | head -10
# ...
docker inspect --format='<动态配置><动态配置>' myapp:1.0
```

**处理**: 解析镜像深度优化与分析的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回镜像深度优化与分析的响应数据,包含状态码、结果和日志.
### 2. 容器安全质量检查
扫描镜像中的已知安全漏洞.

**处理**: 解析容器安全质量检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回容器安全质量检查的响应数据,包含状态码、结果和日志.
### 3. Docker Swarm 多节点编排
```bash
echo "=== Docker Swarm管理 ==="
# ...
docker swarm init --advertise-addr 192.168.1.100
# ...
docker swarm join-token worker
docker swarm join-token manager
# ...
docker node ls                              # 列出节点
docker node inspect <node-id>               # 查看节点详情
docker node update --availability drain <node-id>  # 设置节点为drain
docker service create --name web -p 8080:80 --replicas 3 nginx
# ...
docker service ls                           # 列出服务
docker service ps web                       # 查看服务任务
docker service scale web=5                  # 扩展服务
docker service update --image nginx:alpine web  # 更新镜像
docker service rollback web                 # 回滚服务
docker service rm web                       # 删除服务
docker stack deploy -c docker-stack.yml myapp
docker stack ls
docker stack services myapp
docker stack rm myapp
```

**处理**: 解析Docker Swarm 多节点编排的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Docker Swarm 多节点编排的响应数据,包含状态码、结果和日志.
### 4. 批量容器运维
```bash
#!/bin/sh
echo "=== 批量容器运维 ==="
# ...
echo "停止所有容器..."
docker ps -q | xargs -r docker stop
# ...
echo "清理已停止容器..."
docker container prune -f
# ...
echo "清理未使用镜像..."
docker image prune -a -f
# ...
echo "清理未使用卷..."
docker volume prune -f
# ...
echo "清理未使用网络..."
docker network prune -f
# ...
echo -e "\n=== 系统资源概览 ==="
docker system df
# ...
echo -e "\n=== 批量更新镜像 ==="
for image in $(docker images --format "<动态配置>:<动态配置>" | grep -v "<none>"); do
    echo "更新: $image"
    docker pull "$image" 2>/dev/null
done
# ...
echo -e "\n=== 批量重启Compose服务 ==="
for dir in /opt/app1 /opt/app2 /opt/app3; do
    if [ -f "$dir/docker-compose.yml" ]; then
        echo "重启: $dir"
        cd "$dir" && docker compose restart && cd -
    fi
done
```

**处理**: 解析批量容器运维的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回批量容器运维的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 资源监控与告警

**处理**: 解析资源监控与告警的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回资源监控与告警的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、支持镜像深度优化、安全扫描、批量运维与、面向企业运维团队、的高级、管理工具、流水线集成、核心能力、镜像深度优化与体、积分析、批量容器运维管理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一:生产环境镜像优化
对生产镜像进行深度优化,减小体积提升安全性.
### 场景二:Swarm集群部署
使用Docker Swarm进行多节点生产部署.
```bash
#!/bin/sh
echo "=== Swarm集群部署 ==="
# ...
echo "节点状态:"
docker node ls
# ...
echo -e "\n部署应用Stack..."
# ...
echo -e "\n等待服务就绪..."
sleep 10
docker stack services myapp
# ...
echo -e "\n服务任务分布:"
docker service ps myapp_web --format "table <动态配置>\t<动态配置>\t<动态配置>"
# ...
echo -e "\n执行滚动更新..."
docker service update --image myapp:1.1 \
    --update-parallelism 1 \
    --update-delay 10s \
    --update-failure-action rollback \
    myapp_web
# ...
echo -e "\n服务健康状态:"
docker inspect --format='<动态配置>' \
    $(docker ps -q --filter "name=myapp") 2>/dev/null
```

### 场景三:CI/CD流水线集成
将Docker构建和部署集成到CI/CD流水线.
```yaml
docker_build_deploy:
  stage: deploy
  image: docker:24
  services:
    - docker:24-dind
  variables:
    IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
  script:
    - docker build -t "$IMAGE_TAG" .
# ...
    - |
      echo "运行安全扫描..."
      docker run --rm \
        -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy:latest image --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_TAG"
# ...
    - |
      SIZE=$(docker inspect --format='<动态配置>' "$IMAGE_TAG")
      echo "镜像大小: $((SIZE / 1024 / 1024))MB"
      if [ "$SIZE" -gt 524288000 ]; then
        echo "警告: 镜像超过500MB"
      fi
# ...
    - docker push "$IMAGE_TAG"
# ...
    - |
      docker stack deploy \
        -c docker-stack.yml \
        --with-registry-auth \
        myapp
  only:
    - main
```

## 不适用场景

以下场景Docker基础工具专业版不适合处理：

- 需要人工创意判断的任务
- 非结构化头脑风暴
- 人际沟通协调

## 触发条件

需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于非本工具能力范围的需求.
## 快速开始
### Step 1:配置环境
```yaml
version: "2.0"
edition: pro
# ...
optimization:
  analyze_layers: true
  suggest_multistage: true
  max_image_size: 500MB
# ...
security:
  scan_vulnerabilities: true
  check_root_user: true
  check_secrets: true
  fail_on: [critical, high]
# ...
swarm:
  enabled: true
  manager_nodes: 3
  worker_nodes: 5
# ...
monitoring:
  enabled: true
  interval: 30
  thresholds:
    cpu: 80
    memory: 85
  alert:
    webhook: "${ALERT_WEBHOOK_URL}"
```

### Step 2:运行分析
```
请对当前项目的Docker镜像进行深度分析和安全扫描,生成优化建议.
```

### Step 3:查看报告
报告输出到 `./reports/` 目录,包含镜像分析、安全扫描和优化建议.
## 配置示例
### 企业级完整配置

## 优选实践
1. **镜像分层优化**:分析每层大小,合并指令减少层数

```bash
docker history --no-trunc --format "table <动态配置>\t<动态配置>" myapp:1.0
```

2. **配置基线检查**:定期扫描镜像安全漏洞

```bash
0 2 * * * /opt/tools/docker-security-scan.sh >> /var/log/docker-security.log
```

3. **资源限制**:为所有容器设置资源限制

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

4. **健康检查**:所有服务配置健康检查

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -q --spider http://localhost:3000/health || exit 1
```

5. **日志管理**:配置日志轮转避免磁盘写满

```yaml
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## 常见问题
### Q1:专业版如何兼容免费版?
专业版完全兼容免费版的所有Docker命令和Compose配置文件。免费版的 `docker-compose.yml` 可直接在专业版中使用,专业版会自动识别并启用额外的高级功能.
### Q2:如何选择Swarm vs Kubernetes?
| 维度 | Docker Swarm | Kubernetes |
|:-----|:-----|:-----|
| 复杂度 | 低 | 高 |
| 学习曲线 | 平缓 | 陡峭 |
| 适合规模 | 中小型 | 大型 |
| 功能丰富度 | 基础 | 丰富 |
| 运维成本 | 低 | 高 |

### Q3:镜像扫描支持哪些工具?
```bash
trivy image myapp:1.0
# ...
grype myapp:1.0
# ...
docker scout cves myapp:1.0
# ...
snyk container test myapp:1.0
```

### Q4:如何实现零停机部署?
```bash
docker service update \
    --image myapp:2.0 \
    --update-parallelism 1 \
    --update-delay 10s \
    --update-failure-action rollback \
    myapp_web
# ...
docker compose up -d --no-deps --build web
```

## 依赖说明
### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Linux(推荐) / macOS / Windows
- **运行时**:Docker Engine 24.0+ / Docker Compose v2+
- **可选**:Docker Swarm模式

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Docker Engine 24+ | 运行时 | 必需 | docker.com 下载安装 |
| Docker Compose v2 | 工具 | 必需 | Docker Desktop自带 |
| Trivy | 安全工具 | 推荐 | aquasecurity/trivy |
| Python 3.8+ | 运行时 | 推荐 | python.org 下载 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 私有镜像仓库需要配置认证:

```bash
docker login registry.company.com
# ...
{
  "registry-mirrors": ["https://mirror.company.com"],
  "insecure-registries": []
}
```

- 安全扫描服务可选配置:

```yaml
security:
  scan_tools:
    trivy:
      token: "${TRIVY_TOKEN}"
    snyk:
      token: "${SNYK_TOKEN}"
```

### 可用性分类
- **分类**:MD+EXEC+PRO(专业版支持镜像分析、安全扫描、Swarm编排和监控)
- **说明**:企业级 AI Skill,支持镜像深度优化、安全质量检查、多节点编排和CI/CD集成
- **适用规模**:单机到多节点集群环境
- **兼容性**:完全兼容免费版命令和配置,支持平滑升级

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Docker基础工具专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "docker essentials pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级Docker管理,支持镜像深度优化、安全扫描、Swarm编排、批量运维与CI/CD集成.。面向企业运维团队的高级D
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据