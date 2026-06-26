# aliyun_openclaw Skill

阿里云 OpenClaw 远程部署与管理技能。提供远程服务器上的 OpenClaw 网关部署、SSH 隧道连接、设备配对和日常管理的完整流程。

## 触发词

- 阿里云 OpenClaw
- 远程 OpenClaw 部署
- OpenClaw 配对
- 飞书连接 OpenClaw
- SSH 隧道 OpenClaw

## 环境配置

### 服务器信息

| 项目 | 值 |
|------|-----|
| 远程服务器 IP | `47.115.54.84` |
| SSH 用户名 | `root` |
| SSH 密码 | `Davinci@1984` |
| 本地访问端口 | `18790` |
| 远程网关端口 | `18789` |
| Gateway Token | `f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3` |

### 大模型配置 (已同步)

**默认模型：** `bailian/qwen3.5-plus`

**可用模型列表：**
| 模型 ID | 名称 |
|--------|------|
| `qwen3.5-plus` | Qwen3.5 Plus (默认) |
| `qwen3-max-2026-01-23` | Qwen3 Max |
| `qwen3-coder-next` | Qwen3 Coder Next |
| `qwen3-coder-plus` | Qwen3 Coder Plus |
| `MiniMax-M2.5` | MiniMax M2.5 |
| `glm-5` | GLM-5 |
| `glm-4.7` | GLM-4.7 |
| `kimi-k2.5` | Kimi K2.5 |

**API 配置：**
- Provider: `bailian` (阿里百炼)
- Base URL: `https://coding.dashscope.aliyuncs.com/v1`
- API Key: `sk-sp-dc9e54ca53434d4a828241fb51b60f52`

### MCP 配置

**注意：** 远程服务器暂未安装 MCP 适配器插件。如需使用 TAPD 等 MCP 工具，需要：
1. 在远程服务器安装：`docker exec openclaw npm install -g @openclaw/mcp-adapter`

### Browser Relay 配置

**完整文档：** `skills/aliyun_openclaw/browser_relay_guide.md`

**快速配置：**

```bash
# 1. 安装 Browser Relay（在阿里云执行）
ssh root@47.115.54.84 "docker exec openclaw sh -c 'cd /app && npm install @openclaw/browser-relay'"

# 2. 启动服务
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'cd /app && npx @openclaw/browser-relay --port 18792 &'"

# 3. 建立 SSH 隧道（本地执行）
ssh -f -N -L 18792:localhost:18792 root@47.115.54.84

# 4. 配置扩展
# Port: 18792
# Gateway token: f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3
```
2. 或手动配置 MCP Server

### 已同步的 Skills

本地 Skills 目录：`~/.openclaw/workspace/skills/`

**核心 Skills 列表：**
- `api-gateway` - API 网关集成
- `brave-search` - 网络搜索
- `browser-automation` - 浏览器自动化
- `frontend-design` - 前端设计
- `humanizer` - AI 文本人性化
- `mcp-adapter` - MCP 适配器
- `playwright-scraper-skill` - 网页爬取
- `stock-analysis` - 股票分析
- `tushare-data` - Tushare 财经数据
- `tavily-search` - Tavily 搜索
- `summarize` - 内容摘要
- `oa-check-in` - OA 签到
- `zentao` - 禅道集成
- `aliyun_openclaw` - 本技能 (阿里云部署文档)

**同步 Skills 到远程服务器：**
```bash
# 打包本地 skills
cd ~/.openclaw/workspace/skills/
tar -czf skills.tar.gz */

# 传输到远程服务器
sshpass -p 'Davinci@1984' scp skills.tar.gz root@47.115.54.84:/opt/openclaw/skills/

# 在远程服务器解压
ssh root@47.115.54.84
cd /opt/openclaw/skills/
tar -xzf skills.tar.gz
```

### 目录结构

```
/opt/openclaw/
├── config/         # 配置文件 (openclaw.json)
├── workspace/      # 工作区
├── memory/         # 记忆文件
├── skills/         # 技能文件 (需手动同步)
└── logs/           # 日志文件
```

## 使用流程

### 一、首次部署（仅需执行一次）

```bash
# 1. SSH 登录远程服务器
ssh root@47.115.54.84

# 2. 创建配置目录
mkdir -p /opt/openclaw/{config,workspace,memory,skills,logs}

# 3. 上传配置文件 (从本地)
scp ~/.openclaw/workspace/skills/aliyun_openclaw/remote_config.json root@47.115.54.84:/opt/openclaw/config/openclaw.json

# 4. 启动 Docker 容器
docker run -d \
  --name openclaw \
  --restart always \
  -p 18789:18789 \
  -p 18791:18791 \
  -v /opt/openclaw/config:/home/node/.openclaw \
  -v /opt/openclaw/workspace:/app/workspace \
  -v /opt/openclaw/memory:/app/memory \
  -v /opt/openclaw/skills:/app/skills \
  -v /opt/openclaw/logs:/app/logs \
  registry.cn-hangzhou.aliyuncs.com/qiluo-images/openclaw:latest

# 5. 检查状态
docker logs openclaw --tail 10
```

### 二、本地连接（每次使用）

```bash
# 1. 建立 SSH 隧道（后台运行）
ssh -f -N -L 18790:localhost:18789 root@47.115.54.84

# 2. 验证隧道
curl -s -o /dev/null -w "%{http_code}" http://localhost:18790/
# 应返回 200

# 3. 访问仪表盘
# 浏览器打开：http://localhost:18790/#token=f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3
```

### 三、设备配对流程

```bash
# 1. 查看待配对设备（在远程服务器执行）
docker exec openclaw openclaw devices list

# 2. 批准配对请求
docker exec openclaw openclaw devices approve <requestId>

# 3. 查看已配对设备
docker exec openclaw openclaw devices list
```

### 四、飞书集成

当用户在飞书 App 中连接 OpenClaw 时：

1. 飞书 App 会发起配对请求
2. 执行以下命令查看并批准：

```bash
# 查看待配对请求
docker exec openclaw openclaw devices list

# 批准飞书配对（替换 <requestId> 为实际 ID）
docker exec openclaw openclaw devices approve <requestId>

# 验证已配对
docker exec openclaw openclaw devices list
```

### 五、常用管理命令

```bash
# 查看网关状态
docker exec openclaw openclaw gateway status

# 查看日志
docker logs openclaw --tail 50

# 重启网关
docker restart openclaw

# 停止网关
docker stop openclaw

# 删除容器（重新配置时用）
docker stop openclaw && docker rm openclaw

# 更新到最新版本
docker pull registry.cn-hangzhou.aliyuncs.com/qiluo-images/openclaw:latest
docker restart openclaw

# 同步 Skills 到远程
cd ~/.openclaw/workspace/skills/
tar -czf skills.tar.gz */
sshpass -p 'Davinci@1984' scp skills.tar.gz root@47.115.54.84:/opt/openclaw/skills/
ssh root@47.115.54.84 "cd /opt/openclaw/skills/ && tar -xzf skills.tar.gz"
```

## 故障排查

### SSH 隧道无法建立

```bash
# 检查是否有旧隧道进程
ps aux | grep "ssh.*18790"

# 杀掉旧进程
pkill -f "ssh.*18790"

# 重新建立隧道
ssh -f -N -L 18790:localhost:18789 root@47.115.54.84
```

### 网关无法访问

```bash
# 检查容器状态
docker ps | grep openclaw

# 查看容器日志
docker logs openclaw --tail 30

# 检查端口监听
docker exec openclaw ss -tlnp | grep 18789
```

### 配对失败

```bash
# 清除旧配对（谨慎使用）
docker exec openclaw sh -c 'rm -f /home/node/.openclaw/devices.json'
docker restart openclaw
```

### 模型配置问题

```bash
# 查看当前配置
docker exec openclaw cat /home/node/.openclaw/openclaw.json

# 修复配置
docker exec openclaw openclaw doctor --fix
```

## 安全提示

- ⚠️ SSH 密码、API Key 和 Gateway Token 属于敏感信息，不要公开分享
- ⚠️ 生产环境建议使用 SSH 密钥认证而非密码
- ⚠️ 建议配置防火墙限制 18789 端口仅允许信任 IP 访问
- ⚠️ 定期更新 OpenClaw 到最新版本
- ⚠️ 大模型 API Key 已同步到远程，注意用量监控

## 配置同步清单

| 配置项 | 本地 | 远程 | 状态 |
|--------|------|------|------|
| Gateway 配置 | ✅ | ✅ | 已同步 |
| 大模型配置 | ✅ | ✅ | 已同步 (bailian) |
| Skills | ✅ | ⏳ | 需手动同步 |
| MCP 配置 | ✅ | ❌ | 未安装插件 |
| 记忆文件 | ✅ | ⏳ | 需手动同步 |
| 工作区文件 | ✅ | ⏳ | 需手动同步 |

## 相关链接

- OpenClaw 文档：https://docs.openclaw.ai
- 设备配对文档：https://docs.openclaw.ai/web/control-ui#device-pairing-first-connection
- Docker 镜像：registry.cn-hangzhou.aliyuncs.com/qiluo-images/openclaw:latest
- 阿里百炼文档：https://help.aliyun.com/zh/model-studio/

## 配置文件备份

远程配置文件已保存在：`skills/aliyun_openclaw/remote_config.json`
