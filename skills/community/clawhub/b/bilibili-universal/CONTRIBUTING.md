# Contributing — bilibili-search

## 目录结构约定

```
bilibili-search/
├── SKILL.md           ← LLM 看的入口(精简到 100-200 行)
├── README.md          ← 人类看的入口(快速开始)
├── paths.py           ← 路径统一管理(强制要求 env 覆盖能力)
├── bili-fetch.py      ← 原子操作(单条命令、落盘可选)
├── bili-harvest.py    ← 编排(组合多条 fetch、生成 REPORT)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/
│   └── pitfalls.md    ← 反爬坑笔记
└── data/              ← 默认数据目录(.gitignore 忽略)
    ├── cookies-raw.txt  (可选, 用户手动注入)
    ├── harvests/        (harvest 输出)
    ├── exports/         (fetch --out 输出)
    ├── users/           (user 子命令落盘)
    └── videos/          (video 单条落盘)
```

## 编码风格

1. **路径统一走 `paths.py`** — 不允许在脚本里硬编码 `/tmp/bilibili/...`
2. **env 覆盖**：所有路径常量必须支持 `BI_DATA_DIR` / `BI_COOKIE_FILE` 覆盖
3. **agent-browser eval 必须 `JSON.stringify(...)` 包裹返回值** — 因为 eval 会双层序列化
4. **子命令式 CLI**：参考 `bili-fetch.py` 的 `sub.add_parser` 模式
5. **错误处理**：风控不重试，立即报错（参考 SKILL.md 决策规则）
6. **限速**：每条 fetch 之间默认 sleep 1s；连续 `ab_open` sleep ≥ 2s

## 提 PR 前自检

```bash
# 1. 语法检查
python3 -m py_compile paths.py bili-fetch.py bili-harvest.py

# 2. 路径配置 sanity
python3 paths.py

# 3. dry-run 跑核心子命令
python3 bili-fetch.py paths
python3 bili-fetch.py user-search "影视飓风"
python3 bili-harvest.py user 5294454 --videos 5 --comments 3 --sleep 0
```

## 与 douyin/xhs/zhihu 的对齐点

为了让多个 skill 互相兼容，对齐这些约定：

| 维度 | 约定 |
|---|---|
| 路径 env 变量前缀 | `{SITE}_DATA_DIR` / `{SITE}_COOKIE_FILE` |
| 主数据目录默认 | `$SKILL/data/` |
| 老 `/tmp/{site}/` 路径 | 自动识别，向后兼容 |
| harvest 落盘结构 | `$DATA_DIR/harvests/<topic>-<ts>/{REPORT.md, items, videos/}` |
| agent-browser eval 返回值 | JS 端 `JSON.stringify(...)`，Python 端 `json.loads` 两次 |

## 调试笔记 (写在这里)

```bash
# 看 SPA 是否正常渲染
agent-browser open "https://space.bilibili.com/5294454/upload/video"
sleep 6
agent-browser eval "document.querySelectorAll('.bili-video-card').length"

# 看 fetch 是否能拿到 buvid cookie
agent-browser eval "fetch('https://api.bilibili.com/x/web-interface/view?bvid=BV1K3Gz6pEoo', {credentials:'include'}).then(r=>r.json()).then(j=>j?.data?.title)"
```