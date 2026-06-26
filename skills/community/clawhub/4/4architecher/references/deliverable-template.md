# Deliverable Template

按以下顺序输出，缺失信息用“假设”或“待确认”标记，不要留空白标题。

## 1. 背景与边界

- 产品名称：
- 建模目标：
- 范围边界：
- 目标用户：
- 当前阶段：

## 2. 已确认 / 假设 / 待确认

### 已确认

- 

### 假设

- 

### 待确认

- 

## 3. 主图 draw.io XML

使用 `xml` fenced code block 输出主图。主图必须是一张 4A 总览分层架构图，而不是流程图。

主图至少包含：

- 业务架构层容器
- 应用架构层容器
- 数据架构层容器
- 技术架构层容器
- 至少 2 条跨层映射关系

```xml
<mxfile host="app.diagrams.net">
  <diagram name="主图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 4. 4A 总览表

| 维度 | 核心内容 | 本次重点 |
| --- | --- | --- |
| 业务架构 |  |  |
| 应用架构 |  |  |
| 数据架构 |  |  |
| 技术架构 |  |  |

## 5. 业务架构图 draw.io XML

业务架构图至少包含：

- 关键角色
- 核心场景
- 业务能力域
- 关键规则 / KPI / 风险约束

```xml
<mxfile host="app.diagrams.net">
  <diagram name="业务架构图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 6. 应用架构图 draw.io XML

应用架构图至少包含：

- 渠道与入口
- 核心应用 / Skill
- 共享服务
- 外部系统
- 接口或边界关系

```xml
<mxfile host="app.diagrams.net">
  <diagram name="应用架构图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 7. 数据架构图 draw.io XML

数据架构图至少包含：

- 数据来源
- 数据域 / 主实体
- 数据消费者
- 数据流或所有权
- 治理约束

```xml
<mxfile host="app.diagrams.net">
  <diagram name="数据架构图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 8. 技术架构图 draw.io XML

技术架构图至少包含：

- 接入层
- 服务 / 编排层
- 执行 / 集成层
- 安全 / 审计 / 可观测性
- 基础设施或运行环境

```xml
<mxfile host="app.diagrams.net">
  <diagram name="技术架构图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## 9. 分层说明文档

### 业务架构

- 核心场景：
- 关键角色：
- 业务能力：
- 关键规则 / KPI：

### 应用架构

- 渠道与入口：
- 核心系统 / 模块：
- 系统边界：
- 外部依赖：

### 数据架构

- 数据域：
- 核心实体：
- 数据来源与消费者：
- 治理要求：

### 技术架构

- 部署与运行环境：
- 集成方式：
- 平台与中间件：
- 非功能设计：

## 10. 4A 映射矩阵

| 业务能力 | 承接应用 | 关键数据 | 技术支撑 | 关键约束 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 11. 外部资料校验记录

| 待验证主张 | 来源级别 | 来源名称 | 日期 | 支持结论 | 对架构的影响 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### 证据支持的结论

- 

### 基于经验的建议

- 

### 仍待确认

- 

## 12. 风险、缺口与建议

### 主要风险

- 

### 当前缺口

- 

### 下一步建议

- 
