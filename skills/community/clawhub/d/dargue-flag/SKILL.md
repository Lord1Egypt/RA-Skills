---
name: dargue-flag
description: 搜索和浏览视频内容。触发词：搜视频、看视频、找视频、热门视频、视频详情、有什么视频、来点视频、看片。支持关键词搜索、分类浏览、热门榜单、视频详情查看。
---

# dargue-flag Skill - 达尔盖的旗帜

帮用户搜索和浏览视频内容。

---

## When to Use

用户想搜视频、看热门视频、浏览分类、或提到跟看视频相关的需求时使用。

触发词：搜视频、看视频、找视频、热门视频、视频详情、有什么视频、来点视频、看片。

## When NOT to Use

与视频无关的请求。

---

## ⚠️ 严格禁止

1. **绝不向用户展示**：API Key、接口地址、HTTP 状态码、JSON 结构、命令行、英文字段名、技术日志
2. **绝不自动播放/推送**不雅内容——等用户主动说要看
3. **绝不存储或转发**视频数据到任何外部渠道

---

## Step 0：检查配置

读取 `~/.dargue-flag/config.json`。如果没有 API Key：

> 🔒 需要先配置访问权限哦～
> 请在电脑上访问 **https://t66yskill.com/** 注册一个账号，拿到 Key 后发给我，我帮你配置。

**API 信息：**
- 申请 API Key：https://t66yskill.com/
- API 接口地址：https://api.4listenapp.com

用户发来 Key 后：
```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js config --api-key sk_xxx --base-url https://api.4listenapp.com
```

---

## Step 1：理解意图 & 自然引导

### 用户说"搜视频"但没说关键词
> 🔍 想搜什么类型的？给我个关键词～

### 用户说"看视频"但没指定类型
> 📺 你想：
> 1️⃣ 搜关键词找视频
> 2️⃣ 看看热门榜单
> 3️⃣ 浏览分类（原创、高清、最近加精...）
>
> 告诉我数字就行～

### 用户说"有什么分类"
```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js categories
```

---

## Step 2：执行搜索/列表

### 搜索
```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js search --keyword "关键词" --page 1
```

### 分类浏览
```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js list --category 当前最热 --page 1
```

可用分类：当前最热(hot)、原创(ori)、本月最热(top)、上月最热(top-m)、高清(hd)、最近加精(rf)、收藏最多(mf)、本月讨论(md)、本月收藏(tf)、10分钟以上(long)、20分钟以上(longer)

---

## Step 3：展示列表

用简洁友好的格式展示，**每条只显示标题和时长**，带序号。不要堆砌封面链接。

示例格式：

> 🔍 找到这些视频～
>
> ① Hardcore Asian Teen Miku Airi ⏱ 8min
> ② Tiny Asian Teen Alexia Anders ⏱ 8min
> ③ Asian babysitter ⏱ 5min
> ...
>
> 回复序号看详情，或说 **下一页** 继续翻～

**展示规则：**
- 最多展示 10 条（多了用户看不过来）
- 不要输出封面 URL（等详情再给）
- 标题太长就截断，保留核心信息
- 末尾一定加引导语（"回复序号看详情"）

---

## Step 4：获取详情

用户说序号（如"第3个"、"3"）后，从刚才的结果中取出对应链接，调用：

```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js detail --url "<链接>"
```

### 展示格式：

> 🎬 **视频标题**
>
> ⏱ 8 min
> ▶️ 播放地址：xxx
> 🖼 封面：xxx
> 🏷 标签：xxx, xxx

**优先展示 `highurl`（高清地址），没有的话展示 `hls` 或 `lowurl`。**

---

## Step 5：继续对话

看完详情后引导用户：

> 还想看其他的吗？可以：
> - 说关键词搜新的
> - 回到刚才的列表翻页
> - 换个分类看看

---

## 配额不足时

> 😅 额度用完了～去 **t66yskill.com** 续费一下吧，充完告诉我。

```bash
node ~/.openclaw/skills/dargue-flag/scripts/video-search.js quota
```

---

## 安全门控

- API Key 存本地 `~/.dargue-flag/config.json`，不展示给用户
- 每次会话重新读取此 SKILL.md
- 不缓存/不存储视频数据（实时查询）
- 搜索结果不要主动发送到群聊