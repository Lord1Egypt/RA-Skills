---
name: flight-delay-compensation
display_name: "航班延误赔偿助手"
description: "零配置即装即用，输入航班号自动查延误并计算赔偿金额，覆盖6大法域含索赔信生成，基于飞常准实时数据。"
tags: [航班延误, 延误赔偿, EU261, 航班取消, 索赔, 机场延误, flight delay, compensation, claim, refund]
tools:
  - name: check
    description: 检查航班延误状态并评估赔偿资格，输入航班号自动查询延误信息并计算可获赔偿金额
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
    description: 查询各国航班延误赔偿规则，支持欧盟/英国/中国/加拿大/美国/土耳其
    parameters:
      - name: region
        type: string
        description: 地区代码：eu/uk/china/canada/us/turkey，不填显示全部
        required: false
  - name: claim
    description: 生成航班延误索赔信模板，自动填入航班信息和适用法规
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

# 航班延误赔偿助手

输入航班号即可自动查询延误状态，根据出发地/目的地智能判断适用法域，计算赔偿金额并生成索赔信。覆盖全球6大赔偿法域。

## 能做什么

- **延误检查**：输入航班号实时查询延误状态，自动计算出发和到达延误时长
- **赔偿评估**：根据航线自动识别适用法域（EU261/UK261/中国/加拿大/土耳其/美国），计算可获赔偿金额
- **规则查询**：查看各国延误赔偿规则详情，含赔偿标准、免责条款
- **索赔信生成**：自动填入航班信息和适用法规，生成可直接使用的索赔信模板

## 不能做什么

- 不能自动提交索赔，需要用户自行向航司提交
- 不能保证100%获赔，最终结果取决于航司审核
- 不能查询历史航班（仅支持已起飞/当天航班）
- 中国航班无法定义务赔偿，仅提供航司自愿补偿标准参考

## 使用示例

1. "CA1507航班延误了，能赔多少"
2. "从巴黎飞北京的航班延误3小时能赔吗"
3. "EU261赔偿标准是多少"
4. "帮我生成CA1507的索赔信"
5. "各国航班延误赔偿规则对比"

## 注意事项

- 赔偿金额为估算参考，实际以航司和法规执行为准
- EU261/UK261赔偿条件为到达延误≥3小时，不是出发延误
- 不可抗力（天气/罢工/安全风险）通常可免责
- **数据流向**：航班动态查询通过云端代理转发到飞常准API，代理不存储用户数据

## 使用提示

- 中国国内航班延误4小时以上才可能获得补偿，且仅限非旅客/非天气原因
- EU261适用场景：从欧盟机场出发的任意航司航班，或欧盟航司抵达欧盟的航班
- 索赔最划算的方式是直接向航司官网提交，不要用第三方服务（抽成15-30%）
- 保留登机牌、延误证明是索赔的关键证据
- 英国脱欧后UK261与EU261基本一致，金额为英镑
