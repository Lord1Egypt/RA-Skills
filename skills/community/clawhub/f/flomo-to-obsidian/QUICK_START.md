# ⚡ 快速开始指南

5 分钟上手 Flomo 同步工具！

---

## 🎯 方式1：在 OpenClaw 对话中使用（最简单）

### 说这句话：

```
"帮我设置 flomo 自动同步"
```

### 然后回答几个问题：

1. **Flomo 邮箱**：your-email@example.com
2. **Flomo 密码**：your-password
3. **Obsidian 路径**：/Users/username/mynote/flomo

### 完成！

AI 会自动：
- ✅ 测试同步
- ✅ 创建定时任务
- ✅ 设置自动运行

---

## 🎯 方式2：命令行使用（技术用户）

### 一键设置：

```bash
cd <skill-directory>

./setup.sh
```

### 手动同步：

```bash
./sync.sh
```

---

## 📋 对话示例

### 首次使用

**你**：设置 flomo 自动同步

**AI**：好的！请提供：
- Flomo 邮箱：
- Flomo 密码：

**你**：[提供账号]

**AI**：配置完成！首次同步...

✅ 同步成功！新增 120 条笔记

是否创建定时任务？
1. 每天 22:00
2. 每天 23:00
3. 每 6 小时

**你**：1

**AI**：✅ 已创建！从明天开始自动同步

---

### 日常使用

**你**：立即同步 flomo

**AI**：✅ 同步完成！新增 8 条笔记

---

## 🔧 关键配置

### 标签前缀

建议使用 `flomo/`，避免标签冲突：

```
flomo 标签: #工作
Obsidian 标签: #flomo/工作
```

### 组织模式

**by-date（推荐）**：按日期创建文件

```
2024-03-11.md  ← 当天所有笔记
2024-03-12.md
```

---

## 🆘 故障排查

### 同步失败

**你**：flomo 同步失败了

**AI**：我来帮你排查...

[查看日志 → 分析错误 → 提供方案]

### 查看日志

```bash
tail -f auto_sync.log
```

### 可视化调试

```bash
./sync.sh --no-headless
```

---

## 📚 完整文档

- **[README.md](./README.md)** - 项目总览
- **[USAGE_IN_AGENT.md](./USAGE_IN_AGENT.md)** - 对话使用详解
- **[AUTO_SYNC.md](./AUTO_SYNC.md)** - 技术文档
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - 环境变量指南

---

## 🎉 立即开始

在 OpenClaw 中说：

```
"帮我设置 flomo 自动同步"
```

就这么简单！
