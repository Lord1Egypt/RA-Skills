# Optional atomic Skill dependencies

The workbench owns only its orchestration and built-in `script` draft task. It does not bundle or copy the four independent atomic Skills. Install only the tasks you plan to run. These links point to the authors' public GitHub repositories; repository availability is separate from any listing on ClawHub or another marketplace.

| Task | Skill | Public repository | Install command |
| --- | --- | --- | --- |
| `hot-topic` | `douyin-live-hot-free` | [GitHub](https://github.com/xxjrq/douyin-live-hot-free) | `npx skills add xxjrq/douyin-live-hot-free` |
| `diagnosis` | `douyin-account-diagnosis` | [GitHub](https://github.com/xxjrq/douyin-account-diagnosis) | `npx skills add xxjrq/douyin-account-diagnosis` |
| `comment-insights` | `douyin-comment-insights-free` | [GitHub](https://github.com/xxjrq/douyin-comment-insights-free) | `npx skills add xxjrq/douyin-comment-insights-free` |
| `competitor-research` | `douyin-competitor-research-free` | [GitHub](https://github.com/xxjrq/douyin-competitor-research-free) | `npx skills add xxjrq/douyin-competitor-research-free` |
| `script` | Built in | This package | None |

Check the current skill root with:

```bash
node scripts/workbench.mjs dependencies
```

If an atomic Skill is missing, only its associated task is marked `unavailable`. The report includes that Skill's repository and install command, marks the account result `partial`, and continues with other tasks. A task list containing only `script` does not require any atomic dependency.
