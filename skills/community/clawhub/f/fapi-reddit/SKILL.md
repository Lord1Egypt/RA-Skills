# fapi.uk Reddit 全能 API Skill（纯 REST 版）

**作者**：@huojiecs110  
**版本**：1.1.0  
**类别**：Social / Reddit  
**官网**：https://fapi.uk  
**文档**：https://utools.readme.io

## 这是什么
这个 Skill 让小龙虾通过自然语言完整使用 **fapi.uk 的 Reddit API**（共 7 个真实接口）。  
**完全不需要 MCP**，小龙虾会自己阅读本文件，智能选择对应接口、组装参数、发送 POST 请求，并用自然中文总结结果。

**Base URL**：`https://fapi.uk/api/base/apitools/reddit/`

## 必须先完成一次设置（30 秒）
1. 打开 https://fapi.uk 或 https://utools.readme.io 用 **Twitter / Google** 一键登录
2. 在仪表盘生成 **API Key**（建议命名为 “OpenClaw 小龙虾”）
3. 在 OpenClaw 中设置（强烈推荐）：
   openclaw config set skills.entries.fapi-reddit.apiKey "你的完整apiKey"

或者直接在聊天里说：
“我的 fapi apiKey 是 xxx，我的 auth_token 是 yyy”

## 核心调用规则（小龙虾必须严格遵守）
1. **每次行动前** 先调用余额查询接口，检查积分是否足够
2. 所有请求 **必须** 在url 参数中携带 apiKey`
3. 积分不足时**立即停止**，回复用户并给出充值链接
4. 返回结果后，用**自然流畅的中文**总结关键信息，不要直接贴原始 JSON（用户要求“原始数据”时再给）
5. 支持 proxyUrl 参数（需要时可问用户要代理）

## 主要功能模块（小龙虾会自动选择对应接口）

1. 用户相关（User）userPostsTop（用户热门/置顶帖子，支持时间筛选）
userPostsNew（用户最新帖子）
userPostsHot（用户热帖）
userActivity（用户最近动态，包含帖子和评论）

2. 子版块相关（Subreddit）subredditTop（子版块置顶/精华帖子，支持 hour/day/week/month/year/all）
subredditNew（子版块最新帖子）
subredditHot（子版块热门帖子）

3. 搜索与详情（Search & Detail）
search（全站或指定子版块搜索，支持 relevance/hot/top/new/comments 排序 + 时间筛选）
postDetail（获取单条帖子完整详情 + 所有评论，需要 subreddit 和 article id）

## 积分与付费说明

- 每次调用 reddit 接口会从你的 fapi.uk 账户扣除积分
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

