# 各平台 Settings 完整字段参考

发布时 `postAccounts[].settings` 的完整字段定义。每个 settings 内部不同平台、不同内容类型的字段不同。

> 发布前优先读取 `references/platform-rules/<platform>.md`。该目录按平台拆分了文章/图文/视频、封面、必填/推荐 settings 和不要传的字段；本文件保留为聚合字段参考。

## 通用子对象

### TimerPublish（定时发布）

| 字段 | 类型 | 说明 |
|------|------|------|
| enable | bool | 是否启用定时发布 |
| timer | string | 定时时间，格式 `"YYYY-MM-DD HH:MM:SS"` |

---

## wechat 微信公众号

### 文章/图文

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| author | string | — | 作者 |
| link | string | — | 原文链接 |
| leave | bool | — | 开启留言，默认 true |
| origin | bool | — | 声明原创，默认 false |
| reprint | bool | — | 快捷转载，origin=true 时可设置 |
| publishType | string | — | `"mass"` 群发 / `"publish"` 发布 |
| collection | string | — | 合集 |
| source | uint | — | 0 不声明,1 AI生成,2 官方媒体,3 剧情演绎,4 个人观点,5 健康分享,6 投资观点,7 无需声明 |
| timerPublish | TimerPublish | — | 当前+5分钟 ~ 7天 |

### 视频（继承上述全部，额外增加）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| materTitle | string | — | 素材标题 |
| barrage | bool | — | 弹幕 |
| barrageCheck | uint | — | 弹幕权限：0 所有,1 已关注,2 关注7天+ |
| turn2Channel | bool | — | 发表后转为视频号视频 |
| adTrans | uint | — | 广告过渡：0~6 |

---

## wechat-video 微信视频号

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| location | string | — | 位置，默认 `"auto"` |
| collection | string | — | 合集 |
| linkType | uint | — | 0 不设置,1 公众号文章,2 红包封面 |
| linkAddr | string | — | 链接地址 |
| music | string | — | 音乐 |
| activity | string | — | 活动 |
| origin | bool | — | 声明原创（仅视频，仅账号已开通时生效） |
| timerPublish | TimerPublish | — | 定时发布 |

---

## douyin 抖音

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| activity | string | — | 活动奖励 |
| music | string | — | 音乐 |
| label | string | — | 标签 |
| location | string | — | 位置/商品 |
| hotspot | string | — | 关联热点 |
| collection | string | — | 合集 |
| allowSave | bool | — | 允许他人保存，默认 true |
| lookScope | uint | — | 0 公开,1 好友,2 自己 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## toutiaohao 今日头条

### 文章

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| location | string | — | 位置 |
| placeAD | bool | — | 投放广告 |
| starter | bool | — | 头条首发 |
| collection | string | — | 合集（设了合集不能定时） |
| syncPublish | bool | — | 同时发布微头条 |
| source | uint | — | 0 不声明,1 取材网络,3 个人观点,4 引用AI,5 虚构演绎,6 投资观点,7 健康分享 |
| timerPublish | TimerPublish | — | 当前+2小时 ~ 7天 |

### 图文（继承文章全部，额外增加）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openBgm | bool | — | 开启配乐 |

### 视频（独立结构）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gtEnable | bool | — | 视频生成图文 |
| gtSyncPub | bool | — | 生成图文同时发布 |
| collection | string | — | 合集 |
| stickers | array | — | 互动贴纸 |
| source | uint | — | 0 不声明,1 站外,3 自拍,4 AI,5 虚构,6 投资,7 健康 |
| link | string | — | 扩展链接 |
| lookScope | uint | — | 0 公开,1 粉丝,2 自己 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## xiaohongshu 小红书

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| location | string | — | 位置 |
| collection | string | — | 合集 |
| group | string | — | 群聊 |
| mark | object | — | `{"user":true,"search":"关键词"}` user=true 标记用户,false 标记地点 |
| origin | bool | — | 声明原创 |
| source | uint | — | 0 不声明,1 虚构演绎,2 AI合成,3 自主标注,4 自主拍摄,5 来源转载 |
| reprint | string | — | source=5 时的来源媒体 |
| lookScope | uint | — | 0 公开,1 好友,2 自己 |
| timerPublish | TimerPublish | — | 定时发布，当前+1小时 ~ 14天 |

### 保存/发布规则

- 保存草稿点击 `button "暂存离开"`；当前客户端会记录 `[xiaohongshu.SaveDraft]` 步骤日志，Windows 偶发闪退时优先查看 `%USERPROFILE%\.96Push\panic.log`。
- 发布点击 `button "发布"`；定时发布点击 `button "定时发布"`。
- `origin=true` 时不能同时使用 `source=5` 来源转载。
- 如果要调试保存/发布接口响应，先捕获 `creator.xiaohongshu.com` 下和 `/api/galaxy/creator/note` 相关的 POST 响应，再补等待逻辑。

---

## kuaishou 快手

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| music | string | — | 音乐（仅图文） |
| linkApplet | string | — | 小程序链接 |
| source | uint | — | 0 不声明,1 AI生成,2 演绎情节,3 个人观点,4 素材来源网络 |
| collection | string | — | 合集 |
| location | string | — | 位置 |
| sameFrame | bool | — | 允许拍同框，默认 true |
| download | bool | — | 允许下载，默认 true |
| sameCity | bool | — | 同城页展示，默认 true |
| lookScope | uint | — | 0 公开,1 好友,2 自己 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## bilibili 哔哩哔哩

### 视频/图文

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reprint | string | — | 转载来源，空=自制 |
| partition | string | — | 分区 |
| creation | bool | — | 允许二创 |
| public | bool | — | 公开可见 |
| source | uint | — | 1 AI合成,2 危险行为,3 仅供娱乐,4 引人不适,5 适度消费,6 个人观点 |
| dynamic | string | — | 粉丝动态 |
| timerPublish | TimerPublish | — | 定时发布 |

### 文章

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | — | 专栏分类 |
| origin | bool | — | 声明原创 |
| headerImg | string | — | 头图 URL |
| labels | string | — | 标签，最多10个 |
| collection | string | — | 合集 |
| public | bool | — | 公开可见 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## zhihu 知乎

### 文章/图文

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| question | string | — | 投稿至问题；会搜索并选择第一个可选问题 |
| source | uint | — | 创作声明：0 无声明,1 包含剧透,2 包含医疗建议,3 虚构创作,4 包含理财内容,5 包含 AI 辅助创作 |
| topic | string | — | 文章话题，最多 3 个，`/` 分割 |
| collection | string | — | 专栏；为空表示不发布到专栏 |
| origin | uint | — | 内容来源：0 不设置,1 官方网站,2 新闻报道,3 电视媒体,4 纸质媒体 |

#### 保存/发布规则

- 文章草稿主要依赖知乎自动保存；保存草稿会监听非 GET 的 `/api/articles/drafts`，并主动 blur 当前编辑器触发保存。
- 发布会监听 `POST /content/publish`；知乎可能出现二次确认发布按钮，发布动作会尝试二次点击。
- 接口返回 `error.message`、非 0 `code` 或 `success=false` 时按发布失败处理。

### 视频（继承上述，额外增加）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | 推荐 | 领域分类；前端表单要求选择 |
| reprint | bool | — | true=转载, false=原创；前端默认 true |
| timerPublish | TimerPublish | — | 定时发布，当前+1小时 ~ 14天 |

---

## baijiahao 百家号

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| watermark | uint8 | — | 水印（仅视频）：0 不加,1 水印,2 贴片 |
| location | string | — | 位置 |
| classify | string | — | 分类 `"一级/二级"` 或 `"一级/二级/三级"` |
| activity | string | — | 活动 |
| byAI | bool | — | AI创作声明 |
| timerPublish | TimerPublish | — | 当前+1小时 ~ 7天 |

---

## csdn CSDN

### 文章

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string | — | 标签，`/` 分割，最多7个 |
| collection | string | — | 分类专栏，`/` 分割，最多3个 |
| artType | uint | — | 0 原创,1 转载,2 翻译 |
| originLink | string | 转载必填 | 原文链接 |
| backupGitCode | bool | — | 备份到 GitCode |
| lookScope | uint | — | 0 全部,1 自己,2 粉丝,3 VIP |
| activity | string | — | 活动 |
| topic | string | — | 话题 |
| timerPublish | TimerPublish | — | 当前+4小时 ~ 7天 |

### 视频

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| labels | string | — | 标签，`/` 分割，最多3个 |
| recommend | bool | — | 是否推荐 |

---

## juejin 掘金

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | — | 分类 |
| tag | string | **Yes** | 标签（必填） |
| collection | string | — | 专栏 |
| topic | string | — | 话题 |
| group | string | — | 沸点圈子 |
| link | string | — | 沸点链接 |

---

## sina 新浪微博

### 视频/图文

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | uint | — | 0 原创,1 二创,2 转载 |
| classify | string | — | `"栏目/分类"` |
| stress | bool | — | 允许画重点，默认 true |
| location | string | — | 位置 |
| wait | int | — | 等待 X 秒后发布 |
| （继承文章全部字段） | | | |

### 文章

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| collection | string | — | 专栏 |
| onlyFans | bool | — | 仅粉丝阅读全文，默认 true |
| lookScope | uint | — | 0 公开,1 粉丝 |
| source | uint | — | 0 不声明,1 AI生成,2 虚构演绎 |
| dynamic | string | — | 粉丝动态 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## jianshuhao 简书

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| collection | string | — | 文集 |
| vetoReprint | bool | — | 禁止转载 |

---

## omtencent 腾讯内容开放平台

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | — | 分类 |
| labels | string | — | 标签，`/` 分割；最多 9 个，每个最多 8 字 |
| activity | string | — | 活动 |
| source | uint | — | 内容自主声明：1 该内容由AI生成,2 剧情演绎，仅供娱乐,3 取材网络，谨慎甄别,4 个人观点，仅供参考,5 旧闻；为空或 0 时默认使用 4 |
| timerPublish | TimerPublish | — | 定时发布，当前+5分钟 ~ 7天 |

### 保存/发布规则

- 保存草稿监听 `POST /marticlepublish/omSave`、`/marticlepublish/omBatchSave` 或 `/editorCache/update`。
- 发布监听 `POST /marticlepublish/omPublish` 或 `/marticlepublish/omBatchPublish`；定时发布监听 `/marticlepublish/omSchedulePublish` 或 `/marticlepublish/omBatchPublish`。
- 平台出现“人工智能生成合成内容标识办法”弹窗时会先点“提交”，再重新点击保存/发布。
- 发布按钮若带 `disabled` 或 `aria-disabled=true`，按平台发文上限错误处理。

---

## acfun A站

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | — | 分区 `"一级/二级"` |
| labels | string | — | 标签，最多5个 |
| origin | bool | — | true=原创, false=转载 |
| reprint | string | — | 转载来源 |
| dynamic | string | — | 粉丝动态 |
| timerPublish | TimerPublish | — | 当前+4小时 ~ 14天 |

---

## pinduoduo 拼多多

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | string | — | 商品ID |
| source | uint | — | 0 不声明,1 AI,2 取材网络,3 引人不适,4 虚构演绎,5 危险行为 |
| timerPublish | TimerPublish | — | 当前+4小时 ~ 7天 |

---

## weishi 微视

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source | uint | — | 0 不声明,1 AI,2 剧情演绎,3 个人观点,4 取材网络 |
| lookScope | uint | — | 0 公开,1 自己 |
| timerPublish | TimerPublish | — | 定时发布 |

---

## sohuhao 搜狐号

### 文章/图文/视频

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| classify | string | — | 属性：观点评论/故事传记/消息资讯/八卦爆料/经验教程/知识科普/测评盘点/见闻记录/运势/搞笑段子/美图/美文 |
| declaration | uint8 | — | 信息来源：0 无特别声明,1 引用声明,2 包含AI创作内容,3 包含虚构创作 |
| topic | string | — | 话题关键词，留空则不设置 |
| loginView | bool | — | 可见范围：true=必须登录才能查看全文，默认 false |
| timerPublish | TimerPublish | — | 当前+1小时~7天 |

### 封面图片

- **手动封面**: `autoThumb=false` + `thumb` 提供封面 URL → 自动上传到搜狐号
- **自动提取**: `autoThumb=true` + 文章内含图片 → 搜狐号自动从正文提取
- **无封面**: 搜狐号**允许**无封面发布，不强制要求

### 数据同步 (ListenFeature / WatchNum)

- **ListenFeature**: 监听 `/mpbp/bp/*/publish` 和 `/mpbp/bp/*/draft` API 响应，从 `data` 字段捕获文章数字 ID 作为 `platFeature`
- **WatchNum**: 使用 HTTP 模式，通过 `https://www.sohu.com/a/{articleID}_{accountID}` 构造真实 URL 并验证可访问性
- **accountID**: 登录时从 `/account/check/user?accountId=xxx` URL 提取并存储在 `account.Account` 字段
