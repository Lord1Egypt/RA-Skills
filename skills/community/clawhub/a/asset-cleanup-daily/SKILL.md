---
name: asset-cleanup-daily
version: "1.0.0"
description: "每日资产清理器,Cron每日03:00清理过期临时文件/旧日志/无效缓存/过期素材,释放磁盘空间+写入清理报告。触发:asset-cleanup-daily Cron(每日03:00)/素材清理/资产清理/磁盘清理/临时文件清理。不触发:实时资产告警(health-monitor-mcp负责)"
tools: [read, exec]
dependencies: []
metadata:
  layer: infrastructure
  priority: P2
  category: maintenance
  openclaw:
    emoji: "🧹"
    color: "#16a085"
    vibe: "clean"
    os: ["win32", "linux", "darwin"]
    exec_scripts: ["asset_cleanup.py"]
    requires:
      bins: ["python"]
      config: []
      env: ["JUEJIN_HOME"]
---

# Asset Cleanup Daily 每日资产清理器

**版本**: v1.0.0 | **优先级**: P2（基础设施维护） | **所属层**: 基础设施层(资产清理)

> 来源: T2-6素材清理 | 05文档§五L1096 | BUG-ASSET-CLEANUP-SKILL-MISSING修复
> Cron配置: data/cron_tasks.json `asset-cleanup-daily` (schedule: `0 3 * * *`)

## 使用场景

- 每日03:00自动清理过期临时文件(data/temp_*.txt, data/test_*.txt等临时产物)
- 清理旧日志文件(data/*.jsonl超过30天的日志,与log-rotate Cron互补)
- 清理无效缓存文件(data/*.lock过期锁文件, *.bak备份文件)
- 清理过期素材(调用scripts/asset_cleanup.py清理tenant_assets表中过期记录+物理文件)
- 输出结构化清理报告(删除文件数/释放空间/跳过数/错误列表)
- 仅清理+报告,不触发告警(告警由health-monitor-mcp负责)

## 设计背景

### 问题诊断(BUG-ASSET-CLEANUP-SKILL-MISSING)
cron_tasks.json中已配置`asset-cleanup-daily` Cron任务(schedule: `0 3 * * *`),但对应的Skill未创建,导致Cron触发时OpenClaw找不到Skill执行清理逻辑。

### 业务规则(来源:04部署文档§2环境+§10故障)
- 临时文件保留期: 1天(当日生成的temp/test文件次日清理)
- 日志文件保留期: 30天(与log-rotate Cron互补,log-rotate处理scripts/operation_logger.py日志,本Skill处理data/*.jsonl)
- 锁文件保留期: 1天(超过1天的.lock文件视为僵尸锁,安全清理)
- 备份文件保留期: 7天(.bak/.backup文件超过7天清理)
- 素材有效期: tenant_assets.expires_at < NOW()(来源:09设计文档U2,scripts/asset_cleanup.py已实现)

### 部署约束(来源:04部署文档)
- JUEJIN_HOME环境变量: 项目根路径(默认d:\JueJin)
- 数据目录: $JUEJIN_HOME/data/
- 日志统一入口: db_logger(来源:18_统一入口规则)
- 原子写入入口: atomic_write(来源:18_统一入口规则)
- PG连接: POSTGRES_CONNECTION_STRING环境变量(scripts/asset_cleanup.py使用)

### 闭环验证标准
- L1: frontmatter格式正确,tools/metadata完整
- L2: py_compile语法通过,正常→success=true+data,异常→success=false+error+code
- L3: Cron触发→Skill加载→exec执行→JSON输出
- L4: 磁盘空间释放可验证(清理前后data/目录大小对比)

## 工作流

1. 初始化清理环境
   - 读取JUEJIN_HOME环境变量确定项目根路径
   - 初始化db_logger记录清理过程
   - 执行: `python skills/asset-cleanup-daily/scripts/asset_cleanup.py [--dry-run]`

2. 清理过期临时文件
   - 扫描data/目录下temp_*.txt/test_*.txt/test_*.json/test_*.out等临时产物
   - 文件修改时间超过1天(86400秒)的视为过期
   - 删除过期临时文件,记录删除数量和释放空间

3. 清理旧日志文件
   - 扫描data/目录下*.jsonl日志文件
   - 文件修改时间超过30天(2592000秒)的视为过期
   - 删除过期日志文件(与log-rotate Cron互补,log-rotate处理operation_logger日志)
   - 跳过活跃日志文件(alert_queue.jsonl/budget_alerts.jsonl等高频写入文件即使超龄也保留)

4. 清理无效缓存和锁文件
   - 扫描data/目录下*.lock文件(超过1天的僵尸锁)
   - 扫描项目根目录下*.bak/*.backup文件(超过7天的旧备份)
   - 安全删除,记录清理结果

5. 清理过期素材(可选,PG可用时执行)
   - 调用scripts/asset_cleanup.py清理tenant_assets表中expires_at < NOW()的记录
   - 删除PG记录+物理文件+AList远程文件
   - PG不可用时跳过(降级处理,不影响其他清理步骤)

6. 输出清理报告
   - 汇总各类清理结果(临时文件/日志/缓存/素材)
   - 使用atomic_write写入清理报告到data/audit/asset_cleanup_YYYY-MM-DD.json
   - stdout输出JSON: {success, data:{temp_files, log_files, cache_files, assets, total_freed}, error, code}

## 输入格式

```json
{
  "dry_run": false
}
```

参数说明:
- `dry_run`(可选): true时只扫描不删除,默认false

## 输出格式

```json
{
  "success": true,
  "data": {
    "temp_files": {
      "scanned": 15,
      "deleted": 12,
      "freed_bytes": 245678,
      "errors": []
    },
    "log_files": {
      "scanned": 18,
      "deleted": 3,
      "freed_bytes": 1024000,
      "errors": []
    },
    "cache_files": {
      "scanned": 5,
      "deleted": 2,
      "freed_bytes": 512,
      "errors": []
    },
    "assets": {
      "cleaned": true,
      "expired_count": 5,
      "deleted_records": 5,
      "deleted_files": 4,
      "freed_bytes": 8192000,
      "skipped": "PG不可用时为null"
    },
    "total_freed_bytes": 9457190,
    "total_freed_human": "9.0MB",
    "report_path": "data/audit/asset_cleanup_2026-07-14.json"
  },
  "error": null,
  "code": null
}
```

## 异常处理

1. JUEJIN_HOME环境变量未设置 → 使用默认值d:\JueJin,记录warning
2. data/目录不存在 → 返回success=false+code=DATA_DIR_NOT_FOUND
3. 临时文件删除失败(OSError/PermissionError) → 记录错误到errors列表,继续清理其他文件
4. PG连接失败(scripts/asset_cleanup.py) → 跳过素材清理,其他清理正常执行,assets.cleaned=false
5. atomic_write报告写入失败 → 记录db_logger错误,不影响stdout JSON输出
6. 未知异常 → 返回success=false+error+code=INTERNAL_ERROR,exit(2)

## 清理规则明细

### 临时文件模式(保留1天)
- `data/temp_*.txt` - 临时文本片段
- `data/test_*.txt` / `data/test_*.json` / `data/test_*.out` - 测试产物
- `data/kanban/test.*` - 看板测试文件
- `data/ops/_vacuum_temp.sql` - PG真空临时SQL

### 日志文件模式(保留30天)
- `data/*.jsonl` - JSONL格式日志(排除活跃日志:alert_queue.jsonl, budget_alerts.jsonl, tenant_notifications.jsonl, mcp_pending_tasks.jsonl)
- 与log-rotate Cron互补: log-rotate处理scripts/operation_logger.py的30天轮转,本Skill处理data/目录下的JSONL日志

### 缓存/锁文件模式(保留1天锁/7天备份)
- `data/*.lock` - 过期锁文件(超过1天视为僵尸锁)
- `*.bak` / `*.backup` - 旧备份文件(超过7天)

### 素材清理(委托scripts/asset_cleanup.py)
- 查询tenant_assets表expires_at < NOW()的记录
- 删除PG记录+物理文件+AList远程文件
- PG不可用时降级跳过

## R72.1保护声明

本Skill实现R72.1: asset-cleanup-daily(基础设施层资产清理)为05文档§五L1096要求的Cron编排组件。
- 每日03:00执行,不影响调度公平性(R16例外:维护任务非调度任务)
- 清理操作不可逆,但仅清理过期/临时文件,不影响生产数据
- 与log-rotate Cron互补,不重复清理同一批文件

## 示例

### 示例1: 正常清理
```bash
python skills/asset-cleanup-daily/scripts/asset_cleanup.py
```
输出:
```json
{
  "success": true,
  "data": {
    "temp_files": {"scanned": 5, "deleted": 3, "freed_bytes": 1024, "errors": []},
    "log_files": {"scanned": 18, "deleted": 1, "freed_bytes": 512000, "errors": []},
    "cache_files": {"scanned": 2, "deleted": 1, "freed_bytes": 256, "errors": []},
    "assets": {"cleaned": true, "expired_count": 0, "deleted_records": 0, "deleted_files": 0, "freed_bytes": 0},
    "total_freed_bytes": 513280,
    "total_freed_human": "501.2KB",
    "report_path": "data/audit/asset_cleanup_2026-07-14.json"
  },
  "error": null,
  "code": null
}
```

### 示例2: 试运行(不删除)
```bash
python skills/asset-cleanup-daily/scripts/asset_cleanup.py --dry-run
```
输出同上,`deleted`字段表示待删除数量(实际未删除),`dry_run`标记为true。

### 示例3: PG不可用降级
PG连接失败时,assets字段降级:
```json
{
  "assets": {"cleaned": false, "expired_count": 0, "skipped": "PG不可用,跳过素材清理"}
}
```
