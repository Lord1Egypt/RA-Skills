# Phoenix 单动作（`play_action`）

**适用**：一步、无时间编排的动作 —— `display` → 内层 **`cmd=play_action`**；纯 `playSound`（无 `actions`/定时）时网关也会落成 `play_action`。

多步、定时、并行 → [phoenix-action-control.md](./phoenix-action-control.md)（`action_sequence`）。两种路径**字段口径不同**，见文末对照表。

---

## 1. 外层 envelope

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `msgId` | string | 是 | 消息 id（脚本默认毫秒时间戳） |
| `cmd` | string | 是 | 固定 `play_action` |
| `data` | object | 是 | 见下文各 `type` |

```json
{
  "msgId": "1730000000001",
  "cmd": "play_action",
  "data": { "type": "shake_head", "angle": "3000", "moveTimeMs": "-1", "count": "3" }
}
```

---

## 2. 支持的 `type`

除「休眠 / 复位」外，**`angle` / `moveTimeMs` / `count` 均为 string**。

### 2.1 情绪动作

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | `calm` `happy` `attached` `curious` `angry` `sad` `scared` |
| `angle` | 是 | 等级路径：`level1/1` … `level3/5`（calm/happy/attached 每级 5 个；其余每级 3 个） |
| `moveTimeMs` | 是 | `-1` |
| `count` | 是 | 重复次数；`count=1` 表示再重复 1 次（共 2 遍） |

### 2.2 叫声 `play_sound`

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | `play_sound` |
| `angle` / `file` | 是* | **音效文件名**（单动作 Phoenix 字段为 `angle`；编排为 `file`） |
| `moveTimeMs` | 是 | 单次时长；`-1` 按 **3000ms**；指定 `file` 时网关可填目录时长 |
| `count` | 是 | 播放次数 |

\* 经 `playSound` 下发时：**`category` 与 `file` 二选一**——日常说法用 `category`；需要强度/具体音效时用 `file`。

**命名规则**（指定 `file` 时按表挑选）：

| 情绪/场景 | 文件名规则 | 示例 |
|-----------|------------|------|
| calm / happy / attached | `{情绪}-{l\|m\|h}-{1-5}` | `happy-h-4`, `calm-l-1` |
| curious / angry / sad / scared | `{情绪}-{l\|m\|h}-{1-3}` | `curious-m-2` |
| 回答问题 | 固定名 | `anser-1` |
| 牙牙学语 | 固定名 | `father`, `mother`, `loveyou`, `saybye`, … |

**对话 → 参数（技能侧）**：

| 用户说法 | 建议下发 | 说明 |
|----------|----------|------|
| 「开心的叫一下 / 叫一声」 | `{"category":"happy","count":1}` | 未指定强度；网关在该分类下**随机**选一条 |
| 「开心**大**叫一声 / 大声叫」 | `{"file":"happy-h-<1-5>","count":1}` | 强度 **h**；在 `happy-h-1`…`happy-h-5` 中**任选其一** |
| 「轻轻叫 / 小声叫」 | `{"file":"happy-l-<1-5>","count":1}` | 强度 **l** |
| 「难过地哼一声」 | `{"category":"sad","count":1}` 或 `sad-m-*` / `sad-l-*` | 无强度词用 `category`；有则按 l/m/h 选 band |

`l` / `m` / `h` = 低 / 中 / 高（响度或情绪强度）。编排 `action_sequence` 里每步 `play_sound` 须写具体 `file`（可先按上表选定再填入 JSON）。

**下发示例**：

```bash
# 默认：按情绪分类，网关随机选 file
python3 scripts/ecovacs.py cmd <nick> playSound '{"category":"happy","count":1}'

# 明确强度：技能指定 file
python3 scripts/ecovacs.py cmd <nick> playSound '{"file":"happy-h-3","count":1}'

# 单动作 display
python3 scripts/ecovacs.py display <nick> action play_sound '{"file":"happy-h-3","moveTimeMs":"5387","count":"1"}'
```

### 2.3 头部 `nod_head` / `shake_head` / `cock_head`

| 字段 | 必填 | 说明 |
|------|------|------|
| `angle` | 是 | 目标角度 **×100**（30° → `"3000"`） |
| `moveTimeMs` | 是 | 单次时长；`-1` 为默认速度 |
| `count` | 是 | `1`：到目标角；`>1`：目标角与反向来回 |

**脚本输入**：`display action` 的 JSON 里 **`angle` 可写角度制**（如 `"30"`），脚本会 ×100 后下发。

### 2.4 摆尾 `wag_tail`

| 字段 | 必填 | 说明 |
|------|------|------|
| `angle` | 是 | 速度 **(0–100)×100**（30% → `"3000"`） |
| `moveTimeMs` | 是 | 时长；`-1` 持续摇 |
| `count` | 是 | `"0"` |

**脚本输入**：`percent: 30` 或 `angle: 30`（0–100 视为百分比）。

### 2.5 休眠 / 复位

| 入口 | 载荷 |
|------|------|
| 休眠 | `{ "type": "sleep" }` |
| 停止动作、取消设备端已排队定时 | `display reset` → `type=reset`，`angle=0`，`moveTimeMs=0`，`count=0` |

---

## 3. 与编排路径的字段对照（禁止混写）

| 动作 | 单动作（本文件） | 编排（action_sequence） |
|------|------------------|-------------------------|
| 头部 | `angle` **×100** 下发；CLI JSON 可写角度制，脚本换算 | `angle` **角度制**，**不 ×100**；须落在设备范围内 |
| 头部范围 | 选角时仍遵守设备限位 | 点头 −14~+22 · 摇头 −60~+60 · 扭头 −20~+20 |
| 摆尾 | 下发字段 `angle` = 速度×100；CLI 可用 `percent` | 字段 **`percent`**；不用 `angle` |
| 叫声 | 下发字段 `angle` = 文件名 | 字段 **`file`** |
| 时间 | 无 `delay`；`moveTimeMs` 可 `-1` | 每项 `delay`（ms）；**`moveTimeMs>0`** |

**路由**：单步 → `display action` / 无 `actions` 的 `playSound` → **`play_action`**。  
多步 / 编舞 / 声+动同拍 → **`action_sequence`** → [phoenix-action-control.md](./phoenix-action-control.md)。

**勿**把本文件示例 JSON 直接复制进 `actions[]`（×100 的 `angle`、`-1` 时长、摆尾用 `angle` 等均为单动作口径）。

---

## 4. 脚本示例

```bash
SCRIPT="./scripts/ecovacs.py"

python3 "$SCRIPT" display <nick> sleep
python3 "$SCRIPT" display <nick> reset

python3 "$SCRIPT" display <nick> action shake_head '{"angle":"30","moveTimeMs":"-1","count":"3"}'
python3 "$SCRIPT" display <nick> action wag_tail '{"percent":30,"moveTimeMs":"-1"}'
python3 "$SCRIPT" cmd <nick> playSound '{"category":"happy","count":1}'
python3 "$SCRIPT" cmd <nick> playSound '{"file":"happy-h-3","count":1}'
python3 "$SCRIPT" display <nick> action play_sound '{"file":"happy-h-3","moveTimeMs":"5387","count":"1"}'
python3 "$SCRIPT" display <nick> action happy '{"angle":"level2/3","moveTimeMs":"-1","count":"0"}'
```

---

## 5. 返回

| 字段 | 说明 |
|------|------|
| `code` | `0` 成功 |
| `errMsg` | 失败原因 |

联调时同时看网关外层 `data.resp.body.code`。
