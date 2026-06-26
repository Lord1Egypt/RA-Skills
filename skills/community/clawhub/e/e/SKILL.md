---
name: e
description: Short alias skill for editing files, code, or configurations. Use when you need to make changes to existing content using text editors or IDE shortcuts.
---

# e (Edit)

用于编辑文件、代码或配置的简写技能。快速打开和修改文本，支持 vim、nano、VS Code 等编辑器。

---

## 适用场景

当你说：
- "打开这个文件改一下"
- "帮我快速修个配置"
- "在 VS Code 里定位到这一行"
- "命令行里随便找个编辑器改下就行"

就应该触发 `e` —— **选择合适的编辑方式，把改动控制在安全范围内**。

---

## 编辑器选择速查

**命令行编辑器**

```bash
vim file.txt      # 功能最全，学习曲线陡，但一旦熟练非常高效
nano file.txt     # 上手简单，终端环境下修改小文件首选
vi file.txt       # 兼容模式（许多系统默认提供）
```

**图形/IDE 编辑器**

```bash
code file.txt     # VS Code 打开文件
code .            # 在 VS Code 中打开当前项目
```

在 Windows PowerShell 下：

```powershell
code .\src\app.tsx
notepad .\config.json
```

---

## 安全编辑配置文件

**修改前先备份**

```bash
cp config.yml config.yml.bak          # 复制备份
e config.yml                          # 打开编辑
```

**修改后做语法/格式校验**

```bash
yamllint config.yml                   # YAML 检查
jq . config.json > /dev/null          # JSON 格式检查
nginx -t                              # 检查 Nginx 配置
```

> 原则：**任何会影响服务启动的配置文件，编辑后都要先本地验证，再重启服务。**

---

## 常见编辑操作模式

**在终端中做小改动（nano 风格）**

- 移动光标到要修改的行
- 直接输入/删除文本
- `Ctrl + O` 保存，`Ctrl + X` 退出（nano）

**在 vim 里“只改一点”最小路线**

```text
vim file.txt
  ↓
使用方向键 / j k 在行间移动
按 i 进入插入模式，修改文本
按 Esc 退出插入模式
输入 :wq 回车 保存并退出
```

**在 VS Code 中**

- `Ctrl + P`：快速打开文件
- `Ctrl + G`：跳转到指定行号
- `Ctrl + F`：查找
- `Ctrl + H`：替换

---

## 批量替换与谨慎操作

**命令行替换（sed 示例）**

```bash
# 在文件中把 foo 替换为 bar（单文件）
sed -i 's/foo/bar/g' file.txt          # Linux
sed -i '' 's/foo/bar/g' file.txt       # macOS BSD sed

# 替换前做一份备份
sed -i.bak 's/foo/bar/g' file.txt
```

**多文件批量替换的安全流程**

```bash
rg "oldValue" .                      # 先用 ripgrep 找到所有匹配
rg "oldValue" -n config/            # 缩小范围只看配置目录

# 再结合编辑器批量操作，而不是盲目一键 sed 整仓库
```

---

## 与版本控制配合

**编辑前后用 Git 把握改动边界**

```bash
git diff                   # 看看目前有多少改动
e src/main.ts              # 编辑文件
git diff src/main.ts       # 查看本次编辑的具体差异
```

**改坏了，立刻“撤稿”**

```bash
git restore src/main.ts    # 丢弃该文件的本次修改
git restore .              # 丢弃工作区所有修改
```

> `e` 和 `g`（git）配合使用，可以形成一个安全的“编辑—检查—提交”闭环。

---

## 编辑大文件 / 日志的策略

对于几百 MB 的大日志或数据文件，不要用 GUI 直接打开：

```bash
head -n 200 huge.log       # 只看前 200 行
tail -n 200 huge.log       # 只看最后 200 行
rg "ERROR" huge.log        # 只查包含 ERROR 的行
```

如果必须编辑：

- 先用脚本提取出一小段到临时文件，编辑临时文件
- 再用工具合并或重放，而不是在原始大文件上直接动刀

---

## 心态与习惯

`e` 代表的是一种**可控编辑**的习惯：

- 改前：知道自己在改什么（配合 `l`、`f`、`i` 看清上下文）
- 改时：小步修改、小步保存
- 改后：立刻用 `git diff` 或工具查看改动是否符合预期

---

> `e` 的关键词是：**精确、可回滚、可验证**。任何无法解释清楚的“神秘修改”，都不应该被提交进仓库。
