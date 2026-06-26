# D2 Diagram Creator



D2 Diagram Creator 是一个能将自然语言描述直接转换为高质量 D2 图表代码及图片文件的 SKILL。安装后，你只需用文字描述想要的图表结构，它就能帮你自动生成。

无论是论文写作中的方法流程图、科研绘图里的模型架构示意，还是理解一个新的开源项目时的模块关系图，你都不需要再一点一点手动绘制。



![](https://oss.furina.org.cn:443/images/github/20260402160052535.svg)

## 快速使用

### 依赖安装

推荐且最简单的安装方法是使用 D2 的安装脚本，该脚本将检测您使用的操作系统和架构，并使用最佳安装方法

```bash
curl -fsSL https://d2lang.com/install.sh | sh -s --

# TALA 是一款专为软件架构图设计的图表布局引擎，非常强大，该引擎需要单独安装
curl -fsSL https://d2lang.com/install.sh | sh -s -- --tala
```

具体请参考 D2 的官方文档：

+ https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md
+ https://github.com/terrastruct/tala

安装成功后使用下面的命令检查

```bash
d2 --version
d2 layout tala
```

### 导入 Claude Code

```bash
git clone https://github.com/HuTa0kj/d2-diagram-creator ~/.claude/skills/d2-diagram-creator
```

## 示例提示词

+ 帮我使用 D2 绘制当前项目的系统流程图
+ 使用 D2 SKILL 帮我画一个 TCP 三次握手的时序图

+ 使用 D2 绘制当前项目的数据库ER图，深色模式、草屋风格，导出PNG