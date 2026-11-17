---
name: fitness-planner
description: 健身规划助手，支持训练计划生成、打卡记录、统计周报、自动调整强度、动作讲解和视频教学搜索。触发词：健身、训练计划、打卡、今天练什么、运动、降低强度、增加强度、动作讲解。
---

# Fitness Planner - 健身规划助手

一个帮助用户规划、追踪和调整健身训练的助手。核心理念：**权威模板 + 低负担反馈**。

## 触发场景

- 用户问"帮我安排健身计划"、"生成训练计划"
- 用户说"今天练什么"、"训练提醒"
- 用户说"打卡"、"完成训练"
- 用户说"这周练得怎么样"、"健身周报"
- 用户提到健身、锻炼、运动安排相关话题

## 使用方式

### 调用代码模块

本 skill 包含完整的 TypeScript 实现，通过以下方式调用：

```bash
# 编译
cd ~/.openclaw/workspace/skills/fitness-planner
npm install
npm run build
```

### 在对话中使用

直接响应用户的自然语言输入，根据关键词识别意图：

| 用户输入 | 识别为 | 动作 |
|---------|--------|------|
| 初始化/开始配置 | init | 引导配置流程 |
| 生成计划/安排计划 | plan | 生成周计划 |
| 今天/今日 | today | 返回今日计划 |
| 打卡/完成 | checkin | 记录训练完成 |
| 太累/一般/没练够 | feeling | 更新感受 |
| 本周/进度 | progress | 显示周进度 |
| 统计/数据 | stats | 显示统计数据 |
| 周报/总结 | summary | 生成周总结 |
| 历史/记录 | history | 查看历史记录 |
| 配置/设置 | config | 查看/修改配置 |
| 动作讲解/教学 | exercise | 查看动作详细讲解 |

### 核心功能实现

#### 1. 初始化配置

检查配置完整性，引导用户填写：

```
健身规划助手初始化
==================

请回答几个简单问题（可随时修改）：

1. 性别：男 / 女
2. 年龄：____岁
3. 训练目标：增肌 / 减脂 / 塑形 / 保持 / 增强体能
4. 训练场地：健身房 / 居家徒手 / 户外跑步
5. 每周训练天数：3天 / 4天 / 5天 / 6天
6. 每次训练时长：30分钟 / 45分钟 / 60分钟
7. 健身经验：新手（<6个月）/ 中级（6-24个月）/ 高级（>24个月）
```

**配置存储：** `~/.openclaw/workspace/fitness-planner/config.json`

#### 2. 生成周计划

基于用户配置，从训练模板库中选择：

**计划选择逻辑：**
```
IF 居家 → 居家徒手计划
IF 减脂 AND 户外 → 跑步计划
IF 减脂 AND 时间少 → HIIT
IF 新手 → 全身训练A/B
IF 中级 AND 增肌 → PPL分化
IF 高级 AND 增肌 → 上肢下肢分化
DEFAULT → PPL
```

**计划类型：**
- beginner-fullbody: 新手全身训练（3天）
- push-pull-legs: 推拉腿分化（3-6天）
- upper-lower: 上肢下肢分化（4天）
- home-bodyweight: 居家徒手（3-5天）
- running: 跑步计划（3-4天）
- hiit: HIIT燃脂（3天）

#### 3. 今日训练

```
🏋️ 今日训练提醒

📋 推日 - 胸、肩、三头
⏱️ 预计 45 分钟

动作清单：
✓ 卧推 4×8-10
   💡 收紧肩胛骨，胸部挺起
✓ 上斜哑铃推举 3×10-12
   💡 角度不要超过45°
```

#### 4. 动作讲解（含视频教学）

用户可以查看单个或所有动作的详细讲解，系统会自动搜索 B站教学视频：

```
用户：动作讲解 卧推

📌 卧推

📺 https://www.bilibili.com/video/BVxxxxx/
   > 撸铁孔先森

动作步骤：
1. 平躺在卧推凳上，双脚踩稳地面
2. 双手握杠，握距略宽于肩
3. 下放杠铃至胸部中段，手肘约45°角
4. 推起杠铃至手臂伸直，顶峰收缩胸肌

要点：
• 收紧肩胛骨，胸部挺起
• 下放时吸气，推起时呼气
• 手腕保持中立，不要过度后伸

常见错误：
✗ 手肘外展90°，容易伤肩
✗ 起桥过高，借力腰腹
```

当没有指定动作名时，显示今日所有动作的讲解和视频链接。

**视频搜索功能：**
- 自动调用 exa 搜索 B站教学视频
- 缓存搜索结果 30 天，避免重复搜索
- 缓存文件：`fitness-planner/video-cache.json`

#### 4. 打卡流程

1. 用户说「打卡」→ 记录完成
2. 自动更新统计
3. 询问感受：😫 太累 / 😐 一般 / 💪 没练够

#### 5. 周总结

```
📊 本周训练总结

打卡：5/6 天
总时长：约 4 小时
感受分布：💪 3次 😐 2次 😫 0次

💡 建议：
   - 本周完成率较高，状态良好
```

## 数据文件

| 文件 | 路径 | 说明 |
|------|------|------|
| config.json | fitness-planner/config.json | 用户配置 |
| stats.json | fitness-planner/stats.json | 统计数据 |
| current_week.json | fitness-planner/plans/ | 当前周计划 |
| YYYY-MM.json | fitness-planner/records/ | 月度记录 |

## 代码结构

```
fitness-planner/
├── SKILL.md              # 本文件
├── package.json          # Node.js 配置
├── tsconfig.json         # TypeScript 配置
├── src/
│   ├── index.ts          # 主入口
│   ├── config.ts         # 配置管理
│   ├── templates.ts      # 训练模板
│   ├── recorder.ts       # 打卡记录
│   ├── stats.ts          # 统计模块
│   └── notifier.ts       # 消息格式化
├── references/
│   ├── templates.md      # 训练模板文档
│   └── exercises.md      # 动作库文档
└── scripts/
    └── init.sh           # 初始化脚本
```

## 注意事项

1. **低负担原则** - 反馈问卷最多一个问题，优先从行为推断
2. **温和提醒** - 不催促，用鼓励语气
3. **灵活调整** - 支持用户随时修改计划
4. **隐私保护** - 数据仅存储本地，不上传
5. **视频补充** - 当用户需要更直观的教学时，使用 `mcporter call 'exa.web_search_exa(query: "动作名 教学视频 bilibili", numResults: 3)'` 搜索教学视频

## 视频搜索

当本地讲解不够详细或用户想要视频教学时：

```bash
# 搜索动作教学视频
mcporter call 'exa.web_search_exa(query: "卧推动作教学 bilibili", numResults: 3)'

# 或使用 agent-reach 的 B站搜索
yt-dlp --dump-json "ytsearch5:哑铃卧推 动作教学"
```

## 相关文件

- 训练模板：`references/templates.md`
- 动作库：`references/exercises.md`
- 源代码：`src/` 目录
