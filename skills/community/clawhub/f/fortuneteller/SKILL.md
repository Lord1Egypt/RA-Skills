---
name: zhouyi-benjing-oracle
clawhub-slug: zhouyi-benjing-oracle
description: |
  以《周易》本经原著为底，系统收集并逐一拆解市面上几乎所有可获取的同类 divination agents / skills / 程序，
  汲取百家之长，取其精华，去其糟粕，最终打磨成这一套更准确、更完整、更好用的周易系统。它把同类产品里
  最成熟的交互、百科式组织、起卦体验和规则呈现方式整合进来，同时去掉卦序错误、原文截断、白话混原文、
  未校验命理乱炖和伪精确排盘，让《周易》回到原著，也把产品做到更像市面上值得长期留下来的那一个。
  Built on the original Zhouyi text, this skill was forged by systematically collecting and dissecting virtually
  every comparable divination agent, skill, and app we could access, absorbing the best ideas across the field
  while stripping away the noise. We kept the strongest UX, encyclopedia structure, casting flow, and rule
  presentation, and removed the usual flaws: wrong hexagram mappings, truncated canon, paraphrase mixed into
  scripture, unverified metaphysics mashups, and fake precision. The result is a cleaner, stronger, and more
  enduring I Ching product.
license: MIT-0
compatibility:
  platforms:
    - claude-code
    - claude-ai
    - api
metadata:
  author: pineapple
  version: "1.0.0"
  tags: ["zhouyi", "yijing", "iching", "周易", "易经", "六十四卦", "占卜", "卦辞", "爻辞"]
  openclaw:
    emoji: "☯"
    skillKey: "zhouyi-benjing-oracle"
    requires:
      bins:
        - node
---

# 周易本经占筮

这是一个以《周易》本经为底座的技能包。它包含三部分能力：

1. `起卦`：三钱或蓍草起卦，按七种变爻规则取辞。
2. `查卦`：查六十四卦卦辞、爻辞、用九、用六。
3. `路由`：给出术数百科式总览，但只把周易本经模块当作已校验核心。

## 何时使用

当用户出现以下需求时，优先使用本技能：

- “帮我起一卦”
- “用周易看一下这件事”
- “查乾卦/屯卦/某句卦辞”
- “这个卦该看哪条爻辞”
- “周易和六爻/梅花/八字有什么区别”
- “我想看这个系统怎么用”

以下需求不要冒充已实现高精度：

- 八字排盘
- 奇门遁甲排盘
- 紫微斗数排盘
- 六爻纳甲断卦

这些内容目前只在 `术数百科` 中作为资料要求和边界说明存在。

## 默认工作流

### 1. 现场起卦

优先调用：

```bash
node scripts/zhouyi_cli.js cast --question "我是否该推进这次合作" --method coin --json
```

可选方法：

- `coin`：三钱法，6/7/8/9 概率为 1/8、3/8、3/8、1/8
- `yarrow`：蓍草概率模拟，6/7/8/9 概率为 1/16、5/16、7/16、3/16

如果需要复现结果，可带种子：

```bash
node scripts/zhouyi_cli.js cast --question "测试" --method coin --seed demo --json
```

### 2. 查某一卦

```bash
node scripts/zhouyi_cli.js lookup --name 乾 --json
node scripts/zhouyi_cli.js lookup --number 3 --json
```

### 3. 按关键词搜原文

```bash
node scripts/zhouyi_cli.js search --query "十年乃字" --json
node scripts/zhouyi_cli.js search --query "利涉大川" --json
```

### 4. 看术数百科路由

```bash
node scripts/zhouyi_cli.js catalog --json
node scripts/zhouyi_cli.js catalog --grade S --query 周易 --json
```

### 5. 打开内置网页

如果用户想要直接操作本地网页，打开根目录的 `index.html` 即可。网页包含：

- 周易本经占筮界面
- 六十四卦本经库
- 术数百科导航
- 近占记录

## 解读规则

调用 `cast` 后，按下列规则取辞：

1. 六爻不变：用本卦卦辞。
2. 一爻变：用该动爻爻辞。
3. 二爻变：用两个动爻爻辞，以上爻为主。
4. 三爻变：用本卦卦辞与变卦卦辞。
5. 四爻变：用两个静爻爻辞，以下爻为主。
6. 五爻变：用变卦中唯一静爻所对应的爻辞。
7. 六爻皆变：乾用用九，坤用用六，其余用变卦卦辞。

## 输出原则

1. 先交代本次取辞规则。
2. 再引用本经原文。
3. 最后给白话解释。
4. 不把解释说成确定命令。
5. 不用未校验体系污染周易本经结论。

## 参考资源

- 产品与验证说明：`references/README.md`
- 小白使用说明：`references/user-guide-zh.md`
- 本经底本：`references/zhouyi-benjing-source.txt`

## 维护命令

重建本经数据：

```bash
python3 scripts/build_zhouyi_data.py
```

运行校验：

```bash
node tests/verify_zhouyi_system.js
node tests/verify_system_catalog.js
node tests/verify_cli.js
```
