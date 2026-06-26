---
name: douban-bookmark
description: 输入图书名称，把它加入豆瓣读书的「想读」收藏。适用于“把《xxx》加入豆瓣想读 / 愿望清单 / 想读列表”这类请求。实现方式：先用 HTTP 解析豆瓣搜索结果拿到最优图书详情页，再用 Playwright 持久化浏览器登录态打开详情页，执行豆瓣真实的两段式收藏流程（点“想读”→ 点“保存”）。首次登录后可长期复用浏览器 profile。
---

# 豆瓣图书 Bookmark 自动化

不要再使用 `agent-browser`。

统一使用本 skill 自带脚本：
- `scripts/add_wishlist.py`
- `scripts/add_wishlist.sh`

这套方案分成两段：
1. 用 `requests + BeautifulSoup` 解析豆瓣搜索页，稳定拿到第一本书的详情页 URL
2. 用 `Playwright launch_persistent_context` 复用本地浏览器 profile，打开详情页并点击「想读」

## 前提

环境依赖：
- `python3`
- `requests`
- `beautifulsoup4`
- `playwright`
- 已安装 Chromium：`playwright install chromium`

## 首次登录

首次使用时，先让用户登录一次豆瓣：

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py --login --headed
```

规则：
- 必须带 `--headed`
- 登录完成后，浏览器 profile 会保存在默认目录
- 后续加入「想读」时复用同一个 profile，不要换目录

默认 profile 目录：

```bash
~/.openclaw/browser-profiles/douban-playwright
```

## 正常使用

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py "金钱的艺术"
```

或者：

```bash
skills/douban-bookmark/scripts/add_wishlist.sh "金钱的艺术"
```

脚本会：
1. 搜索书名
2. 解析第一本书详情页 URL
3. 打开详情页
4. 点击「想读」
5. 输出 JSON 结果

## 推荐执行策略

### 已知用户没登录时

先执行：

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py --login --headed
```

等用户登录完成后，再执行：

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py "书名"
```

### 已有登录态时

直接执行：

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py "书名"
```

### 需要观察浏览器行为时

改成有头模式：

```bash
python3 skills/douban-bookmark/scripts/add_wishlist.py "书名" --headed
```

## 输出判断

脚本输出 JSON，重点看这些字段：
- `subject_url`: 命中的豆瓣图书详情页
- `clicked`: 是否实际执行了点击
- `needs_login`: 是否需要先登录
- `success`: 是否大概率成功

如果：
- `needs_login=true` → 先让用户登录
- `clicked=false` → 页面结构变了，需要修脚本
- `success=true` → 可向用户报告已完成或大概率完成

## 实现细节

### 搜索阶段

不要依赖豆瓣图书搜索页前端渲染。

直接请求：

```text
https://www.douban.com/search?cat=1001&q=<书名>
```

从 HTML 里解析 `.result .title a` 或 `.result .pic a`，提取其中跳转到：

```text
https://book.douban.com/subject/<id>/
```

### 点击阶段

不要依赖 ref 编号。

豆瓣这里不是“一次点击就完成”的普通按钮，而是两段式交互：
1. 先点详情页上的 `input[type=submit][value='想读']`
2. 再点弹层表单里的 `input[type=submit][value='保存']`

如果页面已经处于成功态，常见标志是：
- 出现 `我想读这本书`
- 出现 `修改`
- 出现 `删除`

### 登录态

必须使用持久化 context：
- `launch_persistent_context(user_data_dir=...)`

不要使用临时 browser context，否则豆瓣登录态会丢。

## 失败处理

如果失败：
1. 先看是否 `needs_login=true`
2. 再用 `--headed` 重跑一次观察页面
3. 若点击控件失效，更新 `add_wishlist.py` 里的选择器
4. 不要假装成功

## 操作准则

- 优先使用自带脚本，不要临时拼一堆浏览器命令
- 优先复用默认 profile 目录
- 登录问题优先走 `--login --headed`
- 页面结构变化时，修改脚本，不要回退到 agent-browser
