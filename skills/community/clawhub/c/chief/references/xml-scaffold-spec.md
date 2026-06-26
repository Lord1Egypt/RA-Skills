# XML 脚手架规范（v4.2 新增）

> Anthropic 训练模型时深度使用 XML 标签。用 XML 包裹 DiagnosisState 字段，比 Markdown 格式大幅降低早退率和跳脱风险。

---

## 核心原则

1. **每个字段必须用 XML `<tag>` 包裹**，禁止裸文本传递
2. **强制 `<scratchpad>`**：Step 6（综合）和 Step 7（建议）前，必须先写草稿区（≥300 字）
3. **嵌套结构反映思考层级**：父子标签对应思考的包含关系
4. **输出前 XML 校验**：检查所有必填标签是否闭合、是否存在

---

## 完整 XML 模板

```xml
<diagnosis>
  <!-- Step 1: 问题界定 -->
  <problem_definition>用一句话说清问题（不是现象）</problem_definition>
  <cynefin_domain>Simple|Complicated|Complex|Chaotic</cynefin_domain>
  
  <!-- Step 1.5: 苏格拉底审计 -->
  <socratic_audit>
    <status>pass|block</status>
    <gaps>仅 block 时填写：缺失维度说明</gaps>
    <questions>仅 block 时填写：3 个精准问题</questions>
  </socratic_audit>
  
  <!-- Step 2: 分解 -->
  <decomposition>
    <hypotheses>
      <hypothesis>假设 1</hypothesis>
      <hypothesis>假设 2</hypothesis>
      <hypothesis>假设 3</hypothesis>
    </hypotheses>
    <paths>
      <path name="结构视角">...</path>
      <path name="人性视角">...</path>
      <path name="环境视角">...</path>
    </paths>
  </decomposition>
  
  <!-- Step 3: 优先 -->
  <priorities>排序结果，含显性放弃说明</priorities>
  
  <!-- Step 4: 计划 -->
  <verification_plan>验证计划（数据需求+验证标准）</verification_plan>
  
  <!-- Step 5: 分析 -->
  <iceberg_analysis>
    <level1>事件：发生了什么</level1>
    <level2>模式：反复出现的趋势</level2>
    <level3>结构：什么机制导致模式</level3>
    <level4>心智：什么信念维持结构</level4>
  </iceberg_analysis>
  
  <!-- 原始推理（仅存储，不传递） -->
  <tot_paths_raw>完整推理日志</tot_paths_raw>
  
  <!-- 剪枝后断言集（Step 6 唯一输入） -->
  <step5_assertions>
    <assertion path="结构视角">
      <claim>断言 1</claim>
      <evidence>关键证据</evidence>
      <confidence>高|中|低</confidence>
    </assertion>
    <assertion path="人性视角">
      <claim>断言 1</claim>
      <evidence>关键证据</evidence>
      <confidence>高|中|低</confidence>
    </assertion>
    <assertion path="环境视角">
      <claim>断言 1</claim>
      <evidence>关键证据</evidence>
      <confidence>高|中|低</confidence>
    </assertion>
    <debate>
      <consensus>共识点</consensus>
      <divergence>分歧点</divergence>
      <blind_spot>盲点</blind_spot>
    </debate>
  </step5_assertions>
  <pruning_applied>true|false</pruning_applied>
  
  <!-- 草稿区（Step 6/7 前强制写，≥300 字） -->
  <scratchpad>
    <!-- 包含：逻辑推演、反证、取舍理由、代价分析、路径间交叉验证 -->
  </scratchpad>
  
  <!-- Step 6: 综合 -->
  <synthesis>综合结论（含路径间交叉验证）</synthesis>
  
  <!-- Step 7: 建议 -->
  <recommendations>
    <p0>
      <action>动作 1</action>
      <cost>代价</cost>
    </p0>
    <p0>
      <action>动作 2</action>
      <cost>代价</cost>
    </p0>
    <p1>
      <action>动作 1</action>
      <cost>代价</cost>
    </p1>
    <p2>
      <action>动作 1</action>
    </p2>
  </recommendations>
  
  <!-- 对抗性自检 -->
  <adversarial_check>结论最可能错在什么</adversarial_check>
  
  <!-- 引用标注 -->
  <citations>
    <citation>[劳动法.md:第47条]</citation>
    <citation>[company_policy.md:3.2.1]</citation>
  </citations>
  
  <!-- 质检结果 -->
  <quality_score>
    <item1>5</item1>
    <total>32/35</total>
  </quality_score>
  
  <!-- Constitutional Evaluator 批判 -->
  <critique>
    <issue code="R4" severity="high">问题描述</issue>
    <patch>修改指令</patch>
  </critique>
  <evaluator_result>pass|fail</evaluator_result>
  <refinement_target>需要修改的部分</refinement_target>
  <confidence>高|中|低</confidence>
</diagnosis>
```

---

## 必填标签校验清单

每个步骤完成后，用以下规则校验：

| 步骤 | 必填标签 | 校验规则 |
|------|---------|---------|
| Step 1 | `<problem_definition>`, `<cynefin_domain>` | 非空，cynefin 是枚举值之一 |
| Step 1.5 | `<socratic_audit>` 含 `<status>` | status 为 pass 或 block |
| Step 2 | `<decomposition>` 含 `<hypotheses>` | 至少 3 个 hypothesis |
| Step 3 | `<priorities>` | 非空，含显性放弃说明 |
| Step 4 | `<verification_plan>` | 非空 |
| Step 5 | `<iceberg_analysis>` 含 L1-L4 | 4 个层级都存在 |
| Step 5 剪枝 | `<step5_assertions>`, `<pruning_applied>` | S 级必须有 assertions |
| Step 6 | `<scratchpad>` + `<synthesis>` | scratchpad ≥300 字 |
| Step 7 | `<scratchpad>` + `<recommendations>` + `<adversarial_check>` + `<citations>` | 每个 p0/p1 必须有 cost |

---

## Scratchpad 强制规则

- **触发条件**：Step 6 和 Step 7 之前必须写
- **最小字数**：≥300 字
- **内容要求**：
  - Step 6 前：逻辑推演、路径间交叉验证、反证尝试
  - Step 7 前：取舍理由、代价分析、二阶效果推演
- **禁止**：将 `<scratchpad>` 内容输出给用户（这是内部思考）

---

## Constitutional Evaluator XML 格式

```xml
<critique>
  <issue code="R1|R2|R3|R4|S1|S2|S3|I1|I2" severity="critical|high|medium|low">
    具体问题描述
  </issue>
  <patch>
    具体修改指令，禁止"重新生成全文"
  </patch>
</critique>

<refinement_target>需要修改的 XML 节点路径</refinement_target>
```
