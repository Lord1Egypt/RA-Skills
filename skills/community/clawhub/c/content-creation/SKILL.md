---
name: content-creation
description: "部署内容创作Agent团队（墨白主编+探风选题+锦书文案），平台无关的内容生产核心。使用 /content-creation 触发，交互式引导配置品牌信息并自动部署。"
license: MIT
---

# 内容创作团队 - 自动部署

当用户调用 /content-creation 时，执行以下步骤部署 3 人内容创作 Agent 团队。

## 概述

部署平台无关的内容创作核心团队：
- 墨白（主编/审核）、探风（选题策划）、锦书（文案创作）

## Step 1：环境检查

1. 执行 `which openclaw`，确认 OpenClaw 已安装
   - 未安装 → 输出"请先安装 OpenClaw：https://openclaw.ai"→ **终止**
2. 执行 `openclaw agents list`，检查是否已存在 mobai/tanfeng/jinshu
   - 已存在 → 提示用户：团队已部署，是否覆盖？用户拒绝 → **终止**

## Step 2：交互式收集品牌与创作信息

分三轮收集，每轮一次性提问，减少来回次数。用户任意时刻输入"取消" → **终止部署**。

### 第一轮：账号基础（一次性提问）

向用户发送以下消息，等待回复：

```
我需要了解你的账号基础信息，请一次性回答以下问题（可以用序号对应）：

1. 账号/品牌名称是什么？
2. 一句话描述账号定位（是什么、为谁服务、提供什么价值）？
3. 目标读者是谁？（年龄、职业、兴趣、痛点）
4. 主打内容领域？（可多选，如：职场成长 / 科技数码 / 生活方式 / 知识科普）
```

### 第二轮：创作风格（一次性提问）

向用户发送以下消息，等待回复：

```
接下来了解你的内容创作偏好：

5. 文风偏好？（如：专业严谨 / 轻松幽默 / 温暖治愈 / 犀利观点）
6. 有没有 2-3 个你欣赏的对标账号或文章风格参考？（帮助团队理解你想要的感觉）
7. 你的读者最关心什么问题 / 最常遇到什么痛点？（这是选题的核心依据）
8. 有哪些话题或表达方式是绝对不能碰的？
```

### 第三轮：内容规划（一次性提问）

向用户发送以下消息，等待回复：

```
最后是内容规划信息：

9.  发布节奏？（如：每周 2 篇 / 每周 3 篇）
10. 每篇文章期望字数范围？（如：1500-2500 字）
11. 品牌调性关键词，3-5 个词概括你的内容气质？（如：专业、有温度、接地气）
12. 近期有没有想重点发力的内容方向或主题？（可选，没有可跳过）
```

将三轮答案整理后暂存备用。

## Step 3：创建目录结构并部署文件

1. 创建团队根目录：
   ```bash
   mkdir -p ~/.openclaw/workspace-content-creation
   ```
2. 从 `{baseDir}/templates/` 目录复制文件到 3 个子目录：
   ```
   ~/.openclaw/workspace-content-creation/mobai/
   ~/.openclaw/workspace-content-creation/tanfeng/
   ~/.openclaw/workspace-content-creation/jinshu/
   ```
3. 将 Step 2 收集的信息写入每个子目录的 USER.md，按以下映射替换占位符：
   - `{{account_name}}` → 第1题答案
   - `{{positioning}}` → 第2题答案
   - `{{target_audience}}` → 第3题答案
   - `{{main_topics}}` → 第4题答案
   - `{{writing_style}}` → 第5题答案
   - `{{reference_accounts}}` → 第6题答案（未填写则填"暂无"）
   - `{{reader_pain_points}}` → 第7题答案
   - `{{forbidden_topics}}` → 第8题答案
   - `{{publish_frequency}}` → 第9题答案
   - `{{article_length}}` → 第10题答案
   - `{{brand_keywords}}` → 第11题答案
   - `{{focus_topics}}` → 第12题答案（未填写则填"暂无"）
4. 每完成一个目录，输出进度：
   ```
   [1/3] mobai（墨白 - 主编）→ 已部署
   [2/3] tanfeng（探风 - 选题策划师）→ 已部署
   [3/3] jinshu（锦书 - 文案创作师）→ 已部署
   ```

## Step 4：注册 Agent

```bash
openclaw agents add mobai \
  --name "墨白" \
  --workspace "~/.openclaw/workspace-content-creation/mobai" \
  --description "主编/内容总监 - 内容战略与质量把控"

openclaw agents add tanfeng \
  --name "探风" \
  --workspace "~/.openclaw/workspace-content-creation/tanfeng" \
  --description "选题策划师 - 热点追踪与选题规划"

openclaw agents add jinshu \
  --name "锦书" \
  --workspace "~/.openclaw/workspace-content-creation/jinshu" \
  --description "文案创作师 - 文章撰写与标题优化"
```

幂等性：如果 agent 已存在，跳过并提示"已存在，跳过注册"。

## Step 5：验证部署

1. 执行 `openclaw agents list`，确认 3 个 agent 注册成功
2. 输出部署报告：
   ```
   ✅ 内容创作团队部署完成
   ├── ✍️  墨白（主编）          → 已就绪
   ├── 🔍 探风（选题策划师）    → 已就绪
   └── 📝 锦书（文案创作师）    → 已就绪
   ```

## Step 6：后续指引

1. 使用团队：输入 `/content-pipeline` 启动内容创作流水线
2. 自定义角色：编辑 `~/.openclaw/workspace-content-creation/<agent>/SOUL.md`
3. 如需发布到微信公众号：安装 `/wechat-publisher` 并使用 `/wechat-publish-pipeline`
4. 如需发布到其他平台：安装对应平台的发布 Skill

## 错误处理

- `openclaw` 命令不存在 → 提示安装链接，终止
- 目录创建失败 → 检查权限
- Agent 注册失败 → 检查是否重名（`openclaw agents list`）
