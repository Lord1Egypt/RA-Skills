---
name: ai-kujiale-design
description: 室内智能设计skill，分步式对话完成户型确认→风格选择→布局确认→渲染出图。
version: 0.0.6
author: ManycoreTech
tags: [aiDesign, kujiale, coohom]
---

# 室内智能设计

## 说明
必须严格根据本文档流程来执行，不能自作主张发散。

## 初始化配置
首次使用需在项目根目录创建 `.kjlconfig.json` 文件（参考 `.kjlconfig-example.json`），配置 access_token。
若无 token，引导用户访问 https://www.kujiale.com/skills 生成并保存 `.kjlconfig.json`，key 是access_token，value
 是用户复制的值，`.kjlconfig.json`要保存在`.kjlconfig-example.json`同一目录下。

## Token 读取
所有脚本调用前，先从 `.kjlconfig.json` 读取 access_token字段作为 token：

## 版本校验
每次执行前调用：`node ./scripts/versionCheck.js --token=${token} --version=0.0.6`
- action=1：继续
- action=2：提示"版本已过时，建议更新"
- action=3：终止，提示"版本已废弃，需重新安装"

## 输出规则
- 进度反馈通过 `message(action=send)` 发送
- 最终结果只输出渲染图、全景图和设计亮点，最终结果要严格按照./outputs/result.md输出
- 已发送的消息不重复输出

---

## 分步流程

### 阶段1：户型获取与确认

**触发条件**：用户提到要做室内设计/装修设计

**步骤1.1**：询问户型来源
> "请问您有户型信息吗？
> - 输入小区名搜索户型
> - 或直接上传户型图"

**路径A：文字搜索户型**

**步骤1.2a**：询问城市
> "请问房子在哪个城市？"

**步骤1.3a**：询问小区
> "请问是哪个小区？户型信息（几室几厅、面积）也可以一起告诉我。"

**步骤1.4a**：搜索户型
```
node ./scripts/searchPlan.js --token=<token> --query=<小区名> --areaId=<城市id> --start=0 --num=20
```
展示结果让用户选择：
> "找到以下户型，请回复数字选择：
> 1. {小区名} {面积}㎡ {户型结构}
> 2. ..."

用户选择后获得 planId。

**步骤1.5a**：获取户型图并展示给用户确认
```
node ./scripts/getFloorplanInfo.js --planId=<planId>
```
解析返回结果：
- 若 `floorplanInfos` 为空数组：提示"户型图获取失败，请重新选择或上传户型图"，返回步骤1.4a
- 若有数据：取 `floorplanInfos[0].planImage` 展示给用户，直接展示图片

> "户型已生成，请查看户型图：
> [展示 planImage 图片]
> 面积：{realArea}㎡
> 请确认是否满意？
> - 回复「确认」继续创建方案
> - 回复「重新生成」重新搜索户型
> - 回复「上传图片」改为上传户型图"

等待用户回复：
- 若用户确认满意 → 进入步骤1.6创建方案
- 若用户不满意 → 根据用户选择重新执行路径A或路径B

**路径B：上传户型图**

同时监听 `~\.openclaw\media\inbound` 是否有新图片（每5秒检查）。

**步骤1.2b**：识别户型图
检测到图片后：
> "检测到您上传了图片，正在识别户型..."

**步骤1.3b**：上传图片
```
node ./scripts/getUploadToken.js --token=<token>
```
按 ./docs/upload.md 执行上传获取 url。

**步骤1.4b**：创建临摹任务
```
node ./scripts/createBitmapTask.js --token=<token> --bitmap=<url>
```
轮询结果：
```
node ./scripts/getBitmapTaskResult.js --token=<token> --taskId=<taskId>
```
获得 planId。

**步骤1.5b**：获取户型图并展示给用户确认
```
node ./scripts/getFloorplanInfo.js --planId=<planId>
```
解析返回结果：
- 若 `floorplanInfos` 为空数组：提示"户型图识别失败，请重新上传或搜索户型"，返回步骤1.2b
- 若有数据：取 `floorplanInfos[0].planImage` 展示给用户

> "户型已识别生成，请查看户型图：
> [展示 planImage 图片]
> 面积：{realArea}㎡
> 请确认是否满意？
> - 回复「确认」继续创建方案
> - 回复「重新生成」重新上传户型图
> - 回复「搜索户型」改为文字搜索"

等待用户回复：
- 若用户确认满意 → 进入步骤1.6创建方案
- 若用户不满意 → 根据用户选择重新执行路径A或路径B

**步骤1.6**：创建方案（两种路径合并）
```
node ./scripts/createDesign.js --token=<token> --planId=<planId>
```
获得 designId。

**步骤1.7**：确认户型
> "已确认户型：{户型信息}，接下来选择您喜欢的风格～"

---

### 阶段2：风格选择（标签+硬装风格）

**触发条件**：户型已确认

**步骤2.1**：获取标签并展示选项
```
node ./scripts/getTags.js --token=<token>
```
解析返回的标签列表，展示给用户：
> "请选择您的偏好：（单选，回复数字如'1'）
> 1. {标签项1名称}
> 2. {标签项2名称}
> 3. ...
> 或直接描述您的喜好"

用户选择后获得 tagItemIds 列表。

**步骤2.2**：查询硬装风格
```
node ./scripts/getStyles.js --token=<token> --tagItemIds=<id1,id2,...>
```

**步骤2.3**：风格选择
- 若返回多个风格：展示封面图让用户选择
> "以下硬装风格可选，请回复数字选择："
> 展示每个风格的 coverUrl 图片 + styleName，如果非Webchat渠道，直接展示图片

- 若返回单个风格：默认选择
> "已为您匹配{风格名}风格"

获得 styleId，进入下一阶段。

---

### 阶段3：布局生成与确认

**触发条件**：风格已确认。

**步骤3.1**：跟用户确认本次布局会消耗他账号内的智能布局的额度/核豆，需要用户确认知晓后再执行后续步骤

**步骤3.2**：使用 message(action=send) 发送"开始布局，请稍等"

**步骤3.3**：触发智能布局
```
node ./scripts/triggerLayout.js --token=<token> --designId=<designId> --tagIds=<id1,id2,...> --styleId=<styleId> --applyDecorationStyle=true --buildCeiling=true --autoDesign=true
```

**步骤3.4**：等待并查询布局结果
```
node ./scripts/getLayoutResult.js --token=<token> --designId=<designId>
```
若 c!=0 则每10秒重复查询。

**步骤3.5**：展示布局结果并等待用户确认
使用 message(action=send) 发送布局信息：
> "布局已生成！以下是各房间的布局情况：
> - {房间名1}：{家具列表}
> - {房间名2}：{家具列表}
> ...
直接进入阶段4渲染出图



---

### 阶段4：渲染出图

**触发条件**：布局已确认

**步骤4.1**：使用 message(action=send) 发送："开始渲染，请稍等"

**步骤4.2**：触发渲染
```
node ./scripts/trigger-render.js --obsDesignId=<designId> --xToken=<token>
```
发送：`"正在生成效果图，预计几分钟..."`

**步骤4.3**：等待10秒后查询渲染结果
```
node ./scripts/getRenderResult.js --token=<token> --designId=<designId>
```
提取 pictype=0 的 img（渲染图）和 pictype=1 的 panoLink（全景图）。若空则每分钟重试，超5分钟反馈失败。

**步骤4.4**：输出最终结果
发送：`"效果图已生成！"`
严格按 ./outputs/result.md 格式输出：
- 设计亮点（根据第一张渲染图总结）
- 渲染图（按房间优先级：客餐厅→主卧→次卧→其他）
- 全景图链接
- 方案详情链接（https://www.kujiale.com/pcenter/design/{designId}/setting?from=skills）

---

## 渠道规则
- Webchat：直接发送图片链接
- 飞书：推送格式 `MEDIA:图片url`，即直接展示图片

## 结果排序
客餐厅 → 主卧 → 次卧 → 其他

## 接口文档
- 户型搜索：./docs/planSearch.md
- 户型图信息：./docs/floorplanInfo.md
- 生成方案：./docs/createDesign.md
- 硬装风格库：./docs/hardStyle.md
- 客户标签：./docs/customTag.md
- 智能布局：./docs/layout.md
- 布局结果：./docs/layoutResult.md
- 布局候选：./docs/layoutCandidates.md
- 渲染结果：./docs/renderResult.md
- 上传：./docs/upload.md
- 临摹导入：./docs/planUrlCreate.md
- 临摹轮询：./docs/planUrlCreateResult.md
- 版本校验：./docs/versionCheck.md