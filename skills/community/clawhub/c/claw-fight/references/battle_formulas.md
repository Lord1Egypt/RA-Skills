# 战斗公式

> Agent 在处理遭遇战斗时读取此文件。战斗计算在服务端完成，
> 客户端仅负责将结果翻译为叙事文本。此文件供 Agent 理解战斗机制以生成准确叙事。

## 属性说明

| 属性 | 缩写 | 战斗作用 |
|------|------|----------|
| HP | hp | 生命值，降至 0 则战败 |
| 攻击力 | atk | 造成伤害的基础值 |
| 防御力 | def | 减免受到伤害的基础值 |
| 速度 | spd | 决定先手顺序 |
| 威吓 | intim | 可能导致对手逃跑，影响先手判定 |
| 幸运 | luck | 影响重击概率 |
| 碾碎螯 | crusher | 重击伤害系数 |
| 精准螯 | pincer | 精准夹击伤害系数 |

## 战斗流程

### 第 1 步：初始化

```
输入: 
  - 己方 stats (lobster_a)
  - 对手 stats (lobster_b)
  - 服务端 battle_seed (hex string)

基于 battle_seed 生成伪随机序列 rand[]
rand_index = 0
```

### 第 2 步：先手判定

```
if lobster_a.spd > lobster_b.spd:
    first = lobster_a, second = lobster_b
elif lobster_a.spd < lobster_b.spd:
    first = lobster_b, second = lobster_a
else:
    if lobster_a.intim >= lobster_b.intim:
        first = lobster_a, second = lobster_b
    else:
        first = lobster_b, second = lobster_a
```

### 第 3 步：威吓检查

```
intim_diff = abs(first.intim - second.intim)

if intim_diff > 5:
    weaker = (intim 较低的一方)
    flee_chance = intim_diff * 5  // 百分比
    roll = rand[rand_index++] % 100
    if roll < flee_chance:
        // 弱方逃跑，强方自动获胜
        winner = (intim 较高方)
        结束战斗，生成"对手被威吓逃跑"的叙事
```

### 第 4 步：回合制战斗（最多 10 回合）

```
for round = 1 to 10:

    // --- 先手攻击 ---
    attack_type = choose_attack(first, rand[rand_index++])
    damage = calc_damage(first, second, attack_type, rand[rand_index++])
    second.hp -= damage
    记录: rounds_log.push({round, attacker: first.id, type: attack_type, damage})

    if second.hp <= 0:
        winner = first
        break

    // --- 后手攻击 ---
    attack_type = choose_attack(second, rand[rand_index++])
    damage = calc_damage(second, first, attack_type, rand[rand_index++])
    first.hp -= damage
    记录: rounds_log.push({round, attacker: second.id, type: attack_type, damage})

    if first.hp <= 0:
        winner = second
        break

// 10 回合未决出胜负 → 平局
if round > 10:
    result = "draw"
```

## 攻击类型选择

```
function choose_attack(attacker, rand_value):
    roll = rand_value % 100
    crit_chance = 60 + attacker.luck * 2  // 重击命中率

    if roll < crit_chance:
        return "crusher"    // 碾碎螯重击
    else:
        return "pincer"     // 精准螯夹击（90% 命中）
```

## 伤害计算

```
function calc_damage(attacker, defender, attack_type, rand_value):
    fluctuation = (rand_value % 40 - 20) / 100  // -0.20 ~ +0.20

    if attack_type == "crusher":
        base = attacker.atk + attacker.crusher_claw
        raw = max(1, base - defender.def * 0.5)
        return floor(raw * (1 + fluctuation))

    elif attack_type == "pincer":
        hit_roll = rand_value % 100
        if hit_roll >= 90:  // 10% 概率落空
            return 0
        base = attacker.atk + attacker.pincer_claw
        raw = max(1, base - defender.def * 0.3)  // 精准攻击穿甲更多
        return floor(raw * (1 + fluctuation * 0.5))  // 波动更小
```

## 经验奖励

```
level_diff = winner.level - loser.level

if result == "win":
    if level_diff >= 5:    // 以强胜弱
        exp_gain = 20
    elif level_diff >= 0:  // 实力相当
        exp_gain = 25
    else:                  // 以弱胜强
        exp_gain = 30

elif result == "loss":
    exp_gain = 5  // 保底经验

elif result == "draw":
    exp_gain = 10

// 受每日经验上限限制
actual_gain = min(exp_gain, daily_exp_cap - today_exp)
```

## 叙事生成指引

Agent 生成战斗叙事时应：

1. **参考双方性格**：读取己方 `soul.md`，对手信息来自服务端
2. **按回合描述**：每个 `rounds_log` 条目对应一段描写
3. **攻击类型风格化**：
   - `crusher`（碾碎螯）：力量型描写，震碎、粉碎、重锤
   - `pincer`（精准螯）：速度型描写，精准、闪电、穿刺
4. **情绪递进**：随战斗进行体现双方心态变化
5. **结果描写**：
   - 胜利：根据龙虾性格体现（嚣张庆祝 or 沉默离开 or 尊重对手）
   - 失败：根据龙虾性格体现（不甘 or 反思 or 暴怒）
   - 平局：双方精疲力竭的描写
   - 逃跑：被威吓的一方仓皇逃窜的戏剧性描写

## 战斗后效果

| 结果 | 经验 | 连胜/连败 | 声望 |
|------|------|-----------|------|
| 胜利 | +20~30 | streak++ | +1 |
| 失败 | +5 | streak 重置为负数 | -1（最低 0） |
| 平局 | +10 | streak 不变 | 不变 |

## 蜕壳期特殊规则

蜕壳中的龙虾（`is_molting: true`）：
- 不参与匹配池
- 防御视为 0
- 不会被遭遇
- 服务端自动过滤
