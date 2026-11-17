# Email Template

## Subject
```
生物医药每日早报｜YYYY-MM-DD
```

## Body Format

```markdown
📪 生物医药每日早报 — YYYY-MM-DD

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 GitHub Trending 日榜 TOP 15
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [owner/repo](https://github.com/owner/repo)
   📝 2-3行简介：项目做什么，为什么火，适合谁用

2. ...

━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 干细胞治疗
━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 **文章标题**
   核心发现/结论（1-2句，仅基于curl实际读取的内容）
   📎 [原文链接](https://mp.weixin.qq.com/s/xxx)

📄 ...

（如该方向0篇合格文章，必须写：）

> 今日无相关前沿动态

━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 外泌体治疗
━━━━━━━━━━━━━━━━━━━━━━━━━━
（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 质谱诊断
━━━━━━━━━━━━━━━━━━━━━━━━━━
（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 拉曼诊断
━━━━━━━━━━━━━━━━━━━━━━━━━━
（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 卵巢癌检测
━━━━━━━━━━━━━━━━━━━━━━━━━━
（同上结构）

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 今日统计
━━━━━━━━━━━━━━━━━━━━━━━━━━
• WeChat 搜索: 5 方向 × 50 篇 = 250 篇
• 48h时间过滤后: X 篇
• 科普/标题党过滤后: X 篇
• 成功阅读正文: X 篇
• GitHub repos: 15 篇
```

## Empty Topic Handling (MANDATORY)

When a topic returns 0 valid articles after full filtering cycle:

```
🧬 干细胞治疗

> 今日无相关前沿动态
```

**Never replace "今日无相关前沿动态" with fabricated content, web search results, or model-generated filler.**

## Link Format (MANDATORY)

Every article link MUST start with `https://mp.weixin.qq.com/`. If the URL is a sogou intermediate link or any other domain, that article MUST NOT appear in the email.

## Sending

Use qqmail skill:
```bash
python3 <qqmail_dir>/scripts/qqmail.py send \
  --to "$QQMAIL_USER" \
  --subject "生物医药每日早报｜YYYY-MM-DD" \
  --body "<email_body>"
```

Recipient: $QQMAIL_USER (the user's own QQ email)
