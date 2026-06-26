# 抖音本地生活餐饮运营专家 Agent

> 专为餐饮商家打造的抖音本地生活运营 Agent，覆盖从开店诊断到爆款打造的完整运营链路。

## 快速开始

### 安装依赖

```bash
pip install pyyaml pandas openpyxl jinja2 markdown
```

### 基本使用

```bash
# 店铺诊断
python3 scripts/douyin_tool.py diagnose --type hotpot --city "深圳"

# 爆款菜品打造
python3 scripts/douyin_tool.py dish --name "招牌酸菜鱼" --price 88 --selling-points "活鱼现杀,酸爽开胃,分量足"

# 团购方案设计
python3 scripts/douyin_tool.py groupon --restaurant-type hotpot --avg-ticket 120

# 内容运营策略
python3 scripts/douyin_tool.py content --restaurant "我的火锅店" --focus "酸菜鱼,毛肚,虾滑" --days 7

# 数据分析
python3 scripts/douyin_tool.py analyze

# 客服话术生成
python3 scripts/douyin_tool.py script --scenario "差评回复"
```

## 核心能力

### 1. 店铺诊断

针对新店冷启动或老店增长瓶颈，提供系统化诊断：

- 行业对标分析
- 冷启动优先级清单
- 预估起号周期
- 分阶段运营建议

### 2. 爆款菜品打造

从菜品定位到视频脚本，全链路爆款打造：

- 菜品定位（引流款/利润款/形象款）
- 定价梯度设计
- 视频拍摄脚本（3个角度）
- 文案话术库

### 3. 团购方案设计

科学的套餐组合与定价策略：

- 引流款/主推款/利润款/爆款梯度
- 毛利率测算
- 适用场景匹配
- 价格心理学应用

### 4. 内容运营策略

7天内容日历与脚本模板：

- 每日发布主题规划
- 最佳发布时间建议
- DOU+投放策略
- 热点蹭流建议

### 5. 数据分析

核心指标漏斗分析：

- 曝光→点击→下单→核销→复购
- 同城排名对标
- 爆款视频识别
- 优化建议

### 6. 客服话术

场景化话术库：

- 差评回复
- 私聊转化
- 复购引导

## 配置说明

### 用户配置

编辑 `config/user_config.yaml`，填写您的餐厅信息：

```yaml
restaurant:
  name: "我的火锅店"
  type: "hotpot"
  city: "深圳"
  avg_ticket: 120
  signature_dishes:
    - "招牌酸菜鱼"
    - "鲜毛肚"
```

### 行业配置

`config/industry_config.yaml` 包含各餐饮类型的运营要点，无需修改。

## 支持的餐饮类型

| 类型 | 代码 | 特点 |
|------|------|------|
| 火锅 | hotpot | 多人套餐为主 |
| 烧烤 | bbq | 夜宵时段+酒水 |
| 川菜 | sichuan | 单人+多人双轨 |
| 日料 | japanese | 套餐制、午市特价 |
| 茶饮 | tea | 第二杯半价、月卡 |
| 甜品 | dessert | 下午茶套餐 |

## 注意事项

1. **数据安全**：不存储用户抖音账号密码，仅使用官方API授权
2. **合规提醒**：所有团购方案需符合抖音本地生活平台规则
3. **效果预估**：所有预估数据基于行业平均值，实际效果因店而异
4. **更新频率**：行业知识库每月更新一次

## 更新日志

- **v1.0.0** (2026-04-27) — 初始版本
