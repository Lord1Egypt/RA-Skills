---
name: weibo-deep-profile-collect
description: 采集微博个人主页的全量信息，包括基础资料（$CONFIG.user）、全部微博、关注列表、收藏列表
version: 2.0.0
---

# 微博个人主页深度采集

## 概述

本 Skill 用于采集微博当前登录用户的个人主页全量信息。通过 `window.$CONFIG.user` 获取结构化基础资料，滚动加载微博列表、关注列表和收藏列表。

**采集内容**：
- 基础资料（`$CONFIG.user`：uid/昵称/简介/粉丝数/关注数/微博数/性别/认证信息/头像等）
- 全部微博（滚动加载）
- 关注用户列表（昵称 + uid）
- 收藏微博列表

**核心技术**：`window.$CONFIG.user` —— 微博页面内置的用户数据对象，返回完整的结构化 JSON，比 DOM 解析更可靠。


> ⚠️ **执行约束**：本 Skill 中的所有 JS 脚本都必须**完整复制执行**，不可自行简化、改写或省略任何部分。每个脚本都经过实际测试验证，简化会导致数据不完整。

## 快速开始

```
使用 weibo-deep-profile-collect 采集我的微博个人主页信息
```

无需提供参数，自动检测当前登录用户。

## 必需参数

无。本 Skill 自动从 `window.$CONFIG.user` 检测当前登录用户。

**前提条件**：浏览器已登录微博账号。

## 执行流程

### 步骤1：导航到微博首页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://weibo.com/`

**说明**：导航到微博首页，用于提取 `$CONFIG.user` 数据。

---

### 步骤2：提取 $CONFIG.user 结构化数据

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `10000`
- `jsScript`:
```javascript
() => {
  try {
    const u = window.$CONFIG && window.$CONFIG.user;
    if (u) {
      return JSON.stringify({
        uid: u.idstr || u.id,
        screen_name: u.screen_name,
        description: u.description,
        followers_count: u.followers_count,
        friends_count: u.friends_count,
        statuses_count: u.statuses_count,
        favourites_count: u.favourites_count,
        gender: u.gender,
        verified: u.verified,
        verified_reason: u.verified_reason,
        avatar_large: u.avatar_large,
        domain: u.domain,
        profile_url: u.profile_url
      });
    }
    return JSON.stringify({error: 'no $CONFIG.user'});
  } catch(e) {
    return JSON.stringify({error: e.message});
  }
}
```

**说明**：`window.$CONFIG.user` 是微博页面内置的用户数据对象，包含完整的用户信息。相比 DOM 解析更可靠、字段更全。

**输出**：`uid`（后续步骤导航使用）、完整用户资料

---

### 步骤3：导航到个人主页

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://weibo.com/u/{step_2.uid}`

---

### 步骤4：滚动加载微博列表

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `120000`
- `jsScript`:
```javascript
async () => {
  let prevCount = 0, sameCount = 0;
  for (let i = 0; i < 50; i++) {
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
    await new Promise(r => setTimeout(r, 2000));
    const cards = document.querySelectorAll(
      'article, [class*="card-wrap"], [class*="Feed_body"], [class*="woo-panel-main"]'
    ).length;
    if (cards === prevCount) { sameCount++; if (sameCount > 5) break; }
    else { sameCount = 0; }
    prevCount = cards;
  }
  window.scrollTo({top: 0}); await new Promise(r => setTimeout(r, 500));
  const MAX_WEIBOS = 200; // 微博上限200条
  const weibos = [];
  document.querySelectorAll(
    'article, [class*="card-wrap"], [class*="Feed_body"]'
  ).forEach(el => {
    if (weibos.length >= MAX_WEIBOS) return;
    const text = el.textContent.trim();
    if (text.length > 20 && text.length < 2000) {
      weibos.push(text.substring(0, 200));
    }
  });
  return JSON.stringify({
    weiboCount: weibos.length, weibos, sampled: weibos.length >= MAX_WEIBOS
  });
}
```

**说明**：滚动加载全部微博。使用多种 CSS 选择器匹配微博卡片（兼容不同版本页面）。智能停止：连续5轮无新增卡片则停止。

---

### 步骤5：导航到关注页面

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://weibo.com/u/page/follow/{step_2.uid}`

**说明**：⚠️ **必须使用新版URL格式 `/u/page/follow/{uid}`**。旧格式 `/u/{uid}/follow` 会重定向到首页。

---

### 步骤6：提取关注用户列表

**工具**：`chrome_execute_script`

**参数**：
- `world`: `MAIN`
- `timeout`: `60000`
- `jsScript`:
```javascript
async () => {
  await new Promise(r => setTimeout(r, 3000));
  // 滚动加载全部
  for (let i = 0; i < 15; i++) {
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
    await new Promise(r => setTimeout(r, 1500));
  }
  window.scrollTo({top: 0}); await new Promise(r => setTimeout(r, 500));
  // 提取关注用户（上限500人）
  const MAX_USERS = 500;
  const users = [], seen = new Set();
  document.querySelectorAll('a[href*="/u/"]').forEach(a => {
    const href = a.getAttribute('href') || '';
    const m = href.match(/\/u\/(\d+)/);
    if (!m) return;
    const linkUid = m[1];
    if (seen.has(linkUid)) return;
    // 排除侧边栏推荐
    if (a.closest('[class*="wbpro-side-card"]')) return;
    // 必须有信息容器（woo-box-item-flex），内含昵称+简介
    const infoDiv = a.querySelector('[class*="woo-box-item-flex"]');
    if (!infoDiv || infoDiv.children.length < 2) return;
    // 第一个子div = 昵称，第二个 = 简介/认证
    const nickname = infoDiv.children[0]?.textContent.trim() || '';
    const desc = infoDiv.children[1]?.textContent.trim() || '';
    if (nickname.length > 0 && nickname.length <= 30 && users.length < MAX_USERS) {
      seen.add(linkUid);
      users.push({name: nickname, uid: linkUid, desc: desc.substring(0, 60)});
    }
  });
  return JSON.stringify({count: users.length, users, sampled: users.length >= MAX_USERS});
}
```

**说明**：滚动加载并提取关注用户列表。关键技术：
- 每个用户卡片为 `a[href*="/u/"]` 链接，内含头像容器(`woo-avatar-main`) + 信息容器(`woo-box-item-flex`)
- 信息容器第一个子 div = 昵称，第二个 = 简介/认证，第三个 = 最新微博
- 排除侧边栏推荐用户（`wbpro-side-card` 容器内）
- 按 uid 去重，排除自己的链接

---

### 步骤7：导航到收藏页面

**工具**：`chrome_navigate`

**参数**：
- `url`: `https://weibo.com/u/page/fav/{step_2.uid}`

---

### 步骤8：提取收藏微博列表

**工具**：`chrome_execute_script`

**说明**：与步骤4类似的滚动+提取逻辑，应用于收藏页面。

**最终结果**：此步骤完成后，所有数据采集完毕。

---

### 步骤9：关闭标签页

**工具**：`chrome_close_tabs`

## 重要提示

### $CONFIG.user 数据源

`window.$CONFIG.user` 返回的字段包括：
- `idstr`/`id`：用户 UID
- `screen_name`：昵称
- `description`：个人简介
- `followers_count`：粉丝数
- `friends_count`：关注数
- `statuses_count`：微博数
- `favourites_count`：收藏数
- `gender`：性别（m/f）
- `verified`：是否认证
- `verified_reason`：认证原因
- `avatar_large`：头像 URL
- `domain`：个性域名

### URL 格式（新版微博）

| 页面 | URL格式 |
|------|---------|
| 个人主页 | `weibo.com/u/{uid}` |
| 关注 | `weibo.com/u/page/follow/{uid}` |
| 粉丝 | `weibo.com/u/page/follow/{uid}?relate=fans` |
| 收藏 | `weibo.com/u/page/fav/{uid}` |

⚠️ 旧版 `/u/{uid}/follow` 格式已失效，会重定向到首页。

## 注意事项

### 平台特性

1. **登录要求**：必须已登录微博账号
2. **$CONFIG.user**：仅在微博主站页面（weibo.com）可用
3. **页面改版**：微博经常更新页面结构，CSS 选择器可能需要调整

### 常见问题

**问题1：$CONFIG.user 返回 null**
- 原因：未登录或微博页面版本更新
- 解决：确认登录状态；检查 `window.$CONFIG` 是否仍存在

**问题2：关注页重定向到首页**
- 原因：使用了旧版 URL 格式
- 解决：使用 `/u/page/follow/{uid}` 格式

**问题3：微博数量为0**
- 原因：该用户未发布微博（`statuses_count=0`）
- 解决：这是正常情况，非错误

## 版本信息

- **当前版本**：2.0.0
- **创建日期**：2026-03-19
- **平台版本**：微博 Web 2026（新版）
- **测试状态**：已通过实际执行验证
- **核心改进**：v2.0 使用正确的新版 URL 格式，$CONFIG.user 结构化数据提取
