# 组件规范检查清单

生成交付文档时，逐项确认每个组件是否覆盖以下内容：

## 必填项

- [ ] 尺寸（宽 × 高）
- [ ] 背景色（HEX）
- [ ] 文字色（HEX）
- [ ] 字体（family + size + weight + line-height）
- [ ] 内边距（padding）
- [ ] 外边距（margin）
- [ ] 圆角（radius）
- [ ] 边框（粗细 + 颜色 + 样式）
- [ ] 阴影（shadow）

## 状态覆盖

- [ ] Normal（默认态）
- [ ] Pressed / Active（按压/选中态）
- [ ] Disabled（禁用态）
- [ ] Hover（Web/桌面端）
- [ ] Focus（Web/表单）
- [ ] Error（错误态）
- [ ] Loading（加载中）
- [ ] Empty（空数据）

## 交互确认

- [ ] 点击行为（跳转/弹窗/切换/提交）
- [ ] 动效（时长 + 曲线 + 方向）
- [ ] 长按行为（Android/小程序）
- [ ] 滑动行为（左滑删除/右滑操作）
- [ ] 下拉刷新 / 上拉加载（小程序/App）

## 数据确认

- [ ] 每个动态内容对应的数据字段
- [ ] 字段类型（string / number / array / image url）
- [ ] 数据为空时的处理
- [ ] 数据超长时的处理（截断 / 换行 / 省略号）

## 切图确认

- [ ] 图标是否需要多倍图（@2x/@3x 或 mdpi~xxxhdpi）
- [ ] 图片格式（PNG / WebP / SVG）
- [ ] 命名是否规范
- [ ] 动效是否用 Lottie / GIF / 代码实现