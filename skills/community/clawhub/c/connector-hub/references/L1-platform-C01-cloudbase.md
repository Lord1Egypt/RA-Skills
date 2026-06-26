# C01 - 腾讯云 CloudBase

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C01 |
| 连接器名 | cloudbase |
| 显示名 | 腾讯云 CloudBase |
| 层级 | L1 平台级 |
| 可替代 | ❌ 不可替代 |
| 分类 | 云服务/Serverless |

## 能力说明

腾讯云 CloudBase 提供完整的云开发环境：

| 能力 | 说明 |
|------|------|
| 云函数 | 无服务器函数计算，按需执行 |
| 云数据库 | 文档型数据库，实时同步 |
| 云存储 | 对象存储，CDN 加速 |
| 云托管 | 容器化部署，自动扩缩容 |
| 静态托管 | 静态网站托管，自定义域名 |

## 为什么不可替代

**需要平台运行时环境**：
- 云函数需要平台的执行环境（Node.js/Python/Go Runtime）
- 云数据库需要平台的存储引擎和同步机制
- 云存储需要平台的 CDN 节点和存储集群
- 容器托管需要平台的调度系统和扩缩容策略

**Skill 无法提供**：
- ❌ 无法提供服务器运行时环境
- ❌ 无法提供分布式数据库
- ❌ 无法提供 CDN 节点网络
- ❌ 无法提供容器编排系统

## 使用场景

| 场景 | 说明 |
|------|------|
| 小程序后端 | 微信小程序/支付宝小程序云开发 |
| Serverless 应用 | 无服务器架构，按量计费 |
| 静态网站 | 博客、文档站、营销页 |
| 数据存储 | 结构化数据存储和查询 |
| 文件管理 | 图片/视频/文档上传和管理 |

## 配置方式

在 WorkBuddy 连接器管理页面启用 `cloudbase`，配置：
- SecretId / SecretKey（腾讯云 API 密钥）
- Environment ID（CloudBase 环境 ID）
- Region（地域）

## 替代方案（非 Skill）

如果不想用连接器，可直接使用腾讯云 SDK：

```python
# pip install tccli
# 或使用腾讯云 SDK
from tencentcloud.common import credential
from tencentcloud.cloudbase.v20190606 import cloudbase_client

cred = credential.Credential("SecretId", "SecretKey")
client = cloudbase_client.CloudbaseClient(cred, "ap-shanghai")
```

但这不是 Skill 替代，而是直接调用云 API，仍需云平台账号。
