# Microservices Architecture Template

## 适用场景

用户描述包含：微服务、microservices、service mesh、Kubernetes、K8s、分布式服务等关键词。

## 布局结构

```
Clients → API Gateway → [Service A, Service B, Service C] → [DB A, DB B, Cache, MQ]
```

这些坐标只是起始参考，不是必须照抄的固定布局。如果服务或数据节点超出当前模板容量：
- 允许服务列或数据列拆成多行
- 允许增大画布和 cluster 边界
- 仍然拥挤时回退到 `freeflow`

不要把所有服务和数据卡片硬塞进同一行，造成牙膏式排版。

## 组件定义

| 组件 | 类别 | x | y | 宽 | 高 | 特征 |
|------|------|---|---|-----|-----|------|
| Clients | external | 80 | 280 | 140 | 80 | Web/Mobile |
| API Gateway | cloud | 310 | 280 | 150 | 80 | Routing, Auth |
| Service A | backend | 540 | 160 | 150 | 80 | 业务服务 |
| Service B | backend | 540 | 280 | 150 | 80 | 用户服务 |
| Service C | backend | 540 | 400 | 150 | 80 | 订单服务 |
| DB A | database | 780 | 160 | 140 | 80 | 业务数据 |
| DB B | database | 780 | 280 | 140 | 80 | 用户数据 |
| Cache | database | 780 | 400 | 140 | 44 | Redis/ElastiCache |
| MQ | message_bus | 780 | 500 | 140 | 44 | RabbitMQ/Kafka |

## 连接关系

| 从 | 到 | 方向 |
|----|----|------|
| Clients | API Gateway | 水平 → |
| API Gateway | Service A | 水平 → |
| API Gateway | Service B | 水平 → |
| API Gateway | Service C | 水平 → |
| Service A | DB A | 水平 → |
| Service B | DB B | 水平 → |
| Service C | Cache | 水平 → |
| Service C | MQ | 水平 → |

## K8s Cluster Region

- 虚线框：x=290, y=120, width=660, height=450, rx=16
- 描边：`#FBBF24`, `stroke-dasharray="8,4"`, `opacity="0.4"`
- 标签：`Kubernetes Cluster`（x=310, y=110）
- Clients 在 Cluster 框外左侧

## 图例与画布

- Legend 放在左下或底部保留区，不放右上角。
- 最终 SVG 高度必须包含最底部节点、legend、summary cards 和 footer。
- 不得用固定高度容器或裁切把底部内容截断。

## Summary Cards

### Gateway (琥珀色)
- API Gateway routing
- Authentication & authorization
- Rate limiting
- Load balancing

### Services (翠绿色)
- Microservice A/B/C
- Independent deployment
- Service discovery
- Health monitoring

### Data (紫色)
- Database per service
- Redis caching layer
- Message queue
- Event-driven communication
