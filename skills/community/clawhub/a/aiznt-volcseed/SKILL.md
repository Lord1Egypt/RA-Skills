---
name: aiznt-volcseed
description: >
  即梦 Volcseed 智能修图。Use when: 用户要按提示词改图、需提交参考图 URL 与轮询任务。
metadata:
  openclaw:
    primaryEnv: TS_TOKEN
    requires:
      env:
        - AIZNT_PROXY_URLS
---

# 即梦 Volcseed (aiznt-volcseed)

通过天树 `ts_xxx` 与凭证中的 `aiznt_proxy_urls` 调用 **volcseededit** 提交与查询。

## 配置

与 `aiznt-images` 等同类技能相同：`TS_TOKEN`、`AIZNT_PROXY_URLS`（JSON）。TsClaw **Skills** 页「同步天树凭证」会批量写入。

## 命令

```bash
node scripts/volcseed.js submit --prompt "改成水彩风" --image-urls '["https://example.com/a.png"]'
node scripts/volcseed.js fetch --task-id <task_id>
```

## URL 键

- `volcseededit_submit`
- `volcseededit_fetch`（`{task_id}`）
