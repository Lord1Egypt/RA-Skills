# 事实产出器：什么时候跑、怎么跑、输出怎么读

> 本技能自带两个**确定性测量**，由一个零依赖 Node CLI 提供。
> 它们回答的是模型算不准的问题，**不是**「有哪些漏洞」。
>
> 这一页是操作手册：什么情况下必须跑、命令怎么写、输出里哪一节决定你能下什么结论。
> 拿到事实之后「能推出什么、不能推出什么」，看 `fact-contract.md`。

---

## 一、先解决「命令在哪」

CLI **不在技能目录里**，它是本项目的独立程序。按可用性从高到低：

| 情况 | 怎么写 | 备注 |
|---|---|---|
| 已安装 | `euthyna audit …` | `euthyna` 是包声明的命令名 |
| 有本项目检出 | `node <euthyna 仓库>/bin/euthyna.js audit …` | 最常用的形式 |
| 两者都没有 | —— | **把判据标为「不可评估」**，不要手工估算顶上 |

### ⚠️ 一个真实的坑：相对路径只在 euthyna 仓库里成立

`node bin/euthyna.js …` 这种写法**只在当前目录恰好是 euthyna 仓库时**能跑。
审计时你的当前目录是**被审计的项目**，于是：

```
Error: Cannot find module 'D:\axe-core\axe-core\bin\euthyna.js'
```

`history` 有 `--repo`，把仓库路径显式传进去，从任何目录都能跑：

```powershell
node <euthyna 仓库>/bin/euthyna.js history --base <rev> --repo <被审计的仓库>
```

- `--repo` 指的是**被审计的仓库**，不是 euthyna 的路径
- `--base` / `--head` 都相对**被审计的仓库**解析，与当前目录无关
- `--coverage` 没有 `--repo`，把覆盖率文件写成**绝对路径**即可

两条命令都已验证：从 `D:\` 运行、`--repo` 指向另一个仓库，退出码与预期一致。

---

## 二、`history` —— 被删代码的来源

### 什么时候必须跑

| 触发场景 | 对应阶段 |
|---|---|
| 审查一次变更（PR / diff / commit），且**有代码被删除** | 阶段 B |
| 用户问「这次改动有没有把某个防护改弱」 | 阶段 B |
| 需要判断某段代码是不是「曾被移除又加回来」 | 阶段 B |

**只要 diff 里有删除行，就先跑它。** 这不是可选步骤：一个校验被删掉而看着「很干净」的 diff，
正是安全回归最常见的样子，而模型无法对几百行被删代码逐行做 blame 再回溯提交历史。

**通常不必单独跑它** —— `euthyna audit`（见第一节）已经把 history（默认开来源追溯）
和 deps 一次跑完。单独跑 `history` 的场景：换一个 `--base` 重新对比、只要 history 不要 deps。

### 命令

```powershell
# 基础：本次变更删掉的代码来自哪些提交、那些提交像不像安全修复
# （来源追溯默认开启：删除行归属到「最初引入」该内容的提交）
node <euthyna 仓库>/bin/euthyna.js history --base <改前版本> --repo <被审计的仓库>

# 加测「曾被移除又加回来」的行（有探针上限，比基础版慢）
node <euthyna 仓库>/bin/euthyna.js history --base <改前版本> --pickaxe --repo <被审计的仓库>

# 关闭来源追溯，退回 blame 的「最后修改」语义（更快；输出会写明这一点）
node <euthyna 仓库>/bin/euthyna.js history --base <改前版本> --no-origins --repo <被审计的仓库>
```

`--base` 是**改前版本**（PR 的分叉点），`--head` 默认 `HEAD`。
省略 `--base` 时按 `merge-base(<被审的 head>, origin/main)` 推断，并在「范围」那一行标出「推断」、在
「未评估的判据」里加一条 `range-inferred`。推断出的范围**只到分叉点**，看不到更早的历史；
两个引用都解析不出来时报用法错误，不猜 `HEAD~1`。斜杠命令免参数进来靠的就是这条，所以
**看到 `range-inferred` 第一步是确认分叉点对不对**，而不是接受它。
分叉点不确定时用 `git merge-base <目标分支> HEAD` 的结果。

### 归属语义（两个固有近似，已确证≠精确）

`history` 的归属和分类各有一个**写死的近似**，读输出前先知道它们：

1. **归属：默认用 `git log -S` 追「最初引入」；blame 的「最后修改」只是回退。** 一条安全
   修复行如果之后被格式化/重构碰过（移动、复制），blame 会把来源归到最后碰它的那个提交
   ——追引入者正是为了不中这个招。来源追溯用 `git log -S <行内容>` 定位**最初引入**该内容
   的提交；与 blame 不一致时，事实会同时写出两个提交（`detail.blameCommit` = 最后修改、
   `evidence.commit` = 最初引入），并说明「最初引入」。
   追溯只对长度 ≥ 12 字符的行做（太通用的行，-S 会指向整个历史的第一个提交，那不是来源）；
   被追溯的行有探针上限，触顶时剩余行保留 blame 归属并在「未评估的判据」里写明；
   `--no-origins` 显式关闭时同样在「未评估的判据」里写明用的是 blame 语义。
2. **分类：先看提交信息，再看提交 diff，再看被删行本身。** 消息含糊
   （"update utils"）但 diff 动了危险 API、或被删行本身就是安全代码（如
   `if (!authorized) return`）时，都会标 `security`——依据写在
   `detail.classificationBasis`（`message` / `diff` / `deleted-line`）。
   分类偏向宽是有意的：漏掉安全提交比多报更危险。

### 输出长什么样（真实捕获）

```
euthyna-history — 被删除代码的来源归属与安全分类
目标: D:/axe-core/axe-core
范围: 8390a5a9…..397f5fce…

已确证 (8)
  • 本次变更删除了 4 行来自提交 ab877f9d70 的代码，分布在 2 个文件。提交信息：
    "fix(link-in-text-block): don't match style or script text (#3775)"，分类：fix
      证据: lib/checks/color/link-in-text-block-evaluate.js (ab877f9d70)
      复现: git blame --porcelain -L 104,104 -L 114,114 8390a5a9… -- lib/checks/…

⚠ 未评估的判据（缺数据不等于干净）：
  • reintroduction: 未启用 --pickaxe，未检查「被移除又加回」的代码行

已评估的判据：
  • history: 105 条 (euthyna-history)
```

### 怎么读

| 看到什么 | 意味着什么 |
|---|---|
| 「已确证」一节的 `分类：security` | **风险拉到最高**，除非能证明那段代码已无必要 |
| `分类：fix` | 不是安全修复，但**读一眼提交信息本身**——分类器偏向宽，不能只看标签 |
| `分布在 N 个文件` | 证据里那个文件**不包含全部**被删行。不要以为只有这一个文件受影响 |
| 底部的「⚠ 未评估的判据」 | 这一节非空时，**不许**把这次运行读成「查过了没问题」 |
| `已确证 (0)` 且未评估一节为空 | 确实没有删除行。这是一次**完成的测量**，不是失败 |

**不要自己跑 `git blame` 肉眼读提交信息。** 机器判定同一个 diff 跑两次结果一致，人读两次可能不一致。

---

## 三、`coverage` —— 符号调用计数

### 什么时候必须跑

| 触发场景 | 对应阶段 |
|---|---|
| 报告里要写「这个函数**有测试覆盖**」 | 阶段 B / C |
| 报告里要写「这个函数**没有测试覆盖**」 | 阶段 B / C |
| 一条结论的成立依赖「那条路径被测试跑过」 | 阶段 C |

换句话说：**任何关于「测没测过」的话，写之前先跑它。**

### 命令

```powershell
node <euthyna 仓库>/bin/euthyna.js coverage `
  --coverage <覆盖率文件绝对路径> `
  --symbol <符号名> --symbol <符号名>
```

`--symbol` 可重复，一次查多个。加 `--file` 可限定到某个文件。Go profile 另需 `--source`
（见下）。

**五种覆盖率格式都读**（自动识别，无需参数）：

| 格式 | 来源 | 说明 |
|---|---|---|
| c8 / v8-to-istanbul `coverage-final.json` | JS 项目（c8 默认落在 `coverage/coverage-final.json`） | 每文件有 `fnMap` + `f`（调用计数数组） |
| classic istanbul `coverage-final.json` | jest 默认 provider、nyc | 同样的 `fnMap` + `f`，另多一个 `hash` 字段（c8 没有 `hash`），两者走同一条代码路径 |
| coverage.py JSON（format 3） | Python 项目（`coverage json` 产出） | 顶层 `{meta, files}`；`functions` 里「函数名 → 已执行行列表」，**无调用计数**。从未调用的函数仍在列表中且 `executed_lines` 为空 |
| Go `-coverprofile`（文本） | Go 项目（`go test -coverprofile` 产出） | `mode:` 头 + 每区块一行 `路径:起始行.列,结束行.列 语句数 命中数`，**无函数名**。必须加 `--source <模块根目录>`：产出器读源码里的顶层 `func` 把行区间映射回函数 |
| lcov tracefile（文本） | Rust 项目（cargo-llvm-cov / cargo-tarpaulin 产出），gcov / llvm-cov 也产这个格式 | `SF:` 开记录、`end_of_record` 收尾，`FN:<行>,<符号>` 与 `FNDA:<计数>,<符号>` 给出函数名与调用计数（**两段分开出现，不是相邻配对**）；**符号名是 mangled 的**，产出器按 Rust v0 mangling 的 `<十进制长度><名字>` 尾段锚定匹配你写的 `模块::函数` 路径，且绝不落在更长的 `<长度><名字>` 对内——查 `get` 不会答到 `cfg_3get` |

Go 的产出命令（Go 目标）：
```bash
go test ./包路径/ -coverprofile=<绝对路径>.out -run <测试名>
node <euthyna 仓库>/bin/euthyna.js coverage `
  --coverage <绝对路径>.out --symbol <符号名> --source <Go 模块根目录>
```

> Go 专属注意事项（在 act 案例研究中实测）：
> 1. **文件不在 profile 里 ≠ 未执行**——该文件所在的包可能根本没被编译进测试二进制。
>    产出器把这种情况报为「未评估」，绝不当「未被覆盖」。要测到某个包，用
>    `-coverpkg=<包>` 或直接运行对应包的测试。
> 2. profile 路径是模块导入路径（`module/pkg/file.go`）；`--source` 指向含 go.mod 的
>    模块根，产出器据此把导入路径映射回磁盘文件。
> 3. `mode: set` 就够用——两态语义（调用过/从未调用）不需要 `count`/`atomic` 的精确计数。

coverage.py 的产出命令（Python 目标）：
```powershell
uv run --with coverage python -m coverage run `
  --include="*/src/<package>/<file>.py" `
  -m pytest <test-file> -o addopts="" -p no:randomly
uv run --with coverage python -m coverage json -o <输出路径>.json
```

> 两个 Python 专属注意事项（在 crewAI 案例研究中实测）：
> 1. **禁用 xdist**（`-o addopts=""`）——coverage 默认收集不到子进程的 trace，`-n auto`
>    时报告是空的。仓库自带 xdist 默认值时用 `-o addopts=""` 覆盖。
> 2. `--include` 按文件路径限定比 `--source` 对 src 布局更可靠（`--source=包名` 可能报
>    `module-not-imported`）。

覆盖率文件从哪来：项目自己产出就用它。项目不产出覆盖率时，**要么用项目自己的方式跑一次
测试产出它，要么把该判据标为「不可评估」**。

lcov 的产出命令（Rust 目标，本机实测）：

```powershell
# 0. llvm-cov / llvm-profdata 不在 PATH 上，先定位 rustc 自带的那一份
$bin = (rustc --print sysroot) + "\lib\rustlib\x86_64-pc-windows-msvc\bin"
# 1. 插桩构建 + 跑测试
$env:RUSTFLAGS = "-C instrument-coverage"
$env:LLVM_PROFILE_FILE = "<绝对路径>\prof\probe-%p-%m.profraw"
cargo test
# 2. 合并 profraw，再从测试二进制导出 lcov
& "$bin\llvm-profdata.exe" merge -sparse <绝对路径>\prof\*.profraw -o <绝对路径>\probe.profdata
& "$bin\llvm-cov.exe" export --format=lcov --instr-profile=<绝对路径>\probe.profdata `
  "<target\debug\deps\<crate>-<hash>.exe>" --sources src > <绝对路径>\lcov.info
# 3. 查询（lcov 不需要 --source：函数名就在 FN: 行里）
node <euthyna 仓库>/bin/euthyna.js coverage `
  --coverage <绝对路径>\lcov.info --symbol <模块::函数> --file <绝对路径>\src\lib.rs
```

> lcov 专属注意事项（在探针 crate 上实测）：
> 1. **符号名是 mangled 的，本产出器不做 demangle**（本机没有可用的 demangler：
>    `llvm-cov --Xdemangler` 试过 `rust` / `rustfilt` / `llvm-cxxfilt` / `c++filt`
>    四个名字全部报 `could not find the demangler`）。匹配靠 **Rust v0 mangling**
>    （`-C instrument-coverage` 蕴含的版本）的 `<十进制长度><名字>` 尾段编码，
>    所以查询写 `模块::函数`（`split('::')` 后逐段匹配）。每段的名字必须从段边界起算——
>    名字开头、mangling 自己的 `_` 分隔符之后、或已证明的 pair 边界——且绝不落在更长的
>    pair 内部：查 `get` 不会答到 `cfg_3get`。带限定的查询是子序列判定而非路径精确判定。
>    `nested::dup` 只命中 `6nested3dup`，裸 `dup` 会同时命中外层模块里的同名函数——
>    每个命中各自报一条事实并带上自己的 mangled 名。已经 mangled 的查询（`_R`/`_Z` 开头）
>    只做精确匹配，**绝不半解码**。
> 2. **同一个文件可能有多条 `FN:` 指向同一行**（泛型单态化、闭包），这不是重复记录。
>    一个泛型函数实例化两次就是两条事实，各自带自己的 mangled 名。
> 3. `FN:` 行存在而 `FNDA:` 缺失时报「未评估」，**不默认成 0**——凭空造出「从未调用」
>    是这个产出器最不能犯的方向。
> 4. 同一 `SF:` 出现多条记录（或同名多条 `FNDA:`）时**计数求和**；求和不会把非零变零，
>    对唯一可行动的结论（计数为 0）安全。
> 5. 文件不在 tracefile 里报**「未评估」**（llvm-cov / gcov 只为被插桩的目标产记录，
>    `--sources` 还会再过滤一层）——这与 c8 的「文件不在数据里 = 从未执行」刻意相反。
> 6. 认较新的 `FNL:`/`FNA:` 编码时会**明确拒绝**而不是按猜的形状读；`SF:` 路径是绝对
>    路径（Windows 上是带反斜杠的）。
> 7. 规范允许的三种写法照读而不是拒掉：**注释记录**（顶格 `#`）可以在任何位置，而
>    `geninfo --comment` **默认**在顶部写一条；**`KF:` 是 `SF:` 的同义词**；
>    **`FN:<起>,<止>,<名>` 是 gcc 9+ 的形状**，止行丢弃但必须消费掉——否则 `14,` 会粘进
>    符号名，把一个函数拆成「有行号无计数」和「有计数无行号」两条记录，前者随即误报未评估。
>    缩进的 `#` 仍被拒绝。

### 输出长什么样（真实捕获，一次查询命中两种结果）

```
euthyna-coverage — 符号调用计数（只能证伪）

已确证 (1)
  • 符号 cleanup 在本次测试运行中一次都没有被调用（调用计数为 0）
    —— 任何依赖它的行为都没有被执行验证
      证据: …\src\handlers.js:29

无法判定 (1)
  • 符号 checkPermission 被调用了 2 次，但调用计数非零**不能**证明任何特定调用点执行过
    —— 本事实只能证伪，不能证实
      证据: …\src\authz.js:4
```

### 怎么读（本节是整个工具最容易用错的地方）

| 事实 | 能推出 |
|---|---|
| 计数为 0，`status: established` | ✅ **确实没被调用过**。可以据此说「这条路径没有被执行验证」 |
| 计数 > 0，`status: unknown` | ❌ **什么都不能推**。进过这个函数 ≠ 你要问的那个调用点执行过 |

原因在 `fact-contract.md` 里有完整说明：底层覆盖率数据会把**从未执行的调用点报成已覆盖**
（抛出异常之后的直线代码就是典型），所以「已覆盖」这个方向本身不可靠。
**产出器里根本没有「已执行」这个输出，这是刻意的。**

推论：**不要**用「计数非零」去关掉一个「这里没测试」的担忧。要证明确实执行过，
只能靠能真正触达该调用点的演示（阶段 C 的门禁 4）。

---

## 四、退出码：对每个码该做什么

| 码 | 含义 | 你该做什么 |
|---|---|---|
| `0` | 已测量，无安全相关发现 | 继续。**但记得读「未评估的判据」一节** |
| `10` | 已测量，存在 `security` 分类的事实 | **提高优先级**，然后逐条走阶段 C。不要直接当结论 |
| `1` | 用法错误 | 修命令（`--base` 写错、符号名写成空等）。这不是测量结果 |
| **`2`** | **完全无法测量** | **不得当作干净**。要么换测量方式，要么把相关判据标为「不可评估」 |

`2` 与 `0` 的区别是这份契约存在意义的缩影：**没能测量，和测了没问题，是两回事。**

### 会走到 `2` 的常见情形

| 情形 | 输出里的说明 | 处理 |
|---|---|---|
| 目录不在 git 仓库内 | 未评估：不在任何 git 仓库内 | 换到真实仓库，或标不可评估 |
| 覆盖率文件不存在 | 未评估：`ENOENT`，未运行测试 | 产出覆盖率，或标不可评估 |
| 符号名拼错 / 不存在 | 查不到该符号 | 核对符号名；确实不存在就说明它不在测量范围内 |

**这几种都不算「干净」。** 报告里必须把它们写进「未评估的判据」，并说明原因。

---

## 五、把它们接进流程的位置

```
阶段 B（变更面审计）
  ├─ 第一条命令 ────► audit                  → history + deps 一次跑完
  │                                          → 有删除行：结果决定风险是否拉到最高
  ├─ 涉及回归判断 ──► history --pickaxe      → 结果决定是否按「回归」处理
  └─ 要谈测试覆盖 ──► coverage               → 只证伪；计数非零不构成证据

阶段 C（结论面验证）
  └─ 结论依赖「测过没有」──► coverage        → 门禁 4（演示）的真假由它约束
```

**产出器给的是事实，不是裁定。** 它说「这行来自一个安全修复提交」，
**不说**「删掉它就是个漏洞」——后者是阶段 C 的事。

---

## 六、`gate` —— 门禁的程序化校验（不是测量）

`history` / `coverage` 产出事实；`gate` **不测量**，它核对一份审计报告的自我声明
是否符合 6 门禁契约。报告格式见 `SKILL.md` 的「裁定格式」。

```powershell
node <euthyna 仓库>/bin/euthyna.js gate <报告文件>
node <euthyna 仓库>/bin/euthyna.js gate <报告文件> --verify --cwd <被审计仓库>
```

| 看到什么 | 意味着什么 |
|---|---|
| 退出码 `0` | 每条 finding 都带了它该带的证据：TP 有 `path:L123` 证据 + 复现命令 + 影响 + 六门禁全过；FP 有 FAIL 门禁；INCONCLUSIVE 有未评估门禁 |
| 退出码 `10` | 有 finding 被**降级为「观察」**——缺证据 / 缺复现 / 门禁与裁定矛盾。读降级原因，补齐或把结论改成观察 |
| 退出码 `2` | 报告读不了，或里面没有可校验的 finding。**不是干净** |
| `--verify` 的 `复现核验 ✗` | 复现命令真的跑了但没跑通——「说能复现」不算数 |

`gate` 只校验报告自己的话，不去审计目标仓库；所以它不能代替裁定，只保证
拿不出证据的结论不会以已确证的面貌交出去。

---

## 七、已知边界（不要越界使用）

- `history` 的分类器**偏向宽**：漏掉安全提交比多报更危险，所以它宁可把 `fix` 也报出来。
  分类结果是**线索**，提交信息要自己读。
- `history` 的归属**默认追「最初引入」**（`git log -S`，有探针上限，只对 ≥ 12 字符的行做追溯）；
  要退回 blame 的「最后修改」语义用 `--no-origins`（更快，输出会写明）。两个近似都写在本文件「归属语义」一节。
- `history` 只覆盖**被删除的行**。新增的代码它不管（`--pickaxe` 除外）。
- `--graph` 只把上面这些归属**画出来**（Mermaid 源码，不是图片）：范围 → 最后修改者 → 最初引入者。
  它不新增任何测量，也不画严重性——图上只有已测到的状态与行数。这也是契约，不是漏写。
- 图上**没有第二条边不等于内容没被移过**。追溯结果被丢下有两条路：短行（`}`、`return x;`）与
  `--no-origins` 会写成虚线的 `history-origins`；而「来源提交本身没被判为安全相关」是**静默**丢弃，
  图上没有那条边，也没有任何说明。看图谱时把「没有边」当成中性事实，不是清白。
- `coverage` **只能证伪**。见上文。
- `coverage` 依赖调用计数，**不处理动态派发、反射、字符串调用**。
  计数为 0 的结论在存在这些机制时要打折扣。
- `audit` 的两个半边**读的不是同一个东西**：`history` 取 `--base`/`--head` 命名的提交，`deps` 取
  `--repo` 所在**仓库根**当前检出的那份清单（清单只按仓库根查找）。所以判据是**内容**：测到的清单与 `--head` 那份不一致、或在那个提交里根本
  不存在（被 gitignore 的锁文件就是这种），「未评估的判据」里会多一条写明文件名与 `--head` 的理由；
  `code`（`manifest-not-head` / `manifest-unverified`）只在 `--json` 通道上。**看到它就检出到范围的一端再重跑**
  ——声明只保证你不静默踩坑，不会替你把事实测对。
- 两者都**不产出分数、严重性、修复建议**。这是契约，不是遗漏。
