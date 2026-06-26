# Navigation Components

> 来源：Apple HIG - Navigation / Tab Bars / Page Sheets (2026)
> https://developer.apple.com/design/human-interface-guidelines/navigation
> https://developer.apple.com/design/human-interface-guidelines/tab-bars
> https://developer.apple.com/design/human-interface-guidelines/page-sheets

## Navigation Bar（导航栏）

### 用途
提供从子页面返回的能力，显示当前内容的标题和操作按钮。

### iOS Navigation Bar
- 位于屏幕顶部
- 左侧：返回按钮（自动生成）
- 中间：大标题（Large Title）或标准标题
- 右侧：操作按钮（最多 2 个）

### Large Title
- 大标题在滚动时自动收缩为标准标题
- 体现内容层级（App 名 → 页面标题）
- iOS 原生 App（设置、音乐）标配

### 设计规范
- 高度：44pt（不含状态栏）
- 返回按钮文字：上一页标题或 "Back"
- 标题文字：居中，不要截断

---

## Tab Bar（标签栏）

### 用途
在 App 的主要功能区之间快速切换。

### iOS Tab Bar
- 位于屏幕底部（iPhone）/ 侧边（iPad）
- 最多 5 个标签（超过 5 个用"更多"）
- 图标 + 短文字标签
- 选中项：强调色图标 + 可能文字

### Tab Bar 项目
- **图标**：`SF Symbol`（filled 变体）
- **文字**：1-2 个词，全小写或首字母大写
- **Badge**：右上角红点/数字，显示新内容数量

### 分隔线
- Tab Bar 上方细线（1px），在内容滚动时不随动
- 内容与 Tab Bar 留有间距

### iPad 适配
- iPad 上 Tab Bar 可折叠为侧边栏（Sidebar）
- Sidebar 支持嵌套层级

---

## Page Sheets（页面表单）

### 用途
模态展示次要内容或任务流程，完成后可关闭。

### iOS Page Sheet
- 从屏幕底部滑入
- 顶部有小型拖动条（grabber）
- 轻扫向下或拖动条下拉可关闭
- 背景有轻微遮罩（iOS 13+ 的 `.pageSheet` 样式）

### 高度
- Sheet 高度自动适应内容
- 可设定不同的 detents（停靠高度）：
  - `.medium`（半屏）
  - `.large`（全屏，除了顶部圆角区域）

### 表单内容
- 大型标题在顶部
- 主要内容在 ScrollView 中
- 底部可放操作按钮

---

## Toolbar（工具栏）

### 用途
提供与当前上下文相关的操作。

### 位置
- iOS：Navigation Bar 下方或键盘上方
- macOS：窗口顶部（Menu Bar 下方）

### 设计
- 图标按钮 + 可选文字标签
- 图标用 SF Symbols（outline 变体）
- 工具栏分组用细线分隔

---

## Segmented Control（分段控件）

一组互斥选项按钮。

### 场景
- 切换视图模式（列表/网格）
- 切换时间范围（今日/本周/本月）
- 切换筛选条件

### 设计
- 选中项：背景填充 + 白色文字
- 未选中项：透明背景 + label 颜色文字
- 最多 5 项（内容较长时用 3 项以内）
- 不适合表示开关状态（用 Toggle）

---

## Sidebar（侧边栏）

### 用途
iPad 多栏布局中的导航面板，或 macOS App 的主导航。

### 设计
- 毛玻璃背景
- 嵌套列表支持多级展开
- 选中项有背景高亮
- 支持拖动调整宽度

---

## 导航模式对比

| 模式 | 适用平台 | 用途 |
|------|---------|------|
| Navigation Bar + Large Title | iOS/iPadOS | 分层内容浏览 |
| Tab Bar | iOS/iPadOS | 功能模块切换 |
| Toolbar | 全平台 | 上下文操作 |
| Page Sheet | iOS/iPadOS | 模态任务 |
| Sidebar | iPad/macOS | 多栏导航 |
| Segmented Control | 全平台 | 同类选项切换 |
