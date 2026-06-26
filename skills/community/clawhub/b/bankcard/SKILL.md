---
name: "Bank Card Origin Query - 银行卡归属地查询"
description: 根据银行卡号查发卡行与归属地，可做卡号格式校验。当用户说：6222 开头是哪家银行？这张卡号对不对？或类似银行卡归属问题时，使用本技能。
metadata: { "openclaw": { "emoji": "💳", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据银行卡归属地查询（Jisu Bankcard）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [银行卡归属地查询 API](https://www.jisuapi.com/api/bankcard) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/bankcard/bankcard.py`

## 使用方式

传入一个 JSON 字符串，包含银行卡号：

```bash
python3 skills/bankcard/bankcard.py '{"bankcard":"6212261202011584349"}'
```

## 请求参数（传入 JSON）

| 字段名   | 类型   | 必填 | 说明     |
|----------|--------|------|----------|
| bankcard | string | 是   | 银行卡号 |

示例：

```json
{
  "bankcard": "6212261202011584349"
}
```

## 返回结果示例

脚本直接输出接口的 `result` 字段（JSON），典型结构：

```json
{
  "bankcard": "6212261202011594349",
  "name": "牡丹卡普卡",
  "province": "浙江",
  "city": "杭州",
  "type": "借记卡",
  "len": "19",
  "bank": "中国工商银行",
  "logo": "http://www.jisuapi.com/api/bankcard/upload/80/2.png",
  "tel": "95588",
  "website": "http://www.icbc.com.cn",
  "iscorrect": "0"
}
```

返回字段说明：

| 参数名    | 类型   | 说明                           |
|-----------|--------|--------------------------------|
| bankcard  | string | 银行卡号                       |
| name      | string | 卡名称                         |
| province  | string | 省                             |
| city      | string | 市                             |
| type      | string | 银行卡类型                     |
| len       | string | 卡号长度                       |
| bank      | string | 银行名称                       |
| logo      | string | 银行 logo（80/120/200 等尺寸） |
| tel       | string | 银行电话                       |
| website   | string | 银行网站                       |
| iscorrect | string | 卡号校验是否正确：1 正确，0 错误 |

错误时脚本输出形如：

```json
{
  "error": "api_error",
  "code": 202,
  "message": "银行卡号不正确"
}
```

## 常见错误码

来自 [极速数据银行卡 API 文档](https://www.jisuapi.com/api/bankcard)：

**业务错误码：**

| 代号 | 说明           |
|------|----------------|
| 201  | 银行卡号为空   |
| 202  | 银行卡号不正确 |
| 210  | 没有信息       |

**系统错误码：**

| 代号 | 说明                   |
|------|------------------------|
| 101  | APPKEY 为空或不存在    |
| 102  | APPKEY 已过期          |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制       |
| 105  | IP 被禁止              |
| 106  | IP 请求超过限制        |
| 107  | 接口维护中             |
| 108  | 接口已停用             |

## 推荐用法

1. 用户例如：「查一下卡号 6212261202011584349 是哪个银行的。」  
2. 代理构造：`python3 skills/bankcard/bankcard.py '{"bankcard":"6212261202011584349"}'`。  
3. 解析返回的 JSON，为用户总结：银行名称、归属地（省/市）、卡类型、卡号是否校验通过等。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

