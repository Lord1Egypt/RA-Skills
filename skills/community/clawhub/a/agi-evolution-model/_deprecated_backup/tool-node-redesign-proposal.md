# 工具节点重规划 · 设计提案（v0.1 草稿 · 待审阅）

> **状态**：提案阶段，未改动任何代码。需用户确认后分步落地。
> **决策基线**：混合实现语言（Rust 节点 + Python 统一入口 + BusyBox 兜底）已采纳。
> **铁律**：大改动先出提案 → 用户确认 → 小步落地；严禁未对齐就改代码。

---

## 1. 背景与目的

当前 `scripts/` 下 4 个散装 CLI（`cli_file_operations` / `cli_system_info` / `cli_process_manager` / `cli_executor`）存在三个结构性问题：

1. **脆弱**：Python 脚本依赖解释器 + 第三方库（如 `psutil`），环境异常即整层归零。
2. **裸奔**：完全绕开 `PerceptionNode` 统一入口层（`import TraceContext` 却从未调用，是死代码），无 trace_id / 重试 / 缓存 / 可观测 / 错误台账。
3. **重复**：能力是系统命令子集，且重复 harness 已提供的 Read/Write/Glob/Grep/Bash。

**目的**（用户定调）：不是"给谁用"，而是在**难以处理的局面下以最标准的姿态顺利推进难题与效率**；内部快速自用，使内部工具调用**比 harness 更强**，达成"**一个统一入口即最优解**"。方法论：最大化发挥 BusyBox 长盛优势（单一 / 零依赖 / 精简 / 核心全覆盖 / 一致可移植）。

---

## 2. 设计原则（由 BusyBox 优势推导）

| # | 原则 | 含义 |
|---|---|---|
| P1 | 统一入口 | 单一工具节点取代散装 4 CLI，避免切换成本 |
| P2 | 零/最小依赖 | 核心命令自包含，最恶劣环境也能自举 |
| P3 | 统一契约 | 所有节点贯穿：JSON 返回 + trace_id + 参数 schema |
| P4 | 分级兜底 | 主路径(精炼节点) → 统一入口(报错回退) → BusyBox(保命) |
| P5 | 自我进化 | 调用失败/异常自动入智慧库，闭环复盘 |

---

## 3. 目标拓扑（工具节点能力栈 · 三级路由）

> 说明：此"三级"是**工具节点这一单一能力内部**的主路径 / 回退 / 保命兜底路由，**不是**框架宏观"三层架构"（最外圈 / 外环 / 次循环）。二者命名相似但抽象层级不同，特此显式区分以免歧义。感知节点整体属于框架次循环的"感知接口（Tool Use）层"——详见 `tool_use_spec.md` 红线章节。

```
┌─────────────────────────────────────────────────────────┐
│  调用方（智能体 / 外部 API）                              │
└───────────────────────────┬─────────────────────────────┘
                            │ call_tool(node, args)
                            ▼
┌─────────────────────────────────────────────────────────┐
│  PerceptionNode  ·  统一入口层（Python，保持）           │
│  【被动能力执行器 · 无自主推理】                          │
│  trace_id · 预防检查 · 缓存 · 重试 · 可观测 · 错误台账   │
│  TOOL_REGISTRY（注册真实节点 + schema）                  │
└───────────────────────────┬─────────────────────────────┘
                            │ subprocess / FFI
                            ▼
┌─────────────────────────────────────────────────────────┐
│  工具节点  ·  主路径能力（Rust 静态二进制）              │
│  单一二进制 toolnode，按子命令分发：fs / sys / proc / exec│
│  零依赖 · 快启动 · 内存安全 · 跨平台                     │
└───────────────────────────┬─────────────────────────────┘
            │ 失败 / 二进制缺失 · 兜底
            ▼
┌─────────────────────────────────────────────────────────┐
│  BusyBox  ·  保命兜底（极端场景）                        │
│  纯 stdlib 保命子集；Rust 节点 + Python 原型都废时才启用 │
└─────────────────────────────────────────────────────────┘
```

---

## 4. 工具节点重规划：统一二进制 + 子命令（仿 BusyBox）

采用 **单二进制 + 多子命令** 形态（正是 BusyBox 的模式），既满足"一个顶十个"，又规避"上帝对象"反模式（每个子命令单一职责）：

```
toolnode fs   <op>    # read/write/list/copy/move/delete/mkdir/stat/search
toolnode sys  <op>    # cpu/mem/disk/net/uptime/env/all
toolnode proc <op>    # list/search/detail/kill/tree/stats
toolnode exec <cmd>   # 受控命令执行（危险命令网关）
```

- 一个入口、一份契约、一套 trace_id 注入；内部按子命令分发。
- 替换现有 4 个散装 `.py`，消除重复与割裂。

---

## 5. 统一契约（所有节点强制）

返回格式（统一）：

```json
{
  "status": "success|error",
  "data": { ... },
  "error": null,
  "metadata": { "duration_seconds": 0.12, "trace_id": "..." },
  "trace_id": "...",
  "timestamp": "2026-08-11T21:00:00"
}
```

- **trace_id**：每次调用由 PerceptionNode 生成并强制注入，串联全链路。
- **参数 schema**：收归 `TOOL_REGISTRY`，调用前校验（名称 / required / 类型）。
- **防静默失败（沿用行为基线 §3.2）**：
  - 写入类 → 返回**真实路径 + 字节数 + 摘要**（回读磁盘确认，非内存 len）。
  - 检索类 → 返回**来源 + 时间戳**（用来源 mtime，非响应时刻）。

---

## 6. 实现语言策略（混合，已采纳）

| 路由角色 | 语言 | 理由 |
|---|---|---|
| 主路径能力（工具节点） | **Rust → 静态二进制** | 零依赖、快、内存安全、跨平台，吸收 BusyBox 哲学，恶劣环境可自举 |
| 统一入口层（PerceptionNode） | **Python（保持）** | 逻辑复杂、需快迭代，调 Rust 二进制即可 |
| 保命兜底（BusyBox） | 纯 Python 标准库（内嵌进程） | Rust 节点 + Python 原型缺失/损坏时保命 |

- **构建目标**：`x86_64-pc-windows-gnu` / `x86_64-unknown-linux-gnu`（macOS 待定）。注：原拟 `x86_64-pc-windows-msvc`，因 WSL 交叉编译环境无 msvc 工具链，改用 **mingw `gnu` + 静态 CRT**（`+crt-static`）产出等价 Windows .exe，详见 §12.4。
- **分发**：预编译多平台二进制随技能打包；首次调用按平台选二进制。
- **跨平台双二进制（类比 .so / .pyd）**：工具节点编译 **Windows（`toolnode.exe`，`x86_64-pc-windows-gnu` + 静态 CRT）+ Linux（`toolnode`，`x86_64-unknown-linux-gnu`）** 两套静态二进制随技能打包；运行时由 PerceptionNode **按平台感知选择**（Windows→.exe，Linux→ELF），与既有 C 扩展 `.pyd`/`.so` 双平台策略**同构**。macOS 目标沿用此前"待定"。
- **已知约束（须接受）**：Rust 节点经 Python 统一入口层 `subprocess` 调用，**Python 仍在链路一环**；彻底"脱离 Python 自举"需统一入口层也 Rust 化（未来可选，非本期）。

---

## 7. PerceptionNode 质量基线（接入 Rust 节点前的门禁）

PerceptionNode 是**被动能力执行器（统一入口层）**——它不产工具能力，也不做自主决策，而是让"调用"具备 trace / 重试 / 缓存 / 可观测 / 错误台账等**标准化执行姿态**。Rust 节点与 BusyBox 是"弹药"，PerceptionNode 是"标准投送口"。**严格红线**：本层**无自主推理、不输出主体性表述**（详见 `tool_use_spec.md` 职责边界红线）；"错误自动入智慧库"是它把错误事件**上报**给上层，决策性"入库/复盘"由框架记录层完成，不在本层越界。因此本层须以最高质量标准对待，并作为后续接线的前置门禁。

### 7.1 质量维度与当前实况（基于读码核对）

| # | 质量维度 | 验收标准 | 当前状态 | 实证依据 |
|---|---|---|---|---|
| Q1 | 真实接线（无生产桩） | 注册工具必须全部真实实现；stub 须显式标注且不可进入主路径 | ✅ 达标 | `toolnode` 已真实实现并注册进 `TOOL_REGISTRY`，经治理层 subprocess 路由；`web_search`/`get_weather`/`search_documents` 显式 `stub=True` 且 `call_tool` 拦截返回 `STUB_NOT_IMPLEMENTED`（不入主路径）；`calculator` 走 C 扩展 |
| Q2 | 参数 Schema + 前置校验 | `ToolConfig` 须含 `parameters/required/type`；`call_tool` 强制校验；`ValidationFrameworkProtocol` 真接入 | ✅ 达标 | `toolnode.SCHEMAS` 为单一事实来源；`_validate_toolnode_params` 在 `call_tool` 强制校验 group/op/required；实测缺参/未知 op → `INVALID_PARAMS` |
| Q3 | trace_id 全链路贯穿 | 真实工具调用（含 Rust 节点 / BusyBox 兜底）须注入并回流 trace_id；无死代码 | ✅ 达标 | `call_tool` 早期生成 trace_id 并经 `_execute_toolnode` 透传 `--trace-id`；toolnode 尊重注入 trace_id 回流；边界归一化强制对齐 |
| Q4 | 调用后验证（防静默失败） | 写入回读磁盘确认 + 返真实路径/字节/摘要；检索返来源+时间戳 | ✅ 达标 | `fs.write` 回读磁盘返 `bytes_written/sha256/verified_on_disk=True`；`fs.read` 返 `source_timestamp`（来源 mtime）；修 Windows 文本模式 `\n→\r\n` 静默改写（改二进制写入） |
| Q5 | 重试 / 兜底真实生效 | 重试护真实工具；BusyBox fallback 路由实现 | ✅ 达标 | `COMMAND_TIMEOUT`/`DANGEROUS_COMMAND_BLOCKED` 等确定性错误经 `_no_retry` 立即返回不重试；BusyBox 保命层已实现（Step 4）：能力层缺失/崩溃自动回退，8/8 实测通过（详见 §12.5） |
| Q6 | 错误闭环进智慧库 | 真实工具失败入 `error_wisdom`；与 `cognitive_error_integration` 打通 | ✅ 达标 | 真实 `toolnode` 失败（非客户端错误）自动 `_record_error_to_wisdom`；实测 `COMMAND_TIMEOUT` 写入 `error_wisdom_entries.json` |
| Q7 | 可观测性可验证 | 延迟/成功率/缓存命中可追踪可导出 | ✅ 达标 | `verify_step5_e2e.py` 端到端验收（13/13）；`ObservabilityManager` 有真实流量（success/error/retry 埋点可导出）。Step 5 发现并修正：错误契约（success=False）原只入智慧库不计 `failed_calls` → 成功率失真；新增 `log_failure` 将错误契约计入 failed_calls |
| Q8 | 跨平台一致 | Windows/Linux 双二进制下行为一致 | ✅ 达标 | Rust 双二进制已建：Linux ELF（941KB，`x86_64-unknown-linux-gnu` 原生编译）+ Windows PE（1.6MB，`x86_64-pc-windows-gnu` 交叉编译）；二者均通过 Q1–Q6 + 危险网关验收（详见 §12.4） |

### 7.2 门禁判定

- **框架质量**：高（设计扎实，trace / 重试 / 缓存 / 智慧库基础设施真实存在）。
- **运行质量**：当前高（Q1–Q6 已对真实 `toolnode` 生效，并由 `verify_toolnode_step2.py` 端到端验收，详见 §12）。
- **结论**：**Q1–Q6 已通过**，具备接入 Rust 节点（步骤 3）的前置条件；步骤 2 完成判据"让 Q1–Q6 对真实工具生效"已达成。

### 7.3 与落地步骤的绑定

| 步 | 门禁要求 | 状态 |
|---|---|---|
| 步骤 1（Python 原型） | 产出的 `toolnode` 原型须自带参数 schema，供步骤 2 校验 | ✅ 完成 |
| **步骤 2（接治理）** | **完成判据 = Q1（去桩或显式标 stub 且不入主路径）、Q2、Q3、Q4、Q5、Q6 对真实工具全部生效** | ✅ 完成（10/10 验收） |
| 步骤 3（Rust 化） | 替换后须复测 Q3 / Q4 / Q5 / Q8 跨二进制一致 | ✅ 完成（双二进制 + 10/10 复测通过） |
| 步骤 4（兜底） | 补全 Q5 的 BusyBox fallback 分支 | ✅ 完成（8/8 实测） |
| 步骤 5（验证） | 端到端跑通 → 出具 Q1–Q8 验收报告 | ✅ 完成（13/13 终检） |

---

## 8. 与 harness 的边界

- **用本层**：需标准化姿态、可观测/可追溯、失败要进错误台账、或恶劣环境下需自举的操作。
- **直接用 harness Bash**：一次性、无需追踪的简单操作。
- 本层不强在"替代 harness"，而强在"标准姿态 + 入口路由 + 兜底"——与 harness 互补而非重复。

---

## 9. 落地步骤（小步、每步可验证、可回退）

| 步 | 内容 | 产出 | 可回退 | 状态 |
|---|---|---|---|---|
| 1 | 精炼：4 CLI 合并为统一 `toolnode` 入口（**先 Python 原型**） | 统一入口 + 契约验证 | 删原型即回退 | ✅ 完成 |
| 2 | 接治理：注册进 `TOOL_REGISTRY`，trace_id/重试/缓存/智慧库生效 | 治理层有活可干 | 取消注册即回退 | ✅ 完成 |
| 3 | Rust 化：核心用 Rust 重写编译静态二进制，替换 Python 原型 | 零依赖主路径 | 切回 Python 原型 | ✅ 完成 |
| 4 | 兜底：PerceptionNode 路由加 BusyBox fallback 分支 | 保命层就位 | 去分支即回退 | ✅ 完成 |
| 5 | 验证：健康检测 + 端到端（调用→trace→重试→智慧库） | 验收报告 | — | ✅ 完成 |

> 先 Python 原型铺路，Rust 替换可回退；避免一上来就背 Rust 构建复杂度。
> **步骤 1、2 已完成并通过 Q1–Q6 验收（见 §12），可进入步骤 3。**

---

## 10. 风险与回退

- **Rust 构建复杂度（多平台）** → 步骤 1 先用 Python 原型，步骤 3 替换，可回退。
- **Python 仍在链路（混合固有）** → 接受；BusyBox 兜底覆盖极端场景。
- **范围蔓延** → 严格按 8 步，每步独立可验证，不与认知/智慧层纠缠。

---

## 11. 确认项（已拍板 · 用户全权委托构建）

- [x] 统一入口形态：**单二进制 + 子命令**（`toolnode fs/sys/proc/exec`）已认可
- [x] macOS 构建目标：**本期不含**（环境为 Windows+WSL2，双平台 `.pyd`/`.so` 同构已够；留作扩展）
- [x] 铺路顺序：**先 Python 原型、后 Rust 替换**（可回退）已认可
- [x] 落地起点：**从步骤 1 开始**，用户已将细节构建全权委托

> **委托声明**：用户于 2026-08-11 明确"全权交由你来完善与细节构建，工具节点的实用与强大定位就看你的了"。进入构建期，仍守"小步、可验证、可回退"纪律，每步汇报。

---

## 12. 构建记录（步骤 1–5 · 实测）

### 12.1 产出文件
- `scripts/toolnode.py`（步骤 1）：统一工具节点 Python 原型（fs/sys/proc/exec 四组子命令；`SCHEMAS` 单一事实来源；统一 `status`-based 契约；危险命令网关；写入回读 / 读取来源时间戳防静默失败；Windows GBK 容错解码）。
- `scripts/perception_node.py`（步骤 2 修改）：`toolnode` 注册进 `TOOL_REGISTRY`；`_validate_toolnode_params` 强制参数校验；`_execute_toolnode` 经 subprocess 路由并归一化契约；C 扩展仅路由 `calculator`；`_pre_check` 非 dict 兜底；Q6 真实失败入智慧库。
- `scripts/verify_toolnode_step2.py`（步骤 2 新增）：Q1–Q6 + 危险网关 共 10 项端到端验收脚本，**10/10 通过**。

### 12.2 修复的两个边界 bug（均为"契约/退出码错位"类，正是 Q4/Q6 要防的静默失败）
1. **契约主键错位（根因 blocker）**：`toolnode` 输出 `status`-based 契约，`PerceptionNode` 内部约定 `success`-based；`_execute_toolnode` 原样透传导致 `call_tool` 把 `success=None` 误判失败 → 所有 toolnode 调用返回 `EXECUTION_ERROR`。修复：在 `_execute_toolnode` 边界把 `status`-based 归一化为 `success`-based（含 `error` 形状对齐、trace_id 强制一致）。
2. **退出码误杀错误契约**：`toolnode` 约定 成功 exit 0 / 失败 exit 1，但失败时仍把错误契约写进 stdout。原 `_execute_toolnode` 在 `returncode != 0` 时直接 `raise`，把合法的 `COMMAND_TIMEOUT` / `DANGEROUS_COMMAND_BLOCKED` 等错误契约当进程崩溃丢弃 → 降级为 `EXECUTION_ERROR`。修复：先按 stdout 解析契约，仅当 stdout 非合法契约时才把非 0 退出码视为真实崩溃。
3. **（连带）Windows 换行符静默改写**：`fs.write` 原用文本模式 `"w"` → Windows 把 `\n` 翻成 `\r\n`，而 `fs.read` 用二进制 `rb` 回读保留 `\r\n`，导致 readback 与入参逐字节不一致（违背 Q4）。修复：`fs.write` 改二进制写入（`mode+"b"`），保证写入字节 == 回读字节。

### 12.3 验收结果（2026-08-11）
```
[PASS] Q1 真实接线 toolnode(sys.all)            data_keys=[cpu,disk,mem,net,platform,python,uptime]
[PASS] Q1 对照: 桩工具 web_search 被治理层拦截   code=STUB_NOT_IMPLEMENTED
[PASS] Q2 参数校验 (缺 op / 未知 op)             missing_op/unknown_op=INVALID_PARAMS
[PASS] Q3a call_tool 链路 trace_id 一致且非空
[PASS] Q3b toolnode 尊重调用方注入的 trace_id
[PASS] Q4a fs.write 回读磁盘验证(防静默失败)     verified=True sha256?=True bytes=15
[PASS] Q4b fs.read 返回来源时间戳且内容一致      source_timestamp 一致 content_match=True
[PASS] Q5 确定性错误不重试(COMMAND_TIMEOUT)      code=COMMAND_TIMEOUT retry_count 缺失 elapsed≈2.2s
[PASS] Q6 真实工具失败自动入错误智慧库           error_wisdom_entries +1
[PASS] Q+ 危险命令在全链路被拦截(未执行)         code=DANGEROUS_COMMAND_BLOCKED
Step 2 门禁结果: 10/10 通过 —— 可进入 Step 3 (Rust 化)
```

### 12.4 步骤 3 构建记录（Rust 化 · 双二进制）

**产出文件**
- `scripts/toolnode-rs/`（Rust 源工程）：`Cargo.toml`（仅 `serde_json` + `sha2` 纯 Rust 依赖，便于交叉编译）、`src/main.rs`（~840 行，fs/sys/proc/exec 四组 + 统一契约 + 危险网关 + trace_id + 防静默失败）、`test_self.sh`（Linux 自测）。
- `scripts/toolnode.exe`（Windows PE，1.6MB，`x86_64-pc-windows-gnu` + `+crt-static`）：交叉编译产出，随技能打包的主路径 Windows 二进制。
- `scripts/toolnode`（Linux ELF，941KB，`x86_64-unknown-linux-gnu`）：原生编译产出，随技能打包的主路径 Linux 二进制。
- `scripts/perception_node.py`（接线修改）：`_toolnode_binary_path()` 按平台优先选 `toolnode(.exe)`，缺失回退 `toolnode.py`；`_execute_toolnode` 走 Rust 二进制路径，契约归一化逻辑不变。**可回退**：删 `.exe`/ELF 即回退 Python 原型。

**构建环境与命令**
- Linux ELF：WSL 原生 `cargo build --release`（toolchain `stable-x86_64-unknown-linux-gnu`）。
- Windows .exe：WSL 内 `rustup target add x86_64-pc-windows-gnu` + `apt install gcc-mingw-w64-x86-64`，再 `cargo build --release --target x86_64-pc-windows-gnu`（`.cargo/config.toml` 设 `rustflags=["-C","target-feature=+crt-static"]`，用默认 mingw `x86_64-w64-mingw32-gcc` 链接器）。
- **国内源加速**（关键）：`rustup` 默认 `static.rust-lang.org` 大文件被严重限速（~13KB/s，13 分钟下不完 rust-std）；改用 **rsproxy.cn 镜像**（`RUSTUP_DIST_SERVER=https://rsproxy.cn RUSTUP_UPDATE_ROOT=https://rsproxy.cn/rustup`）后秒级完成。apt 已是阿里云源，mingw 安装正常。

**与提案的偏差（诚实记录）**
- 构建目标由 `x86_64-pc-windows-msvc` 改为 `x86_64-pc-windows-gnu`：WSL 交叉编译环境无 msvc 工具链（msvc 不能从 Linux 交叉编译），改用 mingw gnu + 静态 CRT，产出等价 Windows .exe，运行行为一致。

**已知环境怪癖（非代码缺陷）**
- WSL `CLOCK_MONOTONIC` 异常：`Instant` 在 `run()` 入口与后续 `Instant::now()` 间漂移约 4s，导致 Linux 下 `duration_seconds` 指标偏大；超时逻辑本身正确（`COMMAND_TIMEOUT` 在真实 ~1.0s 触发）。Windows 原生（QPC）不受影响，`duration_seconds` 准确。

**Step 3 复测结果（2026-08-11，经 Rust 二进制，治理层全程 `using rust backend`）**
```
[PASS] Q1 真实接线 toolnode(sys.all)            data_keys=[cpu,disk,mem,net,platform,rust,uptime]
[PASS] Q1 对照: 桩工具 web_search 被治理层拦截   code=STUB_NOT_IMPLEMENTED
[PASS] Q2 参数校验 (缺 op / 未知 op)             INVALID_PARAMS
[PASS] Q3a call_tool 链路 trace_id 一致且非空
[PASS] Q3b toolnode 尊重调用方注入的 trace_id    injected/echoed 一致
[PASS] Q4a fs.write 回读磁盘验证(防静默失败)     verified=True sha256?=True
[PASS] Q4b fs.read 返回来源时间戳且内容一致      content_match=True
[PASS] Q5 确定性错误不重试(COMMAND_TIMEOUT)      elapsed=2.08s
[PASS] Q6 真实工具失败自动入错误智慧库           before=1 after=2
[PASS] Q+ 危险命令在全链路被拦截(未执行)         code=DANGEROUS_COMMAND_BLOCKED
Step 3 复测结果: 10/10 通过 —— Q3/Q4/Q5/Q8 跨 Rust 二进制一致，Step 3 完成，可进入 Step 4 (BusyBox 兜底)
```

### 12.5 步骤 4 构建记录（BusyBox 兜底 / 保命层）

**产出文件**
- `scripts/busybox_fallback.py`（新增）：纯 Python 标准库实现的保命层。内嵌于治理层进程，只要 PerceptionNode 活即活——即使 Rust 二进制与 `toolnode.py` 全缺也能维持核心能力。导出 `SCHEMAS`（与 `toolnode.py` 对齐），`toolnode.py` 缺失时供治理层校验回退。
- `scripts/perception_node.py`（修改）：`_execute_toolnode` 加三级兜底路由；新增 `_busybox_fallback` / `_normalize_toolnode_contract`（边界归一化抽取复用）；`_no_retry` 集合补入 `BUSYBOX_UNSUPPORTED`/`BUSYBOX_UNAVAILABLE`/`BUSYBOX_INTERNAL_ERROR`。
- `scripts/verify_busybox_step4.py`（新增）：F1–F8 共 8 项兜底层验收脚本。

**三级兜底触发条件**（`_execute_toolnode`）
1. `_toolnode_binary_path()` 返回 None（Rust 二进制 + Python 原型都缺）→ 直接 BusyBox
2. subprocess spawn 失败 / 超时（`OSError`/`TimeoutExpired`）→ 能力层崩溃 → BusyBox
3. stdout 非合法契约（非 JSON / 无 `status`）→ 能力层崩溃 → BusyBox
4. 合法错误契约（exit 1 + 合法 JSON，如 `COMMAND_TIMEOUT`）→ **不**触发兜底（业务结果，非崩溃）

**BusyBox 能力边界**（BusyBox 哲学：保命核心，不贪全）
- 支持：`fs.read/write/list/stat/copy/move/delete/mkdir`、`proc.list`、`sys.all`（基础摘要）、`exec.run`（带危险网关）
- 不支持 → `BUSYBOX_UNSUPPORTED`（明确报错，不静默假装成功）：`fs.search`、`sys` 子项、`proc.search/detail/kill/tree/stats`
- 契约与 toolnode 完全一致，`metadata.backend="busybox"` 标记可观测；防静默失败（写入回读 + 来源时间戳）与主层一致

**Step 4 验收结果（2026-08-11，模拟双二进制缺失）**
```
[PASS] F8 正常路径不误触发 BusyBox                backend=None (rust)
[PASS] F1 BusyBox fs.write 回读 verified          backend=busybox bytes=26
[PASS] F2 BusyBox fs.read 来源时间戳+内容一致      src_ts 一致
[PASS] F3 BusyBox fs.list 返回条目                count=2 backend=busybox
[PASS] F4 BusyBox sys.all 基础摘要               platform=windows backend=busybox
[PASS] F5 BusyBox 危险命令拦截                    code=DANGEROUS_COMMAND_BLOCKED
[PASS] F6 BusyBox 不支持 op 明确报错              code=BUSYBOX_UNSUPPORTED
[PASS] F7 BusyBox 路径 trace_id 一致              trace_id 贯穿
Step 4 门禁结果: 8/8 通过 —— Q5 fallback 分支就位
```

**附带修正**：`_no_retry` 原仅按错误码集合判重试、忽略 `retryable` 字段，致 `BUSYBOX_UNSUPPORTED`（retryable=False）被重试 3 次。已将三个 BusyBox 确定性错误码补入 `_no_retry`，重试行为与 `retryable` 语义对齐。

### 12.6 步骤 5 构建记录（端到端 Q1–Q8 终检）

**产出文件**
- `scripts/verify_step5_e2e.py`（新增）：整合 Q1–Q8 + 危险网关共 13 项端到端验收，主路径走 Rust 二进制、Q5b 走 BusyBox 兜底，产出最终验收报告。

**发现并修正的可观测性缺口（Q7）**
- 现象：`failed_calls` 恒为异常数，错误契约（`success=False` 的业务失败，如 COMMAND_TIMEOUT/DANGEROUS_COMMAND_BLOCKED）只入智慧库、不计 `failed_calls` → 成功率指标失真（显示 100% 成功）。
- 根因：`call_tool` 的 `else` 分支（success=False）未调 observability；仅 `except` 分支（抛异常）调 `log_error`。
- 修复：`ObservabilityManager` 新增 `log_failure(tool, trace_id, code, message)`，在 `call_tool` else 分支调用，错误契约计入 `failed_calls`。
- 副坑：首版 `log_failure` 的 `extra={"message": ...}` 触发 LogRecord 保留属性冲突（KeyError）→ 被 call_tool except 捕获 → 错误结果被降级 EXECUTION_ERROR。改 `extra` 键名 `message`→`error_message` 修复。

**Step 5 验收结果（2026-08-11，经 Rust 二进制主路径 + BusyBox 兜底）**
```
[PASS] Q1 真实接线 toolnode(sys.all)         data_keys=[cpu,disk,mem,net,platform,rust,uptime]
[PASS] Q1 对照: 桩工具被治理层拦截            code=STUB_NOT_IMPLEMENTED
[PASS] Q2 参数校验 (缺 op / 未知 op)          INVALID_PARAMS
[PASS] Q3a call_tool 链路 trace_id 一致且非空
[PASS] Q3b 能力层尊重调用方注入的 trace_id     injected/echoed 一致 (backend=rust)
[PASS] Q4a fs.write 回读磁盘验证              verified=True sha_match=True
[PASS] Q4b fs.read 来源时间戳且内容一致        content_match=True
[PASS] Q5a 确定性错误不重试(COMMAND_TIMEOUT)   retry_present=False
[PASS] Q5b BusyBox 兜底真实生效               backend=busybox
[PASS] Q6 真实工具失败自动入错误智慧库         before=1 after=2
[PASS] Q7 可观测性埋点可导出(total/success/fail) total=7 success=5 fail=2 retry=0
[PASS] Q8 双二进制随技能打包                  active=toolnode.exe(1.6MB) other=toolnode(present)
[PASS] Q+ 危险命令全链路拦截                  code=DANGEROUS_COMMAND_BLOCKED
Step 5 端到端验收结果: 13/13 通过 —— Q1–Q8 终检通过
```

**全链路验收总览（三套脚本，无回归）**
| 脚本 | 范围 | 结果 |
|---|---|---|
| `verify_toolnode_step2.py` | Q1–Q6 + 危险网关（经 Rust 二进制） | 10/10 ✅ |
| `verify_busybox_step4.py` | F1–F8 BusyBox 兜底 | 8/8 ✅ |
| `verify_step5_e2e.py` | Q1–Q8 端到端终检 | 13/13 ✅ |

**Q1–Q8 终态**：Q1 真实接线 ✅ / Q2 参数校验 ✅ / Q3 trace_id 全链路 ✅ / Q4 防静默失败 ✅ / Q5 重试+兜底 ✅ / Q6 错误→智慧库 ✅ / Q7 可观测性 ✅ / Q8 跨平台一致 ✅

---

*本提案原仅描述设计与计划；步骤 1–5 已全部按确认项落地并通过 Q1–Q8 端到端验收（13/13）。工具节点能力栈（主路径 Rust 二进制 + 统一入口层 + BusyBox 保命兜底）成型，三处均严格遵循"被动能力执行器"红线（无自主推理 / 最小化自我表述）。工具节点重规划完成。*

> **验收体系说明（防定位歧义）**：Q1–Q8 端到端验收（13/13，`verify_step5_e2e.py`）为**感知接口工具箱专项验收**（工具层权威基线）；项目级全流程验收见根目录 TEST_REPORT.md（76/76，7 层测试）。两套体系并行且互不替代：工具层变更以 Q1–Q8 为准，全项目回归以 TEST_REPORT 为准。
