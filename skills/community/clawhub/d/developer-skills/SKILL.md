---
name: developer-skills
description: 开发者十二铁律 + 开发规范 + 高级调试方法论 — 开发者核心技能（合并自 diagnose）
version: 1.0.0
author: 尘天
license: MIT
tags: [developer, karpathy, iron-rules, clean-code, best-practices]
---

# 开发者十二铁律 + 开发规范

面向 AI 辅助开发场景的实用编码准则，可根据项目需要选择性采纳。

---

## 🧠 十二铁律

### 1. Think Before Coding（先思考再动手）
- 明确说出假设
- 不确定就问，别猜
- 有歧义时列出多种解读
- 存在更简方案时主动提出
- 困惑时立即停止并指出不明之处

### 2. Simplicity First（极简优先）
- 用最少代码解决问题
- 不做 speculative 功能
- 不添加需求外的特性
- 一次性代码不做抽象
- 写完自问：资深工程师会说这"过度设计"吗？是就简化

### 3. Surgical Changes（外科手术式改动）
- 只改必须改的代码
- 只清理自己造成的问题
- 不"顺手优化"无关代码、注释、格式
- 不重构没坏的代码
- 严格匹配现有代码风格
- 🔴 **不越权操作**：用户让"检查状态"≠"清理掉"。只做明确被要求的事。不要自作主张删除/修改/清理不相关的资源（cron jobs、配置、文件等）——哪怕你觉得它们"过时了"或"有问题"。用户没说删，就不删。

### 4. Goal-Driven Execution（目标驱动执行）
- 先定义"完成标准"
- 循环迭代直到验证通过
- 不盲从步骤，紧盯目标
- 清晰的成功标准让你能独立闭环

### 5. Use the model only for judgment calls（模型只做判断）
- 让 AI 做：分类、起草、总结、提取
- 不让 AI 做：路由、重试、确定性转换
- 代码能算的，就让代码算

### 6. Token budgets are not advisory（Token 预算是硬约束）
- 接近预算时，先摘要再重启
- 主动上报超限，不静默超标

### 7. Surface conflicts, don't average them（暴露冲突，不折中）
- 出现矛盾模式时，选一个（更新/更可靠）
- 说明理由
- 标记另一个待清理
- 不混 conflicting 写法

### 8. Read before you write（先读再写）
- 改代码前，先读导出、调用方、公共工具
- "看起来无关"很危险
- 不确定历史原因就先问

### 9. Tests verify intent, not just behavior（测试验证意图，非仅行为）
- 测试要体现"为什么重要"，不只"做了什么"
- 业务逻辑变而测试仍能过，就是坏测试

### 10. Checkpoint after every significant step（关键步骤必留检查点）
- 每完成一大步就摘要：已做、已验证、剩余
- 不继续在无法复述的状态上工作
- 混乱时停下重述

### 11. Match the codebase's conventions, even if you disagree（遵守现有规范）
- 项目内：规范 > 个人偏好
- 真有害时，先提出，不私下另起一套

### 12. Fail loud（失败要大声）
- 静默跳过任何步骤，都不算"完成"
- 跳过测试，就不能说"测试通过"
- 默认暴露不确定性，不隐藏

#### 🔴 Pitfall: `patch` tool 会破坏 Python 原始字符串中的转义序列
使用 `patch` 工具编辑包含 `r'...'` 原始字符串的 Python 代码时，转义序列会被错误处理：
- `\n`（原始字符串中表示正则的换行符）被替换为**真换行符**，导致字符串断裂
- `\\` 被加倍为 `\\\\`，破坏正则表达式

```python
# 原始代码
re.sub(r'[<>:"/\\|?*\n\r]', '_', name)

# patch 工具处理后（损坏）
re.sub(r'[<>:"/\\\\|?*\n\n\n]', '_', name)  # ← \n 变成真换行，字符串断裂
```

**修复方法：** 发现 patch 后语法错误时，用 Python 脚本直接重写受影响的行：
```python
with open('script.py', 'r') as f:
    lines = f.readlines()
# 找到并替换损坏的行
lines[start:end] = correct_lines
with open('script.py', 'w') as f:
    f.writelines(lines)
```

**规则：** 编辑含 `r'...'` 原始字符串的 Python 代码时，优先用 `terminal` + Python 脚本修改，避免 `patch` 工具的转义问题。修改后必须用 `py_compile` 验证语法。

#### 🔴 Pitfall: reqwest 0.13 breaks `.query()` API and `Client` type path
reqwest 0.13 (released 2026) introduces breaking API changes:
- `.query(&[("key", "val")])` method removed from `RequestBuilder` — use `.form()` or manual URL encoding
- `Client` type may not be found in scope if using `use reqwest::Client` (re-export path changed)
- `resp.text().await` return type changed — `str` (unsized) instead of `String`

**Fix:** Pin to reqwest 0.12.x in Cargo.toml:
```toml
reqwest = { version = "0.12.15", features = ["json"] }
```

If you must use 0.13, adapt the code:
```rust
// reqwest 0.12 (works):
use reqwest::Client;
let resp = client.get(url).query(&[("api_key", &key)]).send().await?;
let text = resp.text().await?;

// reqwest 0.13 (broken):
// .query() doesn't exist on RequestBuilder
// resp.text() returns Result<str, _> (unsized)
```

**Rule:** When `cargo build` reports "method not found in `RequestBuilder`" or "type `Client` not found", check `Cargo.toml` reqwest version first.

#### 🔴 Pitfall: Rust E0382 — Moved value used across match arms
When a `String` is consumed (moved) in one match arm, it can't be used in another arm of the same match, even if only one arm executes. This happens in XML/JSON parsers where the same `text` variable is shared across nested match blocks.

```rust
// ❌ E0382: text moved in "type_pid" arm, then used in "vod_id" arm
match current_tag.as_str() {
    "type_pid" => { cls.insert("type_pid".into(), Value::String(text)); }  // text moved
    // ...
}
if in_video {
    match current_tag.as_str() {
        "vod_id" => { item.insert("vod_id".into(), Value::String(text)); }  // ERROR: text used after move
    }
}

// ✅ Clone in the first match block, move in the second
match current_tag.as_str() {
    "type_pid" => { cls.insert("type_pid".into(), Value::String(text.clone())); }  // clone
    // ...
}
if in_video {
    match current_tag.as_str() {
        "vod_id" => { item.insert("vod_id".into(), Value::String(text)); }  // OK: text still owned
    }
}
```

**Rule:** When a variable is used in multiple exclusive code paths (match arms, if-else branches), clone in earlier paths and move in the last one.

#### 🔴 Pitfall: Rust E0133 — Unsafe function calls need `unsafe` blocks
Calling an `unsafe fn` requires the call site to be inside an `unsafe` block, even if the caller is already in an `unsafe` context. This is a common error when loading dynamic library symbols.

```rust
// ❌ E0133: unsafe function called outside unsafe block
fn load() -> Result<Self, MpvError> {
    let create = Self::resolve_symbol(&lib, "mpv_create")?;  // ERROR
}

// ✅ Wrap all unsafe calls in a single unsafe block
fn load() -> Result<Self, MpvError> {
    let (create, initialize, free) = unsafe {
        (Self::resolve_symbol(&lib, "mpv_create")?,
         Self::resolve_symbol(&lib, "mpv_initialize")?,
         Self::resolve_symbol(&lib, "mpv_free")?)
    };
}
```

**Rule:** When batch-loading FFI symbols, wrap all `resolve_symbol` calls in one `unsafe` tuple destructuring. This keeps the unsafe scope minimal and clear.

#### 🔴 Pitfall: append 代码后产生重复函数定义
向 Rust 文件末尾 append 新函数时，如果旧版本未删除，会导致重复定义编译失败。常见于迭代修复时"加了增强版但忘了删旧版"。

**症状**：`cargo check` 报 `the name `xxx` is defined multiple times`

**安全移除方法**：用 Python 脚本精确删除旧函数（避免 patch 工具的转义问题）：
```python
from hermes_tools import terminal, read_file, write_file

result = terminal("cat path/to/file.rs")
content = result['output']

# 精确定位旧函数的起止位置
old_start = "/// 旧函数注释\n#[command]\npub async fn old_fn("
old_end = '    Ok(serde_json::json!({...}))\n}'

idx_start = content.find(old_start)
idx_end = content.find(old_end, idx_start) + len(old_end)

new_content = content[:idx_start] + content[idx_end:]

# 验证：新函数数量应为 1
assert new_content.count("pub async fn old_fn(") == 1

write_file("path/to/file.rs", new_content)
```

**规则**：编辑含重复函数的 Rust 文件时，优先用 `terminal` + Python 脚本精确删除旧版本，不要用 patch 工具。删除后用 `cargo check` 验证编译。

#### 🔴 Pitfall: HTTP response body size check is bypassable via chunked transfer
Adding a `Content-Length` pre-check + post-read length check (`resp.bytes().await` then `if bytes.len() > MAX`) does NOT prevent OOM. If the server omits `Content-Length` (chunked transfer) or lies about it, `resp.bytes().await` reads the **entire** response into memory before the check fires. A malicious source can send GB of data through a small `Content-Length`.

```rust
// ❌ DANGEROUS: entire body in memory before size check
let bytes = resp.bytes().await?;  // ← OOM if body is 5GB
if bytes.len() > MAX_SIZE { return Err("too large"); }

// ✅ SAFE: limit reads during download
let mut stream = resp.bytes_stream();
let mut total = 0usize;
let mut buf = Vec::new();
while let Some(chunk) = stream.next().await {
    let chunk = chunk.map_err(|e| e.to_string())?;
    total += chunk.len();
    if total > MAX_SIZE { return Err("too large".into()); }
    buf.extend_from_slice(&chunk);
}

// ✅ ALSO SAFE: reqwest built-in limit
let bytes = resp // .take() truncates at limit
    .bytes()
    .await?;
// (reqwest bytes() still reads all — use the stream approach above)
```

#### 🔴 Pitfall: `str.replace()` 静默失败 — 必须验证替换结果
`str.replace(old, new)` 找不到 `old` 时**不报错**，直接返回原字符串。这导致"修复已应用"但实际文件未变。

```python
# 危险：marker 不存在时静默失败
content = content.replace("// marker not found", new_code)  # ← 没生效但无报错！

# ✅ 必须验证替换是否生效
old_len = len(content)
content = content.replace("// marker", new_code)
if len(content) == old_len:
    raise ValueError("替换未生效！marker 不存在于文件中")
```

**规则：每次 str.replace() 后必须验证结果**——比较长度、搜索新内容、或检查 marker 是否存在。适用于所有文件编辑场景（本地编辑、API 上传前编辑）。

#### 🔴 Pitfall: `read_file()` 返回带行号前缀，不可直接 `write_file()` 回写
`hermes_tools.read_file()` 返回的 `content` 字段格式为 `    86|    86|export const ...`（行号 + 竖线 + 行号 + 竖线 + 内容），直接 `write_file()` 回去会破坏源文件，导致 `error TS1109: Expression expected`。

```python
# ❌ 危险：read_file content 带行号前缀，写回去破坏文件
from hermes_tools import read_file, write_file
data = read_file('app.ts')
write_file('app.ts', data['content'])  # ← 文件被破坏！

# ✅ 正确：用 Python 标准库直接读写
with open('app.ts', 'r') as f:
    content = f.read()
# ... 修改 content ...
with open('app.ts', 'w') as f:
    f.write(content)
```

**规则：** 需要精确修改文件内容时，始终用 Python 标准库 `open()` 而非 `read_file()` + `write_file()`。`read_file()` 只用于**阅读和分析**，`patch` 工具用于小改动，`open()` 用于需要精确控制的大块修改。

#### 🔴 Pitfall: SQLite WAL 模式冲突导致 disk I/O error
当数据库已存在 `.db-wal` 文件、数据库损坏，或进程异常退出后重新连接时，直接执行 `PRAGMA journal_mode=WAL` 可能触发 `sqlite3.OperationalError: disk I/O error`。

```python
# ❌ 危险：无条件设置 WAL，可能与遗留 WAL 文件冲突
async def connect(self):
    self.conn = await aiosqlite.connect(self.db_path)
    await self.conn.execute("PRAGMA journal_mode=WAL")  # ← 可能报错

# ✅ 安全：先查询当前模式，仅在非 WAL 时才设置
async def connect(self):
    self.conn = await aiosqlite.connect(self.db_path)
    cursor = await self.conn.execute("PRAGMA journal_mode")
    row = await cursor.fetchone()
    if row and row[0].lower() != "wal":
        await self.conn.execute("PRAGMA journal_mode=WAL")
    await self.conn.execute("PRAGMA foreign_keys=ON")
```

**规则：** 在 `connect()` 中设置 WAL 前，先读取当前 `journal_mode`。修复损坏数据库时应先备份，然后删除旧数据库及其 `-wal`/`-shm` 文件，再重新初始化。

#### 🔴 Pitfall: 调度/容器环境中 Python venv 缺少 pip/activate 导致环境无法使用
在集群/容器/定时任务环境中，项目的 venv 可能只有 python 解释器链接，而没有 `pip` 和 `activate` 脚本。此时 `source .venv/bin/activate` 会报 `No such file or directory`，直接使用系统 pip 又会触发 `externally-managed-environment` (PEP 668)。

**安全诊断**（不依赖 `lsof`/`ss`）：
- `ls -la .venv/bin` 确认 `pip`/`activate` 是否存在
- `/opt/data/home/.../.venv3/bin/python3 -c "import sys; print(chr(10).join(sys.path))"` 查看 site-packages 路径
- `/proc/net/tcp` 查看端口占用：端口 8080 对应 16 进制 `1F90`，`state=0A` 表示 LISTEN

**uvex/uvicorn 恢复**——用系统 pip 装到 venv 的 site-packages：
```python
import subprocess
proc = subprocess.Popen(
    ['/usr/bin/python3', '-m', 'pip', 'install',
     '--break-system-packages',
     '--target=/path/to/.venv3/lib/python3.13/site-packages',
     'uvicorn'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
stdout, stderr = proc.communicate(timeout=120)
```

**yun验证** (`terminal`/`execute_code` 返回 -1 时，直接用 `subprocess` 更可靠)：
```python
import subprocess
subprocess.run(
    ['/path/to/.venv3/bin/python3', '-c',
     'import uvicorn; print(uvicorn.__version__)'],
    capture_output=True, text=True, check=True
)
```

**规则：** 在自动化/调度任务中不要依赖 `source .venv/bin/activate`；始终使用 venv 解释器的绝对路径，用 `subprocess` 直接调用系统 pip 并将缺失组件安装到 venv 的 site-packages 下。

#### 🔴 Pitfall: FastAPI / Starlette TemplateResponse 缺少 `request` 键
Starlette 的 `Jinja2Templates.TemplateResponse` 签名在较新版本中已统一为 `TemplateResponse(name, context)`，其中 `context` 必须包含 `"request"` 键。旧的 `TemplateResponse(request, name, context)` 三参数调用会导致模板上下文缺失或类型错误。

```python
# ❌ 错误：旧版签名或缺少 request
return templates.TemplateResponse(request, "index.html")
return templates.TemplateResponse(request, "index.html", {"fund": fund})

# ✅ 正确：新版签名，context 必须包含 request
return templates.TemplateResponse("index.html", {"request": request})
return templates.TemplateResponse("fund_detail.html", {
    "request": request,
    "fund": fund,
    "score": score,
})
```

**规则：** 修改 `main.py` 或任何模板路由后，启动后端并用 curl 访问一次页面路由（如 `/`、`/fund/{code}`）验证模板渲染不报错。`HTTP 500` 且日志为 `TemplateResponse() takes ...` 或 `KeyError: request` 时，优先检查此签名。

#### 🔴 Pitfall: 数据采集脚本写入表结构与 models.py 不一致
当项目同时存在 `database/models.py` 的规范 Schema 和采集脚本中内嵌的旧版建表 SQL 时，两者会互相覆盖，导致 API 查询失败、外键约束错误或数据字段丢失。

```python
# ❌ 危险：采集脚本自建简化表，与 models.py 不一致
# models.py 中 fund_info 有 14 个字段，但 run_collection.py 里只有 5 个字段
# 结果：API 查询 f.risk_level / f.manager_name 等字段全部为空或报错
```

**正确做法：**
1. 删除旧数据库（先备份为 `.db.bak`），用 `models.py` 的 `Database` 重新初始化；
2. 删除采集脚本中的自定义 `CREATE TABLE` 逻辑，改为复用 `Database.connect()` + `Database.init_tables()`；
3. 把采集脚本中的插入 SQL 改为调用 `Database` 的 `upsert_fund_info()` / `upsert_nav()` / `upsert_score()` 或 `execute_many()`；
4. 小范围测试（如 `MAX_FUNDS=10`）后，用 `PRAGMA table_info(table)` 验证字段数量。

**规则：** 永远只保留一份 Schema 真相源。如果 `models.py` 是真相源，所有采集、迁移、测试脚本必须通过它初始化数据库，禁止各自建表。

#### 🔴 Pitfall: 外键约束失败说明基础表不完整
在基金/股票等金融数据项目中，`fund_nav` 表通常对 `fund_info(fund_code)` 有外键约束。如果 `fund_info` 只采集了前 N 条，而 `fund_open_fund_rank_em` 等数据源按收益排名返回的基金代码可能不在前 N 条中，写入 `fund_nav` 时就会报 `FOREIGN KEY constraint failed`。

```python
# ❌ 危险：基础表只采部分，下游数据源顺序不同导致外键失败
await collect_fund_list(db, max_funds=10)  # 只有 10 条
await collect_returns_to_nav(db)           # 可能写入第 11 名之后的基金

# ✅ 正确：基础表完整采集，下游仅写入已存在的基金
await collect_fund_list(db)  # 全部基金
await collect_returns_to_nav(db, max_funds=10)  # 只写入前 10 条
```

**规则：** 对于带外键约束的 Schema，先完整采集被引用表（如 `fund_info`），再采集引用表（如 `fund_nav`、`fund_score`、`fund_holding`），并限制引用表只写入基础表中存在的记录。遇到 `FOREIGN KEY constraint failed` 时，先检查被引用的父表是否完整。

#### 🔴 Pitfall: 容器/调度环境无 systemd/systemctl 时如何做常驻服务
当容器 PID 1 为 `tini`（或其他 init）、无 `systemctl` 、无特权访问时，无法真正启用 systemd。此时不能只是报告"无法完成"，而应该：
1. 仍按标准格式准备好 systemd service 文件（放在 `/tmp` 和 `~/.config/systemd/user/` 供后续有权限时部署）。
2. 同时写一个 **supervisor 守护脚本** 作为等效方案：进程退出后自动重启（`Restart=always` 的等效），并将子进程输出落盘。
3. 用 `terminal(background=true)` 启动守护脚本，让服务持续运行。

```python
# supervisor 示例：spot_cache_service_supervisor.py
import os, subprocess, sys, time
SCRIPT = "/opt/data/home/fund-radar/spot_cache_service.py"
PYTHON = "/opt/data/home/fund-radar/.venv3/bin/python3"
RESTART_SEC = 5

def start():
    return subprocess.Popen(
        [PYTHON, SCRIPT], cwd=os.path.dirname(SCRIPT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

while True:
    proc = start()
    for line in proc.stdout:
        sys.stdout.write(line); sys.stdout.flush()
    proc.wait()
    time.sleep(RESTART_SEC)
```

**规则：** 用户要求"systemd 服务"但环境不支持时，保留 systemd 配置文件并立即提供等效的守护方案，不能拖着不解决。

#### 🔴 Pitfall: 金融数据全量采集的性价比与优先级
全量基金历史净值（如 27,166 只）通过单只接口（`fund_open_fund_info_em` 等）采集需要数小时，且容易触发限流。应该：
1. **最新净值批量采集**：优先使用 `fund_open_fund_rank_em(symbol="全部")` 一次性获取全市场最新净值（通常 2-4 秒内返回 1.9w+ 条）。
2. **历史净值按需补齐**：只对缺少 30+ 天历史数据的基金补采，每只请求后加 `time.sleep(HISTORY_PER_FUND_SLEEP)` 限流，每 500 只休息 5 秒。
3. **后台运行**：用 `terminal(background=true)` 启动，让采集脚本在后台执行数小时，不阻塞当前 session。
4. **评分依赖历史数据**：历史净值采集完成后再运行 `compute_scores.py` 或等价评分逻辑，不要在每只基金采集完成后立即评分（频繁 IO）。

```python
# 取得最新净值后，判断哪些基金缺少足够历史数据
SELECT DISTINCT fund_code FROM fund_nav
WHERE fund_code NOT IN (
    SELECT fund_code FROM fund_nav GROUP BY fund_code HAVING COUNT(*) >= 30
)
```

**规则：** 金融数据采集要先做"批量最新"+"后台补历史"，避免对 2w+ 只基金发 2w+ 次单独请求。

#### 🔴 Pitfall: 采集脚本在后台跑时注意日志持久化
后台进程的 `terminal(background=true)` 输出不一定能在 session 结束后保留。应在启动命令里将输出重定向到项目日志文件：
```bash
python run_full_collection.py > run_full_collection.log 2>&1
```

**规则：** 任何后台长运行的采集/计算任务，必须将 stdout/stderr 重定向到项目目录的 `.log` 文件，方便后续排查和验证。

---

## 📏 代码风格规范

### 通用原则
- **命名**：变量/函数名要有意义，不用缩写（除了循环变量 i/j/k）
- **函数长度**：单函数不超过 50 行，超过就拆
- **嵌套深度**：不超过 3 层，超过用 early return 或提取函数
- **魔法数字**：禁止，必须用常量命名
- **注释**：只写"为什么"，不写"是什么"（代码本身应该说明是什么）

### Python 专项
- 遵循 PEP 8
- 用 type hints
- 优先用标准库，第三方依赖要说明理由
- 字符串格式化用 f-string
- 异常处理要具体，不要裸 except

### JavaScript/TypeScript 专项
- 优先 const，其次 let，禁止 var
- 用 === 而非 ==
- async/await 优先于 .then()
- 组件文件名 PascalCase，工具文件名 camelCase

### Rust 专项
- 函数参数用 `&Path` 而非 `&PathBuf`（clippy::ptr_arg）— 修复时记得同步更新 `use std::path::{Path, PathBuf}` 导入
- 跨平台路径拼接用 `PathBuf::join()`，禁止字符串 `.replace('/', "\\")` — PathBuf::join 自动处理分隔符
- 异常处理用 `map_err` + `?` 或 `if let Err(e)`，禁止裸 `unwrap()`/`expect()`（生产代码会 panic）
- 优先用标准库，rayon/serde 等第三方依赖需说明理由
- `serde` 派生顺序：`Serialize` 在 `Deserialize` 前（字母序）
- **🔴 `#[serde(default)]` for optional fields:** When a struct field is `String` (not `Option<String>`), serde will fail to deserialize if the JSON doesn't include that field. The error is silently swallowed by `.ok()` or `.unwrap_or_default()`, resulting in an empty vector. Add `#[serde(default)]` to any field that may be absent in heterogeneous JSON (e.g., TVBox sites where type=3 may lack `api`). One bad site kills the entire array. See `tauri-desktop-apps` references/debugging-pitfalls.md #20.
- **共享模块提取**：当 `file_X.rs` 和 `file_X_streaming.rs`（或其他同族文件）有相同 helper 函数时，提取到独立模块（如 `dissolve_helpers.rs`），在 `mod.rs` 注册，调用方用 `super::module_name::fn()` 引用。提取时统一用 `&Path` 签名（比 `&PathBuf` 更泛用）

### Vue 3 + Vite 纯前端项目初始化

标准初始化流程（不含 Tauri）：

```bash
# 1. 创建项目
cd /path/to/project/frontend
npm create vite@latest . -- --template vue

# 2. 安装依赖
npm install
npm install vue-router@4 vue-chartjs@5 chart.js@4
npm install -D vite-plugin-pwa

# 3. 项目结构
# src/views/       — 页面组件（Home, Detail, Search, Compare）
# src/components/  — 公共组件（Navbar, Loading, Empty, Pagination）
# src/api/         — API 调用层（fetch 封装）
# src/router/      — vue-router 配置
# src/styles/      — 全局 CSS
# public/          — 静态资源（PWA icons, manifest）
```

**PWA 配置**（vite.config.js）：
```js
import { VitePWA } from 'vite-plugin-pwa'
export default {
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: '应用名',
        short_name: '应用名',
        start_url: '/',
        display: 'standalone',
        background_color: '#0a0e17',
        theme_color: '#0a0e17',
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,woff2}'],
      },
    }),
  ],
}
```

**构建产物集成到 FastAPI**：`npm run build` 输出到 `dist/`，FastAPI 用 `StaticFiles` 挂载即可。

**常见问题**：
- `dist/` 不在 git 中提交（.gitignore），CI/CD 或手动 build
- Vite dev server 端口 5173，API 代理在 vite.config.js 中配置 proxy
- PWA 的 `start_url` 和 `scope` 必须与实际部署路径匹配

### Tauri + Vue 专项
- Tauri v2 事件监听器（如 `onDragDropEvent`）返回 `Promise<UnlistenFn>`，必须在 `onUnmounted` 中调用 unlisten 清理，否则内存泄漏
- Vue `shallowRef` 大数组累加禁止用 spread `[...old, ...new]`（O(n²)），改用普通数组 + `push()`，完成后再赋值给 shallowRef
- Tauri IPC 返回类型必须与 TypeScript invoke 泛型参数匹配
- 所有接收路径参数的 Rust command 都需检查系统目录（`/usr`, `/etc`, `C:\\\\Windows`）
- **Remote push via SSH (DeskBox host):** `scp`/`rsync` are blocked by firewall. Always use Python subprocess + base64 encoding to push files (NOT bash heredocs — they fail with complex Vue/TS content due to escaping). Use the reference script `scripts/remote-push.py` for the boilerplate.
- **Remote pnpm:** Always prepend `export PATH=$PATH:/root/.hermes/node/lib/node_modules/corepack/shims` before any `pnpm` command on the remote host.
- **Tauri + Vue project structure convention:** Commands in `src-tauri/src/commands/*.rs`, IPC wrapper in `src/utils/tauri.ts`, views in `src/views/`, components in `src/components/{layout,video,player}/`, router in `src/router/`, global CSS in `src/styles/global.css`, 5-view layout (Home, Live, Favorite, History, Settings).

#### 🔴 Pitfall: rusqlite `execute_batch` requires semicolons in SQL strings
`Connection::execute_batch()` 拼接多个 SQL 语句时，**每条语句必须以 `;` 结尾**。即使每条字符串内部看起来完整，缺少分号会导致 `near "CREATE": syntax error`。

```rust
// ❌ 危险：SQL 字符串末尾没有分号
pub const CREATE_FAVORITES: &str = "CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    UNIQUE(video_id, source_name)
)";  // ← 缺少 ;

// ✅ 每条 SQL 必须以分号结尾
pub const CREATE_FAVORITES: &str = "CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    UNIQUE(video_id, source_name)
);";  // ← 有分号
```

**规则：所有传入 `execute_batch` 的 SQL 常量必须以 `;` 结尾。** `execute_batch(&ALL_MIGRATIONS.join("\n"))` 会把多条 SQL 拼在一起，缺分号时 SQLite 解析器会在下一条 `CREATE` 关键字处报错。

#### 🔴 Pitfall: mpv 动态链接导致 Tauri sidecar 无法直接打包
Linux 上的 mpv 是动态链接的（依赖 libavcodec/libavformat 等几十个 .so），直接把 `/usr/bin/mpv` 复制到 `src-tauri/binaries/` 后在目标机器运行会因缺少依赖库而失败。

**正确做法：** 安装为系统依赖 + 运行时路径检测
```rust
fn find_mpv() -> Option<String> {
    // 1. which mpv
    // 2. 常见路径: /usr/bin/mpv, /usr/local/bin/mpv, /snap/bin/mpv
}
```
- `tauri.conf.json` 的 `bundle.linux.deb.depends` 添加 `["mpv"]`
- Rust 代码在 `setup()` 时检测并报告 mpv 状态
- 找不到 mpv 时给出清晰安装指引（推荐通过系统包管理器安装）

**对于 macOS/Windows:** mpv 在 macOS 上可通过 Homebrew 静态链接，Windows 上可用 mpv-lazy 等预编译包，sidecar 方案更可行。

#### 🔴 Pitfall: Tauri `app.path()` requires `use tauri::Manager`
`app.path()` in `setup()` closure is not found without importing the `Manager` trait. Compiler error: `no method named 'path' found for &mut tauri::App`. Fix: add `use tauri::Manager;` at the top of `lib.rs`.

#### 🔴 Pitfall: xdotool 无法点击 Tauri WebKitGTK webview 中的元素
Tauri 在 Linux 上使用 WebKitGTK 渲染 webview。**xdotool 的鼠标事件（click/mousedown/mouseup）无法正确传递到 webview 内的 HTML 元素。** Tab 导航也往往不按 DOM 顺序走，会跳到意外的元素。

```bash
# ❌ 无效：xdotool click 无法触发 webview 内的按钮
xdotool mousemove --window $WID 465 369 && xdotool click 1  # ← 没有反应

# ❌ 无效：Tab 导航不按预期走
xdotool key Tab Tab Tab space  # ← 可能跳到刷新按钮而非目标按钮
```

**原因：** WebKitGTK 的 X11 事件处理与标准 X11 窗口不同，鼠标事件在 GTK 层被拦截，不会传递到 web DOM。

**可行的替代方案（按可靠性排序）：**
1. **直接操作 SQLite 数据库** — 如果目标是添加数据（如配置源），直接用 Python + sqlite3 写入数据库，然后重启应用
2. **通过 Tauri IPC 注入 JavaScript** — 如果 Tauri 暴露了 `eval` 或 `webview.eval()` 接口
3. **用 `xdotool key` 模拟键盘快捷键** — 键盘事件有时比鼠标事件更可靠（但 Tab 导航仍不可靠）
4. **用 Playwright/Puppeteer 连接 webview** — 如果 webview 暴露了 CDP 端口

**规则：对 Tauri 应用做自动化 UI 测试时，不要依赖 xdotool 鼠标点击。优先用后端 API/数据库操作代替 GUI 交互。**

#### 🔴 Pitfall: TVBox type=3 Spider 站点的 .js 脚本被误用为 API URL
TVBox 配置中 type=3 Spider 站点的 `ext` 字段可能是 JavaScript Spider 脚本路径（如 `https://raw.kkgithub.com/.../88看球.js`），**不是网站 URL**。前端代码若不检查 `.js` 后缀，会将其拼接为无效 API URL（如 `...88看球.js/api.php/provide/vod/`），导致所有内容加载静默失败。

```javascript
// ❌ 危险：将 .js Spider 脚本误当作 API URL
if (typeof site.ext === 'string' && site.ext.startsWith('http')) {
  apiUrl = site.ext  // ← 如果 ext 是 .js 文件，生成无效 URL
}
// 结果：...88看球.js/api.php/provide/vod/ → 404

// ✅ 正确：检测并跳过 .js Spider 脚本
if (typeof site.ext === 'string' && site.ext.startsWith('http')) {
  if (site.ext.endsWith('.js')) {
    console.log(`[DeskBox] 跳过 Spider 脚本: ${site.name}`)
    continue
  }
  apiUrl = site.ext
}
```

**规则：在 `loadContentItems()` 中处理 type=3 站点时，必须先检查 `ext` 是否以 `.js` 结尾，是则跳过。**

#### 🔴 Pitfall: Vue SFC duplicate code blocks cause silent TS errors
When editing Vue `.vue` files, accidentally duplicating a `return list\\n})` block produces `error TS1128: Declaration or statement expected` in `vue-tsc`. This is easy to do when copy-pasting computed properties. **Always verify** the `<script>` section has balanced braces after editing.

#### 🔴 Pitfall: TypeScript catch 参数类型推断导致 TS2339
将 `.catch((e) => console.debug(e))` 改为 `.catch((e) => showToast('失败: ' + e.message, 'error'))` 时，TypeScript 把 `e` 推断为 `unknown` 或 `{}`，直接访问 `e.message` 会报 `error TS2339: Property 'message' does not exist on type '{}'`。

```typescript
// ❌ TS2339: e 被推断为 unknown/{}，e.message 不存在
.catch((e) => showToast('失败: ' + e.message, 'error'))

// ✅ 方案1：加 : any 类型标注
.catch((e: any) => showToast('失败: ' + (e?.message || String(e)), 'error'))

// ✅ 方案2：用 String() 安全转换
.catch((e) => showToast('失败: ' + (e instanceof Error ? e.message : String(e)), 'error'))
```

**规则：** Vue/TS 项目中 catch 参数必须显式标注类型或用安全访问模式。推荐 `(e: any)` + `e?.message || String(e)` 组合。修改 catch 后务必运行 `vue-tsc --noEmit` 验证。

#### 🔴 Pitfall: TypeScript string literals missing quotes cause silent runtime failures
In Vue/TS code, omitting quotes around string literals in comparisons or function arguments causes TypeScript compilation errors AND silent runtime failures. Common patterns:
- `=== string` → should be `=== 'string'`
- `includes(vod)` → should be `includes('vod')`
- `startsWith(http)` → should be `startsWith('http')`
- `getCategoryVideos(首页, ...)` → should be `getCategoryVideos('首页', ...)`

These are easy to introduce when refactoring code that had string literals removed accidentally. **Always run `vue-tsc --noEmit` after editing Vue store files** to catch these.

#### 🔴 Pitfall: WebKitGTK `console.log` 从 SSH 不可见
Tauri 在 Linux 上使用 WebKitGTK。`console.log/warn/error` 输出到 WebKit 内部控制台，**不会出现在 stdout/stderr**，从 SSH 无法捕获。

**解决方案（按可靠性排序）：**
1. **Rust `eprintln!` 写文件** — 最可靠。注册一个 `log_debug` IPC 命令，JS 通过 `invoke('log_debug', { msg })` 调用，Rust 端 `eprintln!` + 写文件。
2. **`WEBKIT_INSPECTOR_SERVER=127.0.0.1:9222`** — 启动时设置环境变量，然后从另一终端连接。但 WebKitGTK 的 inspector 支持不完整。
3. **不要依赖 `console.log` 做远程调试** — 在 Tauri + WebKitGTK 环境下，所有日志必须通过 IPC 写文件。

```typescript
// ✅ 正确：通过 IPC 写日志文件
import { invoke } from '@tauri-apps/api/core'
function dbg(msg: string) {
  invoke('log_debug', { msg }).catch(() => {})
}
```

```rust
// Rust 端
#[command]
pub async fn log_debug(msg: String) -> Result<(), String> {
    use std::io::Write;
    let mut f = std::fs::OpenOptions::new()
        .create(true).append(true)
        .open("/tmp/app_debug.log").map_err(|e| e.to_string())?;
    writeln!(f, "{}", msg).map_err(|e| e.to_string())?;
    Ok(())
}
```

#### 🔴 Pitfall: Tauri IPC 调用链排查方法
当前端 IPC 调用"无声无息"时（无返回、无错误），按以下顺序排查：

**1. 检查命令是否注册在 binary 中：**
```bash
strings /path/to/binary | grep 'command_name'
# 有输出 → 命令已注册
# 无输出 → lib.rs 的 invoke_handler 中未添加
```

**2. 检查 Rust 端是否被调用：**
在命令入口加 `eprintln!`，重新编译，启动后检查日志文件。

**3. 检查 JS 端是否到达调用点：**
在 `invoke()` 前后加 `invoke('log_debug', ...)` 调用，检查日志文件是否存在。

**4. 检查 watcher/异步链是否断裂：**
Vue watcher 的 `.then()` 链如果没有 `.catch()`，前一步异常会导致后续步骤永远不执行。这是"代码路径未到达"的常见原因。

```typescript
// ❌ 危险：无 .catch()，异常会中断整个链
refreshSourceCategories().then(() => loadContentItems())

// ✅ 正确：添加错误处理
refreshSourceCategories()
  .then(() => loadContentItems())
  .catch(e => console.error('[DeskBox] 内容加载失败:', e))
```

#### 🔴 Pitfall: 迭代式 Rust 补丁容易破坏代码结构
通过 Python/sed 逐行向 Rust 文件添加代码（如 `eprintln!` 调试日志），容易破坏花括号匹配、引入语法错误。

**症状：** `cargo build` 报 `mismatched closing delimiter` 或 `unexpected token`

**正确做法：**
1. 从已知好的版本开始（如容器中的源文件 `scp` 到主机）
2. 用 Python 脚本**一次性**插入所有需要的代码行
3. 插入后立即验证花括号平衡：`python3 -c "print(open('file.rs').read().count('{'), open('file.rs').read().count('}'))"`
4. 编译验证：`cargo check`

**不要：** 用 `sed -i 'Na\...'` 逐行插入（容易插到错误位置），或用 Python `str.replace()` 在函数签名中间插入代码。

#### 🔴 Pitfall: 远程 Linux 桌面测试截图
Tauri 应用在远程 Xfce 桌面 (display :10) 上运行时，截图命令：
```bash
DISPLAY=:10 XAUTHORITY=/home/skies/.Xauthority import -window root /tmp/screenshot.png
```
注意：`import` 是 ImageMagick 的命令，不是 Python 的。截图前确保应用窗口已加载（`sleep 8`）。

#### 🔴 Pitfall: qwen3.6 thinking model may return null content
qwen3.6 is a reasoning model. If max_tokens is too low, thinking consumes all tokens and `content` returns `null`. For cronjobs with long prompts, use `glm-4-flash` or `deepseek-v4-flash` instead.

#### 🔴 Pitfall: Rust FFI — OnceLock::get_or_try_init is unstable
When migrating `static mut` + `Once` to `OnceLock` for FFI singletons, `get_or_try_init` requires nightly Rust. Use `OnceLock<Option<T>>` + `get_or_init` instead:

```rust
// ✅ Stable pattern
static MPV_FFI: OnceLock<Option<MpvFfi>> = OnceLock::new();
pub fn init() -> Result<&'static Self, MpvError> {
    MPV_FFI.get_or_init(|| match Self::load() {
        Ok(ffi) => Some(ffi),
        Err(_) => None,
    });
    Self::global()
}
```

**Rule:** Never use `get_or_try_init` on stable Rust.

#### 🔴 Pitfall: Tauri IPC type mismatch causes silent data loss
Frontend `number` ↔ Rust `Option<String>` mismatch causes Tauri to silently deserialize as `None`:

```typescript
// ❌ episode: number → Rust gets None
api.dbAddHistory(videoId, title, episode)
// ✅ Explicit conversion
api.dbAddHistory(videoId, title, String(episode))
```

**Rule:** Always check Rust command parameter types. `number↔String` is the most common mismatch.

#### 🔴 Pitfall: vue-tsc node_modules errors are pre-existing
Errors from `node_modules/@tauri-apps/` and `node_modules/@vue/` about ES2015 features are TypeScript config issues (ES5 target), not caused by code changes. Only `src/` errors matter.

**Rule:** Focus on `src/` errors when running `vue-tsc --noEmit`. Exit code 0 = compiles clean.

#### 🔴 Pitfall: `std::sync::Mutex` 在 Tauri async 命令中阻塞 tokio 线程
Tauri `#[command]` 函数运行在 tokio 运行时上。如果在其中使用 `std::sync::Mutex` 并 `.lock().unwrap()`，会阻塞当前 tokio 线程（不是阻塞整个运行时，但会导致该 worker 线程无法处理其他任务）。在高并发场景下可能引发死锁或性能问题。

```rust
// ❌ DANGEROUS: std::sync::Mutex 在 async fn 中阻塞 tokio 线程
static DB: std::sync::Mutex<Option<Database>> = std::sync::Mutex::new(None);

#[command]
pub async fn get_sources() -> Result<Vec<Source>, String> {
    let db = DB.lock().map_err(|e| e.to_string())?;  // ← 阻塞 tokio worker
    // ...
}

// ✅ Option A: tokio::sync::Mutex（async-aware）
static DB: tokio::sync::Mutex<Option<Database>> = tokio::sync::Mutex::new(None);

#[command]
pub async fn get_sources() -> Result<Vec<Source>, String> {
    let db = DB.lock().await;  // ← async lock, 不阻塞 tokio 线程
    // ...
}

// ✅ Option B: 如果锁时间极短，用 spawn_blocking 包装
#[command]
pub async fn get_sources() -> Result<Vec<Source>, String> {
    let sources = tokio::task::spawn_blocking(|| {
        let db = DB.lock().unwrap();  // ← 在 blocking 线程中，可接受
        // ... 读取数据
    }).await.map_err(|e| e.to_string())?;
    Ok(sources)
}
```

**Rule:** 在 Tauri `#[command]` async 函数中，优先用 `tokio::sync::Mutex`。如果必须用 `std::sync::Mutex`，确保锁持有时间极短（微秒级），且不要在 `.lock()` 和 `.await` 之间夹杂其他 async 操作。

#### 🔴 Pitfall: IPC 参数数量不匹配导致静默数据丢失
前端 IPC wrapper 函数传入的参数数量少于 Rust 后端命令期望的数量时，Tauri 不会报错——缺失的参数被反序列化为 `None`/`0`/`""`，导致数据字段静默丢失。

```typescript
// ❌ 前端只传 3 个参数，后端期望 8 个
api.dbAddHistory(videoId, title, episode)
// cover, source_name, source_url, category, year → 全部丢失

// ✅ 前端补齐所有参数
api.dbAddHistory(videoId, title, episode, cover || '', sourceName, sourceUrl, category || '', year || '')
```

**排查方法：** 对比 `invoke('command_name', ...)` 的参数列表与 Rust `#[command] fn` 的参数列表，逐一匹配。**规则：** 新增 Rust command 参数时，必须同步更新 TypeScript IPC wrapper，反之亦然。

#### 🔴 Pitfall: 双重持久化（localStorage + SQLite）导致数据不一致
同时向 localStorage 和 SQLite 写入数据，但只从其中一个读取，会导致：
- 重启应用后数据丢失（如果只读 SQLite，localStorage 不持久）
- localStorage 被清除后数据丢失（如果只读 localStorage）
- 两个存储源的数据可能不同步

```typescript
// ❌ 危险：写入两个地方，但只从一个读取
async function addToFavorites(item: any) {
  localStorage.setItem('favorites', JSON.stringify([...items.value]))
  invoke('db_add_favorite', { ... })  // 写 SQLite
}

function loadFavorites() {
  const cached = localStorage.getItem('favorites')  // ← 只读 localStorage！
  return cached ? JSON.parse(cached) : []
}

// ✅ 统一读取源：启动时从 SQLite 加载，缓存到 localStorage
async function initFavorites() {
  const dbItems = await invoke('db_get_favorites')  // ← 从 SQLite 读
  favorites.value = dbItems
  localStorage.setItem('favorites', JSON.stringify(dbItems))  // 缓存
}
```

**Rule:** 如果项目同时使用 localStorage 和 SQLite，必须明确读取源：启动时从 SQLite 加载到内存，后续操作同时更新内存和 SQLite，localStorage 仅作缓存。

**规则：** 缓存代理/网络请求结果时，只缓存成功结果。失败时不要缓存原始 URL 作为降级——网络抖动是暂时的，缓存失败会导致永久降级。正确做法：失败时不写缓存，下次请求自动重试。

#### 🔴 Pitfall: FastAPI 路由注册顺序 — 静态路由被参数化路由劫持
FastAPI 按注册顺序匹配路由。如果 `/funds/{code}` 在 `/funds/compare` 之前注册，请求 `/api/funds/compare?codes=...` 会被 `/{code}` 匹配（`code="compare"`），返回 404 "未找到基金 compare"。

```python
# ❌ 错误顺序：参数化路由在前，静态路由被劫持
@router.get("/funds/{code}")      # L104 — 先注册
@router.get("/funds/compare")     # L195 — 永远不会被匹配到
@router.get("/funds/{code}/score")

# ✅ 正确顺序：所有静态路由必须在参数化路由之前
@router.get("/funds/compare")     # 先注册静态路由
@router.get("/funds/{code}")      # 再注册参数化路由
@router.get("/funds/{code}/score")
@router.get("/funds/{code}/radar")
```

**规则：** 在 FastAPI router 中，所有静态路径（如 `/funds/compare`、`/funds/search`）必须在参数化路径（如 `/funds/{code}`、`/funds/{code}/score`）**之前**注册。写完路由后用 curl 测试所有端点验证。

#### 🔴 Pitfall: 同步阻塞库在异步 FastAPI 路由中的处理模式

第三方库（如 `akshare`、`requests`）是同步阻塞的，直接在 `async def` 路由中调用会阻塞整个 event loop，导致所有请求卡死。

**错误做法：**
```python
# ❌ 同步调用阻塞 event loop
@router.get("/api/data")
async def get_data():
    df = ak.stock_zh_a_spot_em()  # 阻塞 90s+，整个服务瘫痪
    return df.to_dict()
```

**`asyncio.to_thread` 的陷阱：**
```python
# ⚠️ 扔线程池仍会超时 — uvicorn 默认 60s 超时
@router.get("/api/data")
async def get_data():
    df = await asyncio.to_thread(ak.stock_zh_a_spot_em)  # HTTP 请求等 90s 超时
    return df.to_dict()

# ⚠️ wait_for + CancelledError 链混乱
df = await asyncio.wait_for(asyncio.to_thread(...), timeout=120)
# uvicorn 的超时触发 CancelledError → 再被 wait_for 捕获 → TimeoutError 链
```

**正确方案：后台缓存 + API 只读**
- 耗时同步操作放在**独立后台进程**中（systemd 服务或 cron）
- 结果写入 SQLite / Redis / 文件
- API 路由只做**毫秒级读取**

```
后台进程(60s循环) → 写入 SQLite → API 读取(1ms)
```

**适用场景：** akshare、requests 爬虫、ffmpeg 转码、大文件处理等任何耗时超过 5s 的同步操作。

**规则：** 任何耗时 >5s 的同步调用，不要放在 HTTP 请求路径中。用后台服务 + 缓存解耦。
当 URL 包含单引号或其他 shell 元字符时，直接嵌入 `sh -c` 命令会导致 shell 注入：

```rust
// ❌ DANGEROUS: URL 直接拼接，含单引号的 URL 可逃逸
let cmd = format!("mpv --fullscreen '{}'", url);
Command::new("sh").args(["-c", &cmd]).spawn()?;

// ✅ 安全：使用数组参数直接传递给 mpv，不经过 shell
Command::new("mpv")
    .args(["--fullscreen", &url])  // ← 不经过 sh -c
    .spawn()?;
```

**Rule:** 外部命令的参数直接作为数组传递给 `Command::args()`，不要拼接到 `sh -c` 中。

#### 🔴 Pitfall: 递归解析器无深度限制（Spider iframe）
Spider 引擎解析播放地址时可能遇到多层 iframe 嵌套。如果递归调用无深度限制，恶意网页可构造无限循环导致栈溢出：

```rust
// ❌ DANGEROSS: 无深度限制
async fn resolve_play(url: &str, client: &Client) -> Result<String, String> {
    if is_iframe(html) {
        let iframe_url = extract_iframe(&html);
        return Box::pin(resolve_play(&iframe_url, client)).await;  // ← 可无限递归
    }
}

// ✅ 安全：添加 depth 参数
async fn resolve_play(url: &str, client: &Client, depth: u32) -> Result<String, String> {
    if depth > 3 {
        return Err("iframe 嵌套过深".into());
    }
    if is_iframe(html) {
        let iframe_url = extract_iframe(&html);
        return Box::pin(resolve_play(&iframe_url, client, depth + 1)).await;
    }
}
```

**Rule:** 所有递归调用（iframe 解析、URL 重定向追踪、页面遍历）必须有最大深度限制（建议 3-5 层）。

#### Tauri + SQLite 持久化模式
推荐的全局数据库模式（注意：在 async 命令中使用 `tokio::sync::Mutex`，见上方 pitfall）：

```rust
// commands/source.rs
use tokio::sync::Mutex;
use crate::db::operations::Database;

static DB: Mutex<Option<Database>> = Mutex::new(None);

/// 在 setup() 中调用
pub fn init_db(db_path: &str) {
    match Database::new(db_path) {
        Ok(db) => { *DB.lock().unwrap() = Some(db); }
        Err(e) => eprintln!("[App] DB init failed: {}", e),
    }
}

pub fn get_db() -> Result<std::sync::MutexGuard<'static, Option<Database>>, String> {
    DB.lock().map_err(|e| e.to_string())
}
```

```rust
// lib.rs setup hook
use tauri::Manager;
.setup(|app| {
    let db_path = app.path().app_data_dir().expect("...").join("app.db");
    commands::source::init_db(&db_path.to_string_lossy());
    Ok(())
})
```

命令中使用：`let db_guard = get_db()?; if let Some(ref db) = *db_guard { db.xxx()?; }`

#### mpv IPC 控制模式
mpv 通过 Unix socket 接收 JSON 命令：

```rust
use std::os::unix::net::UnixStream;
use std::io::Write;

fn send_mpv_command(socket_path: &str, cmd: &str) -> Result<(), String> {
    let mut stream = UnixStream::connect(socket_path)
        .map_err(|e| format!("连接 mpv IPC 失败: {}", e))?;
    let mut msg = cmd.to_string();
    msg.push('\n');
    stream.write_all(msg.as_bytes())
        .map_err(|e| format!("发送命令失败: {}", e))?;
    stream.flush().map_err(|e| e.to_string())?;
    Ok(())
}

// 启动 mpv 时指定 socket
Command::new("mpv")
    .args(["--input-ipc-server=/tmp/app-mpv-socket", url])
    .spawn()?;
// 发送命令
send_mpv_command("/tmp/app-mpv-socket", r#"{"command": ["cycle", "pause"]}"#)?;
```

### Git 规范
- commit message 格式：`<type>(<scope>): <description>`
- type: feat / fix / docs / style / refactor / test / chore
- 一个 commit 只做一件事
- 不提交半成品代码
- **🔴 默认不提交到 Git** — 用户明确要求"代码先不要提交，我要求的时候再提交"时，所有修改保持本地。只有用户明确说"提交"或"push"时才执行 git 操作。即使修复完成且测试通过，也不要主动 commit/push。

---

## 🎨 UI/UX 质量门禁

**当用户要求"样式好看、效果好、交互友好"时，代码不仅要能跑，还要好看好用。**

### 核心原则
1. **样式要好看**: 配色协调，字体大小合适，间距舒适，圆角阴影适当
2. **效果要好**: 动画过渡流畅，加载状态清晰，反馈及时
3. **交互友好**: 操作有反馈，错误提示明确，引导清晰

### 检查清单
- [ ] 配色是否协调？（不要超过3种主色）
- [ ] 字体大小是否合适？（正文14-16px，标题18-24px）
- [ ] 间距是否舒适？（元素间有呼吸感）
- [ ] 按钮/输入框有 hover/active 状态吗？
- [ ] 重要操作有 loading 状态吗？
- [ ] 错误信息用户友好吗？（不要技术术语）
- [ ] 动画过渡流畅吗？（不要突然跳变）
- [ ] 空状态有提示吗？（不要空白页面）

### 桌面端 UI 比例 (User Preference)
当原型是 HTML 页面但目标是桌面端应用时，UI 必须等比例缩小：
- 卡片尺寸：160-180px（桌面端）而非原型的全屏宽度
- 每行 6-8 个卡片（原型可能只有 3-4 个）
- 字体：12-16px（原型通常 16-20px）
- 间距：适当压缩，保持紧凑感
- 桌面端 UI 要比原型更好看，不仅仅是缩小

**用户原话**: "毕竟我做的是桌面端的原型是html界面，但是我理解交互，还有UI要好一点"

### 暗色主题参考
```css
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --accent: #e94560;
  --accent-secondary: #0f3460;
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
}
```

### 常见问题
- ❌ 只关注功能，忽略外观 → 用户觉得"能用但丑"
- ❌ 动画太多太花哨 → 用户觉得"晃眼"
- ❌ 错误信息技术化 → 用户看不懂
- ❌ 没有 loading 状态 → 用户不知道在加载

---

## 🔍 代码审查清单

每次提交前自查：

### 基础检查
- [ ] 代码能跑吗？（基本功能）
- [ ] 有测试吗？测试覆盖了关键路径吗？
- [ ] 命名清晰吗？别人能看懂吗？
- [ ] 有重复代码吗？能提取吗？
- [ ] 有硬编码吗？应该配置化吗？
- [ ] 错误处理完整吗？
- [ ] 有没有安全隐患？（注入、XSS、密钥泄露）
- [ ] 性能有明显问题吗？
- [ ] 文档/注释需要更新吗？
- [ ] 符合项目现有风格吗？

### 结构化审查方法（按维度 + 严重级别）

对项目做全面审查时，按以下维度逐项检查，每个发现标注严重级别：

**维度**：
1. 🔴 **安全性**：硬编码密钥、SQL注入、XSS、不安全的IPC调用、HTTP代理无大小限制、认证绕过
2. 🔴 **代码质量**：死代码、重复逻辑、错误处理缺失、类型不安全
3. 🟡 **架构**：模块划分、耦合度、可维护性、文件过大（>500行应拆分）
4. 🟡 **性能**：内存泄漏风险、不必要的重渲染、串行可改并发、N+1查询
5. 🟢 **亮点**：做得好的设计、值得推广的模式

**输出格式**：
```markdown
## 审查结果
- 项目：[项目名]
- 审查范围：[文件列表]

### 🔴 严重问题（必须修）
1. 问题描述 → 文件:行号 → 修复建议

### 🟡 建议优化
1. 问题描述 → 建议

### 🟢 亮点
1. 做得好的地方

### 评分
- 安全性：X/10
- 代码质量：X/10
- 架构：X/10
- 性能：X/10
- 综合：X/10
```

---

## 🐛 Bug 修复流程

1. **理解问题**：复现步骤、期望行为、实际行为
2. **参考已有实现**：如果有对标产品（如 TVBox 之于 DeskBox），**先读它的源码理解正确逻辑**，再回来查自己的代码。不要凭猜测调试。
3. **定位根因**：不要只看表面症状
4. **最小修复**：只改必须改的（铁律 #3）
5. **验证修复**：写测试证明修复有效（铁律 #9）
6. **回归检查**：确认没有引入新问题

> **用户原话**: "如果不清楚逻辑就去参考 ok 影视 tvbox，看他们逻辑"
> 含义：遇到实现不确定时，先看参考项目的源码，理解"应该怎么做"，再对比"我们哪里不对"。这比盲目加日志排查高效得多。

---

## 🔬 高级调试方法论

对于复杂 Bug 和性能回退，使用系统化诊断循环。完整内容已合并自 `diagnose` skill (2026-06-14)。

### 核心原则：先建反馈循环

**这是调试的灵魂。** 其余都是机械操作。如果你有一个快速、确定性、可由 agent 运行的 pass/fail 信号来判断 Bug，你就能找到原因。

在这里投入不成比例的努力。**要激进。要创造性。拒绝放弃。**

### 反馈循环构建方式（按优先级）

1. 在 Bug 触达的接缝处写**失败测试**
2. 对运行中的 dev server 发 **curl / HTTP 脚本**
3. 用 fixture 输入做 **CLI 调用**，diff stdout
4. **Headless browser 脚本** (Playwright / Puppeteer)
5. **重放捕获的 trace**
6. **一次性测试工具** — 系统的最小化子集
7. **Property / fuzz 循环** — 1000 个随机输入
8. **二分法工具** — 自动化状态检查
9. **差分循环** — 旧版 vs 新版
10. **HITL bash 脚本** — 最后手段，用脚本驱动人工操作

### 迭代优化循环

- 能更快吗？
- 信号能更清晰吗？
- 能更确定性吗？

30 秒的不稳定循环几乎等于没有循环。2 秒的确定性循环是调试超能力。

### 六阶段诊断流程

**Phase 1 — 建立反馈循环** (见上)

**Phase 2 — 复现**
- 循环产生用户描述的失败
- 失败跨多次运行可复现
- 已捕获确切症状

**Phase 3 — 提出假设**
- 生成 3-5 个排序假设
- 每个假设必须**可证伪**：陈述预测
- 格式："如果 <X> 是原因，那么 <改变 Y> 会让 Bug 消失"
- **测试前先向用户展示排序列表**

**Phase 4 — 插桩探测**
- 每个探测对应一个假设。**一次只改一个变量。**
- 工具优先级：调试器/REPL 检查 > 定向日志 > 永远不要"全量日志然后 grep"
- 每条调试日志加唯一前缀，如 `[DEBUG-a4f2]`

**Phase 5 — 修复 + 回归测试**
- 修复前写回归测试（如果有正确的接缝）
- 如果没有正确的接缝，这本身就是发现
- 最小化复现 → 失败测试 → 看它失败 → 应用修复 → 看它通过

**Phase 6 — 清理 + 复盘**
- [ ] 原始复现不再复现
- [ ] 回归测试通过
- [ ] 所有 `[DEBUG-...]` 插桩已移除
- [ ] 一次性原型已删除
- [ ] 正确的假设已写入 commit message

**然后问：什么能预防这个 Bug？**

### 常见环境问题速查

| 症状 | 可能原因 | 修复 |
|------|---------|------|
| INSERT 静默失败 | Schema 不匹配 | `PRAGMA table_info()` → 与代码对比 |
| `pip` 在 venv 中缺失 | venv 损坏 | 找另一个 venv 或用 `--break-system-packages` |
| 服务器刷日志无连接 | uvicorn DEBUG 循环 | `DEBUG=false`，kill 旧进程 |
| numpy/pandas 不可用 | 无 pip 访问 | 用 stdlib fallback (`math`, `statistics`) |
| 服务器 500 启动失败 | 依赖或环境问题 | 检查日志，验证配置 |


---
## 📝 任务执行模板

接到任务时，先输出计划：

```
## 任务理解
[用自己的话复述任务目标]

## 方案
[列出实现步骤]
1. [步骤] → 验证：[如何确认完成]
2. [步骤] → 验证：[如何确认完成]

## 风险/疑问
[不确定的地方，先问]

## 预估
[改动范围、文件列表]
```

完成后输出：

```
## 完成报告
- 改了什么：[文件列表 + 改动摘要]
- 验证了什么：[测试结果/手动验证]
- 遗留问题：[如有]
```
