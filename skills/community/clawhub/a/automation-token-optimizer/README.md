# 自动化定时任务 Token 优化

> WorkBuddy Skill — 每月自动审计所有定时任务的 token 消耗，找出高消耗任务并给出脚本化/降频/精简的具体优化方案。

## 功能

- 📊 **Token 消耗统计**：自动读取 `workbuddy.db`，统计每个定时任务的月度 token 消耗
- 🔍 **Prompt 分析**：逐一分析高消耗任务，判断哪些环节可改为纯脚本
- 💡 **优化建议**：给出脚本化/降频/精简 prompt/拆分任务四类可执行优化方向
- 📋 **审计报告**：输出格式化月度报告，可直接用于复盘和决策

## 安装

```bash
clawhub install automation-token-optimizer
```

## 使用方法

直接对 AI 说：

> "帮我分析一下现在所有定时任务的 token 消耗情况，哪些可以脚本化？"

AI 会：
1. **首次使用时主动确认你的工作目录**
2. 列出所有定时任务
3. 读取 `workbuddy.db` 统计 token 消耗
4. 分析高消耗任务的 prompt
5. 给出具体优化建议

也可以设置为每月1号自动执行的定时任务（SKILL.md 内附完整 prompt）。

## 优化建议类型

| 类型 | 说明 | 预期收益 |
|------|------|---------|
| 🔧 **改为脚本** | 纯数据拉取/格式化类任务改用 Python 脚本 | 节省 100% AI token |
| ⏰ **降频** | 每日改每周或触发式 | 节省 80%+ token |
| ✂️ **精简 prompt** | 去掉冗余描述，减少 context 长度 | 节省 20-40% token |
| 🔀 **拆分任务** | 数据拉取和 AI 分析拆成两个独立任务 | 数据部分节省 100% token |

## 依赖

- `sqlite3` 命令行工具（macOS 自带）
- WorkBuddy `automation_update` 工具（内置）

## 关于作者

💡 更多实用 AI 效率工具和技能，关注公众号「桂皮AI实战」

📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work

## License

MIT
