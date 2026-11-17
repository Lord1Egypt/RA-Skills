#!/usr/bin/env python3
"""
🌙 睡前故事精靈 — 核心故事生成引擎
用預設模板 + 參數填充，生成適合 2-6 歲幼兒的床邊故事
不需要任何 API key！
"""

import argparse
import random
import sys
import os
import json
import re
from typing import Optional

# ─────────────────────────────────────────────
# 🌟 角色與元素資料庫
# ─────────────────────────────────────────────

PROTAGONISTS = [
    "小兔子", "小熊", "小狐狸", "小貓咪", "小狗狗", "小烏龜",
    "小龍貓", "小刺蝟", "小瓢蟲", "小螢火蟲", "小河馬",
    "小公主", "小王子", "小精靈", "小魔法師"
]

PROTAGONIST_EMOJI = {
    "小兔子": "🐰", "小熊": "🧸", "小狐狸": "🦊", "小貓咪": "🐱",
    "小狗狗": "🐶", "小烏龜": "🐢", "小龍貓": "🐭", "小刺蝟": "🦔",
    "小瓢蟲": "🐞", "小螢火蟲": "✨", "小河馬": "🦛",
    "小公主": "👸", "小王子": "🤴", "小精靈": "🧚", "小魔法師": "🧙"
}

PET_OPTIONS = [
    ("小狗狗", "🐶"), ("小貓咪", "🐱"), ("小鳥", "🐦"),
    ("小金魚", "🐟"), ("小烏龜", "🐢"), ("小兔子", "🐰"),
    ("小蝴蝶", "🦋"), ("小瓢蟲", "🐞"), ("小螢火蟲", "✨"),
]

EMOTION_THEMES = [
    "害怕黑暗", "分享", "勇氣", "不生氣", "不哭哭",
    "說對不起", "友誼", "耐心", "好奇心", "愛家人"
]

THEMES_DISPLAY = {
    "friendship": "🌈 友誼冒險",
    "emotion": "💤 認識情緒",
    "idiom": "🏠 成語改編",
    "fairytale": "📖 格林童話改編",
    "original": "✨ 原創互動",
}

# ─────────────────────────────────────────────
# 🎨 故事模板 — 2-3歲版本（短句 + 疊字 + 重複）
# ─────────────────────────────────────────────

STORY_TEMPLATES_TODDLER = {

    # ══ 主題 A：友誼冒險 ══

    "bunny_finds_friend": {
        "title": "🐰 小兔子找朋友",
        "theme": "friendship",
        "setup": "森林裡住著一隻小兔子，小兔子今天好想找一個好朋友一起玩。",
        "problem": "小兔子走呀走，看見小蝴蝶，問：「你可以和我玩嗎？」小蝴蝶說：「我今天要去找花蜜，明天吧！」",
        "attempt": "小兔子又走呀走，看見小鳥，問：「你可以和我玩嗎？」小鳥說：「我今天要學唱歌，明天吧！」",
        "solution": "小兔子有一點點傷心，這時候，小烏龜慢慢爬過來說：「小兔子，我陪你玩好嗎？」小兔子好開心！",
        "ending": "兩個好朋友一起玩捉迷藏，玩得好開心呀！星星出來了，月亮也出來了，晚安，小朋友，明天再一起玩喔！🌙",
        "emoji": "🐰🦋🐢",
        "lesson": "慢慢找，一定會找到好朋友 🌟"
    },

    "bear_finds_star": {
        "title": "🧸 小熊找星星",
        "theme": "friendship",
        "setup": "有一天晚上，小熊抬頭看天空，發現最亮的那顆星星不見了。",
        "problem": "小熊問月亮：「月亮月亮，星星去哪裡了？」月亮說：「我不知道耶，你去問問風吧。」",
        "attempt": "小熊去問小鳥，小鳥說：「我不知道，你去問問大樹吧。」大樹說：「也許星星去旅行了。」",
        "solution": "小熊好傷心，回到家一看——哇！窗台上放著一顆亮晶晶的小星星燈！原來是媽媽準備的禮物！",
        "ending": "小熊抱著小星星燈，鑽進暖暖的被窩，好幸福呀。晚安，小星星，晚安，小熊，晚安，小朋友！🌙✨",
        "emoji": "🧸⭐🌙",
        "lesson": "媽媽的愛，像星星一樣閃閃發亮 🌟"
    },

    "fox_and_soup": {
        "title": "🦊 小狐狸分湯",
        "theme": "friendship",
        "setup": "小狐狸森林裡煮了一鍋好香的胡蘿蔔湯，香噴噴的味道傳得好遠好遠。",
        "problem": "小兔子聞到香味走過來，問：「可以分我一點嗎？」小狐狸說：「好呀好呀！」可是湯只有一點點了。",
        "attempt": "小狐狸把剩下的湯分成兩碗，和小兔子一起喝，「我們一起喝，變得更好喝了！」",
        "solution": "兩個人喝得肚子暖暖的，小鳥也飛過來，小狐狸說：「明天我們一起煮更大一鍋湯！」",
        "ending": "大家約好明天再見，晚安，小狐狸，晚安，小兔子，晚安，小朋友！🌙",
        "emoji": "🦊🥕🐰",
        "lesson": "分享食物，變得更好吃；分享快樂，變得更快樂 🌟"
    },

    "kitty_waiting": {
        "title": "🐱 小貓咪等媽媽",
        "theme": "emotion",
        "setup": "天黑了，小貓咪在家等媽媽回來。窗外的風呼呼吹，樹葉沙沙響，小貓咪有一點點害怕。",
        "problem": "「嗚嗚……媽媽什麼時候才回來呀？」小貓咪的眼淚快要掉下來了。",
        "attempt": "這時候，門鈴叮咚叮咚響了！是小狗來了，說：「不要怕，我陪你等！」",
        "solution": "小貓咪和小狗一起數數：「一、二、三……媽媽！」媽媽推開門，給了小貓咪一個大大的抱抱！",
        "ending": "媽媽回來了！小貓咪好開心，一下子就不害怕了。晚安，小貓咪，晚安，小朋友！🌙",
        "emoji": "🐱🐶💤",
        "lesson": "害怕的時候，有好朋友陪，就不怕了 🌟"
    },

    "turtle_race": {
        "title": "🐢 小烏龜跑跑",
        "theme": "original",
        "setup": "森林裡要舉辦跑步比賽，小烏龜也報名了，大家都笑他：「烏龜烏龜，慢慢爬！」",
        "problem": "小烏龜聽了有一點傷心，可是他跟自己說：「慢慢跑，也是跑呀！」",
        "attempt": "比賽開始了！小兔子一下子就跑得好遠好遠，小烏龜一步一步慢慢爬。",
        "solution": "小兔子跑到一半，想睡覺了，停下來休息。小烏龜一直爬一直爬，最後……小烏龜第一名！",
        "ending": "大家為小烏龜拍手：「你好棒！」小烏龜笑了。晚安，慢吞吞的小烏龜，晚安，小朋友！🌙",
        "emoji": "🐢🏃🐰",
        "lesson": "慢慢來，也會到終點喔 🌟"
    },

    "glowing_bug": {
        "title": "✨ 小螢火蟲亮晶晶",
        "theme": "original",
        "setup": "夏天的晚上，草叢裡住著一隻小螢火蟲，他的屁股可以發出亮亮的光喔！",
        "problem": "可是今天，小螢火蟲的光忽然不見了，他好著急：「沒有光，大家會迷路怎麼辦？」",
        "attempt": "小螢火蟲去找媽媽，媽媽說：「你休息一下，開心的時候自然就會亮了！」",
        "solution": "小螢火蟲睡了一覺醒來，窗外傳來好多小朋友的聲音：「我們來找小螢火蟲！」小螢火蟲好開心，光又亮起來了！",
        "ending": "小螢火蟲提著小燈籠，帶小朋友們找到回家的路。晚安，小螢火蟲，晚安，小朋友！🌙✨",
        "emoji": "✨🦋🐛",
        "lesson": "開心的時候，就會閃閃發光 🌟"
    },

    "rainbow_friends": {
        "title": "🌈 彩虹橋上的朋友",
        "theme": "friendship",
        "setup": "雨停了，天空出現一道好漂亮的彩虹橋，彎彎的，像一個大大的笑臉。",
        "problem": "小兔子站在橋的這一頭，小熊站在橋的那一頭，誰也不敢先走。「橋會不會壞掉呀？」",
        "attempt": "小兔子勇敢地走了一步，橋穩穩的！小熊也走了一步，橋也好好的！",
        "solution": "兩個人在彩虹橋中間見面了！他們一起數：「紅、橙、黃、綠、藍、靛、紫！」然後一起跑回家。",
        "ending": "明天，他們還要一起走彩虹橋。晚安，小兔子，晚安，小熊，晚安，小朋友！🌙🌈",
        "emoji": "🐰🧸🌈",
        "lesson": "勇敢一步，就會遇見好朋友 🌟"
    },

    "sleepy_cloud": {
        "title": "☁️ 雲朵想睡覺",
        "theme": "original",
        "setup": "天空的白雲朵，今天特別特別睏。白雲朵飄呀飄，一直打哈欠：「呵——好想睡覺呀。」",
        "problem": "可是太陽公公還沒下山，天還亮亮的。白雲朵問：「太陽公公，可以早一點睡覺嗎？」",
        "attempt": "太陽公公笑著說：「好呀好呀！」慢慢慢慢地把光變柔和了，天空變成橘黃色。",
        "solution": "白雲朵看著漂亮的夕陽，打了一個大大的哈欠：「呵——好舒服呀。」慢慢飄到天邊，靜靜睡著了。",
        "ending": "天上只剩下閃亮亮的小星星，一顆一顆眨眼睛。晚安，白雲朵，晚安，小星星，晚安，小朋友！🌙☁️",
        "emoji": "☁️🌅⭐",
        "lesson": "累了就要睡覺，身體才會棒棒的 🌟"
    },

    "bunny_bed": {
        "title": "🐰 小兔子的軟綿綿床",
        "theme": "emotion",
        "setup": "小兔子今天好累好累，眼睛睜不開了，可是他還在床上滾來滾去，就是不肯睡。",
        "problem": "「我還要玩！我還要玩！」小兔子翻過來翻過去，枕頭都被他踢到地上去了。",
        "attempt": "兔媽媽輕輕拍拍他：「小兔子，你的身體說它想睡覺了喔。」小兔子看看自己的眼睛，真的好睏好睏。",
        "solution": "小兔子不再滾了，輕輕輕輕地閉上眼睛。兔媽媽唱了一首輕輕的歌，小兔子的呼吸慢慢變均勻了。",
        "ending": "小兔子做了一個好夢，夢見自己在一大片胡蘿蔔田裡跑來跑去。晚安，小兔子，晚安，小朋友！🌙🐰",
        "emoji": "🐰🛏️💤",
        "lesson": "身體累了就要睡，休息完又是元氣滿滿 🌟"
    },

    "butterfly_wing": {
        "title": "🦋 小蝴蝶的彩虹翅膀",
        "theme": "original",
        "setup": "森林裡有一隻小蝴蝶，他的翅膀五顏六色，好漂亮好漂亮，大家都稱讚他。",
        "problem": "可是有一天，一邊翅膀不小心被樹枝弄破了一點點。小蝴蝶好傷心：「我不再漂亮了！」",
        "attempt": "小蝴蝶躲起來不敢見人。小瓢蟲找到他，說：「你的翅膀還是很好看呀！」",
        "solution": "小蝴蝶慢慢飛出來，大家看到他就說：「小蝴蝶，你好漂亮！」小蝴蝶笑了，原來友誼讓他更美麗。",
        "ending": "晚風吹來，小蝴蝶輕輕飛回家。晚安，小蝴蝶，晚安，森林，晚安，小朋友！🌙🦋",
        "emoji": "🦋🐞🌸",
        "lesson": "不完美也很美，真正的朋友會愛你 🌟"
    },

    "moon_song": {
        "title": "🌙 月亮唱的歌",
        "theme": "original",
        "setup": "每天晚上，月亮都會在天上輕輕唱歌。可是今天，月亮的喉嚨不舒服，唱不出聲音來。",
        "problem": "「怎麼辦怎麼辦？」月亮急得眼淚都快掉下來了，「小朋友們還等著聽我唱歌呢！」",
        "attempt": "小星星們說：「我們來幫你唱！」於是，小星星們一起唱：「一閃一閃亮晶晶……」",
        "solution": "可是大家發現，小星星的歌聲還需要月亮一起唱才最好聽。月亮喝了一杯溫水，嗓子舒服了，和星星一起唱了起來。",
        "ending": "歌聲傳到小朋友的房間，小朋友笑著笑著，輕輕進入了夢鄉。晚安，月亮，晚安，小星星，晚安，小朋友！🌙✨",
        "emoji": "🌙⭐🎵",
        "lesson": "每個人都有自己的節奏，大家合在一起更美好 🌟"
    },

    "hedgehog_sharing": {
        "title": "🦔 小刺蝟分蘋果",
        "theme": "friendship",
        "setup": "小刺蝟的果園裡，蘋果樹結了好多好多的紅蘋果，紅彤彤的，好香好香。",
        "problem": "小刺蝟自己吃不完，想拿去分給朋友。可是他的背上都是刺，蘋果怎麼放上去都會滾下來。",
        "attempt": "小刺蝟想了很久，最後用葉子把蘋果包起來，一顆一顆放到背上，終於成功啦！",
        "solution": "小刺蝟揹著蘋果，走了好遠好遠，分給了小兔子、小熊、和小狐狸，大家一起說：「謝謝小刺蝟！」",
        "ending": "雖然很累，可是小刺蝟的心裡好開心。回到家，小刺蝟輕輕躺下，很快睡著了。晚安，小刺蝟，晚安，小朋友！🌙🍎",
        "emoji": "🦔🍎🐰",
        "lesson": "分享很快樂，辛苦也值得 🌟"
    },

    "ladybug_spot": {
        "title": "🐞 小瓢蟲的點點",
        "theme": "emotion",
        "setup": "小瓢蟲的殼上有七個黑色的小點點，他每天都數一遍，一二三四五六七，剛好七個。",
        "problem": "可是今天早上，小瓢蟲發現自己只剩六個點點了！「怎麼辦怎麼辦？我的點點不見了！」",
        "attempt": "小瓢蟽到處找，找了好久好久。蝴蝶姐姐說：「有時候點點會掉，不影響你飛翔喔！」",
        "solution": "小瓢蟲試著飛一飛——哇！飛得好高好高，一點也沒變！他笑了：「沒關係，我還是最會飛的小瓢蟲！」",
        "ending": "小瓢蟲飛回家，媽媽說：「你回來啦！晚安，我的小瓢蟲。」晚安，小瓢蟲，晚安，小朋友！🌙🐞",
        "emoji": "🐞🦋🌸",
        "lesson": "愛自己原本的样子，就是最棒的 🌟"
    },

    "seahorse_dance": {
        "title": "🐴 海馬小姐的舞蹈",
        "theme": "original",
        "setup": "海底舉辦舞蹈大賽，海馬小姐好想參加，可是她跳得和別人不一樣，總是甩甩頭、搖搖尾巴。",
        "problem": "「你不對不對！應該要這樣跳！」其他魚都笑她。海馬小姐好傷心，不想跳了。",
        "attempt": "小丑魚游過來說：「我覺得你的舞很特別呀！可以教我嗎？」海馬小姐開始教小丑魚跳。",
        "solution": "比賽開始了，海馬小姐跳了起來——哇，好特別！大家都看呆了，最後她得到了「最有創意獎」！",
        "ending": "海馬小姐開心地在海底轉圈圈，轉呀轉呀，游回家睡覺了。晚安，海馬小姐，晚安，小朋友！🌙🐠",
        "emoji": "🐴🪼🏆",
        "lesson": "與眾不同不是缺點，是最棒的禮物 🌟"
    },

    "magic_pillow": {
        "title": "🛏️ 神奇的枕頭",
        "theme": "original",
        "setup": "小精靈有一個神奇的枕頭，只要把枕頭放在耳朵旁邊，就會聽到最美的音樂。",
        "problem": "可是今天晚上，小精靈怎麼找都找不到那個枕頭。床底下沒有，衣櫃裡也沒有，小精靈好著急。",
        "attempt": "小精靈去找森林裡的朋友們幫忙找。小熊說：「我聞聞看。」小兔子說：「我找找看。」",
        "solution": "小鳥在天上發現了——枕頭被風吹到高高的大樹上了！大家一起把枕頭拿下來，小精靈開心極了！",
        "ending": "小精靈把頭埋在軟軟的枕頭裡，聽到了最美的音樂。晚安，小精靈，晚安，森林，晚安，小朋友！🌙🧚",
        "emoji": "🧚🛏️🎶",
        "lesson": "重要的東西不見了，朋友會幫你找回來 🌟"
    },

    "cloud_rain": {
        "title": "☁️ 雲朵哭哭",
        "theme": "emotion",
        "setup": "天上有一朵小雲朵，今天他悶悶不樂，嘴巴嘟得好高好高。",
        "problem": "「沒有人和我玩……」小雲朵的眼淚一滴一滴掉下來，雨就下起來了。",
        "attempt": "風吹過來，輕輕地問：「小雲朵，你怎麼了？」小雲朵說：「我沒有朋友，好孤單。」",
        "solution": "風說：「那我當你的朋友吧！」小雲朵笑了，太陽出來了，把雨都收走了，天空又藍了。",
        "ending": "小雲朵和風一起在天上旅行，快快樂樂的。晚安，小雲朵，晚安，小朋友！🌙☁️",
        "emoji": "☁️💧🌈",
        "lesson": "傷心的時候說出來，就會有好心人來幫你 🌟"
    },

    "star_painting": {
        "title": "⭐ 小星星畫畫",
        "theme": "original",
        "setup": "小星星最喜歡畫畫了，他每天都拿著小刷子，把天上的白雲畫成各種形狀。",
        "problem": "可是今天，小星星怎麼畫都畫不好。刷子弄丢了，顏料也打翻了，小星星好洩氣。",
        "attempt": "小星星把打翻的顏料輕輕抹開——哇！變成了一片美麗的極光！比平常更漂亮！",
        "solution": "「咦？原來『錯誤』也可以變成藝術品呀！」小星星又開心起來，繼續快快樂樂地畫。",
        "ending": "畫累了，小星星靜靜地發光，輕輕地閉上眼睛。晚安，小星星，晚安，小朋友！🌙✨",
        "emoji": "⭐🎨🌌",
        "lesson": "失敗了也沒關係，有時會變成大驚喜 🌟"
    },

    "owl_guard": {
        "title": "🦉 貓頭鷹的夜晚",
        "theme": "original",
        "setup": "森林裡有一隻小貓頭鷹，他的工作是晚上守護大家。大家都睡著了，只有他一個人醒著。",
        "problem": "小貓頭鷹有點孤單：「白天大家都在玩，只有我睡覺；晚上大家睡了，只有我醒著……」",
        "attempt": "可是，小貓頭鷹轉念一想：「醒著可以看到美麗的月亮和星星，這是多麼特別的事呀！」",
        "solution": "想到這裡，小貓頭鷹笑了。他輕輕唱著歌，飛過一棵又一棵樹，守護著大家的夢。",
        "ending": "天快亮了，該睡覺啦。晚安，小貓頭鷹，晚安，森林，晚安，小朋友！🌙🦉",
        "emoji": "🦉🌙⭐",
        "lesson": "每個人都不一樣，這就是你的特別之處 🌟"
    },

    "dear_bear": {
        "title": "🧸 親愛的小熊",
        "theme": "emotion",
        "setup": "小熊今天畫了一張卡片要送給媽媽，上面畫了太陽、小花，還有他自己和媽媽手牽手。",
        "problem": "可是畫筆一不小心，卡片上多了一條醜醜的線。小熊好傷心：「怎麼辨，卡片弄壞了……」",
        "attempt": "小熊把卡片藏到身後，不敢拿出來。熊哥哥問：「你在藏什麼呀？」小熊小聲地說了經過。",
        "solution": "熊哥哥看了看說：「我覺得這條線像一條小路呀！你和媽媽手牽手走在上面，很温馨呀！」小熊開心了。",
        "ending": "小熊把卡片送給媽媽，媽媽抱著小熊說：「這是我收到最棒的禮物！」晚安，小熊，晚安，小朋友！🌙🧸",
        "emoji": "🧸💐💤",
        "lesson": "用心做的禮物，就是最好的禮物 🌟"
    },

    "dragon_fire": {
        "title": "🐉 小火龍不生氣",
        "theme": "emotion",
        "setup": "小火山裡住著一條小火龍，他的肚子裡有一團小小的火。平常這團火暖暖的，小火龍很開心。",
        "problem": "可是今天，小火龍生氣了，肚子裡的火變得越來越大、越來越大，連火山都冒煙了！",
        "attempt": "小火龍跑到河邊，想讓火熄掉，可是火太大了。這時候，小精靈飛過來說：「你先深呼吸！」",
        "solution": "小火龍跟著小精靈一起深呼吸，吸——呼——吸——呼——肚子裡的火慢慢慢慢小下來了，小火龍也冷靜了。",
        "ending": "小火龍謝謝小精靈，然後回家睡覺了。晚安，小火龍，晚安，小朋友！🌙🐉",
        "emoji": "🐉🌋💨",
        "lesson": "生氣的時候深呼吸，火氣就會慢慢不見 🌟"
    },
}


# ─────────────────────────────────────────────
# 🎨 故事模板 — 4-6歲版本（情節稍完整）
# ─────────────────────────────────────────────

STORY_TEMPLATES_PRESCHOOL = {

    "honest_chick": {
        "title": "🐥 小雞的誠實餅乾",
        "theme": "emotion",
        "setup": "森林烘焙坊今天舉辦了一場餅乾大賽，獲勝者可以得到一頂金色的小廚師帽。小雞好想得到那頂帽子！",
        "problem": "比賽時，小雞不小心打翻了糖罐，糖撒了一地。評審說：「沒有糖就做不成餅乾，你出局了！」小雞好傷心。",
        "attempt": "小雞偷偷撿了一點點鄰居家飄過來的糖粉，心想：「只要一點點，應該看不出來吧……」",
        "solution": "可是，小雞的心裡一直不安。他走到評審面前說：「對不起，我用了不該用的糖，對不起。」評審點點頭：「誠實比帽子更珍貴！」",
        "ending": "小雞沒有得到帽子，可是他覺得心裡暖暖的，比戴上帽子更快樂。晚安，小雞，晚安，小朋友！🌙🐥",
        "emoji": "🐥👨‍🍳⭐",
        "lesson": "勇於承認錯誤，是最勇敢的表現 🌟"
    },

    "squirrel_store": {
        "title": "🐿️ 小松鼠的愛心商店",
        "theme": "friendship",
        "setup": "秋天到了，小松鼠收集了好多好多的橡果，他把家裡的房間都堆滿了，還是放不下。",
        "problem": "這時候，小兔子走過來說：「小松鼠，我家裡沒有食物了，可以跟你買一些嗎？」小松鼠說：「可是我也要吃呀……」",
        "attempt": "小松鼠想了想：「如果我把橡果分給大家，冬天我怎麼辦？」他猶豫了很久。",
        "solution": "後來，小松鼠決定開一家「愛心商店」——大家有多的食物就放進來，缺食物的人可以來拿。整個森林都來帮忙，商店裡好熱鬧！",
        "ending": "小松鼠的冬天，一點也不孤單，大家輪流請他到家裡吃飯。晚安，小松鼠，晚安，森林，晚安，小朋友！🌙🐿️",
        "emoji": "🐿️🌰🏠",
        "lesson": "分享不會讓你失去，反而會得到更多 🌟"
    },

    "caterpillar_journey": {
        "title": "🐛 小毛毛蟲的大冒險",
        "theme": "original",
        "setup": "小毛毛蟲住在蘋果樹的葉子上，他每天吃樹葉、看螞蟻排隊、數瓢蟲的點點，覺得生活好無聊。",
        "problem": "「好想看看外面的世界喔！」可是蘋果樹好高好高，小毛毛蟲爬都爬不上去。",
        "attempt": "小毛毛蟲請小鳥幫忙，小鳥說：「我馱你去吧！」於是小鳥帶著小毛毛蟲飛過高山、飛過河流，看到了好大好大的世界。",
        "solution": "小毛毛蟲看到了五顏六色的花田，看到了波光粼粼的湖面，看到了金黃色的夕陽。「哇！世界好美呀！」可是，小毛毛蟲想家了。",
        "ending": "小鳥把小毛毛蟲送回家。小毛毛蟲爬上蘋果樹，覺得這裡比以前更美了。晚安，小毛毛蟲，晚安，小朋友！🌙🌳",
        "emoji": "🐛🦋🌸",
        "lesson": "出去看看世界，會更珍惜自己的家 🌟"
    },

    "panda_party": {
        "title": "🐼 大熊貓的生日派對",
        "theme": "friendship",
        "setup": "下週是大熊貓的生日，他想要舉辦一個超級大的生日派對，邀請森林裡所有的動物都來參加。",
        "problem": "大熊貓寫了好多好多的邀請卡，可是他寫字寫得不好看，很多字都歪歪扭扭的，動物們看不懂。",
        "attempt": "小狐狸志願幫忙寫，小猴子也說他可以幫忙。於是大家一起寫，卡片終於寫完了。",
        "solution": "生日派對那天，大家都來了！大熊貓準備了竹子蛋糕，大家一起唱歌、跳舞、吹氣球，好開心呀！",
        "ending": "派對結束了，大熊貓躺在床上，想著今天的事，覺得自己好幸福。晚安，大熊貓，晚安，小朋友！🌙🎂",
        "emoji": "🐼🎈🎉",
        "lesson": "接受朋友的幫助，是送給朋友最好的禮物 🌟"
    },

    "moon_brother": {
        "title": "🌙 月亮的哥哥弟弟",
        "theme": "original",
        "setup": "月亮有兩個哥哥，一個是太陽哥哥，一個是星星弟弟。每天，太陽哥哥在白天陪大家，星星弟弟在夜裡發光，月亮在中間，做兩邊的橋樑。",
        "problem": "有一天，月亮覺得累了，想休息一下。可是如果他休息了，白天太亮，晚上太黑，大家都不開心。",
        "attempt": "月亮找太陽哥哥商量，太陽哥哥說：「我可以每天多工作一點，陪你休息。」可是這樣太陽哥哥太辛苦了。",
        "solution": "最後，大家決定：月亮休息的時候，就變成彎彎的月牙，這樣既可以休息，又不會讓夜晚太黑。從此，月亮就有滿月、弦月、峨眉月各種樣子啦。",
        "ending": "今晚的月亮，是什麼形狀呢？抬頭看看吧！晚安，月亮，晚安，小朋友！🌙⭐",
        "emoji": "🌙☀️⭐",
        "lesson": "每個人都有休息的權利，團隊合作讓大家都能喘口氣 🌟"
    },

    "unicorn_color": {
        "title": "🦄 獨角獸的彩虹雨",
        "theme": "original",
        "setup": "彩虹王國好久沒下雨了，花園裡的花都垂下了頭，小河也變得越來越小。獨角獸的角本來可以變出彩虹的，可是今天怎麼試都不行。",
        "problem": "「怎麼回事呢？」獨角獸使盡力氣，角只冒出一點點彩色的小星星。「一定是出了什麼問題！」",
        "attempt": "獨角獸去請教老巫師，老巫師說：「彩虹需要雨水當材料，沒有雨就沒有彩虹。你要先去找到雨。」",
        "solution": "獨角獸跑到高山頂上，收集了清晨的露水，加上自己的真心眼淚——叮！一道大大的彩虹升起來了，雨也跟著下來了！",
        "ending": "花園裡的花都抬起頭來笑了，小河又開始唱歌了。獨角獸在彩虹下跳了一支舞，然後回家睡覺。晚安，獨角獸，晚安，小朋友！🌙🦄",
        "emoji": "🦄🌈💧",
        "lesson": "真心和努力，可以創造奇蹟 🌟"
    },

    "dolphin_song": {
        "title": "🐬 小海豚的歌聲",
        "theme": "emotion",
        "setup": "大海裡有一個歌唱比賽，冠軍可以得到「海洋好聲音」的獎牌。小海豚最喜歡唱歌了，他每天都練習。",
        "problem": "可是比賽那天，小海豚一張口，聲音就卡住了——他看到評審鯨魚那麼大，嚇得不敢唱了。",
        "attempt": "小海豚低著頭游到最後面，這時候小丑魚游過來說：「不要怕！鯨魚評審最喜歡小朋友唱歌了！」",
        "solution": "小海豚鼓起勇氣，游到前面唱了起來。他的聲音清澈又好聽，整個海洋都安靜下來聽他唱歌。掌聲從四面八方響起！",
        "ending": "小海豚得到了獎牌，可是他最開心的不是獎牌，而是他戰勝了害怕。晚安，小海豚，晚安，小朋友！🌙🏆",
        "emoji": "🐬🎤🌟",
        "lesson": "戰勝害怕，比得到獎牌更了不起 🌟"
    },

    "little_engine": {
        "title": "🚂 小火車的勇氣山",
        "theme": "original",
        "setup": "小火車的工作是每天拉著客人穿過美麗的山谷。可是今天，他要爬一座新的大山——勇氣山，聽說山坡很陡很陡。",
        "problem": "小火車來到山腳下，往上看了一眼：「哇——好高好高喔……我一定爬不上去的……」小火車害怕了。",
        "attempt": "小火車嘗試往上爬，爬了一點點就滑下來了。他垂頭喪氣地停下來，不知道怎麼辦。",
        "solution": "這時候，貨車叔叔說：「我幫你推，你來用力往前！一、二、三——加油！」小火車用力往前冲，終於一步一步爬上了山頂！",
        "ending": "從山頂往下看，整個山谷好美好美。小火車發現：「原來只要有人幫忙，沒有什麼是做不到的！」晚安，小火車，晚安，小朋友！🌙🚂",
        "emoji": "🚂⛰️💪",
        "lesson": "勇氣不是不害怕，而是害怕了還願意往前 🌟"
    },

    "magic_wardrobe": {
        "title": "🧥 神奇的衣櫃",
        "theme": "original",
        "setup": "小精靈的家裡有一個神奇的衣櫃，只要穿上一件特別的衣服，就可以變成另一個樣子。",
        "problem": "小精靈試穿了超人的衣服，變得好神氣！可是有一天，他忘記把衣服脫下來，就這樣以超人的樣子過了一整個星期。",
        "attempt": "大家看到「超人」都嚇跑了，沒有人認識小精靈了。小精靈好傷心：「我想變回我自己！」",
        "solution": "小精靈跑回家，站在衣櫃前說：「我想要變回我自己。」衣櫃打開，小精靈變回了原來的樣子，大家又認出他了。",
        "ending": "小精靈明白了：做自己，是最快樂的事。晚安，小精靈，晚安，小朋友！🌙🧚",
        "emoji": "🧚🧥🪞",
        "lesson": "做真實的自己，就是最棒的 🌟"
    },

    "kangaroo_pouch": {
        "title": "🦘 小袋鼠的口袋",
        "theme": "friendship",
        "setup": "小袋鼠最喜歡他的小口袋了！裡面可以放糖果、放玩具、放石頭，放什麼都好方便。",
        "problem": "可是有一天，小烏龜哭著說：「我走得好累喔……」小袋鼠想讓他坐在口袋裡，可是口袋太小了，裝不下。",
        "attempt": "小袋鼠把糖果拿出來、把玩具拿出來，口袋還是太小。怎麼辦呢？",
        "solution": "小袋鼠靈機一動，讓小烏龜爬到自己的背上，口袋在外面：「這樣就可以一起走啦！」兩個好朋友一起出發了。",
        "ending": "走在路上，口袋裡的糖果送給了小烏龜當零食，兩個好朋友分享了所有的好東西。晚安，小袋鼠，晚安，小朋友！🌙🦘",
        "emoji": "🦘🐢💕",
        "lesson": "好朋友會想辦法一起前進 🌟"
    },
}


# ─────────────────────────────────────────────
# 📖 續集模板系統
# ─────────────────────────────────────────────

SEQUEL_TEMPLATES_TODDLER = [
    "第二天早上，{protagonist}醒來的時候，想起昨天的事，笑了。",
    "過了幾天，{protagonist}又出發去探險了，這一次，他遇到了……",
    "有一天，{protagonist}收到了{pet_name}的一封信，信上說……",
    "第二天，{protagonist}決定把昨天學到的事，教給更多的好朋友……",
]

SEQUEL_TEMPLATES_PRESCHOOL = [
    "一個星期過去了，{protagonist}決定再次踏上旅程，這一次，他要去尋找……",
    "一個月後，{protagonist}收到了一張神秘的地圖，地圖上畫著……",
    "季節變換了，{protagonist}發現自己和朋友們都長大了一點點，這一次他們要一起……",
    "時光飛逝，{protagonist}回想起那天的事，決定把這個故事寫下來，送給……",
]


# ─────────────────────────────────────────────
# 🏠 成語改編故事
# ─────────────────────────────────────────────

IDOM_TEMPLATES_TODDLER = [
    {
        "title": "🐢 烏龜和兔子再比賽",
        "story": (
            "森林裡又舉辦了一場跑步比賽，這一次，小兔子很認真，沒有在中間睡覺。\n"
            "可是小烏龜也變得更厲害了，他學會了滾滾前進，滾得又快又穩！\n"
            "兩個好朋友一起衝向終點，並列第一名！\n"
            "兔子和烏龜都開心地笑了，大家說：「合作比競爭更快樂！」\n"
            "晚安，小朋友，明天也要加油喔！🌙"
        ),
        "moral": "團結合作，比爭第一名更快樂 🌟"
    },
    {
        "title": "🐰 守株待兔新版本",
        "story": (
            "小兔子在森林裡玩耍，忽然一隻小鳥飛過來，說：「兔哥哥，我帶你去一個很棒的地方！」\n"
            "小兔子跟著小鳥去了一個大花園，花園裡有好多好多他從來沒見過的花。\n"
            "小鳥說：「只要願意走出去，就會發現新風景喔！」\n"
            "小兔子點點頭，把這句話記在心裡。\n"
            "晚安，小兔子，晚安，小朋友！🌙"
        ),
        "moral": "勇敢走出去，會發現更棒的風景 🌟"
    },
    {
        "title": "🦊 狐假虎威新故事",
        "story": (
            "森林裡的小狐狸以前很喜歡用別人的名聲嚇人，大家都怕他。\n"
            "可是有一次，颱風來了，小狐狸的家受損了，大家都知道真相：原來小狐狸也很需要幫忙。\n"
            "大家紛紛伸出援手，幫小狐狸蓋了新房子。\n"
            "小狐狸感動地說：「謝謝大家，我以前不應該嚇你們的。」\n"
            "從此，小狐狸成為了森林裡最善良的小動物。\n"
            "晚安，小朋友！🌙"
        ),
        "moral": "真誠待人，才會得到真正的友誼 🌟"
    },
]

IDOM_TEMPLATES_PRESCHOOL = [
    {
        "title": "🐢🐰 龜兔賽跑新篇章",
        "story": (
            "龜兔賽跑之後，小兔子和小烏龜成了好朋友。\n"
            "有一天，森林裡要舉辦一場划船比賽，小兔子問：「誰要和我一起參加大船？」\n"
            "小烏龜說：「我可以幫忙划水喔！」於是，兔子划船、烏龜潛水掌舵，兩人搭檔出賽。\n"
            "比賽中，大船撞到了岩石，快要沉了！小烏龜一個翻身，用殼堵住了破洞，救了大家。\n"
            "雖然他們沒有贏得第一名，但評審說：「你們的友誼，是最大的第一名！」\n"
            "晚安，小朋友！🌙"
        ),
        "moral": "團隊合作，每個人都能發揮所長 🌟"
    },
    {
        "title": "🌱 拔苗助長的新教訓",
        "story": (
            "小農夫的稻子長得慢，他好著急，把稻子一棵一棵往上拔，希望能幫助它們快快長大。\n"
            "可是第二天，稻子全都枯萎了！小農夫傷心地哭了。\n"
            "爺爺走過來說：「種東西要有耐心，每天澆水、每天等待，它自然會長大。」\n"
            "小農夫學到了教訓，重新播種，細心照顧，這一次，稻子長得又高又健康。\n"
            "秋天到了，金黃色的稻田豐收了！\n"
            "晚安，愛護植物的小朋友！🌙"
        ),
        "moral": "耐心等待，用心照顧，會有好的收成 🌟"
    },
    {
        "title": "🦊 狐假虎威之後",
        "story": (
            "狐狸假借老虎的威風嚇走小動物之後，小動物們都知道了真相。\n"
            "有一天，狐狸掉進了河裡，大聲喊救命，可是以前被他嚇過的小動物們都不敢靠近。\n"
            "只有小烏龜游過去，用背殼把狐狸頂上了岸。\n"
            "狐狸問：「我以前欺負過你，你為什麼還要救我？」小烏龜說：「我只是想讓你知道，真正的勇氣是幫助別人，不是嚇唬別人。」\n"
            "狐狸紅著臉，感謝了小烏龜，決定要改過自新。\n"
            "晚安，小朋友！🌙"
        ),
        "moral": "真正的勇氣是善良，不是欺負人 🌟"
    },
]


# ─────────────────────────────────────────────
# 📖 格林童話改編
# ─────────────────────────────────────────────

FAIRYTALE_TEMPLATES_TODDLER = [
    {
        "title": "🏠 小小紅豆餅屋",
        "story": (
            "從前從前，在一座小小的森林裡，住著兔媽媽和兔孩子。\n"
            "有一天，兔媽媽烤了好香好香的紅豆餅，整個森林都聞到了！\n"
            "小熊、小狐狸、小鳥、小松鼠都跑過來了，說：「好香好香！」\n"
            "兔媽媽說：「一起吃吧！」大家開開心心地吃著紅豆餅，唱著歌。\n"
            "晚安，小朋友，甜甜的夢最香了！🌙"
        ),
    },
    {
        "title": "🐑 小小牧羊人",
        "story": (
            "森林裡住著一個小小牧羊人，每天早上，他趕著綿羊去吃草。\n"
            "有一天，小小牧羊人發現草原上有一棵神奇的蘋果樹，蘋果又大又紅。\n"
            "他把蘋果分給了所有的綿羊，綿羊們都說：「謝謝你！」\n"
            "夕陽西下，小小牧羊人數著羊：「一、二、三……一隻也沒少！」\n"
            "晚安，愛護動物的小朋友！🌙"
        ),
    },
]

FAIRYTALE_TEMPLATES_PRESCHOOL = [
    {
        "title": "🏰 十二點的小公主",
        "story": (
            "很久很久以前，有一個小小的王國，住著一位小公主。\n"
            "小公主最喜歡做的事，就是每天晚上數天上的星星。\n"
            "有一天，她許了一個願望：「希望每天都有人陪我數星星！」\n"
            "第二天早上醒來，她發現床邊放著一個小天文望遠鏡，是父王送的！\n"
            "從那天起，每天晚上父王都陪她數星星，一、二、三……\n"
            "數著數著，小公主進入了甜甜的夢鄉。\n"
            "晚安，小公主，晚安，小朋友！🌙"
        ),
    },
    {
        "title": "🪞 魔鏡魔鏡好朋友",
        "story": (
            "從前有一個小女孩，她每天都對著魔鏡說：「魔鏡魔鏡，誰是最漂亮的人？」\n"
            "魔鏡說：「是你呀，但你知道嗎？善良的人才是真正的漂亮喔！」\n"
            "小女孩問：「善良要怎麼做呢？」\n"
            "魔鏡說：「去外面看看吧！」小女孩走出房門，看到鄰居奶奶在搬東西，她過去幫忙。\n"
            "晚上，小女孩又對著魔鏡說：「魔鏡魔鏡，誰是最漂亮的人？」\n"
            "魔鏡說：「現在的你，就是最漂亮的！」\n"
            "晚安，善良的小朋友！🌙"
        ),
    },
    {
        "title": "🌹 玻璃鞋裡的友誼",
        "story": (
            "森林裡舉辦了一個舞會，小兔子和所有人都穿著漂亮的玻璃鞋來參加。\n"
            "可是舞會進行到一半，一隻小老鼠跑過來說：「嗚嗚，我的鞋子不見了，我沒辦法跳舞了。」\n"
            "小兔子說：「我的鞋子借你穿！」可是小老鼠的腳太小，玻璃鞋一直掉。\n"
            "於是大家發明了一種新舞蹈——不用穿鞋子的光腳舞！\n"
            "所有人脫下鞋子，在草地上盡情跳舞，快樂極了！\n"
            "晚安，愛跳舞的小朋友！🌙"
        ),
    },
]


# ─────────────────────────────────────────────
# 🎯 故事生成器核心類別
# ─────────────────────────────────────────────

class StoryGenerator:
    """睡前故事生成器"""

    def __init__(self,
                 protagonist: Optional[str] = None,
                 pet: Optional[str] = None,
                 age: str = "toddler",
                 length: str = "short",
                 theme: Optional[str] = None,
                 sequel_to: Optional[str] = None,
                 seed: Optional[int] = None):
        self.age = age  # toddler=2-3歲, preschool=4-6歲
        self.length = length  # short, medium, long
        self.theme = theme
        self.sequel_to = sequel_to
        self.seed = seed or random.randint(0, 99999)

        # 自動選擇主角
        if protagonist:
            self.protagonist = protagonist
        else:
            rng = random.Random(self.seed)
            self.protagonist = rng.choice(PROTAGONISTS)

        self.protagonist_emoji = PROTAGONIST_EMOJI.get(self.protagonist, "✨")

        # 自動選擇寵物
        if pet:
            for name, emoji in PET_OPTIONS:
                if name == pet:
                    self.pet_name = name
                    self.pet_emoji = emoji
                    break
            else:
                self.pet_name = pet
                self.pet_emoji = "🐾"
        else:
            rng = random.Random(self.seed + 1)
            pet_choice = rng.choice(PET_OPTIONS)
            self.pet_name = pet_choice[0]
            self.pet_emoji = pet_choice[1]

    # ── 段落長度調整 ──

    def _pad(self, text: str) -> str:
        """根據 length 調整內容豐富度"""
        if self.length == "long":
            return text + "\n\n然後呢？\n"
        return text

    def _toddlerify(self, text: str) -> str:
        """將文字改寫得更幼兒化（疊字、重複、短句）"""
        # 簡單的幼兒化處理
        replacements = [
            ("很", "好"),
            ("慢慢", "慢慢慢"),
            ("好開心", "好開心好開心"),
            ("好漂亮", "好漂亮好漂亮"),
            ("傷心", "傷心嗚嗚"),
            ("著急", "好急好急"),
            ("害怕", "有一點點害怕"),
        ]
        result = text
        for old, new in replacements:
            result = result.replace(old, new)
        return result

    # ── 模板選擇 ──

    def _pick_story(self) -> dict:
        """根據 age 和 theme 選擇故事模板"""
        rng = random.Random(self.seed)

        if self.sequel_to:
            if self.age == "toddler":
                templates = SEQUEL_TEMPLATES_TODDLER
            else:
                templates = SEQUEL_TEMPLATES_PRESCHOOL
            sequel_text = rng.choice(templates).format(
                protagonist=self.protagonist,
                pet_name=self.pet_name
            )
            return {"is_sequel": True, "sequel_intro": sequel_text}

        if self.theme == "idiom":
            if self.age == "toddler":
                return rng.choice(IDOM_TEMPLATES_TODDLER)
            else:
                return rng.choice(IDOM_TEMPLATES_PRESCHOOL)

        if self.theme == "fairytale":
            if self.age == "toddler":
                return rng.choice(FAIRYTALE_TEMPLATES_TODDLER)
            else:
                return rng.choice(FAIRYTALE_TEMPLATES_PRESCHOOL)

        if self.theme == "emotion":
            # 情緒主題：優先選情緒相關模板
            emotion_templates = {
                k: v for k, v in
                (STORY_TEMPLATES_TODDLER if self.age == "toddler"
                 else STORY_TEMPLATES_PRESCHOOL).items()
                if v["theme"] == "emotion"
            }
            if emotion_templates:
                return rng.choice(list(emotion_templates.values()))

        if self.age == "toddler":
            return rng.choice(list(STORY_TEMPLATES_TODDLER.values()))
        else:
            return rng.choice(list(STORY_TEMPLATES_PRESCHOOL.values()))

    # ── 故事格式化 ──

    def _build_body(self, template: dict) -> str:
        """根據模板格式建立故事主體（支援段落式或一整段式模板）"""
        # 段落式模板（有 setup/problem/attempt/solution）
        if "setup" in template:
            if self.age == "toddler":
                return (
                    f"{template['setup']} "
                    f"{self._toddlerify(template['problem'])} "
                    f"{self._pad(self._toddlerify(template['attempt']))} "
                    f"{template['solution']}"
                )
            else:
                return (
                    f"{template['setup']} "
                    f"{template['problem']} "
                    f"{self._pad(template['attempt'])} "
                    f"{template['solution']}"
                )
        # 一整段式模板（有 story 欄位）
        elif "story" in template:
            return template["story"]
        return "✨ 今晚的故事來囉！✨"

    def generate(self) -> dict:
        """生成完整故事"""
        template = self._pick_story()

        if template.get("is_sequel"):
            intro = template["sequel_intro"]
            base = self._pick_story()  # 再選一個當續集內容
            body = f"{intro}\n\n{self._build_body(base)}"
        else:
            body = self._build_body(template)

        # 替換角色名稱
        body = body.replace("小兔子", self.protagonist)
        body = body.replace("🐰", self.protagonist_emoji)

        # 加入寵物
        if self.pet_name and self.pet_name not in self.protagonist:
            pet_line = f"還有{self.pet_name}也陪在他身邊呢！"
            body = pet_line + "\n" + body

        # idiom / fairytale 等一整段式模板：story 欄位已包含完整敘事+結尾
        # 不重複附加 ending，避免重複
        if "story" in template and "ending" not in template:
            story_text = body
        else:
            ending = template.get("ending", "晚安，小朋友，明天也要加油喔！🌙")
            story_text = f"{body}\n\n{ending}"

        return {
            "title": template.get("title", "✨ 睡前故事 ✨").replace("🐰", self.protagonist_emoji),
            "story": story_text,
            "lesson": template.get("moral", template.get("lesson", "🌟 晚安 🌟")),
            "emoji": template.get("emoji", self.protagonist_emoji) + self.pet_emoji,
            "theme": self.theme or template.get("theme", "original"),
            "age": self.age,
            "length": self.length,
            "protagonist": self.protagonist,
            "protagonist_emoji": self.protagonist_emoji,
            "pet": self.pet_name,
            "pet_emoji": self.pet_emoji,
            "is_sequel": template.get("is_sequel", False),
        }

    # ── 估時功能 ──

    def estimate_duration(self) -> dict:
        """估算故事時長"""
        lengths = {
            "short": {"paragraphs": 2, "minutes_toddler": 2, "minutes_preschool": 3},
            "medium": {"paragraphs": 4, "minutes_toddler": 4, "minutes_preschool": 5},
            "long": {"paragraphs": 6, "minutes_toddler": 7, "minutes_preschool": 8},
        }
        info = lengths[self.length]
        minutes = (info["minutes_toddler"] if self.age == "toddler"
                   else info["minutes_preschool"])
        return {
            "paragraphs": info["paragraphs"],
            "minutes": minutes,
            "display": f"約 {minutes} 分鐘"
        }


# ─────────────────────────────────────────────
# 🚀 命令列介面
# ─────────────────────────────────────────────

def print_story(story_data: dict, player=None):
    """格式化輸出故事"""
    print()
    print("=" * 50)
    print(f"  {story_data['emoji']}  {story_data['title']}")
    print("=" * 50)
    print()

    story = story_data["story"]
    # 分段顯示
    paragraphs = [p.strip() for p in story.split("\n") if p.strip()]

    for i, para in enumerate(paragraphs, 1):
        print(f"  [{i}/{len(paragraphs)}] {para}")
        print()

    print("─" * 30)
    print(f"  💡 {story_data['lesson']}")
    print("─" * 30)
    print()

    # 朗讀提示
    if player:
        player.prompt_play(story_data)


def list_templates(age: str = "all"):
    """列出所有模板"""
    print("\n📚 故事模板列表\n")

    if age in ("toddler", "all"):
        print("【2-3歲模板】🐰")
        for key, t in STORY_TEMPLATES_TODDLER.items():
            theme_icon = {"friendship": "🌈", "emotion": "💤",
                          "original": "✨", "idiom": "🏠", "fairytale": "📖"}
            icon = theme_icon.get(t["theme"], "✨")
            print(f"  • {icon} {t['title']}")

    if age in ("preschool", "all"):
        print("\n【4-6歲模板】🧒")
        for key, t in STORY_TEMPLATES_PRESCHOOL.items():
            theme_icon = {"friendship": "🌈", "emotion": "💤",
                          "original": "✨", "idiom": "🏠", "fairytale": "📖"}
            icon = theme_icon.get(t["theme"], "✨")
            print(f"  • {icon} {t['title']}")

    print("\n【成語改編】🏠")
    for t in IDOM_TEMPLATES_TODDLER:
        print(f"  🏠 {t['title']}")
    for t in IDOM_TEMPLATES_PRESCHOOL:
        print(f"  🏠 {t['title']}")

    print("\n【格林童話改編】📖")
    for t in FAIRYTALE_TEMPLATES_TODDLER:
        print(f"  📖 {t['title']}")
    for t in FAIRYTALE_TEMPLATES_PRESCHOOL:
        print(f"  📖 {t['title']}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="🌙 睡前故事精靈 — 為 2-6 歲孩童生成床邊故事",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  python3 story_generator.py                         # 隨機故事
  python3 story_generator.py --protagonist 小熊       # 指定主角
  python3 story_generator.py --age preschool          # 4-6歲版本
  python3 story_generator.py --length long            # 長版故事
  python3 story_generator.py --theme emotion          # 情緒主題
  python3 story_generator.py --list-templates         # 列出所有模板
  python3 story_generator.py --sequel-to demo         # 生成續集
        """
    )
    parser.add_argument("--protagonist", "-p", help="主角名稱（預設隨機）")
    parser.add_argument("--pet", help="寵物角色（預設隨機）")
    parser.add_argument("--age", "-a", choices=["toddler", "preschool"],
                        default="toddler", help="年齡分段（預設 toddler）")
    parser.add_argument("--length", "-l", choices=["short", "medium", "long"],
                        default="short", help="故事長度（預設 short）")
    parser.add_argument("--theme", "-t",
                        choices=["friendship", "emotion", "idiom",
                                  "fairytale", "original"],
                        help="故事主題")
    parser.add_argument("--sequel-to", help="接續某個故事 ID 生成續集")
    parser.add_argument("--list-templates", action="store_true",
                        help="列出所有故事模板")
    parser.add_argument("--seed", type=int, help="隨機種子（重現相同故事）")
    parser.add_argument("--no-play", action="store_true",
                        help="僅生成故事，不朗讀")

    args = parser.parse_args()

    if args.list_templates:
        list_templates()
        return

    # 生成故事
    gen = StoryGenerator(
        protagonist=args.protagonist,
        pet=args.pet,
        age=args.age,
        length=args.length,
        theme=args.theme,
        sequel_to=args.sequel_to,
        seed=args.seed,
    )

    story_data = gen.generate()
    duration = gen.estimate_duration()

    print()
    print(f"🌙 生成故事：{story_data['title']}")
    print(f"⏱️  預估時長：{duration['display']}")
    print(f"📂 主角：{story_data['protagonist_emoji']} {story_data['protagonist']}")
    if story_data['pet']:
        print(f"🐾 寵物：{story_data['pet_emoji']} {story_data['pet']}")
    print()

    print_story(story_data)


if __name__ == "__main__":
    main()
