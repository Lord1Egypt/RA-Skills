# 常见问题 (FAQ)

## 一般问题

### Q: 这个 Skill 是做什么的？
A: 为 OpenClaw Agent 提供长期记忆能力，支持语义检索和自动记忆抽取。

### Q: 需要付费吗？
A: 完全免费！LanceDB 是开源的，智谱 AI 提供免费额度（100 万 tokens）。

### Q: 数据安全吗？
A: 所有数据存储在本地，不会上传到任何服务器。

---

## 安装问题

### Q: Python 版本要求？
A: Python 3.8+，推荐 3.10+。

### Q: 安装失败怎么办？
A: 尝试升级 pip：`pip install --upgrade pip`

### Q: 虚拟环境必须吗？
A: 强烈推荐，避免依赖冲突。

---

## 使用问题

### Q: 如何添加记忆？
A: `python3 skill.py add --content "内容" --type preference`

### Q: 如何查看记忆？
A: `python3 skill.py profile`

### Q: 记忆会过期吗？
A: task 类型可以设置过期时间，其他类型永久保存。

### Q: 如何删除记忆？
A: 目前不支持直接删除，可以清理整个数据库：
```bash
rm -rf memory_lancedb/
```

---

## Hook 问题

### Q: Hook 不工作？
A: 检查：
1. Hook 文件是否存在
2. ZHIPU_API_KEY 是否设置
3. 查看 OpenClaw 日志

### Q: 如何禁用 Hook？
A: `openclaw hooks disable memory-system`

### Q: Hook 会影响性能吗？
A: 轻微影响（~100ms），因为要调用 Embedding API。

---

## API 问题

### Q: 智谱 AI API Key 哪里获取？
A: https://open.bigmodel.cn/ 注册后获取。

### Q: 免费额度用完了怎么办？
A: 智谱 AI 充值很便宜，或切换其他 Embedding 服务。

### Q: 可以用其他 Embedding 吗？
A: 可以，修改 `lancedb_memory.py` 中的 ZhipuEmbedding 类。

---

## 性能问题

### Q: 支持多少条记忆？
A: 理论无限制，实测 10 万条记忆检索延迟 <100ms。

### Q: 内存占用多少？
A: ~200MB 基础占用，每 1000 条约 +1MB。

### Q: 数据库多大？
A: ~100MB 基础，每 1000 条约 +100KB。

---

## 开发问题

### Q: 如何贡献代码？
A: Fork 仓库 → 创建分支 → 提交 PR

### Q: 如何报告 Bug？
A: GitHub Issues: https://github.com/asbinbin/claw_lance/issues

### Q: 有 API 文档吗？
A: 查看 [API.md](API.md)

---

需要更多帮助？开 Issue: https://github.com/asbinbin/claw_lance/issues
