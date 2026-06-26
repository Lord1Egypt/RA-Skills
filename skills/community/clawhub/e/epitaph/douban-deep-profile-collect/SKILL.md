---
name: douban-deep-profile-collect
description: 采集豆瓣当前登录用户的全量个人信息，包括基础资料、看过/想看的电影、读过/想读的书、广播动态
version: 2.0.0
---

# 豆瓣个人主页深度采集

## 概述

本 Skill 用于采集豆瓣当前登录用户的个人主页全量信息。通过 `/mine/` 自动重定向获取用户ID，使用 `fetch` + `DOMParser` 在页面内分页采集全量数据（保持 cookie 有效）。

**采集内容**：
- 基础资料（昵称/简介/头像/各模块统计）
- 看过的电影（全量分页，含评分/日期/链接）
- 想看的电影（全量分页）
- 读过的书（全量分页，含评分）
- 想读的书（全量分页）
- 广播/动态（滚动加载）

**核心技术**：`fetch` + `DOMParser` 页面内分页 —— 在已登录页面中用 JS 发起 fetch 请求（带 cookie），用 DOMParser 解析返回的 HTML，实现无需翻页的全量数据采集。


> ⚠️ **执行约束**：本 Skill 中的所有 JS 脚本都必须**完整复制执行**，不可自行简化、改写或省略任何部分。每个脚本都经过实际测试验证，简化会导致数据不完整。

## 快速开始

```
使用 douban-deep-profile-collect 采集我的豆瓣个人主页信息
```

无需提供参数，自动检测当前登录用户。

## 必需参数

无。本 Skill 自动从 `/mine/` 重定向检测当前登录用户。

**前提条件**：浏览器已登录豆瓣账号。

## 执行流程

### 步骤1：导航到豆瓣个人主页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://www.douban.com/mine/`

**说明**：`/mine/` 会自动重定向到 `/people/{doubanId}/`，从重定向后的 URL 中提取用户 ID。

---

### 步骤2：提取基础资料和用户ID

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `5000`
- `jsScript`:
```javascript
() => {
  const url = window.location.href;
  const m = url.match(/\/people\/([^\/\?]+)/);
  const doubanId = m ? m[1] : '';
  const info = {};
  const nameEl = document.querySelector('.info h1');
  info.nickname = nameEl ? nameEl.textContent.trim().split('\n')[0] : '';
  const intro = document.querySelector('#intro_display');
  info.intro = intro ? intro.textContent.trim() : '';
  const avatar = document.querySelector('.basic-info img');
  info.avatar = avatar ? avatar.src : '';
  info.doubanId = doubanId;
  info.profileUrl = url;
  return JSON.stringify(info);
}
```

**说明**：提取基础资料和用户 ID（`doubanId`），后续步骤使用 `{step_2.doubanId}` 构建分页 URL。

**输出**：`doubanId`、`nickname`、`intro`、`avatar`

---

### 步骤3：导航到电影收藏页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://movie.douban.com/people/{step_2.doubanId}/collect`

**说明**：导航到电影收藏页，作为 fetch 分页的起始页（需要 cookie 域名匹配）。

---

### 步骤4：采集看过的电影（全量）

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `180000`
- `jsScript`:
```javascript
async () => {
  const doubanId = '{step_2.doubanId}';
  const MAX_ITEMS = 500; // 上限500条
  const allMovies = [];
  const seen = new Set();
  let start = 0;
  while (allMovies.length < MAX_ITEMS) {
    const url = 'https://movie.douban.com/people/' + doubanId
      + '/collect?start=' + start
      + '&sort=time&rating=all&filter=all&mode=list';
    try {
      const resp = await fetch(url, {credentials: 'include'});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const items = doc.querySelectorAll('.list-view .item');
      if (items.length === 0) break;
      items.forEach(item => {
        const titleEl = item.querySelector('.title a');
        const dateEl = item.querySelector('.date');
        const ratingEl = item.querySelector('[class*="rating"]');
        const title = titleEl ? titleEl.textContent.trim() : '';
        const href = titleEl ? titleEl.getAttribute('href') : '';
        const date = dateEl ? dateEl.textContent.trim() : '';
        let rating = 0;
        if (ratingEl) {
          const m = ratingEl.className.match(/rating(\d)/);
          if (m) rating = parseInt(m[1]);
        }
        const commentEl = item.querySelector('.comment');
        const comment = commentEl ? commentEl.textContent.trim() : '';
        const tagsEl = item.querySelector('.tags');
        const tags = tagsEl ? tagsEl.textContent.trim().replace('标签: ', '') : '';
        const key = title + '|' + date;
        if (title && !seen.has(key)) {
          seen.add(key);
          allMovies.push({title, date, rating, comment, tags, href});
        }
      });
      if (items.length < 15) break;
      start += 15;
      await new Promise(r => setTimeout(r, 800));
    } catch(e) { break; }
  }
  const sampled = allMovies.length >= MAX_ITEMS;
  return JSON.stringify({total: allMovies.length, movies: allMovies, sampled});
}
```

**说明**：采集看过的电影全量数据。关键技术：
- `mode=list`：列表视图，每页15条，DOM 结构稳定
- `fetch({credentials:'include'})`：携带 cookie，保持登录态
- `DOMParser`：在页面内解析 HTML，不触发页面跳转
- 评分提取：CSS class `rating1`~`rating5` 对应 1~5 星
- 智能终止：`items.length === 0` 或 `< 15` 时停止
- 按 `title + date` 去重

---

### 步骤5：采集想看的电影（全量）

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `180000`
- `jsScript`:
```javascript
async () => {
  const doubanId = '{step_2.doubanId}';
  const MAX_ITEMS = 500;
  const allMovies = [];
  const seen = new Set();
  let start = 0;
  while (allMovies.length < MAX_ITEMS) {
    const url = 'https://movie.douban.com/people/' + doubanId
      + '/wish?start=' + start
      + '&sort=time&rating=all&filter=all&mode=list';
    try {
      const resp = await fetch(url, {credentials: 'include'});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const items = doc.querySelectorAll('.list-view .item');
      if (items.length === 0) break;
      items.forEach(item => {
        const titleEl = item.querySelector('.title a');
        const dateEl = item.querySelector('.date');
        const title = titleEl ? titleEl.textContent.trim() : '';
        const href = titleEl ? titleEl.getAttribute('href') : '';
        const date = dateEl ? dateEl.textContent.trim() : '';
        const commentEl = item.querySelector('.comment');
        const comment = commentEl ? commentEl.textContent.trim() : '';
        const tagsEl = item.querySelector('.tags');
        const tags = tagsEl ? tagsEl.textContent.trim().replace('标签: ', '') : '';
        const key = title + '|' + date;
        if (title && !seen.has(key)) {
          seen.add(key);
          allMovies.push({title, date, comment, tags, href});
        }
      });
      if (items.length < 15) break;
      start += 15;
      await new Promise(r => setTimeout(r, 800));
    } catch(e) { break; }
  }
  const sampled = allMovies.length >= MAX_ITEMS;
  return JSON.stringify({total: allMovies.length, movies: allMovies, sampled});
}
```

**说明**：与步骤4逻辑相同，URL 路径改为 `/wish`。想看的电影没有评分（还没看），所以不提取 rating。

---

### 步骤5.5：导航到图书页面

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://book.douban.com/people/{step_2.doubanId}/collect`

**说明**：⚠️ **必须先导航到 book.douban.com 域名下**，否则 fetch 请求因跨域限制会失败（movie.douban.com → book.douban.com 跨域）。

---

### 步骤6：采集读过的书（全量）

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `180000`
- `jsScript`:
```javascript
async () => {
  const doubanId = '{step_2.doubanId}';
  const MAX_ITEMS = 500;
  const allBooks = [];
  const seen = new Set();
  let start = 0;
  while (allBooks.length < MAX_ITEMS) {
    const url = 'https://book.douban.com/people/' + doubanId
      + '/collect?start=' + start
      + '&sort=time&rating=all&filter=all&mode=list';
    try {
      const resp = await fetch(url, {credentials: 'include'});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const items = doc.querySelectorAll('.subject-item, .list-view .item');
      if (items.length === 0) break;
      items.forEach(item => {
        const titleEl = item.querySelector('.title a, h2 a');
        const dateEl = item.querySelector('.date, .short-note .date');
        const ratingEl = item.querySelector('[class*="rating"]');
        const title = titleEl ? titleEl.textContent.trim() : '';
        const href = titleEl ? titleEl.getAttribute('href') : '';
        const date = dateEl ? dateEl.textContent.trim() : '';
        let rating = 0;
        if (ratingEl) {
          const m = ratingEl.className.match(/rating(\d)/);
          if (m) rating = parseInt(m[1]);
        }
        const commentEl = item.querySelector('.comment, .short-note .comment');
        const comment = commentEl ? commentEl.textContent.trim() : '';
        const tagsEl = item.querySelector('.tags');
        const tags = tagsEl ? tagsEl.textContent.trim().replace('标签: ', '') : '';
        const pubEl = item.querySelector('.pub');
        const pub = pubEl ? pubEl.textContent.trim() : '';
        const key = title + '|' + date;
        if (title && !seen.has(key)) {
          seen.add(key);
          allBooks.push({title, date, rating, comment, tags, pub, href});
        }
      });
      if (items.length < 15) break;
      start += 15;
      await new Promise(r => setTimeout(r, 800));
    } catch(e) { break; }
  }
  const sampled = allBooks.length >= MAX_ITEMS;
  return JSON.stringify({total: allBooks.length, books: allBooks, sampled});
}
```

**说明**：采集读过的书。与电影类似但注意：
- 使用 `book.douban.com` 域名
- CSS 选择器兼容两种布局：`.subject-item` 和 `.list-view .item`
- 额外提取 `pub`（出版信息：作者/出版社/年份）

---

### 步骤7：采集想读的书（全量）

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `180000`
- `jsScript`:
```javascript
async () => {
  const doubanId = '{step_2.doubanId}';
  const MAX_ITEMS = 500;
  const allBooks = [];
  const seen = new Set();
  let start = 0;
  while (allBooks.length < MAX_ITEMS) {
    const url = 'https://book.douban.com/people/' + doubanId
      + '/wish?start=' + start
      + '&sort=time&rating=all&filter=all&mode=list';
    try {
      const resp = await fetch(url, {credentials: 'include'});
      const html = await resp.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const items = doc.querySelectorAll('.subject-item, .list-view .item');
      if (items.length === 0) break;
      items.forEach(item => {
        const titleEl = item.querySelector('.title a, h2 a');
        const dateEl = item.querySelector('.date, .short-note .date');
        const title = titleEl ? titleEl.textContent.trim() : '';
        const href = titleEl ? titleEl.getAttribute('href') : '';
        const date = dateEl ? dateEl.textContent.trim() : '';
        const commentEl = item.querySelector('.comment, .short-note .comment');
        const comment = commentEl ? commentEl.textContent.trim() : '';
        const tagsEl = item.querySelector('.tags');
        const tags = tagsEl ? tagsEl.textContent.trim().replace('标签: ', '') : '';
        const pubEl = item.querySelector('.pub');
        const pub = pubEl ? pubEl.textContent.trim() : '';
        const key = title + '|' + date;
        if (title && !seen.has(key)) {
          seen.add(key);
          allBooks.push({title, date, comment, tags, pub, href});
        }
      });
      if (items.length < 15) break;
      start += 15;
      await new Promise(r => setTimeout(r, 800));
    } catch(e) { break; }
  }
  const sampled = allBooks.length >= MAX_ITEMS;
  return JSON.stringify({total: allBooks.length, books: allBooks, sampled});
}
```

**说明**：与步骤6逻辑相同，URL 改为 `/wish`。想读的书没有评分。

---

### 步骤8：导航到广播页面

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://www.douban.com/people/{step_2.doubanId}/statuses`

---

### 步骤9：采集广播/动态

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `60000`
- `jsScript`:
```javascript
async () => {
  await new Promise(r => setTimeout(r, 2000));
  let prevH = 0, same = 0;
  for (let i = 0; i < 30; i++) {
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
    await new Promise(r => setTimeout(r, 1500));
    if (document.body.scrollHeight === prevH) {
      same++; if (same > 5) break;
    } else { same = 0; }
    prevH = document.body.scrollHeight;
  }
  window.scrollTo({top: 0});
  const MAX_STATUSES = 200; // 广播上限200条
  const statuses = [];
  document.querySelectorAll('.status-item, .new-status, [data-sid]').forEach(el => {
    if (statuses.length >= MAX_STATUSES) return;
    const text = el.textContent.trim();
    if (text.length > 10) statuses.push(text.substring(0, 300));
  });
  return JSON.stringify({count: statuses.length, statuses, sampled: statuses.length >= MAX_STATUSES});
}
```

**说明**：滚动加载全部广播内容后提取。智能停止：连续5轮页面高度不变则停止。

---

### 步骤10：关闭标签页

**工具**：`chrome_close_tabs`

## 重要提示

### fetch + DOMParser 分页技术

本 Skill 的核心采集方式：在已登录的豆瓣页面内执行 JS 脚本，使用 `fetch` 请求同域 URL（自动携带 cookie），用 `DOMParser` 解析返回的 HTML 提取数据。

**优势**：
- 无需翻页/点击操作，速度快
- 自动携带 cookie，无需处理登录态
- DOMParser 不触发页面跳转，不影响当前页面
- 可精确控制请求间隔（800ms），避免触发频率限制

**关键参数**：
- `mode=list`：列表视图，DOM 结构最稳定
- `sort=time`：按时间排序
- `rating=all` / `filter=all`：不过滤
- `start=N`：偏移量，每页15条

### 豆瓣 URL 结构

| 页面 | URL |
|------|-----|
| 个人主页 | `www.douban.com/people/{id}/` |
| 自动跳转 | `www.douban.com/mine/` |
| 看过电影 | `movie.douban.com/people/{id}/collect` |
| 想看电影 | `movie.douban.com/people/{id}/wish` |
| 读过的书 | `book.douban.com/people/{id}/collect` |
| 想读的书 | `book.douban.com/people/{id}/wish` |
| 广播 | `www.douban.com/people/{id}/statuses` |

⚠️ 注意不同内容使用不同子域名（movie/book/www）。

## 注意事项

### 每条数据必须包含的字段

⚠️ **不能只提取标题！** 每条数据必须包含以下字段，这些是画像分析的关键输入：

| 数据类型 | 必含字段 | 说明 |
|---------|---------|------|
| 看过的电影 | title, date, rating, comment, tags, href | rating=1-5星, comment=用户短评 |
| 想看的电影 | title, date, comment, tags, href | 无 rating（还没看） |
| 读过的书 | title, date, rating, comment, tags, pub, href | pub=出版信息 |
| 想读的书 | title, date, comment, tags, pub, href | 无 rating |

**为什么这些字段重要**：
- `rating`：分析用户评分风格（严格/宽松/打分率）
- `date`：分析观影时间模式（补标行为/特殊日期）
- `comment`：用户自己的一句话评价，最能反映真实想法
- `tags`：用户自定义标签，反映分类习惯

### 平台特性

1. **登录要求**：必须已登录豆瓣账号
2. **跨域限制**：fetch 只能在同域页面执行（步骤3导航到 movie.douban.com，步骤5.5 导航到 book.douban.com）
3. **频率限制**：请求间隔建议 ≥ 800ms，过快可能触发反爬
4. **评分系统**：CSS class `rating1`~`rating5` 对应 1~5 星（每星=2分）

### 常见问题

**问题1：/mine/ 跳转到登录页**
- 原因：未登录或登录过期
- 解决：在浏览器中重新登录豆瓣

**问题2：fetch 返回空数据**
- 原因：cookie 过期或跨域问题
- 解决：确认当前页面在对应域名下（movie.douban.com/book.douban.com）

**问题3：广播提取内容不干净**
- 原因：广播 DOM 结构复杂，包含嵌套的评分/链接等信息
- 解决：后续可优化选择器，精确提取广播文本内容

## 版本信息

- **当前版本**：2.0.0
- **创建日期**：2026-03-19
- **平台版本**：豆瓣 Web 2026
- **测试状态**：已通过实际执行验证（全量电影采集）
- **核心改进**：v2.0 使用 fetch+DOMParser 分页，取代滚动加载
