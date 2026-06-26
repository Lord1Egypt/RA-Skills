# 百度电商一站式技能包

百度电商一站式服务，覆盖商品知识查询和购物交易全流程。支持商品对比、品牌知识、品类选购指南、商品参数解读、品牌榜单及单品榜单等知识查询能力；同时提供商品搜索、规格查看、地址管理、下单购买、订单查询及售后服务等完整交易链路，帮助用户从决策到购买一步到位。

## 功能特性

### 电商知识

- **商品对比** — 参数/口碑/价格全方位对比（仅支持两个商品对比）
- **品牌知识** — 品牌简介/定位/明星产品/大事记
- **品类知识** — 品类选购要点/避坑指南
- **商品参数** — 单品规格参数及 AI 解读
- **品牌榜单** — 某品类下的品牌排行
- **单品榜单** — 某品牌下的商品排行

### 百度优选（交易链路）

- **商品搜索** — 搜索可直接下单的商品
- **商品详情** — 获取 SKU 规格及价格
- **创建订单 / 订单历史 / 订单详情** — 完整订单管理
- **售后查询** — 查询订单售后信息
- **地址管理** — 地址列表 / 地址识别 / 地址添加

## 安装要求

- Python 3.x（使用标准库，无需额外安装依赖）
- 百度电商 API Token

## 配置

1. 访问 https://openai.baidu.com 并登录百度账号
2. 点击权限申请，勾选需要的能力
3. 设置环境变量：

```bash
export BAIDU_EC_SEARCH_TOKEN="your-token"
export BAIDU_EC_SEARCH_QPS="1"  # 可选，默认1，设为0无限制
```

## 目录结构

```
baidu-ecommerce-search/
├── SKILL.md              # 技能详细说明
├── README.md             # 本文件
└── scripts/
    ├── common.py         # 公共模块（API 请求、Token 管理）
    ├── lock.py           # QPS 限流锁
    ├── compare.py        # 商品对比
    ├── knowledge.py      # 品牌/品类/商品参数知识
    ├── ranking.py        # 品牌榜单 / 单品榜单
    ├── spu.py            # 百度优选商品搜索与详情
    ├── order.py          # 订单创建 / 历史 / 详情
    ├── address.py        # 地址列表 / 识别 / 添加
    └── after_service.py  # 售后查询
```

## 使用示例

### 电商知识

```bash
# 商品对比
python3 scripts/compare.py "iPhone17和iPhone16对比"

# 品牌知识
python3 scripts/knowledge.py brand "华为"

# 品类选购知识
python3 scripts/knowledge.py entity "无人机怎么选"

# 商品参数
python3 scripts/knowledge.py param "iPhone16"

# 品牌榜单
python3 scripts/ranking.py brand "手机排行榜"

# 单品榜单
python3 scripts/ranking.py product "苹果手机排行榜"
```

### 百度优选（交易）

```bash
# 商品搜索
python3 scripts/spu.py list "机械键盘"

# 商品详情
python3 scripts/spu.py detail <spuId>

# 创建订单
python3 scripts/order.py create --sku-id <skuId> --spu-id <spuId> --addr-id <addrId>

# 订单历史
python3 scripts/order.py history

# 订单详情
python3 scripts/order.py detail <orderId>

# 售后查询
python3 scripts/after_service.py <orderId>

# 地址列表
python3 scripts/address.py list

# 地址识别
python3 scripts/address.py recognise "张三 北京市海淀区中关村大街1号 13800138000"

# 地址添加
python3 scripts/address.py add <recogniseId>
```

## 许可证

MIT License
