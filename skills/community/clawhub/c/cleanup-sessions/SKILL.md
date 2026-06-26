# cleanup-sessions

清理已中止的子 agent 会话文件及备份文件，释放磁盘空间。

## 触发条件

用户提到：
- 清理子 agent 会话
- 删除 aborted 的会话
- 清理会话文件
- 清理 sessions 目录
- 清理备份文件
- 清理 .deleted / .reset 文件
- 清理过期会话

## 功能

1. **预览模式**：列出所有 `abortedLastRun: true` 的会话文件，显示大小和路径
2. **清理模式**：删除已确认的废弃会话文件
3. **同步清理**：同时清理 `sessions.json` 索引中的对应条目
4. **备份清理**：清理 `.jsonl.deleted.*` 和 `.jsonl.reset.*` 备份文件

## 使用方式

### 直接清理（用户明确同意时）

```javascript
// 1. 列出所有会话
const sessions = await sessions_list();

// 2. 过滤出 aborted 的子 agent 会话
const abortedSessions = sessions.sessions.filter(s => 
  s.kind === 'other' && 
  s.key.includes('subagent') && 
  s.abortedLastRun === true
);

// 3. 提取会话 ID 并删除对应文件
for (const session of abortedSessions) {
  const sessionId = session.sessionId;
  const filePath = `/Users/miaofengkai115572/.openclaw/agents/main/sessions/${sessionId}.jsonl`;
  // 执行删除
}
```

### 完整清理流程

#### A. 清理已中止的子 agent 会话

1. 调用 `sessions_list()` 获取会话列表
2. 过滤出 `abortedLastRun: true` 且 `key` 包含 `subagent` 的会话
3. **保护近期会话**：排除 48 小时内更新的会话（`updatedAt > Date.now() - 48*60*60*1000`）
4. 向用户展示待删除的文件列表（路径 + 大小 + 最后更新时间）
5. 用户确认后执行删除 `.jsonl` 文件
6. 同步清理 `sessions.json` 中的对应条目

#### B. 清理备份文件

1. 扫描 `*.jsonl.deleted.*` 文件（删除备份）
2. 扫描 `*.jsonl.reset.*` 文件（重置备份，保留 7 天内）
3. 展示待删除的备份文件数量和总大小
4. 用户确认后执行删除

**清理策略**：
- `.deleted` 文件：全部删除（会话已删，备份无用）
- `.reset` 文件：删除 7 天前的（保留近期备份）
- **保护期**：48 小时内的会话不删除（即使 `abortedLastRun: true`）

## 注意事项

- **只删除子 agent 会话**：`key` 包含 `subagent` 的会话
- **只删除已中止的**：`abortedLastRun === true`
- **保留主会话**：不要删除用户正在使用的会话
- **48 小时保护**：不删除 48 小时内更新的会话（即使已中止）
- **建议先预览**：删除前展示文件列表和总大小
- **同步清理 sessions.json**：删除 .jsonl 后必须清理索引文件，否则数据不一致
- **备份文件说明**：
  - `.jsonl.deleted.*` → 会话删除前的备份，可安全删除
  - `.jsonl.reset.*` → 会话重置/压缩前的备份，建议保留 7 天
- **定期清理**：建议每周清理一次备份文件，避免占用过多磁盘空间

## 相关文件

- 会话目录：`~/.openclaw/agents/main/sessions/*.jsonl`
- 会话元数据：通过 `sessions_list()` 获取

## 示例输出

### A. 子 agent 会话清理

```
找到 2 个可清理的已中止子 agent 会话：

| 会话 ID | 大小 | 标签 | 最后更新 |
|---------|------|------|----------|
| 46bf8f99-... | 76K | feishu-creator | 7 天前 |
| a5348a20-... | 149K | feishu-doc-creator | 7 天前 |

已保护：1 个会话（48 小时内更新）
总计可释放：225KB

确认删除？
```

### B. 备份文件清理

```
扫描备份文件：

| 类型 | 文件数 | 总大小 |
|------|--------|--------|
| .deleted | 18 | 2.1 MB |
| .reset (7 天前) | 12 | 4.1 GB |

总计可释放：4.1 GB

确认删除？
```

## 技术实现

### 核心工具

- `sessions_list()` - 获取会话列表和状态
- Node.js `fs` 模块 - 删除会话文件
- `sessions.json` 同步更新 - 保持索引一致性

### 伪代码示例

```javascript
// 获取会话列表
const sessions = await sessions_list();

// 过滤条件
const shouldDelete = sessions.filter(s => 
  s.key.includes('subagent') && 
  s.abortedLastRun === true &&
  Date.now() - s.updatedAt > 48 * 60 * 60 * 1000  // 48 小时保护
);

// 用户确认后删除文件并更新索引
```

## 扩展建议

- 添加 `--dry-run` 模式（预览不删除）
- 添加按时间过滤（只清理 N 天前的）
- 添加按大小过滤（只清理大于 X 的）
- 定期自动清理（结合 heartbeat）
