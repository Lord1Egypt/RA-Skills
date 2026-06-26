---
name: awesome-obsidian
description: Obsidian 个人知识管理工作流。基于 PARA 方法 + 自动化工具链。用于：(1) 整理 Obsidian 库结构和命名规范 (2) Git 同步管理 (3) 每日时间线记录 (4) 插入手绘风格图表 (5) 从小艺帮记收藏整理笔记。触发词：Obsidian、笔记整理、库整理、daily log、时间线、手绘图表、PARA、知识管理。
---

# Awesome Obsidian - 个人知识管理工作流

基于 PARA 方法 + 自动化工具链的 Obsidian 工作流。

## 文件夹结构（PARA）

```
obsidian-vault/
├── inbox/              # 快速收集，临时笔记
├── projects/           # 活跃项目（有明确开始/结束）
├── areas/              # 持续关注的领域
├── resources/          # 长期参考笔记
├── archive/            # 归档（已完成项目）
├── journal/            # 日记（YYYY-MM-DD.md）
└── assets/             # 资源文件
```

## 工具链

| Skill | 用途 |
|-------|------|
| obsidian-git-vault | Git 同步管理 |
| obsidian-organizer | 库整理与命名规范 |
| obsidian-daily-log | 每日时间线记录 |
| excalidraw-handdraw | 手绘风格图表 |

## 日常工作流

### 1. 快速收集 → inbox/

新想法、临时笔记先丢进 `inbox/`，定期整理。

### 2. 每日记录 → journal/

使用 `obsidian-daily-log` 记录时间线：

```markdown
## Timeline

- 09:00 — 开始工作
- 10:30 — 完成文档整理
- 14:00 — 会议讨论
```

### 3. 定期整理

- **每周**：整理 inbox，移动到正确位置
- **每月**：归档完成的项目

### 4. Git 同步

```bash
git pull
git add . && git commit -m "update: 笔记更新"
git push origin main
```

## 命名规范

### 中文笔记（优先）
- `中文标题.md`
- `2026-04-21-会议纪要.md`

### 英文笔记
- `kebab-case.md`
- `YYYY-MM-DD.md`

### 避免
- 特殊符号、emoji 表情
- `Final`、`v2`、`new` 等无意义后缀

## 美化技巧

### 插入手绘图表

使用 `excalidraw-handdraw` 在笔记中插入手绘风格图表。

### Obsidian 主题推荐

- **Minimal** - 极简干净
- **Things** - 温暖舒适
- **AnuPpuccin** - 多彩可爱

安装：设置 → 外观 → 主题 → 浏览

## 自动化脚本

### 审计命名

```bash
python scripts/obsidian_audit.py <vault-path>
```

### 应用修复

```bash
python scripts/obsidian_audit.py <vault-path> --apply
```

## 最佳实践

1. 一个笔记一个主题
2. 及时整理 inbox
3. 用 `[[]]` 连接相关笔记
4. 定期回顾笔记
5. Git 提交 + 远程同步

## ⚠️ 整理规则

**禁止修改人物原话**：
- 整理笔记时，**绝不修改、简化或意译人物的发言原话**
- 引用、演讲、声明、采访内容必须保持原文
- 包括标点符号、语气词、停顿等细节
- 如需概括，应在引用块之外单独撰写摘要

## 详细参考

- [PARA方法详解](references/para-method.md)
- [工具链配置](references/toolchain.md)
- [模板库](references/templates.md)

---

## 📱 手机端查看

### 方案：出境易 + Obsidian Git 插件

在鸿蒙手机上使用 **出境易** 安装 Obsidian，配合 Git 插件同步笔记。

### 配置步骤

#### 1. 安装应用
- 在应用市场下载 **出境易**
- 通过出境易安装 **Obsidian**

#### 2. 安装 Git 插件
- 打开 Obsidian → 设置 → 第三方插件
- 浏览社区插件，搜索 **「Git」**
- 安装并启用

#### 3. 克隆仓库
1. 打开命令面板（左下角菜单）
2. 搜索 **「Git: Clone an existing remote repo」**
3. 输入你的仓库地址：
   ```
   https://oauth2:YOUR_TOKEN@your-git-host.com/username/repo.git
   ```
   > 将 YOUR_TOKEN 替换为你的访问令牌，仓库地址替换为你的实际地址
4. 选择保存目录（如 `Obsidian`）
5. 克隆深度留空（完整克隆）

#### 4. 配置认证
在 Git 插件设置中：
- **Username**：GitCode 用户名
- **Password/Token**：访问令牌

#### 5. 日常同步
- **拉取**：命令面板 → `Git: Pull`
- **推送**：命令面板 → `Git: Commit and sync`

### 注意事项
- 克隆时会删除本地 `.obsidian` 配置
- 建议在 WiFi 环境下同步
- 如遇冲突，手动解决后再提交
