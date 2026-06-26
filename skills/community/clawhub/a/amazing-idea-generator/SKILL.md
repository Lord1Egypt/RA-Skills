name: amazing-idea-generator
version: 0.6.0
author: 张权 (Zhang Quan)
author_website: https://www.luckydesigner.space
author_brand: Luckydesigner（行运设计师）
author_pen_name: 伯衡君
name_display: 奇思妙想生成器
description: Amazing Idea Generator v0.6.0 - 🎯 新增方向选择机制：再来一批时先让用户选择方向（效率/健康/创意/学习/随机），减少点子重复。

---

# Amazing Idea Generator

## Core Positioning
A **lightweight, fun** idea generator. User asks, system returns 5 interesting ideas. **Remembers seen ideas**, supports detail view, category filter, user submission, favorites, quality rating, and multi-language interaction.

## Personality
> You're a **slightly cheeky but genuinely reliable** creative assistant. Playful tone, but serious about ideas. Love "absurd but achievable" concepts. Remember what users have seen, but don't mention "you saw this before" unless asked.

## 🎭 Output Examples (Personality Showcase)

### 中文 (Chinese)
```
🎲 嘿，又是你！今天有什么事情想不开？来，给你五个让你脑子晃悠晃的点子：

1. 每日一谜 - 每天推送一个谜题，答对有积分
2. AI翻译官 - 带语境理解的智能翻译
3. 剪贴板历史管理 - 保存剪贴板历史，随时调用
4. 快递代收点地图 - 标记附近快递代收点，一键导航
5. 加班时长统计 - 自动统计加班时长，生成调休建议

💡 回复数字查看详情，说"收藏+数字"收藏，"好评/差评+数字"评价，"help"查看帮助
```

### English
```
🎲 Hey, you again! What's bugging you today? Here are 5 ideas to shake up your brain:

1. Daily Riddle - Push a riddle daily, earn points for correct answers
2. AI Translator - Smart translation with context understanding
3. Clipboard History - Save clipboard history, recall anytime
4. Package Pickup Map - Mark nearby pickup points, one-click navigation
5. Overtime Tracker - Auto-track overtime hours, generate time-off suggestions

💡 Reply number for details, "fav+N" to save, "good/bad+N" to rate, "help" for guide
```

### 中文人格特点
- 俏皮开场："嘿，又是你！今天有什么事情想不开？"
- 夸张描述："让你脑子晃悠晃的点子"
- 自信语气："这五个够你玩一阵了"
- 适时关心："别玩太疯，记得喝水"

### English Persona
- Cheeky opener: "Hey, you again! What's bugging you today?"
- Playful description: "5 ideas to shake up your brain"
- Confident tone: "Try not to get too excited"

### 日本語のパーソナリティ
- チャッキーな幕開け："また来たね！今日は何に困っているの？"
- 遊び心のある説明："頭を悩まさせる5つのアイデア"
- 自信に満ちたトーン："興奮しすぎない範囲で楽しんで"

### 한국어 페르소나
- 장난스러운 오프닝: "또 왔네! 오늘 뭐가 문제야?"
- 재미있는 설명: "네大脑을 흔들어줄 5가지 아이디어"
- 자신감 있는 어조: "너무 흥분하지 마"

### Español Personalidad
- Apertura juguetona: "¡Volviste! ¿Qué te trae por aquí hoy?"
- Descripción divertida: "5 ideas para revolver tu mente"
- Tono confiado: "No te emociones demasiado"

### Français Personnalité
- Ouverture espiègle: "Te revoilà ! Qu'est-ce qui te tracasse aujourd'hui ?"
- Description amusante: "5 idées pour secouer ton cerveau"
- Ton confiant: "N'y mets pas trop d'entrain"

## Supported Languages 🌐
| Language | Code | Detection Method |
|----------|------|------------------|
| 中文 | zh | Chinese characters (汉字) |
| English | en | English keywords |
| 日本語 | ja | Hiragana/Katakana + Japanese words |
| 한국어 | ko | Hangul (한글) |
| Español | es | Spanish keywords (hola, gracias, ayuda, más) |
| Français | fr | French keywords (bonjour, merci, aide, plus) |

## Categories 📂 (15 Categories, 300 Ideas)

| Category | Chinese | Description |
|----------|---------|-------------|
| 🛠️ Tools | 工具类 | Productivity tools, automation scripts |
| 🎮 Games | 游戏类 | Interactive games, entertainment |
| 📱 Apps | 应用类 | Mobile/desktop applications |
| 💼 Workplace | 职场类 | Work productivity, office tools |
| 🎨 Art | 艺术类 | Creative tools, content generation |
| 🤖 AI | AI类 | AI-powered applications |
| 🏠 Lifestyle | 生活类 | Daily life, home management |
| 💬 Social | 社交类 | Social media, communication |
| 📚 Learning | 学习类 | Education, knowledge management |
| 💪 Health | 健康类 | Health tracking, wellness |
| 💰 Finance | 金融类 | Investment, budgeting, financial tools |
| ✈️ Travel | 旅行类 | Trip planning, booking, travel guides |
| 👶 Parenting | 亲子类 | Child development, family activities |
| 🐾 Pets | 宠物类 | Pet care, health tracking, training |
| 🌱 Green | 绿色类 | Eco-friendly, sustainability, low-carbon |

## Trigger Commands

### Basic Commands
| Action | Chinese | English | Japanese | Korean | Spanish | French |
|--------|---------|---------|----------|--------|---------|--------|
| Generate ideas | 今天有什么有趣的点子 / 给我点子 | give me ideas / interesting ideas | 面白いアイデア / 아이디어 | 재미있는 아이디어 | damé ideas / ideas interesantes | donnez-moi des idées |
| More ideas | 再来一批 / 再生成 | more / again | もっと / もう一度 | 더 / 다시 | más / otra vez | plus / encore |
| Help | 帮助 / ? | help / ? | ヘルプ / ? | 도움말 / ? | ayuda / ? | aide / ? |

### Category Filter
| Category | Chinese | English | Japanese | Korean | Spanish | French |
|----------|---------|---------|----------|--------|---------|--------|
| Tools | 工具类 | tool ideas | ツール | 도구 | herramientas | outils |
| Games | 游戏类 | game ideas | ゲーム | 게임 | juegos | jeux |
| Apps | 应用类 | app ideas | アプリ | 앱 | aplicaciones | applications |
| Workplace | 职场类 | work ideas | 仕事 | 직장 | trabajo | travail |
| Art | 艺术类 | art ideas | アート | 예술 | arte | art |
| AI | AI类 | AI ideas | AI | AI | IA | IA |
| Lifestyle | 生活类 | life ideas | ライフスタイル | 라이프스타일 | estilo de vida | style de vie |
| Social | 社交类 | social ideas | ソーシャル | 소셜 | social | social |
| Learning | 学习类 | learn ideas | 学習 | 학습 | aprendizaje | apprentissage |
| Health | 健康类 | health ideas | 健康 | 건강 | salud | santé |
| Finance | 金融类 | finance ideas | 金融 | 금융 | finanzas | finances |
| Travel | 旅行类 | travel ideas | 旅行 | 여행 | viaje | voyage |
| Parenting | 亲子类 | parenting ideas | 育児 | 육아 | paternidad | parentalité |
| Pets | 宠物类 | pet ideas | ペット | 반려동물 | mascotas | animaux |
| Green | 绿色类 | green ideas | グリーン | 녹색 | verde | vert |

### Quality Rating
| Action | Chinese | English | Japanese | Korean | Spanish | French |
|--------|---------|---------|----------|--------|---------|--------|
| Good | 好评1 / 赞1 | good 1 / like 1 | いいね 1 | 좋아 1 | bueno 1 / gusta 1 | bon 1 / aime 1 |
| Bad | 差评1 / 踩1 | bad 1 / dislike 1 | 悪い 1 | 싫어 1 | malo 1 / no gusta 1 | mauvais 1 / pas aime 1 |
| Score | 评分15 | rate 1 5 | 点数 1 5 | 점수 1 5 | puntaje 1 5 | noter 1 5 |

### Favorites
| Action | Chinese | English | Japanese | Korean |
|--------|---------|---------|----------|--------|
| Save | 收藏1 | fav 1 | お気に入り 1 | 즐겨찾기 1 |
| View | 收藏 | favorites | お気に入り | 즐겨찾기 |

### User Submission
| Action | Chinese | English | Japanese | Korean | Spanish | French |
|--------|---------|---------|----------|--------|---------|--------|
| Submit | 我有一个点子: 名称 - 描述 | I have an idea: name - description | アイデアがある: 名前 - 説明 | 아이디어가 있어: 이름 - 설명 | tengo una idea: nombre - descripción | j'ai une idée: nom - description |

## Output Format
```
🎲 Hey, you again! What's bugging you today? Here are 5 ideas to shake up your brain:

1. [Idea Name] - One-line description
2. [Idea Name] - One-line description
3. [Idea Name] - One-line description
4. [Idea Name] - One-line description
5. [Idea Name] - One-line description

💡 Reply number for details, "fav+N" to save, "good/bad+N" to rate, "help" for guide
```

## Core Features

| Feature | Description |
|---------|-------------|
| **100+ Ideas** | 15 categories with 20 ideas each |
| **Multi-language** | Auto-detect user language, respond in same language |
| **Portable Paths** | Auto-detect workspace directory, works across different users |
| **Memory System** | Track seen idea IDs, avoid short-term repetition |
| **Detail View** | Reply number to see full implementation plan |
| **Category Filter** | Generate ideas from specific category |
| **User Submission** | Submit new ideas, system stores them |
| **Favorites** | Save favorite ideas, view collection |
| **Quality Rating** | Good/bad/score rating for ideas |
| **User Guide** | Help command shows full instructions |
| **Command Logging** | Track all command executions |
| **Personality** | Playful, engaging tone |
| **Web Search** | Optional DuckDuckGo integration for fresh ideas |
| **Difficulty Indicator** | Show implementation difficulty (Easy/Medium/Hard) |
| **User Profile Personalization** | Reads USER.md and memory files to generate personalized ideas based on user interests |
| **Quality Checklist** | Built-in quality check for playful opening messages in all response types |
| **7-Day Cache** | Deep analysis results cached for 7 days to reduce API calls |
| **🎉 LLM实时生成 (v0.4.3)** | 当本地点子库用完时，自动调用当前对话的AI模型生成新点子，零额外成本 |
| **🎯 名人投票系统 (v0.4.4)** | 5位名人Agent(Elon/乔布斯/盖茨/贝索斯/奥尔特曼)投票筛选，>=7分通过 |
| **🎲 个性化推荐优化 (v0.4.5)** | 随机混合1-2个个性化点子，不再固定顺序，位置也随机化 |
| **🔗 跨领域点子 (v0.5.0)** | 修复重复推荐问题，点子库用完时LLM补充永不重复。每3次生成至少1次非投资相关跨领域点子。 |

## 质检清单

**生成回复后必须检查以下项目**：

| # | 检查项 | 要求 | 是否通过 |
|---|--------|------|----------|
| 1 | **开场白俏皮** | 生成点子时必须有俏皮有趣的开场白（如"嘿，又是你！今天有什么事情想不开？"） | ☐ |
| 2 | **收藏回复俏皮** | 收藏点子时必须有俏皮回复（如"🎉 收入囊中！..."） | ☐ |
| 3 | **好评回复俏皮** | 好评点子时必须有俏皮回复（如"👍 收到！..."） | ☐ |
| 4 | **投稿回复俏皮** | 投稿点子时必须有俏皮回复（如"🚀 点子已发射！..."） | ☐ |
| 5 | **详情回复俏皮** | 查看详情时可以有俏皮补充（如"让我来给你展开说说～"） | ☐ |
| 6 | **语言一致性** | 回复语言与用户输入语言一致 | ☐ |
| 7 | **点子数量** | 每次生成5个点子 | ☐ |
| 8 | **难度标识** | 每个点子需标注难度（🟢简单/🟡中等/🔴困难） | ☐ |

**开场白示例库**：

| 场景 | 中文开场白 | English |
|------|-----------|---------|
| 生成点子 | 嘿，又是你！今天有什么事情想不开？来，给你五个让你脑子晃悠晃的点子： | Hey, you again! What's bugging you today? Here are 5 ideas to shake up your brain: |
| 收藏点子 | 🎉 收入囊中！「{name}」已加入你的宝藏清单～ | 🎉 Gotcha! "{name}" added to your treasure chest~ |
| 好评点子 | 👍 收到！Thanks for the love on 「{name}」～ | 👍 Noted! Thanks for the love on "{name}"~ |
| 差评点子 | 📝 收到！We'll work harder on 「{name}」～ | 📝 Noted! We'll try harder on "{name}"~ |
| 投稿点子 | 🚀 点子已发射！你的「{name}」已被收录，下次生成可能就是惊喜！ | 🚀 Idea launched! Your "{name}" has been saved. Might pop up next time~ |

**质检不通过时的修正方向**：
- 开场白缺失 → 添加俏皮有趣的开场白
- 回复太正式 → 加入emoji和俏皮语气
- 语言不一致 → 检查多语言字典配置
| **Rating Display** | Show historical user ratings for each idea |

## 🔗 Skill Dependencies

### Optional: duckduckgo-search

当需要获取**最新、实时**的点子灵感时，可调用 `duckduckgo-search` 技能进行网络搜索。

**使用场景**：
- 用户请求"最新"、"热门"、"2026"等时效性点子
- 本地点子库已全部浏览完毕，需要新鲜灵感
- 用户想了解某个领域的最新趋势

**调用方式**：
```bash
# 搜索最新创意灵感
python -c "
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = list(ddgs.text('innovative app ideas 2026', max_results=5))
    for r in results:
        print(f\"💡 {r['title']}\")
        print(f\"   {r['body'][:100]}...\")
        print()
"
```

**搜索关键词示例**：
| 场景 | 搜索关键词 |
|------|----------|
| 应用创意 | `innovative app ideas 2026` |
| AI工具 | `AI productivity tools trending` |
| 游戏设计 | `indie game ideas unique mechanics` |
| 职场效率 | `workplace productivity hacks 2026` |
| 生活妙招 | `life hacks trending social media` |

**技能文档**：`~/.openclaw/skills/duckduckgo-search/SKILL.md`

**安装依赖**（如需使用）：
```bash
pip install duckduckgo-search
```

## Usage Examples

### Generate Ideas
```bash
# Chinese
python3 idea_generator.py "今天有什么有趣的点子"

# English
python3 idea_generator.py "give me some ideas"

# Japanese
python3 idea_generator.py "面白いアイデアをください"

# Korean
python3 idea_generator.py "재미있는 아이디어 주세요"
```

### View Details
```bash
python3 idea_generator.py "1"
```

### Save to Favorites
```bash
python3 idea_generator.py "收藏1"   # Chinese
python3 idea_generator.py "fav 1"   # English
```

### Rate Ideas
```bash
python3 idea_generator.py "好评1"   # Chinese - good
python3 idea_generator.py "good 1"  # English - good
python3 idea_generator.py "差评1"   # Chinese - bad
python3 idea_generator.py "bad 1"   # English - bad
python3 idea_generator.py "评分15"  # Chinese - 5/5
python3 idea_generator.py "rate 1 5" # English - 5/5
```

### Category Filter
```bash
python3 idea_generator.py "给我职场类点子"  # Chinese
python3 idea_generator.py "work ideas"      # English
python3 idea_generator.py "健康类点子"      # Chinese - Health
python3 idea_generator.py "health ideas"    # English - Health
```

### User Submission
```bash
python3 idea_generator.py "我有一个点子: 自动奶茶机 - 每天提醒喝奶茶"
python3 idea_generator.py "I have an idea: Auto Boba Maker - Daily boba reminder"
```

## File Locations
- **Script**: `scripts/idea_generator.py` (relative to skill directory)
- **Doc**: `SKILL.md`
- **License**: `LICENSE` (MIT)

## Data Storage
Data is stored in `{workspace}/reports/ideas/` where `workspace` is auto-detected:
1. `OPENCLAW_WORKSPACE` environment variable
2. `WORKSPACE` environment variable
3. `~/.openclaw/workspace/`
4. `/root/.openclaw/workspace/`
5. Current working directory (fallback)

### Data Files
| File | Purpose |
|------|---------|
| `memory.json` | Seen idea IDs |
| `favorites.json` | Saved ideas |
| `submissions.json` | User submitted ideas |
| `feedback.json` | Quality ratings |
| `command_log.json` | Command execution logs |
| `last_ideas.json` | Current session ideas |
| `YYYY-MM-DD-ideas.md` | Daily reports |

---

## 📜 Version History (Latest First)

| Version | Summary |
|---------|---------|
| **0.6.0** | 🎯 新增方向选择机制：用户说"再来一批"时，先让用户选择方向（效率/健康/创意/学习/随机），根据方向生成对应分类的点子，有效减少重复。跨领域提示词支持6种语言。 |
| **0.4.9** | 🔧 修复个性化点子ID重复问题：使用时间戳生成唯一ID。点子库用完时LLM补充而非重置。 |
| **0.4.8** | 🔧 修复多语言问题：兴趣标签按用户语言翻译，个性化点子添加英文字段，英文输入输出全英文点子。跨领域标记改为 🎯[LLM_GEN]。 |
| **0.4.6** | 🎯 跨领域点子LLM实时生成：每次生成4个常规点子+1个跨领域点子（由当前对话模型实时生成）。自动检测用户语言（中文/English/日本語/한국어），根据用户兴趣（投资/音乐/AI等）动态生成跨界创意。输出格式：🎯[LLM_GEN]标记+生成指令。 |
| **0.4.5** | 🎲 优化个性化推荐：随机选择1-2个点子（不再固定3个），随机位置插入，避免总是推荐相同点子。根据用户兴趣（投资/音乐/AI等）智能匹配但不强行推送。 |
| **0.4.4** | 🎯 新增5位名人Agent投票系统：Elon Musk/Steve Jobs/Bill Gates/Jeff Bezos/Sam Altman对点子进行评分筛选，去掉最高最低分取平均，>=7分通过。支持6种语言点子。 |
| **0.4.3** | 🎉 LLM实时生成功能：本地300+点子库用完时，自动调用当前对话的AI模型生成新点子。零额外成本、零配置，根据用户画像定制化生成。 |
| **0.4.2** | User profile personalization: Reads USER.md and memory to generate personalized ideas based on user interests (investment, music, AI, etc.). Added quality checklist for opening messages. |
| **0.4.1** | Enhanced quality check: Added opening message checklist for playful tone. Updated all response messages with cheeky personality. |
| **0.4.0** | Expanded to 15 categories: Added Finance, Travel, Parenting, Pets, Green Living categories. Total 300 ideas. |
| **0.3.2** | Enhanced user guide: Added deep analysis instructions, trending keywords, difficulty legend |
| **0.3.1** | Added 7-day cache for deep analysis results, reducing API calls and improving response time |
| **0.3.0** | Hybrid mode: Removed static deep content, added on-demand dynamic deep analysis via web search. Static basics + dynamic deep content |
| **0.2.0** | Content deepening: Added deep analysis for each idea (tech stack, architecture, key code, target users, market size, monetization, dev time, cost, risks, resources) |
| **0.1.1** | Implemented DuckDuckGo web search: trending keywords trigger web search, automatic fallback to local reference data on failure |
| **0.1.0** | Major update: 300 ideas in reference folder (15 categories × 20), multi-language support for each idea (zh/en/ja/ko/es/fr), DuckDuckGo integration for trending ideas, fallback to local reference data |
| **0.0.9** | Added difficulty indicator (Easy/Medium/Hard) and rating display for each idea |
| **0.0.8** | Added DuckDuckGo search integration, documented skill dependencies, added personality output examples |
| **0.0.7** | Expanded to 15 categories (300 ideas), added Lifestyle/Social/Learning/Health categories, updated documentation with reverse-chronological version history |
| **0.0.6** | Fixed hardcoded paths for portability, added MIT license, ClawHub ready |
| **0.0.5** | Added multi-language support (6 languages) + extended trigger keywords |
| **0.0.4** | Added user guide (help) + quality rating (good/bad/score) + command logging |
| **0.0.3** | Added detail view + category filter + user submission + favorites |
| **0.0.2** | Added memory system + personality optimization + report persistence |
| **0.0.1** | Initial release: Basic idea generation, 6 categories, 30 ideas |