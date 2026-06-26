# Daily Report Catch-Up Skill

> **作者**: colbertlee  
> **版本**: 1.5.0  
> **许可证**: MIT-0

码虫日报补课系统 - 基于 Hermes Agent 学习循环思路

## 更新日志 (v1.5.0)

### 修复内容
- **check_quality.py KeyError**：文件不存在或为空时，返回完整 dict（含 sections_found 等字段）
- **check_quality.py exit code**：默认返回 0，避免自动化误判；新增 `--check-only` 获取真实状态码
- **catch-up.py 调用模式**：新增 `--detect`（只检测）、`--quiet`（静默）模式
- **skills.sh symlink 警告**：过滤 `reason=symlink-escape` 和 `Skipping escaped skill path` 警告
- **catch-up.sh 注释**：添加 exec 预检安全机制说明（需使用绝对路径）

### 新增内容
- **TEMPLATE.md**：内置标准日报模板（今日工作、学习、复盘、明日计划）
- **集成说明**：在 `daily-precheck.cjs` 中集成作为质量保障层

---

## 功能模块

| 脚本 | 功能 |
|------|------|
| `catch-up.py` | 漏发检测 + 自动补录 |
| `check_quality.py` | 日报质量检查 |
| `multi_agent_monitor.py` | 多 Agent 汇总监控 |
| `dashboard.py` | HTML 可视化 Dashboard |
| `skills.sh` | 技能管理美化脚本 |
| `TEMPLATE.md` | 内置日报模板（标准板块） |
| `REPORT_CHECKLIST.md` | 质量检查清单 |

## 1. 漏发检测与补录

```bash
# 完整模式（检测 + 生成补录）
bash skills/daily-report-catchup/catch-up.sh

# 只检测，不生成（用于预检集成）
python3 skills/daily-report-catchup/catch-up.py --detect

# 静默模式（无输出，只返回 exit code: 0=无漏发, 1=有漏发）
python3 skills/daily-report-catchup/catch-up.py --quiet
```

**检测逻辑**：
- 扫描过去 7 个工作日
- INDEX 无记录 → 标记为 `missed` 并补录
- success 文件丢失 → 补录
- failed/skipped 无文件 → 正常，不补录

**退出码**：
- `0` - 无漏发
- `1` - 有漏发（已补录或待补录）

## 2. 日报质量检查

```bash
# 标准检查（完整输出）
python3 skills/daily-report-catchup/check_quality.py <报告文件>

# 静默模式（只返回 exit code: 0=合格, 1=不合格）
python3 skills/daily-report-catchup/check_quality.py --check-only <报告文件>

# 详细模式（包含问题列表）
python3 skills/daily-report-catchup/check_quality.py <报告文件> --verbose
```

**评分标准**：
- ⭐⭐⭐ ≥90分：优秀
- ⭐⭐ ≥60分：合格
- ⭐ ≥30分：需改进
- ❌ <30分：不合格

> ⚠️ **注意**：默认 exit code 始终为 0，避免自动化场景被误判为错误。使用 `--check-only` 获取实际质量状态码。

## 3. 多 Agent 汇总监控

```bash
python3 skills/daily-report-catchup/multi_agent_monitor.py
```

## 4. HTML Dashboard 可视化

```bash
python3 skills/daily-report-catchup/dashboard.py [输出路径]
# 默认输出: /tmp/daily-report-dashboard.html
```

打开生成的 HTML 文件即可查看可视化 Dashboard。

## 5. 技能管理助手

```bash
# 查看已安装的技能
bash skills/daily-report-catchup/skills.sh list

# 搜索技能（美化输出）
bash skills/daily-report-catchup/skills.sh search daily-report-catchup

# 安装技能
bash skills/daily-report-catchup/skills.sh install <技能名>

# 更新技能
bash skills/daily-report-catchup/skills.sh update [技能名]
```

## 6. 日报模板

内置标准板块，新写日报时直接使用：

```bash
# 查看模板
cat skills/daily-report-catchup/TEMPLATE.md

# 生成带模板的新日报
cp skills/daily-report-catchup/TEMPLATE.md memory/daily-reports/$(date +%Y-%m-%d).md
```

**标准板块**：
- 📋 今日工作
- 📚 学习总结
- 🔍 复盘（做得好的 + 需要改进）
- 💡 明日计划 / 建议

## 7. 部署到其他 Agent

```bash
# 搜索
openclaw skills search daily-report-catchup

# 安装
openclaw skills install daily-report-catchup
```

## 配置多工作区监控

编辑 `dashboard.py` 和 `multi_agent_monitor.py` 开头的工作区列表：
```python
WORKSPACES = [
    "/path/to/workspace-1",
    "/path/to/workspace-2",
    # 添加更多...
]
```

## 索引格式

```
| 日期 | 星期 | 状态 | 执行时间 | 备注 |
|------|------|------|----------|------|
```

**状态枚举**：
- `success` - 发送成功
- `failed` - 发送失败
- `skipped` - 跳过（周末/节假日）
- `missed` - 漏发（系统离线）
- `caught-up` - 漏发后补录

## 文件结构

```
skills/daily-report-catchup/
├── SKILL.md                 # 本文件
├── catch-up.sh              # 入口脚本（含 exec 预检说明）
├── catch-up.py              # 漏发检测核心（支持 --detect/--quiet）
├── check_quality.py         # 质量检查（修复 KeyError + exit code）
├── multi_agent_monitor.py   # 多 Agent 监控
├── dashboard.py              # HTML Dashboard
├── skills.sh                # 技能管理助手（过滤 symlink 警告）
├── TEMPLATE.md              # 内置日报模板
└── REPORT_CHECKLIST.md      # 质量清单（含快速开始）
```
