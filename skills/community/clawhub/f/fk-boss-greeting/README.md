# 🦞 小龙虾 Boss 直聘自动打招呼工具

> 2026 年，工作不好找，程序员更不好找。  
> 手动刷 Boss 太慢了？让小龙虾帮你。

这是一个基于 [kabi-boss-cli](https://github.com/jackwener/boss-cli) 封装的 **Boss 直聘自动打招呼 Skill**，专为找工作的程序员打造。

它能帮你自动搜索职位、过滤掉不想去的公司、排除不相关的岗位，然后逐个跟 HR 打招呼——让你把时间花在真正重要的面试准备上。

---

## ✨ 功能

- 🔍 **自动搜索**：Java架构师、技术经理、研发经理、软件工程师等 10 个关键词，覆盖上海/北京/苏州/杭州/无锡
- 🚫 **智能过滤**：
  - 公司黑名单：阿里、百度、腾讯、字节、京东、拼多多、滴滴、快手、小米、华为、蚂蚁...
  - 职位黑名单：算法、AI、大模型、测试、产品经理、初级/实习...
  - 只保留 Java 相关的技术岗
- 🐢 **安全第一**：逐个排队打招呼，间隔 1 秒，每轮最多 30 个，避免被风控封号
- 📝 **去重记录**：不会重复打扰同一个 HR
- ⏰ **定时任务**：支持周一/周三上午 9 点自动运行

---

## 📦 安装

### 1. 安装 kabi-boss-cli

```bash
pip install kabi-boss-cli
# 或通过 uv
uv tool install kabi-boss-cli
```

### 2. 登录 Boss 直聘

先在 **Chrome 浏览器**打开 [zhipin.com](https://www.zhipin.com) 并登录，然后：

```bash
boss login --cookie-source chrome
```

> 💡 不需要扫码，直接从 Chrome 读取登录态即可。

### 3. 导入 Skill

在 OpenClaw（或支持 Skill 的 AI 助手）中导入 `fk-boss-greeting.skill`。

---

## 🚀 使用

### 手动打招呼

告诉 AI 助手：

> "帮我找匹配的职位打招呼"  
> "搜索上海 Java 架构师职位并打招呼"

AI 会自动：登录 → 搜索 → 过滤 → 逐个打招呼。

### 定时任务

> "设置每周一、周三上午 9 点自动打招呼"

---

## ⚙️ 规则配置

编辑 `references/filter-rules.json` 可自定义：

```json
{
  "company_blacklist": ["阿里", "百度", "腾讯", ...],
  "job_blacklist": ["算法", "测试", "产品经理", ...],
  "search_keywords": ["Java架构师", "技术经理", ...],
  "city_priority": ["上海", "北京", "苏州", "杭州", "无锡"],
  "max_greets_per_day": 30
}
```

---

## ⚠️ 安全须知

1. **控制频率**：每轮最多 30 个，间隔 1 秒，别贪多
2. **不要并行**：逐个打招呼，别同时发
3. **账号风险**：高频操作可能触发 Boss 直聘风控（code=32/36），如被封需在 APP 手动解封
4. **合理使用**：这工具是帮你省时间的，不是滥用平台的手段

---

## 🛠 技术栈

- [kabi-boss-cli](https://github.com/jackwener/boss-cli) - Boss 直聘命令行工具
- Python 3 - 搜索过滤脚本
- OpenClaw Skill - AI Agent 封装

---

## 📄 License

Apache-2.0

---

> 🦞 小龙虾出品，祝早日上岸！  
> 如果有帮助，给个 ⭐ Star 呗～
