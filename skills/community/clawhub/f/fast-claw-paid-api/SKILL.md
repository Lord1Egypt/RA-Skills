---
name: fast-claw-paid-api
description: 为 Fast Claw 付费演示微服务获取、保存、充值并使用持久 API key。适用于需要发起购买或充值 checkout 流程、把返回的 API key 本地缓存、查询账户余额，或携带 API key 调用 Fast Claw 微服务的场景。
---

# Fast Claw Paid API

优先使用随 skill 附带的客户端脚本，不要手写 HTTP 调用。这个脚本会处理本地 API key 缓存、发起首购和充值 checkout、轮询支付完成状态，并用认证头去调用服务。

## 快速开始

如果服务不在 `http://localhost:8033`，先设置 `FAST_CLAW_SERVICE_URL`。
先执行 `python3 scripts/fast_claw_client.py status` 检查本地 API key 状态。
如果还没有 API key，执行 `python3 scripts/fast_claw_client.py purchase --account-name "<账户名>" --credits 10 --open-browser`。
提示用户在浏览器里完成购买页。脚本会持续轮询，支付完成后把 API key 保存到 `~/.fast-claw/api-key.json`，除非用户通过 `FAST_CLAW_API_KEY_PATH` 或兼容变量 `FAST_CLAW_TOKEN_PATH` 指定了别的位置。
正常调用服务时执行 `python3 scripts/fast_claw_client.py invoke --prompt "..."`。
需要生成耗时较长的分析报告时，执行 `python3 scripts/fast_claw_client.py report --prompt "..."`。这个命令会创建异步 report job，并持续轮询直到完成；如果只想先拿 `job_id`，加上 `--no-wait`，之后再用 `wait-report --job-id ...`。
给同一个账户充值时执行 `python3 scripts/fast_claw_client.py topup --credits 10 --open-browser`，不要更换 API key。
如果想验证外部跳转，创建 checkout 时传 `--success-url "https://www.baidu.com"` 即可。

## 工作流

1. 先用 `status` 查看本地状态。
2. 如果 API key 缺失或失效，执行 `purchase`。
3. 如果服务返回余额不足或次数用尽，执行 `topup`。
4. 需要正式调用时，执行 `invoke`。
5. 需要测试长耗时任务时，执行 `report`，或者先 `report --no-wait` 再 `wait-report`。
6. 如果用户已经从别的入口拿到了 API key，只需要用 `set-api-key` 保存一次。

## 命令说明

- `status`：显示本地 API key 路径、脱敏后的 API key，以及服务端当前余额。
- `purchase`：为新账户创建 checkout 会话，等待支付完成，并把返回的 API key 持久化到本地。
- `topup`：为当前已保存的 API key 创建充值会话。
- `wait --session-id ...`：如果原来的等待超时了，用这个命令继续轮询已有 checkout 会话。
- `invoke --prompt ...`：消耗 1 次额度并调用演示服务。
- `report --prompt ...`：消耗 1 次额度，创建异步分析报告任务，并默认轮询到完成。
- `wait-report --job-id ...`：继续轮询已有 report job，适合 10 到 20 分钟的长任务。
- `set-api-key --api-key ...`：手动保存从其他来源拿到的 API key；旧命令 `set-token --token ...` 仍可用。
- `clear-api-key`：删除本地保存的 API key；旧命令 `clear-token` 仍可用。

## 注意事项

- 每个账户只保留一个稳定 API key。充值应该增加账户额度，而不是签发新 API key。
- 本地文件只是 API key 缓存，不是余额来源。真实额度和账户状态始终由后端维护，用户改本地文件只会导致鉴权失败或切到别的有效 API key。
- 只有在你需要查看底层接口细节，或者想替换掉现有客户端脚本时，才去读 `references/service-api.md`。
