# Keynote MCP Server

> **通过 Model Context Protocol (MCP) 让 AI 直接操作 macOS Keynote**
>
> **作者**: Wang Dongjie, CGMA/AICPA&CIMA, © 2026
>
> **版本**: 3.0 (完整 Keynote 专业优势支持)
> **平台**: macOS 12.0+ (Monterey 及以上)
> **语言**: Python 3.10+

---

## 项目简介

这是一个 **MCP (Model Context Protocol) Server**，封装了 AppleScript 和 JavaScript for Automation (JXA) 调用，让 TRAE 和其他兼容 MCP 的 AI 助手可以直接操作 macOS 上的 Keynote.app，**直接生成 .key 文件**。

**核心能力：**
- 直接创建 Keynote .key 文件（无需 PPTX 中间格式）
- 创建新的 Keynote 演示文稿（含数智财务 SAP 风格）
- 设置超宽屏画布尺寸（3:1 比例）
- 添加/删除/排列幻灯片
- 设置标题、正文、图片等内容
- 应用 Keynote 主题和母版
- 控制文本格式（字体、大小、颜色）
- 添加动画效果和过渡
- 播放/停止/跳转到指定幻灯片
- 导出为 PDF、PPTX、MOV、图片等格式
- 查询当前文档信息和幻灯片结构

**新增能力 (v3.0)：**
- **屏幕适配** - 自动适配多种屏幕尺寸（16:9/16:10/3:1超宽屏）
- **动画效果** - 支持 Magic Move、渐隐、推入等专业动画
- **设计优势** - 利用 Keynote 原生设计引擎（母版、主题、布局）
- **稳定性** - AppleScript 原生调用，稳定可靠
- **视觉渲染** - macOS Core Animation 高质量渲染
- **性能表现** - 原生 Metal 图形引擎，流畅播放
- **字体渲染** - 苹方/SF Pro 专业字体渲染
- **专业展示** - 演讲者模式、计时器、备注显示

---

## Keynote 专业优势

### 1. 屏幕适配

Keynote 支持多种画布尺寸，自动适配不同显示环境：

| 尺寸类型 | 像素尺寸 | 比例 | 适用场景 |
|---------|---------|------|---------|
| **标准 16:9** | 1920 × 1080 | 1.78:1 | 全高清屏幕、投影仪 |
| **标准 16:10** | 1680 × 1050 | 1.60:1 | MacBook Pro 屏幕 |
| **超宽屏 3:1** | 3200 × 1080 | 2.96:1 | 企业峰会、LED大屏 |
| **超宽屏 3.55:1** | 3840 × 1080 | 3.55:1 | 展会大屏、发布会 |
| **4K 超高清** | 3840 × 2160 | 1.78:1 | 4K 显示器、高端投影 |

**MCP 工具支持：**
- `keynote_set_canvas_size(width, height)` - 设置画布尺寸
- `keynote_create_ultra_wide()` - 创建超宽屏演示文稿
- `keynote_get_canvas_info()` - 获取当前画布信息
- `keynote_auto_fit_screen()` - 自动适配当前屏幕

---

### 2. 动画效果

Keynote 提供业界领先的动画效果，让演示更加生动：

**过渡动画类型：**
| 动画名称 | 效果描述 | 适用场景 |
|---------|---------|---------|
| **Magic Move** ⭐ | 神奇移动，元素平滑过渡 | 产品演进、对比展示 |
| **Fade** | 渐隐效果 | 通用过渡 |
| **Push** | 推入效果 | 线性叙事 |
| **Flip** | 翻转效果 | 对比切换 |
| **Cube** | 立方体旋转 | 3D效果 |
| **Page Flip** | 书页翻转 | 文档风格 |
| **Reveal** | 渐显效果 | 内容揭示 |
| **Drop** | 下落效果 | 强调展示 |
| **Object Push** | 对象推入 | 元素动画 |
| **Object Zoom** | 对象缩放 | 细节展示 |

**构建动画（元素动画）：**
| 动画类型 | 效果 | 用途 |
|---------|------|------|
| **Build In** | 进入动画 | 元素出现 |
| **Build Out** | 退出动画 | 元素消失 |
| **Action** | 动作动画 | 强调、移动、缩放 |

**MCP 工具支持：**
- `keynote_set_transition(slide_number, transition_type)` - 设置过渡动画
- `keynote_add_build_animation(slide_number, element, animation_type)` - 添加构建动画
- `keynote_set_magic_move(from_slide, to_slide)` - 设置 Magic Move
- `keynote_preview_animation(slide_number)` - 预览动画效果

---

### 3. 设计优势

Keynote 内置强大的设计引擎，提供专业级视觉效果：

**主题系统：**
- 40+ 内置主题（Black、White、Gradient、Photo Essay 等）
- 自定义主题创建
- 主题一致性保证

**母版系统：**
- 预定义布局模板（Title、Title & Content、Two Column 等）
- 自定义母版创建
- 统一视觉风格

**智能布局：**
- 自动对齐参考线
- 智能间距调整
- 元素自动排列

**MCP 工具支持：**
- `keynote_list_themes()` - 列出可用主题
- `keynote_list_masters()` - 列出可用母版
- `keynote_apply_theme(theme_name)` - 应用主题
- `keynote_set_master(slide_number, master_name)` - 设置母版
- `keynote_align_elements(slide_number, alignment)` - 对齐元素

---

### 4. 稳定性

Keynote 通过 AppleScript 原生调用，确保稳定可靠：

**稳定性特点：**
- AppleScript 是 macOS 原生自动化框架
- Keynote.app 官方支持 AppleScript 控制
- 无第三方依赖，减少故障点
- 进程隔离，不影响主程序
- 错误恢复机制完善

**错误处理：**
- 自动检测 Keynote 运行状态
- 超时保护机制
- 异常捕获和友好提示
- 自动重试机制

**MCP 工具支持：**
- `keynote_check_status()` - 检查 Keynote 状态
- `keynote_is_running()` - 检查运行状态
- `keynote_restart_if_needed()` - 自动重启
- `keynote_error_recovery()` - 错误恢复

---

### 5. 视觉渲染

Keynote 使用 macOS Core Animation 引擎，提供高质量视觉渲染：

**渲染优势：**
- Core Animation 硬件加速
- Metal 图形引擎支持
- Retina 显示优化
- 抗锯齿平滑处理
- 高质量阴影效果
- 透明度混合优化

**渲染质量：**
- 60fps 流畅播放
- 无撕裂现象
- 色彩准确还原
- 渐变平滑过渡
- 文字清晰锐利

**MCP 工具支持：**
- `keynote_set_render_quality(quality)` - 设置渲染质量
- `keynote_enable_retina_mode()` - 启用 Retina 模式
- `keynote_preview_render(slide_number)` - 预览渲染效果

---

### 6. 性能表现

Keynote 使用原生 Metal 图形引擎，性能表现卓越：

**性能指标：**
| 指标 | Keynote | PowerPoint |
|------|---------|------------|
| 启动速度 | ~2秒 | ~5秒 |
| 滑动切换 | <0.1秒 | ~0.3秒 |
| 动画流畅度 | 60fps | 30-60fps |
| 内存占用 | 低 | 较高 |
| 大文件处理 | 快 | 较慢 |

**性能优化：**
- 懒加载机制
- 智能缓存
- GPU 加速
- 内存管理优化
- 大型演示文稿优化

**MCP 工具支持：**
- `keynote_get_performance_info()` - 获取性能信息
- `keynote_optimize_performance()` - 优化性能
- `keynote_clear_cache()` - 清理缓存

---

### 7. 字体渲染

Keynote 提供专业级字体渲染，确保文字清晰美观：

**字体系统：**
| 字体类型 | 字体名称 | 用途 |
|---------|---------|------|
| **中文标题** | 苹方 Bold (PingFang SC) | 封面、章节标题 |
| **中文正文** | 苹方 Regular | 正文、卡片内容 |
| **英文标题** | SF Pro Display Heavy | 英文标题 |
| **英文正文** | SF Pro Text Regular | 英文正文 |
| **数字强调** | SF Pro Display Black | KPI 数字 |

**字体渲染特点：**
- Retina 字体优化
- 抗锯齿平滑
- 字间距智能调整
- 行高自动优化
- 多语言混排支持

**字号规范：**
| 层级 | 字号 | 用途 |
|------|------|------|
| Lv1 封面主标题 | 88-120pt | 封面大标题 |
| Lv2 章节标题 | 48-64pt | 内容页标题 |
| Lv3 卡片标题 | 28-36pt | 卡片小标题 |
| Lv4 正文 | 18-22pt | 段落文字 |
| Lv5 KPI 数字 | 60-120pt | 超大数字强调 |
| Lv6 小字备注 | 12-14pt | 脚注、来源 |

**MCP 工具支持：**
- `keynote_set_font(slide_number, element, font_name)` - 设置字体
- `keynote_set_font_size(slide_number, element, size)` - 设置字号
- `keynote_set_font_color(slide_number, element, color)` - 设置颜色
- `keynote_apply_font_style(style_name)` - 应用字体样式

---

### 8. 专业展示

Keynote 提供专业级演示展示功能：

**演讲者模式：**
- 双屏显示（演讲者看备注，观众看幻灯片）
- 演讲者备注显示
- 下一张预览
- 计时器显示
- 演讲进度指示

**演示控制：**
- 自动播放计时
- 循环播放模式
- 指定范围播放
- 隐藏幻灯片
- 跳转控制

**导出选项：**
| 格式 | 用途 | 特点 |
|------|------|------|
| **PDF** | 打印/分享 | 高质量矢量 |
| **PPTX** | PowerPoint 兼容 | 格式保留 |
| **MOV** | 视频导出 | 包含动画 |
| **HTML** | 网页分享 | 交互式 |
| **Images** | 图片导出 | 每张幻灯片 |

**MCP 工具支持：**
- `keynote_start_presenter_mode()` - 启动演讲者模式
- `keynote_set_timer(duration)` - 设置计时器
- `keynote_set_auto_play(interval)` - 设置自动播放
- `keynote_export(format, path)` - 导出文件
- `keynote_print_notes()` - 打印备注

---

## 目录结构

```
keynote-mcp-server/
├── README.md                          # 详细说明
├── SKILL.md                           # Skill 说明文档（本文件）
├── pyproject.toml                     # 项目配置
├── requirements.txt                   # pip 依赖列表
├── server.py                          # MCP Server 主程序（FastMCP v3.0）
├── quickstart.py                      # 本地测试脚本
├── keynote_tools/                     # Keynote 操作模块
│   ├── __init__.py
│   ├── applescript.py                 # AppleScript 执行引擎（含动画支持）
│   └── keynote_controller.py          # 高层 Keynote 控制器
├── examples/
│   ├── claude_desktop_config.json     # Claude Desktop 配置示例
│   └── demo_presentation.key          # 示例文件
├── install.sh                         # 一键安装脚本
└── test_connection.py                 # 本地连接性测试
```

---

## 快速开始（3 步）

### 步骤 1: 安装依赖

```bash
cd keynote-mcp-server

# 方式 A: 使用一键安装脚本（推荐）
./install.sh

# 方式 B: 手动安装
pip install "mcp[cli]"
```

### 步骤 2: 测试本地脚本

```bash
# 测试 Keynote 连接
python3 quickstart.py --test

# 创建演示文稿
python3 quickstart.py --demo

# 创建数智财务风格演示文稿
python3 quickstart.py --digital-finance

# 创建带动画的演示文稿
python3 quickstart.py --animation-demo
```

### 步骤 3: 配置 MCP 连接

**编辑配置文件：**
```json
{
  "mcpServers": {
    "keynote": {
      "type": "stdio",
      "command": "/usr/bin/python3",
      "args": [
        "/YOUR_PATH/keynote-mcp-server/server.py"
      ]
    }
  }
}
```

---

## 可用工具（MCP Tools）

### 文档管理

| 工具名 | 说明 |
|--------|------|
| `keynote_create` | 创建新的 Keynote 文档 |
| `keynote_create_ultra_wide` | 创建超宽屏演示文稿（3:1） |
| `keynote_create_digital_finance` | 创建数智财务 SAP 风格演示文稿 |
| `keynote_create_valuation_report` | 创建上市公司估值报告（13页） |
| `keynote_open` | 打开现有的 .key 文件 |
| `keynote_save` | 保存当前文档 |
| `keynote_close` | 关闭当前文档 |
| `keynote_export` | 导出为 PDF/PPTX/MOV/图片 |
| `keynote_set_canvas_size` | 设置画布尺寸 |
| `keynote_auto_fit_screen` | 自动适配屏幕 |

### 幻灯片操作

| 工具名 | 说明 |
|--------|------|
| `keynote_add_slide` | 添加新幻灯片 |
| `keynote_add_kpi_slide` | 添加 KPI 数字展示幻灯片 |
| `keynote_delete_slide` | 删除指定幻灯片 |
| `keynote_list_slides` | 列出文档中所有幻灯片 |
| `keynote_duplicate_slide` | 复制幻灯片 |
| `keynote_move_slide` | 移动幻灯片位置 |

### 动画效果

| 工具名 | 说明 |
|--------|------|
| `keynote_set_transition` | 设置过渡动画（Magic Move/Fade/Push 等） |
| `keynote_add_build_animation` | 添加构建动画 |
| `keynote_set_magic_move` | 设置 Magic Move 神奇移动 |
| `keynote_preview_animation` | 预览动画效果 |
| `keynote_clear_animations` | 清除动画效果 |

### 设计与布局

| 工具名 | 说明 |
|--------|------|
| `keynote_list_themes` | 列出可用主题 |
| `keynote_list_masters` | 列出可用母版 |
| `keynote_apply_theme` | 应用主题 |
| `keynote_set_master` | 设置母版 |
| `keynote_align_elements` | 对齐元素 |

### 字体与样式

| 工具名 | 说明 |
|--------|------|
| `keynote_set_font` | 设置字体 |
| `keynote_set_font_size` | 设置字号 |
| `keynote_set_font_color` | 设置颜色 |
| `keynote_apply_font_style` | 应用字体样式 |

### 演示控制

| 工具名 | 说明 |
|--------|------|
| `keynote_start_show` | 开始演示 |
| `keynote_start_presenter_mode` | 启动演讲者模式 |
| `keynote_stop_show` | 停止演示 |
| `keynote_set_timer` | 设置计时器 |
| `keynote_set_auto_play` | 设置自动播放 |
| `keynote_next_slide` | 下一张 |
| `keynote_prev_slide` | 上一张 |
| `keynote_go_to_slide` | 跳转到指定幻灯片 |

### 查询

| 工具名 | 说明 |
|--------|------|
| `keynote_get_info` | 获取当前文档信息 |
| `keynote_get_canvas_info` | 获取画布尺寸信息 |
| `keynote_get_slide_content` | 获取幻灯片内容 |
| `keynote_get_performance_info` | 获取性能信息 |
| `keynote_check_status` | 检查 Keynote 状态 |

---

## 使用示例

### 示例 1: 创建带动画的数智财务演示文稿

```
用 Keynote 创建一个数智财务峰会演示文稿。
标题是 "数智财务峰会"。
使用 Black 深色主题。
设置画布为超宽屏 3200×1080。
添加 Magic Move 过渡动画。
包含以下幻灯片：
1. 封面 - 大标题 + 金色光带
2. KPI 数据展示 - 金色大数字动画进入
3. 业务分析 - 三栏卡片布局
4. 解决方案架构 - 环形图动画
5. 实施成果 - 数据对比动画
6. Thank You - 渐隐过渡
```

### 示例 2: 创建上市公司估值报告（专业展示）

```
用 Keynote 创建一个上市公司估值报告。
股票代码: 600170
公司名称: 上海建工
使用数智财务 SAP 风格。
超宽屏画布 3200×1080。
添加 Magic Move 动画效果。
设置演讲者模式。
包含完整的 13 页估值分析结构。
导出为 PDF 和 MOV 视频。
```

### 示例 3: 屏幕适配演示

```
用 Keynote 创建一个演示文稿。
自动适配当前屏幕尺寸。
使用 Gradient 主题。
添加 5 张幻灯片。
设置 Fade 过渡动画。
启动演讲者模式。
```

---

## 数智财务 SAP 风格配色

```
主背景渐变:
  顶部:     #0A1838 (深海军蓝)
  中部:     #5A0F25 (暗红)
  底部:     #8B0029 (深邃红)

主文本色:   #FFFFFF (纯白)
次要文本:   #E8ECF5 (冷调浅蓝白)

强调色体系:
  金色光带:  #F2B84B ← 装饰/序号/KPI数字
  SAP蓝:    #0070D2 ← 品牌LOGO/官方按钮
  青色:     #25B7E0 ← 矩阵背景/流程节点
  财务绿:   #2FA472 ← 正向数据/提升标记
  品牌红:   #B8003A ← 卡片边框/问题标注

卡片规范:
  内部底色: #0F2050 (深蓝)
  边框颜色: #B8003A (深红)
  圆角:     20px
```

---

## 安全性与权限

### 首次运行时的权限请求

```
"python3" 想要控制 "Keynote"
允许/不允许
```

请点击 **"允许"**。

### 手动授予权限

1. 打开 "系统设置" → "隐私与安全性" → "自动化"
2. 找到 python3
3. 勾选 Keynote 复选框

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v3.0 | 2026 | 新增动画效果支持 / 屏幕适配 / 设计引擎 / 字体渲染 / 专业展示 / 演讲者模式 |
| v2.0 | 2026 | 新增数智财务 SAP 风格支持 / 超宽屏画布 / 估值报告模板 / KPI 幻灯片 |
| v1.0 | 2024 | 初始版本：基础 Keynote 操作 |

---

## 版权声明

**作者**: Wang Dongjie, CGMA/AICPA&CIMA
**版权**: © 2026 Wang Dongjie. All rights reserved.
**许可**: 仅供个人和企业内部使用，未经授权不得用于商业分发。

---

## 参考资源

- **MCP 官方文档**: https://modelcontextprotocol.io/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **Keynote AppleScript 指南**: https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/Keynote_Scripting_Guide/
- **AppleScript 语言指南**: https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/

---

**开始使用**: 运行 `./install.sh` 安装，配置 MCP 连接，即可让 AI 直接生成 Keynote 文件！