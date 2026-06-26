# DolphinDB Docker 自动化部署

## 🚀 快速开始

```bash
# 一键部署（自动检测架构和内存）
./skills/dolphindb-docker/deploy-dolphindb.sh

# 部署指定版本
./skills/dolphindb-docker/deploy-dolphindb.sh v2.00.7

# 自定义内存（GB）
./skills/dolphindb-docker/deploy-dolphindb.sh v2.00.7 8

# 自定义数据目录
./skills/dolphindb-docker/deploy-dolphindb.sh v2.00.7 8 /path/to/data
```

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🎯 **自动架构检测** | ARM64/x86_64 自动识别，选择正确镜像 |
| 🧠 **智能内存分配** | 读取本机内存，按 50% 原则自动分配 |
| 📦 **完整持久化** | 整个 `/data/ddb/server` 目录挂载到主机 |
| 🔑 **License 支持** | 自动挂载 `/etc` 用于指纹采集 |
| 🔄 **版本升级** | 保留数据，只需更换镜像版本 |

## 📊 部署逻辑

### 1. 芯片检测
```bash
uname -m
# arm64  → dolphindb/dolphindb-arm64
# x86_64 → dolphindb/dolphindb
```

### 2. 内存计算（50% 原则）
```bash
# macOS
sysctl -n hw.memsize  # 25769803776 字节 = 24GB
# 分配：24GB / 2 = 12GB

# 限制：最低 2GB，最高 32GB
```

### 3. 数据目录初始化
- 首次部署：从镜像自动初始化
- 再次部署：保留原有数据

### 4. Docker 启动
```bash
docker run -itd --name dolphindb \
  --hostname cnserver10 \
  --platform linux/arm64 \
  -m 12g \
  -p 8848:8848 \
  -p 8849:8849 \
  -v /etc:/dolphindb/etc \
  -v /Users/mac/Documents/dolphindb_docker_server:/data/ddb/server \
  dolphindb/dolphindb-arm64:v2.00.7
```

## 📁 目录结构

```
dolphindb-docker/
├── SKILL.md              # 技能说明
├── deploy-dolphindb.sh   # 部署脚本
└── README.md             # 本文档

主机数据目录：
/Users/mac/Documents/dolphindb_docker_server/
├── dolphindb             # 二进制程序（持久化）
├── dolphindb.cfg         # 配置文件（可编辑）
├── dolphindb.lic         # 许可证
├── dolphindb.log         # 日志文件
├── data/                 # 数据目录
│   ├── local8848/
│   ├── storage/
│   └── ...
├── plugins/              # 插件目录
└── web/                  # Web UI 文件
```

## 🔧 配置说明

### 修改内存
编辑 `dolphindb.cfg`：
```ini
maxMemSize=8  # 单位：GB
```

### 修改端口
编辑 `dolphindb.cfg`：
```ini
localSite=localhost:9999:local9999
subPort=9998
```

启动时修改端口映射：
```bash
-p 9999:9999 -p 9998:9998
```

## 🧪 验证部署

```bash
# 检查容器状态
docker ps --filter name=dolphindb

# 查看日志
docker logs dolphindb

# 访问 Web UI
open http://localhost:8848

# Python 连接测试
python3 << 'EOF'
import dolphindb as ddb
s = ddb.session()
s.connect("localhost", 8848)
print("版本:", s.run("version()"))
print("内存:", s.run("getMemoryStat()"))
s.close()
EOF
```

## 🛠️ 运维命令

```bash
# 启动
docker start dolphindb

# 停止
docker stop dolphindb

# 重启
docker restart dolphindb

# 删除（数据保留）
docker rm dolphindb

# 查看资源使用
docker stats dolphindb

# 进入容器
docker exec -it dolphindb sh
```

## 🔄 版本升级

```bash
# 1. 停止旧容器
docker stop dolphindb
docker rm dolphindb

# 2. 拉取新镜像
docker pull dolphindb/dolphindb-arm64:v2.00.8

# 3. 使用新镜像启动（数据目录不变）
./deploy-dolphindb.sh v2.00.8

# 4. 验证升级
python3 -c "import dolphindb as ddb; s=ddb.session(); s.connect('localhost',8848); print(s.run('version()'))"
```

## 🐛 故障排查

### 容器无法启动
```bash
# 查看详细日志
docker logs dolphindb

# 检查端口占用
lsof -i:8848

# 检查数据目录权限
ls -la /Users/mac/Documents/dolphindb_docker_server/
```

### 内存不足
```bash
# 降低内存限制
./deploy-dolphindb.sh v2.00.7 4

# 或修改配置文件
maxMemSize=2
```

### 架构不匹配
```bash
# 确认本机架构
uname -m

# ARM64 Mac 使用
dolphindb/dolphindb-arm64

# Intel Mac 使用
dolphindb/dolphindb
```

## 📝 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.00.7 | 2026-04-21 | 初始版本，支持 ARM64/x86_64 |

## 📞 支持

- 官方文档：https://dolphindb.cn/
- Docker Hub: https://hub.docker.com/u/dolphindb
- GitHub: https://github.com/dolphindb
