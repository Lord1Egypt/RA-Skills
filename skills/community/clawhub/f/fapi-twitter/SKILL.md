# fapi.uk Twitter 全能 API Skill（纯 REST 版）

**作者**：@good6_api  
**版本**：1.3.0  
**类别**：Social / Twitter / X / Grok / Communities  
**官网**：https://fapi.uk | https://utools.readme.io  
**文档**：https://utools.readme.io/reference

## 这是什么
这个 Skill 让小龙虾（OpenClaw）通过**自然语言**完整使用 fapi.uk 的 Twitter API（60+ 个真实接口）。  
**完全不需要 MCP**，小龙虾会自己阅读本文件，智能选择接口、组装参数、带上 apiKey + auth_token，发送请求，并用流畅中文总结结果。

**Base URL**：`https://fapi.uk/api/base/apitools/`

## 必须先完成一次设置（30 秒）
1. 打开 https://fapi.uk 或 https://utools.readme.io 用 **Twitter / Google** 一键登录
2. 在仪表盘生成 **API Key**（建议命名为 “OpenClaw 小龙虾”）
3. 在 OpenClaw 中设置（强烈推荐）：
   openclaw config set skills.entries.fapi-twitter.apiKey "你的完整apiKey"
   openclaw config set skills.entries.fapi-twitter.auth_token "你的auth_token（从登录API或 https://x.com/good6_api/status/1812496182213845482 获取）"
   openclaw config set skills.entries.fapi-twitter.ct0 "你的ct0（可选）"
或者直接在聊天里说：
“我的 fapi apiKey 是 xxx，我的 auth_token 是 yyy”

## 核心调用规则（小龙虾必须严格遵守）
1. **每次行动前** 先调用余额查询接口，检查积分是否足够
2. 所有请求 **必须** 带 Header：`Authorization: Bearer {{apiKey}}`
3. 大部分写操作需要 `auth_token` 和 `ct0` 参数
4. 积分不足时**立即停止**，回复用户并给出充值链接
5. 返回结果后，用**自然流畅的中文**总结关键信息，不要直接贴原始 JSON（用户要求“原始数据”时再给）
6. 支持 proxyUrl 参数（需要时可问用户要代理）

## 主要功能模块（小龙虾会自动选择对应接口）

### 1. 发推 / 互动（Send Tweets）
- createTweet / CreateNoteTweet（发推文、Note推文，支持 medias、richtext、reply）
- tweetReply（回复推文）
- createRetweet / deleteRetweet
- createBookmark / deleteBookmark
- unlikeTweet / unlikeV2
- uploadMedia / uploadMediaFile（上传图片/GIF/视频）

### 2. 获取推文（Get Tweets）
- tweetSimple / tweetTimeline（单条推文详情 + 回复）
- userTimeline / userTweetsV2 / UserArticlesTweets（用户推文）
- favoritesList / userLikeV2（喜欢列表）
- favoritersV2（推文点赞者）

### 3. 搜索 & 探索（Search）
- search（关键词搜索，支持高级运算符）
- trending / trends（热搜，需 woeid）
- explore / entertainment / sports（探索页、娱乐、体育）
- userTweetReply（用户回复）

### 4. 用户 & 关注（Users & Follows）
- uerByIdOrNameLookUp / userByScreenNameV2 / uerByIdRestIdV2 / usersByIdRestIds（查用户）
- blueVerifiedFollowersV2（蓝V粉丝）
- follow / unfollow
- blocksCreate / blocksDestroy（拉黑）
- accountAnalytics（账号数据）

### 5. Grok 专区（Grok Tools）
- createGrok（新建对话）
- addResponse / addResponsePost（向 Grok 发送消息，支持 reasoning、deepsearch、图片生成等）

### 6. 社区（Communities）
- CommunitiesFetchOneQuery / CommunityQueryV2
- CommunitiesMemberV2 / CommunitiesSearchV2
- CommunitiesTimelineV2 / CommunitiesTweetsTimelineV2
- TopicListV2

### 7. 其他实用
- get Notifications / mentionsTimeline
- DM 相关（uploadMediaDM）
- unlock（账号解锁，额外付费）
- tokenSync（速率限制恢复）
- usernameChanges / history 等

**余额查询**（每次必先调用）：
- 大部分接口返回 ResultT 结构，code=200 为成功

## 积分与付费提醒
- 每次调用都会从你的 fapi.uk 账户扣除积分（不同接口扣分不同）
- 小龙虾**绝不会自动购买积分**（OpenClaw 安全策略禁止）
- 积分不足时小龙虾会主动说：“积分不够啦～本次需要 X，当前剩余 Y，要我帮你打开 https://fapi.uk/pay 或 https://utools.readme.io/pay 充值页面吗？”

## 示例对话风格（小龙虾会模仿）
**用户**：帮我发一条推文：Grok 太强了！附上这张图  
**小龙虾**：好的～先查余额（当前 1247 积分，足够）。正在上传媒体并发推文... 发布成功！推文链接：https://x.com/xxx/status/1890123456789

**用户**：搜索最近关于 OpenClaw 的推文，前 10 条  
**小龙虾**：已搜索“OpenClaw”，找到最新 10 条，最热的总结如下：1. ... 要翻页吗？

**用户**：让我和 Grok 聊聊“未来 AI 发展趋势”  
**小龙虾**：已创建 Grok 会话，正在发送消息... Grok 回复：“......”

## 安装方式（一键安装）
```bash
npx clawhub@latest install fapi-twitter-full



## 积分与付费说明

- 每次调用 Twitter 接口会从你的 fapi.uk 账户扣除积分
- 积分不足此服务会返回 "You have made too many requests. Please contact the administrator to upgrade the frequency limit. "  
- **小龙虾不会自动购买积分**（OpenClaw 安全策略禁止自动支付）
- 积分不足时我会主动告诉你，并给出 https://fapi.uk/pay 充值链接
- 建议提前充值积分，避免中断
- 注意如果调用 MCP接口 使用自己的代理AI 配置 则只扣除1积分，否则MCP接口每次将会消耗100积分

## 如何设置 apiKey（只需做一次）
1. 登录 https://fapi.uk （支持 Twitter/Google 一键登录）
2. 前往 https://fapi.uk/api-keys 生成 Key , 并赠送100积分用于测试
3. 在 OpenClaw 里执行：
   `openclaw config set skills.entries.fapi-uk.apiKey "你的key"`
