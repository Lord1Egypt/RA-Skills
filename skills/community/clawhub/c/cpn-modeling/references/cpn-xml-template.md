# CPN XML 模板参考（CPN Tools 4.x 兼容）

示例场景：餐厅点餐流程（与 `example-restaurant.md` 对应）

## 完整模板

```xml
<?xml version="1.0" encoding="utf-8"?>
<workspaceElements>
  <cpnet>

    <!-- ── 颜色集合（全局定义）── -->
    <globbox>
      <block id="ID1">
        <id>ColorSets</id>
        <color id="ID2">
          <id>OrderType</id>
          <enum>
            <id>堂食</id>
            <id>外卖</id>
          </enum>
        </color>
        <color id="ID3">
          <id>DishType</id>
          <enum>
            <id>热菜</id>
            <id>冷菜</id>
            <id>饮品</id>
          </enum>
        </color>
        <color id="ID4">
          <id>StockStatus</id>
          <enum>
            <id>充足</id>
            <id>不足</id>
          </enum>
        </color>
      </block>
    </globbox>

    <!-- ── 点餐阶段（Page 1）── -->
    <page id="PAGE1">
      <pageattr name="点餐阶段"/>

      <place id="P1">
        <posattr x="100" y="150"/>
        <text>顾客_待点餐</text>
        <type><id>OrderType</id></type>
        <initmark><text>1`堂食</text></initmark>
      </place>
      <place id="P2">
        <posattr x="350" y="150"/>
        <text>订单_已接收</text>
        <type><id>OrderType</id></type>
        <initmark><text>empty</text></initmark>
      </place>

      <!-- 库存资源库所（初始有 token，否则扣减变迁死锁）-->
      <place id="P8">
        <posattr x="100" y="300"/>
        <text>库存_充足</text>
        <type><id>StockStatus</id></type>
        <initmark><text>1`充足</text></initmark>
      </place>
      <place id="P9">
        <posattr x="350" y="300"/>
        <text>库存_已扣减</text>
        <type><id>StockStatus</id></type>
        <initmark><text>empty</text></initmark>
      </place>

      <trans id="T1">
        <posattr x="225" y="150"/>
        <text>接单</text>
        <condition><text>true</text></condition>
      </trans>
      <!-- DEP4: arc_sequence — 库存链内顺序，token 自然流动 -->
      <trans id="T6">
        <posattr x="225" y="300"/>
        <text>扣减库存</text>
        <condition><text>true</text></condition>
      </trans>

      <arc id="A1" orientation="PtoT">
        <transend idref="T1"/><placeend idref="P1"/>
        <annot><text>1`堂食</text></annot>
      </arc>
      <arc id="A2" orientation="TtoP">
        <transend idref="T1"/><placeend idref="P2"/>
        <annot><text>1`堂食</text></annot>
      </arc>
      <arc id="A11" orientation="PtoT">
        <transend idref="T6"/><placeend idref="P8"/>
        <annot><text>1`充足</text></annot>
      </arc>
      <arc id="A12" orientation="TtoP">
        <transend idref="T6"/><placeend idref="P9"/>
        <annot><text>1`充足</text></annot>
      </arc>
    </page>

    <!-- ── 备餐阶段（Page 2）── -->
    <page id="PAGE2">
      <pageattr name="备餐阶段"/>

      <!-- DEP4: fusion_place — 与 PAGE1.P2 共享 token，库存充足才能备餐 -->
      <place id="P2_fusion">
        <posattr x="100" y="150"/>
        <text>订单_已接收</text>
        <type><id>OrderType</id></type>
        <initmark><text>empty</text></initmark>
        <!-- CPN Tools 中将此库所加入与 PAGE1.P2 相同的 fusion set -->
      </place>
      <place id="P3">
        <posattr x="350" y="150"/>
        <text>备餐_进行中</text>
        <type><id>DishType</id></type>
        <initmark><text>empty</text></initmark>
      </place>
      <place id="P4">
        <posattr x="600" y="150"/>
        <text>备餐_已完成</text>
        <type><id>DishType</id></type>
        <initmark><text>empty</text></initmark>
      </place>

      <!-- DEP1: arc_sequence — 接单→备餐，token 流动自然表达顺序 -->
      <trans id="T2">
        <posattr x="225" y="150"/>
        <text>开始备餐</text>
        <condition><text>true</text></condition>
      </trans>
      <trans id="T3">
        <posattr x="475" y="150"/>
        <text>完成备餐</text>
        <condition><text>true</text></condition>
      </trans>

      <arc id="A3" orientation="PtoT">
        <transend idref="T2"/><placeend idref="P2_fusion"/>
        <annot><text>1`堂食</text></annot>
      </arc>
      <arc id="A4" orientation="TtoP">
        <transend idref="T2"/><placeend idref="P3"/>
        <annot><text>1`热菜</text></annot>
      </arc>
      <arc id="A5" orientation="PtoT">
        <transend idref="T3"/><placeend idref="P3"/>
        <annot><text>1`热菜</text></annot>
      </arc>
      <arc id="A6" orientation="TtoP">
        <transend idref="T3"/><placeend idref="P4"/>
        <annot><text>1`热菜</text></annot>
      </arc>
    </page>

    <!-- ── 出餐 & 结账阶段（Page 3）── -->
    <page id="PAGE3">
      <pageattr name="出餐结账阶段"/>

      <place id="P5">
        <posattr x="100" y="150"/>
        <text>出餐_待完成</text>
        <type><id>OrderType</id></type>
        <initmark><text>empty</text></initmark>
      </place>
      <place id="P6">
        <posattr x="350" y="150"/>
        <text>结账_待完成</text>
        <type><id>OrderType</id></type>
        <initmark><text>empty</text></initmark>
      </place>
      <place id="P7">
        <posattr x="600" y="150"/>
        <text>顾客_已离开</text>
        <type><id>OrderType</id></type>
        <initmark><text>empty</text></initmark>
      </place>

      <!-- DEP2: arc_sequence — 备餐完成→出餐，融合库所引用 PAGE2.P4 -->
      <place id="P4_fusion">
        <posattr x="100" y="300"/>
        <text>备餐_已完成</text>
        <type><id>DishType</id></type>
        <initmark><text>empty</text></initmark>
      </place>

      <trans id="T4">
        <posattr x="225" y="150"/>
        <text>出餐</text>
        <condition><text>true</text></condition>
      </trans>
      <!-- DEP3: guard_condition — 出餐完成后才能结账（跨链守卫） -->
      <trans id="T5">
        <posattr x="475" y="150"/>
        <text>结账</text>
        <condition><text>member(出餐_待完成, marking(P5))</text></condition>
      </trans>

      <arc id="A7" orientation="PtoT">
        <transend idref="T4"/><placeend idref="P4_fusion"/>
        <annot><text>1`热菜</text></annot>
      </arc>
      <arc id="A8" orientation="TtoP">
        <transend idref="T4"/><placeend idref="P5"/>
        <annot><text>1`堂食</text></annot>
      </arc>
      <arc id="A9" orientation="PtoT">
        <transend idref="T5"/><placeend idref="P5"/>
        <annot><text>1`堂食</text></annot>
      </arc>
      <arc id="A10" orientation="TtoP">
        <transend idref="T5"/><placeend idref="P7"/>
        <annot><text>1`堂食</text></annot>
      </arc>
    </page>

  </cpnet>
</workspaceElements>
```

## 关键规则

| 规则 | 说明 |
|------|------|
| 每个子项目对应一个 `<page>` | `<pageattr name="..."/>` 设置页面名称 |
| colorset 定义在 `<globbox>` | 所有页面共享，不重复定义 |
| 有初始 token 的库所 | `<initmark><text>1\`堂食</text></initmark>` |
| 空库所 | `<initmark><text>empty</text></initmark>` |
| 输入弧 | `orientation="PtoT"`（Place to Transition） |
| 输出弧 | `orientation="TtoP"`（Transition to Place） |

## 三种依赖机制的 XML 表达

### arc_sequence（链内顺序）
无需额外处理，A 的输出库所直接作为 B 的输入弧，token 自然流动。

### guard_condition（跨链守卫）
在目标变迁的 `<condition>` 中写入前置库所的 token 检查：
```xml
<condition>
  <text>member(出餐_待完成, marking(P5))</text>
</condition>
```

### fusion_place（跨页面融合）
两个 page 中创建**同名库所**，在 CPN Tools 中将它们加入同一个 fusion set，token 自动共享。XML 层面两个库所独立定义，fusion 关系在工具界面中配置。
