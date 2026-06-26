# Business Blueprint Schema 设计原则与扩展性指南

## 一、核心问题：为什么当前文档需要重构

### 问题1：Schema文档职责混淆

**当前问题**：
- `systems-schema.md` 混入了渲染逻辑（导出布局路由规则）
- `entities-schema.md` 混入了业务规则（自动分层推断）
- Schema文档变成了"数据模型 + 业务规则 + 渲染决策"的混合体

**正确职责划分**：

| 文档类型 | 职责 | 内容范围 |
|---------|------|---------|
| **Schema文档** | 数据结构定义 | 字段含义、类型约束、基础示例 |
| **规则文档** | 业务规则定义 | 分类策略、推断逻辑、约束条件 |
| **配置文档** | 可配置规则 | 用户可修改的分层策略、命名映射 |
| **渲染文档** | 渲染决策逻辑 | 路由策略、视图选择、布局规则 |

**重构建议**：
- Schema文档：只定义 `systems` 有哪些字段、`category` 的枚举值
- 分层规则：移到独立的 `layer-strategies.md`（可配置）
- 渲染决策：保留在 `export_routes.py` 代码中（实现细节）

---

### 问题2：分层规则写得太死

**当前问题**：
```markdown
| 名称关键词 | 推断层级 |
|-----------|---------|
| 客户端、前端、APP | 访问入口层 |  ← 硬编码关键词
| 网关、接入、Gateway | 接入网关层 |  ← 约束特定命名
```

**后果**：
- 无法适应其他行业（制造业："工厂层"、"仓储层"、"配送层"）
- 无法适应其他视角（数据蓝图："采集层"、"处理层"、"应用层"）
- 用户无法自定义分层策略

**正确做法**：

#### 分层策略应该是可配置的，而非硬编码

```json
{
  "layerStrategy": "product-capability",  // 用户选择策略
  "strategyConfig": {
    "layers": [
      {"id": "L1", "name": "用户接入层", "keywords": ["客户端", "APP", "小程序"]},
      {"id": "L2", "name": "服务网关层", "keywords": ["网关", "Gateway", "API"]}
    ],
    "fallback": "未分层"  // 未匹配时的默认层
  }
}
```

#### 提供多种预定义策略（用户选择，而非强制）

| 策略名称 | 适用场景 | 分层逻辑 |
|---------|---------|---------|
| `product-capability` | 产品蓝图 | 按产品价值层次（用户接入→平台能力→核心业务） |
| `technical-architecture` | 技术蓝图 | 按技术调用链路（Frontend→Backend→Database） |
| `business-domain` | 业务蓝图 | 按业务域划分（采购域→销售域→财务域） |
| `data-governance` | 数据蓝图 | 按数据生命周期（采集→处理→应用） |
| `organizational` | 组织蓝图 | 按组织架构（事业部→部门→小组） |
| `industry-supply-chain` | 制造业蓝图 | 按供应链环节（原材料→生产→仓储→配送） |
| `custom` | 用户自定义 | 用户配置 keywords → layers 映射 |

---

### 问题3：缺乏场景覆盖

**当前问题**：
只考虑了"产品蓝图"和"技术蓝图"两种场景，缺少：

1. **行业特定蓝图**：
   - 金融业：监管合规层、风控层、核心交易层、客户服务层
   - 制造业：供应商管理→生产执行→质量管控→仓储物流→销售配送
   - 零售业：门店运营→会员管理→供应链→数据分析

2. **业务视角蓝图**：
   - 业务域蓝图：按业务域分层（CRM域、ERP域、OA域）
   - 数据治理蓝图：按数据分层（数据源→数据湖→数据仓库→数据应用）
   - 组织架构蓝图：按部门分层（销售部→市场部→财务部）

3. **决策蓝图**：
   - 决策流程蓝图：按决策层级分层（战略决策→战术决策→运营决策）
   - 风险管控蓝图：按风险类型分层（合规风险→运营风险→财务风险）

**解决方案**：
- Schema文档只定义通用数据模型（category: layer/service）
- 提供多种预定义分层策略（用户选择）
- 允许用户自定义分层策略（通过配置文件）

---

### 问题4：缺乏扩展性设计

**当前问题**：
- 没有说明如何添加新的 `category` 类型
- 没有说明如何添加新的分层策略
- 所有规则硬编码，用户无法修改

**扩展性设计原则**：

#### 1. Schema的可扩展性

**当前枚举约束太死**：
```json
{
  "category": {"enum": ["layer", "service"]}  // ← 只能这两种？
}
```

**扩展设计**：
```json
{
  "category": {
    "type": "string",
    "description": "系统分类类型",
    "suggestedValues": ["layer", "service", "platform", "domain", "region", "organization"],
    "customAllowed": true  // ← 允许用户自定义
  }
}
```

#### 2. 分层策略的可扩展性

**提供分层策略配置文件**：

```
scripts/business_blueprint/configs/layer_strategies/
├── product-capability.json       # 产品能力分层策略
├── technical-architecture.json   # 技术架构分层策略
├── business-domain.json          # 业务域分层策略
├── manufacturing-supply-chain.json # 制造业供应链分层策略
├── finance-regulatory.json       # 金融监管分层策略
└── custom-example.json           # 自定义策略模板
```

**配置文件格式**：
```json
{
  "strategyId": "product-capability",
  "strategyName": "产品能力分层",
  "description": "按产品价值层次分层，适用于产品蓝图",
  "layers": [
    {
      "id": "L1",
      "name": "用户接入层",
      "keywords": ["客户端", "APP", "小程序", "前端"],
      "description": "用户访问系统的入口层"
    },
    {
      "id": "L2",
      "name": "服务网关层",
      "keywords": ["网关", "Gateway", "API网关", "接入层"],
      "description": "流量控制、认证鉴权等网关能力"
    }
  ],
  "fallbackLayer": "未分层",
  "priority": ["exact_match", "keyword_match", "category_inference"]
}
```

#### 3. 用户自定义扩展

**用户可以创建自己的分层策略**：

```bash
# 用户创建自定义策略
python scripts/business_blueprint/cli.py \
  --strategy-create custom-strategy.json \
  --from "制造业供应链蓝图"
```

**或者在Blueprint中直接指定**：

```json
{
  "editor": {
    "layerStrategy": "custom",
    "customLayers": [
      {"id": "L1", "name": "供应商管理层", "keywords": ["供应商", "采购"]},
      {"id": "L2", "name": "生产执行层", "keywords": ["生产", "工厂", "车间"]}
    ]
  }
}
```

---

### 问题5：缺乏专业性

**当前问题**：
- 缺乏蓝图视角的决策指导（什么时候用产品蓝图、什么时候用技术蓝图）
- 缺乏行业实践的参考（不同行业的分层实践）
- 缺乏分层原则（如何判断一个系统应该属于哪一层）

**专业性提升方向**：

#### 1. 蓝图视角决策指南

| 用户场景 | 推荐蓝图视角 | 分层策略 | 示例 |
|---------|------------|---------|------|
| **产品规划** | 产品能力视角 | `product-capability` | 展示产品功能价值层次 |
| **技术架构评审** | 技术架构视角 | `technical-architecture` | 展示技术调用链路和依赖 |
| **业务域规划** | 业务域视角 | `business-domain` | 展示业务域划分和边界 |
| **数据治理设计** | 数据治理视角 | `data-governance` | 展示数据流转和治理层级 |
| **组织架构梳理** | 组织视角 | `organizational` | 展示部门职责和协作关系 |
| **制造业供应链** | 供应链视角 | `industry-supply-chain` | 展示从原材料到交付的全链路 |
| **金融合规监管** | 监管视角 | `finance-regulatory` | 展示监管要求与业务隔离 |

#### 2. 分层决策原则（不是硬编码规则）

**原则1：价值层次原则**（产品蓝图）
- 上层：用户直接接触的价值（用户接入层）
- 中层：平台支撑价值（平台基础层、平台能力层）
- 下层：核心业务价值（核心业务层）
- 底层：基础设施价值（数据存储层）

**原则2：调用链路原则**（技术蓝图）
- 左侧：请求发起端（Frontend）
- 中间：请求处理端（Backend）
- 右侧：数据存储端（Database）

**原则3：业务域边界原则**（业务蓝图）
- 每一层是一个业务域（CRM域、ERP域、OA域）
- 域之间通过接口协作，不直接耦合

**原则4：数据生命周期原则**（数据蓝图）
- 数据产生层（采集层）
- 数据处理层（处理层）
- 数据应用层（应用层）

**原则5：组织职责原则**（组织蓝图）
- 战略层（高管团队）
- 战术层（部门负责人）
- 执行层（一线员工）

#### 3. 行业实践参考（不是强制约束）

**金融行业分层实践**：
```json
{
  "strategyId": "finance-regulatory",
  "layers": [
    {"id": "L1", "name": "监管合规层", "keywords": ["监管", "合规", "审计"]},
    {"id": "L2", "name": "风险控制层", "keywords": ["风控", "风险评估", "预警"]},
    {"id": "L3", "name": "核心交易层", "keywords": ["交易", "账户", "结算"]},
    {"id": "L4", "name": "客户服务层", "keywords": ["客户", "CRM", "营销"]}
  ]
}
```

**制造业分层实践**：
```json
{
  "strategyId": "manufacturing-supply-chain",
  "layers": [
    {"id": "L1", "name": "供应商管理", "keywords": ["供应商", "采购", "原材料"]},
    {"id": "L2", "name": "生产执行", "keywords": ["生产", "工厂", "车间", "MES"]},
    {"id": "L3", "name": "质量管控", "keywords": ["质检", "QA", "品控"]},
    {"id": "L4", "name": "仓储物流", "keywords": ["仓库", "WMS", "配送", "运输"]},
    {"id": "L5", "name": "销售分销", "keywords": ["销售", "分销", "渠道"]}
  ]
}
```

---

## 二、重构方案

### 文档结构重构

#### 1. Schema文档职责清晰化

**`references/entities-schema.md`（数据模型定义）**：
- 只定义字段含义、类型约束
- 不包含业务规则
- 不包含渲染逻辑
- 提供基础示例（不是最佳实践）

**`references/systems-schema.md`（数据模型定义）**：
- 只定义 `systems` 的字段含义
- 只定义 `category` 的基础分类（layer/service）
- 不包含自动推断规则
- 不包含导出路由规则

#### 2. 分层策略独立文档

**新建 `references/layer-strategies.md`（分层策略库）**：
- 提供多种预定义分层策略
- 说明每种策略的适用场景
- 提供决策指南（何时选择哪种策略）
- 提供"如何自定义策略"的说明

#### 3. 行业实践独立文档

**新建 `references/industry-practices.md`（行业实践参考）**：
- 金融行业分层实践
- 制造业分层实践
- 零售业分层实践
- 其他行业参考
- 明确标注："参考实践，非强制约束"

#### 4. 配置文件系统

**新建 `scripts/business_blueprint/configs/layer_strategies/` 目录**：
- 存放预定义策略配置文件（JSON格式）
- 用户可复制修改，创建自定义策略
- 代码读取策略配置，而非硬编码推断逻辑

---

### 代码重构方向

#### 1. 分层推断逻辑改为可配置

**当前硬编码逻辑**（`export_svg.py`）：
```python
def _infer_layer_from_system_name(name: str, category: str | None = None) -> str:
    if "客户端" in name: return "访问入口层"  # ← 硬编码
    if "网关" in name: return "接入网关层"    # ← 硬编码
```

**重构为可配置逻辑**：
```python
def _infer_layer_from_system_name(
    name: str,
    category: str | None = None,
    strategy: dict | None = None  # ← 从配置文件加载
) -> str:
    if not strategy:
        strategy = load_default_strategy()  # ← 默认策略可配置

    # 按策略优先级匹配
    for layer in strategy["layers"]:
        if any(keyword in name for keyword in layer["keywords"]):
            return layer["name"]

    return strategy["fallbackLayer"]
```

#### 2. 策略选择机制

**Blueprint中允许指定策略**：
```json
{
  "editor": {
    "layerStrategy": "product-capability",  // ← 用户选择
    "customLayers": []  // ← 用户自定义（可选）
  }
}
```

**CLI支持策略参数**：
```bash
python scripts/business_blueprint/cli.py \
  --export blueprint.json \
  --strategy product-capability  # ← 用户指定策略
```

---

## 三、扩展性设计清单

### 1. Schema可扩展性

- ✅ `category` 允许自定义值（不仅仅是 layer/service）
- ✅ `layer` 字段允许任意值（不强制6层结构）
- ✅ 新增 `properties` 字段存储扩展属性

### 2. 分层策略可扩展性

- ✅ 提供多种预定义策略（用户选择）
- ✅ 用户可创建自定义策略（配置文件）
- ✅ 策略可继承和组合（如：product-capability + finance-regulatory）

### 3. 行业实践可扩展性

- ✅ 提供行业实践参考（非强制约束）
- ✅ 用户可提交行业实践模板（社区贡献）
- ✅ 行业实践与分层策略分离（用户可选择组合）

### 4. 渲染逻辑可扩展性

- ✅ 路由策略可配置（不硬编码优先级）
- ✅ 布局规则可参数化（间距、颜色、字体等）
- ✅ 用户可创建自定义渲染模板

### 5. 工作流可扩展性

- ✅ 支持多阶段蓝图（初稿→评审→定稿）
- ✅ 支持蓝图演化（版本管理、变更追踪）
- ✅ 支持蓝图协作（多人编辑、评论审批）

---

## 四、实施步骤

### Phase 1：文档重构（优先级：高）

1. **重构 `entities-schema.md`**：
   - 移除业务规则和渲染逻辑
   - 只保留数据模型定义
   - 添加扩展性说明

2. **重构 `systems-schema.md`**：
   - 移除自动推断规则
   - 移除导出路由规则
   - 只保留字段定义和基础分类
   - 添加扩展性说明

3. **新建 `layer-strategies.md`**：
   - 提供多种预定义策略
   - 说明决策指南
   - 提供自定义方法

4. **新建 `industry-practices.md`**：
   - 提供行业实践参考
   - 明确标注"参考而非强制"

### Phase 2：配置文件系统（优先级：中）

1. **创建策略配置目录**：
   ```
   scripts/business_blueprint/configs/layer_strategies/
   ```

2. **提供预定义策略配置文件**：
   - product-capability.json
   - technical-architecture.json
   - business-domain.json
   - manufacturing-supply-chain.json

3. **提供自定义策略模板**：
   - custom-example.json（用户可复制修改）

### Phase 3：代码重构（优先级：中）

1. **重构 `_infer_layer_from_system_name`**：
   - 从配置文件读取策略
   - 支持用户自定义策略

2. **支持Blueprint指定策略**：
   - 读取 `editor.layerStrategy` 字段
   - 读取 `editor.customLayers` 字段

3. **CLI支持策略参数**：
   - 新增 `--strategy` 参数
   - 新增 `--strategy-create` 命令

### Phase 4：行业实践扩展（优先级：低）

1. **提供行业实践模板**：
   - 金融业模板
   - 制造业模板
   - 零售业模板

2. **建立行业实践贡献机制**：
   - 社区提交模板流程
   - 模板评审标准

---

## 五、关键原则总结

### 1. Schema文档职责单一
- 只定义数据结构，不包含业务规则或渲染逻辑

### 2. 分层策略可配置
- 提供多种预定义策略（用户选择，而非强制）
- 允许用户自定义策略（配置文件）

### 3. 规则是参考，不是约束
- 行业实践是参考，非强制
- 分层原则是指导，非硬编码

### 4. 扩展性优于完备性
- 不追求"覆盖所有场景"
- 而追求"用户可以自定义扩展"

### 5. 专业性体现在决策指导
- 不是给用户固定答案
- 而是提供决策原则和方法

---

## 六、后续讨论点

1. **策略配置文件格式是否合理？**
   - 当前设计：JSON格式，包含 layers、keywords、fallback
   - 是否需要更复杂的匹配规则（正则、优先级、权重）？

2. **Blueprint中如何指定策略？**
   - 当前设计：`editor.layerStrategy` 字段
   - 是否需要更灵活的机制（蓝图级别 vs 导出级别）？

3. **行业实践是否需要版本管理？**
   - 行业实践会随时间演进
   - 是否需要版本管理机制？

4. **自定义策略的验证机制？**
   - 用户创建自定义策略时，如何验证有效性？
   - 是否需要策略测试工具？

---

**文档创建日期**：2026-04-25
**状态**：待讨论
**下一步**：等待用户反馈，确认重构方向