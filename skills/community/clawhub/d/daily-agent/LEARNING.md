# LEARNING.md — Daily Agent 学习记录

## 使用说明
每次 Paudy 纠正我、指出错误、或我学到新规则时，自动追加到这里。
格式：日期 + 事件 + 学到的教训。

---

## 学习记录

### 2026-06-02 — Gateway 重启铁律
- **事件**：反复用 `gateway stop` + 杀进程重启，导致配置被覆盖
- **Paudy 纠正**：应该只用 `gateway restart`（SIGUSR1 热重载）
- **教训**：
  1. `gateway stop` 连接远程配置服务器 401，经常失败
  2. 杀进程再启动会触发 PRD preset 合并，覆盖本地配置
  3. SIGUSR1 热重载安全，不杀进程、不合并 preset、配置完整保留
  4. `doctor --fix` 自动修复也覆盖配置，禁止自动执行
- **永久规则**：Gateway 重启只用 `gateway restart`

### 2026-06-02 — L1 cursor bug
- **事件**：L1 记忆提取从 5/28 起持续产出 0 条
- **根因**：cursor 设为精确 max(recorded_at)，下次查询用 `>` 比较排除所有行
- **修复**：cursor +1ms buffer + SELF-CHECK 自动检测
- **教训**：cursor 前进时必须 +1ms 缓冲，避免 `>` 比较排除最新批次

### 2026-06-02 — 配置防覆盖
- **事件**：memorySearch 和 memory-tencentdb 每次重启后被剥离
- **根因**：PRD preset 里没有这些字段
- **修复**：同步更新 PRD preset + openclaw.json
- **教训**：所有自定义配置必须同时写入 PRD preset，否则重启会被覆盖
