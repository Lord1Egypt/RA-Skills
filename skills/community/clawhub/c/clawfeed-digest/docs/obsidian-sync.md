# Obsidian Sync (ClawHub Skill)

> 通过 ClawHub 安装的 Obsidian 同步技能

## 简介

Obsidian Sync 是一个 OpenClaw Skill，可以在 OpenClaw 中直接操作 Obsidian。

- **ClawHub**: https://clawhub.ai/AndyBold/obsidian-sync

---

## 安装

在 OpenClaw 中启用：

```json
{
  "skills": {
    "entries": {
      "obsidian-sync": {
        "enabled": true
      }
    }
  }
}
```

---

## 功能

通过 obsidian-cli 命令，可以：

- 搜索笔记
- 创建笔记
- 移动/重命名笔记
- 删除笔记

---

## obsidian-cli 使用

### 查找 active vault

```bash
# 查看默认 vault
obsidian-cli print-default

# 查看 vault 路径
obsidian-cli print-default --path-only
```

### 搜索笔记

```bash
# 按名称搜索
obsidian-cli search "query"

# 按内容搜索
obsidian-cli search-content "query"
```

### 创建笔记

```bash
obsidian-cli create "Folder/New note" --content "内容" --open
```

### 移动/重命名

```bash
obsidian-cli move "old/path/note" "new/path/note"
```

### 删除笔记

```bash
obsidian-cli delete "path/note"
```

---

## 配合 fast-note-sync-service 使用

推荐同时使用：

1. **fast-note-sync-service**: 自动双向同步文件
2. **obsidian-sync skill**: 在 OpenClaw 中直接操作 Obsidian

两者配合可以实现：
- 文件自动同步（fast-note-sync-service）
- 命令行操作（obsidian-sync）
