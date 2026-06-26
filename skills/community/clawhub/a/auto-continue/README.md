# ▶️ auto-continue

> 任务自动续接。当 Agent 停下等待指令时，主动判断下一步并继续执行。

## 核心问题

Agent 写完 SKILL.md 停下来等用户说"继续" → 浪费时间。

## 解决方案

每当你发来消息且有未完成任务，Agent 自动：
1. 读取 `memory/in_progress.md` 状态
2. 扫描 skills 目录检查完整性
3. 继续执行下一项
4. 更新进度
5. 完成所有步骤后再汇报

## 规则

**任务没完 = 不能停**
- 写了 SKILL.md 但没写脚本 → 立即写脚本
- 写了脚本但没测试 → 立即测试
- 测试通过但没上架 → 立即上架
- 所有步骤完成才汇报

## 安装

```bash
python3 scripts/check_progress.py --check
```
