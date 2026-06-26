# Viking 记忆系统技能

## 功能
- 五级记忆层级自动管理（L0→L4）
- 重要记忆保护（永不降级）
- 向量相似度提及检测（动态重要性）
- 飞书群聊会话自动保存（需飞书插件）
- 跨 Agent 共享（global workspace）
- 自动降级与遗忘算法（LLM 压缩）

## 使用方式

### 1. 安装技能

确保以下文件已复制到你的技能目录：
```
cat-viking-memory/
├── config.json
├── SKILL.md
├── memory-pipeline/     # CLI 主入口和脚本
├── simple-viking/       # 向量搜索
└── references/          # 文档
    ├── README.md        # 详细使用说明
    └── 飞书集成说明.md
```

### 2. 基本配置

编辑 `config.json` 中的配置：
```json
{
  "memory_workspace": "~/.openclaw/viking-{agent}",
  "auto_save_enabled": true,
  "feishu_integration": {
    "enabled": false
  }
}
```

### 3. 定时任务（推荐）

每天凌晨 3 点自动执行记忆降级：
```bash
# crontab -e
0 3 * * ~/.openclaw/workspace/agents/maozhuli/cat-viking-memory/memory-pipeline/memory-tier-cron.sh
```

### 4. 飞书自动保存（可选）

如需飞书群聊会话自动保存：

1. 确保 feishu 插件已安装并启用
2. 修改 `config.json`：
   ```json
   "feishu_integration": {
     "enabled": true,
     "check_interval_ms": 300000,
     "timeout_ms": 1800000
   }
   ```
3. 在 feishu 插件配置中启用 SessionManager
4. 参考 `references/飞书集成说明.md` 详细步骤

### 5. 常用命令

```bash
# 加载记忆上下文
memory-pipeline mp_autoload

# 保存记忆
memory-pipeline mp_global "任务完成说明"

# 搜索记忆
sv_find "关键词"

# 手动触发降级（测试）
memory-pipeline/memory-tier-cron.sh
```

## 相关文档

- **详细使用说明**：`references/README.md`
- **飞书集成指南**：`references/飞书集成说明.md`
- **记忆文件格式**：见 `references/README.md` 的"记忆文件格式"章节

## 技术架构

```
存储流程：
输入 → Ontology映射 → Viking存储 → 向量索引 → 检索

层级管理：
L0(0-1天) → L1(2-7天) → L2(8-30天) → L3(30-90天) → L4(90天+)

自动保存：
会话结束 → memory-session-hook.sh → mp_global → 存储

飞书集成：
FeishuSessionManager → 检测超时 → 触发 Hook → 保存
```

## 注意事项

- **存储规范**：必须使用 `memory-pipeline` 命令存取，不要直接操作文件
- **重要记忆**：使用 `--important` 标记永不忘记的关键信息
- **定期检查**：建议每周检查 crontab 是否正常执行
- **权限**：确保脚本有执行权限 `chmod +x memory-pipeline/*.sh`

## 版本历史

- **v1.0.0** - 初始版本
  - 五级记忆层级完整实现
  - 飞书会话自动保存集成
  - 向量搜索与语义检索
  - 自动降级与遗忘算法

---

*基于 OpenViking 思想设计，专为 OpenClaw Agents 打造*
