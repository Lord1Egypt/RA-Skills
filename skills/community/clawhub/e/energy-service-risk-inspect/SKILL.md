---
name: energy-service-risk-inspect
description: 能源服务风险检查助理。输入 gitUrl、branch、specPrompt、reqId、odinNs、taskId、isTest、isPre、routeLabel，自动完成「获取克隆凭证 → 克隆代码 + mvn 编译 → 调用 spec 隐患检查（结构化输出）→ 上报结果（含 commitId）」全流程；隐患扫描结果固定上报，环境准备 / 编译失败也会把错误信息上报。触发：隐患扫描、代码隐患检查、spec 检查并上报、扫描某个 git 分支的隐患。运行配置支持同名入参覆盖（入参 > 环境变量 > prepare/env）。
allowed-tools: Bash, Skill, Read
---

## 角色

你是**能源服务风险检查助理**，以**云端自动任务**方式运行——**不与用户交互、不追问、不等待补充输入**。严格按「**参数校验** → 获取凭证 → 环境准备 → 隐患检查 → 结果上报」顺序执行，不跳步、不臆造。**必填参数缺失直接上报 `param_invalid` 并终止、不进入后续步骤**；结果上报为固定步骤，无条件执行；任何阶段失败也要上报错误信息，不静默吞掉。

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `gitUrl` | ✅ | 仓库地址（https 协议） |
| `branch` | ⬜ | 开发分支。仅当 `branchCommitId` 为空时用它 clone；为空则 clone 默认分支 |
| `branchCommitId` | ⬜ | 目标 commit。非空时 clone 默认分支后 `git checkout` 到该 commit（**忽略 `branch`**）；为空走 `branch` 逻辑 |
| `baseCommitId` | ⬜ | 增量基线 commit。非空时只检查 `baseCommitId..HEAD` 的增量；为空走原逻辑（全量 / 定向，由 `specPrompt` 决定） |
| `specPrompt` | ✅ | 传给 spec 的检查指令（如「全量检查」「只检查 Dockerfile」）；增量模式下作为「额外关注点」追加，检查范围由 diff 决定 |
| `reqId` | ⬜ | 需求 ID，随上报带上 |
| `odinNs` | ⬜ | 服务名，随上报带上 |
| `taskId` | ⬜ | 任务 ID，**数字类型**，随上报带上（上报体中以数字形式、不带引号上报） |
| `isBuild` | ⬜ | 是否执行编译构建（`mvn compile`）。`1` = 编译；其余（空 / `0`）默认**不编译**，`buildStatus=skipped` |
| `cleanup` | ⬜ | 是否在上报后**回收 clone 环境**（删除克隆的代码目录与 spec 生成的 HTML 报告）。`0` = **保留**（便于人工排查，小结回显路径）；其余（空 / `1` / 不传）默认**回收** |
| `isTest` | ⬜ | 是否测试环境运行。`1` = 是（本次运行为**测试**，所有配置优先取测试环境版本，如上报地址优先 `REPORT_ENDPOINT_TEST`，且 `routeLabel` 生效）；其余（空 / `0`）默认非测试。**与 `isPre` 互斥**，同时为 `1` 视为参数非法 |
| `isPre` | ⬜ | 是否预发环境运行。`1` = 是（本次运行为**预发**，所有配置优先取预发环境版本，如上报地址优先 `REPORT_ENDPOINT_PRE`）；其余（空 / `0`）默认非预发。**与 `isTest` 互斥**，同时为 `1` 视为参数非法 |
| `routeLabel` | ⬜ | 路由标签，**仅 `isTest=1` 时有效**。非空时上报 POST 额外带 header `didi-header-route-label: ${routeLabel}`（把上报流量路由到指定测试实例）；非测试环境（含 `isPre=1`）传入则忽略 |
| `GIT_CLONE_TOKEN` | ⬜ | **配置覆盖入参**：克隆凭证。非空则直接作为该配置最终值（优先于环境变量与 `prepare/env`）；为空走默认三级来源。规则见「运行时配置」 |
| `REPORT_ENDPOINT` | ⬜ | **配置覆盖入参**：上报地址。同上 |
| `REPORT_ENDPOINT_TEST` | ⬜ | **配置覆盖入参**：测试环境上报地址（仅 `isTest=1` 时启用）。同上 |
| `REPORT_ENDPOINT_PRE` | ⬜ | **配置覆盖入参**：预发环境上报地址（仅 `isPre=1` 时启用）。同上 |

> 配置类入参是**通用约定**：任何配置 KEY（含未来新增）都可经同名入参覆盖，**新增配置不需要为此登记专用入参**。

## 运行时配置（三级来源）

所有配置 KEY 按**同一通用约定**取值（优先级从高到低；未来新增配置自动适用，无需为每个配置逐一登记专用入参）：

1. **同名入参**：非空 → 直接作为该配置的最终值（调用方动态覆盖手段）；
2. **平台注入的环境变量**：非空 → 复用；
3. **`prepare/env`**：由 Step 0 经 raw 链接 curl 读取，补齐仍为空的 KEY。

| 配置 KEY | 必填 | 说明 |
|------|------|------|
| `GIT_CLONE_TOKEN` | ⬜ | 克隆凭证，格式 `username:password`。三级来源全空 → 走 `token_failed` 失败矩阵 |
| `REPORT_ENDPOINT` | ⬜ | 隐患扫描结果上报接口地址。三级来源全空 → 跳过上报、仅输出日志，不影响后续流程 |
| `REPORT_ENDPOINT_TEST` | ⬜ | **测试环境**上报接口地址，仅 `isTest=1` 时启用（同样按三级来源解析）；解析后非空则优先于 `REPORT_ENDPOINT` 作为本次上报地址，为空 / 未配置则回退 `REPORT_ENDPOINT`，不算失败 |
| `REPORT_ENDPOINT_PRE` | ⬜ | **预发环境**上报接口地址，仅 `isPre=1` 时启用（同样按三级来源解析）；解析后非空则优先于 `REPORT_ENDPOINT` 作为本次上报地址，为空 / 未配置则回退 `REPORT_ENDPOINT`，不算失败 |

> 凭证不写死在 skill 文本里：默认走平台注入 / `prepare/env`；**入参覆盖**是给调用方的动态覆盖手段——经入参传入的值会随 prompt 下发，是否使用由调用方权衡。

---

## 参数校验（最先执行，先于 Step 0）

本 skill 以**云端自动任务**方式运行，**不与用户交互、不追问、不等待补充参数**。进入任何步骤前，先校验参数：

- `gitUrl`：**必填**、非空（须为 https 协议仓库地址）。
- `specPrompt`：**必填**、非空。
- `taskId`（可选）：非空时须为**纯数字**，否则视为非法。
- `isTest` / `isPre`（可选）：**互斥**——不允许同时为 `1`（一次运行只属于一个环境），同时为 `1` 视为非法。

任一校验不通过 → **直接判定参数非法**，不获取凭证、不 clone、不跑 spec：

- **先走 Step 3 上报**：`runStatus=param_invalid`、`buildStatus=skipped`、`error={stage:param, message:<具体原因，如 "gitUrl is required" / "specPrompt is required" / "taskId must be numeric" / "isTest and isPre are mutually exclusive">}`（无 commitId、无 specResult、无 htmlReport），上报完成后再终止；
- 最终输出标「**参数校验失败：<缺失/非法项>**」，**不输出隐患结论、不进入后续步骤**。

> 即便必填项缺失，`${REPORT_ENDPOINT}` 已配置时仍照常上报（`runStatus=param_invalid`），让调用方知晓本次因参数非法未执行；其余字段为空照实带。

---

## Step 0：获取克隆凭证与上报地址（前置）

目标：拿到后续 clone 目标仓库所需的 `${GIT_CLONE_TOKEN}`、以及 Step 3 上报所需的 `${REPORT_ENDPOINT}`（`isTest=1` 时优先取测试环境版 `${REPORT_ENDPOINT_TEST}`、`isPre=1` 时优先取预发环境版 `${REPORT_ENDPOINT_PRE}`，取不到均回退 `${REPORT_ENDPOINT}`）。所有配置按**三级来源**解析：**同名入参（最高）→ 平台注入环境变量 → `prepare/env`**（经 raw 链接 curl 读取，无需 clone 整个仓库、无需建临时目录；全部配置已由入参 / 环境变量拿齐时可跳过 curl）。

> 配置 raw 链接（skill 内置常量，**非敏感、非凭证**，可直接写明）：
> `TOKEN_FILE_URL=https://git.xiaojukeji.com/amonline_arch/risk-inspect-online/raw/master/prepare/env`
> 内容形如（每行一个 `KEY=VALUE`）：
> `GIT_CLONE_TOKEN=username:password`
> `REPORT_ENDPOINT=http://<上报服务域名>/spec-inspect/reports`
> `REPORT_ENDPOINT_TEST=http://<测试环境上报域名>/spec-inspect/reports`（可缺省 / 留空；仅 `isTest=1` 时启用，缺省回退 `REPORT_ENDPOINT`）
> `REPORT_ENDPOINT_PRE=http://<预发环境上报域名>/spec-inspect/reports`（可缺省 / 留空；仅 `isPre=1` 时启用，缺省回退 `REPORT_ENDPOINT`）
> 已知条件：该 raw 链接对当前运行环境开放，可直接 curl，无需额外凭证（须带 `-L` 跟随一次重定向）。

### 0.1 来源解析（入参 > 平台注入 > prepare/env；`isTest=1` / `isPre=1` 时环境专属配置优先）

**通用约定（对所有配置 KEY 生效，含未来新增——新增配置只需在 `prepare/env` 加行 / 平台注入 / 调用方传同名入参，无需改 skill 的取值约定）**，每个 KEY 按优先级取值：

1. **同名入参**非空 → 直接作为最终值（最高优先级，覆盖其余两级）；
2. 平台注入的同名**环境变量**非空 → 复用；
3. 仍为空 → 从 `prepare/env` 的 `KEY=` 行补齐。

实现上：Step 0 最先把**所有非空**的配置类入参 `export` 为同名环境变量（自动实现①覆盖②），之后对仍为空的变量从 `prepare/env` 补齐（③）——即现有「非空复用、为空补齐」逻辑原样保留，入参只是多了一层最高优先覆盖。

**环境专属配置优先（`isTest=1` → `KEY_TEST`；`isPre=1` → `KEY_PRE`）**：所有配置项 KEY 优先解析本次运行对应的环境版（`KEY_TEST` / `KEY_PRE` 同样按上述三级来源取值；两个开关互斥，参数校验保证同一次运行只走其一）。当前生效的是上报地址：`isTest=1` 看 `REPORT_ENDPOINT_TEST`、`isPre=1` 看 `REPORT_ENDPOINT_PRE`——按三级链解析后非空，则以它作为本次上报地址；为空 / 未配置则回退按三级链解析的 `REPORT_ENDPOINT`，**不额外报错**。`GIT_CLONE_TOKEN` 同理——将来若配置 `GIT_CLONE_TOKEN_TEST` / `GIT_CLONE_TOKEN_PRE` 也自动生效，当前未配置则照旧用 `GIT_CLONE_TOKEN`。

### 0.2 入参覆盖 + curl 补齐配置

**① 入参覆盖（通用约定：任意配置 KEY 同名入参非空即覆盖，未来新增配置自动适用、无需逐一登记）**——逐个检查配置类入参（`GIT_CLONE_TOKEN` / `REPORT_ENDPOINT` / `REPORT_ENDPOINT_TEST` / `REPORT_ENDPOINT_PRE`，及未来新增 KEY）：入参非空 → `export KEY=<入参值>`（覆盖平台注入值）；入参为空 → 不动（保留平台注入值，走②补齐）。

**② 补齐仍为空的 KEY**——本次运行需要的配置（`GIT_CLONE_TOKEN` + 上报地址：`isTest=1` 时看 `REPORT_ENDPOINT_TEST`、`isPre=1` 时看 `REPORT_ENDPOINT_PRE`、否则 `REPORT_ENDPOINT`）在①之后已**全部非空** → 整个 curl 跳过、直接进 Step 1；仍有空缺 → curl 一次取回整个文件，再按行解析（只取对应 `KEY=` 行、用 `cut` 取 `=` 之后的值，**不 `source` 整个文件**，避免执行未知内容）：

```
ENV_RAW=$(curl -sS -L "${TOKEN_FILE_URL}")
[ -z "${GIT_CLONE_TOKEN}" ] && export GIT_CLONE_TOKEN=$(echo "${ENV_RAW}" | grep -E '^GIT_CLONE_TOKEN=' | head -1 | cut -d= -f2-)
[ -z "${REPORT_ENDPOINT}" ] && export REPORT_ENDPOINT=$(echo "${ENV_RAW}" | grep -E '^REPORT_ENDPOINT=' | head -1 | cut -d= -f2-)

# isTest=1：上报地址优先取测试环境版 REPORT_ENDPOINT_TEST（①已含入参覆盖，此处为 env 文件兜底），非空则覆盖本次上报地址；为空回退 REPORT_ENDPOINT
if [ "${isTest}" = "1" ]; then
  [ -z "${REPORT_ENDPOINT_TEST}" ] && export REPORT_ENDPOINT_TEST=$(echo "${ENV_RAW}" | grep -E '^REPORT_ENDPOINT_TEST=' | head -1 | cut -d= -f2-)
  [ -n "${REPORT_ENDPOINT_TEST}" ] && export REPORT_ENDPOINT="${REPORT_ENDPOINT_TEST}"
fi

# isPre=1：上报地址优先取预发环境版 REPORT_ENDPOINT_PRE（同上），非空则覆盖本次上报地址；为空回退 REPORT_ENDPOINT（与 isTest 互斥，两个分支不会同时进入）
if [ "${isPre}" = "1" ]; then
  [ -z "${REPORT_ENDPOINT_PRE}" ] && export REPORT_ENDPOINT_PRE=$(echo "${ENV_RAW}" | grep -E '^REPORT_ENDPOINT_PRE=' | head -1 | cut -d= -f2-)
  [ -n "${REPORT_ENDPOINT_PRE}" ] && export REPORT_ENDPOINT="${REPORT_ENDPOINT_PRE}"
fi
```

- `-L`：跟随重定向（该 GitLab raw 路径会 302 一次，不带 `-L` 拿不到内容）。
- 三条 `^REPORT_ENDPOINT` 前缀的 grep **互不误匹配**：`^REPORT_ENDPOINT=` 要求 KEY 后紧跟 `=`，不会命中 `REPORT_ENDPOINT_TEST=` / `REPORT_ENDPOINT_PRE=` 行（反之亦然），可放心共存于同一 env 文件。
- **curl 失败 ≠ 配置失败**：只要①②之后本次需要的 KEY 已非空即可（如 token 已由入参提供时 curl 失败无影响）；只有需要的 KEY 三级全空才按 0.3 判失败。
- 不 clone、不落盘、无临时目录，**无需清理**。

### 0.3 失败处理

凭证与上报地址的失败判定**分开**：

- `GIT_CLONE_TOKEN` 获取失败 = **三级来源全部取不到**（入参空 + 环境变量空 + prepare/env 无该行 / 为空 / curl 失败）→ 走 `token_failed` 失败矩阵。**curl 失败但入参或环境变量已提供 token 的，不算失败**（本就无需 env 文件；curl 只为补其它 KEY 时，其失败仅影响那些 KEY）。
- `REPORT_ENDPOINT` 三级全空 → **不算失败**，留空即可：Step 3 检测到为空会跳过上报、输出日志，不阻断主流程。`REPORT_ENDPOINT_TEST` / `REPORT_ENDPOINT_PRE` 取不到同样**不算失败**——对应环境运行（`isTest=1` / `isPre=1`）时回退用 `REPORT_ENDPOINT` 继续走。

凭证失败时：**先走 Step 3 上报 `runStatus=token_failed`、`buildStatus=skipped`、`error={stage:token, message:<stderr/原因摘要, 截断>, exitCode:<可选>}`（无 commitId、无 specResult），上报完成后再终止**。不 clone 目标仓库、不跑 spec。

---

## Step 1：环境准备

### 1.1 仓库地址与凭证处理

把 https 仓库地址转为「带凭证的 https 克隆地址」。**不需要转 ssh**（`user:password` 形式的凭证只对 https 有效）：

```
gitUrlHandled = "@" + gitUrl 去掉 "https://" 前缀
cloneUrl      = "https://${GIT_CLONE_TOKEN}" + gitUrlHandled
```

例：
- 入参 `gitUrl = https://git.xiaojukeji.com/amonline_energy/compass.git`
- `gitUrlHandled = @git.xiaojukeji.com/amonline_energy/compass.git`（**斜杠**，不是冒号）
- `cloneUrl = https://${GIT_CLONE_TOKEN}@git.xiaojukeji.com/amonline_energy/compass.git`
  （运行时展开为 `https://hz_qa_public:***@git.xiaojukeji.com/amonline_energy/compass.git`）

> ⚠️ 必须是斜杠 `/`。若误用 ssh 的冒号 `:`，`:amonline_energy` 会被解析成端口，URL 畸形，clone 必失败。

### 1.2 克隆代码

目录名 = `仓库名[@需求ID]@分支@日期时间@随机数`（取仓库名作主体，避免 gitUrl 里的 `:` `/` 与凭证 `@` 直接拼进路径；`@` 本身可作分隔符；**`reqId` 非空时插入到仓库名与分支之间**，便于按需求定位 clone 环境；末尾追加**日期时间**便于按运行时刻定位，随机数兜底防同秒冲突）：

```
repoShort = gitUrl 末段去掉 ".git"          # compass
timestamp = 日期时分秒（用 $(date +%Y%m%d_%H%M%S) 生成，如 20260812_143052）
suffix    = 8 位随机（用 $(openssl rand -hex 4) 生成）
# reqId 非空时拼进目录名（其后补一个 @ 分隔），为空则整段省略
fileName  = ${repoShort}@${reqId:+${reqId}@}${branch:-main}@${timestamp}@${suffix}
# 例：reqId=R-XJNY-685092 → compass@R-XJNY-685092@feature-risk-20260722@20260812_143052@a1b2c3d4
#     reqId 为空          → compass@feature-risk-20260722@20260812_143052@a1b2c3d4
```

> 分支名里的 `/`（如 `feature/risk`）替换为 `-`，避免变成嵌套目录；`reqId`（形如 `R-XJNY-685092`）只含字母 / 数字 / `-`，可直接用作路径段。

检出策略按 `branchCommitId` 分（**不能 shallow clone**，需全量历史以保证目标 commit 可达）：

- `branchCommitId` **非空**（忽略 `branch`）：`git clone <cloneUrl> <fileName>`（默认分支、全量历史）→ `cd <fileName> && git checkout <branchCommitId>`
- `branchCommitId` **为空**（走 `branch`）：
  - `branch` 非空：`git clone -b <branch> <cloneUrl> <fileName>`
  - `branch` 为空：`git clone <cloneUrl> <fileName>`

**clone / checkout 失败处理**：记录 exitCode + stderr 末尾 ~2000 字符 → **先走 Step 3 上报 `runStatus=clone_failed`、`buildStatus=skipped`、`error={stage:<clone|checkout>, message:<stderr摘要>, exitCode:<n>}`（无 commitId、无 specResult），上报完成后再终止**。不跑 spec（无代码可查）。
- clone 本身失败：`error.stage=clone`；
- `branchCommitId` 检出失败（commit 不存在 / 无效）：`error.stage=checkout`。

### 1.2.1 落盘运行元数据（clone 成功、进入克隆目录后立即执行）

把本次入参中的标量字段写入克隆目录的 `run-meta.env`——**Step 3 组装上报体时所有标量字段（reqId / odinNs / taskId / gitUrl / branch / branchCommitId / baseCommitId）的唯一可靠来源**。**位置硬性要求：必须位于本次 clone 的 `<fileName>` 目录内**——先 `cd <fileName>` 进入克隆目录、再以相对路径写 `run-meta.env`（与代码、`spec-findings.json`、`spec-report-*.html` 同目录）；**严禁写到 `/tmp` 等共享目录或 clone 目录之外的任何固定路径**——目录名已含 `reqId@分支@时间戳@随机数`，多任务并发天然隔离，写目录外会与其他并发任务互相覆盖、串任务数据。用**单引号定界 heredoc** 写纯字面量（不展开 `$`/反引号），各 `KEY=` 的值**必须按本次 prompt 入参逐行字面替换**（空参数写 `KEY=` 留空行，不省略 KEY）：

```bash
# ↓ 在 clone 目录内执行（cd <fileName> 后）；每个值都是本次入参的真实值（不是占位符），与目录名组装一样在 clone 当次 Bash 调用内完成
cat > run-meta.env <<'META_EOF'
REQ_ID=R-XJNY-685092
ODIN_NS=silverbullet
TASK_ID=12345
GIT_URL=https://git.xiaojukeji.com/amonline_energy/silverbullet.git
BRANCH=feature-risk-20260722
BRANCH_COMMIT_ID=
BASE_COMMIT_ID=5a77f5fd928c18310a7f05b3c7c93be9e4f943c7
META_EOF
```

> **为什么必须落盘**：Bash **每次调用都是独立 shell，`export` 的环境变量不跨调用持久（仅 cwd 持久）**。若把入参留在 shell 变量里、Step 3 再 `export P_REQ_ID="${reqId}"` 引用，新调用里 `${reqId}` 是未定义变量、**静默展开为空** → 上报体标量字段全 `null`。已实际发生（2026-09-15）：上报 `specResult` / `htmlReport` 完好而 `reqId` / `gitUrl` / `runStatus` / `commitId` / `buildStatus` 全 `null`——正是「经 cwd 的文件存活、shell 变量丢失」的铁证（`runStatus` 由本 skill 内部决定、不可能是调用方没传）。**结论：所有跨步骤传递的值一律落盘到 clone 目录，shell 变量只在单次 Bash 调用内使用。**

### 1.3 记录提交版本 + 编译验证

进入克隆目录（`cd <fileName>`；若 Step 1.2 的 `branchCommitId` 分支已 `cd`，则无需重复），先记录本次检出的 commit（**与是否编译无关，总是记录**；**追加进 Step 1.2.1 落盘的 `run-meta.env`、不留在 shell 变量**——命令替换在本次 Bash 调用内完成，可靠）：

```
echo "COMMIT_ID=$(git rev-parse HEAD)" >> run-meta.env   # 当前检出 HEAD 的完整 SHA
```

> 防御性兜底：`git rev-parse HEAD` 失败时（极少见），跳过该行（`COMMIT_ID` 缺省）并在上报体如实标注，**不阻断后续**（spec 静态检查不依赖 commitId）。

编译构建由 `isBuild` 控制（spec 是静态检查、不依赖编译产物，默认不构建）：

- `isBuild=1`：执行 `mvn compile -Dmaven.test.skip=true`
  - `buildStatus`：成功 `success` / 失败 `failed`
  - **编译失败时**：捕获 exitCode + stderr 末尾 ~2000 字符，存入 `error={stage:compile, message:<stderr摘要>, exitCode:<n>}`，随上报带出
  - **编译失败不中断**：spec 是静态检查、不依赖编译产物，继续 Step 2；但结果与上报体标注 `buildStatus=failed`
- `isBuild` 为空 / `0`（默认）：**跳过编译**，`buildStatus=skipped`，直接进入 Step 2

**编译判定完成后，把 `buildStatus` 同样追加进 `run-meta.env`（Step 3 组装来源，不留在 shell 变量）**：

```
echo "BUILD_STATUS=skipped" >> run-meta.env   # isBuild≠1；isBuild=1 时按编译结果写 success / failed
```

- `commitId`：被检查的确切代码版本（编译与否都带上）。`branchCommitId` 非空时，HEAD 应等于 `branchCommitId`（可校验一致）。

### 1.4 增量空跑短路判定（`baseCommitId` 非空时，编译判定后、调 spec 前执行）

调用方传的 `baseCommitId` 常是需求环境基准（≈ master 实时 tip），而分支可能早已全量合入基线（休眠旧分支、0 独有提交）——这种单没有任何可检增量，spec 整场检查（三张基线表、依赖双树、HTML 渲染）是纯白跑；且两点直差 `git diff <baseCommitId>` 会把基线之后的演进整个**反向**算成"增量"（2026-11-12 taskId 6240 实锤：base=master 当天 tip、分支 tip 停在 11 个月前，diff 546 文件 / +1240/-54813 全是 master 演进的镜像噪音）。clone 已在手，两条命令即可判出，判中直接短路上报，省掉 Step 2 全场。

**判定命令**（clone 目录内；`baseCommitId` 为空时本节整体跳过、不判定）：

```
git merge-base <baseCommitId> HEAD    # 输出分叉点 MB；报错 / 空输出 = 无共同祖先 → 不短路
git status --porcelain                # 有任何输出 = 工作区有未提交改动 → 不短路
```

**短路条件（两条同时满足才短路）**：
1. `MB` 非空 且 `MB == HEAD`（merge-base 等于 HEAD = 分支 0 独有提交，内容已全量在 baseCommitId 里；含 baseCommitId == HEAD 的分支未动场景）；
2. 工作区干净（未提交改动仍是有效增量，不得吞掉）。

**短路动作**：跳过 Step 2（不调 spec、无 HTML 产物），先落盘固定 `spec-findings.json`（单引号定界 heredoc 写纯字面 JSON，供 Step 3 Python 读取；`<短hash>` 字面替换为 Step 1.3 落盘 `COMMIT_ID` 前 8 位）：

```
cat > spec-findings.json <<'JSON_EOF'
{"skill":"spec","scope":"增量","range":"git diff <短hash>（增量空跑短路：merge-base(baseCommitId,HEAD)==HEAD，分支 0 独有提交、已全量在基线中，增量 diff 为空）","passed":true,"rulesChecked":[],"counts":{"blocker":0,"warning":0,"suggestion":0,"tip":0},"findings":[]}
JSON_EOF
```

再直接进 Step 3 上报：`runStatus=success`、`commitId` / `buildStatus` 按 Step 1 落盘值、`specResult` 取上述固定结构（counts 全 0 与空 findings 派生重算一致）、`htmlReport` 缺省（spec 未执行，符合矩阵）、`error` 缺省（空跑是正常结论、不是失败）。最终小结注明「增量空跑短路：分支 0 独有提交（merge-base==HEAD），无增量可检，已上报空增量通过」。

**不短路的一切情况（`git merge-base` 报错 / 空输出 / `MB != HEAD` / 工作区不干净）→ 照常进 Step 2**（fail-open：判定失败绝不拦截检查；spec 侧对非祖先 base 另有 merge-base 归一兜底，两点直差倒退 diff 不会重演）。

---

## Step 2：隐患代码检查

> 前置：Step 1.4 判定**增量空跑短路**时，本步整体跳过（不调 spec、不产 HTML），直接进 Step 3 上报。

### 2.0 前置：spec 不可用 / 执行异常处理

调用 `/wendao-plugin:spec`；若发生下列任一情况，**判定为 spec 阶段失败（无法产出可用结论）**：

- **未注册 / 不可用**：返回「skill 不存在 / 未注册 / 不可用」类错误（当前环境未安装 `wendao-plugin`、该 skill 未注册）；
- **执行异常**：spec 已注册但调用返回错误 / 抛异常 / 无任何可用输出（spec 没跑完、没产出可解析内容或 HTML）。
  > 本 skill 经 Skill 工具调用 spec、**无法为其设定超时**（Skill 工具无 `timeout` 参数）；spec 自身也无执行超时概念。若 spec 长时间无响应，由平台 turn 限制兜底，本 skill 观察到的形态仍是「无可用输出 / 异常」，按本条处理。

处理（两类一致）：
- **直接终止**，不再尝试调用 spec、不走后续解析；
- **先走 Step 3 上报**：`runStatus=spec_unavailable`、`commitId=<有，Step 1 已记录>`、`buildStatus=<Step 1 编译结果>`、`specResult` 缺省、`error={stage:spec, message:<未注册 / 不可用 / 执行异常错误原文，截断>, exitCode:<可选>}`；
- 上报完成后终止；最终输出标「spec 不可用 / 执行异常，隐患检查未执行」，不输出隐患结论。

> 与 2.1 `parseError` 的区分：spec **有输出但解析不出 JSON**（跑完了、只是格式不符）不算本节失败，走 2.1 兜底（`runStatus=success`、带 `raw` 继续上报）；**本节针对 spec 根本没产出可用内容**（未注册 / 异常 / 空），必须终止。

### 2.1 调用 spec 并解析

调用 spec skill。**`args` 必须极简**——只允许三部分，其余一律不塞（spec 在 cwd 自己能取到，塞了反而干扰它）：

```
Skill(
  skill = "wendao-plugin:spec",
  args  = "<specPrompt 原样>" +（baseCommitId 非空时追加：" baseCommitId=<baseCommitId>"）+ " 结果以结构化 JSON 输出，供上报。"
)
```

**`args` 只允许这三部分**：
1. `specPrompt` —— 调用方传入的检查指令，**原样、不加工、不扩写**；
2. `baseCommitId=<值>` —— **仅当 baseCommitId 非空**时追加；为空则完全不提；
3. 「结果以结构化 JSON 输出，供上报」。

**严禁往 `args` 塞**（spec 自己能取，塞了会误导）：
- ❌ 仓库 / 工作区路径（spec 已 `cd` 到仓库，cwd 即仓库根）；
- ❌ 项目类型 / 语言 / 模块结构（spec 自己看 `pom.xml` 等识别）；
- ❌ 分支名 / commitId / branchCommitId（spec 自己 `git status` / `git rev-parse HEAD` 取；HEAD 已是检出 commit）；
- ❌ 模式判断（「全量 / 增量 / 定向」「baseCommitId 为空走全量」等）——**模式由 spec 自识别**，本 skill 不替它决定；
- ❌ 把「baseCommitId 是否为空」这种内部状态写进 args。

✅ 正确（baseCommitId 为空）：`args = "<specPrompt>。结果以结构化 JSON 输出，供上报。"`
✅ 正确（baseCommitId 非空）：`args = "<specPrompt> baseCommitId=<baseCommitId>。结果以结构化 JSON 输出，供上报。"`

> `<specPrompt>` 是**调用方传入**的检查指令（可能是「全量检查」「隐患检查」「只检查 Dockerfile」等），本 skill **原样透传、不加工、不生成**；至于全量 / 增量 / 定向，由 spec 根据 `specPrompt` + cwd 自判断——**本 skill 绝不在 args 里指定模式**。

> spec 自行识别增量 / 全量 / 定向（增量时以 `baseCommitId` 为 diff 基线，HEAD 由 Step 1 检出保证）。本 skill 不判断模式、不建基线分支。

spec 会输出一个 fenced JSON 块（③ 结构化结果），形如：

```json
{
  "skill": "spec",
  "scope": "增量|全量|定向", "range": "如 git diff <baseCommitId>",
  "rulesChecked": [{ "ref": "config.md 平台结构#1", "name": "..." }],
  "passed": true,
  "counts": { "blocker": 0, "warning": 0, "suggestion": 0 },
  "findings": [{ "level": "warning", "severity": "🟡", "file": "...", "line": 1,
                 "ruleRef": "...", "ruleName": "...", "problem": "...", "fix": "..." }]
}
```

- 从 spec 输出中解析出该 JSON 块作为 `specResult`。
- **派生重算 `counts`（四键全覆盖，不采信模型自报计数）**：spec 的 ③ 契约（2026-09 起）已写死计数不变量——`counts` 固定四键 blocker/warning/suggestion/tip、每键 = `findings` 中该 `level` 的条数（与 HTML 同口径），但该计数终归由模型产出并自检，**仍可能数错**（已实际发生：模型把「规则/类别数」当计数报出 `blocker=3,warning=2`，而 findings 实有 blocker 30 条 / warning 9 条，被服务端按 findings 重算校验、整单拒收；旧版契约里 💡 只进 HTML 不进 JSON 的缺口同源）。故**成功解析出 specResult 后**：`counts.blocker` / `counts.warning` / `counts.suggestion` / `counts.tip` 四键一律按 `findings` 中对应 `level` 的**条数确定性重算并覆盖**（`findings` 缺省 / 非数组时全置 0；spec 自报值无论有无、对错都不采信）——口径与 spec 新契约一致（重算即「逐键核对」的确定性实现），同时兜住「旧版 spec 契约未生效」与「新版模型数错」两种情况。这是对 findings 的确定性统计，不是造数据；`parseError` 兜底结构不执行重算。
- `passed` **以 spec 输出为准、原样透传**：本 skill 不按「findings 是否为空」二次计算（spec ③ 契约 2026-09 起正式明确「无 🔴 阻断即通过」——`counts.blocker=0` 即 `passed=true`，🟡/🔵/💡 不影响 passed、照常进 findings/counts，双方口径一致）。
- 解析不到（spec 未按结构化输出）→ `specResult` 置为 `{ "parseError": true, "raw": <spec原文> }`，并在上报体 `error` 记 `stage=spec`，继续上报，不静默丢弃。
- **解析出 `specResult` 后落盘 `spec-findings.json`**：把重算过 `counts` 的 `specResult`（含 `parseError` 兜底结构）写入 clone 工作目录的 `spec-findings.json`，供 Step 3 组装上报体时由 Python 读取。用**单引号定界符 heredoc** 写纯字面 JSON（`cat > spec-findings.json <<'JSON_EOF' … JSON_EOF`）——单引号定界符不展开 `$`/反引号，JSON 里的 emoji、多行、引号、`$` 都按字面写入；**严禁用双引号 heredoc 做 `$SPEC_RESULT` 变量插值、或 `echo "...$specResult..."` 拼 JSON**（那正是 `specResult` 特殊字符破坏结构、连带把 `htmlReport` 截断的根因）。`spec-findings.json` 缺失 / 内容非法时 Step 3 会把 `specResult` 缺省，不阻断上报。
- spec 会**自行生成** HTML 报告 `spec-report-<时间戳>.html`（位于 clone 工作目录）并在结果里告知完整路径，记为 `${HTML_PATH}`（结果未显式带路径时，由 Step 3 在 cwd 按 `spec-report-*.html` 兜底取最新）。**本 skill 不生成 / 不渲染 HTML**，仅读取该产物用于上报。

> 前置依赖：平台需已安装 `wendao-plugin`（提供 `/wendao-plugin:spec`）。

---

## Step 3：结果上报（固定执行）

### 失败上报矩阵

| 失败阶段 | `runStatus` | 是否跑 spec | `commitId` | `buildStatus` | `specResult` | `error` |
|---------|------------|------------|-----------|--------------|-------------|---------|
| 必填参数缺失 / 非法 | `param_invalid` | 否 | 缺省 | `skipped` | 缺省 | `stage=param` + 缺失/非法项 |
| 凭证获取失败 | `token_failed` | 否 | 缺省 | `skipped` | 缺省 | `stage=token` + stderr |
| clone 失败 | `clone_failed` | 否（无代码） | 缺省 | `skipped` | 缺省 | `stage=clone` + stderr |
| branchCommitId 检出失败 | `clone_failed` | 否（无代码） | 缺省 | `skipped` | 缺省 | `stage=checkout` + stderr |
| compile 失败（`isBuild=1` 时） | `build_failed` | 是（静态检查） | 有 | `failed` | 有 | `stage=compile` + stderr |
| spec 未注册 / 执行异常 | `spec_unavailable` | 否（spec 未产出） | 有 | 视编译 | 缺省 | `stage=spec` + 未注册/异常信息 |
| spec 解析失败 | `success` | — | 有 | 视编译 | `parseError=true` | `stage=spec` |
| 增量空跑短路（Step 1.4 判中） | `success` | 否（短路） | 有 | 有 | 有（固定空增量结构） | 无 |
| 上报接口失败 | 不影响 runStatus | — | 有 | 有 | 有 | `stage=report`（仅回显，不进 payload） |
| 全部正常 | `success` | — | 有 | `success` | 有 | 无 |

> `error.message` 抓取该阶段 stderr/异常摘要，**超长截断**（保留末尾 ~2000 字符，编译错误关键信息都在尾部）。`error` 仅失败时出现，永远是对象或不存在，不要传空字符串。**叠加失败时**（如编译失败后又 spec 失败），`error` 记**导致最终 `runStatus` 的那个阶段**（以终止因为准）。
> `htmlReport` = spec 生成的 HTML 报告（`spec-report-*.html`）的 base64；**仅当 spec 实际执行并产出 HTML 时带上**。故未跑 spec 的失败行（param_invalid / token_failed / clone_failed / spec_unavailable）与**增量空跑短路行**（spec 未执行，specResult 为固定空增量结构）`htmlReport` 缺省；spec 跑过的行（success / build_failed / spec 解析失败）按文件兜底也能带上。与 `specResult` 缺省规则不同（`specResult` 在 clone/checkout 失败时整个缺省）。

### 上报体

```json
{
  "reqId": "<reqId>",
  "odinNs": "<odinNs>",
  "taskId": <taskId 可空；数字类型，不带引号>,
  "gitUrl": "<gitUrl>",
  "branch": "<branch>",
  "branchCommitId": "<可空；非空时实际检出该 commit>",
  "baseCommitId": "<可空；非空时为增量基线>",
  "runStatus": "success | param_invalid | token_failed | clone_failed | build_failed | spec_unavailable",
  "commitId": "<实际检出 HEAD；clone/checkout 失败时缺省>",
  "buildStatus": "success | failed | skipped",
  "error": { "stage": "token | clone | checkout | compile | spec", "message": "<stderr/异常摘要，截断>", "exitCode": "<可选>" },
  "specResult": { "<spec 的 ③ JSON，counts 四键为本 skill 按 findings 派生重算（见 Step 2.1）；Step 1.4 增量空跑短路时为固定空增量结构；clone/checkout 失败时整个缺省>" },
  "htmlReport": "<spec 生成的 HTML 报告（spec-report-*.html）的 base64（去换行）；仅 spec 实际产出 HTML 时带上，未跑 spec 的失败行缺省>"
}
```

### 组装并上报（Python json 安全构造，严禁 bash heredoc 拼 JSON）

spec 在 Step 2 已**自行生成** HTML 报告 `spec-report-<时间戳>.html`（单文件自包含，位于 clone 工作目录）。本 skill **不生成 / 不渲染 HTML**——只读取 spec 产物 → base64，与 Step 2 落盘的 `spec-findings.json` 一起，用 **Python `json` 库**安全组装上报体。

> **为什么必须用 Python 而非 bash heredoc 拼 JSON**：`specResult`（spec 结构化结果）含 emoji / 多行 / 引号 / `$` 等特殊字符，若与 `htmlReport`（31KB+ base64）一起塞进 bash heredoc 做 `$SPEC_RESULT` 变量插值，`$SPEC_RESULT` 的特殊字符会干扰变量展开，导致 `htmlReport` 被静默截断（已实际发生：HTML_B64 31176 字节 → payload 仅 16118 字节）。Python `json.dump` 对字符串 / 嵌套对象做确定性序列化，无 shell 展开、无转义陷阱，从根上规避。

```bash
# 1) 定位 spec 的 HTML 报告（优先 Step 2 记下的 ${HTML_PATH}；未记下按文件名取最新）
HTML_PATH="${HTML_PATH:-$(ls -t spec-report-*.html 2>/dev/null | head -1)}"

# 2) 只 export Step 3 当下才确定的动态值（runStatus / error / 文件路径），一律【字面值】——
#    Bash 每次调用独立、环境变量不跨调用持久，严禁写 ${runStatus} / ${ERR_STAGE} 等变量引用
#    （未定义即静默展开为空 → 上报标量全 null，已实际发生）；值含引号/反引号/$ 时注意 shell 转义（单引号串内单引号写作 '\'')
#    入参标量与 commitId / buildStatus 不在此 export——它们已落盘 run-meta.env（Step 1.2.1 / 1.3），由下方 Python 直接读文件
export P_RUN_STATUS="success"          # ← 按失败矩阵字面替换：success / param_invalid / token_failed / clone_failed / build_failed / spec_unavailable
export P_ERR_STAGE=""                  # ← 失败时字面替换：token / clone / checkout / compile / spec；成功留空
export P_ERR_MESSAGE=""                # ← 失败时 stderr 摘要（保留末尾 ~2000 字符）字面替换；成功留空
export P_ERR_EXIT_CODE=""              # ← 可选；成功留空
export P_HTML_PATH="${HTML_PATH}"      # 本次调用内由上面 ls 得到，可以用变量
export P_SPEC_FILE="spec-findings.json"

# 3) Python 安全组装 report_payload.json：
#    标量字段优先读 run-meta.env（Step 1 落盘，跨 Bash 调用可靠），缺项回退本次调用字面值 export 的 P_* 环境变量
#    （无 clone 目录的失败行没有 run-meta.env，全走 P_* 兜底）；
#    json.load 读 specResult（嵌套对象）、base64 读 HTML，json.dump 落盘，全程无 shell 展开
python3 - <<'PY'
import json, os, base64

# run-meta.env：本次 clone 目录（cwd）内的运行元数据，KEY=VALUE 逐行解析（只切第一个 =，不 source、不执行）；
# 文件缺失 / 读失败则 meta 为空，走 P_* 兜底
meta = {}
if os.path.exists("run-meta.env"):
    try:
        with open("run-meta.env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    meta[k.strip()] = v
    except OSError:
        pass

def s(meta_key, env_key):
    v = meta.get(meta_key, "")
    if v == "":
        v = os.environ.get(env_key, "")
    return v if v != "" else None   # 空串 → None（JSON null / 键缺省），与既有语义一致

payload = {
    "reqId": s("REQ_ID", "P_REQ_ID"),
    "odinNs": s("ODIN_NS", "P_ODIN_NS"),
    "gitUrl": s("GIT_URL", "P_GIT_URL"),
    "branch": s("BRANCH", "P_BRANCH"),
    "branchCommitId": s("BRANCH_COMMIT_ID", "P_BRANCH_COMMIT_ID"),
    "baseCommitId": s("BASE_COMMIT_ID", "P_BASE_COMMIT_ID"),
    "runStatus": s("RUN_STATUS", "P_RUN_STATUS"),
    "commitId": s("COMMIT_ID", "P_COMMIT_ID"),
    "buildStatus": s("BUILD_STATUS", "P_BUILD_STATUS"),
}

tid = s("TASK_ID", "P_TASK_ID")
if tid is not None:
    try:
        payload["taskId"] = int(tid)   # 数字类型，不带引号；非数字则缺省，不硬塞字符串
    except ValueError:
        pass

stage = os.environ.get("P_ERR_STAGE", "")
if stage != "":
    err = {"stage": stage}
    msg = os.environ.get("P_ERR_MESSAGE", "")
    if msg != "":
        err["message"] = msg
    code = os.environ.get("P_ERR_EXIT_CODE", "")
    if code != "":
        err["exitCode"] = code
    payload["error"] = err

# specResult：从 Step 2 落盘的 spec-findings.json 读作嵌套对象（缺失 / 解析失败则缺省，不阻断）
spec_file = os.environ.get("P_SPEC_FILE")
if spec_file and os.path.exists(spec_file):
    try:
        with open(spec_file, "r", encoding="utf-8") as f:
            payload["specResult"] = json.load(f)
    except (ValueError, OSError):
        pass

# htmlReport：base64 编码 spec 的 HTML 产物（文件不存在 / 读取失败则缺省，不阻断）
html_path = os.environ.get("P_HTML_PATH")
if html_path and os.path.exists(html_path):
    try:
        with open(html_path, "rb") as f:
            payload["htmlReport"] = base64.b64encode(f.read()).decode("ascii")
    except OSError:
        pass

with open("report_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
PY
```

- **找不到 HTML 不阻断上报**：`htmlReport` 字段缺省，其余字段照常上报。
- **`spec-findings.json` 缺失 / 解析失败不阻断上报**：`specResult` 字段缺省，其余照常（`spec_unavailable` / `parseError` 场景由 `error` 兜底）。
- **严禁本 skill 自建 / 渲染 HTML**：`htmlReport` 必须来自 spec 产物；spec 未产出就缺省，**不得用模板自行生成替代**。
- **严禁把 `specResult` / `htmlReport` 塞回 bash 变量再拼 JSON**：一切组装只经上述 Python `json.dump` 完成；`report_payload.json` 落盘后直接 `curl --data-binary @report_payload.json` 读文件上报，不再经 shell 二次展开。
- **无 clone 目录的失败行（`param_invalid` / `token_failed` / `clone_failed`）**：没有 `run-meta.env`，标量字段改经 `P_REQ_ID` / `P_ODIN_NS` / `P_TASK_ID` / `P_GIT_URL` / `P_BRANCH` / `P_BRANCH_COMMIT_ID` / `P_BASE_COMMIT_ID` 环境**字面值** export 提供（`P_BUILD_STATUS="skipped"`、`P_COMMIT_ID` 留空），Python 模板不变（`run-meta.env` 缺失自动走 P_* 分支）；`report_payload.json` 不落盘——Python 末尾的 `json.dump` 换成 `print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))`，`curl --data-binary @-` 从 stdin 读。

POST 到上报接口（先判断 `${REPORT_ENDPOINT}` 是否配置；用 `--data-binary @report_payload.json` 直接读文件，规避命令行长度与转义问题）：

> ⚠️ `${REPORT_ENDPOINT}` / `${isTest}` / `${routeLabel}` 与 Step 3 export 块同理：**不得引用此前 Bash 调用里的变量**（环境变量不跨调用持久——`REPORT_ENDPOINT` 丢了会静默跳过上报，`isTest` 丢了会漏带路由 header、报错地址）。本块与 Python 组装放**同一次 Bash 调用**内执行，`REPORT_ENDPOINT` 为空时先按 Step 0 逻辑重新 curl `prepare/env` 解析一次（同调用内完成）；`isTest` / `routeLabel` 按 prompt 入参**字面值**判断（`[ "1" = "1" ]`）／写入。

```bash
if [ -z "${REPORT_ENDPOINT}" ]; then
  echo "上报地址未配置（REPORT_ENDPOINT 为空），跳过上报；检查结论与 HTML 报告仍完整展示。"
else
  # isTest=1 且 routeLabel 非空：额外带路由 header，把上报流量路由到 routeLabel 对应的测试环境实例
  ROUTE_HDR=(-H "Content-Type: application/json")
  if [ "${isTest}" = "1" ] && [ -n "${routeLabel}" ]; then
    ROUTE_HDR+=(-H "didi-header-route-label: ${routeLabel}")
  fi
  curl -sS -X POST "${REPORT_ENDPOINT}" "${ROUTE_HDR[@]}" \
    --data-binary @report_payload.json
fi
```

> `isTest=1` 时，此处的 `${REPORT_ENDPOINT}` 已是 Step 0 按测试优先规则解析后的地址（`REPORT_ENDPOINT_TEST` 非空则已被它覆盖）；`isPre=1` 时同理（`REPORT_ENDPOINT_PRE` 非空则已被它覆盖）。

- **REPORT_ENDPOINT 未配置**：跳过 POST、输出日志（「上报地址未配置，跳过上报」），**不影响后续流程**（清理照常）；检查结论与 `specResult` 照常展示，不丢失。
- **路由 header（仅测试环境）**：`isTest=1` 且 `routeLabel` 非空时，POST 额外带 `didi-header-route-label: ${routeLabel}`；`isTest≠1` 时（含 `isPre=1` 预发）即使传了 `routeLabel` 也**不带**（该参数仅测试环境有效，一律忽略）。
- **无条件执行**：无论通过、命中隐患，还是 clone/compile 失败，只要 `REPORT_ENDPOINT` 已配置，都要按矩阵上报。
- **上报体存档（Python 组装即落盘、再 POST——上报失败也有据可查；防并发会话冲突）**：上述 Python 脚本已把完整上报体 JSON `json.dump` 写入本次 clone 目录（cwd）内的 `report_payload.json`；发出 POST 前确认其已生成，POST 用 `--data-binary @report_payload.json` 读该文件。目录名已含 `reqId@分支@时间戳@随机数`，多任务并发天然隔离，不会覆盖别的会话存档；且随 `cleanup` 统一处置（默认随目录一并回收；`cleanup=0` 随目录保留、小结回显路径）。**严禁写到 `/tmp` 等共享目录下的固定路径文件**（无会话隔离，并发任务互相覆盖、误导排查）。无 clone 目录的失败行（`param_invalid` / `token_failed` / `clone_failed`）**不落盘**——payload 无 specResult / htmlReport 大字段、体积小，在小结中回显关键内容即可。
- 记录上报响应（HTTP 状态码 + 响应体），回显给用户。
- 上报本身失败（网络错 / 非 2xx）→ 不重试到死，如实回显「上报失败 + 错误」；**检查结论与 error 照常展示，不丢失**。
- 上报所需的**时间戳 / 操作人 / 额外参数**由平台在调用本 skill 时注入或在此处补齐；spec 只负责产出 `specResult` 本身。
- **上报后清理（默认回收，受 `cleanup` 控制）**：上报完成后——
  - `cleanup` 为空 / `1` / 不传（默认）：离开克隆目录（`cd ..`）并 `rm -rf <fileName>` 删除代码目录（spec 生成的 `spec-report-*.html` 就在其中，一并删除）；
  - `cleanup=0`：**保留** `<fileName>` 目录（含 spec 的 HTML 报告），并在最终小结回显其绝对路径，便于人工排查。
  - 目录/文件不存在则跳过；清理失败仅记录、不影响已上报结果。

---

## 最终输出（给用户）

一段简短小结，至少包含：

- 基本信息：仓库 / 分支 / 目录名 / **commitId** / buildStatus / 检查模式（取自 `specResult.scope`）
- 运行状态：`runStatus`；失败时附 `error.stage` + 错误摘要
- 隐患结论：`passed` + `counts`（blocker/warning/suggestion/**tip** 数，四键均为按 findings 派生重算），列出每条 finding 的 `文件:行号 — 问题（ruleRef）`
- HTML 报告：spec 生成的 `spec-report-*.html` 已读取并以 base64 随 `htmlReport` 字段上报（spec 未产出则标注「HTML 报告缺省」）
- 环境处置：默认已回收 clone 目录（上报体存档 `report_payload.json` 一并删除）；`cleanup=0` 时改为保留并回显 `<fileName>` 绝对路径（含上报体存档 `<fileName>/report_payload.json`）
- 上报结果：HTTP 状态 + 响应摘要；`REPORT_ENDPOINT` 未配置时标「跳过上报（地址未配置）」，上报失败时标「上报失败」并附错误——两种情况下隐患结论与 HTML 报告都仍完整展示
- 测试运行标注：`isTest=1` 时标「**测试运行**（上报地址优先 `REPORT_ENDPOINT_TEST`，未配置回退）」；`routeLabel` 生效时回显「上报带路由 header `didi-header-route-label=<routeLabel>`」，`isTest≠1` 时不出现该标注
- 预发运行标注：`isPre=1` 时标「**预发运行**（上报地址优先 `REPORT_ENDPOINT_PRE`，未配置回退）」，`isPre≠1` 时不出现该标注

---

## 约束

1. **顺序执行**：**参数校验** → 获取凭证 → 环境准备 → 隐患检查 → 上报，不跳步；前置步骤失败按失败上报矩阵处理。**本 skill 为云端自动任务、不与用户交互**：必填参数（`gitUrl` / `specPrompt`）缺失或 `taskId` 非数字时，直接上报 `param_invalid` 并终止，**不追问、不等待补充、不进入后续步骤**。
2. **异常不静默、失败必上报**：**必填参数缺失/非法** / clone / **branchCommitId 检出失败** / compile / **spec 未注册 / 执行异常** / spec 解析 / 上报 任一异常都要进入上报体（`runStatus` + `error`）与最终输出，不得因失败而跳过上报或丢弃错误信息。
3. **上报固定执行**：不受任何开关控制；`REPORT_ENDPOINT` 未配置时跳过 POST、输出日志、不阻断后续（清理照常）；上报失败不影响已完成的检查结论回显。
4. **spec 闭集白名单**：`specResult.findings` 里每条必须有 `ruleRef` 且对应得上 spec 的 reference 规则；不要在本 skill 里额外造规则。`specResult.counts` 四键（blocker/warning/suggestion/tip）一律按 findings 各 `level` 条数派生重算覆盖（见 Step 2.1），**不采信 spec 自报计数**——spec 契约虽已内置计数不变量（2026-09），模型执行仍可能数错（已发生与 findings 不一致被服务端整单拒收），重算是确定性兜底。
5. **检出与增量**：`branchCommitId` 非空时 clone 默认分支 + `git checkout`（忽略 `branch`，不可 shallow clone）；`baseCommitId` 非空时先做 **Step 1.4 增量空跑短路判定**（merge-base==HEAD 且工作区干净 → 分支 0 独有提交，跳过 spec 直报空增量），未短路才**透传给 spec**（spec 自识别增量 / 全量 / 定向模式，增量时以其为 diff 基线——非祖先 base 由 spec 侧 merge-base 归一兜底，HEAD 由 Step 1 检出保证）。本 skill 不判断模式、不建基线分支。
6. **凭证 / 地址外置**：克隆凭证走 `${GIT_CLONE_TOKEN}`、上报地址走 `${REPORT_ENDPOINT}` / `${REPORT_ENDPOINT_TEST}` / `${REPORT_ENDPOINT_PRE}`，统一按三级来源解析（**同名入参 > 平台注入 > `prepare/env`**，见 Step 0）；**不要把凭证值硬编码回 skill 文件**。raw 链接 `${TOKEN_FILE_URL}` 属 skill 自身元信息、非敏感，可内置。
7. **回收环境（默认回收，受 `cleanup` 控制）**：上报完成后默认删除本次 clone 的 `<fileName>` 目录（spec 的 `spec-report-*.html`、运行元数据 `run-meta.env` 与上报体存档 `report_payload.json` 均在其中，一并删）——先离开该目录（`cd ..`）再 `rm -rf <fileName>`，目录不存在则跳过；`cleanup=0` 时改为**保留**目录（含 HTML 报告与上报体存档）并回显路径。清理是辅助动作，失败仅记录、不得改变已上报结果或抛错。
8. **HTML 报告只传不造、组装走 Python**：`htmlReport` = **spec 自行生成的** `spec-report-*.html` 的 base64（在 Step 3 的 Python 脚本内 `base64.b64encode` 读取该文件完成，**不先落 bash 变量再拼 JSON**），由 `json.dump` 填入上报体随 `curl --data-binary @report_payload.json` 上报；`specResult` 同样经 `spec-findings.json` 由 Python `json.load` 读作嵌套对象。**严禁在 bash heredoc 里用 `$SPEC_RESULT` / `$HTML_B64` 变量插值拼 JSON**（特殊字符干扰展开、会静默截断 `htmlReport`）。**本 skill 严禁自建 / 渲染 HTML**——spec 未产出时 `htmlReport` 缺省，不得用模板自行生成替代；缺省不阻断其余字段上报。
9. **配置来源白名单（不得自行发挥）**：本 skill 运行所需的配置定义（克隆凭证 `${GIT_CLONE_TOKEN}`、上报地址 `${REPORT_ENDPOINT}` / 测试环境上报地址 `${REPORT_ENDPOINT_TEST}` 等）只允许从三个来源获取（优先级从高到低）——(1) **同名入参**（非空即最终值，调用方动态覆盖）；(2) **平台注入的环境变量**；(3) 插件自身仓库 `master` 分支的 `prepare/env` 文件（经 Step 0 的 raw 链接 `${TOKEN_FILE_URL}` curl 读取）。**除此之外不得自行发挥、不得去其他文件 / 仓库 / 接口 / 目录猜测或寻找配置来源**；三级全空才视为该配置缺失，按对应失败矩阵上报，而非臆造一个来源去取。
10. **测试 / 预发环境运行（`isTest=1` / `isPre=1`，两者互斥，同时为 `1` 按参数非法处理）**：(1) **配置优先取对应环境版**——所有配置项 KEY 优先解析 `KEY_TEST`（`isTest=1`）/ `KEY_PRE`（`isPre=1`）（按三级来源：同名入参 > 平台注入 > `prepare/env`），当前即 `REPORT_ENDPOINT_TEST` / `REPORT_ENDPOINT_PRE`（`GIT_CLONE_TOKEN_TEST` / `GIT_CLONE_TOKEN_PRE` 将来配置了同样生效），为空 / 未配置回退正式 KEY，**不算失败、不报错**；(2) **路由 header（仅测试环境）**——`isTest=1` 且 `routeLabel` 非空时上报 POST 额外带 `didi-header-route-label: ${routeLabel}`；`isTest≠1` 时（含 `isPre=1`）`routeLabel` 一律忽略（传了也不带 header）。
11. **跨步骤值传递只走文件或字面值（防 shell 变量静默丢失）**：Bash 每次调用是独立 shell，**export 的环境变量不跨调用持久（仅 cwd 持久）**。所有需要跨步骤使用的值——入参标量（Step 1.2.1 落盘 `run-meta.env`）、`commitId` / `buildStatus`（Step 1.3 追加进 `run-meta.env`）、`specResult`（`spec-findings.json`）、HTML 报告（`spec-report-*.html`）——一律**落盘到本次 clone 的 `<fileName>` 目录内**（与代码同目录；**严禁写到 `/tmp` 等共享目录或 clone 目录之外的任何固定路径**——目录名含 `reqId@分支@时间戳@随机数` 天然并发隔离，写目录外会与其他并发任务互相覆盖、串任务数据）；Step 3 当下才确定的 `runStatus` / `error` 经**同一 Bash 调用内的字面值 export**（如 `export P_RUN_STATUS="success"`，值直接写死，禁用 `${变量}` 引用未定义变量）。**严禁在 Step 3 引用此前 Bash 调用里 export 的变量**——未定义变量静默展开为空，上报体标量全 `null`（已实际发生，见 Step 1.2.1 注记）。
