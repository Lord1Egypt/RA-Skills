---
name: "EPC Query For Auto Parts - 汽车配件EPC查询"
description: 按品牌/车型/VIN 查 EPC 结构树、分解图与零件信息。当用户说：查一下这款大众的 EPC 爆炸图、这个零件在图里编号多少？或类似配件 EPC 问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🧩", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据汽车配件 EPC 查询（Jisu EPC）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **车型查询**（`/epc/car`）
- **车型详情**（`/epc/cardetail`）
- **VIN 查询**（`/epc/vin`）
- **车型组查询**（`/epc/group`）
- **组和配件查询**（`/epc/groupparts`）

适合在对话中回答「这台宝马的 EPC 结构树」「这个 VIN 对应什么车型」「发动机分解图里有哪些零件、零件号和位置」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [汽车配件 EPC 查询 API](https://www.jisuapi.com/api/epc/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/epc/epc.py`

## 使用方式

### 1. 车型查询（/epc/car）

```bash
python3 skills/epc/epc.py car '{"parentid":0}'
```

`parentid=0` 时获取品牌列表，非 0 时按上级 ID 继续向下获取车型层级（具体层级结构见接口文档）。

### 2. 车型详情（/epc/cardetail）

```bash
python3 skills/epc/epc.py cardetail '{"carid":629}'
```

### 3. VIN 查询（/epc/vin）

```bash
python3 skills/epc/epc.py vin '{"vin":"LE4HG5EB3AL999908"}'
```

### 4. 车型组查询（/epc/group）

```bash
# 基于 carid
python3 skills/epc/epc.py group '{"carid":630,"parentid":0}'

# 或基于 vin（carid / vin 任选其一）
python3 skills/epc/epc.py group '{"vin":"LE4HG5EB3AL999908","parentid":0}'
```

> 根据返回的 `isend` 和 `isgraph` 字段，递归调用 `/epc/group` 直到到达含有分解图的组或最后一级：
> - `isend=1,isgraph=1`：图片在最后一级；
> - `isend=0,isgraph=1`：图片不在最后一级，需继续按 `grouptype>0` 的组向下；
> - `isend=1,isgraph=0`：组结束，无分解图和配件。

### 5. 组和配件查询（/epc/groupparts）

```bash
python3 skills/epc/epc.py groupparts '{"carid":630,"parentid":3}'
```

`parentid` 为某一组的 ID，对应 `/epc/group` 返回的 `list[].id`。

## 请求参数摘要

### /epc/car

| 字段名   | 类型 | 必填 | 说明     |
|----------|------|------|----------|
| parentid | int  | 是   | 上级 ID  |

### /epc/cardetail

| 字段名 | 类型 | 必填 | 说明   |
|--------|------|------|--------|
| carid  | int  | 是   | 车型 ID |

### /epc/vin

| 字段名 | 类型   | 必填 | 说明  |
|--------|--------|------|-------|
| vin    | string | 是   | VIN  |

### /epc/group

| 字段名   | 类型   | 必填 | 说明                                   |
|----------|--------|------|----------------------------------------|
| parentid | int    | 是   | 上级 ID                                |
| carid    | int    | 否   | 车型 ID，carid 与 vin 需至少提供一个   |
| vin      | string | 否   | VIN，carid 与 vin 需至少提供一个       |

### /epc/groupparts

| 字段名   | 类型 | 必填 | 说明   |
|----------|------|------|--------|
| parentid | int  | 是   | 上级 ID（组 ID） |
| carid    | int  | 是   | 车型 ID |

## 返回结果概览（节选）

### /epc/car

```json
[
  {
    "id": 9,
    "name": "奔驰",
    "initial": "B",
    "parentid": 0,
    "logo": "http://pic1.jisuapi.cn/epc/upload/car/9.png",
    "type": 1
  }
]
```

### /epc/cardetail

```json
{
  "carid": 629,
  "name": "114d",
  "parentname": "F20",
  "intername": "F20",
  "salecode": "1T91",
  "market": "ECE",
  "brand": "宝马",
  "bodytype": "SH",
  "enginemodel": "N47N",
  "steertype": "L",
  "startdate": "2012-11-02",
  "enddate": null,
  "remark": null
}
```

### /epc/vin

```json
{
  "carid": 3981,
  "name": "530Li",
  "intername": "F18N",
  "parentname": "F18 LCI",
  "market": "CHN",
  "brand": "宝马",
  "bodytype": "Lim",
  "enginemodel": "N52N",
  "productiondate": "2014-01"
}
```

### /epc/group

返回包含整车信息和组列表的对象（字段较多，这里仅示意）：

```json
{
  "parentid": 0,
  "car": {
    "carid": 630,
    "name": "114d",
    "parentname": "F20",
    "salecode": "1T92",
    "market": "ECE",
    "brand": "宝马"
  },
  "list": [
    {
      "id": 240,
      "code": "11",
      "isgraph": 0,
      "isend": 0,
      "name": "发动机",
      "enname": "ENGINE",
      "pic": "http://pic1.jisuapi.cn/epc/upload/group/..."
    }
  ]
}
```

### /epc/groupparts

返回每个分解图下的零件清单（含零件号、数量、配置代码和坐标信息），可用于前端绘制可点击的分解图热点区域。

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "上级ID错误"
}
```

## 常见错误码

来源于 [极速数据汽车配件 EPC 文档](https://www.jisuapi.com/api/epc/)：

| 代号 | 说明             |
|------|------------------|
| 201  | 上级 ID 错误     |
| 202  | 车型 ID 错误     |
| 203  | 此 VIN 没有 EPC 信息 |
| 204  | 请直接获取分解图和配件 |
| 205  | 零件号为空       |
| 220  | 没有信息         |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无请求此数据权限、104 请求超过次数限制、105 IP 被禁止、106 IP 请求超过限制、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「查一下这台车（VIN）的 EPC 结构树」→ 先 `vin` 获得 `carid`，再从 `group` 开始递归，构建一棵按组划分的 EPC 树，并可结合 `groupparts` 补充具体零件。  \n
2. 用户：「帮我看 114d 发动机分解图里的零件号」→ 根据已知 `carid` 调用 `group` 找到发动机相关组，再用对应 `parentid` 调 `groupparts`，整理零件号、名称和数量。  \n
3. 用户：「按品牌浏览 EPC」→ 通过 `car {"parentid":0}` 获取品牌列表，再逐步下钻到具体车型、车系和配置，配合对话进行导航。  \n

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

