---
name: jz-fuzzy-oe
description: 使用积智数据模糊译码 API，通过 17 位 VIN 车架号的车型 与 待译码的配件别名列表, 模糊解出这些配件的 标准配件编码OE 与 标准配件名称等信息，用于当精准译码无法解析出配件编码OE 与 标准配件名称时。
metadata: { "openclaw": {  "requires": { "bins": ["python3"], "env": ["JZ_API_KEY"] }, "primaryEnv": "JZ_API_KEY" } }
---

# 积智数据 VIN 模糊译码（ VIN CARTYPE+PARTSNAME）

基于 [VIN 模糊译码 API] 的 OpenClaw 技能，支持：

- **VIN CARTYPE+ PARTSNAME 模糊译码**：通过 17 位 VIN 车架号的车型 与 配件别名列表, 模糊解出 标准配件编码OE 与 标准配件名称等信息，用于当精准译码无法解析出配件编码OE 与 标准配件名称时。


使用技能前需要申请数据，请联系【积智数据】  MOBILE (+86 13916450206/15821282326) ; EMAIL( juyuan@jikugroup.com/jiangzhihui@jikugroup.com)  获取。

## 后端服务
本技能依赖 VIN-CARTYPE+PARTSNAME 模糊译码 服务，接口地址：https://erp.qipeidao.com/jzOpenClaw/getFuzzyOe

## 环境变量配置

```bash
# Linux / macOS
export JZ_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JZ_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/fuzzyoe/get_fuzzy_oe.py`

## 使用方式

### 1. 根据 VIN 车型+ 询价配件别名列表 模糊解析出 询价配件的标准配件编码 与 标准配件名称 信息, 用于当精准译码无法解析出配件编码OE 与 标准配件名称时。

```bash
python3 skills/fuzzyoe/get_parts_epc.py "LSVAL41Z882104202" "[\"前保险杠皮\",\"中网\"]"
```

```
## VIN 模糊译码 请求参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| vin    | string | 是   | 17 位 VIN 车架号                               |
| partsNames | list | 是   | 配件名称列表，每个元素为一个字符串。 |

示例：

```
LSVAL41Z882104202  "[\"前保险杠皮\",\"中网\"]"
```

## VIN CARTYPE+ PARTSNAME 模糊译码 返回结果示例

脚本直接输出接口 `model` 字段，结构与示例一致（示例简化）：

```json
  [
    {
      "referType": 3,
      "oeRefer": "1ZD807221GRU",
      "oeSource": "模糊车型译码",
      "priceRefer": null,
      "vinCode": "LSVAL41Z882104202",
      "partsName": "前保险杠皮",
      "partsAlias": "前保险杠皮",
      "otherReferInfo": null
    },
    {
      "referType": 3,
      "oeRefer": "1ZD8536689B9",
      "oeSource": "模糊车型译码",
      "priceRefer": null,
      "vinCode": "LSVAL41Z882104202",
      "partsName": "中网",
      "partsAlias": "中网",
      "otherReferInfo": null
    }
  ]
```

当出现错误（如 VIN 不正确或无数据），脚本会输出：

```json
{
  "error": "api_error",
  "state": 202,
  "msg": "VIN不正确"
}
```


## 常见错误码


| 代号   | 说明      |
|------|---------|
| 10001 | 参数错误    |
| 10004 | VIN 不正确或无数据 |


## 在 OpenClaw 中的推荐用法

1. 用户给出车架号和待译码的配件名称列表：「帮我查一下 VIN  `LSVAL41Z882104202` 询价配件： 前保险杠皮 中网 的 标准配件编码与标准名信息」。  
2. 调用：  
   `python3 skills/fuzzyoe/get_fuzzy_oe.py "LSVAL41Z882104202" "[\"前保险杠皮\",\"中网\"]"`  
3. 从返回中选取 `oeRefer/partsName/partsAlias/oeSource` 等字段，给出自然语言总结；
