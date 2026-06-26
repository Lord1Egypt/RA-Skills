---
name: daily-screport-analysis
description: "读取收钱吧邮箱中来自 screport@shouqianba.com（市场邮件推送）的网销数据邮件，进行团队/个人排名分析。触发场景：(1) 用户说「网销排名」「网销数据」「团队排名」「分析排名」「邮件的排名数据」 (2) cron 定时触发的每日排名分析 (3) 用户说「今天的网销数据呢」「网销情况怎样」。用于：网销团队每日排名分析、个人审核通过量排名、新人表现追踪、零单人员统计。"
---

# 每日网销数据排名分析

读取 ligaowei@shouqianba.com 邮箱中 screport@shouqianba.com（市场邮件推送）的邮件，解析并展示网销团队/个人排名数据。

## 依赖项

**必须**：已安装 [imap-smtp-email-chinese](https://clawhub.ai/skills/imap-smtp-email-chinese) skill，并在其 `.env` 中配置好邮箱 IMAP 连接信息：

```bash
# /workspace/skills/imap-smtp-email-chinese/.env
IMAP_HOST=imap.feishu.cn
IMAP_PORT=993
IMAP_USER=ligaowei@shouqianba.com
IMAP_PASS=<邮箱专用密码>
IMAP_TLS=true
```

该 skill 会自动查找 imap-smtp-email-chinese 的 node_modules 和.env，无需单独安装 npm 依赖。

## 邮件类型

来自 **screport@shouqianba.com**（显示名：市场邮件推送）有以下邮件：

| 时间(BJT) | 主题 | 内容 |
|-----------|------|------|
| 09:00 | 「网销每日数据」 | 团队级日/月累计统计（有效转化率、审核通过数等） |
| 10:00-15:00（整点） | 「网销开通实时数据报表」 | 团队主管排名表 + 全员个人排名表 |

## 分析脚本

`scripts/daily-screport-analysis.js` — 核心分析脚本。

### 运行方式

```bash
node /workspace/skills/daily-screport-analysis/scripts/daily-screport-analysis.js
```

### 输出 JSON 结构

```json
{
  "success": true,
  "totalEmails": 10,
  "dailyTeamData": [
    { "team": "起点战队", "leader": "何启明",
      "dailyOpen": 126, "dailyValid": 36, "dailyValidRate": 0.29,
      "dailyApproved": 108, "dailyApprovedRate": 0.93,
      "monthlyOpen": 1849, "monthlyValid": 833, "monthlyValidRate": "0.45",
      "monthlyApproved": 1435, "monthlyApprovedRate": "0.96" }
  ],
  "teamAggregation": [
    { "team": "起点战队", "totalPeople": 12, "totalApproved": 50,
      "avgApproved": 4.2, "topPerson": "孙江宁", "members": [...] }
  ],
  "summary": {
    "totalTeams": 11, "totalPeople": 128, "totalApprovedSum": 290,
    "topTeams": ["起点战队(50单)", "极光战队(42单)", ...],
    "topPeople": ["王广超(飞翔, 13单)", ...],
    "zeroApproved": 56,
    "dailyTotalApproved": 2398, "monthlyTotalApproved": 35672
  }
}
```

### 分析维度

1. **团队主管排名**：团队+主管的审核通过数排名
2. **全员个人排名**：按审核通过数降序排列
3. **团队聚合统计**：人均审核通过数、团队人数、Top成员
4. **新人追踪**：识别2026届新人（名单参考 MEMORY.md）表现
5. **零单人员**：审核通过数为0的人员统计

## 报告格式

按以下结构输出结果给用户：

```
📊 网销团队/个人排名日报 | {日期}

▎团队排名Top5（审核通过数）
🥇 {团队名} — {n}单（{主管}）
...

▎个人排名Top10
1️⃣ {姓名（团队）}{n}单
...

▎团队人均审核通过数
🥇 {团队名} — {n}单/人
...

▎2026新人表现突出
🌟 {姓名（团队）}{n}单
⚪ 零单新人需关注：...

▎月度累计
🗓 全团队月累计：**{n}单**
```

## 配置要求

1. IMAP 邮箱连接（在 imap-smtp-email-chinese/.env 中配置）
2. Standing Orders（写入 AGENTS.md）：授权自动执行
3. Cron 定时任务（工作日 09:35 BJT）：自动触发
