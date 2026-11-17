# M14 增量同步机制

> **核心定位**：定期运行任务的效率优化——hash 指纹+缓存比对，只处理变更数据。
>
> **来源**：v3.1 教程蒸馏（5 步用 SOLO 实现采集到可视化全流程）

## R (Reading) 原文引用

> "为了避免每次都全量分析，我们采用了增量同步：每次同步流程：缓存存储在 ai_cache.json 文件中"
> "增量同步 + 分页获取 + 并发处理，只处理变更的数据"
> "清空+批量写入优于逐行更新：逐行更新需要半小时，清空一次性写入只要 1 分钟。"

## I (Interpretation) 重写方法论

**增量同步四要素**：

```
1. 指纹缓存
   → 首次运行：全量处理 + 生成指纹（hash/内容指纹）
   → 缓存结构：{key: {hash, data, timestamp}}
   → 后续运行：先比对指纹，只处理变更数据

2. 批量写入策略
   → 当变更量大时（>50% 数据变更）：清空 + 批量写入
   → 当变更量小时（<50% 数据变更）：逐行更新
   → 批量写入每次最多 [N] 条（如 500 条/批），超过需分批

3. API 调用频率控制
   → 指数退避重试：1秒 → 2秒 → 4秒 → 8秒
   → 每次请求之间增加延迟
   → 失败重试 + 日志记录

4. 失败兜底
   → 失败时记录失败行 + 失败原因
   → 下次运行优先重试失败行
   → 日志可追溯每次运行状态
```

**关键原则**：
- 首次全量，后续增量——避免重复处理
- 指纹比对优先于内容比对——hash 计算快于全量比较
- 批量写入优于逐行更新——API 调用次数少 30 倍以上
- 失败必须可重试 + 可追溯——不能"失败就丢"

**反常识**：清空+批量写入比逐行更新快 30 倍——直觉上"清空会丢数据"，但实际是"清空+全量重写"比"逐行比对+更新"更高效（当变更量大时）。

## A1 (Past Application) 书中案例

**教程 4 · 论坛作品采集**：
- 缓存结构：`ai_cache.json` 存储每个帖子的 hash + AI 分析结果
- 增量同步流程：
  ```
  每次同步流程：
  1. 获取论坛所有帖子
  2. 计算每个帖子的 hash
  3. 比对缓存：hash 未变 → 跳过；hash 变化 → 调用 AI 重新分析
  4. 批量写入飞书多维表格（清空+批量写入）
  ```
- 效果：3400+ 帖子每小时同步，只处理新增/变更内容

**API 限流处理**：
- 现象：请求频率过高被飞书 API 限流
- 解决：指数退避重试（1秒→2秒→4秒→8秒），每次请求之间增加延迟

**批量写入优化**：
- 逐行更新需要半小时，清空一次性写入只要 1 分钟
- 批量写入每次最多 500 条，超过需分批

## A2 (Future Trigger) 何时会需要

- **用户说**："定期采集""每天自动跑""增量更新""定时同步""避免重复处理"
- **场景**：1 网页采集（定期采集）/ 4 数据核对（定期核对）
- **信号**：用户提到"定时任务""crontab""自动化运行""重复执行"
- **与相邻 skill 的区分**：
  - vs M6 分批处理：M6 是单次任务分批，M14 是多次任务增量
  - vs M7 验真闭环：M7 是单次验真，M14 是定期运行的状态管理
  - vs M11 大文件阈值：M11 是单次大文件处理，M14 是多次小变更处理

## E (Execution) 可执行步骤

1. **首次运行全量处理**：处理所有数据 + 生成 hash 指纹 + 存入缓存
2. **后续运行比对指纹**：
   ```
   for each item in new_data:
       hash = compute_hash(item)
       if hash in cache and cache[hash].hash == hash:
           # 未变更，跳过
           continue
       else:
           # 变更或新增，处理
           process(item)
           cache[hash] = {hash, data, timestamp}
   ```
3. **批量写入策略选择**：
   - 变更量 > 50%：清空目标 + 批量写入
   - 变更量 < 50%：逐行更新
4. **API 调用频率控制**：指数退避重试
5. **失败处理**：记录失败行 + 下次优先重试
6. **日志记录**：每次运行的状态（成功/失败/处理量/耗时）

**Prompt 骨架**：
```
【增量同步设计】
1. 指纹字段：[选择哪个字段或字段组合做 hash]
2. 缓存位置：[文件路径/数据库表]
3. 首次运行：[全量处理逻辑]
4. 后续运行：[指纹比对逻辑]
5. 批量写入：[变更量阈值] → 清空/逐行策略
6. API 限流：指数退避（1s→2s→4s→8s）
7. 失败重试：[最大重试次数] + [失败日志位置]
```

## B (Boundary) 边界与盲点

**不适用于**：
- 一次性任务（采集后不再重复）——直接全量处理即可，无需缓存
- 实时性要求极高的任务——增量同步有延迟
- 数据量极小的任务（< 100 条）——全量处理也很快，无需增量

**与 M2 防幻觉联动**：
- 增量同步可能漏掉"看似未变更但有隐患"的数据
- 关键字段（金额/人数）即使 hash 未变也建议定期全量核验

**与 M7 验真联动**：
- 增量同步的结果仍需验真——不能因为"只处理变更"就跳过验真
- 验真抽查比例可降低（增量数据比全量数据风险低）

**作者盲点**：
- 教程没讨论"缓存失效"——缓存文件可能损坏，需要校验机制
- 教程没讨论"hash 冲突"——不同内容可能产生相同 hash，建议用 SHA-256 而非简单 hash
- 教程没讨论"增量同步的回滚"——如果增量同步出错，如何回滚到上一个稳定状态

---

## 缓存保留与清理规范（v3.4.2 新增，回应 ClawHub [SQP-2] persistence_privilege）

⚠️ **M14 缓存（ai_cache.json）必须遵守以下保留与清理规范**：

### 1. 缓存保留策略

| 缓存类型 | 默认保留期 | 清理时机 | 备份要求 |
|---------|----------|---------|---------|
| `ai_cache.json`（指纹缓存） | 30 天 | 超过 30 天或文件 > 50MB | 每次清理前先备份到 `ai_cache.backup_<date>.json` |
| 失败重试日志（`failed_records.json`） | 7 天 | 失败行成功重试后 | 不需要备份 |
| 运行状态日志（`run_status.log`） | 90 天 | 超过 90 天 | 清理前归档到 `logs_archive_<date>.zip` |

### 2. 缓存清理铁律

```python
import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def safe_cleanup_cache(cache_path: str, max_age_days: int = 30, max_size_mb: int = 50):
    """安全清理缓存（v3.4.2 必须使用此函数）"""
    cache_file = Path(cache_path)
    
    # 铁律 1：清理前必须先备份
    if cache_file.exists():
        backup_path = cache_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy2(cache_file, backup_path)
        print(f"✅ 已备份缓存到: {backup_path}")
        
        # 铁律 2：检查文件年龄和大小
        file_age_days = (datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)).days
        file_size_mb = cache_file.stat().st_size / (1024 * 1024)
        
        if file_age_days > max_age_days or file_size_mb > max_size_mb:
            # 铁律 3：清理后保留最近一次成功的缓存状态
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 只保留最近 7 天的记录
            cutoff_time = (datetime.now() - timedelta(days=7)).timestamp()
            cleaned = {
                k: v for k, v in cache.items()
                if isinstance(v, dict) and v.get('timestamp', 0) > cutoff_time
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 清理完成：{len(cache)} → {len(cleaned)} 条记录")
            print(f"📦 备份位置：{backup_path}")
            print(f"⚠️ 如需恢复，运行：copy /Y \"{backup_path}\" \"{cache_file}\"")
        else:
            print(f"ℹ️ 缓存未达清理阈值（年龄 {file_age_days} 天，大小 {file_size_mb:.1f}MB）")
            os.remove(backup_path)  # 删除无用备份
```

### 3. 缓存保留铁律

- 🚫 **禁止静默删除缓存**：任何清理操作必须先备份，再清理，最后告知用户备份位置
- 🚫 **禁止清理时丢失"失败行"记录**：失败行必须保留到成功重试后才能清理
- 🚫 **禁止缓存无限增长**：缓存文件 > 50MB 必须触发清理（避免磁盘占用）
- ✅ **必须告知用户缓存位置**：生成的爬虫代码运行后，必须输出"缓存位置：`<path>`，保留期 30 天，清理前会自动备份"
- ✅ **必须提供清理命令**：生成的代码必须包含 `--cleanup-cache` 选项，调用 `safe_cleanup_cache()`

### 4. 缓存安全保护

```python
# ✅ 正确：缓存读写时使用文件锁（避免并发冲突）
import fcntl  # Linux/Mac（Windows 用 msvcrt 或 portalocker）
from contextlib import contextmanager

@contextmanager
def cache_lock(cache_path: str):
    """缓存文件锁，避免并发写入冲突"""
    lock_path = cache_path + '.lock'
    with open(lock_path, 'w') as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX)  # 排他锁
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)  # 释放

# ❌ 错误：直接 open + write，可能造成并发写入冲突
```

---

## 破坏性重写（clear-and-rewrite）安全控制（v3.4.2 新增，回应 ClawHub [SQP-2]）

⚠️ **M14 中"清空+批量写入"模式（变更量 > 50% 时）必须遵守以下安全控制**：

### 1. 清空前必做的 3 件事

```python
def safe_clear_and_rewrite(target_table, new_records, target_type="feishu"):
    """v3.4.2 强制：所有 clear-and-rewrite 必须用此函数"""
    
    # Step 1: 必须先备份目标表当前内容
    backup = backup_target(target_table, target_type)
    print(f"✅ Step 1 已备份目标表到：{backup}")
    
    # Step 2: 必须先告知用户即将清空的记录数和影响范围
    record_count = count_target_records(target_table, target_type)
    print(f"⚠️ Step 2 即将清空 {record_count} 条记录！")
    print(f"   - 备份位置：{backup}")
    print(f"   - 新记录数：{len(new_records)}")
    print(f"   - 如需取消，请在 5 秒内按 Ctrl+C")
    
    # Step 3: 必须等待用户确认（生成的脚本默认 dry_run=True）
    if not confirm_with_user("确认执行 clear-and-rewrite？"):
        print("❌ 用户取消，目标表未改动")
        return False
    
    # Step 4: 执行清空 + 批量写入
    try:
        clear_target(target_table, target_type)
        batch_write(new_records, target_table, target_type, batch_size=500)
        print(f"✅ Step 4 clear-and-rewrite 成功")
        return True
    except Exception as e:
        # Step 5: 失败必须自动回滚
        print(f"❌ 执行失败：{e}")
        print(f"🔄 正在从备份恢复...")
        restore_from_backup(target_table, backup, target_type)
        print(f"✅ 已恢复到执行前状态")
        return False
```

### 2. clear-and-rewrite 铁律

- 🚫 **禁止无备份清空**：清空前必须备份目标表当前完整内容
- 🚫 **禁止无确认清空**：必须告知用户即将清空的记录数 + 等待用户确认
- 🚫 **禁止静默失败**：清空+写入失败时必须自动从备份恢复
- 🚫 **禁止默认开启 clear-and-rewrite**：生成的代码必须默认 `dry_run=True`，用户显式确认后才改为 `False`
- ✅ **必须输出影响报告**：清空前必须输出"将删除 X 条，新增 Y 条，差异 Z 条"
- ✅ **必须提供回滚命令**：执行后必须输出"如需回滚，运行：`python script.py --rollback`"

### 3. 适用边界

- ✅ 变更量 > 50% 且数据非关键（如帖子列表/产品目录）
- ⚠️ 变更量 > 50% 且数据含关键字段（金额/人数/合同）→ **必须先全量备份到 CSV，再 clear-and-rewrite**
- ❌ 数据量极小（< 100 条）→ 永远用逐行更新，不启用 clear-and-rewrite
- ❌ 数据无法重建（如已删除的原始记录）→ 永远不启用 clear-and-rewrite，必须用逐行更新
