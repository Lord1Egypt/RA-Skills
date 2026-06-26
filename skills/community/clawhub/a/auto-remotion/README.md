# auto-remotion

从已有录屏/产品演示视频生成官网宣传片的 AI Agent 工作流。

## 云端链接

- **GitHub**: https://github.com/16Miku/auto-remotion
- **ClawHub**: https://clawhub.ai/16miku/auto-remotion

## 核心能力

将 20 分钟录屏 → 60 秒官网宣传片，全流程覆盖：

```
环境准备 → 目标确认 → 素材识别（人工/自动）→ 分镜策划
→ 结构化规格 → Remotion 实现 → 字幕轨 → 中文配音 → BGM → 渲染出片
```

## 快速开始

### 安装 skill

```bash
# 方式一：openclaw（推荐）
openclaw skills install 16miku/auto-remotion

# 方式二：clawhub CLI
npx clawhub@latest install 16miku/auto-remotion
```

### 创建 Remotion 项目

```bash
npx create-video --yes --blank --no-tailwind my-video
cd my-video
npm install
npm run dev
```

然后在另一个终端启动 Claude Code：

```bash
claude
```

### 工作流执行

1. **阶段一**：明确目标与约束（输入/输出/时长）
2. **阶段二**：建立结构化中间产物（edit-script/storyboard/edit-spec）
3. **阶段三**：识别母视频时间点（人工或自动）
4. **阶段四**：Remotion 骨架搭建
5. **阶段五-七**：字幕、配音、BGM
6. **阶段八**：渲染出片

## 自动化视频理解（可选）

借鉴 [video-use](https://github.com/browser-use/video-use) 项目，支持自动化：

- **ElevenLabs Scribe** 转录 → 词级时间戳
- **takes_packed.md** → LLM 可读的 phrase 级转录文本
- **LLM 自动分镜** → 从转录文本生成 storyboard.json

## 目录结构

```
auto-remotion-dev/
├── SKILL.md              ← 主 skill 文档
├── README.md             ← 本文档
├── evals/                ← 测试评估
│   ├── evals.json        ← 测试用例
│   └── iteration-1/      ← 评估结果
└── .gitignore
```

## 参考项目

本 skill 借鉴吸收了以下开源项目：

| 项目 | 来源 | 借鉴内容 |
|------|------|---------|
| [video-use](https://github.com/browser-use/video-use) | browser-use | 两段式视频理解、自动分镜、Hard Rules |
| [remotion-video-toolkit](https://clawhub.ai/shreefentsar/remotion-video-toolkit) | ClawHub | Remotion API 技巧 |
| [remotion-best-practices](https://www.remotion.dev/docs/ai/skills) | Remotion 官方 | Remotion 最佳实践 |

## 参考链接

- [Remotion 官网](https://www.remotion.dev/)
- [Remotion + Claude Code](https://www.remotion.dev/docs/ai/claude-code)
- [Remotion Skills](https://www.remotion.dev/docs/ai/skills)

## License

MIT
