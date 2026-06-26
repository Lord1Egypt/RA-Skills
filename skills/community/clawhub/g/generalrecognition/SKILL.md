---
name: "General Text Recognition OCR - 通用文字识别"
description: 图片通用文字 OCR，支持中英文及多语种。当用户说：这张图里的字提取成文本、截图 OCR 一下，或类似通用识图问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据通用文字识别（Jisu General Recognition / OCR）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- `cnen`：中英文（默认）
- `en`：英语
- `fr`：法语
- `pt`：葡萄牙语
- `de`：德语
- `it`：意大利语
- `es`：西班牙语
- `ru`：俄语
- `jp`：日语

使用前需要在极速数据官网申请通用文字识别服务，文档见：[https://www.jisuapi.com/api/generalrecognition/](https://www.jisuapi.com/api/generalrecognition/)


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/generalrecognition/generalrecognition.py`

## 使用方式与请求参数

当前脚本只需直接传一段 JSON 参数，对应 `/generalrecognition/recognize` 接口：

### 1. 从本地图片识别（推荐）

```bash
python3 skills/generalrecognition/generalrecognition.py '{"path":"sfz1.jpg","type":"cnen"}'
```

- `path`：本地图片路径（脚本会读取并转为 base64），支持 JPG/PNG 等，单张图片最大约 500K；
- `type`：文字类型，默认 `cnen`，可选 `en/fr/pt/de/it/es/ru/jp`。

### 2. 直接传 base64 图片内容

如果你在前置流程中已经把图片转成了 base64，可以直接通过 `pic` 传入（注意不要带 `data:image/...;base64,` 前缀，只要纯 base64 字符串）：

```bash
python3 skills/generalrecognition/generalrecognition.py '{
  "pic": "<base64_string>",
  "type": "cnen"
}'
```

### 3. 请求参数说明

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| path   | string | 二选一 | 本地图片路径，脚本会自动读取并转为 base64 |
| image  | string | 二选一 | `path` 的别名 |
| file   | string | 二选一 | `path` 的别名 |
| pic    | string | 二选一 | 已经是 base64 的图片内容（不带前缀） |
| type   | string | 否   | 文字类型：`cnen/en/fr/pt/de/it/es/ru/jp`，默认 `cnen` |

`path/image/file` 与 `pic` 至少提供一个；同时存在时优先使用 `pic`。

## 返回结果说明

接口原始返回示例（参考官网文档）：

```json
{
  "status": 0,
  "msg": "ok",
  "result": [
    "此时此刻我好焦灼!",
    "你别再解释了"
  ]
}
```

本技能会对返回进行一次轻量封装，统一输出：

```json
{
  "result": [
    "此时此刻我好焦灼!",
    "你别再解释了"
  ]
}
```

当出现业务错误时（例如图片为空、格式错误、超过大小限制等），则包装为：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "图片为空"
}
```

网络或解析错误会返回：

```json
{
  "error": "request_failed" | "http_error" | "invalid_json",
  "message": "...",
  "status_code": 500
}
```

## 常见错误码

来源于 [通用文字识别文档](https://www.jisuapi.com/api/generalrecognition/)：

| 代号 | 说明             |
|------|------------------|
| 201  | 图片为空         |
| 202  | 图片格式错误     |
| 204  | 图片大小超过限制 |
| 208  | 识别失败         |
| 210  | 没有信息         |

系统错误码 101–108 与其它极速数据接口一致。

## 推荐用法

1. 用户上传一张带有文字的截图或照片，要求「帮我把图片里的文字全部提取出来」。  
2. 代理将图片保存为本地文件或转为 base64，再调用：`python3 skills/generalrecognition/generalrecognition.py '{"path":"image.jpg","type":"cnen"}'` 或传入 `pic`。  
3. 从返回的 `result` 数组中拼接出完整文本（按行合并或按需要格式化），用自然语言回复用户，并根据场景进一步分析或翻译内容。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

