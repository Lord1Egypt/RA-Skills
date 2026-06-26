# ClawHub技能售卖工作流

> 版本：v2.0
> 创建日期：2026-04-21
> 更新日期：2026-04-22
> 适用场景：整理、上传、销售AI技能获取收益
> 账号：155143783@qq.com / Ft656618（需GitHub账号登录）

---

## 一、ClawHub平台概述

### 平台信息
| 项目 | 说明 |
|------|------|
| **官网** | clawhub.ai |
| **导入页面** | https://clawhub.ai/import |
| **登录方式** | GitHub账号登录（必须） |
| **热门技能** | 工具集成、自动化、内容生成类 |

### 上传方式
| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **网页上传** | 直接拖拽文件夹到 https://clawhub.ai/import | 新手首选，简单快捷 |
| **CLI上传** | 使用 `clawhub publish` 命令 | 自动化、批量发布 |

### 热门技能参考
| 技能名称 | 下载量 | 核心功能 |
|----------|--------|----------|
| self-improving-agent | 390k | 持续自我改进 |
| 全网新闻聚合助手 | 12.9k | 新闻聚合、早报生成 |
| AI文本去味器 | 8.5k | 去除AI痕迹 |
| 股票个股分析 | 6.7k | 技术分析 |

---

## 二、触发词清单

| 触发词 | 功能 | 输出 |
|--------|------|------|
| 上传技能到ClawHub | 上传新技能 | 上传结果 |
| ClawHub上架 | 发布技能 | 发布确认 |
| 发布技能 | 开始发布 | 发布状态 |
| 技能变现 | 查询收益 | 收益统计 |
| 上传新技能 | 上传技能 | 上传结果 |
| 打包ClawHub技能 | 准备技能包 | 技能文件 |
| ClawHub审核 | 审核技能内容 | 审核报告 |

---

## 三、工作流执行步骤

### 步骤1：技能准备与审核

```
触发词：准备ClawHub技能

执行动作：
1. 确定技能定位和功能
2. 审核技能内容（见审核标准）
3. 编写/完善SKILL.md主文件
4. 准备必要的参考文档（references/）
5. 准备脚本文件（scripts/）
6. 编写README和示例
```

### 审核标准

#### 内容审核
- [ ] 无敏感政治内容
- [ ] 无色情低俗内容
- [ ] 无暴力血腥内容
- [ ] 无虚假诈骗信息
- [ ] 无侵犯版权内容
- [ ] 无恶意代码/病毒

#### 格式审核
- [ ] SKILL.md 包含 YAML frontmatter (name + description)
- [ ] Slug 符合规范（小写字母+短横线）
- [ ] 描述简洁明了（50-200字符）
- [ ] 纯文本文件，无二进制文件
- [ ] 无 .git、.DS_Store、LICENSE 等非必要文件

#### 质量审核
- [ ] 功能描述清晰
- [ ] 使用方法完整
- [ ] 示例可操作
- [ ] 无明显错误

### 步骤2：技能打包

```
触发词：打包ClawHub技能

执行动作：
1. 创建技能目录结构
2. 验证SKILL.md格式
3. 清理非必要文件
4. 验证技能可用性
5. 打包为ZIP或保持目录结构
```

### 步骤3：上传发布（CLI方式，推荐）

```
触发词：发布到ClawHub

前置条件：
- GitHub账号注册满7天
- 已安装clawhub CLI

执行动作：
1. 安装CLI（首次）：
   npm i -g clawhub

2. 登录ClawHub（自动登录）：
   # 打开授权页面
   agent-browser open https://clawhub.ai/cli/auth && agent-browser tab 0
   agent-browser snapshot -i
   
   # 自动点击GitHub登录
   agent-browser click "GitHub"  # 或对应的登录按钮
   
   # 如果未登录GitHub，自动填写凭据
   # 邮箱: 155143783@qq.com
   # 密码: Ft656618
   # (从 ../主对话/SECRET.md 读取)
   
   # 如需授权确认
   agent-browser click "Authorize"
   
   # 获取token
   agent-browser get text body  # 提取显示的token
   
   # 保存token
   clawhub login --token <token>

3. 发布技能：
   clawhub publish ./skills/技能目录 \
     --slug 技能slug \
     --name "显示名称" \
     --version 1.0.0 \
     --tags latest \
     --changelog "初始版本"

4. 批量发布所有技能：
   clawhub sync --all
```

### GitHub自动登录
使用 **auto-login-credentials** 技能自动填写GitHub凭据：
- 邮箱: 155143783@qq.com
- 密码: Ft656618
- 存储: ../主对话/SECRET.md

### 步骤3备选：网页上传（手动）

```
触发词：网页上传ClawHub

执行动作（需要手动操作）：
1. 登录GitHub账号（如未登录）
2. 访问 https://clawhub.ai/import
3. 填写技能信息
4. 拖拽上传技能文件夹
5. 点击 "Publish skill"
```

### 步骤4：运营维护

```
触发词：ClawHub技能运营

执行动作：
1. 监控下载量和用户反馈
2. 根据反馈迭代更新
3. 回复用户问题
4. 优化技能描述和定价
```

---

## 四、技能结构模板

```
my-skill/
├── SKILL.md          # 必填：技能主文件（核心）
├── README.md         # 可选：使用说明
├── references/       # 可选：参考文档
│   ├── guide.md
│   └── examples.md
└── scripts/          # 可选：可执行脚本
    └── main.py
```

### SKILL.md 格式要求

```yaml
---
name: skill-slug           # 必填：技能标识（小写+短横线）
description: 简短描述     # 必填：50-200字符
---

# 技能名称

## 概述
[技能功能说明]

## 使用场景
[何时使用此技能]

## 核心功能
[主要功能点]

## 使用方法
[具体使用方法]

## 示例
[使用示例]

## 更新日志
### v1.0.0
- 初始版本
```

---

## 五、可上传技能清单

### 已有技能（可直接上传）

| 技能名称 | 目录 | 状态 | 建议Slug |
|----------|------|------|----------|
| 中文内容去味器 | skills/chinese-content-humanizer/ | ✅ 就绪 | chinese-content-humanizer |
| BotStreet任务代理 | skills/botstreet-task-agent/ | 🔄 待完善 | botstreet-task-agent |
| 提示词变现 | skills/prompt-monetization/ | 🔄 待完善 | prompt-monetization-workflow |
| 视频变现 | skills/video-monetization/ | 🔄 待完善 | video-monetization-workflow |
| 小红书带货 | skills/xhs-affiliate/ | 🔄 待完善 | xhs-affiliate-workflow |

### 待开发技能

| 技能名称 | 优先级 | 预计开发时间 |
|----------|--------|--------------|
| 全网新闻聚合助手 | 🔴 高 | 2小时 |
| AI Agent变现指南 | 🔴 高 | 2小时 |
| 股票技术分析套件 | 🟡 中 | 3小时 |
| 电商运营工作流 | 🟡 中 | 3小时 |

---

## 六、上传记录模板

```markdown
# ClawHub上传记录

| 日期 | 技能名称 | Slug | 版本 | 状态 | 链接 |
|------|----------|------|------|------|------|
| 2026-04-22 | 中文内容去味器 | chinese-content-humanizer | 1.0.0 | ✅ 已发布 | - |
| - | - | - | - | - | - |
```

---

## 七、常见问题

### Q1: Slug格式错误
**问题**: "Slug must be lowercase"
**解决**: 只使用小写字母和短横线，如 `my-skill-name`

### Q2: 非文本文件错误
**问题**: "Remove non-text files"
**解决**: 删除 .git、.DS_Store、LICENSE 等文件

### Q3: SKILL.md未找到
**问题**: "SKILL.md not found"
**解决**: 确保 SKILL.md 在文件夹根目录

### Q4: GitHub登录问题
**问题**: 需要GitHub账号
**解决**: 
1. 访问 github.com 注册账号
2. 确保账号创建超过1周（旧账号才能发布）

---

## 八、定价策略参考

| 定价 | 适用场景 | 收益估算 |
|------|----------|----------|
| 免费 | 引流、积累下载量 | 高下载量，低收益 |
| $1-5 | 基础工具类 | 中下载量，中收益 |
| $5-20 | 专业工具类 | 低下载量，高收益 |
| $20+ | 企业级解决方案 | 极低下载量，定制收益 |

---

## 九、下一步行动

1. [ ] 完善 chinese-content-humanizer 技能的 references/
2. [ ] 测试上传 chinese-content-humanizer 到 ClawHub
3. [ ] 验证上传成功
4. [ ] 完善并上传其他技能
5. [ ] 监控下载量和收益

