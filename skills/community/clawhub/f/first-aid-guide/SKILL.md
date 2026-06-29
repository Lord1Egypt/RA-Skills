---
name: first-aid-guide
description: >
  AI急救指南 — 覆盖心肺复苏CPR+AED、海姆立克急救法、止血包扎、骨折固定、
  烧伤、中毒、中暑、失温、癫痫、心梗卒中识别、溺水、动物咬伤、户外急救、
  家庭急救包配置、急救证获取等15+类急救场景的全流程指导。
  This skill should be used when the user asks about first aid, CPR, AED,
  Heimlich maneuver, choking, bleeding, bandaging, fracture, burn treatment,
  poisoning, heat stroke, hypothermia, seizure, heart attack, stroke, drowning,
  animal/snake bite, outdoor/wilderness first aid, first aid kit, or first aid
  certification (Red Cross/AHA). Trigger words: 急救, CPR, 心肺复苏, AED, 海姆立克,
  止血, 包扎, 骨折, 烧伤, 中毒, 中暑, 失温, 癫痫, 心梗, 卒中, 中风, 溺水, 咬伤,
  蛇咬, 蜂蛰, 户外急救, 急救包, 急救证, 红十字会, AHA急救.
agent_created: true
---

# AI急救指南 — First Aid Guide

## 核心原则

在提供任何急救信息前，必须在回复开头明确输出以下免责声明：

> ⚠️ **重要提醒**：以下内容为急救知识参考，不能替代专业急救培训和120急救服务。如遇紧急情况，请立即拨打120。具体操作可能因AHA/ERC等最新指南更新而有差异，建议参加正规急救培训。

---

## 技能概述

本技能覆盖15+类常见急救场景，通过参考文件库提供结构化的急救知识。
根据用户问题自动匹配对应主题，从`references/`目录加载专业知识，
输出结构清晰的操作步骤、禁忌提醒和就医指征。

---

## 参考文件索引

根据用户问题中的关键词，加载对应的参考文件：

| 用户问题关键词 | 加载文件 | 覆盖内容 |
|---------------|----------|----------|
| CPR、心肺复苏、AED、心脏骤停、除颤 | `references/cpr-aed.md` | 成人/儿童/婴儿CPR标准流程、AED使用、高质量CPR指标 |
| 海姆立克、噎住、窒息、气道梗阻、卡住 | `references/heimlich.md` | 成人/婴儿/孕妇/自救方法、背部拍击+胸部冲击 |
| 出血、止血、包扎、骨折、断肢、扭伤 | `references/trauma.md` | 三类出血识别、止血带使用、包扎方法、各部位骨折固定、脊柱保护 |
| 烧伤、烫伤、化学烧伤、电烧伤 | `references/burns.md` | 三度四分法、冲脱泡盖送、化学/电烧伤专项处理、禁忌 |
| 中毒、误食、一氧化碳、食物中毒、农药 | `references/poisoning.md` | 通用原则、各类中毒专项处理、催吐禁忌 |
| 中暑、热射病、失温、低体温、溺水 | `references/environmental.md` | 中暑分型急救、失温分度复温、溺水CPR（先通气后按压）|
| 癫痫、抽搐、心梗、胸痛、中风、卒中 | `references/medical-emergency.md` | 癫痫五要五不要、FAST卒中识别、心梗急救用药禁忌 |
| 狗咬、猫咬、狂犬、蛇咬、蜂蛰、蜱虫、水母、户外、雷电、高反 | `references/bites-outdoor.md` | 狂犬病暴露分级、蛇咬急救、蜱虫取除、高山病识别、SOS求救 |
| 急救包、急救箱、急救证、红十字会、AHA | `references/kit-certification.md` | 家庭急救包分级清单、红十字/AHA急救证获取流程、维护检查表 |

如用户问题涉及多个主题，加载多个相关文件进行综合分析。

---

## 工作流程

### Step 1: 解析用户意图

从用户输入中提取关键信息：
- **紧急类型**：是什么急救场景？（如 "被狗咬了" → 动物咬伤）
- **患者信息**（如有）：年龄（成人/儿童/婴儿）、特殊状况（孕妇、老人、有慢性病）
- **场景信息**（如有）：户外/家中/车内等

### Step 2: 加载对应参考文件

根据上述索引表，使用 Read 工具加载对应的 `references/*.md` 文件。
如不确定，加载最相关的2-3个文件。

### Step 3: 输出结构化的急救指导

按以下结构组织回复：

1. ⚠️ **免责声明**（必须）
2. **场景识别**：快速定位问题类型，列出关键特征
3. **分步操作**：
   - 用 ✅/❌ 区分正确和错误做法
   - 用表格呈现关键参数（如CPR深度、频率）
   - 标注 ⚠️ 高风险操作
4. **需要就医的指征**：明确列出什么情况必须就医
5. **常见误区**：列出最常见的2-3个错误做法

### Step 4: 需要时生成交互式HTML报告

如用户明确请求"生成报告"、"给我一份可视化指南"或查询内容非常复杂（如多场景对比、完整急救包清单），生成交互式HTML可视化报告。

#### HTML报告设计规范

**配色方案**（急救主题 — 红十字风格）：
- 主色：`#D32F2F`（急救红）
- 背景：`#FAFAFA` → `#FFF5F5`
- 内容卡片：白色 `#FFFFFF`，阴影 `box-shadow: 0 2px 12px rgba(0,0,0,0.06)`
- 文字：`#333333`（正文）、`#666666`（辅助）
- 警告块：红色左边框 `border-left: 4px solid #D32F2F`，背景 `#FFF0F0`
- 正确操作块：绿色左边框 `border-left: 4px solid #4CAF50`，背景 `#F0FFF0`

**报告结构**：
1. 标题区：场景名称 + 红十字图标(🏥/➕) + 紧急程度标签（🟢一般/🟡紧急/🔴致命）
2. 核心步骤区：卡片式步骤，每步用大号数字标识，关键操作高亮
3. 干货对比区：✅正确 vs ❌错误，双列对比布局
4. 就医指征区：带图标列表
5. 页脚免责声明

**交互特性**：
- 步骤区支持点击展开/收起详情
- 使用纯HTML+CSS+JS，无外部依赖
- 响应式布局，手机可读
- 打印友好：`@media print` 隐藏交互元素

#### HTML 报告模板参考

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>急救指南 — [场景名称]</title>
<style>
  /* 急救主题配色 */
  :root {
    --primary: #D32F2F;
    --primary-light: #FFF0F0;
    --success: #4CAF50;
    --success-light: #F0FFF0;
    --warning: #FF9800;
    --warning-light: #FFF8E1;
    --bg: #FAFAFA;
    --card: #FFFFFF;
    --text: #333;
    --text-secondary: #666;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; padding: 20px; }
  .container { max-width: 800px; margin: 0 auto; }
  
  /* 标题 */
  .header { text-align: center; padding: 30px 20px; background: linear-gradient(135deg, var(--primary), #B71C1C); color: white; border-radius: 16px; margin-bottom: 24px; }
  .header h1 { font-size: 28px; margin-bottom: 8px; }
  .header .urgency { display: inline-block; padding: 4px 16px; border-radius: 20px; font-size: 14px; margin-top: 8px; }
  .urgency.critical { background: rgba(255,255,255,0.25); }
  .urgency.urgent { background: rgba(255,255,255,0.2); }
  .urgency.general { background: rgba(255,255,255,0.15); }
  
  /* 免责声明 */
  .disclaimer { background: var(--warning-light); border-left: 4px solid var(--warning); padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; color: #E65100; }
  
  /* 步骤卡片 */
  .step { background: var(--card); border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); cursor: pointer; }
  .step-header { display: flex; align-items: center; gap: 12px; }
  .step-num { width: 36px; height: 36px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; flex-shrink: 0; }
  .step-title { font-size: 18px; font-weight: 600; flex: 1; }
  .step-arrow { transition: transform 0.3s; font-size: 12px; }
  .step.open .step-arrow { transform: rotate(180deg); }
  .step-body { display: none; margin-top: 16px; padding-top: 16px; border-top: 1px solid #F0F0F0; }
  .step.open .step-body { display: block; }
  
  /* 对比 */
  .do-dont { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
  .do { background: var(--success-light); border-left: 4px solid var(--success); padding: 16px; border-radius: 8px; }
  .dont { background: var(--primary-light); border-left: 4px solid var(--primary); padding: 16px; border-radius: 8px; }
  .do h4 { color: var(--success); margin-bottom: 8px; }
  .dont h4 { color: var(--primary); margin-bottom: 8px; }
  
  /* 就医指征 */
  .when-to-see-doctor { background: var(--warning-light); border-radius: 12px; padding: 20px 24px; margin-top: 24px; }
  .when-to-see-doctor h3 { color: #E65100; margin-bottom: 12px; }
  .when-to-see-doctor ul { list-style: none; padding: 0; }
  .when-to-see-doctor li { padding: 6px 0; padding-left: 20px; position: relative; }
  .when-to-see-doctor li::before { content: "⚠️"; position: absolute; left: 0; }
  
  /* 页脚 */
  .footer { text-align: center; padding: 24px; color: var(--text-secondary); font-size: 13px; margin-top: 32px; border-top: 1px solid #E0E0E0; }
  
  @media print {
    .step-body { display: block !important; }
    .step-arrow { display: none; }
    body { background: white; }
  }
  
  @media (max-width: 600px) {
    .do-dont { grid-template-columns: 1fr; }
    .header h1 { font-size: 22px; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🏥 [场景名称] 急救指南</h1>
    <div class="urgency [critical/urgent/general]">[紧急程度标签]</div>
  </div>
  
  <div class="disclaimer">
    ⚠️ <strong>免责声明</strong>：以下内容为急救知识参考，不能替代专业急救培训和120急救服务。如遇紧急情况，请立即拨打120。
  </div>
  
  <!-- [步骤内容] -->
  
  <div class="when-to-see-doctor">
    <h3>🏥 必须就医的情况</h3>
    <ul>
      <!-- [就医指征列表] -->
    </ul>
  </div>
  
  <div class="footer">
    <p>本文内容仅供参考，不能替代专业急救培训</p>
    <p>建议参加中国红十字会或AHA（美国心脏协会）急救培训课程</p>
  </div>
</div>

<script>
// 步骤展开/收起交互
document.querySelectorAll('.step').forEach(step => {
  step.addEventListener('click', () => step.classList.toggle('open'));
});
</script>
</body>
</html>
```

---

## 安全准则（强制遵守）

### 绝对禁止提供的操作

1. **不要在无医疗指征情况下建议切开气管/环甲膜穿刺等高级操作**
2. **不要建议使用未经批准的民间偏方**
3. **不要对婴儿推荐海姆立克腹部冲击法**
4. **不要建议在不确定毒物类型时盲目催吐**

### 必须强调的要点

1. 在任何回复中强调"拨打120"
2. 明确区分"现场急救"和"需要医生处理"的边界
3. 指出常见错误做法及其后果
4. 如患者信息不足，先询问关键信息（年龄、意识状态、有无特殊病史）

---

## 回复风格

- **直接、结构化**：避免冗长叙述，用表格和列表呈现关键信息
- **口语化但专业**：用"捏住鼻翼"而不是"闭塞鼻孔"，用"向上冲击"而不是"向上施力"
- **强调禁忌**：用 ⚠️ 和粗体标出致命错误操作
- **必要时追问**：如用户描述不清晰（"我奶奶不舒服"），追问关键信息
