# code-project-analyzer 📊
OpenClaw 代码项目自动分析技能，一键生成项目介绍文档
## 功能介绍
自动扫描任意本地代码目录，智能识别项目信息，自动生成标准化的项目介绍文档，包含三个核心部分：
1. **基础功能**：识别技术栈、目录结构、核心入口、依赖信息
2. **应用场景**：分析项目适用场景、可复用价值
3. **实现原理**：梳理架构设计、模块划分、核心实现逻辑
## 支持的项目类型
- ✅ 前端项目（JS/TS/Vue/React/Next/Nuxt等）
- ✅ 后端项目（Node.js/Python/Go/Java/Rust等）
- ✅ 工具类项目、脚本项目、CLI工具
- ✅ OpenClaw Skill 项目
## 触发方式
在OpenClaw对话中输入以下关键词即可触发：
```
分析代码目录 <本地项目路径>
生成<路径>的项目介绍文档
梳理这个项目的架构
这个项目是干啥的？
```
## 使用示例
```
分析 C:\Users\wwl\.openclaw\workspace\skills\tech-radar
生成项目介绍文档到 C:\Users\wwl\Desktop\tech-radar介绍.md
```
## 输出示例
```markdown
# tech-radar 项目介绍
## 一、基础功能
- 自动追踪国内外前沿技术动态，生成每日/每周技术快讯
- 技术栈：Node.js
- 目录结构说明：
  * `fetchers`: 各技术平台爬虫模块
  * `templates`: 报告模板目录
## 二、应用场景
- 适合需要自动收集技术资讯的开发者
- 可作为技术周报/快讯自动生成工具
- 可二次开发自定义信息源、输出格式
## 三、实现原理
- 模块化爬虫设计，新增信息源只需添加对应fetcher
- 模板化输出，支持自定义报告格式
```
## 依赖要求
- Node.js 18+
- OpenClaw 环境本地文件读取权限
## 安装方法
1. 克隆仓库到 OpenClaw skills 目录
```bash
cd C:\Users\wwl\.openclaw\workspace\skills
git clone https://gitcode.com/easycurd/code-project-analyzer.git
```
2. 重启 OpenClaw 即可识别使用
## 开发者
吴伟林（吴工）| AI工程师
