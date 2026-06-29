# Root Cause Analysis Methods Reference

Complete catalog of 20 RCA methods for software debugging.

## 1. 分解法 (Divide & Conquer)

**When**: Unknown cause in a large space with many independent variables.

Split the problem space into halves. Test which half contains the bug.
Recurse on the failing half until isolated.

**Software example**: Page load slow → split into DNS / server / frontend /
asset loading → server is 90% of the time → split server into DB query /
rendering / middleware → DB query is the bottleneck.

## 2. 对比法 (Comparison)

**When**: A working case and a failing case exist side by side.

Compare outcomes under different conditions. Identify what differs between
working and failing cases.

**Software example**: Chrome works, IE errors → compare requests, responses,
HTML → IE doesn't support ES6 syntax.

## 3. 回退法 (Rollback)

**When**: Regression — something that used to work broke after a change.

Revert to known-good state. Re-apply changes one at a time. Identify which
change reintroduces the problem.

**Software example**: Deploy broke login → rollback to stable version → apply
commits one by one → JWT expiry config wasn't applied.

## 4. 假设法 (Hypothesis Testing)

**When**: You have a specific theory about the cause.

"If X then Y should Z". Predict an outcome, test it, confirm or refute.

**Software example**: API sometimes returns 500 → hypothesis "connection pool
leak" → restart should restore connection count to normal ✓.

## 5. 逆推法 (Reverse Inference)

**When**: The failure point is clear but the chain of causation is not.

Trace backward from the failure: what had to be true just before? What had to
be true before that?

**Software example**: Order didn't send confirmation email → check MQ has no
task → check order log "SMTP connection refused" → mail server firewall
changed.

## 6. 尝试法 (Trial & Error)

**When**: The search space is small and each attempt is fast to test.

Iterate through plausible fixes rapidly.

**Software example**: Build symbol not found → clean rebuild → update
dependencies → check case sensitivity → restart IDE → index cache issue.

## 7. 透视法 (Look Inside)

**When**: Surface output doesn't match expectations and internal state is
accessible.

Don't trust the interface. Inspect internal state: logs, metrics, dumps,
debuggers, intermediate values.

**Software example**: API returns empty array but data exists → check SQL log
/ ORM mapping / serialization → null field causes Jackson to filter the
entire record.

## 8. 单变量法 (Single Variable)

**When**: Multiple potential factors and you need to isolate which matters.

Change exactly one variable between tests. Keep everything else constant.

**Software example**: Load test TPS fluctuates → fix concurrency/data/hardware,
tune JVM heap → 2GB has frequent GC, 4GB is stable.

## 9. 边界法 (Boundary Testing)

**When**: Calculations, string handling, or edge cases are involved.

Test edge values: empty, null, zero, max, min, overflow, underflow.

**Software example**: Amount calculation wrong → test 0 / 0.01 / max value /
negative → missing non-zero check on divisor at 0.

## 10. 复现法 (Reproduction)

**When**: Bug is intermittent or hard to trigger.

Find minimal, stable, reliable steps to reproduce. A bug you can't reproduce
reliably is a bug you can't fix confidently.

**Software example**: Concurrent bug is sporadic → fix thread count / data /
run 1000 iterations with Thread.sleep(1) → stable deadlock reproduction.

## 11. 排除法 (Elimination)

**When**: Many components and the interaction between them is suspect.

Disable or remove parts of the system. Does the problem go away? When it
does, the last thing removed is connected.

**Software example**: Spring Boot fails to start → comment out @Component
one by one → specific DataSource config conflicts.

## 12. 置换法 (Substitution)

**When**: You suspect a specific component but can't inspect it directly.

Replace the suspicious component with a known-good one. Does the problem
follow the component or stay?

**Software example**: JAR won't run → try different JRE (same problem) →
try known-good JAR on this JRE (works) → original JAR is corrupted.

## 13. 堆栈法 / 依赖链追溯 (Stack Trace / Chain Tracing)

**When**: Error manifests at one layer but the cause is upstream or downstream.

Walk the full dependency chain from symptom to origin. The bug is often not
where the symptom appears.

**Software example**: CORS fails → check request headers Origin → backend
response headers → gateway layer strips the header → misconfigured.

## 14. 日志注入法 (Log Injection)

**When**: Execution path is unclear and you can add observability.

Insert targeted logging at decision points. What path does execution
actually take? Add entry/exit markers, variable dumps, timing.

**Software example**: Multi-threaded record loss → add "enter/exit + ID" at
each step → finally block clears the queue prematurely.

## 15. 时间回溯法 (Time Travel)

**When**: Something changed but you don't know what or when.

Trace timestamps from the failure backward. What changed right before?
Config deploy? Data update? Dependency release?

**Software example**: Config was overwritten → check etcd change history →
10:23 bulk update → CI script ran without environment check.

## 16. 静候法 (Wait & Observe)

**When**: Problem is intermittent with a long cycle time.

Extend observation. Set up monitoring, logging, or periodic checks.
Sometimes you need to see the full cycle.

**Software example**: Service OOM after a week → monitor GC / heap dump →
a cache grows linearly with no expiry.

## 17. 分层剥离法 (Layer Stripping)

**When**: Multiple layers of abstraction and the failure could be at any level.

Bypass outer layers, test the core directly. Then add layers back until
the failure appears.

**Software example**: Service A calls service B with timeout → curl B's IP
and port directly from A's host (works) → sidecar rate-limit config is too
low.

## 18. 离群分析 (Outlier Analysis)

**When**: Some cases fail and others pass with no obvious pattern.

Compare features of failed vs passed cases. Find the common thread in
the failures that's absent in the passes.

**Software example**: Some users can't log in → check their tokens →
user's token contains a newline character, base64 decode fails.

## 19. 强制失败法 (Force Failure)

**When**: Need to verify resilience or confirm understanding of failure mode.

Deliberately induce the failure condition. Verify your understanding by
making it happen on command.

**Software example**: Test retry logic → mock first two calls to return 500,
third returns 200 → verify client actually retries.

## 20. 同行评审法 / 橡皮鸭法 (Peer Review / Rubber Ducking)

**When**: You've been staring at the problem too long and need distance.

Explain the problem aloud or in writing to an imaginary colleague. The act
of structuring the explanation forces you to organize what you know and
often reveals the missing piece.

**Software example**: Explaining to a colleague why a condition always goes
to `false` → mid-explanation realize you used `=` instead of `==`.
