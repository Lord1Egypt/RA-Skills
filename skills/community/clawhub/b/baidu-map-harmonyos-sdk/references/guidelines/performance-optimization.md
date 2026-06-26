## 地图性能与覆盖物分层规范

本文件补充 `SKILL.md` 中「地图功能开发（代码组织与规范）」下的性能与分层要求。

### 1. 性能优化：缓存复用，避免反复重建

在以下场景中，频繁创建/销毁对象会导致不必要的内存分配和 UI 刷新：

- 位置轮询（定时更新坐标）
- 气泡自动消失/重新显示
- 轨迹回放（沿轨迹移动标注/气泡）

**强制要求：**

- 首次创建完整 UI 结构时缓存关键对象（如 `PopView`、`LabelUI` 等）。
- 后续仅更新必要的字段（如文本内容、可见性），禁止每次都重新构建整棵 UI 树。
- 当绑定对象（如 Marker）被销毁并重建时，必须同步重置缓存引用。

示例（正确做法）：

```ts
// ✅ 正确：缓存 PopView + LabelUI，后续只更新文本
private childPopView: PopView | null = null;
private childPopLabel: LabelUI | null = null;

private updatePopView(text: string): void {
  if (this.childPopLabel !== null) {
    this.childPopLabel.setText(text);  // 只更新文本，不重建结构
    return;
  }
  // 首次才创建完整结构...
  this.childPopLabel = new LabelUI();
  // ... 设置样式 ...
  this.childPopView = new PopView();
  // ... 绑定到 Marker ...
}

private togglePopView(visible: boolean): void {
  if (this.childPopView !== null) {
    this.childPopView.setVisibility(
      visible ? SysEnum.Visibility.VISIBLE : SysEnum.Visibility.GONE
    );
  }
}
```

> 提示：回答中若涉及 PopView/信息框或高频更新 UI 的逻辑，应主动提醒「缓存复用」策略，避免每次重建。

### 2. 覆盖物 zIndex 分层规范（必须显式设置）

默认 `zIndex = 0` 容易导致后添加的信息气泡、标注被先添加的轨迹线、面等遮挡，出现“气泡在下面看不到”的问题。

**强制要求：**

- 为所有覆盖物（Marker、Polyline、Polygon、PopView 等）显式指定 `zIndex`，禁止依赖默认值。
- 在项目初期约定统一的分层表，并在新增覆盖物时对照执行。

推荐分层表：

| 层级 | zIndex 范围 | 覆盖物类型 |
|------|-------------|------------|
| 底层 | 0           | 安全区域 Polygon、地理围栏等面状底图 |
| 中层 | 1-2         | 轨迹线 Polyline、路线规划线 |
| 标记层 | 3-5       | 起点/终点 Marker、动画回放 Marker |
| 顶层 | 10+         | 信息气泡 Marker（承载 PopView）、临时标注 |

特别说明：

- 承载 PopView 的透明 Marker 决定了气泡的显示层级，必须高于所有可能与之重叠的覆盖物。
- 若业务上存在额外图层（如告警区域、热点点位），应在以上分层表基础上预留范围，并在文档中补充说明。

