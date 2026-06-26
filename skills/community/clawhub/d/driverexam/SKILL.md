---
name: "Driver's License Exam - 驾考题库"
description: 获取小车/客车/货车/摩托车科目一与科目四题库。当用户说：来几道驾考科目一题、摩托车科四模拟，或类似驾考刷题时，使用本技能。
metadata: { "openclaw": { "emoji": "🚗", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据驾考题库（Jisu DriverExam）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [驾考题库 API](https://www.jisuapi.com/api/driverexam/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

包含 **小车、客车、货车、摩托车 4 类**，支持 **科目一、科目四** 顺序或随机获取试题。

当前封装一个接口：

- **获取考题**（`/driverexam/query`）


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/driverexam/driverexam.py`

## 使用方式

### 获取考题（/driverexam/query）

```bash
python3 skills/driverexam/driverexam.py '{"type":"C1","subject":"1","pagesize":"10","pagenum":"1","sort":"normal"}'
```

请求 JSON 示例：

```json
{
  "type": "C1",
  "subject": "1",
  "pagesize": "10",
  "pagenum": "1",
  "sort": "normal",
  "chapter": "1"
}
```

### 请求参数

| 字段名   | 类型   | 必填 | 说明                                                                 |
|----------|--------|------|----------------------------------------------------------------------|
| type     | string | 是   | 题目类型：A1、A3、B1、A2、B2、C1、C2、C3、D、E、F（默认 C1）        |
| subject  | string | 否   | 科目类别：`1` 为科目一、`4` 为科目四，默认 1                         |
| pagesize | string | 否   | 每页数量，默认 1                                                     |
| pagenum  | string | 否   | 当前页数                                                             |
| sort     | string | 否   | 排序方式：顺序 `normal`，随机 `rand`，默认 `normal`                 |
| chapter  | string | 否   | 章节：科目一为 1–4，科目四为 41–47，摩托车科目一为 7，科目四为 49  |

脚本仅强制要求 `type` 字段必填，其余均为可选参数，按文档原样透传给接口。

## 返回结果示例

脚本直接输出接口的 `result` 字段，结构与官网示例一致，例如（参考
[极速数据驾考题库文档](https://www.jisuapi.com/api/driverexam/)）：

```json
{
  "total": "950",
  "pagenum": "1",
  "pagesize": "3",
  "subject": "1",
  "type": "C1",
  "sort": "normal",
  "list": [
    {
      "question": "未取得驾驶证的学员在道路上学习驾驶技能，下列哪种做法是正确的？",
      "option1": "A、使用所学车型的教练车由教练员随车指导",
      "option2": "B、使用所学车型的教练车单独驾驶学习",
      "option3": "C、使用私家车由教练员随车指导",
      "option4": "D、使用所学车型的教练车由非教练员的驾驶人随车指导",
      "answer": "A",
      "explain": "《公安部令第123号》规定：未取得驾驶证的学员在道路上学习驾驶技能，使用所学车型的教练车由教练员随车指导。",
      "pic": "",
      "type": "C1,C2,C3"
    }
  ]
}
```

字段说明：

- 顶层：
  - `total`：题库总数
  - `pagenum`：当前页
  - `pagesize`：每页数量
  - `subject`：科目类别（1 或 4）
  - `type`：题目类型（驾照类型）
  - `sort`：排序方式（normal / rand）
- `list` 数组：
  - `question`：题目内容
  - `option1`–`option4`：选项（判断题可能为空）
  - `answer`：正确答案（选择题为 A/B/C/D，判断题为 “对/错”）
  - `explain`：答案解析
  - `pic`：配图 URL（如无图片则为空）
  - `type`：适用驾照类型列表（如 `C1,C2,C3`）

## 常见错误码

来自 [极速数据驾考题库文档](https://www.jisuapi.com/api/driverexam/) 的业务错误码：

| 代号 | 说明       |
|------|------------|
| 201  | 类型不正确 |
| 202  | 科目不正确 |
| 210  | 没有信息   |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在     |
| 102  | APPKEY 已过期           |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止               |
| 106  | IP 请求超过限制         |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. 用户需求示例：「我要练 C1 科目一，给我几道随机题并讲解答案。」  
2. 代理构造 JSON：`{"type":"C1","subject":"1","pagesize":"10","pagenum":"1","sort":"rand"}`，调用：  
   `python3 skills/driverexam/driverexam.py '{"type":"C1","subject":"1","pagesize":"10","pagenum":"1","sort":"rand"}'`。  
3. 从返回的 `list` 中逐题读取 `question`、`option1`–`option4`、`answer`、`explain`，将题目以问答形式展示给用户，并在用户作答后对比 `answer` 给出是否正确和解析。  
4. 可按 `chapter` 筛选章节，或基于用户表现自适应调整难度和题量，用于构建对话式刷题体验。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

