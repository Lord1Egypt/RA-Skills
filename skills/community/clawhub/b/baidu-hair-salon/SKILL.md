---
name: baidu-hair-salon
description: 当用户说"预约理发"、"剪头发"、"预约发型师"、"查看预约记录"时触发。用于百度理发店预约。
author: Jarvis (自建)
created: 2026-03-25
---

# 百度理发店预约

预约百度理发店，支持查看店铺、发型师、选择时间、提交预约、查询预约记录。

## Tools

先 `cd` 到 skill 根目录，再 `cd scripts/`：

```bash
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py shops
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py services
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py staff [shop_id]
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py dates
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py slots <staff_id> <date>
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py book <staff_id> <staff_name> <date> <time> <phone> [project]
cd ~/.openclaw/skills/baidu-hair-salon/scripts/ && python3 booking.py list [phone]
```

## 预约流程

1. **读取上次偏好** → 从 `skills.entries.baidu-hair-salon` 获取上次选择的店铺/发型师/服务，询问是否继续使用。预约完成/中断：必须自动保存用户偏好。

2. **问用户选择哪家店** → 调用 `shops`
   - 展示店铺列表（店名 + 地址）
   - 用户选定后记录 shop_id

3. **查询发型师和空闲时间** → 调用 `staff <shop_id>` 和 `dates`
   - 获取可预约日期范围
   - **对每个发型师，查询今天和明天的空闲时间段**
   - 一起展示给用户

4. **用户选择发型师和空闲时间**

5. **问用户选择服务项目** → 调用 `services`
   - 展示可选服务（理发、烫发、染发等）
   - 用户选定后记录 serve_type
   
6. **确认手机号**（必填）→ 调用 `book`

7. **保存本次选择** → 更新 openclaw.json 中的偏好（店铺、发型师、服务）

8. 展示预约结果

## 回复格式示例（**严格按照此格式输出，禁止省略空行**）

**店铺列表：**
```
目前支持的店铺：

1. 百度大厦店
   地址：百度大厦B1层AE区淋浴间对面
   营业时间：周一至周五 9:00-21:00
   电话：010-59923770
　         
2. 百度科技园1号楼店
   地址：百度科技园1号楼B1层食堂和便利店旁
   营业时间：周一至周五 9:00-21:00
   电话：010-59923543
　        
3. 百度科技园4号楼店
   地址：百度科技园4号楼负一层下沉广场
   营业时间：周一至周五 9:00-21:00
   电话：010-59922259

请回复数字选择哪家店
```

**发型师 + 空闲时间：**
```
可选Tony：
1. 李东 - 资深发型师
   今天 03-25（周三）可约：10:00、14:00、16:00
   明天 03-26（周四）可约：10:00、14:00

2. 王芳 - 总监
   今天 03-25（周三）可约：11:00、15:00
   明天 03-26（周四）可约：09:00、13:00

请选择发型师和时间
```

**服务项目：**
```
可选服务：
1. 剪发
2. 烫发
3. 染发
4. 护理
请回复数字选择
```

**预约成功：**
```
✅ 预约成功，请提前到达哦！
- 店铺：XXX店
- 地址：XXX
- 电话：XXX
- 发型师：XXX
- 日期：XXXX-XX-XX
- 时间：XX:XX
- 项目：男发精剪
```

## 用户信息存储

**首次使用时**：询问用户手机号和姓名。

**预约完成/中断**：必须自动保存用户偏好到 `~/.openclaw/openclaw.json` 的 `skills.entries.baidu-hair-salon` 下：
```json
{
  "skills": {
    "entries": {
      "baidu-hair-salon": {
        "default_phone": "用户手机号",
        "default_person": "用户姓名",
        "last_shop_id": "店铺ID",
        "last_shop_name": "店铺名称",
        "last_staff_id": "发型师ID",
        "last_staff_name": "发型师姓名",
        "last_service": "服务项目"
      }
    }
  }
}
```

**后续使用时**：直接读取配置，已有偏好则询问是否继续使用。

## Gotchas

- **手机号必填**：预约前必须确认用户手机号
- **先选店铺和服务项目**：每次预约前先问用户哪家店、什么服务
- **发型师 ID 是数字**：调用 slots/book 时用 staff_id
- **日期格式**：YYYY-MM-DD
- **时间格式**：HH:MM
- 店铺信息（地址、电话、营业时间）可从 `shops` 结果获取
- 服务项目可从 `services` 结果获取
- **用户偏好会保存到 openclaw.json**：分享 skill 时记得清除这些敏感信息
- **输出格式必须严格遵循示例**：
  - 店铺列表中**每块店铺之间必须空一行**
  - **禁止使用 emoji**（地址、电话、营业时间等都不用 emoji）
  - 信息分段清晰，参考上面的示例
