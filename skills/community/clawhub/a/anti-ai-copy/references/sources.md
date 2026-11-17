# 出处与各家要点摘编

只摘要点和少量短引文，原文以链接为准。Semi Design（MIT）引得多一些，其余为转述。2026-09 查阅。

---

## 中文设计系统

### Semi Design（字节 · 抖音前端与 UED）· 缩写 Semi

- 文案规范：https://github.com/DouyinFE/semi-design/blob/main/content/experience/content-guidelines/index.md （站点 https://semi.design/zh-CN/start/content-guidelines ）
- 各组件「文案规范」小节：`content/*/*/index.md`，如 Button、Toast、Modal、Empty、Form、Tooltip。
- MIT License, Copyright (c) 2021 DouyinFE.

要点：
- Voice：直接清晰、真实友好、乐于助人。Tone 随场景变：中性的、庆祝的、同情的、有帮助的、权威的。
- 书写原则：简洁清晰；像人一样说话（「避免使用代码语言」）；开门见山（「文件已上传」好于「你已经成功上传了文件」）；保持一致；与用户平起平坐（少道歉、不说教）；避免夸大其词；包容性。
- 用词表：你（不用您）、抱歉（不用对不起）、账号、登录、新建、添加、删除、移除、启用、停用、其他。
- 按钮：「{动词}+{名词}」；上下文足够时只用动词。
- Toast：「使用 名词 + 动词 的格式」，句尾不用句号，只提供一个动作。
- Modal：标题动词 + 名词（Delete form? 而非 Are you sure you want to delete form?）；按钮只用标题内的动词；正文不重复标题。
- Empty：正文不重复标题，1–2 句；按钮动词 + 名词。
- Form：「标签不是注释信息（help text），因此不应该是输入框的填写说明」，1–3 个词。
- Tooltip：只展示信息说明和引导，不展示报错；不放链接和按钮；尽量一句，不加标点。
- 标点：按钮、一句话的 Toast、占位符、标题、通知、导航菜单、tooltip、radio、checkbox 不用句号；少用感叹号；不用分号。
- 表情：避免 emoji，用 icon 代替。

### Ant Design（蚂蚁）· 缩写 Ant

- 文案：https://github.com/ant-design/ant-design/blob/master/docs/spec/copywriting.zh-CN.md （https://ant.design/docs/spec/copywriting-cn ）
- 按钮文案：`docs/spec/buttons.zh-CN.md`；数据格式：`docs/spec/data-format.zh-CN.md`。MIT。

要点：从用户角度出发、表述一致、重要信息放显著位置、专业精准完整、精简友好正面。用「你」不用「您」；避免「不能 / 不要 / 请勿」等命令口吻与「绝不」等绝对词；报错说「无法完成」并给下一步；「抱歉」只在系统原因时用。数字阿拉伯化、千分位、日期 yyyy-mm-dd、24 小时制；表格空值 `--`。按钮用动词且简短，最好说出结果（发布、登录）而不是「确定」。对照：✅ 保存 / ❌ 保存修改内容；✅ 抱歉，无法完成发布，建议重新部署 / ❌ 抱歉，发布失败；✅ 付款成功 / ❌ 资金流出成功；✅ 你有 3 条短消息 / ❌ 你有三条短消息。

### Arco Design（字节）· 缩写 Arco

- 风格指南：https://github.com/arco-design/arco-design/blob/main/site/docs_spec/style-guideline.zh-CN.md （https://arco.design/docs/spec/style-guideline ）
- 组件文案指南：`site/docs_spec/components/`。MIT。

要点：词汇统一、语法正确、文案精炼、通俗易懂、语言友好。操作用动词 + 名词；数量用数字 + 单位 + 动词 / 名词；报错告知原因；不用「您」，性别不明用 TA；中英文、中文与数字之间加空格。Message：描述现状、解释原因、给出操作指引。Empty：突出用户能做的操作，文字脱离插画也能懂。对照：✅ 新建项目 / ❌ 项目新建；✅ 提交成功 / ❌ 提交成功了哟～；✅ 网络错误，创建失败 / ❌ 创建失败；✅ 请输入公司办公地址 / ❌ 公司办公地址请勿为空。

### TDesign（腾讯）· 缩写 TD

- 无独立文案规范；组件设计文档散见：https://github.com/Tencent/tdesign-common/tree/develop/docs/web/_design 、`docs/mobile/_design`。MIT。

要点：对话框正文明确目的与后果，按钮用指向结果的词而非模棱两可的词；Toast ≤ 30 字；Tag 2–6 字；开关文字只说控制什么；快捷选项「近 7 天」而非「最近 7 天数据」。

### Fusion Design（阿里）

- 未找到公开的文案规范（alibaba-fusion/next 组件文档无文案章节，fusion.design 为前端渲染）。本 skill 未引用。

---

## 英文规范

- **Material Design · M**：M1 Writing https://m1.material.io/style/writing.html ；M3 UX writing https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices 。用 you，少用 we；目标放句首；同一功能同一动词；数字用阿拉伯数字；sentence case；单句不加句号；少用感叹号。对照：「Save changes?」不写「Would you like to save your changes?」；「Message sent」不写「Message has been sent」。
- **Apple HIG · Apple**：Writing https://developer.apple.com/design/human-interface-guidelines/writing ；Alerts https://developer.apple.com/design/human-interface-guidelines/alerts 。按钮用动词，不耍聪明（「Send」而非「Let's do it!」）；不用 we（「Unable to load content」）；报错就近、不责怪、不用 oops；alert 标题说发生了什么，不写「Error」；按钮 1–2 词描述结果，有选择时不用 Yes/No，取消永远是「Cancel」。
- **Microsoft Writing Style Guide · MS**：https://learn.microsoft.com/en-us/style-guide/brand-voice-above-all-simple-human ；top 10 tips https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice ；please / sorry 词条；报错公式来自 Windows UX https://learn.microsoft.com/en-us/windows/win32/uxguide/mess-error 。「Bigger ideas and fewer words」；sentence case；please 只在用户被迫做麻烦事时用；sorry 只在严重问题时用；报错 = 问题 + 原因 + 解决办法；不确定原因就别猜。
- **Atlassian Design · Atl**：Voice and tone https://atlassian.design/foundations/content/voice-tone ；Error / Warning / Empty state / Success messages `atlassian.design/foundations/content/designing-messages/*`。只说此刻需要的信息；报错正文 1–2 句，说原因、怎么办；不用 sorry、please；成功消息不写 Success!、不用感叹号；空状态一个 CTA。
- **Shopify Polaris · Polaris**：https://polaris.shopify.com/content/fundamentals ；error-messages、grammar-and-mechanics、naming；源码 github.com/Shopify/polaris。每个字都要称重；有副文案位不代表要填；不用 invalid；报错说具体数字和用户数据；按钮强动词、无冠词、无标点。对照：「Connection timed out」好于「Sorry, the connection time out. Try again later.」。
- **GOV.UK · GOV**：错误消息 https://design-system.service.gov.uk/components/error-message/ ；写作指南 https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/ ；A–Z 词表（words to avoid）同站 style-guides/a-to-z-style-guide/。报错不用 please、sorry、invalid、oops、forbidden、「you forgot」；空值用指令（Enter your first name），超限用描述（must be 35 characters or less）；重要信息前置；words to avoid：empower、facilitate、leverage、robust、streamline、transform、utilise、one-stop shop 等。
- **Mailchimp Content Style Guide · MC**：https://styleguide.mailchimp.com/voice-and-tone/ ；web-elements；word-list。Plainspoken：不夸张、不推销、不用花哨比喻；「Don't market at people; communicate with them」；报错与警告不用感叹号；按钮必有动词；避免 leverage、incentivize、disruption、automagical、ninja / rockstar 等。

---

## 书与研究

- **Steve Krug《Don't Make Me Think, Revisited》· Krug**：第 5 章 Omit needless words。「Get rid of half the words on each page, then get rid of half of what's left.」Happy talk must die；instructions must die；先做到不言自明（self-evident），做不到再做到一看就懂（self-explanatory）。摘录 https://www.peachpit.com/articles/article.aspx?p=2209309
- **Kinneret Yifrah《Microcopy: The Complete Guide》· Yifrah**：https://www.microcopybook.com/ ；确认弹窗 https://uxdesign.cc/are-you-sure-you-want-to-do-this-microcopy-for-confirmation-dialogues-1d94a0f73ac6 。先定 voice；报错说清问题 + 建设性建议 + 不责怪；按可逆性、严重度、频率决定用确认还是撤销；确认标题说具体动作；首次空与日常空写法不同；每个状态都要写。
- **Torrey Podmajersky《Strategic Writing for UX》· Pod**：O'Reilly 2019；访谈 https://uxpod.com/episodes/ux-writing-an-interview-with-torrey-podmajersky.html 。voice chart（概念、词汇、篇幅、语法、标点、大小写）；四遍编辑：purposeful → concise → conversational → clear；11 类文案模式（标题、按钮、描述、空状态、标签、控件、输入框、过渡、确认、通知、报错）；「{Noun} {verb}ed」式确认、「{Verb}ing…」式过渡。
- **Nielsen Norman Group · NNg**：
  - Error-Message Guidelines https://www.nngroup.com/articles/error-message-guidelines/
  - Hostile Patterns in Error Messages https://www.nngroup.com/articles/hostile-error-messages/
  - Designing Empty States in Complex Applications https://www.nngroup.com/articles/empty-state-interface-design/
  - Tooltip Guidelines https://www.nngroup.com/articles/tooltip-guidelines/
  - UI Copy: Command Names https://www.nngroup.com/articles/ui-copy/
  - Confirmation Dialogs https://www.nngroup.com/articles/confirmation-dialog/
  - "Get Started" Stops Users https://www.nngroup.com/articles/get-started/
  - How Users Read on the Web https://www.nngroup.com/articles/how-users-read-on-the-web/
  - First 2 Words https://www.nngroup.com/articles/first-2-words-a-signal-for-scanning/
  - Placeholders in Form Fields Are Harmful https://www.nngroup.com/articles/form-design-placeholders/
  - User-Centric vs. Maker-Centric Language https://www.nngroup.com/articles/user-centric-language/
  - Cringeworthy Words https://www.nngroup.com/articles/cringeworthy-words/
  - ChatGPT and Tone https://www.nngroup.com/articles/chatgpt-and-tone/

---

## AI 味识别

- Wikipedia: Signs of AI writing https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing （CC BY-SA）：AI vocabulary、negative parallelisms、rule of three、avoiding is/are、boldface / em dash overuse、collaborative communication、historical indicators。
- op7418/Humanizer-zh https://github.com/op7418/Humanizer-zh ：31 类中文 AI 痕迹，每类带保留例。
- ren644/de-ai-flavor-skill https://github.com/ren644/de-ai-flavor-skill ：中文黑话与句式表。
- MrGeDiao/shuorenhua https://github.com/MrGeDiao/shuorenhua ：中文「说人话」改写流程。
- RUC新闻坊《拆解"AI味"》https://news.qq.com/rain/a/20250924A01QWG00 ：对举句频率对比。
- 搜狐《一眼看穿AI：AI中文写作的常见特征》https://www.sohu.com/a/1014931596_523187
- 鸭哥《写作中的AI味是哪儿来的》https://yage.ai/share/ai-chinese-translationese-20260418.html ：翻译腔与中英混杂。
- 翔宇工作流《8 个特征识别和消除 AI 味》https://xiangyugongzuoliu.com/ai-style-writing-8-common-giveaways/

这些都针对文章；本 skill 针对界面字符串。

---

## 真实产品文案

- 腾讯云智能体开发平台：应用发布 https://cloud.tencent.com/document/product/1759/104209 （待发布、发布历史、还原到调试态 → 确认还原；「应用尚未发布，触发器需要基于已发布版本运行」）；应用评测 https://cloud.tencent.com/document/product/1759/104208 （「删除评测任务，删除后无法恢复。」）；文档状态 https://cloud.tencent.com/document/product/1759/112702 （解析中 / 解析失败 / 审核中 / 审核失败 / 学习中 / 学习失败 / 导入完成）。
- 扣子罗盘（开源）https://github.com/coze-dev/coze-loop 的 zh-CN 词条：「暂不支持复制草稿版本，请先提交版本」「草稿已自动保存于{date}」「仅评测集相同且已执行完成的实验可进行对比。」；反例：同一动作「确定 / 确认」混用、「确定已选的{num}数据项吗？」缺动词。
- 扣子 coze-studio https://github.com/coze-dev/coze-studio ：「试运行通过后可以提交」「插件已创建，请继续添加工具」「ID已绑定到{bot_name}，请先解除绑定。」
- 飞书帮助中心：撤回 https://www.feishu.cn/hc/zh-CN/articles/360045143093 （「此消息已撤回」）；删除与恢复 https://www.feishu.cn/hc/zh-CN/articles/360049067425 （删除 → 回收站 → 恢复 / 彻底删除）；解散群组 https://www.feishu.cn/hc/zh-CN/articles/360025144134 （「解散群组后不可恢复」，确认按钮「解散」）。
- Stripe：https://docs.stripe.com/declines/codes （「Your card was declined.」+「The customer needs to use another card.」）；https://docs.stripe.com/api/errors （message 可直接展示给用户；是否值得重试写进 message）。
- Linear：https://linear.app/docs/configuring-workflows （Backlog / Todo / In Progress / Done / Canceled）；https://linear.app/method/write-issues-not-user-stories （plain language）。
- Notion：https://www.notion.com/help/duplicate-delete-and-restore-content （Delete → Trash → Restore；Archive 另一条路）；https://www.notion.com/help/notion-error-messages （「Go online to view this image」是好例，「Hmm… something's not right」是反例）。
