# 常见问题排查

## 1. psql 连接失败

**症状：** `psql: could not connect to server`

**原因：** PostgreSQL 未运行

**解决：**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 2. 密码错误

**症状：** `FATAL: password authentication failed`

**原因：** 密码填错了或没设置

**解决：**
```bash
sudo -u postgres psql -c "ALTER USER cognitivebrain WITH PASSWORD 'cog_brain_2024';"
```
然后更新 `config.json` 里的密码。

---

## 3. vector 扩展不存在

**症状：** `ERROR: extension "vector" not installed`

**解决：**
```bash
sudo -u postgres psql -d cognitive_brain -c "CREATE EXTENSION vector;"
```

如果报错说 vector 扩展不存在，先安装 pgvector：
```bash
sudo apt install postgresql-14-pgvector  # Ubuntu/Debian
```

---

## 4. Redis 连接失败

**症状：** `redis-cli ping` 返回 `Could not connect`

**解决：**
```bash
sudo systemctl start redis
sudo systemctl enable redis
redis-cli ping  # 应该返回 PONG
```

---

## 5. Node.js 未安装

**症状：** `bash: node: command not found`

**解决：**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash -
sudo apt install -y nodejs
node -v  # 应该显示 v18.x.x
```

---

## 6. 数据库不存在

**症状：** `FATAL: database "cognitive_brain" does not exist`

**解决：**
```bash
sudo -u postgres psql -c "CREATE DATABASE cognitive_brain;"
```

---

## 7. 端口被占用

**症状：** PostgreSQL 或 Redis 无法启动，`Address already in use`

**解决：**
```bash
# 查找占用端口的进程
sudo lsof -i :5432  # PostgreSQL
sudo lsof -i :6379  # Redis

# 杀掉进程或改端口
sudo systemctl stop <进程名>
```

---

## 8. Hook 启用失败

**症状：** `openclaw hooks enable` 报错

**解决：**
```bash
# 确认 hook 文件存在
ls ~/.openclaw/hooks/cognitive-recall/

# 手动复制
cp -r ~/.openclaw/workspace/skills/cognitive-brain/hooks/cognitive-recall ~/.openclaw/hooks/

# 启用
openclaw hooks enable cognitive-recall
openclaw hooks list  # 确认状态
```

---

## 9. 向量搜索报错 dimension mismatch

**症状：** 写入记忆时报 `dimension mismatch`

**原因：** 向量模型维度不一致（config.json 里的维度需要和模型匹配）

**解决：**
```bash
# 检查 config.json 里的 embedding provider
# 如果用 all-MiniLM-L6-v2，向量维度是 384
# 如果用其他模型，修改 vector(384) 为实际维度
```

修复维度需要重建表：
```sql
DROP TABLE memories;
CREATE TABLE memories (
    ...
    embedding vector(384),  -- 改成正确的维度
    ...
);
```
