# git post-commit hook（ctx-lockstep）

由 ctx-lockstep init 脚本追加到项目 `.git/hooks/post-commit`。
作用：每次 commit 后机械追加一行 JSON 到 `<项目>/.ctx-lockstep/commits.log`，不经过任何 LLM。
固化时清空 commits.log，log 中的积压行数即"未固化的提交数"。

标记符 `# >>> ctx-lockstep >>>` / `# <<< ctx-lockstep <<<` 用于幂等安装与卸载。

## 内容

```sh
# >>> ctx-lockstep >>>
{
  _cl_root="$(git rev-parse --show-toplevel 2>/dev/null)" &&
  printf '{"commit":"%s","date":"%s","subject":"%s"}\n' \
    "$(git rev-parse --short HEAD)" \
    "$(date '+%Y-%m-%d %H:%M')" \
    "$(git log -1 --pretty=%s)" \
    >> "$_cl_root/.ctx-lockstep/commits.log"
} 2>/dev/null
# <<< ctx-lockstep <<<
```

## 注意

- 失败静默（`2>/dev/null`）：hook 绝不能阻断用户提交
- 若项目已有自己的 post-commit hook，只追加标记块，不覆盖
