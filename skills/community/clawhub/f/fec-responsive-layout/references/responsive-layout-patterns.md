# 响应式布局模式

## 策略选择

| 场景 | 策略 |
| ---- | ---- |
| 页面级结构 | 移动优先断点 |
| 会被放进未知父容器的复用组件 | 容器查询 |
| 卡片网格 | `repeat(auto-fit, minmax())`，并设置合理最小宽度 |
| 数据表格 | 列优先级、横向滚动或移动端摘要行 |
| 编辑器 / 画布 / dashboard | 稳定外壳 + 可滚动工作区 |

## CSS 模式

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: 1rem;
}

.panel {
  min-width: 0;
  container-type: inline-size;
}

@container (min-width: 42rem) {
  .panel-body {
    display: grid;
    grid-template-columns: 16rem minmax(0, 1fr);
  }
}
```

当 grid/flex 子项包含长文本、表格、代码、图表或媒体时，给子项设置 `min-width: 0`。

## 数据密集型界面

- 编码前先确定移动端列优先级。
- 主标识、状态和主要操作保持可见。
- 低优先级元数据移入详情行、抽屉或可展开面板。
- 小屏仍要保留排序、筛选、分页和选择能力。
- 虚拟滚动只解决 DOM 数量问题，不能解决信息层级问题。

## 触控与视口检查

- 空间允许时，交互目标至少 44x44px。
- 移动端输入框字号避免低于 16px。
- 固定底部栏和操作条必须考虑 `env(safe-area-inset-bottom)`。
- 对话框和抽屉需要适配虚拟键盘导致的视口变化。
- 只在 hover 时出现的内容必须提供点击、焦点或常驻可见替代方案。

## 验证清单

- 320-375px：页面级没有横向溢出。
- 768px：布局切换后阅读顺序仍然合理。
- 1024-1440px：内容宽度有约束，扫描路径清晰。
- 长标签、翻译文本、数字以及 empty/error/loading 状态不会撑坏固定格式控件。
- 横竖屏切换不会困住焦点或隐藏主操作。
