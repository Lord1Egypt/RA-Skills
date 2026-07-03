---
name: flight-delay-compensation
display_name: 航班延误权益助手
description: 输入航班号自动查延误状态并计算权益金额，覆盖欧盟/英国/中国/加拿大/美国/土耳其6大法域，含权益申领指引和申领信生成，零配置即装即用。
tags: [航班延误, 延误赔偿, 航班取消, EU261, 旅客权益]
tools:
  - name: check
    description: 检查航班延误状态并评估权益资格，输入航班号自动查询延误信息并计算可获权益金额
    primaryEnv: PROXY_TOKEN
    env:
      - name: PROXY_TOKEN
        description: 代理认证Token（自动配置，无需手动设置）
        required: false
    parameters:
      - name: flight_no
        type: string
        description: 航班号，如 CA1507、MU5102
        required: true
      - name: date
        type: string
        description: 航班日期 YYYY-MM-DD，默认今天
        required: false
  - name: rules
    description: 查询各国航班延误权益规则，支持欧盟/英国/中国/加拿大/美国/土耳其
    parameters:
      - name: region
        type: string
        description: 地区代码：eu/uk/china/canada/us/turkey，不填显示全部
        required: false
  - name: claim
    description: 生成航班延误申领信模板，自动填入航班信息和适用法规
    parameters:
      - name: flight_no
        type: string
        description: 航班号
        required: true
      - name: date
        type: string
        description: 航班日期 YYYY-MM-DD，默认今天
        required: false
      - name: passenger_name
        type: string
        description: 旅客姓名
        required: false
---

# 航班延误权益助手 — 输入航班号，自动计算你能拿多少赔偿

> 基于飞常准实时数据，智能识别适用法域（EU261/UK261/中国/加拿大/土耳其/美国），计算权益金额并生成申领信。

🔥 **核心亮点：**
- **实时延误查询** — 输入航班号即查延误状态，自动计算出发/到达延误时长
- **6大法域覆盖** — 欧盟/英国/中国/加拿大/土耳其/美国权益规则全掌握
- **自动法域识别** — 根据航线自动判断适用哪个法规
- **申领信生成** — 自动填入航班信息和法规条款，可直接提交
- **零配置** — 装上就能用

## 快速入门

**3个开场白示例，复制即用：**

1. "CA1507航班延误了，能赔多少"
2. "EU261权益标准是多少"
3. "帮我生成CA1507的申领信"

## 核心能力

1. **延误检查** — 输入航班号实时查询延误状态
2. **权益评估** — 根据航线自动识别适用法域，计算权益金额
3. **规则查询** — 各国延误权益规则详情，含标准和免责条款
4. **申领信生成** — 自动生成可提交的申领信模板
5. **法域对比** — 6大法域的权益标准和适用条件对比
6. **EU261专项** — 到达延误≥3小时可获€250-600赔偿

## 能做什么

- 输入航班号实时查询延误状态
- 根据航线自动判断适用法域并计算权益金额
- 查询各国延误权益规则
- 生成航班延误申领信模板

## 不能做什么

- 不能自动提交申领（需用户自行向航司提交）
- 不能保证100%获赔（最终取决于航司审核）
- 不能查询历史航班（仅支持已起飞/当天航班）
- 中国航班无法定义务权益，仅提供航司自愿补偿标准参考

## 使用提示

- 中国国内航班延误4小时以上才可能获得补偿，且仅限非旅客/非天气原因
- EU261适用场景：从欧盟机场出发的任意航司，或欧盟航司抵达欧盟
- 申领最划算的方式是直接向航司官网提交，不要用第三方服务（抽成15-30%）
- 保留登机牌、延误证明是申领的关键证据
- 不可抗力（天气/罢工/安全风险）通常可免责

## 🔗 搭配使用

- **机票聪明买** — 机票查询和比价
- **出行保障助手** — 航班延误保险购买
- **出境游旅行助手** — 出境游全链路助手

## 数据流向

航班动态查询通过云端代理转发到飞常准API，代理服务不存储用户数据。
