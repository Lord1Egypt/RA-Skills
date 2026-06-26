---
name: bilibit
version: 0.1.8
description: B 站视频下载工具。支持哔哩哔哩视频下载、弹幕下载。用户说"B 站下载"、"哔哩哔哩"、"bilibili"时使用。无需 API Key。纯下载工具，不支持搜索。
license: MIT
homepage: https://github.com/AoturLab/bilibit
metadata:
  openclaw:
    emoji: 🎬
    requires:
      bins: [bbdown, ffmpeg]
aliases: [B 站下载，哔哩哔哩下载，bilibili 下载，B 站视频，哔哩哔哩，bilibili,B 站，b 站，视频下载，弹幕下载]
---

# 🎬 bilibit - B 站视频下载专家

极简 B 站视频下载工具。粘贴 URL，一键下载视频和弹幕。

---

## 📦 快速安装

```bash
# clawhub
clawhub install bilibit

# npm
npm install -g bilibit
```

---

## 🚀 使用示例

### 下载视频
```bash
bilibit https://b23.tv/BV1xx
```

### 下载带弹幕
```bash
bilibit https://b23.tv/BV1xx --danmaku
```

---

## 💬 AI 交互规范（重要！）

### 触发场景

**当用户说这些话时，使用 bilibit**：
- "下载这个 B 站视频" + URL
- "B 站下载"
- "哔哩哔哩视频"
- "下载弹幕"

**不支持的场景**：
- ❌ "搜索 B 站视频" - bilibit 不支持搜索，需要用户提供 URL
- ❌ "找某个 UP 主的视频" - 不支持搜索，需用户先在 B 站找到 URL

### 输出格式规范

**输出格式规范**：

```
📺 下载完成！已保存到：xxx

📌 回复序号查看历史
```

**禁止行为**：
- ❌ 不要转成表格格式
- ❌ 不要重新排序
- ❌ 不要用 `[]()` 包裹 URL

**必须保留**：
- ✅ 原始输出格式
- ✅ 下载完成提示

---

## 📋 完整命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `bilibit <url>` | 下载视频 | `bilibit https://b23.tv/BV1xx` |
| `bilibit <url> --danmaku` | 下载 + 弹幕 | `bilibit ... --danmaku` |
| `bilibit <url> --quality 4K` | 指定画质 | `bilibit ... --quality 4K` |
| `bilibit history` | 下载历史 | `bilibit history` |

---

## ⚠️ 注意事项

- 仅限个人学习使用
- 大会员画质需要 Cookie
- 弹幕保存为 XML 格式

---

## 🔗 相关链接

- GitHub: https://github.com/AoturLab/bilibit
- 问题反馈：https://github.com/AoturLab/bilibit/issues
