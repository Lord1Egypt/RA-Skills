---
name: ci-long-red-triage
description: "Triage long-running red CI: attribute failures to commits, locate the failing step per job, distinguish a broken gate from a failing one, and fix environment-dependency assertions. Infrastructure failures are not code changes."
---

# 长期红的 CI 分诊与修绿

用于：仓库 CI 连续多天红、多个 job 同时红、不确定是不是自己刚推的那批改动造成的；或某道门「红了很久没人管」。

## 1. 先判归属：与前一个提交的 run 对照

不要凭「我刚推完就红了」认定是自己引入的。拉历史 run 和父提交那一次的 job 结果：

    gh run list --repo <owner/repo> --limit 12 \
      --json databaseId,headSha,status,conclusion,createdAt,displayTitle
    gh run list --repo <owner/repo> --limit 40 --json databaseId,headSha,conclusion \
      --jq '.[]|select(.headSha=="<parent-sha>")'

父提交在同一 job 上以同一原因失败 ⇒ 既有红门；否则才是本批引入。结论按 job 粒度写，不要写「CI 红了」这种整句。

## 2. 逐 job、逐 step 定位，看最下面的失败点

    gh run view <run-id> --repo <owner/repo> --json status,conclusion,jobs \
      --jq '.jobs[]|{name,conclusion}'
    gh run view <run-id> --repo <owner/repo> --log-failed > /tmp/ci.log
    grep -nE 'ERROR|FAIL:|Error:' /tmp/ci.log | head -30

一个 job 里前面的 step 失败，后面所有 step 记为「未执行」—— 不是通过。日志里大量 UNKNOWN STEP 是取日志工具的显示问题，按错误标记行定位。

## 3. 区分「门起不来」与「门判红」

同一个红，处置完全不同：

- **门起不来**：linter 配置格式不被当前版本接受时，它在加载配置阶段就退出（常见 exit 3），此时一条规则都没跑。先本地验证配置能加载（如 golangci-lint config verify），修配置本身。
- **门判红**：配置能加载、规则真的跑了并报问题。逐条修。

修好「起不来」的门后，会一次浮出一大批存量问题（十几天没真正跑过的量），这是预期；按批修完再提交，不要因数量多而回退配置。

## 4. 报出的条数可能被截断

golangci-lint 默认 max-same-issues: 3、max-issues-per-linter: 50，同类问题只报前几条。查全量：

    golangci-lint run --timeout=5m --max-same-issues=0 --max-issues-per-linter=0

「只报了 9 项」不等于「只有 9 项」。

## 5. 本地绿／CI 红 = 环境依赖型断言

迹象：断言里出现「是否配了 key」「某个 home 目录下的数据是否存在」「某个外部服务可达」。这类断言在开发机为真、在 runner 为假。

改法二选一：

- 改断结构态：对权威注册表判成员关系（例如「这个 id 是否在 provider 目录里」），而不是判「有没有配 key」。
- 自建 fixture：t.TempDir() 加环境变量把数据目录指过去，再自己播种最少数据。

复现 CI 条件：

    rm -rf /tmp/fh && mkdir -p /tmp/fh && HOME=/tmp/fh go test -count=1 ./...

干净 HOME 下全过，才算真的修好。

## 6. 基础设施型失败不要改代码

产物上传报「存储配额已满」、通知投递失败一类，属账号或平台侧限制。给该 step 加 continue-on-error: true，并注明它是辅助产物不是门禁；真正的 build / test / lint / 文档门保持硬失败。别为了让它变绿而降低真门禁的严格度。

## 7. 推完必须核对 CI

    git push <url> main:main
    gh run list --repo <owner/repo> --commit <sha>    # 确认这次提交触发的 run 与结论

「推成功」不等于「CI 绿」。核对到 job 级全 success 才算完成。

推送本身失败时按顺序排查，不要反复重试同一个地址：

- 连接被重置 / TLS 非正常终止 / 长时间无输出后超时 ⇒ 换传输路径：把 remote 的加速代理 URL 换成直连 `https://github.com/<owner>/<repo>.git` 再推（`git push https://github.com/<owner>/<repo>.git main:main`）。先用 `timeout 15 curl -sS -o /dev/null -w '%{http_code}' https://github.com/` 判断直连是否可达。
- 用 URL 直推**不会**更新本地 `refs/remotes/origin/main`，`git status` 会一直显示领先若干提交 ⇒ 推成功后手工同步：`git update-ref refs/remotes/origin/main <新sha> <旧sha>`。
- 网络不稳时单次 `git push` 可能挂满两分钟才失败；不要在同一个 exec 里串多次重试。放到后台跑并把输出落盘，或直接重试一次新的调用。
- 核对远端真值用 `gh api repos/<owner>/<repo>/commits/main --jq .sha`，不要只信本地 `rev-parse`。

## 交付

归属结论（既有／本批，附父提交 run 的 job 结论）+ 失败点清单（job → step → 原因）+ 修复 + 本地验证证据（clean-HOME 测试、lint 0 问题、门脚本 OK）。
