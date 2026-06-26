# 🎬 bilibit - B 站视频下载工具

> 简单易用的 B 站视频下载工具。复制 URL，一键下载！

[![npm version](https://img.shields.io/npm/v/bilibit.svg)](https://www.npmjs.com/package/bilibit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[🇺🇸 English Documentation](README.md)**

---

## ✨ 特性

- 🎯 **URL 下载** - 粘贴 URL，下载视频
- 🎬 **弹幕支持** - 下载带弹幕
- 🚀 **简单快速** - 一条命令搞定
- 📦 **自动安装** - BBDown 自动安装
- 📋 **历史记录** - 查看下载历史

---

## 📦 安装

```bash
npm install -g bilibit
```

**BBDown 会自动安装！**

---

## 🚀 快速开始

### 下载视频

```bash
# 基础下载
bilibit https://b23.tv/BV1xx

# 指定画质
bilibit https://b23.tv/BV1xx --quality 4K

# 下载弹幕
bilibit https://b23.tv/BV1xx --danmaku
```

### 查看历史

```bash
bilibit history
bilibit history --limit 20
```

---

## 📋 命令参考

| 命令 | 说明 |
|------|------|
| `bilibit <url>` | 下载视频 |
| `bilibit history` | 查看历史 |
| `bilibit --help` | 帮助信息 |
| `bilibit --version` | 版本号 |

### 下载选项

| 参数 | 简写 | 说明 |
|------|------|------|
| `--quality` | `-q` | 视频画质（4K, 1080P 等） |
| `--danmaku` | `-d` | 下载弹幕 |
| `--output` | `-o` | 输出目录 |

---

## 💡 如何获取 URL

1. 浏览器打开 B 站
2. 找到想要的视频
3. 复制地址栏 URL
4. 运行 `bilibit <URL>`

**URL 示例**: `https://www.bilibili.com/video/BV1yVwXzGEbL`

---

## ⚠️ 注意事项

- **版权**: 仅限个人学习使用
- **BBDown**: 安装 bilibit 时自动安装
- **大会员**: 1080P+ 需要 Cookie

---

## 🔗 相关链接

- **GitHub**: https://github.com/AoturLab/bilibit
- **npm**: https://www.npmjs.com/package/bilibit
- **问题反馈**: https://github.com/AoturLab/bilibit/issues

---

## 📄 许可证

MIT License
