---
name: dolphindb-docker
description: Automate DolphinDB Docker deployment with auto architecture detection (ARM64/x86_64), smart memory allocation (50% rule), and full data persistence.
metadata: {"clawdbot":{"emoji":"🐬","os":["macos","linux"],"requires":{"bins":["docker"]},"install":[{"id":"docker-desktop","kind":"manual","label":"Install Docker Desktop","url":"https://www.docker.com/products/docker-desktop/"}]}}
---

# DolphinDB Docker 部署技能

## 功能说明

自动化部署 DolphinDB Docker 容器，包括：
1. **自动检测本机芯片架构**（ARM64/x86_64）
2. **自动读取本机内存**并按 50% 原则分配
3. **下载指定版本的 DolphinDB 官方 Docker 镜像**
4. **完整持久化** `/data/ddb/server/` 目录到主机
5. **License 指纹采集**挂载 `/etc` 目录

## 使用方法

### 基础部署

```bash
# 部署最新版（自动检测架构和内存）
./deploy-dolphindb.sh

# 部署指定版本
./deploy-dolphindb.sh v2.00.7

# 自定义内存（GB）
./deploy-dolphindb.sh v2.00.7 16

# 自定义数据目录
./deploy-dolphindb.sh v2.00.7 8 /path/to/data
```

### Python 调用

```python
import subprocess

# 部署 DolphinDB
subprocess.run([
    './skills/dolphindb-docker/deploy-dolphindb.sh',
    'v2.00.7',  # 版本
    '8',        # 内存 GB（可选，默认自动计算）
    '/Users/mac/Documents/dolphindb_docker_server'  # 数据目录（可选）
])
```

## 文件结构

```
dolphindb-docker/
├── SKILL.md              # 技能说明（本文件）
├── deploy-dolphindb.sh   # 部署脚本
└── README.md             # 详细文档
```

## 部署逻辑

### 1. 芯片检测
```bash
uname -m
# arm64  → 使用 dolphindb/dolphindb-arm64
# x86_64 → 使用 dolphindb/dolphindb
```

### 2. 内存计算
```bash
# 读取本机内存（字节）
mem_bytes=$(sysctl -n hw.memsize)  # macOS
# 或
mem_bytes=$(grep MemTotal /proc/meminfo | awk '{print $2 * 1024}')  # Linux

# 转换为 GB 并取 50%
mem_gb=$((mem_bytes / 1024 / 1024 / 1024))
mem_limit=$((mem_gb / 2))
```

### 3. Docker 启动命令
```bash
docker run -itd --name dolphindb \
  --hostname cnserver10 \
  --platform <架构> \
  -m <内存>g \
  -p 8848:8848 \
  -p 8849:8849 \
  -v /etc:/dolphindb/etc \
  -v <主机数据目录>:/data/ddb/server \
  dolphindb/<镜像>:<版本>
```

## 验证部署

```bash
# 检查容器状态
docker ps --filter name=dolphindb

# 查看日志
docker logs dolphindb

# 访问 Web UI
curl http://localhost:8848

# Python 连接测试
python3 -c "
import dolphindb as ddb
s = ddb.session()
s.connect('localhost', 8848)
print(s.run('version()'))
"
```

## 注意事项

1. **首次部署**：数据目录会自动初始化
2. **升级版本**：保留数据目录，只需更换镜像版本
3. **内存调整**：修改 `maxMemSize` 配置文件后重启容器
4. **端口冲突**：如 8848 被占用，修改 `-p` 参数

## 故障排查

### 容器启动失败
```bash
# 查看详细日志
docker logs dolphindb

# 检查端口占用
lsof -i:8848
```

### 内存不足
```bash
# 降低内存限制
docker run -m 4g ...
```

### 架构不匹配
```bash
# 确认本机架构
uname -m

# 使用对应镜像
# ARM64: dolphindb/dolphindb-arm64
# x86_64: dolphindb/dolphindb
```
