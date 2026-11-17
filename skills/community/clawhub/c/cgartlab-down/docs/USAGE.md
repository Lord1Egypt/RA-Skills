# down — 使用文档

## 用户视角

对 Hermes Agent 说：
```
"下载 <URL>" 或 "down <URL>" 或 "把这个存下来：<URL>"
```

Agent 会：
1. 决定保存到哪儿（用户显式指定 → 环境偏好 → 临时目录兜底）
2. 探测 URL 是什么类型
3. 挑最小步骤的工具（curl / yt-dlp / aria2c）
4. 如果工具缺失，先问你装不装
5. 下载 + 验证 + 交付

## 用户视角的常见问题

**Q: 我为什么不能直接说"下载这个到 D:\Download"？**
你可以！如果你说"下载到 D:\Movies"，agent 会跳过环境偏好直接用那个路径。skill 里保存路径的解析是"用户显式指定 → 环境偏好 → 临时目录兜底"三级，前三级都是确定性的，所以不用问。

**Q: 为什么 agent 每次都要问装工具？**
防止静默改动系统。你可以回答"go"跳过确认，或者指定"以后这种就自动装"（会写入 memory）。

**Q: 我扔了个 Nitroflare 链接，为什么 agent 拒绝下载？**
因为那些站点有 JS 反爬，CLI 拿不到直链。agent 会如实说明并给你可选方案（手动浏览器、找同源镜像、放弃）。这是"特性"——skill 不假装能下载反爬站点。

## 开发者视角

### 环境准备

```bash
# Windows (git-bash) / Linux / macOS
cd D:/2-Area/github-repos/down
python --version  # 3.9+
```

### 运行单元测试

```bash
python -m unittest evals.test_detect -v
```

### 手工冒烟

```bash
# platform_video
python scripts/detect.py --url "https://x.com/HarrisDecodes/status/2107839872144900463/video/1"

# direct_file
python scripts/detect.py --url "https://example.com/video.mp4"

# magnet
python scripts/detect.py --url "magnet:?xt=urn:btih:abc123def&dn=test"

# unknown (resource aggregator)
python scripts/detect.py --url "https://alfafile.net/file/AXAFy"
```

### 添加新的平台站点

编辑 `scripts/detect.py` 顶部的 `PLATFORM_SITES` 字典：

```python
PLATFORM_SITES: dict[str, str] = {
    "youtube.com": "yt-dlp",
    # ...
    "mysite.com": "yt-dlp",  # 新增
}
```

同步更新：
- `references/detectors.md` 的白名单段落
- `evals/test_detect.py` 加一个测试用例

### 添加新的 kind

如果需要新的分类（比如 `podcast_feed`），改三处：
1. `scripts/detect.py` 的 `classify()` 加判定分支
2. `references/tool-matrix.md` 加能力边界
3. `references/detectors.md` 更新字段契约
4. `evals/test_detect.py` 加测试

## 项目结构

```
down/
├── SKILL.md              # 主入口（agent 加载用）
├── AGENTS.md             # 编码约定（改代码先读）
├── README.md             # 项目介绍
├── CHANGELOG.md          # 变更日志
├── LICENSE               # MIT
├── docs/
│   └── USAGE.md          # 本文件
├── scripts/
│   └── detect.py         # URL 探测器（stdlib only）
├── references/
│   ├── tool-matrix.md    # 工具选择规则
│   ├── detectors.md      # detect.py 契约
│   ├── commands.md       # 命令配方
│   └── anti-bot.md       # 反爬识别
├── evals/
│   ├── __init__.py
│   └── test_detect.py    # 单元测试（stdlib unittest）
└── assets/templates/     # 回复模板（v0.1 空）
```
