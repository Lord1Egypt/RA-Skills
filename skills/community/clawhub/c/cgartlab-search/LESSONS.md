# LESSONS — cgartlab-search

> 统一搜索 Agent Skill（多后端路由：Brave/Exa/Context7 + key-less Bing RSS/腾讯新闻/虎扑/SO/GitHub/HN，Node 18+ 零依赖）。
> 本仓库从真实失误沉淀的「教训→规则」清单。**会话开始先全文阅读并遵循其中所有规则**；出现新失误按 §维护 追加。
> 权威依据：Anthropic Claude Code memory/best practices（<200 行、具体可验证、第二次犯同样错即写入）；社区 lessons.md 惯例（Boris Cherny，Anthropic）。
> 来源：本仓库 SKILL.md / README.md + 已验证 fix 提交；预填为种子，后续由 Agent 在真实工作中增长。

## 维护
- **触发**：用户纠正 / Agent 自查到的失误 / 非显而易见的 gotcha。
- **格式**：`### <主题>` 下，每条 = 失误（具体场景）→ 规则（最小可执行指令），一行可验证。
- **只记项目特有、不可从代码推断的**；通用最佳实践不写；含糊措辞（"小心""注意"）删掉。
- **重复出现** → 升级进 `AGENTS.md` 硬规则；**月度审阅**裁剪过期项；目标 < 200 行。

## SKILL.md Frontmatter

### description YAML 标量格式
- 失误：SKILL.md frontmatter 的 `description` 值含单引号（如 `don't`），未用单引号标量包裹，YAML 解析非法 → 规则：含撇号/特殊字符的 description 用单引号标量包裹，内部撇号双写（见 SKILL.md frontmatter）（commit 1b97f3f）

### version 唯一权威源
- 失误：版本号出现在多处不一致（SKILL.md/README/CHANGELOG/tag） → 规则：`SKILL.md` frontmatter `metadata.version` 是唯一权威，tag 命名 `v<version>` 逐字一致（见 README「发布与版本」）

## 脚本与密钥

### secrets.json 解析路径
- 失误：`secrets.json` 解析路径未从技能根目录查找，在不同 harness 下找不到文件 → 规则：解析路径改为技能根优先（commit 1ad5fb8）

### key-less vs keyed 后端
- 失误：在受限 egress 环境（如 DSH）调用 brave/exa，这两个是 curl-only keyed 后端，WebFetch 不可达 → 规则：key-less 后端（bing/context7/qqnews/hupu/so/github/hn）走 WebFetch，keyed 后端（brave/exa）走 curl，不可达时降级用 bing 替代（见 SKILL.md「Backend status」）

### 失败后端不编造
- 失误：某后端不可达时编造结果替代 → 规则：不可达的后端在回复中加一行说明（如 "Brave/Exa 在本环境不可达，已用 bing 替代"），绝不编造（见 SKILL.md「Step 3」）

### python3 可能是空存根
- 失误：`scripts/search.sh` 直接用 `python3`，本机该命令是 Microsoft Store 别名存根，exit 0 且不输出，全部后端静默返回空 JSON → 规则：脚本必须探测解释器并验证真实输出（`"$cand" -c 'print(1)'` 等于 `1`），不能只看命令是否存在

### 原生工具不读 MSYS 路径
- 失误：把 `$(cd … && pwd)` 得到的 `/d/...` 路径当参数传给 Windows 原生 Python，抛 `FileNotFoundError` → 规则：给原生工具的数据一律走 stdin（或先 `cygpath -w`），不把 MSYS 路径用作参数

### 安装器不改 PATH
- 失误：`tencent` 适配器只解析裸命令名，而官方安装器把二进制放在 `~/.tencent-news-cli/bin/` 且不改 `PATH`，已装好的机器仍报 "not found" → 规则：外部 CLI 依赖按 `环境变量` → `PATH` → `安装器默认目录` 三级解析

## CI 与发布

### public 仓库不能调用 private 仓库的 reusable workflow
- 失误：`publish.yml` 用 `uses: cgartlab/cgartlab-skills/.github/workflows/publish-skill.yml@main` 复用发布逻辑，仓库转为 public 后 `gh workflow run publish.yml` 直接报 `workflow was not found`，registry 发布整条链路静默失效 → 规则：skill 仓库的发布逻辑内联在本仓库（`.github/actions/publish/action.yml`），不跨仓库引用 reusable workflow

### GITHUB_TOKEN 创建的 Release 不触发其它 workflow
- 失误：`release.yml` 用 `GITHUB_TOKEN` 创建 Release，指望 `publish.yml` 的 `on: release: [published]` 接力，实际永不触发（GitHub 防递归），历史上 `publish.yml` 只被 push 触发过一次 → 规则：release 与 publish 放在同一个 workflow 里用 `needs:` 串联，不靠事件接力

### workflow YAML 交付前本地解析
- 失误：workflow 的缩进/键名错误只有推到 GitHub 才知道，一轮反馈几十秒起步 → 规则：`scripts/gate.sh` 的 [5/5] 解析 `.github/workflows/*.yml` 与 `.github/actions/*/action.yml`（composite step 必须显式写 `shell`），依赖 PyYAML，缺失时降级为 warn

## 路由与降级

### 知乎未配置时的降级
- 失误：zhihu 未配置时不降级，直接报错 → 规则：用 `bing site:zhihu.com` 作为 best-effort 替代，miss 时诚实说明降级（见 SKILL.md「Step 1」）

### 语义化路由
- 失误：所有查询都走同一后端，未按意图路由 → 规则：general web→bing、docs→context7、dev Q&A→so+hn、news→qqnews、足球→hupu、deep research→bing+context7+hn（见 SKILL.md「Step 1」）
