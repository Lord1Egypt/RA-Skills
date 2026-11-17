# 排错手册

## 先看日志

每次运行结果都会落到 skill 目录下：

- `logs/runs.jsonl` — 每行一次运行的完整结构化结果，最适合排查历史
- `logs/YYYY-MM.log` — 人读的流水

单次排查用 `python claim.py --site xxx --dry-run` 核对请求，再真跑看输出里的「响应片段」。

## 常见故障对照

| 现象 | 原因 | 处理 |
|---|---|---|
| HTTP 401 / 403，或响应是登录页 HTML | Cookie 过期或没带全 | 浏览器重新登录复制 Cookie，`python claim.py --set-cookie <id> "..."` |
| 响应是一大段 HTML 而不是 JSON | URL 抄错，或被重定向到登录/验证页 | 检查 `request.url`；加 `Referer`；`--dry-run` 看最终地址 |
| 状态「待确认」，附响应片段 | 判定规则没匹配上 | 照响应片段改 `expect`，字段名大小写要一致 |
| 提示成功但积分没涨 | 接口有签名校验，或点的是"预览"接口 | 对照真实抓包看 `sign` 字段，见 config-guide 第六节 |
| 每天都是「已领」但实际没领到 | `already_when` 关键字太宽泛 | 把判断收窄到具体字段，例如用 `code` + `msg` 双条件 |
| SSL 证书报错 `CERTIFICATE_VERIFY_FAILED` | 站点证书链不完整/自签 | `settings.insecure_skip_verify` 设为 `true` |
| 返回「请求过于频繁」「操作异常」 | 风控 | 换真实 `User-Agent`；不要在一天内反复重试；确认是否需要 `Referer` |
| 跨零点领到前一天 | 服务端按自己的时区算日期 | 模板变量已固定按北京时间；若站点在别的时区，手动把 `{{yesterday}}` 写死进 body |
| 输出中文乱码 | 控制台编码问题 | 在 PowerShell 里先执行 `chcp 65001`，或改用 `--json` 读取 |

## Cookie 过期：最常见的失败源

Cookie 不是永久的。多数站点 3~30 天失效，表现为某天开始连续 401 或跳转登录页。建议：

1. 每周扫一眼 `logs/runs.jsonl` 里最近的失败记录；
2. 出现连续两天失败时，重新抓一次 Cookie；
3. 更新命令：`python claim.py --set-cookie mysite "sessionid=新值; token=新值"`，只改 Cookie 不碰其他配置。

若站点用 token 而非 Cookie，更新 `request.headers.Authorization` 字段即可。

## 定时任务没执行

- 确认 automation 处于启用状态、上次运行时间正常；
- 确认执行时机器是开机状态——WorkBuddy 的定时任务需要客户端在运行；
- 手动跑一次 `python claim.py` 看是否本身失败，排除脚本问题后再看调度。

## 想加一个新站点

不要手改容易漏字段，直接跑向导：

```bash
python add_site.py
```

它会问 id、URL、Cookie、请求体、判定方式，写入后可选立即测试。
