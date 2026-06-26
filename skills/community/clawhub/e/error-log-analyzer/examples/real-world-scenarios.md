# Real-World Test Scenarios

This document contains real-world error scenarios to test the analyzer.

---

## Scenario 1: Node.js Production App Crash

```json
{"level":"error","message":"UnhandledPromiseRejectionWarning: Error: Connection lost: The server closed the connection.","timestamp":"2026-03-06T14:23:11.456Z","stack":"Error: Connection lost: The server closed the connection.\n    at Protocol._enqueue (/app/node_modules/mysql/lib/protocol/Protocol.js:144:48)\n    at Protocol.handshake (/app/node_modules/mysql/lib/protocol/Protocol.js:51:23)\n    at Connection.connect (/app/node_modules/mysql/lib/Connection.js:119:18)"}
{"level":"error","message":"Failed to connect to database after 5 retries","timestamp":"2026-03-06T14:23:12.123Z"}
{"level":"fatal","message":"Application shutting down due to database connection failure","timestamp":"2026-03-06T14:23:12.789Z"}
```

**Expected Analysis:**
- 3 errors detected
- Critical severity (database failure)
- Root cause: MySQL connection lost
- Suggestions: Check MySQL status, verify credentials, check network

---

## Scenario 2: Python Django Application Error

```
2026-03-06 09:15:33,456 - django.request - ERROR - Internal Server Error: /api/v1/users/
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/usr/local/lib/python3.11/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
    return view_func(*args, **kwargs)
  File "/app/api/views.py", line 234, in get_users
    users = User.objects.filter(is_active=True).select_related('profile')
  File "/usr/local/lib/python3.11/site-packages/django/db/models/query.py", line 256, in filter
    return self._filter_or_exclude(False, *args, **kwargs)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
OperationalError: could not connect to server: Connection refused
	Is the server running on host "db" (172.18.0.2) and accepting
	TCP/IP connections on port 5432?
```

**Expected Analysis:**
- 1 critical error
- Root cause: PostgreSQL connection refused
- Suggestions: Check PostgreSQL status, verify Docker network, check port 5432

---

## Scenario 3: Go Microservices Communication Error

```
2026/03/06 15:45:22 ERROR: Failed to call user-service: Post "http://user-service:8080/api/users": dial tcp 172.18.0.5:8080: connect: connection refused
2026/03/06 15:45:23 ERROR: Retry 1/3: user-service unavailable
2026/03/06 15:45:24 ERROR: Retry 2/3: user-service unavailable
2026/03/06 15:45:25 ERROR: Retry 3/3: user-service unavailable
2026/03/06 15:45:26 FATAL: Circuit breaker opened for user-service
```

**Expected Analysis:**
- 5 errors (1 unique pattern)
- Critical severity (service unavailable)
- Root cause: user-service down
- Suggestions: Check service health, verify Kubernetes/Docker status, check logs

---

## Scenario 4: Memory Leak in Node.js

```json
{"level":"warn","message":"JavaScript heap out of memory","timestamp":"2026-03-06T16:00:00.000Z"}
{"level":"error","message":"FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory","timestamp":"2026-03-06T16:00:01.000Z","stack":"FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory\n 1: node::Abort() [node]\n 2: 0x109e42bec [node]\n 3: v8::Utils::ReportOOMFailure() [node]"}
```

**Expected Analysis:**
- 2 errors (1 warn, 1 fatal)
- Critical severity (out of memory)
- Root cause: Memory leak
- Suggestions: Increase heap size, profile memory usage, check for leaks

---

## Scenario 5: Python Celery Task Failure

```
2026-03-06 18:30:45,123 - celery.worker - ERROR - TaskHandlerError
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/celery/app/trace.py", line 450, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/app/tasks/email_tasks.py", line 45, in send_welcome_email
    send_mail(
  File "/usr/local/lib/python3.11/site-packages/django/core/mail/__init__.py", line 87, in send_mail
    return EmailMessage(...).send()
  File "/usr/local/lib/python3.11/site-packages/django/core/mail/message.py", line 284, in send
    return self.get_connection(fail_silently).send_messages([self])
  File "/usr/local/lib/python3.11/site-packages/django/core/mail/backends/smtp.py", line 102, in send_messages
    new_conn_created = self.open()
SMTPServerDisconnected: Connection unexpectedly closed
```

**Expected Analysis:**
- 1 error
- High severity (email service failure)
- Root cause: SMTP connection closed
- Suggestions: Check SMTP server, verify credentials, check firewall

---

## Scenario 6: Database Migration Failure

```
2026-03-06 20:15:33,789 - django.db.migrations - ERROR - Error applying migration users.0012_alter_user_email
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/migrations/executor.py", line 116, in apply_migration
    migration.apply(project_state, schema_editor)
  File "/usr/local/lib/python3.11/site-packages/django/db/migrations/migration.py", line 153, in apply
    operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
  File "/usr/local/lib/python3.11/site-packages/django/db/migrations/operations/fields.py", line 236, in database_forwards
    schema_editor.alter_field(from_model, from_field, to_field)
django.db.utils.ProgrammingError: column "email" of relation "auth_user" contains null values
```

**Expected Analysis:**
- 1 error
- High severity (migration failed)
- Root cause: NULL constraint violation
- Suggestions: Add default value, run data migration, check constraints

---

## Scenario 7: Kubernetes Pod CrashLoopBackOff

```
2026/03/06 22:00:00 ERROR: Liveness probe failed: HTTP probe failed with statuscode: 500
2026/03/06 22:00:05 ERROR: Readiness probe failed: HTTP probe failed with statuscode: 500
2026/03/06 22:00:10 FATAL: Application crashed: panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x8a3b4c]
```

**Expected Analysis:**
- 3 errors (probe failures + crash)
- Critical severity (pod crashing)
- Root cause: Nil pointer dereference
- Suggestions: Add nil checks, fix code bug, review recent changes

---

## Test Results Summary

Run these scenarios with:
```bash
python3 test_real_world.py
```

Expected results:
- All scenarios should be parsed correctly
- Severity should be correctly assessed
- Root causes should be identified
- Actionable suggestions should be provided
