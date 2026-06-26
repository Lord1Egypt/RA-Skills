# 使用示例

## 基础使用

### 1. 生成标准提案

```bash
freelance-proposal write \
  --job "Need React developer for e-commerce dashboard with real-time analytics" \
  --skills "React, TypeScript, Node.js, MongoDB" \
  --name "John" \
  --save
```

**输出示例**:
```
Hi John,

I've carefully reviewed your project "e-commerce dashboard" and I'm excited about the opportunity to help.

With 5+ years of experience in React, TypeScript, Node.js, MongoDB, I've successfully delivered 50+ similar projects...
```

### 2. 分析客户

```bash
freelance-proposal analyze \
  --client "Looking for experienced developer, must have 5+ years experience, budget flexible" \
  --budget 5000
```

**输出示例**:
```
📊 客户分析

匹配度：75%

痛点:
  • 时间紧迫

建议:
  • 高端定位，强调专业性和 ROI
  • 明确范围，避免范围蔓延
```

### 3. 优化现有提案

```bash
freelance-proposal optimize "Hi, I am interested in your project. I have experience..."
```

**输出示例**:
```
✓ 优化建议

📊 基础分析:
  字数：45 (过短)
  段落数：1

💡 优化建议:
  ⚠ 提案过短，建议扩展到 150-300 字
  ⚠ 缺少个性化称呼
  💡 建议添加问题以增加互动
```

### 4. 查看模板库

```bash
freelance-proposal templates
```

**输出示例**:
```
📋 提案模板库

  STANDARD
  标准投标提案
  适用于大多数项目的标准提案
  结构：个性化开场白 → 展示相关经验 → 提出解决方案 → 明确交付时间 → 呼吁行动

  PREMIUM
  高端定制提案
  针对高预算项目的详细提案
  结构：深度需求分析 → 详细解决方案 → 案例展示 → 分阶段交付计划 → 投资回报说明

  ...
```

### 5. 获取优化技巧

```bash
freelance-proposal tips
```

**输出示例**:
```
💡 成功率优化技巧

OPENING:
  • 前 3 句必须抓住注意力
  • 使用客户姓名增加个性化
  • 提及具体项目细节显示认真阅读
  • 避免通用开场白如"I am interested"

BODY:
  • 展示相关案例和成果
  • 用数据说话（完成率、满意度等）
  • 提出具体问题显示专业度
  • 聚焦客户痛点而非自我吹嘘

...
```

---

## 高级使用

### 使用不同模板

```bash
# 高端提案（适合>$3000 项目）
freelance-proposal write \
  --job "Enterprise CRM system development" \
  --skills "Full-stack development, System architecture" \
  --template premium \
  --save

# 快速提案（适合紧急小额项目）
freelance-proposal write \
  --job "Fix WordPress bug" \
  --skills "WordPress, PHP" \
  --template quick

# 跟进提案
freelance-proposal write \
  --job "Mobile app development" \
  --template followup \
  --name "Sarah"
```

### 交互式使用（未来功能）

```bash
# 启动交互模式
freelance-proposal interactive

# 将引导你完成：
# 1. 输入职位描述
# 2. 输入你的技能
# 3. 选择模板
# 4. 预览并编辑
# 5. 保存或发送
```

---

## 实际案例

### 案例 1: Upwork Web 开发项目

**职位描述**:
```
Looking for a full-stack developer to build a marketplace platform.
Must have experience with React, Node.js, and PostgreSQL.
Budget: $5000-8000
Timeline: 6-8 weeks
```

**使用命令**:
```bash
freelance-proposal write \
  --job "Looking for a full-stack developer to build a marketplace platform. Must have experience with React, Node.js, and PostgreSQL. Budget: \$5000-8000. Timeline: 6-8 weeks" \
  --skills "React, Node.js, PostgreSQL, AWS" \
  --template premium \
  --name "Michael" \
  --save
```

**生成提案**:
```
Dear Michael,

After analyzing your project "marketplace platform", I understand you're looking for an experienced full-stack developer to build a scalable marketplace.

**Why I'm the right fit:**
- Built 3 successful marketplace platforms with 10k+ users
- 7+ years of experience with React and Node.js
- Expert in PostgreSQL optimization and AWS deployment

**My Approach:**
Phase 1: Requirements & Design (2 weeks)
Phase 2: Core Development (4 weeks)
Phase 3: Testing & Launch (2 weeks)

**Investment:** $6,500
**Expected ROI:** Platform ready for 10k+ users, scalable architecture

I've attached relevant case studies. Let's schedule a call to discuss how we can achieve your marketplace goals.

Best,
[Your Name]
[Portfolio Link]
```

### 案例 2: Freelancer 设计项目

**职位描述**:
```
Need logo design for tech startup. Quick turnaround needed.
Budget: $300
```

**使用命令**:
```bash
freelance-proposal write \
  --job "Need logo design for tech startup. Quick turnaround needed." \
  --skills "Logo Design, Branding, Adobe Illustrator" \
  --template quick \
  --save
```

**生成提案**:
```
Hi,

I can help you with logo design for tech startup.

✓ Logo Design
✓ Branding
✓ Adobe Illustrator

Ready to start immediately. Can deliver within 3 days.

Let's chat!
[Your Name]
```

---

## 最佳实践

### ✅ 应该做的
1. **个性化** - 始终使用客户姓名
2. **具体** - 提及项目具体细节
3. **简洁** - 保持 150-300 字
4. **专业** - 展示相关案例
5. **行动** - 包含明确的呼吁行动

### ❌ 不应该做的
1. 通用开场白（"I am interested"）
2. 过长篇幅（>400 字）
3. 过度自我吹嘘
4. 模糊的时间承诺
5. 拼写/语法错误

### 📊 成功率提升技巧
- 24 小时内投标 → 成功率提升 3 倍
- 包含具体数字 → 转化率提升 47%
- 提出问题 → 回复率提升 35%
- 使用客户姓名 → 打开率提升 60%

---

## 故障排除

### 问题：命令未找到
```bash
# 确保已全局安装
npm install -g freelance-proposal-writer

# 或者使用 npx
npx freelance-proposal-writer write --job "..."
```

### 问题：提案生成失败
```bash
# 检查职位描述是否完整
freelance-proposal write --job "完整的职位描述" --skills "你的技能"

# 确保使用引号包裹长文本
freelance-proposal write --job "This is a long job description..." --skills "..."
```

### 问题：模板未找到
```bash
# 查看可用模板
freelance-proposal templates

# 使用正确的模板名称
freelance-proposal write --template standard  # ✓ 正确
freelance-proposal write --template Standard  # ✗ 错误（区分大小写）
```

---

## 获取帮助

```bash
# 查看所有命令
freelance-proposal --help

# 查看特定命令帮助
freelance-proposal write --help
freelance-proposal analyze --help
```

---

**开始生成你的高转化率提案吧！** 🚀
