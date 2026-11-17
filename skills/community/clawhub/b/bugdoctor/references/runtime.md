# Browser, performance and memory evidence

Use the existing authorized tools. Bind observations to the affected page, process, build, request and relevant input. For browser failures, compare console errors, network status and payload, runtime state and the point where the expected UI behavior diverges. A successful network request alone does not establish a successful user action.

For a performance complaint, establish the operation, input and measurement boundary. Use a trace, profiler or query plan to locate the expensive work. Compare equivalent conditions before and after a change; cold starts, cache state or different workloads can invalidate the comparison.

For memory growth, compare snapshots across the relevant lifecycle and inspect retaining paths or unreleased resources. Allocations alone do not establish a leak. Verify the lifecycle that should release the resource before recommending generic cleanup.

If the tool or target is unavailable, say which observation is missing and give the smallest next check. Do not install or expose a remote inspection service merely to satisfy this guide.
