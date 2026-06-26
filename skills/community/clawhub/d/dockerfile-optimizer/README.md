# dockerfile-optimizer

## 功能说明
这个 skill 旨在扮演一个高级 DevOps 工程师，专门为你审查并重构臃肿、缓慢或不安全的 `Dockerfile`。它可以：
- **减小镜像体积**：通过引入多阶段构建（Multi-stage build）、替换更小的基础镜像（如 `alpine` 或 `slim`）以及清理无用的包管理器缓存（`apt`/`apk`）来大幅缩减镜像大小。
- **提升构建速度**：通过优化指令顺序（如优先 COPY `package.json` 或 `go.mod`）来最大化利用 Docker 的层缓存（Layer Caching）。
- **增强安全性**：检查并建议添加非 root 用户运行权限，以及提醒配置 `.dockerignore` 文件以防泄露敏感代码。
- 支持中英双语输出，会根据用户的提问语言自动适配。

## 使用场景
当你在打包应用时发现 Docker 镜像动辄几个 G，或者每次修改一行代码都要重新拉取依赖导致构建缓慢，将你的 `Dockerfile` 发送给这个 skill，它会直接返回一个优化好的版本并解释原因。

## 提问示例

**中文模式：**
```text
帮我看看这个 Dockerfile 怎么优化，感觉体积太大了：
FROM node:18
COPY . .
RUN npm install
CMD ["npm", "start"]
```

**英文模式：**
```text
Review this Dockerfile for a Go app:
FROM golang:1.20
WORKDIR /app
COPY . .
RUN go build -o myapp
CMD ["./myapp"]
```