---
slug: "docker-essentials-free"
name: "docker-essentials-free"
version: 1.0.1
displayName: "Docker核心操作免费版"
summary: "免费版Docker操作指南，涵盖容器管理、镜像操作与基础调试命令。。Docker核心操作指南免费版，提供容器生命周期管理基础命令. 包含镜像管理、容器调试与常用工作流. 适用于个人开发与学习"
summary_zh: "免费版Docker操作指南，涵盖容器管理、镜像操作与基础调试命令。。Docker核心操作指南免费版，提供容器生命周期管理基础命令. 包含镜像管理、容器调试与常用工作流. 适用于个人开发与学习"
license: "MIT"
description: "|-. 适用于需要docker essentials相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  Docker核心操作指南免费版，提供容器生命周期管理基础命令.
  包含镜像管理、容器调试与常用工作流.
  适用于个人开发与学习场景的Docker容器化操作.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 系统运维
  - docker
  - essentials
  - automation
  - productivity
  - 容器
  - DevOps
  - container
  - bash
  - agent
category: "Development"
pricing_tier: free
---
# Docker核心操作指南（免费版）

涵盖容器管理、镜像操作与基础调试的Docker核心命令.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Docker核心操作免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 容器生命周期管理（Container Lifecycle）
创建、启动、停止、删除容器：

```bash
docker run -d --name my-nginx -p 8080:80 nginx  # 后台运行带端口映射
docker ps                    # 查看运行中容器
docker ps -a                 # 查看所有容器
docker stop container_name   # 停止容器
docker start container_name  # 启动容器
docker rm container_name     # 删除容器
docker container prune       # 清理已停止容器
```

### 镜像管理（Image Management）
构建与管理Docker镜像：

```bash
docker build -t myapp:1.0 .      # 构建镜像
docker images                    # 列出镜像
docker pull nginx:latest         # 拉取镜像
docker rmi image_name            # 删除镜像
docker image prune               # 清理悬空镜像
```

### 容器调试（Container Inspection & Debugging）
查看日志与进入容器调试：

```bash
docker logs -f container_name          # 跟踪日志
docker logs --tail 100 container_name  # 最后100行
docker exec -it container_name bash    # 进入容器
docker stats                           # 资源使用
docker inspect container_name          # 容器详情
```

### 常用工作流（Common Workflows）
预置开发与数据库容器工作流：

```bash
# 开发容器
docker run -it --rm -v $(pwd):/app -w /app -p 3000:3000 node:18 npm run dev
# ...
# 数据库容器
docker run -d --name postgres -e POSTGRES_PASSWORD=secret -v postgres-data:/var/lib/postgresql/data -p 5432:5432 postgres:15
```

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. 确认Docker Engine已安装并运行
2. 使用自然语言描述需求，Agent生成对应的Docker命令
3. Agent执行命令并检查输出结果
4. 如遇错误，参考错误处理章节进行排查

#
## 示例

### 示例1：启动并管理Nginx容器

```
用户: 帮我启动一个Nginx容器
# ...
Agent: docker run -d --name my-nginx -p 8080:80 nginx
- 容器已在后台启动
- 访问 http://${SERVER_HOST}:${SERVER_PORT} 查看欢迎页
- docker stop my-nginx 可停止容器
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| `Cannot connect to the Docker daemon` | Docker服务未启动 | 启动Docker服务或Docker Desktop |
| `port is already allocated` | 端口被占用 | 更换映射端口或停止占用容器 |
| `image not found locally` | 镜像不存在 | 执行 `docker pull <image>` 拉取镜像 |

## 常见问题

### Q1: 免费版与付费版有什么区别？
A: 免费版提供容器管理、镜像操作与基础调试功能。付费版额外涵盖Docker Compose、网络配置、数据卷管理、系统管理与完整工作流.
### Q2: 如何查看容器日志？
A: 使用 `docker logs -f <container>` 跟踪日志输出，使用 `docker logs --tail 100 <container>` 查看最后100行.
### Q3: 如何进入运行中的容器？
A: 使用 `docker exec -it <container> bash` 进入容器的交互式bash，若容器无bash可使用 `sh` 替代.
## 已知限制

- 不包含Docker Compose多容器编排功能
- 不包含网络配置与数据卷管理详解
- 不包含系统级清理命令详解
- 部分命令在Windows上语法不同

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Docker核心操作免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "docker-essentials"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
