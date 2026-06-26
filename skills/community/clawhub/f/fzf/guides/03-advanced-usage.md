# 高级用法

**适用场景**: 已掌握 fzf 基础操作，希望构建定制化工作流、集成到脚本与工具链

---

## 一、自定义 Shell 函数

### 目标

将常用 fzf 命令封装为 Shell 函数，提升重用性

**AI 执行说明**: AI 可将以下函数自动添加到用户的 Shell 配置文件

### fo：模糊打开文件

```bash
# 模糊搜索文件，用默认编辑器打开
fo() {
  local file
  file=$(fzf --query="$1" --select-1 --exit-0 \
    --preview 'bat --color=always {} 2>/dev/null || cat {}')
  [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}

# 用法
fo            # 搜索当前目录所有文件
fo "main.go"  # 初始查询为 main.go
```

### fcd：模糊跳转目录

```bash
# 模糊搜索目录并 cd 进入
fcd() {
  local dir
  dir=$(fd --type d --hidden --exclude .git 2>/dev/null | \
    fzf --preview 'ls -la {}' --query="$1") && cd "$dir"
}
```

### fh：增强历史命令搜索

```bash
# 搜索历史命令并执行（而非粘贴到命令行）
fh() {
  local cmd
  cmd=$(history | awk '{$1=""; print $0}' | sort -u | \
    fzf --tac --no-sort --query="$1")
  [[ -n "$cmd" ]] && eval "$cmd"
}
```

### fkill：交互式杀死进程

```bash
# 模糊搜索进程并发送 kill 信号
fkill() {
  local pid
  pid=$(ps -ef | \
    fzf --header-lines=1 --multi \
        --preview 'echo {}' --preview-window=down:3:wrap | \
    awk '{print $2}')
  [[ -n "$pid" ]] && echo "$pid" | xargs kill -${1:-9}
}
```

### fe：在编辑器中打开近期文件

```bash
# 打开最近修改的文件
fe() {
  local file
  file=$(find . -type f -newer ~/.bashrc 2>/dev/null | \
    fzf --preview 'bat --color=always {}')
  [[ -n "$file" ]] && ${EDITOR:-vim} "$file"
}
```

---

## 二、Git 工作流集成

**AI 执行说明**: AI 会将以下 Git 相关函数集成到 Shell 配置文件

### fbr：交互式切换 Git 分支

```bash
# 列出本地分支，预览该分支最近提交，切换选中分支
fbr() {
  local branches branch
  branches=$(git branch -vv) &&
  branch=$(echo "$branches" | \
    fzf --ansi --preview 'git log --oneline --graph --color=always $(echo {} | awk "{print \$1}")' | \
    awk '{print $1}')
  git checkout "$branch"
}

# 包含远程分支
fbrr() {
  local branches branch
  branches=$(git branch --all | grep -v HEAD) &&
  branch=$(echo "$branches" | \
    fzf --preview 'git log --oneline --graph --color=always $(echo {} | sed "s/.* //" | sed "s#remotes/[^/]*/##")' | \
    sed "s/.* //" | sed "s#remotes/[^/]*/##")
  git checkout "$branch"
}
```

### fco：交互式 git checkout 文件

```bash
# 交互式选择已修改文件执行 checkout（撤销修改）
fco() {
  local files
  files=$(git diff --name-only | \
    fzf --multi --preview 'git diff --color=always {}')
  [[ -n "$files" ]] && echo "$files" | xargs git checkout
}
```

### fadd：交互式 git add

```bash
# 交互式选择文件执行 git add
fadd() {
  local files
  files=$(git diff --name-only | \
    fzf --multi \
        --preview 'git diff --color=always {}' \
        --bind 'ctrl-a:select-all')
  [[ -n "$files" ]] && echo "$files" | xargs git add
  git status -s
}
```

### fshow：交互式查看 Git 提交

```bash
# 交互式浏览提交历史，预览 diff
fshow() {
  git log --graph --color=always \
      --format="%C(auto)%h%d %s %C(black)%C(bold)%cr" "$@" |
  fzf --ansi --no-sort --reverse --tiebreak=index \
      --bind "ctrl-m:execute:
                (grep -o '[a-f0-9]\{7\}' | head -1 |
                xargs -I % sh -c 'git show --color=always % | less -R') << 'FZF-EOF'
                {}
FZF-EOF"
}
```

### fstash：交互式 Git Stash 管理

```bash
# 查看 stash 列表，预览内容，弹出选中 stash
fstash() {
  local out q k sha
  while out=$(
    git stash list --pretty="%C(yellow)%h %>(14)%Cgreen%cr %C(blue)%gs" |
    fzf --ansi --no-sort --query="$q" --print-query \
        --expect=ctrl-d,ctrl-b \
        --preview 'git stash show --color=always -p $(echo {} | cut -d" " -f1)'
  ); do
    mapfile -t out <<< "$out"
    q="${out[0]}"
    k="${out[1]}"
    sha="${out[-1]}"
    sha="${sha%% *}"
    [[ -z "$sha" ]] && continue
    if [[ "$k" == 'ctrl-d' ]]; then
      git stash drop "$sha"
    elif [[ "$k" == 'ctrl-b' ]]; then
      git stash branch "stash-$sha" "$sha"
      break
    else
      git stash pop "$sha"
      break
    fi
  done
}
```

---

## 三、实时内容搜索（与 ripgrep 集成）

**AI 执行说明**: AI 会根据搜索需求自动构建 rg+fzf 联动命令

### 实时搜索文件内容

```bash
# 实时搜索文件内容，预览匹配行上下文
# 输入变化时自动重新执行 rg
rg_fzf() {
  fzf --ansi \
      --disabled \
      --query "" \
      --bind "start:reload:rg --line-number --no-heading --color=always --smart-case '' || true" \
      --bind "change:reload:rg --line-number --no-heading --color=always --smart-case {q} || true" \
      --delimiter : \
      --preview 'bat --color=always {1} --highlight-line {2}' \
      --preview-window 'up,60%,border-bottom,+{2}+3/3,~3' \
      --bind "enter:become(${EDITOR:-vim} {1} +{2})"
}
```

### 搜索并跳转到指定行

```bash
# 搜索内容，用 vim 打开并跳转到匹配行
rgf() {
  local result
  result=$(rg --line-number --no-heading --color=always "${1:-.}" |
    fzf --ansi \
        --delimiter : \
        --preview 'bat --color=always {1} --highlight-line {2}' \
        --preview-window 'right:50%,+{2}+3/3')
  if [[ -n "$result" ]]; then
    local file line
    file=$(echo "$result" | cut -d: -f1)
    line=$(echo "$result" | cut -d: -f2)
    ${EDITOR:-vim} "+$line" "$file"
  fi
}
```

---

## 四、Docker 工作流集成

**AI 执行说明**: AI 可生成 Docker + fzf 的便捷函数

### 进入容器

```bash
# 选择运行中的容器并进入
dexec() {
  local cid
  cid=$(docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}" |
    fzf --header-lines=1 \
        --preview 'docker inspect $(echo {} | awk "{print \$1}") | bat -l json --color=always' |
    awk '{print $1}')
  [[ -n "$cid" ]] && docker exec -it "$cid" "${1:-bash}"
}
```

### 查看容器日志

```bash
# 选择容器并实时查看日志
dlogs() {
  local cid
  cid=$(docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}" |
    fzf --header-lines=1 | awk '{print $1}')
  [[ -n "$cid" ]] && docker logs -f "$cid"
}
```

### 停止/删除容器

```bash
# 多选容器并停止
dstop() {
  docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}" |
    fzf --header-lines=1 --multi |
    awk '{print $1}' |
    xargs -r docker stop
}
```

---

## 五、高级界面定制

### 颜色主题配置

```bash
# Catppuccin Mocha 主题
export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS \
  --color=bg+:#313244,bg:#1e1e2e,spinner:#f5e0dc,hl:#f38ba8 \
  --color=fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc \
  --color=marker:#b4befe,fg+:#cdd6f4,prompt:#cba6f7,hl+:#f38ba8 \
  --color=selected-bg:#45475a"

# Dracula 主题
export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS \
  --color=fg:#f8f8f2,bg:#282a36,hl:#bd93f9 \
  --color=fg+:#f8f8f2,bg+:#44475a,hl+:#bd93f9 \
  --color=info:#ffb86c,prompt:#50fa7b,pointer:#ff79c6 \
  --color=marker:#ff79c6,spinner:#ffb86c,header:#6272a4"
```

### 高级键绑定

```bash
export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS \
  --bind='ctrl-a:select-all' \
  --bind='ctrl-d:deselect-all' \
  --bind='ctrl-/:toggle-preview' \
  --bind='ctrl-y:execute-silent(echo {} | pbcopy)+abort' \
  --bind='ctrl-e:execute(${EDITOR:-vim} {})' \
  --bind='alt-up:preview-page-up' \
  --bind='alt-down:preview-page-down'"
```

### 分隔符与字段选择

```bash
# 只显示第 2、3 字段，但传递完整行
# 适用于处理有结构的输入（如 CSV、日志）
echo -e "id:name:email\n1:alice:a@x.com\n2:bob:b@x.com" | \
  fzf --header-lines=1 \
      --delimiter=: \
      --with-nth=2,3

# 自定义显示字段（仅展示，不影响输出）
ps -ef | fzf --header-lines=1 --delimiter=' ' --with-nth=1,8..
```

---

## 六、在脚本中嵌入 fzf

**AI 执行说明**: AI 可根据脚本需求生成对应的 fzf 调用代码

### 返回值处理

```bash
#!/usr/bin/env bash
# 基础选择脚本
select_option() {
  local selected
  selected=$(printf '%s\n' "$@" | fzf --prompt="选择: " --height=10)
  if [[ $? -eq 0 && -n "$selected" ]]; then
    echo "$selected"
    return 0
  fi
  return 1
}

# 使用
choice=$(select_option "option1" "option2" "option3")
if [[ $? -eq 0 ]]; then
  echo "您选择了: $choice"
fi
```

### 批量处理选中文件

```bash
#!/usr/bin/env bash
# 选择多个文件并批量处理
process_files() {
  local files
  mapfile -t files < <(fzf --multi --preview 'cat {}')
  
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "未选择任何文件"
    return 1
  fi
  
  for file in "${files[@]}"; do
    echo "处理: $file"
    # 在此添加处理逻辑
  done
}
```

### 带确认的危险操作

```bash
#!/usr/bin/env bash
# 选择文件后二次确认再删除
safe_delete() {
  local files
  mapfile -t files < <(fzf --multi --prompt="选择要删除的文件: ")
  
  [[ ${#files[@]} -eq 0 ]] && return 0
  
  echo "将删除以下文件："
  printf '  %s\n' "${files[@]}"
  
  local confirm
  confirm=$(echo -e "取消\n确认删除" | fzf --prompt="操作: ")
  
  if [[ "$confirm" == "确认删除" ]]; then
    rm -v "${files[@]}"
  else
    echo "已取消"
  fi
}
```

---

## 七、fzf 与 tmux 集成

```bash
# 使用 fzf-tmux 在 tmux 弹出窗口中打开 fzf（需要 fzf 0.29+）
fzf-tmux -p 80%,80%

# 配置 CTRL-T 使用 tmux 弹出窗口
export FZF_TMUX_OPTS='-p80%,60%'
```

---

## 八、Vim/Neovim 集成

### 使用 fzf.vim 插件

```vim
" 安装（vim-plug 示例）
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" 常用命令
:Files          " 模糊查找文件
:GFiles         " git ls-files 查找
:Buffers        " 切换 Buffer
:Lines          " 搜索所有 Buffer 的行
:BLines         " 搜索当前 Buffer 的行
:Rg <pattern>   " 实时内容搜索
:History        " 最近文件/命令历史
:Maps           " 搜索快捷键
:Commands       " 搜索命令
```

---

## 完成确认

### 检查清单

- [ ] 已编写并测试至少 2 个自定义 fzf 函数
- [ ] Git 工作流中能使用 fzf 交互式选择
- [ ] 了解 rg + fzf 实时内容搜索用法
- [ ] 已配置颜色主题和高级键绑定
- [ ] 能在 Shell 脚本中正确嵌入 fzf 并处理返回值

### 参考资源

- [官方 Wiki 示例集合](https://github.com/junegunn/fzf/wiki/examples)
- [fzf.vim 插件文档](https://github.com/junegunn/fzf.vim)
- [awesome-fzf 精选列表](https://github.com/unixorn/fzf-zsh-plugin)
