# AGENTS.md — down 仓库编码约定

> **会话约定**：开始任何工作前，先读根目录 `LESSONS.md`（本仓库从真实失误沉淀的「教训→规则」清单）并遵循其中所有规则；遇到新失误按其 §维护 追加。

给在本仓库工作的 coding agent 的指引。

## 这是什么

`down` —— Hermes Agent Skill，一个"万能下载"技能。用户扔 URL，skill 分析后用最少的工具步骤下载到本地。

主入口：`SKILL.md`。工作流见 SKILL.md，工具矩阵见 `references/tool-matrix.md`。

## 四条元规则

1. **不静默安装工具**：脚本或 SKILL.md 里的任何安装命令必须走用户批准流程。脚本只能**检测**工具是否存在，绝不**执行**安装动作。
2. **探测器纯函数**：`scripts/detect.py` 只根据 URL 形状分类，**不发网络请求**，**不修改文件系统**。任何需要网络的判定都留给 caller（SKILL.md 的 Phase 3+）。
3. **辅助脚本也只读**：`scripts/check_tools.py` 和 `scripts/proxy_chain.py` 都只做**只读检查**——前者查工具是否可用，后者解析代理链。都不发网络、不修改环境变量、不安装任何东西。
4. **报告如实**：任何工具缺失、硬墙站点、验证失败都必须写进回复；禁止编造下载成功或跳过验证。

## 工作约定

- **脚本黑盒**：`scripts/*.py` 是 CLI 接口，caller 通过命令行参数传入、读 stdout JSON。**改脚本要同步更新 `references/detectors.md` 的字段契约**。
- **只读探测**：detect.py 不写入任何文件（除了 `--help` 输出到 stdout）。任何需要落盘的逻辑都不该进 detect.py。
- **安全分层**：
  - 只读探测（detect.py / check_tools.py / proxy_chain.py）：自动执行，无副作用
  - 工具安装：必须先展示命令、大小、理由，等用户"go"
  - 文件下载：默认执行（用户明确要求了），保存路径按 SKILL.md 的三级优先级解析
- **不编造**：URL 无法识别就说 unknown；工具缺失就说缺失；下载失败就说失败。**"没查成"必须写成"没查成"，不得写成"没有"**。

## skill 的能力边界（v0.2 新增）

skill 只做文件下载，不越界：

- **做**：下载直链文件（curl）、下载平台视频（yt-dlp）、下载 .torrent 文件本体（curl）
- **识别但不做**：网盘链接（cloud_drive kind → 用户手动转存）
- **明确拒绝**：magnet 内容拉取（需要 BT 客户端）、网盘内容下载（需要账号登录）、JS 反爬破解、资源搜索
- **不做**：网络探测（probe_host.py）、下载执行器（download.py）——见 `docs/PLAN-v0.2.md` 的决策记录 D1/D2

## 改本仓库时

- **提交规约**：conventional commits（`feat` / `fix` / `docs` / `chore` / `test` / `refactor`）；body 讲 WHY。
- **版本策略**：`0.1.0` 与 `0.2.0` 均已发布（远端 tag 仅 `v0.2.0`；`0.1.0` 无 tag）。v0.3 尚未开始，正在进行的变更记入 `CHANGELOG.md` 的 `[Unreleased]`（当前该章节不存在，说明没有未发布变更）。语义版本遵循 semver。
- **改探测器要同步**：改 `detect.py` 的判定逻辑 → 同步 `references/detectors.md` 的判定表 → 同步 `evals/test_detect.py` 的测试用例。三处不一致即为漂移。
- **不要在 SKILL.md 复述 references 的细节**：SKILL.md 只做**路由**（读哪个文件）+ **流程**（Phase 顺序）+ 元规则 + 能力边界。所有命令配方、判定表、站点清单都在 references 里。
- **加规则要配对减规则**：往 SKILL.md 或 AGENTS.md 加条文时必须同时指出可删除或合并的旧条文。文档膨胀是唯一刹车。

## 自检（提交前跑）

```bash
# 全部单元测试
python -m unittest discover -s evals -v

# 手工冒烟：跑几个不同 kind 的 URL
python scripts/detect.py --url "https://youtube.com/watch?v=dQw4w9WgXcQ"
python scripts/detect.py --url "https://example.com/file.mp4"
python scripts/detect.py --url "https://pan.baidu.com/s/abc"      # cloud_drive
python scripts/detect.py --url "magnet:?xt=urn:btih:abc&dn=test"  # magnet → none

# 工具检查
python scripts/check_tools.py --json

# 代理链解析
python scripts/proxy_chain.py --json
```

## 依赖

- **必需**：Python 3.9+（所有 scripts 只依赖 stdlib）
- **可选**：`pytest`（如果不用 `unittest`）——v0.2 未使用，保持 unittest

## 未来方向（v0.3+）

- **多 profile 支持**：不同 Hermes profile 可以有不同默认下载路径
- **aria2 会话管理**：扫 `~/.aria2/session` 报告未完成的下载
- **uvx 分发**：把 detect.py / check_tools.py 打包成 CLI 工具
- **~/.downrc 支持 TOML**（Python 3.11+ 用 tomllib，3.9+ 保持 JSON）

**明确不做**（决策见 `docs/PLAN-v0.2.md`）：
- probe_host.py（网络探测）
- download.py（下载执行器）
- headless browser 自动化
