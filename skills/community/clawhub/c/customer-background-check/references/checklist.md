# 客户背调三查速查表

## 一、公司名 OFAC 检索

- 网址：<https://sanctionssearch.ofac.treas.gov/>
- 输入：公司名关键词
- 通过标准：显示 `0 Found` 或 `Your search has not returned any results.`
- 风险标准：出现候选记录，需要人工复核名称、地址、类型、分数

## 二、注册地址 ECFR 检索

- 网址：<https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-744/appendix-Supplement%20No.%204%20to%20Part%20744>
- 操作：页面内查找地址关键词
- 通过标准：页面无匹配
- 风险标准：页面有匹配，需要截取上下文并人工复核

## 三、商务部协查出口数据

- 优先联系人：Dora
- 备选联系人：Shellen
- 目标：确认出口数据、出口国、是否涉及敏感国家

## 推荐关键词提取规则

### 公司名

1. 去掉 LLC、Ltd、Inc、Corp 等后缀
2. 保留品牌名、主识别词、区域词
3. 长名称先试 2 到 4 个核心词

### 地址

1. 先试门牌号 + 街道名
2. 再试街道名 + 城市
3. 再试邮编 + 城市
4. 必要时拆成多个关键词重试

## 建议结论用语

- 初筛未命中
- 疑似命中，需人工复核
- 信息不足，待补充
- 已起草协查消息，待发送
- 已发送协查请求，待回执
