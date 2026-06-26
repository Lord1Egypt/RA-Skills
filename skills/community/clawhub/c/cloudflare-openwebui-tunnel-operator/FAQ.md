# FAQ

## Should the public hostname come from the machine name? | 公网 hostname 应该取自机器名吗？

No. It should come from the project meaning.
不应该。应当取自项目语义。

## Is the Cloudflare API token supposed to live in Git? | Cloudflare API token 应该放进 Git 吗？

No. Keep it in 1Password or another secret manager.
不应该。应当放在 1Password 或其他密钥管理器中。

## Can `account_id` be inferred from the zone? | `account_id` 可以从 zone 推断吗？

Yes, but it is better to write it back into the 1Password item after the first successful run.
可以，但最好在第一次成功执行后回填到 1Password 条目中。

## Why did the public URL return `502` right after startup? | 为什么刚启动时公网 URL 会返回 `502`？

Because `cloudflared` may connect to Cloudflare before the Open WebUI origin is ready inside the Docker network.
因为 `cloudflared` 可能先连上 Cloudflare，而 Docker 网络里的 Open WebUI origin 还没就绪。

## Why must `systemd` use the same `op` binary as the shell? | 为什么 `systemd` 必须使用和 shell 相同的 `op`？

Because the working shell command may actually be a wrapper that injects a service-account token before calling the real CLI.
因为 shell 里能工作的命令，实际可能是一个包装器：它先注入 service-account token，再调用真正的 CLI。

## Should ClawHub be treated as the source of truth? | ClawHub 应该作为事实源吗？

No. Keep the source of truth in `knowledge/` and the local skill folder.
不应该。事实源应保留在 `knowledge/` 和本地 skill 目录中。
