# 抖音内容引擎 完整选项参数说明

## 🔎 抖音关键词搜索

| 参数         | 缩写 | 作用         | 可选值                                                 | 必填 | 默认值 |
| :----------- | :--: | :----------- | :----------------------------------------------------- | :--- | :----: |
| `--keyword`  | `-k` | 搜索关键词   | 2-50 位长度的字符或单词                                | 是   |        |
| `--sort`     | `-s` | 排序方式     | 0 = 综合排序 / 1 = 最多点赞 / 2 = 最新发布             | 否   |   0    |
| `--time`     | `-t` | 时间范围     | 0 = 全部 / 1 = 一天内 / 7 = 七天内 / 180 = 半年内      | 否   |   0    |
| `--duration` | `-d` | 视频时长     | 0 = 不限 / 1 = 1分钟以下 / 2 = 1-5分钟 / 3 = 5分钟以上 | 否   |   0    |
| `--content`  | `-c` | 内容类型     | 0 = 不限 / 1 = 视频 / 2 = 图文                         | 否   |   0    |
| `--limit`    | `-l` | 获取数量     | 1-10000 条（**包月 Token 实际最多 30**）               | 否   |   10   |
| `--help`     | `-h` | 显示帮助信息 |                                                        | 否   |        |

```bash
# **基础语法**
node src/douyin/search-cli.js --keyword <关键词> --sort <排序方式> --time <时间范围> --duration <视频时长> --content <内容类型> --limit <获取数量>

# **使用示例**

# 搜索"AI 教程"的抖音内容
node src/douyin/search-cli.js --keyword "AI 教程"

# 搜索 AI 获取最多点赞的抖音内容
node src/douyin/search-cli.js --keyword "AI" --sort 1

# 搜索近7天"AI 模型"的抖音内容
node src/douyin/search-cli.js --keyword "AI 模型" --time 7

# 搜索"AI 教程"视频时长在5分钟以上的抖音内容
node src/douyin/search-cli.js --keyword "AI 教程" --duration 3

# 搜索半年内最新20条"AI 教程"的抖音内容
node src/douyin/search-cli.js --keyword "AI 教程" --sort 2 --time 180 --limit 20
```

> **套餐双上限**：技能硬上限 10000（按量）。包月 Token 超限返回 `PLAN_LIMIT`：视频搜索/用户搜索/作品 ≤30，评论 ≤50。详情与热榜无此条数限制。

## 👤 抖音用户搜索

按关键词搜用户/达人/账号。搜视频/图文请用上方关键词搜索；已有主页链接请用博主作品命令。暂不支持粉丝量/认证类型筛选。

| 参数         | 缩写 | 作用         | 可选值                                   | 必填 | 默认值 |
| :----------- | :--: | :----------- | :--------------------------------------- | :--- | :----: |
| `--keyword`  | `-k` | 用户搜索关键词 | 2-50 位长度的字符或单词                | 是   |        |
| `--limit`    | `-l` | 获取数量     | 1-10000 条（**包月 Token 实际最多 30**） | 否   |   10   |
| `--help`     | `-h` | 显示帮助信息 |                                          | 否   |        |

```bash
# **基础语法**
node src/douyin/user-search-cli.js --keyword <关键词> --limit <获取数量>

# **使用示例**

# 按关键词找 AI 相关账号
node src/douyin/user-search-cli.js --keyword "AI"

# 找美妆达人，取 20 条
node src/douyin/user-search-cli.js --keyword "美妆达人" --limit 20
```

成功时 `results` 为用户数组，字段含 `sec_uid`、`nickname`、`avatar`、`fans`、`like`、`publish_cnt`；有 `sec_uid` 时含 `author_url`。可用 `author_url` / `sec_uid` 衔接 `post-cli.js`。

## 🦸 抖音博主作品获取

| 参数      | 缩写 | 作用                     | 可选值     | 必填 | 默认值 |
| :-------- | :--: | :----------------------- | :--------- | :--- | :----: |
| `--url`   | `-u` | 抖音博主主页URL或sec_uid |            | 是   |        |
| `--limit` | `-l` | 获取作品数量             | 0-10000 条（**包月最多 30**；0 = 只要博主互动数据） | 否   |   10   |
| `--help`  | `-h` | 显示帮助信息             |            | 否   |        |

> **💡"抖音博主主页URL"说明**
>
> - PC端 ( 格式：<https://www.douyin.com/user/MS4wLjABxxx> )
> - 移动端 ( 格式：<https://v.douyin.com/xxx> )
> - 技能关键词搜索返回的 `author_sec_uid`，或用户搜索返回的 `sec_uid` / `author_url`

```bash
# **基础语法**
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"

# **使用示例**

# 获取抖音博主 MS4wLjABxxx 已发布的20条作品
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 20

# 获取抖音博主 MS4wLjABxxx 的互动数据（关注数、粉丝数、总获赞数）等信息。
node src/douyin/post-cli.js -u "https://www.douyin.com/user/MS4wLjABxxx" -l 0
```

## 💬 抖音作品评论数据

| 参数      | 缩写 | 作用                          | 可选值     | 必填 | 默认值 |
| :-------- | :--: | :---------------------------- | :--------- | :--- | :----: |
| `--url`   | `-u` | 抖音视频(或图文)URL或aweme_id |            | 是   |        |
| `--limit` | `-l` | 获取评论数量                  | 1-10000 条（**包月最多 50**） | 否   |   10   |
| `--help`  | `-h` | 显示帮助信息                  |            | 否   |        |

> **💡 评论链接说明**
>
> - 视频 ( 格式：<https://www.douyin.com/video/xxx> )
> - 图文 ( 格式：<https://www.douyin.com/note/xxx> )
> - 短链 ( 格式：<https://v.douyin.com/xxx> )
> - 纯数字 aweme_id

```bash
# **基础语法**
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"

# **使用示例**

# 获取视频 xxx 的100条评论
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 100
```

## 📄 抖音作品详情

一条视频或图文的文案、互动、作者和播放地址。不取评论，也不取博主作品列表。

| 参数     | 缩写 | 作用                          | 可选值 | 必填 | 默认值 |
| :------- | :--: | :---------------------------- | :----- | :--- | :----: |
| `--url`  | `-u` | 抖音视频(或图文)URL或aweme_id |        | 是   |        |
| `--help` | `-h` | 显示帮助信息                  |        | 否   |        |

> **💡 详情链接说明**
>
> - 视频 ( 格式：<https://www.douyin.com/video/xxx> )
> - 图文 ( 格式：<https://www.douyin.com/note/xxx> )
> - 短链 ( 格式：<https://v.douyin.com/xxx> )
> - iesdouyin 分享链（`/share/video/`、`/share/note/`）
> - 纯数字 aweme_id

```bash
# **基础语法**
node src/douyin/detail-cli.js --url "https://www.douyin.com/video/xxx"

# **使用示例**

# 获取视频 xxx 的详情
node src/douyin/detail-cli.js --url "https://www.douyin.com/video/xxx"
```

## 📡 抖音热搜榜单

- 无需参数

```bash
# **基础语法**
node src/douyin/hot-cli.js
```
