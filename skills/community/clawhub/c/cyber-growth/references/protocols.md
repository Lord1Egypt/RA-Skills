# Protocols - 里程碑协议

预定义的成就协议，完成时自动解锁。

## 基础协议（Lv.1-3）

| Protocol ID | 名称 | 解锁条件 | 奖励 XP |
|-------------|------|----------|---------|
| `first-blood` | First Blood | 完成第一次成长记录 | 10 |
| `week-streak` | 数据流稳定 (7天) | 连续 7 天有成长记录 | 50 |
| `first-skill` | Chrome 植入 | 发布第一个 skill 到 ClawHub | 100 |
| `multi-domain` | 多线程操作员 | 3 个不同领域都有记录 | 30 |
| `help-one` | 信号初播 | 帮助他人解决第一个问题 | 20 |

## 中级协议（Lv.3-6）

| Protocol ID | 名称 | 解锁条件 | 奖励 XP |
|-------------|------|----------|---------|
| `month-streak` | 数据流稳定 (30天) | 连续 30 天有成长记录 | 150 |
| `five-skills` | Chrome 收藏家 | 发布 5 个 skill 到 ClawHub | 200 |
| `bug-hunter` | 漏洞猎手 | 修复 10 个 bug/问题 | 80 |
| `doc-master` | Doc Codec Master | 编写完整的文档/SKILL.md 5 次 | 60 |
| `automation-king` | 自动化之王 | 创建 10 个自动化脚本 | 100 |

## 高级协议（Lv.6-10）

| Protocol ID | 名称 | 解锁条件 | 奖励 XP |
|-------------|------|----------|---------|
| `quarter-streak` | 数据流稳定 (90天) | 连续 90 天有成长记录 | 500 |
| `ten-skills` | Chrome 帝国 | 发布 10 个 skill 到 ClawHub | 400 |
| `full-stack` | 全栈幽灵 | 8 个领域都达到 Lv.3+ | 300 |
| `mentor` | 神经领主 | 帮助 10 人解决问题 | 200 |
| `system-builder` | 系统架构师 | 搭建完整系统（含监控+自动化+文档） | 300 |

## 自定义 Protocol

在 `~/.openclaw/memory/cyber-growth.json` 的 `customProtocols` 数组中添加：

```json
{
  "id": "my-protocol",
  "name": "我的自定义协议",
  "condition": "完成某项特定成就",
  "rewardXp": 100,
  "unlocked": false,
  "unlockedAt": null
}
```
