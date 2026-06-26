---
name: citic-creditcard-auto-apply
description: 基于中信银行信用卡官网进行卡种推荐，并使用 OpenClaw browser 工具辅助预填官方申请表；默认停在最终提交前，需客户本人确认。
version: 3.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "💳"
    homepage: "https://creditcard.ecitic.com/"
---

# 中信银行信用卡自动申请（OpenClaw 原生改写版）

## 什么时候使用

当用户希望：

- 根据年龄、收入、消费习惯、出行偏好、权益诉求推荐中信信用卡；
- 查看官网当前仍可申请的卡种；
- 读取自己在 OpenClaw 工作区中**已授权**的申请资料；
- 用 OpenClaw 的 **browser** 工具打开官网申请页并预填资料；

就使用本 skill。

## 这版 skill 的实现方式

这不是一个“YAML steps 自动执行器”。

- `SKILL.md`：告诉 agent 何时调用哪些工具。
- `config/workflow.template.yaml`：只是流程模板和字段配置，不会被 OpenClaw 直接执行。
- `scripts/profile_extractor.py`：从工作区资料中提取候选申请字段。
- `scripts/build_application_plan.py`：把候选字段、推荐结果和预填边界整理成一个可执行计划 JSON。
- `browser` 工具：真正执行打开网页、快照、点击、输入。

## 硬规则

1. **只用中信银行信用卡官网和官网可达申请页作为产品与申请依据。**
2. **推荐与申请分两阶段进行。** 先推荐，再预填，不要一上来直接填表。
3. **默认只做预填，不做最终提交。**
4. **只有在用户明确授权时，才读取 `profiles/applicant_profile.json`、`USER.md`、`MEMORY.md`、`memory/*.md`。**
5. **从工作区读取到的内容都只是候选值。** 必须展示来源并让用户确认。
6. **不要猜测或伪造敏感信息。** 包括身份证号、手机号、收入、单位、地址等。
7. **验证码、短信 OTP、人脸识别、征信授权、协议勾选、最终提交，一律交给用户本人完成。**
8. **如果官网表单与本地数据不一致，以官网实时页面为准。**
9. **优先使用 OpenClaw 托管浏览器 profile `openclaw`。** 只有用户明确要求复用当前登录态时，才考虑 `user` profile。

## 推荐阶段

### 1）准备客户画像

优先收集：

- 年龄
- 月收入 / 年收入
- 是否有稳定单位与职业信息
- 是否常做餐饮、网购、航旅、酒店、车主、境外消费
- 航司 / 酒店偏好
- 所需权益（积分、里程、酒店、航延险、车主权益、境外返现等）
- 年费容忍度

### 2）先看本地数据与模板

优先读取：

- `data/card_catalog.json`
- `profiles/applicant_profile.json`（若存在）
- `profiles/applicant_profile.template.json`

### 3）推荐命令

```bash
python3 scripts/citic_cc_advisor.py recommend --profile profiles/applicant_profile.template.json
```

如果要产出结构化结果：

```bash
python3 scripts/citic_cc_advisor.py recommend --profile profiles/applicant_profile.template.json --format json
```

### 4）推荐输出要求

必须包含：

- 推荐 TOP 3
- 每张卡的适配原因
- 风险提示 / 限制条件
- 官网详情页 / 申请页
- 明确写出“最终批核、额度、权益解释以官网和审批结果为准”

## 申请阶段（browser 工具执行）

### A. 先生成候选资料

```bash
python3 scripts/profile_extractor.py --workspace . --json
```

或生成完整执行计划：

```bash
python3 scripts/build_application_plan.py   --workspace .   --workflow config/workflow.template.yaml   --out output/application_plan.json
```

### B. 先向用户确认候选字段

必须展示：

- 字段名
- 脱敏预览
- 来源文件
- 置信度

只有用户确认后的字段才能用于填表。

### C. browser 工具的推荐顺序

1. 打开官网或目标卡的申请页。
2. 先做 `snapshot`，拿到页面 ref。
3. 通过 ref 点击“立即申请/申请/办卡”等按钮。
4. 再 `snapshot` 新页面，识别表单字段。
5. 仅填写已经确认的字段。
6. 遇到验证码、OTP、协议勾选、最终提交时停止。

### D. browser 填表原则

- 尽量用页面 ref，而不是脆弱的文本选择器。
- 每进入新页面或发生跳转后，都重新 snapshot。
- 动态表单或 iframe 先确认上下文，再填值。
- 对于官网未明确显示的字段，不要强行猜测映射。
- 若必填字段缺失，立即停止并提示用户补充。

## 建议的对话/执行流程

1. 收集客户画像。
2. 生成推荐结果并让用户选定卡片。
3. 用户授权读取本地资料。
4. 生成候选字段和预填计划。
5. 使用 browser 工具进入官网申请页。
6. 逐页预填并停在最终提交前。
7. 提示用户本人核对并完成最终提交。

## 文件说明

- `config/workflow.template.yaml`：把你原先的 YAML 改写成“流程模板”，供脚本或人工读取。
- `scripts/build_application_plan.py`：把 workflow、推荐结果、候选字段组装成 JSON 计划。
- `scripts/profile_extractor.py`：抽取待确认字段。
- `scripts/citic_cc_advisor.py`：推荐卡种，支持 markdown / json 两种格式。

## 不要这样做

- 不要把 `workflow.template.yaml` 当成 OpenClaw 原生可执行步骤。
- 不要静默读取并外发用户全部 memory。
- 不要自动勾选授权、征信、协议条款。
- 不要自动最终提交信用卡申请。
