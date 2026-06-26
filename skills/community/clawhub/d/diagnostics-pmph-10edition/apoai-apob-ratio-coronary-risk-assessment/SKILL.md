---
name: apoai-apob-ratio-coronary-risk-assessment
description: 根据血清载脂蛋白AI（apoAI）和载脂蛋白B（apoB）浓度计算其比值，用于评估冠心病及动脉粥样硬化风险。当用户已获得apoAI和apoB的检测结果（单位：g/L），且无急性炎症、严重肝肾功能衰竭等干扰因素时，应使用本技能进行风险判断。
metadata:
  openclaw:
    emoji: "🩺"
    skillKey: "apoai-apob-ratio-coronary-risk-assessment"
---

# 载脂蛋白AI/B比值冠心病风险评估

## 适用条件
- 已分别测定血清apoAI和apoB浓度（单位：g/L）
- 患者处于非急性状态（无急性炎症、创伤或严重肝肾功能衰竭）

## 执行步骤
1. 获取血清载脂蛋白AI（apoAI）浓度。
2. 获取血清载脂蛋白B（apoB）浓度。
3. 计算比值：`ratio = apoAI / apoB`。
4. 判断风险：
   - 若比值 < 1，提示显著冠心病风险升高；
   - 正常参考区间为1~2，但该比值随年龄增长自然降低。
5. 结合临床背景综合评估，尤其在糖尿病、高脂血症、肥胖等代谢性疾病患者中更需关注比值降低。

> **注意**：该比值优于传统血脂指标（如TC、TG、HDL、LDL），因其直接反映HDL与LDL颗粒数量的平衡，而非易受病理状态影响的胆固醇含量。

## 触发场景
- 用户提供apoAI和apoB数值并询问心血管风险
- 需要解释apoAI/apoB比值的临床意义
- 对比传统血脂指标与载脂蛋白指标的预测价值