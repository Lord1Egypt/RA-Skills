# D2 Diagram Creator

D2 Diagram Creator is a skill that can directly convert natural language descriptions into high-quality D2 diagram code and image files. After installation, you only need to describe the desired diagram structure in text, and it will automatically generate it for you.

Whether it's a flowchart in academic writing, a model architecture diagram in scientific illustration, or a module relationship diagram when understanding a new open-source project, you no longer need to draw it manually step by step.

[中文版本(Chinese version)](README_zh.md)

![](https://oss.furina.org.cn:443/images/github/20260402160052535.svg)

## Quick Use

### Dependency Installation

The recommended and simplest installation method is to use D2's installation script, which will detect your operating system and architecture and use the best installation method.

```bash
curl -fsSL https://d2lang.com/install.sh | sh -s --

# TALA is a powerful diagram layout engine specifically designed for software architecture diagrams. It requires separate installation.
curl -fsSL https://d2lang.com/install.sh | sh -s -- --tala
```

Please refer to the official D2 documentation for details:

+ https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md

+ https://github.com/terrastruct/tala

After successful installation, use the following command to check

```bash
d2 --version
d2 layout tala
```

### Import Claude Code

```bash
git clone https://github.com/HuTa0kj/d2-diagram-creator ~/.claude/skills/d2-diagram-creator
```

## Example Prompts

+ Please use D2 to draw the system flowchart for the current project.

+ Please use D2 SKILL to draw a TCP three-way handshake sequence diagram.

+ Please use D2 to draw the database ER diagram for the current project, in dark mode and a thatched cottage style, and export it as a PNG.
