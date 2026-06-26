# URL 路由表与站点特殊处理

## URL 路由表

按域名/URL 模式匹配差异化提取策略。**匹配到时执行额外步骤,未匹配走默认流程。**

| URL 模式 | 自动 category | 额外提取 | 特殊处理 |
|----------|--------------|---------|---------|
| 内网域名(见下方清单) | `articles` | 标题、作者(如有) | **必须走 Chrome Relay**,见下方「内网文章收藏流程」 |
| `arxiv.org/abs/*` | `articles` | abstract、authors 列表、PDF 链接、subjects/categories | 标签自动加 `论文`;从 abs 页提取,不下载 PDF |
| `github.com/*/*`(repo 首页) | `articles` | stars、primary language、description、license、最近 commit 日期 | 提取 README 前 500 字作为正文摘要;区分 repo 页 vs 文件页(文件页走默认流程) |
| `mp.weixin.qq.com/*` | `wechat` | 公众号名称(`#js_name` 或 meta `og:site_name`) | 优先 browser 提取(见「站点选择器」) |
| `youtube.com/watch*` | `videos` | 频道名、时长、观看数 | 优先 Supadata transcript;Schema.org 通常有 VideoObject |
| `xiaohongshu.com/explore/*` 或 `xhslink.com/*`(视频类) | `videos` | 作者、点赞数 | `video_transcribe.sh` 本地转录(whisper);非视频笔记走默认流程 |
| `douyin.com/video/*` 或 `v.douyin.com/*` | `videos` | 作者、点赞数 | `video_transcribe.sh` 本地转录(whisper) |
| `x.com/*/status/*` | `tweets` | likes、retweets、replies、是否 thread | thread(连续 tweet)自动展开全部推文 |
| `news.ycombinator.com/item*` | `articles` | HN 得分、评论数、top 3 高赞评论 | **同时**抓取原文链接的内容(HN 页面本身只有讨论) |
| `substack.com/p/*` 或 `*.substack.com/p/*` | `articles` | 作者、发布日期、likes | Substack JSON-LD 通常完整 |
| `medium.com/*` 或 `*.medium.com/*` | `articles` | 作者、claps、reading time | 注意付费墙截断(见「站点选择器」) |

### 路由匹配逻辑
1. 按 URL 正则从上到下匹配,**首个命中**生效
2. 命中后执行「额外提取」列的步骤,**叠加**到默认流程上(不替代)
3. `自动 category` 列覆盖默认分类逻辑
4. 未命中任何规则 → 走默认 URL 内容流程,category 默认 `articles`

### 扩展方式
后续遇到新的高频站点,直接在表格中追加一行。无需改代码逻辑。

---

## 内网文章收藏流程

### 内网域名清单
```
*.alibaba-inc.com    # 阿里内网通用(含 ata.alibaba-inc.com / aone / done 等)
*.aliyun-inc.com     # 阿里云内网
*.alibaba.net        # 阿里内部
*.taobao.org         # 淘系内网
*.antfin.com         # 蚂蚁内网(含 yuque.antfin.com)
*.atatech.org        # ATA 技术博客(ata.atatech.org)
alidocs.dingtalk.com # 钉钉文档(阿里内部文档)
```

### 识别方式
1. clip 脚本自动检测:消息以 `[内网]` 开头
2. 手动发送:用户发内网 URL 时,agent 按域名匹配识别

### 收藏步骤
1. **不调用 web_fetch / supadata**(内网必失败,浪费时间和 credit)
2. **提示老板点 Chrome Relay**:
   > 📌 检测到内网链接,我需要通过你的浏览器读取内容。
   > 请确认当前 Tab 已打开这个页面,然后**点一下 Chrome Relay 按钮**(toolbar 上,badge 变 ON),我来提取。
3. **等老板确认**(老板说"好了"/"点了"/"OK" 等)
4. **通过 user 提取**:
   ```
   browser(action=snapshot, profile="user")
   ```
   获取页面正文内容
5. **正常走收藏流程**:提取标题/作者/正文 → 生成收藏文件 → 更新索引 → 同步 Obsidian
6. **提取完成后提醒老板**可以关掉 Relay(可选,不关也没事)

### 降级处理
- 老板不方便点 Relay → 仅保存 URL + 标题(从消息或老板口述获取),frontmatter 加 `incomplete: true`,正文加 `> ⚠️ 内网文章,正文待补充。下次在浏览器打开时可重新收藏。`
- user 提取正文 < 200 字 → 同上降级,可能是页面需要额外操作(如展开全文)

### 标签
内网文章自动加标签 `内网`、`阿里`。

---

## 站点选择器

当 `web_fetch` 提取结果残缺(正文 < 200 字)时,自动触发 `browser evaluate` + CSS 选择器精准提取。

| 站点 | 常见问题 | CSS 选择器 | 降级策略 |
|------|---------|-----------|---------|
| 内网域名(见清单) | 无外部访问权限 | 按页面结构判断 | **必须 Chrome Relay**,见「内网文章收藏流程」 |
| `mp.weixin.qq.com` | web_fetch 经常拿不到正文或格式混乱 | `#js_content` | Chrome Relay 打开原始页面提取 |
| `medium.com` | 付费墙截断,web_fetch 只拿到前几段 | `article section` | 仅保存可见部分,frontmatter 加 `incomplete: true`,标注"内容可能不完整(付费墙)" |
| `substack.com` | 部分文章需登录/付费 | `.post-content, .body` | web_fetch 通常可用;失败时同 medium 处理 |
| `36kr.com` | 反爬严重,web_fetch 可能返回空 | `.article-content` | browser 打开提取 |

### 触发条件
- `web_fetch` / `supadata` 返回的正文 **< 200 字**
- 或者正文明显是错误页(包含"请在微信客户端打开"/"Enable JavaScript" 等)
- 命中以上条件 → 自动尝试 browser 方案

### 降级原则
- 选择器提取失败 → **不阻塞收藏**
- 保存已有内容 + frontmatter 加 `incomplete: true`
- 收藏文件正文顶部加 `> ⚠️ 本文内容可能不完整,原始页面提取受限。`
