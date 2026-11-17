# down — 万能下载 skill

分析任何 URL，用最少的步骤把它落到本地。**只使用当前环境已装工具**，任何安装动作必须先询问用户批准。

## 这是什么

Agent Skill（本仓库根目录 `SKILL.md`）。用户扔 URL 过来时激活：
1. **确定保存路径**（用户显式指定 → 环境偏好 → 临时目录兜底；skill 不硬编码默认路径）
2. **探测 URL 类型**（platform_video / direct_file / torrent / magnet / unknown）
3. **选最小步骤工具**（curl → yt-dlp → aria2c 优先级）
4. **安装缺失工具前先问**（不静默装）
5. **验证 + 回复**（ffprobe/file/sha256sum 数字写进回复）

## 三条不可让渡的规则

1. **不静默安装**：任何工具缺失时先展示"要装什么、多大多、怎么装"，等"go"再装。
2. **最小步骤**：能用 curl 解决的不上 yt-dlp；能用 yt-dlp 解决的不上 aria2。
3. **验证才算完成**：ffprobe/file/sha256sum 出真实数字，不凭退出码声称成功。

## 目录结构

```
down/
├── SKILL.md               # 主入口（agent 加载后按此执行）
├── AGENTS.md              # 本仓库编码约定（改代码先读）
├── README.md              # 本文件
├── CHANGELOG.md           # 变更日志
├── scripts/
│   └── detect.py          # URL 探测器：URL → JSON 分类
├── references/
│   ├── tool-matrix.md     # 工具选择规则与能力边界
│   ├── detectors.md       # detect.py 契约与判定逻辑
│   ├── commands.md        # curl/yt-dlp/aria2c 命令配方
│   └── anti-bot.md        # 反爬站点识别与降级
├── evals/
│   └── test_detect.py     # detect.py 单元测试（stdlib unittest）
├── docs/
│   ├── USAGE.md           # 用户使用文档
│   └── PLAN-v0.2.md       # v0.2 开发计划（单一真源）
└── assets/templates/      # 回复模板（v0.1 空，v0.2 补）
```

## 快速上手

在 Hermes Agent 里：
```
用户："帮我下载 https://x.com/foo/status/123/video/1"
agent：（加载本 skill）
        1. 按三级优先级确定保存路径（用户显式指定 → 环境偏好 → 临时目录兜底，不询问）
        2. python scripts/detect.py --url <url>  → kind=platform_video, tool=yt-dlp
        3. 检查 yt-dlp 是否装了：yt-dlp --version
        4. 若缺失 → 询问用户"装不装"
        5. 装 → 执行 yt-dlp 命令
        6. ffprobe 验证
        7. 回复 MEDIA: + 规格摘要
```

## 与旧 skill `file-download` 的关系

`file-download` 是老版本，硬编码 `D:\Download`、假设 yt-dlp 存在、不覆盖 torrent/magnet。
本 skill 是**正式替代**：
- 保存路径按三级优先级解析（用户显式指定 → 环境偏好 → 临时目录兜底，不询问）
- 工具安装强制询问
- 覆盖 torrent/magnet（新增）
- 保留 X/Twitter 最佳实践（`--no-playlist`、`http-*` 格式优先等）

加载本 skill 后，新的下载请求应走 `down`，不走 `file-download`。

## 依赖

- **必需**：`curl`（Windows/git-bash 自带）、`python`（3.9+）
- **可选**：`yt-dlp`（视频平台）、`aria2c`（torrent/magnet）
- **验证**：`ffprobe`（Hermes 自带）、`file`（POSIX 自带）、`sha256sum`（`coreutils`）

## 版本

- **v0.2.0**（2026-10-11）：能力边界明确化（skill 不做什么）。新增 `scripts/check_tools.py`（工具检查）和 `scripts/proxy_chain.py`（代理链解析）。detect.py 加 `cloud_drive` kind（10 个网盘）、`.torrent`→curl、magnet→none、`user_action`/`reason` 字段、`dest_name` 路径净化。SKILL.md 加 6 个新章节（能力边界 / Phase 2.5 代理兜底 / Phase 3.0 文件名冲突 / 网盘处理 / Magnet 处理 / 平台视频失败应对）。`references/commands-windows.md`（PowerShell 命令模板）。测试 15→58 用例。
- **v0.1.0**（2026-10-10）：初版骨架。SKILL.md + detect.py + references + evals。

## License

MIT — 见仓库根 `LICENSE`（TODO v0.2 补）。
