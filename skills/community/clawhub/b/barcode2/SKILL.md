---
name: "Barcode Inquiry - 商品条码查询"
description: 按类型与参数生成条形码图（base64），或识别条码图内容。当用户说：生成一个 Code128 条码图、识别这张条码里的数字，或类似条码生成/识别时，使用本技能。
metadata: { "openclaw": { "emoji": "🏷️", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据条码生成识别（Jisu Barcode）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- 生成多种类型条形码（EAN13、EAN8、CODE11、CODE128、CODE39、CODE93、GS1128、I25、ISBN、MSI、UPCA、UPCE、CODEBAR 等），返回 base64 图片内容；
- 从条形码图片（URL 或 base64）中识别出条码类型与编号。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [条码生成识别 API](https://www.jisuapi.com/api/barcode/) 页面，点击「申请数据」
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

当前脚本提供 2 个子命令：

- `generate`：条码生成（/barcode/generate）
- `read`：条码识别（/barcode/read）

### 1. 条码生成（/barcode/generate）

```bash
python3 skills/barcode/barcode.py generate '{
  "type": "ean13",
  "barcode": "6901236341056",
  "fontsize": 12,
  "dpi": 72,
  "scale": 2,
  "height": 40
}'
```

请求字段：

| 字段名   | 类型   | 必填 | 说明 |
|----------|--------|------|------|
| type     | string | 是   | 条码类型，如 `ean13` 等 |
| barcode  | string | 是   | 条码号 |
| fontsize | string/int | 是 | 字号 |
| dpi      | string/int | 是 | DPI |
| scale    | string/int | 是 | 比例 |
| height   | string/int | 是 | 高度 |

返回字段（`result`）：

| 字段名   | 类型   | 说明 |
|----------|--------|------|
| type     | string | 条码类型（如 EAN13 等） |
| fontsize | string | 字号 |
| dpi      | string | DPI |
| scale    | string | 比例 |
| height   | string | 高度 |
| barcode  | string | 条码图片 base64 内容 |

### 2. 条码识别（/barcode/read）

```bash
python3 skills/barcode/barcode.py read '{
  "barcode": "https://api.jisuapi.com/barcode/barcode/1471602033673149.png"
}'
```

请求字段：

| 字段名   | 类型   | 必填 | 说明 |
|----------|--------|------|------|
| barcode  | string | 是   | 支持 base64 或可访问的条码图片 URL，图片文件最大支持 500K |

返回字段：

`result` 为数组，每个元素包含：

| 字段名 | 类型   | 说明   |
|--------|--------|--------|
| type   | string | 条码类型 |
| number | string | 条码内容 |

## 常见错误码

业务错误码（来源于官网文档）：

| 代号 | 说明         |
|------|--------------|
| 201  | 条码类型不正确 |
| 202  | 条码号为空     |
| 203  | 条码不正确     |
| 206  | 条码地址不正确 |
| 210  | 没有信息       |

系统错误码：

| 代号 | 说明             |
|------|------------------|
| 101  | APPKEY 为空或不存在 |
| 102  | APPKEY 已过期    |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制   |
| 105  | IP 被禁止       |
| 106  | IP 请求超过限制   |
| 107  | 接口维护中       |
| 108  | 接口已停用       |

## 推荐用法

1. 用户提问：「帮我生成一个 EAN13 条形码图片」「帮我识别这个条形码里的编号」。  
2. 对于生成需求：根据用户提供的条码号与类型构造 `generate` 请求，从返回的 `barcode` 字段中获取 base64 图片内容，供前端直接展示或保存为 PNG；  
3. 对于识别需求：将条码图片 URL 或 base64 作为 `barcode` 参数调用 `read`，遍历返回数组，读取每条记录的 `type/number` 回答给用户。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

