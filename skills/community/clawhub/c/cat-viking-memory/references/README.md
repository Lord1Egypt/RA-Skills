# Viking 记忆系统

适用于 OpenClaw AI Agents 的轻量级、纯文本上下文管理系统。

## 核心思想

1. **五级记忆层级**：L0 → L1 → L2 → L3 → L4，按时间自动降级
2. **重要记忆保护**：手动标记的重要记忆不降级
3. **动态重要性**：向量相似度检测，被反复提及的记忆重要性提升
4. **自动保存**：会话结束自动保存 + 凌晨定时处理
5. **向量搜索**：语义检索 + 关键词混合搜索
6. **跨 Agent 共享**：全局记忆供所有 Agent 访问

## 记忆层级

| 层级 | 目录 | 时间范围 | 内容保留 |
|------|------|---------|---------|
| L0 | hot/ | 0-1天 | 100% 完整细节 |
| L1 | warm/ | 2-7天 | 70% 核心轮廓 |
| L2 | cold/ | 8-30天 | 30% 关键词 |
| L3 | archive/ | 30-90天 | 10% 标签 |
| L4 | archive/ | 90天+ | 仅标题 |
| 重要 | important/ | 永久 | 不降级 |

## 记忆衰减（降级）规则

每天凌晨自动执行降级，每个层级的压缩规则：

- **L0 → L1**：保留标题、标签、背景、结果、待办，去掉部分细节
- **L1 → L2**：仅保留标题和结果
- **L2 → L3**：仅保留标题和标签
- **L3 → L4**：仅保留标题

## 重要记忆分类

以下记忆会被保护，不参与降级：

1. **显式标记**：`importance: high`
2. **标签包含**：`重要`、`高优先级`
3. **内容关键词**：`紧急`、`严重`、`致命`、`关键决策`、`重要里程碑`

## 动态重要性机制

### 核心思路
- 不那么重要的记忆，如果被**反复提及** → 变得重要
- 重要的记忆，如果**长期不被提及** → 变得不那么重要

### 向量相似度提及检测

每次会话结束时，用本次会话内容与历史记忆做向量相似度匹配：

```
会话结束 
    ↓
提取本次会话内容
    ↓
与 hot/ warm/ 中的历史记忆做向量相似度
    ↓
相似度 > 0.63 → access_count +1
```

**匹配规则：**
- 相似度阈值：0.63
- 匹配成功 → 该记忆的 access_count +1

### 动态调整规则

| 条件 | 行为 |
|------|------|
| 访问次数 > 10 | low → medium |
| 访问次数 > 20 | 自动标记重要 |
| 30天未访问 | 重要性降级 |
| 90天+ 未访问 | 封存到 archived/ |

## 目录结构

```
viking-{agent}/
├── agent/memories/
│   ├── hot/          # L0: 0-1天
│   ├── warm/         # L1: 2-7天
│   ├── cold/        # L2: 8-30天
│   ├── archive/     # L3-L4: 30天+
│   ├── important/   # 重要记忆（不降级）
│   └── archived/    # 封存库
├── user/
│   └── preferences/  # 用户偏好
└── shared/          # 跨 Agent 共享
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/TanDongTaotao/viking-memory-system.git

# 添加到 PATH
export PATH="$HOME/viking-memory-system/memory-pipeline:$HOME/viking-memory-system/simple-viking:$PATH"
```

## 使用方式

### 保存记忆
```bash
# 存储到 hot (L0)
memory-pipeline mp_store --content "内容" --title "标题"

# 写入全局记忆
memory-pipeline mp_global "任务完成：xxx"
```

### 搜索记忆
```bash
# 混合搜索
memory-pipeline mp_search "关键词"

# 或使用 simple-viking
sv hybrid "关键词"
```

### 提及检测（动态重要性）
```bash
# 手动检测
mp_mention_detect.sh detect "会话内容" [agent]
```

### 自动加载
```bash
memory-pipeline mp_autoload
# 或
sv autoload maojingli
```

## 定时任务（Cron）

每天凌晨 3 点自动执行：

1. **智能提取**：从昨日会话中提取摘要
2. **降级处理**：L0→L1→L2→L3→L4
3. **向量索引**：构建语义搜索索引

```bash
# crontab -e
0 3 * * * ~/viking-memory-system/memory-pipeline/memory-tier-cron.sh
```

## 脚本说明

### memory-pipeline/
| 脚本 | 功能 |
|------|------|
| `memory-pipeline` | CLI 主入口 |
| `memory-auto-save.sh` | 会话结束自动保存 |
| `memory-session-hook.sh` | 会话钩子（含提及检测） |
| `memory-tier-cron.sh` | 定时任务入口 |
| `memory-tier-downgrade.sh` | 记忆降级处理 |
| `memory-extract-summary.sh` | LLM 智能摘要 |
| `mp_mention_detect.sh` | 向量相似度提及检测 |

### simple-viking/
| 脚本 | 功能 |
|------|------|
| `sv` | 向量搜索 CLI |
| `sv_autoload.sh` | 自动加载上下文 |
| `lib.sh` | 基础库 |

## Bug 修复记录

1. ✅ tier 格式不识别 → 添加 `tier: L0` 支持
2. ✅ L0→L1 文件丢失 → 修复删除逻辑
3. ✅ global 错误生成记忆 → 跳过自动保存
4. ✅ 自动保存误判重要 → 简化判断逻辑
5. ✅ 新增：向量相似度提及检测
6. ✅ 新增：飞书群聊会话自动检测保存

---

## 飞书群聊会话自动保存（扩展功能）

配合 Viking 记忆系统使用，可自动判断飞书群聊会话结束，自动保存记忆。

### 功能特性

- **自动检测**：每5分钟检查会话活跃状态
- **超时保存**：30分钟无新消息自动触发记忆保存
- **多会话支持**：每个飞书群聊独立计时，互不影响
- **无缝集成**：自动调用 `memory-session-hook.sh` 保存记忆

### 工作原理

```
飞书群收到消息
    ↓
更新会话活跃时间
    ↓
每5分钟检查所有会话
    ↓
超过30分钟无新消息
    ↓
调用 memory-session-hook.sh 保存记忆
```

### 安装

飞书插件需要安装 OpenClaw 飞书扩展：

```bash
# 确保已安装飞书插件
openclaw plugins install feishu
```

### 配置

会话管理器代码位于飞书插件中：

```
~/.npm-global/lib/node_modules/openclaw/extensions/feishu/src/session-manager.ts
```

**默认参数：**
- 检查间隔：5分钟
- 超时时间：30分钟

如需修改，可编辑源码中的配置：

```typescript
const config = {
  checkIntervalMs: 5 * 60 * 1000,  // 5分钟
  timeoutMs: 30 * 60 * 1000,        // 30分钟
};
```

### 使用

1. 启动 OpenClaw Gateway：
   ```bash
   openclaw gateway start
   ```

2. 在飞书群聊中正常对话，系统会自动检测会话结束

3. 30分钟无新消息后，自动保存记忆到 Viking 系统

### 日志

查看会话管理器日志：
```bash
tail -f /tmp/openclaw/openclaw-YYYY-MM-DD.log | grep session-manager
```

---

基于 OpenViking 思想设计
