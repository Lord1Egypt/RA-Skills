# 06 批量处理规则

## 适用场景

用户表达"多个任务 / 分别处理 / 不要合并 / 并行 / 批量"时走这份文档。

## 核心规则

1. **没有执行口令不跑**：没收到"开跑/直接跑/确认执行"，必须停在 `batch-prefill` 阶段
2. **不能循环拼单任务**：多任务必须走 `batch-prefill`，不能循环调单任务 `--run`
3. **并发上限**：用户侧默认 3，从 `config.json` 的 `batch.max_concurrency` 读取
4. **任务数上限**：用户侧默认 5，从 `config.json` 的 `batch.max_tasks` 读取
5. **超限需确认**：超过配置上限时必须先让用户确认

## 命令

### 批量预填

```bash
python3 scripts/cli.py batch-prefill --model <ROUTE_ID> --batch-json '[{"label":"A","prompt":"白猫"},{"label":"B","prompt":"黑狗"}]'
```

### 批量执行（用户确认后）

```bash
python3 scripts/cli.py batch-run --model <ROUTE_ID> --batch-json '[...]' --confirm-run
```

### 提高并发（需用户确认）

```bash
python3 scripts/cli.py batch-run --model <ROUTE_ID> --batch-concurrency 4 --batch-concurrency-approved --batch-json '[...]'
```

### 超任务数（需用户确认）

```bash
python3 scripts/cli.py batch-run --model <ROUTE_ID> --batch-task-count-approved --batch-json '[...]'
```

## 配置

```json
{
  "batch": {
    "max_concurrency": 3,
    "max_tasks": 5
  }
}
```

更高的硬系统上限在脚本内部兜底，不作为用户配置项暴露。
