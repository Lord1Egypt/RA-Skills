# chameleon-ultra-cli

一个用于 [WorkBuddy](https://www.codebuddy.cn/) 的技能（Skill），让你用大白话指挥
[Chameleon Ultra](https://github.com/RfidResearchGroup/ChameleonUltra) 读写卡器，
把加密 IC 卡（门禁卡、电梯卡等）复制、读取、模拟出来，全程不用自己敲命令行。

## 语言 / Languages / Langues

- **中文**
  - [简体中文](#简体中文)
  - [香港正體](#香港正體)
  - [新加坡中文](#新加坡中文)
- [English](#english)
- [Français](#french)

---

## 简体中文

### 背景介绍

在国内，很多小区的物业会限制业主自由使用属于自己的门禁卡：补一张卡动辄几十上百元、
绑定手机号、甚至规定「一张卡只能对应一个人」，本质是把本该免费提供给业主的便利变成
持续的收费项目，情节严重的已经涉嫌恶意收费、侵占业主权益。

而绝大多数业主手里的门禁卡其实是**加密的 IC 卡（MIFARE Classic 居多）**。一旦丢了或
需要多备一张，物业就借机收费。其实，只要是你**自己小区、自己名下的卡**，复制一张备用
完全是你个人的正当权利。

问题在于：变色龙 Ultra 这类设备的官方操作依赖一个命令行程序，要在交互式界面里手敲一堆
命令，对普通小白极不友好。为了解决这个问题，我制作了这个 Skill——把复杂的命令行交互
封装起来，你只需要用自然语言告诉 WorkBuddy 想做什么，它就会自动完成连接、读卡、复制、
模拟等全流程操作。

> 说明：本工具仅用于复制**你本人拥有合法使用权**的卡片（自家门禁、自家电梯卡等）。
> 请勿用于复制不属于你的、或未经授权的他人卡片。

### 使用方法（小白向）

**第 1 步：下载变色龙 Ultra 的命令行程序**

本程序**只支持 Windows 系统**，请在 Windows 电脑上操作。

- 下载地址：https://wwaxz.lanzoul.com/iar123ylt1sh
- 提取密码：**6bm4**
- 下载后解压，你会得到一个 `chameleon_cli_main.exe` 文件，**记住它的完整路径**
  （例如 `C:\tools\chameleon\chameleon_cli_main.exe`）。

**第 2 步：安装本 Skill 到 WorkBuddy**

把整个 `chameleon-ultra-cli` 文件夹放到 WorkBuddy 的用户技能目录：

```
C:\Users\你的用户名\.workbuddy\skills\chameleon-ultra-cli\
```

**第 3 步：告诉 Skill 程序在哪（只需一次）**

打开 WorkBuddy，对助手说类似这样的话，把第 1 步记下的路径填进去：

```
请设置变色龙程序路径为 C:\tools\chameleon\chameleon_cli_main.exe
```

（本质就是执行了 `python scripts/chameleon_control.py --set-exe "你的路径"`，
路径会保存下来，以后不用再设。）

**第 4 步：插上设备，开始用大白话指挥**

用 USB 把变色龙 Ultra 连上电脑，然后直接用自然语言下指令即可，例如：

- 「读一下我这张门禁卡的信息」
- 「把这张卡复制一份到卡槽 8 里」
- 「扫描一下这张高频卡，看看 UID 是什么」

Skill 会自动连上设备、执行对应命令、把结果翻成你能看懂的话返回给你。

**常用参数（进阶，可不看）**

- `--timeout 秒数`：读卡 / 跑攻击比较慢时用，把等待时间调大（默认 120 秒）
- `--file 命令.txt`：把一堆命令写进文本文件，逐行批量执行（`#` 开头是注释）
- `--raw`：保留原始终端输出，仅在排查问题时用

### 技术原理（简述）

为什么不能直接用官方命令行程序？因为它是一个**交互式 REPL**（基于 prompt_toolkit），
就像个一直在等你敲命令的小窗口——你没法简单地把命令「管道」喂给它，在 Windows 上尤其
会直接报错。

本 Skill 的解法是：

1. **伪终端（PTY）包裹**：在 Windows 上用 `pywinpty`（首次运行会自动建好环境安装），
   在 Linux / macOS 上用系统自带的 `pty` 模块，把官方程序包进一个「假终端」里，
   这样就能像真人一样给它下发命令、并可靠地读回输出。
2. **自动会话管理**：每次调用都会自动先发 `hw connect` 连设备、最后发 `exit` 退出，
   保证每次都是干净、能自己结束的独立会话。
3. **踩过的关键坑**（已自动处理，你无需关心）：
   - 换行符必须用 `LF(\n)`，用回车 `\r` 会被当成补全触发；
   - 程序启动会发终端能力查询并等应答才显示提示符，Skill 会自动回写应答，
     否则它会「卡死」、什么都不输出。

### 致谢

本 Skill 建立在变色龙 Ultra 开源项目的成果之上，衷心感谢原作者的无私开源：

**RfidResearchGroup / ChameleonUltra**
https://github.com/RfidResearchGroup/ChameleonUltra

没有这个优秀的开源硬件与固件，普通用户根本无法低成本地拿回本就属于自己那张卡的控制权。

---

## 香港正體

### 背景介紹

在國內，很多小區的物業會限制業主自由使用屬於自己的門禁卡：補一張卡動輒幾十上百元、
綁定手機號、甚至規定「一張卡只能對應一個人」，本質是把本該免費提供給業主的便利變成
持續的收費項目，情節嚴重的已經涉嫌惡意收費、侵占業主權益。

而絕大多數業主手裡的門禁卡其實是**加密的 IC 卡（MIFARE Classic 居多）**。一旦掉了或
需要多備一張，物業就藉機收費。其實，只要是你**自己小區、自己名下的卡**，複製一張備用
完全是你個人的正當權利。

問題在於：變色龍 Ultra 這類設備的官方操作依賴一個命令列程式，要在互動式介面裡手敲一堆
命令，對普通小白極不友善。為了解決這個問題，我製作了這個 Skill——把複雜的命令列互動
封裝起來，你只需要用自然語言告訴 WorkBuddy 想做什麼，它就會自動完成連接、讀卡、複製、
模擬等全流程操作。

> 說明：本工具僅用於複製**你本人擁有合法使用權**的卡片（自家門禁、自家電梯卡等）。
> 請勿用於複製不屬於你的、或未經授權的他人卡片。

### 使用方法（小白向）

**第 1 步：下載變色龍 Ultra 的命令列程式**

本程式**只支援 Windows 系統**，請在 Windows 電腦上操作。

- 下載地址：https://wwaxz.lanzoul.com/iar123ylt1sh
- 提取密碼：**6bm4**
- 下載後解壓，你會得到一個 `chameleon_cli_main.exe` 檔案，**記住它的完整路徑**
  （例如 `C:\tools\chameleon\chameleon_cli_main.exe`）。

**第 2 步：安裝本 Skill 到 WorkBuddy**

把整個 `chameleon-ultra-cli` 資料夾放到 WorkBuddy 的使用者技能目錄：

```
C:\Users\你的使用者名稱\.workbuddy\skills\chameleon-ultra-cli\
```

**第 3 步：告訴 Skill 程式在哪（只需一次）**

開啟 WorkBuddy，對助手說類似這樣的話，把第 1 步記下的路徑填進去：

```
請設定變色龍程式路徑為 C:\tools\chameleon\chameleon_cli_main.exe
```

（本質就是執行了 `python scripts/chameleon_control.py --set-exe "你的路徑"`，
路徑會儲存下來，以後不用再設。）

**第 4 步：插上裝置，開始用大白話指揮**

用 USB 把變色龍 Ultra 連上電腦，然後直接用自然語言下指令即可，例如：

- 「讀一下我這張門禁卡的資訊」
- 「把這張卡複製一份到卡槽 8 裡」
- 「掃描一下這張高頻卡，看看 UID 是什麼」

Skill 會自動連上裝置、執行對應命令、把結果翻成你能看懂的話傳回給你。

**常用參數（進階，可不看）**

- `--timeout 秒數`：讀卡 / 跑攻擊比較慢時用，把等待時間調大（預設 120 秒）
- `--file 命令.txt`：把一堆命令寫進文字檔，逐行批次執行（`#` 開頭是註解）
- `--raw`：保留原始終端輸出，僅在排查問題時用

### 技術原理（簡述）

為什麼不能直接用官方命令列程式？因為它是一個**互動式 REPL**（基於 prompt_toolkit），
就像個一直在等你敲命令的小視窗——你沒法簡單地把命令「管道」餵給它，在 Windows 上尤其
會直接報錯。

本 Skill 的解法是：

1. **偽終端（PTY）包裹**：在 Windows 上用 `pywinpty`（首次執行會自動建好環境安裝），
   在 Linux / macOS 上用系統自帶的 `pty` 模組，把官方程式包進一個「假終端」裡，
   這樣就能像真人一樣給它下發命令、並可靠地讀回輸出。
2. **自動會話管理**：每次呼叫都會自動先發 `hw connect` 連裝置、最後發 `exit` 退出，
   保證每次都是乾淨、能自己結束的獨立會話。
3. **踩過的關鍵坑**（已自動處理，你無需關心）：
   - 換行符必須用 `LF(\n)`，用回車 `\r` 會被當成補全觸發；
   - 程式啟動會發終端能力查詢並等應答才顯示提示符，Skill 會自動回寫應答，
     否則它會「卡死」、什麼都不輸出。

### 致謝

本 Skill 建立在變色龍 Ultra 開源專案的成果之上，衷心感謝原作者的無私開源：

**RfidResearchGroup / ChameleonUltra**
https://github.com/RfidResearchGroup/ChameleonUltra

沒有這個優秀的開源硬體與韌體，普通用戶根本無法低成本地拿回本就屬於自己那張卡的控制權。

---

## 新加坡中文

### 背景介绍

在中国，许多住宅区（组屋区 / 公寓区）的物业管理公司会限制居民自由使用属于自己的门禁卡：
补一张卡动辄几十上百元、绑定手机号、甚至规定「一张卡只能对应一个人」，本质是把本应免费
提供给居民的便利变成持续的收费项目，情节严重的已涉嫌恶意收费、侵犯居民权益。

而绝大多数居民手里的门禁卡其实是**加密的 IC 卡（MIFARE Classic 居多）**。一旦遗失或
需要多备一张，物管公司就借机收费。其实，只要是你**自己住宅、自己名下的卡**，复制一张
备用完全是你个人的正当权利。

问题在于：变色龙 Ultra 这类设备的官方操作依赖一个命令行程序，要在交互式界面里手敲一堆
命令，对普通用户极不友好。为了解决这个问题，我制作了这个 Skill——把复杂的命令行交互
封装起来，你只需用自然语言告诉 WorkBuddy 想做什么，它就会自动完成连接、读卡、复制、
模拟等全流程操作。

> 说明：本工具仅用于复制**你本人拥有合法使用权**的卡片（自家门禁、自家电梯卡等）。
> 请勿用于复制不属于你的、或未经授权的他人卡片。

### 使用方法（小白向）

**第 1 步：下载变色龙 Ultra 的命令行程序**

本程序**只支持 Windows 系统**，请在 Windows 电脑上操作。

- 下载地址：https://wwaxz.lanzoul.com/iar123ylt1sh
- 提取密码：**6bm4**
- 下载后解压，你会得到一个 `chameleon_cli_main.exe` 文件，**记下它的完整路径**
  （例如 `C:\tools\chameleon\chameleon_cli_main.exe`）。

**第 2 步：安装本 Skill 到 WorkBuddy**

把整个 `chameleon-ultra-cli` 文件夹放到 WorkBuddy 的用户技能目录：

```
C:\Users\你的用户名\.workbuddy\skills\chameleon-ultra-cli\
```

**第 3 步：告诉 Skill 程序在哪（只需一次）**

打开 WorkBuddy，对助手说类似这样的话，把第 1 步记下的路径填进去：

```
请设置变色龙程序路径为 C:\tools\chameleon\chameleon_cli_main.exe
```

（本质就是执行了 `python scripts/chameleon_control.py --set-exe "你的路径"`，
路径会保存下来，以后不用再设。）

**第 4 步：插上设备，开始用大白话指挥**

用 USB 把变色龙 Ultra 连上电脑，然后直接用自然语言下指令即可，例如：

- 「读一下我这张门禁卡的信息」
- 「把这张卡复制一份到卡槽 8 里」
- 「扫描一下这张高频卡，看看 UID 是什么」

Skill 会自动连上设备、执行对应命令、把结果翻成你能看懂的话返回给你。

**常用参数（进阶，可不看）**

- `--timeout 秒数`：读卡 / 跑攻击比较慢时用，把等待时间调大（默认 120 秒）
- `--file 命令.txt`：把一堆命令写进文本文件，逐行批量执行（`#` 开头是注释）
- `--raw`：保留原始终端输出，仅在排查问题时用

### 技术原理（简述）

为什么不能直接用官方命令行程序？因为它是一个**交互式 REPL**（基于 prompt_toolkit），
就像个一直在等你敲命令的小窗口——你没法简单地把命令「管道」喂给它，在 Windows 上尤其
会直接报错。

本 Skill 的解法是：

1. **伪终端（PTY）包裹**：在 Windows 上用 `pywinpty`（首次运行会自动建好环境安装），
   在 Linux / macOS 上用系统自带的 `pty` 模块，把官方程序包进一个「假终端」里，
   这样就能像真人一样给它下发命令、并可靠地读回输出。
2. **自动会话管理**：每次调用都会自动先发 `hw connect` 连设备、最后发 `exit` 退出，
   保证每次都是干净、能自己结束的独立会话。
3. **踩过的关键坑**（已自动处理，你无需关心）：
   - 换行符必须用 `LF(\n)`，用回车 `\r` 会被当成补全触发；
   - 程序启动会发终端能力查询并等应答才显示提示符，Skill 会自动回写应答，
     否则它会「卡死」、什么都不输出。

### 致谢

本 Skill 建立在变色龙 Ultra 开源项目的成果之上，衷心感谢原作者的无私开源：

**RfidResearchGroup / ChameleonUltra**
https://github.com/RfidResearchGroup/ChameleonUltra

没有这个优秀的开源硬件与固件，普通用户根本无法低成本地拿回本就属于自己那张卡的控制权。

---

## English

A [WorkBuddy](https://www.codebuddy.cn/) Skill that lets you command the
[Chameleon Ultra](https://github.com/RfidResearchGroup/ChameleonUltra) card reader
in plain language — clone, read, and emulate encrypted IC cards (access cards,
elevator cards, etc.) without ever typing commands yourself.

### Background

In China, many residential communities' property management restricts owners from
freely using their own access cards: replacing a lost card can cost dozens or even
over a hundred yuan, they force-binding phone numbers, and some even rule that
"one card may only belong to one person". In essence, a convenience that should be
provided to owners for free is turned into a recurring money-making scheme — in
serious cases it amounts to extortionate fees that infringe on owners' rights.

Most owners' access cards are actually **encrypted IC cards (mostly MIFARE Classic)**.
The moment you lose one or need a spare, the property management charges you again.
In reality, as long as it is a card for **your own home that you legitimately own**,
making a backup copy is entirely your personal right.

The problem: operating the Chameleon Ultra officially requires a command-line program
where you must type a pile of commands in an interactive prompt — far too unfriendly
for ordinary users. To solve this, I built this Skill: it wraps the complex CLI
interaction so you only need to tell WorkBuddy what you want in natural language, and
it automatically connects, reads, clones, and emulates the card for you.

> Note: This tool is only for cloning cards **you yourself have the legal right to
> use** (your own access card, your own elevator card, etc.). Do not use it to clone
> someone else's card without authorization.

### How to use (for beginners)

**Step 1: Download the Chameleon Ultra command-line program**

This program **only supports Windows**. Use a Windows computer.

- Download: https://wwaxz.lanzoul.com/iar123ylt1sh
- Password: **6bm4**
- After extracting you get a `chameleon_cli_main.exe` file — **remember its full path**
  (e.g. `C:\tools\chameleon\chameleon_cli_main.exe`).

**Step 2: Install this Skill into WorkBuddy**

Place the whole `chameleon-ultra-cli` folder into WorkBuddy's user skills directory:

```
C:\Users\your-username\.workbuddy\skills\chameleon-ultra-cli\
```

**Step 3: Tell the Skill where the program is (once only)**

Open WorkBuddy and tell the assistant something like this, filling in the path from Step 1:

```
Set the Chameleon program path to C:\tools\chameleon\chameleon_cli_main.exe
```

(Under the hood this runs `python scripts/chameleon_control.py --set-exe "your-path"`;
the path is saved so you never set it again.)

**Step 4: Plug in the device and just talk to it**

Connect the Chameleon Ultra to your PC via USB, then give instructions in natural language, e.g.:

- "Read the info of this access card of mine"
- "Clone this card into slot 8"
- "Scan this HF card and show me the UID"

The Skill auto-connects, runs the right commands, and returns the result in plain language.

**Common parameters (advanced, optional)**

- `--timeout SECONDS`: raise the wait limit for slow reads / attacks (default 120)
- `--file commands.txt`: run commands listed line-by-line in a text file (`#` starts a comment)
- `--raw`: keep raw terminal output, only for troubleshooting

### Technical principle (brief)

Why can't we just use the official CLI directly? Because it is an **interactive REPL**
(based on prompt_toolkit) — like a little window that always waits for you to type. You
cannot simply pipe commands into it; on Windows it fails outright.

This Skill's approach:

1. **Pseudo-terminal (PTY) wrapping**: on Windows it uses `pywinpty` (auto-installed on
   first run), and on Linux / macOS it uses the built-in `pty` module, wrapping the
   official program in a "fake terminal" so we can feed commands like a human and reliably
   read back the output.
2. **Automatic session management**: every call auto-sends `hw connect` first and `exit`
   last, guaranteeing a clean, self-terminating independent session each time.
3. **Key pitfalls already handled for you**:
   - The line terminator must be `LF(\n)`; a carriage return `\r` is mistaken for completion.
   - On startup the program sends terminal capability queries and waits for a reply before
     showing the prompt; the Skill auto-replies, otherwise it would "freeze" with no output.

### Acknowledgements

This Skill is built upon the Chameleon Ultra open-source project. Deep thanks to the
original authors for their generous open-source work:

**RfidResearchGroup / ChameleonUltra**
https://github.com/RfidResearchGroup/ChameleonUltra

Without this excellent open-source hardware and firmware, ordinary users could never
low-cost regain control over a card that was rightfully theirs.

---

## French

Un Skill pour [WorkBuddy](https://www.codebuddy.cn/) qui vous permet de piloter le lecteur
[Chameleon Ultra](https://github.com/RfidResearchGroup/ChameleonUltra) en langage courant —
cloner, lire et émuler des cartes IC chiffrées (cartes d'accès, cartes d'ascenseur, etc.)
sans jamais taper de commandes vous-même.

### Contexte

En Chine, la gestion immobilière de nombreuses résidences restreint les propriétaires dans
l'usage libre de leur propre carte d'accès : remplacer une carte perdue coûte des dizaines
voire plus d'une centaine de yuans, impose la liaison d'un numéro de téléphone, et certains
imposent même qu'« une carte ne peut correspondre qu'à une seule personne ». En substance,
une commodité qui devrait être fournie gratuitement aux propriétaires est transformée en
source de revenus récurrents — dans les cas graves, il s'agit de frais abusifs portant
atteinte aux droits des propriétaires.

La plupart des cartes d'accès des propriétaires sont en réalité des **cartes IC chiffrées
(le plus souvent MIFARE Classic)**. Dès que vous en perdez une ou en avez besoin d'une
supplémentaire, la gestion immobilière vous facture à nouveau. Or, tant qu'il s'agit d'une
carte **de votre propre logement dont vous êtes légitimement propriétaire**, en faire une
copie de sauvegarde est un droit strictement personnel.

Le problème : utiliser officiellement le Chameleon Ultra exige un programme en ligne de
commande où il faut taper une série de commandes dans un invite interactif — beaucoup trop
difficile pour un utilisateur ordinaire. Pour résoudre cela, j'ai créé ce Skill : il
encapsule l'interaction complexe de la CLI pour que vous n'ayez qu'à dire à WorkBuddy ce
que vous voulez, et il se connecte, lit, clone et émule la carte automatiquement.

> Note : cet outil sert uniquement à cloner les cartes **dont vous détenez légalement
> l'usage** (votre propre carte d'accès, votre propre carte d'ascenseur, etc.). Ne l'utilisez
> pas pour cloner la carte de quelqu'un d'autre sans autorisation.

### Mode d'emploi (pour débutants)

**Étape 1 : Télécharger le programme en ligne de commande du Chameleon Ultra**

Ce programme **ne fonctionne que sous Windows**. Utilisez un ordinateur Windows.

- Téléchargement : https://wwaxz.lanzoul.com/iar123ylt1sh
- Mot de passe : **6bm4**
- Après extraction vous obtenez un fichier `chameleon_cli_main.exe` — **notez son chemin
  complet** (par ex. `C:\tools\chameleon\chameleon_cli_main.exe`).

**Étape 2 : Installer ce Skill dans WorkBuddy**

Placez tout le dossier `chameleon-ultra-cli` dans le répertoire des compétences utilisateur
de WorkBuddy :

```
C:\Users\votre-nom-utilisateur\.workbuddy\skills\chameleon-ultra-cli\
```

**Étape 3 : Indiquer à le Skill où se trouve le programme (une seule fois)**

Ouvrez WorkBuddy et dites à l'assistant quelque chose comme ceci, en renseignant le chemin
de l'étape 1 :

```
Définir le chemin du programme Chameleon sur C:\tools\chameleon\chameleon_cli_main.exe
```

(En coulisses, cela exécute `python scripts/chameleon_control.py --set-exe "votre-chemin"` ;
le chemin est enregistré et vous n'aurez plus à le redéfinir.)

**Étape 4 : Branchez l'appareil et parlez-lui simplement**

Connectez le Chameleon Ultra à votre PC via USB, puis donnez des instructions en langage
naturel, par ex. :

- « Lis les infos de cette carte d'accès à moi »
- « Clone cette carte dans le slot 8 »
- « Scanne cette carte HF et montre-moi l'UID »

Le Skill se connecte automatiquement, exécute les bonnes commandes et renvoie le résultat
en langage clair.

**Paramètres courants (avancé, facultatif)**

- `--timeout SECONDES` : augmente la durée d'attente pour les lectures / attaques lentes
  (par défaut 120)
- `--file commandes.txt` : exécute les commandes ligne par ligne depuis un fichier texte
  (`#` commence un commentaire)
- `--raw` : conserve la sortie terminal brute, uniquement pour le dépannage

### Principe technique (en bref)

Pourquoi ne peut-on pas simplement utiliser la CLI officielle directement ? Parce que c'est
un **REPL interactif** (basé sur prompt_toolkit) — comme une petite fenêtre qui attend
toujours que vous tapiez. On ne peut pas simplement lui envoyer des commandes via un tube ;
sous Windows, cela échoue carrément.

L'approche de ce Skill :

1. **Enrobage dans un pseudo-terminal (PTY)** : sous Windows il utilise `pywinpty`
   (installé automatiquement à la première exécution), et sous Linux / macOS il utilise le
   module natif `pty`, enveloppant le programme officiel dans un « faux terminal » afin de
   pouvoir envoyer des commandes comme un humain et relire la sortie de façon fiable.
2. **Gestion automatique des sessions** : chaque appel envoie automatiquement `hw connect`
   au début et `exit` à la fin, garantissant une session indépendante, propre et
   auto-terminable à chaque fois.
3. **Pièges connus déjà gérés pour vous** :
   - Le terminateur de ligne doit être `LF(\n)` ; un retour chariot `\r` est pris pour une
     complétion.
   - Au démarrage, le programme envoie des requêtes de capacités du terminal et attend une
     réponse avant d'afficher l'invite ; le Skill y répond automatiquement, sinon il
     « gelait » sans rien afficher.

### Remerciements

Ce Skill s'appuie sur le projet open-source Chameleon Ultra. Merci profondément aux auteurs
originaux pour leur travail généreusement partagé :

**RfidResearchGroup / ChameleonUltra**
https://github.com/RfidResearchGroup/ChameleonUltra

Sans ce matériel et ce firmware open-source d'excellente qualité, les utilisateurs ordinaires
ne pourraient jamais, à faible coût, retrouver le contrôle d'une carte qui leur appartient
légitimement.

---

## 许可证 / License / Licence

[MIT-0](./LICENSE) —— 无需署名，可自由使用、修改、再分发 / No attribution required, free to
use, modify and redistribute / Aucune attribution requise, libre d'utiliser, modifier et
redistribuer.
