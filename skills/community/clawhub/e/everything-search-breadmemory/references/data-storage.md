# 数据存储结构

所有数据存储在 `~/.everything_search/`：

```
~/.everything_search/
├── breadcrumb.json         # 面包屑知识条目
├── donuts.json             # 拓扑甜甜圈关联图谱（独立存储）
├── config.json             # 配置（es.exe 路径、艾宾浩斯参数等）
├── review_log.jsonl        # 复习历史日志
├── breadcrumb_backup_01~09.bat  # 容灾备份（循环覆盖）
└── breadcrumb_backup_01~09.py   # 容灾恢复脚本
```
