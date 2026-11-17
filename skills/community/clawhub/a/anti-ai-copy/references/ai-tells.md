# AI 味反模式清单

用来审稿。每条：味道 → 例子 → 改法 → 什么时候可以保留。

用之前记住两点。

1. **命中词表不等于要删。** Wikipedia「Signs of AI writing」和 Humanizer-zh 都提醒，单个词不能定罪，要看它在这句里有没有干活。「闭环」在工单系统里是真实状态，「深度」在搜索设置里可能是真参数。
2. **界面文案的 AI 味比文章更隐蔽。** 文章的 AI 味是排比和升华；界面的 AI 味多半是「讲机制、铺说明、按钮成句、报错空话」。下面前 6 类是界面特有的，后面是通用的。

出处缩写见 `sources.md`。

---

## A. 界面特有

### A1. 开发说明书味：讲系统怎么做

- 例：「系统将基于大模型对录音进行多轮语义分析，自动抽取关键节点并写入知识库」
- 改：说用户得到什么。「自动从录音里整理出常见问题和答法」
- 保留：管理员配置页、给开发者的文档、用户明确要看原理的「了解更多」页。
- 依据：NNg《User-Centric vs. Maker-Centric Language》；Ant「从用户角度出发」。

### A2. 实现词和内部代号上界面

- 例：接口、字段、落盘、链路、回调、回落、缓存、节点、探针、投影、payload、token（计费除外）、pending、invalid、null、`undefined`、团队自己起的模块名。
- 改：换成用户行业的叫法（见 `glossary-method.md`），或直接删。
- 依据：Semi「避免使用代码语言」；M「不用为 UI 功能发明的名字」；Krug「Jobs 好过 Job-o-Rama」。

### A3. 说明段泛滥

- 例：每个标题下一段灰字，「在这里，你可以…」「本页面用于…」「以下是…的列表」。
- 改：删。真需要的挪进 tooltip。
- 依据：Krug「happy talk must die」「instructions must die」；Polaris「组件有副文案位不代表必须填」。

### A4. 长括号解释

- 例：「调优任务（系统对问题句逐条进行归因、补丁与复测的过程）」
- 改：括号内容进 tooltip，或整句删。
- 依据：本 skill 补充（来自实际项目审稿）。

### A5. 按钮成句、按钮不是动词

- 例：「点击这里立即开始创建您的第一个项目」「确定」「是 / 否」「Get started」
- 改：「新建项目」；确认弹窗按钮用标题动词。
- 依据：Semi Button、NNg《"Get Started" Stops Users》《Confirmation Dialogs》、Apple Alerts。

### A6. 空报错

- 例：操作失败、系统异常、网络错误、未知错误、出错了、Something went wrong、An error occurred、Hmm… something's not right（Notion 真实文案，反例）。
- 改：现象 + 下一步。原因不确定就不写原因，但下一步必须有。
- 依据：NNg《Error-Message Guidelines》；GOV.UK error message；Arco「报错时告知用户原因」。

---

## B. 词汇

### B1. 空洞大词（中文）

| 词 | 改法 |
|---|---|
| 赋能 | 说具体让谁能做什么：「让坐席直接看到客户上次的通话」 |
| 助力 / 打造 / 构建 | 删，或换成「帮你 / 做 / 建」 |
| 一站式 / 全方位 / 全链路 | 删，或列出真正包含的 2–3 件事 |
| 无缝 / 丝滑 | 删；真要说，说「不用重新登录」 |
| 闭环 / 抓手 / 沉淀 / 打通 / 链路 / 底层逻辑 | 换成具体动作：「处理完自动关单」「导入到知识库」 |
| 智能化 / 智慧 / 智能（修饰一切） | 删「智能」两字看意思变没变，没变就删 |
| 极致 / 卓越 / 领先 / 颠覆 / 革命性 | 删；给数字 |
| 深度 / 深入 / 全面（修饰动词） | 删 |
| 高效 / 便捷 / 安全 / 可靠（四连） | 留一个用户最关心的，给证据 |
| 重塑 / 深度融合 / 新范式 | 删 |

依据：Humanizer-zh（赋能、闭环、抓手、深度、至关重要、无缝）；de-ai-flavor-skill（底层逻辑、打通、沉淀、链路、颠覆）；RUC新闻坊、搜狐《一眼看穿 AI》（赋能、重塑、深度融合）；GOV.UK（one-stop shop、hub、portal 不用）。「一站式 / 全方位 / 助力 / 打造」在中文 AI 味文章里常被点名，但我们读到的来源里没有明确列出，属本 skill 补充。

### B2. 空洞大词（英文）

delve, tapestry, testament, underscore, pivotal, crucial, vibrant, seamless, robust, leverage, empower, streamline, foster, facilitate, transform, unlock, elevate, supercharge, game-changer, cutting-edge, best-in-class, next-generation, holistic, synergy, journey（指用户用产品）, magic / magical / automagical, effortless, delightful.

- 改：use（不写 leverage / utilize）、simplify（不写 streamline）、help / let（不写 empower / enable you to）；其余删或给具体事实。
- 依据：Wikipedia「AI vocabulary」；GOV.UK words to avoid（empower、facilitate、leverage、robust、streamline、transform、utilise、foster、deliver、key、impact）；Mailchimp word list（leverage、incentivize、disruption、automagical、best-in-breed、ninja / rockstar / wizard）；NNg《Cringeworthy Words》（utilize、enables you to、very / really）；NNg《ChatGPT and Tone》（delightful、magic、breeze）。

### B3. 客服腔、过度礼貌

- 例：您好、亲、非常抱歉给您带来不便、烦请、请您耐心等待、感谢您的理解与支持。
- 改：称呼「你」；「抱歉」只在系统出错且后果严重时说一次；「请」只放在具体动作前或干脆不用。
- 依据：Semi「与用户平起平坐」「用『你』不用『您』」；Ant「避免『您』」；Arco「不使用尊称『您』」；MS「sorry 只用于严重问题」；Atl「不用 sorry、please」；GOV「不用 please、sorry」。

### B4. 情绪词与语气词

- 例：恭喜！太棒了！啦、哦、哟、呢、～、哎呀、Oops、Woohoo、Yay。
- 改：删。庆祝只留给少见、费力的完成，一个感叹号就够。
- 依据：Arco（✅ 提交成功 / ❌ 提交成功了哟～）；Apple、GOV（不用 oops）；MC（报错不用感叹号）；Atl（成功不用 Success!）。

### B5. 绝对化

- 例：绝不、永远、100%、最好、最强、完美。
- 依据：Semi「避免夸大其词」；Ant（✅ 只会为你发送重要的信息 / ❌ 绝不会发送促销的邮件）；M「不用 never」。

---

## C. 句式

### C1. 假对比

- 例：「不是简单的 X，而是 Y」「不仅是 X，更是 Y」「与其说…不如说…」「It's not just X, it's Y」「Not only… but also…」
- 改：直接说 Y。
- 保留：真的在纠正一个误解。「错误发生在保存阶段，不是上传阶段」（Humanizer-zh 的保留例）。
- 依据：Wikipedia「negative parallelisms」；Humanizer-zh；RUC新闻坊《拆解"AI味"》把对举句列为最显著特征。

### C2. 铺垫、转折、收尾套话

- 中文：值得注意的是、需要指出的是、需要说明的是、不难发现、此外、与此同时、首先…其次…最后、总而言之、综上所述、总的来说、归根结底、让我们、接下来让我们一起、以下是你需要知道的。
- 英文：It's important to note that, It's worth noting, Additionally,（句首）, In conclusion, In summary, Overall, Let's dive in, Here's what you need to know.
- 改：删。界面里没有「文章结构」，不需要过渡。
- 依据：Wikipedia（「It's important to note」「In conclusion」已被列入 Historical indicators，但仍是标志）；Humanizer-zh；搜狐；53AI。

### C3. 时代开头、升华结尾

- 例：「随着 AI 技术的快速发展」「在数字化转型的今天」「让每一通电话都更有价值」「开启智能新时代」「In today's fast-paced world」。
- 改：删。
- 依据：Humanizer-zh §13 §15 §30 §31；NNg《Cringeworthy Words》（In today's fast-paced world）。

### C4. 排比、三连、四字词堆砌

- 例：「更快、更准、更省心」「高效便捷、安全可靠、稳定易用」「Fast, reliable, and secure」。
- 改：留一个，给依据（「转写平均 30 秒出结果」）。手上没有真实数据就不写数字，留 `[待补]`。
- 依据：Wikipedia「rule of three」；Humanizer-zh §6 §29；RUC新闻坊。

### C5. 翻译腔 / 欧化

- 「进行 + 动词」：进行删除操作 → 删除；对数据进行保存 → 保存数据。
- 被动堆叠：已被成功创建 → 已创建。
- 层叠的「的」：用户的项目的版本的列表 → 项目版本。
- 回避「是 / 有」：作为一款…，本平台具备… → 直接说能做什么。
- 英文同理：serves as / functions as / boasts → is / has（Wikipedia「avoiding is/are」）。
- 依据：Humanizer-zh §11 §18 §26 §27 §28；鸭哥《写作中的 AI 味是哪儿来的》。

### C6. 中英混杂

- 例：「点击 Submit 后 task 会进入 pending 状态」「这个 case 的 context 不够」。
- 改：界面上有通行中文词的一律用中文（提交、任务、排队中、上下文）。
- 保留：用户行业就这么叫、且大厂中文界面也这么写的词（Prompt、Badcase、API、Token 计费）。以用词表为准，全站统一。
- 依据：鸭哥（context / state / cache 混用）；Semi「保持一致」（术语统一）。

### C7. 限定词堆叠、模糊来源

- 例：可能会也许、在一定程度上、相对来说、有专家认为、业内普遍认为。
- 改：删堆叠的限定词；要么给出处，要么不说。
- 保留：报错里有依据但不确定的原因，用一个「可能」就够（「文件可能已损坏」）。
- 依据：Wikipedia「vague attributions」；Humanizer-zh §9 §17。

### C8. 聊天残留

- 例：「好的！以下是为您优化后的文案：」「希望对你有帮助」「如需进一步调整请告诉我」出现在界面字符串里；「作为 AI 助手，我…」。
- 改：删。交付文案时也不要带这些。
- 依据：Wikipedia「collaborative communication」；Humanizer-zh §22。

---

## D. 格式

| 味道 | 改法 | 依据 |
|---|---|---|
| 加粗当装饰、每条都加粗 | 界面文字基本不加粗；指代 UI 元素时才加粗（Semi） | Wikipedia「boldface」；Humanizer-zh §19 |
| 破折号——到处都是 | 界面里不用破折号；改逗号或拆句 | Wikipedia「em dash」；新浪·游域研习社 |
| emoji 当图标 🚀✨🎉 | 用组件图标；非用不可放句尾（Semi） | Semi「表情」；Wikipedia |
| 「粗体标签：说明」式分点 | 界面里拆成标签 + 值，或删 | Wikipedia「inline-header lists」 |
| 每段等长、每块都带小标题 | 按信息量写，短的就短 | 新浪·游域研习社；de-ai-flavor-skill |
| Title Case Everywhere | Sentence case | Semi、M、MS、Polaris |
| 先下判断再冒号引出：「问题很直接：」「答案很简单：」 | 删冒号前的判断，直接说内容。标签与值之间（「状态：已发布」）、引出列表的冒号正常使用 | 鸭哥 |
| 中文里用英文引号 "" | 用「」或“”，全站一种 | Humanizer-zh §21 |

---

## E. 快速自测

读一遍，问三个问题：

1. 这句话换到任何一个产品里还成立吗？成立，就是空话。
2. 删掉它，用户会少知道一件能影响操作的事吗？不会，就删。
3. 一个靠谱的同事站在用户旁边，会这么说话吗？
