---
name: ckt-design
version: 1.0.3
description: 根据用户的海报平面设计需求，调用创客贴智能设计API生成设计缩略图。擅长制作邀请函、日签、小红书配图、商品海报、Banner等平面设计。当用户提到需要做海报、设计、邀请函、日签、小红书图、商品图、Banner，或提及平面设计、创客贴相关需求时使用此技能。
---

# 创客贴智能海报设计

根据用户的设计需求，调用创客贴智能设计服务生成海报缩略图并展示。

## 执行流程

### Step 1: 调用智能设计API

使用 HTTP GET 请求调用创客贴设计服务，将用户的原始设计需求作为 `prompt` 参数传入：

```bash
curl -G "https://gw.chuangkit.com/openplatform/intelligentDesign/api/generate" \
  --data-urlencode "prompt=用户的设计需求"
```

API 返回 JSON 格式，结构如下：

```json
{
  "body": {
    "code": 200,
    "msg": "success",
    "data": [
      {
        "taskId": "任务ID",
        "designId": "设计ID",
        "imageUrl": "缩略图地址",
        "redirectUrl": "编辑跳转地址"
      }
    ]
  },
  "header": {
    "code": "1"
  }
}
```

每个设计结果包含：`imageUrl`（缩略图地址）和 `redirectUrl`（在线编辑地址）。

### Step 2: 解析并展示结果

根据返回的 `body.code` 判断执行结果：

- **code != 200**：设计生成失败，向用户提示错误信息（`body.msg`）。
- **code == 200**：设计生成成功，执行以下操作：
  1. 从 `body.data` 数组中取第一个设计结果的 `imageUrl`
  2. 使用默认浏览器打开该缩略图地址展示给用户

打开浏览器命令参考：

```bash
# macOS
open "缩略图URL"

# Windows
start "缩略图URL"

# Linux
xdg-open "缩略图URL"
```

## 注意事项

- `prompt` 参数需要进行 URL 编码（--data-urlencode 会自动处理）
- API 可能返回多个设计结果，默认取第一个展示
- 如果用户需要查看更多设计方案，可以遍历 `data` 数组中的其他结果
