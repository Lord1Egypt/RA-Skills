# better-skill-audit 完整检查规则

## 扫描范围约定

> **必读：每条规则的扫描目标必须遵从以下约定，以消除审计员间的判定差异。**

| 目录/文件 | 扫描内容 | 说明 |
|----------|---------|------|
| `SKILL.md` | 全文扫描 | 触发词、步骤描述、引用路径、护栏声明等 |
| `scripts/*` | **全文扫描（默认）** | 主要执行代码，所有安全/代码规范类规则默认扫描此范围 |
| `references/*.md`、`references/*.json` | **仅用于文件存在性校验（D6-E5/D6-W3）** | 参考文档是知识性内容，**不对其中的 CLI 命令、URL、代码片段做规范性扫描**；例外详见各规则说明 |
| 根目录其他 `.py`/`.sh` 等脚本 | 扫描（参见 D4-W1 目录规范） | 根目录脚本不符合目录规范，同时纳入代码规范扫描 |
| `__pycache__/`、`.git/`、`node_modules/` | 仅 D4-E5 打包规范检查 | 不做代码内容扫描 |

**关键原则**：
- `references/` 里的示例代码、映射表、底层 CLI 降级说明等，是**文档内容**，不触发代码执行类规则。
- 若同一内容既出现在 `scripts/` 又出现在 `references/`，以 `scripts/` 的实际调用为准。
- 被审计 Skill 目录下的 `AUDIT-*.md` 由 better-skill-audit 生成，**一律排除**，不参与任何检查维度。

---

## 防误报通则

> 规则未明确覆盖、或证据不足以下定论的边界场景，统一按本通则处理，**不硬判 ERR/WARN**。

1. **证据不足不硬判**：扫描命中后无法确认是真问题（如无法判断两端字段实际格式、无法判断分支是否可达），标注「⚠️ 待人工确认」并在报告中说明原因，**不计扣分**。
2. **注释/示例/文档不算违规**：仅出现在代码注释、字符串字面量、`references/` 文档、SKILL.md 示例代码块中的可疑模式，不触发代码执行类规则（除非该规则明确说明扫描 SKILL.md/references）。
3. **本 skill 内部模块不算外部依赖**：import / 函数调用先走「三步联立」算法第①步反查本 skill 内，命中即排除（见 D7-W2）。
4. **标准库与已知 PyPI 包直接排除**：os/sys/json/re/pathlib/requests/openpyxl/pandas 等不进依赖归属判定。
5. **适用范围豁免优先**：规则若声明「仅当 Skill 含写操作时适用」「纯文档型跳过」等适用范围，先判范围，不在范围内直接 ✅ 通过，不进入扣分逻辑。
6. **去重不重复计分**：同一代码行被多条规则命中时，按各规则声明的去重约定只计一次（如 D3-E2 token 子项与 D5-E1 共用扫描模式时只计 D5-E1）。

> 目的：保证不同 Agent / 多次执行对同一被审 skill 的判定结果稳定一致，且偏向「不冤枉」。

---

## 目录
- [D1 流程闭环与幂等性（13分）](#d1-流程闭环与幂等性13分)
- [D2 工具与命令规范（10分）](#d2-工具与命令规范10分)
- [D3 可移植性与防御（15分）](#d3-可移植性与防御15分)
- [D4 Skill 可用性规范（21分）](#d4-skill-可用性规范21分)
- [D5 安全与操作风险（21分）](#d5-安全与操作风险21分)
- [D6 代码与文档质量（31分）](#d6-代码与文档质量31分)
- [D7 依赖与体量健康度（4分）](#d7-依赖与体量健康度4分)

---

## 评分体系

**满分 115 分**

| 维度 | 满分 | L1适用满分 | L2(dryRun)适用满分 | 核心问题 |
|------|------|-----------|--------------------|---------|
| D1 流程闭环与幂等性 | 13 | 13 | 13 | 跑起来结果对不对？跑两遍还安全吗？|
| D2 工具与命令规范 | 10 | 10 | 10 | 命令调用是否安全、可审计？|
| D3 可移植性与防御 | 15 | 13（D3-W2跳过） | 15 | 能在别人的环境跑起来吗？|
| D4 Skill 可用性规范 | 21 | 21 | 21 | 用户拿到能不能顺利用起来？|
| D5 安全与操作风险 | 21 | 21 | 21 | 跑完安不安全？高危操作有没有保护？|
| D6 代码与文档质量 | 31 | 31 | 31 | 代码写得对吗？文档说的和代码一致吗？|
| D7 依赖与体量健康度 | 4 | 3（D7-W1跳过）| 4 | 整体架构是否健康、可维护？|
| **合计** | **115** | **112** | **115** | |

> 📊 **分值规则**：①**ERR 全部统一 3 分**——命中即 FAIL，分值无意义，不做伪差异；②**WARN 按真实优先级分 3 档**（高3/中2/低1），分值差异决定用户修复顺序。
> 注：L1 适用满分已扣除跳过项分值（L1 满分实为 112，扣 D3-W2(2) + D7-W1(1)）。L2(dryRun) 吸收 L1 + Hub 校验 + 依赖存在性 + 分支可达性模拟，为最完整深度。**L1/L2 通过线统一 90 分**。

## 设计指导原则

```
能不能跑起来？  → D3 可移植性 + D4 可用性规范
跑起来对不对？  → D1 流程闭环 + D6 代码文档质量
跑完安不安全？  → D5 安全风险
符不符合规范？  → D2 工具/命令规范
整体健不健康？  → D7 依赖体量
```

## 通过标准（双重判定）

各检查深度的实际满分和通过线不同（跳过项不计入满分）：

| 检查深度 | 实际满分 | 通过线 | 跳过项 |
|---------|---------|--------------|-------|
| L1 静态分析 | 112 分 | **≥ 90 分** | D7-W1(1)、D3-W2(2) |
| L2 dryRun | 115 分 | **≥ 90 分** | 无 |

> ⚠️ **L1 满分仅 112**（跳过 D7-W1 Hub 校验、D3-W2 分支模拟等需碰外部系统的项），但**通过线仍统一 90 分**。L2 dryRun 满分 115，通过线同为 90。
> L2 dryRun 只做**只读查询/可达性验证**（验文件存在性、验 env 可达、模拟未命中分支、Hub 查询），**无任何写入/更新操作**。

**判定规则（两个条件同时满足才算通过）**：

| 条件 | 结果 |
|------|------|
| 总分 ≥ 对应深度通过线 **且** 零 ERR | ✅ **通过** |
| 有任何 ERR，**或** 总分 < 对应深度通过线 | ❌ **不通过** |

> WARN 不影响通过/不通过判定，但会拉低总分，间接影响是否达到通过线。

---

## D1 流程闭环与幂等性（13分）

> 核心问题：这次跑完结果正确吗？第二次跑还安全吗？

### D1-E1 写操作后必须有结果验收（3分，ERR，L1）

**适用范围**：仅当 Skill 含有实际写操作（上传文件、调用提交/创建 API、写数据库等）时适用；纯查询/纯分析型 Skill 跳过此项（✅ 视为通过）。

**判定逻辑**：
- 扫描脚本中是否有实际写操作函数调用：`upload_`、`submit_`、`create_`、`requests.post`、`requests.put`、`insert`、`write` 等（注意：仅出现在注释或字符串中不算）
- 确认为写操作类后，检查后续是否有查询验收：`query`、`get`、`verify`、`validate`、`assert`、`status_code`
- 若有写操作但**没有**后续验收查询/校验 → **ERR**

**典型错误**：
```python
upload(file_path)
print("上传成功")  # ❌ 无验收
```

**正确方式**：
```python
resp = upload(file_path)
result = query_result(resp["id"])
assert result["status"] == "OK"
```

---

### D1-E2 写操作执行前必须检查是否已完成（3分，ERR，L1）

**说明**：对有状态/不可重复的写操作，重复执行会导致重复提交、数据错误。

**适用范围**：仅当 Skill 含有**不可幂等的写操作**（提交订单、创建记录、扣款类）时适用；幂等写（upsert、PUT 覆盖）或纯查询 → 跳过（✅）。

**判定逻辑**：
- 若 Skill 包含不可幂等写操作命令/调用
- 执行前无 `query`/`status`/`已完成`/`DONE`/`COMPLETED`/`exists` 检查 → **ERR**

**正确方式**：
```python
status = query_status(item_id)
if status == "COMPLETED":
    print("⚠️ 该操作已完成，跳过执行，防止重复")
    sys.exit(0)
```

---

### D1-E3 异常分支必须阻断后续流程（3分，ERR，L1）

**判定逻辑**：
- 若有明显的外部 IO 操作但无任何错误处理 → **ERR**
- 若有错误处理但捕获后 `pass` 或仅 `print` 而不 `exit`/`raise`/`sys.exit` → **ERR**

---

### D1-W1 流程末尾必须有执行摘要输出（2分，WARN，L1）

**判定逻辑**：检查主脚本末尾是否输出汇总性信息（如「共检查 N 项，通过 X 项」「发送成功 N / 失败 N」「处理 N 条记录」）。

- 含明显批量/多步处理流程但脚本末尾无任何汇总输出 → **WARN**

> 纯单步工具 Skill 不强制摘要，避免误报。

---

### D1-W2 冗余操作 / 无效中转检测（2分，WARN，L1）

**说明**：流程中出现不必要的中转、搬运、重复操作，增加失败点且无实际产出。

**判定逻辑**（Agent 追踪数据流向）：
- 追踪文件/数据：从哪来 → 中间经过什么处理 → 最终去哪
- **典型冗余模式（命中 → WARN）**：
  - 同一存储系统内搬运（A 下载本地 → 再上传回 A）
  - 多步中转下载（A 下载本地 → 传给 B 再下载 → 最终存储）
  - 同一文件在多个步骤重复校验行数/格式
- **不算冗余（✅）**：中间步骤有解压/合并/计算/格式转换等实际产出

---

## D2 工具与命令规范（10分）

### D2-E1 禁止对敏感/受控域名使用裸 HTTP 或 browser 绕过（3分，ERR，L1，可配置）

> ⚠️ **本规则需配置受控域名清单后才生效**。通用版**默认受控清单为空**，本项默认 ✅ 通过。
> 团队若有「必须走 SDK/CLI 门面、禁止裸 HTTP 直连」的内网服务，在
> [references/controlled-domains.md](./controlled-domains.md) 中登记后，本规则对这些域名生效。

**判定逻辑**：当 controlled-domains.md 配置了受控域名时，同时出现以下两类即为 ERR：
- 访问方式：`requests.post`/`requests.get`/`fetch(`/`curl `/`urllib`/`httpx` 或 `browser(`/`web_fetch(`
- 命中任一配置的受控域名（模糊匹配）

> ⚠️ **执行提醒（避免漏扫）**：HTTP 调用必须**整组关键词一起 grep**，不能只搜 `requests.post`。实战中常用 `urllib.request.Request` / `urllib.request.urlopen` 直连，只搜 requests 会漏判。推荐先 `grep -nE "urllib|requests\.|httpx|fetch\(|curl |browser\(|web_fetch\(" {file}` 列出全部，再逐一比对域名。

**修复**：改用团队规定的 SDK / CLI 门面访问受控服务。

---

### D2-W1 动态命令拼接审查（3分，WARN，L1）

**问题**：脚本里用字符串拼接构造 CLI/shell 命令（`cmd = "tool " + user_input`、f-string 拼接外部输入到命令），会**绕过静态命令扫描**，且有注入风险。

**判定**：
- grep `subprocess.*f"|subprocess.*+ |os.system.*+|cmd *= *.*\+|shell=True` 等拼接模式
- 命中且拼接源含外部输入（argv/input/环境变量/文件内容）→ **WARN**：动态命令存在注入/绕过审计风险，建议改用参数列表（`subprocess.run([...])`）而非 shell 字符串拼接

---

### D2-W2 硬编码 URL 必须审查（2分，WARN，L1）

**说明**：脚本或 SKILL.md 中任何硬编码的 URL 都必须被审查，确保在不同环境（不同用户/机器）都能正常访问。

**扫描模式**：`https?://[^\s"'>]+`（非注释/非示例上下文中的完整 URL）

| 情况 | 级别 |
|------|------|
| 无任何硬编码 URL | ✅ 通过 |
| 已配置的受控域名 | 走 D2-E1，不计入本项 |
| 其他内网域名 | **WARN**：确认对应接口可在目标环境调用（含鉴权） |
| 外网域名 | **WARN**：确认外部链接在目标环境可访问，或在 SKILL.md 注明访问前提 |

**修复方向**：内网域名确认调用方式；外网域名确认宿主机网络可达，或在 SKILL.md 中注明访问前提。

---

### D2-W3 跨层命令调用追踪（2分，WARN，L1）

**问题**：脚本通过 `subprocess` 调 shell 脚本、shell 脚本内再调其他命令/工具，这种**跨层套娃调用**静态扫描追踪不到。

**判定**：
- grep 脚本里 `subprocess.*\.sh|os.system.*\.sh|bash .*\.sh` → 找到被调的 shell 脚本
- 进入该 shell 脚本 grep 是否含底层敏感调用（直连接口、未声明的外部工具）→ 命中 → **WARN**：跨层调用绕过规范，建议在 SKILL.md 标注调用链

---

## D3 可移植性与防御（15分）

### D3-E1 禁止硬编码本地绝对路径（3分，ERR，L1）

**扫描模式**：`/home/[a-z0-9_-]+/`、`/Users/[a-zA-Z0-9_-]+/`、`C:\\Users\\`

**例外（不扣分）**：
- Shell/命令行中：`~/.openclaw/workspace/`、`$HOME`、`~`（shell 中自动展开）
- Python 中：`Path.home()`、`os.path.expanduser("~")` — `Path("~/...")` **不在例外内**（Python 不自动展开 `~`，属于无效路径）
- 环境变量引用：`os.environ.get("XXX_WORKSPACE")`、`$XXX_WORKSPACE`

**业务文件路径上下文加强**：
- 当出现「读取数据文件」场景时（命中 `pd.read_excel`/`openpyxl`/`pdfplumber`/`docx.Document`/`open(` 解析），以下路径**即使在 Python 中也算硬编码 ERR**：
  - 任何「具体文件路径」（含文件名+扩展名）的写死，而非用户传参或环境变量
- 修复方向：通过 `sys.argv`、`argparse`、`os.environ.get(...)` 传入。

---

### D3-E2 禁止硬编码环境相关固定值（3分，ERR，L1）

| 类型 | 扫描模式 | 例外 | 级别 |
|------|---------|------|------|
| 硬编码邮箱 | `[a-z0-9.]+@[a-z0-9.]+\.[a-z]+` 出现在赋值语句 | 注释/示例不计 | ERR |
| 硬编码 Token | `token\s*=\s*["'][a-zA-Z0-9]{20,}` | 从 config 读取不计；与 D5-E1 共用扫描模式，命中时**不重复计分** | ERR |
| **硬编码 IP 地址** | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` 赋值语句 | localhost/127.0.0.1/0.0.0.0 不计 | ERR |
| **硬编码端口号** | `:\d{4,5}` 出现在 URL/连接串上下文 | 443/80/8080/3000 等通用端口不计 | WARN |
| **硬编码主机名** | `host\s*=\s*["'][^"']+["']` | 从环境变量/配置文件读取不计 | ERR |
| **硬编码系统绝对路径** | `/app/` `/opt/` `/data/` `/etc/` `/var/` `/root/` 赋值 | 非 `/home/`（D3-E1 已覆盖）；`/tmp/` 仅 WARN | ERR |

> ⚠️ **去重规则**：D3-E2 的「硬编码 Token」与 D5-E1 使用相同扫描模式，同一代码行触发两条规则时，仅按 **D5-E1** 计，D3-E2 的 token 子项不重复计分。

---

### D3-E3 禁止列索引硬编码（3分，ERR，L1）

**扫描**：
- pandas：`\.iloc\[.*,\s*\d+\]`、`row\[\d+\]` 在 Excel/CSV 解析上下文
- openpyxl：`ws.cell(row=..., column=N)`、`ws.cell(column=N)` 中 N 为硬编码数字
- 行索引取值：`row[N]`、`data[N]`、`vals[N]`、`cells[N]`、`columns[N]` 中 N ≥ 10（两位数以上，排除常见循环索引 0/1/2）

**表头映射豁免（关键，降误报）**：命中行的**前 30 行**范围内若出现以下任一，视为已做列名映射，**不报风险**：
- `col_map`、`COLUMN_MAP`、`col_index`、`REQUIRED_COLS`、`get_col`、`_build_header_map`
- `header` + `enumerate` 组合、`列名→索引`/`列名匹配` 中文描述

**判定**：命中硬编码模式且无表头映射上下文 → **ERR**（布局表增删列即静默读错）；注释行排除。

**正确方式**：`col_idx = df.columns.get_loc('原币金额')`

---

### D3-W1 共享脚本禁止在多 Skill 下维护副本（2分，WARN，L1）

同一文件名出现在 3+ 个 Skill 目录下 → **WARN**，建议建立 `skills/shared/scripts/` 公共目录。

---

### D3-W2 分支可达性模拟（2分，WARN，L2 dryRun）

> ⚠️ **只读模拟，绝不实跑被审 skill**。审计器对提取出的分支做**只读可达性验证**（文件存在性、env 配置可达性），覆盖「未命中分支」。**严禁 spawn 子会话运行被审 skill**。

**判定逻辑（L2 dryRun 执行）**：
1. **提取分支**：从 SKILL.md（if/否则/不存在/分支判断表）和脚本（`if not os.path.exists`、`elif`、`else`、Bash `if [`）提取所有条件分支
2. **只读模拟未命中分支**：
   - **文件存在性分支**：分支引用的文件路径，审计器用 `os.path.exists` 验证 → 不存在时检查 SKILL.md/脚本是否有对应处理逻辑；**无处理逻辑 → WARN**（文件不存在时会崩）
   - **环境分支**：分支提到 env/不同环境，审计器 grep 脚本是否有对应环境的 URL/配置映射 → **某环境无映射 → WARN**（换环境会失效）
3. **只验可达性，不执行业务逻辑**：审计器只跑 `os.path.exists`、grep 等无副作用命令
4. 输出每个分支的「命中/未命中（模拟）」+ 可达性结论

---

### D3-W3 错误提示可操作性（2分，WARN，L1）

**问题**：脚本捕获异常/报错时只输出「失败/出错/error」等**无指引信息**，用户拿到报错不知道下一步怎么办。

**判定**：
- grep `except.*:\s*(print|raise).*("失败"|"出错"|"error")` 等裸报错且无后续指引文案
- 命中比例高（关键 except 块多数只报「失败」无方案）→ **WARN**：错误提示缺可操作指引，建议补「失败原因 + 修复方向」

---

## D4 Skill 可用性规范（21分）

> 核心问题：用户（含非技术背景）拿到这个 Skill，能不能顺利用起来？

### D4-E1 SKILL.md frontmatter 必须完整（3分，ERR，L1）

缺少 `name` 或 `description` 字段，或无 frontmatter → **ERR**

**version 字段子项（WARN，不计入 D4-E1 的 3 分 ERR）**：frontmatter 缺少 `version` 字段 → **WARN**。
说明：`name`/`description` 是硬性 ERR；`version` 仅部分发布渠道要求，缺失不影响 skill 运行，故降为 WARN 提示补全。

---

### D4-E2 description 必须包含触发时机（3分，ERR，L1）

长度 < 30 字符，或不含触发动作词（`当`、`使用`、`用于`、`当用户`、`Use when`）→ **ERR**

---

### D4-E3 必须有前置条件说明（3分，ERR，L1）

**说明**：Skill 必须告诉用户「跑这个 Skill 之前需要做什么」。

**判定逻辑**：在 SKILL.md 全文中扫描以下任一关键词即视为有前置条件说明：
- 结构关键词：`前置条件`、`Prerequisites`、`前提`、`使用前`
- 依赖描述：`依赖`、`需要安装`、`需要配置`、`需先完成`、`必备环境`、`需要权限`
- 明确豁免：`无特殊前置条件`、`无依赖`、`开箱即用`

无任何上述关键词 → **ERR**（即使没有依赖，也必须明确写「无特殊前置条件」）

---

### D4-E4 必填参数缺失时必须有明确提示（3分，ERR，L1）

**判定逻辑**：
- 扫描脚本中 `sys.argv`、`argparse`、`input()` 的参数读取逻辑
- 若必填参数为空/缺失时直接 `KeyError`/`IndexError` 崩溃，无友好提示 → **ERR**

**正确方式**：
```python
if len(sys.argv) < 2:
    print("❌ 缺少必填参数：目标文件路径")
    print("用法：python3 run.py <file_path>")
    sys.exit(1)
```

---

### D4-E5 打包文件必须规范（3分，ERR，L1）

**扫描范围**：递归扫描 Skill 目录，**排除** `AUDIT-*.md`。

> **关于 `__pycache__` 的判定**：打包工具一般已自动排除 `__pycache__`，且 Python 对 `.pyc` 完全容错，故 `__pycache__` 是**打包规范问题而非运行安全问题**，降级为 **WARN**。

**ERR 级别（真正阻断运行或破坏安全的文件）**：

| 文件/目录 | 原因 | 级别 |
|----------|------|------|
| `.git/` | 版本控制历史，可能泄露提交记录和凭证 | ERR |
| `node_modules/` | JS 依赖包，体积可能极大，导致安装失败 | ERR |
| `*.zip`、`*.tar.gz` 中的打包产物 | 递归嵌套打包 | ERR |
| `*.log`、`*.tmp` 含敏感信息的文件 | 可能泄露 Token、接口返回、用户数据 | ERR |

**WARN 级别（不影响运行，但影响规范性）**：

| 文件/目录 | 原因 | 级别 |
|----------|------|------|
| `__pycache__/`、`*.pyc`、`*.pyo` | 本地运行缓存，打包时已自动排除 | WARN |
| `.gitignore`、`.DS_Store` | 开发辅助文件，无实际危害 | WARN |
| 无敏感内容的 `*.log`、`*.tmp` | 轻量临时文件 | WARN |

**关于 sign.key**：若存在，**不触发 ERR 也不触发 WARN**。`sign.key` 是发布时自动生成的签名验证文件，不含私钥，是标准打包产物。

**关于 AUDIT-*.md**：若存在，提示用户清理，**不触发 ERR 也不触发 WARN**（审计残留，下次打包自动排除）。

---

### D4-W1 目录结构规范（2分，WARN，L1）

- 脚本文件（`.py`、`.sh` 等）位于根目录而非 `scripts/` → **WARN**
- 文档引用文件（`.md`，除 SKILL.md 外）散落在根目录 → **WARN**

---

### D4-W2 高风险操作必须有护栏声明（3分，WARN，L1）

Skill 含写操作但 SKILL.md 无 `禁止`、`NEVER`、`必须`、`MUST`、`严格禁止` 等护栏内容 → **WARN**

---

### D4-W3 关键步骤有进度反馈（1分，WARN，L1）

**说明**：长时间无输出会让用户以为卡死。

**判定逻辑**：
- 脚本中存在 `time.sleep(>30)`、轮询等待、大批量操作循环
- 无任何 `print`/`logging` 进度输出 → **WARN**

---

### D4-W4 错误提示可操作性（已合并至 D3-W3，不另计分）

> 检查项已合并至 D3-W3 中统一处理。

---

### D4-W5 模糊指令扫描（提示项，不另计分，L1）

**说明**：很多 Skill 是「Agent 内判型」（无脚本，靠 SKILL.md 指挥 Agent 执行）。SKILL.md 里若出现让 Agent 行为不可预测的模糊措辞，会导致同一指令每次执行结果不一致。

**判定逻辑（Agent 阅读 SKILL.md 正文）**：
- 扫描模糊指令措辞：`合理判断`、`酌情`、`酌情处理`、`按需调整`、`适当处理`、`一般情况`、`视情况`、`灵活处理`、`自行决定`、`根据实际情况`
- 命中后判断该措辞是否出现在**关键执行步骤 / 判定条件 / 写操作分支**上：
  - 出现在关键步骤的判定条件里 → 报告中标注 **建议明确化**（高优先级提示）
  - 出现在非关键的辅助说明里 → 轻提示或忽略

**输出形式**：在报告中以「🟡 模糊指令提示」列出命中的措辞 + 所在步骤 + 改进建议，不扣分。

---

## D5 安全与操作风险（21分）

### D5-E1 禁止明文存储敏感凭证（3分，ERR，L1）

扫描赋值语句中的敏感模式：
```
password\s*=\s*["'][^"']{3,}
secret\s*=\s*["'][^"']{3,}
token\s*=\s*["'][a-zA-Z0-9]{20,}
api_key\s*=\s*["'][^"']{10,}
```

**例外**：`os.environ.get(...)` 或从配置文件读取不计。

---

### D5-E2 高风险操作禁止硬编码 `--yes` / 强制确认直通（3分，ERR，L1）

写操作命令中直接硬编码 `--yes`/`--force`/`-y`（非用户确认后动态追加）→ **ERR**

**例外场景（以下情况不触发 ERR）**：

| 场景 | 判据 | 原因 |
|------|------|------|
| 全自动化编排脚本 | SKILL.md 中明确说明「本 Skill 为自动化流程，由上层编排触发，无交互确认」且同文件有其他保护机制 | 无 TTY 场景下 `input()` 无法使用 |
| 查询类命令 | `query`、`list`、`get`（纯读操作） | 查询不产生数据变更 |
| 已有外层 pre-check 且结果明确 | 执行前有状态检查，仅当状态为特定可执行值时才继续 | 前置校验已代替人工确认 |

**正确方式（交互式场景）**：
```python
confirm = input("确认执行？(y/n): ")
if confirm.lower() == 'y':
    run("tool action --yes")
```

---

### D5-E3 URL 中禁止硬编码凭证（3分，ERR，L1）

**扫描模式（任一命中即 ERR）**：

| 模式 | 示例 |
|------|------|
| URL userinfo 部分 | `http://user:pass@host` |
| URL 查询参数含凭证 | `?token=xxx` / `?api_key=xxx` / `?password=xxx` / `?secret=xxx` |
| Authorization header 直接拼接 | `"Authorization: Bearer " + "hardcoded_token_xxx"` |
| requests/httpx 的 `auth=("user","pass")` 字面量 | `auth=("admin", "123456")` |

**例外（不触发）**：
- 从环境变量读取：`os.environ.get("API_TOKEN")`
- 从配置文件读取：`config["token"]`
- 占位符/示例标注：`<your-token-here>`、`${TOKEN}` 等

---

### D5-W1 批量操作必须有上限保护（3分，WARN，L1）

循环结构中的写操作调用无 `size`/`limit`/`MAX_BATCH` 限制 → **WARN**（推荐上限 ≤ 30 条）

**覆盖规则**（以下情况视为「已有保护」，不触发 WARN）：

| 覆盖方式 | 判据 |
|---------|------|
| SKILL.md 护栏声明 | SKILL.md 中有 `禁止`/`NEVER`/`严格禁止` 护栏且明确提及批量上限 |
| 代码层显式限制 | 脚本中出现 `size`/`limit`/`MAX_BATCH`/`batch_size` 赋值，值 ≤ 30 |
| 分页遍历有终止条件 | 循环有 `total_count` 上限判断或 `max_page` 限制 |
| 调用方已限流 | SKILL.md 说明由编排层控制并发 |

---

### D5-W2 写操作前必须有确认环节（3分，WARN，L1）

**说明**：仅限可交互式对话场景。纯脚本/非交互式（无 TTY、无 input()）场景不检查。

**判定逻辑**：
- Skill 含写操作命令（提交、上传、删除等）
- 脚本中存在交互式界面（`input()`、确认提示词等），但写操作前无任何确认逻辑 → **WARN**

> 纯自动化脚本（无 TTY）自动跳过该项检查。

---

### D5-W3 配置文件明文凭证扫描（3分，WARN，L1）

**问题**：D5-E1 只扫**脚本赋值语句**里的明文凭证，不扫配置文件内容（config.json / .env / *.yaml）。

**判定**：
- 扫 `{skill}/` 下所有 `.json/.yaml/.yml/.env/.ini/.toml` 文件内容
- 匹配 `token|secret|password|api_key|access_key` 等键且值为非占位明文（非 `<...>`、非 `${...}`、非空）→ **WARN**：建议改为环境变量注入或运行时拉取

---

### D5-W4 HTTP 批量写操作审查（3分，WARN，L1）

**问题**：直接调 HTTP 接口做批量写（`requests.post` 循环、批量 insert API）无上限保护。

**判定**：
- grep `for .*requests\.(post|put|patch)|requests\.(post|put).*for |batch.*insert|bulk.*write` 等 HTTP 批量写模式
- 命中且无 `len(...) <= N` / `MAX_` 上限判断 → **WARN**：HTTP 批量写无上限保护，建议加批量上限

---

## D6 代码与文档质量（31分）

> 核心问题：代码写得对吗？文档说的和代码做的一致吗？

### D6-E1 脚本语法正确（3分，ERR，L1）

```bash
# Python
for f in $(find {skill-path}/scripts -name "*.py" 2>/dev/null); do
  python3 -m py_compile "$f" 2>&1 || echo "SYNTAX ERR: $f"
done

# Shell
for f in $(find {skill-path}/scripts -name "*.sh" 2>/dev/null); do
  bash -n "$f" 2>&1 || echo "SYNTAX ERR: $f"
done
```

任意文件语法错误 → **ERR**。无脚本文件时视为通过。

---

### D6-E2 逻辑完整性缺陷（3分，ERR，L1）

Agent 阅读代码判断：

| 缺陷类型 | 示例 |
|---------|------|
| 函数部分分支无 return，调用方使用返回值 | `def get_amount(): if cond: return 100` （else 缺 return）|
| 关键业务变量赋值后从未使用 | `total = calc()` 但下面用的是 `amount` |
| 条件判断逻辑反转 | `if not data: process(data)` |
| 死代码（return 后仍有执行语句）| `return result; print("done")` |

---

### D6-E3 关键边界未处理（3分，ERR，L1）

| 边界类型 | 风险 |
|---------|------|
| None/空值未检查，API 返回值直接使用 | `amount = data["amount"] * rate`（data 可能为 None）|
| 除零未保护 | `avg = total / count`（count 可能为 0）|
| 列表/字典直接访问无长度检查 | `records[0]["amount"]`（records 可能为空）|
| Excel/JSON 字符串直接参与数值运算 | `total += row["金额"]`（可能是字符串）|
| `open(path)` 前无文件存在性检查 | FileNotFoundError 崩溃 |
| HTTP 请求无 timeout；while True 无退出条件 | 永久挂起 |
| HTTP 调用后**不检查响应状态码**，直接用返回体 | 把失败响应（4xx/5xx/网关错误页）当成功，数据静默错误 |

**HTTP 响应状态码子项判定**：扫描 `requests.get/post`、`httpx`、`urllib`、`fetch(` 等调用，若调用后**未**出现 `raise_for_status()`、`status_code`/`resp.status` 判断、或 `resp.ok` 检查，就直接解析/使用返回体（`resp.json()` / `resp.text`）→ **命中本子项**。把网关 5xx 错误页或登录跳转页当成业务数据，会导致静默错误。

无法判断时标注「需人工复核」，不强行扣分。

---

### D6-E4 SKILL.md 描述的功能步骤必须有对应实现（3分，ERR，L1）

**说明**：SKILL.md 里写了「Step 3：自动上传」，但脚本里找不到对应逻辑，这是描述与实现不一致。

**适用范围**：仅当 Skill 包含脚本文件时适用；纯文档型 Skill（无 `.py`/`.sh` 文件）→ 跳过此项（✅ 视为通过）。

**判定逻辑**（Agent 判断）：
- 提取 SKILL.md 中的步骤列表（Step N / 第N步 / 数字序号）
- 逐一在脚本中查找对应的实现代码，允许同义词映射：
  - 上传 ↔ upload、submit、post
  - 查询 ↔ query、get、fetch、list
  - 生成 ↔ generate、create、build、render
  - 校验 ↔ validate、verify、check、assert
- 若步骤描述过于模糊（如「自动处理」、「执行操作」）无法映射 → 跳过该步骤（转由 D4-W5 模糊指令扫描捕获）
- 若有具体动作描述的步骤在脚本中**完全找不到**语义对应的代码 → **ERR**

**示例命令/参数一致性子项（WARN，不计入 D6-E4 的 3 分 ERR）**：
- 提取 SKILL.md 中的命令示例（` ```bash ` 代码块、`python3 xxx.py --arg` 调用样例）
- 与脚本实际接受的参数（`argparse` 的 `add_argument`、`sys.argv` 解析）逐一比对
- 若示例里的**参数名/子命令/脚本路径**在脚本中不存在或拼写不一致 → **WARN**

---

### D6-E5 SKILL.md 引用的必须文件路径必须存在（3分，ERR，L1）

**判定逻辑**：

1. 从 SKILL.md 中提取所有相对路径引用（`scripts/`、`references/`、`assets/` 开头的路径）
2. 判断该路径是否「必须」— 路径前有「必填/必须/required/need/依赖/务必」等关键词
3. **必须文件不存在 → ERR**
4. **非必须文件不存在 → WARN**（见 D6-W3）

---

### D6-E6 跨表/跨源字段格式兼容性（3分，ERR，L1）

**说明**：两表/两源做 join / 字段匹配 / 规则筛选时，两端数据格式不兼容会导致**所有行静默不命中且不报错**——典型如规则列是 `100201 民生银行`（code_name 拼接），数据列只有 `100201`（code_only），匹配结果全空但程序正常退出。

**判定逻辑**（Agent 阅读代码 + 采样判断）：
- 扫描脚本中两个数据源的字段匹配逻辑：`merge`、`join`、`isin`、`== `、`in [`、`map(`、字典 key 查找
- 检查参与匹配的两端字段是否做了格式归一化（`.strip()`、`.split()[0]`、正则提取、统一去掉中文名）
- 若两端字段来源不同（一个来自配置/Excel，一个来自 DB/接口）且**无显式格式对齐处理** → **ERR**
- 无法判断两端实际格式时 → 标注「需人工采样核实」，不强行扣分

---

### D6-E7 关键列解析后必须做格式校验（3分，WARN，L1）

**说明**：读取 Excel/CSV 关键列（日期、金额、编码等）后未做显式格式验证就直接用于计算，上游文件格式变化时会静默产生错误。

**判定逻辑**：
- 扫描取值模式：`df.iloc[...][col]`、`row["金额"]`、`ws.cell(...).value`、`data[col]` 后直接参与运算/拼接
- 检查取值后是否有格式校验：`re.fullmatch`/`re.match`、类型断言（`isinstance`、`float(x)` 带 try）、范围检查、`datetime.strptime`
- 关键列（含「日期/期间/金额/编码/code/period/amount」语义）取值后**无任何格式校验**直接使用 → **WARN**

---

### D6-W1 代码完整性（2分，WARN，L1）

- `# TODO`、`# FIXME`、`# HACK` 出现在脚本中
- `def xxx():` 后仅有 `pass` 或 `...`（非抽象基类）
- `"TODO"`、`"替换这里"` 等占位字符串未替换
- 硬编码测试数据遗留（`test`、`fake`、`mock` 出现在变量赋值中）
- SKILL.md 中无任何示例（输入参数示例、预期输出示例）→ 缺少使用说明

---

### D6-W2 依赖工具版本有声明（2分，WARN，L1）

**判定逻辑**：
- 依赖第三方 Python 包（如 `pandas`、`openpyxl`）但无 `requirements.txt` 或版本说明 → **WARN**
- 依赖外部 CLI 工具但 SKILL.md 中无最低版本说明 → **WARN**

---

### D6-W3 SKILL.md 引用的非必须文件路径缺失（3分，WARN，L1）

**判定逻辑**：SKILL.md 中引用的相对路径（`scripts/`、`references/`、`assets/`），不含「必须」等强约束词，且实际文件不存在 → **WARN**

---

### D6-W4 大代码量缺测试覆盖（3分，WARN，L1）

**判定**：
- `find {skill} -name "*.py" | xargs wc -l` 总行数 ≥ 2000
- 且 `find {skill} -name "test_*.py" -o -name "*_test.py"` 为空、无 TEST.md → **WARN**：建议为核心脚本补冒烟/回归测试

---

## D7 依赖与体量健康度（4分）

> 核心问题：整体架构是否健康、可维护？

### D7-W1 Hub 发布状态（1分，WARN，L2 dryRun）

从 frontmatter 提取 `name`，通过可用的 Hub 查询工具校验：
- 已发布 → 通过
- 未发布 → **WARN**：上线前请完成发布
- Hub 工具不可用 → 标注「无法校验」，降级 WARN，不中止审计

---

### D7-W2 依赖 Skill 清单与健康度（2分，WARN，L1 提取 + L2 dryRun 存在性验证）

**第一步：精确提取依赖来源**

逐类扫描，识别被审 skill 真实依赖了哪些其他 skill。**Python import 这一类不能只看 `from X import` 行**——模块名 X 本身不暴露它属于哪个 skill，必须走「三步联立 + 反查归属」算法（见下）。

| 依赖类型 | 扫描模式 | 示例 |
|---------|---------|------|
| 跨 skill Python import | 走下方「三步联立」算法 | `from query_app import load_token` → 反查归属 |
| subprocess 调其他 skill 脚本 | `skills/<x>/scripts/*.py`、`<skill_root>/scripts/xxx.py` 路径拼接 | |
| 外部 CLI 工具型 skill | SKILL.md 中声明的外部 CLI 工具 | 归档/取数依赖 |
| SKILL.md 显式声明 | frontmatter `metadata.requires`、正文「依赖 xxx skill」「需先安装 xxx」 | 文档声明 |

#### 🔑 Python import 归属判定：三步联立 + 反查（核心算法）

> **背景**：`from query_app import load_token` 里的 `query_app` 是**模块名**，不是 skill 名。可能是①本 skill 内部模块、②某邻居 skill 的模块、③真正的第三方 PyPI 包。只看 import 行无法区分，会误报或漏报归属。

对每个 `from X import ...` / `import X`（X 为非标准库、非已知 PyPI 包的可疑模块名），按顺序判定：

```
① 本 skill 内反查
   在 {skill-path}/scripts/ 下找 X.py 或 def X(...)：
     grep -rln "^\(def \|class \)X\b" {skill-path}/scripts/   # 同名函数/类
     find {skill-path} -name "X.py"                            # 同名模块文件
   找到 → X 是【本 skill 内部模块/函数】→ ❌ 不算外部 skill 依赖，跳过

② 看 sys.path 注入 / skill_root 拼接（确定归属哪个 skill）
   找 import X 同文件里有没有：
     sys.path.insert(0, ... skills/<y>/scripts ...)
     <y>_skill_root = ... / "skills" / "<y>"
   有，且 X.py 确实在 skills/<y>/scripts/ 下 → X 归属【skill <y>】→ ✅ 真外部依赖

③ workspace 范围反查归属（②没线索时兜底）
   grep -rln "^\(def \|class \)X\b\|/X\.py" ~/.openclaw/workspace/skills/*/scripts/
   命中唯一 skill <z> → X 归属【skill <z>】→ ✅ 真外部依赖
   命中多个 → ⚠️ 归属歧义，标「疑似依赖，归属待人工确认」
   零命中 → ⚠️ 标「非 skill 依赖（疑似 PyPI/动态），不计入 skill 依赖」，不硬判
```

> ⚠️ 去重 + 排除误报通则：
> ①正文里「参考/类似 xxx skill」等**非调用**语境不算依赖；
> ②本 skill 内部同名模块/函数不算（已由①拦截）；
> ③ `try/except ImportError` 包裹的跨 skill 动态 import 是**标准写法**，照常计入依赖但标注「软依赖（import 失败有兜底）」；
> ④标准库与已知 PyPI 包直接排除。

**第二步：为每个依赖标注用途**（Agent 阅读上下文判断「依赖它做什么」）

**第三步：存在性验证（L2 dryRun 执行）**
- 本地 `ls ~/.openclaw/workspace/skills/<dep>/SKILL.md` 存在 → **本地已装 ✅**
- 本地无、Hub 有 → **Hub 有未装 ⚠️**
- 本地无、Hub 也查不到 → **找不到 ❌**

**判定**：
- 依赖数量 ≥ 5 个 → **WARN**，逐一分析：核心依赖 / 可内嵌 / 建议拆分
- 依赖了「找不到 ❌」的 skill → **ERR**（运行必崩）
- 依赖了「Hub 有未装 ⚠️」的 skill → **WARN**
- 无论几个依赖，都在报告「六、Skill 依赖」章节输出完整清单

---

### D7-W3 Skill 体量合理（1分，WARN，L1）

满足以下任一 → **WARN**，给出拆分方向建议：
- 脚本文件 ≥ 10 个
- 代码总行数 ≥ 5000 行（`wc -l` 统计脚本文件）

---

## 已知局限

以下场景当前规则集未覆盖，标记为后续版本方向：

| 场景 | 影响 | 建议 |
|------|------|------|
| 非显式声明的运行时网络依赖 | 当前仅 D2-W2 WARN 级覆盖 | 若出现安全事件，考虑通过 controlled-domains.md 升级为 ERR |
| 多语言混合 skill 的深度静态分析 | 当前以 Python/Shell 为主 | JS/TS 仅做语法+清单层面检查 |
