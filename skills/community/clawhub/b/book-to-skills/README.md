# "电子书拆解成技能包" · WorkBuddy Skill

"This skill should be used when the user provides an electronic book (PDF, EPUB, TXT, MD) and wants to automatically extract knowledge, analyze structure, and generate multiple WorkBuddy skills. Trigger phrases: 拆解这本书, 从这本书提取技能, 把这本书变成技能, 生成技能包, book to skills. Supports three modes: Knowledge Base, Action Guide, Hybrid."

## 特性

- 请参考 SKILL.md 中的详细说明

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「"电子书拆解成技能包"」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/workbuddy-book-to-skills.git \
  ~/.workbuddy/skills/book-to-skills
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 path/to/skill-creator/scripts/package_skill.py \
  ~/.workbuddy/skills/{skill-name} \
  ~/workbuddy-output/{YYYY-MM-DD}-book-to-skills/{book-slug}/
```

## 输出

请参考 SKILL.md

## 项目结构

```
.gitignore
LICENSE
SKILL.md
references
scripts
scripts/extract_epub.py
scripts/extract_pdf.py
```

## 作者

**guipi888**



## License

MIT License — 详见 [LICENSE](./LICENSE)
