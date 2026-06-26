---
name: CSDN 文章发布技能
description: CSDN 文章发布技能
---

# CSDN 文章发布技能

## 描述

自动化发布文章到 CSDN 博客平台。支持打开编辑器、填写标题和内容、发布文章。

## 触发条件

当用户要求：
- 发布文章到 CSDN
- 在 CSDN 写博客
- 发布技术文章到 CSDN 平台

## 发布流程

### 1. 打开 CSDN 编辑器

```
browser.open(
  url="https://mp.csdn.net/mp_blog/creation/editor?spm=1010.2135.3001.4503",
  profile="openclaw"
)
```

### 2. 检查登录状态

使用 `browser.snapshot` 检查页面状态：
- 如果看到登录框/验证码 → 停止任务，告知用户需要先登录
- 如果看到编辑器界面（标题输入框、工具栏）→ 继续

### 3. 填写文章标题

找到标题输入框（aria ref 通常为 `e41`），使用 `browser.act` 填写：

```
browser.act(
  kind="type",
  ref="e41",
  text="文章标题"
)
```

### 4. 填写文章内容

点击编辑器内容区域（iframe 内的 `f1e1`），然后输入 Markdown 格式的文章内容：

```
browser.act(
  kind="click",
  ref="f1e1"
)

browser.act(
  kind="type",
  ref="f1e1",
  text="完整的 Markdown 文章内容"
)
```

### 5. 点击发布按钮

找到发布按钮（aria ref 通常为 `e322`），点击发布：

```
browser.act(
  kind="click",
  ref="e322"
)
```

### 6. 确认发布结果

再次使用 `browser.snapshot` 检查发布结果：
- 如果看到"发布成功！正在审核中" → 成功
- 提取文章链接告知用户

## 注意事项

1. **登录检查**：必须先确认用户已登录 CSDN，否则无法发布
2. **内容格式**：支持 Markdown 格式，包括代码块、标题、列表等
3. **标题要求**：5-100 个字符
4. **审核机制**：发布后需要审核，审核通过后才能公开可见
5. **浏览器配置**：使用 `profile="openclaw"` 确保浏览器可用

## 文章链接提取

发布成功后，从页面中提取文章链接（通常在 `查看文章` 按钮的 href 中），格式类似：
```
https://blog.csdn.net/{username}/article/details/{article_id}
```

## 错误处理

| 情况 | 处理方式 |
|------|---------|
| 未登录 | 停止任务，提示用户先登录 CSDN |
| 标题太短 | 提示用户标题至少 5 个字符 |
| 内容为空 | 提示用户需要填写文章内容 |
| 网络错误 | 重试或提示用户检查网络 |

## 示例调用

用户：帮我发布一篇 Python 教程到 CSDN

助手：
1. 打开编辑器页面
2. 检查登录状态 ✓
3. 填写标题"Python 入门教程"
4. 填写完整的教程内容
5. 点击发布
6. 返回文章链接
