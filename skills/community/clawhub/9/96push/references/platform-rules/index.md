# 平台规则索引

发布前先根据目标账号的平台读取对应文件：`python3 scripts/96push.py rules --platform <平台> --type <article|graph_text|video>`。

| 平台键 | 名称 | 支持类型 | 规则文件 | 重点 |
| --- | --- | --- | --- | --- |
| `wechat` | 微信公众号 | article, graph_text | `wechat.md` | 文章封面必备，`publishType` 影响群发/发布 |
| `wechat-video` | 微信视频号 | graph_text, video | `wechat-video.md` | 视频号链接、原创、定时等字段独立 |
| `douyin` | 抖音 | graph_text, video | `douyin.md` | `files` 是内容，封面可自动或手动 |
| `toutiaohao` | 今日头条 | article, graph_text, video | `toutiaohao.md` | 文章封面建议 1/3 张 JPEG/PNG，定时最早 +2h |
| `kuaishou` | 快手 | graph_text, video | `kuaishou.md` | 默认允许同框/下载/同城，按需显式关 |
| `xiaohongshu` | 小红书 | graph_text, video | `xiaohongshu.md` | `origin=true` 不能和 `source=5` 混用 |
| `omtencent` | 腾讯内容开放平台 | article, video | `omtencent.md` | 标签最多 9 个，每个最多 8 个汉字 |
| `weishi` | 微视 | video | `weishi.md` | 无草稿能力，别伪装草稿成功 |
| `bilibili` | 哔哩哔哩 | article, video | `bilibili.md` | 视频 `partition` 很重要，文章标签最多 10 个 |
| `baijiahao` | 百家号 | article, graph_text, video | `baijiahao.md` | 文章/视频封面容易成为硬失败 |
| `sohuhao` | 搜狐号 | article, graph_text, video | `sohuhao.md` | 允许无封面，分类值要用平台枚举 |
| `wangyihao` | 网易号 | article | `wangyihao.md` | 文章封面自动/单图/三图，视频暂不对最终用户开放 |
| `jianshuhao` | 简书 | article | `jianshuhao.md` | 文集和禁止转载是主要 settings |
| `zhihu` | 知乎 | article, graph_text, video | `zhihu.md` | 文章话题最多 3 个，视频推荐 `classify` |
| `pinduoduo` | 拼多多 | video | `pinduoduo.md` | 商品 ID 和声明按内容需要补 |
| `juejin` | 掘金 | article, graph_text | `juejin.md` | `tag` 必填 |
| `tiktok` | TikTok | video | `tiktok.md` | 品牌内容、AIGC、可见范围有互斥限制 |
| `csdn` | CSDN | article, video | `csdn.md` | 转载文章 `originLink` 必填 |

本目录只保留 `platform.json` 里 `status=2` 的已启用平台。开发中或已禁用平台若没有规则文件，不要猜测 settings 发布。
