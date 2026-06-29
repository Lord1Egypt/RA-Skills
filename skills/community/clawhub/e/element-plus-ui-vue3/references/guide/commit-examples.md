---
name: "commit-examples"
description: "提交示例 -- Element Plus Vue3 桌面端组件。Invoke when user needs 提交示例 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/guide/commit-examples.html"
---

---

# 提交示例 [​](#提交示例)

## 为什么存在这个章节? [​](#为什么存在这个章节)

详情请参阅 [通用惯例](https://www.conventionalcommits.org/)。

一个好的 Git 提交信息能够使我们：

1.  了解贡献者试图做什么
2.  自动生成更改日志

### 写入提交消息的规则 [​](#写入提交消息的规则)

md

```
# (如果通过, 当前提交会实现...) <subject> (最多 72 个字符)

# |<---- 使用最多 72 个字符 ---->|

# 解释清楚为什么要作出此修改

# |<---- 尝试将每一行控制在 72 个字符以内 ---->|

# 提供链接、相关标签关键词、文章或其他资源信息

# 使用issue和合并请求的全链接地址替代部分链接

# 因为它们在GitLab之外显示为纯文本

# --- 提交结束 ---

# --------------------

# 不要忘记

# 将主题行大写(英文标题)

# 主题行使用命令式语气

# 不要在主题行末尾带有一段时间

# 主题行至少包含 3 个单词

# 主题和空行之间使用空行隔开

# 当提交的更改行数超过30行或至少3个文件需要发生修改时

# 应在提交的主体信息中说明修改的详情

# 不要使用 Emojis 表情符号

# 在主体信息中解释提交的是什么内容, 为什么提交, 如何实现

# 每行以 "-" 开头, 写入多行可描述信息要点

# 详见: https://chris.beams.io/posts/git-commit/

# --------------------
```

### 提交消息的模板 [​](#提交消息的模板)

下面是供参考的模板提交消息。

md

```
feat(components): [button] 我用按钮实现了某些功能

主体行和主体内容之间用空白行隔开(可以有预期时间)
通过一行或多行描述你的修改信息
每一行的首字母大写
且每一行的总字符数限制在72个以内最优, 超过了将不易于他人理解

- 你也可以通过添加子项列表符号来为内容布局
```

主题标题的格式是：

```
[type](scope 域): [messages]
```

关于**type** 和 **scope**属性允许的值可以在 [commitlint.config.js](https://github.com/element-plus/element-plus/blob/c2ee36a7fc72b17742d43ecdff4e2912c416141d/commitlint.config.js#L57) 文件内查看

### 相关链接 [​](#相关链接)

[保持 git 提交历史简洁](https://about.gitlab.com/blog/2018/06/07/keeping-git-commit-history-clean/)

[开发常见问题](https://element-plus.org/zh-CN/guide/dev-faq)

[翻译](https://element-plus.org/zh-CN/guide/translation)


