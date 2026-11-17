# 避坑（X 发帖）

主路径是已登录页面上的 `page.fetch` CreateTweet。不要点「发帖」，也不要另写一套请求体。

1. **先装 Ego Lite，`ego-browser` 要在 PATH 上。** 缺失是 soft-fail（退出码 2），不要硬调浏览器。
2. **每次发帖前先 `check-login`。** 退出码 2 必须停。把 `login_tip` 告诉用户。
3. **没有 `--yes` 不发送。** 退出码 3，stdout 是草稿。Agent 先给人看草稿。不要把草稿当成已经发出。
4. **不要猜 POST body，也不要猜 queryId。** 只使用 `references/create-tweet.md` 里 2026-11-04 捕获并验证过的 CreateTweet。客户端包里读到的 `operationName:"CreateTweet"` 可以覆盖捕获值。读不到就用 `l4hk8uVGvR-a8kzQ4nOhPA`。不要发明别的 mutation。
5. **功能开关用捕获下来的那一份。** 少字段或多字段都可能失败。不要为了“补全”去添键。
6. **登录墙和限流。** 401 或没有 `auth_token` 就是要在 Ego 里登录 x.com。HTTP 429 或错误码 88 是限流，不要重试，不要换端点。
7. **GraphQL 226、CORS、ECONNREFUSED 和空缓存。** transaction id 必须按本次 POST 路径现算。不要复用别的 GraphQL 请求上的头。`ondemand.s` 和 `main.*.js` 在 `abs.twimg.com`。`page.fetch` 从 x.com 拉它们会被 CORS 拒绝，得到 0 字节。Node HTTPS 对 `ECONNRESET` 这类中断退避重试最多 4 次，但有的机器（Pro）对这个主机是 `ECONNREFUSED` / 超时，重试也没有正文。check-login 之后的主页经常还没把 `ondemand.s` 放进 CDP 资源树，只读缓存会直接失败。字节因此还有一条浏览器路径，和 Node 并行：CDP `Network.loadNetworkResource` 用 Ego 的网络去拉；拉不到就往当前 x.com 页面插入 script，再读 script 文本、performance resource、`Page.getResourceContent` 和 `Network.getResponseBody`。谁先拿到字节就取消另一边。热身不打开作曲框，也不点发帖。verification key 和 `loading-x-anim` 仍从页面文档读。两边都没有材料就退出，`sent: false`。长文在材料齐了之后才打开 `https://x.com/compose/post`，等两秒，再 `page.fetch` 发帖。 **344** 是每日上限。
8. **`ct0` 必须等于 `x-csrf-token`。** 对不上会 403。这是会话密钥，禁止打印、禁止写进日志、禁止让用户粘贴。
9. **`auth_token` 是 HttpOnly。** `document.cookie` 看不到它。`page.fetch` 必须 `credentials: "include"`，由浏览器自己带上。不要自己拼 Cookie 头。
10. **成功只认状态链接。** `rest_id` 加上 `core.user_results.result.core.screen_name` 组成 `https://x.com/<screen_name>/status/<id>`。没有链接就不是成功。不要把页面上的 toast 当成唯一证据，也不要点掉无关确认框。
11. **回复未验证。** schema 来自客户端包（`in_reply_to_tweet_id` + `exclude_reply_user_ids`）。实页 `page.fetch` 回复没有成功过。
12. **超长走 CreateNoteTweet。** 加权长度大于 280（或 `--long`）不要再发 CreateTweet，否则服务端回 **186**。长文的 `semantic_annotation_options` 多一个 `composition_signal_1: true`。全文看 `note_tweet…text`，不要只看被截断的 `legacy.full_text`。硬上限仍是 25000 字。
13. **图片只走 2026-11-04 捕获的上传。** `--image` 最多 4 张 png / jpeg / webp，每张 ≤ 5 MiB。GIF 不做。没有 `--yes` 不上传。上传必须在 x.com 页面里 `page.evaluate`（`fetch` + `FormData`），不要从 Node 直接 POST 文件，也不要给上传请求加 `x-client-transaction-id`。私信、点赞、关注仍不做。没有图片时 `media_entities` 仍是空数组。
14. **ego 内嵌 Node 不继承 shell 环境变量。** 文案写在临时 entry 的 JSON 里再交给 `ego-browser nodejs`。不要指望 `VAR=x ego-browser` 能读到 `VAR`。
15. **默认关掉 space。** 发帖和 check-login 结束都是 `finish({ keep: [] })`，除非 `--keep`。`cleanup` 只关任务空间 `x-post`，不调用 DeleteTweet。
16. **queryId 会过期。** 新的 `main.*.js` 发布后，旧 id 会失败。失败时重新从包里读 CreateTweet，或由人用 `--query-id` 传入新捕获的 id。不要从别的操作抄一个 id 来试。
