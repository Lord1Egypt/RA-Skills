---
name: cm-celery-task-analyzer
description: Analyze Celery task configurations for reliability, performance, and debugging. Checks retry policies, task routing, serialization, result backends, worker configuration, beat schedules, and task design patterns. Use when asked to review Celery tasks, audit task reliability, check Celery best practices, optimize worker performance, review beat schedules, or troubleshoot task failures. Triggers on "celery", "celery task", "celery worker", "celery beat", "task queue", "celery retry", "celery routing", "celery config", "celery performance", "celery debug", "celery audit".
metadata:
  tags: ["celery", "python", "task-queue", "async", "distributed", "worker", "redis", "rabbitmq", "scheduling", "reliability"]
---

# Celery Task Analyzer

Analyze Celery task configurations for reliability, performance, and operational excellence. Reviews task definitions, retry policies, routing rules, serialization settings, result backend configuration, worker tuning, and beat schedules. Acts as a senior distributed systems engineer auditing your Celery deployment.

## Usage

Invoke this skill when you need to review Celery task configurations, optimize worker performance, or ensure reliability best practices.

**Basic invocation:**
> Analyze the Celery tasks in /path/to/app/tasks/
> Review this Celery configuration for production readiness
> Check task reliability across the project

**Focused analysis:**
> Audit retry policies for all Celery tasks
> Review task routing configuration
> Check beat schedule for overlapping tasks
> Analyze worker configuration for memory leaks

The agent reads Celery task files, configuration modules, and beat schedules, then produces a comprehensive quality report.

## How It Works

### Step 1: Discover and Parse Celery Components

The agent locates all Celery-related code:

```bash
# Find Celery app configuration
grep -rl "Celery(\|celery_app\|make_celery" /path/to/app/ --include="*.py"

# Find task definitions
grep -rl "@app.task\|@shared_task\|@celery.task" /path/to/app/ --include="*.py"

# Find beat schedule definitions
grep -rl "beat_schedule\|CELERYBEAT_SCHEDULE\|crontab\|solar" /path/to/app/ --include="*.py"

# Find configuration files
grep -rl "broker_url\|result_backend\|CELERY_" /path/to/app/ --include="*.py"
```

The agent parses each component to extract:
- **App configuration** (broker, backend, serialization, timezone)
- **Task definitions** (name, module, decorators, arguments)
- **Retry policies** (max_retries, retry_backoff, retry_jitter)
- **Routing rules** (queues, exchanges, routing keys)
- **Beat schedules** (periodic tasks, crontab, intervals)
- **Signal handlers** (task_prerun, task_postrun, task_failure)
- **Worker configuration** (concurrency, prefetch, pool type)

### Step 2: Audit Task Definitions

The agent checks each task's configuration:

**Task decorator analysis:**

```python
# GOOD: Well-configured task
@shared_task(
    bind=True,
    name="orders.process_payment",
    max_retries=3,
    default_retry_delay=60,
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    acks_late=True,
    reject_on_worker_lost=True,
    time_limit=300,
    soft_time_limit=270,
    rate_limit="100/m",
    track_started=True,
    ignore_result=False,
)
def process_payment(self, order_id: int) -> dict:
    ...

# PROBLEMS the agent detects:
```

```
FAIL: Task "send_email" — no retry configuration
  @shared_task
  def send_email(to, subject, body):
  RISK: Transient SMTP failures cause permanent message loss
  FIX: Add retry policy:
    @shared_task(bind=True, max_retries=3, retry_backoff=True)
    def send_email(self, to, subject, body):
        try: ...
        except SMTPException as exc:
            raise self.retry(exc=exc)

FAIL: Task "process_payment" — no time_limit
  RISK: Stuck payment processing blocks worker indefinitely
  FIX: Add time_limit=300, soft_time_limit=270
  The soft limit raises SoftTimeLimitExceeded so you can clean up

FAIL: Task "generate_report" — acks_late=False (default)
  RISK: If worker crashes mid-task, message is already acknowledged
  The report generation is lost with no retry
  FIX: acks_late=True, reject_on_worker_lost=True

WARN: Task "sync_inventory" — no rate_limit
  This task calls external API with rate limits
  RISK: Worker bursts can trigger API throttling for all consumers
  FIX: rate_limit="30/m" (match API rate limit)

WARN: Task "cleanup_temp_files" — ignore_result not set
  Results are stored but never read for this fire-and-forget task
  FIX: ignore_result=True — saves result backend storage and bandwidth

WARN: Task "update_search_index" — no bind=True
  Cannot access self.retry() or self.request without bind=True
  FIX: @shared_task(bind=True) and add self as first parameter
```

**Task naming audit:**

```
Task Naming Analysis:

  FAIL: Task uses auto-generated name
    "app.tasks.send_email" — derived from module path
    RISK: Renaming the module or moving the file breaks all pending tasks
    FIX: Set explicit name: @shared_task(name="notifications.send_email")

  FAIL: Inconsistent naming convention
    "process_order" (no namespace)
    "payments.charge_card" (dotted namespace)
    "UserSync" (PascalCase)
    FIX: Use consistent dotted namespace: "domain.action_verb"
      "orders.process_order", "payments.charge_card", "users.sync_user"

  WARN: Task name collision risk
    "process" defined in both orders/tasks.py and payments/tasks.py
    Auto-generated names differ but explicit names might collide
    FIX: Always use namespaced explicit names
```

### Step 3: Analyze Retry Policies

The agent evaluates retry configurations for reliability:

```
Retry Policy Analysis:

  Task: "orders.process_payment"
    max_retries: 3
    retry_backoff: True (exponential: 1s, 2s, 4s)
    retry_backoff_max: 600s
    retry_jitter: True
    PASS: Well-configured — exponential backoff with jitter prevents thundering herd

  Task: "integrations.sync_crm"
    max_retries: 10
    default_retry_delay: 5
    retry_backoff: False
    FAIL: Fixed 5-second delay with 10 retries = only 50 seconds of retry window
    For CRM API issues that may last minutes, this is insufficient
    FIX: retry_backoff=True, retry_backoff_max=1800
    This gives: 5s, 10s, 20s, 40s, ... up to 30 min — covers longer outages

  Task: "reports.generate_pdf"
    max_retries: None (infinite retries!)
    FAIL: Infinite retries — a poison message retries forever
    RISK: Consumes worker slots indefinitely, fills dead letter queue
    FIX: Set finite max_retries (3-5 for most tasks)

  Task: "notifications.send_push"
    Retries on all exceptions (bare except)
    FAIL: Retries on ValueError, TypeError — bugs never surface
    FIX: Only retry on transient errors:
      except (ConnectionError, TimeoutError) as exc:
          raise self.retry(exc=exc)
      # Let ValueError, TypeError propagate as failures

  Task: "etl.import_csv"
    autoretry_for=(Exception,)
    FAIL: autoretry_for too broad — retries on programming errors
    FIX: autoretry_for=(IOError, ConnectionError, OperationalError)

  Retry Summary:
    Tasks with retry:       8/15
    Tasks without retry:    5/15 (REVIEW NEEDED)
    Tasks with bad retry:   2/15 (NEEDS FIX)
    Infinite retry tasks:   1/15 (CRITICAL)
```

### Step 4: Review Task Routing and Queues

The agent analyzes routing configuration:

```
Routing Analysis:

  Queue Configuration:
    Queues defined: ["default", "high_priority", "bulk", "notifications"]

  FAIL: No task_routes configured
    All 15 tasks go to "default" queue
    RISK: Bulk import tasks starve payment processing tasks
    FIX: Configure routing:
      task_routes = {
          "orders.process_payment": {"queue": "high_priority"},
          "etl.import_*": {"queue": "bulk"},
          "notifications.*": {"queue": "notifications"},
      }

  FAIL: No dedicated workers per queue
    Single worker process consumes all queues
    RISK: Cannot scale queues independently, cannot set per-queue concurrency
    FIX: Run separate workers:
      celery -A app worker -Q high_priority -c 4
      celery -A app worker -Q bulk -c 2
      celery -A app worker -Q notifications -c 8

  WARN: No priority_steps configured
    Default priority is FIFO only — cannot prioritize within a queue
    FIX: For RabbitMQ: task_queue_max_priority=10
    Then: process_payment.apply_async(priority=9)

  WARN: No dead letter exchange configured
    Failed messages after max_retries are silently discarded
    FIX: Configure DLX for post-mortem analysis:
      task_reject_on_worker_lost = True
      task_acks_on_failure_or_timeout = False
```

### Step 5: Audit Serialization and Security

The agent checks serialization settings:

```
Serialization Analysis:

  FAIL: task_serializer = "pickle"
    RISK: Pickle deserialization allows arbitrary code execution
    Any message injected into the broker can execute code on workers
    FIX: task_serializer = "json"
    AND: accept_content = ["json"]  (reject pickle messages)

  WARN: result_serializer not explicitly set
    Defaults to task_serializer — if pickle, results are also pickled
    FIX: result_serializer = "json"

  FAIL: accept_content = ["json", "pickle"]
    Still accepts pickle — attacker can send pickle-serialized message
    FIX: accept_content = ["json"] only

  WARN: Task "ml.train_model" passes non-JSON-serializable argument
    Argument: numpy array, pandas DataFrame
    RISK: Will fail with json serializer
    FIX: Serialize data before sending:
      - Pass file path or S3 key instead of raw data
      - Use msgpack serializer for binary data
      - Convert to list/dict before sending

  PASS: No task passes ORM model instances as arguments
    (ORM objects are not serializable and create stale data issues)
```

### Step 6: Review Result Backend Configuration

The agent evaluates result backend setup:

```
Result Backend Analysis:

  Backend: Redis (redis://localhost:6379/1)

  FAIL: result_expires not configured
    Default: 24 hours — results accumulate in Redis
    For 10,000 tasks/day = 10,000 keys consuming memory
    FIX: result_expires = 3600  (1 hour, or match your read pattern)

  FAIL: Same Redis instance for broker and results
    redis://localhost:6379/0 (broker)
    redis://localhost:6379/1 (results)
    RISK: Result storage OOM can crash the broker
    FIX: Use separate Redis instances for broker and results

  WARN: result_extended = False (default)
    Extended results include task args, worker hostname, timestamps
    Valuable for debugging production issues
    FIX: result_extended = True

  WARN: 8 tasks have ignore_result=False but results are never read
    These tasks store results that nobody fetches
    FIX: Set ignore_result=True on fire-and-forget tasks:
      send_email, update_cache, sync_analytics, log_event,
      send_webhook, cleanup_files, update_counter, emit_metric

  FAIL: No result_backend_transport_options
    No connection pooling or timeout configuration
    FIX: result_backend_transport_options = {
        "retry_policy": {"max_retries": 3, "interval_start": 0.2},
        "socket_timeout": 5,
    }
```

### Step 7: Analyze Beat Schedule

The agent reviews periodic task configuration:

```
Beat Schedule Analysis:

  Schedule: 12 periodic tasks configured

  FAIL: Overlapping schedules detected
    "sync_all_users" runs every 5 minutes (crontab(*/5))
    "sync_premium_users" runs every 3 minutes (crontab(*/3))
    Both query user table — concurrent runs cause lock contention
    FIX: Stagger schedules or merge into single task with priority flag

  FAIL: Task "generate_daily_report" — no expires setting
    Schedule: crontab(hour=2, minute=0) — runs at 2 AM
    If worker is down at 2 AM, task queues and runs when worker recovers
    By then the report may be stale or a new execution is already scheduled
    FIX: Add expires=3600 — discard if not executed within 1 hour

  FAIL: No task locking — concurrent executions possible
    "sync_inventory" runs every 10 minutes, average runtime 12 minutes
    Overlap: new execution starts before previous completes
    FIX: Use celery-once or implement distributed lock:
      from celery_once import QueueOnce
      @task(base=QueueOnce, once={"graceful": True})

  WARN: Beat schedule uses intervals instead of crontab for daily tasks
    "cleanup" — schedule=timedelta(hours=24)
    RISK: Interval drifts over time (runs at 2:00, then 2:01, 2:03...)
    FIX: Use crontab for fixed-time tasks:
      schedule=crontab(hour=2, minute=0)

  WARN: No jitter on high-frequency tasks
    5 tasks run every minute — all hit broker simultaneously
    FIX: Stagger start times:
      crontab(minute="*/5")  — :00, :05, :10...
      crontab(minute="1-59/5")  — :01, :06, :11... (offset by 1)

  Beat Health:
    Total periodic tasks: 12
    Tasks with expires: 3/12 (NEEDS ATTENTION)
    Tasks with lock protection: 1/12 (CRITICAL)
    Overlapping schedules: 2 pairs detected
```

### Step 8: Review Worker Configuration

The agent audits worker settings:

```
Worker Configuration Analysis:

  FAIL: worker_prefetch_multiplier = 4 (default)
    With long-running tasks, worker grabs 4 tasks but can only process 1
    Other tasks wait in prefetch buffer — poor load distribution
    FIX: worker_prefetch_multiplier = 1 for long tasks
    OR: worker_prefetch_multiplier = 0 (disable) for strict fair scheduling

  FAIL: No worker_max_tasks_per_child configured
    RISK: Memory leaks in tasks accumulate until worker OOM
    FIX: worker_max_tasks_per_child = 1000
    Worker restarts after 1000 tasks — recovers leaked memory

  FAIL: No worker_max_memory_per_child configured
    RISK: Single memory-intensive task can crash the worker
    FIX: worker_max_memory_per_child = 400000  (400 MB in KB)
    Worker restarts if memory exceeds limit

  WARN: worker_pool = "prefork" with I/O-bound tasks
    Most tasks are API calls and database queries (I/O bound)
    Prefork creates heavy processes for each worker
    CONSIDER: worker_pool = "gevent" or "eventlet" for I/O-bound workloads
    CAUTION: Not safe if tasks use non-greenlet-safe libraries

  WARN: worker_concurrency not explicitly set
    Defaults to CPU count — may be too high for memory-heavy tasks
    FIX: Set based on workload:
      CPU-bound: worker_concurrency = CPU_COUNT
      I/O-bound (prefork): worker_concurrency = CPU_COUNT * 2
      I/O-bound (gevent): worker_concurrency = 100-500

  FAIL: No task_soft_time_limit default
    Individual tasks can run forever if no per-task limit set
    FIX: Set global defaults:
      task_soft_time_limit = 300  (5 minutes)
      task_time_limit = 330  (hard kill 30s after soft limit)
```

### Step 9: Check Task Design Patterns

The agent evaluates task design for correctness:

```
Task Design Analysis:

  FAIL: Task "process_batch" accepts queryset as argument
    def process_batch(self, queryset):
    RISK: Django querysets are not serializable
    RISK: Even if pickled, data is stale by the time task runs
    FIX: Pass IDs, query in the task:
      def process_batch(self, item_ids: list[int]):
          items = Item.objects.filter(id__in=item_ids)

  FAIL: Task "update_dashboard" has database transaction spanning task
    with transaction.atomic():
        ... (entire task body)
    RISK: Long-running transaction holds locks, blocks other queries
    FIX: Use smaller transactions within the task, or use bulk operations

  FAIL: Task "send_notifications" iterates and sends one by one
    for user in users:
        send_push(user.id)  # Synchronous call inside task
    RISK: If task fails at user #500 of 1000, all 500 are lost
    FIX: Fan out to individual tasks:
      group(send_push.s(user_id) for user_id in user_ids).apply_async()

  WARN: Task "import_data" has no idempotency check
    Re-running creates duplicate records
    FIX: Use unique constraints and upsert logic, or check task ID:
      if cache.get(f"task_done:{self.request.id}"):
          return  # Already processed

  WARN: Task "process_order" calls another task synchronously
    result = charge_card.delay(order_id).get(timeout=30)
    FAIL: .get() blocks the worker — deadlock risk if workers exhausted
    FIX: Use chain or callback:
      chain(charge_card.s(order_id), fulfill_order.s()).apply_async()

  PASS: Task arguments are JSON-serializable primitives
  PASS: No global mutable state accessed between tasks
```

### Step 10: Produce the Analysis Report

The agent generates a comprehensive report:

```
# Celery Task Analysis Report
# Project: /path/to/app/ | Date: April 30, 2026

## Overview
  Tasks: 15
  Periodic tasks: 12
  Queues: 4 (default, high_priority, bulk, notifications)
  Broker: RabbitMQ
  Result backend: Redis
  Worker pool: prefork

## Overall Health Score: 51/100

## Category Scores
  Task Configuration:     5/10  (missing retries, no time limits)
  Retry Policies:         4/10  (infinite retries, broad exception catch)
  Routing & Queues:       4/10  (no routing, single worker)
  Serialization:          3/10  (pickle in use — security risk)
  Result Backend:         5/10  (no expiry, shared instance)
  Beat Schedule:          5/10  (overlaps, no expires, no locks)
  Worker Config:          4/10  (no memory limits, no prefetch tuning)
  Task Design:            6/10  (queryset args, sync calls)
  Monitoring:             5/10  (no Flower, no metrics)

## Critical Issues
  1. Pickle serializer enabled — remote code execution risk
  2. Infinite retry task — poison messages never cleared
  3. No task time limits — stuck tasks block workers indefinitely
  4. Synchronous .get() call inside task — deadlock risk
  5. No worker memory limits — OOM crashes

## Recommendations Summary
  Estimated effort: 3-5 days for critical + high priority fixes
  Expected improvement: 51 -> 80 health score
  Risk reduction: Eliminates security vulnerability and 3 crash scenarios
```

## Output

The agent produces:

- **Health score**: 0-100 overall Celery configuration quality rating
- **Category scores**: granular ratings for each quality dimension
- **Critical issues**: problems that pose reliability or security risk
- **Per-task analysis**: configuration audit for each task definition
- **Retry policy review**: evaluation of each task's failure handling
- **Routing map**: visual representation of task-to-queue assignments
- **Beat schedule timeline**: periodic task execution timeline with overlap detection
- **Worker tuning recommendations**: pool, concurrency, and memory settings
- **Remediation code**: exact Python code to fix each issue
- **Priority matrix**: issues ranked by risk and effort

## Scope Options

| Scope | What It Covers |
|-------|---------------|
| **Full** (default) | All tasks, config, beat, workers |
| **Single task** | Deep analysis of one task definition |
| **Config only** | Broker, backend, serialization, worker settings |
| **Beat only** | Periodic task schedule analysis |
| **Retry audit** | Retry policies across all tasks |
| **Security** | Serialization, auth, and message signing |

## Broker Support

The agent adapts recommendations based on the broker detected:

| Feature | RabbitMQ | Redis | SQS |
|---------|----------|-------|-----|
| Priority queues | Native support | Limited (0-9) | Not supported |
| Dead letter exchange | Native DLX | Manual implementation | Native DLQ |
| Message persistence | Per-message | AOF/RDB | Always persistent |
| Task routing | Exchange/routing key | Queue name only | Queue URL |
| Visibility timeout | ack_late + prefetch | visibility_timeout | Default 30s |
| Max message size | 128 MB default | 512 MB | 256 KB (use S3) |

## Tips for Best Results

- Point the agent at your entire project for full task discovery
- Include celeryconfig.py or Django settings for configuration analysis
- Share Flower metrics or task logs for runtime behavior analysis
- Run before major deployments or scaling events
- Combine with broker monitoring to correlate config issues with runtime failures
- For Django projects, include settings.py and all apps with tasks.py files
