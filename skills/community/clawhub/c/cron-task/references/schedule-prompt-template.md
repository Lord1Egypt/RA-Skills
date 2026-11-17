# Schedule Message 提示词模板

> Schedule message 是 TRAE agent 在每次调度时读取的执行指令。
> 必须自包含——agent 在调度时没有会话上下文，只能依赖 message 内容。

---

## 模板结构

```markdown
执行 <任务名> 完整流程：<核心逻辑一句话摘要>

请按顺序执行：

```bash
cd "<project_root>" && python scripts/<task-name>_executor.py
```

任务说明：
- 数据源: <sources>
- 抓取/处理数量: <count>
- <其他关键参数>: <values>
- 凭证: 从环境变量 <VAR_NAMES> 读取（已在 User 级环境变量中配置）

归档要求（三端同步）：
- 飞书云盘: <folder_name>/<date>.md
- Obsidian inbox: <local_path>/<task-name>-<date>.md
- IMA知识库: <kb_id> / <knowledge_name>
- 归档格式: Markdown + 元数据头（任务名/运行时间/数据源/状态）

IM提醒：运行完成后通过 lark-im skill 发送飞书 Interactive Card：
- 卡片标题: <任务名> <date> 运行<状态>
- 卡片内容: 摘要（3-5条要点）
- 卡片按钮: 跳转飞书云盘详情文档

如果主执行器失败，回退到分步：
1. python scripts/<step1>.py <args>
2. python scripts/<step2>.py <args>
3. python scripts/<step3>.py <args>
4. python scripts/<step4>.py <args>

请报告每步执行结果。任何步骤失败都要记录详细错误信息。
归档失败时记录日志但不中断主流程。
```

---

## 变量说明

| 变量 | 来源 | 示例 |
|------|------|------|
| `<任务名>` | 上下文扫描 | ClawHub Daily |
| `<核心逻辑摘要>` | 上下文扫描 | 抓取200个Skill→计算指标→生成推荐→归档→发卡片 |
| `<project_root>` | 工作目录 | d:/TRAE SOLO CN/project |
| `<task-name>` | 任务名kebab-case | clawhub-daily |
| `<sources>` | 数据源扫描 | ClawHub Convex API (wry-manatee-359.convex.cloud) |
| `<count>` | 参数扫描 | 200 |
| `<VAR_NAMES>` | 环境变量扫描 | FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID |
| `<folder_name>` | 飞书云盘文件夹 | ClawHub Daily |
| `<local_path>` | Obsidian inbox路径 | D:/Obsidian/Inbox |
| `<kb_id>` | IMA知识库ID | aFEGG-4YH3z_CaCSNVNC5dSJR5cutjlatcEQcNZjtlA= |
| `<stepN>` | 分步脚本名 | fetch_clawhub / compute_metrics / daily_recommend / push_to_feishu |
| `<date>` | 运行日期 | 2026-07-11 |

---

## 撰写要点

### 1. 自包含性
- agent 在调度时没有会话上下文
- 所有路径、凭证名、参数必须显式写出
- 不用"上次说的那个脚本"这种引用

### 2. 失败回退
- 必须包含至少2层回退（主脚本 → 分步 → 手动提示）
- 分步命令必须可独立执行
- 每步失败都要有明确的处理指令

### 3. 归档指令
- 三端路径必须完整写出
- 归档格式统一为 Markdown + 元数据头
- 任一端失败不中断主流程，只记录日志

### 4. IM提醒指令
- 明确使用 lark-im skill
- 卡片结构：标题 + 摘要 + 按钮
- 状态分类：成功 / 部分失败 / 完全失败

### 5. 执行报告
- 要求 agent 报告每步执行结果
- 失败时记录详细错误信息
- 不要求 agent 自行修复（只报告，不修复）

---

## 完整示例

```markdown
执行 ClawHub Daily 完整流程：抓取 200 个 Skill → 计算指标 → 生成 8-10 个推荐（4维度轮换 + 7天去重 + 痛点匹配）→ 归档三端 → 发送飞书卡片消息

请按顺序执行：

```bash
cd "<project_root>" && python scripts/clawhub_daily_executor.py
```

技能说明：
- 数据源: ClawHub Convex API (wry-manatee-359.convex.cloud)
- 抓取数量: 200 个 Skill
- 推荐维度: 4 个维度轮换（D1 趋势 / D2 质量 / D3 新星 / D4 全景），按日期自动选择
- 去重窗口: 7 天
- 痛点库: 7 大场景（自动化办公/开发工具/内容创作/数据采集/AI 增强/中文支持/金融分析）
- 飞书凭证: 从环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID 读取（已在 User 级环境变量中配置）

归档要求（三端同步）：
- 飞书云盘: ClawHub Daily/2026-07-11.md
- Obsidian inbox: D:/Obsidian/Inbox/clawhub-daily-2026-07-11.md
- IMA知识库: aFEGG-4YH3z_CaCSNVNC5dSJR5cutjlatcEQcNZjtlA= / FIM知识库
- 归档格式: Markdown + 元数据头（任务名/运行时间/数据源/状态）

IM提醒：运行完成后通过 lark-im skill 发送飞书 Interactive Card：
- 卡片标题: ClawHub Daily 2026-07-11 运行<成功/部分失败/失败>
- 卡片内容: 今日推荐Top5 + 总抓取数 + 推荐维度
- 卡片按钮: 跳转飞书云盘详情文档

如果主执行器失败，回退到分步：
1. python "clawhub-daily/scripts/fetch_clawhub.py" --num 200 --date <today>
2. python "clawhub-daily/scripts/compute_metrics.py" --input "data/snapshots/<date>.json"
3. python "clawhub-daily/scripts/daily_recommend.py" --date <today> --data-dir data
4. python "clawhub-daily/scripts/push_to_feishu.py" --recommendation "data/recommended/<date>.json"

请报告每步执行结果。任何步骤失败都要记录详细错误信息。
归档失败时记录日志但不中断主流程。
```
