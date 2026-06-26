---
name: fliggy-search
version: 1.0.1
description: Search flights, hotels, tickets, and holidays on Fliggy (飞猪). IMPORTANT: Before ANY search, CHECK login state by running `ls ~/.fliggy-session.json`. If NO login state exists, FIRST run `fliggy login` to login and save state. After login, use `--headless` for background searches. Use when user wants to: (1) Search flights (机票), (2) Search hotels (酒店), (3) Search scenic tickets (门票), (4) Search holidays/tours (度假/跟团游/一日游), (5) Plan travel, (6) Book travel products.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["fliggy"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "fliggy-cli",
              "bins": ["fliggy"],
              "label": "Install Fliggy CLI (npm)",
            },
          ],
      },
  }
---

# Fliggy Travel Search

飞猪旅行搜索工具，支持机票、酒店、门票、度假搜索。

## 安装

```bash
npm install -g fliggy-cli
```

## 使用流程（自动检查登录态）

**重要：每次执行搜索前，先检查是否有登录态！**

### 检查登录态

```bash
# 检查是否存在登录状态文件
ls ~/.fliggy-session.json
```

### 如果没有登录态

```bash
# 先执行登录
fliggy login

# 登录成功后，登录态自动保存，后续搜索无需重复登录
```

### 有登录态后执行搜索

```bash
# 机票搜索
fliggy flight --type oneway --from 北京 --to 上海 --date 2026-05-10 --headless

# 酒店搜索
fliggy hotel --city 北京 --check-in 2026-05-10 --check-out 2026-05-12 --headless

# 门票搜索
fliggy ticket --keyword "故宫门票" --headless

# 度假搜索
fliggy holiday --keyword "三亚跟团游" --headless
```

## 登录命令详解

```bash
# 登录飞猪账号并保存状态
fliggy login

# 清除登录状态
fliggy login --clear
```

登录成功后状态自动保存到 `~/.fliggy-session.json`，后续搜索无需重复登录。

## 机票搜索

### 单程机票

```bash
fliggy flight --type oneway --from 北京 --to 上海 --date 2026-05-10
```

### 往返机票

```bash
fliggy flight --type round --from 北京 --to 上海 --date 2026-05-10 --return-date 2026-05-15
```

### 使用 headless 模式

```bash
fliggy flight --type oneway --from 北京 --to 杭州 --date 2026-05-10 --headless
```

### 机票详情查询

```bash
# 按航班号搜索
fliggy flight-detail --keyword "MU5193" --from 北京 --to 上海 --date 2026-05-10

# 按航空公司搜索
fliggy flight-detail --keyword "东航" --from 北京 --to 上海 --date 2026-05-10

# 按机型搜索
fliggy flight-detail --keyword "宽体机" --from 北京 --to 上海 --date 2026-05-10
```

## 酒店搜索

### 搜索酒店

```bash
fliggy hotel --city 北京 --check-in 2026-05-10 --check-out 2026-05-12
```

### 搜索带关键词

```bash
fliggy hotel --city 北京 --check-in 2026-05-10 --check-out 2026-05-12 --keywords "亚奥"
```

### 酒店详情查询

```bash
fliggy hotel-detail --name "亚奥国际" --city 北京 --check-in 2026-05-10 --check-out 2026-05-12
```

## 门票搜索

门票搜索会自动访问详情页获取完整信息（价格、评分、销量、标签等）。

### 搜索门票

```bash
# 搜索景点门票
fliggy ticket --keyword "故宫门票"
fliggy ticket --keyword "香港迪士尼"
fliggy ticket --keyword "黄山门票"

# 使用 headless 模式
fliggy ticket --keyword "故宫门票" --headless
```

### 输出示例

```
景点名称：故宫鼓浪屿外国文物馆
价格：¥12
销量：已售5
特色标签：免预约, 随买随用
链接：https://s.fliggy.com/scenic/detail.htm?sid=23344
```

## 度假搜索

度假搜索会自动访问详情页获取完整信息（行程天数、出发城市、评分、销量、特色标签、酒店舒适度等）。

### 搜索度假产品

```bash
# 一日游
fliggy holiday --keyword "香港一日游"
fliggy holiday --keyword "北京一日游"

# 跟团游
fliggy holiday --keyword "三亚跟团游"
fliggy holiday --keyword "云南跟团游"

# 多日游
fliggy holiday --keyword "云南5天4晚"
fliggy holiday --keyword "桂林3天2晚"

# 使用 headless 模式
fliggy holiday --keyword "三亚跟团游" --headless
```

### 输出示例

```
产品名称：三亚南山寺天涯海角一日游纯玩含接送
价格：¥112
行程天数：1天0晚
出发城市：三亚出发
评分：4.7分
销量：已售58786
特色标签：无购物, 纯玩, 含餐, 私家团, 自由活动, 含接送
酒店舒适度：准四星
```

## 智能 Headless 模式

使用 `--headless` 参数时：

| 场景 | 行为 |
|-----|------|
| 有登录状态 | 🤖 后台运行，不显示浏览器 |
| 需要登录 | 🖥️ 自动打开浏览器，等待登录 |
| 登录成功 | 自动保存状态，继续运行 |

**推荐流程：**

1. 首次使用：`fliggy login`
2. 之后所有搜索都用 `--headless`

## 命令参数说明

### 通用参数

- `--headless`: 使用后台模式（不显示浏览器窗口）

### 机票参数

- `--type`: 单程 `oneway` / 往返 `round`
- `--from`: 出发城市
- `--to`: 到达城市
- `--date`: 出发日期 (YYYY-MM-DD)
- `--return-date`: 返回日期 (往返必填)

### 酒店参数

- `--city`: 城市
- `--check-in`: 入住日期 (YYYY-MM-DD)
- `--check-out`: 退房日期 (YYYY-MM-DD)
- `--keywords`: 搜索关键词（可选）

### 门票/度假参数

- `--keyword`: 搜索关键词（景点名称或产品名称）

## 注意事项

1. 登录状态有效期约 7-30 天
2. 门票和度假搜索会自动访问详情页获取完整信息
3. 建议首次使用前执行 `fliggy login`
4. headless 模式需要登录状态，否则会自动打开浏览器

## 帮助命令

```bash
fliggy --help
fliggy flight --help
fliggy hotel --help
fliggy ticket --help
fliggy holiday --help
```