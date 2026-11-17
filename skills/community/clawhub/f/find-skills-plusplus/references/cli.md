# 命令行工具 `findskills.py`

零依赖 Python CLI（仅标准库）。让发现/审查/安装脱离 agent 也能跑、可演示、可测试。

```bash
python findskills.py <子命令> [选项]
```

## 子命令总览（20 个）

| 子命令 | 作用 |
|---|---|
| `search` | 搜索（本地已装 + 离线注册表 + SkillHub 缓存 + 可选联网），语义匹配 + 合并去重 + 综合排序 |
| `scan` | 安全静态扫描（正则 + AST），四级风险，输出权限清单 |
| `install` | 下载社区技能 → 扫描 → 解压（EXTREME/P0 阻断） |
| `update` | 重下最新并覆盖已装社区技能（同样过安全网关） |
| `uninstall` | 卸载本地技能（进回收站，可还原） |
| `clean-dupes` | 清理重复安装（保留最新一份，其余进回收站） |
| `sync` | 拉取 SkillHub 全量目录到本地缓存（离线全能） |
| `discover` | 新上架 / 热门 / 精选榜单（含跨源版本仲裁） |
| `list` | 列出本地已装技能 |
| `audit` | 审计所有已装技能风险 |
| `quality` | 评估单个技能质量（0-100，七维含引用完整性） |
| `redundancy` | 检测重复安装与功能冗余 |
| `prune` | 基于静态信号给出瘦身建议（只读） |
| `registry` | 离线注册表 `registry.json` 校验 / 查看 / 追加 |
| `promote` | **生成自我推广素材包**（简介/banner/卖点/对比表/社交文案/发布清单，5000+ 字） |
| `demo` | **可录屏端到端演示**（搜索→评级→安检→治理→自述，5 场景带耗时） |
| `elevator` | **30 秒电梯演讲**（差异化自述，对话中可直接复述） |
| `outdated` | 巡检已装技能是否有新版本可更新（基于注册表 / 缓存） |
| `doctor` | **环境体检**：frontmatter 合法性 / 质量分 / 重复安装 / 连接器依赖 / 硬编码路径密钥 |
| `publish` | **发布就绪校验（上架闸门）**：查市场门槛 + 调 `scripts/smoke.py` 端到端冒烟自证 |

## 常用示例

```bash
# 搜索（离线优先）
python findskills.py search pdf --offline --limit 5
python findskills.py search 股票 --limit 6          # 语义匹配，自然语言可用

# 安全扫描
python findskills.py scan <技能目录> --lang zh-CN
python findskills.py scan <技能目录> --json          # 机器可读，含权限清单

# 安装 / 更新 / 卸载
python findskills.py install <slug> [--target DIR] [--yes] [--force]
python findskills.py update <slug> [--yes] [--force]
python findskills.py uninstall <slug>                # 进回收站，非硬删除

# 生态治理
python findskills.py sync [--limit N]                # 同步全量目录到缓存
python findskills.py discover [--new|--trending] [--limit N]
python findskills.py list | audit
python findskills.py quality <slug> [--path DIR]
python findskills.py redundancy | prune
python findskills.py registry validate|show|add ...

# ——— 自我营销（Phase 5）———
python findskills.py elevator                     # 30 秒电梯演讲
python findskills.py demo [--query Q] [--lines N] # 端到端演示，可录屏
python findskills.py promote [--out PROMO.md]     # 生成全套推广素材

# ——— 生命周期闭环 + 发布闸门（Phase 7）———
python findskills.py outdated                  # 巡检可更新技能
python findskills.py doctor                    # 环境体检，逐项排查问题
python findskills.py publish [--no-smoke] [--strict]  # 上架前校验 + 冒烟自证
```

## 设计要点

- **离线优先**：内置 `registry.json` + SkillHub 缓存（`registry.cache.json`，TTL 24h）；API 挂了也能推荐。
- **联网可选**：`--offline` 强制离线；`sync` 主动补齐全量目录。
- **跨平台**：目标目录自动判定（WorkBuddy `~/.workbuddy/skills/` / CodeBuddy `~/.codebuddy/skills/`）。
- **安全闸门**：`install` / `update` 前强制过扫描器（正则 + **AST 语法树级**双重检测），EXTREME 阻断。
- **卸载安全**：`uninstall` / `clean-dupes` 走系统回收站（Windows 原生 / `gio trash` / `trash-put`），非 `rm`；不可用时回落 `~/.workbuddy/.trash/`。
- **质量评级**：七维，含**环境感知引用完整性**（声明却不存在的文件/技能引用会大幅降级，专治假优）。

## 测试

```bash
python -m pytest tests/ -q
```

覆盖：扫描器（正则 + AST）、四级风险分类、权限清单、排序、去重、注册表、缓存、引用校验、生命周期、发现榜单、CLI。CI 自动校验 SKILL.md frontmatter + 跑扫描器自测 + pytest。
