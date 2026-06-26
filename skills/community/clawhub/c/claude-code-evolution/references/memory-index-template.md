# MEMORY.md — 记忆索引（基于Claude Code架构）

**注意**: 这是基于Claude Code记忆系统生成的索引文件，最多200行/25KB。实际记忆内容在`memory/`目录下的具体文件中。

## 索引使用说明
1. 每条索引格式：`- [名称](文件.md) -- 一行描述`
2. 单行不超过150字符（Claude Code限制）
3. 按类型分组，最新记忆在前
4. 索引容量：200行/25KB，超限自动截断

## user类型记忆（用户画像）

- [用户画像](memory/user-profile.md) -- 用户的角色、目标、知识背景、工作偏好和习惯

## feedback类型记忆（反馈指导）

- [反馈与错误记录](memory/feedback-logs.md) -- 系统错误、用户反馈、成功经验和持续改进记录

## project类型记忆（项目状态）

- [项目状态总览](memory/project-states.md) -- 当前所有活跃项目的状态、进度、依赖关系和资源配置

## reference类型记忆（外部引用）

- [系统引用指针](memory/reference-pointers.md) -- 核心配置文件、关键数据文件、运行进程、技能位置和故障排除引用

## 最近7日记忆（按日期）

- [YYYY-MM-DD](memory/YYYY-MM-DD.md) -- [每日活动摘要]

## 容量状态
- 当前行数：X行（Y%使用率）
- 当前大小：约Z KB（W%使用率）
- 最后更新：YYYY-MM-DD HH:MM
- 索引版本：v1.1（Claude Code兼容格式）
- 新增条目：[最新记忆条目]

## 维护提示
1. 新增记忆时，先确定类型（user/feedback/project/reference）
2. 为记忆文件添加Frontmatter元数据（name, description, type）
3. 更新此索引文件，保持格式一致
4. 定期检查容量，接近限制时优先保留高价值记忆

## 校验状态
- [ ] 所有核心记忆文件已添加Frontmatter
- [ ] 符合闭合四类型系统（user, feedback, project, reference）
- [ ] 索引格式符合Claude Code规范
- [ ] 容量控制有效（当前远低于限制）

---
*索引生成时间：YYYY-MM-DD HH:MM CST*
*基于Claude Code记忆系统架构 v1.1*
*包含阶段一至五的完整记忆系统实现*