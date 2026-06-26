# Family Bookkeeping Category System

Use this file for the canonical category tree and classification defaults.

## Default Principles

- Prefer a stable two-level hierarchy: `一级类型` / `二级类型`
- Keep `金额` positive; use `收支类型` to represent direction
- If uncertain, fall back to `其他 / 暂未分类`
- Treat refunds as `收入 / 退款` unless the user explicitly wants another convention

## Category Tree

### 餐饮
- 早饭
- 午饭
- 晚饭
- 外卖
- 饮料
- 咖啡
- 零食
- 聚餐

### 交通
- 打车
- 地铁
- 公交
- 火车
- 高铁
- 机票
- 加油
- 停车
- 过路费
- 共享单车

### 日用购物
- 买菜
- 超市
- 日用品
- 家居用品
- 清洁用品
- 母婴用品
- 宠物用品

### 居住
- 房租
- 水费
- 电费
- 燃气费
- 物业费
- 宽带
- 维修
- 家电

### 医疗健康
- 挂号
- 药品
- 检查
- 治疗
- 保健
- 运动

### 教育成长
- 学费
- 书籍
- 课程
- 培训
- 文具

### 娱乐休闲
- 电影
- 游戏
- KTV
- 演出
- 景点
- 旅游
- 酒店
- 兴趣消费

### 人情社交
- 红包
- 礼物
- 聚会
- 请客
- 孝敬父母
- 人情往来

### 服饰美妆
- 衣服
- 鞋包
- 配饰
- 护肤
- 彩妆
- 理发

### 孩子 / 家庭专项
- 奶粉
- 尿不湿
- 玩具
- 学习用品
- 家庭公共支出

### 金融支出
- 信用卡还款
- 手续费
- 利息支出
- 保险

### 收入
- 工资
- 奖金
- 报销
- 兼职
- 红包收入
- 转账收入
- 理财收益
- 退款
- 其他收入

### 其他
- 暂未分类
- 其他支出
- 其他收入

## Keyword Heuristics

Use these only as soft rules.

- `瑞幸` / `库迪` / `星巴克` → 餐饮 / 咖啡
- `美团外卖` / `饿了么` → 餐饮 / 外卖
- `滴滴` / `T3` → 交通 / 打车
- `12306` → 交通 / 高铁
- `航空` / `机票` / `携程机票` → 交通 / 机票
- `盒马` / `美团买菜` / `叮咚买菜` → 日用购物 / 买菜
- `京东` / `天猫超市` / `超市` → 日用购物 / 超市
- `退款` → 收入 / 退款

If confidence is low, avoid forced classification.
