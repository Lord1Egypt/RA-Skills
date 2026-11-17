# 动态交互图

选择一个场景，说明静态模型中的对象如何在运行时协作。

## 画法

- 本例使用 L2 容器和外部系统。需要内部细节时另画 L3 时序，避免把容器与其组件列为同级参与者。
- 用 `sequenceDiagram` 表达顺序和条件，交互需有结构关系支持。
- 区分请求已受理、支付已终结和商家已确认接收。超时表示结果不确定。

示例是发起支付与结果通知的虚构目标方案。图例中实线箭头是请求，虚线箭头是响应，Note 是约束。

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
sequenceDiagram
    autonumber
    participant Merchant as 商家订单系统<br/>外部系统
    participant PayApp as 支付应用<br/>应用容器
    participant PayDB as 支付库<br/>数据容器
    participant Provider as 支付渠道<br/>外部系统
    Merchant->>PayApp: 发起支付，携带商家订单键
    PayApp->>PayDB: 按唯一订单键受理或读取原支付
    PayDB-->>PayApp: 原支付或新建的待确认记录
    alt 重复请求
        PayApp-->>Merchant: 返回原支付标识与状态
    else 首次受理
        PayApp->>Provider: 请求扣款，复用稳定幂等标识
        alt 已取得可验证的终态
            Provider-->>PayApp: 支付结果与凭证
            Note over PayApp: 验证渠道结果，应用状态规则
            PayApp->>PayDB: 原子提交终态与通知任务
            PayApp-->>Merchant: 返回支付标识与终态
        else 超时或结果不确定
            Note over PayApp,Provider: 后台查询或已验证回调核实结果<br/>在终态前保持待确认，按策略限次处理
            PayApp-->>Merchant: 返回支付标识与待确认状态
        end
    end
    opt 存在终态通知任务，包括后来核实的结果
        Note over PayApp,PayDB: 后来核实为终态时同样原子保存状态与任务
        PayApp->>PayDB: 领取通知任务并建立处理租约
        PayDB-->>PayApp: 通知事件与稳定事件标识
        PayApp->>Merchant: 签名结果通知，商家按事件标识去重
        alt 商家确认接收
            Merchant-->>PayApp: 确认
            PayApp->>PayDB: 标记任务完成
        else 未确认或超时
            PayApp->>PayDB: 记录失败与下次投递时间
            Note over PayApp: 退避重试，达到边界后告警或人工处理
        end
    end
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
sequenceDiagram
    autonumber
    participant Merchant as 商家订单系统<br/>外部系统
    participant PayApp as 支付应用<br/>应用容器
    participant PayDB as 支付库<br/>数据容器
    participant Provider as 支付渠道<br/>外部系统
    Merchant->>PayApp: 发起支付，携带商家订单键
    PayApp->>PayDB: 按唯一订单键受理或读取原支付
    PayDB-->>PayApp: 原支付或新建的待确认记录
    alt 重复请求
        PayApp-->>Merchant: 返回原支付标识与状态
    else 首次受理
        PayApp->>Provider: 请求扣款，复用稳定幂等标识
        alt 已取得可验证的终态
            Provider-->>PayApp: 支付结果与凭证
            Note over PayApp: 验证渠道结果，应用状态规则
            PayApp->>PayDB: 原子提交终态与通知任务
            PayApp-->>Merchant: 返回支付标识与终态
        else 超时或结果不确定
            Note over PayApp,Provider: 后台查询或已验证回调核实结果<br/>在终态前保持待确认，按策略限次处理
            PayApp-->>Merchant: 返回支付标识与待确认状态
        end
    end
    opt 存在终态通知任务，包括后来核实的结果
        Note over PayApp,PayDB: 后来核实为终态时同样原子保存状态与任务
        PayApp->>PayDB: 领取通知任务并建立处理租约
        PayDB-->>PayApp: 通知事件与稳定事件标识
        PayApp->>Merchant: 签名结果通知，商家按事件标识去重
        alt 商家确认接收
            Merchant-->>PayApp: 确认
            PayApp->>PayDB: 标记任务完成
        else 未确认或超时
            PayApp->>PayDB: 记录失败与下次投递时间
            Note over PayApp: 退避重试，达到边界后告警或人工处理
        end
    end
```

同一商家订单键复用原支付记录，渠道请求复用稳定幂等标识。后台任务或已验证回调核实结果，终态与通知任务原子保存。通知按至少一次投递设计，商家按事件标识去重。重试采用退避并设次数或时间边界，超限后告警或人工处理。

## 检查

- 确认交互能映射回结构，状态变更与异常处理有负责者。
- 核对重复请求、回调与投递的幂等策略，以及不确定结果和重试的结束条件。

定义见 [C4 动态图](https://c4model.com/diagrams/dynamic)。
