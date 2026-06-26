# Code Patterns

## Use This Reference For

- Writing or editing spider classes
- Carrying request state through callbacks
- Returning items or task updates
- Applying render mode or middleware hooks

## Minimal `AirSpider` Pattern

```python
import feapder
from feapder.utils.log import log


class DemoSpider(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://example.com", page=1)

    def parse(self, request, response):
        title = response.xpath("//title/text()").extract_first()
        log.info(f"第{request.page}页标题 | {title}")
```

## Logging and Comment Style

- Default to `from feapder.utils.log import log` and logger methods such as `log.info(...)` instead of `print(...)`.
- Default to Chinese runtime logs, for example `log.info(f"第{request.page}页原始结果 | {response.json}")`.
- Default to Chinese comments when comments are needed, but avoid restating self-evident code.
- Only preserve `print(...)` when the user explicitly asks to mimic upstream examples verbatim or wants the most minimal possible throwaway demo.

## Common Request Flow Rules

- Emit new work with `yield feapder.Request(...)`.
- Use `callback=self.some_parser` for non-default parsers.
- Carry state by passing extra keyword arguments on the request and reading them back from `request.<name>`.
- Use `download_midware(self, request)` to mutate the request before download.
- Use `validate(self, request, response)` to retry or drop invalid responses.

## `Spider` Pattern

```python
import feapder
from feapder.utils.log import log
from items import spider_data_item


class DemoSpider(feapder.Spider):
    def start_requests(self):
        yield feapder.Request("https://example.com")

    def parse(self, request, response):
        title = response.xpath("//title/text()").extract_first()
        log.info(f"准备入库标题 | {title}")
        item = spider_data_item.SpiderDataItem()
        item.title = title
        yield item
```

Use `Spider(..., redis_key="namespace:name")` at startup. Keep Redis settings in `setting.py` or `__custom_setting__`.

## `TaskSpider` Pattern

- Implement `start_requests(self, task)` instead of a no-arg seed method.
- Keep master and worker startup separate:
  - `start_monitor_task()` for feeding or monitoring tasks
  - `start()` for workers
- If tasks come from MySQL, update their state after successful processing.

## `BatchSpider` Pattern

```python
import feapder
from feapder.utils.log import log


class DemoSpider(feapder.BatchSpider):
    def start_requests(self, task):
        task_id, url = task
        yield feapder.Request(url, task_id=task_id)

    def parse(self, request, response):
        log.info(f"任务{request.task_id}抓取完成，准备更新批次状态")
        yield self.update_task_batch(request.task_id, 1)
```

Additional rules:

- Carry `task_id` on the request when the task state must change later.
- Use `failed_request` to mark permanently bad tasks with `-1`.
- Override `init_task` only when the batch reset behavior must change, such as incremental crawling.

## Persistence Rules

- Use `Item` for inserts and `UpdateItem` for updates when you want feapder-managed batch persistence.
- Use manual DB access only when the project already does that or the storage workflow is non-standard.
- If a project defines custom `ITEM_PIPELINES`, follow that pipeline contract instead of bypassing it.

## Render and Custom Downloader Rules

- Set `render=True` on `feapder.Request` for Selenium or Playwright-based fetches.
- Put downloader and browser configuration in `setting.py` or `__custom_setting__`.
- If using a custom downloader in middleware, return `(request, response)` and remember that `response` may no longer be feapder's default response wrapper.

## Upstream Anchors

- [vendor/feapder-1.9.2/docs/usage/AirSpider.md](vendor/feapder-1.9.2/docs/usage/AirSpider.md)
- [vendor/feapder-1.9.2/docs/usage/Spider.md](vendor/feapder-1.9.2/docs/usage/Spider.md)
- [vendor/feapder-1.9.2/docs/usage/TaskSpider.md](vendor/feapder-1.9.2/docs/usage/TaskSpider.md)
- [vendor/feapder-1.9.2/docs/usage/BatchSpider.md](vendor/feapder-1.9.2/docs/usage/BatchSpider.md)
- [vendor/feapder-1.9.2/tests/air-spider/test_air_spider.py](vendor/feapder-1.9.2/tests/air-spider/test_air_spider.py)
- [vendor/feapder-1.9.2/tests/spider/spiders/test_spider.py](vendor/feapder-1.9.2/tests/spider/spiders/test_spider.py)
- [vendor/feapder-1.9.2/tests/batch-spider/spiders/test_spider.py](vendor/feapder-1.9.2/tests/batch-spider/spiders/test_spider.py)
