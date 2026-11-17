# dsh-my-bundle

零代码组合包骨架（T1 形态）。**不包含任何 JavaScript** —— 全部行为由 `cordis.patch.yml` 描述。

## 复制后要改的地方

| 文件 | 改什么 |
|---|---|
| `package.json` | `name`、`version`、`description`、`keywords`，以及补上 `repository` |
| `cordis.patch.yml` | 换成你真正要挂载的能力（示例行删掉） |
| `README.md` | 这份说明 |

## 五条容易致命的规则

1. **`dsh.bundle.patch` 不能少。** 少了它，`dsh plugin add` 会打一条 `declares no dsh.bundle` 警告，然后**什么都不做** —— 这是新手最常见的「我明明装了啊」。
2. **`files` 里必须包含 `cordis.patch.yml`。** 漏了它，发布后补丁文件不会进 npm 包，装上有警告、功能全无。
3. **`exports` 要显式声明 `'./cordis.patch.yml'` 与 `'./package.json'`。** 本包是零代码组合包，**没有 JS 入口，所以不要加 `'.'`**（没有可指向的文件）。官方 6 个 bundle 包全部带 `'.'`、`'./cordis.patch.yml'`、`'./package.json'`，部分还有 `'./src/*'`；组合包取与本包实际路径相符的那两个即可，与官方约定保持一致。
4. **`id` 全局唯一。** ⚠️ 0.1.6-alpha.1 起重复 `id` **不再报错**，而是同 id 两行互相覆盖（后者胜，静默生效）；`--dump-config` 里两行都在，但只有一行真的起作用。
5. **`config` 是整段替换，不是深合并。** 后续层覆盖某一行时，必须把整个 `config` 重述一遍。

## 显示元数据与图标（`0.2.1-alpha.1` 起的官方检查清单）

Plugin Manager 与 Settings 会**在不激活插件的前提下**直接读 `locale/*.json` 里的 `meta.title` / `meta.description` 与 `./icon`。零代码组合包**同样适用**（官方 `SKILL.md`：「This applies to Host-only and configuration-only bundles too」）。缺字段会**优雅回落**到 `package.json` 的 `name` / `description`、缺图用面板默认美术 —— 这不是硬报错，但**要让插件在列表里可辨识、好看，就得补上**：

1. 建 `locale/en.json`（以及用户语言的 `locale/zh.json`）：`{"meta":{"title":"…","description":"…"}}`，**别留与本插件无关的模板文案**。
2. 放一枚图标：原创，或许可允许再分发的素材并保留署名；格式 SVG / PNG / JPEG / WebP，**≤ 256 KiB**，且必须留在包内。
3. `exports` 补 `"./locale/*.json"` 与 `"./icon"`；`files` 是**白名单**，新增模块或资源**必须同步补进去**，否则不进包。

完整清单与「怎么验」（含无浏览器控制时**不得声称视觉通过**）：`references/02b-official-templates.md` §「显示元数据与图标」。

## 安全使用（含 MCP 示例，必读）

`cordis.patch.yml` 里的 MCP 示例会**在 DSH 启动时下载并执行外部包** —— 这是这份骨架里唯一有真实安全含义的地方。三条硬要求：

1. **版本必须写精确号。** 写 `my-mcp-server@1.2.3`，不要写 `my-mcp-server` / `latest` / `^1` / `~1.x`。
   浮动规格意味着「每次启动跑的都是当时的线上最新版」—— 这份配置被审阅之后，实际执行的代码**仍然可以变**。上游被攻陷、发布恶意新版本、形近包抢注，都会直接落到本机。
2. **凭据只列真正需要的那一把，并优先用低配额、可随时撤销的专用 key。**
   子进程以与 DSH 相同的权限运行：能读写文件、能发网络请求，也能读到 `env:` 里列出的**每一个**凭据。
3. **拿不准就先别开。** `failOnStartupError: false` 已经保证依赖没装好时不会拖垮整个 DSH —— 可以先注释掉这一行把插件装起来，确认其它部分正常后，再单独处理这个集成。

> 更稳的做法：把「下载」与「执行」分成两步 —— 先在独立步骤里显式安装（并审阅解析出的依赖树），再让补丁的 `command:` 指向本地已安装的可执行文件。这样「包里到底跑了什么」在运行前就是确定的。

## 安装

```bash
# 本地目录
dsh plugin --profile <profile 名> add ./minimal-bundle

# 已发布到 npm
dsh plugin --profile <profile 名> add dsh-my-bundle
```

`--profile` 是**必填**参数。

## 验证

```bash
dsh plugin --profile <profile 名> ls
dsh --dump-config          # 打印组装后的配置树，不启动就能检查补丁是否生效
```

## 参考

- 完整模板与逐行讲解：`references/02-templates.md` 的 T1、T2
- 补丁语法与 `!!js` 求值范围：同上 T2
- 踩坑百科：`references/05-pitfalls.md`
- 真实范本：`Q00/ouroboros → integrations/dsh-plugin/`（官方精选清单里唯一的纯配置零代码插件）
