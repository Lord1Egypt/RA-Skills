# Spider Types and Scaffolding

## Use This Reference For

- Choosing between `AirSpider`, `Spider`, `TaskSpider`, and `BatchSpider`
- Creating a new feapder project, spider, or item
- Preserving the framework's expected project layout

## Pick the Right Spider Type

- `AirSpider`
  - Use for lightweight, local crawling.
  - Avoid for distributed queues, Redis-backed resumability, or periodic batches.
- `Spider`
  - Use for Redis-backed distributed crawling with resumable tasks.
  - Use when the project wants automatic item batching and standard distributed startup via `redis_key`.
- `TaskSpider`
  - Use when seeds come from a task source managed by the framework, typically MySQL or Redis.
  - Keep `start_monitor_task()` and `start()` as separate master and worker entrypoints.
- `BatchSpider`
  - Use for periodic full or incremental batches with batch metadata and task-state transitions.
  - Expect explicit task updates such as `yield self.update_task_batch(request.task_id, 1)`.

## Preferred Learning Order

The feapder docs recommend understanding the framework in this order:

1. `AirSpider`
2. `Spider`
3. `BatchSpider`

`TaskSpider` is also supported in 1.9.2 and should be chosen only when its seed-management model matches the task better than plain `Spider`.

## Preferred Scaffolding Commands

Use the framework's CLI when creating new code:

```bash
feapder create -p <project_name>
feapder create -s <spider_name>
feapder create -i <table_name>
feapder create --setting
```

## Default Project Layout

When the user wants a full project instead of a single script, preserve this shape:

- `main.py`: central startup and command dispatch
- `setting.py`: shared framework configuration
- `spiders/`: spider modules
- `items/`: `Item` and `UpdateItem` classes

## Practical Selection Rules

- If the user only says "write a feapder spider" and the request looks like a pure crawling or parsing demo, default to a single-file `AirSpider` modeled after `vendor/feapder-1.9.2/tests/air-spider/test_air_spider.py`.
- If the request mentions `Item`, `UpdateItem`, pipeline, 入库, Redis, MySQL, task tables, or batch scheduling, do not fall back to the single-file `AirSpider` demo. Choose the spider type and project layout that match that persistence or orchestration requirement.
- Need one simple crawler script and no Redis or MySQL coordination: choose `AirSpider`.
- Need distributed workers sharing a Redis task queue: choose `Spider`.
- Need the framework to load seeds from a MySQL or Redis task source: choose `TaskSpider`.
- Need recurring batches with batch record tables, task reset rules, and completion monitoring: choose `BatchSpider`.

## Upstream Anchors

- [vendor/feapder-1.9.2/docs/usage/使用前必读.md](vendor/feapder-1.9.2/docs/usage/使用前必读.md)
- [vendor/feapder-1.9.2/docs/command/cmdline.md](vendor/feapder-1.9.2/docs/command/cmdline.md)
- [vendor/feapder-1.9.2/feapder/templates/project_template/main.py](vendor/feapder-1.9.2/feapder/templates/project_template/main.py)
- [vendor/feapder-1.9.2/feapder/templates/project_template/setting.py](vendor/feapder-1.9.2/feapder/templates/project_template/setting.py)
