---
name: essential-skills-package
description: 核心技能包 - 包含科研、开发、自动化等常用功能
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "requires": { "anyBins": ["python", "node", "git"] },
      },
  }
---

# 核心技能包

专为高效工作设计的核心技能集合，覆盖科研、开发、自动化等场景。

## 📚 科研工具
- 文献搜索与分析
- 数据提取与处理
- 学术内容总结

## 💻 开发工具  
- 代码编写与审查
- 项目结构创建
- 自动化脚本开发

## 🔄 自动化工具
- 定时任务管理
- 文件批量处理
- 工作流自动化

## 使用方法

### 科研文献搜索
```bash
# 使用 web_search + 模型分析实现文献调研
web_search query:"your research topic" count:10
# 模型自动进行内容分析和分类
```

### 代码开发
```bash
# 使用 ACP 会话进行代码开发
sessions_spawn runtime:"acp" task:"Create project for [your topic]"
```

### 自动化任务
```bash
# 设置定时提醒
cron action:"add" job:"{...定时任务配置...}"
```

## 核心优势

1. **无需额外安装** - 使用现有工具和模型能力
2. **即开即用** - 无需等待技能下载
3. **高度定制** - 可根据需求灵活调整
4. **持续更新** - 随时添加新功能

## 立即开始

选择你的任务类型，我为你提供最佳解决方案！