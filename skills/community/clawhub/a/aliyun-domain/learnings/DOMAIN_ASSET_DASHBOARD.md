# 📊 域名资产评估仪表盘功能说明

**版本**: v1.9.0  
**日期**: 2026-03-15  
**功能**: 一键生成域名资产总览/到期分布/价值统计/资产建议

---

## 📋 功能说明

### 问题背景

域名投资者通常持有多个域名，面临以下管理痛点：

1. **资产不清**：不知道账号下有多少域名，总价值多少
2. **到期混乱**：难以掌握哪些域名即将到期，容易过期损失
3. **价值不明**：不清楚哪些域名是高价值资产，哪些应该放弃
4. **决策困难**：缺乏数据支持，难以做出续费/出售/开发的决策

### 解决方案

**域名资产评估仪表盘** - 一键生成全面的域名资产分析报告

- 📊 **资产总览**：域名总数、总价值、市场估值、续费成本
- ⏰ **到期分布**：按紧急程度分类，快速识别风险
- 🌐 **后缀分布**：了解资产构成，优化后缀策略
- 💎 **价值分布**：识别高价值资产，重点保护
- 💡 **资产建议**：AI 生成针对性建议，辅助决策

---

## 🎯 功能特性

### 1. 资产总览

| 指标 | 说明 |
|:---|:---|
| 域名总数 | 账号下所有域名数量 |
| 评估总价值 | 基于注册成本的资产评估 |
| 市场估值 | 参考成交价的市值估算 |
| 年续费成本 | 所有域名一年的续费总成本 |
| 平均单个价值 | 域名平均价值 |

### 2. 到期分布

| 状态 | 说明 | 颜色 |
|:---|:---|:---|
| 🚨 已过期 | 域名已过期 | 红色 |
| ⚠️ 7 天内 | 7 天内到期 | 橙色 |
| 📅 30 天内 | 30 天内到期 | 黄色 |
| ✅ 90 天内 | 90 天内到期 | 蓝色 |
| 🛡️ 安全 | 90 天以上到期 | 绿色 |

### 3. 后缀分布

统计各后缀的域名数量和占比，帮助了解资产构成。

**示例**:
```
.cn         3 个 ( 33.3%) ██████
.xin        2 个 ( 22.2%) ████
.com        1 个 ( 11.1%) ██
.xyz        1 个 ( 11.1%) ██
```

### 4. 价值分布

| 价值区间 | 说明 |
|:---|:---|
| >5000 | 高价值域名 |
| 1000-5000 | 中等价值域名 |
| 500-1000 | 一般价值域名 |
| 100-500 | 基础价值域名 |
| <100 | 低价域名 |

### 5. 高价值域名 TOP 10

按市场估值排序，展示前 10 个高价值域名。

| 排名 | 域名 | 后缀 | 估值 | 到期状态 |
|:---:|:---|:---:|:---:|:---|
| 1 | claweat.com | .com | ¥9,000 | 🛡️ 安全 |
| 2 | claw88.cn | .cn | ¥8,100 | 🛡️ 安全 |
| 3 | linkgo.xin | .xin | ¥7,800 | 🚨 过期 |

### 6. 资产建议

AI 根据资产状况生成针对性建议：

| 建议类型 | 说明 | 优先级 |
|:---|:---|:---:|
| 🚨 紧急 | 域名已过期或即将到期 | P0 |
| ⚠️ 警告 | 域名 30 天内到期 | P1 |
| 💎 机会 | 高价值域名识别 | P2 |
| 💰 成本 | 续费成本优化建议 | P3 |
| 💡 建议 | 资产配置优化建议 | P4 |

---

## 🔧 技术实现

### 价值评估模型

```python
# 1. 基础价值（后缀）
SUFFIX_VALUE = {
    'com': 90, 'cn': 38, 'net': 90, 'xyz': 7,
    'io': 380, 'ai': 800, 'tv': 300, ...
}

# 2. 长度系数
LENGTH_MULTIPLIER = {
    1: 1000,  # 单字母
    2: 500,   # 双字母
    3: 200,   # 三字母
    4: 100,   # 四字母
    5: 50,    # 五字母
    6: 20,    # 六字母
    ...
}

# 3. 关键词价值
KEYWORD_VALUE = {
    'ai': 500, 'bot': 300, 'tech': 200,
    'cloud': 200, 'data': 200, ...
}

# 4. 数字价值
if name.isdigit():
    if len(name) <= 3:
        number_bonus = 10000
    elif len(name) <= 4:
        number_bonus = 1000
    ...

# 5. 总价值计算
total_value = (base_value * length_mult) + keyword_bonus + number_bonus
market_value = total_value * 10  # 市场估值
```

### 到期分析

```python
# 1. 获取域名详情
info = client.query_domain_detail(domain_name)
exp_date = info['ExpirationDate']

# 2. 计算剩余天数
days_left = (exp_datetime - datetime.now()).days

# 3. 判断状态
if days_left < 0:
    status = 'expired'
elif days_left <= 7:
    status = 'urgent'
elif days_left <= 30:
    status = 'warning'
elif days_left <= 90:
    status = 'normal'
else:
    status = 'safe'
```

### 资产建议生成

```python
def _generate_recommendations(assessment):
    recommendations = []
    
    # 到期建议
    if exp_dist.get('expired', 0) > 0:
        recommendations.append({
            'type': 'urgent',
            'title': '🚨 紧急：有域名已过期',
            'description': f"发现 {exp_dist['expired']} 个域名已过期",
            'action': '立即续费或赎回'
        })
    
    # 价值建议
    high_value = value_dist.get('>5000', 0) + value_dist.get('1000-5000', 0)
    if high_value > 0:
        recommendations.append({
            'type': 'opportunity',
            'title': '💎 高价值域名',
            'description': f"发现 {high_value} 个高价值域名",
            'action': '重点保护，考虑出售或开发'
        })
    
    return recommendations
```

---

## 📊 输出示例

```
================================================================================
🦐 域小虾 - 域名资产评估仪表盘
================================================================================
生成时间：2026-03-15 11:35:36

📊 资产总览
--------------------------------------------------------------------------------
  域名总数：     9 个
  评估总价值：   ¥2,738 元（注册成本）
  市场估值：     ¥27,375 元（参考成交价）
  年续费成本：   ¥329 元
  平均单个价值：¥304 元

⏰ 到期分布
--------------------------------------------------------------------------------
  🚨 已过期          4 个 ████
  🛡️ 安全          5 个 █████

🌐 后缀分布
--------------------------------------------------------------------------------
  .cn         3 个 ( 33.3%) ██████
  .xin        2 个 ( 22.2%) ████
  .com        1 个 ( 11.1%) ██
  .xyz        1 个 ( 11.1%) ██

💎 价值分布
--------------------------------------------------------------------------------
  >5000          3 个 ( 33.3%) ██████
  500-1000       3 个 ( 33.3%) ██████
  100-500        3 个 ( 33.3%) ██████

🏆 高价值域名 TOP 10
--------------------------------------------------------------------------------
排名     域名                             后缀       估值           到期状态        
--------------------------------------------------------------------------------
1      claweat.com                    .com     ¥   9,000 🛡️ 安全       
2      claw88.cn                      .cn      ¥   8,100 🛡️ 安全       
3      linkgo.xin                     .xin     ¥   7,800 🚨 过期        

💡 资产建议
--------------------------------------------------------------------------------
  🚨 紧急：有域名已过期
    发现 4 个域名已过期，需立即处理！
    建议：立即续费或赎回

  💎 高价值域名
    发现 3 个高价值域名（估值>1000 元）
    建议：重点保护，考虑出售或开发

  💡 建议增加.com 域名
    .com 域名仅 1 个，占比偏低
    建议：考虑注册核心品牌的.com 后缀

🔗 快速操作
--------------------------------------------------------------------------------
  1. 续费到期域名：https://domain.console.aliyun.com/renew
  2. 域名管理控制台：https://domain.console.aliyun.com
  3. 域名交易：https://jiyi.aliyun.com

================================================================================
📄 评估报告已保存：domain_assessment.json
```

---

## 🎯 使用方式

### 命令行

```bash
# 运行仪表盘
python3 scripts/domain_asset_dashboard.py

# 查看生成的报告
cat reports/domain_assessment.json
```

### Python 代码

```python
from domain_asset_dashboard import DomainAssetDashboard

# 创建仪表盘
dashboard = DomainAssetDashboard()

# 获取域名
dashboard.fetch_domains()

# 生成评估
dashboard.generate_assessment()

# 打印仪表盘
dashboard.print_dashboard()

# 获取评估数据
assessment = dashboard.assessment
print(f"域名总数：{assessment['summary']['total_domains']}")
print(f"市场估值：¥{assessment['summary']['total_market_value']}")
```

### 对话触发

```
用户：帮我看看账号下的域名资产情况

AI: 🦐 正在生成域名资产评估仪表盘...
    📊 资产总览
    域名总数：9 个
    市场估值：¥27,375 元
    ...
```

---

## 💡 应用场景

### 场景 1: 定期资产盘点

**频率**: 每月一次

**目的**: 了解资产状况，发现潜在风险

**操作**:
```bash
python3 scripts/domain_asset_dashboard.py
```

**输出**: 完整的资产报告 + JSON 数据

### 场景 2: 到期风险排查

**频率**: 每周一次

**目的**: 避免域名过期损失

**操作**:
```python
dashboard = DomainAssetDashboard()
dashboard.fetch_domains()
assessment = dashboard.generate_assessment()

# 查看到期分布
expired = assessment['expiration_distribution'].get('expired', 0)
urgent = assessment['expiration_distribution'].get('urgent', 0)

if expired + urgent > 0:
    print(f"⚠️ 发现 {expired + urgent} 个域名需要立即处理")
```

### 场景 3: 高价值域名识别

**频率**: 每季度一次

**目的**: 识别核心资产，重点保护

**操作**:
```python
# 获取高价值域名
high_value_domains = [
    d for d in assessment['domains']
    if d['value'].get('market_value', 0) > 1000
]

print(f"💎 发现 {len(high_value_domains)} 个高价值域名")
for d in high_value_domains:
    print(f"  - {d['domain_name']}: ¥{d['value']['market_value']}")
```

### 场景 4: 续费预算规划

**频率**: 每年一次

**目的**: 规划续费预算，优化成本

**操作**:
```python
summary = assessment['summary']
print(f"年续费成本：¥{summary['total_renewal_cost']}")
print(f"平均单个：¥{summary['total_renewal_cost'] / summary['total_domains']}")

# 识别可放弃的域名
low_value = [
    d for d in assessment['domains']
    if d['value'].get('market_value', 0) < 100
]
print(f"可考虑放弃：{len(low_value)} 个域名")
```

---

## 📈 价值评估方法论

### 评估维度

| 维度 | 权重 | 说明 |
|:---|:---:|:---|
| 后缀价值 | 30% | .com/.cn 等主流后缀价值高 |
| 长度 | 25% | 越短越有价值 |
| 关键词 | 20% | 含热门关键词（AI/tech 等） |
| 数字 | 15% | 纯数字或吉利数字 |
| 含义 | 10% | 有明确含义或品牌感 |

### 市场估值参考

| 类型 | 估值倍数 | 说明 |
|:---|:---:|:---|
| 普通域名 | 10x | 注册成本的 10 倍 |
| 短域名（≤6 字母） | 50-100x | 稀缺资源 |
| 关键词域名 | 20-50x | 有明确用途 |
| 数字域名 | 50-200x | 国人偏好 |
| 品牌域名 | 100-1000x | 有终端意向 |

---

## ⚠️ 注意事项

### 1. 估值仅供参考

- 估值基于算法模型，非实际成交价
- 实际价值受市场供需、终端意向等影响
- 建议结合 NameBio 等成交数据参考

### 2. 及时更新数据

- 域名状态可能随时变化
- 建议定期（每周）运行仪表盘
- 重要决策前重新生成报告

### 3. 综合决策

- 不要仅依赖估值做决策
- 结合行业趋势、个人战略综合考虑
- 高价值域名建议重点保护

---

## 📚 相关文件

| 文件 | 说明 |
|:---|:---|
| `scripts/domain_asset_dashboard.py` | 仪表盘主脚本 |
| `scripts/aliyun_domain.py` | 阿里云域名 API 客户端 |
| `reports/domain_assessment.json` | 生成的评估报告 |
| `SKILL.md` | 技能说明文档（v1.9.0） |

---

## 🚀 未来优化

1. **更精准的估值模型**
   - 整合 NameBio 成交数据
   - 机器学习模型训练
   - 考虑历史成交价

2. **更多评估维度**
   - SEO 权重（收录、外链）
   - 流量数据（如有解析）
   - 品牌匹配度

3. **可视化增强**
   - Web 界面展示
   - 图表更丰富（饼图、柱状图）
   - 导出 PDF 报告

4. **智能建议**
   - 自动续费建议
   - 出售时机建议
   - 开发方向建议

---

**维护者**: 神月 🦐  
**最后更新**: 2026-03-15  
**技能版本**: v1.9.0
