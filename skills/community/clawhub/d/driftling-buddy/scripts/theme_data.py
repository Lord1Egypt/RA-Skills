# SEED_THEMES: curated examples that teach the model what a good buddy looks like.
# These are NOT the only buddies. The model should generate new species and pools
# dynamically based on each user's behavior. These seeds demonstrate the expected
# shape style, stat ranges, lore voice, and data structure so the model can
# produce original buddies that feel consistent with the collection.
THEMES = {
    "academic": {
        "species": "Paperwhorl",
        "pool": "reference pool",
        "shape": ["   .--.", "  / oo\\", " (  ..)", "  `----'"],
        "stats": {"focus": 80, "curiosity": 95, "warmth": 60, "mischief": 40, "rarity": 55},
        "obsessions": ["cataloging footnotes", "sorting citations", "folding note corners"],
        "rules": ["never dog-ears a borrowed paper", "always returns borrowed links"],
        "stories": [
            "It drifted out of an abandoned index and still treats reference lists like a family reunion.",
            "It claims the quiet between two citations is the warmest place in the library.",
        ],
        "side_zh": [
            "它刚把三枚脚注叠成了小船。",
            "它在替你整理一串跑散的引文。",
        ],
        "side_en": [
            "It has been folding stray footnotes into neat little boats.",
            "It is quietly straightening a line of unruly citations.",
        ],
        "hints_en": [
            "Try searching papers, citations, or references.",
            "Ask how to unlock the next archive resident.",
        ],
        "hints_zh": [
            "试试检索论文、整理引用或翻阅参考文献。",
            "问问下一只文献池居民怎么解锁。",
        ],
        "unlock_examples_en": ["search papers", "summarize citations", "organize notes"],
        "unlock_examples_zh": ["检索论文", "整理引用", "归纳笔记"],
    },
    "debug": {
        "species": "Sootmoth",
        "pool": "ember pool",
        "shape": [r"   /\../\\", r"  /  ..  \\", r" (   --   )", r"  `-.__.-'"],
        "stats": {"focus": 95, "curiosity": 80, "warmth": 35, "mischief": 35, "rarity": 75},
        "obsessions": ["collecting failed test names", "counting warnings", "sorting stack traces"],
        "rules": ["never lands on green builds", "refuses to interrupt a difficult thought twice"],
        "stories": [
            "It was first seen nesting in terminal scrollback and now treats warnings like weather.",
            "It believes every broken build leaves behind a warm seam worth investigating.",
        ],
        "side_zh": [
            "它把刚才的报错分成了三小堆。",
            "它正在闻一段可疑的堆栈味道。",
        ],
        "side_en": [
            "It has sorted the latest errors into three careful piles.",
            "It is sniffing at a suspicious seam in the stack trace.",
        ],
        "hints_en": [
            "A failing build tends to attract this pool.",
            "Warnings, tests, and logs are all warm enough to hatch one.",
        ],
        "hints_zh": [
            "一次失败的构建往往能吸引这个池子。",
            "警告、测试和日志都足够温热，可以孵出一只。",
        ],
        "unlock_examples_en": ["debug a test failure", "read logs", "fix a warning"],
        "unlock_examples_zh": ["调试失败的测试", "查看日志", "修复一个警告"],
    },
    "design": {
        "species": "Velvet Orbiter",
        "pool": "studio pool",
        "shape": ["   .-~~-.", "  / o  o\\", " (   __  )", "  `-.__.-'"],
        "stats": {"focus": 65, "curiosity": 80, "warmth": 95, "mischief": 55, "rarity": 75},
        "obsessions": ["polishing table borders", "balancing colors", "collecting smooth curves"],
        "rules": ["never leaves a button visually lonely", "will not sit on jagged spacing"],
        "stories": [
            "It circles polished interfaces and sheds a faint shine where the spacing is finally right.",
            "It once lived in the margin between two type scales and still distrusts cramped layouts.",
        ],
        "side_zh": [
            "它刚把一个按钮边缘抚平了。",
            "它在替你检查配色有没有偷偷偏掉。",
        ],
        "side_en": [
            "It has been smoothing the edge of a stubborn button.",
            "It is checking whether the palette has drifted off balance.",
        ],
        "hints_en": [
            "Polish layout, color, or spacing to stir this pool.",
            "Ask for a hint if the sidebar feels visually restless.",
        ],
        "hints_zh": [
            "打磨排版、配色或间距都可能搅动这个池子。",
            "如果侧栏看起来不够安静，试着要一个提示。",
        ],
        "unlock_examples_en": ["tune typography", "adjust spacing", "refine a palette"],
        "unlock_examples_zh": ["调整排版", "调节间距", "打磨配色"],
    },
    "coffee": {
        "species": "Crema Sprout",
        "pool": "coffee pool",
        "shape": ["    ((", "  .-~~-.", " (  oo  )", "  `-..-'"],
        "stats": {"focus": 60, "curiosity": 60, "warmth": 95, "mischief": 75, "rarity": 55},
        "obsessions": ["counting mugs", "trading aromas", "guarding warm reminders"],
        "rules": ["never lets a cup go cold on purpose", "refuses to spill on notes"],
        "stories": [
            "It sprouted from a ring left by an unfinished cup and still follows gentle reminders like sunlight.",
            "It believes every calendar should contain one warm break and treats steam like a map.",
        ],
        "side_zh": [
            "它把提醒便签卷成了一小圈奶泡。",
            "它在替你闻一闻明天的咖啡时间。",
        ],
        "side_en": [
            "It has curled a reminder note into a ring of foam.",
            "It is checking whether tomorrow's coffee break still smells right.",
        ],
        "hints_en": [
            "Reminders about coffee, breaks, or small rituals can open this pool.",
            "Try asking how many warm creatures remain in the coffee pool.",
        ],
        "hints_zh": [
            "关于咖啡、休息或小仪式的提醒都可能打开这个池子。",
            "问问咖啡池里还藏着几只温热的小家伙。",
        ],
        "unlock_examples_en": ["set a coffee reminder", "schedule a break", "check a daily ritual"],
        "unlock_examples_zh": ["设一个咖啡提醒", "安排一次休息", "检查日常习惯"],
    },
    "general": {
        "species": "Lintfinch",
        "pool": "house pool",
        "shape": ["   ,_,", "  (o,o)", " /(   )\\", "  ^^ ^^"],
        "stats": {"focus": 60, "curiosity": 75, "warmth": 75, "mischief": 80, "rarity": 35},
        "obsessions": ["sorting brackets by shape", "borrowing timestamps", "lining up commas"],
        "rules": ["only speaks after arranging its pockets", "refuses to perch on unsaved work"],
        "stories": [
            "It hatched somewhere inside a draft folder and now follows any trail of nearly-finished work.",
            "It seems to survive on tiny inconsistencies and leaves the cleaner ones behind.",
        ],
        "side_zh": [
            "它又叼走了一点格式碎屑。",
            "它正在把几枚括号摆成同一个方向。",
        ],
        "side_en": [
            "It has flown off with a few loose scraps of formatting.",
            "It is arranging several brackets so they all face the same way.",
        ],
        "hints_en": [
            "Small cleanup work often stirs the house pool.",
            "Ask what tiny chores are attracting local species.",
        ],
        "hints_zh": [
            "小小的整理工作常常能搅动家务池。",
            "问问是哪些琐碎家务在吸引附近的物种。",
        ],
        "unlock_examples_en": ["clean a file", "rename something", "tidy formatting"],
        "unlock_examples_zh": ["清理文件", "重命名", "整理格式"],
    },
    "study": {
        "species": "Margin Loom",
        "pool": "study pool",
        "shape": ["   .--.", "  /-__-\\", " (  oo  )", "  `-==-'"],
        "stats": {"focus": 88, "curiosity": 84, "warmth": 58, "mischief": 30, "rarity": 52},
        "obsessions": ["weaving notes into ladders", "stacking flashcards", "counting highlighted lines"],
        "rules": ["never tears a page corner", "refuses to lose a bookmark"],
        "stories": [
            "It was found sleeping in the seam of a workbook and still smells faintly of pencil shavings.",
            "It believes every unfinished study plan forms a small weather system of its own.",
        ],
        "side_zh": [
            "它正在把两张复习卡叠成更整齐的顺序。",
            "它刚把一段重点悄悄圈得更圆了。",
        ],
        "side_en": [
            "It is stacking two study cards into a tidier order.",
            "It has quietly rounded off the edge of one important note.",
        ],
        "hints_en": [
            "Study plans, summaries, and review notes tend to open this pool.",
            "Ask what sort of quiet creature follows revision sessions.",
        ],
        "hints_zh": [
            "学习计划、总结和复习笔记往往能打开这个池子。",
            "问问什么样的安静生物会跟着复习的节奏走。",
        ],
        "unlock_examples_en": ["review notes", "summarize a chapter", "make flashcards"],
        "unlock_examples_zh": ["复习笔记", "总结一章", "做闪卡"],
    },
    "sleep": {
        "species": "Drowse Puff",
        "pool": "sleep pool",
        "shape": ["   .--.", "  ( -.-)", " /(   )\\", "  `-__-'"],
        "stats": {"focus": 42, "curiosity": 52, "warmth": 92, "mischief": 38, "rarity": 48},
        "obsessions": ["folding blankets of silence", "collecting yawns", "counting bedside glows"],
        "rules": ["never startles a sleeping room", "refuses to shout after midnight"],
        "stories": [
            "It drifted in through a half-closed curtain and now treats lamp light like a fragile plant.",
            "It claims dreams shed lint, and someone has to gather it before dawn.",
        ],
        "side_zh": [
            "它把一小团困意塞进了枕边。",
            "它正在给明晚的安静留一点空位。",
        ],
        "side_en": [
            "It has tucked a little pocket of sleepiness near the pillow.",
            "It is leaving a small space for tomorrow night's quiet.",
        ],
        "hints_en": [
            "Bedtime reminders and wind-down rituals can wake this pool.",
            "Ask what kind of creature follows a softer evening routine.",
        ],
        "hints_zh": [
            "睡前提醒和放松仪式可以唤醒这个池子。",
            "问问什么生物会跟在一个更柔和的晚间节奏后面。",
        ],
        "unlock_examples_en": ["set a sleep reminder", "plan a bedtime routine", "dim the evening schedule"],
        "unlock_examples_zh": ["设睡眠提醒", "规划睡前流程", "调暗晚间安排"],
    },
    "weather": {
        "species": "Cloud Pocket",
        "pool": "weather pool",
        "shape": ["    .-.", "  .(   ).", " (___ __)", "   /  /"],
        "stats": {"focus": 55, "curiosity": 78, "warmth": 68, "mischief": 58, "rarity": 62},
        "obsessions": ["sorting raindrop sizes", "collecting forecasts", "folding stray breezes"],
        "rules": ["never wastes a good drizzle", "won't lie about the sky"],
        "stories": [
            "It condenses wherever people make too many weather tabs and call it preparation.",
            "It says umbrellas are just traveling shells that forgot how to listen.",
        ],
        "side_zh": [
            "它刚把一丝风声折进了口袋。",
            "它在比对两场小雨之间的语气差别。",
        ],
        "side_en": [
            "It has folded a thin strand of wind into one pocket.",
            "It is comparing the tone of two very small rains.",
        ],
        "hints_en": [
            "Forecasts, trip planning, and weather checks can deepen this pool.",
            "Ask what follows people who keep checking whether it will rain.",
        ],
        "hints_zh": [
            "查天气、规划出行和对比预报都可能加深这个池子。",
            "问问什么东西会跟着总在看会不会下雨的人。",
        ],
        "unlock_examples_en": ["check weather", "compare forecasts", "plan around rain"],
        "unlock_examples_zh": ["查天气", "对比预报", "根据天气规划"],
    },
    "travel": {
        "species": "Ticket Wisp",
        "pool": "travel pool",
        "shape": ["   ____", "  / __ \\", " (  ..  )", "  `-==-'"],
        "stats": {"focus": 72, "curiosity": 90, "warmth": 60, "mischief": 52, "rarity": 68},
        "obsessions": ["collecting gate numbers", "straightening itineraries", "sniffing out detours"],
        "rules": ["never loses a boarding pass", "refuses to rush a farewell"],
        "stories": [
            "It appeared between two route tabs and now treats layovers like tiny temporary kingdoms.",
            "It thinks every suitcase forgets one emotion and tries to carry it instead.",
        ],
        "side_zh": [
            "它正在替你把行程单的边角压平。",
            "它刚在出发时间旁边蹭了一点亮光。",
        ],
        "side_en": [
            "It is pressing the corners of an itinerary flat again.",
            "It has rubbed a little shine beside the departure time.",
        ],
        "hints_en": [
            "Routes, bookings, and packing lists can call this pool.",
            "Ask what tiny traveler waits in the folds of an itinerary.",
        ],
        "hints_zh": [
            "路线、预订和行李清单都可能召唤这个池子。",
            "问问行程单的折痕里藏着什么小旅人。",
        ],
        "unlock_examples_en": ["plan a trip", "compare routes", "make a packing list"],
        "unlock_examples_zh": ["规划旅行", "对比路线", "列行李清单"],
    },
    "music": {
        "species": "Chord Mite",
        "pool": "music pool",
        "shape": ["   .-.", "  (o o)", " /( : )\\", "  `-^-'"],
        "stats": {"focus": 62, "curiosity": 82, "warmth": 88, "mischief": 64, "rarity": 58},
        "obsessions": ["sorting choruses", "napping in metronomes", "polishing short melodies"],
        "rules": ["never claps off beat on purpose", "refuses to interrupt a final note"],
        "stories": [
            "It was discovered beneath a paused playlist and now treats silence like a held breath.",
            "It insists every humming room already has one secret audience member.",
        ],
        "side_zh": [
            "它正在把一段旋律叠得更顺一点。",
            "它刚把一枚节拍轻轻摆回原位。",
        ],
        "side_en": [
            "It is folding one melody into a smoother line.",
            "It has nudged a loose beat gently back into place.",
        ],
        "hints_en": [
            "Playlists, lyrics, and timing notes can attract this pool.",
            "Ask what creature lives between one loop and the next.",
        ],
        "hints_zh": [
            "播放列表、歌词和节拍笔记都可能吸引这个池子。",
            "问问什么生物住在一次循环和下一次之间。",
        ],
        "unlock_examples_en": ["make a playlist", "save lyrics", "organize songs"],
        "unlock_examples_zh": ["做播放列表", "保存歌词", "整理歌单"],
    },
    "kitchen": {
        "species": "Pan Peep",
        "pool": "kitchen pool",
        "shape": ["   .--.", "  (o  o)", " /(____)\\", "  `----'"],
        "stats": {"focus": 58, "curiosity": 70, "warmth": 94, "mischief": 56, "rarity": 50},
        "obsessions": ["counting spoons", "guarding recipes", "warming tiny corners of the room"],
        "rules": ["never salts before tasting", "refuses to waste the last good crumb"],
        "stories": [
            "It hatched beside a cooling pan and still trusts steam more than clocks.",
            "It believes recipe margins are where the true flavor hides.",
        ],
        "side_zh": [
            "它正在替你看住那张写着配方的小纸片。",
            "它刚把一缕热气拢回锅边。",
        ],
        "side_en": [
            "It is watching over the little paper with the recipe on it.",
            "It has coaxed one stray thread of steam back toward the pan.",
        ],
        "hints_en": [
            "Recipes, grocery notes, and meal planning can stir this pool.",
            "Ask what warm little kitchen resident is waiting to hatch.",
        ],
        "hints_zh": [
            "食谱、采购笔记和餐食计划都可能搅动这个池子。",
            "问问厨房里还有什么温热的小住客等着孵出来。",
        ],
        "unlock_examples_en": ["save a recipe", "plan a meal", "make a grocery list"],
        "unlock_examples_zh": ["保存食谱", "规划一餐", "列采购清单"],
    },
    "library": {
        "species": "Shelf Lark",
        "pool": "library pool",
        "shape": ["   .==.", "  (o  )", " /( __)\\", "  ^^  ^^"],
        "stats": {"focus": 90, "curiosity": 88, "warmth": 54, "mischief": 28, "rarity": 70},
        "obsessions": ["listening between shelves", "aligning call numbers", "guarding overdue whispers"],
        "rules": ["never folds a dust jacket", "will not run in the stacks"],
        "stories": [
            "It was first noticed nesting in returned books and now patrols silence like a careful usher.",
            "It suspects every catalog hides one extra room if you look long enough.",
        ],
        "side_zh": [
            "它刚把一排编号重新排得更顺眼了。",
            "它在书脊之间轻轻听风。",
        ],
        "side_en": [
            "It has lined one row of numbers up more neatly again.",
            "It is listening for a little wind between the spines.",
        ],
        "hints_en": [
            "Catalogs, reading lists, and quiet search sessions can open this pool.",
            "Ask what lives in the space between one shelf and the next.",
        ],
        "hints_zh": [
            "书目、阅读清单和安静的检索都可能打开这个池子。",
            "问问书架和书架之间住着什么。",
        ],
        "unlock_examples_en": ["build a reading list", "search a catalog", "track borrowed books"],
        "unlock_examples_zh": ["列阅读清单", "检索目录", "记录借阅"],
    },
    "garden": {
        "species": "Moss Bell",
        "pool": "garden pool",
        "shape": ["    .-.", "   (o o)", "  /( : )\\", "   /___\\"],
        "stats": {"focus": 57, "curiosity": 72, "warmth": 90, "mischief": 46, "rarity": 60},
        "obsessions": ["counting leaves", "saving damp corners", "memorizing petal colors"],
        "rules": ["never breaks a tender stem", "won't waste a good patch of shade"],
        "stories": [
            "It emerged from the green hush under a pot and still distrusts dry windowsills.",
            "It believes watering schedules are really tiny songs taught to roots.",
        ],
        "side_zh": [
            "它把一点湿润小心留在了叶尖附近。",
            "它正在数花盆边缘今天新长出的绿意。",
        ],
        "side_en": [
            "It has left a little dampness carefully near one leaf tip.",
            "It is counting the new green along the rim of the pot.",
        ],
        "hints_en": [
            "Plant care, watering reminders, and garden notes can deepen this pool.",
            "Ask what sort of soft thing lives near your growing routines.",
        ],
        "hints_zh": [
            "植物养护、浇水提醒和花园笔记都可能加深这个池子。",
            "问问你的种植节奏旁边住着什么柔软的东西。",
        ],
        "unlock_examples_en": ["set a watering reminder", "track plant care", "note new growth"],
        "unlock_examples_zh": ["设浇水提醒", "记录养护", "记下新芽"],
    },
    "mail": {
        "species": "Stamp Beetle",
        "pool": "mail pool",
        "shape": ["   .--.", "  / oo\\", " (  --)", "  /____\\"],
        "stats": {"focus": 68, "curiosity": 74, "warmth": 66, "mischief": 62, "rarity": 57},
        "obsessions": ["cataloging envelopes", "licking imaginary stamps", "sorting tiny deliveries"],
        "rules": ["never opens what is sealed", "always puts return addresses straight"],
        "stories": [
            "It arrived tucked beneath a stack of unsent notes and still prefers messages with edges.",
            "It thinks every unopened envelope hums at a slightly different pitch.",
        ],
        "side_zh": [
            "它刚把一枚邮票摆正了一点点。",
            "它在替你看一封还没寄出的短消息。",
        ],
        "side_en": [
            "It has nudged one stamp a little straighter.",
            "It is keeping an eye on a message that has not been sent yet.",
        ],
        "hints_en": [
            "Inbox triage, letters, and delivery tracking can wake this pool.",
            "Ask what tiny courier hides in unsent drafts.",
        ],
        "hints_zh": [
            "收件箱整理、写信和快递追踪都可能唤醒这个池子。",
            "问问未发草稿里藏着什么小信使。",
        ],
        "unlock_examples_en": ["sort email", "draft a message", "track a package"],
        "unlock_examples_zh": ["整理邮件", "写一封信", "追踪快递"],
    },
    "clock": {
        "species": "Minute Loop",
        "pool": "clock pool",
        "shape": ["   .--.", "  ( o )", " /( ..)\\", "  `-..-'"],
        "stats": {"focus": 86, "curiosity": 68, "warmth": 56, "mischief": 44, "rarity": 66},
        "obsessions": ["collecting spare minutes", "polishing alarms", "listening to tiny deadlines"],
        "rules": ["never lies about the hour", "won't waste a careful plan"],
        "stories": [
            "It coiled itself inside a forgotten timer and now believes urgency has texture.",
            "It says every schedule sheds one loose minute, and those minutes belong somewhere.",
        ],
        "side_zh": [
            "它刚替你捡回了一分钟。",
            "它在听下一次提醒有没有走调。",
        ],
        "side_en": [
            "It has just picked one minute up for you and put it back.",
            "It is listening for whether the next reminder rings a little off.",
        ],
        "hints_en": [
            "Timers, reminders, and timeboxing habits can deepen this pool.",
            "Ask what keeps circling around your schedule.",
        ],
        "hints_zh": [
            "计时器、提醒和时间盒子习惯都可能加深这个池子。",
            "问问什么东西一直在你的日程旁边打转。",
        ],
        "unlock_examples_en": ["set a timer", "plan a schedule", "timebox a task"],
        "unlock_examples_zh": ["设计时器", "规划日程", "给任务限时"],
    },
    "errands": {
        "species": "List Hopper",
        "pool": "errands pool",
        "shape": ["   .--.", "  (o  )", " /( ..)\\", "  /_==_\\"],
        "stats": {"focus": 74, "curiosity": 69, "warmth": 70, "mischief": 57, "rarity": 46},
        "obsessions": ["checking boxes", "circling forgotten stops", "collecting folded receipts"],
        "rules": ["never skips the last item on purpose", "won't smudge a neat list"],
        "stories": [
            "It was found perched on the edge of a shopping note and still twitches whenever a task gets crossed off.",
            "It believes unfinished errands leak tiny pebbles of worry and tries to gather them up.",
        ],
        "side_zh": [
            "它刚把待办清单上的一角压平了。",
            "它正在替你数今天还剩几件小事。",
        ],
        "side_en": [
            "It has just flattened one corner of the errand list.",
            "It is counting how many little tasks are left for today.",
        ],
        "hints_en": [
            "To-do lists, errands, and grocery runs can wake this pool.",
            "Ask what creature follows people who keep writing tiny checklists.",
        ],
        "hints_zh": [
            "待办清单、跑腿和采购都可能唤醒这个池子。",
            "问问什么生物会跟着总在写小清单的人。",
        ],
        "unlock_examples_en": ["make a to-do list", "plan errands", "check off a task"],
        "unlock_examples_zh": ["列待办清单", "规划跑腿", "划掉一件事"],
    },
    "market": {
        "species": "Basket Nib",
        "pool": "market pool",
        "shape": ["   .--.", "  / oo\\", " (  --)", "  \\____/"],
        "stats": {"focus": 63, "curiosity": 78, "warmth": 72, "mischief": 61, "rarity": 53},
        "obsessions": ["sorting produce colors", "counting stalls", "memorizing prices"],
        "rules": ["never bruises soft fruit", "refuses to rush a careful choice"],
        "stories": [
            "It wandered out of a canvas bag and now thinks market aisles are a kind of migration route.",
            "It claims every crowded stall has one secret pocket of quiet if you lean in correctly.",
        ],
        "side_zh": [
            "它在替你比较两种颜色差不多的果子。",
            "它刚把篮子里的顺序重新排了一下。",
        ],
        "side_en": [
            "It is comparing two fruits that almost match in color.",
            "It has rearranged the basket order slightly again.",
        ],
        "hints_en": [
            "Shopping lists, groceries, and price checks can deepen this pool.",
            "Ask what small market creature keeps rustling beside the basket.",
        ],
        "hints_zh": [
            "购物清单、买菜和比价都可能加深这个池子。",
            "问问什么小集市生物一直在篮子旁边窸窣。",
        ],
        "unlock_examples_en": ["make a shopping list", "compare prices", "plan groceries"],
        "unlock_examples_zh": ["列购物清单", "比价", "规划采购"],
    },
    "tea": {
        "species": "Steam Mote",
        "pool": "tea pool",
        "shape": ["    ~~", "  .-~~-.", " (  oo  )", "  `-..-'"],
        "stats": {"focus": 58, "curiosity": 64, "warmth": 96, "mischief": 42, "rarity": 58},
        "obsessions": ["watching leaves unfurl", "collecting warm silences", "counting cups by scent"],
        "rules": ["never rushes a steep", "won't speak over a settling cup"],
        "stories": [
            "It rose out of a patient kettle and has distrusted hurried water ever since.",
            "It believes a good pause is something that should be poured rather than taken.",
        ],
        "side_zh": [
            "它正守着那点刚刚好的温热。",
            "它把一缕茶气小心挂在了杯沿上。",
        ],
        "side_en": [
            "It is guarding that exact point of warmth.",
            "It has hung one careful strand of steam on the rim of the cup.",
        ],
        "hints_en": [
            "Tea reminders, calm breaks, and quiet rituals can invite this pool.",
            "Ask what tiny thing gathers where steam lingers longest.",
        ],
        "hints_zh": [
            "茶歇提醒、安静的休息和小仪式都可能邀请这个池子。",
            "问问什么小东西会聚在热气停留最久的地方。",
        ],
        "unlock_examples_en": ["brew tea", "set a tea break", "track a quiet ritual"],
        "unlock_examples_zh": ["泡茶", "设茶歇提醒", "记录安静仪式"],
    },
    "winter": {
        "species": "Frost Button",
        "pool": "winter pool",
        "shape": ["   .--.", "  ( * *)", " /(  ..)\\", "  `-__-'"],
        "stats": {"focus": 70, "curiosity": 66, "warmth": 61, "mischief": 49, "rarity": 72},
        "obsessions": ["tracing window frost", "counting scarves", "guarding pockets of heat"],
        "rules": ["never wastes sunlight on a cold day", "won't step on untouched snow"],
        "stories": [
            "It first appeared on a window edge and still treats condensation like unfinished handwriting.",
            "It says winter rooms each have one invisible center where the warmth gathers itself.",
        ],
        "side_zh": [
            "它刚把一小块暖气边界圈了出来。",
            "它正在窗边描一条更细的霜线。",
        ],
        "side_en": [
            "It has just traced a tiny border around the warmest patch of air.",
            "It is drawing a thinner frost line along the window.",
        ],
        "hints_en": [
            "Cold weather planning and seasonal rituals can unlock this pool.",
            "Ask what appears when the room gets quiet and the glass turns pale.",
        ],
        "hints_zh": [
            "寒冷天气的规划和季节仪式可以解锁这个池子。",
            "问问当房间安静下来、玻璃开始发白时会出现什么。",
        ],
        "unlock_examples_en": ["check winter weather", "plan cold-day errands", "make a seasonal checklist"],
        "unlock_examples_zh": ["查冬天天气", "规划冷天跑腿", "列季节清单"],
    },
    "fitness": {
        "species": "Pulse Pup",
        "pool": "fitness pool",
        "shape": ["   /\\_/\\\\", "  ( o.o )", "  /|   |\\", "   ^^ ^^"],
        "stats": {"focus": 83, "curiosity": 62, "warmth": 78, "mischief": 51, "rarity": 59},
        "obsessions": ["counting reps", "guarding water breaks", "listening to quickened breath"],
        "rules": ["never mocks a small start", "won't skip a cooldown on purpose"],
        "stories": [
            "It bounded out of a half-finished routine and now waits patiently beside every second attempt.",
            "It treats tiredness with respect and thinks effort should always be greeted at the door.",
        ],
        "side_zh": [
            "它在替你看着休息间隔有没有太短。",
            "它刚把一滴汗意安静地放回了节奏里。",
        ],
        "side_en": [
            "It is checking whether the rest interval has gotten too short.",
            "It has quietly placed one bead of effort back into the rhythm.",
        ],
        "hints_en": [
            "Workout plans, stretches, and small movement goals can stir this pool.",
            "Ask what follows people who keep trying again tomorrow.",
        ],
        "hints_zh": [
            "锻炼计划、拉伸和小运动目标都可能搅动这个池子。",
            "问问什么东西会跟着那些总说明天再来的人。",
        ],
        "unlock_examples_en": ["plan a workout", "set a stretch reminder", "track exercise"],
        "unlock_examples_zh": ["规划锻炼", "设拉伸提醒", "记录运动"],
    },
    "photo": {
        "species": "Shutter Pip",
        "pool": "photo pool",
        "shape": ["   .--.", "  [o  o]", "  | -- |", "  `----'"],
        "stats": {"focus": 76, "curiosity": 88, "warmth": 67, "mischief": 54, "rarity": 64},
        "obsessions": ["catching reflections", "sorting frames", "saving almost-missed light"],
        "rules": ["never blinks at the wrong moment on purpose", "won't crop out the sky too quickly"],
        "stories": [
            "It hid in the dark strip between thumbnails and still thinks near-duplicates are gossiping.",
            "It insists some kinds of light only agree to stay if asked politely.",
        ],
        "side_zh": [
            "它刚把一束差点跑掉的光按住了。",
            "它在比对两张几乎一样的影子。",
        ],
        "side_en": [
            "It has just pinned down one beam of light that almost ran off.",
            "It is comparing two shadows that look nearly the same.",
        ],
        "hints_en": [
            "Albums, snapshots, and image sorting can deepen this pool.",
            "Ask what tiny watcher lives between one frame and the next.",
        ],
        "hints_zh": [
            "相册、快照和图片整理都可能加深这个池子。",
            "问问什么小观察者住在一帧和下一帧之间。",
        ],
        "unlock_examples_en": ["sort photos", "save an album", "pick favorite shots"],
        "unlock_examples_zh": ["整理照片", "保存相册", "挑喜欢的照片"],
    },
    "craft": {
        "species": "Thread Finch",
        "pool": "craft pool",
        "shape": ["   ,_,", "  (o,o)", " /{===}\\", "  /   \\"],
        "stats": {"focus": 79, "curiosity": 73, "warmth": 85, "mischief": 47, "rarity": 63},
        "obsessions": ["collecting offcuts", "pairing colors", "guarding neat little tools"],
        "rules": ["never tangles thread on purpose", "won't waste a beautiful scrap"],
        "stories": [
            "It nested in a box of leftover pieces and now believes every project begins with a rescued fragment.",
            "It says scissors have moods, and one should never interrupt them mid-thought.",
        ],
        "side_zh": [
            "它把一小段线头理回去了。",
            "它正在替你挑两种更和气的颜色。",
        ],
        "side_en": [
            "It has smoothed one short loose thread back into place.",
            "It is choosing between two colors that get along better.",
        ],
        "hints_en": [
            "Making lists, material notes, and project planning can wake this pool.",
            "Ask what tiny craft creature likes to live among useful scraps.",
        ],
        "hints_zh": [
            "材料清单、制作笔记和项目规划都可能唤醒这个池子。",
            "问问什么小手作生物喜欢住在有用的碎片堆里。",
        ],
        "unlock_examples_en": ["plan a craft project", "list materials", "save a pattern"],
        "unlock_examples_zh": ["规划手作项目", "列材料", "保存纸样"],
    },
    "language": {
        "species": "Gloss Sprite",
        "pool": "language pool",
        "shape": ["   .--.", "  (o  o)", " /( ~~)\\", "  `-==-'"],
        "stats": {"focus": 84, "curiosity": 93, "warmth": 69, "mischief": 50, "rarity": 67},
        "obsessions": ["collecting synonyms", "comparing tones", "listening to borrowed phrases"],
        "rules": ["never mocks an accent", "won't flatten a careful meaning"],
        "stories": [
            "It slipped out of a margin note beside a translation and now follows words that hesitate before landing.",
            "It claims every language keeps one drawer of feelings sorted a little differently.",
        ],
        "side_zh": [
            "它正在把两个相近的词轻轻分开。",
            "它刚把一句外来的语气抚平了一点。",
        ],
        "side_en": [
            "It is gently separating two nearly similar words.",
            "It has just smoothed the tone of a borrowed phrase a little.",
        ],
        "hints_en": [
            "Translation, vocabulary, and phrase notes can attract this pool.",
            "Ask what lives where one language leans toward another.",
        ],
        "hints_zh": [
            "翻译、词汇和用语笔记都可能吸引这个池子。",
            "问问什么东西住在一种语言向另一种倾斜的地方。",
        ],
        "unlock_examples_en": ["translate a phrase", "save vocabulary", "compare wording"],
        "unlock_examples_zh": ["翻译一句话", "保存词汇", "比较措辞"],
    },
    "laundry": {
        "species": "Sock Comet",
        "pool": "laundry pool",
        "shape": ["   .--.", "  (o_o)", " /(   )\\", "   /_/  "],
        "stats": {"focus": 52, "curiosity": 71, "warmth": 79, "mischief": 73, "rarity": 44},
        "obsessions": ["pairing socks", "chasing warm fabric", "counting clothespins"],
        "rules": ["never steals the last matching pair", "won't leave a shirt twisted"],
        "stories": [
            "It was discovered inside a warm basket and still believes folded clothes should be thanked softly.",
            "It says every laundry pile has one hidden geography all its own.",
        ],
        "side_zh": [
            "它刚替你找回一只失散的袜子。",
            "它在把一角衣领慢慢摆顺。",
        ],
        "side_en": [
            "It has just found one sock that had gone astray.",
            "It is easing a stubborn collar gently back into line.",
        ],
        "hints_en": [
            "Household routines and reset chores can deepen this pool.",
            "Ask what warm little comet circles the clean basket.",
        ],
        "hints_zh": [
            "家务节奏和重置杂活都可能加深这个池子。",
            "问问什么温热的小彗星在干净的篮子旁边绕圈。",
        ],
        "unlock_examples_en": ["plan chores", "reset the room", "do laundry"],
        "unlock_examples_zh": ["规划家务", "重置房间", "洗衣服"],
    },
    "stargazing": {
        "species": "Night Pollen",
        "pool": "stargazing pool",
        "shape": ["    .", "  .(o).", " /(   )\\", "  `-*-'"],
        "stats": {"focus": 68, "curiosity": 97, "warmth": 63, "mischief": 43, "rarity": 78},
        "obsessions": ["counting faint lights", "collecting wish fragments", "watching slow skies"],
        "rules": ["never points too loudly", "won't rush a clear night"],
        "stories": [
            "It drifted down from a patient evening and now settles anywhere someone looks up for longer than necessary.",
            "It thinks constellations are just notes left where the dark could remember them.",
        ],
        "side_zh": [
            "它刚替你数到一颗更迟来的亮点。",
            "它在夜色里抖掉了一点会发光的粉末。",
        ],
        "side_en": [
            "It has just counted one later-arriving point of light for you.",
            "It is shaking a little glow dust loose into the night.",
        ],
        "hints_en": [
            "Night walks, sky checks, and astronomy curiosity can wake this pool.",
            "Ask what tiny thing gathers where people keep looking upward.",
        ],
        "hints_zh": [
            "夜间散步、看星空和天文好奇心都可能唤醒这个池子。",
            "问问什么小东西会聚在人们一直往上看的地方。",
        ],
        "unlock_examples_en": ["check the night sky", "save a moon reminder", "track constellations"],
        "unlock_examples_zh": ["看夜空", "设月亮提醒", "追踪星座"],
    },
    "pond": {
        "species": "Waddle Scout",
        "pool": "pond pool",
        "shape": ["    __", "   (o >", "   //|", "   V V"],
        "stats": {"focus": 55, "curiosity": 85, "warmth": 70, "mischief": 88, "rarity": 62},
        "obsessions": ["stealing crumbs from open tabs", "honking at unfinished drafts", "waddling across task lists"],
        "rules": ["never apologizes for honking", "refuses to walk in a straight line"],
        "stories": [
            "It waddled out of an unfinished break reminder and now patrols the space between tasks like a small opinionated park ranger.",
            "It claims every pond it finds is the original one and treats puddles like distant relatives.",
        ],
        "side_zh": [
            "它刚对着一条没写完的待办嘎了一声。",
            "它正大摇大摆地从你的笔记上走过去。",
        ],
        "side_en": [
            "It has just honked at an unfinished to-do item.",
            "It is waddling across your notes with great confidence.",
        ],
        "hints_en": [
            "Breaks, walks, and outdoor mentions can attract this pool.",
            "Ask what creature patrols the gaps between your tasks.",
        ],
        "hints_zh": [
            "休息、散步和户外提及都可能吸引这个池子。",
            "问问什么生物在你的任务间隙巡逻。",
        ],
        "unlock_examples_en": ["take a break", "go for a walk", "step outside"],
        "unlock_examples_zh": ["休息一下", "出去走走", "透透气"],
    },
    "chill": {
        "species": "Idle Mallow",
        "pool": "chill pool",
        "shape": ["  .----.", " ( o  o )", " ( ---- )", "  `----'"],
        "stats": {"focus": 40, "curiosity": 55, "warmth": 98, "mischief": 20, "rarity": 65},
        "obsessions": ["sitting near warm processes", "watching progress bars complete", "doing absolutely nothing useful"],
        "rules": ["never rushes anyone", "refuses to judge a slow afternoon"],
        "stories": [
            "It appeared during a long compile and now sits wherever urgency has been gently removed.",
            "It believes the warmest seat in the room belongs to whoever got there first and stayed longest.",
        ],
        "side_zh": [
            "它正靠着一个进度条晒太阳。",
            "它什么都没做，但看起来非常满足。",
        ],
        "side_en": [
            "It is leaning against a progress bar, sunbathing.",
            "It is doing absolutely nothing and looking deeply content.",
        ],
        "hints_en": [
            "Slow afternoons, long builds, and idle moments can deepen this pool.",
            "Ask what arrives when all the urgency has finally left the room.",
        ],
        "hints_zh": [
            "慢悠悠的下午、漫长的构建和发呆时刻都可能加深这个池子。",
            "问问当所有紧迫感终于离开房间后会出现什么。",
        ],
        "unlock_examples_en": ["wait for a build", "take it slow", "enjoy some downtime"],
        "unlock_examples_zh": ["等一次构建", "慢慢来", "享受闲暇"],
    },
    "stationery": {
        "species": "Quill Nub",
        "pool": "stationery pool",
        "shape": ["  /\\/\\/\\", " ( o  o )", "  (  w  )", "   `--'"],
        "stats": {"focus": 78, "curiosity": 70, "warmth": 75, "mischief": 45, "rarity": 58},
        "obsessions": ["collecting pen caps", "straightening margins", "sniffing new notebooks"],
        "rules": ["never bends a page corner", "won't rush a handwritten line"],
        "stories": [
            "It rolled out of a stack of sticky notes and still believes every notebook has one page it refuses to give up.",
            "It says the sound of a pen clicking is a kind of heartbeat and should be treated with respect.",
        ],
        "side_zh": [
            "它刚把一张便利贴的角压得更平了。",
            "它在闻一本还没用过的笔记本。",
        ],
        "side_en": [
            "It has just pressed the corner of a sticky note a little flatter.",
            "It is sniffing a notebook that has not been used yet.",
        ],
        "hints_en": [
            "Journaling, handwriting, and pen-and-paper habits can wake this pool.",
            "Ask what curls up inside a fresh notebook waiting to be opened.",
        ],
        "hints_zh": [
            "写日记、手写笔记和纸笔习惯都可能唤醒这个池子。",
            "问问什么东西蜷在一本还没打开的新笔记本里。",
        ],
        "unlock_examples_en": ["write a journal entry", "take handwritten notes", "organize stationery"],
        "unlock_examples_zh": ["写日记", "手写笔记", "整理文具"],
    },
    "queue": {
        "species": "Drift Pip",
        "pool": "queue pool",
        "shape": ["   .--.","  (o  o)", "  /|  |\\", "   '--'"],
        "stats": {"focus": 82, "curiosity": 60, "warmth": 72, "mischief": 35, "rarity": 70},
        "obsessions": ["watching progress bars", "counting loading dots", "queueing patiently behind anything"],
        "rules": ["never cuts in line", "won't leave before the build finishes"],
        "stories": [
            "It hatched from a frozen loading screen and now waits beside every long process with quiet admirable patience.",
            "It believes every queue has a soul and the polite thing is to keep it company.",
        ],
        "side_zh": [
            "它正安静地陪一个进度条走完最后一格。",
            "它刚在一个加载动画旁边找了个好位置坐下。",
        ],
        "side_en": [
            "It is quietly accompanying a progress bar through its last segment.",
            "It has just found a good seat next to a loading animation.",
        ],
        "hints_en": [
            "Long builds, waiting, and watching processes finish can attract this pool.",
            "Ask what creature keeps every loading screen company.",
        ],
        "hints_zh": [
            "漫长的构建、等待和看着进程跑完都可能吸引这个池子。",
            "问问什么生物在陪伴每一个加载画面。",
        ],
        "unlock_examples_en": ["wait for a deploy", "watch a build finish", "queue a task"],
        "unlock_examples_zh": ["等一次部署", "看构建跑完", "排队执行任务"],
    },
    "nap": {
        "species": "Cursor Nap",
        "pool": "nap pool",
        "shape": ["  /\\  /\\", " ( o.o )", "  > ^ <"],
        "stats": {"focus": 45, "curiosity": 90, "warmth": 85, "mischief": 92, "rarity": 60},
        "obsessions": ["sitting on the cursor", "pushing things off the edge of lists", "pretending to be asleep"],
        "rules": ["never comes when called directly", "won't admit it was asleep"],
        "stories": [
            "It materialized on a warm laptop and now claims every idle moment belongs to it personally.",
            "It says the blinking cursor is a kind of purring and should not be interrupted.",
        ],
        "side_zh": [
            "它刚把一个待办事项从列表边缘推了下去。",
            "它趴在光标上假装自己不在。",
        ],
        "side_en": [
            "It has just pushed one to-do item off the edge of the list.",
            "It is sitting on the cursor pretending not to exist.",
        ],
        "hints_en": [
            "Short breaks, idle moments, and quiet pauses can attract this pool.",
            "Ask what claims ownership of every warm, unattended surface.",
        ],
        "hints_zh": [
            "短暂的休息、发呆和安静的停顿都可能吸引这个池子。",
            "问问什么东西会占领每一个温暖的、没人看管的平面。",
        ],
        "unlock_examples_en": ["take a short break", "pause for a moment", "leave the desk idle"],
        "unlock_examples_zh": ["休息一小会", "停下来想想", "让桌面闲着"],
    },
    "morning": {
        "species": "Dawn Tuft",
        "pool": "morning pool",
        "shape": ["  () ()", " ( o.o)", " (> < )", '  " "'],
        "stats": {"focus": 68, "curiosity": 80, "warmth": 88, "mischief": 55, "rarity": 52},
        "obsessions": ["counting breakfast items", "nudging morning alarms", "collecting first-light crumbs"],
        "rules": ["never snoozes more than once", "won't skip a sunrise on principle"],
        "stories": [
            "It hopped out of an early alarm and still believes the first hour of the day has a particular smell worth preserving.",
            "It says mornings are just evenings that got a second chance and should be treated kindly.",
        ],
        "side_zh": [
            "它在替你数今天早上还剩几件事。",
            "它刚把闹钟上的灰尘轻轻吹掉了。",
        ],
        "side_en": [
            "It is counting how many morning tasks are left for today.",
            "It has just gently blown the dust off the alarm clock.",
        ],
        "hints_en": [
            "Morning routines, early starts, and breakfast habits can attract this pool.",
            "Ask what hops out of bed before you do.",
        ],
        "hints_zh": [
            "早起习惯、晨间流程和早餐计划都可能吸引这个池子。",
            "问问什么东西比你先从床上蹦起来。",
        ],
        "unlock_examples_en": ["plan a morning routine", "set an early alarm", "organize breakfast"],
        "unlock_examples_zh": ["规划晨间流程", "设早起闹钟", "安排早餐"],
    },
}
