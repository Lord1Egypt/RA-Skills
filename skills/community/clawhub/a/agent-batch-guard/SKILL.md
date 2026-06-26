---
name: agent-batch-guard
version: 1.0.0
description: AI Agent 大任务防卡死指南。解决 agent 在批量操作中 session transcript 膨胀导致 compaction 超时、agent 卡死的问题。涵盖 session 保护策略、脚本化批处理、断点续传、熔断器、OpenClaw 配置调优和实战案例。
---

# Agent 大任务防卡死指南

AI Agent 执行大任务（批量抓取、翻页采集、历史数据导出）时，极易因 session transcript 膨胀导致卡死。本指南提供从认知层到配置层的完整防护方案。

## 这个 Skill 解决什么问题

AI Agent（如 OpenClaw agent）在执行大量重复操作时，每一轮工具调用的输入和输出都会堆积在 session transcript 中。当 transcript 膨胀到数 MB 级别后：

1. **Compaction 超时** — 压缩旧对话的过程本身超过时间限制
2. **Agent 彻底卡死** — 无法处理新消息，也无法自行恢复
3. **用户无感知** — agent 停止响应，但没有任何报错通知

**真实案例**：agent 被要求翻阅手机 App 抓取 1 年的订单数据，在对话中逐页执行 scroll → uiautomator dump → parse → repeat，200+ 轮后 transcript 膨胀到 9.6MB，compaction 两次超时，agent 静默卡死数小时。

---

## 第一层：Agent 行为规范（写入 AGENTS.md）

这是最重要的一层。Agent 不具备对自身运行环境的 meta 认知——它不知道 transcript 有容量上限，需要在 workspace 配置中显式告知。

### 核心原则

**数据写文件，不要堆在对话里。**

### 判断标准

| 任务规模 | 做法 |
|---------|------|
| < 5 页/轮 | 可以在对话里直接操作 |
| 5-20 页/轮 | 写脚本，一次跑完，结果存文件 |
| 20+ 页/轮 | 写脚本 + 分批（按月/按平台/按类别），每批存档 |

### 黄金规则

1. **超过 5 页的翻页操作 → 写脚本**，不在对话里循环
2. **数据写文件**（如 `data/scrape/`），不堆在 transcript 里
3. **分批 + 断点续传**（每批存档，支持中断恢复）
4. **对话里只做三件事**：写脚本 → 检查进度 → 汇总回复
5. **超过 10 轮重复操作 = 立刻停下来写脚本**
6. **熔断保护**：连续失败 5 次暂停，不要无脑重试

### 建议写入 AGENTS.md 的模板

```markdown
## 大任务处理规范（防止 session 卡死）

**核心原则：数据写文件，不要堆在对话里。**

当任务涉及大量重复操作时（批量处理、翻阅多页数据、爬取历史记录），
**禁止**在对话中逐页循环。

详细批处理模式请读取：
~/.openclaw/skills/agent-batch-guard/SKILL.md

### 快速规则
1. 超过 5 页的翻页操作 → 写脚本，不在对话里循环
2. 数据写文件，不堆在 transcript 里
3. 分批 + 断点续传（每批存档，支持中断恢复）
4. 对话里只做三件事：写脚本 → 检查进度 → 汇总回复
5. 超过 10 轮重复操作 = 立刻停下来写脚本
6. 熔断保护：连续失败 5 次暂停，不要无脑重试
```

---

## 第二层：正确的大任务执行模式

### 模式一：脚本化批处理（推荐）

把循环操作封装成独立脚本，agent 只负责写脚本、运行脚本、读取结果。

**错误做法**（agent 在对话中循环）：
```
对话轮 1: scroll 到第 1 页 → 截图 → 解析
对话轮 2: scroll 到第 2 页 → 截图 → 解析
...
对话轮 200: scroll 到第 200 页 → 截图 → 解析
→ transcript 9.6MB → compaction 超时 → 卡死
```

**正确做法**（agent 写脚本后一次执行）：
```
对话轮 1: 写 /tmp/scrape_orders.py（脚本内部处理循环和翻页）
对话轮 2: python3 /tmp/scrape_orders.py → 结果存到 data/scrape/orders.json
对话轮 3: 读取 orders.json → 汇总回复
→ transcript 3 轮 → 安全
```

### 模式二：分批执行 + 文件存档

大任务拆成小批次，每批结果立即写入独立文件：

```
data/scrape/
├── orders_taobao_2025-01.json
├── orders_taobao_2025-02.json
├── ...
├── orders_taobao_2025-12.json
└── orders_summary.json    ← 最终汇总
```

脚本示例（Python，ADB 翻页采集）：

```python
#!/usr/bin/env python3
"""批量采集 App 订单 — 分批存档 + 断点续传"""
import json, os, subprocess, time
from pathlib import Path

SERIAL = "DEVICE_SERIAL"
OUTPUT_DIR = Path("data/scrape")
PROGRESS_FILE = OUTPUT_DIR / "progress.json"

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"last_page": 0, "total_items": 0}

def save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2))

def dump_ui():
    """读取当前屏幕元素"""
    subprocess.run(["adb", "-s", SERIAL, "shell", "uiautomator", "dump", "/sdcard/ui.xml"], check=True)
    subprocess.run(["adb", "-s", SERIAL, "pull", "/sdcard/ui.xml", "/tmp/ui.xml"], check=True)
    return Path("/tmp/ui.xml").read_text()

def scroll_down():
    subprocess.run(["adb", "-s", SERIAL, "shell", "input", "swipe", "500", "1500", "500", "500", "300"])
    time.sleep(1.5)  # 等待加载

def parse_orders(xml_content):
    """解析 uiautomator dump 的 XML，提取订单信息"""
    # 实际解析逻辑根据 App 界面调整
    pass

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    progress = load_progress()
    page = progress["last_page"]
    all_items = []
    consecutive_empty = 0

    while consecutive_empty < 3:  # 连续 3 页无新数据则停止
        page += 1
        xml = dump_ui()
        items = parse_orders(xml)

        if not items:
            consecutive_empty += 1
        else:
            consecutive_empty = 0
            all_items.extend(items)

            # 每 10 页存档一次
            if page % 10 == 0:
                batch_file = OUTPUT_DIR / f"batch_{page}.json"
                batch_file.write_text(json.dumps(all_items, ensure_ascii=False, indent=2))
                all_items = []

        # 更新进度
        progress["last_page"] = page
        progress["total_items"] += len(items)
        save_progress(progress)

        scroll_down()

    # 最终存档
    if all_items:
        batch_file = OUTPUT_DIR / f"batch_{page}.json"
        batch_file.write_text(json.dumps(all_items, ensure_ascii=False, indent=2))

    print(json.dumps(progress))

if __name__ == "__main__":
    main()
```

### 模式三：子 agent 隔离

对于特别大的任务，用子 agent 执行。子 agent 的 transcript 独立于主会话，不会撑爆主 session：

```
主 agent 对话轮 1: 派子 agent 执行批量抓取
子 agent: 独立 session 中执行 200 轮（即使卡死也不影响主 agent）
主 agent 对话轮 2: 读取子 agent 输出文件 → 汇总回复
```

---

## 第三层：平台配置调优（OpenClaw）

### contextPruning（上下文裁剪）

工具输出的缓存过期时间。缩短 TTL 可以让旧的工具输出更快从上下文中释放，减轻 transcript 膨胀压力：

```jsonc
// openclaw.json → agents.defaults.contextPruning
{
  "mode": "cache-ttl",
  "ttl": "30m"          // 默认 1h → 改为 30m，工具输出更快过期
}
```

### thinkingDefault（推理等级）

注意：并非所有模型都支持高推理等级。例如部分推理模型不支持 `xhigh`，会自动降级并产生大量警告日志。建议设为目标模型实际支持的等级：

```jsonc
{
  "thinkingDefault": "high"  // 确保兼容性，避免不必要的降级警告
}
```

### 推荐配置

```jsonc
{
  "agents": {
    "defaults": {
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "30m"
      },
      "thinkingDefault": "high",
      "timeoutSeconds": 900
    }
  }
}
```

> **注意**：OpenClaw 的 `compaction.mode` 目前仅支持 `"safeguard"`。配置层能做的调优有限，防止 session 膨胀主要靠第一层（agent 行为规范）和第二层（脚本化批处理）。

---

## 第四层：批处理代码模式

### 并发调度

自适应并发池，根据耗时动态调整并发数：

```typescript
class AdaptiveScheduler {
  private concurrency: number;
  private running = 0;
  private queue: (() => void)[] = [];

  constructor(
    private min: number,
    private max: number,
    private slowThresholdMs: number
  ) {
    this.concurrency = Math.ceil((min + max) / 2);
  }

  async run<T>(fn: () => Promise<T>): Promise<T> {
    if (this.running >= this.concurrency) {
      await new Promise<void>((resolve) => this.queue.push(resolve));
    }
    this.running++;
    const start = Date.now();
    try {
      return await fn();
    } finally {
      const elapsed = Date.now() - start;
      this.running--;
      if (elapsed > this.slowThresholdMs && this.concurrency > this.min) {
        this.concurrency--;
      } else if (elapsed < this.slowThresholdMs / 2 && this.concurrency < this.max) {
        this.concurrency++;
      }
      if (this.queue.length > 0) this.queue.shift()!();
    }
  }
}
```

| 场景 | 初始 | 最小 | 最大 | 慢阈值 |
|------|------|------|------|--------|
| CPU 密集（FFmpeg 转码） | 4 | 1 | CPU 核数 | 3s |
| API 调用（AI 服务） | 3 | 1 | 5 | 8s |
| 文件 I/O | 2 | 1 | 3 | 30s |
| App 翻页采集（ADB） | 1 | 1 | 1 | - |

### 熔断器

连续失败过多时自动暂停：

```typescript
class CircuitBreaker {
  private consecutiveFailures = 0;

  constructor(
    private maxFailures: number = 5,
    private onTrip?: (failures: number) => void
  ) {}

  recordSuccess() { this.consecutiveFailures = 0; }

  recordFailure(): boolean {
    this.consecutiveFailures++;
    if (this.consecutiveFailures >= this.maxFailures) {
      this.onTrip?.(this.consecutiveFailures);
      return true; // tripped
    }
    return false;
  }

  get isTripped() { return this.consecutiveFailures >= this.maxFailures; }
  reset() { this.consecutiveFailures = 0; }
}
```

### 断点续传

```typescript
const completedSet = new Set(loadCompletedFromDisk());

for (const item of items) {
  if (abortController.aborted) break;

  if (completedSet.has(item.id)) continue; // 跳过已完成

  try {
    await processItem(item);
    completedSet.add(item.id);
    saveCompletedToDisk(completedSet); // 每项完成后持久化
  } catch (err) {
    if (circuitBreaker.recordFailure()) {
      notify("连续失败 5 次，暂停任务，等待指示");
      break;
    }
  }
}
```

### 指数退避重试

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 2000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries) throw err;
      if (isFatalError(err)) throw err;
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
      await sleep(delay);
    }
  }
  throw new Error('unreachable');
}
```

### 错误分类

| 错误类型 | 行为 | 示例 |
|---------|------|------|
| 瞬态网络错误 | 重试 | timeout, ECONNRESET |
| 401 Unauthorized | **停止** | API Key 无效 |
| 403 / 余额不足 | **停止** | 账户问题 |
| 429 Too Many Requests | **退避重试** | 限流 |
| 500+ Server Error | 有限重试（3 次） | 服务端异常 |
| 文件/页面不存在 | 跳过此项 | 输入丢失 |
| 磁盘空间不足 | **停止全部** | ENOSPC |
| ADB 连接断开 | **停止 + 通知用户** | 手机离线 |

### 反风控（批量 HTTP/ADB 请求）

```typescript
// 同域名/同操作限速
const lastAction = new Map<string, number>();

async function throttle(action: string) {
  const last = lastAction.get(action) || 0;
  const minInterval = 1500 + Math.random() * 1500; // 1.5-3s 随机间隔
  const wait = minInterval - (Date.now() - last);
  if (wait > 0) await sleep(wait);
  lastAction.set(action, Date.now());
}
```

---

## Checklist

### Agent 大任务启动前
- [ ] 评估任务规模（< 5 页直接做，≥ 5 页写脚本）
- [ ] 确定分批策略（按时间/按平台/按类别）
- [ ] 确定输出文件路径和格式
- [ ] 脚本包含断点续传逻辑

### 脚本编写
- [ ] 循环操作在脚本内部，不在对话中
- [ ] 每批/每 N 项写入文件（不全存内存）
- [ ] 有 progress.json 记录当前进度
- [ ] 熔断器：连续失败 5 次暂停
- [ ] 错误分类：致命错误停止，瞬态错误重试
- [ ] ADB/HTTP 操作间有随机延迟

### 平台配置
- [ ] compaction 设为 rolling + maxTurns ≤ 40
- [ ] contextPruning TTL ≤ 30m
- [ ] thinkingDefault 兼容目标模型

---

## 来源

基于 OpenClaw agent 实际运维事故（session 膨胀 9.6MB 导致 compaction 超时、agent 静默卡死数小时）和生产级批处理系统经验整理。
