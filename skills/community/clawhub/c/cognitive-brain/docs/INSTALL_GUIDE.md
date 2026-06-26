# Cognitive Brain v5.0 - 完整安装使用指南

## 📋 目录
1. [安装前准备](#安装前准备)
2. [安装步骤](#安装步骤)
3. [初始配置](#初始配置)
4. [验证安装](#验证安装)
5. [基础使用](#基础使用)
6. [高级功能](#高级功能)
7. [故障排查](#故障排查)

---

## 安装前准备

### 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Linux / macOS | Ubuntu 22.04 LTS |
| Node.js | 18.x | 20.x |
| 内存 | 2GB | 4GB+ |
| 磁盘 | 10GB 可用空间 | 50GB+ |
| PostgreSQL | 14.x | 16.x |
| Redis | 6.x | 7.x |

### 依赖安装

**Ubuntu/Debian:**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 PostgreSQL 和 Redis
sudo apt install -y postgresql postgresql-contrib redis-server

# 安装 pgvector 扩展
sudo apt install -y postgresql-16-pgvector  # 根据 PG 版本调整

# 启动服务
sudo systemctl start postgresql
sudo systemctl start redis-server
sudo systemctl enable postgresql
sudo systemctl enable redis-server

# 创建数据库
sudo -u postgres createdb cognitive_brain
```

**macOS:**
```bash
# 使用 Homebrew
brew install node postgresql redis pgvector

# 启动服务
brew services start postgresql
brew services start redis

# 创建数据库
createdb cognitive_brain
```

---

## 安装步骤

### 方式一：ClawHub 安装（推荐）

```bash
# 检查系统
skillhub search cognitive-brain

# 安装
skillhub install cognitive-brain

# 安装程序会自动:
# 1. 检查系统依赖
# 2. 提示输入配置
# 3. 初始化数据库
# 4. 运行测试
```

### 方式二：手动安装

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills

# 2. 克隆仓库
git clone <repository-url> cognitive-brain
cd cognitive-brain

# 3. 检查依赖
node scripts/tools/check-requirements.cjs

# 4. 安装依赖
npm install

# 5. 运行安装脚本（交互式配置）
npm run install
# 或
node scripts/tools/postinstall.cjs
```

### 安装过程示例

```
🧠 Cognitive Brain v5.0 安装程序
==================================================

🔍 检查系统依赖...

  Node.js... ✅ v20.11.0
  PostgreSQL... ✅ 16.4
  PostgreSQL 服务... ✅ running
  Redis... ✅ running
  pgvector 扩展... ✅ available

⚙️  配置 Cognitive Brain

请提供数据库连接信息（按 Enter 使用默认值）

PostgreSQL 主机 [localhost]: 
PostgreSQL 端口 [5432]: 
PostgreSQL 数据库名 [cognitive_brain]: 
PostgreSQL 用户名 [postgres]: 
PostgreSQL 密码: mysecretpassword
Redis 主机 [localhost]: 
Redis 端口 [6379]: 

✅ 配置已保存

🗄️  测试数据库连接...
  ✅ PostgreSQL 连接成功

🗄️  初始化数据库...
  ✅ 数据库表已创建
  ✅ 索引已建立

🔄 同步 hooks...
  ✅ Hook 已安装: cognitive-recall

📅 设置定时任务...
  ✅ 定时任务已设置

📁 创建数据文件...
  ✅ 创建: .user-model.json
  ✅ 创建: .working-memory.json
  ✅ 创建: .prediction-cache.json

🧪 运行测试...
  ✅ should create instance
  ✅ should encode memory
  ✅ should recall memory
  ✅ should get stats

==================================================
✨ Cognitive Brain v5.0 安装完成!

使用方法:
  node src/index.js              # v5.0 新架构
  node scripts/core/brain.cjs    # v4.x 兼容
  ./tests/run.sh                 # 运行测试
```

---

## 初始配置

### 配置文件位置

主配置文件：`config.json`

```json
{
  "version": "5.3.25",
  "storage": {
    "primary": {
      "type": "postgresql",
      "host": "${PGHOST}",
      "port": "${PGPORT}",
      "database": "${PGDATABASE}",
      "user": "${PGUSER}",
      "password": "${PGPASSWORD}",
      "extensions": ["pgvector", "pg_trgm"]
    },
    "cache": {
      "type": "redis",
      "host": "${REDIS_HOST}",
      "port": "${REDIS_PORT}"
    }
  }
}
```

### 修改配置

```bash
# 直接编辑
nano config.json

# 或使用配置管理器
node src/config/index.js set storage.primary.password newpassword
```

---

## 验证安装

### 1. 健康检查

```bash
npm run health
# 或
node scripts/tools/health_check.cjs
```

预期输出：
```
🏥 Cognitive Brain 健康检查

==================================================

检查结果:
✅ 数据库          记忆:0 概念:0 关联:0
✅ Redis        模块可用
✅ 配置           格式正确
✅ 数据文件         全部初始化
✅ Cron任务       已配置
✅ 磁盘空间         已用 45%

==================================================

健康分数: 100/100 (A)
✨ 系统状态良好！
```

### 2. 运行测试

```bash
# 运行所有测试
npm test

# 运行 v5.0 测试
npm run test:v5

# 预期输出
🧪 Running Cognitive Brain Tests

============================================================
  ✅ should create instance
  ✅ should encode memory
  ✅ should recall memory
  ✅ should get stats

============================================================

Results: 4 passed, 0 failed
```

### 3. 基础功能测试

```bash
# 编码记忆
node scripts/core/encode.cjs "这是我的第一条记忆" -t conversation -i 0.8

# 检索记忆
node scripts/core/recall.cjs --query "记忆" --limit 5
```

---

## 基础使用

### 使用 v5.0 新架构（推荐）

```javascript
// test-brain.js
const { CognitiveBrain } = require('./src/index.js');

async function main() {
  const brain = new CognitiveBrain();
  
  // 编码记忆
  const memory = await brain.encode('今天学习了 Node.js 的 Stream API', {
    type: 'conversation',
    importance: 0.8,
    sourceChannel: 'qq',
    role: 'user',
    entities: ['Node.js', 'Stream API']
  });
  
  console.log('已创建记忆:', memory.id);
  
  // 检索记忆
  const memories = await brain.recall('Node.js', { limit: 5 });
  console.log('找到记忆:', memories.length);
  
  // 获取统计
  const stats = await brain.stats();
  console.log('系统统计:', stats);
}

main().catch(console.error);
```

运行：
```bash
node test-brain.js
```

### 使用 CLI 工具

```bash
# 编码记忆
node scripts/core/encode.cjs "内容" \
  -t conversation \
  -i 0.8 \
  -c qq

# 参数说明:
# -t, --type      记忆类型 (conversation|reflection|lesson|...)
# -i, --importance 重要性 (0-1)
# -c, --channel    来源渠道

# 检索记忆
node scripts/core/recall.cjs \
  --query "关键词" \
  --limit 10 \
  --type conversation

# 遗忘记忆（清理低重要性）
node scripts/core/forget.cjs run

# 查看统计
node scripts/core/forget.cjs stats

# 可视化
node scripts/core/visualize.cjs
```

### 使用 API（开发中）

```javascript
// 启动 API 服务器（计划中）
node src/api/server.js

// 使用 HTTP API
curl -X POST http://<your-host>:<your-port>/api/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "测试", "type": "conversation"}'
```

---

## 高级功能

### 1. 事务操作

```javascript
const { UnitOfWork } = require('./src/repositories/UnitOfWork.js');
const { MemoryRepository } = require('./src/repositories/MemoryRepository.js');

await UnitOfWork.withTransaction(pool, async (uow) => {
  const memRepo = new MemoryRepository(uow.getQueryClient());
  
  // 多个操作原子执行
  await memRepo.create(memory1);
  await memRepo.create(memory2);
  await memRepo.update(id, { importance: 0.9 });
  
  // 自动 commit 或 rollback
});
```

### 2. 批量操作

```javascript
// 批量编码
const memories = [
  { content: '记忆1', type: 'test' },
  { content: '记忆2', type: 'test' }
];

for (const m of memories) {
  await brain.encode(m.content, { type: m.type });
}
```

### 3. 自定义查询

```javascript
const { MemoryRepository } = require('./src/repositories/MemoryRepository.js');

const repo = new MemoryRepository(pool);

// 高重要性记忆
const important = await repo.findImportant(0.8, ['lesson', 'reflection'], 10);

// 搜索
const results = await repo.search('关键词', {
  limit: 10,
  type: 'conversation',
  minImportance: 0.5
});
```

---

## 故障排查

### 问题1：数据库连接失败

**现象：**
```
❌ PostgreSQL 连接失败: connection refused
```

**解决：**
```bash
# 检查服务状态
sudo systemctl status postgresql

# 启动服务
sudo systemctl start postgresql

# 检查监听配置
sudo nano /etc/postgresql/16/main/postgresql.conf
# 确保: listen_addresses = 'localhost'

# 重启服务
sudo systemctl restart postgresql
```

### 问题2：pgvector 扩展未安装

**现象：**
```
❌ ERROR: extension "vector" is not available
```

**解决：**
```bash
# Ubuntu/Debian
sudo apt install postgresql-16-pgvector

# 或在数据库中启用
sudo -u postgres psql cognitive_brain -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 问题3：Hook 未生效

**现象：**
记忆没有自动注入到对话中

**解决：**
```bash
# 检查 hook 是否安装
ls ~/.openclaw/hooks/cognitive-recall/

# 手动同步
npm run sync-hooks

# 重启 OpenClaw
openclaw gateway restart
```

### 问题4：权限错误

**现象：**
```
permission denied for table episodes
```

**解决：**
```bash
# 授予权限
sudo -u postgres psql cognitive_brain -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;"
```

### 问题5：内存不足

**现象：**
```
FATAL: Out of memory
```

**解决：**
```bash
# 限制 Redis 内存
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# 或编辑配置文件
sudo nano /etc/redis/redis.conf
```

---

## 常用命令速查

```bash
# 安装和配置
npm install                    # 安装依赖
npm run check                  # 检查系统
npm run install                # 交互式安装
npm test                       # 运行测试

# 日常使用
npm run health                 # 健康检查
npm run encode -- "内容"        # 编码记忆
npm run recall -- --query "x"  # 检索记忆
npm run forget                 # 运行遗忘
npm run visualize              # 生成可视化

# 调试
node scripts/tools/health_check.cjs
node scripts/core/brain.cjs health_check
ls -la ~/.openclaw/hooks/
tail -f /tmp/brain-cron.log
```

---

## 下一步

- 阅读 [API 文档](./docs/README.md)
- 阅读 [架构文档](./docs/ARCHITECTURE.md)
- 查看 [示例代码](./examples/)

---

**遇到问题？** 提交 Issue 或查看 [FAQ](./docs/FAQ.md)

