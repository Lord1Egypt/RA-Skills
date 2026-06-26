# Settings, Debugging, and Source Anchors

## Use This Reference For

- Choosing between `setting.py` and `__custom_setting__`
- Understanding common config groups
- Using feapder-native debugging workflows
- Jumping to the right upstream files

## Configuration Placement

- Use `setting.py` for project-wide defaults shared by multiple spiders.
- Use `__custom_setting__` for spider-local overrides or single-file examples.
- Remember the precedence: `__custom_setting__` overrides `setting.py`.

## Config Groups Worth Checking First

- Redis and MySQL connectivity
- `ITEM_PIPELINES`
- `SPIDER_THREAD_COUNT`, retry counts, and keep-alive behavior
- Downloader selection and render settings
- Request and item dedup settings
- Warning and logging settings

The vendored project template already documents the main keys:

- [vendor/feapder-1.9.2/feapder/templates/project_template/setting.py](vendor/feapder-1.9.2/feapder/templates/project_template/setting.py)

## Debugging Workflow

- For extraction debugging, prefer `feapder shell -u <url>` or `feapder shell --curl '<curl command>'`.
- For `Spider`, convert to a debug spider with `to_DebugSpider(...)` and pass either `request` or `request_dict`.
- For `BatchSpider`, use `to_DebugBatchSpider(...)` and pass `task_id` or `task`.
- Keep debug-mode data out of production storage unless the user explicitly wants persistence.

## Project-Level Runtime Conventions

- Centralize multi-spider startup in `main.py` when the project has more than one spider.
- Use `ArgumentParser` when matching the framework's own examples for command dispatch.
- Keep master and worker process entrypoints explicit in `TaskSpider` and `BatchSpider` projects.

## Useful Upstream Files

- Overview and install notes: [vendor/feapder-1.9.2/README.md](vendor/feapder-1.9.2/README.md)
- CLI usage: [vendor/feapder-1.9.2/docs/command/cmdline.md](vendor/feapder-1.9.2/docs/command/cmdline.md)
- Project template: [vendor/feapder-1.9.2/feapder/templates/project_template/README.md](vendor/feapder-1.9.2/feapder/templates/project_template/README.md)
- Core spider implementations:
  - [vendor/feapder-1.9.2/feapder/core/spiders/air_spider.py](vendor/feapder-1.9.2/feapder/core/spiders/air_spider.py)
  - [vendor/feapder-1.9.2/feapder/core/spiders/spider.py](vendor/feapder-1.9.2/feapder/core/spiders/spider.py)
  - [vendor/feapder-1.9.2/feapder/core/spiders/task_spider.py](vendor/feapder-1.9.2/feapder/core/spiders/task_spider.py)
  - [vendor/feapder-1.9.2/feapder/core/spiders/batch_spider.py](vendor/feapder-1.9.2/feapder/core/spiders/batch_spider.py)
- Request and response internals:
  - [vendor/feapder-1.9.2/feapder/network/request.py](vendor/feapder-1.9.2/feapder/network/request.py)
  - [vendor/feapder-1.9.2/feapder/network/response.py](vendor/feapder-1.9.2/feapder/network/response.py)
- Pipeline example:
  - [vendor/feapder-1.9.2/tests/test-pipeline/pipeline.py](vendor/feapder-1.9.2/tests/test-pipeline/pipeline.py)
