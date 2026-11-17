# 支持平台与 URL 规范 (Supported Platforms)

本文档记录了当前 Skill 支持的主流社交/视频平台的搜索与交互规范。

---

## 1. 抖音 (Douyin)
- **平台代码**: `douyin` / `tiktok`
- **首页**: `https://www.douyin.com/`
- **搜索 URL**: `https://www.douyin.com/search/{encoded_name}?type=user`
- **识别特征**:
  - 用户卡片: `div[data-e2e="search-user-item"]`，以及限定在搜索区域内的用户卡片
  - 关注按钮: `button:has-text("关注")`
  - 已关注状态: `已关注`, `互相关注`
- **注意事项**: `douyin.com` 可能跳转至「抖音精选」，搜索结果会在 SPA 中异步出现。执行器仅轮询带用户主页链接的搜索结果卡片，最长等待 22 秒，不会把侧边栏「我的」当作结果；高频检索可能触发滑块验证。

---

## 2. 哔哩哔哩 (Bilibili)
- **平台代码**: `bilibili` / `b站`
- **首页**: `https://www.bilibili.com/`
- **搜索 URL**: `https://search.bilibili.com/upuser?keyword={encoded_name}`
- **识别特征**:
  - 用户卡片: `li.user-item`, `div.user-item`
  - 关注按钮: `button:has-text("关注")`, `button:has-text("+ 关注")`
  - 已关注状态: `已关注`, `已互粉`
- **注意事项**: 需注意未登录时点击关注会弹出登录弹窗。

---

## 3. 小红书 (Xiaohongshu)
- **平台代码**: `xiaohongshu` / `red` / `小红书`
- **首页**: `https://www.xiaohongshu.com/`
- **搜索 URL**: `https://www.xiaohongshu.com/search_result?keyword={encoded_name}&type=user`
- **识别特征**:
  - 用户卡片: `div.onebox a[href*="/user/profile/"]`（昵称和粉丝数位于该结果卡片文本中）
  - 关注按钮: `button:has-text("关注")`
  - 已关注状态: `已关注`, `互相关注`
- **注意事项**: 搜索页通过 SPA 异步渲染。只等待结果卡片内的资料链接，最长约 17.5 秒；不可用页面任意资料链接作就绪信号，因为侧边栏“我”的链接会提前出现。小红书网页版对未登录搜索有频率限制，务必保持登录状态。

---

## 4. X / Twitter
- **平台代码**: `x` / `twitter` / `推特`
- **首页**: `https://x.com/`
- **搜索 URL**: `https://x.com/search?q={encoded_name}&f=user`
- **识别特征**:
  - 用户卡片: `div[data-testid="UserCell"]`
  - 关注按钮: `button[data-testid$="-follow"]`, `button:has-text("Follow")`
  - 已关注状态: `Following`, `已关注`
- **注意事项**: 需具备可用网络环境与已登录状态。

---

## 5. YouTube
- **平台代码**: `youtube` / `油管`
- **首页**: `https://www.youtube.com/`
- **搜索 URL**: `https://www.youtube.com/results?search_query={encoded_name}&sp=EgIQAg%253D%253D`
- **识别特征**:
  - 频道卡片: `ytd-channel-renderer`
  - 订阅按钮: `button:has-text("订阅")`, `button:has-text("Subscribe")`
  - 已订阅状态: `已订阅`, `Subscribed`
