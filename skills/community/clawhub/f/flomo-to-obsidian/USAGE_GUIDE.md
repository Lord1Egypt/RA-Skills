# Flomo to Obsidian 使用指南

## 🎯 快速开始

### 第一步：从 Flomo 导出数据

1. 访问 [Flomo 网页版](https://flomoapp.com/)
2. 登录你的账号
3. 点击右上角头像 → **设置**
4. 进入 **账号详情**
5. 滚动到页面底部，找到 **导出数据** 按钮
6. 点击导出，等待 Flomo 生成导出文件
7. 下载 `index.html` 文件到本地

> ⚠️ **注意**：Flomo 限制每 7 天只能导出一次

### 第二步：安装依赖

在终端中运行：

```bash
pip install beautifulsoup4 markdownify
```

或者使用 requirements.txt：

```bash
cd flomo-to-obsidian
pip install -r scripts/requirements.txt
```

### 第三步：转换数据

#### 基础转换（推荐新手）

```bash
python scripts/convert.py \
  --input ~/Downloads/index.html \
  --output ~/Obsidian/Flomo \
  --mode by-date
```

这将把所有笔记按日期组织，每天一个文件。

#### 查看结果

打开 Obsidian，导航到输出目录，你会看到：

```
Flomo/
├── 2024-01-15.md
├── 2024-01-16.md
├── 2024-01-17.md
└── ...
```

## 📊 三种组织模式对比

### 模式 1: By-Date（按日期）

**适合场景**：
- 日记型笔记
- 想要按时间线查看思考
- 笔记数量较多

**优点**：
- 按时间线组织，便于回顾
- 文件数量可控
- 符合日记习惯

**缺点**：
- 单个文件可能较长
- 不便于单独笔记的管理

**使用方法**：
```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --mode by-date
```

**输出示例**：
```
2024-03-15.md (包含当天所有笔记)
├── 09:23 - 工作计划
├── 14:30 - 学习笔记
└── 20:15 - 读书笔记
```

---

### 模式 2: Individual（单独文件）

**适合场景**：
- 每条笔记都是独立的想法
- 需要频繁引用单条笔记
- 喜欢原子化笔记

**优点**：
- 每条笔记独立管理
- 便于建立笔记间的链接
- 符合 Zettelkasten 方法

**缺点**：
- 文件数量多
- 不便于按时间线浏览

**使用方法**：
```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --mode individual \
  --preserve-time
```

**输出示例**：
```
flomo-2024-03-15-092315.md
flomo-2024-03-15-143022.md
flomo-2024-03-15-201533.md
```

---

### 模式 3: Single（单文件）

**适合场景**：
- 只想归档 Flomo 笔记
- 不需要在 Obsidian 中编辑
- 笔记数量较少

**优点**：
- 只有一个文件，最简单
- 便于备份和分享

**缺点**：
- 文件可能非常大
- 不便于编辑和管理

**使用方法**：
```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --mode single
```

**输出示例**：
```
flomo-all-notes.md (包含所有笔记)
```

## 🏷️ 标签处理

### 基本标签

Flomo 的标签会自动转换为 Obsidian 标签：

**Flomo**：
```
这是一条笔记 #工作 #项目管理
```

**Obsidian**：
```markdown
这是一条笔记 #工作 #项目管理
```

### 添加标签前缀

如果想给所有导入的笔记添加统一前缀（便于区分来源）：

```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --tag-prefix "imported/flomo/"
```

**结果**：
```markdown
这是一条笔记 #imported/flomo/工作 #imported/flomo/项目管理
```

### 在 Obsidian 中使用标签

1. **标签面板**：在 Obsidian 左侧可以看到所有标签
2. **搜索标签**：使用 `tag:#工作` 搜索
3. **标签嵌套**：使用 `/` 创建层级，如 `#flomo/工作`

## 🔄 增量同步

如果你定期从 Flomo 导出数据，可以使用增量模式避免重复：

### 首次导出

```bash
python scripts/convert.py \
  --input flomo-2024-03-01.html \
  --output ~/Obsidian/Flomo \
  --incremental \
  --state-file ~/.flomo-sync-state.json
```

### 后续导出

```bash
python scripts/convert.py \
  --input flomo-2024-03-15.html \
  --output ~/Obsidian/Flomo \
  --incremental \
  --state-file ~/.flomo-sync-state.json
```

只有新增的笔记会被导入。

### 状态文件说明

状态文件 `.flomo-sync-state.json` 记录：
- 已处理的笔记 ID
- 最后同步时间

**位置**：建议放在用户目录（`~/.flomo-sync-state.json`）

**内容示例**：
```json
{
  "processed_notes": [
    "2024-03-15 09:23:15_123456789",
    "2024-03-15 14:30:22_987654321"
  ],
  "last_sync": "2024-03-15T15:46:37.881234"
}
```

## 🛠️ 高级技巧

### 1. 自定义文件名

编辑 `scripts/config.yaml` 自定义文件命名规则：

```yaml
filename_templates:
  by_date: "{date}.md"
  individual: "memo-{timestamp}.md"
```

### 2. 批量处理多个导出文件

创建一个脚本：

```bash
#!/bin/bash
for file in ~/Downloads/flomo-exports/*.html; do
    python scripts/convert.py \
        --input "$file" \
        --output ~/Obsidian/Flomo \
        --mode by-date \
        --incremental
done
```

### 3. 定期自动同步

使用 cron 定时任务（macOS/Linux）：

```bash
# 编辑 crontab
crontab -e

# 添加每周日晚上 10 点自动同步
0 22 * * 0 /usr/bin/python3 /path/to/convert.py --input ~/Downloads/flomo.html --output ~/Obsidian/Flomo --incremental
```

### 4. 过滤特定标签

如果只想导入带特定标签的笔记，可以修改脚本添加过滤逻辑：

```python
# 在 FlomoParser._extract_tags 方法后添加
def should_include(self, note: FlomoNote, include_tags: List[str]) -> bool:
    return any(tag in note.tags for tag in include_tags)
```

### 5. 处理图片

Flomo HTML 中的图片是外部链接。可以使用 Obsidian 插件下载：

推荐插件：
- **Local Images Plus** - 自动下载外部图片
- **Paste image rename** - 重命名粘贴的图片

## 📝 实战案例

### 案例 1：整理年度笔记

```bash
# 导出 2024 年的所有笔记
python scripts/convert.py \
  --input flomo-2024.html \
  --output ~/Obsidian/Archive/Flomo-2024 \
  --mode by-date \
  --tag-prefix "archive/2024/"
```

### 案例 2：迁移到 Obsidian

```bash
# 第一次完整迁移
python scripts/convert.py \
  --input flomo-all.html \
  --output ~/Obsidian/Flomo \
  --mode individual \
  --preserve-time

# 之后每周同步新笔记
python scripts/convert.py \
  --input flomo-new.html \
  --output ~/Obsidian/Flomo \
  --mode individual \
  --incremental \
  --state-file ~/.flomo-sync.json
```

### 案例 3：备份存档

```bash
# 导出为单个文件作为备份
python scripts/convert.py \
  --input flomo-backup.html \
  --output ~/Backups/Flomo \
  --mode single
```

## 🐛 常见问题

### Q1: 转换后有乱码怎么办？

**A**: 指定正确的编码：

```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --encoding utf-8
```

如果还有问题，尝试 `--encoding gbk` 或 `--encoding gb2312`

---

### Q2: 某些笔记没有被导入？

**A**: 检查日志文件：

```bash
cat conversion.log
```

可能原因：
- HTML 格式不完整
- 笔记缺少时间戳
- 内容为空

---

### Q3: 如何处理重复导入？

**A**: 使用增量模式：

```bash
python scripts/convert.py \
  --input flomo.html \
  --output ~/Obsidian/Flomo \
  --incremental \
  --state-file ~/.flomo-sync.json
```

或者在转换前清空目标目录：

```bash
rm -rf ~/Obsidian/Flomo/*
```

---

### Q4: 标签在 Obsidian 中不可点击？

**A**: 确保标签格式正确：

- ✅ 正确：`#标签`
- ❌ 错误：`# 标签`（有空格）
- ❌ 错误：`##标签`（两个井号）

---

### Q5: 如何批量添加双链？

**A**: 转换后，使用 Obsidian 的全局搜索和替换：

1. 打开命令面板（Cmd+P）
2. 搜索 "Search and Replace"
3. 查找关键词，替换为 `[[关键词]]`

---

### Q6: 转换速度很慢？

**A**: 对于大量笔记（>1000条），可能需要几分钟。你可以：

1. 使用 `--verbose` 查看进度
2. 分批转换
3. 使用更快的解析器：

```bash
pip install lxml
```

脚本会自动使用更快的 lxml 解析器。

## 📚 进阶资源

### Obsidian 相关插件推荐

- **Dataview** - 查询和展示笔记
- **Calendar** - 日历视图
- **Templater** - 笔记模板
- **Tag Wrangler** - 标签管理

### 进一步学习

- [Obsidian 官方文档](https://help.obsidian.md/)
- [Zettelkasten 方法](https://zettelkasten.de/)
- [Obsidian 社区论坛](https://forum.obsidian.md/)

## 💡 最佳实践

1. **定期备份**：转换前备份 Obsidian vault
2. **测试先行**：用小量数据测试转换效果
3. **统一标签**：在 Flomo 中保持标签命名一致
4. **增量同步**：使用增量模式避免重复
5. **版本控制**：将 Obsidian vault 纳入 Git 管理

## 🎯 下一步

1. 运行测试脚本查看效果
2. 选择适合你的组织模式
3. 转换你的 Flomo 数据
4. 在 Obsidian 中探索你的笔记
5. 建立笔记间的链接关系

祝你使用愉快！📖✨
