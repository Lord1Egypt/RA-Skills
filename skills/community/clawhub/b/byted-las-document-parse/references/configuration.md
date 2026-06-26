# 配置说明 & 依赖安装

## 依赖安装
使用本地文件上传功能需要安装以下依赖：
```bash
pip install tos Pillow requests
```

## LAS API 认证配置
- **认证方式**：优先使用环境变量 `LAS_API_KEY`，也可以在当前目录提供 `env.sh` 文件
  - 默认使用 `Authorization: Bearer <LAS_API_KEY>` 认证头
- **区域配置**：通过 `--region cn-beijing|cn-shanghai` 参数或环境变量 `LAS_REGION` 指定
- **API 地址**：通过 `--api-base` 参数或环境变量 `LAS_API_BASE` 自定义

API Key 读取优先级：
1. 环境变量 `LAS_API_KEY`
2. 当前目录 `env.sh` 文件（支持 `export LAS_API_KEY="..."` 或 `LAS_API_KEY=...` 格式）

### LAS_API_KEY 获取方式
请参考火山引擎官方文档获取LAS API密钥：
[获取LAS API密钥](https://www.volcengine.com/docs/6492/2191994?lang=zh)

## TOS 上传配置（本地文件上传必需）
使用本地 PDF 或图片文件时，需要配置 TOS 凭证：

| 环境变量 | 说明 | 是否必需 |
|---------|------|---------|
| `TOS_ACCESS_KEY` | TOS 访问密钥 | 是 |
| `TOS_SECRET_KEY` | TOS 密钥 | 是 |
| `TOS_BUCKET` | 默认存储桶名称 | 可选（可通过 `--tos-bucket` 参数指定） |
| `TOS_ENDPOINT` | TOS 接入点 | 可选（默认根据区域自动推断） |

### TOS 密钥获取方式
请参考火山引擎官方文档获取TOS访问密钥：
[获取TOS Access Key和Secret Key](https://www.volcengine.com/docs/6291/65568?lang=zh)

## 配置示例（env.sh）
```bash
export LAS_API_KEY="your-las-api-key"
export TOS_ACCESS_KEY="your-tos-access-key"
export TOS_SECRET_KEY="your-tos-secret-key"
export TOS_BUCKET="your-bucket-name"
export LAS_REGION="cn-beijing"
```

## 区域对应的 API 地址
| 区域 | API 域名 |
|------|---------|
| cn-beijing | operator.las.cn-beijing.volces.com |
| cn-shanghai | operator.las.cn-shanghai.volces.com |
