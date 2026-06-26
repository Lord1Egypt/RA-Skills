# 快速开始

**适用场景**: 已安装 fzf，开始学习核心用法，掌握日常工作中最常用的操作

---

## 一、基础交互操作

### 目标

掌握 fzf 的基本界面操作与搜索语法

### 启动 fzf

**AI 执行说明**: AI 可演示 fzf 的基础交互

```bash
# 最简单的启动方式（递归列出当前目录文件）
fzf

# 从标准输入读取候选项
ls /usr/bin | fzf

# 将选中结果传递给命令
cat $(fzf)
vim $(fzf)
```

### 界面说明

fzf 界面由两部分组成：
- **候选列表**（上方）：显示所有候选项，当前选中项高亮
- **输入框**（下方）：实时输入过滤条件

**键盘操作**:

| 按键 | 功能 |
|------|------|
| `↑` / `↓` 或 `CTRL-P` / `CTRL-N` | 上下移动光标 |
| `Enter` | 确认选中 |
| `Esc` 或 `CTRL-C` | 取消退出 |
| `Tab` | 多选模式下切换选中状态 |
| `CTRL-A` | 全选（多选模式） |
| `CTRL-D` | 向下翻页 |
| `CTRL-U` | 向上翻页 |
| `CTRL-/` | 切换预览窗口 |

---

## 二、搜索语法

### 目标

掌握 fzf 的各种搜索模式，精准定位目标

**AI 执行说明**: AI 会根据用户描述自动构建正确的搜索语法

### 模糊搜索（默认）

```bash
# 直接输入字符，fzf 会模糊匹配
# 例如：输入 "vimrc" 可匹配 ".vimrc"、"vim-config" 等
echo -e ".vimrc\nvim-config\nneovim.conf\nbashrc" | fzf
```

### 精确匹配模式

```bash
# 在查询前加单引号 '，强制精确匹配
echo -e "foobar\nfoo bar\nfoo_bar" | fzf --query "'foo bar"
```

### 前缀与后缀匹配

```bash
# ^ 前缀匹配：只匹配以 "foo" 开头的项
echo -e "foobar\nbarfoo\nfoo123" | fzf --query "^foo"

# $ 后缀匹配：只匹配以 ".go" 结尾的项
find . -type f | fzf --query ".go$"
```

### 组合搜索

```bash
# 空格分隔 = AND（必须同时满足）
find . -type f | fzf --query "src .go"

# 管道符 | = OR（满足其一即可）
find . -type f | fzf --query ".go | .ts"

# ! 取反（排除匹配项）
find . -type f | fzf --query "!test"

# 组合示例：在 src 目录下的 Go 文件，但排除测试文件
find . -type f | fzf --query "src .go !_test"
```

---

## 三、Shell 快捷键实战

### CTRL-T：文件路径插入

**场景**: 在命令中需要指定文件路径，但不记得确切路径

```bash
# 在命令提示符下，输入 vim 后按 CTRL-T
vim <CTRL-T>
# → fzf 弹出文件选择界面，选中后路径自动插入命令行
# → 最终变成：vim /path/to/selected/file.txt
```

**AI 执行说明**: AI 会模拟此操作并建议合适的文件

---

### CTRL-R：历史命令搜索

**场景**: 记得曾经执行过某个命令，但不记得完整命令

```bash
# 在命令提示符下按 CTRL-R
# → fzf 弹出历史命令搜索界面
# → 输入关键词（如 "docker run"）筛选历史
# → 选中后命令自动填入命令行
```

**对比默认 CTRL-R**:
- 默认 Shell：只显示最近一条匹配
- fzf 增强：显示所有匹配历史，可交互选择

---

### ALT-C：目录跳转

**场景**: 快速 cd 进入深层目录

```bash
# 在命令提示符下按 ALT-C（macOS 需按 ESC+C 或配置 Option 为 Meta 键）
# → fzf 弹出目录选择界面（仅显示目录）
# → 选中后自动执行 cd 命令
```

---

## 四、常用工作流示例

### 打开文件

```bash
# 在当前目录模糊查找并用 vim 打开
vim $(fzf)

# 使用 bat 预览，用 vim 打开
vim $(fzf --preview 'bat --color=always {}')

# 忽略 .gitignore，搜索所有文件
vim $(git ls-files | fzf)
```

### 查找并 cd 进入目录

```bash
# 查找目录并进入
cd $(find . -type d | fzf)

# 使用 fd 列出目录
cd $(fd --type d | fzf)
```

### 杀死进程

```bash
# 查找进程并 kill
kill -9 $(ps aux | fzf | awk '{print $2}')

# 更友好的版本（只显示进程名和 PID）
kill -9 $(ps -ef | fzf --header-lines=1 | awk '{print $2}')
```

### 搜索并查看 Git 提交

```bash
# 交互式查看 git log
git log --oneline | fzf --preview 'git show --stat $(echo {} | cut -d" " -f1)'

# 签出分支
git branch | fzf | xargs git checkout

# 交互式 git add
git diff --name-only | fzf --multi | xargs git add
```

### 切换 Docker 容器

```bash
# 进入运行中的 Docker 容器
docker exec -it $(docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' | fzf --header-lines=1 | awk '{print $1}') bash
```

---

## 五、基础参数速查

**AI 执行说明**: AI 会根据使用场景自动选择合适的参数组合

### 显示与布局

```bash
# 反向布局（输入框在上）
fzf --reverse

# 显示边框
fzf --border

# 占用屏幕高度的 40%（而不是全屏）
fzf --height=40%

# 设置提示文字
fzf --prompt="选择文件: "

# 显示匹配信息
fzf --info=inline
```

### 预览窗口

```bash
# 右侧预览，占 50% 宽度
fzf --preview 'cat {}' --preview-window=right:50%

# 下方预览，占 40% 高度
fzf --preview 'cat {}' --preview-window=down:40%

# 预览时显示行号
fzf --preview 'cat -n {}'

# 使用 bat 高亮预览
fzf --preview 'bat --color=always --style=numbers {}'

# 切换预览（按 CTRL-/）
fzf --preview 'bat --color=always {}' --bind 'ctrl-/:toggle-preview'
```

### 初始查询与默认选项

```bash
# 设置初始查询字符串
fzf --query "main.go"

# 设置初始选中项（选中包含 main 的第一项）
fzf --select-1 --query "main"

# 多选模式
fzf --multi

# 设置最多可选数量
fzf --multi=5
```

---

## 六、自定义键绑定入门

**AI 执行说明**: AI 会根据个人工作流定制键绑定

```bash
# 按 CTRL-Y 将选中项复制到剪贴板（macOS）
fzf --bind 'ctrl-y:execute-silent(echo {} | pbcopy)'

# 按 CTRL-E 在编辑器中打开
fzf --bind 'ctrl-e:execute(vim {})'

# 按 Enter 在新 tmux 窗口中打开
fzf --bind 'enter:execute(tmux new-window vim {})'

# F2 切换预览开关
fzf --preview 'cat {}' --bind 'f2:toggle-preview'
```

---

## 七、配置 FZF_DEFAULT_OPTS

通过环境变量持久化默认选项，避免每次手动指定：

**AI 执行说明**: AI 会将以下内容添加到 Shell 配置文件

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export FZF_DEFAULT_OPTS='
  --height=40%
  --layout=reverse
  --border
  --info=inline
  --preview "bat --color=always {} 2>/dev/null || cat {}"
  --preview-window=right:50%:hidden
  --bind "ctrl-/:toggle-preview"
  --bind "ctrl-a:select-all"
  --bind "ctrl-d:deselect-all"
'

# 使用 fd 替代 find（更快、尊重 .gitignore）
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'

# CTRL-T 使用 fd
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# ALT-C 只列出目录
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
```

---

## 完成确认

### 检查清单

- [ ] 能够运行 `fzf` 并使用基础模糊搜索
- [ ] 理解搜索语法（模糊、精确、前/后缀、AND/OR/NOT）
- [ ] 能使用 CTRL-T、CTRL-R、ALT-C 快捷键
- [ ] 能使用 `--preview` 显示文件预览
- [ ] 已配置 `FZF_DEFAULT_OPTS` 优化默认行为

### 下一步

继续阅读 [高级用法](03-advanced-usage.md) 学习脚本集成、自定义函数等进阶技巧
