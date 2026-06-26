---
name: dev-var-name
description: 程序员变量名生成器。将中文（或英文）关键词转换为多种编程命名风格。支持 7 种全称风格：驼峰、下划线蛇形、帕斯卡、全大写、短横线、点分隔符(dot.case)、路径分隔符(path/case)，以及对应的缩写版本。触发场景：用户输入中文或英文关键词，要求生成变量名、函数名、API 命名等。
---

# 程序员变量名生成器

## 核心规则

**输入**：用户提供的关键词（中文或英文）
**输出格式**（固定，不可更改）：

```
全称：驼峰：xxx；蛇形：xxx；帕斯卡：Xxx；全大写：XXX；短横线：xxx；点分隔：xxx；路径分隔：xxx
缩写：驼峰：xxx；蛇形：xxx；帕斯卡：Xxx；全大写：XXX；短横线：xxx；点分隔：xxx；路径分隔：xxx
```

### 七种命名风格

| 风格 | 英文名 | 示例 |
|------|--------|------|
| 驼峰 | camelCase | userAvatar |
| 蛇形 | snake_case | user_avatar |
| 帕斯卡 | PascalCase | UserAvatar |
| 全大写 | SCREAMING_SNAKE | USER_AVATAR |
| 短横线 | kebab-case | user-avatar |
| 点分隔 | dot.case | user.avatar |
| 路径分隔 | path/case | user/avatar |

## 缩写规则

| 原文 | 缩写 | 原文 | 缩写 |
|------|------|------|------|
| 小数 | dec | 整数 | int |
| 数字 | num | 字符串 | str |
| 布尔 | bool | 数组 | arr |
| 长度 | len | 大小 | sz |
| 数量 | cnt | 颜色 | clr |
| 配置 | cfg | 数据 | data/dat |
| 列表 | lst | 字典 | dict |
| 消息 | msg | 错误 | err |
| 成功 | suc | 状态 | sta/st |
| 用户 | user/usr | 认证 | auth |
| 登录 | login/lgn | 注册 | reg |
| 密码 | pwd | 邮箱 | mail |
| 头像 | avatar/avt | 搜索 | search/srch |
| 分页 | page/pg | 限制 | limit/lmt |
| 偏移 | offset/off | 排序 | sort/srt |
| 过滤 | filter/ft | 时间 | time/tm |
| 创建 | create/cr | 更新 | update/upd |
| 删除 | del | 复制 | copy/cp |
| 移动 | mv | 重命名 | rn |
| 路径 | path/pth | 文件 | file/fl |
| 目录 | dir | 链接 | link/lnk |
| 图片 | img | 视频 | vid |
| 音频 | aud | 文档 | doc |
| 表格 | tbl | 列 | col |
| 行 | row | 主键 | pk |
| 外键 | fk | 索引 | idx |
| 标识 | id | 名称 | name/nm |
| 类型 | type/typ | 描述 | desc |
| 备注 | remark/rmk | 版本 | ver |
| 日期 | date/dt | 时间戳 | ts |
| 金额 | amt | 价格 | price/prc |
| 折扣 | disc | 税率 | tax |
| 订单 | order/ord | 支付 | pay |
| 物流 | ship | 退款 | ref |
| 评论 | review/rvw | 评分 | rate |
| 收藏 | fav | 分享 | share/shr |
| 推荐 | rec | 热门 | hot |
| 最新 | latest/lst | 统计 | stat |
| 图表 | chart/cht | 模板 | tpl |
| 主题 | theme/thm | 语言 | lang |
| 区域 | region/rgn | 接口 | api |

> 未在上表中的词汇，按以下原则取前 3~4 个辅音字母：保留首个字母 + 取后续辅音（bcdfghjklmnpqrstvwxyz），不足3个时取全部辅音。

## 示例

**输入**：小数

**输出**：
全称：驼峰：decimal；蛇形：decimal；帕斯卡：Decimal；全大写：DECIMAL；短横线：decimal；点分隔：decimal；路径分隔：decimal
缩写：驼峰：dec；蛇形：dec；帕斯卡：Dec；全大写：DEC；短横线：dec；点分隔：dec；路径分隔：dec

---

**输入**：用户头像

**输出**：
全称：驼峰：userAvatar；蛇形：user_avatar；帕斯卡：UserAvatar；全大写：USER_AVATAR；短横线：user-avatar；点分隔：user.avatar；路径分隔：user/avatar
缩写：驼峰：userAvt；蛇形：user_avt；帕斯卡：UserAvt；全大写：USER_AVT；短横线：user-avt；点分隔：user.avt；路径分隔：user/avt

---

**输入**：订单金额

**输出**：
全称：驼峰：orderAmount；蛇形：order_amount；帕斯卡：OrderAmount；全大写：ORDER_AMOUNT；短横线：order-amount；点分隔：order.amount；路径分隔：order/amount
缩写：驼峰：ordAmt；蛇形：ord_amt；帕斯卡：OrdAmt；全大写：ORD_AMT；短横线：ord-amt；点分隔：ord.amt；路径分隔：ord/amt

---

## 执行步骤

1. 解析输入关键词（中文转拼音首字母缩写；英文直接处理）
2. 生成全称七种风格
3. 生成缩写七种风格（使用缩写规则表或辅音规则）
4. 按格式输出

## 中文转拼音

使用常见拼音映射表处理中文输入：
- 小数 → xiaoshu → xs
- 用户 → yonghu → yh
- 头像 → touxiang → tx
- 订单 → dingdan → dd
- 金额 → jine → jn
- 接口 → jiekou → jk

若输入为中文但无映射，按每个汉字拼音首字母拼接处理。