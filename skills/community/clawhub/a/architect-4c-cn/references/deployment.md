# 部署图

在一个确定环境中，将逻辑容器的实例映射到部署节点，并说明通信路径。

## 画法

- 本例为拟议生产环境，包含入口负载均衡、两个 JVM 和一个数据库运行环境。
- 每个 JVM 运行一个支付应用实例，两者都映射到 L2 的支付应用。数据库实例映射到支付库。
- 渠道回调经过入口，应用向商家和渠道发出请求并访问数据库。
- 可用区、网络和故障切换按实际资料补充。托管位置与逻辑归属分开说明。

示例是虚构目标方案。图例中外层虚线框为部署环境，内层为运行节点，绿色为应用实例，紫色为数据实例，黄色为基础设施，灰色为外部系统，实线表示通信。

绘图与配色见共用的 [绘图与视觉规范](diagram-guidelines.md)。

## 完整模板

### 暗色

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: true, background: '#07111F', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif', fontSize: 15px,
      primaryColor: '#0B2B25', primaryTextColor: '#E6EDF3', primaryBorderColor: '#34D399', lineColor: '#B8C4D4',
      textColor: '#E6EDF3', secondaryColor: '#211532', tertiaryColor: '#101B2B', clusterBkg: '#101B2B', clusterBorder: '#66758A',
      edgeLabelBackground: '#07111F', actorBkg: '#101B2B', actorBorder: '#34D399', actorTextColor: '#E6EDF3', actorLineColor: '#66758A',
      signalColor: '#B8C4D4', signalTextColor: '#E6EDF3', labelBoxBkgColor: '#101B2B', labelBoxBorderColor: '#66758A',
      labelTextColor: '#E6EDF3', loopTextColor: '#E6EDF3', noteBkgColor: '#28220E', noteBorderColor: '#FACC15',
      noteTextColor: '#E6EDF3', activationBkgColor: '#0B2B25', activationBorderColor: '#34D399', sequenceNumberColor: '#07111F'}
  themeCSS: |
    .nodeLabel small { color: #9AA9BC; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #07111F; color: #9AA9BC; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart TB
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph Production["☁ 拟议生产环境"]
        direction TB
    Ingress("<b>入口负载均衡</b><br/><small>基础设施 | HTTPS</small>")
        subgraph NodeA["运行节点 A｜JVM"]
    AppA("<b>支付应用实例 A</b><br/><small>容器实例｜映射：支付应用</small>")
        end
        subgraph NodeB["运行节点 B｜JVM"]
    AppB("<b>支付应用实例 B</b><br/><small>容器实例｜映射：支付应用</small>")
        end
        subgraph NodeDB["数据库运行节点"]
    Database[("<b>支付库实例</b><br/><small>容器实例｜映射：支付库 | PostgreSQL</small>")]
        end
    Ingress -->|"路由 API 与回调 | HTTPS"| AppA
    Ingress -->|"路由 API 与回调 | HTTPS"| AppB
    AppA -->|"读写支付与任务 | SQL/TLS"| Database
    AppB -->|"读写支付与任务 | SQL/TLS"| Database
    end
    Merchant -->|"发起支付 | HTTPS"| Ingress
    Provider -->|"回传渠道结果 | HTTPS"| Ingress
    AppA -->|"扣款与查询 | HTTPS"| Provider
    AppB -->|"扣款与查询 | HTTPS"| Provider
    AppA -->|"通知支付结果 | HTTPS"| Merchant
    AppB -->|"通知支付结果 | HTTPS"| Merchant
    classDef external fill:#101B2B,stroke:#66758A,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef infra fill:#28220E,stroke:#FACC15,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Ingress infra
    classDef service fill:#0B2B25,stroke:#34D399,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class AppA,AppB service
    classDef data fill:#211532,stroke:#C084FC,color:#E6EDF3,stroke-width:1.2px,rx:8,ry:8
    class Database data
    style Production fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeA fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeB fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeDB fill:#081821,stroke:#34D399,color:#34D399,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

### 亮色

```mermaid
---
config:
  theme: "base"
  look: "classic"
  fontFamily: "\"PingFang SC\", \"Helvetica Neue\", Arial, sans-serif"
  flowchart: {nodeSpacing: 28, rankSpacing: 40, padding: 14, curve: basis}
  sequence: {mirrorActors: false, actorMargin: 42, messageMargin: 28, boxMargin: 10}
  themeVariables: {darkMode: false, background: '#F8FAFC', fontFamily: '"PingFang SC", "Helvetica Neue", Arial, sans-serif',
      fontSize: 15px, primaryColor: '#ECFDF5', primaryTextColor: '#142238', primaryBorderColor: '#047857', lineColor: '#52657D',
      textColor: '#142238', secondaryColor: '#FAF5FF', tertiaryColor: '#F1F5F9', clusterBkg: '#F1F5F9', clusterBorder: '#8090A4',
      edgeLabelBackground: '#F8FAFC', actorBkg: '#F1F5F9', actorBorder: '#047857', actorTextColor: '#142238', actorLineColor: '#8090A4',
      signalColor: '#52657D', signalTextColor: '#142238', labelBoxBkgColor: '#F1F5F9', labelBoxBorderColor: '#8090A4',
      labelTextColor: '#142238', loopTextColor: '#142238', noteBkgColor: '#FFFBEB', noteBorderColor: '#92400E',
      noteTextColor: '#142238', activationBkgColor: '#ECFDF5', activationBorderColor: '#047857', sequenceNumberColor: '#F8FAFC'}
  themeCSS: |
    .nodeLabel small { color: #53647A; font-size: 12px; }
    .nodeLabel b { font-weight: 600; }
    .cluster-label { font-weight: 600; }
    .edgeLabel { background-color: #F8FAFC; color: #53647A; }
    .cluster rect { rx: 10; ry: 10; }
    .actor { rx: 8; ry: 8; }
---
flowchart TB
    Merchant("<b>商家订单系统</b><br/><small>外部软件系统<br/>管理订单与接收支付结果</small>")
    Provider("<b>支付渠道</b><br/><small>外部软件系统<br/>执行扣款与确认结果</small>")
    subgraph Production["☁ 拟议生产环境"]
        direction TB
    Ingress("<b>入口负载均衡</b><br/><small>基础设施 | HTTPS</small>")
        subgraph NodeA["运行节点 A｜JVM"]
    AppA("<b>支付应用实例 A</b><br/><small>容器实例｜映射：支付应用</small>")
        end
        subgraph NodeB["运行节点 B｜JVM"]
    AppB("<b>支付应用实例 B</b><br/><small>容器实例｜映射：支付应用</small>")
        end
        subgraph NodeDB["数据库运行节点"]
    Database[("<b>支付库实例</b><br/><small>容器实例｜映射：支付库 | PostgreSQL</small>")]
        end
    Ingress -->|"路由 API 与回调 | HTTPS"| AppA
    Ingress -->|"路由 API 与回调 | HTTPS"| AppB
    AppA -->|"读写支付与任务 | SQL/TLS"| Database
    AppB -->|"读写支付与任务 | SQL/TLS"| Database
    end
    Merchant -->|"发起支付 | HTTPS"| Ingress
    Provider -->|"回传渠道结果 | HTTPS"| Ingress
    AppA -->|"扣款与查询 | HTTPS"| Provider
    AppB -->|"扣款与查询 | HTTPS"| Provider
    AppA -->|"通知支付结果 | HTTPS"| Merchant
    AppB -->|"通知支付结果 | HTTPS"| Merchant
    classDef external fill:#F1F5F9,stroke:#8090A4,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Merchant,Provider external
    classDef infra fill:#FFFBEB,stroke:#A16207,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Ingress infra
    classDef service fill:#ECFDF5,stroke:#047857,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class AppA,AppB service
    classDef data fill:#FAF5FF,stroke:#7E22CE,color:#142238,stroke-width:1.2px,rx:8,ry:8
    class Database data
    style Production fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeA fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeB fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
    style NodeDB fill:#F5FBFA,stroke:#047857,color:#047857,stroke-width:1px,stroke-dasharray:4 3,rx:10,ry:10
```

两个应用实例都包含后台任务，任务领取需要租约或等价并发控制，并处理重复投递。单数据库示例没有声明自动切换或高可用。

## 检查

- 确认环境、实例数和运行位置有依据或属于明确的目标设计，每个实例能映射回 L2 容器。
- 核对入口、回调、出站和数据库路径，以及多实例任务协调、状态一致性与故障恢复。

定义见 [C4 部署图](https://c4model.com/diagrams/deployment)。
