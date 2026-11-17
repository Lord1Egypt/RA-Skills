# LESSONS — down

> 万能下载 Agent Skill（URL 分析 → 最少步骤下载到本地，Python 3.9+ stdlib，detect.py 纯函数探测，不静默安装工具）。
> 本仓库从真实失误沉淀的「教训→规则」清单。**会话开始先全文阅读并遵循其中所有规则**；出现新失误按 §维护 追加。
> 权威依据：Anthropic Claude Code memory/best practices（<200 行、具体可验证、第二次犯同样错即写入）；社区 lessons.md 惯例（Boris Cherny，Anthropic）。
> 来源：本仓库 AGENTS.md 的四条元规则 / 工作约定 + 已验证 fix 提交；预填为种子，后续由 Agent 在真实工作中增长。

## 维护
- **触发**：用户纠正 / Agent 自查到的失误 / 非显而易见的 gotcha。
- **格式**：`### <主题>` 下，每条 = 失误（具体场景）→ 规则（最小可执行指令），一行可验证。
- **只记项目特有、不可从代码推断的**；通用最佳实践不写；含糊措辞（"小心""注意"）删掉。
- **重复出现** → 升级进 `AGENTS.md` 硬规则；**月度审阅**裁剪过期项；目标 < 200 行。

## 元规则

### 不静默安装工具
- 失误：脚本检测到工具缺失后直接执行安装命令 → 规则：脚本只检测工具是否存在，绝不执行安装动作；安装必须先展示命令、大小、理由，等用户"go"（见 AGENTS.md「四条元规则」）

### 探测器纯函数
- 失误：`detect.py` 发网络请求或修改文件系统 → 规则：`detect.py` 只根据 URL 形状分类，不发网络请求，不修改文件系统，任何需要网络的判定留给 caller（见 AGENTS.md「四条元规则」）

### 报告如实
- 失误：URL 无法识别时说"没有"而非"没查成"，或工具缺失时跳过验证 → 规则："没查成"必须写成"没查成"，不得写成"没有"；下载失败就说失败，不编造成功（见 AGENTS.md「四条元规则」）

## 能力边界

### 不越界
- 失误：skill 尝试做资源搜索或 JS 反爬破解 → 规则：skill 只做文件下载（curl 直链/yt-dlp 视频/.torrent 文件），识别但不做网盘链接（用户手动转存），明确拒绝 magnet 内容拉取/网盘内容下载/JS 反爬/资源搜索（见 AGENTS.md「能力边界」）

### 不做的功能
- 失误：实现 `probe_host.py`（网络探测）或 `download.py`（下载执行器） → 规则：明确不做，决策见 `docs/PLAN-v0.2.md` D1/D2（见 AGENTS.md「未来方向」）

## 文档与脚本同步

### 改探测器要同步三处
- 失误：改了 `detect.py` 判定逻辑但未同步 `references/detectors.md` 和 `evals/test_detect.py` → 规则：三处不一致即为漂移，改一处必须同步三处（见 AGENTS.md「改本仓库时」）

### SKILL.md 不复述 references
- 失误：在 SKILL.md 中复述命令配方、判定表、站点清单 → 规则：SKILL.md 只做路由（读哪个文件）+ 流程（Phase 顺序）+ 元规则 + 能力边界，细节在 references 里（见 AGENTS.md「改本仓库时」）

### 加规则配对减规则
- 失误：往 SKILL.md/AGENTS.md 加条文不删旧条文，文档膨胀 → 规则：加条文时必须同时指出可删除或合并的旧条文（见 AGENTS.md「改本仓库时」）

## 脚本约定

### 脚本黑盒
- 失误：caller 直接 import 脚本内部函数而非通过 CLI 接口 → 规则：`scripts/*.py` 是 CLI 接口，caller 通过命令行参数传入、读 stdout JSON，改脚本要同步更新 `references/detectors.md` 字段契约（见 AGENTS.md「工作约定」）

### 辅助脚本也只读
- 失误：`check_tools.py` 或 `proxy_chain.py` 发网络请求或修改环境变量 → 规则：两者都只做只读检查，不发网络、不修改环境变量、不安装任何东西（见 AGENTS.md「四条元规则」）

## 测试

### unittest 而非 pytest
- 失误：引入 pytest 依赖 → 规则：所有 scripts 只依赖 stdlib，v0.2 保持 unittest 不用 pytest（见 AGENTS.md「依赖」）
### 保存路径三级优先级
- 失误：skill 硬编码默认下载路径 → 规则：保存路径按三级优先级解析（用户显式指定 → 环境偏好 → 临时目录兜底，不询问）（见 README「三条不可让渡的规则」）

## CI 与标签

### labeler v5 需要 `any-glob-to-any-file`
- 失误：`changed-files` 写成裸字符串数组，触发 actions/labeler@v5 的结构错误 → 规则：v5 语法必须用 `any-glob-to-any-file:` / `all-globs-to-all-files:` 显式包装（commit abad3a6）

### labeler 路径必须映射真实结构
- 失误：labeler 规则照抄别处，glob 指向本仓库不存在的目录 → 规则：改 labeler 先核对本仓库真实目录，并优先用分支名标签（commit 8aa8ebe）

### CI 要跑单测与探测器
- 失误：CI 只做语法检查，探测器回归无人拦 → 规则：CI 必须包含 `unittest discover` 与探测器冒烟（commit 8aa8ebe）

### 版本策略文档不能漂移
- 失误：`AGENTS.md` 的版本策略与真实 tag 状态不一致（0.1.0 无 tag）→ 规则：改版本相关文档前先 `git tag --list` 核对真实已发布状态（commit a991ed6）

## 版本管理

### author 名修正
- 失误：author 名写成 `cgart` 而非 `cgartlab` → 规则：correct author name from cgart to cgartlab（commit 747220c）
