#!/usr/bin/env bash
# CronLint -- Scheduled Task & Cron Job Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate execution overlap or silent failure risk
#   high     -- Significant scheduling problem requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   OE (Overlapping Execution) -- 15 patterns (OE-001 to OE-015)
#   TZ (Timezone & Scheduling) -- 15 patterns (TZ-001 to TZ-015)
#   ER (Error & Recovery)      -- 15 patterns (ER-001 to ER-015)
#   RC (Resource Contention)   -- 15 patterns (RC-001 to RC-015)
#   LM (Lifecycle Management)  -- 15 patterns (LM-001 to LM-015)
#   OB (Observability)         -- 15 patterns (OB-001 to OB-015)

set -euo pipefail

# ============================================================================
# 1. OVERLAPPING EXECUTION (OE-001 through OE-015)
#    Detects cron jobs without file locks, missing mutex/semaphore on
#    scheduled tasks, no singleton enforcement, concurrent run risks,
#    missing pid file checks.
# ============================================================================

declare -a CRONLINT_OE_PATTERNS=()

CRONLINT_OE_PATTERNS+=(
  # OE-001: cron.schedule() call without flock or mutex protection
  'cron\.schedule\([[:space:]]*["\x27]|critical|OE-001|cron.schedule() call without visible flock or mutex protection|Wrap scheduled task body in a distributed lock or flock to prevent overlapping execution'

  # OE-002: setInterval used for scheduled work without overlap guard
  'setInterval\([[:space:]]*[a-zA-Z]*[[:space:]]*,[[:space:]]*[0-9]|high|OE-002|setInterval() used for recurring task without overlap guard|Replace setInterval with a scheduler that prevents overlapping runs or add a running flag check'

  # OE-003: node-cron or cron without any lock import nearby
  'require\([[:space:]]*["\x27]node-cron["\x27]\)|high|OE-003|node-cron imported without visible lock or mutex mechanism|Add file locking (flock) or distributed lock (redis SETNX) to prevent concurrent job execution'

  # OE-004: schedule.scheduleJob without singleton enforcement
  'schedule\.scheduleJob\([[:space:]]*["\x27]|high|OE-004|node-schedule scheduleJob() without singleton enforcement|Add a running flag or distributed lock to ensure only one instance of the job runs at a time'

  # OE-005: APScheduler add_job without misfire_grace_time or max_instances
  'add_job\([^)]*trigger[[:space:]]*=|medium|OE-005|APScheduler add_job() without max_instances or coalesce configuration|Set max_instances=1 and coalesce=True to prevent overlapping execution of the same job'

  # OE-006: crontab entry without flock wrapper
  '[0-9*][[:space:]][0-9*][[:space:]][0-9*][[:space:]][0-9*][[:space:]][0-9*][[:space:]].*\.(sh|py|rb|php)|critical|OE-006|Crontab entry executing script without flock wrapper|Wrap with flock: */5 * * * * flock -n /tmp/job.lock /path/to/script.sh'

  # OE-007: Celery beat schedule without singleton task lock
  'beat_schedule[[:space:]]*=[[:space:]]*\{|medium|OE-007|Celery beat schedule defined without singleton task locking|Use celery-once or redis-based locks to prevent duplicate task execution across workers'

  # OE-008: setTimeout used recursively for scheduling without guard
  'setTimeout\([[:space:]]*[a-zA-Z]*[[:space:]]*,[[:space:]]*[0-9]|medium|OE-008|setTimeout() used for recurring scheduling without overlap prevention|Add an isRunning guard or use a proper scheduler with overlap protection'

  # OE-009: Kubernetes CronJob without concurrencyPolicy
  'kind:[[:space:]]*CronJob|high|OE-009|Kubernetes CronJob without visible concurrencyPolicy setting|Set concurrencyPolicy to Forbid or Replace to prevent overlapping job executions'

  # OE-010: Spring @Scheduled without lock annotation
  '@Scheduled\([^)]*\)|high|OE-010|Spring @Scheduled annotation without distributed lock (ShedLock)|Add @SchedulerLock or ShedLock to prevent multiple instances from running the same scheduled method'

  # OE-011: Python schedule library run_pending without lock
  'schedule\.run_pending\(\)|medium|OE-011|Python schedule run_pending() in loop without overlap guard|Check if the previous job is still running before calling run_pending() to prevent overlap'

  # OE-012: Bull/BullMQ repeat job without removeOnComplete limit
  'repeat[[:space:]]*:[[:space:]]*\{|medium|OE-012|Bull/BullMQ repeat job configuration without removeOnComplete limit|Set removeOnComplete and removeOnFail limits to prevent unbounded job queue growth'

  # OE-013: Quartz cron trigger without disallowConcurrentExecution
  'CronTrigger\([^)]*\)|medium|OE-013|Quartz CronTrigger without @DisallowConcurrentExecution|Add @DisallowConcurrentExecution annotation to the Job class to prevent overlap'

  # OE-014: Sidekiq periodic job without unique lock
  'sidekiq_options[[:space:]].*queue|low|OE-014|Sidekiq job options without unique lock for periodic scheduling|Use sidekiq-unique-jobs to prevent duplicate execution of periodic tasks'

  # OE-015: Generic cron expression in code without any lock reference
  '["\x27][0-9*][[:space:]][0-9*][[:space:]][0-9*][[:space:]][0-9*][[:space:]][0-9*]["\x27]|low|OE-015|Cron expression string detected without visible lock or mutex reference|Ensure scheduled tasks using this expression have overlap protection via locks or semaphores'
)

# ============================================================================
# 2. TIMEZONE & SCHEDULING (TZ-001 through TZ-015)
#    Detects hardcoded timezone strings, DST boundary scheduling,
#    UTC vs local confusion, cron without timezone comment, midnight pitfalls.
# ============================================================================

declare -a CRONLINT_TZ_PATTERNS=()

CRONLINT_TZ_PATTERNS+=(
  # TZ-001: Hardcoded America/New_York timezone string
  'America/New_York|medium|TZ-001|Hardcoded America/New_York timezone in scheduling code|Use Etc/UTC for scheduling and convert to local time only for display purposes'

  # TZ-002: Hardcoded US/Eastern timezone (deprecated)
  'US/Eastern|medium|TZ-002|Deprecated US/Eastern timezone identifier in scheduling code|Replace with IANA timezone America/New_York, or preferably use Etc/UTC for scheduling'

  # TZ-003: new Date().getHours() used in scheduler logic (timezone-naive)
  'new[[:space:]]Date\(\)\.getHours\(\)|high|TZ-003|Date().getHours() in scheduling logic is timezone-naive|Use date-fns-tz or luxon for timezone-aware hour calculations in scheduling code'

  # TZ-004: Hardcoded Europe/London timezone
  'Europe/London|medium|TZ-004|Hardcoded Europe/London timezone in scheduling code|Use Etc/UTC for scheduling logic; Europe/London observes BST which shifts by 1 hour'

  # TZ-005: Cron job scheduled at exactly midnight (DST risk)
  '["\x27]0[[:space:]]0[[:space:]][*0-9]|high|TZ-005|Job scheduled at midnight (00:00) which is risky during DST transitions|Schedule at 00:15 or later to avoid DST skip/repeat window around midnight'

  # TZ-006: Hardcoded Asia/Tokyo or Asia/Shanghai timezone
  'Asia/[A-Z][a-z]+|medium|TZ-006|Hardcoded Asia region timezone in scheduling code|Use Etc/UTC for all scheduling and convert to regional time only for user-facing display'

  # TZ-007: localtime or strftime without explicit timezone
  'localtime\([^)]*\)|medium|TZ-007|localtime() used without explicit timezone (depends on server TZ)|Use gmtime() or explicitly set TZ before calling localtime() for predictable scheduling'

  # TZ-008: Cron scheduled at 2 AM (DST spring-forward skip risk)
  '["\x27][0-9]+[[:space:]]2[[:space:]][*0-9]|high|TZ-008|Job scheduled at 2 AM which may be skipped during DST spring-forward|Avoid scheduling between 1:00-3:00 AM local time; use UTC-based scheduling instead'

  # TZ-009: timezone option set to non-UTC value in scheduler
  'timezone[[:space:]]*:[[:space:]]*["\x27][A-Z]|medium|TZ-009|Scheduler timezone option set to a non-UTC value|Set timezone to Etc/UTC and handle local time conversion at the application layer'

  # TZ-010: Python datetime.now() without timezone in scheduler
  'datetime\.now\(\)[[:space:]]*[^(]|high|TZ-010|datetime.now() without timezone parameter in scheduling context|Use datetime.now(tz=timezone.utc) or datetime.utcnow() for timezone-safe scheduling'

  # TZ-011: Hardcoded UTC offset instead of IANA timezone
  'GMT[+-][0-9]+|medium|TZ-011|Hardcoded GMT offset instead of IANA timezone identifier|Use IANA timezone names (e.g., America/Chicago) which handle DST automatically'

  # TZ-012: time.sleep used for scheduling instead of proper scheduler
  'time\.sleep\([[:space:]]*[0-9]{3,}\)|low|TZ-012|time.sleep() used for long-interval scheduling (drift-prone)|Use a proper scheduler (cron, APScheduler, node-cron) instead of sleep for periodic tasks'

  # TZ-013: cron expression without timezone documentation comment
  'cron\.[a-z]+\([[:space:]]*["\x27][0-9*]|low|TZ-013|Cron expression used without timezone documentation comment|Add a comment indicating which timezone the cron expression is relative to'

  # TZ-014: Hardcoded Pacific timezone
  'US/Pacific|medium|TZ-014|Deprecated US/Pacific timezone identifier in scheduling code|Replace with IANA timezone America/Los_Angeles, or preferably use Etc/UTC'

  # TZ-015: Date constructor with timezone offset string
  'new[[:space:]]Date\([[:space:]]*["\x27][0-9]{4}-[0-9]{2}|low|TZ-015|Date constructor with string argument may parse timezone inconsistently across engines|Use explicit timezone parsing with Intl.DateTimeFormat or a timezone library'
)

# ============================================================================
# 3. ERROR & RECOVERY (ER-001 through ER-015)
#    Detects missing try/catch in scheduled handlers, no retry on failure,
#    no dead letter queue, silent failures, no cleanup on partial failure.
# ============================================================================

declare -a CRONLINT_ER_PATTERNS=()

CRONLINT_ER_PATTERNS+=(
  # ER-001: schedule/cron handler without try-catch wrapping
  'cron\.[a-z]+\([^)]*function|high|ER-001|Scheduled job handler without try-catch error wrapping|Wrap the entire job handler body in try-catch to prevent unhandled exceptions from crashing the scheduler'

  # ER-002: Scheduled task without any error handling visible
  '\.schedule\([^)]*\{[[:space:]]*$|high|ER-002|Scheduled task definition without visible error handling|Add try-catch or .catch() to scheduled task handlers to capture and log failures'

  # ER-003: cron job that calls process.exit on error
  'process\.exit\([[:space:]]*1[[:space:]]*\)|critical|ER-003|process.exit(1) in scheduled job handler kills the entire scheduler|Use error logging and retry logic instead of process.exit() in job handlers'

  # ER-004: Missing retry logic for failed scheduled job
  'catch[[:space:]]*\([[:space:]]*[a-z]+[[:space:]]*\)[[:space:]]*\{[[:space:]]*console\.log|medium|ER-004|Catch block in scheduled job only logs error without retry|Add retry logic with exponential backoff for transient failures in scheduled jobs'

  # ER-005: No dead letter queue or failed job tracking
  '\.on\([[:space:]]*["\x27]failed["\x27]|medium|ER-005|Job failure event handler without dead letter queue or persistent tracking|Send failed jobs to a dead letter queue for investigation and potential reprocessing'

  # ER-006: Empty catch block in scheduled code (silent failure)
  'catch[[:space:]]*\([[:space:]]*[a-z]*[[:space:]]*\)[[:space:]]*\{[[:space:]]*\}|critical|ER-006|Empty catch block in scheduled task silently swallows errors|Log the error and emit a metric or alert on catch; never silently swallow exceptions'

  # ER-007: Scheduled job without timeout configuration
  'cron\.schedule\([^)]*\{|medium|ER-007|Scheduled job without visible timeout or deadline configuration|Set a maximum execution time for jobs to prevent hung tasks from blocking the scheduler'

  # ER-008: No cleanup handler for partial failure
  'finally[[:space:]]*\{[[:space:]]*\}|medium|ER-008|Empty finally block in scheduled task (no cleanup on partial failure)|Add resource cleanup in finally blocks: close connections, release locks, flush buffers'

  # ER-009: sys.exit in Python scheduled handler
  'sys\.exit\([[:space:]]*[0-9]|critical|ER-009|sys.exit() in scheduled job handler kills the entire process|Use exception handling and job retry instead of sys.exit() in scheduled tasks'

  # ER-010: Missing error handler on job queue
  '\.on\([[:space:]]*["\x27]error["\x27][[:space:]]*,[[:space:]]*function|low|ER-010|Generic error handler on job queue without specific failure recovery|Implement specific error recovery strategies per job type rather than generic error logging'

  # ER-011: raise/throw in scheduler without outer catch
  'raise[[:space:]][A-Z][a-zA-Z]*Error|medium|ER-011|Exception raised in scheduled context without visible outer error handler|Ensure all scheduled task entry points have top-level error handling to prevent scheduler crashes'

  # ER-012: Job executed without checking prerequisite conditions
  'async[[:space:]]function[[:space:]][a-z]*[Jj]ob|low|ER-012|Async job function without visible precondition or health check|Validate prerequisites (database connectivity, API availability) before executing scheduled work'

  # ER-013: No circuit breaker on external calls in scheduled job
  'fetch\([[:space:]]*["\x27]https|medium|ER-013|HTTP fetch in scheduled job without circuit breaker or retry policy|Add a circuit breaker or retry-with-backoff for external API calls in scheduled tasks'

  # ER-014: Celery task without retry configuration
  '@app\.task|medium|ER-014|Celery task decorator without retry or autoretry configuration|Add autoretry_for, retry_backoff, and max_retries to @app.task for failure recovery'

  # ER-015: No error notification or alerting in job failure path
  'console\.error\([[:space:]]*["\x27].*[Ff]ail|low|ER-015|Job failure logged to console without notification or alerting|Send alerts (email, Slack, PagerDuty) on job failures in addition to logging'
)

# ============================================================================
# 4. RESOURCE CONTENTION (RC-001 through RC-015)
#    Detects all jobs at same minute, database-heavy jobs without pooling,
#    no rate limiting on batch jobs, memory-unbounded processing in cron.
# ============================================================================

declare -a CRONLINT_RC_PATTERNS=()

CRONLINT_RC_PATTERNS+=(
  # RC-001: Cron expression running every minute (resource abuse)
  '["\x27][*][[:space:]][*][[:space:]][*][[:space:]][*][[:space:]][*]["\x27]|critical|RC-001|Cron expression runs every minute (excessive resource consumption)|Increase the interval to match actual requirements; every-minute jobs are rarely necessary'

  # RC-002: Multiple jobs scheduled at the top of the hour (:00)
  '["\x27]0[[:space:]]0[[:space:]][*][[:space:]][*][[:space:]][*]["\x27]|high|RC-002|Job scheduled at exactly midnight daily without staggering|Stagger job start times (e.g., 00:05, 00:15, 00:30) to reduce resource contention at midnight'

  # RC-003: Database query inside a scheduled loop without connection pooling
  '\.query\([[:space:]]*["\x27]SELECT|medium|RC-003|SQL query in scheduled job without visible connection pooling|Use a connection pool for database operations in scheduled jobs to prevent connection exhaustion'

  # RC-004: Unbounded SELECT in scheduled job (no LIMIT)
  'SELECT[[:space:]][*][[:space:]]FROM[[:space:]]|high|RC-004|SELECT * FROM in scheduled job without LIMIT clause (memory risk)|Add LIMIT and pagination to queries in scheduled jobs to prevent memory exhaustion on large tables'

  # RC-005: Batch processing without rate limiting
  'forEach\([[:space:]]*async|medium|RC-005|Async forEach in scheduled job fires all promises simultaneously|Use a rate-limited queue (p-limit, bottleneck) or process items in sequential batches'

  # RC-006: Promise.all on unbounded array in scheduled job
  'Promise\.all\([[:space:]]*[a-zA-Z]+\.map|high|RC-006|Promise.all on mapped array in scheduled job (unbounded concurrency)|Use Promise.allSettled with concurrency limit or p-limit to control parallel execution'

  # RC-007: No memory limit on batch processing
  'while[[:space:]]*\([[:space:]]*true[[:space:]]*\)|medium|RC-007|Infinite while loop in scheduled context without memory or iteration bounds|Add iteration count limit and memory checks to prevent runaway resource consumption'

  # RC-008: File system operations in cron without cleanup
  'writeFileSync\([[:space:]]*["\x27]/tmp|medium|RC-008|Temp file written in scheduled job without visible cleanup|Add cleanup logic (try/finally with unlink) for temporary files created in scheduled jobs'

  # RC-009: Spawning child processes in cron without limits
  'child_process\.[a-z]+\(|medium|RC-009|Child process spawned in scheduled job without resource limits|Set maxBuffer, timeout, and CPU/memory limits on child processes in scheduled jobs'

  # RC-010: Multiple cron jobs all at minute 0
  '["\x27]0[[:space:]][0-9]+[[:space:]][*]|low|RC-010|Job scheduled at minute 0 of the hour (common contention point)|Stagger job start minutes (use prime numbers: 7, 13, 23, 37, 47) to distribute load'

  # RC-011: Large file read in scheduled job without streaming
  'readFileSync\([[:space:]]*["\x27]|medium|RC-011|Synchronous file read in scheduled job blocks event loop|Use streaming (createReadStream) or async file reads for large files in scheduled tasks'

  # RC-012: No backpressure handling in scheduled batch
  '\.pipe\([[:space:]]*[a-zA-Z]+|low|RC-012|Piped stream in scheduled job without visible backpressure handling|Implement backpressure handling (pause/resume or highWaterMark) for streamed batch jobs'

  # RC-013: Cron running every 5 seconds or less
  '["\x27][*]/[1-5][[:space:]][*][[:space:]][*]|high|RC-013|Cron running every 1-5 minutes (excessive frequency for most use cases)|Evaluate if the frequency is truly needed; most jobs work fine at 10-15 minute intervals'

  # RC-014: No concurrency limit on worker pool
  'new[[:space:]][A-Z][a-zA-Z]*Pool\([[:space:]]*\)|medium|RC-014|Worker pool created without explicit concurrency limit|Set a maximum worker count matching available CPU cores to prevent resource overcommitment'

  # RC-015: Scheduled job accessing shared resource without locking
  'redis\.[a-z]+\([[:space:]]*["\x27]lock|low|RC-015|Redis lock referenced in scheduled job (verify lock is properly acquired and released)|Ensure locks have TTL expiry and are released in finally blocks to prevent deadlocks'
)

# ============================================================================
# 5. LIFECYCLE MANAGEMENT (LM-001 through LM-015)
#    Detects missing graceful shutdown, orphaned scheduled tasks,
#    no job deregistration on deploy, no health check for scheduler,
#    stale cron entries.
# ============================================================================

declare -a CRONLINT_LM_PATTERNS=()

CRONLINT_LM_PATTERNS+=(
  # LM-001: No SIGTERM/SIGINT handler for scheduler process
  'cron\.schedule\([^)]*\)|high|LM-001|Scheduler running without visible SIGTERM or SIGINT graceful shutdown handler|Add process.on SIGTERM/SIGINT handlers to stop accepting new jobs and drain current ones'

  # LM-002: No graceful shutdown on scheduler stop
  '\.start\(\)[[:space:]]*;[[:space:]]*$|medium|LM-002|Scheduler started without corresponding graceful shutdown logic|Implement stop() or destroy() call on process exit to drain in-flight jobs cleanly'

  # LM-003: Scheduled jobs not cleared on application restart
  'schedule\.scheduleJob|medium|LM-003|scheduleJob() called without clearing previous schedule on restart|Call schedule.gracefulShutdown() or cancelAll() before re-registering jobs on restart'

  # LM-004: No health check endpoint for scheduler service
  'app\.listen\([[:space:]]*[0-9]|low|LM-004|Server started without visible scheduler health check endpoint|Add a /health or /ready endpoint that verifies the scheduler is running and processing jobs'

  # LM-005: Cron job referencing deleted or moved script path
  '/usr/local/bin/[a-z]+|low|LM-005|Cron references absolute path which may become stale after deployment|Use relative paths with proper working directory or deploy-time path resolution'

  # LM-006: setInterval without clearInterval on shutdown
  'setInterval\([[:space:]]*[a-zA-Z]+|medium|LM-006|setInterval() without corresponding clearInterval() on process shutdown|Store the interval ID and call clearInterval() in shutdown handler to prevent orphaned timers'

  # LM-007: Job queue not properly drained before shutdown
  '\.close\(\)[[:space:]]*;[[:space:]]*$|medium|LM-007|Queue or connection closed without waiting for in-flight jobs to complete|Use graceful close with drain: await queue.close(30000) to finish running jobs before exit'

  # LM-008: No job version or idempotency key management
  'add\([[:space:]]*["\x27][a-z]|low|LM-008|Job added to queue without visible idempotency key or version tracking|Add idempotency keys to prevent duplicate processing during deployments and restarts'

  # LM-009: Scheduler not restarting failed workers
  'cluster\.fork\(\)|medium|LM-009|Worker forked without visible restart-on-exit logic for scheduler continuity|Add cluster.on exit handler to respawn failed workers maintaining scheduler availability'

  # LM-010: No deployment-safe job re-registration
  'register[Jj]ob|low|LM-010|Job registration function without deployment-safe deregistration of old jobs|Implement remove-then-register pattern to prevent stale jobs from persisting across deploys'

  # LM-011: Orphaned setTimeout reference without cleanup tracking
  'setTimeout\([[:space:]]*function|medium|LM-011|setTimeout with anonymous function cannot be cleared on shutdown|Store timeout references and clear them on process exit to prevent orphaned callbacks'

  # LM-012: No scheduler heartbeat or liveness probe
  'CronJob\([[:space:]]*["\x27]|low|LM-012|CronJob created without visible heartbeat or liveness monitoring|Emit periodic heartbeat events from the scheduler for external monitoring systems'

  # LM-013: Multiple scheduler instances without leader election
  'new[[:space:]]Cron[A-Za-z]*\(|medium|LM-013|Cron scheduler instantiated without visible leader election for multi-instance|Use leader election (redis, etcd, pg advisory lock) to run scheduler on single instance only'

  # LM-014: Process exit handler missing in scheduler
  'process\.on\([[:space:]]*["\x27]exit["\x27]|low|LM-014|Process exit handler found but verify it properly cleans up scheduled tasks|Ensure exit handler cancels all pending jobs and releases locks before exiting'

  # LM-015: atexit handler without scheduler cleanup in Python
  'atexit\.register\(|low|LM-015|atexit handler registered but verify scheduler shutdown is included|Ensure atexit handler calls scheduler.shutdown(wait=True) to drain pending jobs'
)

# ============================================================================
# 6. OBSERVABILITY (OB-001 through OB-015)
#    Detects missing job duration logging, no start/end timestamps,
#    no alerting on skip/failure, no metrics emission, missing execution
#    history tracking.
# ============================================================================

declare -a CRONLINT_OB_PATTERNS=()

CRONLINT_OB_PATTERNS+=(
  # OB-001: Scheduled job without start timestamp logging
  'cron\.[a-z]+\([^)]*function[[:space:]]*\(\)|high|OB-001|Scheduled job handler without start timestamp logging|Log job start time at the beginning of every scheduled handler for duration tracking'

  # OB-002: Scheduled job without end/completion logging
  'console\.log\([[:space:]]*["\x27].*[Cc]omplete|low|OB-002|Job completion logged without structured end timestamp or duration|Use structured logging with startTime, endTime, and durationMs fields for observability'

  # OB-003: No job execution duration measurement
  'Date\.now\(\)[[:space:]]*;[[:space:]]*$|medium|OB-003|Date.now() captured without visible duration calculation in scheduled job|Calculate and log duration: const duration = Date.now() - startTime at job completion'

  # OB-004: Missing metrics emission for job execution
  '\.schedule\([^)]*\{|medium|OB-004|Scheduled job without visible metrics emission (e.g., StatsD, Prometheus)|Emit metrics for job_started, job_completed, job_failed, and job_duration_seconds'

  # OB-005: No alerting on consecutive job failures
  'catch[[:space:]]*\([[:space:]]*[a-z]+\)[[:space:]]*\{[[:space:]]*console\.|medium|OB-005|Job failure caught and logged without alerting on consecutive failures|Implement alerting (PagerDuty, Slack) after N consecutive failures of the same job'

  # OB-006: No tracking of skipped job runs
  'if[[:space:]]*\([[:space:]]*[a-z]*[Rr]unning|low|OB-006|Job skip condition detected without logging or metric for skipped runs|Log and emit a metric when a job run is skipped due to overlap or condition check'

  # OB-007: Job queue without visibility into pending count
  'add\([[:space:]]*["\x27][a-z]+["\x27][[:space:]]*,|low|OB-007|Job added to queue without visibility into queue depth or pending count|Expose queue depth metrics and alert when pending jobs exceed threshold'

  # OB-008: No structured logging in scheduled task
  'console\.log\([[:space:]]*["\x27]cron|medium|OB-008|Cron job uses console.log instead of structured logger|Use a structured logger (winston, pino, bunyan) with job_id, timestamp, and severity fields'

  # OB-009: Missing job execution history persistence
  'schedule\.[a-z]+\([[:space:]]*["\x27]|medium|OB-009|Scheduled job without execution history persistence|Store job execution records (start, end, status, error) in a database for audit and debugging'

  # OB-010: No last-successful-run tracking
  '["\x27]last[_-]run["\x27]|low|OB-010|last_run reference found but verify successful run tracking is separate from any run|Track last_successful_run separately from last_run to detect silently failing jobs'

  # OB-011: Silent job completion without any logging
  'return[[:space:]]*;[[:space:]]*\}[[:space:]]*\)|medium|OB-011|Scheduled job returns without any completion logging|Add a log statement before every return point in scheduled jobs for execution tracing'

  # OB-012: No SLA monitoring for job completion time
  'timeout[[:space:]]*:[[:space:]]*[0-9]+|low|OB-012|Timeout configured but no visible SLA monitoring for job completion|Track p95 and p99 job durations and alert when jobs exceed SLA thresholds'

  # OB-013: Error logged without job context (job_id, attempt number)
  'console\.error\([[:space:]]*[a-z]+\)|medium|OB-013|Error logged in scheduled job without context (job_id, attempt, run_id)|Include job_id, attempt_number, and run_id in all error logs for correlation'

  # OB-014: No dashboard or monitoring for scheduler status
  'new[[:space:]]CronJob\(|low|OB-014|CronJob instantiated without visible monitoring dashboard setup|Create a scheduler dashboard showing job statuses, last run times, and failure rates'

  # OB-015: Job processor without trace or span context
  'process\([[:space:]]*[a-z]+[[:space:]]*\)[[:space:]]*\{|low|OB-015|Job processor function without distributed tracing span or context|Add OpenTelemetry span or trace context to job processors for end-to-end observability'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
cronlint_pattern_count() {
  local count=0
  count=$((count + ${#CRONLINT_OE_PATTERNS[@]}))
  count=$((count + ${#CRONLINT_TZ_PATTERNS[@]}))
  count=$((count + ${#CRONLINT_ER_PATTERNS[@]}))
  count=$((count + ${#CRONLINT_RC_PATTERNS[@]}))
  count=$((count + ${#CRONLINT_LM_PATTERNS[@]}))
  count=$((count + ${#CRONLINT_OB_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
cronlint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_cronlint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_cronlint_patterns_for_category() {
  local category="$1"
  case "$category" in
    OE|oe) echo "CRONLINT_OE_PATTERNS" ;;
    TZ|tz) echo "CRONLINT_TZ_PATTERNS" ;;
    ER|er) echo "CRONLINT_ER_PATTERNS" ;;
    RC|rc) echo "CRONLINT_RC_PATTERNS" ;;
    LM|lm) echo "CRONLINT_LM_PATTERNS" ;;
    OB|ob) echo "CRONLINT_OB_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_cronlint_category_label() {
  local category="$1"
  case "$category" in
    OE|oe) echo "Overlapping Execution" ;;
    TZ|tz) echo "Timezone & Scheduling" ;;
    ER|er) echo "Error & Recovery" ;;
    RC|rc) echo "Resource Contention" ;;
    LM|lm) echo "Lifecycle Management" ;;
    OB|ob) echo "Observability" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_cronlint_categories() {
  echo "OE TZ ER RC LM OB"
}

# Get categories available for a given tier level
# free=0 -> OE, TZ (30 patterns)
# pro=1  -> OE, TZ, ER, RC (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_cronlint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "OE TZ ER RC LM OB"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "OE TZ ER RC"
  else
    echo "OE TZ"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
cronlint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in OE TZ ER RC LM OB; do
      cronlint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_cronlint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_cronlint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_cronlint_category() {
  local category="$1"
  case "$category" in
    OE|oe|TZ|tz|ER|er|RC|rc|LM|lm|OB|ob) return 0 ;;
    *) return 1 ;;
  esac
}
