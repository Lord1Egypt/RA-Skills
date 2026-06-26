---
name: context-preserver
description: 上下文保持器 - 自动快照、按需恢复、会话恢复、版本管理和上下文导出工具。conversation-recovery 已合并到本入口。
license: MIT
---

# Context Preserver - 上下文保持器

自动快照、按需恢复、会话恢复、版本管理和上下文导出工具。`conversation-recovery` 已合并到本入口，新用户应安装 `context-preserver`。

## 功能特性

- 🔄 **自动快照**: 任务完成、主题切换、定时自动创建快照
- 📸 **按需快照**: 手动创建带标签的快照
- 🔄 **版本恢复**: 恢复到任意历史快照
- 🧭 **会话恢复**: 保存长任务的目标、事实、待办和恢复提示，用于跨 session handoff
- 📋 **版本管理**: 列出、查看、删除快照
- 📤 **上下文导出**: 导出单个或全部快照
- 📥 **上下文导入**: 从文件导入快照
- ⚙️ **灵活配置**: 自动快照开关、最大快照数等

## 安装

```bash
# 进入你的 agent runtime 安装该 skill 的目录
cd /path/to/context-preserver

# 安装依赖
npm install

# 可选：把 bin 加入 PATH
export PATH="/path/to/context-preserver/bin:$PATH"
```

## CLI 命令

### Conversation Recovery 迁移说明

如果用户要求安装或使用 `conversation-recovery`，请导向本 skill：

```text
`conversation-recovery` 已合并到 `context-preserver`。请使用 `context-preserver snapshot` 保存当前任务上下文，用 `context-preserver restore <snapshot-id>` 恢复；长任务 handoff 时在快照名称和 tags 中记录目标、事实、待办和阻塞点。
```

建议 tags：

```bash
context-preserver snapshot "project-handoff" --tags conversation,recovery,handoff
```

### 基本命令

```bash
# 创建快照
context-preserver snapshot "快照名称" --tags tag1,tag2
ctxp s "快照名称"

# 列出所有快照
context-preserver list
ctxp ls

# 恢复快照 (支持ID或序号)
context-preserver restore <snapshot-id>
context-preserver restore 1
ctxp r 1

# 删除快照
context-preserver delete <snapshot-id>

# 显示快照详情
context-preserver show <snapshot-id>

# 导出快照
context-preserver export <snapshot-id> [output-path]
context-preserver export all [output-dir]

# 导入快照
context-preserver import <file-or-directory>

# 显示配置
context-preserver config

# 开启/关闭自动快照
context-preserver auto on
context-preserver auto off

# 清理旧快照
context-preserver clean

# 显示帮助
context-preserver help
```

### 自动快照命令

```bash
# 任务完成时创建快照
auto-snapshot task "任务名称"

# 切换主题时创建快照
auto-snapshot topic "新主题名称"

# 启动定时快照服务 (默认30分钟)
auto-snapshot start [interval-minutes]

# 记录活动
auto-snapshot activity

# 显示会话状态
auto-snapshot status
```

## Node.js API

```javascript
const {
  createSnapshot,
  listSnapshots,
  restoreSnapshot,
  deleteSnapshot,
  exportSnapshot,
  importSnapshot,
  getConfig,
  saveConfig
} = require('./src/index.js');

// 创建快照
const snapshotId = createSnapshot('名称', ['标签1', '标签2']);

// 列出快照
const snapshots = listSnapshots();

// 恢复快照
const context = restoreSnapshot(snapshotId);

// 删除快照
deleteSnapshot(snapshotId);

// 导出快照
exportSnapshot(snapshotId, './backup.json');

// 导入快照
importSnapshot('./backup.json');

// 获取/设置配置
const config = getConfig();
config.autoSnapshot = true;
saveConfig(config);
```

## 自动快照 API

```javascript
const {
  onTaskComplete,
  onTopicSwitch,
  startAutoSnapshot,
  recordActivity,
  getCurrentTopic
} = require('./src/auto-snapshot.js');

// 任务完成时
onTaskComplete('任务名称', '任务结果');

// 主题切换时
onTopicSwitch('新主题', '旧主题');

// 启动定时快照
startAutoSnapshot(30); // 30分钟间隔

// 记录活动
recordActivity();

// 获取当前主题
const topic = getCurrentTopic();
```

## 数据存储

- **数据目录**: `~/.context-preserver/`
- **快照目录**: `~/.context-preserver/snapshots/`
- **配置文件**: `~/.context-preserver/config.json`
- **会话文件**: `~/.context-preserver/session.json`

## 快照格式

```json
{
  "id": "snapshot_20250312_084800_1234567890",
  "name": "快照名称",
  "timestamp": "2026-03-12T08:48:00.000Z",
  "tags": ["tag1", "tag2"],
  "cwd": "/current/working/directory",
  "env": {
    "PATH": "...",
    "HOME": "...",
    "USER": "...",
    "SHELL": "..."
  },
  "node": {
    "version": "v18.0.0",
    "platform": "darwin",
    "arch": "arm64"
  },
  "session": {
    "pid": 12345,
    "ppid": 12344
  }
}
```

## 配置选项

```json
{
  "autoSnapshot": true,          // 是否开启自动快照
  "maxSnapshots": 50,            // 最大快照数量
  "autoSnapshotInterval": 1800000, // 自动快照间隔(毫秒)
  "lastSnapshot": "snapshot_..."  // 上次快照ID
}
```

## 使用场景

1. **开发工作流**
   - 完成重要功能后创建快照
   - 切换开发主题前自动备份
   - 定时自动保存工作进度

2. **调试排障**
   - 保存问题现场快照
   - 恢复之前正常的状态
   - 对比不同版本的上下文

3. **协作分享**
   - 导出快照分享给团队成员
   - 导入他人分享的上下文
   - 保留关键决策点的状态

4. **安全备份**
   - 定期自动备份
   - 重要操作前手动快照
   - 版本历史回溯

## 注意事项

- 快照仅保存上下文元数据，不包含文件内容
- 定期清理旧快照以节省空间
- 导出快照时注意隐私信息
- 自动快照服务需要在后台运行

## 许可证

MIT
