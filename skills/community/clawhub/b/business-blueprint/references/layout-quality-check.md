# 架构图质量检查标准

## 1. 节点完整性

- [ ] **Clients 入口节点**: 如果 blueprint 有 actors，必须生成 Clients 节点作为数据流起点
- [ ] **所有 systems 都有节点**: layout 节点数 = blueprint systems 数 + Clients（如果有 actors）

## 2. 无重叠

- [ ] 任意两个节点矩形不重叠（x/y 间距足够）
- [ ] 同列垂直堆叠的节点间距 >= 50px（gap = y_b - (y_a + h_a)）
- [ ] 同行水平排列的节点间距 >= 200px（中心到中心）

## 3. 文字不溢出

- [ ] 节点标题文字宽度 < 节点宽度 * 0.85（中文按 8px/字符，英文按 6px/字符）
- [ ] 节点副标题文字宽度 < 节点宽度 * 0.9（按 5px/字符估算）
- [ ] 过长文字需要截断（_get_subtitle 自动截断到 ~120px）

## 4. 标题不遮挡

- [ ] 标题栏（title-block rect）y=10 到 y=62
- [ ] 所有渲染后的节点 y >= 72（标题底部 + 10px 间距）
- [ ] Region 框 y >= 72
- [ ] Region 标签 y >= 75

## 5. 区域框内文字不溢出

- [ ] AWS Region 框 x/y 应包含所有框内节点 + 至少 40px 边距
- [ ] Region 框不覆盖标题区域

## 6. 箭头完整性

- [ ] 所有 flowSteps 之间的 nextStepIds 连接都有对应箭头
- [ ] 如果有 actors，必须有 Clients → 第一个主流程系统的箭头
- [ ] 同系统自连接（source == target）应被过滤
- [ ] 箭头不穿过无关节点（使用 elbow routing）

## 7. 画布尺寸

- [ ] 画布宽度 >= 1000px（容纳主流程 + Clients + 辅助系统）
- [ ] 画布高度 >= 400px（容纳主流程 + 上方辅助 + 下方辅助）
- [ ] viewBox 正确包含所有元素

## 8. 布局逻辑

- [ ] 主流程系统在同一水平线（y=230），L→R 排列
- [ ] 辅助系统对齐到相关主系统列（如 Auth 在 API Gateway 上方列）
- [ ] Clients 节点在最左侧（x=80），与主流程水平对齐

## 9. 颜色完整性

- [ ] 所有节点 rect 的 fill 和 stroke 不为空字符串
- [ ] message_bus 类别有对应的颜色定义

## 10. 箭头路由

- [ ] 同列节点使用垂直箭头（bottom → top 或 top → bottom）
- [ ] 同行节点使用水平箭头（right edge → left edge）
- [ ] 跨行节点使用 elbow 路径（水平 → 垂直 → 水平）
- [ ] 不允许对角线直连

## 自动检查函数

`_check_layout_quality(layout, blueprint) -> list[str]` 返回质量问题列表。
空列表 = 通过所有检查。
