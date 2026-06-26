---
name: china-phone
description: 中国手机号码归属地与运营商查询。Use when the user wants to look up the province, city, and carrier (运营商) of a Chinese mobile phone number. Identifies China Mobile, China Unicom, China Telecom, and virtual operators (虚拟运营商). No API key required — uses free public endpoints plus offline prefix rules as fallback, and decodes Unicode JSON responses into readable Chinese.
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins:
        - curl
        - python3
---

# 中国手机号归属地查询 China Phone Lookup

查询手机号码归属省市及运营商，无需任何 API key。主查询使用 `curl` 获取接口响应，并用 `python3` 解析 JSON，确保 `\u6cb3\u5357` 这类 Unicode 转义会正确显示为中文。

## 触发时机

- "这个手机号是哪里的" / "138xxxx是什么运营商"
- "帮我查一下这个号码的归属地"
- "这个号是移动还是联通"
- 验证用户手机号归属地、识别虚拟运营商号段

---

## 查询接口（无需 API key，按优先级使用）

### 接口 A：360手机查询（主力，精确到省市）

```bash
curl -s "https://cx.shouji.360.cn/phonearea.php?number={手机号}" | python3 -c '
import sys, json
obj = json.load(sys.stdin)
data = obj.get("data") or {}
print(json.dumps({
  "code": obj.get("code"),
  "province": data.get("province", ""),
  "city": data.get("city", ""),
  "sp": data.get("sp", "")
}, ensure_ascii=False))
'
```

示例：
```bash
curl -s "https://cx.shouji.360.cn/phonearea.php?number=13812345678" | python3 -c '
import sys, json
obj = json.load(sys.stdin)
data = obj.get("data") or {}
print(f"{data.get(\"province\", \"\")} {data.get(\"city\", \"\")} {data.get(\"sp\", \"\")}".strip())
'
```

响应：
```json
{
  "code": 0,
  "data": {
    "province": "江苏",
    "city": "南京",
    "sp": "移动"
  }
}
```

原始接口有时会返回：
```json
{"code":0,"data":{"province":"\u6cb3\u5357","city":"\u5357\u9633","sp":"\u8054\u901a"}}
```

注意：
- 不要把 `\u6cb3\u5357` 这类转义字符串原样展示给用户
- 必须先解析 JSON，再输出解码后的中文，如 `河南 / 南阳 / 联通`
- 对用户最终回复时，始终输出自然中文，不输出原始转义内容

字段说明：
- `province`：归属省份
- `city`：归属城市（部分号段无城市信息）
- `sp`：运营商（移动 / 联通 / 电信 / 虚拟运营商）
- `code`：0=成功，其他=失败

### 接口 B：淘宝手机查询（备用，精确到省）

```bash
curl -s "https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel={手机号}"
```

示例：
```bash
curl -s "https://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel=13812345678"
```

响应（JSONP格式，需提取内容）：
```
__GetZoneResult_ = {
  mts:'1381234',
  province:'江苏',
  catName:'中国移动',
  telString:'13812345678',
  carrier:'江苏移动'
}
```

提取 `province`（省份）和 `catName`（运营商全称）字段即可。

### 接口 C：离线号段前缀规则（两个接口均失败时降级）

根据手机号前3位快速判断运营商：

```
中国移动：
  134-139, 147, 148, 150-152, 157-159
  165, 172, 178, 182-184, 187, 188, 195, 197, 198

中国联通：
  130-132, 145, 146, 155, 156, 166
  167, 171, 175, 176, 185, 186, 196

中国电信：
  133, 149, 153, 162, 173, 174, 177, 180, 181
  189, 190, 191, 193, 199

中国广电：
  192

虚拟运营商（转售）：
  162, 165, 167, 170, 171
  注：170/171开头需结合第4位细分具体虚商

卫星电话：
  1349（中国移动卫星）

特殊号段：
  400/800  企业客服号（非手机号，无法查归属地）
  010/021等 固话号段（非手机号）
```

---

## 号码合法性验证

查询前先验证号码格式：

```
合法手机号条件：
1. 长度为11位
2. 全部为数字
3. 以 1 开头
4. 第二位为 3-9

不合法情况：
- 少于或多于11位
- 包含非数字字符（如 +86、空格、横线）
- 不以1开头
- 170/171需进一步验证（虚拟运营商转售）

预处理：自动去除 +86、86、空格、横线等前缀
```

---

## 格式化输出

### 单号查询

```
📱 手机号查询结果
━━━━━━━━━━━━━━━━━━━━
手机号码：138****5678（已脱敏）
归属地：江苏省 南京市
运营商：中国移动
号段类型：普通手机号
```

### 虚拟运营商

```
📱 手机号查询结果
━━━━━━━━━━━━━━━━━━━━
手机号码：170****1234（已脱敏）
归属地：北京市
运营商：中国联通（虚拟运营商转售）
号段类型：虚拟运营商号段
提示：此号段为虚拟运营商，实际网络由联通承载
```

### 批量查询

```
📱 批量手机号查询（3个）
━━━━━━━━━━━━━━━━━━━━
1. 138****5678  江苏南京  中国移动
2. 186****9012  广东深圳  中国联通
3. 189****3456  北京      中国电信
━━━━━━━━━━━━━━━━━━━━
移动：1个 / 联通：1个 / 电信：1个
```

---

## 执行流程

```
用户输入手机号
  ↓
[验证] 格式检查（11位、1开头、数字）
  ↓ 格式不合法
[提示] 告知用户号码格式有误
  ↓ 合法
[预处理] 去除 +86/空格/横线 等前缀
  ↓
[查询] curl 360接口（主力）
  ↓ 成功后解析 JSON，解码 Unicode 中文
  ↓ 失败
[查询] curl 淘宝接口（备用）
  ↓ 失败
[降级] 号段前缀规则判断运营商（无法确定城市）
  ↓
[脱敏] 中间4位替换为 ****
  ↓
[输出] 格式化结果
```

---

## 隐私说明

- 输出时对手机号中间4位脱敏（如 138****5678）
- 不存储、不记录任何查询的手机号码
- 仅查询号段归属，无法获取手机号实名信息

---

## 注意事项

- 手机号归属地是**号段注册地**，不代表用户实际所在地（异地使用很常见）
- 携号转网用户的运营商查询结果可能不准确（号段归属运营商与实际使用运营商不同）
- 虚拟运营商号段（170/171）需要结合第4位才能判断具体转售商
- 400/800 企业号、固话号段不属于手机号，无法查询归属地
