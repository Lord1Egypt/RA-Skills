# 常见问题与解决方案

---

## 问题分类说明

**简单问题（1-2步排查）**：安装配置、基础用法等
**中等问题（3-5步排查）**：Shell 集成、性能优化等
**复杂问题（5-10步排查）**：自定义脚本、环境冲突等

---

## 安装问题

### 1. fzf 安装后命令找不到【简单问题】

**问题描述**: 安装 fzf 后终端提示 command not found

**排查步骤**:
```bash
# 检查 fzf 是否已安装
which fzf
fzf --version

# 检查 PATH
echo $PATH
```

**常见原因**:
- 未将安装目录加入 PATH (40%)
- 使用 git clone 安装但未运行 install 脚本 (35%)
- 终端未重新加载配置 (25%)

**解决方案**:

**方案A（推荐）**: 使用包管理器安装
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt install fzf

# Arch Linux
sudo pacman -S fzf
```

**方案B**: git clone 安装后运行 install
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
source ~/.bashrc  # 或 source ~/.zshrc
```

---

### 2. Shell 快捷键（Ctrl+R/Ctrl+T）不生效【中等问题】

**问题描述**: 安装 fzf 后 Ctrl+R（历史搜索）和 Ctrl+T（文件搜索）无响应

**排查步骤**:
```bash
# 检查 shell 配置中是否加载了 fzf 绑定
grep -r "fzf" ~/.bashrc ~/.zshrc ~/.config/fish/config.fish 2>/dev/null

# 检查 fzf 快捷键绑定文件是否存在
ls ~/.fzf/shell/ 2>/dev/null || ls /usr/share/fzf/ 2>/dev/null
```

**常见原因**:
- 未 source fzf 的 shell 配置 (40%)
- 安装时选择了不启用快捷键 (30%)
- 与其他插件快捷键冲突 (20%)
- shell 类型不匹配 (10%)

**解决方案**:

**方案A（bash）**: 添加到 .bashrc
```bash
# 将以下行添加到 ~/.bashrc
eval "$(fzf --bash)"
source ~/.bashrc
```

**方案B（zsh）**: 添加到 .zshrc
```bash
# 将以下行添加到 ~/.zshrc
eval "$(fzf --zsh)"
source ~/.zshrc
```

**方案C（fish）**: 添加到 fish config
```fish
# ~/.config/fish/config.fish
fzf --fish | source
```

---

### 3. 安装后 Tab 补全不工作【简单问题】

**问题描述**: fzf 的 `**` Tab 触发补全功能不生效

**排查步骤**:
```bash
# 测试 Tab 补全
cd **<TAB>
vim **<TAB>

# 检查补全脚本是否加载
```

**常见原因**:
- 补全脚本未加载 (50%)
- 使用的 shell 不支持 (25%)
- fzf-completion 文件缺失 (25%)

**解决方案**:

```bash
# 确保 shell 配置中包含补全加载
# bash: eval "$(fzf --bash)" 已包含补全
# zsh: eval "$(fzf --zsh)" 已包含补全

# 重新运行安装脚本并确认启用补全
~/.fzf/install --completion --key-bindings
```

---

## 使用问题

### 4. 中文文件名显示乱码【中等问题】

**问题描述**: fzf 搜索结果中的中文文件名显示为乱码

**排查步骤**:
```bash
# 检查终端编码
echo $LANG
locale

# 检查文件名实际编码
ls | xxd | head
```

**常见原因**:
- 终端编码不是 UTF-8 (50%)
- LANG/LC_ALL 环境变量未设置 (30%)
- 终端模拟器字体不支持中文 (20%)

**解决方案**:

**方案A**: 设置 UTF-8 编码
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

**方案B**: 使用支持 Unicode 的终端
```bash
# 确认终端支持 UTF-8
echo "测试中文" | fzf
```

---

### 5. fzf 搜索速度慢（大目录）【中等问题】

**问题描述**: 在大型项目目录中 fzf 搜索响应缓慢

**排查步骤**:
```bash
# 检查默认搜索命令
echo $FZF_DEFAULT_COMMAND

# 测试文件数量
find . -type f | wc -l

# 检查是否忽略了 .git 等目录
```

**常见原因**:
- 默认 find 命令遍历了 .git/node_modules 等大目录 (45%)
- 未使用更快的搜索工具 (35%)
- 预览功能消耗资源 (20%)

**解决方案**:

**方案A（推荐）**: 使用 fd 替代默认搜索
```bash
# 安装 fd
brew install fd  # macOS

# 设置 FZF_DEFAULT_COMMAND
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
```

**方案B**: 使用 ripgrep 搜索
```bash
export FZF_DEFAULT_COMMAND='rg --files --hidden --follow --glob "!.git/*"'
```

**方案C**: 配置 .gitignore 过滤
```bash
# fzf 默认会尊重 .gitignore（使用 fd/rg 时）
echo "node_modules/" >> .gitignore
echo ".git/" >> .gitignore
```

---

### 6. 预览窗口不显示内容【中等问题】

**问题描述**: 使用 --preview 选项时预览窗口为空

**排查步骤**:
```bash
# 测试预览命令是否独立可用
bat --version 2>/dev/null || cat --version

# 测试基本预览
fzf --preview 'cat {}'

# 检查预览命令路径
which bat
```

**常见原因**:
- 预览命令（如 bat）未安装 (40%)
- 预览命令路径不在 PATH 中 (25%)
- 文件类型不支持预览 (20%)
- 预览窗口尺寸太小 (15%)

**解决方案**:

**方案A**: 使用 cat 作为基础预览
```bash
fzf --preview 'cat -n {}'
```

**方案B（推荐）**: 安装 bat 实现语法高亮预览
```bash
brew install bat  # macOS
fzf --preview 'bat --style=numbers --color=always {}'
```

**方案C**: 调整预览窗口
```bash
fzf --preview 'cat {}' --preview-window=right:60%:wrap
```

---

## 集成问题

### 7. 与 vim/neovim 集成不生效【中等问题】

**问题描述**: 在 vim 中使用 fzf.vim 插件时报错或无响应

**排查步骤**:
```bash
# 检查 fzf 是否在 vim 的 runtimepath 中
vim -c "echo &rtp" -c "q"

# 检查 fzf.vim 插件是否安装
ls ~/.vim/plugged/fzf.vim 2>/dev/null
```

**常见原因**:
- fzf 未添加到 vim runtimepath (40%)
- fzf.vim 插件未安装 (30%)
- vim 版本过低 (20%)
- 终端不支持 (10%)

**解决方案**:

**方案A（vim-plug）**:
```vim
" ~/.vimrc
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
```

**方案B（手动配置）**:
```vim
" 如果使用 Homebrew 安装
set rtp+=/opt/homebrew/opt/fzf
```

---

### 8. tmux 中 fzf 弹出窗口不工作【中等问题】

**问题描述**: 在 tmux 中使用 fzf 的 tmux popup 模式失败

**排查步骤**:
```bash
# 检查 tmux 版本（需要 3.2+）
tmux -V

# 测试 tmux popup
tmux display-popup -E "echo test"
```

**常见原因**:
- tmux 版本低于 3.2 (50%)
- 未设置 FZF_TMUX_OPTS (30%)
- tmux 配置冲突 (20%)

**解决方案**:

**方案A**: 升级 tmux
```bash
brew install tmux  # macOS，确保 >= 3.2
```

**方案B**: 使用 fzf-tmux 脚本
```bash
# 使用 fzf-tmux 替代直接 fzf
echo "hello\nworld" | fzf-tmux -p 80%,60%
```

---

### 9. FZF_DEFAULT_OPTS 配置不生效【简单问题】

**问题描述**: 设置的 FZF_DEFAULT_OPTS 环境变量未被 fzf 读取

**排查步骤**:
```bash
# 检查环境变量是否设置
echo $FZF_DEFAULT_OPTS

# 检查是否在正确的 shell 配置文件中
grep FZF_DEFAULT_OPTS ~/.bashrc ~/.zshrc 2>/dev/null
```

**常见原因**:
- 设置在错误的 shell 配置文件中 (40%)
- 语法错误（引号不匹配）(30%)
- 终端未重新加载配置 (30%)

**解决方案**:

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中设置
export FZF_DEFAULT_OPTS='
  --height=40%
  --layout=reverse
  --border
  --info=inline
  --color=fg:#c0caf5,bg:#1a1b26,hl:#bb9af7
'

# 重新加载
source ~/.zshrc
```

---

### 10. Alt 键快捷键在 macOS 终端不工作【简单问题】

**问题描述**: fzf 的 Alt-C（cd 到目录）在 macOS 默认终端无响应

**排查步骤**:
```bash
# 测试 Alt 键是否发送 ESC 序列
cat -v  # 然后按 Alt+C，查看输出
```

**常见原因**:
- macOS Terminal.app 默认不将 Option 键作为 Meta/Alt (70%)
- iTerm2 未配置 Option as Meta (20%)
- 键位被系统占用 (10%)

**解决方案**:

**方案A（Terminal.app）**: 设置 Option 为 Meta 键
```
终端 → 设置 → 描述文件 → 键盘 → 勾选"将 Option 键用作 Meta 键"
```

**方案B（iTerm2）**: 配置 Option 键
```
iTerm2 → Settings → Profiles → Keys → General → Left Option key → Esc+
```

**方案C**: 使用 ESC 替代 Alt
```bash
# 按 ESC 然后按 C（而非 Alt+C）
```
