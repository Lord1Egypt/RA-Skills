---
name: "Barcode Generation And Recognition - 条码生成识别"
description: 按条形码查询商品名称、品牌、规格与产地等。当用户说：扫这个条码是什么商品、690 开头的条码查一下信息，或类似商品条码查询时，使用本技能。
metadata: { "openclaw": { "emoji": "🏷️", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据商品条码查询（Barcode2）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。
通过商品条形码（EAN8/EAN13，69 开头）查询商品基础信息。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [商品条码查询 API](https://www.jisuapi.com/api/barcode2/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/barcode/barcode.py`

## 使用方式

### 按条形码查询商品信息

```bash
python3 skills/barcode/barcode.py '{"barcode":"06917878036526"}'
```

请求参数以 JSON 形式传入，仅需一个字段：

```json
{
  "barcode": "06917878036526"
}
```

## 请求参数

| 字段名   | 类型   | 必填 | 说明    |
|---------|--------|------|---------|
| barcode | string | 是   | 商品条码 |

## 返回结果示例

脚本直接输出接口 `result` 字段，典型结构与官网示例一致（简化版）：

```json
{
  "barcode": "06917878036526",
  "name": "雀巢咖啡臻享白咖啡",
  "ename": "NESCAFE White Coffee",
  "unspsc": "50201708 (食品、饮料和烟草>>饮料>>咖啡和茶>>咖啡饮料)",
  "brand": "NESCAFE",
  "type": "29g",
  "width": "70毫米",
  "height": "160毫米",
  "depth": "55毫米",
  "origincountry": "中国",
  "originplace": "",
  "assemblycountry": "中国",
  "barcodetype": "",
  "catena": ",",
  "isbasicunit": "0",
  "packagetype": "",
  "grossweight": "",
  "netcontent": "5条",
  "netweight": "145克",
  "description": "",
  "keyword": "雀巢咖啡臻享白咖啡",
  "pic": "",
  "price": "",
  "licensenum": "QS3117 0601 0440",
  "healthpermitnum": ""
}
```

当出现错误（如条码不正确或无数据）时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 202,
  "message": "条码不正确"
}
```

## 常见错误码

基于 [极速数据条码文档](https://www.jisuapi.com/api/barcode2/)：

| 代号 | 说明                               |
|------|------------------------------------|
| 201  | 条码为空                           |
| 202  | 条码不正确                         |
| 203  | 该条码已下市（扣次数）             |
| 204  | 该条码已注册，但编码信息未通报（扣次） |
| 205  | 该条码异常（扣次数）               |
| 210  | 没有信息                           |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户拍照/输入条码号：「帮我查一下条码 `06917878036526` 是什么商品」。  
2. 代理构造 JSON：`{"barcode":"06917878036526"}` 并调用：  
   `python3 skills/barcode/barcode.py '{"barcode":"06917878036526"}'`  
3. 从结果中读取 `name/brand/type/netcontent/netweight/origincountry` 等字段，为用户总结商品名称、品牌、规格和产地信息。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

