---
name: "Bank Card Recognition OCR - 银行卡识别"
description: 对银行卡图片 OCR，返回卡号、银行与卡类型等。当用户说：银行卡卡号从照片里读出来、识别这张卡哪家银行，或类似银行卡 OCR 时，使用本技能。
metadata: { "openclaw": { "emoji": "💳", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据银行卡识别（Jisu BankCardCognition）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- `number`：银行卡号
- `type`：银行卡类型（借记卡/信用卡等）
- `bankname`：银行名称
- `bankno`：银行编号

使用前需要在极速数据官网申请服务，文档见：[https://www.jisuapi.com/api/bankcardcognition/](https://www.jisuapi.com/api/bankcardcognition/)


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/bankcardcognition/bankcardcognition.py`

## 使用方式与请求参数

当前脚本封装了 `/bankcardcognition/recognize` 接口，统一通过一段 JSON 调用。

### 1. 从本地图片识别银行卡（推荐）

```bash
python3 skills/bankcardcognition/bankcardcognition.py '{"path":"bankcard.jpg"}'
```

- `path`：本地银行卡图片路径（脚本会读取并转为 base64），建议使用较清晰的 JPG/PNG，大小不超过 500K。

### 2. 直接传 base64 图片内容

如果前置流程已经将图片转为 base64，可以直接传 `pic` 字段：

```bash
python3 skills/bankcardcognition/bankcardcognition.py '{
  "pic": "<base64_string>"
}'
```

> 注意：`pic` 只需要纯 base64 内容，不要带 `data:image/...;base64,` 前缀。

### 3. 请求参数说明

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| path   | string | 二选一 | 本地图片路径，脚本会自动读取并转为 base64 |
| image  | string | 二选一 | `path` 的别名 |
| file   | string | 二选一 | `path` 的别名 |
| pic    | string | 二选一 | 已是 base64 的图片内容（不带前缀） |

`path/image/file` 与 `pic` 至少提供一个，同时存在时优先使用 `pic`。

## 返回结果说明

原始接口返回结构示例（参考官网文档）：

```json
{
  "status": 0,
  "msg": "ok",
  "result": {
    "number": "9559980210010631815",
    "type": "借记卡",
    "bankname": "农业银行",
    "bankno": "01030000"
  }
}
```

本技能会直接输出 `result` 对象，例如：

```json
{
  "number": "9559980210010631815",
  "type": "借记卡",
  "bankname": "农业银行",
  "bankno": "01030000"
}
```

当出现业务错误（如图片为空、格式错误、大小超限等）时，统一包装为：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "图片为空"
}
```

网络或解析错误则返回：

```json
{
  "error": "request_failed" | "http_error" | "invalid_json",
  "message": "...",
  "status_code": 500
}
```

## 常见错误码

来源于 [银行卡识别文档](https://www.jisuapi.com/api/bankcardcognition/)：

| 代号 | 说明               |
|------|--------------------|
| 201  | 图片为空           |
| 202  | 图片格式错误       |
| 204  | 图片大小超过限制   |
| 208  | 识别失败           |
| 210  | 没有信息           |

系统错误码 101–108 与其它极速数据接口一致。

## 推荐用法

1. 用户上传一张银行卡照片，希望确认卡号、银行名称或卡类型。  
2. 代理将图片保存为本地文件或转为 base64，调用：`python3 skills/bankcardcognition/bankcardcognition.py '{"path":"bankcard.jpg"}'`。  
3. 从返回结果中读取 `number/type/bankname/bankno` 字段，用自然语言总结，并根据场景提醒注意隐私和安全，仅在安全环境下展示或存储卡号信息。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

