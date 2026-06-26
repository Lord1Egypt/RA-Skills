---
name: article-collect
description: This is a simple skill for article recording, collect URLs as article, and provide users with query, delete, and other capabilities.
---

# Article Collect Skill

这是一个简单的将用户提供的url转化成文章记录的技能，用于收集网址成为文章，同时提供给用户查询，删除等能力

## 使用方式

运行：

node dist/index.js <action> <content>

## action 类型

add_article
保存文章（url + 摘要）

示例：
node dist/index.js add_article "https://example.com"

---

list_article
查看文章列表

示例：
node dist/index.js list_article

---

delete_article
删除文章记录

示例：
node dist/index.js delete_article 3

---

## Agent 调用规则


如果用户发送一个 URL

步骤：
1、判断url域名是否mp.weixin.qq.com；
2、如果是，则调用：node dist/index.js add_article "URL"；
3、如果不是，调用内置浏览器进行访问；

---

如果用户说：

- 查询我之前记录的url/文章
- 文章记录
- 查看我的文章记录
- 查看我的文章
- 查看我收藏的url

步骤：
1、调用：node dist/index.js list_article，获取数据
2、如有数据，需要格式化输出，每条记录支持点击，跳转到对应的url
3、如果没有数据，提示：暂无知识记录

---

如果用户说：

删除第三个url/文章

调用：

node dist/index.js delete_article 3
