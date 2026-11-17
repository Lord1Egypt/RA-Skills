# 避坑（快手创作者平台）

创作者发布页没有 wujie / shadow DOM。snapshot、`page.click`、`role:` 定位可以直接用。下面这些例外是脚本已经处理过的，Agent 重试时不要绕开。

1. **先布防文件选择器，再点「上传视频」。** 点击会弹出原生文件框。定位用 `loc=role:button[name='上传视频']`。页面上还有同文案的 tab，`text=` 会点错。
2. **「发布」是 DIV，不是 `<button>`。** 页面上还有「立即发布」「定时发布」。只匹配元素**自身文本精确等于「发布」**。表单在内部滚动容器里，`window.scrollTo` 无效，要点击前 `scrollIntoView({ block: "center" })`。
3. **上传完成要双确认。** 先等到「重新上传」（文件已被接受），再等到「上传中」消失，并隔 2 秒再看一次。进度条会闪。
4. **「生成中…」的智能封面不挡住发布。** 封面没画完也可以发，平台会补。
5. **默认设置就能发。** 所有人可见、立即发布、同城页勾选。调用方没另说就不要改。要改就在点发布之前改。
6. **描述必须回读。** `execCommand` 写进 contenteditable 之后，比对 `innerText` 和传入的 `desc`。不一致就是失败，不要当成功。
7. **成功信号是管理页 URL + 「审核中」。** 没有单独的成功 toast。点击可能带 `receipt.dialog`，有就 `acceptDialog()`。管理页：`https://cp.kuaishou.com/article/manage/video?status=2&from=publish`。
8. **非标准竖屏可以直接传。** 例如 608×1080，平台会适配，不必先转码。调用方给什么本地文件就传什么。
9. **评论管理用直链，不要点侧栏。** 「互动管理」子菜单跨 ego 调用会收起。脚本直接打开 `https://cp.kuaishou.com/article/comment`。
10. **cp 后台和 www.kuaishou.com 不共享登录。** 公开页即使用后台已登录也是未登录。评论只走后台评论管理。
11. **评论页默认选中最新作品。** 用标题片段核对。要评别的作品，先让人点右上「选择视频」，再带 `spaceId` 重跑。
12. **发送按钮用精确文本 `text="发送"`。** 页面上还有「发送成功」，模糊匹配会点错。
13. **作品标题不是链接。** 在管理列表里点标题会开新标签，后面的 `task.page("p2")` 会拿错页。需要公开链接时，从 `div.video-item` 的 HTML 里取 `3x` 开头的 photoId，拼 `https://www.kuaishou.com/short-video/<photoId>`。
14. **「审核中」看的是待发布列表。** `status=2` 上的「审核中」就是发布终点。过审后这条会离开待发布列表。
15. **ego 内嵌 Node 不继承 shell 环境变量。** 参数由 `publish.sh` / `comment.sh` 写入 `/tmp/kuaishou-video-publish.json` 或 `/tmp/kuaishou-video-comment.json`。不要裸跑 `.js`，也不要指望 `VAR=x ego-browser nodejs` 能读到 `VAR`。
16. **每次发布前先 `check-login`。** 退出码 `2` 必须停。缺 `ego-browser` 也是 soft-fail，不要硬调浏览器。
17. **默认关掉 space。** 成功后 `finish({ keep: [] })`。只有人还要看页面时才传 keep `1`。
