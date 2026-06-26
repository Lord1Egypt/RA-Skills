---
name: "GEO & Address Conversion - 经纬度地址转换"
description: 在百度/Google 坐标系下做经纬度与地址互转。当用户说：把这个地址转成经纬度、这两个坐标是什么地方？或类似地图坐标问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📍", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据经纬度地址转换（Jisu GeoConvert）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

支持：

- **经纬度转地址**（`/geoconvert/coord2addr`）
- **地址转经纬度**（`/geoconvert/addr2coord`）

可选择使用 `baidu` 或 `google` 类型的地理编码服务。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [经纬度地址转换 API](https://www.jisuapi.com/api/geoconvert/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/geoconvert/geoconvert.py`

## 使用方式

### 1. 经纬度转地址（/geoconvert/coord2addr）

```bash
python3 skills/geoconvert/geoconvert.py coord2addr '{"lat":"30.2812129803","lng":"120.11523398","type":"baidu"}'
```

请求 JSON：

```json
{
  "lat": "30.2812129803",
  "lng": "120.11523398",
  "type": "baidu"
}
```

### 2. 地址转经纬度（/geoconvert/addr2coord）

```bash
python3 skills/geoconvert/geoconvert.py addr2coord '{"address":"益乐路39号","type":"baidu"}'
```

请求 JSON：

```json
{
  "address": "益乐路39号",
  "type": "baidu"
}
```

`type` 说明：  
- `baidu`：使用百度地图坐标  
- `google`：使用 Google Maps 坐标  

## 请求参数

### 经纬度转地址

| 字段名 | 类型   | 必填 | 说明                        |
|--------|--------|------|-----------------------------|
| lat    | string | 是   | 纬度                        |
| lng    | string | 是   | 经度                        |
| type   | string | 否   | 类型，`baidu` 或 `google`，默认 baidu |

### 地址转经纬度

| 字段名  | 类型   | 必填 | 说明                        |
|---------|--------|------|-----------------------------|
| address | string | 是   | 地址                        |
| type    | string | 否   | 类型，`baidu` 或 `google`，默认 baidu |

## 返回结果示例（节选）

### 经纬度转地址

```json
{
  "lat": "30.2812129803",
  "lng": "120.11523398",
  "type": "google",
  "address": "中国浙江省杭州市西湖区文二西路11号 邮政编码: 310000",
  "country": "中国",
  "province": "浙江省",
  "city": "杭州市",
  "district": "西湖区",
  "description": ""
}
```

### 地址转经纬度

```json
{
  "address": "益乐路39号",
  "type": "google",
  "lat": "30.279864",
  "lng": "120.113885",
  "fulladdress": "中国浙江省杭州市西湖区益乐路39号 邮政编码: 310000",
  "precise": "",
  "confidence": "",
  "level": "street_address"
}
```

## 常见错误码

来源于 [极速数据经纬度文档](https://www.jisuapi.com/api/geoconvert/)：

| 代号 | 说明         |
|------|--------------|
| 201  | 经纬度为空   |
| 202  | 地址为空     |
| 203  | 经纬度不正确 |
| 210  | 没有信息     |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户给出坐标：「这个点 `30.2812129803,120.11523398` 是哪里？」  
2. 代理构造 JSON：`{"lat":"30.2812129803","lng":"120.11523398","type":"baidu"}` 并调用：  
   `python3 skills/geoconvert/geoconvert.py coord2addr '{"lat":"30.2812129803","lng":"120.11523398","type":"baidu"}'`  
3. 从返回结果中读取 `address/country/province/city/district` 字段，为用户总结清晰的地址描述；  
4. 反向场景下，可根据用户提供的地址调用 `addr2coord` 获取经纬度，用于后续地图或定位相关技能。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

