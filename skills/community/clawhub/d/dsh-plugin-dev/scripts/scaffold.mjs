#!/usr/bin/env node
/**
 * DSH 插件骨架生成器（零依赖，Node >= 18）
 *
 * 用法：
 *   node scaffold.mjs --dir <目标目录> --id <插件id> [--pkg <npm包名>] [--scope <npm账号>] [--tool <工具名>] [--force]
 *
 * 产出纯 ESM JS 骨架（免构建、免 prepare 授权，npm 可直发）：
 *   package.json（含 dsh.bundle manifest） / cordis.patch.yml / index.js / README.md
 *   .github/workflows/publish.yml / .gitignore
 *
 * 退出码：0 成功；1 参数或文件错误（不覆盖已有文件，除非 --force）
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

// ---------- 参数解析 ----------
const args = process.argv.slice(2)
const opts = {}
for (let i = 0; i < args.length; i++) {
  const a = args[i]
  if (a === '--force') opts.force = true
  else if (a.startsWith('--')) { opts[a.slice(2)] = args[i + 1]; i++ }
}

function die(msg) {
  console.error(`[scaffold] FAIL: ${msg}`)
  console.error('用法: node scaffold.mjs --dir <目标目录> --id <插件id> [--pkg <包名>] [--scope <npm账号>] [--tool <工具名>] [--force]')
  process.exitCode = 1
}

function main() {
if (!opts.dir || !opts.id) return die('缺少 --dir 或 --id')
if (!/^[a-z][a-z0-9-]*$/.test(opts.id)) return die(`插件 id "${opts.id}" 不合法：须为小写字母开头的小写连字符串`)

const tool = opts.tool || 'hello'
const pkg = opts.pkg || (opts.scope ? `@${opts.scope}/dsh-${opts.id}` : `dsh-${opts.id}`)
if (!/^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/.test(pkg)) return die(`包名 "${pkg}" 不是合法 npm 包名`)

const dir = path.resolve(opts.dir)
if (fs.existsSync(dir) && fs.readdirSync(dir).length > 0 && !opts.force) {
  return die(`目录 ${dir} 非空；确认覆盖请加 --force`)
}
fs.mkdirSync(dir, { recursive: true })

// ---------- 文件内容 ----------
const quotedName = pkg.startsWith('@') ? `'${pkg}'` : pkg // @ 开头的 YAML 纯标量非法，必须加引号

const files = {
  'package.json': JSON.stringify({
    name: pkg,
    version: '0.1.0',
    description: `TODO: 一句话说明本插件用途（收录审查要求描述与代码一致）`,
    type: 'module',
    main: 'index.js',
    files: ['index.js', 'cordis.patch.yml', 'README.md'],
    keywords: ['dsh-plugin', 'deepseek-harness', 'cordis'],
    license: 'MIT',
    peerDependencies: { '@deepseek-ai/dsh-tools': '*' },
    peerDependenciesMeta: { '@deepseek-ai/dsh-tools': { optional: true } },
    dsh: { bundle: { patch: './cordis.patch.yml' } },
  }, null, 2) + '\n',

  'cordis.patch.yml': `# bundle 层：被 dsh plugin add 安装时激活
# name 必须写包名（Node 模块解析），不是源码路径
- insert:
    - id: ${opts.id}
      name: ${quotedName}
`,

  'index.js': `// ${pkg} — DeepSeek Harness (DSH) 插件
// 文档: https://deepseek-harness.github.io/deepseek-harness/develop/basic/
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = '${opts.id}'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: '${tool}',
    description: 'TODO: 一句话说明工具用途（会展示给模型）',
    parameters: {
      input: { type: 'string', required: true, description: 'TODO: 参数说明' },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      // TODO: 换成真实实现
      return \`echo: \${args.input}\`
    },
  }))
}
`,

  'README.md': `# ${pkg}

TODO: 一句话说明插件做什么（收录审查硬要求：描述与代码一致——声称几个工具就得有几个）。

## 安装

\`\`\`bash
# npm（推荐）
dsh plugin --profile <你的profile> add ${quotedName}

# GitHub 仓库（纯 JS 免构建授权）
dsh plugin --profile <你的profile> add github:<owner>/<repo>

# tarball
dsh plugin --profile <你的profile> add ./${pkg}-0.1.0.tgz
\`\`\`

## 使用

对模型说：\`Use the ${tool} tool ...\`

## 发布

推 tag 即自动发布（需先配置 NPM_TOKEN，见 .github/workflows/publish.yml）：

\`\`\`bash
npm version patch && git push --follow-tags
\`\`\`
`,

  '.github/workflows/publish.yml': `name: publish

on:
  push:
    tags: ['v*']
  workflow_dispatch:
    inputs:
      publish:
        description: 'Publish to npm (false = dry-run pack only)'
        type: boolean
        default: false

jobs:
  pack:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Verify tag matches package version
        if: startsWith(github.ref, 'refs/tags/')
        run: node -e "const p=require('./package.json');const t=process.env.GITHUB_REF_NAME.slice(1);if(p.version!==t){console.error('tag v'+t+' != package.json version '+p.version);process.exit(1)}"
      - name: Pack
        run: npm pack
      - uses: actions/upload-artifact@v4
        with:
          name: tarball
          path: ./*.tgz

  publish:
    needs: pack
    if: startsWith(github.ref, 'refs/tags/') || (github.event_name == 'workflow_dispatch' && inputs.publish)
    runs-on: ubuntu-latest
    environment: npm-publish
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: tarball
      - name: Publish to npm
        run: npm publish ./*.tgz --provenance --access public
        env:
          NODE_AUTH_TOKEN: \${{ secrets.NPM_TOKEN }}

  release:
    needs: pack
    if: startsWith(github.ref, 'refs/tags/')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: tarball
      - uses: softprops/action-gh-release@v2
        with:
          files: ./*.tgz
`,

  '.gitignore': `node_modules/
*.tgz
`,
}

// ---------- 写盘 ----------
const written = []
for (const [rel, content] of Object.entries(files)) {
  const fp = path.join(dir, rel)
  fs.mkdirSync(path.dirname(fp), { recursive: true })
  fs.writeFileSync(fp, content, 'utf8')
  written.push(rel)
}

console.log(`[scaffold] PASS: 已生成 ${pkg} 骨架 → ${dir}`)
for (const rel of written) console.log(`  + ${rel}`)
console.log(`下一步:
  1. 编辑 index.js 实现真实工具逻辑；README/package.json 的 description 去掉 TODO
  2. 自检: node ${path.join(path.dirname(fileURLToPath(import.meta.url)), 'check-plugin.mjs')} "${dir}"
  3. npm pack 本地验证 → npm publish → PR 收录 awesome-dsh-plugin`)
}

main()
