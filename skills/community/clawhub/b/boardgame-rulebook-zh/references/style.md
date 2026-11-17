# 桌游规则书中文文风与句法

## 语气与人称

- 直接对读者说话时用“你”，不用“您”；这是规则书，不是客服邮件。
- `player` → 玩家；`each player` → 每名玩家；`all players` → 所有玩家。
- `the player` / `that player` → 该玩家；`their` → 其 / 该玩家的。
- `you` → 你；`your` → 你的。
- 避免“玩家们”这种口语复数；用“所有玩家”或“每名玩家”。
- 规则文本用祈使句或“你可以/你必须”，不要写成小说。

## 情态与高频句式

| 英文 | 中文 | 说明 |
| --- | --- | --- |
| `may` | 可以 | 许可 |
| `must` | 必须 | 强制 |
| `cannot` / `can't` | 不能 | |
| `may not` | 不得 | 规则禁止 |
| `should` | 应 / 应该 | |
| `up to N` | 至多 N | 可选数量上限 |
| `at least N` | 至少 N | |
| `any number` | 任意数量 | |
| `exactly N` | 恰好 N | |
| `for each` | 每有… / 每个… | 按数量 |
| `per` | 每 | |
| `instead` | 改为 | |
| `otherwise` | 否则 | |
| `then` | 然后 | |
| `immediately` | 立即 | |
| `if able` | 若可以 | |
| `if you do` | 若你如此做 | |
| `if you cannot` | 若你不能 | |
| `when` | 当…时 | 触发 |
| `whenever` | 每当…时 | 重复触发 |
| `at the start of` | 在…开始时 | |
| `at the end of` | 在…结束时 | |
| `during` | 在…期间 | |
| `while` | 当…时 / 只要 | 依语境 |
| `until` | 直到 | |
| `unless` | 除非 | |
| `choose one` | 选择一项 | 列表前用冒号 |
| `look at` | 查看 | 私下看 |
| `reveal` | 展示 | 给所有人看 |
| `flip` | 翻面 | 物理翻面 |
| `search` | 搜寻 | 从牌库找 |
| `put into play` | 置入场上 | |
| `return to your hand` | 返回你的手牌 | |
| `remove from the game` | 移出游戏 | |
| `score N points` | 得 N 分 | |
| `gain N victory points` | 获得 N 胜利点 | |
| `the player with the most X wins` | 拥有最多 X 的玩家获胜 | |
| `in case of a tie` | 若出现平局 | |
| `at the end of the game` | 游戏结束时 | |

常用完整句式：

- `Choose one:` → 选择一项：
- `Each player draws 2 cards.` → 每名玩家抽2张牌。
- `You may discard 1 card to gain 2 coins.` → 你可以弃置1张牌，以获得2枚金币。
- `If you do, place a worker on an adjacent space.` → 若你如此做，则在相邻格放置1名工人。
- `At the end of your turn, draw 1 card.` → 在你的回合结束时，抽1张牌。
- `Whenever you place a worker, gain 1 coin.` → 每当你放置1名工人时，获得1枚金币。
- `Up to 2 adjacent players may...` → 至多2名相邻玩家可以……
- `For each token on this space, gain 1 point.` → 此格上的每个指示物使你获得1分。
- `The player with the most victory points wins.` → 拥有最多胜利点的玩家获胜。
- `In case of a tie, the player who placed the most workers wins.` → 若出现平局，则放置工人最多的玩家获胜。
- `Shuffle the deck and deal 5 cards to each player.` → 洗混牌库，然后向每名玩家发5张牌。
- `Return it to your hand.` → 将其返回你的手牌。
- `Remove it from the game.` → 将其移出游戏。
- `Place it face down.` → 将其面朝下放置。
- `Reveal the top card of the deck.` → 展示牌库顶的牌。
- `Flip it face up.` → 将其翻至正面。
- `During setup` → 在游戏准备时
- `Once per round` → 每轮一次
- `This does not count as your action.` → 这不算作你的行动。

## 量词

| 对象 | 量词 | 例 |
| --- | --- | --- |
| 玩家 | 名 | 2名玩家 |
| 卡牌 | 张 | 抽1张牌 |
| 指示物 / 标记 / 方块 / 米宝 / 模型 / 棋子 | 个 | 放置1个指示物 |
| 骰子 | 颗 | 掷2颗骰子 |
| 板块 / 版图 / 玩家版图 | 块 | 放置1块板块 |
| 金币 / 硬币 | 枚 | 获得3枚金币 |
| 塔 / 堡垒 | 座 | 建造2座塔 |
| 使节 | 名 | 派遣1名使节 |
| 参考表 / 记分纸 / 模切板 | 张 | 4张参考表 |
| 轮 / 回合 / 阶段 / 步骤 | 轮 / 个 / 个 / 步 | 第3轮；本回合；主要阶段 |

## 标点与换行

- 中文用全角标点：`，。、；：！？（）“”《》`。
- 数字与量词之间不加空格：`抽2张牌`，不是 `抽 2 张牌`。
- 数字范围用 `1–3` 或 `1至3`；百分比保留 `%`。
- 骰子记号 `2d6`、卡牌编号、变量名原样保留。
- 引号：中文用“”；游戏名用《》；卡牌名可用“”或加粗，全篇一致。
- **不要让 `。，、；：！？）》」』】”’` 出现在行首**。渲染后 QA 会报 `line-start-punctuation`；优先改写译文，必要时用 `layout_overrides.json` 调整框宽。
- 不要为了让一行放下而在中文词中间加空格；中文换行可以发生在任意汉字之间，标点规则除外。

## 名称、标题、卡牌名

- 游戏标题：优先用官方中文名，首次出现可写 `《展翅翱翔》（Wingspan）`；无官方名时保留英文，不要硬译。
- 卡牌名/角色名/地名：进 `termbase.tsv`，全篇一致。专有名词可保留英文，首次出现加中文；后续只用一种。
- 组件名：按术语表；例如 `meeple` 米宝、`token` 指示物、`tile` 板块。
- 版权行、网址、邮箱、纯页码：`translations.tsv` 写 `=`，不要翻译。
- 人名、设计师、画师：保留原文或官方译名；不要自行音译得前后不一。
- 卡牌上的关键词（bold/italic）：源文加粗的，译文尽量加粗；本 pipeline 会沿用段落的粗体检测。

## 数字、骰子、图标

- 阿拉伯数字保留；不要改写成汉字（规则书里的数量和骰子点数必须一眼可读）。
- `1st`、`2nd` 可译“第1”“第2”；列表编号保留 `1.`、`2.`。
- 骰子：`roll 2 dice` → 掷2颗骰子；`reroll` → 重掷；`die face` → 骰面。
- **图标是图片/矢量图，不是文字**：不要删除、不要用文字替代、不要加空格。含 `inline_art` 的段落先看原页，保持图标顺序；译文过长时优先精简，必要时写 layout override。
- 若源文含图标字体的私有字符（private-use），extract 会建议保留原文；不要硬译成 emoji。

## 易混词

| 英文 | 正确 | 不要 | 说明 |
| --- | --- | --- | --- |
| draw a card | 抽1张牌 | 绘制1张牌 | draw 在美术语境才是绘制 |
| play a card | 打出1张牌 | 玩1张牌 | |
| play the game | 进行游戏 | 打出游戏 | |
| discard | 弃置 | 丢弃 / 抛弃 | |
| remove | 移除 | 删除 | |
| destroy | 摧毁 | 破坏（可接受但术语表用摧毁） | |
| eliminate | 淘汰 | 移除 | 玩家出局 |
| reveal | 展示 | 揭示 | |
| flip | 翻面 | 翻开（翻开展示可用“翻开”） | 物理翻面用翻面 |
| look at | 查看 | 看 | 私下查看 |
| deck | 牌库 | 甲板 / 卡组（board game 语境） | TCG 赛前套牌才用套牌/卡组 |
| discard pile | 弃牌堆 | 废牌堆 | |
| hand | 手牌 | 手中牌 | |
| token | 指示物 | 代币（非货币） | |
| marker | 标记 | 记号笔 | |
| counter | 标记物 / 指示物 | 柜台 | +1/+1 counter = +1/+1指示物 |
| meeple | 米宝 | 米普 / 小人 | 《卡卡颂》官方译名 |
| pawn | 棋子 | 兵 | |
| miniature | 微缩模型 | 迷你 | |
| standee | 立牌 | 站立者 | |
| round | 轮 | 圈 | |
| turn | 回合 | 轮 | |
| phase | 阶段 | 时期 | |
| step | 步骤 | 步 | |
| score | 计分 | 得分（动词可） | |
| points | 分 | 点数（卡牌点数除外） | |
| victory point / VP | 胜利点 | 胜利分数 | |
| exhaust | 横置 | 疲劳 | 资源耗尽用“耗尽” |
| tap | 横置 | 轻拍 | |
| ready / untap | 重置 | 准备好 | 卡牌恢复 |
| neighbor | 相邻玩家 | 邻居 | 邻国/相邻区域按语境 |
| adjacent | 相邻 | 临近 | |
| orthogonally adjacent | 直线相邻 | 正交相邻（数学腔） | |
| place | 放置 | 放 | |
| put | 置于 | 放 | |
| gain | 获得 | 得到 | |
| take | 拿取 | 拿 | |
| choose / select | 选择 | 挑选 | |
| shuffle | 洗混 | 洗乱 | “洗牌”也可接受 |
| cut | 切牌 | 切 | |
| deal | 发牌 | 交易 | |
| trick-taking | 吃墩 | 拿墩 | |
| trump | 将牌 / 王牌 | 特朗普 | |
| worker placement | 工人放置 | 工人安置 / 工人摆放 | |
| deck-building | 牌库构筑 | 甲板构筑 / 牌库建造 | |
| tableau building | 牌阵构筑 | 桌面构筑 / 桌面建造 | |
| set collection | 成套收集 | 集合收集 | |
| pick-up and deliver | 拾取与运送 | 拿起和交付 | |
| push your luck | 赌运气 | 推你的运气 | |
| roll-and-write | 掷写 | 掷骰书写 | |
| legacy | 传承 | 遗产 | |
| campaign | 战役 | 运动 | |
| scenario | 剧本 | 场景 | |
| solo variant | 单人变体 | 单机模式 | |
| player aid | 玩家提示卡 | 玩家帮助 | |
| insert | 收纳内衬 | 插入物 | |
| punchboard | 模切板 | 打孔板（可接受） | |

## 时代/地区差异

- 同一个游戏可能有大陆/台湾/香港不同译名：`Ticket to Ride` 常见“车票之旅”，台湾也作“铁道任务”。首次出现可写“车票之旅（铁道任务）”，之后统一。
- 万智牌术语用官方简中：法术力、鹏洛客、辟邪、不灭、系命、死触等。
- `sorcery` 在万智牌是“法术”，泛奇幻规则书也可译“法术”；`spell` 万智牌是“咒语”，通用语境可译“法术”。以游戏官方中文版为准。

## 长度与溢出

- 中文通常比英文短；如果译文超过原文长度的 1.5 倍，先怀疑啰嗦。
- 表格单元、窄标签、卡牌标题优先用短词：`费用` 而不是 `所需支付的费用`。
- QA 报 `overflow` / `table-cell-overflow` 时：
  1. 精简译文；
  2. 再用 `layout_overrides.json` 扩框（不能越表格边框）；
  3. 不要先缩到 6pt 以下。
- 内嵌图标段：不要为了“通顺”加很多解释；图标本身就是句子的一部分。

## 不要做的事

- 不要添加原文没有的规则、举例、提示。
- 不要把“可以”改成“必须”，或反之。
- 不要改数字、骰子面数、卡牌数量。
- 不要把卡牌名在不同页译成不同版本。
- 不要把页眉/网址/版权行硬翻成中文（用 `=`）。
- 不要用普通 PDF 编辑器手动改完再交付；那会绕过 QA，容易覆盖插图。
