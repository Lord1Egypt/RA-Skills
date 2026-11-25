# 常见问题与环境配置

> **何时读**：排障、配 TOKEN、查落盘路径或计费口径时再读。日常执行不必每次打开。

## 环境

- Node.js 16.14.0+，Windows / Linux / macOS；必需环境变量 `GUAIKEI_API_TOKEN`（16–256 位字母、数字、下划线或连字符）。
- Windows cmd：`set GUAIKEI_API_TOKEN=你的TOKEN`
- Windows PowerShell：`$env:GUAIKEI_API_TOKEN="你的TOKEN"`
- Linux/macOS：`export GUAIKEI_API_TOKEN=你的TOKEN`

## 合规

- 仅处理抖音公开数据；调用会把关键词/链接发送至第三方 API（ www.guaikei.com ）。
- 不上传本地文件、不登录、无写操作。数据仅限个人/团队内部分析，禁止违规分发。
- 更多帮助：[抖音数据获取技能官网](https://www.guaikei.com)

## FAQ

- **没结果**：放宽关键词或减少限定（`--time 0`），换更常用的词；空结果退出码是 0，属正常。
- **结果太多**：补场景/人群/品牌/时间/账号，并控制 `--limit`。
- **调用失败**：先看退出码——3 = token 问题；2 = 参数问题；1 = 关键词/链接/网络/服务端。完整码表见 [errors.md](errors.md)。
- **`Cannot find module`**：先 `cd` 到本技能目录（含 `SKILL.md` 的那一层），再执行 `node src/douyin/...`。
- **播放地址和分享链接有时效**，过期后需要重新获取。图文通常没有播放数和时长。
- **计费与单次上限**以官网说明为准。技能侧硬上限 10000 条/次（按量）；**包月**视频搜索/用户搜索/作品最多 30、评论最多 50，超限为 `PLAN_LIMIT`，不是网络故障。
- **账号安全**：只读能力，不登录/不发布/不点赞/不评论，无封号风险。
- **落盘**：搜索/用户搜索/作品/评论/详情写入 `logs/`；热榜不落盘。详见表与命名见仓库 `readme.md`。

口语化指令完整参数表：[options.md](options.md)。GitHub 默认展示与技术人员查阅见仓库根目录 `readme.md`。
