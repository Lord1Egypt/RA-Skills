# Draw.io XML Template

## 目录

- 基本原则
- 必备结构
- 分层容器规范
- 节点与连线规范
- 各图最小元素集
- 输出顺序
- 最小模板

## 基本原则

所有架构图默认输出为可直接导入 draw.io 的 XML 代码块。

- 不要输出伪 XML
- 不要省略根节点
- 不要把多个图混在同一个代码块里
- 即使是初稿，也必须保证 XML 可导入
- 不要用单条链路的流程图替代 4A 分层图

## 必备结构

每张图都至少包含：

- `<mxfile host="app.diagrams.net">`
- `<diagram name="图名称">`
- `<mxGraphModel>`
- `<root>`
- `<mxCell id="0"/>`
- `<mxCell id="1" parent="0"/>`

## 分层容器规范

主图必须包含 4 个容器节点，推荐使用 `swimlane` 或带标题的容器形状。

固定顺序：

1. 业务架构层
2. 应用架构层
3. 数据架构层
4. 技术架构层

要求：

- 容器必须覆盖整层元素
- 层标题必须可见
- 每层容器内至少放入 2 个业务对象
- 跨层映射线连接具体对象，不连接层标题本身

## 节点与连线规范

- 节点使用 `mxCell`，并设置 `vertex="1"`
- 连线使用 `mxCell`，并设置 `edge="1"`
- 节点必须有 `value`、`style`、`parent`
- 节点必须带 `mxGeometry`，至少包含 `x`、`y`、`width`、`height`
- 连线必须带 `source`、`target` 和相应 `mxGeometry`
- 同一张图内 id 不重复
- 图名固定使用：`主图`、`业务架构图`、`应用架构图`、`数据架构图`、`技术架构图`
- 主图中的连线默认表达“映射”而不是“时序”

## 各图最小元素集

- 主图：4 个层容器 + 每层至少 2 个元素 + 至少 2 条跨层映射线
- 业务架构图：角色、场景、能力、规则/KPI
- 应用架构图：渠道、应用、共享服务、外部系统
- 数据架构图：来源、核心数据、消费者、治理/所有权
- 技术架构图：接入、编排、执行/集成、安全/审计、基础设施

## 输出顺序

1. 主图
2. 业务架构图
3. 应用架构图
4. 数据架构图
5. 技术架构图

如果用户要求分阶段产出，就先交主图，后续每一轮追问只补新增或更新的分图。

## 最小模板

```xml
<mxfile host="app.diagrams.net">
  <diagram name="主图">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="layer-business" value="业务架构层" style="swimlane;rounded=0;html=1;fillColor=#fef6e7;strokeColor=#d6b656;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="1680" height="220" as="geometry"/>
        </mxCell>
        <mxCell id="layer-application" value="应用架构层" style="swimlane;rounded=0;html=1;fillColor=#edf7ed;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="300" width="1680" height="220" as="geometry"/>
        </mxCell>
        <mxCell id="layer-data" value="数据架构层" style="swimlane;rounded=0;html=1;fillColor=#eef3fc;strokeColor=#6c8ebf;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="560" width="1680" height="220" as="geometry"/>
        </mxCell>
        <mxCell id="layer-technology" value="技术架构层" style="swimlane;rounded=0;html=1;fillColor=#f3edf7;strokeColor=#9673a6;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="820" width="1680" height="220" as="geometry"/>
        </mxCell>
        <mxCell id="business-role" value="关键角色" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="120" y="120" width="140" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="business-capability" value="核心能力" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="380" y="120" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="application-app" value="核心应用" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="380" y="390" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="data-domain" value="核心数据域" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="380" y="650" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="technology-platform" value="技术支撑" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="380" y="910" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="map-ba-aa" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;" edge="1" parent="1" source="business-capability" target="application-app">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="map-aa-da" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;" edge="1" parent="1" source="application-app" target="data-domain">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="map-aa-ta" style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;" edge="1" parent="1" source="application-app" target="technology-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
