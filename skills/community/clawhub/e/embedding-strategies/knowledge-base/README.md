# 知识库总索引

> 最后更新：2026-03-07 01:40  
> 创建者：阿福（AI 助理）

---

## 📚 知识库结构

knowledge-base/
├── README.md (本文件 - 总索引)
├── projects/              # 项目知识库
├── doubao-sessions/       # 豆包原始记录
└── worklog.txt            # 工作流水账（根目录）

---

## 🎯 触发词指南

| 触发词 | 功能 | 输出 |
|--------|------|------|
| **豆包** | 保存豆包聊天记录 | doubao-sessions/日期.md |
| **提取豆包** | 提取知识 + 专家点评 | 项目知识库 + HTML |
| **同步项目** | 更新项目进度 | 项目知识库更新 |
| **专家点评** | 生成专家视角分析 | HTML 报告 |
| **生成周报** | 生成正式周报 | workreport.txt |

---

## 📁 项目列表

### 感知与行动中心
- 项目卡片：knowledge-base/projects/感知与行动中心/
- 专家点评：knowledge-base/projects/感知与行动中心/专家点评/
- 工作记录：knowledge-base/projects/感知与行动中心/工作记录/

### 产能监控系统
- 项目卡片：knowledge-base/projects/产能监控系统/
- 专家点评：knowledge-base/projects/产能监控系统/专家点评/
- 工作记录：knowledge-base/projects/产能监控系统/工作记录/

---

## 📝 豆包会话

位置：knowledge-base/doubao-sessions/

命名规则：YYYY-MM-DD-主题.md

---

## 🔍 快速搜索

搜索项目内容：
Select-String -Path "knowledge-base\projects\*.md" -Pattern "关键词" -Recurse

搜索豆包会话：
Select-String -Path "knowledge-base\doubao-sessions\*.md" -Pattern "关键词" -Recurse

---

## 📊 数据流

用户输入 → 识别触发词 → 调用 Skill → 存储知识库 → 应用（周报/点评）

---

_知识库由阿福维护 | 渐进式优化 | 持续迭代_
