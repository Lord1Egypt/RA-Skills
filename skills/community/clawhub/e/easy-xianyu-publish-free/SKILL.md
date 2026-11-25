---
name: easy-xianyu-publish-free
description: 免费、免第三方 API Key 的闲鱼商品上架助手。用户想把商品资料和图片整理后填写到闲鱼发布页、检查必填项或生成待发布草稿时使用。它通过用户已登录的 Easy WebBridge 浏览器工作，必须指定 browserId 和账号别名；默认停在最终发布确认前，不承诺成交、流量或规避风控。
---

# 免费闲鱼商品上架

把已有的商品资料填进闲鱼发布页，减少重复复制粘贴；也可以先按关键词查看闲鱼公开同款，帮助补齐分类和卖点。这个 Skill 不提供闲鱼账号，也不绕过登录、验证码或风控。

## 适用场景

- 商品资料已经在本地 Markdown、TXT、JSON 或表格中，想整理成闲鱼发布草稿。
- 想先搜索公开同款，参考同类商品的标题、价格带和常见卖点。
- 需要在指定的闲鱼账号环境中填写标题、描述、价格、分类、数量和图片。
- 需要在发布前检查字段是否完整，而不是让智能体直接替你发布。

## 前置条件

1. macOS（仅 Apple 芯片）和 Windows 打开 EasyBR 即可使用内置 Easy WebBridge；官方[客户端下载页](https://www.ebrower.com/down.html)，另有 [GitHub Release 镜像](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)。其他系统按 [GitHub 源码说明](https://github.com/xxjrq/easy-webbridge)安装（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)）。
2. 在 EasyBR 中登录闲鱼，提供一个明确的在线 `browserId`、账号别名和商品资料路径。

## 输入

```json
{
  "browserId": "easybr-xianyu-a",
  "accountAlias": "闲鱼主店",
  "source": "./product.json",
  "search": {"query": "机械键盘", "limit": 5},
  "mode": "draft-only",
  "images": ["./images/01.jpg", "./images/02.jpg"]
}
```

`source` 至少包含 `title`、`description`、`price`、`category`；缺少字段时先返回清单，不猜价格或分类。`search` 为可选项，提供 `query` 时只读取公开搜索结果，不把搜索价格直接当成商品定价。`mode` 只能是 `draft-only` 或 `confirm-before-publish`。

## 操作步骤

1. 校验 `browserId`、账号别名、资料路径和图片是否存在；同一 `browserId` 已有任务时排队，不并发操作。
2. 通过 Easy WebBridge 的已公开连接能力选择浏览器，不在 Skill 内虚构接口或保存 Cookie、密码、Token。
3. 若提供 `search.query`，先打开闲鱼公开搜索页，读取不超过 `limit` 条可见同款的标题、价格、成色和卖点；每条结果保留来源链接或页面位置，读不到就标记缺失，不编造。
4. 打开闲鱼发布入口，确认页面显示的是目标账号。未登录、验证码、实名、风控或权限提示立即返回 `needs_user_action`。
5. 按页面实际字段依次填写标题、描述、分类、价格、数量、成色和图片；每个关键字段填完后重新读取页面确认。
6. 输出同款搜索摘要、字段检查结果和发布页截图或链接（若浏览器能力提供），状态为 `draft_ready` 时停在发布按钮前。
7. 只有用户在当前任务中明确确认，才能带 `--confirm` 执行一次真实上架；写入前登记 `intentId`，收到商品 ID 并回读详情后才标记成功。超时或回读失败标记 `uncertain`，不得自动重试。

## 执行

```bash
# 只检查并生成草稿报告
node scripts/run.mjs --input /absolute/input.json --output /absolute/result.json

# 用户确认后执行一次上架；输入必须含唯一 intentId
node scripts/run.mjs --input /absolute/input.json --output /absolute/result.json --confirm
```

目标 EasyBR 环境必须安装 `dianqunhelp`。脚本只使用该环境现有登录态，不读取 Cookie。

## 输出

生成 JSON 或 Markdown 报告，至少包含 `status`、`browserId`、`accountAlias`、`filledFields`、`missingFields`、`imageCount`、`searchResults`、`sourceUrl`、`nextAction` 和 `errors`。状态只使用 `draft_ready`、`published`、`uncertain`、`needs_user_action`、`partial`、`failed`。

## 失败处理

- Easy WebBridge 未启动或找不到 `browserId`：返回 `needs_user_action`，说明启动地址和需要选择的浏览器。
- 闲鱼要求登录、验证码、实名或风控：停止当前账号，不重试绕过；其他账号任务不受影响。
- 图片格式、大小或数量不符合页面要求：列出具体文件和修复建议，不伪造上传成功。
- 页面字段改版或读取不到值：保留已经完成的字段，返回 `partial`，不要点击发布。

## 安全边界

默认不发布、不改价、不下架、不删除、不私信、不付款。真实上架需要输入模式、`--confirm` 和唯一 `intentId` 三重条件；同一浏览器的任务必须串行，多账号结果必须带账号别名和 `browserId`。

## 自测

```bash
node scripts/self-test.mjs
```

## 定制服务与电脑接口

原创定制服务使用 `sourceType: "original"`、独立 `localId`、`fulfillmentMode: "custom-service"` 和非空 `serviceScope`；原创成品继续要求真实 `deliveryFiles`。不能给定制服务填写假交付文件或竞品ID。

现有扩展走电脑 MTOP 发布接口，依然使用平台推荐的匹配类目。网页提示App发布时先核对接口能力，不直接判定只能手机操作。`inspectListing` 可只读回查真实商品ID、标题、价格、类目和远端状态；平台受理与持续在售分开保存，回读状态异常或超时不能重发。
