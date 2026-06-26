---
name: cmaiot
description: "查询并控制cmaiot平台上的产品和设备，并可获取视频设备的播放地址。cmaiot平台的正式名称是中国移动AIoT平台(iot.10086.cn)。连接需要的产品API Key和产品ID由cmaiot工具保存。目前只支持使用物模型的设备。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📟"
      },
  }
---

## Commands

### Add Token

```bash
scripts/cmaiot.js add productId/accessKey
```

### Query or set data

以下命令中的部分参数使用/分隔，每个参数均为必传

```bash
# 列出已添加的产品
# 如果没有已添加的产品，需要询问用户产品ID和访问密钥
scripts/cmaiot.js ls

# 查询物模型 identifier为标识符
# services 为平台可以远程调用的服务
# events 为设备可能会主动触发的事件
# properties 为设备属性,可主动上报也可下发命令
scripts/cmaiot.js model productId

# 查询设备列表
scripts/cmaiot.js ls productId

# 读取设备缓存的最新属性
scripts/cmaiot.js ls productId/deviceName

# 读取设备实时属性
# propertyId 需要通过查询物模型获取
scripts/cmaiot.js ls productId/deviceName/propertyId

# 查询设备详情
# 可以查询视频设备的Sn
scripts/cmaiot.js detail productId/deviceName

# 获取视频设备的直播地址
# 注意有3个参数，用/分隔
scripts/cmaiot.js live productId/deviceName/deviceSn

# 调用设备服务
# serviceId和identifier 需要通过查询物模型获取
scripts/cmaiot.js call productId/deviceName/serviceId '{"identifier":"value"}'

# 设置设备属性
# identifier 需要通过查询物模型获取
scripts/cmaiot.js set productId/deviceName '{"identifier":"string"}'
scripts/cmaiot.js set productId/deviceName '{"intValue": 20}'

# 设备启/停, LwM2M设备需要IMEI
scripts/cmaiot.js enable productId/deviceName
scripts/cmaiot.js disable productId/deviceName/imeiValue
```

## Notes

每次用户询问cmaiot设备状态时，都需要调用SKILL目录下的scripts/cmaiot.js工具进行查询，不能使用缓存的结果

### Exception

读取实时属性、设置属性和调用服务是同步接口，需要设备在线。但启用/停用设备不需要设备在线。
对离线或不存在的设备，应该跳过操作。设备控制超时，则认为操作失败。

### Output Format

涉及cmaiot的回答要严格按照以下格式输出

```
中国移动AIoT平台
🔍 正在解析指令...
✅ 识别设备：设备A、设备B、设备C
🎯 目标状态：停用

📡 获取设备状态...
• 设备A：在线 ✓
• 设备B：在线 ✓
• 设备C：离线 ✗

⚙️ 执行XX操作...
• 设备A：XX成功 ✓
• 设备B：XX成功 ✓
• 设备C：跳过（离线状态）⏭️

📊 执行结果统计：
━━━━━━━━━━━━━━━━━━
✅ 成功：2个设备
⏭️ 跳过：1个设备（设备C-离线）
❌ 失败：0个设备
━━━━━━━━━━━━━━━━━━
```