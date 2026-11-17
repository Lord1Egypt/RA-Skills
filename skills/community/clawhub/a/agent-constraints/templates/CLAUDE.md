@AGENTS.md

<!-- 本文件只做两件事：导入 AGENTS.md，以及承载 Claude Code 专属指令。
     不要在这里重复 AGENTS.md 的任何内容——重复是冲突指令的主要来源，
     而两条规则矛盾时模型可能任意挑一条。

     没有 Claude 专属内容时，删掉下面整节，或直接改用软链：
       ln -s AGENTS.md CLAUDE.md
     （Windows 需管理员权限或开发者模式，用上面的 @ 导入更稳。）

     验证是否加载：会话里跑 /context，看 Memory files 一栏。 -->

## Claude Code 专属

- <例如：`src/billing/` 下的改动先用 plan mode>
