# ChromaDB官方插件 - LanceDB无缝迁移指南
本指南提供完整的LanceDB到ChromaDB迁移方案，全程可回滚，不影响现有业务运行。

## 📋 迁移前准备
### 1. 环境检查
✅ Python 3.10+
✅ 记忆进化成长项目V1.0+正常运行
✅ LanceDB数据目录完整（默认：I:\OpenClaw\知识库\lancedb）
✅ 剩余磁盘空间 >= 现有LanceDB数据大小的2倍
✅ 已安装ChromaDB插件（参考快速安装指南）

### 2. 数据备份
迁移前务必备份现有LanceDB数据：
```bash
# 直接复制整个lancedb目录到备份位置
xcopy I:\OpenClaw\知识库\lancedb I:\OpenClaw\知识库\lancedb_backup\ /E /H /C /I
```

### 3. 服务暂停建议
如果是生产环境，建议暂停每日量化任务10分钟，避免迁移过程中有新数据写入，迁移完成后自动恢复。如果是开发环境，可以不停机在线迁移。

## ⚡ 一键迁移（推荐）
运行内置迁移脚本自动完成全量迁移：
```bash
python tools/migrate_lancedb_to_chromadb.py
```

### 迁移脚本自动完成以下步骤：
1. ✅ 读取现有LanceDB配置，连接LanceDB数据库
2. ✅ 初始化ChromaDB数据库，自动创建相同结构的集合
3. ✅ 分批读取LanceDB中的所有数据（文本、向量、元数据、ID）
4. ✅ 批量写入到ChromaDB，显示实时进度条
5. ✅ 全量数据校验，对比两个库的文档数量、向量相似度、元数据一致性
6. ✅ 生成迁移报告，包含迁移耗时、成功率、错误列表（如果有）

### 迁移输出示例：
```
[*] 开始LanceDB到ChromaDB迁移...
[+] LanceDB连接成功，总文档数：2221
[+] ChromaDB连接成功，初始化集合完成
[*] 开始迁移数据，批次大小：100
[==================================================] 100% 2221/2221 [00:12<00:00, 185条/秒]
[+] 数据写入完成，开始校验...
[+] 文档数量校验通过：2221/2221
[+] 向量相似度校验通过：100% 数据完全一致
[+] 元数据校验通过：100% 元数据完全一致
[+] 迁移完成！总耗时：15.2秒，成功率：100%
[*] 迁移报告已保存到：reports/migration_report_20260329_1330.md
```

## 🔄 手动迁移步骤（可选）
如果需要自定义迁移流程，可以按以下步骤操作：
### 步骤1：导出LanceDB数据
```python
from core.vector_store import LanceDBStore

lance_vs = LanceDBStore(path="I:/OpenClaw/知识库/lancedb")
all_data = lance_vs.get_all()  # 获取所有数据

# 保存到临时JSON文件
import json
with open("lance_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
```

### 步骤2：导入到ChromaDB
```python
from core.vector_store import ChromaDBStore

chroma_vs = ChromaDBStore(path="I:/OpenClaw/知识库/chromadb")
chroma_vs.add(
    texts=all_data["documents"],
    metadatas=all_data["metadatas"],
    ids=all_data["ids"]
)
```

### 步骤3：校验数据一致性
```python
# 对比文档数量
assert lance_vs.count() == chroma_vs.count()

# 随机抽样验证
import random
sample_ids = random.sample(all_data["ids"], 100)
for doc_id in sample_ids:
    lance_doc = lance_vs.get_by_id(doc_id)
    chroma_doc = chroma_vs.get_by_id(doc_id)
    assert lance_doc == chroma_doc

print("所有数据校验通过！")
```

## ✅ 切换到ChromaDB
迁移完成并校验通过后，修改`config.yaml`配置：
```yaml
vector_store:
  type: chromadb  # 把原来的lancedb改成chromadb
  # 其他配置保持不变
```
重启服务即可生效，所有现有业务代码完全不需要修改。

## ↩️ 回滚方案
如果遇到任何问题，可以随时回滚到LanceDB：
1. 停止服务
2. 把`config.yaml`中的`type`改回`lancedb`
3. 重启服务即可，原有LanceDB数据完全不受影响

## 📈 迁移后验证
切换完成后运行测试脚本验证所有功能正常：
```bash
python tools/test_chromadb.py
```
确保所有测试用例通过后，删除临时备份文件即可。

## ⏱️ 迁移时间参考
| 数据量 | 迁移时间 | 校验时间 |
|--------|----------|----------|
| 1万条以内 | <30秒 | <10秒 |
| 10万条 | <5分钟 | <1分钟 |
| 100万条 | <30分钟 | <5分钟 |
| 1000万条 | <3小时 | <30分钟 |

## ⚠️ 注意事项
1. 迁移过程中不要修改LanceDB数据，否则会导致数据不一致
2. 大数量迁移建议在业务低峰期执行
3. 云端部署的ChromaDB迁移请参考官方文档调整批量大小，避免触发限流
4. 迁移完成后原有LanceDB数据可以保留3天，确认没问题再删除

---
**文档版本**: v1.0.0
**更新时间**: 2026-03-29 13:30
**作者**: 岚岚
