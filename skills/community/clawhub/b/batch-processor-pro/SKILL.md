---
slug: batch-processor-pro
name: batch-processor-pro
version: "1.0.0"
displayName: 批处理专家
summary: 解决OOM、中断无法恢复、缺乏幂等、进度不可见四大痛点，附检查点与并行决策矩阵。
license: MIT
description: |-
  批处理专家是处理大量数据项的能力包。它不只说"处理前dry-run、处理中报进度"，更解决
  四个高频痛点：大批量一加载就OOM、中断后无法恢复只能从头重跑、缺乏幂等性导致重复
  处理、进度不可见不知道还要等多久。

  核心能力：
  - 流式分块：按行/按文件分块处理，内存恒定不OOM
  - 检查点恢复：每N项存检查点，中断后从断点续跑而非从头
  - 幂等设计：每项有唯一键，重复执行只处理一次
  - 进度报告：每10项报进度，预估剩余时间
  - 并行决策矩阵：按任务类型选串行/并行/分片
  - 五级错误分级：瞬时错误重试、数据错误跳过、系统错误中止

  适用场景：
  - 批量处理目录下数百个文件
  - 批量调API处理上万条记录
  - 批量图片/视频转换
  - 批量数据清洗与校验
  - 任何"要对N个东西做同样操作"的任务

  差异化：
  - 原始版本只有"前/中/后"三段口号，本版补齐可执行的检查点格式与恢复脚本
  - 新增流式分块策略（按行/按文件/按批次）
  - 新增幂等设计章节（唯一键+去重检查）
  - 新增并行vs串行决策矩阵
  - 新增五级错误分级与对应处理
  - 增加FAQ与故障排查

  触发关键词：批处理、批量、检查点、断点续跑、幂等、并行、流式、OOM、进度
tags:
- 自动化
- 批处理
- 效率工具
tools:
- read
- exec
---

# 批处理专家

处理多个数据项时应用本skill。核心信条：**永远先dry-run少量样本，必有检查点可恢复，每项必幂等。**

## 四大痛点与对策

| 痛点 | 典型表现 | 本skill对策 |
|:-----|:---------|:------------|
| OOM内存爆炸 | 10万条一加载就崩 | 流式分块，内存恒定 |
| 中断无法恢复 | 跑到80%断了，只能从头重跑 | 检查点机制，从断点续跑 |
| 缺乏幂等 | 重跑导致重复处理/重复扣款 | 唯一键 + 去重检查 |
| 进度不可见 | 不知道跑到哪了、还要多久 | 每10项报进度 + 预估剩余 |

---

## 处理前三必做

### 1. Dry-run（2-3项样本）

```python
# 先用少量样本验证全流程
SAMPLE_SIZE = 3
sample_items = items[:SAMPLE_SIZE]
results = [process(item) for item in sample_items]
# 人工核对结果正确再放量
```

### 2. 计数与预估

```text
"将处理47项，预计2分钟完成"
"将处理10000项，预计3小时，已存检查点可中断恢复"
```

### 3. 确认破坏性操作

```text
"将删除200个文件，不可恢复。确认继续？[y/N]"
"将向1000个客户发送邮件，不可撤回。确认继续？[y/N]"
```

---

## 流式分块（避免OOM）

### 按行分块（大文件）

```python
import json

def process_large_file(path, chunk_size=1000):
    with open(path, 'r', encoding='utf-8') as f:
        chunk = []
        for line_no, line in enumerate(f, 1):
            item = json.loads(line)
            chunk.append(item)
            if len(chunk) >= chunk_size:
                process_chunk(chunk)
                chunk = []  # 释放内存
        if chunk:  # 处理剩余
            process_chunk(chunk)
```

### 按文件分块（目录批量）

```python
from pathlib import Path

def process_directory(dir_path):
    files = list(Path(dir_path).glob("*"))
    for file in files:  # 逐文件处理，内存恒定
        process_one_file(file)
        # 每文件处理完即释放
```

### 按批次分块（API调用）

```python
def batch_call_api(items, batch_size=50):
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        api.batch_process(batch)  # 50条/批，减少请求次数
```

---

## 检查点与恢复

### 检查点格式

```json
{
  "job_id": "batch-process-20260718",
  "total": 10000,
  "completed": 6500,
  "failed": 23,
  "last_processed_id": "item_6500",
  "last_checkpoint": "2026-07-18T10:30:00Z",
  "processed_ids": ["item_1", "item_2", "..."],
  "failed_items": [
    {"id": "item_123", "error": "timeout", "retry_count": 3}
  ],
  "status": "in_progress"
}
```

### 检查点写入策略

```python
import json
from datetime import datetime

CHECKPOINT_INTERVAL = 50  # 每50项存一次

def process_with_checkpoint(items, job_id):
    checkpoint = load_or_init_checkpoint(job_id)
    start_idx = checkpoint["completed"]  # 从断点续跑

    for i, item in enumerate(items[start_idx:], start=start_idx):
        if item["id"] in checkpoint["processed_ids"]:
            continue  # 幂等：跳过已处理
        try:
            process(item)
            checkpoint["processed_ids"].append(item["id"])
        except Exception as e:
            checkpoint["failed_items"].append({
                "id": item["id"],
                "error": str(e),
                "retry_count": 0
            })
        checkpoint["completed"] = i + 1

        # 每50项存检查点
        if (i + 1) % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(job_id, checkpoint)
            report_progress(i + 1, len(items))

    save_checkpoint(job_id, checkpoint)
    return checkpoint
```

### 恢复脚本

```python
def resume_job(job_id, items):
    checkpoint = load_checkpoint(job_id)
    if checkpoint is None:
        print("无检查点，从头开始")
        return process_with_checkpoint(items, job_id)

    print(f"从检查点恢复：已完成 {checkpoint['completed']}/{checkpoint['total']}")
    print(f"失败 {len(checkpoint['failed_items'])} 项")
    return process_with_checkpoint(items, job_id)  # 内部会跳过已处理
```

---

## 幂等设计

> 重复处理是批处理第一大坑。每项必须有唯一键。

### 幂等键构造

```python
# 文件处理：用文件路径+修改时间
idempotency_key = f"{file_path}:{file_mtime}"

# 数据库记录：用主键
idempotency_key = f"record:{record_id}"

# API调用：用业务唯一ID
idempotency_key = f"order:{order_id}"

# 定时任务：用日期+任务名
idempotency_key = f"daily_report:{date}"
```

### 去重检查模式

```python
def process_with_idempotency(item, redis_client):
    key = f"idem:{item['id']}"
    # 处理前先查"是否已处理"
    if redis_client.exists(key):
        return {"status": "skipped", "reason": "already_processed"}
    # 处理
    result = do_process(item)
    # 处理后标记（带TTL）
    redis_client.setex(key, 86400, "1")  # 24小时TTL
    return result
```

---

## 进度报告

### 报告格式

```text
[10:30:15] 23/47 完成 (49%) - 预计剩余 1分30秒
[10:30:25] 33/47 完成 (70%) - 预计剩余 45秒
[10:30:35] 44/47 完成 (94%) - 预计剩余 10秒
[10:30:38] 47/47 完成 (100%) - 用时 38秒
```

### 进度计算

```python
import time
from datetime import datetime, timedelta

def report_progress(completed, total, start_time):
    elapsed = time.time() - start_time
    rate = completed / elapsed if elapsed > 0 else 0
    remaining = (total - completed) / rate if rate > 0 else 0
    pct = (completed / total * 100) if total > 0 else 0
    eta = datetime.now() + timedelta(seconds=remaining)
    print(f"{completed}/{total} 完成 ({pct:.0f}%) - 预计剩余 {int(remaining)}秒 (ETA {eta:%H:%M:%S})")
```

### 报告频率

| 总项数 | 报告频率 |
|:-------|:---------|
| <100 | 每项报 |
| 100-1000 | 每10项报 |
| 1000-10000 | 每100项报 |
| >10000 | 每1000项报 |

---

## 并行 vs 串行决策矩阵

| 任务特征 | 推荐策略 | 原因 |
|:---------|:---------|:-----|
| CPU密集（计算、压缩） | 串行或进程级并行 | GIL限制，多线程无效 |
| IO密集（API、文件、网络） | 并发（asyncio/线程池） | 等IO时可切换 |
| 有顺序依赖 | 串行 | 后项依赖前项结果 |
| 无依赖 + 可并行 | 分片并行 | 多worker各处理一片 |
| 有API限流 | 限流并行（令牌桶） | 并发但不超限 |
| 数据量小（<100） | 串行 | 并行开销大于收益 |
| 数据量大 + 无依赖 | 分片并行 | 多worker加速 |

### 并发实现示例

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_concurrent(items, max_workers=10):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process, item): item for item in items}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"error": str(e), "item": futures[future]})
    return results
```

### 分片并行示例

```python
# 启动多个worker各处理一片
def shard_items(items, num_workers):
    shards = [[] for _ in range(num_workers)]
    for i, item in enumerate(items):
        shards[i % num_workers].append(item)
    return shards

# 每个worker独立跑，各自存检查点
# worker_0: items[0::4]
# worker_1: items[1::4]
# worker_2: items[2::4]
# worker_3: items[3::4]
```

---

## 五级错误分级

| 级别 | 错误类型 | 处理策略 | 示例 |
|:-----|:---------|:---------|:-----|
| L1 瞬时 | 超时、限流、网络抖动 | 重试3次（1s/2s/4s退避） | API 429、连接超时 |
| L2 数据 | 格式错、字段缺、值非法 | 跳过+记录，继续其余 | JSON解析失败、必填字段空 |
| L3 可恢复 | 服务暂不可用 | 排队等待恢复后重试 | 上游503、数据库锁 |
| L4 系统 | 鉴权失败、磁盘满 | 中止整个批次，告警 | 401/403、磁盘空间不足 |
| L5 数据完整性 | 重复处理、数据丢失 | 立即中止，人工介入 | 幂等键冲突、校验和不符 |

### 错误处理实现

```python
import time

def process_with_error_handling(item):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return do_process(item)
        except (TimeoutError, RateLimitError):  # L1
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"status": "failed", "error": "timeout", "item": item}
        except (ValueError, KeyError) as e:  # L2
            return {"status": "skipped", "error": str(e), "item": item}
        except ServiceUnavailable:  # L3
            queue_for_retry(item)
            return {"status": "queued", "item": item}
        except (AuthError, DiskFull):  # L4
            raise  # 中止整个批次
```

---

## 处理后必报

```text
批处理完成报告
==============================
任务: batch-process-20260718
总数: 10000
成功: 9977
失败: 23 (已保存到 failed.json 待重试)
跳过: 0
用时: 38分12秒
平均速率: 4.36项/秒
检查点: ~/.checkpoints/batch-process-20260718.json
==============================
失败项TOP原因:
- timeout: 15
- invalid_format: 8
```

### 失败项重试

```python
def retry_failed(job_id):
    checkpoint = load_checkpoint(job_id)
    failed = checkpoint["failed_items"]
    print(f"重试 {len(failed)} 个失败项")
    for item in failed:
        if item["retry_count"] < 3:  # 最多重试3次
            try:
                process(item)
                checkpoint["failed_items"].remove(item)
            except Exception:
                item["retry_count"] += 1
    save_checkpoint(job_id, checkpoint)
```

---

## 边界情况与陷阱

- **内存爆炸**：永远用流式/分块，不要一次性load全部
- **中断恢复**：检查点频率别太低（最多丢50项），也别太高（IO开销）
- **幂等陷阱**：非幂等操作（扣款、发邮件）重试会重复，必须先做幂等
- **并行陷阱**：有共享状态时别并行，会数据竞争
- **限流陷阱**：并行别超API限流，加令牌桶
- **顺序依赖**：后项需要前项结果时必须串行
- **进度丢失**：检查点要持久化到磁盘，别只在内存
- **超长任务**：超过1小时的任务必分片，避免单点失败全丢

---

## FAQ

**Q：处理10万条记录一加载就OOM怎么办？**
A：用流式分块——按行读大文件、逐文件处理目录、按批次调API。内存恒定，不一次性load。

**Q：跑到80%断了怎么办？**
A：检查点机制。每50项存一次检查点，中断后从断点续跑。`resume_job(job_id, items)`自动跳过已处理。

**Q：重跑会不会重复处理？**
A：用幂等键。每项有唯一ID，处理前先查"是否已处理"。已处理则跳过。

**Q：该用串行还是并行？**
A：看决策矩阵。CPU密集串行，IO密集并发，有顺序依赖串行，无依赖大数据量分片并行。

**Q：API限流导致批量失败？**
A：限流并行（令牌桶）+ 退避重试（1s/2s/4s）+ 批量请求（50条/批）。

**Q：失败项怎么处理？**
A：L1瞬时错误重试，L2数据错误跳过记录，L4系统错误中止。失败项存failed.json待重试，最多重试3次。

---

## 故障排查

| 症状 | 可能原因 | 解决 |
|:-----|:---------|:-----|
| OOM崩溃 | 一次性load全部 | 改流式分块 |
| 中断后从头跑 | 无检查点 | 加checkpoint机制 |
| 重复处理 | 无幂等键 | 加唯一键+去重检查 |
| 进度卡住 | 单项卡死 | 加per-item timeout |
| 全部失败 | API限流/凭证过期 | 加令牌桶、检查Token |
| 并行数据错乱 | 共享状态竞争 | 改串行或加锁 |
| 检查点丢失 | 仅存内存 | 持久化到磁盘 |

---

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+（推荐3.10+，用asyncio）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Redis | 服务 | 可选（幂等去重） | 自部署或云服务 |
| Python运行时 | 运行时 | 可选（脚本实现） | python.org |

### API Key 配置
- 本skill基于Markdown指令，无需额外API Key
- 涉及外部API批量调用时，通过环境变量配置API Key

### 可用性分类
- **分类**：MD+EXEC（Markdown指令 + 脚本执行）
- **说明**：通过自然语言指令驱动Agent按检查点+幂等模式处理批量任务
