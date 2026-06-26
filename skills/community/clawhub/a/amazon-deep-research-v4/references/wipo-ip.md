# WIPO IP 合规审计 (V4 Mandatory)

## 规则

**每个Amazon产品分析必须包含IP合规检测，不可跳过。**
未通过IP检测的产品不能被标记为"合格"。
HIGH风险产品直接淘汰，不进入最终报告。

## 5步IP审计流程

### Step 1: 商标检索 (5 min)
- 工具: [WIPO Global Brand Database](https://branddb.wipo.int/)
- 搜索OEM品牌名 → Nice Class 12(车辆), 9(电子), 11(灯具)
- 确认listing标题使用 "Compatible with [Brand] [Model]" 格式
- Brand字段 = 卖家自有品牌 ONLY（不能填OEM品牌名）

### Step 2: 外观专利检索 (10 min)
- 工具: [Google Patents](https://patents.google.com/)
- 搜索: `[OEM Brand] [Part Type] design patent`
- 检查D前缀专利（<15年有效期）
- 如果产品外形与活跃外观专利高度相似 → 标记风险

### Step 3: 实用新型/发明专利检索 (10 min)
- 工具: [WIPO PATENTSCOPE](https://patentscope.wipo.int/) + [USPTO](https://ppubs.uspto.gov/)
- 按关键词 + IPC分类搜索:
  - B60Q = 车辆灯光
  - B62D = 底盘
  - F16D = 刹车
  - H02J = 充电
- 检查Amazon APEX历史记录

### Step 4: 认证合规检查
| 产品类型 | 必须认证 |
|----------|----------|
| LED大灯 | DOT/SAE |
| EV充电器 | UL 2594 + FCC + NEC 2026 |
| 排气系统 | EPA (cat-back legal) |
| 进气系统 | CARB Executive Order |
| 刹车组件 | FMVSS 135 + G3000 |
| 后视镜 | FMVSS 111 |
| 电子设备 | FCC Part 15 |
| CarPlay屏 | Apple MFi |

### Step 5: 风险评级
- 🟢 **LOW**: 无已知IP问题，标准上架
- 🟡 **MEDIUM**: 已知IP持有者存在，需设计差异化+安全listing语言
- 🔴 **HIGH**: 活跃专利/诉讼/执法，**直接淘汰**

## 自动HIGH风险品类

以下品类自动标记🔴HIGH，需IP律师审核后才能入选：
- 三折Tonneau Cover (Extang/BAK专利 US 9,815,358)
- Jump Starter (NOCO外观专利 D738,307S)
- OEM品牌诊断工具 (Autel/LAUNCH 仅授权经销)
- 无线CarPlay屏 (Apple MFi强制认证)
- OEM格栅复制品 (2025-2026 OEM外观专利执法趋势)

## Excel/HTML输出列

| 列名 | 内容 |
|------|------|
| IP Risk Level | 🟢/🟡/🔴 + 条件格式 |
| Key IP Risk | 具体专利号/商标/执法案例 |
| Required Cert | DOT/FCC/UL/CARB/FMVSS/EPA/MFi |
| Safe Listing | 推荐标题格式 + 设计差异化建议 |
