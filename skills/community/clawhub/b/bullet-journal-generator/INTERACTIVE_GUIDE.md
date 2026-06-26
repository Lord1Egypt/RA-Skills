# 交互式任务管理使用指南

## 📖 概述

子弹笔记生成器的交互式版本允许你：
- ✅ 点击任务符号切换状态（● → × → > → ~~ → <）
- ✅ 使用操作按钮进行精确操作
- ✅ 实时查看统计信息
- ✅ 自动更新打印版本

## 🚀 快速开始

### 1. 生成测试数据

```bash
cd /Users/sirutong/Desktop/skills/bullet-journal-gen/scripts
python3 test_interactive.py
```

这会生成包含任务的测试数据和交互式HTML卡片。

### 2. 启动HTTP服务器

```bash
python3 server.py
```

服务器将在 `http://localhost:8000` 启动，用于处理任务状态更新和打印版同步。

### 3. 打开交互式卡片

在浏览器中打开生成的HTML文件：

```bash
open cards/2026-03-16-interactive.html
```

或者直接在浏览器中访问：
```
file:///Users/sirutong/Desktop/skills/bullet-journal-gen/cards/2026-03-16-interactive.html
```

## 🎯 使用交互式卡片

### 方式1：点击符号切换状态

1. 将鼠标悬停在任务符号（●）上，会显示操作提示
2. 点击符号，任务会自动切换到下一个状态
3. 状态变化顺序：`待办` → `已完成` → `待办`（可撤销）

### 方式2：使用操作按钮

悬停在任务项上，会显示操作按钮：

- **✓ 完成** - 将任务标记为已完成（×）
- **→ 迁移** - 将任务延期到新日期（>）
- **✗ 取消** - 取消任务（~~）

### 查看统计信息

页面底部显示今日任务统计：
- 总任务数
- 已完成数
- 待办数
- 完成率

统计信息会随着任务状态变化实时更新。

## 🔄 状态变化规则

### 符号系统

| 符号 | 状态 | 含义 |
|------|------|------|
| ● | 待办 | 需要执行的任务 |
| × | 已完成 | 任务已成功完成 |
| > | 已迁移 | 任务延期到新日期 |
| ~~ | 已取消 | 任务不再需要 |
| < | 已计划 | 任务升级为项目 |

### 状态转换

```
●（待办）
  ├─→ ×（已完成）─→ ●（可撤销）
  ├─→ >（已迁移）
  ├─→ ~~（已取消）
  └─→ <（已计划）

>（已迁移）
  ├─→ ●（在新日期重新开始）
  └─→ ~~（取消）

<（已计划）─→ ●（开始执行）
```

## 📄 打印版自动更新

### 功能说明

每次在交互式卡片中更新任务状态后，系统会自动：

1. 更新本地JSON文件中的任务状态
2. 重新生成打印版HTML文件
3. 保存最新的任务状态到 `tasks.json`

### 查看打印版

打印版会自动保存在 `printable/` 目录中：

```bash
open printable/2026-03-16.html
```

打印版包含：
- 当前日期和天气信息
- 所有笔记内容（包含最新状态）
- A4纸张格式
- 高分辨率打印样式

## 🔧 技术实现

### HTTP API

服务器提供以下API端点：

#### 1. 健康检查
```bash
GET http://localhost:8000/health
```

#### 2. 更新任务状态
```bash
POST http://localhost:8000/update_task_status

Content-Type: application/json

{
  "task_id": "task_001",
  "date": "2026-03-16",
  "from_status": "task",
  "to_status": "completed"
}
```

响应：
```json
{
  "success": true,
  "message": "任务状态更新成功：待办 → 已完成",
  "result": {
    "task_id": "task_001",
    "status": "completed"
  }
}
```

#### 3. 同步到打印版
```bash
POST http://localhost:8000/sync_to_printable

Content-Type: application/json

{
  "date": "2026-03-16"
}
```

响应：
```json
{
  "success": true,
  "message": "打印版已更新",
  "printable_path": "/path/to/printable/2026-03-16.html"
}
```

### 数据流

```
用户点击符号
    ↓
JavaScript捕获事件
    ↓
调用HTTP API
    ↓
服务器更新tasks.json
    ↓
服务器更新data.json
    ↓
服务器重新生成打印版HTML
    ↓
返回成功响应
    ↓
JavaScript更新UI
```

## 📂 文件结构

```
bullet-journal-gen/
├── scripts/
│   ├── server.py              # HTTP服务器
│   ├── test_interactive.py    # 测试数据生成
│   ├── task_manager.py        # 任务状态管理
│   └── generate_interactive_card.py  # 交互式卡片生成
├── templates/
│   └── interactive_card_template.html  # 交互式卡片模板
├── cards/
│   └── 2026-03-16-interactive.html  # 生成的交互式卡片
├── printable/
│   └── 2026-03-16.html        # 自动更新的打印版
└── data/
    ├── 2026/03/16/
    │   ├── data.json          # 笔记数据
    │   └── tasks.json         # 任务状态数据
    └── tasks/
        └── 2026-03-16/
            └── tasks.json     # 任务详细数据
```

## 💡 使用技巧

### 1. 批量完成任务

可以连续点击多个任务的●符号，快速标记为已完成。

### 2. 迁移未完成任务

对于未完成但重要的任务，点击→按钮，将任务延期到新日期。

### 3. 取消不需要的任务

对于不再需要的任务，点击✗按钮，将其标记为已取消。

### 4. 查看任务历史

任务的所有状态变化都会记录在 `tasks.json` 中，可以随时查看。

## ⚠️ 注意事项

1. **服务器必须运行**：交互式功能需要HTTP服务器运行，否则只能本地更新UI
2. **CORS问题**：如果遇到跨域问题，确保服务器在本地运行
3. **数据备份**：建议定期备份 `data/` 目录
4. **打印版更新**：打印版会在每次状态更新后自动更新，无需手动操作

## 🔍 故障排查

### 问题1：点击符号没有反应

**可能原因**：
- HTTP服务器未启动
- 浏览器控制台有JavaScript错误

**解决方案**：
```bash
# 检查服务器是否运行
curl http://localhost:8000/health

# 查看浏览器控制台（F12）查看错误信息
```

### 问题2：打印版没有更新

**可能原因**：
- 服务器API调用失败
- 文件权限问题

**解决方案**：
```bash
# 检查服务器日志
# 手动同步到打印版
curl -X POST http://localhost:8000/sync_to_printable \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-03-16"}'
```

### 问题3：任务状态没有保存

**可能原因**：
- `tasks.json` 文件权限问题
- 磁盘空间不足

**解决方案**：
```bash
# 检查文件权限
ls -la data/tasks/2026-03-16/

# 检查磁盘空间
df -h
```

## 🎉 总结

交互式任务管理功能让子弹笔记更加实用和高效：

- ✅ 直观的可视化界面
- ✅ 便捷的任务状态切换
- ✅ 实时的统计信息
- ✅ 自动的打印版更新
- ✅ 完整的状态历史记录

享受智能化的任务管理体验！
