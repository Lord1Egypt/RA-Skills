# 知识库管理流程

知识库内容存入SQLite，支持FTS5全文检索+向量语义检索，返回精确段落而非整个文件。
所有写入操作通过 `db_query.py` CLI 完成，智能体不可自行写文件或创建脚本。

## 添加知识

1. 接收用户内容（文本/文件）
2. 确认分类和产品名
3. 将文件放入知识库集对应目录 → 调用同步脚本写入数据库
4. 自动：生成摘要 → 提取关键词 → 切分段落(300字/段) → 计算向量 → FTS5索引

## 检索知识（核心优化）

**全量读取**：读取整个txt文件（500-1500字）→ 全部注入上下文
**精准检索**：只返回相关段落 → token节省70-90%

```bash
# 语义+关键词混合检索
python scripts/db_query.py --type knowledge --action search --query "养生保健" --top-k 5 --data-dir <控制台目录>

# 获取token预算内的精准上下文
python scripts/db_query.py --type knowledge --action context --query "产品A产品特点" --max-tokens 1000 --data-dir <控制台目录>

# 按分类浏览
python scripts/db_query.py --type knowledge --action list --data-dir <控制台目录>
python scripts/db_query.py --type knowledge --action docs --category 产品目录 --data-dir <控制台目录>
```

## 从文件批量导入

```bash
python scripts/db_sync.py --direction to-db --data-dir <控制台目录>
```

## 删除知识

```bash
# 从数据库删除文档
python scripts/db_query.py --type knowledge --action delete --id "产品目录/产品A/产品背书.txt" --data-dir <控制台目录>
```

删除操作同时将文件移入回收站（含.meta.json记录原始路径），恢复时从回收站移回并重新 `db_sync.py` 同步。
