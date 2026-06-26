---
name: LDH Isoenzymes in Acute Myocardial Infarction Diagnosis
description: 基于急性心肌梗死（AMI）患者发病后12–48小时内的血清LDH同工酶检测结果，评估LDH₁/LDH₂比值及LDH₅水平以支持诊断和预后判断。当用户提供AMI病史及LDH同工酶分型数据时触发此技能。
metadata:
  openclaw:
    emoji: "❤️"
    skillKey: "ldh-isoenzymes-in-acute-myocardial-infarction-diagnosis"
---

# 急性心肌梗死中LDH同工酶的诊断应用

## 何时使用
- 患者确诊或疑似急性心肌梗死（AMI）
- 发病时间在12–48小时内
- 已完成血清LDH同工酶分型检测
- 不适用于非心源性胸痛或非心肌损伤情况

## 执行步骤
1. 确认AMI发病时间（小时数），确保在12–48小时窗口内。
2. 检查LDH₁与LDH₂比值：
   - 若LDH₁/LDH₂ > 1.0（正常为LDH₂ > LDH₁），支持AMI诊断。
   - 12–24小时内约50%患者出现此变化，48小时达80%。
3. 检查LDH₅是否增高：
   - 若LDH₅同时升高，提示可能合并心力衰竭导致的肝淤血或肝损伤，预后较差。
4. 结合其他心肌标志物（如cTnT、CK-MB）综合判断，因LDH升高较晚（8–18小时起，24–72小时达峰）。
5. 排除其他可致LDH₁升高的疾病（如恶性贫血）。

## 输出模板
若LDH₁/LDH₂>1.0且发病时间符合，则支持AMI诊断；若同时LDH₅↑，则提示预后不良。