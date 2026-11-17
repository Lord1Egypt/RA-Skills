# Element Plus 完整文档参考

> 本文档从 Element Plus 官方中文站点 (element-plus.org/zh-CN/) 抓取生成，版本 v2.14.3。
> **每个组件独立存储，按需查阅**，无需一次性加载全部内容。

## 如何使用

1. **查找特定组件 API**：根据下方索引，读取 `components/` 目录下对应文件
2. **查阅开发指南**：读取 `guides/` 目录下对应文件
3. **快速发现**：查看 `llms.txt` 获取完整文档链接清单

## 组件列表

### Basic 基础
- [layout](components/layout.md) — Layout 布局：通过 row/col 创建栅格布局
- [container](components/container.md) — Container 布局容器：页面整体布局容器
- [color](components/color.md) — Color 色彩：主题色、辅助色、中性色规范
- [icon](components/icon.md) — Icon 图标：@element-plus/icons-vue 图标库使用说明
- [button](components/button.md) — Button 按钮：按钮样式、尺寸、状态、加载态
- [link](components/link.md) — Link 文字链接：文字超链接组件
- [text](components/text.md) — Text 文本：文本样式的组件
- [scrollbar](components/scrollbar.md) — Scrollbar 滚动条：自定义滚动条
- [space](components/space.md) — Space 间距：组件间距控制
- [splitter](components/splitter.md) — Splitter 分割面板：面板分割拖拽
- [border](components/border.md) — Border 边框：边框样式规范
- [typography](components/typography.md) — Typography 排版：字号、行高、字体规范

### Config 配置
- [config-provider](components/config-provider.md) — Config Provider 全局配置：全局配置组件

### Form 表单
- [autocomplete](components/autocomplete.md) — Autocomplete 自动补全：输入框自动补全
- [cascader](components/cascader.md) — Cascader 级联选择器：多级联动选择
- [checkbox](components/checkbox.md) — Checkbox 多选框：多选按钮组
- [color-picker](components/color-picker.md) — ColorPicker 颜色选择器：颜色拾取器
- [color-picker-panel](components/color-picker-panel.md) — ColorPickerPanel 颜色选择面板
- [date-picker](components/date-picker.md) — DatePicker 日期选择器：日期选择
- [date-picker-panel](components/date-picker-panel.md) — DatePickerPanel 日期选择面板
- [datetime-picker](components/datetime-picker.md) — DateTimePicker 日期时间选择器
- [form](components/form.md) — Form 表单：表单验证规则、校验、布局
- [input](components/input.md) — Input 输入框：文本输入、文本域
- [input-number](components/input-number.md) — InputNumber 数字输入框：数字输入控件
- [input-tag](components/input-tag.md) — InputTag 标签输入框：标签式输入
- [input-otp](components/input-otp.md) — InputOTP OTP 输入框：一次性密码输入
- [mention](components/mention.md) — Mention 提及：@提及输入
- [radio](components/radio.md) — Radio 单选框：单选按钮组
- [rate](components/rate.md) — Rate 评分：星级评分组件
- [select](components/select.md) — Select 选择器：下拉选择，支持远程搜索、多选
- [select-v2](components/select-v2.md) — SelectV2 虚拟化选择器：大数据量下拉选择
- [slider](components/slider.md) — Slider 滑块：范围值拖动选择
- [switch](components/switch.md) — Switch 开关：布尔值切换
- [time-picker](components/time-picker.md) — TimePicker 时间选择器：时间点选择
- [time-select](components/time-select.md) — TimeSelect 时间选择：固定时间选项
- [transfer](components/transfer.md) — Transfer 穿梭框：双列数据转移
- [tree-select](components/tree-select.md) — TreeSelect 树形选择：树形下拉选择
- [upload](components/upload.md) — Upload 上传：文件上传，支持拖拽、多文件

### Data 数据展示
- [avatar](components/avatar.md) — Avatar 头像：头像展示组件
- [badge](components/badge.md) — Badge 标记：角标/徽标
- [calendar](components/calendar.md) — Calendar 日历：日历组件
- [card](components/card.md) — Card 卡片：卡片容器
- [carousel](components/carousel.md) — Carousel 走马灯：轮播组件
- [collapse](components/collapse.md) — Collapse 折叠面板：手风琴效果
- [empty](components/empty.md) — Empty 空状态：空数据占位
- [image](components/image.md) — Image 图片：图片展示，支持懒加载、预览
- [infinite-scroll](components/infinite-scroll.md) — InfiniteScroll 无限滚动：滚动加载指令
- [pagination](components/pagination.md) — Pagination 分页：分页导航
- [progress](components/progress.md) — Progress 进度条：进度指示
- [result](components/result.md) — Result 结果：操作结果反馈
- [skeleton](components/skeleton.md) — Skeleton 骨架屏：加载占位图
- [table](components/table.md) — Table 表格：数据表格，支持排序、筛选、多选、固定列
- [table-v2](components/table-v2.md) — TableV2 虚拟化表格：大数据量表格
- [tag](components/tag.md) — Tag 标签：标记和分类
- [timeline](components/timeline.md) — Timeline 时间线：时间线组件
- [tour](components/tour.md) — Tour 漫游式引导：分步引导
- [tree](components/tree.md) — Tree 树形控件：树形数据展示，支持懒加载、拖拽
- [tree-v2](components/tree-v2.md) — TreeV2 虚拟化树：大数据量树形控件
- [statistic](components/statistic.md) — Statistic 统计数值：统计数值展示
- [segmented](components/segmented.md) — Segmented 分段控制器：分段选择
- [descriptions](components/descriptions.md) — Descriptions 描述列表：描述信息展示

### Navigation 导航
- [affix](components/affix.md) — Affix 固钉：元素固定定位
- [anchor](components/anchor.md) — Anchor 锚点：页面内锚点导航
- [backtop](components/backtop.md) — Backtop 回到顶部：一键返回页面顶部
- [breadcrumb](components/breadcrumb.md) — Breadcrumb 面包屑：路径导航
- [dropdown](components/dropdown.md) — Dropdown 下拉菜单：下拉操作菜单
- [menu](components/menu.md) — Menu 导航菜单：侧边/顶部导航菜单
- [page-header](components/page-header.md) — PageHeader 页头：页面头部
- [steps](components/steps.md) — Steps 步骤条：分步骤引导
- [tabs](components/tabs.md) — Tabs 标签页：选项卡切换

### Feedback 反馈
- [alert](components/alert.md) — Alert 提示：警告提示
- [dialog](components/dialog.md) — Dialog 对话框：模态对话框
- [drawer](components/drawer.md) — Drawer 抽屉：侧边栏抽屉
- [loading](components/loading.md) — Loading 加载：加载指令与服务
- [message](components/message.md) — Message 消息提示：全局消息 ElMessage
- [message-box](components/message-box.md) — MessageBox 消息弹窗：确认框 ElMessageBox
- [notification](components/notification.md) — Notification 通知：通知提醒 ElNotification
- [popconfirm](components/popconfirm.md) — Popconfirm 气泡确认框：确认操作气泡
- [popover](components/popover.md) — Popover 气泡卡片：悬浮卡片
- [tooltip](components/tooltip.md) — Tooltip 文字提示：悬浮文字提示

### Others 其他
- [watermark](components/watermark.md) — Watermark 水印：页面水印
- [divider](components/divider.md) — Divider 分割线：内容分隔

### 组件总览
- [overview](components/overview.md) — Overview 组件总览

---

## 开发指南

- [installation](guides/installation.md) — 安装：npm/CDN 安装、浏览器兼容性
- [quickstart](guides/quickstart.md) — 快速上手：完整引入 vs 按需引入
- [design](guides/design.md) — 设计原则：一致性、反馈、效率、可控
- [dark-mode](guides/dark-mode.md) — 暗黑模式：CSS Vars 切换
- [theming](guides/theming.md) — 主题定制：CSS 变量覆盖
- [i18n](guides/i18n.md) — 国际化：多语言配置
- [migration](guides/migration.md) — 迁移：Element UI (Vue 2) → Element Plus (Vue 3)
- [ssr](guides/ssr.md) — 服务端渲染：SSR 配置
- [namespace](guides/namespace.md) — 命名空间：自定义 CSS 前缀
- [transitions](guides/transitions.md) — 过渡动画：内置过渡效果
- [nav](guides/nav.md) — 导航指南：导航设计规范
- [custom-defaults](guides/custom-defaults.md) — 自定义默认值

---

## 补充文档

- [changelog](extra-guides/changelog.md) — 更新日志：完整版本历史
- [commit-examples](extra-guides/commit-examples.md) — Git 提交示例
- [dev-guide](extra-guides/dev-guide.md) — 开发者指南
- [translation](extra-guides/translation.md) — 翻译指南
- [dev-faq](extra-guides/dev-faq.md) — 开发常见问题
