# Cognitive Brain 部署详细指南

## 环境要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| 系统 | Ubuntu 20.04+ / Debian 11+ | Ubuntu 22.04 |
| 内存 | 2 GB | 4 GB+ |
| 硬盘 | 10 GB | 20 GB+ |
| PostgreSQL | 14+ | 14+ |
| Redis | 6+ | 7+ |
| Node.js | 18+ | 20 LTS |

---

## 第一步：安装基础依赖

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash - && \
sudo apt install -y postgresql postgresql-contrib redis-server git && \
sudo systemctl enable --now postgresql redis
```

**验证：**
```bash
sudo -u postgres psql -c "SELECT version();"
redis-cli ping
```

---

## 第二步：创建数据库

### 2.1 创建数据库和用户

```bash
sudo -u postgres psql
```

在 psql 里执行：

```sql
CREATE DATABASE cognitive_brain;
CREATE USER cognitivebrain WITH PASSWORD 'cog_brain_2024';
GRANT ALL PRIVILEGES ON DATABASE cognitive_brain TO cognitivebrain;
\c cognitive_brain
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
GRANT ALL ON SCHEMA public TO cognitivebrain;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cognitivebrain;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cognitivebrain;
```

### 2.2 创建表结构

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'general',
    importance FLOAT DEFAULT 0.5,
    embedding vector(384),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE associations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    to_id UUID REFERENCES memories(id) ON DELETE CASCADE,
    weight FLOAT DEFAULT 0.5,
    relation_type VARCHAR(50),
    UNIQUE(from_id, to_id)
);

CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON memories USING gin (content gin_trgm_ops);
\q
```

### 2.3 测试连接

```bash
PGPASSWORD=cog_brain_2024 psql -h localhost -U cognitivebrain -d cognitive_brain -c "SELECT COUNT(*) FROM memories;"
```

---

## 第三步：安装 Cognitive Brain Skill

```bash
mkdir -p ~/.openclaw/workspace/skills
cd ~/.openclaw/workspace/skills
git clone <repo> cognitive-brain
cd cognitive-brain
npm install
```

### 配置 config.json

```json
{
  "storage": {
    "primary": {
      "host": "localhost",
      "port": 5432,
      "database": "cognitive_brain",
      "user": "cognitivebrain",
      "password": "cog_brain_2024"
    },
    "cache": {
      "type": "redis",
      "host": "localhost",
      "port": 6379
    }
  },
  "embedding": {
    "provider": "local"
  }
}
```

### 可选：安装向量模型（让搜索更聪明）

```bash
pip3 install sentence-transformers --break-system-packages
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## 第四步：验证部署

```bash
cd ~/.openclaw/workspace/skills/cognitive-brain

# 健康检查
node scripts/recall.cjs health_check

# 测试写入
node scripts/encode.cjs \
  --content "测试记忆" \
  --metadata '{"type":"fact","importance":0.8}'

# 测试搜索
node scripts/recall.cjs --query "测试"
```

---

## 第五步：配置定时任务

```bash
crontab -e
```

添加：

```crontab
# 每天凌晨3点：清理不重要记忆
0 3 * * * cd ~/.openclaw/workspace/skills/cognitive-brain && node scripts/forget.cjs >> ~/.openclaw/logs/brain-forget.log 2>&1

# 每天凌晨4点：自我反思
0 4 * * * cd ~/.openclaw/workspace/skills/cognitive-brain && node scripts/reflect.cjs >> ~/.openclaw/logs/brain-reflect.log 2>&1

# 每天凌晨5点：自主学习
0 5 * * * cd ~/.openclaw/workspace/skills/cognitive-brain && node scripts/autolearn.cjs >> ~/.openclaw/logs/brain-autolearn.log 2>&1
```

```bash
mkdir -p ~/.openclaw/logs
touch ~/.openclaw/logs/brain-forget.log ~/.openclaw/logs/brain-reflect.log ~/.openclaw/logs/brain-autolearn.log
```

---

## 第六步：启用 Hook

```bash
cp -r ~/.openclaw/workspace/skills/cognitive-brain/hooks/cognitive-recall ~/.openclaw/hooks/
openclaw hooks enable cognitive-recall
openclaw hooks list
```

---

## 一句话流程

```
数据库装好 → 表建好 → Skill下载 → config.json填密码 → cron配好 → Hook启用
```
