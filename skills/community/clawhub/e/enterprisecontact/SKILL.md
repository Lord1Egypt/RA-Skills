---
name: "Enterprise Contact Information Query - 企业联系方式查询"
description: 按名称、统一社会信用代码等查企业地址、电话、邮箱与网站等联系方式。当用户说：这家公司的联系电话是多少？总部地址在哪？或类似企业联系方式问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🏢", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据企业联系方式查询（Jisu Enterprise Contact）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [企业联系方式查询 API](https://www.jisuapi.com/api/enterprisecontact/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/enterprisecontact/enterprisecontact.py`

## 使用方式

### 企业联系方式查询（query）

```bash
python3 skills/enterprisecontact/enterprisecontact.py query '{"company":"北京抖音信息服务有限公司"}'
python3 skills/enterprisecontact/enterprisecontact.py query '{"creditno":"91110000xxxx"}'
python3 skills/enterprisecontact/enterprisecontact.py query '{"regno":"110000xxxx"}'
python3 skills/enterprisecontact/enterprisecontact.py query '{"orgno":"xxxx"}'
```

| 参数     | 类型   | 必填 | 说明 |
|----------|--------|------|------|
| company  | string | 否   | 工商名称（与下列参数任选一个） |
| creditno | string | 否   | 统一信用代码 |
| regno    | string | 否   | 注册号 |
| orgno    | string | 否   | 组织机构代码 |

至少提供 `company`、`creditno`、`regno`、`orgno` 中的一个。

## 返回结果说明

`result` 为对象，包含：

- **list**：联系方式列表。每项含 name、number、position、source、url、type、num、iskeyperson、checkstatus（2 活跃/3 空号/4 沉默/5 风险）、activepr、location、epnum、dept、agentstatus 等。
- **company** / **creditno** / **regno** / **orgno**：对应查询到的企业信息。

## 常见错误码

| 代号 | 说明 |
|------|------|
| 201  | 公司名称、信用代码和注册号都为空 |
| 202  | 公司不存在（扣次数） |
| 210  | 没有信息 |

系统错误码 101–108 见极速数据官网。

## 推荐用法

1. 用户问某企业的联系电话、邮箱等时，用企业全称或统一信用代码等调用 `query`。
2. 从返回的 `result.list` 中取需要的联系方式与职务，用自然语言回复；注意脱敏与合规使用。更多计费与说明见 [极速数据](https://www.jisuapi.com/)。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

