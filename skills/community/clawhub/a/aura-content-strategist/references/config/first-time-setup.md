# First-Time Setup

Run when EXTEND.md not found. Collect user preferences for persistent configuration.

## Questions (Ask in Order)

### 1. Account Handles
```
你的账号信息：
- 小红书账号名: [用户输入]
- Pinterest账号名: [用户输入]
```

### 2. Niche/Vertical
```
你的主要内容方向是什么？
选项: 美妆 / 家居 / 穿搭 / 美食 / 科技 / 生活方式 / 其他
[用户选择或输入]
```

### 3. Target Audience
```
你的目标受众是？
选项: 学生党 / 打工人 / 宝妈 / 精致女孩 / 技术宅 / 其他
[用户选择或输入]
```

### 4. Brand Colors (Optional)
```
你有品牌主色调吗？（可选，用于视觉方案）
格式: #hex1, #hex2, #hex3
[用户输入或跳过]
```

### 5. Posting Schedule (Optional)
```
你的发布频率？
选项: 每天 / 每周3-5次 / 每周1-2次 / 不固定
[用户选择]
```

### 6. Content Language
```
你的内容主要用什么语言？
- 小红书: [默认中文，可改]
- Pinterest: [默认英文，可改]
```

### 7. Monetization Goal (Optional)
```
你的变现目标是？（可选）
选项: 接广告 / 带货 / 引流私域 / 纯涨粉 / 暂无
[用户选择]
```

## Save Location

After collecting, save to:

**Priority 1 (Project-level)**:
```
.baoyu-skills/aura-content-strategist/EXTEND.md
```

**Priority 2 (User-level)**:
```
$HOME/.baoyu-skills/aura-content-strategist/EXTEND.md
```

Ask user: "保存到项目目录还是用户目录？(project/user)"

## EXTEND.md Format

```yaml
---
# Aura Content Strategist Preferences
version: 1.0

accounts:
  xiaohongshu: "账号名"
  pinterest: "账号名"

niche: "美妆"
target_audience: "学生党"

brand_colors:
  - "#FF6B9D"
  - "#C44569"
  - "#FFC048"

posting_schedule: "每周3-5次"

content_language:
  xiaohongshu: "zh"
  pinterest: "en"

monetization_goal: "接广告"
---
```

## After Setup

Confirm saved location and proceed to Step 1 (Briefing).
