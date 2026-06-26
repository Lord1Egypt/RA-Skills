---
name: "Baidu Top - 百度热搜榜单"
description: 获取百度首页热搜、小说、电影、电视剧等榜单。当用户说：百度今天热搜榜？热播剧榜单，或类似百度榜单问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"] } } }
---

# 百度榜单（baidu-top）

获取百度首页榜单并按分类输出：

- 热搜榜
- 小说榜
- 电影榜
- 电视剧榜

数据来源页面：<https://top.baidu.com/board?platform=pc&tab=homepage&sa=pc_index_homepage_all>

## 依赖

```bash
pip install requests beautifulsoup4
```

## 脚本路径

- `skills/baidu-top/get.py`

## 使用方式

### 1) 默认可读输出（每类 Top 10）

```bash
python3 skills/baidu-top/get.py
```

### 2) 指定返回条数

```bash
python3 skills/baidu-top/get.py -n 20
```

### 3) 输出 JSON

```bash
python3 skills/baidu-top/get.py --json
```

### 4) 自定义 User-Agent（可选）

```bash
python3 skills/baidu-top/get.py --ua "Mozilla/5.0 ..."
```

## 输出说明

- 默认输出可读文本，按四个榜单分组展示。
- `--json` 时返回结构：
  - `ok`
  - `source`
  - `limit`
  - `boards.hot[] / boards.novel[] / boards.movie[] / boards.tv[]`
- 每条榜单项字段：
  - `rank`：排名
  - `title`：标题
  - `hot_score`：热度值（若页面未提供则为空）

## 注意事项

- 榜单数据来自网页解析，百度页面结构变化时可能需要调整规则。
- 若请求频率过高，可能触发风控或返回异常。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

