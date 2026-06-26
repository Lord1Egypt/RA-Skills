---
name: bilibili-summary
description: 通过内置脚本获取B站视频信息并总结
user-invocable: true
---

# 功能

输入 B站视频链接，返回视频信息并总结

---

# 执行流程

1. 接收用户输入（URL 或 BV号）
2. 调用内部脚本：
   scripts/fetch.js
3. 获取 JSON 数据
4. 生成总结

---

# 输出格式

- 标题：
- UP主：
- 播放量：
- 点赞数：
- 内容总结：

---

# 约束

- 必须调用内部 scripts
- 不允许使用 web_fetch
- 不允许使用 browser