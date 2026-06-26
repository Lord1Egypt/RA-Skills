# Douyin Comment Ops Playbook

## 1. Trigger examples

Use this skill for requests like:

- 帮我回复我抖音视频下面这些评论
- 给我做一套抖音评论区自动回复 SOP
- 这些评论哪些该回，哪些不用回？
- 帮我把评论按意图分类再给回复
- Build a Douyin comment reply workflow for my account
- Draft replies for these comments under my Douyin video

## 2. Intent buckets

### 咨询 / Inquiry
Questions about what it is, how it works, how to buy, whether it fits.

### 成交意向 / Buying intent
Strong signals such as price, how to start, where to sign up, can you do this for me.

### 价格异议 / Price objection
Too expensive, not worth it, can it be cheaper, why pay for this.

### 质疑 / Skepticism
真的假的, does this actually work, scam suspicion, challenge to credibility.

### 催更 / Engagement
Interesting, want part 2, teach more, how to do this step.

### 售后 / Support
Already purchased, cannot use, where is the file, follow-up issue.

### 无效 / Noise
Trolling, abuse, irrelevant spam, nonsense.

## 3. Priority logic

High priority:
- buying intent
- high-quality inquiry
- support issues
- credible skepticism from real prospects

Medium priority:
- curiosity comments
- engagement comments worth boosting

Low priority:
- repetitive low-value comments
- obvious trolling
- comments with no business or community value

## 4. Reply formulas

### Inquiry
`先回答一个核心问题 + 给下一步`

Example:
这个可以做，主要看你现在是想自己用还是给团队一起用，想了解细一点可以私信我。  
Yes, this can be done. It mostly depends on whether you want it for yourself or for a team—DM me if you want the detailed version.

### Buying intent
`建立确定感 + 引导私信/动作`

Example:
可以的，这类我这边有现成方案，私信我发你适合你的版本。  
Yes, I already have a working setup for this. DM me and I’ll send the version that fits you.

### Price objection
`承认顾虑 + 给价值锚点`

Example:
如果只是体验一下，确实不一定适合所有人；但如果你是想直接拿来提升效率，这个会省很多试错时间。  
If you only want to try it casually, it may not fit everyone; but if you want something that saves trial-and-error time, that’s where the value is.

### Skepticism
`不对冲情绪 + 给一条事实`

Example:
你的顾虑正常，这类东西最怕讲得太虚。我这边更看重实际落地，所以只会讲能真正做成的部分。  
That concern is fair. This kind of topic easily sounds overhyped, so I focus on what can actually be implemented.

### Engagement
`轻互动 + 埋下下一条内容`

Example:
这个方向后面我会继续拆，下一条我讲最容易卡住的那一步。  
I’ll keep breaking this down. Next post I’ll cover the step where most people get stuck.

## 5. Auto-reply policy suggestion

Safe for draft-first or semi-auto:
- inquiry
- engagement
- common FAQs
- low-risk buying intent

Review first:
- price objection
- skepticism
- support issues
- policy-sensitive comments
- conflict-heavy threads

## 6. Batch handling strategy

When many comments arrive:
1. deduplicate similar comments
2. group into top 5-7 intent clusters
3. write one master reply per cluster
4. create 2-3 humanized variants
5. mark manual-review comments separately

## 7. Voice control

Possible brand voices:
- 专业克制 / professional and restrained
- 有温度但不油腻 / warm but not cheesy
- 创始人直给 / founder-like and direct
- 顾问式 / consultative

Pick one and stay consistent.

## 8. Execution design notes

A future executable version can connect:
- comment export source
- browser automation
- approval queue
- sent-reply log
- escalation keyword list

Prefer review-first before full automation.
