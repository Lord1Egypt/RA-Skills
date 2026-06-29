# 权限说明

> 本文件为 everything-search-breadmemory 技能的权限风险说明，
> 供 AI 执行时判断授权方式。

## 权限总览

| # | 文件 | 行号 | 匹配内容 | 风险等级 | 授权方式 | 说明 |
|---|------|------|----------|----------|----------|------|
| 1 | `scripts/es_search.py` | （待扫描） | `subprocess` / `os.system` | 🔴 高 | 即时授权 | 调用 es.exe 进行本地文件搜索 |
| 2 | `scripts/breadcrumb.py` | （待扫描） | 文件读写 | 🟡 中 | 统一授权 | 读写 `~/.everything_search/breadcrumb.json` |
| 3 | `scripts/ebbinghaus.py` | （待扫描） | 文件读写 | 🟡 中 | 统一授权 | 读写 `~/.everything_search/review_log.jsonl` |

## 敏感信息访问

- **访问内容**：`~/.everything_search/` 目录下的知识条目、复习记录
- **访问方式**：Python 文件读写（`open()`）
- **授权方式**：统一授权（首次执行前批准，后续不再询问）
- **风险等级**：🟡 中（知识数据属于用户私人信息）

## 关键位置写入

- **写入内容**：面包屑条目、复习记录、拓扑甜甜圈关联数据
- **写入路径**：`~/.everything_search/breadcrumb.json`、`review_log.jsonl`、`donuts.json`
- **授权方式**：统一授权
- **风险等级**：🟡 中

## 授权方式说明

- **即时授权**：每次执行前需获得用户批准（高风险操作）
- **统一授权**：首次执行前获得用户批准，后续不再询问（中风险操作）
- **静默执行**：无需授权，直接执行（低风险操作）

## 备注

- es.exe 调用通过 `subprocess.run()` 执行，属于高风险操作，需即时授权
- 知识数据存储在用户主目录，不对外传输，风险可控
- 容灾备份脚本（`breadcrumb_backup_*.bat`/`*.py`）仅本地操作，风险等级🟢 低
