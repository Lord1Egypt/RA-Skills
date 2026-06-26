# aios-transfer-file

> 本技能只适用于受控 AIOS 部署。它可能访问真实业务系统，必须按最小权限配置。只读操作可以自动执行；任何会改变状态的操作，包括创建、更新、提交、审批、驳回、删除或触发，都必须先预览目标应用、命令和请求体，并获得明确人工确认。CLI 必须固定到经过评审的版本，Ontology 来源必须可信且可审计。

OpenClaw/AIOS 文件传输 skill。使用 `scripts/transfer_s3.mjs` 动态加载当前目录本地安装的 `@aws-sdk/client-s3`，把 `file_input://...` 对象下载到工作区，或把本地文件上传到发件箱 bucket。

## 依赖要求

- Node.js
- `@aws-sdk/client-s3`
- `AIOS_S3_ENDPOINT`
- `AIOS_S3_REGION`
- `AIOS_S3_ACCESS_KEY_ID`
- `AIOS_S3_SECRET_ACCESS_KEY`
- `AIOS_S3_FORCE_PATH_STYLE`
- `AIOS_S3_AGENT_INBOX_BUCKET`
- `AIOS_S3_AGENT_OUTBOX_BUCKET`

## 用法

```bash
npm install
node scripts/transfer_s3.mjs download-uri --uri "file_input://bucket/path/to/file.bin" --workspace .
node scripts/transfer_s3.mjs upload-file --source "/abs/path/to/file.bin" --workspace .
```

## Docker

推荐做法：在 Docker 镜像内预装依赖，但仍然把它作为这个 skill 的本地依赖，而不是使用 `npm install -g`。

Dockerfile 示例模式：

```dockerfile
# 把 skill 复制进镜像
COPY skills/aios-transfer-file /opt/aios/skills/aios-transfer-file

# 在镜像构建阶段安装这个 skill 的本地依赖
WORKDIR /opt/aios/skills/aios-transfer-file
RUN npm ci
```

运行时要求：

- `package.json`、`package-lock.json` 和 `node_modules/` 必须保留在同一个 skill 目录下。
- 从这个 skill 目录运行脚本，或者确保启动脚本的进程模块解析路径能够看到这个本地 `node_modules`。
- 不要依赖 `npm install -g @aws-sdk/client-s3`；这个脚本的设计就是动态导入本地安装的包。
