# 安装说明：baby-growth-tracker

面向收到这个技能包的人。照着做 3 分钟即可用。

## 这是什么

一个 WorkBuddy Skill：用自然语言让 AI 帮你记录宝宝每餐吃了什么、身高体重，自动算营养缺口、WHO 生长曲线判型、7/30 天报告。

- 不依赖任何 App、不联网、不上传数据、不需要手机或 adb
- 只用 Python 标准库，无 pip 依赖
- 包内**不含任何个人数据**，你拿到的是空库

## 环境要求

| 项 | 要求 |
|---|---|
| WorkBuddy | 桌面端，支持用户级 / 项目级 Skill |
| Python | 3.8 及以上（Windows 用 `python`，macOS/Linux 可能是 `python3`） |
| 系统 | Windows / macOS / Linux 均可 |

## 安装

### 方式 A：个人使用（推荐）

1. 解压 `baby-growth-tracker.zip`，得到 `baby-growth-tracker/` 文件夹。
2. 把**整个文件夹**放进用户技能目录：

   - Windows：`C:\Users\你的用户名\.workbuddy\skills\`
   - macOS / Linux：`~/.workbuddy/skills/`

3. 最终结构必须是：

   ```
   ~/.workbuddy/skills/baby-growth-tracker/SKILL.md
   ```

   注意层级：`SKILL.md` 必须在 `baby-growth-tracker/` 里面，不要多套一层，也不要把里面的文件散着放。

4. 重启 WorkBuddy（或在技能设置里刷新），在「已安装」里应能看到 `baby-growth-tracker`。

### 方式 B：团队 / 项目共享

把 `baby-growth-tracker/` 放到项目根目录的 `.workbuddy/skills/baby-growth-tracker/`，随代码仓库提交。clone 该项目的人都会自动带上这个技能。

命令行写法（在项目根目录执行）：

```bash
mkdir -p .workbuddy/skills
cp -r baby-growth-tracker .workbuddy/skills/
```

### 方式 C：从 Git 仓库安装

适合直接发仓库链接、不走 zip 的场景。完整版见仓库根目录 `README.md` 第 9 节。

**1) 克隆仓库**

```bash
git clone https://github.com/qredsun-a11y/baby-growth.git
cd baby-growth
```

只想拿 Skill、不想下载 App 源码：

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/qredsun-a11y/baby-growth.git
cd baby-growth
git sparse-checkout set skills/baby-growth-tracker
```

**2) 把整个文件夹拷进用户技能目录**（别只拷里面的文件）

```bash
mkdir -p ~/.workbuddy/skills
cp -r skills/baby-growth-tracker ~/.workbuddy/skills/
```

上面这条在 Windows Git Bash、macOS、Linux 通用。Windows PowerShell 写法：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.workbuddy\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\baby-growth-tracker" "$env:USERPROFILE\.workbuddy\skills\"
```

最终结构同样必须是 `~/.workbuddy/skills/baby-growth-tracker/SKILL.md`。

**3) 重启 WorkBuddy**，然后按下方「首次使用」初始化。

> 仓库是公开的且含 App 源码，但 Skill 不依赖 Flutter / App / 手机。别把 `data.json` 或导出的备份 JSON 提交进仓库。

## 首次使用：必须初始化数据

数据文件默认在 `~/.workbuddy/baby-growth/data.json`，**首次不存在**。在技能目录下执行：

```bash
python scripts/baby.py init
python scripts/baby.py add-baby --name 宝宝 --birth 2025-01-30 --height 80 --weight 10
python scripts/baby.py status
```

如果发送方另外给了 `备份.json`：

```bash
python scripts/baby.py import-backup --file "备份.json" --replace
```

初始化之后，最方便的用法是直接用自然语言跟 AI 说，例如「记一下今天中午吃了米饭 100g 和鸡蛋 50g」「今天营养够吗」「量了身高 81.5、体重 10.4」。

## 验证安装

```bash
python scripts/baby.py status          # 显示数据路径与当前宝宝
python scripts/baby.py foods --search 鸡蛋
python scripts/baby.py advice          # 空库会提示先建档
```

三条都不报错即安装成功。

## 数据与隐私

- 所有记录只在本机 `~/.workbuddy/baby-growth/data.json`，每次写入自动留 `.json.bak`。
- 想换位置（加密盘、项目目录等）：命令加 `--data 路径`，或设环境变量 `BABY_GROWTH_DATA`。
- **要连数据一起分享**：执行 `python scripts/baby.py export --out "备份.json"`，把该文件单独发给对方。里面含儿童姓名、生日、身高体重和喂养记录，属于敏感健康信息，只走可信渠道，不要传公共群或公开网盘。
- 技能包本身（zip）不含这些数据，可以放心转发。

## 常见问题

| 现象 | 处理 |
|---|---|
| 提示「数据文件不存在」 | 跑 `init`，或 `import-backup --file 备份.json` |
| 提示「未知食物 id」 | 用 `foods --search 名称` 查准确 id，例如 `rice`、`egg` |
| AI 没自动触发技能 | 检查目录层级是否为 `skills/baby-growth-tracker/SKILL.md`，然后重启 WorkBuddy |
| `python` 找不到 | macOS/Linux 换成 `python3`；Windows 确认 Python 已加进 PATH |
| 中文输出乱码 | Windows 终端执行 `chcp 65001` 或用 Windows Terminal |

完整命令与规则见 `SKILL.md`、`references/data-contract.md`、`references/nutrition-rules.md`。要接到其它 Agent 宿主或别的模型，见 `UNIVERSAL.md`。

## 免责声明

内置营养数据为常见食材近似值，建议由本地规则生成，仅供参考，不构成医疗诊断。WHO 标准适用于足月儿，早产儿需按矫正月龄咨询医生。宝宝如有特殊健康状况，请咨询医生或营养师。
