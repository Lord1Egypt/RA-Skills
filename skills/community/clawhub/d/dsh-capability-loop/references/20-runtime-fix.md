# 20 · 运行时修复与升级（Runtime Fix）

> 顺序：**备份 → DryRun → 小步 apply → 立即 verify → 写证据**。每类修复都要能一句话回滚。
> 沙箱前提：DSH 会话默认 `workspace-write`，写 `~/.dsh` / 安装目录会被拒（需用户终端或一次审批放宽）；脚本全部设计成「用户/审批后执行 + 自动备份」。

## 1. P0-1 跨会话检索（session_search 不可用）

**症状**：`SESSION_QUERY_SEARCH_DISABLED`、搜索无结果、5 个搜索工具白占前缀字符。

**根因**：`optional-session-query-sqlite` 被改成 `path: ':memory:'` + `openAt: never`（为防崩溃止血）。

**修复（`cordis.patch.yml`）**：

```yaml
- id: optional-session-query-sqlite
  config:
    path: !!js dshHomePath('session-index.sqlite')
    openAt: first-search
    journalMode: wal
- id: optional-tool-session-query
  config:
    searchTimeoutMs: 600000   # 首次建库保护
```

**首次建库**：256 会话/≈194MB → **2–3 分钟、索引 213–250MB**。建库期间旧桌面壳可能在 ~23s 误杀 → 先做 §2 桌面壳补丁，或用离线预建：

```powershell
# 独立 headless 进程 + 本地假模型（不联网、不消耗真实 token）触发一次 session_search
node "upgrade\tools\offline-index\fake-llm.mjs"          # 窗口 1，端口 18080
$env:FAKE_API_KEY='dummy-local-key'; node "<dsh bin.js>" headless --patch "upgrade\tools\offline-index\prebuild-index-fake.yml" "验证检索。"
```

**索引异常**：`SESSION_QUERY_INDEX_FAILED` / `STALE_CURSOR` / 半成品库 → 完全退出 DSH，删 `%USERPROFILE%\.dsh\session-index.sqlite*`（3 个文件）→ 重开再搜一次（或再跑离线预建）。

**回滚**：`openAt` 改回 `never`（恢复「不崩但不可搜」）；整段删掉则回 bundle 默认。

**验收**：`session_search("断点清单")` 返回真实结果（session id/parent/seq/snippet），秒回；无错误码。

## 2. P0-2 桌面壳反复退出 /「任务已停止」

**机制**：旧壳 `startHealthWatch()` 每 5s 探活、8s 超时，连续 3 次失败 → `handleServerDown()` → `killTree(serverProc.child)`；最坏 ~23s 事件循环阻塞就被判死。建索引、大文件解析、长测试都会触发。

**修复（`main.js`）**：见 `00-baseline.md` 锚点表——探活 12s/8s/6 次 + 连续失败 ≥60s 才 kill + TCP 忙判定（可 accept 只告警）+ kill 前 5s 复核 + 崩溃退避 3s + 服务器 stderr 尾部落 `desktop.log`。

**施加纪律**：
1. 先 `apply.ps1 -DryRun` 校验基线哈希/`git apply --check`；
2. 哈希不匹配（DSH 升级覆盖）→ **跳过，不强刷**，按新版本 diff 重做；
3. 施加后 `node --check main.js.new` + `verify.ps1`；
4. **必须完全退出并重开桌面版**才生效（Electron 主进程不热加载）；
5. 重启后跑 `post-restart-check.ps1`：新壳启动时间晚于补丁、无失败 `startup-*.log`、重启后 0 次 `3/3`、`desktop.log` 有「已启动内置服务器」。

**诚实边界**：补丁根治「探活误杀」这一类；`0x40010004`/`0xC0000142` 属系统/杀软级故障，补丁只能退避 + 留证；仍频繁时给 `node.exe`、`DeepSeek Harness.exe` 加杀软白名单。

## 3. 插件与技能清理（死重量）

**判定**：装了但依赖的 CLI/MCP/服务不可用 → 会误导模型调用不存在的工具，且白占 catalog/工具前缀 → 移出。

**顺序（token-insights 教训）**：先删 patch 插入段 → 再删 `disabled: true` 行 → 再 `pnpm remove`/`dsh plugin remove` → 最后移 storage。**顺序反了会被 `uninstall-blocked` 拦截**。

**市场收敛**：只留一个入口（源环境留技能市场 `@montersy123/dsh-skill-market`）；`dshmarket` 的自重启是 3080 `EADDRINUSE` 的直接来源。

**skills 清理**：内置编辑器/CLI 依赖缺失的批（TeamHarness 7 件套 + browser-use + mcporter）移入 `skills-disabled/`（保留可回滚），活动 catalog 21→12 条。

**验收**：`--dump-config` exit 0 且已移除插件出现 0 次；catalog 条目/描述字符数符合预期（磁盘 description 合计 6,419→3,673）。

## 4. Token 与上下文收敛

1. **批量一次做完**：工具集/skill 清单变更击穿 prompt 缓存（源环境命中 95.96%），碎改更贵。
2. **压 description**：每条 ≤200 字符（硬上限 500，超出被 catalog 截断）；无触发限定的 skill 重写 description。
3. **路由纪律**：默认固定 flash；切模型只在任务边界/新会话；贵模型只做短上下文规划/评审（源环境 5.6% 调用吃 43% 成本）。
4. **长会话策略**：断点清单 + 子代理隔离检索（子代理有独立上下文）；结束前把结论写回 `memory/`，避免下轮重读全部历史。
5. **工具输出**：大输出会裁剪/spill；需要保留时写文件再引用路径，不整段贴回对话。

## 5. 修复完成校验（缺一不可）

| 项 | 命令/证据 |
|---|---|
| 配置语法 | `--dump-config` exit 0；无缺失依赖/激活错误 |
| 检索 | `session_search` 真实返回 |
| 桌面壳 | `post-restart-check.ps1` → `PASS（FAIL=0，待重启项=0）` |
| 插件 | `node_modules` 目标包目录消失；patch/package/storage 无残留 |
| 技能 | 活动/停用数量符合预期；catalog 里新 skill 出现、旧 skill 消失 |
| 回滚 | 备份目录存在且 `rollback.ps1` 可执行（至少 DryRun 一遍） |
