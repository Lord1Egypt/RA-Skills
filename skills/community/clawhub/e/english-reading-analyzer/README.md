# English Reading Analyzer 🐳

英语阅读长难句分析 Skill，适用于考研英语、四六级等考试阅读。

## 核心功能

- **五步分析法**：断句 → 找主干 → 翻主干 → 翻修饰 → 合成
- **五大基本句型**：S V / S V O / S V O O / S V O C / S V C
- **后置定语**：7 种类型 + 翻译规则（介词短语/to do/V-ing/V-ed/形容词短语）
- **定语 vs 状语区分**："有名词优先定语"原则
- **并列结构识别**：从后往前找 + 省略陷阱
- **同位语**：5 种形式 + A=B 等号关系
- **非谓语**：to do / doing / done 的判断
- **逻辑敏感度**：因果/对比/并列/递进

## 安装

### OpenClaw 用户

从 ClawHub 一键安装：
```
（待发布）
```

## 触发词

梳理阅读 / 分析句子 / 长难句 / 阅读理解 / 拆解句子 / 精读分析 / 英语阅读

## 示例

```
用户：梳理阅读这句话：
During the 2016 presidential campaign, nearly a quarter of web content 
shared by Twitter users in the politically critical state of Michigan 
was fake news.

输出：
📌 主干：web content was fake news → 网络内容是假新闻
📍 修饰拆解：
  - During...campaign → 时间状语
  - shared by...users → 过去分词后置定语，修饰 web content
  - in...Michigan → 介词短语定语，修饰 users
🔗 完整翻译：2016年总统大选期间，密歇根州推特用户分享的近四分之一的网络内容是假新闻
```

## 知识点来源

整理自考研英语语法课程讲义（6 课时），覆盖：
1. 五大基本句型 + 句子切分
2. 后置定语 + 定语状语区分
3. 并列结构 + 省略陷阱
4. 同位语 + 插入语
5. 词义选择 + 逻辑敏感
6. 非谓语 + 综合实战

## License

MIT
