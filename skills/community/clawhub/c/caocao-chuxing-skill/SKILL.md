---
name: caocao-chuxing-skill
description: Use this skill for all 曹操出行 ride-hailing requests after the user installs the skill and provides an API key from https://mcp.caocaokeji.cn/console. Trigger when the user wants to call a ride, estimate fares, generate a ride link, create an order, query an ongoing order, or cancel an order through 曹操出行.
---

# 曹操出行 Skill

这个 skill 用来处理 **所有曹操出行打车相关需求**。

安装这个 skill 后，接入者只需要做一件事：

1. 打开 `https://mcp.caocaokeji.cn/console`
2. 获取自己的 **API Key**
3. 提供给 agent 完成配置

配置完成后，就可以直接用自然语言完成：
- 搜索上车点 / 目的地
- 查看车型和价格预估
- 生成打车链接
- 直接创建订单
- 查询订单状态
- 取消订单

## 什么时候用

当用户出现以下意图时，直接使用这个 skill：
- “帮我叫个曹操”
- “从 A 到 B 打车”
- “查一下曹操打车多少钱”
- “生成曹操打车链接”
- “直接下单一个最便宜的车型”
- “查一下司机多久到”
- “取消这个曹操订单”
- “安装 / 配置 曹操出行 skill”

## 首次配置

当用户给出 API Key 时，执行：

```bash
python3 <skill_dir>/scripts/caocao_mcp.py configure --api-key "<API_KEY>"
```

然后建议立刻做一个简单测试：

```bash
python3 <skill_dir>/scripts/caocao_mcp.py maps_text_poi --keywords "杭州东站" --city-name "杭州"
```

如果返回地点列表，说明已经可以正常使用。

## 推荐用法

### 1. 高层流程

优先使用高层命令：

#### 只估价
```bash
python3 <skill_dir>/scripts/caocao_mcp.py ride_flow --from-keywords "百度科技园" --to-keywords "北京西站" --city-name "北京" --action estimate
```

#### 生成打车链接
```bash
python3 <skill_dir>/scripts/caocao_mcp.py ride_flow --from-keywords "百度科技园" --to-keywords "北京西站" --city-name "北京" --action link
```

#### 直接下单（默认最便宜车型）
```bash
python3 <skill_dir>/scripts/caocao_mcp.py ride_flow --from-keywords "百度科技园" --to-keywords "百度大厦" --city-name "北京" --action create-order
```

#### 指定车型下单
```bash
python3 <skill_dir>/scripts/caocao_mcp.py ride_flow --from-keywords "百度科技园" --to-keywords "北京西站" --city-name "北京" --action create-order --service-type 3
```

### 2. 低层命令

需要精确控制时，再使用：
- `maps_text_poi`
- `trip_estimate`
- `trip_generate_ride_link`
- `trip_create_order`
- `trip_query_order`
- `trip_cancel_order`

## 对话策略

### 当用户说“从 A 到 B 打车”
默认顺序：
1. 搜起点
2. 搜终点
3. 做价格预估
4. 展示车型和价格

### 当用户说“生成打车链接”
优先走：
- `ride_flow --action link`

### 当用户说“直接下单最便宜的车型”
优先走：
- `ride_flow --action create-order`
- 不指定 `service-type`，默认选最便宜车型

## 输出要求

- 地址搜索：返回前 3 个最相关 POI，带名称和经纬度
- 价格预估：清楚列车型、价格、service_type
- 链接：直接给可点击链接
- 下单成功：明确给出订单号
- 查单：优先提炼司机、车牌、距离、预计到达时间
- 取消：明确反馈是否成功

## 注意事项

- 下单、取消都属于真实外部动作
- 如果用户语义不明确，先确认
- 如果用户明确要求直接下单，可以直接执行
