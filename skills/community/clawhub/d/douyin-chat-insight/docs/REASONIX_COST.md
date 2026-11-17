# Reasonix 复核费用说明 · douyin-chat-insight

更新：2026-08-04

## 计费依据

- 模型：`deepseek/deepseek-v4-flash`
- 单价来源：本机 Reasonix 配置快照（`~/.reasonix`）
  - input **$0.14 / 1M tokens**
  - output **$0.28 / 1M tokens**
  - cache hit **$0.0028 / 1M tokens**
- **重要**：`~/.reasonix/usage.jsonl` 在这两次 `-p` print 模式复核中 **没有追加新行**（`session: null` 历史账本未记入这两次）。
  因此费用按 **会话 transcript 重建多轮 input/output** + 上述单价估算，不是账单 API 原始回执。

## 两次会话

| 轮次 | Session ID | 墙钟（UTC） | 估算 input tokens（累计计费） | 估算 output | **费用（含缓存乐观）** | **费用（无缓存上限）** |
|------|------------|-------------|-------------------------------|-------------|------------------------|------------------------|
| **上次 R1** | `20260804-132642…-flash` | 13:26:42 → 13:28:41 | ~316k billed / miss~47k hit~269k | ~14k | **≈ $0.011** | ≈ $0.048 |
| **这次 R2** | `20260804-140701…-flash` | 14:07:01 → 14:08:44 | ~603k billed / miss~57k hit~546k | ~13k | **≈ $0.013** | ≈ $0.088 |

## 建议对外口径

| 项 | 金额 |
|----|------|
| 上次复核（R1） | **约 $0.01**（人民币约 **¥0.08**，按 7.2） |
| 这次复核（R2） | **约 $0.013**（约 **¥0.09**） |
| **两轮合计** | **约 $0.024**（约 **¥0.17**） |
| 无缓存极端上限合计 | < $0.14（实际有 prefix cache，不会摸到） |

> Flash 复核本身极便宜。若改用 `deepseek-v4-pro`，同工作量大约会贵一个数量级（配置价 input $3 / output $6 per 1M）。

## 如何自己复核账本

```bash
# 1) 全局 usage 账本（可能不含 -p 会话）
wc -l ~/.reasonix/usage.jsonl
python3 -c "import json;from pathlib import Path;r=[json.loads(l) for l in Path.home().joinpath('.reasonix/usage.jsonl').read_text().splitlines() if l.strip()];print(sum(x['costUsd'] for x in r))"

# 2) 项目会话
ls ~/.reasonix/projects/*douyin-chat-insight/sessions/
```

## 诚实边界

1. 非支付平台官方 invoice，是 **可复算估算**。
2. token 用「字符/2.5」粗算，和真实 tokenizer 会有 ±30% 偏差。
3. 缓存命中按「上一轮上下文为 hit」模型估算，偏低/偏高都可能。
4. 若你需要审计级数字，应在 Reasonix 打开 usage 落盘或查 DeepSeek 控制台调用记录。
